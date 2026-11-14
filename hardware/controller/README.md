# Exploratory modular controller

Status: unrouted design experiment, revised 2026-11-14; not a fabrication release.

The [intelligent-output review](intelligent-output-review.md) records the current
pin, default-state, power and ESD assessments, including the complete fresh
component/pin inventory. It supersedes the earlier direct-GPIO output portions
of the [pin-bias review](pin-bias-review.md). Output boards now have local MCUs,
isolated current/voltage observations and a shared buffered line reference.
Sensor-enable remains GPIO11 with a local 10k pull-down; sensor-bus reset pulls
still need off-domain review. Loaded drive, temperature/leakage, power budgets,
timing and contact-loss transients remain unqualified. Structural checks do not
close draft `MOT-HW-001/002` or qualify hardware defaults.

Native files now have hidden `Requirements` fields and explicit RQML links.
`uv run scripts/hardware_trace.py` checks 20 native source files and all 257
design footprints by hierarchical UUID identity. The fields record electrical
design applicability; MOT-HW-003 file links cover annotation integrity and
whole-file drift, not completion of the draft electrical requirements.
The fresh schematic inventory is 247 components / 706 symbol-pin identities
across the three designs; two output copies give 319 components / 897 pins per
complete unit. The 257 PCB footprints include ten board-only mechanical items.

The [ESD and access review](esd-access-review.md) records the added connector
clamps, per-port 100 ohm series resistors, marked local-GND touch copper and
optional wire-loop/post probe points. Its previous $3.31 protection estimate is
historical; the additional output bus/SYNC/power protection has not been requoted.
Bare access features require no purchased contacts. All fitted sensor components,
including
upstream clamps D60/D61 and the bare touch pad, are on the front. All boards
have top-side touch access, and assembly remains single-sided. System ESD,
clamp coordination, panel CC/shield and touch/clip qualification remain open.

## Scope and requirements boundary

This KiCad study makes the discussed controller, mux, probe and heater choices
concrete for review. The developer selected **three designs and four physical
boards per unit**: one integrated ESP32-C6 controller with AC input and isolated supply, two identical
single-output AC modules, and one mux with sensor connectors.
[ADR-0011](../../.rqml/adr/0011-single-output-modules-and-sensor-core.md)
records the board partition; [ADR-0014](../../.rqml/adr/0014-integrated-controller-and-switched-sensor-supply.md)
records the integrated controller and sensor supply. [Hardware candidates](../../docs/hardware-candidates.md)
records preliminary parts and unresolved engineering questions.

Under `MOT-PROC-001`, this remains a scoped exploratory exception for reviewing
schematics, interfaces, placement and trimming geometry before agreeing maintained
hardware requirements. It does not approve a mains design, implement firmware,
or qualify a PCB. `GOAL-MOT-SENSING` and `MOT-SENS-005` remain draft. Native
traceability tooling implements approved MOT-HW-003, while the electrical
study uses design-input relationships without claiming hardware verification.

The boards contain schematic nets and ratsnests but **no tracks, vias or copper
pours**. Footprint qualification, routing, enclosure design, manufacturing files,
purchasing and energization remain outside this experiment. Passing structural
checks does not establish mains safety or functioning trimmed boards.

## Open and review

