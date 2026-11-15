"""
BT4-V 3D Printed Antenna — Spine Segment Generator (v0.3.0)

Generates the modular vertical spine strut that spaces adjacent bay brackets
at the exact 130.0 mm pitch (between Bay 1–2 and Bay 3–4), exported as
'stl/BT4V_Spine_Segment.stl'. Quantity required: 2.

Technical Specifications:
- Requirements Baseline: Requirements.md §7, §16.3
- Body Dimensions / Extents: 30.0 mm (X) x 14.0 mm (Y) x 110.0 mm (Z) (tol +/-0.1 mm)
  * Active length: 100.0 mm between shoulder stops (+ 10.0 mm tenon = 110.0 mm total Z),
    yielding an exact 130.0 mm center-to-center bay pitch when assembled with 30.0 mm
    active bay brackets (15.0 + 100.0 + 15.0 = 130.0 mm).
- Nominal Volume: 21,000 mm^3 (+/-2% -> acceptable range: 20,580 – 21,420 mm^3)
- Solid Count: Exactly 1 valid solid (len(shape.Solids) == 1, shape.isValid() == True)

Mechanical & RF Features:
- Flanged I-Beam Profile: 30.0 mm (X) x 14.0 mm (Y) cross-section with continuous
  bending flanges and stiffening transverse ribs to minimize weight while preventing
  sag, droop, and wind-induced flutter.
- Straight-Through 25.0 mm Phase Line Grooves: 2 x parallel 3.2 mm x 3.0 mm wire guide
  channels spaced at the exact 25.0 mm center-to-center pitch (X = -12.5 and +12.5 mm)
  on the front face, matching the Bay Brackets, Center Feed Hub, and Phase Crossovers
  with zero wire jogging or impedance discontinuity.
- Mid-Span Crossover Clip Zone: Central 20.0 mm recessed waist at Z = 35.0 to 65.0 mm
  allowing the Phase Crossover Spacer (`bt4v_phase_crossover.py`) to snap directly onto
  the spine segment.
- Modular Spine Interlock: Standardized male tenon (+Z, 12.0 x 8.0 x 10.0 mm) and female
  mortise (-Z, 12.0 x 8.0 x 10.0 mm) with 2.6 mm cross-pin locking holes.

Run headless:
    /snap/bin/freecad.cmd python/bt4v_spine_segment.py
or:
    freecadcmd python/bt4v_spine_segment.py
"""

import math
import os
import sys
import traceback

import FreeCAD as App
import Mesh
import Part

# --------------------------------------------------------------------------
# VERIFICATION BASELINES & TOLERANCES (Requirements.md §7.3, §16.3)
# --------------------------------------------------------------------------
EXPECT_EXTENTS = (30.0, 14.0, 110.0)  # mm: X, Y, Z extents (100 mm active + 10 mm tenon)
EXPECT_VOLUME = 21000.0  # mm^3: nominal volume
BBOX_TOL = 0.1  # mm: per-axis bounding-box extent tolerance
VOL_TOL = 0.02  # +/- fraction of expected volume (2%)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "stl", "BT4V_Spine_Segment.stl")

# --------------------------------------------------------------------------
# PARAMETERS (mm)
# --------------------------------------------------------------------------
# Outer body envelope
BODY_X = 30.0  # Width (X: -15.0 to +15.0) supporting 25.0 mm phase-line pitch
BODY_Y = 14.0  # Depth (Y: -7.0 to +7.0)
BODY_Z = 100.0  # Active body length between shoulders (Z: 0.0 to 100.0)

# Spine interlock joints (standardized across BT4-V spine components)
TENON_W = 12.0  # Male tenon width in X
TENON_D = 8.0  # Male tenon depth in Y
TENON_H = 10.0  # Male tenon height in Z (protrudes Z: 100.0 to 110.0)

MORTISE_W = 12.0  # Female mortise socket width in X
MORTISE_D = 8.0  # Female mortise socket depth in Y
MORTISE_H = 10.0  # Female mortise socket depth in Z (recess Z: 0.0 to 10.0)

