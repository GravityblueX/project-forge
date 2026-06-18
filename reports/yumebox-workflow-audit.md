# Workflow Policy Audit

Scan root: `YumeBox-MaterialDesign-Study`
Last refreshed: 2026-06-18 11:01 UTC
Workflow files scanned: `13`
Findings: `44`

| Severity | File | Line | Rule | Fix |
|---|---|---:|---|---|
| high | `.github/workflows/build-release-preview.yml` | 1 | missing-top-level-permissions | Add the narrowest required `permissions:` block at workflow or job level. |
| high | `.github/workflows/reusable-build-apk-only.yml` | 47 | mutable-action-ref | Pin to a release tag or audited commit SHA. |
| high | `.github/workflows/reusable-build-geo.yml` | 32 | mutable-action-ref | Pin to a release tag or audited commit SHA. |
| high | `.github/workflows/reusable-build-native-abi.yml` | 38 | mutable-action-ref | Pin to a release tag or audited commit SHA. |
| medium | `.github/workflows/Preview.yml` | 31 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/Preview.yml` | 33 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/Preview.yml` | 47 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/Preview.yml` | 253 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/build-release-preview.yml` | 13 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/build-release-preview.yml` | 16 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/build-release-preview.yml` | 39 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/ci-channel.yml` | 20 | write-permission | Keep write permissions only on release or automation jobs that need them. |
| medium | `.github/workflows/dependency.yml` | 13 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/dependency.yml` | 15 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/release.yml` | 19 | write-permission | Keep write permissions only on release or automation jobs that need them. |
| medium | `.github/workflows/reusable-build-apk-only.yml` | 35 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-apk-only.yml` | 41 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-apk-only.yml` | 53 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-apk-only.yml` | 59 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-apk-only.yml` | 76 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-apk-only.yml` | 121 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-geo.yml` | 20 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-geo.yml` | 26 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-geo.yml` | 46 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-native-abi.yml` | 26 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-native-abi.yml` | 32 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-native-abi.yml` | 52 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-native-abi.yml` | 72 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-native-abi.yml` | 78 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-build-native-abi.yml` | 124 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-bundle-native.yml` | 20 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-bundle-native.yml` | 26 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-bundle-native.yml` | 43 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-notify-telegram.yml` | 32 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-notify-telegram.yml` | 37 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-notify-telegram.yml` | 54 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-prepare-publish.yml` | 38 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-prepare-publish.yml` | 44 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-prepare-publish.yml` | 197 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-publish-release.yml` | 26 | write-permission | Keep write permissions only on release or automation jobs that need them. |
| medium | `.github/workflows/reusable-publish-release.yml` | 35 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-publish-release.yml` | 43 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `.github/workflows/reusable-publish-release.yml` | 71 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| low | `.github/workflows/ci-channel.yml` | 11 | scheduled-workflow | Keep schedule frequency modest and make generated commits deterministic. |

## Details

### HIGH - missing-top-level-permissions

- File: `.github/workflows/build-release-preview.yml`
- Line: `1`
- Detail: Workflow does not declare top-level GITHUB_TOKEN permissions.
- Suggested fix: Add the narrowest required `permissions:` block at workflow or job level.

### HIGH - mutable-action-ref

- File: `.github/workflows/reusable-build-apk-only.yml`
- Line: `47`
- Detail: `fwilhe2/setup-kotlin` uses moving ref `main`.
- Suggested fix: Pin to a release tag or audited commit SHA.

### HIGH - mutable-action-ref

- File: `.github/workflows/reusable-build-geo.yml`
- Line: `32`
- Detail: `fwilhe2/setup-kotlin` uses moving ref `main`.
- Suggested fix: Pin to a release tag or audited commit SHA.

### HIGH - mutable-action-ref