Open any of these KiCad 10 projects in this directory using the
[pinned mise installation](../../docs/tooling.md#kicad); each has its own matching
root schematic, netlist and PCB:

| Project | Quantity per unit | Physical contents | Trial outline |
| --- | ---: | --- | --- |
| [motley-carrier.kicad_pro](motley-carrier.kicad_pro) | 1 | WROOM-N8, panel USB harness interface, automatic power selector, separate controller/sensor regulators, AC input, main fuse, MEAN WELL IRM-05-5, shared isolated line reference and inter-board connections | 100 x 85 mm |
| [motley-ac-output.kicad_pro](motley-ac-output.kicad_pro) | 2 identical copies | One output: STM32C011 and local logic supply/recovery, random-phase optotriac/triac, cutoff relay, isolated voltage/current feedback, branch fuse, configurable snubber, outlet and heatsink reservation | 100 x 90 mm |
| [motley-sensors.kicad_pro](motley-sensors.kicad_pro) | 1 | TCA9548A and support parts, upstream interface, eight QT sensor ports with pull-ups | L-shaped, 80 x 44 mm overall |

The former `motley-controller` monolithic root/project/PCB is replaced by these
three projects. Shared libraries remain in this directory. No board is panelized
with another, and no mechanical mating height or installed orientation is fixed.
The shapes are movable starting geometry, not minimum-size or enclosure claims.

**Board-size target:** keep each individual board's overall outline width and
height at or below **100 mm**, including the full untrimmed sensor board.
Exactly 100 mm meets the target. If design work suggests either dimension may
need to exceed it, raise the proposed size, reasons and alternatives with the
developer before proceeding with that enlargement. Larger boards can be agreed;
this is a strong target and discussion trigger, not a hard dimensional limit.
The sensor common area's width/depth trade remains flexible within this target.
Draft `MOT-HW-007/008` record the target and review process respectively.

All functional groups are unlocked. Hover an item and press **M** to move its
native group; enter the group to move individual items. The sensor core and bank
are grouped separately; the output module has separate power/MCU, heater,
feedback and access groups. The carrier keeps separate controller, USB/selection,
regulator, input/supply, shared line-reference and interface groups. Mounting
locations and the WROOM antenna reserve are provisional. Isolation corridors are
drawings, not qualified clearance rules.

## Inter-board connections

The connector numbers below define signal correspondence, not an approved
harness or rated connector selection. Low-voltage 2.54 mm pin headers are study
placeholders; short ordinary pins may join matching plated holes when the
mechanical arrangement is settled. Mechanical-only plated support holes are
isolated from circuit nets. Mains uses its separate terminal connection and must
never use the signal-header interface.

| Link | Mating references | Pin order |
| --- | --- | --- |
| Sensor low voltage | Carrier J13 to sensor J12 | 1 GND, 2 switched 3V3_SENS, 3 SDA, 4 SCL, 5 mux RESET_N (GPIO21) |
| Output 1 low voltage | Carrier J15 to first output module J14 | 1 GND, 2 selected logic 5 V, 3 LP_I2C_SDA, 4 LP_I2C_SCL, 5 LINE_SYNC, 6 raw +5V_SYS |
| Output 2 low voltage | Carrier J18 to second output module J14 | Same six shared signals as output 1 |
| Output 1 mains | Carrier J16 to first output module J17 | 1 AC_L_FUSED, 2 AC_N, 3 PE |
| Output 2 mains | Carrier J19 to second output module J17 | 1 AC_L_FUSED, 2 AC_N, 3 PE |

Carrier contact 2 is `+5V_SELECTED`; the corresponding output net is `+5V_LOGIC`.
It feeds the output's local `+3V3_OUT` regulator, permitting USB-powered logic
commissioning without powering the raw 5 V relay/opto actuators. These two rails
are not tied together on the output. All boards share low-voltage GND.
Each module's MCU drives its own local `HEAT_EN`/`CUT_EN`; identity and a configured
I2C address determine the logical output, rather than the chosen carrier socket.
Each module's J10 is its own outlet; physical copies are not separate schematic
instances. Shared LINE_SYNC requires the same AC source/phase at every output.
Full and partial unplugging, missing GND and separately powered bus endpoints
remain unqualified.

The main fuse is on the carrier; each heater retains its branch fuse on the
output board. Neutral and PE continue to both outlets. PE is not low-voltage
GND. The isolated supply remains ahead of heater switching so the controller
stays powered. The signal names apply to the current experiment; connector
ratings, wire sizes, source isolation and protective-earth implementation remain
engineering work.

## Optional Qwiic bench interfaces

The five-pin J13/J12 deployment link above is retained, including mux reset.
Six additional four-pin JST-SH sockets use standard Qwiic order:
**1 GND, 2 3.3 V, 3 SDA, 4 SCL**.

| Socket | Bus | Power contact |
| --- | --- | --- |
| Carrier J23/J25, HP pair | GPIO19 SDA / GPIO18 SCL, also used by J13 | Switched sensor rail through individual removable R44/R46 = 0 ohm; power OUT |
| Carrier J24/J26, LP pair | GPIO6 SDA / GPIO7 SCL; independent low-power I2C controller and shared output bus | Main +3V3 through individual removable R45/R47 = 0 ohm; power OUT |
| Sensor J10/J11 | Parallel mux upstream SDA/SCL, also used by J12/J13 | Shared connector-side power enters through removable R50 = 0 ohm |

Carrier-local pull-ups are 10k on the HP sensor bus to switched `+3V3_SENS`
and 4k7 on the LP bus to main `+3V3`, one pair per bus rather than per socket.
The mux keeps its local 4k7 upstream pull-ups
through separately removable R55/R56 = 0 ohm and retains its reset pull-up,
so it can be used without the carrier. Carrier port TVSs protect each signal pair and power
contact; the mux inputs share existing upstream protection. The farther J10
entry is roughly 20-26 mm from those clamps, so final routing may require local
protection. Entry/clamp/return geometry remains unqualified. The
carrier bench leaf is [qwiic-bench.kicad_sch](qwiic-bench.kicad_sch).

For standalone mux bench operation, **disconnect deployment links to another
host or supply**. Mux-to-mux five-pin links may pass through the same bench bus.
Use one controlling host and one power source on a connected bus. Carrier
Qwiic ports supply peripheral power; do not feed them from an external host's
power output. Removing a 0-ohm power link permits a separate peripheral supply
only with compatible powered bus endpoints: it does not isolate SDA/SCL or
permit driving an unpowered controller. Sensor-rail EN low is not isolation;
the regulator has an output-discharge path. The existing off-domain concerns
remain open. Enable sensor power and wait for startup before transactions.

Keep one SHT45 heater pulse active at a time across the connected system,
tracking its completion even if the mux channel is deselected. Its strongest
heater can draw 100 mA maximum; roughly 110 mA including other sensors/pulls
is an illustrative load, not a qualified budget. SparkFun gives a conservative
226 mA cable guideline. Include both buses' peripherals, USB entitlement,
regulator heating and cable drop before adding higher loads. The regulator's
600 mA headline rating is not an allowance per socket.
[SHT4x electrical limits](https://sensirion.com/media/documents/33FD6951/6A7C10A0/HT_DS_Datasheet_SHT4x_V7.3.pdf),
[Qwiic guidance](https://www.sparkfun.com/qwiic),
[AP2112 output discharge](https://www.diodes.com/datasheet/download/AP2112.pdf).
ADR-0017 and draft MOT-HW-009/010 record the interface direction; no firmware,
hot-plug, cable-length, load or ESD qualification is claimed.

## Multiple mux boards and addressing

Sensor SW1 is a three-position CTS 219-3MSTR DIP switch (JLC C3012353).
Each switch connects an address input to local 3.3 V, with a separate 10k
pull-down. OFF = 0, ON = 1; positions 1/2/3 have weights 1/2/4 for A0/A1/A2.
Address = **0x70 + A0 + 2*A1 + 4*A2**. All OFF selects 0x70. The selected
suffix ships ON, so set the desired unique address with power off; factory
position is not the configured baseline. The generic CTS-family land pattern
is preliminary, including actuator/height and assembly checks.

Sensor J12/J13 pass through all five deployment signals, including shared reset;
asserting reset affects all muxes on that reset chain. J10/J11 are parallel
upstream Qwiic connectors. Daisy-chain through these upstream connectors,
not through the eight switched sensor branches. Four-wire chains omit reset;
use power-cycle or separate reset access if hardware recovery is needed.

Carrier duplicate sockets permit branching on either bus. Choose chains or
branches without loops, duplicate supplies or extra controlling hosts. Upstream
Qwiic power contacts share their connector-side node: removing sensor R50
does not isolate those two external power sources from one another.

R55/R56 independently disconnect mux R2/R3 pull-ups. Remove excess upstream
pull-ups for the actual shared-bus load; ensure some suitable pulls remain.
Separate links avoid coupling SDA and SCL through a floating common resistor
feed. Downstream per-port pulls and local reset bias remain unchanged.

There are eight selectable mux addresses per bus, not a qualified eight-board
current/cable limit. All connected power, capacitance and pull-ups accumulate.
Firmware must deselect the previous mux before selecting another; writing a
different mux address does not clear the first device's latched selection.
Keep only one downstream branch visible across a bus when using identical-
address sensors. Draft MOT-SENS-006 records that future scheduler obligation;
no firmware behavior is implemented here. See ADR-0018.

## Sensor trimming plan

The common mux/interface area has no fixed width in connector positions. It
can trade width along the connector row against depth behind it; the row sets
the full board length. [ADR-0016](../../.rqml/adr/0016-flexible-sensor-core-aspect-ratio.md)
records this clarification. The geometry below describes the current placement
snapshot. Wider common circuitry would change the minimum retained cut-down
width and require the cuts to be reassessed.

The sensor board's long arm is 18 mm deep. Its 49 mm wide fixed leg contains the
mux, reset pull-up, decoupling, fitted upstream pull-ups, protection and five-pin interface.
The eight horizontal JST-SH sockets face the same enclosure wall at 10 mm center
spacing. Connector envelopes and end margins determine the 80 mm board length;
the core is entirely behind the first five connector positions. Side-wall
rotation and protrusion remain enclosure questions.

The three marked cuts retain ports **0 through N-1**, for N = 5 through 7;
the complete board retains all eight. Each removed port takes its two pull-ups
with it. Relative to the outline's upper-left corner, connector centers are at
x = 5 + 10*i mm and cut centers are x = 50, 60 and 70 mm. The
fixed leg survives every cut. An unwanted socket can be omitted or removed;
that does not require cutting away the core behind it. The layout reserves a
nominal 1 mm kerf and
0.25 mm positioning allowance; the cutting process is not selected or qualified.

Later routing must keep all required core and retained-port connections on the
retained board. Downstream conductors must cross earlier cut lines, so those
lanes cannot be completely copper-free. Use deliberate separated crossings,
exclude pours/pads/vias from the cutting corridor, and provide post-cut edge
clearance, deburring and short/continuity checks. The present unrouted geometry
only demonstrates component retention, not electrical cut-down operation.

## Shared circuits and repeated placement

- [heater-channel.kicad_sch](heater-channel.kicad_sch) is instantiated once in
  the AC-output design. Build two copies of that board for two outlets. Its
  local MCU supplies its `HEAT_EN`/`CUT_EN` controls; `TRIAC_A1` stays local.
- [sensor-port.kicad_sch](sensor-port.kicad_sch) is instantiated eight times by
  [sensor-ports.kicad_sch](sensor-ports.kicad_sch). Each port has its own SDA/SCL
  pair and two pull-ups; power and ground are intentionally shared.

Native KiCad **Repeat Layout** was exercised on the earlier combined study.
This revision retains one heater's geometry on the output module and places the
sensor instances at 10 mm pitch. These transforms were applied programmatically;
no new GUI repeat/autoplace operation is claimed. One heater and eight sensor
placement areas remain. Output reuse comes from building one board twice;
sensor ports still have repeated placement within one board.

To propagate a sensor template placement edit, enter its group, select
`SENSOR_PORT_0`, then use **Tools -> Multi-Channel -> Repeat Layout**. Enable
footprint placement only; disable routing, other-item copying, target grouping
and locked-item overrides. Review the result and DRC. Editing the shared
schematic changes its instances, but PCB placement only propagates when copied.

## Review exports and footprint limitations

The two combined review files retain their original paths:
`review/motley-controller.pdf` contains all three schematics (24 pages), and
`review/motley-controller-placement.pdf` contains the three front placements
(three pages). Both use carrier, AC output, then sensor board order, with a
bookmark for each board. These PDFs remain current even though the native
monolithic project has been retired.

Each project's ignored `review/` exports include a schematic PDF, placement PDF,
XML netlist and JSON ERC/DRC reports. Regenerate, for example:

```sh
kicad-cli sch export pdf hardware/controller/motley-carrier.kicad_sch \
  --output hardware/controller/review/motley-carrier.pdf
kicad-cli pcb export pdf hardware/controller/motley-carrier.kicad_pcb \
  --output hardware/controller/review/motley-carrier-placement.pdf \
  --layers F.Cu,F.SilkS,Dwgs.User,Edge.Cuts --mode-single --black-and-white
```

Use the other project basenames for their exports. The PDFs omit the interactive
ratsnest available in PCB Editor. The carrier schematic has seven pages, the
single-output module has five, and the sensor project has twelve, including eight
shared-port instances. The output design is shown once; build two copies.

Seven blank schematic footprint fields still have board-only
study assignments: fuse holders, mains terminals, relays and snubber R/C parts.
Their schematic-parity warnings remain explicit. New mains terminals use the
same 7.50 mm stock footprint as a packaging placeholder. This selects no rated
terminal for purchase. The 10 mm-pitch capacitor pattern does not qualify an X2
part. Review these assignments when updating the PCB from its schematic.

The local G6DN pattern derives from Omron's package drawing: pins 1, 2, 5 and 8
at 0, 2.54, 10.16 and 17.78 mm, with provisional 1.1 mm drills and 2 mm pads.
Check viewing direction, tolerances and actual parts. The module's 35 x 29 mm
heatsink drawing reserves 12 mm nominal height; triac mounting, clip/interface
selection and heat flow are not qualified.

`U10` is the ESP32-C6-WROOM-1-N8 module. Its symbol and footprint derive from
Espressif's KiCad library tag 3.0.1, with a local library path and omitted
unavailable external 3D model; see [license](Espressif-LICENSE.md). All nine
center pads are numbered 29 and connected to GND, along with pins 1/28.
Both symbol units
of each G6DN are one physical relay. Logical AC connector numbering does not
establish manufacturer terminal numbering on the inlet, cord or outlets.


## Circuit choices and open questions

- The accepted sensor is the standard **7Semi ES-12289, non-membrane** stainless
  tube with 1 m factory lead. Eight connector positions provide expansion;
  eight probes are not a selected purchase quantity. The 7Semi wire-color map
  is unverified; terminate by signal, not an assumed color convention.
- Carrier GPIO1 / module pin 9 observes shared LINE_SYNC through R87=1k;
  GPIO4 is an unused strap, and former direct output GPIO0/2/3 are NC.
  GPIO6/7 carry LP output I2C; GPIO21 pulls mux reset low; GPIO18/19 are HP SCL/SDA.
  GPIO11 enables the separate sensor rail;
  GPIO10 drives a status LED. GPIO12/13 are USB D-/D+. Reset/boot buttons,
  EN 10k/1u RC, GPIO8/9 pull-ups and a 3.3 V UART service header provide recovery
  access. No firmware behavior is added by these drawings.
- The Feather and JP1 are removed. [usb-power.kicad_sch](usb-power.kicad_sch)
  shows TPS2116 selection with mains-derived 5 V at VIN1, USB at VIN2 and MODE tied to VIN1.
  The 316k/100k, 0.1% priority divider has an approximately 4.16 V typical
  threshold; TI's reference tolerance alone spans about 3.82-4.50 V. The
  relay/opto supplies remain on raw mains-derived 5 V, ahead of the selector;
  the output MCU/feedback logic receives selected 5 V separately. Source transfer,
  backfeed, current/inrush/suspend budgets and thermal behavior remain untested.
- PS1 is now MEAN WELL IRM-05-5 / JLC C48603696, isolated 5 V at 1 A.
  The stock four-pin symbol/footprint replaces RECOM: 1 neutral, 2 fused line,
  3 secondary GND, 4 raw 5 V. The 45.7 x 25.4 x 21.5 mm body fits the current
  100 x 85 mm study outline. Mains-first supply priority and the
  Omron G6DN-1A-L DC5 cutoff relay remain selected. The 1 A supply is not a
  qualified sixteen-active-output power budget; two-output and USB-only logic
  operation also need actual peak/current/inrush accounting.
  Ripple, inrush, fuse coordination and enclosed-temperature behavior need
  qualification. Earlier JLC quotation exports describe the previous supply
  and placement; regenerate them before relying on a new manufacturing quote.
- J21 is the provisional Adafruit 6153 panel USB-C harness interface, with a
  six-position JST-PH header. Its pin order is a **project-defined placeholder**:
  1 VBUS, 2 GND, 3 D+, 4 D-, 5 CC1, 6 CC2. Verify the actual harness and repin
  it or revise the board before use. CC pins are not connected on this board;
  the assembly has built-in separate sink pull-downs. A more robust shielded
  cable, defined shell termination, strain relief and panel retention remain
  explicitly unsatisfied preferences. The 175 mm loose-wire harness is not a
  qualified USB or ingress solution.
- U23 TS3USB221ERSER connects USB data only when raw host VBUS is valid.
  U24 TLV3011BIDBVR compares a 226k/100k VBUS divider to its 1.242 V reference;
  approximately 4.05 V typical enables the active-low data gate. A 47k pull-up
  defaults to disconnect; the B variant's fail-safe inputs and POR behavior
  matter. D20 USBLC6-2SC6 is an ESD starting point. This hardware path is
  independent of application firmware, including ROM flashing, but actual
  sequencing, both plug orientations and operation during heater switching
  need physical tests. Host current entitlement is not established by sink Rd.
- Two AP2112K-3.3TRG1 regulators draw in parallel from selected 5 V. The main
  rail powers the ESP; GPIO11 and a local 10k pull-down control the separate
  sensor rail. The mux, reset pull-up, upstream pull-ups and all sensor ports
  share switched `+3V3_SENS`, retaining the five-wire board link. Grounds are
  common. Keep SDA/SCL/RESET_N high impedance without internal pull-ups while
  off; enable the rail and wait for startup before I2C. Actual discharge,
  back-power paths and firmware sequencing remain unverified. Schedule at most
  one SHT45 heater at a time; qualify radio peaks, LDO heat and cable drop.
- Branch pull-ups start at 2.2 kOhm. Mux R2/R3 are now fitted at 4.7 kOhm to
  the switched sensor rail, replacing the Feather's upstream pull-ups.
  Verify actual probe pull-ups and the complete
  cable/bundle at the proposed 10 kHz; no cable length is qualified here.
- Each output uses an STM32C011F6P6 with a local AP2112 logic regulator,
  accessible recovery shunt/reset/SWD, and the factory ROM I2C interface on
  PB6/PB7 (7-bit default 0x64). The factory UID is distinct from runtime address.
  ESP commissioning/programming, unique-ID tracking, watchdog policy, commands,
  communications-loss response and verified double-buffered persistence are
  future firmware. The 32 KB dual-image/configuration space plan is unproven;
  mutable boot options can prevent recovery despite immutable ROM.
- Each Vishay VO3053-X007T random-phase LED uses R101=270 ohm from raw 5 V
  and a low-side NPN. The approximately 10-11 mA corner scenario and 5 mA
  maximum trigger-current condition do not qualify all temperature/pulse cases.
  D101 blocks the reverse return into a LOW command during missing-ground
  connection states; R102 is 470 ohm, R103 is 10k, and C102 is now 1n directly
  base-to-emitter. These are receiver-local prototype protections, not a
  qualified six-contact hot-plug interface. The exact local option 7 footprint
  follows Vishay's land pattern; JLC assembly availability remains unconfirmed.
  The gate network uses a 430 ohm pulse-rated 2512 candidate and a
  330 ohm gate-to-A1 shunt. Leading-edge phase-angle and zero-cross-aligned
  whole-cycle burst control require local scheduling and qualified line timing;
  neither firmware mode is implemented by this drawing.
- Each 5 V relay coil is approximately 36 mA, driven by an MMBT3904 with
  200 ohm 1% base resistor, a 10k base-emitter pull-down, 100n base-emitter filter,
  series input blocking diode D102 and the existing coil flyback diode.
  Both command diodes face from the local MCU toward the base resistor.
  R106's conservative capacitor-charge bound is 18.18 mA; a pessimistic steady
  base-current scenario gives 4.36 mA against approximately 42 mA coil current.
  Loaded GPIO HIGH, cold-coil/full-temperature margin and contact-loss paths
  still need qualification.
  Normal switching happens with the
  triac off; interruption after a triac fault and low-current contact behavior
  still need validation. Diode suppression delays relay release.
- U30 TMCS1123B5AQDVGR senses series outlet current and drives separate current
  and zero-current-reference ADC inputs. U31 ACPL-K370 observes outlet voltage
  pulses with its own burden, including when no load is attached; low/high-line
  regional resistor/shunt BOMs remain unqualified. U40 ACPL-K376 and U41
  SN74LVC1G17 on the carrier distribute buffered LINE_SYNC. Threshold gaps need
  a qualified timing model; these are not exact zero-voltage timestamps.
  Current measurement/filtering, startup validity, leakage/no-load discrimination,
  sixteen-board fanout, detector heat/surges and full insulation need validation.
  U30's unused open-collector outputs retain TI-directed GND terminations and
  two explicit ERC findings rather than incorrect symbol types.
- Main T6.3 A and branch T3.15 A fuses are provisional. Final breaking capacity,
  inrush, interrupt energy, conductor/connector protection, surge protection,
  EMI, and leakage need assessment. The provisional 100 Ohm + 10 nF X2 snubber
  parts are fitted, with J20 configuring whether the series branch is connected;
  actual part ratings and values remain unqualified.
- Snubber review: fitting a correctly rated RC network is a reasonable
  preliminary option for transient immunity. At 120 V / 60 Hz, 10 nF passes
  approximately 0.45 mA while the relay is closed, negligible heating for the
  intended resistive loads; opening the relay breaks that path. Check actual
  voltage waveforms and capacitor/resistor pulse ratings before settling the
  values. A full 170 V step through 100 Ohm gives an illustrative initial 1.7 A
  pulse and 1 microsecond RC time constant, not a worst-case surge specification.
- **J20 is a provisional manual snubber setting, default ON.** Header pins
  1/3 share the capacitor-side net; 2/4 share triac A1. Fit two closed-top shunts
  across 1-2 and 3-4 for ON, or rotate both across 1-3 and 2-4 for OFF. This
  covers every pin in both configurations; one horizontal shunt alone still
  enables the branch. The caps are assembly accessories, two per output board
  / four per unit. The bare-PCB schematic netlist contains no fitted-shunt
  connections; configured-state audits model them explicitly. No extra GPIO or
  inter-board signal is required. Configure only while unplugged and discharged.
  Closed caps do not establish a touch-safe mains rating. The stock header
  footprint is a placement placeholder; select and verify compatible short pins
  (at most 5.6 mm for the Harwin M7685-05 candidate), cap retention, coverage,
  transients and mains spacing. The previously discussed 6.1 mm header is too
  long for this closed cap. No insulating blank cap has been selected.
- Each output retains two discrete MMBT3904 drivers. Driver-array alternatives
  remain unselected; the earlier combined-board array discussion is not the
  current modular circuit.
- Triac heatsinks/clips, socket and mains connector footprints, mechanical
  access, antenna clearance, creepage/clearance, and enclosure protection have
  not been qualified. Study assignments do not resolve blank schematic items.
  The shown JST-SH footprint is a reference; side-wall rotation and connector
  protrusion remain enclosure/layout questions, not settled placement.
  The additional relays are cutoff actuators; they do not independently protect
  against a shared controller or sensor failure.

## Primary references

- [Espressif WROOM datasheet](https://documentation.espressif.com/esp32-c6-wroom-1_wroom-1u_datasheet_en.html),
  [hardware checklist](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/schematic-checklist.html)
  and [KiCad library tag 3.0.1](https://github.com/espressif/kicad-libraries/tree/3.0.1).
- [TPS2116](https://www.ti.com/lit/ds/symlink/tps2116.pdf),
  [AP2112](https://www.diodes.com/datasheet/download/AP2112.pdf),
  [TS3USB221E](https://www.ti.com/lit/ds/symlink/ts3usb221e.pdf),
  [TLV3011B](https://www.ti.com/lit/ds/symlink/tlv3012.pdf),
  [USBLC6-2](https://www.st.com/resource/en/datasheet/usblc6-2.pdf)
  and [Adafruit 6153](https://www.adafruit.com/product/6153).
- [TCA9548A datasheet](https://www.ti.com/lit/ds/symlink/tca9548a.pdf).
- [7Semi ES-12289](https://7semi.com/7semi-sht45-digital-humidity-and-temperature-sensor-probe/)
  and [SHT4x datasheet](https://sensirion.com/media/documents/33FD6951/6A7C10A0/HT_DS_Datasheet_SHT4x_V7.3.pdf).
- [MEAN WELL IRM-05 datasheet](https://www.meanwell.eu/Upload/PDF/IRM-05/IRM-05-SPEC.PDF).
- [ST BTA08 datasheet](https://www.st.com/resource/en/datasheet/bta08.pdf)
  and [phototriac application note AN5114](https://www.st.com/resource/en/application_note/an5114-controlling-a-triac-with-a-phototriac-stmicroelectronics.pdf),
  plus [RC snubber guidance AN437](https://www.st.com/resource/en/application_note/an437-rc-snubber-circuit-design-for-triacs-stmicroelectronics.pdf).
- [Vishay VO3052/VO3053](https://www.vishay.com/docs/83749/vo3052.pdf),
  [ST STM32C011](https://www.st.com/resource/en/datasheet/stm32c011d6.pdf),
  [ROM loader AN2606](https://www.st.com/resource/en/application_note/an2606-.pdf),
  [TI TMCS1123](https://www.ti.com/lit/ds/symlink/tmcs1123.pdf),
  [Broadcom ACPL-K370/K376](https://docs.broadcom.com/doc/AV02-2153EN)
  and [TI SN74LVC1G17](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf).
- [Omron G6DN datasheet](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g6dn.pdf).
- [Toshiba TBD62003AFWG](https://toshiba.semicon-storage.com/us/semiconductor/product/general-purpose-logic-ics/detail.TBD62003AFWG.html).

The local triac/optotriac graphics are adapted from KiCad's standard symbols,
with the selected part's description and datasheet. The split relay symbol
uses the pin map above. KiCad's standard symbol graphics retain their
[upstream library license](https://gitlab.com/kicad/libraries/kicad-symbols/-/blob/master/LICENSE.md).

## Verification

KiCad parsing, ERC, exported-netlist inspection, and visual PDF review are
structural checks. They do not prove mains safety, thermal performance, sensor
accuracy, or successful operation on hardware. Record final check results and
source identities in `verification.md`; no checks are hidden or excluded to
obtain a clean ERC result.
