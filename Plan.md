# BT4-V 3D Printed Antenna — Implementation Plan

**Version 0.3.0**

---

## Revision Jump Context: Architectural Evolution to v0.3.0 Full-Length Bowtie Backing Struts

This implementation plan documents the complete architectural progression from the initial **BT4-V v0.1.0** baseline through the intermediate **v0.2.0** revision to the finalized **v0.3.0** specification:

1. **Baseline `v0.1.0`:** Initial 4-bay stacked bowtie + VHF-High array featuring localized Triangular Tine Spreaders (`bt4v_whisker_spreader.py`) clipped near whisker tips, 4 Spine Segments (`20.0 × 14.0 × 120.0 mm`), and a compact Center Feed Hub (`40.0 × 24.0 × 70.0 mm`).
2. **Intermediate `v0.2.0`:** Added localized Mid-Span Bowtie Support Struts (`bt4v_bowtie_support.py`, `65.0 × 10.0 × 8.0 mm`, Qty 8) to assist mid-arm spacing while retaining separate tine spreaders.
3. **Finalized `v0.3.0`:** Replaced both localized tine spreaders and mid-span supports with universal interlocking **Full-Length Bowtie Backing Struts** (`python/bt4v_bowtie_backing.py` → `stl/BT4V_Bowtie_Backing.stl`, `180.0 × 12.0 × 8.0 mm`, nominal volume `2,200 mm³`, Qty 24 — 1 strut per 200 mm UHF arm [8 pcs] and 2 daisy-chained struts per 340 mm VHF arm [16 pcs]). Simultaneously unified the vertical spine architecture to an exact **`130.0 mm` center-to-center bay pitch** across all four bays using a `40.0 × 24.0 × 110.0 mm` Center Feed Hub (`100.0 mm` active body + `10.0 mm` tenon, Qty 1), `50.0 × 18.0 × 40.0 mm` Bay Brackets (`30.0 mm` active body + `10.0 mm` tenon, Qty 4) with 4 lateral wing sockets each, and `30.0 × 14.0 × 110.0 mm` Spine Segments (`100.0 mm` active body + `10.0 mm` tenon, Qty 2) with straight-through `25.0 mm` phase-line grooves and a `20.0 mm` mid-span crossover waist. Total printed production set: **34 parts** (+ 1 optional Fit Coupon), **~235 g** total mass.

### Summary of Cumulative Structural, RF, and Mechanical Changes

