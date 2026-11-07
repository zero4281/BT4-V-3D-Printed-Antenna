"""
BT4-V 3D Printed Antenna — Mid-Span Bowtie Support Strut Generator (v0.2.0)

Generates the rigid mid-span support strut bridging between the central bay bracket
and intermediate points along the bowtie whisker arms, exported as 'stl/BT4V_Bowtie_Support.stl'.
Quantity required: 8 (2 per bay across Bays 1–4).

Technical Specifications:
- Requirements Baseline: Requirements.md §10, §16.3
- Plan Baseline: Plan.md §2.1, §2.2, §3.1 (T1.1, T1.2)
- Body Dimensions / Extents: 65.0 mm (X) x 10.0 mm (Y) x 8.0 mm (Z) (tol +/-0.1 mm)
- Nominal Volume: 1,800 mm^3 (+/-2% -> acceptable range: 1,764 – 1,836 mm^3)
- Solid Count: Exactly 1 valid solid (len(shape.Solids) == 1, shape.isValid() == True)

Mechanical & RF Features:
- Purpose: Eliminates manual positioning difficulty during assembly, locks bowtie arms
  at exact flare angles (32.5° UHF, 25.5° VHF), and prevents mechanical drift, sagging, or vibration.
- Mounting Ends: Inner end locks securely into the bay bracket support pocket; outer end
  features a snap-fit C-clip jaw (2.2 mm mouth into 3.2 mm circular cavity) gripping the
  12 AWG whisker at mid-span (~100 mm for UHF, ~200 mm for VHF).
- Strut Profile: 6.0 mm x 3.0 mm ribbed truss profile for maximum rigidity at minimum mass (~2.5 g each).

Run headless:
    /snap/bin/freecad.cmd -c python/bt4v_bowtie_support.py
or:
    freecadcmd -c python/bt4v_bowtie_support.py
"""

import math
import os
import sys
import traceback

import FreeCAD as App
import Mesh
import Part

# --------------------------------------------------------------------------
# VERIFICATION BASELINES & TOLERANCES (Requirements.md §10.3, §16.3; Plan.md §3.1)
# --------------------------------------------------------------------------
EXPECT_EXTENTS = (65.0, 10.0, 8.0)  # mm: X, Y, Z extents
EXPECT_VOLUME = 1800.0  # mm^3: nominal volume
BBOX_TOL = 0.1  # mm: per-axis bounding-box extent tolerance
VOL_TOL = 0.02  # +/- fraction of expected volume (2%)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "stl", "BT4V_Bowtie_Support.stl")

# --------------------------------------------------------------------------
# PARAMETERS (mm)
# --------------------------------------------------------------------------
# Outer body envelope
BODY_X = 65.0  # Total length (X: -32.5 to +32.5)
BODY_Y = 10.0  # Body depth (Y: -5.0 to +5.0)
BODY_Z = 8.0  # Body height (Z: 0.0 to 8.0)

# Outer end (snap-fit C-clip jaw for 12 AWG wire at mid-span)
JAW_CENTER_X = 29.5
WIRE_CAV_D = 3.2  # Circular wire retention cavity diameter (12 AWG clearance)
SNAP_MOUTH_W = 2.2  # Snap mouth opening width in X
LEAD_IN_W = 3.6  # Lead-in flare at mouth entry (Z: 6.8 to 8.0 mm)

# Ribbed truss strut parameters (central active span)
STRUT_Z_MIN = 1.5  # Lower Z boundary of central strut
STRUT_Z_MAX = 6.5  # Upper Z boundary of central strut (5.0 mm height)
FLANGE_Y = 6.0  # Outer flange width in Y (-3.0 to +3.0 mm)
WEB_Y = 3.0  # Central web thickness in Y (-1.5 to +1.5 mm)

POCKET_Z_MIN = 2.8  # Web pocket lower Z
POCKET_Z_MAX = 5.2  # Web pocket upper Z

# Lightening windows through central web
WIN_X_W = 5.5  # Window length in X
WIN_Y_W = 3.2  # Window width in Y

# Calibrated pocket depth to achieve exact 1,800 mm^3 volume
CAL_POCKET_D = 1.4  # Pocket depth into web faces
CAL_END_POCKET_D = 2.4  # Weight relief depth at inner/outer solid ends


# --------------------------------------------------------------------------
# GEOMETRY HELPERS
# --------------------------------------------------------------------------
def make_chamfer(cx, cy0, cy_len, z0, z1, w0, w1):
    """Create a flared entry chamfer cutter prism in X-Z plane extruded along Y."""
    p1 = App.Vector(cx - w1 / 2.0, cy0, z1)
    p2 = App.Vector(cx - w0 / 2.0, cy0, z0)
    p3 = App.Vector(cx + w0 / 2.0, cy0, z0)
    p4 = App.Vector(cx + w1 / 2.0, cy0, z1)
    poly = Part.makePolygon([p1, p2, p3, p4, p1])
    face = Part.Face(poly)
    return face.extrude(App.Vector(0.0, cy_len, 0.0))


