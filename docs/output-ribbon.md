# Internal output ribbon

Selected 2026-11-17 for the initial two-output controller. One continuous cable
has a socket at the carrier and each output board. Its conductors remain uncut
at intermediate taps, so downstream power does not traverse intermediate boards
or their mating contacts. Each output has fitted J14 and an electrically parallel
J22 footprint, **DNP by default**. Carrier J15/J18 are parallel sources; connect
a given harness to only one of them. This is an internal enclosure interface,
separate from mains/PE distribution, with no hot-plug qualification.

## Parts and numbered wiring

| Part | Selection | Evidence and purchasing snapshot |
| --- | --- | --- |
| Board header | Kinghelm **KH-2.54PH180-2X3P-L8.9**, JLC **C5157626** | Keyed/shrouded 2×3, 2.54 mm; 0.64 mm square posts, 1.02 mm PCB holes, 3 A component rating. Actual Economic/top-side matching confirmed factory THT installation; $0.1262 each, 346 catalogued. |
| Cable socket | HARTING **09185065813** | Open-ended IDC cover and strain-relief clamp; explicitly accepts 26/7–28/7 AWG, 1.27 mm ribbon. 2.5 A component rating. DigiKey $2.15 each / $1.824 at ten, 20 listed. |
| Cable | **3M 3801/06** | Six conductors, 26 AWG, 7×34 tinned copper; 1.27±0.05 mm spacing, 0.99±0.08 mm thickness, 7.62±0.254 mm width; −20…105°C. DigiKey cut lengths, $0.67/ft at one or $0.54/ft at five. |

The header's nominal 13.02×6.5 mm cavity and 4.5 mm key opening accommodate the
socket's nominal 12.20×6.1 mm body and 3.8 mm key. This is a dimensional match
between manufacturers, pending a sample mating and termination check. The
local footprint reserves body tolerance and assembly clearance; allow additional
height and access for the socket, folded cable and strain relief.

