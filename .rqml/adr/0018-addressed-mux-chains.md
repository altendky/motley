# ADR-0018: Addressed mux boards with upstream chains and branches

- **Status:** Accepted for the exploratory hardware study
- **Date:** 2026-11-13
- **Classification:** discretionary_design_choice
- **Related requirements:** MOT-PROC-001, MOT-HW-003; draft MOT-HW-001/004/009/010/011/012, MOT-SENS-005/006
- **Related ADRs:** ADR-0016, ADR-0017
- **Affected components:** Carrier Qwiic leaf, mux and upstream interfaces, PCB placement, review PDFs

## Context

The developer accepted selectable mux addresses, upstream chaining and extra
carrier accessory sockets. TCA9548A offers three address bits; its eight sensor
outputs remain switched branches rather than upstream chain connections.

## Decision drivers

- Use several mux boards on one bus without address collisions.
- Permit chains or branches without sacrificing the deployment reset wire.
- Keep address pins defined with switches open and cables absent.
- Avoid excessive pull-ups as more boards join a shared bus.

## Options considered

| Option | Benefits | Costs and limits |
| --- | --- | --- |
| Carrier branching only | Short individual feeds | Requires more carrier sockets or a hub; no direct board chaining |
| Qwiic chaining only | Standard cables | Four wires omit shared reset |
| Both upstream connector pairs and carrier branching | Flexible bench and five-wire deployment topology | Extra connectors, address configuration and shared-load review |

## Decision

Provide two sockets for each carrier I2C controller; duplicates are electrically
parallel on that bus. Keep the controllers independent. On every mux provide
two upstream Qwiic sockets and two five-pin deployment headers, the latter
passing through shared reset as well as power, GND and I2C. Keep these parts in
the fixed common area; its width may grow behind more connector positions.

Use a three-position DIP switch to connect A0/A1/A2 individually to local 3.3 V,
with separate 10k pull-downs. OFF = 0, ON = 1; mark binary weights 1/2/4.
Set addresses before powering the bus. All OFF gives 0x70; duplicate addresses
on one bus are not supported. Factory switch position must be checked rather
than inferred from the desired baseline setting.

Give each upstream 4k7 pull-up a separate removable 0-ohm link. Removing both
does not connect SDA and SCL through a shared floating feed. Reset bias and
downstream per-port pulls remain independent. Configure the aggregate pull-ups
for the actual connected boards; eight available addresses are not a qualified
eight-board electrical/current/cable rating.

Carrier sockets remain power outputs from the switched sensor rail. Qwiic
upstream sockets share one connector-side power node and removable local link;
five-wire deployment rails/reset pass directly through. Use one supply/host,
avoid loops between chains and branches, and assess current through every feed
segment. No automatic source isolation or added current limiter is implied.

## Consequences

Shared five-wire reset resets all connected muxes. Four-wire-only boards need
power-cycle or separate reset access for hardware recovery. Firmware must clear
the previous mux selection before enabling another; writing a different mux
does not clear selections already latched elsewhere. Record that future
obligation as MOT-SENS-006 without claiming firmware implementation here.
Heater pulses continue after channel deselection and remain part of the combined
power budget. All boards remain unrouted studies awaiting physical validation.

## Supersession

Supersedes only ADR-0017's single-socket counts and fixed mux upstream pull-ups.
Its pinouts, retained deployment link, shared switched supply and bounded bench
power assumptions remain applicable. Superseded by: None.