def make_z_cutout_top():
    """Create top Z contour cutter prism tapering from ends down to central strut."""
    p1 = App.Vector(-26.0, -BODY_Y / 2.0 - 2.0, BODY_Z + 1.0)
    p2 = App.Vector(-26.0, -BODY_Y / 2.0 - 2.0, BODY_Z)
    p3 = App.Vector(-20.0, -BODY_Y / 2.0 - 2.0, STRUT_Z_MAX)
    p4 = App.Vector(22.0, -BODY_Y / 2.0 - 2.0, STRUT_Z_MAX)
    p5 = App.Vector(26.0, -BODY_Y / 2.0 - 2.0, BODY_Z)
    p6 = App.Vector(26.0, -BODY_Y / 2.0 - 2.0, BODY_Z + 1.0)
    poly = Part.makePolygon([p1, p2, p3, p4, p5, p6, p1])
    face = Part.Face(poly)
    return face.extrude(App.Vector(0.0, BODY_Y + 4.0, 0.0))


def make_z_cutout_bot():
    """Create bottom Z contour cutter prism tapering from ends up to central strut."""
    p1 = App.Vector(-26.0, -BODY_Y / 2.0 - 2.0, -1.0)
    p2 = App.Vector(-26.0, -BODY_Y / 2.0 - 2.0, 0.0)
    p3 = App.Vector(-20.0, -BODY_Y / 2.0 - 2.0, STRUT_Z_MIN)
    p4 = App.Vector(22.0, -BODY_Y / 2.0 - 2.0, STRUT_Z_MIN)
    p5 = App.Vector(26.0, -BODY_Y / 2.0 - 2.0, 0.0)
    p6 = App.Vector(26.0, -BODY_Y / 2.0 - 2.0, -1.0)
    poly = Part.makePolygon([p1, p2, p3, p4, p5, p6, p1])
    face = Part.Face(poly)
    return face.extrude(App.Vector(0.0, BODY_Y + 4.0, 0.0))


def make_y_cutout_front():
    """Create front Y waist contour cutter prism."""
    half_f = FLANGE_Y / 2.0
    p1 = App.Vector(-26.0, BODY_Y / 2.0 + 1.0, -2.0)
    p2 = App.Vector(-26.0, BODY_Y / 2.0, -2.0)
    p3 = App.Vector(-20.0, half_f, -2.0)
    p4 = App.Vector(22.0, half_f, -2.0)
    p5 = App.Vector(26.0, BODY_Y / 2.0, -2.0)
    p6 = App.Vector(26.0, BODY_Y / 2.0 + 1.0, -2.0)
    poly = Part.makePolygon([p1, p2, p3, p4, p5, p6, p1])
    face = Part.Face(poly)
    return face.extrude(App.Vector(0.0, 0.0, BODY_Z + 4.0))


def make_y_cutout_rear():
    """Create rear Y waist contour cutter prism."""
    half_f = FLANGE_Y / 2.0
    p1 = App.Vector(-26.0, -BODY_Y / 2.0 - 1.0, -2.0)
    p2 = App.Vector(-26.0, -BODY_Y / 2.0, -2.0)
    p3 = App.Vector(-20.0, -half_f, -2.0)
    p4 = App.Vector(22.0, -half_f, -2.0)
    p5 = App.Vector(26.0, -BODY_Y / 2.0, -2.0)
    p6 = App.Vector(26.0, -BODY_Y / 2.0 - 1.0, -2.0)
    poly = Part.makePolygon([p1, p2, p3, p4, p5, p6, p1])
    face = Part.Face(poly)
    return face.extrude(App.Vector(0.0, 0.0, BODY_Z + 4.0))


