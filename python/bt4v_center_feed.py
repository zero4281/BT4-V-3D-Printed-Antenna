"""
BT4-V 3D Printed Antenna — Center Feed Hub Generator (v0.1.0)

Generates the central structural and electrical hub located between Bay 2 and
Bay 3 of the modular vertical spine, exported as 'stl/BT4V_Center_Feed.stl'.

Technical Specifications:
- Requirements Baseline: Requirements.md §5, §16.3
- Plan Baseline: Plan.md §2.1, §2.2, §3.1 (T1.1, T1.2)
- Body Dimensions / Extents: 40.0 mm (X) x 24.0 mm (Y) x 70.0 mm (Z) (tol +/-0.1 mm)
- Target Volume: 28,500 mm^3 (+/-2% -> acceptable range: 27,930 – 29,070 mm^3)
- Solid Count: Exactly 1 valid solid (len(shape.Solids) == 1, shape.isValid() == True)

Mechanical & RF Features:
- Balun Cradle: Custom cavity contour cradling commercial RCA VH101R 4:1 matching
  transformer body with downward-facing F-connector coax exit.
- Coaxial Strain Relief: Integrated 4.0 x 2.0 mm zip-tie loop slot below balun cradle.
- Terminal Posts: 25.0 mm center-to-center terminal posts for phase-line feed connections.
- Hardware Ports: 2 x M4 bolt clearance holes (4.3 mm) with rear captured hex nut pockets
  (7.2 mm across flats x 3.5 mm deep).
- Wire Channels: 3.2 mm wide x 3.0 mm deep vertical wire routing channels for 12 AWG
  solid copper phase lines on the front face.
- Spine Joints: Standardized male tenon (+Z) and female mortise (-Z) interlocking interfaces
  with 2.6 mm cross-pin locking holes mating with bt4v_spine_segment.py.

Run headless:
    /snap/bin/freecad.cmd -c python/bt4v_center_feed.py
or:
    freecadcmd -c python/bt4v_center_feed.py
"""

import math
import os
import sys
import traceback

import FreeCAD as App
import Mesh
import Part

# --------------------------------------------------------------------------
# VERIFICATION BASELINES & TOLERANCES (Requirements.md §5.3, §16.3; Plan.md §2.2)
# --------------------------------------------------------------------------
EXPECT_EXTENTS = (40.0, 24.0, 70.0)  # mm: X, Y, Z extents
EXPECT_VOLUME = 28500.0  # mm^3: nominal volume
BBOX_TOL = 0.1  # mm: per-axis bounding-box extent tolerance
VOL_TOL = 0.02  # +/- fraction of expected volume (2%)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "stl", "BT4V_Center_Feed.stl")

# --------------------------------------------------------------------------
# PARAMETERS (mm)
# --------------------------------------------------------------------------
# Outer body envelope
BODY_X = 40.0  # Width (X: -20.0 to +20.0)
BODY_Y = 24.0  # Depth (Y: -12.0 to +12.0)
BODY_Z = 60.0  # Main body height (Z: 0.0 to 60.0)

# Spine interlock joints
TENON_W = 12.0  # Male tenon width in X
TENON_D = 8.0  # Male tenon depth in Y
TENON_H = 10.0  # Male tenon height in Z (protrudes Z: 60.0 to 70.0)

MORTISE_W = 12.0  # Female mortise socket width in X
MORTISE_D = 8.0  # Female mortise socket depth in Y
MORTISE_H = 10.0  # Female mortise socket depth in Z (recess Z: 0.0 to 10.0)

PIN_D = 2.6  # Cross-pin hole diameter (2.5 mm pin / M2.5 screw clearance)
PIN_TOP_Z = 65.0  # Top cross-pin center Z (5.0 mm above shoulder)
PIN_BOT_Z = 5.0  # Bottom cross-pin center Z (5.0 mm above bottom face)

# Phase line channels and terminal posts
TERM_PITCH = 25.0  # Center-to-center terminal spacing (X = -12.5, +12.5)
TERM_Z = 50.0  # Terminal post vertical center
M4_HOLE_D = 4.3  # M4 clearance hole diameter
HEX_AF = 7.2  # M4 hex nut pocket across flats (0.2 mm clearance)
HEX_DEPTH = 3.5  # M4 captured hex nut pocket depth
WIRE_CH_W = 3.2  # Phase line channel width (12 AWG clearance)
WIRE_CH_D = 3.0  # Phase line channel depth

# RCA VH101R balun cradle
BALUN_CRADLE_R = 9.0  # Balun body radius (18.0 mm diameter)
BALUN_CRADLE_Z0 = 18.0  # Balun body lower Z
BALUN_CRADLE_LEN = 28.0  # Balun body length in Z (to Z = 46.0)
BALUN_NECK_R = 6.0  # Balun F-connector neck radius (12.0 mm diameter)
BALUN_NECK_Z0 = 10.0  # Balun neck lower Z (to Z = 18.0)
BALUN_LEAD_Z0 = 46.0  # Balun spade lead breakout lower Z (to Z = 52.0)

