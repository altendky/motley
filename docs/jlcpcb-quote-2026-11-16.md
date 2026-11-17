# JLCPCB quote after AC passive revision

Historical snapshot: the later
[exact-part integration quote](jlcpcb-quote-2026-11-16-exact-parts.md) supersedes
this result for the current native boards. Values below retain their original
inputs and factory/manual split.

Actual quotation API results obtained 2026-11-16 from fresh current-board
Gerbers and matching BOM/CPL pairs. Prices are USD for fabrication, selected
components and Economic front-side assembly, including JLC's component attrition
and minimum purchases. No cart addition, order, payment or inventory purchase
was made. Shipping, tax, duties and hand-completion parts are excluded.

One planned controller uses one carrier, one sensor mux and two output boards.
The current **LOW regional population** is quoted. HIGH population notes are
not a separately submitted or priced BOM.

| Controllers planned | Fabricated: carrier / mux / output | Assembled: carrier / mux / output | Carrier job | Mux job | Output job | JLC total | JLC cost per planned controller |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1, minimum Economic case | 5 / 5 / 5 | 2 / 2 / 2 | $126.92 | $47.27 | $103.97 | **$278.16** | $278.16 |
| 2 | 5 / 5 / 5 | 2 / 2 / 5 | $126.92 | $47.27 | $128.56 | **$302.75** | $151.38 |
| 5 | 5 / 5 / 10 | 5 / 5 / 10 | $161.17 | $63.31 | $178.14 | **$402.62** | $80.52 |

The minimum case buys spare carrier/mux assemblies; the two-controller case
buys a spare output assembly. These are partial factory assemblies, not finished
controller prices. Larger quantities have additional stock omissions below.

## New passive selections are included

Exact input codes, persisted selected references and final priced component
rows were independently reconciled. All new LOW passive selections are selected
and priced at every scenario's quantities, with no generic substitutions or
Standard-only rows accepted:

- TDK B32651A7472K000 / C3781178: two 4.7 nF snubber capacitors per output.
- Vishay PR02000203300JA100 / C1365089: snubber and gate-shunt 330 ohm parts.
- Vishay PR02000201201JA100 / C1366069: two fitted 1.2k gate resistors per output.
- TE CRGP2512F8K2 / C3992729: four fitted detector resistors per output.
- TE CRGP2512F18K / C2082909: three carrier line-reference resistors.
- UNI-ROYAL C25469 zero-ohm links and C17530 2.7k detector shunts.

The new through-hole capacitors and PR02 resistors are included in Economic
assembly. Each design's job includes a **$3.61 through-hole setup fee**.
Variable through-hole charges are $0.69 / $0.33 / $0.66 for the minimum
carrier/mux/output jobs and $1.63 / $0.83 / $3.30 for the five-controller jobs.
Each job also includes $8.24 assembly setup, $1.55 stencil, $3.09 per charged
Extended component type, component purchases and SMT placement charges.

Purchased quantities already include excess components where required. For
example, two output assemblies price ten CRGP8k2 resistors for eight installed
and fourteen zero-ohm links for six installed. Ten output assemblies price
42 CRGP8k2 parts for forty installed. Do not add these excess quantities again.

## Remaining hand completion

| Scenario | Factory positions per carrier / mux / output | Submitted rows excluded for insufficient stock |
| ---: | --- | --- |
| 1 | 80 / 74 / 60 | Carrier R25; output K1 Omron relay |
| 2 | 80 / 74 / 59 | Same, plus output U31 ACPL-K370-500E |
| 5 | 79 / 74 / 58 | Same, plus carrier U40 ACPL-K376-000E and output U2 VO3053-X007T |

There are also twelve manual/unresolved BOM positions across the three designs:
carrier F1, J1, J15, J16, J18, J19; output F2, J10, J14, J17, J20, SW20.
These cover fuses/clips, mains/deployment connections and configuration hardware.
A fuse position requires a cartridge plus two clips. Off-board outlets, wiring,
heatsinks/clips, panel USB and other completion hardware are separate costs.
The previous complete-controller budget must be reconciled against these new
factory selections before reuse; its hand-fitted passive allowances would now
double-count factory-fitted parts.

## Inputs and limits

JLC recognized all three boards as four layers with exact dimensions:
carrier 95 x 80 mm, output **90 x 85 mm**, sensor L 80 x 40 mm overall.
Five bare PCBs cost $8 per design; ten output PCBs cost $14, already included
above. Settings remain 1.6 mm FR4, green mask, leaded HASL, 1 oz outer / 0.5 oz
inner copper and normal nonurgent service. Current settings still permit two
or five assemblies from five boards, and ten from ten.

All 263 footprints were classified: 216 factory candidates, twelve manual
positions, two LOW DNP parts and 33 excluded mechanical/access features.
Every included BOM row has an explicit code. Source hashes stayed unchanged
during export and quotation. Placement coordinates/angles match native anchors;
actual assembly centroids, lead forming, rotations and placeholder package fit
still require manufacturing review. Quote acceptance does not qualify hardware.

| Native board | SHA-256 |
| --- | --- |
| motley-carrier.kicad_pcb | `bf769075e662eed372fe9a0bfc58c47819c43a1c4fe2f96f58ff364c4279bd1f` |
| motley-ac-output.kicad_pcb | `95ac0aed5d2f0a2c0f0ba1ca824c9fb16528e2cd6a8d1043f3d2f8487209f8a2` |
| motley-sensors.kicad_pcb | `cccc0aa9f2753b86abd544f71891ea86f915e3018359fc6a2738d2dcd71f50aa` |

Exports, API requests/responses, per-reference selection audits, fee
reconciliation and the minimal `quote-summary.json` remain temporary evidence
under `/tmp/agents/PUOfdDTNUf/quote-2026-11-16/`. The reusable process is the
[quote skill](../.agents/skills/jlcpcb-quote/SKILL.md).
