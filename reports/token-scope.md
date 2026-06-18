# Token Scope Doctor

Last refreshed: 2026-06-18 11:50 UTC
`gh auth status` exit code: `0`

## Diagnosis

- Repository access appears available.
- `workflow` scope was not detected. Keep workflow templates outside `.github/workflows/` until the token is upgraded.

## Least-Privilege Notes

- Do not paste token values into reports or chat logs.
- Prefer short-lived or narrowly scoped tokens for automation.
- Add `workflow` only when you explicitly need to create or edit GitHub Actions workflow files.

## Redacted gh Auth Status

```text
github.com
  ✓ Logged in to github.com account GravityblueX (keyring)
  - Active account: true
  - Git operations protocol: ssh
  - Token: <redacted-token>
  - Token scopes: 'admin:public_key', 'gist', 'read:org', 'repo'
```