- File: `.github/workflows/reusable-build-native-abi.yml`
- Line: `38`
- Detail: `fwilhe2/setup-kotlin` uses moving ref `main`.
- Suggested fix: Pin to a release tag or audited commit SHA.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/Preview.yml`
- Line: `31`
- Detail: `actions/checkout` uses broad major tag `v6`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/Preview.yml`
- Line: `33`
- Detail: `actions/setup-node` uses broad major tag `v4`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/Preview.yml`
- Line: `47`
- Detail: `actions/github-script` uses broad major tag `v7`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/Preview.yml`
- Line: `253`
- Detail: `actions/upload-artifact` uses broad major tag `v7`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/build-release-preview.yml`
- Line: `13`
- Detail: `actions/checkout` uses broad major tag `v4`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/build-release-preview.yml`
- Line: `16`
- Detail: `actions/setup-java` uses broad major tag `v4`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/build-release-preview.yml`
- Line: `39`
- Detail: `actions/upload-artifact` uses broad major tag `v4`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - write-permission

- File: `.github/workflows/ci-channel.yml`
- Line: `20`
- Detail: Workflow grants `contents: write`.
- Suggested fix: Keep write permissions only on release or automation jobs that need them.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/dependency.yml`
- Line: `13`
- Detail: `actions/checkout` uses broad major tag `v6`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/dependency.yml`
- Line: `15`
- Detail: `actions/dependency-review-action` uses broad major tag `v4`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - write-permission

- File: `.github/workflows/release.yml`
- Line: `19`
- Detail: Workflow grants `contents: write`.
- Suggested fix: Keep write permissions only on release or automation jobs that need them.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-apk-only.yml`
- Line: `35`
- Detail: `actions/checkout` uses broad major tag `v6`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-apk-only.yml`
- Line: `41`
- Detail: `actions/setup-java` uses broad major tag `v5`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-apk-only.yml`
- Line: `53`
- Detail: `android-actions/setup-android` uses broad major tag `v4`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-apk-only.yml`
- Line: `59`
- Detail: `actions/cache` uses broad major tag `v5`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-apk-only.yml`
- Line: `76`
- Detail: `actions/download-artifact` uses broad major tag `v8`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-apk-only.yml`
- Line: `121`
- Detail: `actions/upload-artifact` uses broad major tag `v7`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-geo.yml`
- Line: `20`
- Detail: `actions/checkout` uses broad major tag `v6`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-geo.yml`
- Line: `26`
- Detail: `actions/setup-java` uses broad major tag `v5`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-geo.yml`
- Line: `46`
- Detail: `actions/upload-artifact` uses broad major tag `v7`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-native-abi.yml`
- Line: `26`
- Detail: `actions/checkout` uses broad major tag `v6`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-native-abi.yml`
- Line: `32`
- Detail: `actions/setup-java` uses broad major tag `v5`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-native-abi.yml`
- Line: `52`
- Detail: `actions/cache` uses broad major tag `v5`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-native-abi.yml`
- Line: `72`
- Detail: `android-actions/setup-android` uses broad major tag `v4`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-native-abi.yml`
- Line: `78`
- Detail: `actions/cache` uses broad major tag `v5`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-build-native-abi.yml`
- Line: `124`
- Detail: `actions/upload-artifact` uses broad major tag `v7`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-bundle-native.yml`
- Line: `20`
- Detail: `actions/download-artifact` uses broad major tag `v8`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-bundle-native.yml`
- Line: `26`
- Detail: `actions/download-artifact` uses broad major tag `v8`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-bundle-native.yml`
- Line: `43`
- Detail: `actions/upload-artifact` uses broad major tag `v7`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-notify-telegram.yml`
- Line: `32`
- Detail: `actions/checkout` uses broad major tag `v6`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-notify-telegram.yml`
- Line: `37`
- Detail: `actions/download-artifact` uses broad major tag `v8`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-notify-telegram.yml`
- Line: `54`
- Detail: `actions/cache` uses broad major tag `v5`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-prepare-publish.yml`
- Line: `38`
- Detail: `actions/checkout` uses broad major tag `v6`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-prepare-publish.yml`
- Line: `44`
- Detail: `actions/download-artifact` uses broad major tag `v8`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-prepare-publish.yml`
- Line: `197`
- Detail: `actions/upload-artifact` uses broad major tag `v7`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - write-permission

- File: `.github/workflows/reusable-publish-release.yml`
- Line: `26`
- Detail: Workflow grants `contents: write`.
- Suggested fix: Keep write permissions only on release or automation jobs that need them.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-publish-release.yml`
- Line: `35`
- Detail: `actions/download-artifact` uses broad major tag `v8`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-publish-release.yml`
- Line: `43`
- Detail: `actions/github-script` uses broad major tag `v7`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `.github/workflows/reusable-publish-release.yml`
- Line: `71`
- Detail: `softprops/action-gh-release` uses broad major tag `v2`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### LOW - scheduled-workflow

- File: `.github/workflows/ci-channel.yml`
- Line: `11`
- Detail: Scheduled workflow should be checked for rate, permissions, and idempotence.
- Suggested fix: Keep schedule frequency modest and make generated commits deterministic.
