# Termux GitHub Authority Bridge

**State:** implemented locally for read-only GitHub work; tested locally and
against the authenticated GitHub account for the identified SWI repository.
Consequential operations remain blocked until a trusted SWI approval verifier
is supplied. This document does not claim production integration.

## Roles

- Git and GitHub remain the repository and remote-source authority.
- Termux is the primary local SWI development and test environment.
- `gh` supplies GitHub account/API access and uses its existing credential
  store. Codex CLI is not used for account identity and is optional.
- `swi_v2.github_authority_bridge` is a client of the existing
  `swi_v2.kernel.authority.require_authorization_for_action` boundary. It does
  not implement a second authorization engine.

## Read-only workflow

From an SWI checkout:

```sh
python -m swi_v2.github_authority_bridge inspect
python -m swi_v2.github_authority_bridge account
python -m swi_v2.github_authority_bridge compare origin/main HEAD
python -m swi_v2.github_authority_bridge verify-commit HEAD
python -m swi_v2.github_authority_bridge releases --limit 10
python -m swi_v2.github_authority_bridge prepare-pr main HEAD --title 'Describe verified change'
```

`verify-commit` distinguishes an available Git commit object from a valid
cryptographic signature. Unsigned or unverifiable commits remain
`UNVERIFIED`. Pull-request preparation only produces a local draft; it does
not create a PR or push a branch. The account command returns only the GitHub
login and never reads or prints a token.

## Consequential operations

The library exposes fetch, clone, commit, push and release operations. Each
requires an approval bound to the exact repository, action and target, then
passes through the existing SWI authorization function. A caller must also
provide an `approval_verifier` that validates the approval evidence against
the actual SWI human-authority source. With no verifier, all such operations
halt. A JSON record by itself is not authority. Force push and remote history
rewriting are not provided.

The current repository has no discovered trusted approval-verifier service or
cryptographic approval-record validator. Therefore the mutation path is
**fail-closed but not operationally integrated**. Do not configure a permissive
verifier merely to make commands run. Commit, push, release and repository
changes still need independently validated SWI authorization and human
approval.

## Evidence and limitations

- The authenticated account and repository smoke-test results are recorded in
  `reports/TERMUX_GITHUB_BRIDGE_EVIDENCE_20261111.md`; that run record is
  evidence for that account/repository pair, not a reusable identity setting.
- `gh api user --jq .login` returns only the login and never reads or prints a
  token. GitHub account authentication remains separate from SWI authority.
- No remote Actions result is used to infer that a local branch is
  authoritative.
- No fetch, clone, commit, push, release, PR creation, credential change, or
  SSH-key operation was performed.
- The bridge's tests use a fake command runner for local command construction
  and scope checks. They do not authenticate a test write against GitHub.

States remain `EXPERIMENTAL` for publication integration,
`PROVEN=NO`, `SEALED=NO`, and `PRODUCTION_AUTHORIZED=NO`.