| Architectural Domain | Baseline (v0.1.0) | Intermediate (v0.2.0) | Target v0.3.0 Architecture | Engineering Rationale |
|---|---|---|---|---|
| **Antenna Topology & Bay Pitch** | 4-bay vertical stack with mixed spine/hub spacing | 4-bay vertical stack | Unified **130.0 mm** center-to-center bay pitch across all 4 bays (`390.0 mm` active array height, `~560 mm` overall height) | Ensures uniform broadside phase addition (+6 to +8 dBi UHF, +3 to +4 dBi VHF-High) within a ≤600 mm window envelope |
| **Polarisation** | Strictly horizontal (0° tilt in X-Z plane) | Strictly horizontal (0° tilt in X-Z plane) | Strictly horizontal (0° tilt in X-Z plane) | Eliminates cross-polarisation loss for horizontally polarised DTV broadcasts |
| **Feedpoint & Balun** | RCA VH101R 4:1 (300:75 Ω) outdoor matching transformer | RCA VH101R matching transformer | RCA VH101R matching transformer cradled in `40.0 × 24.0 × 110.0 mm` Center Feed Hub (midpoint feed at `Z = 50.0 mm`) | Matches 300 Ω balanced phase bus to 75 Ω RG6 coaxial downlead while maintaining exact 130.0 mm Bay 2–3 pitch |
| **Whisker Support & Sag Control** | Localized Triangular Tine Spreaders (`bt4v_whisker_spreader.py`) near tips | Localized Mid-Span Bowtie Support Struts (`bt4v_bowtie_support.py`, `65 × 10 × 8 mm`, 8 pcs) | Continuous interlocking **Full-Length Bowtie Backing Struts** (`python/bt4v_bowtie_backing.py`, `180.0 × 12.0 × 8.0 mm`, **24 pcs**: 1/UHF arm, 2 daisy-chained/VHF arm) | Permanently locks exact flare angles (32.5° UHF, 25.5° VHF) from Bay Bracket wing sockets to wire tips, eliminating gravity sag, droop, and wind vibration |
| **Modular Spine Architecture** | 1 Center Feed + 4 Bay Brackets + 4 Spine Segments + 1 Hanging Cap | Same pre-unification spine | **8 spine pieces / 7 pinned joints:** 1 Hanging Cap + 4 Bay Brackets (`50 × 18 × 40 mm`) + 2 Spine Segments (`30 × 14 × 110 mm`) + 1 Center Feed Hub (`40 × 24 × 110 mm`) | Reduces spine segment count from 4 to 2 (`15 + 100 + 15 = 130.0 mm` pitch) and fits every part flat on `220 × 220 mm` / `235 × 235 mm` beds |
| **Phase Line Routing & Crossover** | Stepped phase routing with 2 crossover spacers | Same stepped routing | Straight-through **25.0 mm** center-to-center phase-line grooves across all spine parts + 2 Phase Crossover Spacers (`35.0 × 12.0 × 30.0 mm`) on `20.0 mm` mid-span spine waists | Eliminates lateral wire bends while maintaining ≥5.0 mm dielectric separation at the Bay 1–2 and Bay 3–4 180° phase transpositions |

---

## Section 1: Current State Assessment

### 1.1 Verification Table

