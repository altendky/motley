# Third-party notices

The [repository license scope](LICENSE.md) grants rights in original Motley
material. The exceptions below retain upstream rights and terms. Copies in
Git history retain their original third-party terms too.

## KiCad and Espressif library material

The reusable upstream-derived parts listed below are licensed under
[CC-BY-SA-4.0](LICENSES/CC-BY-SA-4.0.txt) with the
[KiCad library exception](LICENSES/KiCad-library-exception.txt). Preserve the
upstream attribution, exception and modification notices when redistributing
those library parts. These notices also apply to later adaptations of them.

The exception permits electronic designs using these parts, and their generated
outputs, to use a different license. It does not relicense a redistributed
reusable library part. See [KiCad's explanation](https://www.kicad.org/libraries/license/).
Library references to an installed KiCad distribution are not separate vendored
copies; embedded symbol/footprint data used in a board design benefits from
the design exception.

### Espressif

Source: [Espressif KiCad libraries, tag 3.0.1](https://github.com/espressif/kicad-libraries/tree/3.0.1),
copyright its upstream contributors. The
[upstream license/warranty notice](LICENSES/Espressif-library-notice.md) is
preserved verbatim from the repository's earlier local notice. Espressif uses
the same library exception as KiCad.

| Local reusable part | Upstream part and local modifications |
| --- | --- |
| `hardware/controller/Motley.kicad_sym`, symbol `ESP32-C6-WROOM-1` | Espressif `ESP32-C6-WROOM-1`; project-local footprint/library reference and project metadata |
| `hardware/controller/Motley.pretty/ESP32-C6-WROOM-1.kicad_mod` | Espressif `ESP32-C6-WROOM-1`; local library identity and omitted unavailable external 3D model |

These adaptations entered the project in the 2026-11-13 CAD study, with later
KiCad 10 serialization. Refer to the part descriptions and hardware verification
record for electrical interpretation; licensing provenance does not establish
part qualification.

### KiCad symbols

Source: the KiCad library contributors. The local triac/optotriac graphics are
adapted from standard KiCad library graphics; selected-part names, descriptions,
pin information, footprint assignments and project metadata were added or
adjusted for Motley.

| Local entry in `hardware/controller/Motley.kicad_sym` | Upstream graphics and modifications |
| --- | --- |
| `BTA08_600SWRG` | `Triac_Thyristor:Generic_Triac_A1A2G`; retained coordinate paths with adjusted stroke widths and selected-part properties |
| `MOC3063S_TA1` | `Relay_SolidState:MOC3063M`, whose graphics inherit from `MOC3031M`; retained optotriac/zero-cross graphics with selected-part properties |
| `VO3053_X007T` | Adapted optotriac graphics from the same KiCad family; removed zero-cross graphics and selected the VO3053 properties/pin/footprint mapping |

The triac and MOC adaptations were present in the initial CAD study committed
on 2026-11-13; the VO3053 adaptation was introduced with the intelligent-output
study committed on 2026-11-14. Geometry was compared against KiCad symbols tag **9.0.0**:
[triacs](https://gitlab.com/kicad/libraries/kicad-symbols/-/blob/9.0.0/Triac_Thyristor.kicad_sym)
and [solid-state relays](https://gitlab.com/kicad/libraries/kicad-symbols/-/blob/9.0.0/Relay_SolidState.kicad_sym).
That tag is a verified comparison reference, not a claim about the exact
historical download revision. Later KiCad 10 serialization preserves this
provenance.

### KiCad footprints

Source: the KiCad library contributors. These adaptations were present in the
initial CAD study committed on 2026-11-13 and later serialized with KiCad 10.

| Local file under `hardware/controller/Motley.pretty/` | Upstream source and modifications |
| --- | --- |
| `WirePost_1mm.kicad_mod` | [`TestPoint:TestPoint_THTPad_D2.0mm_Drill1.0mm`](https://gitlab.com/kicad/libraries/kicad-footprints/-/blob/master/TestPoint.pretty/TestPoint_THTPad_D2.0mm_Drill1.0mm.kicad_mod); renamed reusable part and project metadata |
| `WireLoop_P2.54.kicad_mod` | [`TestPoint:TestPoint_2Pads_Pitch2.54mm_Drill0.8mm`](https://gitlab.com/kicad/libraries/kicad-footprints/-/blob/master/TestPoint.pretty/TestPoint_2Pads_Pitch2.54mm_Drill0.8mm.kicad_mod); renamed/described for the loop, both pads assigned number 1, and project metadata |

The comparison used the libraries shipped with the pinned **KiCad 10.0.8**
AppImage; the original acquisition revision is not recorded. Matching UUIDs
and graphics establish these copies independently of the functional dimensions.

## Original reusable hardware parts

The following independently authored local entries use **CERN-OHL-P-2.0** under
[LICENSE.md](LICENSE.md). Sharing a file with an upstream-derived entry does
not apply the upstream license to these independent entries.

| Local symbol library | Original entries |
| --- | --- |
| `hardware/controller/Motley.kicad_sym` | `Feather_ESP32_C6_5933`, `G6DN_1A_L_DC5`, `PESD5V0S2BT` |
| `hardware/controller/MotleyPower.kicad_sym` | `AP2112K-3.3`, `C`, `PWR_FLAG`, `R`, `TLV3011BIDBVR`, `TPS2116DRL`, `TS3USB221ERSER`, `USBLC6-2SC6`, `USB_PANEL_PH6` |
| `hardware/controller/OutputStudy.kicad_sym` | `ACPL_K370`, `ACPL_K376`, `TMCS1123_B5` |

Original footprints under `hardware/controller/Motley.pretty/`:

- `Mechanical_Pin_PTH_Study.kicad_mod`
- `Relay_G6DN_1A_L_DC5_Study.kicad_mod`
- `TouchGround_8mm.kicad_mod`
- `TMCS1123_DVG10_Study.kicad_mod`
- `VO3053_Option7_Study.kicad_mod`
- `ACPL_K37x_SSO8_Study.kicad_mod`

The repository history and source descriptions record custom construction and
manufacturer pin maps/package dimensions for these parts. Conventional
electrical graphics or factual dimensions alone are not a claim to upstream
library authorship. In particular, the ACPL footprint records a 0.64 mm pad
width from stock SSO geometry, with independent package layout/graphics.
Datasheets and manufacturer drawings remain their owners' material; this grant
covers the original local part definitions, not those external documents.

## Historical research excerpts

`PLANNING_SESSION.md` is historical research. Its earlier versions embedded
third-party examples; the current document uses factual prose and links instead.
The default Motley licenses do not relicense those historical excerpts or imply
that the referenced projects license all of their files identically.

- **Espressif ESP-Matter:** the window-covering configuration and related
  SDK examples were attributed to [ESP-Matter](https://github.com/espressif/esp-matter),
  which is licensed under [Apache-2.0](LICENSES/Apache-2.0.txt). Preserve
  Espressif/upstream attribution for those excerpts; other SDK components can
  have different licenses.
- **lemauee's roof-window controller:** the researched patterns refer to its
  [application source](https://github.com/lemauee/esp32c6-matter-over-thread-roof-window-controller/blob/e345786843be47f2a716b6e09f7c33890e6b0818/main/app_main.cpp),
  which declares public-domain or CC0 availability. This observation applies to
  that file's notice, not an inferred repository-wide license.
- **thorio's ESPHome projects:** the GPIO pulse YAML and shortened time-based
  cover example were attributed to the
  [Velux firmware](https://github.com/thorio/esphome-projects/blob/fdbcb51f53e94a207e05f66754bc7eeafa1315bb/velux-controller/firmware.yml)
  in the [GPL-3.0 project](https://github.com/thorio/esphome-projects/blob/fdbcb51f53e94a207e05f66754bc7eeafa1315bb/LICENSE).
  The [GPL version 3 text](LICENSES/GPL-3.0-only.txt) is included for these
  historical attributed excerpts. It is not the license of Motley's original
  software, hardware or prose.

The linked revisions identify reviewed upstream evidence; they are not a claim
that the original research recorded those exact revision IDs.

## License-text sources

The MIT, Apache-2.0, CERN-OHL-P-2.0, CC-BY-SA-4.0 and GPL-3.0 texts were copied
from [SPDX license-list-data revision 31846481de7ea17d92f2f46fad76abe58b2e9bb0](https://github.com/spdx/license-list-data/tree/31846481de7ea17d92f2f46fad76abe58b2e9bb0/text).
Whitespace was normalized and the MIT copyright placeholder was filled with
`2026 altendky and contributors`; the license terms were not changed. The KiCad
exception is preserved verbatim from the upstream license notice.
