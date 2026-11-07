"""
BT4-V 3D Printed Antenna — Phase Crossover Spacer Generator (v0.3.0)

Generates the clip-on phase transposition spacer placed between Bay 1–2 and
Bay 3–4 of the modular vertical spine, exported as 'stl/BT4V_Phase_Crossover.stl'.

Technical Specifications:
- Requirements Baseline: Requirements.md §8, §16.3
- Plan Baseline: Plan.md §2.1, §2.2, §3.1 (T1.1, T1.2)
- Body Dimensions / Extents: 35.0 mm (X) x 12.0 mm (Y) x 30.0 mm (Z) (tol +/-0.1 mm)
- Target Volume: 6,100 mm^3 (+/-2% -> acceptable range: 5,978 – 6,222 mm^3)
- Solid Count: Exactly 1 valid solid (len(shape.Solids) == 1, shape.isValid() == True)

Mechanical & RF Features:
- Spine Interface: 20.0 mm wide interface (X: -10.0 to +10.0 mm) clipping securely
  onto the spine segment strut.
- Phase Transposition: 180° phase inversion transposition for the two continuous
  12 AWG vertical phase lines spaced at 25.0 mm center-to-center pitch.
- Diagonal Crossing Channels: Two 3.2 mm wide x 3.0 mm deep wire routing channels
  crossing diagonally on separate front (Y = +6.0 mm) and rear (Y = -6.0 mm) planes.
- Dielectric Isolation: Solid 6.0 mm plastic dielectric separator between front
  and rear channel floors, maintaining >=5.0 mm dielectric/air separation to prevent
  capacitive coupling, RF degradation, and electrical shorting.
- Snap-Fit Retention Clip: Snap-fit clip featuring a 2.4 mm mouth opening into a
  3.3 mm round retention cavity to lock securely onto the spine strut.
- Wire Transition Ports: 3.2 mm through-slots at top-right and bottom-left ends
  routing the rear transposed wire cleanly between front and rear planes.

Run headless:
    /snap/bin/freecad.cmd -c python/bt4v_phase_crossover.py
or:
    freecadcmd -c python/bt4v_phase_crossover.py
"""

import math
import os
import sys
import traceback

import FreeCAD as App
import Mesh
import Part

# --------------------------------------------------------------------------
# VERIFICATION BASELINES & TOLERANCES (Requirements.md §8.3, §16.3; Plan.md §3.1)
# --------------------------------------------------------------------------
EXPECT_EXTENTS = (35.0, 12.0, 30.0)  # mm: X, Y, Z extents
EXPECT_VOLUME = 6100.0  # mm^3: nominal volume
BBOX_TOL = 0.1  # mm: per-axis bounding-box extent tolerance
VOL_TOL = 0.02  # +/- fraction of expected volume (2%)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "stl", "BT4V_Phase_Crossover.stl")

# --------------------------------------------------------------------------
# PARAMETERS (mm)
# --------------------------------------------------------------------------
# Outer body envelope
BODY_X = 35.0  # Width (X: -17.5 to +17.5)
BODY_Y = 12.0  # Depth (Y: -6.0 to +6.0)
BODY_Z = 30.0  # Height (Z: 0.0 to 30.0)

# Phase line channels
WIRE_PITCH = 25.0  # Center-to-center phase line pitch (X = -12.5 and +12.5)
WIRE_CH_W = 3.2  # Wire channel width (12 AWG clearance)
WIRE_CH_D = 3.0  # Wire channel depth into front/rear faces

# Spine strut interface
SPINE_W = 20.0  # Spine segment interface width in X (X: -10.0 to +10.0)
SPINE_RECESS_D = 7.8  # Spine seating recess depth into rear face (from Y = -6.0 mm)

# Central dielectric bridge zone
BRIDGE_Z_MIN = 11.5  # Central bridge lower Z
BRIDGE_Z_MAX = 18.5  # Central bridge upper Z

# Snap-fit retention clip
SNAP_MOUTH_W = 2.4  # Snap mouth opening width in X
SNAP_CAV_D = 3.3  # Cylindrical snap cavity diameter

# Side waist cutouts
WAIST_W = 2.8  # Lateral waist cutout depth in X

# Front weight relief pockets (calibrated to meet exact 6,100 mm^3 volume target)
CAL_POCKET_D = 3.190326  # Calibrated pocket depth from front face (Y = +6.0 inwards)


