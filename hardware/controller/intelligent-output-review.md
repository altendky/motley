# Intelligent output: pin, default, power and ESD review

Review date: 2026-11-14. This reviews the current exploratory schematics for
`motley-carrier`, `motley-ac-output` and `motley-sensors`. It supplements the
[pin-bias review](pin-bias-review.md) and [ESD/access review](esd-access-review.md).
For the changed circuits, the dispositions here supersede those documents'
earlier direct-GPIO output interface, MOC3063, R106=150 ohm and LP switched-power
descriptions. The original sensor assessments remain unchanged.

This is a source/connectivity and engineering-scenario review. It is not a
fabrication release, measured immunity result, thermal approval or proof of
default OFF at every temperature or connector state. No firmware was added by
the drawing. MOT-HW-003 governs native annotation integrity; the electrical,
AC-control, programming and persistence proposals remain design inputs rather
than completed product claims.

Fresh KiCad 10 XML exports of all three roots were independently enumerated
with Python's `xml.etree.ElementTree`, without using the CAD-generation helper
to infer connectivity. The inventory reconciles **247 components and 706 distinct
symbol-pin identities**: carrier 95/291, output 72/191, sensors 80/224. One carrier,
two outputs and one sensor board instantiate **319 components / 897 symbol pins**.
Counts include optional bare probe contacts and DNP parts, exclude virtual ERC
power flags and board-only mechanical holes, and count a repeated physical pad
number once electrically. The WROOM's repeated GND-29 lands retain one shared
electrical disposition. U41's physical NC lead 1 is explicitly included in the
current symbol and inventory. This inventory concerns the schematics; final PCB
geometry and source hashes are recorded separately after placement settles.

## Current electrical architecture

Carrier J15/J18 and output J14 now use six contacts. They carry common low-voltage
ground; these are not isolated buses between boards.

| Contact | Carrier J15/J18 | Output J14 | Default / disconnection disposition |
| --- | --- | --- | --- |
| 1 | GND | GND | Required local return. Full removal is different from a missing-ground partial connection; no guaranteed contact sequence. |
| 2 | +5V_SELECTED | +5V_LOGIC | Selected mains-derived/USB supply powers local logic and sensing. It does not feed the relay coil or optotriac LED. |
| 3 | LP_I2C_SDA | OUT_SDA | Open-drain bus with carrier R42=4k7 to main +3V3; no duplicate output-board pull-up. Missing carrier/pull-up leaves the disconnected bus undefined, so communication must not authorize actuation. |
| 4 | LP_I2C_SCL | OUT_SCL | Same disposition with R43=4k7. Clock stretching, capacitance and electrical timing need qualification. |
| 5 | LINE_SYNC | LINE_SYNC | Carrier push-pull source; each output has 1k series and 100k local LOW bias. Missing reference means invalid timing, not a valid zero crossing. |
| 6 | +5V_SYS | +5V_SYS | Raw mains-derived actuator supply, upstream of the output relay. Absent raw supply removes sustained LED/coil energy; stored energy and signal injection remain assessment cases. |

The output regulator U21 derives +3V3_OUT from +5V_LOGIC. USB-only power can
therefore keep the MCU and observations alive for commissioning while raw 5 V
actuators are unavailable. Opening the output relay does not remove its MCU
logic supply. There is no hardware interlock proving that only valid firmware
can assert a command: after initialization the MCU can intentionally drive HIGH.
Local pulls establish the intended high-impedance/reset defaults, subject to the
remaining leakage, ramp and transient limits.

Full cable removal, loss of SDA/SCL alone, loss of SYNC alone, logic-only power,
raw-only power, missing GND, externally powered service equipment, brownout and
partially inserted connectors are distinct states. The six-contact link expands
the old four-contact analysis; that earlier enumeration does not qualify this
new topology. Power links and common net names provide no hot-plug isolation.
Until tested, commissioning/reconfiguration should use the defined unpowered
connection procedure rather than assume arbitrary live insertion is supported.

## Changed carrier pins and default states

Unchanged U10 pins inherit C-MCU/C-BOOT/C-SENSEN/C-USBDATA/C-UART/C-LED from the
earlier review, including its unresolved sensor-domain injection, unused straps,
LED high-impedance and externally powered UART cases. The following changes are
explicit; an NC marker is a wiring choice, not proof of firmware input bias.

| U10 module pin / function | Normal / reset / ROM / disconnect assessment |
| --- | --- |
| 9 / GPIO1 | LINE_SYNC input through R87=1k. Source U41 is on the same main 3.3 V domain. No separate GPIO pull is fitted: a powered source drives the line; a powered U41 with inactive detector sees R85's HIGH. Do not interpret a constant HIGH/LOW as valid timing. ROM/application input configuration, power ramps and faulted-buffer behavior still need checking. GPIO1 is not a C6 strap. |
| 4 / GPIO4 | Restored NC; MTMS/strap behavior remains an explicit unused-pin/eFuse policy item. No external SYNC bias now perturbs this strap. |
| 8 / GPIO0; 26 / GPIO3; 27 / GPIO2 | Former direct CUT/HEAT connections removed; pins are NC. Configure unused pins appropriately after boot. Their reset/ROM behavior no longer directly commands either actuator. |
| 6 / GPIO6, 7 / GPIO7 | LP I2C SDA/SCL retain main 3.3 V 4k7 external pulls, including when the switched sensor rail is OFF. MTCK/MTDO/JTAG/reset alternate functions and LP-controller SDK support require deliberate configuration; avoid drive conflicts in ROM/recovery. No direct actuator path remains. |

The C6 straps include GPIO4/5/8/9/15. The choice of GPIO1 for SYNC avoids adding
a continuously driven timing signal to GPIO4's strap sampling. This does not
close the pre-existing policy for the other unused/boot straps.
[Espressif schematic checklist](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/schematic-checklist.html).

LP Qwiic J24/J26 power links R45/R47, connector power TVSs D43/D47 and pull-ups
R42/R43 now use **main +3V3**. HP Qwiic J23/J25 and the sensor deployment interface
stay on **switched +3V3_SENS**. Removing a 0-ohm power link neither disconnects
the data pair nor prevents an external supply from driving it. One host/supply,
no competing supplies and no unqualified powered signals into an unpowered
board remain necessary bench constraints. AP2112 reverse-current blocking is
not established. The sensor GPIO18/19/21 reset-pull/off-domain concern PB-02
is unchanged by moving the independent LP bank.

