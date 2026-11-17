# AC passive-component review

Engineering review, 2026-11-16, against native CAD at
`e60c3ee1a5526c87c87e9289372fc5ef30b4a6a3`. Recommendations below are for the
next circuit revision. The subsequently authorized schematic/PCB update now
implements the candidate populations described below. A subsequent
[actual assembly quote](../../docs/jlcpcb-quote-2026-11-16.md) includes all new LOW
passives in Economic assembly. No bench measurements were performed.

The native default is LOW: two fitted 1.2 kΩ gate resistors, two DNP expansion
resistors with fitted SMT zero-ohm bypasses; the HIGH population fits all four
1.2 kΩ resistors and omits both bypasses. LOW voltage sensing uses four 8.2 kΩ
parts as 8.2k + 8.2k + (8.2k parallel 8.2k), plus a zero-ohm series link and
2.7 kΩ shunt. HIGH uses four series 8.2 kΩ parts, omits the parallel part and
fits a 1.5 kΩ shunt. The common PCB needs no rewiring. The carrier uses three
stocked 18 kΩ parts, 54 kΩ total. The output placement is 90 × 85 mm; front
assembly, four layers, the isolation boundary and bottom-right AC connectors
are preserved. Final native verification is recorded in `verification.md`.

## Scope and design inputs

The user confirmed an indoor, ventilated controller, outside the humid animal
enclosure, with approximately 60 °C maximum air around the boards as a design
target. Air temperature is not component or junction temperature.

Review both leading-edge phase-angle and whole-cycle operation (`MOT-AC-001/002`),
unloaded shorted-triac detection (`MOT-AC-003`), isolation (`MOT-AC-008`) and the
initial 300 W / 120 V resistive-load target (`MOT-AC-014`). Screen the preferred
regional ranges 90–132 and 180–264 VAC, 50/60 Hz (`MOT-AC-013`), without treating
that preference as an existing whole-device rating. General inductive-load and
higher-current qualification remain outside this review.

## Recommended direction

| Block | Recommendation | Reason |
|---|---|---|
| Snubber capacitor | TDK B32651A7472K000, 4.7 nF ±10%; provide a second parallel position | An actual high-pulse/snubber part: 450 VAC, 1250 VDC, 4000 V/µs. |
| Initial snubber network | Two capacitors (9.4 nF) with 330 Ω pulse-rated resistor | Ordinary discharge stress clears the published component screen; greater transient shunting than the smaller option. |
| Smaller snubber candidate | One capacitor with approximately 660–680 Ω | Halves capacitance/leakage/energy; retain as an alternative for switching/EMC evaluation, not an assumed equivalent network. |
| Gate series resistance | Evaluate approximately 2.4 kΩ LOW / 4.8 kΩ HIGH, using pulse-rated series parts | Bounds optotriac fault current and power more effectively than the existing 430 Ω placeholder; regional values reduce the firing-delay penalty. |
| Gate–A1 shunt | Retain 330 Ω electrically, but replace or pulse-qualify the ordinary 0805 placeholder | A failed main-triac gate can expose this resistor to substantial fault energy. |
| Output detector banks | Add deliberate leakage-bypass shunts and revise series resistance | Check the lower hysteretic release threshold as well as initial activation. |
| Carrier timing bank | Prefer about 60 kΩ electrically; 54 kΩ is a stocked-part alternative | More useful low-line margin than 72 kΩ, with modest extra dissipation. Preserve multiple series parts for voltage sharing. |

These are engineering recommendations, not qualified substitution instructions.
Circuit geometry, protection, temperature and actual waveforms remain part of
the selection. In particular, there is no reason to preserve exactly 100 Ω,
10 nF, 430 Ω or four identical 17 kΩ parts.

## Snubber: resolved component-rating checks

Reject Vishay BFC233820103/MKP3382X2 as the default phase-angle capacitor:
its datasheet page 11 explicitly excludes continuous pulse applications.
The inexpensive STE X2 candidate has no established repetitive-pulse envelope
in the available documentation. An X2 marking alone does not select a snubber.

The TDK candidate is explicitly intended for snubbing. It is not X2 and must
not be substituted into a general across-line EMI-filter position. Its body is
13 × 5 × 11 mm, with 10 mm lead spacing; the placeholder needs a body/courtyard
update. Its AC rating, pulse slope and pulse characteristic are ample for the
normal-operation screen below. Temperature ratings/derating still apply.

Use Vishay PR02000203300JA100 (PR02, 330 Ω ±5%, 2 W) as a sourced starting
resistor. At 264 VAC, including resistor/capacitor tolerance, 9.4 nF / 330 Ω
has at most approximately 445 W initial power, 0.721 mJ discharge energy and
86.5 mW average discharge heating at 120 pulses/s. The equivalent rectangular
pulse duration is at least 1.326 µs. Vishay's published equal-peak/equal-energy
conversion is RC/2; the PR02 repetitive-pulse graph covers this region with
substantial margin. Capacitor slope is approximately 141 V/µs versus its
4000 V/µs rating. These are sinusoidal line-peak discharge calculations, not
unspecified mains-surge bounds.

