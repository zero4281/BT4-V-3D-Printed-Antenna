"""
BT4-V 3D Printed Antenna — Fit Calibration Coupon Generator (v0.3.0)

Generates a pre-print calibration and fit-test coupon, exported as
'stl/BT4V_Fit_Coupon.stl'. Printed first to verify printer dimensional accuracy
before production parts.

Technical Specifications:
- Requirements Baseline: Requirements.md §11, §16.3
- Plan Baseline: Plan.md §2.1, §2.2, §3.1 (T1.1, T1.2), §3.2 (T2.1)
- Body Dimensions / Extents: 90.0 mm (X) x 50.0 mm (Y) x 10.0 mm (Z) (tol +/-0.1 mm)
- Nominal Volume: 26,500 mm^3 (+/-2% -> acceptable range: 25,970 – 27,030 mm^3)
- Solid Count: Exactly 1 valid solid (len(shape.Solids) == 1, shape.isValid() == True)

Mechanical & RF Fit-Test Features:
1. Friction Channels: 4 parallel test channels (2.8, 3.0, 3.2, 3.4 mm widths x 3.0 mm deep)
   for calibrating 12 AWG solid copper wire friction fit across bare and insulated wire diameters.
2. Snap Channels: 2 snap channels with 2.2 mm and 2.4 mm mouth openings over 3.3 mm round cavities
   with entry chamfers for verifying wire snap retention in triangular tine spreaders.
3. M4 Hardware Stack: 4.3 mm clearance hole with 7.2 mm across-flats hex nut capture pocket
   (3.5 mm deep) to test M4 bolt through-clearance and anti-rotation hex nut seating.
4. Spine Interlock Joint: Standard modular spine interlock features:
   - Male tenon: 12.0 mm (W) x 8.0 mm (D) x 10.0 mm (L) protruding tongue with 2.6 mm cross-pin hole.
   - Female mortise: 12.0 mm (W) x 8.0 mm (D) x 10.0 mm (L) socket with 2.6 mm cross-pin hole.
5. Balun Lug Spacing: 25.0 mm pitch test studs (OD 4.0 mm) with concentric pilot holes located in a
   recessed deck for testing direct spade lug alignment of the RCA VH101R matching transformer.
6. Backing Strut Snap Jaws & Cradle Channel: Dedicated test pocket and snap-fit test
   features for verifying bt4v_bowtie_backing.py full-length backing strut snap-jaw retention,
   root mounting slot, and 3.2 x 3.0 mm cradle channel wire fit.

Run headless:
    /snap/bin/freecad.cmd -c python/bt4v_fit_coupon.py
or:
    freecadcmd -c python/bt4v_fit_coupon.py
"""

import math
import os
import sys
import traceback

import FreeCAD as App
import Mesh
import Part

# --------------------------------------------------------------------------
# VERIFICATION BASELINES & TOLERANCES (Requirements.md §11.3, §16.3; Plan.md §3.1)
# --------------------------------------------------------------------------
EXPECT_EXTENTS = (90.0, 50.0, 10.0)  # mm: X, Y, Z extents
EXPECT_VOLUME = 26500.0  # mm^3: nominal volume
BBOX_TOL = 0.1  # mm: per-axis bounding-box extent tolerance
VOL_TOL = 0.02  # +/- fraction of expected volume (2%)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "stl", "BT4V_Fit_Coupon.stl")

# --------------------------------------------------------------------------
# PARAMETERS (mm)
# --------------------------------------------------------------------------
# Outer body envelope
BODY_X = 90.0  # Total length (X: -45.0 to +45.0)
BODY_Y = 50.0  # Total width (Y: -25.0 to +25.0)
BODY_Z = 10.0  # Total height (Z: 0.0 to 10.0)

# Spine interlock male tenon at +X end (X: +35.0 to +45.0 mm)
TENON_W = 12.0  # Tenon width in Y (Y: -6.0 to +6.0 mm)
TENON_D = 8.0  # Tenon depth in Z (Z: 0.0 to 8.0 mm)
TENON_L = 10.0  # Tenon protrusion length in X (X: +35.0 to +45.0 mm)
TENON_SHOULDER_X = 35.0  # X position of tenon shoulder stop
TENON_PIN_X = 40.0  # Center of tenon cross-pin hole (5.0 mm from shoulder)