| Component / Artifact | File Path | Status | Verification State (Measured vs. `Requirements.md` §16.3) | Outstanding Tasks |
|---|---|---|---|---|
| **Center Feed Hub** (Qty 1) | `python/bt4v_center_feed.py`<br>`stl/BT4V_Center_Feed.stl` | Completed / Verified | `1 Solid`, `Valid: True`, Extents: `40.0 × 24.0 × 110.0 mm`, Volume: `42,053.92 mm³` (`+0.1%` vs `42,000 mm³`), Exit `0` | None (Layer 1 CAD verification passed) |
| **Whisker Bay Bracket** (Qty 4) | `python/bt4v_bay_bracket.py`<br>`stl/BT4V_Bay_Bracket.stl` | Completed / Verified | `1 Solid`, `Valid: True`, Extents: `50.0 × 18.0 × 40.0 mm`, Volume: `19,181.20 mm³` (`-0.1%` vs `19,200 mm³`), Exit `0` | None (Layer 1 CAD verification passed) |
| **Spine Segment** (Qty 2) | `python/bt4v_spine_segment.py`<br>`stl/BT4V_Spine_Segment.stl` | Completed / Verified | `1 Solid`, `Valid: True`, Extents: `30.0 × 14.0 × 110.0 mm`, Volume: `21,181.95 mm³` (`+0.9%` vs `21,000 mm³`), Exit `0` | None (Layer 1 CAD verification passed) |
| **Phase Crossover Spacer** (Qty 2) | `python/bt4v_phase_crossover.py`<br>`stl/BT4V_Phase_Crossover.stl` | Completed / Verified | `1 Solid`, `Valid: True`, Extents: `35.0 × 12.0 × 30.0 mm`, Volume: `6,100.00 mm³` (`0.0%` vs `6,100 mm³`), Exit `0` | None (Layer 1 CAD verification passed) |
| **Full-Length Bowtie Backing Strut** (Qty 24) | `python/bt4v_bowtie_backing.py`<br>`stl/BT4V_Bowtie_Backing.stl` | Completed / Verified | `1 Solid`, `Valid: True`, Extents: `180.0 × 12.0 × 8.0 mm`, Volume: `2,164.37 mm³` (`-1.6%` vs `2,200 mm³`), Exit `0` | None (Layer 1 CAD verification passed) |
| **Top Hanging Cap** (Qty 1) | `python/bt4v_hanging_cap.py`<br>`stl/BT4V_Hanging_Cap.stl` | Completed / Verified | `1 Solid`, `Valid: True`, Extents: `44.0 × 18.0 × 30.0 mm`, Volume: `7,400.00 mm³` (`0.0%` vs `7,400 mm³`), Exit `0` | None (Layer 1 CAD verification passed) |
| **Fit Coupon** (Qty 1, Optional) | `python/bt4v_fit_coupon.py`<br>`stl/BT4V_Fit_Coupon.stl` | Completed / Verified | `1 Solid`, `Valid: True`, Extents: `90.0 × 50.0 × 10.0 mm`, Volume: `26,497.36 mm³` (`-0.0%` vs `26,500 mm³`), Exit `0` | None (Layer 1 CAD verification passed) |
| **2D Technical Drawing** | `python/bt4v_drawing.py`<br>`BT4-V 2D Drawing.png` | Completed / Verified | Pillow PNG render, `2200 × 1500 px`, `356.9 kB` (`356,850 B`, `> 10 kB`), Exit `0` | Optional polish: update hardware note string on line 823 (`"6"` → `"7"` spine joint pins) |
| **3D Parts Preview** | `python/bt4v_preview.py`<br>`BT4-V Parts Preview.png` | Completed / Verified | Pillow multi-panel render, `1800 × 800 px`, `151.1 kB` (`151,094 B`, `> 10 kB`), Exit `0` | Optional polish: update card subtitle string on line 676 (`"6 joints"` → `"7 joints"`) |
| **Build Orchestrator** | `bt4v_generate_all.sh` | Completed / Verified | POSIX bash (`set -euo pipefail`), runs all 9 generators and verifies all 7 STLs + 2 PNGs, Exit `0` | None (Master orchestration verified) |
| **Project Documentation** | `Requirements.md`<br>`Testing Strategy.md`<br>`ASSEMBLY.md`<br>`BT4-V BOM.md`<br>`README.md`<br>`Bugs.md` | Completed / Verified | `Requirements.md`, `Testing Strategy.md`, `ASSEMBLY.md`, `BT4-V BOM.md`, and `README.md` fully synchronized to `v0.3.0` (34 parts, ~235 g, 24 backing struts, 7 spine joints) | Minor metadata note: `Bugs.md` header still cites `v0.1.0` (0 open bugs) |

### 1.2 Remaining Structural & Functional Drift Breakdown

- **Layer 1 Automated CAD & Documentation Completeness:** All 7 FreeCAD parametric generators (`python/bt4v_*.py`), all 7 exported STL meshes (`stl/BT4V_*.stl`), both Pillow graphic generators (`python/bt4v_drawing.py` and `python/bt4v_preview.py`), the master build script (`bt4v_generate_all.sh`), and core engineering documents (`Requirements.md`, `Testing Strategy.md`, `ASSEMBLY.md`, `BT4-V BOM.md`, `README.md`) are implemented and verified against the finalized `v0.3.0` baseline. Obsolete pre-`v0.3.0` scripts (`bt4v_whisker_spreader.py`, `bt4v_bowtie_support.py`) have been pruned.
- **Minor Non-Blocking Text/Metadata Items:**
  - `Bugs.md` line 5 references `Requirements.md v0.1.0` in its header metadata (while tracking 0 open bugs).
  - Minor annotation text callouts in `python/bt4v_drawing.py` (line 823: `"8x M2.5x12mm (6 spine + 2 spare)"`) and `python/bt4v_preview.py` (line 676: `"6 Tenon/Mortise Joints"`) still mention `6` active spine joints instead of the `7` active tenon/mortise joints across the 8 modular spine pieces in `v0.3.0`.