# --------------------------------------------------------------------------
# MODEL BUILDER
# --------------------------------------------------------------------------
def build_bowtie_support():
    """Build the Mid-Span Bowtie Support Strut solid model conforming to BT4-V specifications."""
    # 1. Base body envelope block (65.0 x 10.0 x 8.0 mm, centered on X and Y, Z: 0.0 to 8.0)
    base = Part.makeBox(
        BODY_X,
        BODY_Y,
        BODY_Z,
        App.Vector(-BODY_X / 2.0, -BODY_Y / 2.0, 0.0),
    )

    cutters = []

    # 2. Wire retention cylindrical cavity (3.2 mm dia) at outer jaw (X = +29.5 mm)
    cav_outer = Part.makeCylinder(
        WIRE_CAV_D / 2.0,
        BODY_Y + 4.0,
        App.Vector(JAW_CENTER_X, -BODY_Y / 2.0 - 2.0, BODY_Z / 2.0),
        App.Vector(0.0, 1.0, 0.0),
    )
    cutters.append(cav_outer)

    # 3. Snap mouth slot (2.2 mm wide in X extending from outer edge to cavity)
    mouth_outer = Part.makeBox(
        SNAP_MOUTH_W + 4.0,
        BODY_Y + 4.0,
        BODY_Z / 2.0 + 2.0,
        App.Vector(
            BODY_X / 2.0 - SNAP_MOUTH_W - 4.0,
            -BODY_Y / 2.0 - 2.0,
            BODY_Z / 2.0,
        ),
    )
    cutters.append(mouth_outer)

    # 4. Lead-in chamfer entry funnel at top face of outer jaw
    chamfer_outer = make_chamfer(
        JAW_CENTER_X,
        -BODY_Y / 2.0 - 2.0,
        BODY_Y + 4.0,
        6.8,
        8.5,
        SNAP_MOUTH_W,
        LEAD_IN_W,
    )
    cutters.append(chamfer_outer)

    # 5. Top and bottom strut profile cutouts in Z
    cutters.append(make_z_cutout_top())
    cutters.append(make_z_cutout_bot())

    # 6. Side waist profile cutouts in Y
    cutters.append(make_y_cutout_front())
    cutters.append(make_y_cutout_rear())

    # 7. Ribbed I-beam side pockets on front (+Y) and rear (-Y) faces
    pocket_x_spans = [
        (-20.0, -14.0),
        (-12.0, -6.0),
        (-4.0, 2.0),
        (4.0, 10.0),
        (12.0, 18.0),
    ]
    pocket_zh = POCKET_Z_MAX - POCKET_Z_MIN

    for x0, x1 in pocket_x_spans:
        xw = x1 - x0
        p_front = Part.makeBox(
            xw,
            CAL_POCKET_D,
            pocket_zh,
            App.Vector(x0, WEB_Y / 2.0, POCKET_Z_MIN),
        )
        p_rear = Part.makeBox(
            xw,
            CAL_POCKET_D,
            pocket_zh,
            App.Vector(x0, -WEB_Y / 2.0 - CAL_POCKET_D, POCKET_Z_MIN),
        )
        cutters.append(p_front)
        cutters.append(p_rear)

    # 8. Vertical lightening windows through the central web
    win_x_centers = [-17.0, -9.0, -1.0, 7.0, 15.0]
    for cx in win_x_centers:
        win = Part.makeBox(
            WIN_X_W,
            WIN_Y_W,
            BODY_Z + 2.0,
            App.Vector(cx - WIN_X_W / 2.0, -WIN_Y_W / 2.0, -1.0),
        )
        cutters.append(win)

    # 9. Weight relief pockets at inner and outer ends
    p_end_il_f = Part.makeBox(
        4.0,
        CAL_END_POCKET_D,
        4.0,
        App.Vector(-31.0, BODY_Y / 2.0 - CAL_END_POCKET_D, 2.0),
    )
    p_end_il_r = Part.makeBox(
        4.0,
        CAL_END_POCKET_D,
        4.0,
        App.Vector(-31.0, -BODY_Y / 2.0, 2.0),
    )
    p_end_ol_f = Part.makeBox(
        4.0,
        CAL_END_POCKET_D,
        4.0,
        App.Vector(25.0, BODY_Y / 2.0 - CAL_END_POCKET_D, 2.0),
    )
    p_end_ol_r = Part.makeBox(
        4.0,
        CAL_END_POCKET_D,
        4.0,
        App.Vector(25.0, -BODY_Y / 2.0, 2.0),
    )
    cutters.extend([p_end_il_f, p_end_il_r, p_end_ol_f, p_end_ol_r])

    # Apply all cuts sequentially to ensure valid single solid
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
        if arg.endswith("bt4v_bowtie_support.py") and i + 1 < len(sys.argv):
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
    shape = build_bowtie_support()
    verify_shape(
        shape,
        "BT4V_Bowtie_Support",
        EXPECT_EXTENTS,
        EXPECT_VOLUME,
        out_path,
    )
    print("BT4-V Mid-Span Bowtie Support Strut generator completed successfully.", flush=True)


# --------------------------------------------------------------------------
# EXECUTION CONTRACT
# --------------------------------------------------------------------------
try:
    main()
except Exception as exc:
    print("ERROR: BT4-V Mid-Span Bowtie Support Strut generation failed: %r" % (exc,), file=sys.stderr, flush=True)
    traceback.print_exc()
    sys.exit(1)
