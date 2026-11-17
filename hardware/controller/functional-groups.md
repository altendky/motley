# Functional component allocation

Every physical schematic component and PCB footprint has one hidden
`FunctionalGroup` field. The versioned
[catalog](functional-groups.toml) defines stable identifiers, ownership boundaries
and the boards on which each group is applicable. This is functional attribution;
there is no price database, cost calculation or purchasing model.

Run the executable uv script directly, from any working directory:

```sh
/path/to/motley/scripts/hardware_groups.py
```

From the repository root:

```sh
./scripts/hardware_groups.py
./scripts/hardware_groups.py --json
./scripts/test_hardware_groups.py
```

Both scripts use a `uv run` shebang and PEP 723 inline dependency declarations.
The checker currently needs only the Python standard library and the adjacent
native parser in `scripts/hardware_trace.py`. No KiCad process, quotation
credentials or network service is needed once uv has the required Python.

The local pre-commit `hardware-groups` hook runs on every commit. CI's existing
Repository checks job runs that same hook with `--all-files`; the regression
fixtures also run there. The checker never writes CAD or assigns a default group.

## Maintaining allocations

Edit `FunctionalGroup` in KiCad's Symbol Fields Table or a symbol's properties.
Keep it hidden. Update the PCB from the schematic so the footprint property
agrees. For a board-only mechanical footprint, edit the property on that
footprint. New groups need a catalog entry with a description and allowed boards.
The maintained root list is shared with the trace checker as
`scripts/hardware_trace.py:DESIGNS`; add new board roots there when introducing
another maintained design.

Checks reject missing/empty/duplicate fields, multiple/unknown identifiers,
groups disallowed on a board, inconsistent units of a multi-unit part, source/PCB
disagreement, duplicate/missing footprint matches and unresolved native identity.
All repeated sheet instances are counted separately. A multi-unit physical part
is counted once. DNP, excluded-BOM parts, test loops, touch pads and board-only
mounts still need allocations. Physical symbols with `on_board=no` also need a
group and appear in the inventory without a footprint. Virtual `#` power symbols,
sheet containers and embedded library definitions do not represent purchased
physical components and are excluded.

Known identifiers alone cannot prove that a component serves the claimed
function. Review that decision, including supporting passives and protection,
when editing the circuit. The current allocations cover 259 physical schematic
components and ten board-only mechanical footprints, 269 total across the three
board designs. Building two identical output boards repeats that board inventory;
the checker does not impose a system purchase quantity.

## Ownership boundaries

- The optional USB J27, three copper source selectors and two DNP CC pull-downs
  belong to `usb.service`, including the excluded-BOM copper features and DNP
  components. Their lack of purchased default parts does not remove allocation.
- Each package has one owner. A dual ESD array serving more than one signal is
  allocated as a package rather than split into fictitious components.
- Carrier Qwiic-sheet R40/R41 support the deployed sensor link and belong to
  `sensors.mux`; R42/R43 support the output bus and belong to `output.control`.
  Optional socket parts belong to `interfaces.bench`.
- The shared AC timing generator belongs to `ac.line-reference`. Output-local
  timing receiver filtering and protection belong to `output.control`, along
  with its regulator, recovery controls and programming connector.
- Carrier UART service J22 and its dedicated protection belong to
  `diagnostics.access`, as do the clip probe points and ground touch pads.
- A shared deployment header or supply clamp has one documented owner. Removing
  a group can require retaining or replacing shared support; attribution does
  not establish removable cost savings or safe electrical variants.

The initial metadata-only edit was checked by comparing parsed native files
with the new field removed. Wires, nets, UUIDs, multi-unit/repeated identity,
positions, pads, copper and all pre-existing properties are preserved. Group
fields are hidden and do not require different committed board SVGs.
