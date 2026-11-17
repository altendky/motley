# Exact purchasing selections after the passive review

Reviewed 2026-11-16 for the current 120 VAC, two nominal 300 W resistive-output
prototype and indoor ventilated electronics, with about 60°C air as a design
input. These are exact sourcing decisions and integration requirements, not
a fabrication release or a new populated-board quote. No purchase was made.
The twelve previously unresolved board positions now have concrete choices.
The subsequent assembly-matching pass selects JST PH for the six-wire harness
and integrates exact terminal, holder and configuration-header footprints.
Factory installation, hand installation and remaining qualification are separate
decisions; a catalogue listing alone is not evidence of factory assembly.

## Board parts

Quantities are for one carrier and two output boards. Prices are observed
small-quantity USD parts-only snapshots; shipping, tax, tools and assembly are
additional. JLC matching probes below establish process eligibility; final
current-board quantities, omissions and prices require complete assembly jobs.

| Function / references | Selected exact part | Qty / controller | Sourcing and integration |
| --- | --- | ---: | --- |
| Carrier mains terminals: J1/J16/J19 | GOOSVN **GS007S-5.08-03P-11-00A(H)**, JLC **C5142603** | 3 | $0.1895 each; 43 catalogued. Actual Economic matching confirms factory hand soldering. Exact local footprint uses 1.60 mm holes. |
| Output mains terminals: J17/J10 | GOOSVN **GS007S-7.5-03P-11-00A(H)**, JLC **C5142605** | 4 | $0.2133 each; 110 catalogued. Actual Economic matching confirms factory hand soldering. Exact local footprint uses 1.60 mm holes. J10 is the outlet-wire handoff, not the receptacle itself. |
| F1/F2 fuse holder | Schurter **0031.8201** OGN | 3 | Refreshed Mouser $1.13 at one; 25,348 listed. Actual matching confirms JLC can install C3204125, but its two stocked pieces cannot cover a complete batch. Plan retail hand fitting; exact covered footprint is integrated. |
| Fuse-holder cover | Schurter **0853.0571**, black | 3 | Correct OGN accessory; DigiKey $1.57 / 4,017 listed. JLC C17365258 unavailable. Fitted after soldering, not a second PCB position. |
| F1 main cartridge | Littelfuse **021506.3MXP**, JLC **C142721** | 1 | T6.3 A, ceramic 5×20 mm, 250 VAC. JLC 9,351 / $0.1594; refreshed US Mouser catalogue lists $2.29. Loose cartridge, hand inserted. |
| F2 output cartridge | Littelfuse **02153.15MXP**, JLC **C142723** | 2 | T3.15 A, ceramic 5×20 mm, 250 VAC. JLC 1,938 / $0.1486; refreshed Mouser $1.95 / 990. Loose cartridge, hand inserted. |
| Six-pin LV headers: carrier J15/J18, output J14 | JST **B6B-PH-K(LF)(SN)**, JLC **C274409** | 4 | Actual Economic matching confirms factory hand soldering; 6,924 listed, $0.1105 each. Keyed 2.00 mm PH replaces the proposed retail Molex KK; same part family already used on carrier J21. |
| Six-way cable housings | JST **PHR-6** | 4 | One per harness end; hand assemble or source complete correctly wired PH harnesses. |
| Loose cable contacts | JST **SPH-002T-P0.5S** | 24 | Standard-force contact, 24–30 AWG, insulation diameter 0.8–1.5 mm. Prefer 24 AWG power conductors for the series' 2 A rating. Harness fabrication remains separate from PCB assembly. |
| J20 snubber header | Samtec **HMTSW-102-07-L-D-200** | 2 | Short-post, high-temperature 2×2 header. DigiKey $0.51 at one, 151 listed plus factory stock; no exact JLC assembly established. LOW-only provisional assembly as discussed below. |
| SW20 recovery header | Samtec **HMTSW-102-07-G-S-200** | 2 | Short-post 1×2, about $0.291 direct; manufacturer listed 432. Exact JLC stock/assembly not established. RUN stays open, RECOVERY uses a cap. |
| Covered configuration caps | Harwin **M7685-05** | 4 normally fitted at J20, plus 2 recovery accessories | DigiKey $0.49 at one, $0.417 at ten; 10,476 listed. Retains the previously accepted closed-top arrangement. |
| Carrier R25 | YAGEO **AC0603FR-07226KL**, JLC **C227714** | 1 | Same 226k/1%/0.1 W/0603, AEC-Q200 family. Confirmed Economic match including twenty purchased parts for two placements. $0.0039 each; 272 listed. Replaces the RC part whose fourteen stocked pieces cannot meet attrition. |
| Output K1 | **G6DN-1A-L DC5**, retained Omron part, now also sold as Aratas | 2 | Exact existing relay, not a substitution. JLC C6624853 lacks stock; DigiKey lists 18,810 / $2.76 at one. Existing local pad geometry matches the manufacturer drawing; native identity/footprint fields are now filled. |