The selected PESD5V0S2BT signal clamp is specified at up to 45 pF per line.
Sixteen output-board I2C clamps alone can therefore contribute 720 pF per bus
line before carrier clamps, MCU pins or cables. With 4k7 pulls, the simple
30–70% RC rise estimate is already about 2.9 microseconds. Lower clock frequency
does not itself establish standard I2C rise-time compliance. A qualified larger
population may require different low-capacitance protection, pull-ups, topology
or a lower declared count; the sixteen-board target is not closed by address
space or the present two-output schematic. See the
[Nexperia capacitance specification](https://assets.nexperia.com/documents/data-sheet/PESD5V0S2BT.pdf).

## Shared line-reference pins

| Device / every physical lead | Bias and normal/reset/disconnect disposition |
| --- | --- |
| U40 ACPL-K376: 1 AC1, 4 AC2 | Mains-side AC input through four series R80-R83=17k, 68k total, between fused line and neutral. Analog threshold/current terminals; no pull to LV ground is appropriate. Input loss releases VO; thresholds, hysteresis, regional line range and transient survivability remain unqualified. |
| U40: 2 DC+, 3 DC−, 7 NC | Intentionally open for the chosen AC-input configuration. No logic pull. These terminals remain on their manufacturer's designated sides of the isolation barrier. |
| U40: 8 VCC, 5 GND | VCC from +5V_SELECTED through R84=240 ohm with C80=100n/C81=10n; GND to LV ground. Power pins need decoupling/domain bounds, not input bias. |
| U40: 6 VO | Open collector; R85=4k7 to main 3.3 V defines HIGH when detector is inactive/high impedance. It drives only U41's input, rather than sixteen board pulls directly. HIGH denotes a threshold gap or unavailable input, not mains absence proved healthy. |
| U41 SN74LVC1G17: 2 A | Connected to U40 VO/R85; HIGH defined by the external pull when VO is released. No extra input pull is required for this topology. Partial-power and fault behavior must still be bounded. |
| U41: 4 Y | Push-pull output through R86=47 ohm to LINE_SYNC. No DC pull is added at the source; receivers provide their local 100k LOW biases. Drives ESP observation and output timing inputs only. |
| U41: 5 VCC, 3 GND, 1 NC | Main 3.3 V with C82=100n; GND reference. Physical pin 1 is NC and left open; the current embedded symbol and footprint retain all five pins/lands. |

ACPL-K376 senses magnitude: the line has a gap around every zero crossing.
It does not provide an exact, invariant zero-voltage timestamp. Both gap edges,
threshold hysteresis, supply/temperature, waveform distortion, detector/buffer
delays and cable edges affect the inferred midpoint. All output boards must
share the reference's AC source/phase. Missing/implausible timing must inhibit
firing; implementing and validating that rule remains firmware work.

The 68k input network dissipates approximately V²/R: 0.212 W at 120 Vac and 1.025 W
at 264 Vac before accounting for detector voltage. This is a network estimate,
not resistor derating/surge approval. The four actual 2512/HV/1 W order codes,
working/pulse voltage, flame behavior, spacing and enclosure temperature are
unselected/unqualified. K376's filtered supply remains above 3 V in the illustrative
4.5 V input minus240 ohm×3 mA case (3.78 V); use actual tolerance/transients to close
that bound. [Broadcom AV02-2153EN, Tables 5/6](https://docs.broadcom.com/doc/AV02-2153EN).

Sixteen 100k output pulls present about 6.25k, drawing 0.528 mA at 3.3 V. Each
1k/100k receiver divider retains approximately 99.01% of the line voltage.
An unbuffered 4k7 pull-up would only deliver about 1.88 V into that fanout; the
push-pull buffer removes that concrete DC problem. Source 47 ohm and distributed
cable/TVS/input capacitance still affect edge shape. The deliberately pessimistic
TI guaranteed 2.4 V HIGH at 3 V/16 mA and local rail+1.5% scenario leaves only about 31 mV
above C011's 0.7 VDD threshold after the receiver divider alone. Including the
shared 47 ohm source resistor and sixteen 101k branches reduces that illustrative
margin to about 14 mV, before resistor tolerances, leakage or other loading.
Actual static current is much smaller than 16 mA, but this is not a closed corner
proof. Verify delivered HIGH/
LOW, partial-power Ioff conditions, ringing and phase jitter at actual fanout.
[SN74LVC1G17 datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf).

## Output MCU: all twenty pins

U20 is the STM32C011F6P6 TSSOP20 candidate. The following is the hardware pin
assignment and required treatment, not implemented application/loader behavior.
Reset, ROM, watchdog reset and an unprogrammed application must not be credited
with completed software protection. [ST DS13866 Rev 5](https://www.st.com/resource/en/datasheet/stm32c011d6.pdf).

| Pin / function | Pull/default and normal/reset/ROM/disconnection disposition |
| --- | --- |
| 1 PB7 | OUT_SDA runtime and ROM I2C1. Carrier 4k7 pull to main 3.3 V; no local output pull. Open-drain configuration; no arbitrary internal pull to local +3V3_OUT. Carrier removal removes the source pull. Powered bus/unpowered MCU injection and capacitance remain open. |
| 2 PC14 | NC. No external resistor selected; unused low-leakage/input policy required. No actuator load. |
| 3 PC15 | NC; same unused-pin assessment as 2. |
| 4 VDD/VDDA | +3V3_OUT with C202 = 100n/C203 = 1u; supply/ADC reference domain. No logic pull; qualify ramp/brownout and ADC supply noise. |
| 5 VSS/VSSA | Local GND. No logic pull; shared supply/reference return. |
| 6 PF2-NRST | Local R204 = 10k HIGH, C204 = 100n and SW21 momentary to GND; service J21.5. Open/omitted switch retains HIGH. Supported options must retain reset functionality. Ramp/debug/partial-power timing remains open. |
| 7 PA0 | CURRENT_V ADC through sensor 100 ohm/1n filter. Driven from same local rail when valid; no extra pull because it would bias the measurement. Sensor startup/invalidity must be observed, not interpreted as zero current. |
| 8 PA1 | OUT_VOLT_N digital input. R315 = 4k7 local +3V3_OUT pull defines HIGH when U31 releases; LOW marks detected magnitude. No extra pull. Constant HIGH can mean unavailable sensing; require valid observations before declaring output healthy. |
| 9 PA2 | CUT_EN relay command. R201 = 100k MCU-side LOW plus diode D102, R106 = 200 ohm and receiver-local R107 = 10k/C103 = 100n. High-Z/reset/unprogrammed states intend coil OFF. ROM does not use this as its selected I2C interface; actual startup/reset waveforms still need validation. Only deliberate firmware drive may energize it. |
| 10 PA3 | CURRENT_REF ADC. Reads U30's driven VREF_OUT through independent 100 ohm/1n filter; do not drive this pin or add a measurement-corrupting divider. Same-domain startup/off limits apply. |
| 11 PA4 | NC; unused-pin input/analog configuration policy, no external pull selected. |
| 12 PA5 | NC; same treatment as 11. |
| 13 PA6 | SYNC/TIM3_CH1 input through R202 = 1k with R203 = 100k local LOW. Disconnect gives LOW, not valid timing. No RC timing capacitor. Firmware must qualify both edges/period before enabling outputs. Powered source with unpowered local MCU remains an injection case. |
| 14 PA7 | HEAT_EN/TIM3_CH2. R200 = 100k MCU-side LOW, D101 blocking diode, R102 = 470 ohm and receiver R103 = 10k/C102 = 1n. High-Z/reset intends LED OFF. Firmware-controlled HIGH and pulses require verified timing/drive, including ROM and watchdog transition tests. |
| 15 PA8 | NC; unused-pin policy, no external pull selected. |
| 16 PA9/PA11 | NC; retain the package's selectable pin mapping and ROM USART considerations. No actuator path. |
| 17 PA10/PA12 | NC; same treatment as 16. |
| 18 PA13 | SWDIO to J21.3. Retain debugger/MCU-defined behavior; no extra external pull. Service-header exposure/partial-power and debug halt behavior need procedure/testing. |
| 19 PA14 | SWCLK/BOOT0 to J21.4. R206 = 47k LOW for RUN; recovery shunt SW20 applies local 3.3 V through R205 = 1k. Remove shunt for ordinary SWD. Intentional recovery HIGH overrides RUN pull; contention/current/options need qualification. |
| 20 PB6 | OUT_SCL runtime/ROM I2C1. Same upstream-pull/reset/disconnection assessment as 1. |

U21 AP2112: pin 1 VIN and pin 3 EN are hard tied to +5V_LOGIC; pin 2 GND is local
ground; pin 5 OUT feeds +3V3_OUT with C200 = 1u input/C201 = 4.7u output bypass; pin 4 is
true NC. EN is not floating and receives no separate pull. Selected-rail ramps,
capacitor/inrush/stability, thermal limits, output discharge and reverse-current
paths remain to be qualified. J21 service contacts 1/2 are local 3.3 V reference/GND,
not permission for a debugger to inject a competing supply; contacts 3/4/5 inherit
the SWD/reset dispositions above.
[AP2112 datasheet](https://www.diodes.com/datasheet/download/AP2112.pdf).

ROM I2C uses PB6/PB7 and 7-bit 0x64. One **new/default-address board** may be
commissioned while differently addressed boards remain present; recovery of
multiple responders at 0x64 is not supported by this wiring alone. Runtime
identity must use the factory 96-bit UID, not treat the mutable I2C address as
identity. Reservation of 0x64 and other agreed/common addresses, commissioning,
updates, fault association and ESP-side protocol implementation remain software
work. [ST AN2606 Rev 71](https://www.st.com/resource/en/application_note/an2606-.pdf).

The system-memory ROM cannot be overwritten by an ordinary application-flash
update. Mutable option configuration can nevertheless prevent pin recovery.
Supported provisioning must preserve NBOOT_SEL=0, NBOOT1=1, BOOT_LOCK=0 and reset
functionality and exclude RDP2. An accessible shunt/reset/SWD fallback does not
prove that an ESP can recover every option-byte state. The32 KB proposal
(dispatcher, two approximately 10 KB images, redundant configuration/selector)
has no measured firmware fit or power-cut proof. Double-buffered verified
persistence, verified image selection and option-byte mutation remain unresolved
MOT-STOR-001 work. [ST RM0490](https://www.st.com/resource/en/reference_manual/dm00781702.pdf).

The internal independent watchdog supplies a possible hardware clocked reset
mechanism. Every MCU still needs an implemented progress signal/feed policy,
bounded response and tests. No external supervisor or autonomous fault relay
interlock was added. Configurable communications-failure responses (OFF, ON,
hold latest, hold configured setting) and reset/recovery-safe transitions are
software obligations; they must not silently turn invalid timing into permission
to fire. A reset's off-bias is separate from a deliberate, validated ON policy.

## Changed actuator pins and drive margins

| Group / pins | Current disposition |
| --- | --- |
| Q101 B/E/C; D101 pins 1/2; R102/R103; C102 | MCU command→blocking diode→470 ohm base resistor;10k B-E pull-down and 1n filter are receiver-local. Emitter GND; collector sinks U2 LED. OFF bias survives a missing command; no collector pull-down is appropriate.1n×10k=10 us nominal, replacing1 ms. Stored BJT charge and actual optical/triac release remain unmeasured. |
| U2 VO3053-X007T pins 1 A / 2 C | Raw 5 V current-limited LED through R101 = 270 ohm/Q101; no separate logic pull. Random-phase 600 V candidate supports scheduled leading-edge phase-angle control and whole-cycle burst control in principle. Actual temperature/pulse-width firing remains to be qualified. |
| U2 pins 3/5 | True NC; leave open, no pull. |
| U2 pins 4 MT1/6 MT2 | Mains-side phototriac/gate path; no connection/pull to LV GND. Exact option 7 local footprint has 1.52×1.78 mm pads,9.53 mm row centers and 8.01 mm inner copper gap, derived from the Vishay drawing rather than generic SMDIP6 assumptions. Assembly/paste/insulation still need qualification. |
| Q102 A1/A2/G; R104/R105 | Existing BTA08-600SWRG and 330 ohm G-to-A1 shunt retained. R104 now 430 ohm pulse-rated 2512 candidate. Switching, inrush, dv/dt, minimum holding/load current, mains range, gate pulse rating and heatsinking remain open. |
| Q103 B/E/C; D102 pins 1/2; R106/R107; C103 | Diode plus 200 ohm 1% base resistor,10k/100n receiver B-E bias/filter. Emitter GND, collector coil low-side. High-Z/reset intends relay deenergized. No arbitrary collector pull-down. |
| K1 coil/contacts; D1 | Raw 5 V coil with flyback diode. Normally-open contacts provide commanded cutoff, not a guarantee against welded contacts or a deenergization-time bound. Diode/storage/mechanical delay must enter fault timing. |

R101 LED estimate at raw 5 V−5%, VF 1.5 V and VCEsat 0.3 V gives 10.9 mA with nominal 270
ohm or 10.4 mA at +5% resistance. This exceeds VO3053's 5 mA maximum IFT condition,
not a guaranteed full-temperature/pulse margin or a minimum non-trigger current.
R102 base drive is approximately 3.8 mA nominal; its loaded MCU level, diode drop
and actual transistor saturation/leakage must be bounded. The active candidate
is **Vishay VO3053-X007T**, not obsolete onsemi MOC3053SR2M. JLC assembly availability
is unconfirmed; a catalog/LCSC identifier is not assembly qualification.
[Vishay VO3052/VO3053 Rev 2.5](https://www.vishay.com/docs/83749/vo3052.pdf).

R106=200 ohm 1% changes the previous capacitor-charge upper bound. At absolute
VDDmax 3.6 V, initially discharged capacitor, zero credited diode/B-E drop and
198 ohm minimum, GPIO peak is bounded by 3.6/198=**18.18 mA**, below the 20 mA absolute
single-pin limit. That absolute limit is not a recommended continuous current.
The previous 150 ohm did not meet that deliberately conservative bound.

A separate pessimistic steady-drive scenario uses 3.3 V−1.5%, VOH=VDD−0.4 V,
diode VF 1 V, VBE 0.95 V,202 ohm and the 10k bleed: about **4.36 mA base current**.
At 5.25 V and Omron's 139 ohm−10% coil resistance at 23°C, approximately 42 mA coil
current needs 4.2 mA for forced beta 10. That is narrow scenario margin, not a
full-temperature proof. Cold-coil resistance, loaded MCU VOH, BJT variant,
saturation, diode leakage and release delay remain unresolved. C103 retains
100n, so its 10k decay is nominal 1 ms. [ST GPIO limits](https://www.st.com/resource/en/datasheet/stm32c011d6.pdf),
[onsemi MMBT3904 reference](https://www.onsemi.com/download/data-sheet/pdf/mmbt3904lt1-d.pdf),
[Omron G6DN](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g6dn.pdf).

The original diode/bias analysis remains useful for the local driver path, but
cannot establish missing-ground safety with the new I2C/SYNC/dual-power harness.
No resistor guarantees OFF if firmware or another fault actively drives HIGH.
Inductive-load suitability is deferred; the drawing is not general approval for
motors/transformers. Higher-current capability, fusing and thermal capability
also remain separate review items.

## Feedback pins, no-load detection and regional components

| U30 TMCS1123B5AQDVGR pin | Bias/default/operating disposition |
| --- | --- |
| 1 IN+, 2 IN− | Series mains conductor from CUT_L_UNSENSED to OUTLET_L, respectively; no wire bypass to J10live. No LV pull. Inrush/overrange, conductor heating and complete isolation layout remain open. |
| 3 GND,8VS | Local GND/+3V3_OUT with C300 = 100n/C301 = 1u. No logic pull. Valid supply/startup precedes valid current data. |
| 4 ALERT,7 OC | Unused open-collector outputs hard tied GND according to TI Table 5-1; retain their true symbol types. Not used as an independent hardware cutoff. |
| 5 VREF_OUT | Actively generated reference **output**, separately sampled through R301 = 100/C303 = 1n as CURRENT_REF. Do not drive it from a divider/reference input assumption. |
| 6 VOUT | Driven current output through R300 = 100/C302 = 1n as CURRENT_V. No added pull that offsets ADC data. Offset, ADC settling and filter phase require qualification. |
| 9 VOC | Unused threshold input tied VS per manufacturer's guidance. Defined supply-level state, not a floating high-impedance input. |
| 10NC | True NC. Leave open. |

The chosen 150 mV/A variant/reference gives an illustrative approximately±10.3 A
linear range at 3.3 V; lamp inrush can saturate it. Gain/offset/calibration, ADC
source/sample timing and synchronized acquisition remain unimplemented. Sensor
startup is 34 ms after a valid supply condition; unavailable/clipped measurements
must not count as a healthy zero. Current can support RMS/phase/load analysis
and redundant observations, but current alone cannot establish a shorted triac
with no external load. The outlet-voltage detector provides its own burden for
that case. [TI TMCS1123 RevD](https://www.ti.com/lit/ds/symlink/tmcs1123.pdf).

U31 ACPL-K370 pin 1 AC1/pin 4 AC2 observe OUTLET_L versus AC_N through R310-R313.
Pins 2DC+/3 DC−/7 NC are open for AC use. Pin 8 VCC uses +5V_LOGIC through R314 = 240
ohm and C304 = 100n/C305 = 10n; pin 5 GND is LV GND. Pin 6 VO has R315 = 4k7 to +3V3_OUT,
so inactivity releases OUT_VOLT_N HIGH. These are analog/supply/open-collector
dispositions, not a reason for arbitrary pulls on mains or unused DC terminals.

Default 90–132 Vac assembly uses 4×8k2 (32.8k total) and omits R316. The proposed
180–264 Vac assembly uses 4×12k and fits R316 = 3k9 across the AC detector input.
This is a **regional BOM variant**, not an automatically universal circuit.
The added high-line shunt raises rejection of low leakage; each variant still
needs guaranteed threshold/hysteresis and waveform analysis. Approximate network
heat is 0.44 W at 120 V in the low-line network and 1.45 W at 264 V in the high-line
series network. Select voltage/pulse/flame-rated parts and check each resistor,
shunt and detector's temperature. K370 filtered VCC is 3.54 V in the illustrative
4.5 V−240 ohm×4 mA case; actual tolerances and transients remain open.

U31 is intentionally unsmoothed. Compare its pulses with qualified shared line
timing and commands; do not interpret one sample or a constant inactive level as
an output-health guarantee. Triac leakage, fitted 10n snubber (about 0.45 mA
capacitive current at 120 V/60 Hz), detector burden, leakage tolerances, stray
capacitance and disconnected-load waveforms must be jointly checked. The
regional shunt and finite input burden aim to distinguish leakage from a live
shorted output, but no corner/bench proof is claimed. Intentional near 100%
drive may defer shorted-triac observation until a suitable commanded-off window;
window policy and fault response are software work. Threshold devices also
do not measure precise mains voltage or replace input surge qualification.

## External/service ESD and touch/probe access

The original ESD-DUAL/ESD-POWER groups remain candidate component topologies,
not board immunity results. Carrier D34 now clamps LP SDA/SCL; D35 clamps
LINE_SYNC and leaves its second channel NC. D36 raw 5 V and D37 selected 5 V are
separate supply clamps. Output D110 clamps OUT_SDA/OUT_SCL; D112 clamps SYNC
with its unused branch NC; D111 protects raw 5 V and D113 logic 5 V. PESD5V0S2BT
branches 1/2 are bidirectional shunts to pin 3 GND, not normal powered steering
diodes; ESD5Z6.0T1G is a6 V-standoff shunt, pin 1 K to supply/pin 2 A to GND.
Neither provides a DC input pull or proof that residual clamp voltage is safe
for a3.3 V IC. Leakage,45 pF-per branch loading, missing-ground paths, pulse current
and short connector-return routing remain open. The new output MCU's local
SWD/reset/recovery access has no added connector-local TVS; its handling scope
and whether that needs protection remain explicit service-design decisions.

LP power clamps follow main 3.3 V; HP sensor clamps follow switched 3.3 V. The USB
data/VBUS protection, provisional CC resistors in the selected panel assembly,
unshielded internal harness and unmet preference for a sturdier shielded panel
connection remain as assessed previously. No mains terminal is clamped to LV GND,
and no PE-to-LV GND bond was introduced. Return geometry and a clamp's component
rating do not establish system ESD performance.

Each TP1 remains a **top/front exposed LV GND touch reference**, not a PE point
or permission to touch powered mains. TP2 is the LV GND clip reference. Existing
output TP3/4/5 expose raw 5 V/HEAT_EN/CUT_EN. New optional bare loops TP20..24 expose
+3V3_OUT, LINE_SYNC, CURRENT_V, CURRENT_REF and OUT_VOLT_N. Unfitted pads inherit
their nets' original bias; a probe can load or capacitively disturb those nets.
These are not independent high-impedance inputs needing duplicate pulls.
Keep clip/finger/tool access and earth-referenced instruments clear of mains;
actual PCB touch-side, clearance and isolation corridors are reviewed separately.

## Power and outstanding qualification

The current 1 A / 5 V source has not been qualified for sixteen active output boards.
Using earlier engineering estimates,16 nominal 36 mA coils contribute576 mA,
opto LEDs approximately 220 mA and current sensors176 mA typical: approximately
972 mA before MCUs, driver base current, carrier/radio, regulators, voltage
detectors or temperature probes. Sensor maximum-current accounting alone can
reach232 mA for sixteen. Exact operating totals, AC/DC supply derating and radio/
startup peaks must be calculated for two outputs and separately for expanded
capacity. Address capacity is not power capacity.

USB-only commissioning likewise does not authorize arbitrary USB sources to
power all sixteen logic boards. Confirm current entitlement, cable drop,
TPS2116/path limits, aggregate local/input capacitance, inrush, reverse currents,
plug sequence and brownout. Shared voltage-detector pull-ups or a powered bus
can outlive a different local rail. Default-OFF testing must include raw-only,
logic-only, reset/ROM/debug halt/watchdog, corrupted configuration, supply ramps,
every relevant connector loss and stored-energy decay. No new default/noise
curves, ESD immunity, thermal tests or power-cut firmware tests were performed.

## Native ERC findings retained honestly

Fresh native carrier ERC reports one existing library mismatch warning for PS1
IRM-05-5. Output ERC reports exactly these two errors:

| Finding | Native item | Disposition |
| --- | --- | --- |
| Open collector connected to power output | U30 pin 4 ALERT, UUID 44fc109f-807f-447a-9775-6fdcf75e9afd, against GND power flag #FLG11 | Manufacturer-directed unused-pin GND connection; not a falsely declared passive pin. |
| Open collector connected to power output | U30 pin 7 OC, UUID 14555a4f-a62c-4759-82ea-a2b5fb80f02c, against GND power flag #FLG11 | Same narrow disposition. |

TI TMCS1123 RevD, Table 5-1 specifies the unused ALERT/OC terminations to GND
and VOC to VS. Their true open-collector types and physical GND connections are
retained; no global severity change or incorrect pin-type edit was used to hide
the findings. These are bounded review exceptions, not a claim that ERC passes
without findings. [Manufacturer Table 5-1, page 4](https://www.ti.com/lit/ds/symlink/tmcs1123.pdf).

## Inventory assessment keys

For unchanged references, the assessment key below refers to the identically
named group in [pin-bias-review.md](pin-bias-review.md#pin-group-dispositions).
The original S-MUX/S-RESET/S-UPSTREAM/S-PULL-LINK/S-ADDRESS/S-BRANCH/S-INTERFACE/
S-PORT/S-DECOUP/S-SERIES/S-QWIIC sensor assessments and their open qualifications
are inherited unchanged. ESD-DUAL, ESD-POWER, P-TOUCH and P-PROBE inherit the
handling limitations above and in [esd-access-review.md](esd-access-review.md).

| New/overriding key | Applicable disposition in this review |
| --- | --- |
| C-MCU-NEW | Changed carrier pins/R87; same-domain driven SYNC, removed direct outputs, unused-pin and boot policy. |
| BUS-6 | Six-contact logic/raw power plus I2C/SYNC; full/partial disconnect and supply states. |
| LP-MAIN | Main 3.3 V LP Qwiic power, pull-ups and socket power clamps; one supply/host, no signal isolation. |
| BUS-ESD | Updated bus/SYNC/split-power clamp assignments; unused branchesNC; no logic bias or immunity claim. |
| LINE-ACPL | U40 and input/filter/pull-up components; isolated threshold reference and unqualified heat/timing. |
| LINE-BUF | U41/source 47 ohm/decoupling; push-pull fanout and physical NC pin 1. |
| O-MCU | All 20 U20 pins; bias, reset/ROM/domain and unimplemented firmware obligations. |
| O-LDO | U21 and local input/output bypass; hard EN, NC pin 4, no arbitrary pull on supply pins. |
| O-MCU-BIAS | MCU OFF/SYNC pulls, decoupling and reset network; passive terminals inherit their named net function. |
| O-RECOVERY / O-RESET / O-SERVICE | Shunt 1k/47k boot choice,10k/100n reset, momentary switch and five-pin service connector. Open contacts retain their fixed bias; not all option states recoverable. |
| O-HEAT-NEW / O-OPTO-NEW / O-GATE-NEW / O-RELAY-NEW | Updated random-phase LED270 ohm,1n gate filter,430 ohm mains gate resistor and 200 ohm 1% relay drive. The rest of O-HEAT/O-RELAY/O-GATE remains the earlier topology with these changed shared-net limits. |
| O-CURRENT | U30, separate ADC 100 ohm/1n filters and supply capacitors. VREF is driven; unused outputs GND per TI. |
| O-VOLT | U31, regional input/shunt networks, local 4k7 output pull and 240 ohm supply filter. DNP shunt contacts are passive mains nodes, not unassessed floating logic pins. |

## Complete fresh component and pin inventory

Each row below contains every pin actually instantiated in the root XML, its
symbol function/type and exported net. `+no_connect` records an explicit NC
marker; an `unconnected-…` net is not silently treated as biased. All listed
passive/power pins inherit the named circuit disposition instead of acquiring
arbitrary logic pulls. The inventory is an independent one-time audit, not a
new maintained test that merely mirrors the generator.


### motley-carrier

| Reference / value | Every symbol pin: number, function, type → net | Assessment |
| --- | --- | --- |
| **C1** — 100n / 16V | `1`  (passive) → `+5V_SYS`<br>`2`  (passive) → `GND` | C-DECOUP |
| **C2** — 10u / 16V | `1`  (passive) → `+5V_SYS`<br>`2`  (passive) → `GND` | C-DECOUP |
| **C10** — 1u / 10V | `1`  (passive) → `ESP_EN`<br>`2`  (passive) → `GND` | C-BOOT |
| **C11** — 10u / 10V | `1`  (passive) → `+3V3`<br>`2`  (passive) → `GND` | C-DECOUP |
| **C12** — 100n / 10V | `1`  (passive) → `+3V3`<br>`2`  (passive) → `GND` | C-DECOUP |
| **C20** — 1u / 16V | `1`  (passive) → `+5V_SYS`<br>`2`  (passive) → `GND` | C-PMUX |
| **C21** — 1u / 16V | `1`  (passive) → `USB_VBUS_RAW`<br>`2`  (passive) → `GND` | C-PMUX |
| **C22** — 22u / 10V | `1`  (passive) → `+5V_SELECTED`<br>`2`  (passive) → `GND` | C-PMUX |
| **C23** — 22u / 10V | `1`  (passive) → `+3V3`<br>`2`  (passive) → `GND` | C-LDO |
| **C24** — 1u / 16V | `1`  (passive) → `+5V_SELECTED`<br>`2`  (passive) → `GND` | C-LDO |
| **C25** — 4.7u / 10V | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `GND` | C-LDO |
| **C26** — 100n / 16V | `1`  (passive) → `+3V3`<br>`2`  (passive) → `GND` | C-USBDATA |
| **C27** — 100n / 16V | `1`  (passive) → `+3V3`<br>`2`  (passive) → `GND` | C-VBUS |
| **C80** — 100n / 16V | `1`  (passive) → `Net-(U40-VCC)`<br>`2`  (passive) → `GND` | LINE-ACPL |
| **C81** — 10n / 16V | `1`  (passive) → `Net-(U40-VCC)`<br>`2`  (passive) → `GND` | LINE-ACPL |
| **C82** — 100n / 16V | `1`  (passive) → `+3V3`<br>`2`  (passive) → `GND` | LINE-BUF |
| **D10** — STATUS | `1` K (passive) → `GND`<br>`2` A (passive) → `Net-(D10-A)` | C-LED |
| **D20** — USBLC6-2SC6 | `1` I/O1 (passive) → `Net-(J21-D+)`<br>`2` GND (passive) → `GND`<br>`3` I/O2 (passive) → `Net-(J21-D-)`<br>`4` I/O2 (passive) → `Net-(J21-D-)`<br>`5` VBUS (passive) → `USB_VBUS_RAW`<br>`6` I/O1 (passive) → `Net-(J21-D+)` | C-ESD |
| **D30** — PESD5V0S2BT,215 | `1` IO1 (passive) → `+3V3_SENS`<br>`2` IO2 (passive) → `I2C_SDA`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D31** — PESD5V0S2BT,215 | `1` IO1 (passive) → `I2C_SCL`<br>`2` IO2 (passive) → `MUX_RESET_N`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D32** — PESD5V0S2BT,215 | `1` IO1 (passive) → `+3V3`<br>`2` IO2 (passive) → `UART_RX`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D33** — PESD5V0S2BT,215 | `1` IO1 (passive) → `UART_TX`<br>`2` IO2 (passive+no_connect) → `unconnected-(D33-IO2-Pad2)`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D34** — PESD5V0S2BT,215 | `1` IO1 (passive) → `LP_I2C_SDA`<br>`2` IO2 (passive) → `LP_I2C_SCL`<br>`3` REF (passive) → `GND` | BUS-ESD |
| **D35** — PESD5V0S2BT,215 | `1` IO1 (passive) → `LINE_SYNC`<br>`2` IO2 (passive+no_connect) → `unconnected-(D35-IO2-Pad2)`<br>`3` REF (passive) → `GND` | BUS-ESD |
| **D36** — ESD5Z6.0T1G | `1` K (passive) → `+5V_SYS`<br>`2` A (passive) → `GND` | ESD-POWER |
| **D37** — ESD5Z6.0T1G | `1` K (passive) → `+5V_SELECTED`<br>`2` A (passive) → `GND` | BUS-ESD |
| **D38** — ESD5Z6.0T1G | `1` K (passive) → `USB_VBUS_RAW`<br>`2` A (passive) → `GND` | ESD-POWER |
| **D40** — PESD5V0S2BT,215 | `1` IO1 (passive) → `I2C_SDA`<br>`2` IO2 (passive) → `I2C_SCL`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D41** — PESD5V0S2BT,215 | `1` IO1 (passive) → `/Independent Qwiic bench ports/QWIIC_HP_3V3`<br>`2` IO2 (passive+no_connect) → `unconnected-(D41-IO2-Pad2)`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D42** — PESD5V0S2BT,215 | `1` IO1 (passive) → `LP_I2C_SDA`<br>`2` IO2 (passive) → `LP_I2C_SCL`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D43** — PESD5V0S2BT,215 | `1` IO1 (passive) → `/Independent Qwiic bench ports/QWIIC_LP_3V3`<br>`2` IO2 (passive+no_connect) → `unconnected-(D43-IO2-Pad2)`<br>`3` REF (passive) → `GND` | LP-MAIN |
| **D44** — PESD5V0S2BT,215 | `1` IO1 (passive) → `I2C_SDA`<br>`2` IO2 (passive) → `I2C_SCL`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D45** — PESD5V0S2BT,215 | `1` IO1 (passive) → `/Independent Qwiic bench ports/QWIIC_HP2_3V3`<br>`2` IO2 (passive+no_connect) → `unconnected-(D45-IO2-Pad2)`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D46** — PESD5V0S2BT,215 | `1` IO1 (passive) → `LP_I2C_SDA`<br>`2` IO2 (passive) → `LP_I2C_SCL`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D47** — PESD5V0S2BT,215 | `1` IO1 (passive) → `/Independent Qwiic bench ports/QWIIC_LP2_3V3`<br>`2` IO2 (passive+no_connect) → `unconnected-(D47-IO2-Pad2)`<br>`3` REF (passive) → `GND` | LP-MAIN |
| **F1** — T6.3A / 250V provisional | `1`  (passive) → `/Mains input and isolated 5 V supply/AC_L_IN`<br>`2`  (passive) → `AC_L_FUSED` | C-MAINS |
| **J1** — AC INPUT / cord or inlet | `1` Pin_1 (passive) → `/Mains input and isolated 5 V supply/AC_L_IN`<br>`2` Pin_2 (passive) → `AC_N`<br>`3` Pin_3 (passive) → `PE` | C-MAINS |
| **J13** — SENSOR LINK | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+3V3_SENS`<br>`3` Pin_3 (passive) → `I2C_SDA`<br>`4` Pin_4 (passive) → `I2C_SCL`<br>`5` Pin_5 (passive) → `MUX_RESET_N` | C-SENSIF |
| **J15** — OUTPUT BUS / LOGIC + ACTUATOR POWER | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+5V_SELECTED`<br>`3` Pin_3 (passive) → `LP_I2C_SDA`<br>`4` Pin_4 (passive) → `LP_I2C_SCL`<br>`5` Pin_5 (passive) → `LINE_SYNC`<br>`6` Pin_6 (passive) → `+5V_SYS` | BUS-6 |
| **J16** — MAINS LINK / provisional terminal | `1` Pin_1 (passive) → `AC_L_FUSED`<br>`2` Pin_2 (passive) → `AC_N`<br>`3` Pin_3 (passive) → `PE` | C-MAINS |
| **J18** — OUTPUT BUS / LOGIC + ACTUATOR POWER | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+5V_SELECTED`<br>`3` Pin_3 (passive) → `LP_I2C_SDA`<br>`4` Pin_4 (passive) → `LP_I2C_SCL`<br>`5` Pin_5 (passive) → `LINE_SYNC`<br>`6` Pin_6 (passive) → `+5V_SYS` | BUS-6 |
| **J19** — MAINS LINK / provisional terminal | `1` Pin_1 (passive) → `AC_L_FUSED`<br>`2` Pin_2 (passive) → `AC_N`<br>`3` Pin_3 (passive) → `PE` | C-MAINS |
| **J21** — PANEL USB-C / ADAFRUIT 6153 | `1` VBUS (passive) → `USB_VBUS_RAW`<br>`2` GND (passive) → `GND`<br>`3` D+ (passive) → `Net-(J21-D+)`<br>`4` D- (passive) → `Net-(J21-D-)`<br>`5` CC1 (passive+no_connect) → `unconnected-(J21-CC1-Pad5)`<br>`6` CC2 (passive+no_connect) → `unconnected-(J21-CC2-Pad6)` | C-USBPORT |
| **J22** — 3V3 UART SERVICE / NO 5V | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+3V3`<br>`3` Pin_3 (passive) → `UART_TX`<br>`4` Pin_4 (passive) → `UART_RX` | C-UART |
| **J23** — QWIIC MAIN / 3V3 OUT | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `/Independent Qwiic bench ports/QWIIC_HP_3V3`<br>`3` Pin_3 (passive) → `I2C_SDA`<br>`4` Pin_4 (passive) → `I2C_SCL` | C-QWIIC |
| **J24** — QWIIC LP / 3V3 OUT | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `/Independent Qwiic bench ports/QWIIC_LP_3V3`<br>`3` Pin_3 (passive) → `LP_I2C_SDA`<br>`4` Pin_4 (passive) → `LP_I2C_SCL` | LP-MAIN |
| **J25** — QWIIC MAIN / 3V3 OUT | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `/Independent Qwiic bench ports/QWIIC_HP2_3V3`<br>`3` Pin_3 (passive) → `I2C_SDA`<br>`4` Pin_4 (passive) → `I2C_SCL` | C-QWIIC |
| **J26** — QWIIC LP / 3V3 OUT | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `/Independent Qwiic bench ports/QWIIC_LP2_3V3`<br>`3` Pin_3 (passive) → `LP_I2C_SDA`<br>`4` Pin_4 (passive) → `LP_I2C_SCL` | LP-MAIN |
| **PS1** — IRM-05-5 / 5V 1A | `1` AC/N (power_in) → `AC_N`<br>`2` AC/L (power_in) → `AC_L_FUSED`<br>`3` -Vo (power_out) → `GND`<br>`4` +Vo (power_out) → `+5V_SYS` | C-MAINS |
| **R10** — 10k | `1`  (passive) → `+3V3`<br>`2`  (passive) → `ESP_EN` | C-BOOT |
| **R11** — 10k | `1`  (passive) → `+3V3`<br>`2`  (passive) → `Net-(U10-GPIO9)` | C-BOOT |
| **R12** — 10k | `1`  (passive) → `+3V3`<br>`2`  (passive) → `Net-(U10-GPIO8)` | C-BOOT |
| **R13** — 22 | `1`  (passive) → `Net-(U10-GPIO12/USB_D-)`<br>`2`  (passive) → `USB_DM` | C-USBDATA |
| **R14** — 22 | `1`  (passive) → `Net-(U10-GPIO13/USB_D+)`<br>`2`  (passive) → `USB_DP` | C-USBDATA |
| **R15** — 2k2 | `1`  (passive) → `Net-(U10-GPIO10)`<br>`2`  (passive) → `Net-(D10-A)` | C-LED |
| **R20** — 316k / 0.1% | `1`  (passive) → `+5V_SYS`<br>`2`  (passive) → `/USB input, source selection and 3V3 rails/MAINS_PRIORITY_SENSE` | C-PMUX |
| **R21** — 100k / 0.1% | `1`  (passive) → `/USB input, source selection and 3V3 rails/MAINS_PRIORITY_SENSE`<br>`2`  (passive) → `GND` | C-PMUX |
| **R22** — 10k / EN pull-down | `1`  (passive) → `SENS_PWR_EN`<br>`2`  (passive) → `GND` | C-SENSEN |
| **R23** — 10k / VBUS bleed | `1`  (passive) → `USB_VBUS_RAW`<br>`2`  (passive) → `GND` | C-RAWUSB |
| **R24** — 47k / default DISCONNECT | `1`  (passive) → `+3V3`<br>`2`  (passive) → `/USB input, source selection and 3V3 rails/USB_DATA_OE_N` | C-VBUS |
| **R25** — 226k / 1% | `1`  (passive) → `USB_VBUS_RAW`<br>`2`  (passive) → `Net-(U24-IN-)` | C-VBUS |
| **R26** — 100k / 1% | `1`  (passive) → `Net-(U24-IN-)`<br>`2`  (passive) → `GND` | C-VBUS |
| **R40** — 10k | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `I2C_SDA` | C-QWPULL |
| **R41** — 10k | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `I2C_SCL` | C-QWPULL |
| **R42** — 4k7 | `1`  (passive) → `+3V3`<br>`2`  (passive) → `LP_I2C_SDA` | LP-MAIN |
| **R43** — 4k7 | `1`  (passive) → `+3V3`<br>`2`  (passive) → `LP_I2C_SCL` | LP-MAIN |
| **R44** — 0 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `/Independent Qwiic bench ports/QWIIC_HP_3V3` | QW-POWER |
| **R45** — 0 | `1`  (passive) → `+3V3`<br>`2`  (passive) → `/Independent Qwiic bench ports/QWIIC_LP_3V3` | LP-MAIN |
| **R46** — 0 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `/Independent Qwiic bench ports/QWIIC_HP2_3V3` | QW-POWER |
| **R47** — 0 | `1`  (passive) → `+3V3`<br>`2`  (passive) → `/Independent Qwiic bench ports/QWIIC_LP2_3V3` | LP-MAIN |
| **R80** — 17k / 1W / HV | `1`  (passive) → `AC_L_FUSED`<br>`2`  (passive) → `Net-(R80-Pad2)` | LINE-ACPL |
| **R81** — 17k / 1W / HV | `1`  (passive) → `Net-(R80-Pad2)`<br>`2`  (passive) → `Net-(U40-AC1)` | LINE-ACPL |
| **R82** — 17k / 1W / HV | `1`  (passive) → `Net-(R82-Pad1)`<br>`2`  (passive) → `Net-(U40-AC2)` | LINE-ACPL |
| **R83** — 17k / 1W / HV | `1`  (passive) → `AC_N`<br>`2`  (passive) → `Net-(R82-Pad1)` | LINE-ACPL |
| **R84** — 240 | `1`  (passive) → `+5V_SELECTED`<br>`2`  (passive) → `Net-(U40-VCC)` | LINE-ACPL |
| **R85** — 4k7 | `1`  (passive) → `+3V3`<br>`2`  (passive) → `Net-(U40-VO)` | LINE-ACPL |
| **R86** — 47 | `1`  (passive) → `Net-(R86-Pad1)`<br>`2`  (passive) → `LINE_SYNC` | LINE-BUF |
| **R87** — 1k | `1`  (passive) → `LINE_SYNC`<br>`2`  (passive) → `Net-(U10-GPIO1/ADC1_CH1/XTAL_32K_N)` | C-MCU-NEW |
| **SW1** — RESET | `1` 1 (passive) → `GND`<br>`2` 2 (passive) → `ESP_EN` | C-BOOT |
| **SW2** — BOOT / GPIO9 | `1` 1 (passive) → `Net-(U10-GPIO9)`<br>`2` 2 (passive) → `GND` | C-BOOT |
| **TP1** — TOUCH LV GND; optional bare contact | `1` 1 (passive) → `GND` | P-TOUCH |
| **TP2** — GND / LOOP; optional bare contact | `1` 1 (passive) → `GND` | P-PROBE |
| **TP3** — +5V_SYS / LOOP; optional bare contact | `1` 1 (passive) → `+5V_SYS` | P-PROBE |
| **TP4** — +5V_SELECTED / LOOP; optional bare contact | `1` 1 (passive) → `+5V_SELECTED` | P-PROBE |
| **TP5** — +3V3 / LOOP; optional bare contact | `1` 1 (passive) → `+3V3` | P-PROBE |
| **TP6** — +3V3_SENS / LOOP; optional bare contact | `1` 1 (passive) → `+3V3_SENS` | P-PROBE |
| **TP7** — USB_VBUS_RAW / LOOP; optional bare contact | `1` 1 (passive) → `USB_VBUS_RAW` | P-PROBE |
| **U10** — ESP32-C6-WROOM-1-N8 / C5366877 | `1` GND (power_in) → `GND`<br>`2` 3V3 (power_in) → `+3V3`<br>`3` EN/CHIP_PU (input) → `ESP_EN`<br>`4` MTMS/GPIO4/ADC1_CH4 (bidirectional+no_connect) → `unconnected-(U10-MTMS/GPIO4/ADC1_CH4-Pad4)`<br>`5` MTDI/GPIO5/ADC1_CH5 (bidirectional+no_connect) → `unconnected-(U10-MTDI/GPIO5/ADC1_CH5-Pad5)`<br>`6` MTCK/GPIO6/ADC1_CH6 (bidirectional) → `LP_I2C_SDA`<br>`7` MTDO/GPIO7 (bidirectional) → `LP_I2C_SCL`<br>`8` GPIO0/ADC1_CH0/XTAL_32K_P (bidirectional+no_connect) → `unconnected-(U10-GPIO0/ADC1_CH0/XTAL_32K_P-Pad8)`<br>`9` GPIO1/ADC1_CH1/XTAL_32K_N (bidirectional) → `Net-(U10-GPIO1/ADC1_CH1/XTAL_32K_N)`<br>`10` GPIO8 (bidirectional) → `Net-(U10-GPIO8)`<br>`11` GPIO10 (bidirectional) → `Net-(U10-GPIO10)`<br>`12` GPIO11 (bidirectional) → `SENS_PWR_EN`<br>`13` GPIO12/USB_D- (bidirectional) → `Net-(U10-GPIO12/USB_D-)`<br>`14` GPIO13/USB_D+ (bidirectional) → `Net-(U10-GPIO13/USB_D+)`<br>`15` GPIO9 (bidirectional) → `Net-(U10-GPIO9)`<br>`16` GPIO18 (bidirectional) → `I2C_SCL`<br>`17` GPIO19 (bidirectional) → `I2C_SDA`<br>`18` GPIO20 (bidirectional+no_connect) → `unconnected-(U10-GPIO20-Pad18)`<br>`19` GPIO21 (bidirectional) → `MUX_RESET_N`<br>`20` GPIO22 (bidirectional+no_connect) → `unconnected-(U10-GPIO22-Pad20)`<br>`21` GPIO23 (bidirectional+no_connect) → `unconnected-(U10-GPIO23-Pad21)`<br>`22` NC (no_connect) → `unconnected-(U10-NC-Pad22)`<br>`23` GPIO15 (bidirectional+no_connect) → `unconnected-(U10-GPIO15-Pad23)`<br>`24` U0RXD/GPIO17 (bidirectional) → `UART_RX`<br>`25` U0TXD/GPIO16 (bidirectional) → `UART_TX`<br>`26` GPIO3/ADC1_CH3 (bidirectional+no_connect) → `unconnected-(U10-GPIO3/ADC1_CH3-Pad26)`<br>`27` GPIO2/ADC1_CH2 (bidirectional+no_connect) → `unconnected-(U10-GPIO2/ADC1_CH2-Pad27)`<br>`28` GND (passive) → `GND`<br>`29` GND (passive) → `GND` | C-MCU-NEW |
| **U20** — TPS2116DRLR | `1` GND (power_in) → `GND`<br>`2` VOUT (power_out) → `+5V_SELECTED`<br>`3` VIN1 (power_in) → `+5V_SYS`<br>`4` PR1 (input) → `/USB input, source selection and 3V3 rails/MAINS_PRIORITY_SENSE`<br>`5` MODE (input) → `+5V_SYS`<br>`6` VIN2 (power_in) → `USB_VBUS_RAW`<br>`7` VOUT (passive) → `+5V_SELECTED`<br>`8` ST (open_collector+no_connect) → `unconnected-(U20-ST-Pad8)` | C-PMUX |
| **U21** — AP2112K-3.3TRG1 / ESP | `1` VIN (power_in) → `+5V_SELECTED`<br>`2` GND (power_in) → `GND`<br>`3` EN (input) → `+5V_SELECTED`<br>`4` NC (no_connect) → `unconnected-(U21-NC-Pad4)`<br>`5` VOUT (power_out) → `+3V3` | C-LDO |
| **U22** — AP2112K-3.3TRG1 / SENS | `1` VIN (power_in) → `+5V_SELECTED`<br>`2` GND (power_in) → `GND`<br>`3` EN (input) → `SENS_PWR_EN`<br>`4` NC (no_connect) → `unconnected-(U22-NC-Pad4)`<br>`5` VOUT (power_out) → `+3V3_SENS` | C-LDO |
| **U23** — TS3USB221ERSER | `1` 1D+ (bidirectional) → `Net-(J21-D+)`<br>`2` 1D- (bidirectional) → `Net-(J21-D-)`<br>`3` 2D+ (bidirectional+no_connect) → `unconnected-(U23-2D+-Pad3)`<br>`4` 2D- (bidirectional+no_connect) → `unconnected-(U23-2D--Pad4)`<br>`5` GND (power_in) → `GND`<br>`6` ~{OE} (input) → `/USB input, source selection and 3V3 rails/USB_DATA_OE_N`<br>`7` D- (bidirectional) → `USB_DM`<br>`8` D+ (bidirectional) → `USB_DP`<br>`9` S (input) → `GND`<br>`10` VCC (power_in) → `+3V3` | C-USBDATA |
| **U24** — TLV3011BIDBVR / VBUS VALID | `1` OUT (open_collector) → `/USB input, source selection and 3V3 rails/USB_DATA_OE_N`<br>`2` GND (power_in) → `GND`<br>`3` IN+ (input) → `/USB input, source selection and 3V3 rails/USB_VREF_1V242`<br>`4` IN- (input) → `Net-(U24-IN-)`<br>`5` REF (output) → `/USB input, source selection and 3V3 rails/USB_VREF_1V242`<br>`6` VCC (power_in) → `+3V3` | C-VBUS |
| **U40** — ACPL-K376-000E / LINE REF | `1` AC1 (passive) → `Net-(U40-AC1)`<br>`2` DC+ (passive+no_connect) → `unconnected-(U40-DC+-Pad2)`<br>`3` DC- (passive+no_connect) → `unconnected-(U40-DC--Pad3)`<br>`4` AC2 (passive) → `Net-(U40-AC2)`<br>`5` GND (power_in) → `GND`<br>`6` VO (open_collector) → `Net-(U40-VO)`<br>`7` NC (no_connect) → `unconnected-(U40-NC-Pad7)`<br>`8` VCC (power_in) → `Net-(U40-VCC)` | LINE-ACPL |
| **U41** — SN74LVC1G17DBVR | `1` NC (no_connect) → `unconnected-(U41-NC-Pad1)`<br>`2`  (input) → `Net-(U40-VO)`<br>`3` GND (power_in) → `GND`<br>`4`  (output) → `Net-(R86-Pad1)`<br>`5` VCC (power_in) → `+3V3` | LINE-BUF |

Reconciliation: **95 components / 291 distinct symbol-pin identities**.

### motley-ac-output

| Reference / value | Every symbol pin: number, function, type → net | Assessment |
| --- | --- | --- |
| **C101** — 10n X2 | `1`  (passive) → `Net-(C101-Pad1)`<br>`2`  (passive) → `Net-(J20-Pin_1)` | O-SNUB |
| **C102** — 1n / 50V | `1`  (passive) → `Net-(Q101-B)`<br>`2`  (passive) → `GND` | O-HEAT-NEW |
| **C103** — 100n / 50V | `1`  (passive) → `Net-(Q103-B)`<br>`2`  (passive) → `GND` | O-RELAY |
| **C200** — 1u / 16V | `1`  (passive) → `+5V_LOGIC`<br>`2`  (passive) → `GND` | O-LDO |
| **C201** — 4.7u / 10V | `1`  (passive) → `+3V3_OUT`<br>`2`  (passive) → `GND` | O-LDO |
| **C202** — 100n / 16V | `1`  (passive) → `+3V3_OUT`<br>`2`  (passive) → `GND` | O-MCU-BIAS |
| **C203** — 1u / 10V | `1`  (passive) → `+3V3_OUT`<br>`2`  (passive) → `GND` | O-MCU-BIAS |
| **C204** — 100n / 16V | `1`  (passive) → `/Local output MCU, power and recovery/OUT_NRST`<br>`2`  (passive) → `GND` | O-MCU-BIAS |
| **C300** — 100n / 10V | `1`  (passive) → `+3V3_OUT`<br>`2`  (passive) → `GND` | O-CURRENT |
| **C301** — 1u / 10V | `1`  (passive) → `+3V3_OUT`<br>`2`  (passive) → `GND` | O-CURRENT |
| **C302** — 1n / 10V | `1`  (passive) → `CURRENT_V`<br>`2`  (passive) → `GND` | O-CURRENT |
| **C303** — 1n / 10V | `1`  (passive) → `CURRENT_REF`<br>`2`  (passive) → `GND` | O-CURRENT |
| **C304** — 100n / 16V | `1`  (passive) → `Net-(U31-VCC)`<br>`2`  (passive) → `GND` | O-VOLT |
| **C305** — 10n / 16V | `1`  (passive) → `Net-(U31-VCC)`<br>`2`  (passive) → `GND` | O-VOLT |
| **D1** — 1N4148W | `1` K (passive) → `+5V_SYS`<br>`2` A (passive) → `Net-(D1-A)` | O-RELAY |
| **D101** — 1N4148W | `1` K (passive) → `Net-(D101-K)`<br>`2` A (passive) → `HEAT_EN` | O-HEAT |
| **D102** — 1N4148W | `1` K (passive) → `Net-(D102-K)`<br>`2` A (passive) → `CUT_EN` | O-RELAY |
| **D110** — PESD5V0S2BT,215 | `1` IO1 (passive) → `OUT_SDA`<br>`2` IO2 (passive) → `OUT_SCL`<br>`3` REF (passive) → `GND` | BUS-ESD |
| **D111** — ESD5Z6.0T1G | `1` K (passive) → `+5V_SYS`<br>`2` A (passive) → `GND` | BUS-ESD |
| **D112** — PESD5V0S2BT,215 | `1` IO1 (passive) → `LINE_SYNC`<br>`2` IO2 (passive+no_connect) → `unconnected-(D112-IO2-Pad2)`<br>`3` REF (passive) → `GND` | BUS-ESD |
| **D113** — ESD5Z6.0T1G | `1` K (passive) → `+5V_LOGIC`<br>`2` A (passive) → `GND` | BUS-ESD |
| **F2** — T3.15A provisional | `1`  (passive) → `AC_L_FUSED`<br>`2`  (passive) → `Net-(Q102-A2)` | O-MAINS |
| **J10** — Qualtek 738W-X2/03 (wired) | `1` Pin_1 (passive) → `OUTLET_L`<br>`2` Pin_2 (passive) → `AC_N`<br>`3` Pin_3 (passive) → `PE` | O-MAINS |
| **J14** — OUTPUT BUS / LOGIC + ACTUATOR POWER | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+5V_LOGIC`<br>`3` Pin_3 (passive) → `OUT_SDA`<br>`4` Pin_4 (passive) → `OUT_SCL`<br>`5` Pin_5 (passive) → `LINE_SYNC`<br>`6` Pin_6 (passive) → `+5V_SYS` | BUS-6 |
| **J17** — MAINS LINK / provisional terminal | `1` Pin_1 (passive) → `AC_L_FUSED`<br>`2` Pin_2 (passive) → `AC_N`<br>`3` Pin_3 (passive) → `PE` | O-MAINS |
| **J20** — SNUBBER CONFIG | `1` Pin_1 (passive) → `Net-(J20-Pin_1)`<br>`2` Pin_2 (passive) → `/Heater 1/TRIAC_A1`<br>`3` Pin_3 (passive) → `Net-(J20-Pin_1)`<br>`4` Pin_4 (passive) → `/Heater 1/TRIAC_A1` | O-SNUB |
| **J21** — 3V3 SWD / SERVICE | `1` Pin_1 (passive) → `+3V3_OUT`<br>`2` Pin_2 (passive) → `GND`<br>`3` Pin_3 (passive) → `/Local output MCU, power and recovery/OUT_SWDIO`<br>`4` Pin_4 (passive) → `/Local output MCU, power and recovery/OUT_BOOT0_SWCLK`<br>`5` Pin_5 (passive) → `/Local output MCU, power and recovery/OUT_NRST` | O-SERVICE |
| **K1** — G6DN-1A-L DC5 | `1` COIL (passive) → `+5V_SYS`<br>`2` COIL (passive) → `Net-(D1-A)`<br>`5` NO (passive) → `/Heater 1/TRIAC_A1`<br>`8` COM (passive) → `CUT_L_UNSENSED` | O-RELAY |
| **Q101** — MMBT3904 | `1` B (input) → `Net-(Q101-B)`<br>`2` E (passive) → `GND`<br>`3` C (passive) → `Net-(Q101-C)` | O-HEAT |
| **Q102** — BTA08-600SWRG | `1` A1 (passive) → `/Heater 1/TRIAC_A1`<br>`2` A2 (passive) → `Net-(Q102-A2)`<br>`3` G (input) → `Net-(Q102-G)` | O-GATE |
| **Q103** — MMBT3904 | `1` B (input) → `Net-(Q103-B)`<br>`2` E (passive) → `GND`<br>`3` C (passive) → `Net-(D1-A)` | O-RELAY |
| **R101** — 270 | `1`  (passive) → `+5V_SYS`<br>`2`  (passive) → `Net-(R101-Pad2)` | O-OPTO-NEW |
| **R102** — 470 | `1`  (passive) → `Net-(D101-K)`<br>`2`  (passive) → `Net-(Q101-B)` | O-HEAT |
| **R103** — 10k | `1`  (passive) → `Net-(Q101-B)`<br>`2`  (passive) → `GND` | O-HEAT |
| **R104** — 430 / pulse-rated | `1`  (passive) → `Net-(R104-Pad1)`<br>`2`  (passive) → `Net-(Q102-A2)` | O-GATE-NEW |
| **R105** — 330 | `1`  (passive) → `Net-(Q102-G)`<br>`2`  (passive) → `/Heater 1/TRIAC_A1` | O-GATE |
| **R106** — 200 / 1% | `1`  (passive) → `Net-(D102-K)`<br>`2`  (passive) → `Net-(Q103-B)` | O-RELAY-NEW |
| **R107** — 10k | `1`  (passive) → `Net-(Q103-B)`<br>`2`  (passive) → `GND` | O-RELAY |
| **R108** — 100 | `1`  (passive) → `Net-(Q102-A2)`<br>`2`  (passive) → `Net-(C101-Pad1)` | O-SNUB |
| **R200** — 100k / OFF | `1`  (passive) → `HEAT_EN`<br>`2`  (passive) → `GND` | O-MCU-BIAS |
| **R201** — 100k / OFF | `1`  (passive) → `CUT_EN`<br>`2`  (passive) → `GND` | O-MCU-BIAS |
| **R202** — 1k / SYNC | `1`  (passive) → `/Local output MCU, power and recovery/SYNC_IN`<br>`2`  (passive) → `LINE_SYNC` | O-MCU-BIAS |
| **R203** — 100k / SYNC default | `1`  (passive) → `/Local output MCU, power and recovery/SYNC_IN`<br>`2`  (passive) → `GND` | O-MCU-BIAS |
| **R204** — 10k | `1`  (passive) → `+3V3_OUT`<br>`2`  (passive) → `/Local output MCU, power and recovery/OUT_NRST` | O-MCU-BIAS |
| **R205** — 1k / boot bias | `1`  (passive) → `+3V3_OUT`<br>`2`  (passive) → `Net-(SW20-A)` | O-MCU-BIAS |
| **R206** — 47k / RUN | `1`  (passive) → `/Local output MCU, power and recovery/OUT_BOOT0_SWCLK`<br>`2`  (passive) → `GND` | O-MCU-BIAS |
| **R300** — 100 | `1`  (passive) → `Net-(U30-VOUT)`<br>`2`  (passive) → `CURRENT_V` | O-CURRENT |
| **R301** — 100 | `1`  (passive) → `Net-(U30-VREF_OUT)`<br>`2`  (passive) → `CURRENT_REF` | O-CURRENT |
| **R310** — 8k2 | `1`  (passive) → `OUTLET_L`<br>`2`  (passive) → `Net-(R310-Pad2)` | O-VOLT |
| **R311** — 8k2 | `1`  (passive) → `Net-(R310-Pad2)`<br>`2`  (passive) → `Net-(R311-Pad2)` | O-VOLT |
| **R312** — 8k2 | `1`  (passive) → `Net-(R311-Pad2)`<br>`2`  (passive) → `Net-(R312-Pad2)` | O-VOLT |
| **R313** — 8k2 | `1`  (passive) → `Net-(R312-Pad2)`<br>`2`  (passive) → `Net-(U31-AC1)` | O-VOLT |
| **R314** — 240 | `1`  (passive) → `+5V_LOGIC`<br>`2`  (passive) → `Net-(U31-VCC)` | O-VOLT |
| **R315** — 4k7 | `1`  (passive) → `+3V3_OUT`<br>`2`  (passive) → `OUT_VOLT_N` | O-VOLT |
| **R316** — 3k9 / DNP; DNP | `1`  (passive) → `Net-(U31-AC1)`<br>`2`  (passive) → `AC_N` | O-VOLT |
| **SW20** — RUN open / RECOVERY closed | `1` A (passive) → `Net-(SW20-A)`<br>`2` B (passive) → `/Local output MCU, power and recovery/OUT_BOOT0_SWCLK` | O-RECOVERY |
| **SW21** — RESET | `1` 1 (passive) → `/Local output MCU, power and recovery/OUT_NRST`<br>`2` 2 (passive) → `GND` | O-RESET |
| **TP1** — TOUCH LV GND; optional bare contact | `1` 1 (passive) → `GND` | P-TOUCH |
| **TP2** — GND / LOOP; optional bare contact | `1` 1 (passive) → `GND` | P-PROBE |
| **TP3** — +5V_SYS / LOOP; optional bare contact | `1` 1 (passive) → `+5V_SYS` | P-PROBE |
| **TP4** — HEAT_EN / LOOP; optional bare contact | `1` 1 (passive) → `HEAT_EN` | P-PROBE |
| **TP5** — CUT_EN / LOOP; optional bare contact | `1` 1 (passive) → `CUT_EN` | P-PROBE |
| **TP20** — +3V3_OUT; optional bare contact | `1` 1 (passive) → `+3V3_OUT` | P-PROBE |
| **TP21** — LINE_SYNC; optional bare contact | `1` 1 (passive) → `LINE_SYNC` | P-PROBE |
| **TP22** — CURRENT_V; optional bare contact | `1` 1 (passive) → `CURRENT_V` | P-PROBE |
| **TP23** — CURRENT_REF; optional bare contact | `1` 1 (passive) → `CURRENT_REF` | P-PROBE |
| **TP24** — OUT_VOLT_N; optional bare contact | `1` 1 (passive) → `OUT_VOLT_N` | P-PROBE |
| **U2** — VO3053-X007T / RANDOM PHASE | `1`  (passive) → `Net-(R101-Pad2)`<br>`2`  (passive) → `Net-(Q101-C)`<br>`3` NC (no_connect) → `unconnected-(U2-NC-Pad3)`<br>`4`  (passive) → `Net-(Q102-G)`<br>`5` NC (no_connect) → `unconnected-(U2-NC-Pad5)`<br>`6`  (passive) → `Net-(R104-Pad1)` | O-OPTO-NEW |
| **U20** — STM32C011F6P6 / C5456198 | `1` PB7 (bidirectional) → `OUT_SDA`<br>`2` PC14 (bidirectional+no_connect) → `unconnected-(U20-PC14-Pad2)`<br>`3` PC15 (bidirectional+no_connect) → `unconnected-(U20-PC15-Pad3)`<br>`4` VDD (power_in) → `+3V3_OUT`<br>`5` VSS (power_in) → `GND`<br>`6` PF2 (bidirectional) → `/Local output MCU, power and recovery/OUT_NRST`<br>`7` PA0 (bidirectional) → `CURRENT_V`<br>`8` PA1 (bidirectional) → `OUT_VOLT_N`<br>`9` PA2 (bidirectional) → `CUT_EN`<br>`10` PA3 (bidirectional) → `CURRENT_REF`<br>`11` PA4 (bidirectional+no_connect) → `unconnected-(U20-PA4-Pad11)`<br>`12` PA5 (bidirectional+no_connect) → `unconnected-(U20-PA5-Pad12)`<br>`13` PA6 (bidirectional) → `/Local output MCU, power and recovery/SYNC_IN`<br>`14` PA7 (bidirectional) → `HEAT_EN`<br>`15` PA8 (bidirectional+no_connect) → `unconnected-(U20-PA8-Pad15)`<br>`16` PA9/PA11 (bidirectional+no_connect) → `unconnected-(U20-PA9/PA11-Pad16)`<br>`17` PA10/PA12 (bidirectional+no_connect) → `unconnected-(U20-PA10/PA12-Pad17)`<br>`18` PA13 (bidirectional) → `/Local output MCU, power and recovery/OUT_SWDIO`<br>`19` PA14 (bidirectional) → `/Local output MCU, power and recovery/OUT_BOOT0_SWCLK`<br>`20` PB6 (bidirectional) → `OUT_SCL` | O-MCU |
| **U21** — AP2112K-3.3TRG1 / LOGIC | `1` VIN (power_in) → `+5V_LOGIC`<br>`2` GND (power_in) → `GND`<br>`3` EN (input) → `+5V_LOGIC`<br>`4` NC (no_connect) → `unconnected-(U21-NC-Pad4)`<br>`5` VOUT (power_out) → `+3V3_OUT` | O-LDO |
| **U30** — TMCS1123B5AQDVGR | `1` IN+ (passive) → `CUT_L_UNSENSED`<br>`2` IN- (passive) → `OUTLET_L`<br>`3` GND (power_in) → `GND`<br>`4` ALERT (open_collector) → `GND`<br>`5` VREF_OUT (output) → `Net-(U30-VREF_OUT)`<br>`6` VOUT (output) → `Net-(U30-VOUT)`<br>`7` OC (open_collector) → `GND`<br>`8` VS (power_in) → `+3V3_OUT`<br>`9` VOC (input) → `+3V3_OUT`<br>`10` NC (no_connect) → `unconnected-(U30-NC-Pad10)` | O-CURRENT |
| **U31** — ACPL-K370-500E | `1` AC1 (passive) → `Net-(U31-AC1)`<br>`2` DC+ (passive+no_connect) → `unconnected-(U31-DC+-Pad2)`<br>`3` DC- (passive+no_connect) → `unconnected-(U31-DC--Pad3)`<br>`4` AC2 (passive) → `AC_N`<br>`5` GND (power_in) → `GND`<br>`6` VO (open_collector) → `OUT_VOLT_N`<br>`7` NC (no_connect) → `unconnected-(U31-NC-Pad7)`<br>`8` VCC (power_in) → `Net-(U31-VCC)` | O-VOLT |

Reconciliation: **72 components / 191 distinct symbol-pin identities**.

### motley-sensors

| Reference / value | Every symbol pin: number, function, type → net | Assessment |
| --- | --- | --- |
| **C3** — 100n | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `GND` | S-DECOUP |
| **D40** — PESD5V0S2BT,215 | `1` IO1 (passive) → `/Sensor ports/Port 0/SDA_CABLE`<br>`2` IO2 (passive) → `/Sensor ports/Port 0/SCL_CABLE`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D41** — PESD5V0S2BT,215 | `1` IO1 (passive) → `+3V3_SENS`<br>`2` IO2 (passive+no_connect) → `unconnected-(D41-IO2-Pad2)`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D42** — PESD5V0S2BT,215 | `1` IO1 (passive) → `/Sensor ports/Port 1/SDA_CABLE`<br>`2` IO2 (passive) → `/Sensor ports/Port 1/SCL_CABLE`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D43** — PESD5V0S2BT,215 | `1` IO1 (passive) → `+3V3_SENS`<br>`2` IO2 (passive+no_connect) → `unconnected-(D43-IO2-Pad2)`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D44** — PESD5V0S2BT,215 | `1` IO1 (passive) → `/Sensor ports/Port 2/SDA_CABLE`<br>`2` IO2 (passive) → `/Sensor ports/Port 2/SCL_CABLE`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D45** — PESD5V0S2BT,215 | `1` IO1 (passive) → `+3V3_SENS`<br>`2` IO2 (passive+no_connect) → `unconnected-(D45-IO2-Pad2)`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D46** — PESD5V0S2BT,215 | `1` IO1 (passive) → `/Sensor ports/Port 3/SDA_CABLE`<br>`2` IO2 (passive) → `/Sensor ports/Port 3/SCL_CABLE`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D47** — PESD5V0S2BT,215 | `1` IO1 (passive) → `+3V3_SENS`<br>`2` IO2 (passive+no_connect) → `unconnected-(D47-IO2-Pad2)`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D48** — PESD5V0S2BT,215 | `1` IO1 (passive) → `/Sensor ports/Port 4/SDA_CABLE`<br>`2` IO2 (passive) → `/Sensor ports/Port 4/SCL_CABLE`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D49** — PESD5V0S2BT,215 | `1` IO1 (passive) → `+3V3_SENS`<br>`2` IO2 (passive+no_connect) → `unconnected-(D49-IO2-Pad2)`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D50** — PESD5V0S2BT,215 | `1` IO1 (passive) → `/Sensor ports/Port 5/SDA_CABLE`<br>`2` IO2 (passive) → `/Sensor ports/Port 5/SCL_CABLE`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D51** — PESD5V0S2BT,215 | `1` IO1 (passive) → `+3V3_SENS`<br>`2` IO2 (passive+no_connect) → `unconnected-(D51-IO2-Pad2)`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D52** — PESD5V0S2BT,215 | `1` IO1 (passive) → `/Sensor ports/Port 6/SDA_CABLE`<br>`2` IO2 (passive) → `/Sensor ports/Port 6/SCL_CABLE`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D53** — PESD5V0S2BT,215 | `1` IO1 (passive) → `+3V3_SENS`<br>`2` IO2 (passive+no_connect) → `unconnected-(D53-IO2-Pad2)`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D54** — PESD5V0S2BT,215 | `1` IO1 (passive) → `/Sensor ports/Port 7/SDA_CABLE`<br>`2` IO2 (passive) → `/Sensor ports/Port 7/SCL_CABLE`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D55** — PESD5V0S2BT,215 | `1` IO1 (passive) → `+3V3_SENS`<br>`2` IO2 (passive+no_connect) → `unconnected-(D55-IO2-Pad2)`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D60** — PESD5V0S2BT,215 | `1` IO1 (passive) → `+3V3_SENS`<br>`2` IO2 (passive) → `I2C_SDA`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **D61** — PESD5V0S2BT,215 | `1` IO1 (passive) → `I2C_SCL`<br>`2` IO2 (passive) → `MUX_RESET_N`<br>`3` REF (passive) → `GND` | ESD-DUAL |
| **J2** — JST-SH 4p | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+3V3_SENS`<br>`3` Pin_3 (passive) → `/Sensor ports/Port 0/SDA_CABLE`<br>`4` Pin_4 (passive) → `/Sensor ports/Port 0/SCL_CABLE` | S-PORT |
| **J3** — JST-SH 4p | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+3V3_SENS`<br>`3` Pin_3 (passive) → `/Sensor ports/Port 1/SDA_CABLE`<br>`4` Pin_4 (passive) → `/Sensor ports/Port 1/SCL_CABLE` | S-PORT |
| **J4** — JST-SH 4p | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+3V3_SENS`<br>`3` Pin_3 (passive) → `/Sensor ports/Port 2/SDA_CABLE`<br>`4` Pin_4 (passive) → `/Sensor ports/Port 2/SCL_CABLE` | S-PORT |
| **J5** — JST-SH 4p | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+3V3_SENS`<br>`3` Pin_3 (passive) → `/Sensor ports/Port 3/SDA_CABLE`<br>`4` Pin_4 (passive) → `/Sensor ports/Port 3/SCL_CABLE` | S-PORT |
| **J6** — JST-SH 4p | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+3V3_SENS`<br>`3` Pin_3 (passive) → `/Sensor ports/Port 4/SDA_CABLE`<br>`4` Pin_4 (passive) → `/Sensor ports/Port 4/SCL_CABLE` | S-PORT |
| **J7** — JST-SH 4p | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+3V3_SENS`<br>`3` Pin_3 (passive) → `/Sensor ports/Port 5/SDA_CABLE`<br>`4` Pin_4 (passive) → `/Sensor ports/Port 5/SCL_CABLE` | S-PORT |
| **J8** — JST-SH 4p | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+3V3_SENS`<br>`3` Pin_3 (passive) → `/Sensor ports/Port 6/SDA_CABLE`<br>`4` Pin_4 (passive) → `/Sensor ports/Port 6/SCL_CABLE` | S-PORT |
| **J9** — JST-SH 4p | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+3V3_SENS`<br>`3` Pin_3 (passive) → `/Sensor ports/Port 7/SDA_CABLE`<br>`4` Pin_4 (passive) → `/Sensor ports/Port 7/SCL_CABLE` | S-PORT |
| **J10** — QWIIC UPSTREAM 2 | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `/QWIIC_UP_3V3`<br>`3` Pin_3 (passive) → `I2C_SDA`<br>`4` Pin_4 (passive) → `I2C_SCL` | S-QWIIC |
| **J11** — QWIIC UPSTREAM 1 | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `/QWIIC_UP_3V3`<br>`3` Pin_3 (passive) → `I2C_SDA`<br>`4` Pin_4 (passive) → `I2C_SCL` | S-QWIIC |
| **J12** — CARRIER / 3V3 I2C + RESET | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+3V3_SENS`<br>`3` Pin_3 (passive) → `I2C_SDA`<br>`4` Pin_4 (passive) → `I2C_SCL`<br>`5` Pin_5 (passive) → `MUX_RESET_N` | S-INTERFACE |
| **J13** — DEPLOYMENT PASS-THROUGH | `1` Pin_1 (passive) → `GND`<br>`2` Pin_2 (passive) → `+3V3_SENS`<br>`3` Pin_3 (passive) → `I2C_SDA`<br>`4` Pin_4 (passive) → `I2C_SCL`<br>`5` Pin_5 (passive) → `MUX_RESET_N` | S-INTERFACE |
| **R1** — 10k | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `MUX_RESET_N` | S-RESET |
| **R2** — 4k7 | `1`  (passive) → `Net-(R2-Pad1)`<br>`2`  (passive) → `I2C_SDA` | S-UPSTREAM |
| **R3** — 4k7 | `1`  (passive) → `Net-(R3-Pad1)`<br>`2`  (passive) → `I2C_SCL` | S-UPSTREAM |
| **R10** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SDA0` | S-BRANCH |
| **R11** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SCL0` | S-BRANCH |
| **R12** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SDA1` | S-BRANCH |
| **R13** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SCL1` | S-BRANCH |
| **R14** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SDA2` | S-BRANCH |
| **R15** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SCL2` | S-BRANCH |
| **R16** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SDA3` | S-BRANCH |
| **R17** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SCL3` | S-BRANCH |
| **R18** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SDA4` | S-BRANCH |
| **R19** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SCL4` | S-BRANCH |
| **R20** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SDA5` | S-BRANCH |
| **R21** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SCL5` | S-BRANCH |
| **R22** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SDA6` | S-BRANCH |
| **R23** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SCL6` | S-BRANCH |
| **R24** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SDA7` | S-BRANCH |
| **R25** — 2k2 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `SCL7` | S-BRANCH |
| **R30** — 100 | `1`  (passive) → `SDA0`<br>`2`  (passive) → `/Sensor ports/Port 0/SDA_CABLE` | S-SERIES |
| **R31** — 100 | `1`  (passive) → `SCL0`<br>`2`  (passive) → `/Sensor ports/Port 0/SCL_CABLE` | S-SERIES |
| **R32** — 100 | `1`  (passive) → `SDA1`<br>`2`  (passive) → `/Sensor ports/Port 1/SDA_CABLE` | S-SERIES |
| **R33** — 100 | `1`  (passive) → `SCL1`<br>`2`  (passive) → `/Sensor ports/Port 1/SCL_CABLE` | S-SERIES |
| **R34** — 100 | `1`  (passive) → `SDA2`<br>`2`  (passive) → `/Sensor ports/Port 2/SDA_CABLE` | S-SERIES |
| **R35** — 100 | `1`  (passive) → `SCL2`<br>`2`  (passive) → `/Sensor ports/Port 2/SCL_CABLE` | S-SERIES |
| **R36** — 100 | `1`  (passive) → `SDA3`<br>`2`  (passive) → `/Sensor ports/Port 3/SDA_CABLE` | S-SERIES |
| **R37** — 100 | `1`  (passive) → `SCL3`<br>`2`  (passive) → `/Sensor ports/Port 3/SCL_CABLE` | S-SERIES |
| **R38** — 100 | `1`  (passive) → `SDA4`<br>`2`  (passive) → `/Sensor ports/Port 4/SDA_CABLE` | S-SERIES |
| **R39** — 100 | `1`  (passive) → `SCL4`<br>`2`  (passive) → `/Sensor ports/Port 4/SCL_CABLE` | S-SERIES |
| **R40** — 100 | `1`  (passive) → `SDA5`<br>`2`  (passive) → `/Sensor ports/Port 5/SDA_CABLE` | S-SERIES |
| **R41** — 100 | `1`  (passive) → `SCL5`<br>`2`  (passive) → `/Sensor ports/Port 5/SCL_CABLE` | S-SERIES |
| **R42** — 100 | `1`  (passive) → `SDA6`<br>`2`  (passive) → `/Sensor ports/Port 6/SDA_CABLE` | S-SERIES |
| **R43** — 100 | `1`  (passive) → `SCL6`<br>`2`  (passive) → `/Sensor ports/Port 6/SCL_CABLE` | S-SERIES |
| **R44** — 100 | `1`  (passive) → `SDA7`<br>`2`  (passive) → `/Sensor ports/Port 7/SDA_CABLE` | S-SERIES |
| **R45** — 100 | `1`  (passive) → `SCL7`<br>`2`  (passive) → `/Sensor ports/Port 7/SCL_CABLE` | S-SERIES |
| **R50** — 0 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `/QWIIC_UP_3V3` | QW-POWER |
| **R51** — 10k | `1`  (passive) → `/I2C multiplexer/MUX_A0`<br>`2`  (passive) → `GND` | S-ADDRESS |
| **R52** — 10k | `1`  (passive) → `/I2C multiplexer/MUX_A1`<br>`2`  (passive) → `GND` | S-ADDRESS |
| **R53** — 10k | `1`  (passive) → `/I2C multiplexer/MUX_A2`<br>`2`  (passive) → `GND` | S-ADDRESS |
| **R55** — 0 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `Net-(R2-Pad1)` | S-PULL-LINK |
| **R56** — 0 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `Net-(R3-Pad1)` | S-PULL-LINK |
| **SW1** — CTS 219-3MSTR / C3012353 | `1`  (passive) → `+3V3_SENS`<br>`2`  (passive) → `+3V3_SENS`<br>`3`  (passive) → `+3V3_SENS`<br>`4`  (passive) → `/I2C multiplexer/MUX_A2`<br>`5`  (passive) → `/I2C multiplexer/MUX_A1`<br>`6`  (passive) → `/I2C multiplexer/MUX_A0` | S-ADDRESS |
| **TP1** — TOUCH LV GND; optional bare contact | `1` 1 (passive) → `GND` | P-TOUCH |
| **TP2** — GND / LOOP; optional bare contact | `1` 1 (passive) → `GND` | P-PROBE |
| **TP3** — +3V3_SENS / LOOP; optional bare contact | `1` 1 (passive) → `+3V3_SENS` | P-PROBE |
| **TP4** — I2C_SDA / POST; optional bare contact | `1` 1 (passive) → `I2C_SDA` | P-PROBE |
| **TP5** — I2C_SCL / POST; optional bare contact | `1` 1 (passive) → `I2C_SCL` | P-PROBE |
| **TP6** — MUX_RESET_N / POST; optional bare contact | `1` 1 (passive) → `MUX_RESET_N` | P-PROBE |
| **U1** — TCA9548APWR / 0x70..77 | `1` A0 (input) → `/I2C multiplexer/MUX_A0`<br>`2` A1 (input) → `/I2C multiplexer/MUX_A1`<br>`3` ~{RESET} (input) → `MUX_RESET_N`<br>`4` SD0 (bidirectional) → `SDA0`<br>`5` SC0 (output) → `SCL0`<br>`6` SD1 (bidirectional) → `SDA1`<br>`7` SC1 (output) → `SCL1`<br>`8` SD2 (bidirectional) → `SDA2`<br>`9` SC2 (output) → `SCL2`<br>`10` SD3 (bidirectional) → `SDA3`<br>`11` SC3 (output) → `SCL3`<br>`12` GND (power_in) → `GND`<br>`13` SD4 (bidirectional) → `SDA4`<br>`14` SC4 (output) → `SCL4`<br>`15` SD5 (bidirectional) → `SDA5`<br>`16` SC5 (output) → `SCL5`<br>`17` SD6 (bidirectional) → `SDA6`<br>`18` SC6 (output) → `SCL6`<br>`19` SD7 (bidirectional) → `SDA7`<br>`20` SC7 (output) → `SCL7`<br>`21` A2 (input) → `/I2C multiplexer/MUX_A2`<br>`22` SCL (input) → `I2C_SCL`<br>`23` SDA (bidirectional) → `I2C_SDA`<br>`24` VCC (power_in) → `+3V3_SENS` | S-MUX |

Reconciliation: **80 components / 224 distinct symbol-pin identities**.
