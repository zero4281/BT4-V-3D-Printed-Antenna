"""
BT4-V 3D Printed Antenna — Spine Segment Generator (v0.3.0)

Generates the modular vertical spine strut that spaces adjacent bay brackets
at the exact 130 mm pitch along the modular vertical spine, exported as
'stl/BT4V_Spine_Segment.stl'.

Technical Specifications:
- Requirements Baseline: Requirements.md §7, §16.3
- Plan Baseline: Plan.md §2.1, §2.2, §3.1 (T1.1, T1.2)
- Body Dimensions / Extents: 20.0 mm (X) x 14.0 mm (Y) x 120.0 mm (Z) (tol +/-0.1 mm)
  * Active length: 110.0 mm between shoulder stops (+ 10.0 mm tenon = 120.0 mm total Z)
- Nominal Volume: 16,800 mm^3 (+/-2% -> acceptable range: 16,464 – 17,136 mm^3)
- Solid Count: Exactly 1 valid solid (len(shape.Solids) == 1, shape.isValid() == True)

Mechanical & RF Features:
- Flanged I-Beam Profile: 20.0 mm (X) x 14.0 mm (Y) cross-section with 2.5 mm front and rear
  continuous bending flanges and stiffening transverse ribs to minimize weight while preventing
  sag, droop, and wind-induced flutter.
- Wire Retention / Guide Grooves: 2 x parallel 3.2 mm wire guide channels spaced across front face
  for 12 AWG solid copper phase lines, recessed to provide clean seating for clip-on crossover spacers.
- Modular Spine Interlock: Standardized male tenon (+Z, 12.0 x 8.0 x 10.0 mm) and female mortise
  (-Z, 12.0 x 8.0 x 10.0 mm) with 2.6 mm cross-pin locking holes mating with Center Feed, Bay Brackets,
  and Hanging Cap.

Run headless:
    /snap/bin/freecad.cmd -c python/bt4v_spine_segment.py
or:
    freecadcmd -c python/bt4v_spine_segment.py
"""

import math
import os
import sys
import traceback

import FreeCAD as App
import Mesh
import Part

# --------------------------------------------------------------------------
# VERIFICATION BASELINES & TOLERANCES (Requirements.md §7.3, §16.3; Plan.md §3.1)
# --------------------------------------------------------------------------
EXPECT_EXTENTS = (20.0, 14.0, 120.0)  # mm: X, Y, Z extents
EXPECT_VOLUME = 16800.0  # mm^3: nominal volume
BBOX_TOL = 0.1  # mm: per-axis bounding-box extent tolerance
VOL_TOL = 0.02  # +/- fraction of expected volume (2%)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "stl", "BT4V_Spine_Segment.stl")

# --------------------------------------------------------------------------
# PARAMETERS (mm)
# --------------------------------------------------------------------------
# Outer body envelope
BODY_X = 20.0  # Width (X: -10.0 to +10.0)
BODY_Y = 14.0  # Depth (Y: -7.0 to +7.0)
BODY_Z = 110.0  # Active body length between shoulders (Z: 0.0 to 110.0)

# Spine interlock joints (standardized across BT4-V spine components)
TENON_W = 12.0  # Male tenon width in X
TENON_D = 8.0  # Male tenon depth in Y
TENON_H = 10.0  # Male tenon height in Z (protrudes Z: 110.0 to 120.0)

MORTISE_W = 12.0  # Female mortise socket width in X
MORTISE_D = 8.0  # Female mortise socket depth in Y
MORTISE_H = 10.0  # Female mortise socket depth in Z (recess Z: 0.0 to 10.0)

PIN_D = 2.6  # Cross-pin hole diameter (2.5 mm pin / M2.5 screw clearance)
PIN_TOP_Z = 115.0  # Top cross-pin center Z (5.0 mm above shoulder Z = 110.0)
PIN_BOT_Z = 5.0  # Bottom cross-pin center Z (5.0 mm above bottom face Z = 0.0)

# Wire retention / phase line guide grooves on front face (Y = +7.0 mm)
WIRE_CH_W = 3.2  # Wire channel width (12 AWG solid copper wire clearance)
WIRE_CH_D = 2.2  # Wire channel depth into front face (from Y = 7.0 inwards)
WIRE_PITCH = 12.0  # Center-to-center groove pitch (grooves centered at X = -6.0 and +6.0)

# Flanged I-beam side pockets and transverse stiffening ribs
# Front flange thickness: 2.5 mm (Y: +4.5 to +7.0 mm)
# Rear flange thickness: 2.5 mm (Y: -7.0 to -4.5 mm)
# Pocket height along Y: 9.0 mm (Y: -4.5 to +4.5 mm)
POCKET_Y_H = 9.0
POCKET_Y_0 = -POCKET_Y_H / 2.0