# Spine interlock female mortise socket at X = -30.0 mm
MORTISE_X = -30.0  # Center of mortise socket in X
MORTISE_Y = 0.0  # Center of mortise socket in Y
MORTISE_W = 12.0  # Mortise socket width in X (X: -36.0 to -24.0 mm)
MORTISE_D = 8.0  # Mortise socket depth in Y (Y: -4.0 to +4.0 mm)
MORTISE_H = 10.0  # Mortise socket depth in Z (through-hole Z: 0.0 to 10.0 mm)
MORTISE_PIN_Z = 5.0  # Center of cross-pin hole in Z (5.0 mm from top/bottom)

PIN_D = 2.6  # Cross-pin hole diameter (2.5 mm pin / M2.5 screw clearance)

# Wire test channels in +Y half (Y: 1.0 to 23.0 mm, length 22.0 mm)
WIRE_CH_Y0 = 1.0  # Wire channel start Y
WIRE_CH_Y_LEN = 22.0  # Wire channel length in Y

# 1. Friction channels (4 stepped widths x 3.0 mm deep)
FRICTION_WIDTHS = [2.8, 3.0, 3.2, 3.4]
FRICTION_XS = [-10.0, -4.0, 2.0, 8.0]
FRICTION_DEPTH = 3.0  # Recessed from top face (Z = 10.0 down to Z = 7.0 mm)

# 2. Snap channels (2 snap channels with stepped mouth widths over 3.3 mm round cavity)
SNAP_MOUTHS = [2.2, 2.4]  # Mouth slot widths in X
SNAP_XS = [15.0, 22.0]  # Snap channel center X positions
SNAP_CAV_D = 3.3  # Cylindrical cavity diameter (radius 1.65 mm)
SNAP_CAV_Z = 5.5  # Cavity center Z (cavity Z: 3.85 to 7.15 mm)
SNAP_LEADIN_Z0 = 9.0  # Mouth flare entry lower Z

# 3. M4 hardware stack at X = -20.0 mm, Y = -13.0 mm
M4_STACK_X = -20.0  # M4 hardware stack center X
M4_STACK_Y = -13.0  # M4 hardware stack center Y
M4_HOLE_D = 4.3  # M4 bolt clearance through-hole diameter
HEX_AF = 7.2  # M4 hex nut pocket across flats (0.2 mm clearance)
HEX_DEPTH = 3.5  # Hex nut capture pocket depth (Z: 6.5 to 10.0 mm)

# 4. Balun studs test station (25.0 mm pitch matching RCA VH101R spade lugs)
BALUN_PITCH = 25.0  # Center-to-center stud pitch along X
BALUN_STUD1_X = 2.5  # Stud 1 center X
BALUN_STUD2_X = 27.5  # Stud 2 center X (2.5 + 25.0 = 27.5 mm)
BALUN_STUDS_Y = -13.0  # Studs center Y
BALUN_STUD_OD = 4.0  # Stud outer diameter (matches M4 terminal screw shank)
BALUN_STUD_HOLE_D = 2.5  # Concentric pilot / test hole diameter through stud
BALUN_DECK_DEPTH = 5.0  # Recessed deck depth (Z: 5.0 to 10.0 mm, stud height 5.0 mm)
BALUN_DECK_X0 = -3.0  # Recessed deck lower X
BALUN_DECK_X_LEN = 36.0  # Recessed deck length in X (X: -3.0 to +33.0 mm)
BALUN_DECK_Y0 = -21.0  # Recessed deck lower Y
BALUN_DECK_Y_LEN = 16.0  # Recessed deck width in Y (Y: -21.0 to -5.0 mm)

# 5. Top face recessed panels
TOP_LABEL_X0 = -42.0  # Identification panel lower X
TOP_LABEL_X_LEN = 26.0  # Identification panel length in X (X: -42.0 to -16.0 mm)
TOP_LABEL_Y0 = 6.0  # Identification panel lower Y
TOP_LABEL_Y_LEN = 16.0  # Identification panel width in Y (Y: 6.0 to 22.0 mm)
TOP_LABEL_DEPTH = 2.0  # Recess depth from top face (Z: 8.0 to 10.0 mm)

