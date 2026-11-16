from pathlib import Path

import pytest

from swi_v2.github_authority_bridge import (
    AuthorizationRequired,
    BridgeError,
    GitHubAuthorityBridge,
    HumanApproval,
    parse_github_remote,
)


def test_parse_https_and_ssh_github_remotes():
    assert parse_github_remote("https://github.com/swi-owner/swi-repository.git").slug == "swi-owner/swi-repository"
    assert parse_github_remote("git@github.com:swi-owner/swi-repository.git").slug == "swi-owner/swi-repository"


@pytest.mark.parametrize("value", [
    "https://example.com/owner/repo.git",
    "https://github.com/owner/repo/extra.git",
    "file:///tmp/repo",
])
def test_rejects_non_github_or_ambiguous_remote(value):
    with pytest.raises(BridgeError):
        parse_github_remote(value)


class FakeGit:
    def __init__(self):
        self.calls = []

    def __call__(self, args, *, cwd=None):
        self.calls.append(tuple(args))
        if args[:3] == ("git", "remote", "get-url"):
            return "https://github.com/swi-owner/swi-v2-repository.git"
        if args[:3] == ("git", "branch", "--show-current"):
            return "feature/test"
        if args[:3] == ("git", "rev-parse", "HEAD"):
            return "a" * 40
        if args[:3] == ("git", "rev-parse", "--abbrev-ref"):
            raise BridgeError("no upstream")
        if args[:3] == ("git", "check-ref-format", "--branch"):
            return args[3]
        if args[:3] == ("git", "rev-parse", "--verify"):
            raise BridgeError("tag not found")
        if args[:3] == ("git", "status", "--porcelain=v1"):
            return ""
        if args[:3] == ("git", "rev-list", "--left-right"):
            return "2 1"
        if args[:3] == ("git", "diff", "--stat"):
            return "1 file changed"
        if args[:2] == ("git", "fetch"):
            return ""
        raise AssertionError(f"unexpected command: {args}")


def test_read_only_inspection_reports_git_state_without_authority_claim():
    runner = FakeGit()
    bridge = GitHubAuthorityBridge(Path.cwd(), runner=runner)
    result = bridge.inspect()
    assert result.result == "INSPECTED"
    assert result.details["repository"] == "swi-owner/swi-v2-repository"
    assert result.details["head"] == "a" * 40
    assert result.authorization_source == "READ_ONLY"


def test_fetch_without_authorization_is_halted_before_git_fetch():
    runner = FakeGit()
    bridge = GitHubAuthorityBridge(Path.cwd(), runner=runner)
    with pytest.raises(AuthorizationRequired):
        bridge.fetch("origin", None)
    assert not any(call[:2] == ("git", "fetch") for call in runner.calls)


def test_fetch_requires_exact_repository_action_and_target_binding():
    runner = FakeGit()
    bridge = GitHubAuthorityBridge(Path.cwd(), runner=runner)
    bad = HumanApproval("auth-1", "owner", "other/repo", "fetch",
                        "remote=origin;no-tags=true", True, "evidence://1")
    with pytest.raises(AuthorizationRequired):
        bridge.fetch("origin", bad)
    assert not any(call[:2] == ("git", "fetch") for call in runner.calls)


def test_authorized_fetch_runs_without_fetching_tags():
    runner = FakeGit()
    bridge = GitHubAuthorityBridge(Path.cwd(), runner=runner,
                                   approval_verifier=lambda record: record.evidence_ref == "swi-evidence://approval/2")
    approval = HumanApproval(
        "auth-2", "human-owner", "swi-owner/swi-v2-repository", "fetch",
        "remote=origin;no-tags=true", True, "swi-evidence://approval/2",
    )
    result = bridge.fetch("origin", approval)
    assert result.result == "FETCHED"
    assert result.authorization_id == "auth-2"
    assert ("git", "fetch", "--no-tags", "--", "origin") in runner.calls


def test_supplied_record_is_not_authority_without_trusted_verifier():
    runner = FakeGit()
    bridge = GitHubAuthorityBridge(Path.cwd(), runner=runner)
    approval = HumanApproval(
        "fake", "anyone", "swi-owner/swi-v2-repository", "fetch",
        "remote=origin;no-tags=true", True, "arbitrary-string",
    )
    with pytest.raises(AuthorizationRequired, match="verifier"):
        bridge.fetch("origin", approval)
    assert not any(call[:2] == ("git", "fetch") for call in runner.calls)


@pytest.mark.parametrize("operation", ["clone", "commit", "push", "release"])
def test_all_other_mutations_halt_without_trusted_verifier(operation, tmp_path):
    runner = FakeGit()
    bridge = GitHubAuthorityBridge(Path.cwd(), runner=runner)
    notes = tmp_path / "release-notes.md"
    notes.write_text("draft notes", encoding="utf-8")
    unverified = HumanApproval("unverified", "human", "owner/repo", operation,
                               "some-target", True, "evidence://unverified")
    with pytest.raises(AuthorizationRequired, match="verifier"):
        if operation == "clone":
            bridge.clone("https://github.com/owner/repo.git", tmp_path / "new-clone", unverified)
        elif operation == "commit":
            bridge.commit("approved change", unverified)
        elif operation == "push":
            bridge.push("origin", "feature/test", unverified)
        else:
            bridge.create_release("v0.1.0", "Release", notes, unverified)
    mutation_prefixes = {
        ("git", "clone"), ("git", "commit"), ("git", "push"),
        ("gh", "release", "create"),
    }
    assert not any(call[:len(prefix)] == prefix for call in runner.calls
                   for prefix in mutation_prefixes)


def test_pr_preparation_is_local_and_does_not_publish():
    runner = FakeGit()
    bridge = GitHubAuthorityBridge(Path.cwd(), runner=runner)
    result = bridge.prepare_pull_request("main", "feature/test", "Test PR")
    assert result.result == "PREPARED_NOT_PUBLISHED"
    assert "awaiting human review" in result.details["body"]
    assert not any(call[:2] == ("gh", "pr") for call in runner.calls)


def test_pr_title_rejects_multiline_input():
    bridge = GitHubAuthorityBridge(Path.cwd(), runner=FakeGit())
    with pytest.raises(BridgeError):
        bridge.prepare_pull_request("main", "feature/test", "title\nbody")