One 4.7 nF capacitor with 680 Ω has corresponding bounds of approximately
216 W, 0.360 mJ, 43.2 mW and 1.366 µs. Two stocked 330 Ω resistors give a
nearby 660 Ω implementation. Equal RC constants do not establish equal EFT
immunity: the high-frequency branch impedances differ.

The main triac can handle ideal resistive commutation without a snubber in
principle. Final capacitance/resistance should be selected from actual load,
wiring, false-triggering, overshoot and EFT measurements, rather than adding
unnecessary capacitance by default. Keep the manual snubber configuration.

## Gate network: include failure behavior

If the main triac fails to turn on, the phototriac can remain latched through
the gate/shunt/load path until current zero. Ending its LED pulse does not
necessarily terminate that secondary current. The original 430 Ω path can
exceed the VO3053's 100 mA RMS rating in this failure; even 660 Ω does not
provide a satisfactory continuous-current bound at high line.

Both RMS current and output power must be checked. VO3053 lists 100 mA RMS and
200 mW at 25 °C; checking one does not establish the other. Its 3 V maximum
on-state drop is specified at 100 mA peak and 25 °C. With ±5% gate resistance,
2.4 kΩ at 132 VAC or 4.8 kΩ at 264 VAC limits the conservative gate-short
screen to 81.9 mA peak / 57.9 mA RMS, with approximately 156 mW output power
assuming that 3 V drop. This avoids using its surge-current rating to justify
an entire half-cycle of fault current.

Those results are a useful 25 °C screen, not a full-temperature guarantee.
The datasheet's steady thermal network permits an estimate once the actual
board temperature/copper path is known; it does not publish transient thermal
data qualifying an arbitrary 50 ms fault. Establish the allowed board/junction
temperatures and verify the warm fault waveform. Do not invent a temperature
derating curve or use typical cold trigger-current curves as guaranteed limits.

A conditional adjacent-board target of at most 85 °C gives useful modeled
margin: routing all 183 mW estimated package heat through each junction-to-board
thermal resistance in turn gives approximately 99 °C output junction and
113 °C LED junction, below their 125 °C maxima. Include neighboring resistor
and heatsink heating when establishing that board temperature. This is a
layout/test condition, not an observed temperature or a guaranteed warm VTM.

A stocked concrete implementation uses two/four PR02 1.2 kΩ resistors for
LOW/HIGH. It is larger than the current SMD placeholder. A pulse-rated 330 Ω
shunt is also a candidate; normal gate clamping makes its usual heating tiny,
but a failed/open gate changes the energy. The relay must interrupt failed
delivery, and repeated firing into a failed-to-latch condition must be bounded
by local fault handling (`MOT-AC-004/005`). A 50 ms total interruption interval
is a design/test target to evaluate, not an observed relay deadline.

Larger gate resistance delays initial conduction. At 25 °C datasheet gate
limits and a 30 W fixed resistive load rated for the region's nominal 120/240 V,
2.4 kΩ at 90 V and 4.8 kΩ at 180 V retain roughly 99% of the otherwise
available sine-wave power. Timing,
cold operation, low-load latching and maximum delivered power must be included
in the declared mode envelope. The existing values were not uniquely correct.

## Detector banks: design for release, heat and observation windows

ACPL-K370 full-temperature activation is 1.96–3.11 mA; release is
1.00–1.62 mA. Existing LOW 32.8 kΩ/no shunt and HIGH 48 kΩ/3.9 kΩ shunt do
not guarantee a uniformly released indication after prior conduction under
the conservative leakage bound. This is not proof they always malfunction:
phase-aware observation could work, but a turn-on-current comparison alone
does not establish that behavior.

For the two-capacitor 9.4 nF option, use the following electrical starting
points. Calculations use full-temperature Broadcom thresholds, ±3% passive
allowance (initial tolerance, TCR and finite life-drift allowance), maximum
capacitance and 1 mA maximum hot main-triac leakage. Additional driver leakage
and stray capacitance must fit the remaining current margin.

| Variant | Series bank / input shunt | Release margin over assumed leakage | Minimum full-sine pulse at minimum line, 60 Hz | Upper bank heat at maximum line |
|---|---|---:|---:|---:|
| LOW 90–132 V | Approximately 20.4 kΩ / 2.7 kΩ | 17.6% | 3.70 ms | 0.881 W |
| HIGH 180–264 V | 32.8 kΩ / 1.5 kΩ | 16.4% | 3.29 ms | 2.191 W |