# --------------------------------------------------------------------------
# GEOMETRY HELPERS
# --------------------------------------------------------------------------
def make_diagonal_channel(p_start_x, p_start_z, p_end_x, p_end_z, width, y_start, y_extrude, ext=5.0):
    """Create an angled wire channel cutter prism in X-Z plane extruded along Y."""
    dx = p_end_x - p_start_x
    dz = p_end_z - p_start_z
    length = math.hypot(dx, dz)
    ux = dx / length
    uz = dz / length

    # Unit normal vector rotated 90 degrees in X-Z plane
    nx = -uz
    nz = ux
    half_w = width / 2.0

    # Extend endpoints so channel cleanly passes through boundaries
    p0_x = p_start_x - ux * ext
    p0_z = p_start_z - uz * ext
    p1_x = p_end_x + ux * ext
    p1_z = p_end_z + uz * ext

    v1 = App.Vector(p0_x - nx * half_w, y_start, p0_z - nz * half_w)
    v2 = App.Vector(p0_x + nx * half_w, y_start, p0_z + nz * half_w)
    v3 = App.Vector(p1_x + nx * half_w, y_start, p1_z + nz * half_w)
    v4 = App.Vector(p1_x - nx * half_w, y_start, p1_z - nz * half_w)

    poly = Part.makePolygon([v1, v2, v3, v4, v1])
    face = Part.Face(poly)
    return face.extrude(App.Vector(0.0, y_extrude, 0.0))