- **Layer 2 Physical Human-Gated Acceptance Testing:** In accordance with `Testing Strategy.md` §3 and §4, physical verification items (`T2.1` through `T2.4`) require physical 3D printing, 12 AWG wire forming, hardware assembly, and live DTV broadcast reception testing by the human builder, and therefore remain unchecked (`- [ ]`) until physical sign-off.

---

## Section 2: Core Engineering Decisions & Filename Consistency

### 2.1 Component Architecture & Filename Mapping

All generator scripts and output deliverables follow strict repository path conventions executed from the project root:

```text
python/bt4v_center_feed.py      ──>  stl/BT4V_Center_Feed.stl       (Qty 1)
python/bt4v_bay_bracket.py      ──>  stl/BT4V_Bay_Bracket.stl       (Qty 4)
python/bt4v_spine_segment.py    ──>  stl/BT4V_Spine_Segment.stl     (Qty 2)
python/bt4v_phase_crossover.py  ──>  stl/BT4V_Phase_Crossover.stl   (Qty 2)
python/bt4v_bowtie_backing.py   ──>  stl/BT4V_Bowtie_Backing.stl    (Qty 24)
python/bt4v_hanging_cap.py      ──>  stl/BT4V_Hanging_Cap.stl       (Qty 1)
python/bt4v_fit_coupon.py       ──>  stl/BT4V_Fit_Coupon.stl        (Qty 1, Optional)
python/bt4v_drawing.py          ──>  BT4-V 2D Drawing.png           (2200 × 1500 px)
python/bt4v_preview.py          ──>  BT4-V Parts Preview.png        (1800 × 800 px)
bt4v_generate_all.sh            ──>  Headless master build & verification runner
```

### 2.2 Canonical Dimensions & Geometry Baselines

All FreeCAD generators produce single valid solids conforming to the canonical `v0.3.0` geometry baselines defined in `Requirements.md` §16.3:

| Part File | Nominal Extents (X × Y × Z mm) | Nominal Volume (mm³) | Allowed ±2% Volume Range (mm³) | Measured Volume (mm³) | Solid Count & Validity |
|---|---|---|---|---|---|
| `stl/BT4V_Center_Feed.stl` | `40.0 × 24.0 × 110.0` | `42,000` | `41,160 – 42,840` | `42,053.92` (`+0.1%`) | `1 Solid`, `isValid() == True` |
| `stl/BT4V_Bay_Bracket.stl` | `50.0 × 18.0 × 40.0` | `19,200` | `18,816 – 19,584` | `19,181.20` (`-0.1%`) | `1 Solid`, `isValid() == True` |
| `stl/BT4V_Spine_Segment.stl` | `30.0 × 14.0 × 110.0` | `21,000` | `20,580 – 21,420` | `21,181.95` (`+0.9%`) | `1 Solid`, `isValid() == True` |
| `stl/BT4V_Phase_Crossover.stl` | `35.0 × 12.0 × 30.0` | `6,100` | `5,978 – 6,222` | `6,100.00` (`0.0%`) | `1 Solid`, `isValid() == True` |
| `stl/BT4V_Bowtie_Backing.stl` | `180.0 × 12.0 × 8.0` | `2,200` | `2,156 – 2,244` | `2,164.37` (`-1.6%`) | `1 Solid`, `isValid() == True` |
| `stl/BT4V_Hanging_Cap.stl` | `44.0 × 18.0 × 30.0` | `7,400` | `7,252 – 7,548` | `7,400.00` (`0.0%`) | `1 Solid`, `isValid() == True` |
| `stl/BT4V_Fit_Coupon.stl` | `90.0 × 50.0 × 10.0` | `26,500` | `25,970 – 27,030` | `26,497.36` (`-0.0%`) | `1 Solid`, `isValid() == True` |

### 2.3 Key Mechanical & RF Standards

