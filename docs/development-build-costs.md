# Development-build budget basis

Updated 2026-11-15. These are planning allowances for the current four-layer
designs, not a current BOM match or vendor quotation. One complete controller
uses one controller/AC-input board, one sensor mux and two identical output
boards. The README rounds the estimated batch ranges to the nearest $25.

## Quantities and included hardware

The 2026-11-13 JLCPCB Economic quotation exercise observed these quantities:

| Finished controllers | Fabricated: controller / mux / output | Factory assembled: controller / mux / output |
| ---: | --- | --- |
| 1 | 5 / 5 / 5 | 2 / 2 / 2 |
| 2 | 5 / 5 / 5 | 2 / 2 / 5 |
| 5 | 5 / 5 / 10 | 5 / 5 / 10 |

The minimum case therefore pays for a spare controller and mux assembly; the
two-controller case pays for a spare output assembly. Only boards needed for
the finished controllers receive the remaining hand-fitted parts. This is the
smallest previously observed Economic order, not an optimization across every
assembly service or an all-hand-soldered build.

The budget includes PCB fabrication, partial factory assembly, remaining board
components, output heatsinks/interfaces, cord entry, two outlets per controller,
panel USB and consumed internal wiring. It assumes the retained Omron cutoff
relays and a captive mains cord. A detachable entry can change the allowance.

It excludes sensor probes/extensions, enclosure and mounting hardware, tools,
shipping, tax/tariffs, and buying whole spools or containers beyond the consumed
allowances. Hand assembly time is not priced. Spare factory assemblies are not
assumed to be fully hand-completed. The selected
[7Semi ES-12289 probe](https://7semi.com/7semi-sht45-digital-humidity-and-temperature-sensor-probe/)
is listed at $13; the number purchased need not equal the eight available ports.

## Reconciliation with earlier estimates

The saved November 13 mixed-assembly estimates, including manual completion
and captive-cord/offboard allowances, were $228–238 for one controller,
$291.17–311.17 for two, and $509.16–559.16 for five. These describe the earlier
two-layer output design without local MCUs and feedback. They are historical
inputs, not prices for the current design.

The current planning calculation adds:

- Four-layer fabrication: approximately $12 per batch for the first two cases
  and $17 for five controllers, from November 14 calculator comparisons at the
  current board sizes. The extra charge applies to fabricated spares too.
- New output electronics: about $15 per factory-assembled output for small
  quantities, falling toward $12.50 at ten. This covers the MCU, isolated current
  and voltage observations, random-phase driver and supporting circuitry.
- Shared line reference and support: about $10 per factory-assembled controller
  board, including the spare in the minimum case.
- The MEAN WELL supply replacing the earlier RECOM: approximately $7 saved per
  finished controller. The minimum case may incur the cost of an additional
  supply on its spare factory assembly.

Those adjustments give illustrative subtotals around $283–293, $384–404 and
$666–716. Allowing for additional part-loading/assembly charges, support parts,
quantity effects and rounding gives the README's **$275–325 / $375–425 /
$650–750** planning ranges. These are approximate budget bands, not guaranteed
upper/lower bounds or a claim that the old assembly matches remain valid.

## Price references and uncertainty

Current small-quantity price checks supporting the electronics allowances:

| Part | Observed USD price | Source |
| --- | --- | --- |
| STM32C011F6P6 | About $1.47 each; $1.23 at ten | [JLC C5456198](https://jlcpcb.com/partdetail/STMicroelectronics-STM32C011F6P6/C5456198) |
| MEAN WELL IRM-05-5 | About $4.93 | [JLC C48603696](https://jlcpcb.com/partdetail/50875454-MW_PCB_AC_DC_5W_IRM_055/C48603696) |
| TMCS1123B5AQDVGR | $5.25 each; $4.51 at ten | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TMCS1123B5AQDVGR/22116895) |
| ACPL-K370-500E | $5.16 each; $3.78 at ten | [Mouser](https://www.mouser.com/ProductDetail/Broadcom-Avago/ACPL-K370-500E?qs=WpC4P%252BDU3FkkR3M3Qiegkg%3D%3D) |
| ACPL-K376-000E | $7.38 each | [Mouser](https://www.mouser.com/en/ProductDetail/Broadcom-Avago/ACPL-K376-000E?qs=WpC4P%252BDU3FnO2YOR%2FlQ05Q%3D%3D) |
| VO3053-X007T | $1.16 each; $0.81 at ten | [DigiKey](https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/VO3053-X007T/2355056) |

[JLC's published assembly fees](https://jlcpcb.com/help/article/pcb-assembly-price)
include $8.18 setup, $1.53 stencil and $3.07 per Extended component type.
Distributor prices are sourcing references, not confirmation that JLC can
assemble the exact variants. The earlier totals already included setup and
Extended-part fees for their matched BOMs; only changes belong in the allowance.

Current BOM matching, stock, component attrition/minimum purchases, exact
heatsink/connector selections, insulation/thermal requirements and enclosure
choices can materially change the result. See the
[hardware guide](../hardware/controller/README.md) for the current design and
its unresolved choices. No purchasing or new quotation submission is implied.