# --------------------------------------------------------------------------
# MODEL BUILDER
# --------------------------------------------------------------------------
def build_phase_crossover():
    """Build the Phase Crossover Spacer solid model conforming to BT4-V specifications."""
    # 1. Base body block (35.0 x 12.0 x 30.0 mm, centered on X and Y, Z: 0.0 to 30.0)
    base = Part.makeBox(BODY_X, BODY_Y, BODY_Z, App.Vector(-BODY_X / 2.0, -BODY_Y / 2.0, 0.0))

    cutters = []

    # 2. Front diagonal wire routing channel (3.2 mm wide x 3.0 mm deep)
    # Connects top-left (-12.5, 30.0) to bottom-right (+12.5, 0.0)
    # Cuts from Y = +3.0 mm outward past front face at Y = +6.0 mm
    c_front = make_diagonal_channel(
        -WIRE_PITCH / 2.0,
        BODY_Z,
        WIRE_PITCH / 2.0,
        0.0,
        WIRE_CH_W,
        BODY_Y / 2.0 - WIRE_CH_D,
        WIRE_CH_D + 1.0,
    )
    cutters.append(c_front)

    # 3. Rear diagonal wire routing channel (3.2 mm wide x 3.0 mm deep)
    # Connects top-right (+12.5, 30.0) to bottom-left (-12.5, 0.0)
    # Cuts from Y = -3.0 mm outward past rear face at Y = -6.0 mm
    c_rear = make_diagonal_channel(
        WIRE_PITCH / 2.0,
        BODY_Z,
        -WIRE_PITCH / 2.0,
        0.0,
        WIRE_CH_W,
        -BODY_Y / 2.0 + WIRE_CH_D,
        -(WIRE_CH_D + 1.0),
    )
    cutters.append(c_rear)

    # 4. Wire transition pass-through slots routing rear transposed wire through body
    # Top-right slot at X = +12.5 mm, Z: 26.0 to 31.0 mm (full Y depth)
    slot_top = Part.makeBox(
        WIRE_CH_W,
        BODY_Y + 2.0,
        5.0,
        App.Vector(WIRE_PITCH / 2.0 - WIRE_CH_W / 2.0, -BODY_Y / 2.0 - 1.0, 26.0),
    )
    cutters.append(slot_top)

    # Bottom-left slot at X = -12.5 mm, Z: -1.0 to 4.0 mm (full Y depth)
    slot_bot = Part.makeBox(
        WIRE_CH_W,
        BODY_Y + 2.0,
        5.0,
        App.Vector(-WIRE_PITCH / 2.0 - WIRE_CH_W / 2.0, -BODY_Y / 2.0 - 1.0, -1.0),
    )
    cutters.append(slot_bot)

    # 5. Spine segment 20 mm interface seating recess on rear face (X: -10.0 to +10.0 mm)
    # Preserves a solid 7.0 mm central bridge (Z: 11.5 to 18.5 mm) for uninterrupted
    # 6.0 mm dielectric isolation between crossing channels.
    recess_top = Part.makeBox(
        SPINE_W,
        SPINE_RECESS_D + 1.0,
        11.5,
        App.Vector(-SPINE_W / 2.0, -BODY_Y / 2.0 - 1.0, BRIDGE_Z_MAX),
    )
    recess_bot = Part.makeBox(
        SPINE_W,
        SPINE_RECESS_D + 1.0,
        11.5,
        App.Vector(-SPINE_W / 2.0, -BODY_Y / 2.0 - 1.0, 0.0),
    )
    cutters.append(recess_top)
    cutters.append(recess_bot)

    # 6. Snap-fit retention clip with 2.4 mm mouth over 3.3 mm cavity
    # Located along the spine interface to clip securely onto spine strut
    mouth_top = Part.makeBox(
        SNAP_MOUTH_W,
        3.0,
        12.0,
        App.Vector(-SNAP_MOUTH_W / 2.0, -BODY_Y / 2.0 + SPINE_RECESS_D - 2.0, BRIDGE_Z_MAX),
    )
    cavity_top = Part.makeCylinder(
        SNAP_CAV_D / 2.0,
        12.0,
        App.Vector(0.0, -BODY_Y / 2.0 + SPINE_RECESS_D, BRIDGE_Z_MAX),
        App.Vector(0.0, 0.0, 1.0),
    )
    mouth_bot = Part.makeBox(
        SNAP_MOUTH_W,
        3.0,
        12.0,
        App.Vector(-SNAP_MOUTH_W / 2.0, -BODY_Y / 2.0 + SPINE_RECESS_D - 2.0, -0.5),
    )
    cavity_bot = Part.makeCylinder(
        SNAP_CAV_D / 2.0,
        12.0,
        App.Vector(0.0, -BODY_Y / 2.0 + SPINE_RECESS_D, -0.5),
        App.Vector(0.0, 0.0, 1.0),
    )
    cutters.append(mouth_top)
    cutters.append(cavity_top)
    cutters.append(mouth_bot)
    cutters.append(cavity_bot)

    # 7. Side waist cutouts (Z: 5.0 to 25.0 mm), preserving corner lands at Z = 0 and 30 mm
    cut_wl = Part.makeBox(
        WAIST_W + 1.0,
        BODY_Y + 2.0,
        20.0,
        App.Vector(-BODY_X / 2.0 - 1.0, -BODY_Y / 2.0 - 1.0, 5.0),
    )
    cut_wr = Part.makeBox(
        WAIST_W + 1.0,
        BODY_Y + 2.0,
        20.0,
        App.Vector(BODY_X / 2.0 - WAIST_W, -BODY_Y / 2.0 - 1.0, 5.0),
    )
    cutters.append(cut_wl)
    cutters.append(cut_wr)

    # 8. Front lightening pockets flanking the diagonal wire
    # Top-right pocket: X: 2.0 to 9.5 mm, Z: 18.0 to 28.0 mm
    pocket_tr = Part.makeBox(
        7.5,
        CAL_POCKET_D + 1.0,
        10.0,
        App.Vector(2.0, BODY_Y / 2.0 - CAL_POCKET_D, 18.0),
    )
    # Bottom-left pocket: X: -9.5 to -2.0 mm, Z: 2.0 to 12.0 mm
    pocket_bl = Part.makeBox(
        7.5,
        CAL_POCKET_D + 1.0,
        10.0,
        App.Vector(-9.5, BODY_Y / 2.0 - CAL_POCKET_D, 2.0),
    )
    cutters.append(pocket_tr)
    cutters.append(pocket_bl)

    # 9. Lateral bridge weight relief pockets flanking the crossover center
    # Left bridge pocket: X: -9.5 to -4.5 mm, Z: 11.5 to 18.5 mm
    bridge_l = Part.makeBox(
        5.0,
        4.0,
        7.0,
        App.Vector(-9.5, BODY_Y / 2.0 - 3.0, BRIDGE_Z_MIN),
    )
    # Right bridge pocket: X: 4.5 to 9.5 mm, Z: 11.5 to 18.5 mm
    bridge_r = Part.makeBox(
        5.0,
        4.0,
        7.0,
        App.Vector(4.5, BODY_Y / 2.0 - 3.0, BRIDGE_Z_MIN),
    )
    cutters.append(bridge_l)
    cutters.append(bridge_r)

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
        if arg.endswith("bt4v_phase_crossover.py") and i + 1 < len(sys.argv):
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
    shape = build_phase_crossover()
    verify_shape(
        shape,
        "BT4V_Phase_Crossover",
        EXPECT_EXTENTS,
        EXPECT_VOLUME,
        out_path,
    )
    print("BT4-V Phase Crossover Spacer generator completed successfully.", flush=True)


# --------------------------------------------------------------------------
# EXECUTION CONTRACT
# --------------------------------------------------------------------------
try:
    main()
except Exception as exc:
    print("ERROR: BT4-V Phase Crossover Spacer generation failed: %r" % (exc,), file=sys.stderr, flush=True)
    traceback.print_exc()
    sys.exit(1)