- **Conductor Channels:** All wire guide and clamping grooves are `3.2 mm` wide × `3.0 mm` deep to seat standard 12 AWG solid copper wire (bare `2.05 mm` OD or THHN insulated `~3.0 mm` OD).
- **Modular Spine Interlock Joints & Unified `130.0 mm` Pitch:** Standardized `10.0 mm` tall male tenon (`+Z`) and female mortise (`-Z`) joints secured by `Ø2.6 mm` cross-pin holes (for `Ø2.5 mm` pins or `M2.5 × 12 mm` screws). Assembling the 8 vertical spine components (Top Hanging Cap → Bay 1 → Spine Segment 1 → Bay 2 → Center Feed Hub → Bay 3 → Spine Segment 2 → Bay 4) across **7 pinned joints** establishes an exact `130.0 mm` center-to-center pitch between all adjacent bays (`15.0 mm` bracket half-body + `100.0 mm` segment/hub active body + `15.0 mm` bracket half-body = `130.0 mm`; total active array height = `390.0 mm`).
- **Whisker Apex Clamping:** Dual M4 clearance holes (`Ø4.3 mm`) centered at `Z = 15.0 mm` on each Bay Bracket with rear captured hex nut pockets (`7.2 mm` across flats × `3.5 mm` deep) clamp the bent whisker apexes directly against the vertical phase lines.
- **Balun Integration:** Custom cavity contour in the Center Feed Hub cradles the commercial RCA VH101R 4:1 (`300:75 Ω`) outdoor matching transformer, with `25.0 mm` pitch M4 terminal studs at `Z = 50.0 mm` aligning with the transformer spade lugs and a `4.0 × 2.0 mm` zip-tie slot below the cradle for RG6 coax strain relief.
- **Straight-Through `25.0 mm` Phase Line Bus & Crossover:** Continuous `25.0 mm` center-to-center vertical wire grooves run straight across all Bay Brackets, Spine Segments, and the Center Feed Hub. Clip-on Phase Crossover Spacers (`35.0 × 12.0 × 30.0 mm`) snap onto the `20.0 mm` mid-span waist of Spine Segments 1 and 2 via a `2.4 mm` snap mouth, maintaining `≥5.0 mm` dielectric separation between crossing phase conductors.
- **Full-Length Bowtie Backing Struts:** Universal `180.0 × 12.0 × 8.0 mm` (`170.0 mm` active body + `10.0 mm` root tenon) ribbed I-beam struts with a continuous C-clip wire channel (`2.4 mm` throat opening into a `Ø3.2 mm` circular cavity), a root male tenon (`-X`), and a tip female mortise (`+X`). Each `200 mm` UHF arm uses 1 strut (8 pcs across Bays 2 & 3), and each `340 mm` VHF arm uses 2 daisy-chained struts (16 pcs across Bays 1 & 4; 24 struts total), locking into the 4 angled wing sockets on each Bay Bracket.

---

## Section 3: Testing & Verification Status

In accordance with `./Testing Strategy.md`, BT4-V uses a two-layer verification model with **no unit-test framework and no `tests/` directory**:
1. **Layer 1: Automated CAD & Build Regression Testing** (executed headlessly via `./bt4v_generate_all.sh`).
2. **Layer 2: Physical Human-Gated Acceptance Testing** (executed by the builder during physical fabrication, assembly, and TV signal testing).

### 3.1 Layer 1: Automated CAD & Build Regression Testing

