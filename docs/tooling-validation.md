# RQML comparison and validation

Observed on 2026-11-06 with Node 26.13.0 and npm 12.2.1 on Linux x86-64.
Installed packages: `@rqml/cli` 0.11.0, core 0.9.0, schema package 0.2.2;
document schema 2.2.0. These are tool and representation checks, not firmware or
hardware acceptance.

This branch starts at planning-only main commit
`6ee995ecdebdfbb1baac7b95bdce67baae57205e`. The comparison corpus is the
[OpenLore branch at 1b4f73a725c962285ba55575f065faf71dfc9929](https://github.com/altendky/motley/tree/1b4f73a725c962285ba55575f065faf71dfc9929),
submitted as [PR #2](https://github.com/altendky/motley/pull/2). The planning
document remains unchanged in both alternatives.

## Same requirements, different supporting tools

Programmatic comparison confirmed the same 12 requirement IDs, titles, statements
and 14 acceptance scenarios. Whitespace and the OpenLore-to-RQML report name in
one criterion are the only normative-text adaptations. Each RQML criterion also
has a stable native ID; scenario titles are preserved as XML comments.

| Concern | OpenLore/OpenSpec PR #2 | This RQML alternative |
| --- | --- | --- |
| Authored requirements | Markdown in four domain specs | XML in four requirement packages |
| Requirement identity | Project `MOT-*` convention inside headings | Native `id` separate from title; criterion IDs too |
| Scoped retrieval observed | Keyword requirement search and function orientation | `show`, scoped views, declared `impact` and matrix |
| C++ navigation observed | Function extraction and a cross-file call | No recovered source call/include graph |
| C++ implementation links observed | Exact symbol anchor reported `not-assessed` | File locator/hash works; `#symbol` is not verified |
| Maintenance observed | Initial C++ mapping limitation established | File changes/moves detected; explicit repair preserves requirements |
| Test evidence | Links/graphs are not test execution | `verifiedBy` is a relationship; no test content or existence checking through the drift gate |
| Initial completion state | 12 unmapped requirements | 12 unimplemented and 12 unverified requirements |

These trials were not identical workload benchmarks. RQML's maintenance cases
were broader than the initial OpenLore fixture. Neither option has demonstrated
the complete repeated-change application workflow, and neither has run firmware
tests. RQML is the more directly useful requirements/identity layer in this trial;
OpenLore supplies source navigation that RQML lacks. No combined integration is
configured or established by this PR.

## Project checks

| Operation | Observed result |
| --- | --- |
| Clean `npm ci --no-audit --no-fund --loglevel=error` | Exit 0; six dependency packages installed |
| `npm run requirements:validate` | Exit 0; valid schema 2.2.0 and references |
| `npm run requirements:lint` | Exit 0; no strict lint findings |
| `npm run requirements:check` | Exit 2; 12 unimplemented and 12 unverified requirements, no orphan requirements or uncovered goals |
| Standard check | Exit 0 while still reporting the missing implementation/test links |
| `show MOT-SENS-004` | Returned the statement, native criterion ID and goal edge |
| `impact MOT-SENS-004` | Returned its goal and the other sensing requirements through declared goal edges |
| Matrix JSON | Twelve draft, unimplemented, unverified requirement rows |

The strict check is an intentionally unmet completion gate. A green standard
check is not used to hide the initial gaps. No project implementation/test edges
or reviewed-content baseline were fabricated.

## Disposable C++ trace trial

Twenty-eight CLI operations exercised two synthetic requirements with a shared
C++ implementation file, two function fragments, one shared test locator and a
declared goal. The fixture's approved statuses were test data, not human approval
of Motley requirements. No C++ code was compiled and no behavioral test ran.

| Case | Observed result |
| --- | --- |
| Three implementation links and two test links | Recorded successfully; a strict fixture check passed |
| Many-to-many matrix | One requirement had two code locators; both requirements shared a code locator and test |
| Requirement retitle | Requirement and criterion IDs stayed unchanged; show and check succeeded |
| Behavior-changing statement and acceptance edit | Strict check still passed and implementation baseline bytes were unchanged |
| Change one function in the linked C++ file | Strict check exited 2 with changed implementation findings for whole-file links |
| Restore the original source bytes | Baseline check passed again |
| Replace fragment with `#does_not_exist` | Link and strict check passed; C++ symbol existence was not validated |
| Move the implementation file | Strict check exited 2 with missing implementation findings |
| Repoint all affected edges with `link --update` | Strict check passed; the requirements section remained byte-identical |
| Change the linked test's assertion | Strict check still passed |
| Remove the linked test file | Strict check still passed |
| Declare a nonexistent local goal endpoint | Document validation failed with exit 1 |
| Start CLI impact from an external source locator | Rejected with exit 64; use matrix inspection for reverse file-to-requirement lookup |

The matrix called the synthetic rows `implemented` and `verified` even though no
behavioral tests ran. Those labels indicate trace relationships; they must not be
reported as execution evidence. The unchanged baseline after a requirement edit
also means the agent must explicitly reconsider previous implementation and
verification against the new requirement content.

The fixture and raw operation outputs were temporary trial material, removed
after these findings were recorded. The source-navigation companion, function
resolution, requirement-revision invalidation and test freshness remain distinct
work items. No automatic RQML/OpenLore bridge or agent-host hooks were tested.

## Content identification

The validated uncommitted working content is identified by these SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `requirements.rqml` | `031aded3a99a30bb903b584690881553258c80a6f5d2dcf6e8e229c2e3195cab` |
| `package-lock.json` | `696bab5a168e885dbd9afb6f284af0691e67f541eb791da2a1ffc0dca979c4a1` |

No ESP-IDF build, sensor read, cable qualification, Home Assistant commissioning,
reboot recovery or heater test has run. These remain the same pending application
acceptance work as in the OpenLore alternative.
