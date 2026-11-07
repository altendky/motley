# Repository automation

## Local checks

Mise pins Python, uv, and pre-commit for repository checks. From the repository
root:

```sh
mise trust
mise install --locked
mise exec -- pre-commit install
mise exec -- pre-commit run --all-files
```

Keep `mise.lock` and the native package dependency graphs under `.mise/locks/`
together when updating tools. The lock covers Linux x64/arm64, macOS x64/arm64,
and Windows x64.

## CI

GitHub Actions runs on pull requests and pushes to `main`. It checks the Mise
lockfile and runs pre-commit: whitespace, file syntax, merge conflicts, workflow
lint, Mergify configuration validation, requirements consistency/approval, and
firmware metadata tests. A separate [firmware build](firmware-build.md) job builds
and verifies the ESP32-C6 target and retains verified firmware artifacts or failed
build diagnostics. The aggregate `all` job supplies the required GitHub status
check. Hosted execution and physical-board behavior have separate verification
evidence.

## Dependency updates

Renovate runs every six hours and on manual dispatch through the
`altendky-renovate` GitHub App. App authentication uses the repository variable
`RENOVATE_CLIENT_ID` and secret `RENOVATE_APP_PRIVATE_KEY`.

It updates GitHub Actions, Mise tools, and pre-commit hooks. Python stays on the
selected 3.14 minor release. Mise updates regenerate `mise.lock` together with
the native package dependency graphs under `.mise/locks/` for all five platforms.
The workflow allows only the declared post-update commands.

## Merge queue

Mergify queues non-draft pull requests to `main` when labeled `enqueue`, using
merge commits and the required GitHub checks. Renovate pull requests receive
that label automatically; bot approval and queue admission are separate rules.
The `agent` issue label identifies work suitable for autonomous selection.
