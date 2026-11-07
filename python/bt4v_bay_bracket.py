"""
BT4-V 3D Printed Antenna — Whisker Bay Bracket Generator (v0.1.0)

Generates the whisker mounting bracket used at each of the four bays
(Bays 1, 2, 3, and 4) along the modular vertical spine, exported as
'stl/BT4V_Bay_Bracket.stl'.

Technical Specifications:
- Requirements Baseline: Requirements.md §6, §16.3
- Plan Baseline: Plan.md §2.1, §3.1 (T1.1, T1.2)
- Body Dimensions / Extents: 50.0 mm (X) x 18.0 mm (Y) x 40.0 mm (Z) (tol +/-0.1 mm)
- Nominal Volume: 19,200 mm^3 (+/-2% -> acceptable range: 18,816 – 19,584 mm^3)
- Solid Count: Exactly 1 valid solid (len(shape.Solids) == 1, shape.isValid() == True)

Mechanical & RF Features:
- Dual Flare Guide: Supports both 32.5° (UHF Bays 2 & 3) and 25.5° (VHF Bays 1 & 4)
  whisker angles with rounded lead-in apex and 3.2 mm wide x 3.0 mm deep wire
  retention channels on +/-X sides.
- Apex Clamping: 2 x M4 clearance holes (4.3 mm) with 7.2 mm across flats (3.5 mm deep)
  rear hex nut pockets clamping whiskers directly against vertical phase lines.
- Phase Line Channels: Vertical guide channels (3.2 x 3.0 mm) spaced 25.0 mm apart
  on front face to seat phase lines against whisker apex.
- Spine Interlock: Symmetrical interlocking male tenon (+Z) and female mortise (-Z)
  connectors (12.0 mm wide x 8.0 mm deep x 10.0 mm height) with 2.6 mm cross-pin holes.

Run headless:
    /snap/bin/freecad.cmd -c python/bt4v_bay_bracket.py
or:
    freecadcmd -c python/bt4v_bay_bracket.py
"""

import math
import os
import sys
import traceback

import FreeCAD as App
import Mesh
import Part

# --------------------------------------------------------------------------
# VERIFICATION BASELINES & TOLERANCES (Requirements.md §6.3, §16.3; Plan.md §3.1)
# --------------------------------------------------------------------------
EXPECT_EXTENTS = (50.0, 18.0, 40.0)  # mm: X, Y, Z extents
EXPECT_VOLUME = 19200.0  # mm^3: nominal volume
BBOX_TOL = 0.1  # mm: per-axis bounding-box extent tolerance
VOL_TOL = 0.02  # +/- fraction of expected volume (2%)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "stl", "BT4V_Bay_Bracket.stl")

# --------------------------------------------------------------------------
# PARAMETERS (mm)
# --------------------------------------------------------------------------
# Outer body envelope
BODY_X = 50.0  # Total width (X: -25.0 to +25.0)
BODY_Y = 18.0  # Total depth (Y: -9.0 to +9.0)
BODY_Z = 30.0  # Main body height (Z: 0.0 to 30.0)

# Spine interlock joints
TENON_W = 12.0  # Male tenon width in X
TENON_D = 8.0  # Male tenon depth in Y
TENON_H = 10.0  # Male tenon height in Z (protrudes Z: 30.0 to 40.0)

MORTISE_W = 12.0  # Female mortise socket width in X
MORTISE_D = 8.0  # Female mortise socket depth in Y
MORTISE_H = 10.0  # Female mortise socket depth in Z (recess Z: 0.0 to 10.0)

PIN_D = 2.6  # Cross-pin hole diameter (2.5 mm pin / M2.5 screw clearance)
PIN_TOP_Z = 35.0  # Top cross-pin center Z (5.0 mm above shoulder Z = 30.0)
PIN_BOT_Z = 5.0  # Bottom cross-pin center Z (5.0 mm above bottom face Z = 0.0)

# Phase line channels and whisker apex clamping
TERM_PITCH = 25.0  # Center-to-center terminal spacing (X = -12.5, +12.5)
TERM_Z = 20.0  # Terminal post / whisker apex vertical center
M4_HOLE_D = 4.3  # M4 clearance hole diameter
HEX_AF = 7.2  # M4 hex nut pocket across flats (0.2 mm clearance)
HEX_DEPTH = 3.5  # M4 captured hex nut pocket depth
WIRE_CH_W = 3.2  # Phase line and whisker channel width (12 AWG clearance)
WIRE_CH_D = 3.0  # Phase line and whisker channel depth

