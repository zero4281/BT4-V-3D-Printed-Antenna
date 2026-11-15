"""
BT4-V 3D Printed Antenna — Full-Length Bowtie Backing Strut Generator (v0.3.0)

Generates the universal interlocking full-length structural backing strut that snaps
behind every V-whisker arm from the central bay bracket out to the wire tip,
exported as 'stl/BT4V_Bowtie_Backing.stl'.
Quantity required: 24 (1 strut per 200 mm UHF arm across Bays 2 & 3 [8 pcs];
2 daisy-chained struts per 340 mm VHF arm across Bays 1 & 4 [16 pcs]).

Technical Specifications:
- Requirements Baseline: Requirements.md §9, §16.3
- Body Dimensions / Extents: 180.0 mm (X) x 12.0 mm (Y) x 8.0 mm (Z) (tol +/-0.1 mm)
  * Active body span: 176.0 mm + 4.0 mm root tenon = 180.0 mm total X extent
    (X: -90.0..-86.0 root tenon + X: -86.0..+90.0 body with 4.2 x 6.2 x 4.2 mm tip mortise).
  * Combined with ~15.0 mm inside the Bay Bracket wing:
    - 1 strut backs a 200 mm UHF arm (~15 + 176 = ~191 mm root-to-tip support).
    - 2 daisy-chained struts back a 340 mm VHF arm (interlocking the outer strut's
      4.0 mm root tenon into the inner strut's 4.2 mm tip mortise).
- Nominal Volume: 2,200 mm^3 (+/-2% -> acceptable range: 2,156 – 2,244 mm^3)
- Solid Count: Exactly 1 valid solid (len(shape.Solids) == 1, shape.isValid() == True)

Mechanical & RF Features:
- Purpose: Provides continuous 3D-printed structural backing behind the entire length
  of every V-whisker arm (from bracket root to wire tip), permanently locking exact
  flare angles (32.5° UHF, 25.5° VHF) and completely eliminating gravity droop, sag,
  or vibration.
- Snap-Fit C-Clip Cradle Channel: Continuous snap-fit wire retention channel (2.4 mm
  snap throat opening into a 3.2 mm circular wire cavity) gripping the 12 AWG solid
  copper wire along its entire span.
- Interlocking Root Tenon & Tip Mortise: Inner root end (-X) features a 4.0 x 6.0 x 4.0 mm
  male tenon that locks into either the Bay Bracket wing socket or the female mortise
  socket (+X) of an adjacent backing strut for 340 mm VHF arm extension.
- Strut Profile: Ribbed I-beam / truss cross-section providing maximum rigidity along
  the full arm length while maintaining minimal mass (~2.7 g each).

Run headless:
    /snap/bin/freecad.cmd python/bt4v_bowtie_backing.py
or:
    freecadcmd python/bt4v_bowtie_backing.py
"""

import math
import os
import sys
import traceback

import FreeCAD as App
import Mesh
import Part

# --------------------------------------------------------------------------
# VERIFICATION BASELINES & TOLERANCES (Requirements.md §9.3, §16.3)
# --------------------------------------------------------------------------
EXPECT_EXTENTS = (180.0, 12.0, 8.0)  # mm: X, Y, Z extents (176.0 mm active body span + 4.0 mm root tenon = 180.0 mm)
EXPECT_VOLUME = 2200.0  # mm^3: nominal volume
BBOX_TOL = 0.1  # mm: per-axis bounding-box extent tolerance
VOL_TOL = 0.02  # +/- fraction of expected volume (2%)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "stl", "BT4V_Bowtie_Backing.stl")

# --------------------------------------------------------------------------
# PARAMETERS (mm)
# --------------------------------------------------------------------------
# Outer body envelope
BODY_X = 180.0  # Total length (X: -90.0 to +90.0)
BODY_Y = 12.0   # Body depth (Y: -6.0 to +6.0)
BODY_Z = 8.0    # Body height (Z: 0.0 to 8.0)

# Snap-fit C-clip wire cradle channel along top face
SNAP_MOUTH_W = 2.4  # Snap throat opening width in Y
WIRE_CAV_D = 3.2    # Circular wire cavity diameter (12 AWG clearance)
WIRE_CAV_Z = 6.1    # Center Z of circular wire cavity

# I-beam profile parameters
WEB_Y = 1.0       # Central web thickness in Y (-0.5 to +0.5 mm)
STRUT_Z_MIN = 2.40 # Lower Z boundary of web
STRUT_Z_MAX = 5.40 # Upper Z boundary of web

# Pocket depth
CAL_POCKET_D = 5.5  # Depth of web pockets into front/rear faces