The base fuse/holder ordering model is **one holder + one cartridge + one cover**
per F1/F2. Do not assign a single loose fuse or clip MPN to a combined footprint
and let an exporter silently price one piece. The current quote deliberately
leaves holders manual because of insufficient shared stock; cartridges and
covers are inserted separately in every case. The catalogue's thirteen-piece
purchase minimum did not apply to the two-piece factory-matching probe.

### Retail hand-fitting basket

For one finished controller, the base board parts, configuration accessories
and two output harnesses total **$25.67** at the refreshed single-unit tiers.
This excludes wire, tools, shipping/tax/tariffs, off-board outlets/heatsinks/USB
hardware and any additional stock omissions in the final assembly quote.

| Parts | Purchase quantities | Extended USD |
| --- | --- | ---: |
| OGN holders / black covers | 3 / 3 | $3.39 / $4.71 |
| Main / branch fuse cartridges | 1 / 2 | $2.29 / $3.90 |
| Retained Omron relays | 2 | $5.52 |
| Samtec J20 / recovery headers | 2 / 2 | $1.02 / $0.582 |
| Harwin caps, including recovery accessories | 6 | $2.94 |
| PHR-6 housings / standard contacts | 4 / 25 | $0.44 / $0.875 |

All selected retail paths allow single-piece purchasing. Buy **25 contacts**:
Mouser's $0.035 tier costs about $0.88, less than buying 24 at its $0.042 tier
(about $1.01). DigiKey's indexed contact offer starts at 100 pieces. Stock
omissions and price breaks for larger batches must be reconciled separately.
The main fuse's $2.29 price is from a current US catalogue row; its exact product
page timed out. Other refreshed basket entries were checked on product pages.

## Mains terminal fit and access

Both GOOSVN variants have manufacturer-documented 300 V / 16 A UL ratings;
that is not a system current/temperature rating. Their 1.0×0.8 mm leads are
3.50±0.30 mm long; the drawings recommend **1.60 mm PCB holes**, versus the
existing MetzConnect stand-in's 1.30 mm. Specified strip length is 6–7 mm and
screw torque 0.5 N·m. The listed conductor range includes the contemplated
internal mains wiring; ferrule suitability and actual wire selection remain
installation details. Manufacturer current derating at the actual board
temperature still needs review/measurement.

The 7.50 mm part is 22.5×10.2×14.1 mm. Both output blocks are placed at the
bottom edge; reserve room for wires and a screwdriver in the enclosure.
The 5.08 mm part is 15.24×10.2×14.1 mm, with a roughly 0.6 mm side feature.
It is selected for the carrier because three large side-entry blocks stacked
eleven millimetres apart block one another's wire access.

The integrated placement retains the 95×80 mm carrier: rotate the three smaller
blocks so wire entries face the
right edge, with pin-1 anchors at (129,81.2), (129,98.1), (129,115.0) mm. Put
the OGN covered envelope in the inner mains lane and rearrange the three line
detector resistors behind/above it. Exact pad tables and the envelope audit are
retained with the research evidence. Check mounting, conductor bends, all-layer
isolation, functional creepage and copper spacing during integration: a rated
terminal does not qualify the exposed PCB gaps. Do not force a 7.62 mm part into
the old 7.50 mm pattern. TE 282854-3 was rejected for this packing after its
actual drawing showed a deeper footprint and side screw access.

## Fuse holder and cartridge fit

The existing footprint labelled Littelfuse 111 Inline is not a verified fit to
the current **01110501Z** clip: its four collinear holes differ from that clip's
rectangular 18.796×5.0 mm pattern and recommended 1.17 mm holes. A correct pair
would be a viable smaller fallback, but requires two real clip instances and a
separate cartridge in the purchasing model.

The preferred OGN is one orderable holder. Its drawing requires **22.5 mm pin
spacing and 1.30 +0.10/−0 mm holes**. Body dimensions are 25×9.6 mm; cover
installation width is 10.8 mm and covered height 12.7 mm. It does not fit the
old fuse midpoint unchanged: carrier F1 crosses the edge/adjacent terminals,
and output F2 approaches the capacitor and terminal courtyards. The new native
placement moves the holders, terminal blocks and adjacent passives; the output
outline increases by 2 mm to 90×87 mm. The stock optional center fixing
feature should be considered when choosing board support.