# Whisker flare guide parameters
FLARE_UHF_DEG = 32.5  # UHF included flare angle (tip-to-tip)
FLARE_VHF_DEG = 25.5  # VHF included flare angle (tip-to-tip)
APEX_ROUND_R = 4.5  # Rounded lead-in radius at whisker apex

# Weight relief / calibration parameters
REAR_POCKET_W = 10.0  # Central rear lightening pocket width in X (X: -5.0 to +5.0)
REAR_POCKET_Z0 = 11.0  # Lower Z (above mortise ceiling at 10.0 mm)
REAR_POCKET_ZH = 14.0  # Height in Z (to Z = 25.0 mm)
REAR_POCKET_D = 2.139  # Depth of rear lightening pocket (calibrated for 19,200 mm^3)

# Support mounting slot parameters
SUPP_SLOT_W = 4.1  # Depth of support mounting slot in X
SUPP_SLOT_Y = 6.0  # Width of support mounting slot in Y
SUPP_SLOT_H = 8.0  # Height of support mounting slot in Z (Z: 16.0 to 24.0)


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


def make_angled_channel(apex_x, apex_z, sign_x, angle_deg, width, length, y_start, y_depth):
    """Create an angled channel cutter prism in X-Z plane extruded along Y."""
    theta = math.radians(angle_deg)
    u_x = sign_x * math.cos(abs(theta))
    u_z = math.sin(theta)

    # Normal vector rotated 90 degrees CCW in X-Z
    n_x = -u_z
    n_z = u_x
    hw = width / 2.0

    p1 = App.Vector(apex_x - hw * n_x, y_start, apex_z - hw * n_z)
    p2 = App.Vector(apex_x + hw * n_x, y_start, apex_z + hw * n_z)
    p3 = App.Vector(apex_x + length * u_x + hw * n_x, y_start, apex_z + length * u_z + hw * n_z)
    p4 = App.Vector(apex_x + length * u_x - hw * n_x, y_start, apex_z + length * u_z - hw * n_z)

    poly = Part.makePolygon([p1, p2, p3, p4, p1])
    face = Part.Face(poly)
    return face.extrude(App.Vector(0.0, y_depth, 0.0))


