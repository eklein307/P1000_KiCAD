# AutomationDirect Productivity1000 (P1000) KiCad Symbols

KiCad symbols for 39 Productivity1000 modules: the P1-540 CPU, the P1-01AC power supply, and the discrete, relay, combo, analog and temperature I/O modules. Each symbol is a simplified picture of the module's front terminal block, so pin order on screen matches the order of the physical terminals.

## Files

| File | Contents |
|---|---|
| `P1000.kicad_sym` | Library with 0.25" (4 grid) row pitch |
| `P1000_0p5in.kicad_sym` | Same symbols, 0.5" (8 grid) row pitch |
| `P1000_0p75in.kicad_sym` | Same symbols, 0.75" (12 grid) row pitch |
| `p1000_symgen.py` | Generator script that writes all three libraries |
| `P1000_preview_*.png` | Preview sheets of every symbol (0.25" pitch) |
| `P1-540_preview.png` | CPU at all three pitches |

The three libraries contain the same 39 symbols with the same names and pin numbers. Pick one by how much room you want for wiring; a design can use only one library per symbol, but all three can be installed together. Install a library through *Preferences, Manage Symbol Libraries* and add the `.kicad_sym` file. The format is KiCad 8 (`version 20231120`). The format was checked in KiCad on an early single-symbol version; the full libraries have not been opened in KiCad yet.

## Symbol conventions

- **Grid:** everything is on a 0.0625" (1.5875 mm) grid, so set the schematic grid to 62.5 mil (1.5875 mm) and wires will land on every connection point.
- **One row per terminal.** Row *n* from the top is terminal *n* of the module. Terminals that are blank on the module (for example the gaps in the 4-point relay card) keep their row but have no pin.
- **Connection points** are zero-length pins sitting exactly on the left and right edges of the body. There are no pin stubs.
- **Pin numbers** are drawn inside the body next to each connection point. They are graphic text, so they do not update if you renumber a pin in the symbol editor.
- **Left and right pins are duplicates.** Every terminal appears on both edges with the same number. The left pin carries the name (`I1`, `O3`, `C1`, `V1+`, and so on) and the right pin is named `~` so nothing is drawn. KiCad treats the pair as one pad in the netlist. The electrical rules checker may warn about duplicate pin numbers; the pairing is deliberate, so connect either side.
- **Dividers:** a 0.25" line from the left edge marks where terminal groups change (commons versus channels, supply versus outputs, and so on), matching the grouping printed on the module.
- **Part number** runs vertically inside the body near the right edge.
- **Width** is the smallest body that fits the longest pin name (minimum 0.5"); the CPU is 0.875" wide because of its "ETHERNET" label.
- **Pin type** is passive for every pin.

## Naming

- Discrete inputs `I#`, discrete outputs `O#`, with commons and supplies as printed on the module (`C1`, `C2`, `V+`, `0V`, `24V`, and so on).
- Analog outputs are `O#+` for current and `V#+` for voltage; analog inputs are `I#+` and `V#+`.
- On the P1-12CDRS the input commons are `IC1` and `IC2`.
- Thermocouple, thermistor and RTD inputs use the pair names printed on the module.

## The CPU (P1-540)

The CPU has one pin per connection rather than one per terminal:

| Pin | Name | Meaning |
|---|---|---|
| 1 | 24V | 24 VDC from the power supply |
| 2 | COM | Power common |
| 3 | GND | Ground |
| 4 | RS-485 | The T, +, -, G terminal block, collapsed to one pin |
| 5 | USB | Micro USB port |
| 6 | RS-232 | RJ12 port |
| 7 | ETHERNET | RJ45 port |

Notes:

- The real P1-540 has no wired power terminals. Power arrives through the stacking connector from the power supply, so the 24V / COM / GND pins stand for that backplane power.
- The RS-485 terminal detail is recorded in the symbol's Description field.
- The microSD slot has no pin.
- Pin numbers 1 to 7 are an arbitrary ordering, not manufacturer numbers.

## Included modules

| Group | Parts |
|---|---|
| Power supply | P1-01AC |
| CPU | P1-540 |
| DC inputs | P1-08ND-TTL, P1-08ND3, P1-16ND3 |
| DC outputs | P1-08TD-TTL, P1-08TD1, P1-08TD2, P1-15TD1, P1-15TD2 |
| DC combo | P1-15CDD1, P1-15CDD2 |
| AC and AC/DC inputs | P1-08NE3, P1-16NE3, P1-08NA |
| AC and AC/DC outputs | P1-08TA, P1-04TEPS |
| Relay outputs | P1-04TRS, P1-08TRS, P1-16TR |
| Relay combo | P1-16CDR, P1-12CDRS |
| Analog inputs | P1-04AD, P1-04AD-1, P1-04AD-2, P1-04ADL-1, P1-04ADL-2, P1-08ADL-1, P1-08ADL-2 |
| Analog outputs | P1-04DAL-1, P1-04DAL-2, P1-08DAL-1, P1-08DAL-2 |
| Analog combo | P1-4ADL2DAL-1, P1-4ADL2DAL-2 |
| Temperature | P1-04THM, P1-04THMS, P1-04NTC, P1-04RTD |

**Not included:** remote I/O (P1-RX, P1-UX), the motion and specialty modules (PS-AMC, P1-02HSC, P1-04PWM, P1-08SIM), other CPUs, other power supplies, and the Mini PLCs.

## Source of the pin orders

Terminal order for each module was read from the wiring drawing in the AutomationDirect module insert or datasheet, not from the text of the PDFs, which proved ambiguous. Each symbol's Datasheet field links to the AutomationDirect specification sheet. Check the physical module and current datasheet before building a board or panel.

## Regenerating or extending

```
python3 p1000_symgen.py
```

writes all three libraries into the current directory. To add a module, append an `add(part, description, rows, keywords, ds=...)` call, where `rows` is a list of `(pin_name_or_None, group_tag)` per terminal from top to bottom. A divider is drawn wherever the group tag changes between consecutive rows. To add another pitch, add an entry to `LIBRARIES` mapping a filename to a pitch in multiples of `G`.

## Disclaimer

Unofficial and not affiliated with AutomationDirect. Productivity1000 is a trademark of AutomationDirect. Verify wiring against the manufacturer's documentation.