The 215 cartridges retain the existing time-lag/current intent and provide
1,500 A breaking capacity at their specified 250 V conditions. Their ratings
are prototype candidates, not validated protection coordination. Temperature,
power-supply/cold-lamp inrush, prospective fault current, total-clearing energy,
wiring/traces, relay contacts and the current-sensor leadframe must be reviewed.
In particular, the branch fuse's nominal melting I²t of 43.255 A²s already
exceeds the BTA08's 36 A²s / 10 ms figure under different test conditions: it
cannot be credited with preserving the triac during a hard short. The design's
shorted-triac response remains necessary. Do not claim the 250 V cartridges
cover the proposed 264 VAC HIGH range; that is a separate selection/review.

## LV harness and configuration details

The carrier also has a normally-DNP **J27 1×6, 2.54 mm alternative USB header**
and independent normally-DNP R28/R29 5k1/1% CC pull-downs. Its pin order is
VBUS, GND, D+, D-, CC1, CC2. Copper JP30/31/32 select PH by default; cut those
1-2 bridges and join 2-3 on all three for ALT. Fit the CC resistors only when
the alternate USB-C assembly lacks Rd; the primary Adafruit cable retains its
own resistors. This adds no default purchased parts. See the
[carrier interface notes](../hardware/controller/README.md) before populating.
J27 is a bare pin-strip footprint, not a reserved larger locking-header body.

The JST PH harness preserves the six signals in order: GND, selected logic 5 V,
SDA, SCL, LINE_SYNC, raw actuator 5 V. Preserve pin numbers and verify end-to-end
continuity rather than inferring a cable's pin order from photographs. The
existing KiCad PH footprint's 0.75 mm holes fit JST's 0.70 +0.10/−0 mm drawing.
Its pins run along local +X; −90° PCB rotation keeps the prior +Y pin order.
Body dimensions are 13.9×4.5×6 mm, with 8 mm mated height. The series rating is
2 A with 24 AWG, 100 V AC/DC, and −40 to 105°C including temperature rise;
the current system's 5 V supply is 1 A. Exact wire, crimp tooling, pull testing
and harness strain relief remain assembly qualifications.

The panel-USB carrier header J21 also uses six-way PH, with a different pinout
(including VBUS/GND in the opposite first-two-pin order). These harnesses are
**not electrically interchangeable**. Identify them by function and verify
polarity/continuity before power; mechanical differentiation remains an open
enclosure/harness design concern for the exploratory build.

Molex 0022232061 + 0022013067 + 0008500032 remains a documented retail fallback.
It was superseded because PH has confirmed factory installation and a smaller
body, not because the Molex parts are unavailable. It is not a mating substitute.

Harwin M20-9990645 + M20-1060600 + M20-1180042 is a documented narrow-body backup
that fits the present nominal pin-strip geometry. It is unpolarized/unlatched,
so it is not preferred for deployed wiring. Previously quoted generic 4/5-pin
Kinghelm headers also call for 1.02 mm holes; correct their footprints during
the same manufacturing cleanup rather than silently claiming exact matches.

The selected Samtec HMTSW headers have **5.08 mm mating posts**, 3.30 mm tails
and 1.02 mm recommended holes, now represented by exact local footprints.
Even the post's upper tolerance stays below the
Harwin cap's **5.6 mm maximum**; the previously discussed 6.0/6.1 mm posts do not.
Their pad-center grids can stay unchanged. Use the lead-free-capable HMTSW
family rather than substituting the ordinary MTSW processing specification.

J20's two caps go across 1–2 and 3–4 for ON, or 1–3 and 2–4 for OFF, retaining
coverage of all pins in either state. The cap has a **250 V DC / AC-peak**
working rating: 132 Vrms gives about 187 V peak, whereas 264 Vrms gives about
373 V peak. This makes the current arrangement a **LOW-only provisional choice**.
The roughly 0.60 A normal LOW peak and 1.19 A HIGH peak through the 330-ohm
network are below its headline 3 A rating, but do not establish pulse life,
hot-ambient or surge performance. A working-voltage specification for the bare
header and whole-assembly insulation qualification are still required. A closed
cap is not a touch-safety approval. Configure only unplugged and discharged.

## Other retained parts and unresolved physical checks

Keep the previously accepted Qualtek 738W-X2/03 outlets, Adafruit 6153 panel
USB cable and existing heatsink/clip candidates. This pass does not replace
the two open power-entry alternatives or claim the enclosure has been designed.
The outlet tabs deserve a specific fit check: Qualtek documents 4.8 mm width
and 0.6 mm thickness, while common 187-series females are specified for 0.51 or
0.81 mm test tabs. No exact insulated female is declared a verified match merely
from its width. TE 2-520193-2 / 2-520194-2 and the variable-thickness 2293255-1
do not, on the reviewed evidence, establish this intermediate tab's qualification.
Retain insulated crimp connections as the plan; resolve by a manufacturer
compatibility statement or a controlled sample fit/retention test before ordering
a complete harness. The cord/bushing fit likewise depends on actual jacket and
panel dimensions. These are bounded physical-fit questions, not unavailable
component technologies.