PIN_D = 2.6  # Cross-pin hole diameter (2.5 mm pin / M2.5 screw clearance)
PIN_TOP_Z = 105.0  # Top cross-pin center Z (5.0 mm above shoulder Z = 100.0)
PIN_BOT_Z = 5.0  # Bottom cross-pin center Z (5.0 mm above bottom face Z = 0.0)

# Wire retention / phase line guide grooves on front face (Y = +7.0 mm)
WIRE_CH_W = 3.2  # Wire channel width (12 AWG solid copper wire clearance)
WIRE_CH_D = 3.0  # Wire channel depth into front face (from Y = 7.0 inwards)
WIRE_PITCH = 25.0  # Exact 25.0 mm center-to-center groove pitch (X = -12.5 and +12.5)

# Flanged I-beam side pockets and transverse stiffening ribs
POCKET_Y_H = 9.0
POCKET_Y_0 = -4.8

# 4 lightening bays bounded by transverse ribs along active strut (Z: 11.0 to 92.0 mm)
BAYS = [
    (11.0, 22.0),
    (36.0, 12.5),
    (51.5, 12.5),
    (67.0, 24.0),
]

WEB_THICK = 2.6  # Central I-beam web thickness in X


# --------------------------------------------------------------------------
# MODEL BUILDER
# --------------------------------------------------------------------------
def build_spine_segment():
    """Build the Spine Segment solid model conforming to BT4-V specifications."""
    # 1. Base body block (30.0 x 14.0 x 100.0 mm, Z: 0.0 to 100.0)
    base = Part.makeBox(BODY_X, BODY_Y, BODY_Z)
    base.translate(App.Vector(-BODY_X / 2.0, -BODY_Y / 2.0, 0.0))

    # 2. Male tenon joint at +Z end (12.0 x 8.0 x 10.0 mm, Z: 100.0 to 110.0)
    tenon = Part.makeBox(TENON_W, TENON_D, TENON_H)
    tenon.translate(App.Vector(-TENON_W / 2.0, -TENON_D / 2.0, BODY_Z))
    solid = base.fuse(tenon)

    cutters = []

    # 3. Female mortise socket at -Z end (12.0 x 8.0 x 10.0 mm, Z: 0.0 to 10.0)
    mortise = Part.makeBox(MORTISE_W, MORTISE_D, MORTISE_H)
    mortise.translate(App.Vector(-MORTISE_W / 2.0, -MORTISE_D / 2.0, 0.0))
    cutters.append(mortise)

    # 4. Standard 2.6 mm cross-pin locking holes through Y
    top_pin = Part.makeCylinder(
        PIN_D / 2.0, BODY_Y + 4.0, App.Vector(0.0, -BODY_Y / 2.0 - 2.0, PIN_TOP_Z), App.Vector(0.0, 1.0, 0.0)
    )
    cutters.append(top_pin)
    bot_pin = Part.makeCylinder(
        PIN_D / 2.0, BODY_Y + 4.0, App.Vector(0.0, -BODY_Y / 2.0 - 2.0, PIN_BOT_Z), App.Vector(0.0, 1.0, 0.0)
    )
    cutters.append(bot_pin)

    # 5. Wire retention / phase line guide grooves on front face (Y = +7.0 mm)
    # 3.2 mm wide x 3.0 mm deep parallel channels at 25.0 mm pitch along active length
    wire_y0 = BODY_Y / 2.0 - WIRE_CH_D
    wire_yd = WIRE_CH_D + 1.0
    wire_l = Part.makeBox(
        WIRE_CH_W,
        wire_yd,
        BODY_Z + 2.0,
        App.Vector(-WIRE_PITCH / 2.0 - WIRE_CH_W / 2.0, wire_y0, -1.0),
    )
    wire_r = Part.makeBox(
        WIRE_CH_W,
        wire_yd,
        BODY_Z + 2.0,
        App.Vector(WIRE_PITCH / 2.0 - WIRE_CH_W / 2.0, wire_y0, -1.0),
    )
    cutters.append(wire_l)
    cutters.append(wire_r)

    # 6. Mid-span crossover clip recess (Z: 35.0 to 65.0 mm): narrows X to 20.0 mm
    # so the Phase Crossover Spacer (20.0 mm spine recess) clips cleanly over the strut
    cutters.append(Part.makeBox(6.0, BODY_Y + 2.0, 30.0, App.Vector(-16.0, -BODY_Y / 2.0 - 1.0, 35.0)))
    cutters.append(Part.makeBox(6.0, BODY_Y + 2.0, 30.0, App.Vector(10.0, -BODY_Y / 2.0 - 1.0, 35.0)))

    # 7. Flanged I-beam side pockets with transverse stiffening ribs
    pocket_depth = (BODY_X - WEB_THICK) / 2.0
    for z0, zlen in BAYS:
        p_left = Part.makeBox(
            pocket_depth,
            POCKET_Y_H,
            zlen,
            App.Vector(-BODY_X / 2.0, POCKET_Y_0, z0),
        )
        cutters.append(p_left)
        p_right = Part.makeBox(
            pocket_depth,
            POCKET_Y_H,
            zlen,
            App.Vector(BODY_X / 2.0 - pocket_depth, POCKET_Y_0, z0),
        )
        cutters.append(p_right)

    # Apply all cuts
    for cutter in cutters:
        solid = solid.cut(cutter)

    return solid


