# Pin bias and default-state review

Review date: 2026-11-13. Scope: the current unrouted three-design study,
including both physical copies of the AC-output module. Governing proposals:
`MOT-HW-001` (complete assessment) and `MOT-HW-002` (defined hardware defaults).
Both requirements are draft for developer review. This is an audit and
correction plan, not implementation or completed hardware verification.

The revised review accounts for 193 schematic components and 550 distinct symbol-pin
identities across the three designs: carrier 82/253, output 31/73, sensors
80/224. Building the output twice gives 224 component instances and 623
symbol-pin instances. Repeated physical lands sharing one pin number, such as
the nine WROOM GND-29 lands, share an electrical disposition. Board-only
mechanical holes are not circuit pins; isolated support pads have no circuit
connection or logic-bias requirement. ERC power flags are virtual, not parts.
The inventory below explicitly includes unused and NC symbol pins.

The initial audit changed no CAD. The developer subsequently authorized the
inexpensive corrections documented below; schematic, grouped PCB placement
and both review PDFs now include them. Firmware is unchanged. Manufacturer
limits, scenario calculations and connectivity checks remain distinct from
measurements; no hardware measurements or immunity tests occurred.

The subsequent [ESD/access revision](esd-access-review.md) adds connector
clamps, branch series impedance and bare-PCB touch/probe contacts. Native
`Requirements` fields now cross-reference this review and other design inputs;
approved MOT-HW-003 covers annotation integrity only. All new pins are included
below. ESD clamps and test pads do not close the outstanding electrical limits.

## Findings

| ID | Finding | Disposition |
| --- | --- | --- |
| PB-01 | Former GPIO20 reset pull-up conflicted with sensor-enable default OFF. | EN moved to GPIO11 with local 10k; complete supply/reset behavior still needs qualification. |
| PB-02 | GPIO18/19/21 reset pull-ups interact with the switched sensor domain. | Known conductive paths; off-state voltage, reset-pin range and sequencing need resolution. |
| PB-03 | Original 100k output bias had no qualified leakage/noise margin. | Revised to local 10k and 100n filters; full-temperature and transient qualification remains open. |
| PB-04 | An NC marker does not establish unused MCU input or strap behavior; the status LED is not a DC logic pull-down. | Record per-pin configuration policy or add justified hardware bias. |
| PB-05 | Former CUT2 GPIO7 also serves MTDO. | CUT2 moved to GPIO0; actual startup/ROM/brownout waveforms remain unmeasured. |
| PB-06 | Ground-first contact loss permitted a return through the other command's pull-down into its LOW driver. | D101/D102 now block that reverse path; leakage, stored energy and contact transients remain unqualified. |
| PB-07 | External UART and USB harness pin/power assumptions remain unresolved. | Bound external-powered/off-controller cases; verify actual pigtail mapping and built-in CC resistors. |

### PB-01: sensor-enable conflict

In the initial revision, U10 module pin 18, GPIO20/SDIO_DATA0, drove EN.
Espressif specifies a weak pull-up
**at reset**, followed by an input-enabled state after reset. The drawing
directly connected it to U22 EN, with external R22 = 100k to GND. AP2112 has
a typical internal 3 Mohm EN pull-down. Using the ESP's typical 45k pull-up:

`Rdown = 100k || 3M = 96.77k`

`VEN = 3.3 * 96.77 / (45 + 96.77) = 2.25 V`

