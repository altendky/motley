# Motley

Motley is a modular embedded-control project for building connected devices
without rebuilding the hardware integration and firmware infrastructure for
every application. The starting platform is ESP32-C6, C++, and Matter over
Thread, with Home Assistant as the initial integration target.

The first application is temperature control and humidity monitoring for an
animal enclosure. The broader goal is a reusable foundation for DIY sensing
and control: combine the boards you need, write application-specific behavior,
and reuse the sensor, output, storage and network integration.

**Early development:** the repository contains a buildable Matter identity
foundation and exploratory KiCad schematics and routed boards. Sensor drivers,
regulation algorithms, output-module firmware and the Matter application
interface are still to be implemented. The boards are designs to develop and
review, not tested products or a manufacturing release.

## Writing applications

The intended programming model keeps application decisions in a portable C++
core. It receives measurements, time and operation results, updates its state,
and describes the work it wants performed. Adapters handle sensors, outputs,
persistent storage and Matter; the same application logic can run in host tests
with controlled inputs.

For the enclosure application, that means concentrating on which sensor controls
which heater, setpoints, control modes, limits and fault responses. New
applications should be able to reuse the surrounding infrastructure rather
than couple their decisions directly to ESP-IDF or Matter APIs. This separation
is the [planned architecture](.rqml/adr/0001-portable-core-and-adapters.md);
an application framework and example application are still future work.

Extensibility includes separate sensor and output boards, addressed expansion,
and Qwiic access to both controller I2C buses. Additional interfaces, displays
and local controls are being considered. The hardware and software are intended
to grow through useful applications rather than require a fixed enclosure or
sensor/output count.

## First application: enclosure thermal control

The initial arrangement puts the controller outside a humid enclosure, with
remote temperature/humidity probes inside. Two independently controlled AC
heater or lamp outputs are planned, with a starting design target of **300 W
of resistive load per output at nominal 120 VAC**.

Planned output modes include slow, zero-cross-aligned whole-cycle switching for
heaters and phase-angle control for lamps. Each output module has its own MCU
for line-synchronous operation, current and voltage observations, and a series
cutoff relay. Temperature regulation will run locally in the device so it can
continue without Home Assistant or network access.

Exact regulation algorithms, sensor assignments, communication-loss policies
and the Matter control/reporting model are being defined. Higher output ratings,
international mains support and inductive loads are separate investigations;
the component ratings do not establish a finished system rating.

## Board designs

There are three KiCad designs. The initial two-output device uses one controller,
two copies of the output board and one sensor board. All currently use four
copper layers with ground/power planes and components on the front side.

| Board | High-level capabilities | Current outline |
| --- | --- | --- |
| [Controller and AC input](hardware/controller/motley-carrier.kicad_pro) | ESP32-C6 with 8 MB flash; Matter/Thread platform; isolated 5 V mains supply; automatic mains/USB logic-power selection; separately switched sensor supply; both I2C buses exposed through Qwiic; output connections and shared line timing | 95 × 80 mm |
| [Single AC output](hardware/controller/motley-ac-output.kicad_pro) | Local STM32 MCU; triac with random-phase isolated drive; series cutoff relay; isolated current/voltage feedback; branch fuse and configurable snubber; programming/recovery access | 90 × 65 mm |
| [Sensor multiplexer](hardware/controller/motley-sensors.kicad_pro) | Eight independently selected I2C branches with JST-SH/Qwiic-compatible connectors; selectable mux address; deployment and Qwiic upstream connections; cut-down layout for fewer ports | L-shaped, 80 × 40 mm overall |

The preferred expansion target is at least sixteen output boards, subject to
bus and power-budget work. Eight mux addresses provide sensor expansion, also
subject to electrical limits. These are design directions, not demonstrated
maximum configurations. Qwiic is a 3.3 V interface here; it is not the mains or
output-actuator power connection.

See the [board images](hardware/controller/generated/board-images/README.md)
for each copper layer, and the [hardware guide](hardware/controller/README.md)
for interfaces, preliminary parts and remaining engineering work.

## First development-build budget

These are **planning ranges in USD, rounded to the nearest $25**, updated
2026-11-15 for the four-layer, intelligent-output design. They combine earlier
JLCPCB Economic assembly prices with allowances for the newer electronics and
hand-fitted parts; they are not quotes for the current boards.
Fresh bare-PCB prices have been obtained from the current Gerbers; the updated
assembly quote still requires authenticated API matching.

One complete controller means one controller board, one eight-port sensor board
and two output boards. Small-order minimums mean paying for spare boards even
when finishing only one device.

| Completed controllers | Boards assembled: controller / sensor / output | Estimated total batch cost |
| --- | --- | ---: |
| 1, smallest previously observed Economic assembly order | 2 / 2 / 2 | $275–$325 |
| 2 | 2 / 2 / 5 | $375–$425 |
| 5 | 5 / 5 / 10 | $650–$750 |

The allowance includes PCB fabrication and partial factory assembly, parts to
finish the required boards, heatsinks, mains cord/entry, outlets, panel USB and
internal wiring. Remaining parts require hand assembly. It excludes probes and
extensions, enclosure/mounting hardware, tools, shipping, tax and tariffs.
The selected [7Semi SHT45 probes](https://7semi.com/7semi-sht45-digital-humidity-and-temperature-sensor-probe/)
are about $13 each; probe count is independent of the eight available ports.

See the [budget basis](docs/development-build-costs.md) for quantity assumptions,
design-change allowances and uncertainty. Part sourcing and assembly eligibility
can materially change these figures.

## Explore or contribute

- [Open work](https://github.com/altendky/motley/issues): current hardware,
  application and integration decisions.
- [Hardware candidates](docs/hardware-candidates.md) and
  [output-module design](docs/ac-output-module.md): component research and
  architectural context.
- [Development tools](docs/tooling.md), [firmware build](docs/firmware-build.md)
  and [Matter development](docs/matter-development.md): working with the code.
- [Requirements](requirements.rqml) and [architecture decisions](.rqml/adr/):
  agreed obligations, draft proposals and their rationale.

The first useful contributions are likely to be application design, firmware,
hardware review and practical packaging. Requirements distinguish planned
behavior from implementation and verification; build and CAD checks alone do
not establish that the assembled device works.
