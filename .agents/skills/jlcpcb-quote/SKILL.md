---
name: jlcpcb-quote
description: Prepare current Motley KiCad exports and obtain JLCPCB prices through its web API, separating fabrication, confirmed assembly and unquoted costs.
---

# JLCPCB quotes

Use quotation-only API operations. Do not add to a cart, order, pay or purchase
component inventory. These are undocumented frontend APIs; inspect current
contracts and responses before relying on them. Browser automation is not
needed for the verified fabrication workflow.

## Current inputs

- Export each current `hardware/controller/motley-*.kicad_pcb` separately with
  pinned KiCad, actual saved copper fills, all enabled copper layers, mask,
  silkscreen, outline and drills. Use disposable copies for export origins;
  preserve native source hashes.
- Generate matching BOM/CPL pairs from current placements. Reconcile every
  footprint as factory candidate, manual/unmatched, DNP or bare mechanical/access
  feature. Catalogue codes require exact manufacturer/package/variant checks;
  generic quotation candidates must be explicit. Keep required unmatched parts
  visible, including mains/pulse resistors. Catalogue presence is not assembly
  availability or a quote.
- One complete controller currently uses one carrier, one sensor mux and **two
  identical output boards**. Check actual fabrication/assembly minimums and price
  spare boards; finish only the required assemblies unless requested otherwise.

## Verified API operations

Base: `https://cart.jlcpcb.com/api/overseas-core-platform`.

| Operation | Request |
| --- | --- |
| Gerber upload | `POST /file/uploadGerber`, multipart `gerberFile=@archive.zip`, `calculationCostsType=1`; retain `data.fileId` |
| Gerber analysis | `POST /order/analysisGerber`, form `fileId`, `calculationCostsType=1`, `fromDemo=`; poll boundedly until `data.head=ok` |
| PCB price | `POST /shoppingCart/calculationGoodsCostsNew`, JSON with current `pcbGoodsRequest`, `calculationCostsType=1`, `smtGoodRequest:null`, `steelmeshGoodsRequest:null`, `editCartFlag:false` and applicable service settings |
| Part lookup | `GET /shoppingCart/smtGood/getComponentDetail?componentCode=C...` |
| Assembly configuration | `GET /order/getSmtOrderConfig` and `GET /shoppingCart/getSmtConfigFee` |
| Final assembly price | `POST /newShoppingCart/calculation`, with `calculationCostsType:4`, `orderType:4`, `pcbGoodsRequest:{pcbGoodsAccessId}` and the actual matched `smtGoodRequest` |

For PCB pricing, configure `stencilWidth`/`stencilLength` in mm, `stencilCounts`,
`stencilLayer`, `stencilPly`, outer/inner copper, material, finish and mask to
match the requested comparison. Verify detected dimensions and layer count
against the exports. Check response `code`, not HTTP status alone; retain the
request, response, date, settings and input hashes. A PCB-only price has
`smtGoodRequest:null` and cannot be reported as a populated-board quote.

Assembly BOM/CPL upload uses `/bomCpl/upload/file`. Final assembly pricing needs
the saved job and matched `selectList` records, quantities and BOM/CPL file IDs;
catalogue prices cannot substitute for those records. Both job operations and
the final calculator return **460** when logged out. Obtain an authorized API
session or report the authentication block; do not invent assembly costs or
switch to a browser silently.
Only claim an assembly quote after actual matching/selections, stock, quantities
and service charges have been confirmed by JLC. Keep credentials out of logs.

## Report

Separate quoted PCB/assembly charges, missing or hand-fitted parts and off-board
allowances. Include quantity/attrition constraints, unresolved matches, shipping
and tax exclusions. A fuse record may require a cartridge plus two clips; an
outlet handoff terminal does not include the receptacle. Round presentation
totals only after summing unrounded amounts. Preserve useful aggregate evidence
with the cost documentation; keep generated quote files temporary. Export and
quote acceptance do not establish manufacturing readiness.