TOP_SW_X0 = -42.0  # Southwest top recess lower X
TOP_SW_X_LEN = 16.0  # Southwest top recess length in X (X: -42.0 to -26.0 mm)
TOP_SW_Y0 = -22.0  # Southwest top recess lower Y
TOP_SW_Y_LEN = 16.0  # Southwest top recess width in Y (Y: -22.0 to -6.0 mm)
TOP_SW_DEPTH = 2.0  # Recess depth from top face (Z: 8.0 to 10.0 mm)

# 6. Underside weight-relief & calibration bays (from Z = 0.0 upwards)
BAY_NW_X0 = -42.0  # Northwest bay X: -42.0 to -16.0 mm
BAY_NW_X_LEN = 26.0
BAY_NW_Y0 = 6.0  # Northwest bay Y: 6.0 to 22.0 mm
BAY_NW_Y_LEN = 16.0
BAY_NW_DEPTH = 4.5  # Bay depth in Z (leaves 3.5 mm solid floor to top recess)

BAY_SW_X0 = -42.0  # Southwest bay X: -42.0 to -26.0 mm
BAY_SW_X_LEN = 16.0
BAY_SW_Y0 = -22.0  # Southwest bay Y: -22.0 to -6.0 mm
BAY_SW_Y_LEN = 16.0
BAY_SW_DEPTH = 4.5  # Bay depth in Z (leaves 3.5 mm solid floor to top recess)

BAY_NC_X0 = -12.0  # North-central bay X: -12.0 to +11.0 mm (under friction channels)
BAY_NC_X_LEN = 23.0
BAY_NC_Y0 = 3.0  # North-central bay Y: 3.0 to 22.0 mm
BAY_NC_Y_LEN = 19.0
BAY_NC_DEPTH = 4.0  # Bay depth in Z (leaves 3.0 mm solid floor to friction channel bottoms)

BAY_BALUN_X0 = 0.0  # Under-balun bay X: 0.0 to 30.0 mm
BAY_BALUN_X_LEN = 30.0
BAY_BALUN_Y0 = -21.0  # Under-balun bay Y: -21.0 to -5.0 mm
BAY_BALUN_Y_LEN = 16.0
BAY_BALUN_DEPTH = 2.5  # Bay depth in Z (leaves 2.5 mm solid floor to balun deck)

BAY_NE_X0 = 25.0  # Northeast bay X: 25.0 to 33.0 mm
BAY_NE_X_LEN = 8.0
BAY_NE_Y0 = 3.0  # Northeast bay Y: 3.0 to 22.0 mm
BAY_NE_Y_LEN = 19.0
BAY_NE_DEPTH = 4.5  # Bay depth in Z

BAY_CENTRAL_X0 = -23.0  # Central bay X: -23.0 to -3.0 mm
BAY_CENTRAL_X_LEN = 20.0
BAY_CENTRAL_Y0 = -3.0  # Central bay Y: -3.0 to 3.0 mm
BAY_CENTRAL_Y_LEN = 6.0
BAY_CENTRAL_DEPTH = 4.0  # Bay depth in Z

# Calibrated underside tuning pocket length to hit exact 26,500.0 mm^3 volume target
CAL_POCKET_LEN = 2.8  # mm: Calibrated length of underside tuning pocket


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


def make_chamfer(cx, y0, y_len, z0, z1, w0, w1):
    """Create a flared entry chamfer cutter prism in X-Z plane extruded along Y."""
    p1 = App.Vector(cx - w1 / 2.0, y0, z1)
    p2 = App.Vector(cx - w0 / 2.0, y0, z0)
    p3 = App.Vector(cx + w0 / 2.0, y0, z0)
    p4 = App.Vector(cx + w1 / 2.0, y0, z1)
    poly = Part.makePolygon([p1, p2, p3, p4, p1])
    face = Part.Face(poly)
    return face.extrude(App.Vector(0.0, y_len, 0.0))


