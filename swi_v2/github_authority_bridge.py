"""GitHub operations for SWI, delegated to the existing authority boundary.

Read operations use Git and GitHub CLI without changing repository state.
Operations that change refs or publish require an exact, in-process SWI
authorization record. This module is an integration client, not an identity
provider or a replacement for the Python governing spine.
"""
from __future__ import annotations

import json
import argparse
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
from urllib.parse import urlparse

from swi_v2.kernel.authority import require_authorization_for_action


class BridgeError(RuntimeError):
    """Operation could not be completed safely."""


class AuthorizationRequired(BridgeError):
    """The SWI authority boundary denied a consequential operation."""


@dataclass(frozen=True)
class GitHubRepository:
    owner: str
    name: str

    @property
    def slug(self) -> str:
        return f"{self.owner}/{self.name}"


@dataclass(frozen=True)
class HumanApproval:
    """Approval input passed from an SWI authority caller.

    The record is scope-bound but is not itself cryptographic proof. A caller
    must obtain it from the real SWI human-authority workflow.
    """

    approval_id: str
    approved_by: str
    repository: str
    action: str
    target: str
    human_approved: bool
    evidence_ref: str


@dataclass(frozen=True)
class OperationEvidence:
    operation: str
    repository: str
    result: str
    details: Mapping[str, Any]
    authorization_id: str | None = None
    authorization_source: str = "READ_ONLY"


def parse_github_remote(remote_url: str) -> GitHubRepository:
    """Parse public GitHub HTTPS/SSH remotes without returning credentials."""
    value = remote_url.strip()
    if value.startswith("git@github.com:"):
        path = value.removeprefix("git@github.com:")
    else:
        parsed = urlparse(value)
        if parsed.hostname and parsed.hostname.lower() != "github.com":
            raise BridgeError("remote host is not github.com")
        if parsed.scheme not in {"https", "ssh"} or parsed.hostname is None:
            raise BridgeError("unsupported GitHub remote format")
        path = parsed.path.lstrip("/")
    path = path.removesuffix(".git").strip("/")
    parts = path.split("/")
    if len(parts) != 2 or not all(re.fullmatch(r"[A-Za-z0-9_.-]+", p) for p in parts):
        raise BridgeError("remote must identify exactly owner/repository")
    return GitHubRepository(*parts)


def _run(args: Sequence[str], *, cwd: Path | None = None) -> str:
    """Run an argument-vector command; never invoke a shell or print secrets."""
    try:
        result = subprocess.run(
            list(args), cwd=cwd, text=True, capture_output=True, check=False
        )
    except OSError as exc:
        raise BridgeError(f"could not run {args[0]}: {exc}") from exc
    if result.returncode:
        # GitHub CLI and Git stderr can include a remote URL; omit it from errors.
        safe_stderr = re.sub(r"https?://[^\s]+", "[remote URL]", result.stderr.strip())
        raise BridgeError(f"{args[0]} exited {result.returncode}: {safe_stderr[:500]}")
    return result.stdout.strip()