## Evidence and qualification

Native changes now include the confirmed R25 replacement, retained K1 identity,
exact terminal/holder/configuration footprints, PH deployment connectors and
associated placement/routing. J20 retains its LOW-only selection constraint.
The [November 16 quote](jlcpcb-quote-2026-11-16.md) remains a dated result for its
recorded passive-revision inputs. The
[new exact-part quote](jlcpcb-quote-2026-11-16-exact-parts.md) prices these
integrated connector/holder choices and reports the actual factory omissions.

Primary drawings/specifications and retail acquisition references:

- [GOOSVN 7.50 mm catalogue](https://jlcpcb.com/partdetail/C5142605),
  [5.08 mm catalogue](https://jlcpcb.com/partdetail/C5142603),
  [manufacturer 7.50 mm drawing](https://www.goosvn.com/uploads/ueditor/file/20180929/6367382481749100251922503.pdf),
  [manufacturer 5.08 mm drawing, page 2](https://www.goosvn.com/uploads/ueditor/file/20180820/6367035820032422801238022.pdf).
- [Schurter OGN drawing/specification](https://www.schurter.com/en/datasheet/typ_OGN.pdf),
  [OGN accessory table](https://www.schurter.com/en/datasheet/Accessories_for_OGN),
  [Mouser holder](https://www.mouser.com/en/ProductDetail/Schurter/0031.8201?qs=A0AD9A9uYPZ%2F5Y96FqMyAQ%3D%3D),
  [DigiKey black cover](https://www.digikey.com/en/products/detail/schurter-inc/0853-0571/669931).
- [Littelfuse 215](https://www.littelfuse.com/assetdocs/littelfuse_fuse_215_datasheet?assetguid=990f7193-d9a2-48e4-b760-2b43514249cf),
  [111 clip drawing](https://www.littelfuse.com/assetdocs/littelfuse-fuse-clip-111-datasheet?assetguid=b1ca8750-5406-48d2-b921-b86728e90adf).
- [Molex header](https://www.molex.com/en-us/products/part-detail/0022232061),
  [housing](https://www.molex.com/en-us/products/part-detail/0022013067),
  [loose contact](https://www.molex.com/en-us/products/part-detail/0008500032),
  [Molex-authored header drawing](https://www.jameco.com/Jameco/Products/ProdDS/232266.pdf).
- [JST PH manufacturer drawing and specifications](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf).
  [DigiKey PHR-6](https://www.digikey.com/en/products/detail/jst-sales-america-inc/PHR-6/608604),
  [Mouser contacts](https://www.mouser.com/en/ProductDetail/JST-Commercial/SPH-002T-P0.5S?qs=QpmGXVUTftFJKuym4Sxf3w%3D%3D).
- [Samtec HMTSW drawing](https://suddendocs.samtec.com/prints/hmtsw-xxx-xx-xxx-x-xxxx-xx-xx-mkt.pdf),
  [recommended footprint](https://suddendocs.samtec.com/prints/tsw-xxx-xx-x-x-xx-xxx-footprint.pdf),
  [Harwin M7685-05](https://www.harwin.com/products/M7685-05).
- [YAGEO resistor specification](https://yageogroup.com/content/datasheet/asset/file/PYU-RC_GROUP_51_ROHS_L),
  [selected YAGEO AC resistor specification](https://yageogroup.com/content/datasheet/asset/file/PYU-AC_51_ROHS_L),
  [DigiKey R25](https://www.digikey.com/en/products/detail/yageo/RC0603FR-07226KL/727066),
  [Omron relay specification](https://components.omron.com/us-en/system/files/2024-01/datasheet_pdf/K276-E1.pdf),
  [DigiKey relay](https://www.digikey.com/en/products/detail/omron-electronics-inc-emc-div/G6DN-1A-L-DC5/6819352).
- [Qualtek outlet drawing](https://www.qualtekusa.com/images/AC_Receptacles/pdfs/738wx203.pdf),
  [TE 187 application specification](https://docs.rs-online.com/7e0c/0900766b815c13cf.pdf),
  [Adafruit 6153](https://www.adafruit.com/product/6153).

Full read-only fit reports, drawings, current catalogue responses and the native
before/after metadata audit are temporary evidence under
`/tmp/agents/PUOfdDTNUf/exact-selections/`. Integration audits and matching probes
are under that session's `assembly-integration/` and `assembly-matching/` paths.
Individual uncertainty and rejected
alternatives remain there; none is silently promoted to a qualified selection.