# 4 lightening bays bounded by transverse ribs along active strut (Z: 12.0 to 100.0 mm):
# - Solid collar over mortise: Z = 0.0 to 12.0 mm
# - Bay 1: Z = 12.0 to 32.0 mm (length 20.0 mm)
# - Rib 1: Z = 32.0 to 35.0 mm (thickness 3.0 mm)
# - Bay 2: Z = 35.0 to 53.0 mm (length 18.0 mm)
# - Rib 2 (mid-strut crossover snap zone): Z = 53.0 to 57.0 mm (thickness 4.0 mm)
# - Bay 3: Z = 57.0 to 77.0 mm (length 20.0 mm)
# - Rib 3: Z = 77.0 to 80.0 mm (thickness 3.0 mm)
# - Bay 4: Z = 80.0 to 100.0 mm (length 20.0 mm)
# - Solid shoulder supporting tenon: Z = 100.0 to 110.0 mm
BAYS = [
    (12.0, 20.0),
    (35.0, 18.0),
    (57.0, 20.0),
    (80.0, 20.0),
]

# Calibrated central web thickness to meet exact 16,800.0 mm^3 volume target
WEB_THICK = 2.369131  # Central I-beam web thickness in X


# --------------------------------------------------------------------------
# MODEL BUILDER
# --------------------------------------------------------------------------
def build_spine_segment():
    """Build the Spine Segment solid model conforming to BT4-V specifications."""
    # 1. Base body block (20.0 x 14.0 x 110.0 mm, Z: 0.0 to 110.0)
    base = Part.makeBox(BODY_X, BODY_Y, BODY_Z)
    base.translate(App.Vector(-BODY_X / 2.0, -BODY_Y / 2.0, 0.0))

    # 2. Male tenon joint at +Z end (12.0 x 8.0 x 10.0 mm, Z: 110.0 to 120.0)
    tenon = Part.makeBox(TENON_W, TENON_D, TENON_H)
    tenon.translate(App.Vector(-TENON_W / 2.0, -TENON_D / 2.0, BODY_Z))
    solid = base.fuse(tenon)

    cutters = []

    # 3. Female mortise socket at -Z end (12.0 x 8.0 x 10.0 mm, Z: 0.0 to 10.0)
    mortise = Part.makeBox(MORTISE_W, MORTISE_D, MORTISE_H)
    mortise.translate(App.Vector(-MORTISE_W / 2.0, -MORTISE_D / 2.0, 0.0))
    cutters.append(mortise)

    # 4. Standard 2.6 mm cross-pin locking holes through Y
    # Top pin through male tenon at Z = 115.0 mm
    top_pin = Part.makeCylinder(
        PIN_D / 2.0, BODY_Y + 4.0, App.Vector(0.0, -BODY_Y / 2.0 - 2.0, PIN_TOP_Z), App.Vector(0.0, 1.0, 0.0)
    )
    cutters.append(top_pin)
    # Bottom pin through female mortise at Z = 5.0 mm
    bot_pin = Part.makeCylinder(
        PIN_D / 2.0, BODY_Y + 4.0, App.Vector(0.0, -BODY_Y / 2.0 - 2.0, PIN_BOT_Z), App.Vector(0.0, 1.0, 0.0)
    )
    cutters.append(bot_pin)

    # 5. Wire retention / phase line guide grooves on front face (Y = +7.0 mm)
    # 3.2 mm wide x 2.2 mm deep parallel channels along the active body length (Z: 0.0 to 110.0 mm)
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

    # 6. Flanged I-beam side pockets with transverse stiffening ribs
    pocket_depth = (BODY_X - WEB_THICK) / 2.0
    for z0, zlen in BAYS:
        # Left pocket (-X side)
        p_left = Part.makeBox(
            pocket_depth,
            POCKET_Y_H,
            zlen,
            App.Vector(-BODY_X / 2.0, POCKET_Y_0, z0),
        )
        cutters.append(p_left)
        # Right pocket (+X side)
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
# STRUCTURAL VERIFICATION CONTRACT (Plan.md §3.1, §4; Requirements.md §16.3)
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
    for i, arg in enumerate(sys.argv):
        if arg in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        if arg.endswith("bt4v_spine_segment.py") and i + 1 < len(sys.argv):
            candidate = sys.argv[i + 1]
            if candidate.startswith("-"):
                print(
                    "ERROR: Unrecognized or invalid parameter flag: %s" % candidate,
                    file=sys.stderr,
                    flush=True,
                )
                sys.exit(2)
            out_path = candidate
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