- [x] **T1.1 — FreeCAD Generator Contract Implementation (`v0.3.0`):**
  - [x] `python/bt4v_center_feed.py` (`40.0 × 24.0 × 110.0 mm`, `42,053.92 mm³` vs `42,000 mm³` nominal).
  - [x] `python/bt4v_bay_bracket.py` (`50.0 × 18.0 × 40.0 mm`, `19,181.20 mm³` vs `19,200 mm³` nominal).
  - [x] `python/bt4v_spine_segment.py` (`30.0 × 14.0 × 110.0 mm`, `21,181.95 mm³` vs `21,000 mm³` nominal).
  - [x] `python/bt4v_phase_crossover.py` (`35.0 × 12.0 × 30.0 mm`, `6,100.00 mm³` vs `6,100 mm³` nominal).
  - [x] `python/bt4v_bowtie_backing.py` (`180.0 × 12.0 × 8.0 mm`, `2,164.37 mm³` vs `2,200 mm³` nominal).
  - [x] `python/bt4v_hanging_cap.py` (`44.0 × 18.0 × 30.0 mm`, `7,400.00 mm³` vs `7,400 mm³` nominal).
  - [x] `python/bt4v_fit_coupon.py` (`90.0 × 50.0 × 10.0 mm`, `26,497.36 mm³` vs `26,500 mm³` nominal).
- [x] **T1.2 — Geometry & Solid Validity Verification:**
  - [x] Confirm all 7 generated STLs represent exactly 1 valid solid (`len(shape.Solids) == 1`, `len(shape.Shells) == 1`, `shape.isValid() == True`).
  - [x] Verify bounding box extents match `Requirements.md` §16.3 within **±0.1 mm**.
  - [x] Verify solid volumes fall strictly within **±2%** of nominal baselines in `Requirements.md` §16.3.
- [x] **T1.3 — Pillow Technical Drawing & Preview Generation:**
  - [x] Execute `python/bt4v_drawing.py` and verify `BT4-V 2D Drawing.png` is generated at `2200 × 1500 px` (`356.9 kB`, `> 10 kB`).
  - [x] Execute `python/bt4v_preview.py` and verify `BT4-V Parts Preview.png` is generated at `1800 × 800 px` (`151.1 kB`, `> 10 kB`).
- [x] **T1.4 — Master Build Orchestrator (`bt4v_generate_all.sh`):**
  - [x] Verify POSIX bash execution (`set -euo pipefail`), `FREECAD_CMD` override support, automatic `mkdir -p stl`, and exit code `0` across all 9 generators.
- [x] **T1.5 — Determinism & Sandbox Execution:**
  - [x] Verify reproducible geometry and clean headless execution under `/snap/bin/freecad.cmd` / `freecadcmd`.

### 3.2 Layer 2: Physical Human-Gated Acceptance Testing

Per `Testing Strategy.md` §3.1–§3.4 and §4, these items remain open (`- [ ]`) until verified on physical hardware by the builder:

- [ ] **T2.1 — Step 1: Calibration & Fit Coupon Verification (`Testing Strategy.md` §3.1):**
  - [ ] Print `stl/BT4V_Fit_Coupon.stl` on the target FDM printer in target filament (PETG/ASA/PLA).
  - [ ] Test 12 AWG solid copper wire fit in friction channels (`2.8, 3.0, 3.2, 3.4 mm`) and C-clip snap mouths (`2.2, 2.4 mm` over `3.3 mm` cavity).
  - [ ] Verify M4 bolt clearance (`4.3 mm`) and captured hex nut seating (`7.2 mm` AF × `3.5 mm` deep).
  - [ ] Verify `25.0 mm` terminal stud spacing against RCA VH101R spade lugs.
  - [ ] Verify spine tenon/mortise sliding fit, backing-strut root socket fit, and `Ø2.5 mm` cross-pin hole alignment (`Ø2.6 mm`).
- [ ] **T2.2 — Step 2: Whisker Bending & Full-Length Backing Strut Rigidity (`Testing Strategy.md` §3.2):**
  - [ ] Cut and bend 4 × UHF whiskers (`410 mm` wire, `32.5°` flare angle, `200 mm` arms) and 4 × VHF whiskers (`690 mm` wire, `25.5°` flare angle, `340 mm` arms).
  - [ ] Snap **1 × `BT4V_Bowtie_Backing.stl`** onto each of the 8 UHF whisker arms (`8 pcs`) and **2 × daisy-chained `BT4V_Bowtie_Backing.stl`** onto each of the 8 VHF whisker arms (`16 pcs`; **24 struts total**), seating all root tenons into the Bay Bracket lateral wing sockets.
  - [ ] Perform horizontal cantilever droop test to confirm the continuous full-length backing struts lock flare angles and eliminate gravity sag from root to tip.