# --------------------------------------------------------------------------
# STRUCTURAL VERIFICATION CONTRACT (Requirements.md §16.3)
# --------------------------------------------------------------------------
def verify_shape(shape, label, expected_extents, expected_volume, out_path):
    """Enforce one valid solid, bbox extents within BBOX_TOL, volume within
    VOL_TOL, and a single non-empty STL export via Mesh.export. Exits non-zero
    on any check failure; never reports failure as success."""
    failures = []
    shells = len(shape.Shells)
    solids = len(shape.Solids)
    valid = bool(shape.isValid())
    bb = shape.BoundBox
    extents = (bb.XMax - bb.XMin, bb.YMax - bb.YMin, bb.ZMax - bb.ZMin)
    bbox_ok = all(abs(e - x) <= BBOX_TOL for e, x in zip(extents, expected_extents))
    volume = shape.Volume
    vol_tol = abs(expected_volume) * VOL_TOL
    volume_ok = abs(volume - expected_volume) <= vol_tol

    if solids != 1:
        failures.append("solids == 1 (got %d)" % solids)
    if not valid:
        failures.append("isValid() == True")
    if not bbox_ok:
        failures.append(
            "bbox extents within +/-%.2f mm of %.1f x %.1f x %.1f "
            "(got %.3f x %.3f x %.3f)"
            % ((BBOX_TOL,) + tuple(expected_extents) + tuple(extents))
        )
    if not volume_ok:
        failures.append(
            "volume within +/-%.1f%% of %.1f mm^3 (got %.2f mm^3)"
            % (VOL_TOL * 100.0, expected_volume, volume)
        )

    exported = False
    file_ok = False
    file_size = 0
    if not failures:
        out_dir = os.path.dirname(out_path) or "."
        try:
            os.makedirs(out_dir, exist_ok=True)
        except OSError as exc:
            print(
                "ERROR: cannot create STL output directory %r: %r"
                % (out_dir, exc),
                file=sys.stderr,
                flush=True,
            )
            sys.exit(1)

        try:
            doc = App.newDocument(label)
            part_obj = doc.addObject("Part::Feature", label)
            part_obj.Shape = shape
            doc.recompute()
            Mesh.export([part_obj], out_path)
            exported = True
        except Exception as exc:
            try:
                shape.exportStl(out_path)
                exported = True
            except Exception as exc2:
                failures.append("STL export failed: %r / %r" % (exc, exc2))

        if exported:
            file_ok = os.path.isfile(out_path) and os.path.getsize(out_path) > 0
            if file_ok:
                file_size = os.path.getsize(out_path)
            else:
                failures.append("exported STL missing or empty: %s" % out_path)

    print("--- STRUCTURAL VERIFICATION: %s ---" % label, flush=True)
    print("  shells     : %d" % shells, flush=True)
    print("  solids     : %d" % solids, flush=True)
    print("  valid      : %s" % valid, flush=True)
    print(
        "  volume     : %.2f mm^3 (expected %.1f +/-%.1f%%)"
        % (volume, expected_volume, VOL_TOL * 100.0),
        flush=True,
    )
    print(
        "  bbox       : X %.3f..%.3f  Y %.3f..%.3f  Z %.3f..%.3f"
        % (bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax),
        flush=True,
    )
    print(
        "  extents    : %.3f x %.3f x %.3f mm (expected %.1f x %.1f x %.1f +/-%.2f mm)"
        % (tuple(extents) + tuple(expected_extents) + (BBOX_TOL,)),
        flush=True,
    )
    print("  [%s] solids == 1" % ("PASS" if solids == 1 else "FAIL"), flush=True)
    print("  [%s] isValid() == True" % ("PASS" if valid else "FAIL"), flush=True)
    print(
        "  [%s] bbox extents within +/-%.2f mm"
        % ("PASS" if bbox_ok else "FAIL", BBOX_TOL),
        flush=True,
    )
    print(
        "  [%s] volume within +/-%.1f%%"
        % ("PASS" if volume_ok else "FAIL", VOL_TOL * 100.0),
        flush=True,
    )
    if file_ok:
        print(
            "  [PASS] STL exported once, non-empty: %s (%d bytes)"
            % (out_path, file_size),
            flush=True,
        )
    elif exported:
        print(
            "  [FAIL] STL exported but missing/empty: %s" % out_path,
            flush=True,
        )
    else:
        print(
            "  [SKIP] STL export (structural checks failed)"
            if failures
            else "  [FAIL] STL export",
            flush=True,
        )

    if failures:
        print("  RESULT: FAIL", flush=True)
        raise RuntimeError(
            "%s structural verification failed: %s"
            % (label, "; ".join(failures))
        )
    print("  RESULT: PASS", flush=True)
    return True