AP2112 specifies EN low at at most 0.4 V and high at at least 1.5 V. The
nominal model therefore enables the rail during reset. This disproves the
assumption that the former 100k guaranteed OFF; it is not a measured reset
waveform or a worst-case prediction. [ESP32-C6 datasheet, Table 7-1 and DC
characteristics](https://documentation.espressif.com/esp32-c6_datasheet_en.pdf),
[AP2112 datasheet, 3.3 V electrical characteristics](https://www.diodes.com/datasheet/download/AP2112.pdf).

Implemented correction: GPIO11 / module pin 12 now drives U22 EN, with R22
changed to 10k; GPIO20 is unused. GPIO11 has no specified reset weak pull-up
and is not a strap. This removes the identified divider conflict. A 1%-high
10k resistor permits about 39.6 uA total injected current before reaching the
AP2112's 0.4 V LOW limit in a resistive model. That is an available budget,
not a specified leakage value or disturbance measurement. Qualify the combined
limits, ramp behavior and PB-02 before claiming sensor power is OFF.

### PB-02: sensor-domain power sequencing

GPIO18/19/21 also have reset weak pull-ups to the main MCU rail. Even after
correcting EN, they connect to the switched rail through mux R2/R3 = 4k7 and
R1 = 10k. Application instructions to disable internal pulls do not control
the hardware reset interval.

With 45k typical internal pulls and an ideal grounded sensor rail, these
three branches supply approximately `2 * 3.3/(45k+4.7k) + 3.3/(45k+10k)` =
193 uA. AP2112 advertises an active output discharge of **60 ohm typical**
while disabled with its input supply present. Including that resistance gives
approximately 12 mV at the sensor rail and 0.61 V at mux RESET in this nominal
resistive model. Thus this is not proof that the sensor rail necessarily
rises to operating voltage. Neither 45k nor 60 ohm has the needed guaranteed
bounds for a full off-state proof.

TI specifies a recommended RESET high-input upper bound of VCC + 0.5 V during
valid powered operation; recommended operation itself starts at VCC = 1.65 V.
The off-state model is outside that operating regime and needs explicit
powered-off tolerance evidence, not an assumption based on a clean ERC.
Absolute-maximum input voltage is a separate stress limit, not proof of
functional off-state behavior or an assumed clamp voltage.
[TCA9548A datasheet, sections 5.1/5.3/5.5](https://www.ti.com/lit/ds/symlink/tca9548a.pdf).

Decide whether reset/rail sequencing, GPIO reassignment, series resistance or
powered-off isolation is needed. Measure all relevant pin/rail voltages and
injection currents with the sensor rail disabled and during MCU reset.
Also check the inverse case: external sensor/interface power present while
the controller is unpowered. The present shared supply does not intentionally
support separately powered sensor heads.

### PB-03/PB-06: output defaults and unplugging

The initial revision had R103/R107 = 100k directly base-to-emitter at
Q101/Q103. These were on the output board, **after** the removable
J14 interface. HEAT_EN sees approximately 102.2k to local ground through
R102 = 2k2; CUT_EN sees approximately 100.47k through R106 = 470 ohm.
Bias therefore remained when command wires or the entire cable were removed.
Full removal also removes the raw mains-derived coil/opto supply through J14.2.

The intended state is optotriac LED off and relay coil deenergized, with its
normally-open contact open. Values still need a leakage/coupling budget:
5 uA through 100k would produce 0.5 V in a linear model before base conduction.
This is a sensitivity illustration, not a predicted induced current or a
guaranteed BJT switching threshold. A 10k base-emitter value is a candidate;
at 0.8 V it would divert 80 uA of base drive. Check actual transistor variant,
drive margin, temperature and transient conditions before changing it.

When ground disconnects before command/power contacts, these local resistors
reference a potentially moving local ground. Equal-length headers provide no
guaranteed contact sequence. Complete-unplug topology alone does not qualify
live unplugging, missing-ground operation or partially inserted connectors.
Determine the supported procedure and test the corresponding contact-loss
states. OFF may involve triac commutation and relay release time, extended
by the flyback diode; it does not mean instantaneous zero current or recovery
from a shorted triac/welded contact.

#### Follow-up: partial-contact path and incremental cost

The developer clarified that outputs should be OFF unless intentionally ON,
requested checking the additional circuitry/cost, then approved implementing
the inexpensive correction. The investigation below records its rationale;
the implemented values and remaining limits follow it. This is not a closed
hardware-qualification finding.

For J14's four contacts, the 16 present/absent combinations reduce to four
power-reference groups. With GND and 5 V present, a missing command retains
its local base-emitter pull-down. With GND present but 5 V absent, actuator
power is absent, but stored energy and command-to-collector injection still
need checking. With both power contacts absent, stored/parasitic energy and
command injection remain qualification cases. The important additional DC
path occurs with **GND absent and 5 V present** while one command is HIGH and
the other LOW:

`HIGH command -> base resistor -> first transistor B-E -> floating local GND
-> other B-E pull-down -> other base resistor -> LOW command`.

Using 3.3 V and about 0.7 V B-E, this path carries roughly 26 uA with the
existing 100k pull-down, or 0.25 mA after replacing it with 10k. These are
nominal path estimates, not guaranteed optotriac non-trigger limits. The
MOC3063's maximum LED trigger-current rating is not a guaranteed minimum
current below which triggering is impossible. Stronger pull-downs alone
therefore do not establish the required missing-ground behavior.

The minimal candidate adds **one series blocking diode to each command**:
anode toward J14/controller, cathode toward the base resistor/transistor.
Keep the base-emitter pull-down on the transistor side. This is two diodes
per output board, **four per complete two-output unit**, with no extra MCU
pin. It blocks the identified reverse return into a LOW command, subject to
diode leakage/capacitance and alternate-path qualification. Small local
base-emitter capacitors are an optional noise filter, not a substitute for
the blocking function. A controller-side buffer alone does not remove this
receiver-board path.

The series diode consumes ON-state voltage margin, so R102/R106 must be
recalculated rather than retaining 2k2/470 ohm automatically. Illustratively,
at 2.64 V source HIGH, 1.0 V diode drop and 0.95 V B-E, the existing 470 ohm
allows only about 1.47 mA before pull-down current. A lower resistor or a
different transistor drive solution needs qualification against actual GPIO
VOH/current, coil/opto load, cold diode drop and transistor temperature limits.
Resistor substitutions do not add placements. No final values are selected.

Public JLCPCB price snapshot, 2026-11-12 local / 2026-11-13 UTC, USD lowest
quantity tier; this is an incremental estimate, excluding tax, shipping,
attrition/minimum-order quantities and unchanged board/setup costs:

| Candidate | Unit price | Quantity per complete unit | Increment |
| --- | --- | --- | --- |
| Basic 1N4148W, C81598 | $0.0124 | 4 | $0.0496 |
| Extended low-leakage BAS116, C68953 | $0.0252 | 4, alternative to above | $0.1008 |
| Basic 100n 0805, C49678 | $0.0138 | up to 4 optional filters; value unselected | $0.0552 |
| Basic 10k 0805, C17414 | $0.0034 | substitutions for existing pull-downs | approximately neutral |

These price examples support budgeting **$0.10-$0.20 extra components per
complete unit**, with final diode type/filter choice open. C68953 showed only
three in stock, so it is a price reference rather than a purchasable complete
four-diode set. Its manufacturer is Jiangsu Changjing; limits from another
manufacturer's BAS116 must not be transferred to it. Generic 1N4148W must
also pass the temperature/leakage budget before selection.

At Economic SMT's $0.0016/joint, four two-pad diodes add $0.0128 in joint
charges; four three-pad diodes add $0.0192. Four optional two-pad capacitors
add another $0.0128. Allow roughly **$0.01-$0.04 extra joint charges per unit**.
A newly introduced Extended part type adds **$3.07 per assembly batch**, not
per diode or unit; the quoted Basic alternatives avoid that loading fee.
For comparison, a C7813 SN74LVC125APWR quad buffer was $0.3542 plus its support
parts, joints and any new Extended-type loading fee. It is not recommended
solely as a cure for this ground-loss path.
[JLC 1N4148W](https://jlcpcb.com/partdetail/C81598),
[JLC BAS116](https://jlcpcb.com/partdetail/70066-BAS116/C68953),
[JLC capacitor](https://jlcpcb.com/partdetail/C49678),
[JLC resistor](https://jlcpcb.com/partdetail/C17414),
[JLC buffer](https://jlcpcb.com/partdetail/C7813),
[JLC assembly pricing](https://jlcpcb.com/help/article/pcb-assembly-price).

Before closing PB-03/PB-06, select actual manufacturer parts, bound permitted
OFF current/pulse duration, and check all command/power/contact sequences,
reverse B-E stress, stored energy, noise injection and relay release/triac
commutation. Diodes and pull-downs do not block an actively driven unwanted
HIGH. No hardware test or default-OFF qualification is claimed here.

#### Implemented prototype and drive scenarios

The authorized revision retains the MMBT3904 drivers and fits Semtech
1N4148W/C81598 at D101/D102, R102 = 470 ohm, R106 = 150 ohm, R103/R107 = 10k,
and C102/C103 = 100n/50 V (Yageo CC0805KRX7R9BB104 / C49678) directly base-to-emitter. No new GPIO is needed.
The four added diodes and four added capacitors across two output boards cost
$0.1048 in components plus $0.0256 Economic solder-joint charges at the quoted
prices. Both selected added types are Basic, avoiding a new Extended loading
fee. Resistor substitutions add no placements. Neither existing NPN's exact
manufacturer/order code has been finalized; its schematic datasheet link is
now corrected from PZT3904 to the onsemi MMBT3904 reference.

At an illustrative loaded GPIO HIGH of 2.64 V, diode drop 1.0 V, 1%-high
series resistors and 1%-low pull-downs:

- HEAT with VBE = 0.85 V: `(2.64-1.0-0.85)/474.7 - 0.85/9900`
  gives about 1.58 mA base current.
- CUT with VBE = 0.95 V: `(2.64-1.0-0.95)/151.5 - 0.95/9900`
  gives about 4.46 mA base current. A 5.25 V supply and the 139 ohm nominal
  coil's -10% resistance tolerance at 23 C give 42 mA before transistor loss,
  a forced-beta scenario of about 9.4.

These are engineering scenarios, **not guaranteed operating bounds**.
Espressif's 0.8 VDD VOH table specifies a high-impedance load; its large GPIO
source-current figure is typical. onsemi's saturation limits are at specific
25 C test currents, not a blanket guarantee at this load/temperature. The
nominal 3.3 V / 0.6 V diode / 0.8 V B-E case draws about 4.0 mA per HEAT
command and 12.7 mA per CUT command through its series resistor. Qualify actual
loaded HIGH, total GPIO loading, cold diode drop, coil/opto current and the
final transistor variant before a build release.

The exact Semtech sheet specifies VF maxima 0.715 V at 1 mA, 0.855 V at 10 mA
and 1 V at 50 mA at 25 C. Its IR maximum is 25 nA at 20 V/25 C, but 30 uA
at 25 V/150 C. The latter corresponds to 0.303 V across a 1%-high 10k resistor;
this is not a guaranteed transistor OFF threshold or a closed extreme-hot
corner. No minimum non-trigger opto current is inferred from maximum IFT.
The 2 pF maximum diode capacitance and local 100n filter support a charge-
injection analysis; 10k x 100n gives a nominal 1 ms decay time constant, not
a measured rejection or relay-release time.
[Semtech original datasheet via LCSC](https://datasheet.lcsc.com/lcsc/1811061725_ST-Semtech-1N4148W_C81598.pdf),
[ESP32-C6](https://documentation.espressif.com/esp32-c6_datasheet_en.pdf),
[onsemi MMBT3904](https://www.onsemi.com/pdf/datasheet/mmbt3904lt1-d.pdf),
[Omron coil limits](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g6dn.pdf).

### PB-04/PB-05/PB-07: remaining MCU and service states

- GPIO4/5/15/20/22/23 are intentionally unused in the revised drawing. Their MCU
  pins have to be assessed as inputs/straps, unlike U10.22 which is true NC.
  GPIO4/5/15 are straps; record the SDIO edge-selection and JTAG/eFuse policy.
  After-reset input-buffer configuration and internal pulls need explicit
  firmware policy or external bias. No blanket resistor on every NC pin is
  implied, and no actual strap failure has been established.
- GPIO10 connects through R15 and D10 to ground. A diode branch does not
  guarantee a low logic level below its forward-conduction region. Resolve
  its high-impedance input/LED behavior; possible indicator flicker has a
  different consequence from unwanted heater operation.
- CUT2 is now GPIO0, replacing GPIO7/MTDO; GPIO6/7 now expose LP I2C. This removes the
  identified alternate-function conflict without a carrier part. Actual
  reset/ROM/brownout behavior still needs measurement; a pull-down cannot
  override an actively driven HIGH.
- J22 exposes RX/TX and main 3.3 V directly. Record whether a powered UART
  adapter may be connected to an unpowered controller, and which header pins
  may source power; no injection/isolation qualification exists yet.
- J21's six-pin order is project-defined pending sample verification. The
  selected Adafruit 6153 contains separate 5.1k sink resistors; its NC CC
  pins on the carrier are intentional and do not call for duplicate Rd.

## Pin-group dispositions

The inventory assigns every pin to one of the following assessments. A
disposition of "path present" is not a claim of worst-case qualification.
Power pins, passive terminals and true NCs still have a recorded reason why
ordinary logic pulls do not apply.

| Key | Pins/function | Current assessment and remaining work |
| --- | --- | --- |
| C-MCU | U10 all pins | Detailed breakdown below; PB-01/02/04/05/07 remain open. |
| C-BOOT | EN RC, reset/boot switches, GPIO8/9 pull-ups | R10/11/12 = 10k define HIGH, C10 only delays EN; switch open/omitted retains pull-up. Qualify ramp/brownout and intentional boot states. |
| C-SENSEN | U22 EN and R22 | GPIO11 replaces GPIO20; local 10k replaces 100k. Divider conflict removed; combined limits/ramp and PB-02 still need qualification. |
| C-PMUX | TPS2116, priority divider and its capacitors | PR1 is a defined divider; MODE is hard-wired to the mains-derived rail. An absent mains-derived rail has a 416k divider path to GND, not an open net; budget leakage/coupling/decay. ST is unused open-drain output, legitimately NC. |
| C-LDO | AP2112 main/sensor rails and capacitors | VIN/GND/VOUT are supply pins; main EN is hard VIN, sensor EN is C-SENSEN, pin 4 is true NC. Capacitors provide no DC logic bias. Off/partial-power/discharge limits remain open. |
| C-USBDATA | USB switch, series resistors and switch decoupling | S is hard GND; OE has local 47k pull-up to main 3.3 V. Selected analog pair follows USB; unselected analog pins may be open. Do not add arbitrary pulls to data lines. |
| C-VBUS | Comparator, 226k/100k divider, 47k OE pull-up and comparator decoupling | IN+ = REF, IN- = grounded divider, OUT open drain. B-version POR gives Hi-Z and local receiver pull-up gives disconnect. Quantify combined leakage/ramp margin. |
| C-RAWUSB | R23 VBUS bleed | 10k gives raw VBUS a local discharge/reference when cable is absent; no assumed host current entitlement. |
| C-ESD | D20 all pins | Data clamp/pass-through pins are analog, GND/VBUS are references. No arbitrary logic pulls; powered-off clamp/gate leakage still needs review. |
| C-USBPORT | J21 all contacts | Power and USB analog pair follow attached cable; CC resistors reside in selected panel assembly. PB-07 and physical mapping remain open. |
| C-SENSIF | J13 all contacts | GND/switched rail and remote SDA/SCL/reset. Local main-bus 10k pulls now survive mux removal; the receiver retains its own bus/reset pulls. PB-02/04 and reset off-domain behavior remain open. |
| C-QWIIC | J23/J25 HP and J24/J26 LP, all contacts | GND, switched 3.3 V power OUT, SDA/SCL on independent HP/LP buses; duplicates within each pair share data. Carrier-local pulls survive mux removal; individual power links are not I/O isolation. One host/supply; no external power backfeed or signals into unpowered boards. PB-02/04 and full partial-contact behavior remain open. |
| C-QWPULL | R40/R41 main 10k; R42/R43 LP 4k7 | Two-contact passive pulls to switched sensor rail define idle HIGH while powered, surviving removal of either socket/mux. Main nominal 10k parallel mux 4k7 and selected branch 2k2 gives 1.303k before probe-added pulls. Off-domain, GPIO6/7 JTAG/reset defaults, leakage, LOW/rise margins and temperatures remain unqualified. |
| QW-POWER | Carrier R44-R47 and sensor R50 | Two-contact 0-ohm power links, not logic pulls or automatic source isolation. Removal disconnects local supply from the respective carrier socket or shared sensor Qwiic pair; it does not isolate sensor J10/J11 power contacts from each other. No SDA/SCL isolation. Passive power pins need no arbitrary bias. One source only; AP2112 disabled output discharge still loads external backfeed. |
| S-QWIIC | J10/J11 all contacts | Local GND, shared bench power through R50, parallel upstream SDA/SCL with configurable local 4k7 pulls; reset remains locally pulled HIGH. Disconnect deployment links to another controlling host/supply for standalone bench use. No added I/O isolation or qualified hot plugging. |
| C-OUTPUTIF | J15/J18 all contacts | GND/raw mains-derived 5 V/HEAT/CUT. Receiver-local bias is on output board, not credited from carrier. PB-03/05/06. |
| C-UART | J22 all contacts | Direct UART/service power interface; RX reset pull-up and default TX activity are intentional. PB-07. |
| C-LED | R15/D10 | Current-limited indicator load; no guaranteed DC logic-low bias at GPIO10. PB-04. |
| C-MAINS | AC connectors, F1 and PS1 | Power/neutral/PE/isolated output references, not ordinary logic inputs. IRM-05-5 PS1 has four used pins: 1 neutral, 2 fused line, 3 secondary GND, 4 raw 5 V; the old RECOM NC3 is removed. No arbitrary pull is appropriate. Never add mains-to-LV-GND bias. Protection/discharge/earthing are separate assessments. |
| C-DECOUP | C1/C2/C11/C12 | Supply decoupling, not a DC bias mechanism; supply pins retain their own power-domain obligations. |
| O-INPUT | J14 all contacts | Local ground and raw 5 V plus commands; receiving base pull-downs survive full connector removal. PB-03/06. |
| O-HEAT | Q101/R102/R103/D101/C102 | Local 10k/100n B-E bias/filter after series command diode and 470 ohm base resistor. Collector sinks opto LED; no collector pull-down. Drive/leakage/transients remain PB-03/06. |
| O-OPTO | U2/R101 | Pins 1/2 are a current-limited LED circuit; 3/5 true NC; 4/6 mains analog switching terminals. No universal pull. |
| O-GATE | Q102/R104/R105 | Gate has 330 ohm local shunt to A1; A1/A2 are mains terminals. Gate transient/dv/dt and part-specific margins still need qualification. |
| O-RELAY | Q103/R106/R107/K1/D1/D102/C103 | Local 10k/100n B-E bias/filter after series command diode and 150 ohm base resistor. Coil/flyback define collector load, contacts normally open. PB-03/06 and release timing remain. |
| O-MAINS | J17/J10/F2 | Fused line, neutral and PE/power contacts; logic pulls N/A. Preserve isolation/PE continuity. |
| O-SNUB | R108/C101/J20 | J20 1/3 are capacitor side, 2/4 A1. No shunts = snubber OFF, two same-net shunts = OFF, either cross-net shunt = ON. Capacitor-side node intentionally floats in OFF; assess charge/transients/insulation, not a pull to LV GND. Reconfigure unplugged/discharged. |
| S-MUX | U1 all pins | Addresses are defined by SW1 and local 10k pull-downs; reset locally pulled HIGH, upstream/branch I2C have configurable/local pull-ups. Domain-off behavior is PB-02. |
| S-RESET | R1 | 10k to local sensor rail defines reset HIGH with carrier unplugged if sensor rail remains powered. Reset reinitialization on power loss still follows POR limits. |
| S-UPSTREAM | R2/R3 | Local 4k7 to sensor rail through independent fitted R55/R56 = 0 define upstream idle HIGH when enabled. Removing excess board pulls requires suitable remaining bus pulls; stand-alone operation cannot credit removed paths. PB-02 when off. |
| S-PULL-LINK | R55/R56 | Independent two-contact 0-ohm pull-up feeds. Removing one leaves only its resistor feed floating; no shared floating node couples SDA/SCL. Reset bias is independent. No added pull-down on these passive link contacts; configure the complete bus before use. |
| S-ADDRESS | SW1 and R51/R52/R53 | Three SPST address switches connect pins 6/5/4 (A0/A1/A2) to local 3.3 V via pins 1/2/3. Each 10k pull-down stays with the mux and defines LOW with its switch open or cable absent. ON switch current is nominal 0.33 mA. CTS dry-circuit life rating supports preliminary signal-level fit, not physical qualification at every corner. Configure unpowered; factory MSTR switches ship ON. |
| S-BRANCH | All port pull-ups | Each SDA/SCL has 2k2 to local sensor rail, surviving an unplugged probe and removed higher ports. Verify probe-added pulls, sink current, capacitance and noise. |
| S-INTERFACE | J12/J13 | Parallel local GND/rail/upstream SDA/SCL/shared reset. Bus and reset paths stay on the mux when a link is removed; local pulls depend on R55/R56 configuration. A remaining chain/Qwiic feed may still power the board. Partial contact loss, external-powered cases and shared reset require supported procedures and qualification. |
| S-PORT | J2-J9 | GND/rail/SDA/SCL; digital pair locally pulled HIGH when powered, even with probe absent. No pull on power/ground. Partial-power contact loss needs a supported procedure. |
| S-DECOUP | C3 | Supply bypass; not DC bias. |
| ESD-DUAL | New PESD5V0S2BT clamps | Pins 1/2 are passive bidirectional shunts, pin 3 is local GND. The populated signal/3.3 V branch follows its connected net; unused channels are true NC and need no logic bias. No rail-steering path is added. Normal-voltage, leakage/capacitance, powered-off, clamp-current and missing-ground limits remain in the ESD review. Never replace command clamps with unidirectional steering paths without repeating PB-06. |
| ESD-POWER | New ESD5Z6.0T1G clamps | Passive 6 V-standoff supply shunt: K1 to 5 V/VBUS, A2 to GND. No ordinary logic pull; assess leakage, residual clamp and reverse/partial-supply states. These do not establish an OFF default or continuous overvoltage regulation. |
| S-SERIES | Sensor R30-R45 | Passive 100 ohm series impedance, not a pull. Existing 2k2 pulls remain mux-side; connector-side nets reach them through the resistor. Disconnection, off-domain pin limits, pulse coordination and I2C LOW margins still require qualification. |
| P-TOUCH | TP1 on each design | One passive local-GND net, exposed 8 mm copper with no purchased component. Not an independent high-impedance input, earth bond, or qualified finger-discharge accessory; grounding/ESD return and handling scope in the ESD review. |
| P-PROBE | Remaining TP contacts | Bare direct-net probe access, not an independent input needing a pull. Optional two-hole wire loop has both lands numbered 1 on one net; sensor diagnostics use one-hole posts. Unfitted contacts retain the net's original bias. Clip loading, access and earth-grounded instruments remain qualification/procedure considerations. |

### MCU pin-by-pin breakdown

| U10 pin(s) | Function and default-state disposition |
| --- | --- |
| 1,28,29 | GND/reference; all physical GND-29 lands share this disposition. |
| 2 | Main 3.3 V supply with decoupling; no logic pull. |
| 3 | EN: C-BOOT. |
| 4,5 | GPIO4/5 unused straps: PB-04, explicit unused-SDIO policy required. |
| 6 | GPIO6 LP_I2C_SDA: carrier 4k7 to switched rail. MTCK/default-pull and unpowered-domain behavior require qualification; keep USB-JTAG policy, no actuator connection. |
| 7 | GPIO7 LP_I2C_SCL: carrier 4k7 to switched rail. MTDO/default-drive and unpowered-domain behavior require qualification; keep USB-JTAG policy, no actuator connection. |
| 8 | GPIO0 CUT2: receiver-local O-RELAY protection; startup waveform still to qualify. |
| 9,27 | GPIO1/2 HEAT1/2: receiving O-HEAT bias; no carrier-local pull. |
| 10 | GPIO8 boot strap: R12 HIGH, C-BOOT. |
| 11 | GPIO10 LED: C-LED/PB-04. |
| 12 | GPIO11 sensor EN: local R22 = 10k; no reset WPU/strap; PB-01 correction, PB-02 still open. |
| 13,14 | USB DM/DP: C-USBDATA; protocol pull-up behavior is intentional. |
| 15 | GPIO9 boot strap: R11 HIGH, SW2 grounds intentionally. |
| 16,17 | GPIO18/19 I2C: new carrier 10k plus retained mux 4k7 pulls to switched rail; reset WPU and PB-02 remain. |
| 18 | GPIO20 unused with reset WPU: PB-04; no regulator EN connection. |
| 19 | GPIO21 reset: remote R1, open-drain firmware intent, reset WPU, PB-02. |
| 20,21 | GPIO22/23 unused: PB-04; reset pull does not substitute for documented later input configuration. |
| 22 | True module NC, leave open. |
| 23 | GPIO15 unused strap: PB-04; record JTAG-selection eFuse policy. |
| 24,25 | UART RX/TX: C-UART and external-powered connection PB-07. |
| 26 | GPIO3 CUT1: receiving O-RELAY bias; no carrier-local pull. |

### Sensor pin-by-pin breakdown

| U1 pin(s) | Function and default-state disposition |
| --- | --- |
| 1,2,21 | A0/A1/A2: SW1 selects local 3.3 V, with independent 10k pull-downs; open contacts define zero. S-ADDRESS covers all switch/contact states. |
| 3 | RESET has local R1 = 10k HIGH on sensor rail; PB-02 for off-state external drive. |
| 4-11,13-20 | Eight SDA/SCL pairs; every line has its local 2k2 pull-up to sensor rail. |
| 12,24 | GND/VCC; C3 bypass, supply-domain treatment. |
| 22,23 | Upstream SCL/SDA; local R3/R2 = 4k7 HIGH through independently removable R56/R55. With links removed, suitable pulls must remain elsewhere on the bus. |

At 3.3 V, TI's 1 uA maximum input-current term alone drops 10 mV across R1
or 4.7 mV across an upstream pull-up; the high threshold is 0.7 VCC. These
are individual contributions, not total leakage/noise budgets. With one
channel enabled, 4k7 and 2k2 pulls are effectively parallel through the mux:
about 1.50k, or 1.93 mA at VOL = 0.4 V, before probe pull-ups and switch loss.
The mux powers up with channels deselected; power-cycle voltage/timing must
meet its POR specification. [TI source](https://www.ti.com/lit/ds/symlink/tca9548a.pdf).

The external SHT45 probe is represented by its port, not by a chip symbol in
these PCBs: VDD/GND are supply references, SDA/SCL need the documented I2C
pull-ups, and unplugged probe pins are unpowered passive connections. A
partially powered probe can violate its signal-to-VDD limits and needs its
own sequencing disposition. [SHT4x electrical and maximum ratings](https://sensirion.com/media/documents/33FD6951/6A7C10A0/HT_DS_Datasheet_SHT4x_V7.3.pdf).

## Verification and correction plan

1. Review the two draft requirements and decide the live-unplug/contact-order
   scope. Assign a required state to every critical control net.
2. Correct PB-01 and resolve PB-02 together, then calculate bias from guaranteed
   leakage/internal-pull/threshold/tolerance limits. Add isolation/filtering if
   a resistor alone does not satisfy the selected disturbance envelope.
3. Qualify O-HEAT/O-RELAY blocking/bias/filtering, unused-pin/service policies and each
   removable connection. Do not infer noise immunity from DC continuity.
4. Update the schematic, PCB, notes and both PDFs after design agreement.
   Re-run ERC, pad/net parity, DRC, source comparison and visual review.
5. Before hardware acceptance, test relevant supply ramps, reset/bootloader,
   brownout/shutdown, absent/partial connectors and shunt variants. Inject the
   agreed bounded disturbances; measure receiver voltages, rail/injection
   currents and actuator LED/coil drive, including recovery/release time.

For pull-down sizing, a first DC bound is `R <= VIL_max / I_source_max`,
including competing pulls and resistor tolerance. For pull-ups, check
`Vrail_min - I_sink_max * R >= VIH_min`. Also check active-drive current and
power. Fast capacitive charge injection and RC decay need a time-domain budget;
these DC inequalities alone do not qualify a mains-adjacent control line.

Output component references:
[Lite-On MOC306X](https://optoelectronics.liteon.com/upload/download/DS70-2001-026/MOC306X%20series%20Jun23.PDF),
[ST BTA08](https://www.st.com/resource/en/datasheet/bta08.pdf),
[Omron G6DN](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g6dn.pdf),
[onsemi MMBT3904L](https://www.onsemi.com/pdf/datasheet/mmbt3904lt1-d.pdf).
The schematic's generic MMBT3904 now links the correct onsemi family reference;
select the actual manufacturer variant before claiming worst-case leakage.

USB/power references:
[TPS2116](https://www.ti.com/lit/ds/symlink/tps2116.pdf),
[TS3USB221E](https://www.ti.com/lit/ds/symlink/ts3usb221e.pdf),
[TLV3011B](https://www.ti.com/lit/ds/symlink/tlv3011.pdf),
[Adafruit 6153](https://www.adafruit.com/product/6153).
TS3USB221E's 1 uA control leakage contributes 47 mV across R24; at nominal
3.3 V the remaining 3.253 V is above its 0.46 VCC high threshold, before
comparator leakage and supply/ramp margins. TPS2116 PR1/MODE leakage and
divider coupling/rail decay also need explicit worst-case closure.

## Complete component and pin inventory

### motley-carrier

| Reference | Value | Every symbol pin | Assessment |
| --- | --- | --- | --- |
| C1 | 100n / 16V | 1, 2 | C-DECOUP |
| C2 | 10u / 16V | 1, 2 | C-DECOUP |
| C10 | 1u / 10V | 1, 2 | C-BOOT |
| C11 | 10u / 10V | 1, 2 | C-DECOUP |
| C12 | 100n / 10V | 1, 2 | C-DECOUP |
| C20 | 1u / 16V | 1, 2 | C-PMUX |
| C21 | 1u / 16V | 1, 2 | C-PMUX |
| C22 | 22u / 10V | 1, 2 | C-PMUX |
| C23 | 22u / 10V | 1, 2 | C-LDO |
| C24 | 1u / 16V | 1, 2 | C-LDO |
| C25 | 4.7u / 10V | 1, 2 | C-LDO |
| C26 | 100n / 16V | 1, 2 | C-USBDATA |
| C27 | 100n / 16V | 1, 2 | C-VBUS |
| D10 | STATUS | 1, 2 | C-LED |
| D20 | USBLC6-2SC6 | 1, 2, 3, 4, 5, 6 | C-ESD |
| D30 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D31 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D32 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D33 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D34 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D35 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D36 | ESD5Z6.0T1G | 1, 2 | ESD-POWER |
| D37 | ESD5Z6.0T1G | 1, 2 | ESD-POWER |
| D38 | ESD5Z6.0T1G | 1, 2 | ESD-POWER |
| D40 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D41 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D42 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D43 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D44 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D45 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D46 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D47 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| F1 | T6.3A / 250V provisional | 1, 2 | C-MAINS |
| J1 | AC INPUT / cord or inlet | 1, 2, 3 | C-MAINS |
| J13 | SENSOR LINK | 1, 2, 3, 4, 5 | C-SENSIF |
| J15 | HEATER LV LINK | 1, 2, 3, 4 | C-OUTPUTIF |
| J16 | MAINS LINK / provisional terminal | 1, 2, 3 | C-MAINS |
| J18 | HEATER LV LINK | 1, 2, 3, 4 | C-OUTPUTIF |
| J19 | MAINS LINK / provisional terminal | 1, 2, 3 | C-MAINS |
| J21 | PANEL USB-C / ADAFRUIT 6153 | 1, 2, 3, 4, 5, 6 | C-USBPORT |
| J22 | 3V3 UART SERVICE / NO 5V | 1, 2, 3, 4 | C-UART |
| J23 | QWIIC MAIN / 3V3 OUT | 1, 2, 3, 4 | C-QWIIC |
| J24 | QWIIC LP / 3V3 OUT | 1, 2, 3, 4 | C-QWIIC |
| J25 | QWIIC MAIN / 3V3 OUT | 1, 2, 3, 4 | C-QWIIC |
| J26 | QWIIC LP / 3V3 OUT | 1, 2, 3, 4 | C-QWIIC |
| PS1 | IRM-05-5 / 5V 1A | 1, 2, 3, 4 | C-MAINS |
| R10 | 10k | 1, 2 | C-BOOT |
| R11 | 10k | 1, 2 | C-BOOT |
| R12 | 10k | 1, 2 | C-BOOT |
| R13 | 22 | 1, 2 | C-USBDATA |
| R14 | 22 | 1, 2 | C-USBDATA |
| R15 | 2k2 | 1, 2 | C-LED |
| R20 | 316k / 0.1% | 1, 2 | C-PMUX |
| R21 | 100k / 0.1% | 1, 2 | C-PMUX |
| R22 | 10k / EN pull-down | 1, 2 | C-SENSEN |
| R23 | 10k / VBUS bleed | 1, 2 | C-RAWUSB |
| R24 | 47k / default DISCONNECT | 1, 2 | C-VBUS |
| R25 | 226k / 1% | 1, 2 | C-VBUS |
| R26 | 100k / 1% | 1, 2 | C-VBUS |
| R40 | 10k | 1, 2 | C-QWPULL |
| R41 | 10k | 1, 2 | C-QWPULL |
| R42 | 4k7 | 1, 2 | C-QWPULL |
| R43 | 4k7 | 1, 2 | C-QWPULL |
| R44 | 0 | 1, 2 | QW-POWER |
| R45 | 0 | 1, 2 | QW-POWER |
| R46 | 0 | 1, 2 | QW-POWER |
| R47 | 0 | 1, 2 | QW-POWER |
| SW1 | RESET | 1, 2 | C-BOOT |
| SW2 | BOOT / GPIO9 | 1, 2 | C-BOOT |
| TP1 | TOUCH LV GND | 1 | P-TOUCH |
| TP2 | GND / LOOP | 1 | P-PROBE |
| TP3 | +5V_SYS / LOOP | 1 | P-PROBE |
| TP4 | +5V_SELECTED / LOOP | 1 | P-PROBE |
| TP5 | +3V3 / LOOP | 1 | P-PROBE |
| TP6 | +3V3_SENS / LOOP | 1 | P-PROBE |
| TP7 | USB_VBUS_RAW / LOOP | 1 | P-PROBE |
| U10 | ESP32-C6-WROOM-1-N8 / C5366877 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29 | C-MCU |
| U20 | TPS2116DRLR | 1, 2, 3, 4, 5, 6, 7, 8 | C-PMUX |
| U21 | AP2112K-3.3TRG1 / ESP | 1, 2, 3, 4, 5 | C-LDO |
| U22 | AP2112K-3.3TRG1 / SENS | 1, 2, 3, 4, 5 | C-LDO |
| U23 | TS3USB221ERSER | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | C-USBDATA |
| U24 | TLV3011BIDBVR / VBUS VALID | 1, 2, 3, 4, 5, 6 | C-VBUS |

Inventory reconciliation: 82 components, 252 symbol pins; every listed pin inherits the cited group assessment.

### motley-ac-output

| Reference | Value | Every symbol pin | Assessment |
| --- | --- | --- | --- |
| C101 | 10n X2 | 1, 2 | O-SNUB |
| C102 | 100n / 50V | 1, 2 | O-HEAT |
| C103 | 100n / 50V | 1, 2 | O-RELAY |
| D1 | 1N4148W | 1, 2 | O-RELAY |
| D101 | 1N4148W | 1, 2 | O-HEAT |
| D102 | 1N4148W | 1, 2 | O-RELAY |
| D110 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D111 | ESD5Z6.0T1G | 1, 2 | ESD-POWER |
| F2 | T3.15A provisional | 1, 2 | O-MAINS |
| J10 | Qualtek 738W-X2/03 (wired) | 1, 2, 3 | O-MAINS |
| J14 | HEATER LV LINK | 1, 2, 3, 4 | O-INPUT |
| J17 | MAINS LINK / provisional terminal | 1, 2, 3 | O-MAINS |
| J20 | SNUBBER CONFIG | 1, 2, 3, 4 | O-SNUB |
| K1 | G6DN-1A-L DC5 | 1, 2, 5, 8 | O-RELAY |
| Q101 | MMBT3904 | 1, 2, 3 | O-HEAT |
| Q102 | BTA08-600SWRG | 1, 2, 3 | O-GATE |
| Q103 | MMBT3904 | 1, 2, 3 | O-RELAY |
| R101 | 330 | 1, 2 | O-OPTO |
| R102 | 470 | 1, 2 | O-HEAT |
| R103 | 10k | 1, 2 | O-HEAT |
| R104 | 360 / pulse-rated | 1, 2 | O-GATE |
| R105 | 330 | 1, 2 | O-GATE |
| R106 | 150 | 1, 2 | O-RELAY |
| R107 | 10k | 1, 2 | O-RELAY |
| R108 | 100 | 1, 2 | O-SNUB |
| TP1 | TOUCH LV GND | 1 | P-TOUCH |
| TP2 | GND / LOOP | 1 | P-PROBE |
| TP3 | +5V_SYS / LOOP | 1 | P-PROBE |
| TP4 | HEAT_EN / LOOP | 1 | P-PROBE |
| TP5 | CUT_EN / LOOP | 1 | P-PROBE |
| U2 | MOC3063S-TA1 / ZC | 1, 2, 3, 4, 5, 6 | O-OPTO |

Inventory reconciliation: 31 components, 73 symbol pins; every listed pin inherits the cited group assessment.

### motley-sensors

| Reference | Value | Every symbol pin | Assessment |
| --- | --- | --- | --- |
| C3 | 100n | 1, 2 | S-DECOUP |
| D40 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D41 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D42 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D43 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D44 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D45 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D46 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D47 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D48 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D49 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D50 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D51 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D52 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D53 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D54 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D55 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D60 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| D61 | PESD5V0S2BT,215 | 1, 2, 3 | ESD-DUAL |
| J2 | JST-SH 4p | 1, 2, 3, 4 | S-PORT |
| J3 | JST-SH 4p | 1, 2, 3, 4 | S-PORT |
| J4 | JST-SH 4p | 1, 2, 3, 4 | S-PORT |
| J5 | JST-SH 4p | 1, 2, 3, 4 | S-PORT |
| J6 | JST-SH 4p | 1, 2, 3, 4 | S-PORT |
| J7 | JST-SH 4p | 1, 2, 3, 4 | S-PORT |
| J8 | JST-SH 4p | 1, 2, 3, 4 | S-PORT |
| J9 | JST-SH 4p | 1, 2, 3, 4 | S-PORT |
| J10 | QWIIC UPSTREAM 2 | 1, 2, 3, 4 | S-QWIIC |
| J11 | QWIIC UPSTREAM 1 | 1, 2, 3, 4 | S-QWIIC |
| J12 | CARRIER / 3V3 I2C + RESET | 1, 2, 3, 4, 5 | S-INTERFACE |
| J13 | DEPLOYMENT PASS-THROUGH | 1, 2, 3, 4, 5 | S-INTERFACE |
| R1 | 10k | 1, 2 | S-RESET |
| R2 | 4k7 | 1, 2 | S-UPSTREAM |
| R3 | 4k7 | 1, 2 | S-UPSTREAM |
| R10 | 2k2 | 1, 2 | S-BRANCH |
| R11 | 2k2 | 1, 2 | S-BRANCH |
| R12 | 2k2 | 1, 2 | S-BRANCH |
| R13 | 2k2 | 1, 2 | S-BRANCH |
| R14 | 2k2 | 1, 2 | S-BRANCH |
| R15 | 2k2 | 1, 2 | S-BRANCH |
| R16 | 2k2 | 1, 2 | S-BRANCH |
| R17 | 2k2 | 1, 2 | S-BRANCH |
| R18 | 2k2 | 1, 2 | S-BRANCH |
| R19 | 2k2 | 1, 2 | S-BRANCH |
| R20 | 2k2 | 1, 2 | S-BRANCH |
| R21 | 2k2 | 1, 2 | S-BRANCH |
| R22 | 2k2 | 1, 2 | S-BRANCH |
| R23 | 2k2 | 1, 2 | S-BRANCH |
| R24 | 2k2 | 1, 2 | S-BRANCH |
| R25 | 2k2 | 1, 2 | S-BRANCH |
| R30 | 100 | 1, 2 | S-SERIES |
| R31 | 100 | 1, 2 | S-SERIES |
| R32 | 100 | 1, 2 | S-SERIES |
| R33 | 100 | 1, 2 | S-SERIES |
| R34 | 100 | 1, 2 | S-SERIES |
| R35 | 100 | 1, 2 | S-SERIES |
| R36 | 100 | 1, 2 | S-SERIES |
| R37 | 100 | 1, 2 | S-SERIES |
| R38 | 100 | 1, 2 | S-SERIES |
| R39 | 100 | 1, 2 | S-SERIES |
| R40 | 100 | 1, 2 | S-SERIES |
| R41 | 100 | 1, 2 | S-SERIES |
| R42 | 100 | 1, 2 | S-SERIES |
| R43 | 100 | 1, 2 | S-SERIES |
| R44 | 100 | 1, 2 | S-SERIES |
| R45 | 100 | 1, 2 | S-SERIES |
| R50 | 0 | 1, 2 | QW-POWER |
| R51 | 10k | 1, 2 | S-ADDRESS |
| R52 | 10k | 1, 2 | S-ADDRESS |
| R53 | 10k | 1, 2 | S-ADDRESS |
| R55 | 0 | 1, 2 | S-PULL-LINK |
| R56 | 0 | 1, 2 | S-PULL-LINK |
| SW1 | CTS 219-3MSTR / C3012353 | 1, 2, 3, 4, 5, 6 | S-ADDRESS |
| TP1 | TOUCH LV GND | 1 | P-TOUCH |
| TP2 | GND / LOOP | 1 | P-PROBE |
| TP3 | +3V3_SENS / LOOP | 1 | P-PROBE |
| TP4 | I2C_SDA / POST | 1 | P-PROBE |
| TP5 | I2C_SCL / POST | 1 | P-PROBE |
| TP6 | MUX_RESET_N / POST | 1 | P-PROBE |
| U1 | TCA9548APWR / 0x70..77 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24 | S-MUX |

Inventory reconciliation: 80 components, 224 symbol pins; every listed pin inherits the cited group assessment.

## Reviewed source identities

RQML validation and standard consistency/drift checks pass (exit 0). Full
repository pre-commit passes (exit 0), using command-scoped write access for
the two protected repository configuration files and writable caches/network
access as required. The two pin-bias requirements remain draft, unimplemented and
unverified; current total backlog is 25 unverified and 19 unimplemented requirements.
This report is not linked as a passing hardware test or maintained circuit
implementation. The authorized bias correction and subsequent ESD/access/
annotation revision update native sources and both PDFs, with structural
evidence in `verification.md`. MOT-HW-003 has actual annotation/checker
implementation and verification links; none claims electrical qualification.

The following are current reviewed native source identities after correction.

| Source | SHA-256 |
| --- | --- |
| Motley.kicad_sym | `e557a1de158ea9264df70cc5a8d7471576b9f40f7d6d8ba468c7652cd32a8367` |
| Motley.pretty/ESP32-C6-WROOM-1.kicad_mod | `5714c18133f1fcfaab88beddf92bcba0a4f37726f0f2404bd1e6ff7005934b15` |
| Motley.pretty/Mechanical_Pin_PTH_Study.kicad_mod | `f54ac1d1b04da3e525a552b15dc9589ddfac2b462b33ca2334a3d2665cac1b3e` |
| Motley.pretty/Relay_G6DN_1A_L_DC5_Study.kicad_mod | `21014fe1eb67b2dd9b7a64feea7bde100896bada291868d180b482a4793c3422` |
| Motley.pretty/TouchGround_8mm.kicad_mod | `87a41340e670c19887619da49b37fd0c87ddb3c8321462fae2d1748636b80149` |
| Motley.pretty/WireLoop_P2.54.kicad_mod | `e187fa4a7795c2ccfab4c438ead377fe4535129bee00f00a980a776ff0052bff` |
| Motley.pretty/WirePost_1mm.kicad_mod | `6e2e4600edccd3cac271d7a7e6a5a3381976f8831ad356b3cdd1c0ea7e5cf949` |
| MotleyPower.kicad_sym | `bb5dd2e24a42f15357ed9ce591cfa0a2b7825bbeff566270b977f35307f9d909` |
| carrier-access.kicad_sch | `d2975adc9f3ed7c2a1c331dab80b92d1335d8d95739fd4ec4cdc3ce22391e30b` |
| controller.kicad_sch | `73ad913970aaefdf7064b3c9dbf60e966d87927a17b64032b4971dea2a7c5c68` |
| fp-lib-table | `a5c48b258c5ef02214d292e07da18c5b0f2f0cffa773c8bb6dbd3c11b66e83e3` |
| heater-channel.kicad_sch | `a5e21f6c13f875cd1bafa127c820390dec9b6fb2c8c6a4f6351ef77532a2ca4c` |
| motley-ac-output.kicad_pcb | `4077efa09ecd78d1ebf3540ecd91999b5e94b0189125c69a015ce0322819447e` |
| motley-ac-output.kicad_pro | `e7f1284a2a56f64884d80ee2d9c7f5cd17d4b8881d7d1fb9b48631d5caa094e5` |
| motley-ac-output.kicad_sch | `a4b5362bec1d6d4618e0e1472f6e661e4edd6c1539982e938381e89d79c244d6` |
| motley-carrier.kicad_pcb | `164c14fe6d68409f88af1e43bfc27f96c7f0646b2f1676e9d1a0cfd3948f56da` |
| motley-carrier.kicad_pro | `31bbd4990d03d0c164afeed26713d3cc113a59b6d10c1993abb459209e5e807f` |
| motley-carrier.kicad_sch | `f8dac93b03c1891baf500a1f4f34ab9bd08301a25445c19373f6971c411d77d1` |
| motley-sensors.kicad_pcb | `01febb2380997c044b24faadc1214fdddabcc0d3caf6fc9a8082da2970716d35` |
| motley-sensors.kicad_pro | `ce8f50b8cfd251904732c6868ff9ba98d9a917059801e3d7280df4472ba5f527` |
| motley-sensors.kicad_sch | `9101d48a3edf78b480238c01cc1077844c0b2112728f11fbe50ca54b6e861257` |
| mux.kicad_sch | `95cad4a7e2b2de0fdb53f34afd9a9c5cbf2f3564efa499a6f3a48bfb01e6e47e` |
| output-access.kicad_sch | `bb3ae7d4c430cd54ea1f08a0c0b0d27f438aa3f653ab54c3ddf6c6e66c5e5cb4` |
| power.kicad_sch | `7d28e1aa3cb93cc1e64c3bd6dff164347795f66de0d59ac172272e7ce5a0bf6b` |
| qwiic-bench.kicad_sch | `7fb17c0ee7b63ad16440a31e12084ee211d8b876341c104258a17ca054eed457` |
| sensor-access.kicad_sch | `6aad7b16b91da885ea0939c474ca10f280e96e0b30cf052018afdbc436d40790` |
| sensor-port.kicad_sch | `ceaffb60fd391ac18a4592e845581049851a5bfae359873efe42c2160d1072e5` |
| sensor-ports.kicad_sch | `f6116bc20fe6297a3d46ca7931911f46a905f4e08deb4c41a356a99363aec671` |
| sym-lib-table | `786e986bca637e3f7e6d679adce07df1cfbaa1c744d39fc80148da961bcf599b` |
| usb-power.kicad_sch | `23ac8b24e12196fa678ff7587a1341882022814e03f54bffd8ceec622e474109` |