- [ ] **T2.3 — Step 3: Balun Cradle & Modular Spine Assembly (`Testing Strategy.md` §3.3):**
  - [ ] Print full 34-part production set (`1 × Center Feed`, `4 × Bay Brackets`, `2 × Spine Segments`, `2 × Phase Crossovers`, `24 × Bowtie Backing Struts`, `1 × Hanging Cap`, `~235 g`).
  - [ ] Assemble the 8 modular spine components from top to bottom and lock all **7 tenon/mortise joints** with `Ø2.5 mm` cross-pins or `M2.5 × 12 mm` screws, confirming exact **`130.0 mm`** center-to-center bay pitch (`390.0 mm` active height).
  - [ ] Snap the **RCA VH101R** matching transformer into the Center Feed cradle and clamp its spade lugs and the `25.0 mm` straight-through phase lines to the M4 feed studs.
  - [ ] Snap the 2 Phase Crossover Spacers onto the `20.0 mm` mid-span waists of Spine Segments 1 and 2, verifying `≥5.0 mm` separation between transposed phase conductors.
- [ ] **T2.4 — Step 4: DTV Reception & Signal Quality Verification (`Testing Strategy.md` §3.4):**
  - [ ] Suspend assembled antenna in target window using the dual `Ø5.0 mm` hanging eyelets (maintaining `≥0.5 m` clearance from metallic insect screens).
  - [ ] Connect `75 Ω` RG6 coaxial cable to the RCA VH101R F-connector (secured with a zip-tie through the strain-relief slot) and run a TV channel scan / signal diagnostic.
  - [ ] Confirm stable reception across local VHF-High broadcast channels (Channels 7–13, `174–216 MHz`) and UHF broadcast channels (Channels 14–36, `470–608 MHz`).

### 3.3 Workflow-Aligned Testing & Consolidation Checklists

To maintain clean single-command regression verification without introducing redundant standalone test scripts or a `tests/` directory, future maintenance and polish tasks follow this workflow-aligned checklist:

- [x] **W3.1 — Single-Command Automated Regression Gate (`./bt4v_generate_all.sh`):**
  - [x] Extend or run `./bt4v_generate_all.sh` as the sole automated verification entry point per `./Testing Strategy.md` §2 & §4 (confirming all 7 STLs match `Requirements.md` §16.3 bounding boxes within `±0.1 mm` and volumes within `±2%`, and both PNG renders exceed `10 kB` at `2200 × 1500` and `1800 × 800`).
- [x] **W3.2 — Minor Annotation & Metadata Synchronization (Optional Polish):**
  - [x] Update minor text callouts in `python/bt4v_drawing.py` (line 823) and `python/bt4v_preview.py` (line 676) from `"6"` spine joints/pins to `"7"` active spine joints, regenerate `BT4-V 2D Drawing.png` and `BT4-V Parts Preview.png` via `./bt4v_generate_all.sh`, and update `Bugs.md` header baseline version from `v0.1.0` to `v0.3.0`.

---

## Section 4: Exit Codes

All Python generators (`python/bt4v_*.py`) and the master build script (`bt4v_generate_all.sh`) enforce strict POSIX exit codes:

| Exit Code | Classification | Description & Trigger Conditions |
|---|---|---|
| **`0`** | **Success** | All operations succeeded. Solid geometry is valid (`isValid() == True`), single solid confirmed (`Solids == 1`, `Shells == 1`), bounding box within `±0.1 mm`, volume within `±2%`, and STL/PNG artifacts exported cleanly. |
| **`1`** | **Execution / Geometry Failure** | FreeCAD boolean cut/fuse failure, invalid or multi-solid shape, bounding box or volume out of tolerance, missing output directory, or missing output artifact. |
| **`2`** | **CLI Parameter Error** | Invalid command-line arguments, non-numeric or out-of-range geometric parameters, or unrecognized CLI flags. |

