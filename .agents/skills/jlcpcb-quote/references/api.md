# Verified quotation API

Observed 2026-11-15. Base:
`https://cart.jlcpcb.com/api/overseas-core-platform`.
Check response `code`, not HTTP status alone. Code 460 means logged out.

## Fabrication

1. `POST /file/uploadGerber`: multipart `gerberFile`,
   `calculationCostsType=1`; retain `data.fileId`.
2. `POST /order/analysisGerber`: form `fileId`, `calculationCostsType=1`,
   `fromDemo=`. Poll boundedly until `data.head=ok`.
3. `POST /shoppingCart/quereyOrderService`: JSON `plateType:1`,
   `stencilLayer`. Preserve the spelling `querey`.
4. `POST /shoppingCart/calculationGoodsCostsNew`: JSON with current
   `pcbGoodsRequest`, `calculationCostsType:1`, `smtGoodRequest:null`,
   `steelmeshGoodsRequest:null`, `editCartFlag:false` and applicable services.

PCB attributes include `stencilWidth`/`stencilLength` in mm, `stencilCounts`,
`stencilLayer`, `stencilPly`, copper weights, material, finish and mask.
Build `orderServiceConfigVos` from the defaults' `configOptionListVos` and
`defaultOption`; an empty service list produced code 500. Retain actual selected
normal build time. PCB-only pricing cannot stand in for populated-board pricing.

## Assembly quantities and drafts

Read `/order/getSmtOrderConfig`, `/shoppingCart/getSmtConfigFee` and
`/order/getOrderMaxDimensions`. With `smtFiveChoiceTwoSwitch:yes`, Economic
(`pcbAType:1`) allowed two or five assemblies from five fabricated boards,
and ten from ten. Arbitrary smaller quantities required Standard
(`pcbAType:0`). Recheck these rules rather than forcing an unsupported count.

`POST /newShoppingCart/temp/pcbGoods/add` saves a quotation draft, without cart
addition. Use the full current frontend form, not the reduced pricing DTO:

- `pcbGoods` includes `goodsType:4`, `typeNum:4`, `fileAccessId`, uploaded filename,
  detected technology identifiers, physical attributes and selected build time.
- `orderServiceAddCartVos` carries the actual selected service options/fees.
- `orderType:"example"`, `pcbGerberResult:1` after successful analysis.
- `smtGoodsParam` includes Economic type, top `patchLocation:"T"`,
  `pasteNumber`, `patchType:"all"` or `"no"` for partial assembly, and current
  fiducial/location-hole/fixture/personal-service settings.

Read back `GET /newShoppingCart/pcbGoods/temp/info?fileAccessId=GERBER_ID`.
The response uses `data.pcbGoods` and `data.smtGoodsCache`. Draft creation and
editing can return **new** `pcbGoodsAccessId` values; verify actual readback
instead of assuming IDs remain stable. Fabrication count is `stencilCounts`;
the persisted assembly count is `smtGoodsCache.allPatchNum`.

## BOM/CPL matching

1. `POST /bomCpl/upload/file?fileType=bom` and `fileType=coordinate`:
   multipart `bomCplFile`, `multiSheetCheckFlag:true`. The file ID is returned
   in **`message`**.
2. `POST /bomCpl/analyze/file` with actual `pcbGoodsAccessId`, `bomFileNo`,
   `coordinateFileNo`, `fromDemo:false`.
3. `GET /bomCpl/analyze/status?bomFileNo=...`; wait for `taskState:4` and retain
   `bomParsingTaskId`.
4. `POST /bomCpl/analyze/result` with Gerber `fileAccessId`,
   `checkDesignatorFlag:true`, `checkSpellBordFlag:true`, and full
   `smtGoodsParam` containing these file/task IDs and requested quantity/settings.
5. Audit `data.componentList` against every submitted reference/code. A row
   must be selected, matched and in stock (`selectStatus:1`, `matchStatus:1`,
   `stockStatus:"inStock"`), with an approved exact code and appropriate service
   eligibility. `confirmedNum` also counts deselected matches.
6. Deselect unsuitable automatic matches through
   `POST /bomCpl/row/update/selectStatus` with actual
   `smtGoodsCacheDetailsAccessIds` and `selectStatus:2`.
7. Refresh using `POST /bomCpl/select/by/file` with `fileAccessId`, and read
   temp info again. Reconcile the selected reference set and quantities.

Repeat matching for changed quantities: stock and attrition can move parts
between factory and hand assembly. `GET
/shoppingCart/smtGood/getComponentDetail?componentCode=C...` supports part
research but does not establish assembly availability.

## Final price

`POST /newShoppingCart/calculation` accepts:

```json
{
  "calculationCostsType": 4,
  "orderType": 4,
  "pcbGerberResult": 0,
  "pcbGoodsRequest": {"pcbGoodsAccessId": "ACTUAL_DRAFT_ID"},
  "smtGoodRequest": "ACTUAL_CACHE_WITH_FULL_SELECTED_ROWS"
}
```

Replace the illustrative string with the actual cache object, `pasteNumber`,
`pcbAType`, `patchLocation` and `selectList` of full persisted selected rows.
Do not invent row IDs or multiply an earlier quote for another quantity.

The final calculator uses JLC's normal key-initializing HTTP client. Raw fetch
returned code 29003 (missing key). Use the active frontend's normal request
wrapper so it performs its own key setup/retry/decryption; never extract key
storage or return the whole Axios response, which includes request headers.
Observed quote-page wrapper: module 1's `http` (SMT page: `H`), with
`http.post('/overseas-core-platform/newShoppingCart/calculation')(payload,
{flat:false,errToReject:false,hideDefaultErrorMsg:true})`. Retain only response
status/data. Verify current public frontend code before relying on this shape.
Remove any task-local request adapter afterward without closing the client.

Use returned `totalRealMoney`, actual PCB charge and
`itemCosts.smtPriceInfo`. `smtRealMoney` was null while `smtDummyMoney` contained
the assembly/component total. Verify these reconcile. Report current stock
omissions separately; quoted assembly can remain partial.