class GitHubAuthorityBridge:
    """Local Git/GitHub client whose writes go through SWI authorization."""

    def __init__(
        self,
        repository_path: str | Path,
        *,
        runner: Callable[..., str] = _run,
        approval_verifier: Callable[[HumanApproval], bool] | None = None,
    ) -> None:
        self.path = Path(repository_path).resolve()
        if not self.path.is_dir():
            raise BridgeError("repository path does not exist")
        self._run = runner
        self._approval_verifier = approval_verifier

    def _git(self, *args: str) -> str:
        return self._run(("git", *args), cwd=self.path)

    def repository(self, remote: str = "origin") -> GitHubRepository:
        value = self._git("remote", "get-url", remote)
        return parse_github_remote(value)

    def _authorize(
        self, *, action: str, target: str, approval: HumanApproval | None,
        repository: str | None = None,
    ) -> HumanApproval:
        repository = repository or self.repository().slug
        if approval is None:
            raise AuthorizationRequired(f"SWI authorization required for {action}")
        if self._approval_verifier is None:
            raise AuthorizationRequired("no trusted SWI approval verifier is configured")
        if not self._approval_verifier(approval):
            raise AuthorizationRequired("SWI approval evidence failed validation")
        if not all((approval.approval_id, approval.approved_by, approval.evidence_ref)):
            raise AuthorizationRequired("approval record is incomplete")
        if (
            not approval.human_approved
            or approval.repository.lower() != repository.lower()
            or approval.action != action
            or approval.target != target
        ):
            raise AuthorizationRequired("approval does not bind this exact operation")
        try:
            require_authorization_for_action(
                authorization_present=approval.human_approved,
                authorization_scope=f"github:{repository}:{action}:{target}",
                requested_action=f"github:{repository}:{action}:{target}",
                declared_scopes=(f"github:{repository}:{action}:{target}",),
                evidence=asdict(approval),
            )
        except Exception as exc:
            raise AuthorizationRequired(str(exc)) from exc
        return approval

    def inspect(self) -> OperationEvidence:
        repository = self.repository().slug
        status = self._git("status", "--porcelain=v1", "--untracked-files=all")
        details = {
            "repository": repository,
            "branch": self._git("branch", "--show-current") or None,
            "head": self._git("rev-parse", "HEAD"),
            "upstream": self._optional_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"),
            "status": status.splitlines(),
        }
        return OperationEvidence("inspect", repository, "INSPECTED", details)

    def _optional_git(self, *args: str) -> str | None:
        try:
            return self._git(*args) or None
        except BridgeError:
            return None

    def authenticated_account(self) -> OperationEvidence:
        login = self._run(("gh", "api", "user", "--jq", ".login"))
        return OperationEvidence(
            "github_account", self.repository().slug, "AUTHENTICATED", {"login": login}
        )

    def compare(self, base: str, head: str) -> OperationEvidence:
        repository = self.repository().slug
        counts = self._git("rev-list", "--left-right", "--count", f"{base}...{head}")
        diffstat = self._git("diff", "--stat", f"{base}...{head}")
        left, right = (int(part) for part in counts.split())
        return OperationEvidence(
            "compare", repository, "COMPARED",
            {"base": base, "head": head, "base_only_commits": left,
             "head_only_commits": right, "diffstat": diffstat,
             "comparison_source": "LOCAL_GIT_REFS",
             "remote_freshness": "NOT_CHECKED"},
        )

    def verify_commit(self, revision: str) -> OperationEvidence:
        repository = self.repository().slug
        commit = self._git("rev-parse", "--verify", f"{revision}^{{commit}}")
        signature = subprocess.run(
            ["git", "verify-commit", commit], cwd=self.path,
            text=True, capture_output=True, check=False,
        )
        signature_status = "SIGNATURE_VALID" if signature.returncode == 0 else "UNVERIFIED"
        github_status: dict[str, Any] = {"verified": None, "reason": "API_NOT_CHECKED"}
        try:
            raw = self._run(("gh", "api", f"repos/{repository}/commits/{commit}",
                             "--jq", ".commit.verification"))
            verified = json.loads(raw)
            github_status = {
                "verified": verified.get("verified"),
                "reason": verified.get("reason"),
            }
        except BridgeError:
            # Local signature status remains separate from GitHub API evidence.
            pass
        return OperationEvidence(
            "verify_commit", repository, "OBJECT_PRESENT",
            {"commit": commit, "signature": signature_status,
             "signature_detail": signature.stderr.strip()[:300],
             "github_verification": github_status},
        )

    def inspect_releases(self, limit: int = 10) -> OperationEvidence:
        if not 1 <= limit <= 100:
            raise BridgeError("release limit must be between 1 and 100")
        repository = self.repository().slug
        raw = self._run(("gh", "release", "list", "--repo", repository,
                         "--limit", str(limit), "--json", "tagName,name,isDraft,isPrerelease,publishedAt"))
        return OperationEvidence("inspect_releases", repository, "INSPECTED", {"releases": json.loads(raw)})

    def prepare_pull_request(self, base: str, head: str, title: str) -> OperationEvidence:
        if not title.strip() or "\n" in title:
            raise BridgeError("pull request title must be a single non-empty line")
        comparison = self.compare(base, head)
        details = {
            "base": base, "head": head, "title": title.strip(),
            "body": (f"## SWI verification\n\n"
                     f"- Source branch: `{head}`\n- Target branch: `{base}`\n"
                     f"- Comparison commits: {comparison.details['head_only_commits']} ahead, "
                     f"{comparison.details['base_only_commits']} behind\n"
                     "- SWI test evidence: attach the exact report and command output.\n"
                     "- Authority state: awaiting human review; no publication performed."),
            "diffstat": comparison.details["diffstat"],
        }
        return OperationEvidence("prepare_pull_request", self.repository().slug, "PREPARED_NOT_PUBLISHED", details)

    def fetch(self, remote: str, approval: HumanApproval | None) -> OperationEvidence:
        remote_repository = parse_github_remote(self._git("remote", "get-url", remote)).slug
        target = f"remote={remote};no-tags=true"
        authorization = self._authorize(action="fetch", target=target, approval=approval,
                                        repository=remote_repository)
        if parse_github_remote(self._git("remote", "get-url", remote)).slug != remote_repository:
            raise BridgeError("remote changed after authorization; fetch halted")
        self._git("fetch", "--no-tags", "--", remote)
        return OperationEvidence("fetch", self.repository().slug, "FETCHED",
                                 {"remote": remote, "tags_changed": False},
                                 authorization.approval_id, "SWI_AUTHORITY_BOUND")

    def clone(
        self, remote_url: str, destination: str | Path,
        approval: HumanApproval | None,
    ) -> OperationEvidence:
        repository = parse_github_remote(remote_url)
        dest = Path(destination).expanduser().resolve()
        target = f"remote={repository.slug};destination={dest}"
        authorization = self._authorize(action="clone", target=target, approval=approval,
                                        repository=repository.slug)
        if dest.exists():
            raise BridgeError("clone destination already exists; refusing to overwrite")
        self._run(("git", "clone", "--", remote_url, str(dest)))
        return OperationEvidence("clone", repository.slug, "CLONED", {"destination": str(dest)},
                                 authorization.approval_id, "SWI_AUTHORITY_BOUND")

    def push(self, remote: str, branch: str, approval: HumanApproval | None) -> OperationEvidence:
        if branch.startswith("-") or not branch:
            raise BridgeError("invalid branch name")
        self._git("check-ref-format", "--branch", branch)
        remote_repository = parse_github_remote(self._git("remote", "get-url", remote)).slug
        head = self._git("rev-parse", "HEAD")
        target = f"remote={remote};branch={branch};head={head};force=false"
        authorization = self._authorize(action="push", target=target, approval=approval,
                                        repository=remote_repository)
        if self._git("rev-parse", "HEAD") != head:
            raise BridgeError("HEAD changed after authorization; push halted")
        if parse_github_remote(self._git("remote", "get-url", remote)).slug != remote_repository:
            raise BridgeError("remote changed after authorization; push halted")
        self._git("push", "--", remote, f"HEAD:refs/heads/{branch}")
        return OperationEvidence("push", self.repository().slug, "PUSHED", {"remote": remote, "branch": branch},
                                 authorization.approval_id, "SWI_AUTHORITY_BOUND")

    def commit(self, message: str, approval: HumanApproval | None) -> OperationEvidence:
        if not message.strip() or "\n" in message:
            raise BridgeError("commit message must be a single non-empty line")
        staged_digest = self._staged_patch_digest()
        head = self._git("rev-parse", "HEAD")
        target = f"parent={head};staged_patch_sha256={staged_digest};message={message}"
        authorization = self._authorize(action="commit", target=target, approval=approval)
        if self._git("rev-parse", "HEAD") != head or self._staged_patch_digest() != staged_digest:
            raise BridgeError("HEAD or staged patch changed after authorization; commit halted")
        commit = self._git("commit", "-m", message)
        return OperationEvidence("commit", self.repository().slug, "COMMITTED",
                                 {"commit_output": commit, "parent_before": head,
                                  "staged_patch_sha256": staged_digest},
                                 authorization.approval_id, "SWI_AUTHORITY_BOUND")

    def _staged_patch_digest(self) -> str:
        import hashlib
        staged = subprocess.run(["git", "diff", "--cached", "--binary"], cwd=self.path,
                                text=False, capture_output=True, check=False)
        if staged.returncode:
            raise BridgeError("could not inspect the staged patch")
        return hashlib.sha256(staged.stdout).hexdigest()

    def create_release(
        self, tag: str, title: str, notes_file: str | Path,
        approval: HumanApproval | None,
    ) -> OperationEvidence:
        if not re.fullmatch(r"[A-Za-z0-9._/-]+", tag) or tag.startswith("-"):
            raise BridgeError("invalid release tag")
        repository = self.repository().slug
        notes = Path(notes_file).resolve()
        head = self._git("rev-parse", "HEAD")
        notes_digest = _sha256_file(notes)
        tag_ref = f"refs/tags/{tag}"
        existing_tag = self._optional_git("rev-parse", "--verify", f"{tag_ref}^{{commit}}")
        if existing_tag and existing_tag != head:
            raise BridgeError("release tag points to a different commit")
        target = f"tag={tag};head={head};title={title};notes_sha256={notes_digest}"
        authorization = self._authorize(action="release", target=target, approval=approval)
        if self._git("rev-parse", "HEAD") != head or _sha256_file(notes) != notes_digest:
            raise BridgeError("HEAD or release notes changed after authorization; release halted")
        current_tag = self._optional_git("rev-parse", "--verify", f"{tag_ref}^{{commit}}")
        if current_tag and current_tag != head:
            raise BridgeError("release tag changed after authorization; release halted")
        url = self._run(("gh", "release", "create", tag, "--repo", repository,
                         "--target", head, "--title", title, "--notes-file", str(notes)))
        return OperationEvidence("create_release", repository, "PUBLISHED",
                                 {"url": url, "tag": tag, "target_commit": head},
                                 authorization.approval_id, "SWI_AUTHORITY_BOUND")


