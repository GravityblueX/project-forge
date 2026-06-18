# Dependency Update Config Draft

Scan root: `YumeBox-MaterialDesign-Study`
Last refreshed: 2026-06-18 11:48 UTC

## Detected Ecosystems

| Ecosystem | Directories |
|---|---|
| gradle | `.`, `app`, `core`, `data`, `extension`, `feature/editor`, `feature/meta`, `feature/override`, `feature/proxy`, `feature/substore`, `locale`, `platform`, `runtime/api`, `runtime/client`, `runtime/service`, `ui`, `ui-miuix` |

## Renovate Draft

Save as `renovate.json` after review.

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended"
  ],
  "schedule": [
    "before 5am on monday"
  ],
  "dependencyDashboard": true,
  "labels": [
    "dependencies",
    "gradle"
  ],
  "packageRules": [
    {
      "matchUpdateTypes": [
        "minor",
        "patch",
        "pin",
        "digest"
      ],
      "groupName": "low-risk dependency updates",
      "automerge": false
    },
    {
      "matchUpdateTypes": [
        "major"
      ],
      "labels": [
        "dependencies",
        "major-update"
      ],
      "automerge": false
    }
  ]
}
```

## Dependabot Draft

Save as `.github/dependabot.yml` after review.

```yaml
version: 2
updates:
  - package-ecosystem: "gradle"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/app"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/core"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/data"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/extension"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/feature/editor"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/feature/meta"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/feature/override"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/feature/proxy"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/feature/substore"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/locale"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/platform"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/runtime/api"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/runtime/client"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/runtime/service"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/ui"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "gradle"
    directory: "/ui-miuix"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

## Review Notes

- Keep major updates separate from patch/minor batches.
- Require tests before enabling automerge.
- Add private registry credentials only through encrypted secrets.