# Coaxial strain relief
ZIPTIE_W = 4.0  # Zip-tie loop slot width in X
ZIPTIE_H = 2.0  # Zip-tie loop slot height in Z
ZIPTIE_Z = 13.0  # Zip-tie slot center Z (below balun cradle)

# Weight relief and profile shaping
SIDE_CUT_W = 3.5  # Lateral waist cutout width
REAR_POCKET_D = 6.305  # Rear lightening pocket depth (calibrated for 28,500 mm^3)


# --------------------------------------------------------------------------
# GEOMETRY HELPERS
# --------------------------------------------------------------------------
def hex_prism(across_flats, height):
    """Generate a regular hexagonal prism aligned along Z."""
    r = across_flats / math.sqrt(3.0)
    pts = []
    for i in range(6):
        angle = math.radians(60.0 * i + 30.0)
        pts.append(App.Vector(r * math.cos(angle), r * math.sin(angle), 0.0))
    pts.append(pts[0])
    face = Part.Face(Part.makePolygon(pts))
    return face.extrude(App.Vector(0.0, 0.0, height))


# --------------------------------------------------------------------------
# MODEL BUILDER
# --------------------------------------------------------------------------
def build_center_feed():
    """Build the Center Feed Hub solid model conforming to BT4-V specifications."""
    # 1. Base body block (40.0 x 24.0 x 60.0 mm)
    base = Part.makeBox(BODY_X, BODY_Y, BODY_Z)
    base.translate(App.Vector(-BODY_X / 2.0, -BODY_Y / 2.0, 0.0))

    # 2. Male tenon joint at +Z end (12.0 x 8.0 x 10.0 mm, Z: 60.0 to 70.0)
    tenon = Part.makeBox(TENON_W, TENON_D, TENON_H)
    tenon.translate(App.Vector(-TENON_W / 2.0, -TENON_D / 2.0, BODY_Z))
    solid = base.fuse(tenon)

    cutters = []

    # 3. Female mortise socket at -Z end (12.0 x 8.0 x 10.0 mm, Z: 0.0 to 10.0)
    mortise = Part.makeBox(MORTISE_W, MORTISE_D, MORTISE_H)
    mortise.translate(App.Vector(-MORTISE_W / 2.0, -MORTISE_D / 2.0, 0.0))
    cutters.append(mortise)

    # 4. Standard 2.6 mm cross-pin locking holes through Y
    # Top pin through male tenon at Z = 65.0 mm
    top_pin = Part.makeCylinder(
        PIN_D / 2.0, 26.0, App.Vector(0.0, -13.0, PIN_TOP_Z), App.Vector(0.0, 1.0, 0.0)
    )
    cutters.append(top_pin)
    # Bottom pin through female mortise at Z = 5.0 mm
    bot_pin = Part.makeCylinder(
        PIN_D / 2.0, 26.0, App.Vector(0.0, -13.0, PIN_BOT_Z), App.Vector(0.0, 1.0, 0.0)
    )
    cutters.append(bot_pin)

    # 5. Vertical wire routing channels on front face (Y = +12.0 mm)
    # 3.2 mm wide x 3.0 mm deep, spaced 25.0 mm apart (X = -12.5 and +12.5)
    wire_l = Part.makeBox(
        WIRE_CH_W,
        WIRE_CH_D + 1.0,
        BODY_Z + 2.0,
        App.Vector(-TERM_PITCH / 2.0 - WIRE_CH_W / 2.0, BODY_Y / 2.0 - WIRE_CH_D, -1.0),
    )
    wire_r = Part.makeBox(
        WIRE_CH_W,
        WIRE_CH_D + 1.0,
        BODY_Z + 2.0,
        App.Vector(TERM_PITCH / 2.0 - WIRE_CH_W / 2.0, BODY_Y / 2.0 - WIRE_CH_D, -1.0),
    )
    cutters.append(wire_l)
    cutters.append(wire_r)

    # 6. M4 bolt clearance holes (4.3 mm dia) at terminal posts (Z = 50.0 mm)
    m4_l = Part.makeCylinder(
        M4_HOLE_D / 2.0,
        BODY_Y + 2.0,
        App.Vector(-TERM_PITCH / 2.0, -BODY_Y / 2.0 - 1.0, TERM_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    m4_r = Part.makeCylinder(
        M4_HOLE_D / 2.0,
        BODY_Y + 2.0,
        App.Vector(TERM_PITCH / 2.0, -BODY_Y / 2.0 - 1.0, TERM_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    cutters.append(m4_l)
    cutters.append(m4_r)

    # 7. Captured hex nut pockets (7.2 mm across flats x 3.5 mm deep) on rear face (Y = -12.0 mm)
    hex_l = hex_prism(HEX_AF, HEX_DEPTH)
    hex_l.rotate(App.Vector(0.0, 0.0, 0.0), App.Vector(1.0, 0.0, 0.0), 90.0)
    hex_l.translate(App.Vector(-TERM_PITCH / 2.0, -BODY_Y / 2.0 + HEX_DEPTH, TERM_Z))

    hex_r = hex_prism(HEX_AF, HEX_DEPTH)
    hex_r.rotate(App.Vector(0.0, 0.0, 0.0), App.Vector(1.0, 0.0, 0.0), 90.0)
    hex_r.translate(App.Vector(TERM_PITCH / 2.0, -BODY_Y / 2.0 + HEX_DEPTH, TERM_Z))

    cutters.append(hex_l)
    cutters.append(hex_r)

    # 8. RCA VH101R balun cradle cavity (18.0 mm diameter cylinder + front opening)
    cradle_cyl = Part.makeCylinder(
        BALUN_CRADLE_R,
        BALUN_CRADLE_LEN,
        App.Vector(0.0, 3.0, BALUN_CRADLE_Z0),
        App.Vector(0.0, 0.0, 1.0),
    )
    cradle_open = Part.makeBox(
        BALUN_CRADLE_R * 2.0,
        10.0,
        BALUN_CRADLE_LEN,
        App.Vector(-BALUN_CRADLE_R, 3.0, BALUN_CRADLE_Z0),
    )
    cutters.append(cradle_cyl.fuse(cradle_open))

    # 9. Balun F-connector neck / exit channel (12.0 mm diameter cylinder + front opening)
    neck_cyl = Part.makeCylinder(
        BALUN_NECK_R,
        8.0,
        App.Vector(0.0, 3.0, BALUN_NECK_Z0),
        App.Vector(0.0, 0.0, 1.0),
    )
    neck_open = Part.makeBox(
        BALUN_NECK_R * 2.0,
        10.0,
        8.0,
        App.Vector(-BALUN_NECK_R, 3.0, BALUN_NECK_Z0),
    )
    cutters.append(neck_cyl.fuse(neck_open))

    # 10. Balun lead breakout pocket (Z: 46.0 to 52.0 mm)
    cutters.append(
        Part.makeBox(
            28.0,
            8.0,
            6.0,
            App.Vector(-14.0, 4.0, BALUN_LEAD_Z0),
        )
    )

    # 11. Coaxial strain relief slot (4.0 x 2.0 mm zip-tie loop slot below balun cradle)
    cutters.append(
        Part.makeBox(
            ZIPTIE_W,
            BODY_Y + 2.0,
            ZIPTIE_H,
            App.Vector(-ZIPTIE_W / 2.0, -BODY_Y / 2.0 - 1.0, ZIPTIE_Z),
        )
    )

    # 12. Top shoulder transitions from 40 mm wing width to 20 mm spine strut (Z: 55.0 to 60.0 mm)
    cutters.append(Part.makeBox(10.0, BODY_Y + 2.0, 6.0, App.Vector(-20.0, -BODY_Y / 2.0 - 1.0, 55.0)))
    cutters.append(Part.makeBox(10.0, BODY_Y + 2.0, 6.0, App.Vector(10.0, -BODY_Y / 2.0 - 1.0, 55.0)))

    # 13. Bottom shoulder transitions outside the 20 mm spine interface (Z: 0.0 to 8.0 mm)
    cutters.append(Part.makeBox(10.0, BODY_Y + 2.0, 8.0, App.Vector(-20.0, -BODY_Y / 2.0 - 1.0, 0.0)))
    cutters.append(Part.makeBox(10.0, BODY_Y + 2.0, 8.0, App.Vector(10.0, -BODY_Y / 2.0 - 1.0, 0.0)))

    # 14. Side waist cutouts (between Z = 8.0 and 42.0 mm)
    cutters.append(Part.makeBox(SIDE_CUT_W, BODY_Y + 2.0, 34.0, App.Vector(-20.0, -BODY_Y / 2.0 - 1.0, 8.0)))
    cutters.append(Part.makeBox(SIDE_CUT_W, BODY_Y + 2.0, 34.0, App.Vector(20.0 - SIDE_CUT_W, -BODY_Y / 2.0 - 1.0, 8.0)))

    # 15. Rear lightening pockets flanking the central spine (Z: 8.0 to 42.0 mm)
    cutters.append(Part.makeBox(10.0, REAR_POCKET_D, 34.0, App.Vector(-17.5, -BODY_Y / 2.0, 8.0)))
    cutters.append(Part.makeBox(10.0, REAR_POCKET_D, 34.0, App.Vector(7.5, -BODY_Y / 2.0, 8.0)))

    # 16. Central rear I-beam channel (Z: 16.0 to 44.0 mm)
    cutters.append(Part.makeBox(10.0, 3.0, 28.0, App.Vector(-5.0, -BODY_Y / 2.0, 16.0)))

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
        if arg.endswith("bt4v_center_feed.py") and i + 1 < len(sys.argv):
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
    shape = build_center_feed()
    verify_shape(
        shape,
        "BT4V_Center_Feed",
        EXPECT_EXTENTS,
        EXPECT_VOLUME,
        out_path,
    )
    print("BT4-V Center Feed Hub generator completed successfully.", flush=True)


# --------------------------------------------------------------------------
# EXECUTION CONTRACT
# --------------------------------------------------------------------------
try:
    main()
except Exception as exc:
    print("ERROR: BT4-V Center Feed Hub generation failed: %r" % (exc,), file=sys.stderr, flush=True)
    traceback.print_exc()
    sys.exit(1)

sys.exit(0)