# --------------------------------------------------------------------------
# CLI PARSER
# --------------------------------------------------------------------------
def parse_args():
    """Parse command line arguments and environment variables."""
    out_path = os.environ.get("OUT_PATH", DEFAULT_OUT)
    if any(arg in ("-h", "--help") for arg in sys.argv):
        print(__doc__, flush=True)
        sys.exit(0)
    for i, arg in enumerate(sys.argv):
        if arg.endswith("bt4v_spine_segment.py"):
            extra = [a for a in sys.argv[i + 1 :] if a not in ("--", "--pass")]
            for candidate in extra:
                if candidate.startswith("-"):
                    print(
                        "ERROR: Unrecognized or invalid parameter flag: %s" % candidate,
                        file=sys.stderr,
                        flush=True,
                    )
                    sys.exit(2)
            if extra:
                out_path = extra[0]
            break
    return out_path


# --------------------------------------------------------------------------
# ENTRY POINT
# --------------------------------------------------------------------------
def main():
    out_path = parse_args()
    shape = build_spine_segment()
    verify_shape(
        shape,
        "BT4V_Spine_Segment",
        EXPECT_EXTENTS,
        EXPECT_VOLUME,
        out_path,
    )
    print("BT4-V Spine Segment generator completed successfully.", flush=True)


# --------------------------------------------------------------------------
# EXECUTION CONTRACT
# --------------------------------------------------------------------------
try:
    main()
except Exception as exc:
    print("ERROR: BT4-V Spine Segment generation failed: %r" % (exc,), file=sys.stderr, flush=True)
    traceback.print_exc()
    sys.exit(1)

sys.exit(0)