# --------------------------------------------------------------------------
# MODEL BUILDER
# --------------------------------------------------------------------------
def build_bay_bracket():
    """Build the Whisker Bay Bracket solid model conforming to BT4-V specifications."""
    # 1. Base body block (50.0 x 18.0 x 30.0 mm)
    base = Part.makeBox(BODY_X, BODY_Y, BODY_Z)
    base.translate(App.Vector(-BODY_X / 2.0, -BODY_Y / 2.0, 0.0))

    # 2. Male tenon joint at +Z end (12.0 x 8.0 x 10.0 mm, Z: 30.0 to 40.0)
    tenon = Part.makeBox(TENON_W, TENON_D, TENON_H)
    tenon.translate(App.Vector(-TENON_W / 2.0, -TENON_D / 2.0, BODY_Z))
    solid = base.fuse(tenon)

    cutters = []

    # 3. Female mortise socket at -Z end (12.0 x 8.0 x 10.0 mm, Z: 0.0 to 10.0)
    mortise = Part.makeBox(MORTISE_W, MORTISE_D, MORTISE_H)
    mortise.translate(App.Vector(-MORTISE_W / 2.0, -MORTISE_D / 2.0, 0.0))
    cutters.append(mortise)

    # 4. Standard 2.6 mm cross-pin locking holes through Y
    # Top pin through male tenon at Z = 35.0 mm
    top_pin = Part.makeCylinder(
        PIN_D / 2.0, BODY_Y + 4.0, App.Vector(0.0, -BODY_Y / 2.0 - 2.0, PIN_TOP_Z), App.Vector(0.0, 1.0, 0.0)
    )
    cutters.append(top_pin)
    # Bottom pin through female mortise at Z = 5.0 mm
    bot_pin = Part.makeCylinder(
        PIN_D / 2.0, BODY_Y + 4.0, App.Vector(0.0, -BODY_Y / 2.0 - 2.0, PIN_BOT_Z), App.Vector(0.0, 1.0, 0.0)
    )
    cutters.append(bot_pin)

    # 5. Vertical phase line channels on front face (Y = +9.0 mm)
    # 3.2 mm wide x 3.0 mm deep, spaced 25.0 mm apart (X = -12.5 and +12.5)
    wire_y0 = BODY_Y / 2.0 - WIRE_CH_D
    wire_yd = WIRE_CH_D + 1.0
    wire_l = Part.makeBox(
        WIRE_CH_W,
        wire_yd,
        BODY_Z + 2.0,
        App.Vector(-TERM_PITCH / 2.0 - WIRE_CH_W / 2.0, wire_y0, -1.0),
    )
    wire_r = Part.makeBox(
        WIRE_CH_W,
        wire_yd,
        BODY_Z + 2.0,
        App.Vector(TERM_PITCH / 2.0 - WIRE_CH_W / 2.0, wire_y0, -1.0),
    )
    cutters.append(wire_l)
    cutters.append(wire_r)

    # 6. M4 bolt clearance holes (4.3 mm dia) at whisker apex clamping posts (Z = 20.0 mm)
    m4_l = Part.makeCylinder(
        M4_HOLE_D / 2.0,
        BODY_Y + 4.0,
        App.Vector(-TERM_PITCH / 2.0, -BODY_Y / 2.0 - 2.0, TERM_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    m4_r = Part.makeCylinder(
        M4_HOLE_D / 2.0,
        BODY_Y + 4.0,
        App.Vector(TERM_PITCH / 2.0, -BODY_Y / 2.0 - 2.0, TERM_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    cutters.append(m4_l)
    cutters.append(m4_r)

    # 7. Captured hex nut pockets (7.2 mm across flats x 3.5 mm deep) on rear face (Y = -9.0 mm)
    hex_l = hex_prism(HEX_AF, HEX_DEPTH)
    hex_l.rotate(App.Vector(0.0, 0.0, 0.0), App.Vector(1.0, 0.0, 0.0), 90.0)
    hex_l.translate(App.Vector(-TERM_PITCH / 2.0, -BODY_Y / 2.0 + HEX_DEPTH, TERM_Z))

    hex_r = hex_prism(HEX_AF, HEX_DEPTH)
    hex_r.rotate(App.Vector(0.0, 0.0, 0.0), App.Vector(1.0, 0.0, 0.0), 90.0)
    hex_r.translate(App.Vector(TERM_PITCH / 2.0, -BODY_Y / 2.0 + HEX_DEPTH, TERM_Z))

    cutters.append(hex_l)
    cutters.append(hex_r)

    # 8. Whisker apex rounded lead-in pockets (radius APEX_ROUND_R, depth 3.0 mm)
    lead_in_l = Part.makeCylinder(
        APEX_ROUND_R,
        wire_yd,
        App.Vector(-TERM_PITCH / 2.0, wire_y0, TERM_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    lead_in_r = Part.makeCylinder(
        APEX_ROUND_R,
        wire_yd,
        App.Vector(TERM_PITCH / 2.0, wire_y0, TERM_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    cutters.append(lead_in_l)
    cutters.append(lead_in_r)

    # 9. Dual flare guide angled channels for UHF (32.5° / 2 = 16.25°) and VHF (25.5° / 2 = 12.75°)
    theta_uhf = FLARE_UHF_DEG / 2.0
    theta_vhf = FLARE_VHF_DEG / 2.0
    ch_len = 16.0  # Extends past outer body edge (from X = 12.5 to >25.0)

    # Left whisker (apex at X = -12.5, flaring towards -X)
    cutters.append(make_angled_channel(-TERM_PITCH / 2.0, TERM_Z, -1.0, theta_uhf, WIRE_CH_W, ch_len, wire_y0, wire_yd))
    cutters.append(make_angled_channel(-TERM_PITCH / 2.0, TERM_Z, -1.0, theta_vhf, WIRE_CH_W, ch_len, wire_y0, wire_yd))
    cutters.append(make_angled_channel(-TERM_PITCH / 2.0, TERM_Z, -1.0, -theta_vhf, WIRE_CH_W, ch_len, wire_y0, wire_yd))
    cutters.append(make_angled_channel(-TERM_PITCH / 2.0, TERM_Z, -1.0, -theta_uhf, WIRE_CH_W, ch_len, wire_y0, wire_yd))

    # Right whisker (apex at X = +12.5, flaring towards +X)
    cutters.append(make_angled_channel(TERM_PITCH / 2.0, TERM_Z, 1.0, theta_uhf, WIRE_CH_W, ch_len, wire_y0, wire_yd))
    cutters.append(make_angled_channel(TERM_PITCH / 2.0, TERM_Z, 1.0, theta_vhf, WIRE_CH_W, ch_len, wire_y0, wire_yd))
    cutters.append(make_angled_channel(TERM_PITCH / 2.0, TERM_Z, 1.0, -theta_vhf, WIRE_CH_W, ch_len, wire_y0, wire_yd))
    cutters.append(make_angled_channel(TERM_PITCH / 2.0, TERM_Z, 1.0, -theta_uhf, WIRE_CH_W, ch_len, wire_y0, wire_yd))

    # 10. Top shoulder transitions from 50 mm wing width to 20 mm central spine (Z: 26.0 to 30.0 mm)
    # Outside central spine (X < -10.0 and X > +10.0 mm)
    cutters.append(Part.makeBox(16.0, BODY_Y + 4.0, 5.0, App.Vector(-26.0, -BODY_Y / 2.0 - 2.0, 26.0)))
    cutters.append(Part.makeBox(16.0, BODY_Y + 4.0, 5.0, App.Vector(10.0, -BODY_Y / 2.0 - 2.0, 26.0)))

    # 11. Bottom shoulder transitions outside 20 mm central spine (Z: 0.0 to 6.0 mm)
    cutters.append(Part.makeBox(16.0, BODY_Y + 4.0, 7.0, App.Vector(-26.0, -BODY_Y / 2.0 - 2.0, -1.0)))
    cutters.append(Part.makeBox(16.0, BODY_Y + 4.0, 7.0, App.Vector(10.0, -BODY_Y / 2.0 - 2.0, -1.0)))

    # 12. Central rear lightening / I-beam pocket (Z: 11.0 to 25.0 mm)
    cutters.append(
        Part.makeBox(
            REAR_POCKET_W,
            REAR_POCKET_D,
            REAR_POCKET_ZH,
            App.Vector(-REAR_POCKET_W / 2.0, -BODY_Y / 2.0, REAR_POCKET_Z0),
        )
    )

    # 13. Support strut inner attachment mounting slots / pockets (Z: 16.0 to 24.0 mm)
    supp_slot_l = Part.makeBox(
        SUPP_SLOT_W,
        SUPP_SLOT_Y,
        SUPP_SLOT_H,
        App.Vector(-25.1, -SUPP_SLOT_Y / 2.0, TERM_Z - SUPP_SLOT_H / 2.0),
    )
    supp_slot_r = Part.makeBox(
        SUPP_SLOT_W,
        SUPP_SLOT_Y,
        SUPP_SLOT_H,
        App.Vector(BODY_X / 2.0 - SUPP_SLOT_W, -SUPP_SLOT_Y / 2.0, TERM_Z - SUPP_SLOT_H / 2.0),
    )
    cutters.append(supp_slot_l)
    cutters.append(supp_slot_r)

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
        if arg.endswith("bt4v_bay_bracket.py") and i + 1 < len(sys.argv):
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
    shape = build_bay_bracket()
    verify_shape(
        shape,
        "BT4V_Bay_Bracket",
        EXPECT_EXTENTS,
        EXPECT_VOLUME,
        out_path,
    )
    print("BT4-V Whisker Bay Bracket generator completed successfully.", flush=True)


# --------------------------------------------------------------------------
# EXECUTION CONTRACT
# --------------------------------------------------------------------------
try:
    main()
except Exception as exc:
    print("ERROR: BT4-V Whisker Bay Bracket generation failed: %r" % (exc,), file=sys.stderr, flush=True)
    traceback.print_exc()
    sys.exit(1)

sys.exit(0)