def _sha256_file(path: Path) -> str:
    import hashlib
    if not path.is_file():
        raise BridgeError("release notes file does not exist")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence_json(evidence: OperationEvidence) -> str:
    """Stable JSON serialization suitable for a caller's evidence report."""
    return json.dumps(asdict(evidence), sort_keys=True, indent=2)


def _approval(path: str | None) -> HumanApproval | None:
    if path is None:
        return None
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
        return HumanApproval(**value)
    except (OSError, ValueError, TypeError) as exc:
        raise BridgeError(f"invalid SWI authorization record: {exc}") from exc


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SWI GitHub authority bridge (Git + gh)")
    parser.add_argument("--repo", default=".", help="existing local Git checkout")
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("inspect")
    sub.add_parser("account")
    compare = sub.add_parser("compare")
    compare.add_argument("base")
    compare.add_argument("head")
    verify = sub.add_parser("verify-commit")
    verify.add_argument("revision")
    releases = sub.add_parser("releases")
    releases.add_argument("--limit", type=int, default=10)
    pr = sub.add_parser("prepare-pr")
    pr.add_argument("base")
    pr.add_argument("head")
    pr.add_argument("--title", required=True)
    fetch = sub.add_parser("fetch")
    fetch.add_argument("--remote", default="origin")
    fetch.add_argument("--approval-json", required=True)
    push = sub.add_parser("push")
    push.add_argument("--remote", default="origin")
    push.add_argument("--branch", required=True)
    push.add_argument("--approval-json", required=True)
    commit = sub.add_parser("commit")
    commit.add_argument("--message", required=True)
    commit.add_argument("--approval-json", required=True)
    release = sub.add_parser("create-release")
    release.add_argument("--tag", required=True)
    release.add_argument("--title", required=True)
    release.add_argument("--notes-file", required=True)
    release.add_argument("--approval-json", required=True)
    args = parser.parse_args(argv)
    try:
        bridge = GitHubAuthorityBridge(args.repo)
        if args.operation == "inspect":
            result = bridge.inspect()
        elif args.operation == "account":
            result = bridge.authenticated_account()
        elif args.operation == "compare":
            result = bridge.compare(args.base, args.head)
        elif args.operation == "verify-commit":
            result = bridge.verify_commit(args.revision)
        elif args.operation == "releases":
            result = bridge.inspect_releases(args.limit)
        elif args.operation == "prepare-pr":
            result = bridge.prepare_pull_request(args.base, args.head, args.title)
        elif args.operation == "fetch":
            result = bridge.fetch(args.remote, _approval(args.approval_json))
        elif args.operation == "push":
            result = bridge.push(args.remote, args.branch, _approval(args.approval_json))
        elif args.operation == "commit":
            result = bridge.commit(args.message, _approval(args.approval_json))
        else:
            result = bridge.create_release(args.tag, args.title, args.notes_file,
                                           _approval(args.approval_json))
        print(evidence_json(result))
        return 0
    except BridgeError as exc:
        print(json.dumps({"result": "HALTED", "reason": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
