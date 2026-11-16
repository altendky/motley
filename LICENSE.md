# Licensing

Copyright (c) 2026 altendky and contributors. Each contributor retains copyright
in their contributions. The grants below apply to original Motley material;
third-party material retains its identified upstream terms.

All complete license texts and the upstream library exception are in
[`LICENSES/`](LICENSES/).

| Material | License |
| --- | --- |
| Original software, scripts, tooling/configuration, general documentation and requirements | [MIT](LICENSES/MIT.txt) **OR** [Apache-2.0](LICENSES/Apache-2.0.txt), at your option |
| Original hardware designs and independently created symbols/footprints | [CERN-OHL-P-2.0](LICENSES/CERN-OHL-P-2.0.txt) |
| Generated hardware design/manufacturing outputs | CERN-OHL-P-2.0 for the original Motley design, with applicable upstream exceptions preserved |
| Third-party material, including copied/adapted reusable library parts and attributed historical research excerpts | The terms identified in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) |

## Hardware scope

The CERN-OHL-P-2.0 grant covers the original content of native KiCad schematics,
boards, projects, rules, symbol and footprint libraries, and library tables
under `hardware/`: `*.kicad_sch`, `*.kicad_pcb`, `*.kicad_pro`, `*.kicad_dru`,
`*.kicad_sym`, `*.kicad_mod`, `sym-lib-table` and `fp-lib-table`. It also covers
generated design representations and fabrication data such as board SVGs,
schematic drawings, Gerbers and drill/placement/BOM exports. Original symbols
and footprints use CERN-OHL-P-2.0 even when shared in a reusable library.

General explanatory Markdown, scripts and non-CAD configuration remain under
the MIT OR Apache-2.0 grant. An embedded/exported hardware drawing follows the
hardware license; placing it in a document does not relicense the drawing.

The local libraries contain both original and upstream-derived parts. Their
names do not determine ownership. The per-entry exceptions in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) identify the reusable parts
that retain CC-BY-SA-4.0 with the upstream KiCad library exception. The CERN
grant does not replace the upstream license on those parts or their adaptations.

KiCad and Espressif waive CC-BY-SA article 3 for electronic designs using their
library material and generated files from those designs. This permits the
Motley board designs and their outputs to use CERN-OHL-P-2.0 while redistributed
reusable library parts retain the upstream terms. Preserve that exception
alongside the [CC-BY-SA-4.0 text](LICENSES/CC-BY-SA-4.0.txt) and
[attribution/modification notices](THIRD_PARTY_NOTICES.md).

## Third-party and historical material

The default grants do not relicense upstream code, artwork, libraries, license
documents or attributed excerpts, including excerpts retained in Git history.
Dependencies and downloaded development tools retain their own licenses; a
firmware distribution must preserve the notices applicable to its actual
included components. The repository grants do not grant rights to someone
else's patents, trademarks or datasheets.
