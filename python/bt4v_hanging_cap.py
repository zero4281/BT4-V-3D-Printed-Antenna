"""
BT4-V 3D Printed Antenna — Top Hanging Cap Generator (v0.3.0)

Generates the top termination cap locking onto the top tenon of Whisker Bay 1,
exported as 'stl/BT4V_Hanging_Cap.stl'. Quantity required: 1.

Technical Specifications:
- Requirements Baseline: Requirements.md §10, §16.3
- Plan Baseline: Plan.md §2.1, §2.2, §3.1 (T1.1, T1.2)
- Body Dimensions / Extents: 44.0 mm (X) x 18.0 mm (Y) x 30.0 mm (Z) (tol +/-0.1 mm)
- Nominal Volume: 7,400 mm^3 (+/-2% -> acceptable range: 7,252 – 7,548 mm^3)
- Solid Count: Exactly 1 valid solid (len(shape.Solids) == 1, shape.isValid() == True)

Mechanical & RF Features:
- Anti-Rotation Dual Suspension: 2 x Ø5.0 mm eyelets spaced 30.0 mm apart along
  the X axis (centered at X = -15.0 mm and X = +15.0 mm, Z = 23.0 mm) with 4.5 mm
  radial wall reinforcement, preventing antenna twisting when hung against a window
  using suction cups, picture wire, or nylon hanging cord.
- Spine Interlock Female Mortise: 12.0 mm wide x 8.0 mm deep x 10.0 mm high mortise
  socket at bottom (-Z end, Z: 0.0 to 10.0 mm) mating securely with the top tenon of
  Whisker Bay 1 bracket.
- Cross-Pin Locking Port: Transverse 2.6 mm through-hole along Y at Z = 5.0 mm
  aligning with the Bay 1 tenon cross-pin hole for a 2.5 mm locking pin or M2.5 screw.
- Structural Transition: Smooth 45° chamfers flaring from the 20.0 mm base shoulder
  out to the 44.0 mm eyelet span in X, and tapering from 18.0 mm spine depth at the
  base to the calibrated upper yoke thickness in Y.
- Central Saddle Arch: Cylindrical concave arch (radius 12.0 mm) between eyelets
  providing clearance for suspension cords and hook hardware.

Run headless:
    /snap/bin/freecad.cmd -c python/bt4v_hanging_cap.py
or:
    freecadcmd -c python/bt4v_hanging_cap.py
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
EXPECT_EXTENTS = (44.0, 18.0, 30.0)  # mm: X, Y, Z extents
EXPECT_VOLUME = 7400.0  # mm^3: nominal volume
BBOX_TOL = 0.1  # mm: per-axis bounding-box extent tolerance
VOL_TOL = 0.02  # +/- fraction of expected volume (2%)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "stl", "BT4V_Hanging_Cap.stl")

# --------------------------------------------------------------------------
# PARAMETERS (mm)
# --------------------------------------------------------------------------
# Outer body envelope
BODY_X = 44.0  # Total width across eyelets (X: -22.0 to +22.0)
BODY_Y = 18.0  # Base depth matching Bay 1 bracket (Y: -9.0 to +9.0)
BODY_Z = 30.0  # Total height from base to top of eyelets (Z: 0.0 to 30.0)

# Spine interlock female mortise joint (mating to Bay 1 top tenon)
MORTISE_W = 12.0  # Mortise socket width in X (X: -6.0 to +6.0)
MORTISE_D = 8.0  # Mortise socket depth in Y (Y: -4.0 to +4.0)
MORTISE_H = 10.0  # Mortise socket depth in Z (Z: 0.0 to 10.0)

PIN_D = 2.6  # Cross-pin hole diameter (2.5 mm pin / M2.5 screw clearance)
PIN_Z = 5.0  # Cross-pin center Z (5.0 mm above base Z = 0.0)

# Dual suspension eyelets (30.0 mm pitch along X)
EYE_PITCH = 30.0  # Center-to-center eyelet spacing along X
EYE_X = EYE_PITCH / 2.0  # Eyelet center X: +/-15.0 mm
EYE_HOLE_D = 5.0  # Eyelet through-hole diameter (along Y)
EYE_OUTER_R = 7.0  # Eyelet outer cylinder radius (X: +/-22.0 mm, Z: 30.0 mm)
EYE_Z = 23.0  # Eyelet center Z (23.0 + 7.0 = 30.0 mm top)

# Central top saddle arch between eyelets
SADDLE_R = 12.0  # Central saddle cutout cylinder radius
SADDLE_Z = 30.0  # Saddle cylinder center Z (dips down to Z = 18.0 mm)

# Lower side shoulder transitions (flaring from 20 mm central spine out to 44 mm eyelets)
BASE_X = 20.0  # Central base width matching Bay 1 shoulder (X: -10.0 to +10.0)
SIDE_CHAMFER_Z0 = 4.0  # Start of 45° chamfer at |X| = 10.0 mm
SIDE_CHAMFER_Z1 = 16.0  # End of 45° chamfer at |X| = 22.0 mm

# Front and rear Y-chamfer shoulder transitions (from 18 mm base to upper yoke)
Y_CHAMFER_Z0 = 8.0  # Lower Z boundary of Y-chamfer
Y_CHAMFER_H = 4.0  # Height of 45° Y-chamfer (reaches upper yoke at Z = 12.0 mm)

# Calibrated upper yoke / eyelet arm depth in Y to meet exact 7,400.0 mm^3 volume target
ARM_Y = 7.241315  # Yoke thickness in Y (calibrated for 7,400.0 mm^3 solid volume)


# --------------------------------------------------------------------------
# MODEL BUILDER
# --------------------------------------------------------------------------
def build_hanging_cap():
    """Build the Top Hanging Cap solid model conforming to BT4-V specifications."""
    # 1. Base bounding box block (44.0 x 18.0 x 30.0 mm)
    base = Part.makeBox(BODY_X, BODY_Y, BODY_Z)
    base.translate(App.Vector(-BODY_X / 2.0, -BODY_Y / 2.0, 0.0))
    solid = base

    cutters = []

    # 2. Female mortise socket at bottom (-Z end, Z: 0.0 to 10.0 mm)
    mortise = Part.makeBox(MORTISE_W, MORTISE_D, MORTISE_H)
    mortise.translate(App.Vector(-MORTISE_W / 2.0, -MORTISE_D / 2.0, 0.0))
    cutters.append(mortise)

    # 3. Standard 2.6 mm cross-pin locking hole through Y at Z = 5.0 mm
    pin = Part.makeCylinder(
        PIN_D / 2.0,
        BODY_Y + 4.0,
        App.Vector(0.0, -BODY_Y / 2.0 - 2.0, PIN_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    cutters.append(pin)

    # 4. Dual suspension eyelet through-holes (Ø5.0 mm along Y at X = +/-15.0 mm, Z = 23.0 mm)
    eye_l = Part.makeCylinder(
        EYE_HOLE_D / 2.0,
        BODY_Y + 4.0,
        App.Vector(-EYE_X, -BODY_Y / 2.0 - 2.0, EYE_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    eye_r = Part.makeCylinder(
        EYE_HOLE_D / 2.0,
        BODY_Y + 4.0,
        App.Vector(EYE_X, -BODY_Y / 2.0 - 2.0, EYE_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    cutters.append(eye_l)
    cutters.append(eye_r)

    # 5. Top outer corner rounding outside R = 7.0 mm at X = +/-15.0 mm, Z = 23.0 mm
    # Right corner rounding (X > +15.0 mm, Z > 23.0 mm)
    box_r = Part.makeBox(8.0, BODY_Y + 4.0, 8.0, App.Vector(EYE_X, -BODY_Y / 2.0 - 2.0, EYE_Z))
    cyl_r = Part.makeCylinder(
        EYE_OUTER_R,
        BODY_Y + 6.0,
        App.Vector(EYE_X, -BODY_Y / 2.0 - 3.0, EYE_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    cutters.append(box_r.cut(cyl_r))

    # Left corner rounding (X < -15.0 mm, Z > 23.0 mm)
    box_l = Part.makeBox(8.0, BODY_Y + 4.0, 8.0, App.Vector(-EYE_X - 8.0, -BODY_Y / 2.0 - 2.0, EYE_Z))
    cyl_l = Part.makeCylinder(
        EYE_OUTER_R,
        BODY_Y + 6.0,
        App.Vector(-EYE_X, -BODY_Y / 2.0 - 3.0, EYE_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    cutters.append(box_l.cut(cyl_l))

    # 6. Lower side transitions outside 20.0 mm central base (|X| > 10.0 mm)
    # Right 45° chamfer from (10.0, 4.0) to (22.0, 16.0)
    p_r1 = App.Vector(BASE_X / 2.0, -BODY_Y / 2.0 - 2.0, -1.0)
    p_r2 = App.Vector(BODY_X / 2.0 + 1.0, -BODY_Y / 2.0 - 2.0, -1.0)
    p_r3 = App.Vector(BODY_X / 2.0 + 1.0, -BODY_Y / 2.0 - 2.0, SIDE_CHAMFER_Z1)
    p_r4 = App.Vector(BASE_X / 2.0, -BODY_Y / 2.0 - 2.0, SIDE_CHAMFER_Z0)
    poly_r = Part.makePolygon([p_r1, p_r2, p_r3, p_r4, p_r1])
    cutters.append(Part.Face(poly_r).extrude(App.Vector(0.0, BODY_Y + 4.0, 0.0)))

    # Left 45° chamfer from (-10.0, 4.0) to (-22.0, 16.0)
    p_l1 = App.Vector(-BASE_X / 2.0, -BODY_Y / 2.0 - 2.0, -1.0)
    p_l2 = App.Vector(-BODY_X / 2.0 - 1.0, -BODY_Y / 2.0 - 2.0, -1.0)
    p_l3 = App.Vector(-BODY_X / 2.0 - 1.0, -BODY_Y / 2.0 - 2.0, SIDE_CHAMFER_Z1)
    p_l4 = App.Vector(-BASE_X / 2.0, -BODY_Y / 2.0 - 2.0, SIDE_CHAMFER_Z0)
    poly_l = Part.makePolygon([p_l1, p_l2, p_l3, p_l4, p_l1])
    cutters.append(Part.Face(poly_l).extrude(App.Vector(0.0, BODY_Y + 4.0, 0.0)))

    # 7. Central top saddle arch between eyelets
    saddle = Part.makeCylinder(
        SADDLE_R,
        BODY_Y + 4.0,
        App.Vector(0.0, -BODY_Y / 2.0 - 2.0, SADDLE_Z),
        App.Vector(0.0, 1.0, 0.0),
    )
    cutters.append(saddle)

    # 8. Front (+Y) and rear (-Y) shoulder chamfers tapering from 18.0 mm to ARM_Y
    # Front cutter: transitions from Y = +9.0 at Z = Y_CHAMFER_Z0 to Y = +ARM_Y/2 at Z = Y_CHAMFER_Z0 + Y_CHAMFER_H
    yf1 = App.Vector(-BODY_X / 2.0 - 1.0, BODY_Y / 2.0 + 1.0, Y_CHAMFER_Z0)
    yf2 = App.Vector(-BODY_X / 2.0 - 1.0, BODY_Y / 2.0, Y_CHAMFER_Z0)
    yf3 = App.Vector(-BODY_X / 2.0 - 1.0, ARM_Y / 2.0, Y_CHAMFER_Z0 + Y_CHAMFER_H)
    yf4 = App.Vector(-BODY_X / 2.0 - 1.0, ARM_Y / 2.0, BODY_Z + 1.0)
    yf5 = App.Vector(-BODY_X / 2.0 - 1.0, BODY_Y / 2.0 + 1.0, BODY_Z + 1.0)
    poly_yf = Part.makePolygon([yf1, yf2, yf3, yf4, yf5, yf1])
    cutters.append(Part.Face(poly_yf).extrude(App.Vector(BODY_X + 2.0, 0.0, 0.0)))

    # Rear cutter: transitions from Y = -9.0 at Z = Y_CHAMFER_Z0 to Y = -ARM_Y/2 at Z = Y_CHAMFER_Z0 + Y_CHAMFER_H
    yr1 = App.Vector(-BODY_X / 2.0 - 1.0, -BODY_Y / 2.0 - 1.0, Y_CHAMFER_Z0)
    yr2 = App.Vector(-BODY_X / 2.0 - 1.0, -BODY_Y / 2.0, Y_CHAMFER_Z0)
    yr3 = App.Vector(-BODY_X / 2.0 - 1.0, -ARM_Y / 2.0, Y_CHAMFER_Z0 + Y_CHAMFER_H)
    yr4 = App.Vector(-BODY_X / 2.0 - 1.0, -ARM_Y / 2.0, BODY_Z + 1.0)
    yr5 = App.Vector(-BODY_X / 2.0 - 1.0, -BODY_Y / 2.0 - 1.0, BODY_Z + 1.0)
    poly_yr = Part.makePolygon([yr1, yr2, yr3, yr4, yr5, yr1])
    cutters.append(Part.Face(poly_yr).extrude(App.Vector(BODY_X + 2.0, 0.0, 0.0)))

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
        if arg.endswith("bt4v_hanging_cap.py") and i + 1 < len(sys.argv):
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
    shape = build_hanging_cap()
    verify_shape(
        shape,
        "BT4V_Hanging_Cap",
        EXPECT_EXTENTS,
        EXPECT_VOLUME,
        out_path,
    )
    print("BT4-V Top Hanging Cap generator completed successfully.", flush=True)


# --------------------------------------------------------------------------
# EXECUTION CONTRACT
# --------------------------------------------------------------------------
try:
    main()
except Exception as exc:
    print("ERROR: BT4-V Top Hanging Cap generation failed: %r" % (exc,), file=sys.stderr, flush=True)
    traceback.print_exc()
    sys.exit(1)

sys.exit(0)