# --------------------------------------------------------------------------
# MODEL BUILDER
# --------------------------------------------------------------------------
def build_bowtie_backing():
    """Build the Full-Length Bowtie Backing Strut solid model conforming to BT4-V specifications."""
    # 1. Base body envelope block (180.0 x 12.0 x 8.0 mm, centered on X and Y, Z: 0.0 to 8.0)
    base = Part.makeBox(
        BODY_X,
        BODY_Y,
        BODY_Z,
        App.Vector(-BODY_X / 2.0, -BODY_Y / 2.0, 0.0),
    )

    cutters = []

    # 2. Continuous C-clip snap-fit wire channel along top face (X: -86.0 to +86.0 mm)
    channel_len = 172.0
    # Narrow 2.4 mm snap throat at top face (Z: 6.1 to 8.1 mm)
    throat = Part.makeBox(
        channel_len,
        SNAP_MOUTH_W,
        BODY_Z - WIRE_CAV_Z + 0.5,
        App.Vector(-channel_len / 2.0, -SNAP_MOUTH_W / 2.0, WIRE_CAV_Z),
    )
    cutters.append(throat)

    # Circular 3.2 mm wire retention cavity along X
    cav = Part.makeCylinder(
        WIRE_CAV_D / 2.0,
        channel_len,
        App.Vector(-channel_len / 2.0, 0.0, WIRE_CAV_Z),
        App.Vector(1.0, 0.0, 0.0),
    )
    cutters.append(cav)

    # 3. Root male tenon shoulder cuts at -X end (X: -90.0 to -86.0 mm, forming 4.0 x 6.0 x 4.0 mm tenon)
    cutters.append(Part.makeBox(4.0, 3.0, BODY_Z + 2.0, App.Vector(-90.0, 3.0, -1.0)))
    cutters.append(Part.makeBox(4.0, 3.0, BODY_Z + 2.0, App.Vector(-90.0, -6.0, -1.0)))
    cutters.append(Part.makeBox(4.0, BODY_Y + 2.0, 2.0, App.Vector(-90.0, -BODY_Y / 2.0 - 1.0, 0.0)))
    cutters.append(Part.makeBox(4.0, BODY_Y + 2.0, 2.0, App.Vector(-90.0, -BODY_Y / 2.0 - 1.0, 6.0)))

    # 4. Tip female mortise socket at +X end (X: +85.8 to +90.1 mm, 4.2 x 6.2 x 4.2 mm socket)
    mortise_tip = Part.makeBox(
        4.3,
        6.2,
        4.2,
        App.Vector(BODY_X / 2.0 - 4.2, -3.1, 1.9),
    )
    cutters.append(mortise_tip)

    # 5. Top and bottom Z-profile cutouts (leaving end solid blocks for root/tip integrity)
    span_len = BODY_X - 18.0  # 162.0 mm central span (X: -81.0 to +81.0)
    z_cut_top = Part.makeBox(
        span_len,
        BODY_Y + 4.0,
        BODY_Z - STRUT_Z_MAX + 1.0,
        App.Vector(-span_len / 2.0, -BODY_Y / 2.0 - 2.0, STRUT_Z_MAX),
    )
    z_cut_bot = Part.makeBox(
        span_len,
        BODY_Y + 4.0,
        STRUT_Z_MIN + 1.0,
        App.Vector(-span_len / 2.0, -BODY_Y / 2.0 - 2.0, -1.0),
    )
    cutters.append(z_cut_top)
    cutters.append(z_cut_bot)

    # 6. Side Y-profile cutouts (forming I-beam flanges)
    y_cut_front = Part.makeBox(
        span_len,
        BODY_Y / 2.0 - WEB_Y / 2.0 + 1.0,
        BODY_Z + 2.0,
        App.Vector(-span_len / 2.0, WEB_Y / 2.0, -1.0),
    )
    y_cut_rear = Part.makeBox(
        span_len,
        BODY_Y / 2.0 - WEB_Y / 2.0 + 1.0,
        BODY_Z + 2.0,
        App.Vector(-span_len / 2.0, -BODY_Y / 2.0 - (BODY_Y / 2.0 - WEB_Y / 2.0 + 1.0), -1.0),
    )
    cutters.append(y_cut_front)
    cutters.append(y_cut_rear)

    # 7. Ribbed I-beam side pockets along central web
    pocket_spans = [
        (-78.0, -58.0),
        (-54.0, -34.0),
        (-30.0, -10.0),
        (-6.0, 14.0),
        (18.0, 38.0),
        (42.0, 62.0),
        (66.0, 78.0),
    ]
    pocket_z0 = STRUT_Z_MIN + 0.2
    pocket_zh = (STRUT_Z_MAX - STRUT_Z_MIN) - 0.4

    for x0, x1 in pocket_spans:
        xw = x1 - x0
        p_front = Part.makeBox(
            xw,
            CAL_POCKET_D,
            pocket_zh,
            App.Vector(x0, WEB_Y / 2.0, pocket_z0),
        )
        p_rear = Part.makeBox(
            xw,
            CAL_POCKET_D,
            pocket_zh,
            App.Vector(x0, -WEB_Y / 2.0 - CAL_POCKET_D, pocket_z0),
        )
        cutters.append(p_front)
        cutters.append(p_rear)

    # 8. Vertical lightening windows through the central web
    win_centers = [-68.0, -44.0, -20.0, 4.0, 28.0, 52.0, 72.0]
    win_x_w = 10.0
    win_y_w = 3.2
    for cx in win_centers:
        win = Part.makeBox(
            win_x_w,
            win_y_w,
            BODY_Z + 2.0,
            App.Vector(cx - win_x_w / 2.0, -win_y_w / 2.0, -1.0),
        )
        cutters.append(win)

    # Apply all cuts sequentially to ensure valid single solid
    solid = base
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
        if arg.endswith("bt4v_bowtie_backing.py"):
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
    shape = build_bowtie_backing()
    verify_shape(
        shape,
        "BT4V_Bowtie_Backing",
        EXPECT_EXTENTS,
        EXPECT_VOLUME,
        out_path,
    )
    print("BT4-V Full-Length Bowtie Backing Strut generator completed successfully.", flush=True)


# --------------------------------------------------------------------------
# EXECUTION CONTRACT
# --------------------------------------------------------------------------
try:
    main()
except Exception as exc:
    print("ERROR: BT4-V Full-Length Bowtie Backing Strut generation failed: %r" % (exc,), file=sys.stderr, flush=True)
    traceback.print_exc()
    sys.exit(1)

sys.exit(0)
