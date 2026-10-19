#!/usr/bin/env python3
"""Generate KiCad (v8+) symbols for AutomationDirect Productivity1000 modules.

Everything sits on a 0.0625 in (1.5875 mm) grid. One terminal = one row, rows are
4 grid units (0.25 in) apart. Unused terminals ("N.C." / blank) keep their row but
get no pin, so the symbol mirrors the physical terminal block.

Per symbol:
  * left edge  : zero-length connection points, pin name drawn inside the body
  * right edge : duplicate connection points (same pin numbers), name "~" (no name)
  * pin numbers are drawn as text inside the body next to each connection point
    (KiCad's own pin-number display is hidden)
  * divider lines (0.25 in long, from the left edge) separate terminal groups
  * part number runs vertically inside the body

Usage:  python3 p1000_symgen.py            -> writes P1000.kicad_sym
Add modules by appending to MODULES below. Terminal order was read from each
module's wiring drawing in the AutomationDirect datasheet / insert.
"""
G = 1.5875            # 0.0625 in in mm
PITCH = 4 * G         # one terminal row = 0.25 in
SEP_LEN = 4 * G       # divider lines run 0.25 in in from the left (name) side
NUM_DX = 1.4          # pin-number text centre, mm inside the body edge
NUM_FONT = 1.0
NAME_OFF = 2 * G      # pin names start this far inside the left edge
FONT = 1.27
INSERT = "https://cdn.automationdirect.com/static/manuals/p1userm/inserts/{}.pdf"
SPEC = "https://cdn.automationdirect.com/static/specs/{}.pdf"


