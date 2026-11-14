# ADR-0013: USB-C internal Feather connection

- **Status:** Superseded by ADR-0014 (integrated controller); not implemented
- **Date:** 2026-11-12
- **Classification:** discretionary_design_choice
- **Related requirements:** `MOT-PROC-001`; preserve `MOT-PLAT-004`'s USB development interface
- **Related ADRs:** [ADR-0012](0012-automatic-usb-power-and-panel-port.md)
- **Affected components:** Internal carrier-to-Feather USB connection and USB cost estimate

## Context

The developer rejected an intermediate USB-A connector. The automatic RECOM
priority / optional USB backup and panel USB-C plan remains in scope. Native
CAD still contains the earlier manual JP1 circuit; this is a planning correction.

## Decision drivers

- Use USB-C for the internal connection to the unmodified Feather.
- Preserve automatic power preference and independent upstream host detection.
- Account explicitly for Type-C configuration instead of treating a C receptacle
  as a mechanical replacement for the rejected A receptacle.

## Options considered

| Option | Benefits | Costs and limitations |
| --- | --- | --- |
| Intermediate A receptacle and A-to-C cable | Ordinary cable termination | Rejected by developer |
| Internal C receptacle and short C-to-C cable | Replaceable cable and unmodified Feather | Requires correct source-side CC/attachment and VBUS control |
| Captive USB-C plug harness | Could remove the carrier socket | Exact harness, pinout, retention and CC implementation not selected |

## Decision

Replace the internal A socket and Adafruit 4472 with a carrier **USB-C source
receptacle and short data-capable C-to-C cable** to the Feather. Keep the panel
bulkhead -> carrier USB-C sink input, TPS2116 priority selection, upstream
raw-VBUS data gate, and separate RECOM-only output-driver supply from ADR-0012.
Do not join external host CC to the internal Feather CC connection.

Reserve source-side CC attachment detection, suitable current advertisement,
VBUS switching/discharge and current protection on the carrier-to-Feather port.
The selected 5 V feeds that controlled source port. Do not simply copy the
upstream sink's Rd resistors or assume two passive Rp resistors complete a
qualified source port. A Type-C controller such as TUSB320LAI is a research
candidate; exact controller/power-switch choices and cost remain pending.
Power that source controller from `FEATHER_5V_SELECTED` or an independent
regulator, not the Feather's 3.3 V output: that output cannot exist until the
source port turns on, so using it would create a startup deadlock. Keep the
raw-upstream-VBUS data gate separate from this downstream source controller.
Keep this an internal dedicated connection, not an externally accessible host
port, and verify both C-plug orientations, brownouts and ROM/application USB.

[Adafruit 6370](https://www.adafruit.com/product/6370) demonstrates an available
100 mm right-angle C-to-C cable with manufacturer-confirmed power/data/CC
connections, listed at $6.95. It is a packaging candidate, not a final cable
choice or a power-rating qualification. Check reach and plug orientation;
seek a lower-cost suitable cable before settling the cost estimate.

## Consequences

There is no USB-A connector in the planned internal topology. The previously
quoted $11-14 total used the rejected A-to-C implementation and is historical;
reprice the replacement cable and Type-C source support before giving a new
complete total. The bulkhead ($4.50) and TPS2116 ($1.05) planning prices remain
applicable. No native CAD, PDFs, firmware, hardware trace edges or purchases
change in this planning correction.

## Supersession

Supersedes ADR-0012's internal A receptacle, Adafruit 4472 selection and cost
total. Its other architecture and qualification obligations remain applicable.
Superseded by: None.

## References

- [TUSB320LAI Type-C port control](https://www.ti.com/product/TUSB320LAI)
- [TI: An Engineer's Guide to USB Type-C](https://www.ti.com/lit/eb/slyy228/slyy228.pdf)
- [Adafruit 6370](https://www.adafruit.com/product/6370)