Four 5.1 kΩ parts would provide the LOW bank; that exact pulse-family sourcing
remains open. A practical currently stocked alternative is
8.2 kΩ + 8.2 kΩ + (8.2 kΩ parallel 8.2 kΩ) = 20.5 kΩ, using four of the same
TE CRGP2512F8K2 parts as the HIGH bank. It gives approximately 3.66 ms minimum
full-sine pulse and 0.876 W upper bank heat, with the same 17.6% release margin.
The largest healthy resistor share is about 415 V for the assumed 1 kV
network transient, below its 500 V working ceiling; its normal heat is below
0.36 W. This uses a parallel pair for a concrete stock/common-part advantage,
not because equal-valued resistors are required. The four-series 5.1 kΩ option
shares transient voltage more evenly if suitable parts become available.

If switching qualification supports one 4.7 nF capacitor, LOW 24.6 kΩ / 5.1 kΩ
and HIGH 41 kΩ / 3.0 kΩ give approximately 13.4% / 11.6% release margin and
0.730 / 1.752 W bank heat. These use three/five stocked 8.2 kΩ series parts.
Thus reducing capacitance can save detector heat as well as leakage, but
capacitance must first satisfy the switching-stage needs.

For the carrier K376, four 15 kΩ parts (60 kΩ) provide a guarded minimum
sinusoidal activation voltage of about 72 V RMS and upper bank heat of
1.20 W at 264 V. Three stocked 18 kΩ parts (54 kΩ) improve that to about
65 V RMS at 1.33 W. Four 18 kΩ parts give about 86 V RMS under the same
allowances, leaving much less headroom below 90 V. Resistor count also changes
surge voltage sharing; select it together with the protected-input envelope.

Late phase-angle pulses can be below a voltage-presence detector's amplitude
threshold. Firmware must report an insufficient observation window as
unavailable rather than healthy. These threshold detectors cannot establish
the exact firing instant at every dimming level.

## Sourcing and remaining qualification

Public JLC catalogue checks on 2026-11-16, USD parts only:

| Part | JLC code | Stock | 1+ price |
|---|---|---:|---:|
| TDK 4.7 nF B32651A7472K000 | C3781178 | 2584 | $0.1133 |
| Vishay 330 Ω PR02000203300JA100 | C1365089 | 200 | $0.3128 |
| Vishay 1.2 kΩ PR02000201201JA100, gate-bank building block | C1366069 | 100 | $0.1724 |
| TE 8.2 kΩ CRGP2512F8K2 | C3992729 | 150 | $0.5924 ($0.4795 at 10+) |
| TE 18 kΩ CRGP2512F18K | C2082909 | 22 | $0.2521 |

Two TDK capacitors plus the 330 Ω PR02 cost about $0.54 per output before
assembly. The proposed gate bank plus pulse-rated 330 Ω shunt adds approximately
$0.66 LOW / $1.00 HIGH. This parts-only screen excludes through-hole assembly
charges. The subsequent actual quote above confirms the LOW parts' selected
assembly charges; physical footprint/placement qualification remains separate.

The TE CRGP pulse family is preferable to unqualified ordinary 200 V chips.
An explicit protected-network screen of at most 1 kV absolute / 100 µs rare
impulses gives useful voltage/power margin in the proposed series networks;
no selected protector currently establishes that envelope. Do not represent
it as an existing product surge rating. The whole-stage protection must also
coordinate with the current 600 V triac/driver; an RC snubber is not a clamp.

Bench qualification still needs normal/fault pulse waveforms, low-load firing,
relay interruption time, temperatures, false-trigger immunity and EMI. Include
capacitor-short and detector-component faults: the main fuse will not reliably
clear milliamp detector faults or every sub-ampere snubber fault. PR02's
documented flameproof/interruption behavior is relevant but is not a certified
fuse or proof of benign whole-board failure.

## Primary references

- [ST AN437, snubber functions and application measurements](https://www.st.com/resource/en/application_note/an437-rc-snubber-circuit-design-for-triacs-stmicroelectronics.pdf)
- [ST AN5114, phototriac gate-network tradeoffs](https://www.st.com/resource/en/application_note/an5114-controlling-a-triac-with-a-phototriac-stmicroelectronics.pdf)
- [ST BTA08, gate/latch/leakage limits](https://www.st.com/resource/en/datasheet/bta08.pdf)
- [Vishay VO3052/3053, simultaneous current/power/thermal limits](https://www.vishay.com/docs/83749/vo3052.pdf)
- [Vishay MKP3382X2, page 11 continuous-pulse exclusion](https://www.vishay.com/docs/28119/mkp3382x2.pdf)
- [TDK B32651A7472K000 product and ratings](https://product.tdk.com/en/search/capacitor/film/snubbering_pfc/info?part_no=B32651A7472K000)
- [Vishay PR01/02/03 pulse and interruption curves](https://www.vishay.com/docs/28729/pr010203.pdf)
- [Vishay pulse-shape conversion](https://www.vishay.com/docs/20103/geninfo.pdf)
- [Broadcom ACPL-K370/K376 thresholds](https://docs.broadcom.com/doc/AV02-2153EN)
- [TE-authored CRGP datasheet mirror](https://www.ic-components.se/files/c7/CRGP0402F12R.pdf)