def f(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ---------------------------------------------------------------- terminal rows
# A row is (name, group). name None = unused terminal (row kept, no pin).
# A divider is drawn wherever the group changes between two consecutive rows.
GAP = (None, "gap")


def seq(fmt, a, b, grp):
    return [(fmt.format(i), grp) for i in range(a, b + 1)]


def gaps(n, tag="gap"):
    return [(None, tag)] * n


def disc_in8(prefix="I"):          # C1, 1-4, C2, 5-8
    return [("C1", "c1")] + seq(prefix + "{}", 1, 4, "g1") + [("C2", "c2")] + seq(prefix + "{}", 5, 8, "g2")


def disc_16(prefix="I"):           # C1, 1-8, C2, 9-16
    return [("C1", "c1")] + seq(prefix + "{}", 1, 8, "g1") + [("C2", "c2")] + seq(prefix + "{}", 9, 16, "g2")


MODULES = []


def add(part, desc, rows, kw="", ds=None):
    MODULES.append(dict(part=part, desc=desc, rows=rows, keywords=kw or "P1000 Productivity1000 PLC",
                        ds=ds or INSERT.format(part)))


# ---- Power supply / CPU ---------------------------------------------------------
add("P1-01AC", "Productivity1000 power supply, 100-240VAC / 125VDC in, 24VDC 0.67A out",
    [("L/+V", "ac"), ("N/-V", "ac"), ("G", "g"), ("LG", "lg")],
    "P1000 power supply AC")
add("P1-540", "Productivity1000 CPU. One pin per port: RS-485 (T,+,-,G terminal block), micro USB, RS-232 (RJ12), "
    "Ethernet (RJ45). 24V/COM/GND = 24VDC supplied through the stacking connector from the power supply",
    [("24V", "pwr"), ("COM", "pwr"), ("GND", "pwr"),
     ("RS-485", "rs485"), ("USB", "usb"), ("RS-232", "rs232"), ("ETHERNET", "eth")],
    "P1000 CPU RS485 RS232 USB Ethernet", ds=SPEC.format("P1-540"))

# ---- DC discrete ----------------------------------------------------------------
add("P1-08ND-TTL", "Productivity1000 8-pt 3.3-5VDC TTL input, 2 commons", disc_in8(), "P1000 discrete input TTL",
    ds=SPEC.format("P1-08ND-TTL"))
add("P1-08ND3", "Productivity1000 8-pt 12-24VDC fast input (sink/source), 2 commons", disc_in8(),
    "P1000 discrete input DC")
add("P1-16ND3", "Productivity1000 16-pt 12-24VDC fast input (sink/source), 2 commons", disc_16(),
    "P1000 discrete input DC")
add("P1-08TD-TTL", "Productivity1000 8-pt TTL output, 2 commons",
    [("COM", "c1")] + seq("O{}", 1, 4, "g1") + [("COM", "c2")] + seq("O{}", 5, 8, "g2"),
    "P1000 discrete output TTL", ds=SPEC.format("P1-08TD-TTL"))
add("P1-08TD1", "Productivity1000 8-pt 12-24VDC sinking output",
    [("24V", "pwr")] + seq("O{}", 1, 4, "g1") + [("COM", "com")] + seq("O{}", 5, 8, "g2"),
    "P1000 discrete output DC sinking")
add("P1-08TD2", "Productivity1000 8-pt 12-24VDC sourcing output",
    [("V+", "pwr")] + seq("O{}", 1, 4, "g1") + [("COM", "com")] + seq("O{}", 5, 8, "g2"),
    "P1000 discrete output DC sourcing")
add("P1-15TD1", "Productivity1000 15-pt 12-24VDC sinking output, 2 commons",
    [("C1", "c1")] + seq("O{}", 1, 8, "g1") + [("C2", "c2")] + seq("O{}", 9, 15, "g2") + [("V+", "pwr")],
    "P1000 discrete output DC sinking")
add("P1-15TD2", "Productivity1000 15-pt 12-24VDC sourcing output, 2 supplies",
    [("V1", "c1")] + seq("O{}", 1, 8, "g1") + [("V2", "c2")] + seq("O{}", 9, 15, "g2") + [("0V", "pwr")],
    "P1000 discrete output DC sourcing")
add("P1-15CDD1", "Productivity1000 combo: 8-pt DC input, 7-pt sinking DC output",
    [("C1", "c1")] + seq("I{}", 1, 8, "in") + [("C2", "c2")] + seq("O{}", 1, 7, "out") + [("V+", "pwr")],
    "P1000 discrete combo DC")
add("P1-15CDD2", "Productivity1000 combo: 8-pt DC input, 7-pt sourcing DC output",
    [("C1", "c1")] + seq("I{}", 1, 8, "in") + [("V+", "pwr")] + seq("O{}", 1, 7, "out") + [("C2", "c2")],
    "P1000 discrete combo DC")

# ---- AC discrete ----------------------------------------------------------------
add("P1-08NE3", "Productivity1000 8-pt 24VAC/DC input, 2 commons", disc_in8(), "P1000 discrete input AC DC")
add("P1-16NE3", "Productivity1000 16-pt 24VAC/DC input, 2 commons", disc_16(), "P1000 discrete input AC DC")
add("P1-08NA", "Productivity1000 8-pt 100-240VAC input, 2 commons", disc_in8(), "P1000 discrete input AC")
add("P1-08TA", "Productivity1000 8-pt 100-240VAC output, 2 commons", disc_in8("O"), "P1000 discrete output AC")

# ---- Relay / solid-state output -------------------------------------------------
add("P1-04TRS", "Productivity1000 4-pt isolated relay output (Form C)",
    [("C1", "r1"), ("NO1", "r1"), ("NC1", "r1")] + gaps(2) +
    [("C2", "r2"), ("NO2", "r2"), ("NC2", "r2")] + gaps(2) +
    [("C3", "r3"), ("NO3", "r3"), ("NC3", "r3")] + gaps(2) +
    [("C4", "r4"), ("NO4", "r4"), ("NC4", "r4")],
    "P1000 relay output")
add("P1-08TRS", "Productivity1000 8-pt isolated relay output (CH1 and CH5 Form C)",
    [("NC1", "r1"), ("C1", "r1"), ("NO1", "r1"),
     ("C2", "r2"), ("NO2", "r2"), ("C3", "r3"), ("NO3", "r3"), ("C4", "r4"), ("NO4", "r4"),
     ("NC5", "r5"), ("C5", "r5"), ("NO5", "r5"),
     ("C6", "r6"), ("NO6", "r6"), ("C7", "r7"), ("NO7", "r7"), ("C8", "r8"), ("NO8", "r8")],
    "P1000 relay output")
add("P1-16TR", "Productivity1000 16-pt relay output, 2 commons", disc_16("O"), "P1000 relay output")
add("P1-16CDR", "Productivity1000 combo: 8-pt DC input, 8-pt relay output",
    [("C1", "c1")] + seq("I{}", 1, 8, "in") + [("C2", "c2")] + seq("O{}", 1, 8, "out"),
    "P1000 discrete combo relay")
add("P1-12CDRS", "Productivity1000 combo: 8-pt DC input, 4-pt isolated relay output",
    [("IC1", "c1")] + seq("I{}", 1, 4, "g1") + [("IC2", "c2")] + seq("I{}", 5, 8, "g2") +
    [("C1", "r1"), ("NO1", "r1"), ("C2", "r2"), ("NO2", "r2"),
     ("C3", "r3"), ("NO3", "r3"), ("C4", "r4"), ("NO4", "r4")],
    "P1000 discrete combo relay")
add("P1-04TEPS", "Productivity1000 4-pt isolated AC/DC solid-state output (N.C. terminals unused)",
    [GAP, ("C1", "ch1"), ("O1", "ch1"), ("C2", "ch2"), ("O2", "ch2"), GAP,
     ("C3", "ch3"), ("O3", "ch3"), ("C4", "ch4"), ("O4", "ch4")],
    "P1000 solid state output")

# ---- Analog input ---------------------------------------------------------------
add("P1-04AD", "Productivity1000 4-ch analog input, 0-20mA or 0-5/0-10V selectable (jumper I+ to V+ for current)",
    [("COM", "c0")] + [(n, "in") for i in range(1, 5) for n in (f"V{i}+", f"I{i}+")] +
    [("COM", "c1")] * 3 + gaps(4) + [("0V", "pwr"), ("24V", "pwr")],
    "P1000 analog input voltage current")
add("P1-04AD-1", "Productivity1000 4-ch 0-20mA analog input",
    [("24V", "pwr")] + seq("I{}+", 1, 4, "in") + [("0V", "ret")] + [("COM", "com")] * 4, "P1000 analog input current")
add("P1-04AD-2", "Productivity1000 4-ch 0-5/0-10V analog input",
    [("24V", "pwr")] + seq("V{}+", 1, 4, "in") + [("0V", "ret")] + [("COM", "com")] * 4, "P1000 analog input voltage")
add("P1-04ADL-1", "Productivity1000 4-ch 0-20mA analog input, 13-bit",
    [("24V", "pwr")] + seq("I{}+", 1, 4, "in") + [("0V", "ret")] + [("COM", "com")] * 4, "P1000 analog input current",
    ds=SPEC.format("P1-04ADL-1"))
add("P1-04ADL-2", "Productivity1000 4-ch 0-10V analog input, 13-bit",
    [("24V", "pwr")] + seq("V{}+", 1, 4, "in") + [("0V", "ret")] + [("COM", "com")] * 4, "P1000 analog input voltage")
add("P1-08ADL-1", "Productivity1000 8-ch 0-20mA analog input, 13-bit",
    [("24V", "pwr")] + seq("I{}+", 1, 4, "in1") + [("0V", "ret")] + seq("I{}+", 5, 8, "in2"), "P1000 analog input current")
add("P1-08ADL-2", "Productivity1000 8-ch 0-10V analog input, 13-bit",
    [("24V", "pwr")] + seq("V{}+", 1, 4, "in1") + [("0V", "ret")] + seq("V{}+", 5, 8, "in2"), "P1000 analog input voltage")

# ---- Analog output --------------------------------------------------------------
add("P1-04DAL-1", "Productivity1000 4-ch 4-20mA analog output, 12-bit",
    [("24V", "pwr")] + seq("O{}+", 1, 4, "out") + [("0V", "ret")] + [("COM", "com")] * 4, "P1000 analog output current",
    ds=SPEC.format("P1-04DAL-1"))
add("P1-04DAL-2", "Productivity1000 4-ch 0-10V analog output, 12-bit",
    [("24V", "pwr")] + seq("V{}+", 1, 4, "out") + [("0V", "ret")] + [("COM", "com")] * 4, "P1000 analog output voltage")
add("P1-08DAL-1", "Productivity1000 8-ch 4-20mA analog output, 12-bit",
    [("24V", "pwr")] + seq("O{}+", 1, 4, "out1") + [("0V", "ret")] + seq("O{}+", 5, 8, "out2"), "P1000 analog output current",
    ds=SPEC.format("P1-08DAL-1"))
add("P1-08DAL-2", "Productivity1000 8-ch 0-10V analog output, 12-bit",
    [("24V", "pwr")] + seq("V{}+", 1, 4, "out1") + [("0V", "ret")] + seq("V{}+", 5, 8, "out2"), "P1000 analog output voltage")

# ---- Analog combo ---------------------------------------------------------------
add("P1-4ADL2DAL-1", "Productivity1000 analog I/O: 4x 0-20mA in (13-bit), 2x 4-20mA out (12-bit)",
    [("24V", "pwr")] + seq("I{}+", 1, 4, "in") + [("0V", "ret")] + seq("O{}+", 1, 2, "out") + [("COM", "com")] * 2,
    "P1000 analog current input output", ds=SPEC.format("P1-4ADL2DAL-1"))
add("P1-4ADL2DAL-2", "Productivity1000 analog I/O: 4x 0-10V in (13-bit), 2x 0-10V out (12-bit)",
    [("24V", "pwr")] + seq("V{}+", 1, 4, "in") + [("0V", "ret")] + seq("O{}+", 1, 2, "out") + [("COM", "com")] * 2,
    "P1000 analog voltage input output", ds=SPEC.format("P1-4ADL2DAL-2"))

# ---- Temperature ----------------------------------------------------------------
add("P1-04THM", "Productivity1000 4-ch thermocouple input",
    [("TC1+", "ch1"), ("TC1-", "ch1"), ("TC2+", "ch2"), ("TC2-", "ch2"), GAP,
     ("TC3+", "ch3"), ("TC3-", "ch3"), ("TC4+", "ch4"), ("TC4-", "ch4"), GAP],
    "P1000 thermocouple temperature input")
add("P1-04THMS", "Productivity1000 4-ch thermocouple input, 2 isolated groups (18-pos terminal block)",
    [("TC1+", "ch1"), ("TC1-", "ch1")] + gaps(4) + [("TC2+", "ch2"), ("TC2-", "ch2")] + gaps(2) +
    [("TC3+", "ch3"), ("TC3-", "ch3")] + gaps(4) + [("TC4+", "ch4"), ("TC4-", "ch4")],
    "P1000 thermocouple temperature input")
add("P1-04NTC", "Productivity1000 4-ch thermistor (NTC) input",
    [("CH1+", "ch1"), ("CH1-", "ch1"), ("CH2+", "ch2"), ("CH2-", "ch2"), GAP,
     ("CH3+", "ch3"), ("CH3-", "ch3"), ("CH4+", "ch4"), ("CH4-", "ch4"), GAP],
    "P1000 thermistor NTC temperature input")
add("P1-04RTD", "Productivity1000 4-ch RTD input",
    [("R1+", "ch1"), ("R1-", "ch1"), ("R2+", "ch2"), ("R2-", "ch2"), ("COM", "com"), ("COM", "com"),
     ("R3+", "ch3"), ("R3-", "ch3"), ("R4+", "ch4"), ("R4-", "ch4")],
    "P1000 RTD temperature input")


# ------------------------------------------------------------------- geometry
def geometry(m, pitch=PITCH):
    import math
    rows = m["rows"]
    n = len(rows)
    top = (n - 1) / 2 * pitch                       # y of terminal 1
    maxlen = max(len(name) for name, _ in rows if name)
    # body half-width: 0.5 in for names up to 3 chars, grows (in grid steps) for longer names
    half_w = G * max(4, math.ceil((6.85 + 1.87 * maxlen) / 2 / G - 1e-9))
    pins = [(str(i + 1), name, top - i * pitch) for i, (name, _) in enumerate(rows) if name]
    seps = []
    for i in range(n - 1):
        if rows[i][1] != rows[i + 1][1]:
            seps.append(top - i * pitch - pitch / 2)
    return dict(n=n, top=top, half_w=half_w, body_top=top + pitch / 2, body_bot=-(top + pitch / 2),
                pins=pins, seps=seps, label_x=half_w - 2 * G)


def build_symbol(m, pitch=PITCH):
    g = geometry(m, pitch)
    hw, name = g["half_w"], m["part"]
    eff = f"(effects (font (size {f(FONT)} {f(FONT)})))"
    hid = f"(effects (font (size {f(FONT)} {f(FONT)})) hide)"
    out = []
    out.append(f'  (symbol "{name}" (pin_numbers hide) (pin_names (offset {f(NAME_OFF)})) '
               f'(exclude_from_sim no) (in_bom yes) (on_board yes)')
    out.append(f'    (property "Reference" "U" (at 0 {f(g["body_top"] + 2*G)} 0) {eff})')
    out.append(f'    (property "Value" "{name}" (at 0 {f(g["body_bot"] - 2*G)} 0) {eff})')
    out.append(f'    (property "Footprint" "" (at 0 0 0) {hid})')
    out.append(f'    (property "Datasheet" "{m["ds"]}" (at 0 0 0) {hid})')
    out.append(f'    (property "Description" "{m["desc"]}" (at 0 0 0) {hid})')
    out.append(f'    (property "Manufacturer" "AutomationDirect" (at 0 0 0) {hid})')
    out.append(f'    (property "ki_keywords" "{m["keywords"]}" (at 0 0 0) {hid})')

    out.append(f'    (symbol "{name}_0_1"')
    out.append(f'      (rectangle (start {f(-hw)} {f(g["body_top"])}) (end {f(hw)} {f(g["body_bot"])})'
               f' (stroke (width 0.254) (type default)) (fill (type background)))')
    for y in g["seps"]:
        out.append(f'      (polyline (pts (xy {f(-hw)} {f(y)}) (xy {f(-hw + SEP_LEN)} {f(y)}))'
                   f' (stroke (width 0.1524) (type default)) (fill (type none)))')
    for num, _, y in g["pins"]:
        for x in (-hw + NUM_DX, hw - NUM_DX):       # left and right pin numbers (drawn text)
            out.append(f'      (text "{num}" (at {f(x)} {f(y)} 0)'
                       f' (effects (font (size {f(NUM_FONT)} {f(NUM_FONT)}))))')
    out.append(f'      (text "{name}" (at {f(g["label_x"])} 0 900) (effects (font (size 1.0 1.0))))')
    out.append('    )')

    out.append(f'    (symbol "{name}_1_1"')
    for num, pname, y in g["pins"]:
        out.append(f'      (pin passive line (at {f(-hw)} {f(y)} 0) (length 0)'
                   f' (name "{pname}" {eff}) (number "{num}" {eff}))')
        out.append(f'      (pin passive line (at {f(hw)} {f(y)} 180) (length 0)'
                   f' (name "~" {eff}) (number "{num}" {eff}))')
    out.append('    )')
    out.append('  )')
    return "\n".join(out)


# one library per terminal-row spacing; symbol names are identical in each library
LIBRARIES = {
    "P1000.kicad_sym": 4 * G,           # 0.25 in rows
    "P1000_0p5in.kicad_sym": 8 * G,     # 0.50 in rows
    "P1000_0p75in.kicad_sym": 12 * G,   # 0.75 in rows
}


def main():
    for path, pitch in LIBRARIES.items():
        lines = ['(kicad_symbol_lib (version 20231120) (generator "p1000_symgen") (generator_version "2.1")']
        lines += [build_symbol(m, pitch) for m in MODULES]
        lines.append(")")
        with open(path, "w") as fh:
            fh.write("\n".join(lines) + "\n")
        print("wrote", path, "-", len(MODULES), "symbols, row pitch", round(pitch / 25.4, 3), "in")


if __name__ == "__main__":
    main()
