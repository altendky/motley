# ADR-0016: Flexible sensor-core aspect ratio behind the connector row

- **Status:** Accepted for the exploratory hardware study
- **Date:** 2026-11-13
- **Classification:** discretionary_design_choice
- **Related requirements:** `MOT-PROC-001`
- **Related ADRs:** [ADR-0011](0011-single-output-modules-and-sensor-core.md)
- **Affected components:** Sensor-board placement, outline and cut-down variants

## Context

The developer clarified that accepting a core spanning two or more connector
positions did not constrain the common mux circuitry to two positions. Its area
can trade width along the connector row against depth behind it. The existing
19 mm-wide fixed leg is one placement study, not a packaging requirement.

## Decision drivers

- Let the connector row determine the full board's length.
- Keep the common circuitry behind the connectors.
- Allow practical component placement and enclosure aspect-ratio choices.
- Retain optional trimming without removing required common circuitry.

## Options considered

| Option | Benefits | Costs and limitations |
| --- | --- | --- |
| Fix the common area to two connector positions | Smaller minimum retained width | Artificially constrains placement and can increase depth |
| Choose the common area's aspect ratio during placement | Can spread parts behind more connectors and reduce depth | A wider common area increases the minimum retained width after trimming |

## Decision

Allow the mux, upstream interface, support parts and mechanical/access features
to occupy a flexible common area behind the connector row. There is no fixed
number of connector positions that this area must span. Trade width against
depth within the full connector-controlled board length and enclosure needs.

Tail cuts must preserve the complete common circuitry. Determine available
cut-down variants from the chosen placement; do not assume that every future
layout can retain the current two-connector minimum.

## Consequences

The current native board and PDFs remain a placement snapshot. A later revision
can use a wider, shallower common area, including investigating room for all
fitted components on the front. This clarification changes no circuit, assembly
selection or qualification claim. Recheck cut retention and placement clearances
when geometry changes.

## Supersession

Supersedes only ADR-0011's restriction of the common area to the first two
connector positions. Its connector-controlled length, per-output modularity and
other decisions remain applicable. Superseded by: None.