Sources: [Kinghelm drawing](https://www.kinghelm.net/upload/file/20230103/KH-2.54PH180-2X3P-L8.9.pdf),
[HARTING data](https://b2b.harting.com/files/download/PRD/PDF_DS/PDF_DS_09185065813_EN.pdf),
[HARTING family drawing, page 08-22](https://b2b.harting.com/files/livebooks/en/PRD0200000100166/downloads/livebook.pdf),
[3M cable drawing](https://multimedia.3m.com/mws/media/22031O/3m-tm-round-cond-flat-cable-050-stranded-3801-series-ts0063.pdf),
[socket purchase](https://www.digikey.com/en/products/detail/harting/09185065813/4335657),
[cut-length cable purchase](https://www.digikey.com/en/products/detail/3m/3801-06/22532405).
Prices exclude shipping, tax, tariffs, tools and assembly fees; stock can change.

| Pin / ribbon wire | Carrier J15/J18 | Output J14/J22 |
| --- | --- | --- |
| 1, red edge | +5V_SELECTED | +5V_LOGIC |
| 2 | LP_I2C_SDA | OUT_SDA |
| 3 | GND | GND |
| 4 | LP_I2C_SCL | OUT_SCL |
| 5 | Raw +5V_SYS | Raw +5V_SYS |
| 6 | LINE_SYNC | LINE_SYNC |

**Wire 1 to pin 1 at every socket**, remaining wires in order. Use the actual
pin-1 marking; mating-face views mirror board-header top views. This numbering
deliberately replaces the earlier PH6 pinout. The two 5 V rails stay separate:
selected power can commission logic over USB, while raw mains-derived power
alone supplies relay/opto actuators. Ground separates SDA/SCL. C200 already
bypasses logic power; new C205 = 100n bypasses raw power at each output tap,
also giving the neighbouring SYNC conductor a local AC return.

## Construction and placement

- Target **50 mm nominal tap spacing**. Allow cable for IDC strain-relief folds
  and service bends before committing the physical board spacing. Fifty
  millimetres between terminations need not produce fifty millimetres between
  installed boards after folding.
- A two-tap screening example has a 250 mm controller lead and 50 mm between
  outputs. Sixteen taps would span 750 mm plus the lead and fold allowance;
  the 1 m calculations below are an engineering screen, not a cable rating.
- Terminate the uncut ribbon with a suitable IDC press/parallel-jaw fixture
  loading the cover evenly. The socket clamp normally folds cable over its
  cover; check the first mid-span assembly before making the whole harness.
  Open-barrel crimp dies are not the correct termination tool.
- Check every numbered connection end-to-end, absence of shorts, socket
  retention and key orientation before powering. Keep the LV run away from
  mains terminals, triac switching paths, heatsinks and the antenna keepout.

The three cable sockets for one two-output unit cost about **$6.45**; five feet
of cable costs about **$2.70** and provides construction allowance. These are
harness parts only. The second output headers add no default purchased parts.
An intentionally populated J22 permits optional separate-cable chaining, with
its additional board/contact resistance and disconnected-chain consequences.

## Initial electrical screen

Retain the existing PESD5V0S2BT protection. Change the single carrier pull-up
pair R42/R43 from 4k7 to **2k2**, UNI-ROYAL **0805W8F2201T5E / C17520**, already
used elsewhere in the BOM. No output-board I2C pull-ups are added. Unused LP
Qwiic sockets still contribute protection capacitance; attaching accessories
adds their cable, input capacitance and any extra pull-ups.

Use the planning envelope **C = 165 + 55N + 100L pF** per I2C line, with N
output boards and L metres of ribbon. It includes three carrier and one TVS
per output at 45 pF maximum under the datasheet test condition, 5 pF typical
STM32 input plus 5 pF board allowance per output, 30 pF carrier allowance, and
100 pF/m cable allowance. The cable's published ground/signal/ground value is
53.1 pF/m. Board, connector, MCU and temperature bounds are not fully extracted
or guaranteed, so this is a design screen rather than a worst-case rating.

| Outputs / ribbon | Estimated capacitance | Rise with 4k7 | Rise with 2k2 |
| --- | ---: | ---: | ---: |
| 2 / 0.30 m | 305 pF | 1.21 µs | 0.57 µs |
| 2 / 1.00 m | 375 pF | 1.49 µs | 0.70 µs |
| 3 / 0.30 m | 360 pF | 1.43 µs | 0.67 µs |
| 3 / 1.00 m | 430 pF | 1.71 µs | 0.80 µs |
| 16 / 1.00 m | 1145 pF | 4.56 µs | 2.13 µs |

Calculation: 30–70% rise = 0.8473 RC; 1% resistor tolerance adds 1%. This initial
screen retains the ordinary Standard-mode envelope of 1 µs rise and 400 pF.
NXP §7.2.1 permits a separately calculated reduced-frequency arrangement above
the usual capacitance limit, using the limiting devices' HIGH/LOW times and
actual rise/fall times. Selecting 10 kHz alone is not that qualification.
Three/1 m is outside our conservative capacitance screen despite its rise time;
it is not declared physically impossible. Start with two outputs; longer runs
or larger populations need device-specific timing and waveform checks.
[NXP I2C specification, tables and §7.5](https://www.nxp.com/docs/en/user-guide/UM10204.pdf),
[TVS capacitance](https://assets.nexperia.com/documents/data-sheet/PESD5V0S2BT.pdf).

At 3.6 V and minimum 1% resistor value, a 2k2 pull draws at most 1.65 mA,
or 1.47 mA at a 0.4 V LOW; each resistor dissipates under 6 mW. This is below
the STM32's specified 8 mA sink test. ESP LP-I2C drive/VOL still needs checking
at temperature. Disconnected or unpowered endpoints retain the existing local
reset/actuator defaults; this is not proof against partial-contact injection.
[STM32 electrical data](https://www.st.com/resource/en/datasheet/stm32c011f6.pdf),
[ESP electrical data](https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_en.pdf).

For power, allow roughly 55 mA raw actuator plus 50 mA logic per enabled output,
including the retained 36 mA relay coil, optotriac, transistor base drive, Hall
sensor and MCU. With estimated conductor resistance 0.142 Ω/m at 60°C and
20 mΩ assumed per carrier/tap contact, the two-output example loses about
22 mV including shared ground; treating both loads at 1 m gives about 55 mV.
These use copper geometry and assumed contacts, not a measured maximum cable
resistance. The common GND carries both rail currents. Measure actual supply
dips, ground movement and temperature with the assembled harness.

The buffered LINE_SYNC HIGH load is about 65 µA for two boards, or 0.52 mA
for sixteen, through the existing 47 Ω source and 1k/100k receiver networks.
No new buffer is needed for that DC screen; actual edge/ringing and AC detector
timing remain unqualified.
[Relay](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g6dn.pdf),
[Hall sensor](https://www.ti.com/lit/ds/symlink/tmcs1123.pdf),
[SYNC buffer](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf).

**Sixteen is a soft exploration target.** Its estimated 1.68 A output demand
already exceeds the current 1 A supply before carrier/sensors, and the present
TVS capacitance exceeds the shared-bus budget. The pin-compatible low-capacitance
PESD5V0U2BT,215 / C85399 passed Economic matching and costs $0.0349 each, but
has weaker documented ESD/surge coverage. It remains a deferred alternative,
not fitted here. Revisiting protection, supply and practical count together is
more useful than declaring sixteen supported from address space alone.
[Supply](https://www.meanwell.com/Upload/PDF/IRM-05/IRM-05-SPEC.PDF),
[alternative TVS](https://assets.nexperia.com/documents/data-sheet/PESD5V0U2BT.pdf).

## Twisted and toolless alternatives

Ordinary ribbon remains the default for the short internal run. If twisting is
needed, pair each signal with ground or a properly decoupled supply return;
do not pair SDA with SCL. Twisting helps coupling/noise behaviour but does not
remove the capacitance limit. NXP §7.5 describes both ribbon and twisted wiring.

[3M 1700](https://www.3m.com/3M/en_US/p/d/b00039381/) alternates twisted sections
with flat IDC termination sections. It could preserve continuous taps, subject
to flat-section pitch, cable gauge/current and connector qualification. For
ordinary twisted cable, [Phoenix LPC lever plugs](https://www.phoenixcontact.com/en-us/products/pcb-connector-lpc-15-6-st-381-lr-1849230)
allow stripped-wire termination without crimping. Separate branch splices or
feed-through terminals would be needed for equivalent taps. Neither alternative
is selected or mechanically reserved by this PCB revision.
