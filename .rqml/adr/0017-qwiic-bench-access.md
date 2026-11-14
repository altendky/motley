# ADR-0017: Qwiic access alongside the deployment link

- **Status:** Accepted for the exploratory hardware study
- **Date:** 2026-11-13
- **Classification:** discretionary_design_choice
- **Related requirements:** `MOT-PROC-001`, `MOT-HW-003`; draft `MOT-HW-001/002/004/009/010`, `MOT-SENS-005`
- **Related ADRs:** ADR-0014, ADR-0015, ADR-0016
- **Affected components:** Carrier and sensor interfaces, native CAD, review PDFs

## Context

The developer requested separate Qwiic sockets for both ESP32-C6 hardware I2C
controllers and an upstream Qwiic input on the mux for flexibility and bench
work, explicitly retaining the five-pin deployment interface and reset wire.

## Decision drivers

- Keep deployment wiring and independent MCU control of mux reset.
- Permit either carrier bus to serve peripherals without the mux attached.
- Permit standalone mux bench operation without a custom five-wire harness.
- Preserve single-side assembly, top touch access and the preferred board sizes.

## Options considered

| Option | Benefits | Costs and limits |
| --- | --- | --- |
| Replace the deployment link with Qwiic | One connector family | Loses the separate reset wire; rejected by the developer |
| Retain five pins and add bench sockets | Direct standard-cable access to both buses and mux | Requires local pulls, protection and explicit single-source/host use |
| Add automatic power and data-source isolation | Could support more simultaneous connections | Additional circuitry and qualification beyond this bench-access request |

## Decision

Keep carrier J13 and sensor J12 unchanged. Add carrier J23 for GPIO19 SDA /
GPIO18 SCL, and J24 for LP GPIO6 SDA / GPIO7 SCL. Add sensor J11 for the same
upstream bus as J12. All new sockets use Qwiic pin order 1 GND, 2 3.3 V,
3 SDA, 4 SCL. Sensor reset stays on the deployment link and locally biased.

Power both carrier sockets from switched `+3V3_SENS`, avoiding a new connection
between independent main and sensor regulator outputs. Provide removable 0-ohm
power links; these are configuration components, not automatic isolation.
Add carrier-local 10k main-bus and 4k7 LP-bus pull-up pairs. Retain the mux's
4k7 upstream pulls for standalone operation. Add protection at the new carrier
entries and keep the mux input adjacent to existing upstream protection.

Carrier sockets supply peripheral power: do not feed them from an external
host's supply. For a standalone mux, unplug the five-pin deployment cable and
use one Qwiic host and supply. Do not drive signals into an unpowered board;
removing a power link does not isolate SDA/SCL. AP2112 output discharge means
EN low is not isolation from externally supplied power. Existing off-domain
reset/pull concerns remain qualification work.

## Consequences

One new carrier schematic leaf and three sockets add bench flexibility without
changing deployment pinout or implementing firmware. The short upstream cable
must carry all attached probe currents. Keep one SHT heater pulse active at a
time, track pulse completion even after deselection, and include both buses'
loads in the shared rail budget. The conservative Qwiic cable guideline is not
the same as the SH contact rating or the regulator's nominal current rating.
No new cable-length, continuous-load, hot-plug or ESD-immunity rating is claimed.

## Supersession

Extends ADR-0014's sensor-supply and interface arrangement without replacing its
five-pin deployment link. Other prior decisions remain applicable.
Superseded in part by [ADR-0018](0018-addressed-mux-chains.md) for socket counts,
selectable mux addresses and configurable upstream pull-ups.
