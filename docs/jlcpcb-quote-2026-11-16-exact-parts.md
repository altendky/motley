# JLCPCB quote after exact-part integration

Later revision, 2026-11-17: the optional USB J27/R28/R29 DNP footprints and
three BOM-excluded copper selectors change the carrier CAD after these exports.
They add no default purchased components and keep the 95×80 mm outline, but
the quoted input hashes below remain the November 16 snapshot; no new quote
has been submitted for that later copper revision.

Actual quotation-only API results obtained 2026-11-16 from the revised native
four-layer boards and matching Gerber/BOM/CPL exports. Prices include bare PCBs,
selected components, Economic front-side assembly and component attrition.
Shipping, tax/duties and hand-completion parts are excluded. No cart addition,
order, payment or component-inventory purchase was made.

One finished controller uses one carrier, one sensor mux and two identical
output boards. These quotes use the LOW population. HIGH remains a separate,
unqualified population, including unresolved higher-voltage fusing and links.

| Finished controllers planned | Fabricated: carrier / mux / output | Assembled: carrier / mux / output | Carrier job | Mux job | Output job | JLC total | JLC per planned controller |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1, minimum Economic case | 5 / 5 / 5 | 2 / 2 / 2 | $132.48 | $47.29 | $105.49 | **$285.26** | $285.26 |
| 2 | 5 / 5 / 5 | 2 / 2 / 5 | $132.48 | $47.29 | $132.31 | **$312.08** | $156.04 |
| 5 | 5 / 5 / 10 | 5 / 5 / 10 | $170.18 | $63.33 | $185.62 | **$419.13** | $83.83 |

The minimum case includes spare carrier/mux assemblies; the two-controller case
includes a spare output assembly. These are partial factory assemblies, not
finished-controller prices. Complete-controller allowances must be reconciled
against actual factory selections rather than added from an older generic BOM.
Compared with the preceding passive-revision quote, the batch increases are
**$7.10 / $9.33 / $16.51**, respectively. Stock and component prices were
rechecked at each quantity, so these are actual recalculations.

## Factory assembly and hand fitting

Exact selected codes in the priced jobs include the newly integrated GOOSVN
GS007S terminals and JST PH six-way output-bus headers. JLC installs these by
hand soldering within Economic service; they do not require us to solder them.
YAGEO AC0603FR-07226KL / C227714 replaces R25's same-value RC part because the
original stock could not satisfy the twenty-piece attrition purchase.

| Scenario | Factory positions per carrier / mux / output | Additional stock omissions |
| ---: | --- | --- |
| 1 | 86 / 74 / 63 | Output K1, retained Omron relay |
| 2 | 86 / 74 / 62 | Same, plus output U31 ACPL-K370-500E |
| 5 | 85 / 74 / 61 | Same, plus carrier U40 ACPL-K376-000E and output U2 VO3053-X007T |

Four deliberately manual positions remain across the unique designs:
carrier F1 holder; output F2 holder, J20 snubber header and SW20 recovery header.
The retained relay is separately omitted for lack of JLC stock. Each fuse
position now means **one Schurter OGN holder**, plus a separately inserted
cartridge and black cover. There are no fictitious single-piece clip/fuse
assemblies or cartridge placements in the factory BOM/CPL.

The [exact selection guide](hardware-exact-selections.md) gives a refreshed
**$25.67 base hand-fitting basket per finished controller**, including fuse
holders/cartridges/covers, relays, configuration headers/caps and two output
harnesses' housings/contacts. This excludes wire, tools/acquisition charges,
off-board hardware and extra quantity-dependent stock omissions. Spare factory
assemblies need not be hand-completed. Larger-batch retail price breaks are
not assumed in that one-controller basket.

K1 is already included in the base basket; do not count it again. For two
finished controllers, hand completion needs four U31 parts, even though the
factory job buys five output assemblies. For five finished controllers, the
additional omissions are five U40, ten U2 and ten U31 parts. These optical
parts are outside the $25.67 base allowance.

Every priced row was reconciled against the submitted exact codes and native
references, including selected/matched/in-stock state and actual attrition.
The 263 unique-design footprints divide into 224 factory candidates, four
explicit manual positions, two LOW DNP positions and 33 mechanical/access
features. Those classifications are distinct from quantity-dependent stock
omissions. All new LOW passives remain factory-selected at every quantity.
Combined attrition demand for all seventeen codes shared between the three
five-controller jobs also fits available stock; separate job matching alone
would not establish that. Quotes do not reserve inventory.

## Included fees

Each board job includes $8.24 assembly setup, $1.55 stencil and $3.61 manual
soldering setup. Variable manual-soldering charges for carrier / mux / output
are $1.39 / $0.33 / $1.06 in the minimum case, $1.39 / $0.33 / $2.64 for two
controllers, and $3.37 / $0.83 / $5.28 for five. Charged Extended part-type
fees are $55.62 / $12.36 / $37.08, then $55.62 / $12.36 / $33.99, then
$52.53 / $12.36 / $30.90. Component purchases and SMT placement are included
in the totals above. Do not add these fees or excess parts again.

## Inputs and limits

JLC detected the current outlines and copper counts correctly:

| Board | Current outline | Five bare PCBs | Ten bare PCBs |
| --- | --- | ---: | ---: |
| Carrier | 95×80 mm | $8 | Not requested |
| Single output | 90×87 mm | $8 | $14 |
| Sensor mux | L-shaped, 80×40 mm overall | $8 | Not requested |

Fabrication totals are $24 / $24 / $30, already included in the job prices.
Settings are four layers, 1.6 mm FR4, green mask, leaded HASL, 1 oz outer /
0.5 oz inner copper and normal lead time. The current Economic rules allow
two or five assemblies from five fabricated boards, and ten from ten.

The exact-part change retains source/pad identities and pin-net connectivity.
Both revised boards pass physical DRC with no opens; independent copper,
isolation-screen and drill audits are recorded in the
[verification evidence](../hardware/controller/verification.md). New exact
footprints have manufacturer-derived dimensions, but actual parts, lead forming,
assembly centroids/rotations, enclosure access and physical electrical/thermal
qualification still need review before manufacture. Quote acceptance does not
establish manufacturing readiness.

| Native board | SHA-256 |
| --- | --- |
| motley-carrier.kicad_pcb | `543eabf96cbf424bb785e4668c660ce4672964dfbb7659c98546d38dede6ba70` |
| motley-ac-output.kicad_pcb | `ef9f7dc9058d4277370079e7154b7d21aaaf9b22b9fc3009f056eecf6194d85f` |
| motley-sensors.kicad_pcb | `cccc0aa9f2753b86abd544f71891ea86f915e3018359fc6a2738d2dcd71f50aa` |

Fresh exports, source hashes, actual reference-level matching, requests/responses
and fee reconciliations remain temporary evidence under
`/tmp/agents/PUOfdDTNUf/assembly-integration/quote-inputs/` and `quote-live/`.
The repeatable process is the [quote skill](../.agents/skills/jlcpcb-quote/SKILL.md).