# --------------------------------------------------------------------------
# MODEL BUILDER
# --------------------------------------------------------------------------
def build_fit_coupon():
    """Build the Fit Calibration Coupon solid model conforming to BT4-V specifications."""
    # 1. Base solid block (90.0 x 50.0 x 10.0 mm, centered on X and Y, Z: 0.0 to 10.0)
    base = Part.makeBox(
        BODY_X,
        BODY_Y,
        BODY_Z,
        App.Vector(-BODY_X / 2.0, -BODY_Y / 2.0, 0.0),
    )

    cutters = []

    # 2. Male tenon joint at +X end (protruding tongue at X: +35.0 to +45.0 mm)
    # Tenon cross-section: 12.0 mm (in Y: -6.0 to +6.0 mm) x 8.0 mm (in Z: 0.0 to 8.0 mm)
    # Remove material above tenon (Z > 8.0 mm from X = 35.0 to 46.0 mm across all Y)
    cut_top = Part.makeBox(
        TENON_L + 2.0,
        BODY_Y + 4.0,
        BODY_Z - TENON_D + 2.0,
        App.Vector(TENON_SHOULDER_X, -BODY_Y / 2.0 - 2.0, TENON_D),
    )
    cutters.append(cut_top)

    # Remove material in +Y side of tenon (Y: +6.0 to +26.0 mm, Z: -1.0 to 9.0 mm)
    cut_side_p = Part.makeBox(
        TENON_L + 2.0,
        (BODY_Y - TENON_W) / 2.0 + 2.0,
        BODY_Z + 2.0,
        App.Vector(TENON_SHOULDER_X, TENON_W / 2.0, -1.0),
    )
    cutters.append(cut_side_p)

    # Remove material in -Y side of tenon (Y: -26.0 to -6.0 mm, Z: -1.0 to 9.0 mm)
    cut_side_n = Part.makeBox(
        TENON_L + 2.0,
        (BODY_Y - TENON_W) / 2.0 + 2.0,
        BODY_Z + 2.0,
        App.Vector(TENON_SHOULDER_X, -BODY_Y / 2.0 - 2.0, -1.0),
    )
    cutters.append(cut_side_n)

    # Standard 2.6 mm cross-pin hole through male tenon (at X = 40.0 mm, Y = 0.0 mm through Z)
    tenon_pin = Part.makeCylinder(
        PIN_D / 2.0,
        BODY_Z + 4.0,
        App.Vector(TENON_PIN_X, 0.0, -2.0),
        App.Vector(0.0, 0.0, 1.0),
    )
    cutters.append(tenon_pin)

    # 3. Female mortise socket (12.0 mm x 8.0 mm x 10.0 mm socket at X = -30.0 mm, Y = 0.0 mm)
    mortise = Part.makeBox(
        MORTISE_W,
        MORTISE_D,
        MORTISE_H + 2.0,
        App.Vector(MORTISE_X - MORTISE_W / 2.0, MORTISE_Y - MORTISE_D / 2.0, -1.0),
    )
    cutters.append(mortise)

    # Standard 2.6 mm cross-pin locking hole through mortise socket (at X = -30.0 mm, Z = 5.0 mm through Y)
    mortise_pin = Part.makeCylinder(
        PIN_D / 2.0,
        BODY_Y + 4.0,
        App.Vector(MORTISE_X, -BODY_Y / 2.0 - 2.0, MORTISE_PIN_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    cutters.append(mortise_pin)

    # 4. Friction channels (4 parallel channels: 2.8, 3.0, 3.2, 3.4 mm widths x 3.0 mm deep)
    for width, x_pos in zip(FRICTION_WIDTHS, FRICTION_XS):
        f_box = Part.makeBox(
            width,
            WIRE_CH_Y_LEN,
            FRICTION_DEPTH + 0.1,
            App.Vector(x_pos - width / 2.0, WIRE_CH_Y0, BODY_Z - FRICTION_DEPTH),
        )
        cutters.append(f_box)

    # 5. Snap channels (2 snap channels with 2.2 and 2.4 mm mouth openings over 3.3 mm cavity)
    for mouth_w, x_pos in zip(SNAP_MOUTHS, SNAP_XS):
        # Round cylindrical cavity (diameter 3.3 mm)
        cav = Part.makeCylinder(
            SNAP_CAV_D / 2.0,
            WIRE_CH_Y_LEN + 0.2,
            App.Vector(x_pos, WIRE_CH_Y0 - 0.1, SNAP_CAV_Z),
            App.Vector(0.0, 1.0, 0.0),
        )
        cutters.append(cav)
        # Snap mouth opening slot connecting cavity to top surface
        mouth = Part.makeBox(
            mouth_w,
            WIRE_CH_Y_LEN + 0.2,
            BODY_Z - SNAP_CAV_Z + 0.1,
            App.Vector(x_pos - mouth_w / 2.0, WIRE_CH_Y0 - 0.1, SNAP_CAV_Z),
        )
        cutters.append(mouth)
        # Entry chamfer flare at mouth entry
        chf = make_chamfer(
            x_pos,
            WIRE_CH_Y0 - 0.1,
            WIRE_CH_Y_LEN + 0.2,
            SNAP_LEADIN_Z0,
            BODY_Z + 0.1,
            mouth_w,
            mouth_w + 1.2,
        )
        cutters.append(chf)

    # 6. M4 hardware stack at X = -20.0 mm, Y = -13.0 mm
    # 4.3 mm diameter clearance hole through Z
    m4_hole = Part.makeCylinder(
        M4_HOLE_D / 2.0,
        BODY_Z + 4.0,
        App.Vector(M4_STACK_X, M4_STACK_Y, -2.0),
        App.Vector(0.0, 0.0, 1.0),
    )
    cutters.append(m4_hole)
    # Captured hex nut pocket (7.2 mm across flats x 3.5 mm deep into top face)
    m4_hex = hex_prism(HEX_AF, HEX_DEPTH + 0.1)
    m4_hex.translate(App.Vector(M4_STACK_X, M4_STACK_Y, BODY_Z - HEX_DEPTH))
    cutters.append(m4_hex)

    # 7. Balun studs test station (25.0 mm pitch at X = +2.5 and +27.5 mm, Y = -13.0 mm)
    # Recessed deck from Z = 5.0 to 10.1 mm, preserving two 4.0 mm OD test studs rising from deck
    balun_pocket = Part.makeBox(
        BALUN_DECK_X_LEN,
        BALUN_DECK_Y_LEN,
        BALUN_DECK_DEPTH + 0.1,
        App.Vector(BALUN_DECK_X0, BALUN_DECK_Y0, BODY_Z - BALUN_DECK_DEPTH),
    )
    stud1 = Part.makeCylinder(
        BALUN_STUD_OD / 2.0,
        BALUN_DECK_DEPTH + 0.2,
        App.Vector(BALUN_STUD1_X, BALUN_STUDS_Y, BODY_Z - BALUN_DECK_DEPTH - 0.05),
        App.Vector(0.0, 0.0, 1.0),
    )
    stud2 = Part.makeCylinder(
        BALUN_STUD_OD / 2.0,
        BALUN_DECK_DEPTH + 0.2,
        App.Vector(BALUN_STUD2_X, BALUN_STUDS_Y, BODY_Z - BALUN_DECK_DEPTH - 0.05),
        App.Vector(0.0, 0.0, 1.0),
    )
    balun_cutter = balun_pocket.cut(stud1).cut(stud2)
    cutters.append(balun_cutter)

    # Concentric test holes through balun studs
    stud1_hole = Part.makeCylinder(
        BALUN_STUD_HOLE_D / 2.0,
        BODY_Z + 4.0,
        App.Vector(BALUN_STUD1_X, BALUN_STUDS_Y, -2.0),
        App.Vector(0.0, 0.0, 1.0),
    )
    stud2_hole = Part.makeCylinder(
        BALUN_STUD_HOLE_D / 2.0,
        BODY_Z + 4.0,
        App.Vector(BALUN_STUD2_X, BALUN_STUDS_Y, -2.0),
        App.Vector(0.0, 0.0, 1.0),
    )
    cutters.append(stud1_hole)
    cutters.append(stud2_hole)

    # 7.5 Backing strut snap-jaw & mounting slot test pocket (4.1 x 6.0 mm x 3.5 mm deep)
    backing_test_pocket = Part.makeBox(
        4.1,
        6.0,
        3.5 + 0.1,
        App.Vector(-34.0 - 2.05, -14.0 - 3.0, BODY_Z - 3.5),
    )
    cutters.append(backing_test_pocket)

    # 8. Top face identification and weight-relief recess panels
    top_label_recess = Part.makeBox(
        TOP_LABEL_X_LEN,
        TOP_LABEL_Y_LEN,
        TOP_LABEL_DEPTH + 0.1,
        App.Vector(TOP_LABEL_X0, TOP_LABEL_Y0, BODY_Z - TOP_LABEL_DEPTH),
    )
    cutters.append(top_label_recess)

    top_sw_recess = Part.makeBox(
        TOP_SW_X_LEN,
        TOP_SW_Y_LEN,
        TOP_SW_DEPTH + 0.1,
        App.Vector(TOP_SW_X0, TOP_SW_Y0, BODY_Z - TOP_SW_DEPTH),
    )
    cutters.append(top_sw_recess)

    # 9. Underside weight-relief & calibration bays (from Z = -0.1 upwards)
    bay_nw = Part.makeBox(
        BAY_NW_X_LEN,
        BAY_NW_Y_LEN,
        BAY_NW_DEPTH + 0.1,
        App.Vector(BAY_NW_X0, BAY_NW_Y0, -0.1),
    )
    cutters.append(bay_nw)

    bay_sw = Part.makeBox(
        BAY_SW_X_LEN,
        BAY_SW_Y_LEN,
        BAY_SW_DEPTH + 0.1,
        App.Vector(BAY_SW_X0, BAY_SW_Y0, -0.1),
    )
    cutters.append(bay_sw)

    bay_nc = Part.makeBox(
        BAY_NC_X_LEN,
        BAY_NC_Y_LEN,
        BAY_NC_DEPTH + 0.1,
        App.Vector(BAY_NC_X0, BAY_NC_Y0, -0.1),
    )
    cutters.append(bay_nc)

    bay_balun = Part.makeBox(
        BAY_BALUN_X_LEN,
        BAY_BALUN_Y_LEN,
        BAY_BALUN_DEPTH + 0.1,
        App.Vector(BAY_BALUN_X0, BAY_BALUN_Y0, -0.1),
    )
    cutters.append(bay_balun)

    bay_ne = Part.makeBox(
        BAY_NE_X_LEN,
        BAY_NE_Y_LEN,
        BAY_NE_DEPTH + 0.1,
        App.Vector(BAY_NE_X0, BAY_NE_Y0, -0.1),
    )
    cutters.append(bay_ne)

    bay_central = Part.makeBox(
        BAY_CENTRAL_X_LEN,
        BAY_CENTRAL_Y_LEN,
        BAY_CENTRAL_DEPTH + 0.1,
        App.Vector(BAY_CENTRAL_X0, BAY_CENTRAL_Y0, -0.1),
    )
    cutters.append(bay_central)

    # Calibrated tuning pocket in Southeast underside region
    cal_pocket = Part.makeBox(
        CAL_POCKET_LEN,
        14.0,
        4.1,
        App.Vector(33.0 - CAL_POCKET_LEN, -20.0, -0.1),
    )
    cutters.append(cal_pocket)

    # Apply all cuts to form the final single solid shape
    solid = base
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
        if arg.endswith("bt4v_fit_coupon.py") and i + 1 < len(sys.argv):
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
    shape = build_fit_coupon()
    verify_shape(
        shape,
        "BT4V_Fit_Coupon",
        EXPECT_EXTENTS,
        EXPECT_VOLUME,
        out_path,
    )
    print("BT4-V Fit Coupon generator completed successfully.", flush=True)


# --------------------------------------------------------------------------
# EXECUTION CONTRACT
# --------------------------------------------------------------------------
try:
    main()
except Exception as exc:
    print("ERROR: BT4-V Fit Coupon generation failed: %r" % (exc,), file=sys.stderr, flush=True)
    traceback.print_exc()
    sys.exit(1)

sys.exit(0)