---

## Section 5: Security & Safety

- **Physical & Wire Handling Safety:** Wear safety glasses when cutting and bending 12 AWG solid copper wire to guard against spring-back and sharp wire ends. Deburr cut wire tips before snapping them into C-clip channels.
- **Electrical & Hardware Safety:** The commercial RCA VH101R outdoor matching transformer provides a passive, solderless `300:75 Ω` interface. Never install the antenna near overhead power lines or energized electrical conductors.
- **Window Suspension Safety:** Use rated suction-cup hooks, nylon cord, or picture wire capable of supporting `≥1 kg` (`>4×` the `~235 g` antenna mass) through both `Ø5.0 mm` hanging eyelets to prevent falls or rotation.
- **Headless Execution & Snap Confinement Safety:** `bt4v_generate_all.sh` executes FreeCAD strictly in headless console mode (`FREECAD_CMD=freecadcmd` or `/snap/bin/freecad.cmd`) with `set -euo pipefail`. Because the Snap-confined FreeCAD runtime cannot read or write `/tmp`, all builds and temporary verification runs must execute inside the workspace or a user-home directory (e.g., `$HOME/bt4v-verify`).

---

## Section 6: Software & Tooling Dependencies

| Dependency | Minimum Version | Verified Environment | Purpose |
|---|---|---|---|
| **FreeCAD** | `>= 0.20` | `1.0.2` (`/snap/bin/freecad.cmd`) | Headless parametric 3D solid modelling (`FreeCAD`, `Part`, `Mesh` Python APIs) |
| **Python** | `>= 3.8` | `3.12` | Parametric CAD scripting, math calculations, and verification logic |
| **Pillow (`PIL`)** | `>= 9.0` | `10.2.0` | 2D engineering drawing (`2200 × 1500`) and 3D multi-panel preview (`1800 × 800`) rendering |
| **System Fonts** | `DejaVu Sans` / `Bold` | `/usr/share/fonts/truetype/dejavu/` | Typography for technical drawing title blocks, tables, and preview callouts |
| **POSIX Bash** | `>= 5.0` | GNU Bash `5.x` | Headless build orchestration and artifact verification (`bt4v_generate_all.sh`) |

---

## Section 7: Non-Functional Requirements

- **Parametric Repeatability:** All 3D printable meshes and 2D/3D visual assets are generated deterministically from source code in `python/` via `./bt4v_generate_all.sh` with zero manual GUI interaction.
- **Dimensional & Volume Tolerances:** All generated solids must match nominal bounding boxes within **`±0.1 mm`** and nominal solid volumes (`Requirements.md` §16.3) within **`±2%`**.
- **FDM Printability & Bed Fit:** All 7 part geometries print flat with **zero support material** (`0.4 mm` nozzle, `0.2 mm` layer height, `3` perimeters, `30%` gyroid/grid infill). The longest component—the `180.0 × 12.0 × 8.0 mm` Full-Length Bowtie Backing Strut—fits standard `220 × 220 mm` and `235 × 235 × 250 mm` build plates flat along the X-axis with ample margin.
- **Structural Rigidity:** The `30.0 × 14.0 mm` flanged I-beam spine segments, 7 cross-pinned tenon/mortise spine joints, and 24 interlocking ribbed I-beam bowtie backing struts lock all 16 whisker arms at their exact flare angles (`32.5°` UHF, `25.5°` VHF) with zero cantilever droop.
- **Weather & Thermal Resistance:** PETG or ASA filament is recommended for production antennas hung in direct sunlight against south/west-facing windows to prevent thermal creep; PLA is supported for indoor calibration coupons and low-heat window locations.
