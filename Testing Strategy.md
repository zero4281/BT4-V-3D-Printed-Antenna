# BT4-V Testing Strategy

**Version:** 0.1.0  
**Applies to:** BT4-V 3D Printed Antenna, revision v0.1.0  
**Requirements baseline:** `Requirements.md` v0.1.0  

---

## 1. Overview & Verification Philosophy

BT4-V is a physical 3D modelling, CAD script generation, and fabrication project, not a software application.
There is **no unit-test framework and no automated software unit-test suite**, and none is required.

Verification is divided into two distinct tiers:
1. **Automated CAD & Build Regression Testing:** Validated via the headless build orchestrator `bt4v_generate_all.sh` and python scripts in `python/`. This verifies solid validity, bounding box extents, volume baselines, non-zero failure exits, and image rendering.
2. **Physical Human-Gated Acceptance Testing:** Carried out by the builder during printing, assembly, and television reception verification. These tests cannot be completed by an automated agent without explicit builder confirmation.

---

## 2. Automated CAD Regression Testing

### 2.1 The Sandbox Build Regression

Prior to any git commit or release of CAD scripts, the entire pipeline must pass the headless build regression. Because the FreeCAD snap environment cannot access `/tmp`, execution must occur either in the workspace or in a disposable sandbox directory such as `$HOME/bt4v-verify`:

```bash
# Example verification execution:
FREECAD_CMD=/snap/bin/freecad.cmd ./bt4v_generate_all.sh
# or on native Linux FreeCAD builds:
FREECAD_CMD=freecadcmd ./bt4v_generate_all.sh
```

### 2.2 Verification Checks

Every full regression run must verify the following automated criteria:

1. **Artifact Count & Existence:**
   - All 7 STL meshes exist in `stl/`:
     - `BT4V_Center_Feed.stl`
     - `BT4V_Bay_Bracket.stl`
     - `BT4V_Spine_Segment.stl`
     - `BT4V_Phase_Crossover.stl`
     - `BT4V_Whisker_Spreader.stl`
     - `BT4V_Hanging_Cap.stl`
     - `BT4V_Fit_Coupon.stl`
   - Both PNG deliverables exist at the repository root:
     - `BT4-V 2D Drawing.png`
     - `BT4-V Parts Preview.png`
2. **Solid Validity & Geometry Baselines:**
   - Every STL must represent exactly **1 solid**, with `Valid: True`.
   - Measured bounding boxes must match nominal dimensions within **±0.1 mm**.
   - Measured volumes must agree with the baseline table in `Requirements.md` §16.3 within **±2%**.
3. **Exit Code Propagation:**
   - Generators must return `0` on successful export.
   - Any failure (invalid parameters, failed FreeCAD boolean cut/fuse, missing output directory) must terminate with non-zero exit code (`1` or `2`).
4. **Drawing & Preview Integrity:**
   - `bt4v_drawing.py` and `bt4v_preview.py` must run without error and generate non-empty (>10 kB) PNG files matching their target pixel resolutions.

---

## 3. Physical Human-Gated Test Procedures

Physical acceptance items must be evaluated and confirmed by the builder:

### 3.1 Step 1 — Fit Coupon Verification
Print `stl/BT4V_Fit_Coupon.stl` first on the target printer and profile:
- **Wire fit:** Test 12 AWG solid copper wire in friction and snap channels. Confirm wire snaps in firmly without loose play.
- **Hardware fit:** Verify M4 hex bolts slide smoothly through clearance holes and M4 hex nuts seat firmly into captured pockets.
- **Balun terminal fit:** Check 25 mm post spacing against RCA VH101R spade lugs.
- **Joint tolerances:** Check tenon/mortise fit and 2.5 mm cross-pin alignment.
- **Decision:** If tolerances are too tight/loose, adjust generator parameters in `python/` and regenerate before committing production prints.

### 3.2 Step 2 — Whisker Bending & Spreader Rigidity
- Cut and bend 12 AWG solid copper wire for UHF (410 mm cut, 32.5° flare) and VHF (690 mm cut, 25.5° flare).
- Snap `BT4V_Whisker_Spreader.stl` onto the VHF whiskers at ~150 mm radius.
- **Droop test:** Mount whisker in bay bracket and hold horizontally. Confirm that the triangular tine spreader prevents wire sagging under gravity.

### 3.3 Step 3 — Balun Cradle & Assembly
- Assemble the modular spine (Center Feed + 4 Spine Segments + 4 Bay Brackets + Hanging Cap).
- Verify that the **RCA VH101R** matching transformer snaps snugly into the Center Feed cradle.
- Confirm phase lines route through crossover clips with ≥5 mm separation between crossing conductors.

### 3.4 Step 4 — Reception & Signal Quality Verification
- Suspend assembled antenna in target window using dual hanging eyelets.
- Connect 75 Ω RG6 coax downlead to RCA VH101R transformer and television tuner.
- Use TV signal meter / diagnostics to confirm reception across target broadcast bands:
  - VHF-High: Local broadcast channels (Channels 7–13, 174–216 MHz).
  - UHF: Local broadcast channels (Channels 14–36, 470–608 MHz).

---

## 4. SDLC Workflow & Commit Gating

- **No Unit Test Suite:** Do not create a `tests/` directory or pytest suites.
- **`sdlc-commit` / `sdlc-implement` Integration:**
  - Automated test gate is the execution of `./bt4v_generate_all.sh` and verification of output geometry against `Requirements.md` §16.3.
  - Physical test steps (print fit, droop test, TV reception) remain unchecked in `Plan.md` until builder verification.
- **Safety Rule:** Never hand-edit STL files. STLs in `stl/` are reproducible build artifacts generated from `python/bt4v_*.py`.
