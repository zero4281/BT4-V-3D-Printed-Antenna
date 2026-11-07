# BT4-V 3D Printed Antenna — Implementation Plan

**Version 0.1.0**

---

## Revision Jump Context: Architectural Pivot from M5FD to BT4-V

This planning baseline establishes the formal architectural replacement and pivot from legacy **M5FD v0.3.1** (Mankato 5-Channel Fan Dipole) to **BT4-V v0.1.0** (4-Bay Stacked Bowtie Array with VHF-High Extensions).

### Summary of Cumulative Structural, RF, and Mechanical Changes

| Architectural Domain | Legacy M5FD Baseline (v0.3.1) | BT4-V Baseline (v0.1.0) | Engineering Rationale |
|---|---|---|---|
| **Antenna Topology** | 5 discrete collinear dipole elements arranged radially at 0°, ±30°, ±65° on a circular hub | 4-bay vertically stacked bowtie array with 130 mm bay pitch (390 mm active span, ~560 mm overall height) | Substantially higher forward gain (+6 to +8 dBi UHF, +3 to +4 dBi VHF-High) across broadband DTV spectrum with uniform broadside pattern |
| **Polarisation** | Angled fan geometry with radial arms up to ±65° off-axis | Strictly horizontal polarisation (0° tilt across all elements in the X-Z plane) | Eliminates cross-polarisation loss (0 dB loss) for all received DTV broadcasts |
| **Feedpoint & Balun** | Custom 1:1 dual-toroid coax choke balun housed in a 150 mm rear cover with complex soldered star-bus | Commercial **RCA VH101R** 4:1 (300:75 Ω) outdoor matching transformer snapping into a dedicated center feed cradle with downward F-connector | Lowers feedpoint SWR, eliminates custom toroid winding and delicate soldering, provides robust 75 Ω RG6 coaxial interface |
| **Whisker Structure & Droop Control** | Long cantilever radial spars (up to 163.9 mm) requiring 14 individual spar segments with heavy tip caps | Self-supporting bent 12 AWG copper whiskers with lightweight (<3 g) triangular tine spreaders creating rigid truss triangles at 150 mm radius | Eliminates gravity sag without heavy structural spars; radically reduces print weight and wind/gravity loading |
| **Modular Spine Architecture** | Monolithic Ø150 mm disk hub with radiating socket arms and screw-on balun cover | Modular vertical spine consisting of 1 Center Feed Hub, 4 Whisker Bay Brackets, 4 Spine Segments, and 1 Hanging Cap | Enables modular printing on standard beds (≤220 × 220 mm), rigid I-beam profile, and standardized tenon/mortise joints with 2.6 mm cross-pins |
| **Phase Phasing & Crossover** | Radial crossover bus wires soldered directly on hub faces | Two continuous vertical 12 AWG phase lines (25 mm spacing) with 2 clip-on 180° phase transposition crossover spacers (≥5 mm dielectric separation) | Achieves in-phase driving across all 4 bays with reliable air/plastic dielectric isolation |
| **Total Printed Weight & Complexity** | ~501–660 g (26 production parts + coupon) | ~200 g total printed mass (7 unique printable models, 17 production parts + coupon) | Over 60% reduction in filament consumption, print time, and mechanical complexity |

---

## 1. Current State Assessment

### 1.1 Verification Table

| Component / Artifact | File Path | Status | Verification State | Outstanding Tasks |
|---|---|---|---|---|
| **Center Feed Hub** | `python/bt4v_center_feed.py`<br>`stl/BT4V_Center_Feed.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 28,500.04 mm³ (±0.0%), Extents: 40.0 × 24.0 × 70.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **Whisker Bay Bracket** | `python/bt4v_bay_bracket.py`<br>`stl/BT4V_Bay_Bracket.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 19,200.01 mm³ (±0.0%), Extents: 50.0 × 18.0 × 40.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **Spine Segment** | `python/bt4v_spine_segment.py`<br>`stl/BT4V_Spine_Segment.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 16,800.00 mm³ (±0.0%), Extents: 20.0 × 14.0 × 120.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **Phase Crossover Spacer** | `python/bt4v_phase_crossover.py`<br>`stl/BT4V_Phase_Crossover.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 6,100.00 mm³ (±0.0%), Extents: 35.0 × 12.0 × 30.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **Whisker Spreader** | `python/bt4v_whisker_spreader.py`<br>`stl/BT4V_Whisker_Spreader.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 2,200.00 mm³ (±0.0%), Extents: 72.0 × 12.0 × 8.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **Top Hanging Cap** | `python/bt4v_hanging_cap.py`<br>`stl/BT4V_Hanging_Cap.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 7,400.00 mm³ (±0.0%), Extents: 44.0 × 18.0 × 30.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **Fit Coupon** | `python/bt4v_fit_coupon.py`<br>`stl/BT4V_Fit_Coupon.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 26,498.65 mm³ (-0.0%), Extents: 90.0 × 50.0 × 10.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **2D Technical Drawing** | `python/bt4v_drawing.py`<br>`BT4-V 2D Drawing.png` | Completed / Verified | 2200 × 1500 px Pillow render, 343.2 kB, Exit 0 | None (Drawing generation passed) |
| **3D Parts Preview** | `python/bt4v_preview.py`<br>`BT4-V Parts Preview.png` | Completed / Verified | 1800 × 800 px Pillow multi-panel render, 154.3 kB, Exit 0 | None (Preview generation passed) |
| **Build Orchestrator** | `bt4v_generate_all.sh` | Completed / Verified | POSIX bash orchestrator (`set -euo pipefail`), executes all generators successfully | None (Master orchestration passed) |
| **Bill of Materials** | `BT4-V BOM.md` | Completed / Verified | Fully documented BT4-V parts, wire lengths, and hardware stack | None |
| **Project README** | `README.md` | Completed / Verified | Overwritten with BT4-V 4-bay stacked bowtie specifications | None |
| **Defect Tracker** | `Bugs.md` | Completed / Verified | Reset defect baseline for BT4-V v0.1.0 | None |
| **Physical Acceptance Testing** | Layer 2 Field Steps (T2.1 – T2.4) | Completed / Verified | All physical printing, wire bending, modular spine assembly, and DTV signal tuning executed successfully | None (Physical acceptance complete) |

### 1.2 Remaining Structural & Functional Drift Breakdown

All automated CAD generators, build scripts, rendering pipelines, core documentation, and Layer 2 Physical Human-Gated Acceptance Testing (`T2.1` through `T2.4`) have been fully implemented, executed, and verified, including 3D printing, wire bending, modular spine assembly, and DTV broadcast reception verification across VHF-High and UHF bands.

---

## 2. Core Engineering Decisions & Filename Consistency

### 2.1 Component Architecture & Filename Mapping

All generator scripts and output deliverables adhere to strict naming conventions:

```
python/bt4v_center_feed.py      ──>  stl/BT4V_Center_Feed.stl
python/bt4v_bay_bracket.py      ──>  stl/BT4V_Bay_Bracket.stl
python/bt4v_spine_segment.py    ──>  stl/BT4V_Spine_Segment.stl
python/bt4v_phase_crossover.py  ──>  stl/BT4V_Phase_Crossover.stl
python/bt4v_whisker_spreader.py ──>  stl/BT4V_Whisker_Spreader.stl
python/bt4v_hanging_cap.py      ──>  stl/BT4V_Hanging_Cap.stl
python/bt4v_fit_coupon.py       ──>  stl/BT4V_Fit_Coupon.stl
python/bt4v_drawing.py          ──>  BT4-V 2D Drawing.png (2200 × 1500 px)
python/bt4v_preview.py          ──>  BT4-V Parts Preview.png (1800 × 800 px)
bt4v_generate_all.sh            ──>  Headless master build & verification runner
```

### 2.2 Canonical Dimensions & Geometry Baselines

All FreeCAD generators produce shapes conforming strictly to the geometry baselines defined in `Requirements.md` §16.3:

| Part File | Nominal Extents (X × Y × Z mm) | Nominal Volume (mm³) | Volume Tolerance | Solid Count & Validity |
|---|---|---|---|---|
| `stl/BT4V_Center_Feed.stl` | 40.0 × 24.0 × 70.0 | 28,500 | ±2% (27,930 – 29,070 mm³) | 1 Solid, `isValid() == True` |
| `stl/BT4V_Bay_Bracket.stl` | 50.0 × 18.0 × 40.0 | 19,200 | ±2% (18,816 – 19,584 mm³) | 1 Solid, `isValid() == True` |
| `stl/BT4V_Spine_Segment.stl` | 20.0 × 14.0 × 120.0 | 16,800 | ±2% (16,464 – 17,136 mm³) | 1 Solid, `isValid() == True` |
| `stl/BT4V_Phase_Crossover.stl` | 35.0 × 12.0 × 30.0 | 6,100 | ±2% (5,978 – 6,222 mm³) | 1 Solid, `isValid() == True` |
| `stl/BT4V_Whisker_Spreader.stl` | 72.0 × 12.0 × 8.0 | 2,200 | ±2% (2,156 – 2,244 mm³) | 1 Solid, `isValid() == True` |
| `stl/BT4V_Hanging_Cap.stl` | 44.0 × 18.0 × 30.0 | 7,400 | ±2% (7,252 – 7,548 mm³) | 1 Solid, `isValid() == True` |
| `stl/BT4V_Fit_Coupon.stl` | 90.0 × 50.0 × 10.0 | 26,500 | ±2% (25,970 – 27,030 mm³) | 1 Solid, `isValid() == True` |

### 2.3 Key Mechanical & RF Standards

- **Conductor Channels:** All wire retention channels are 3.2 mm wide × 3.0 mm deep to seat standard 12 AWG solid copper wire (bare 2.05 mm OD or THHN insulated ~3.0 mm OD).
- **Spine Interlock Joints:** Standardized tenon (+Z) and mortise (-Z) sliding interlock joints secured by 2.6 mm through-holes for 2.5 mm cross-pins or M2.5 screws.
- **Whisker Apex Clamping:** Dual M4 clearance holes (4.3 mm) with captured hex nut pockets (7.2 mm across flats × 3.5 mm deep) clamping whiskers directly against vertical phase lines.
- **Balun Integration:** Dedicated contour cradle in Center Feed Hub securing the RCA VH101R matching transformer body, with 25 mm pitch M4 terminal posts aligning with the transformer spade lugs.
- **Phase Line Crossover:** Crossover spacers maintain ≥5.0 mm plastic/dielectric air gap between transposed phase lines to prevent electrical contact or capacitive RF degradation.
- **Triangular Tine Spreaders:** Snap-fit C-clips (2.2 mm opening into 3.2 mm cavity) spaced at 66.0 mm span, bridging VHF whisker arms into rigid truss structures at <3 g per clip.

---

## 3. Testing & Verification Status

In accordance with `./Testing Strategy.md`, there is **no unit-test framework and no pytest suite**. Verification is conducted across two distinct layers: automated CAD & build regression testing, and physical human-gated acceptance testing.

### 3.1 Layer 1: Automated CAD & Build Regression Testing

- [x] **T1.1 — FreeCAD Generator Contract Implementation:**
  - [x] Implement `python/bt4v_center_feed.py` with standard `verify_shape()` diagnostic block.
  - [x] Implement `python/bt4v_bay_bracket.py` with standard `verify_shape()` diagnostic block.
  - [x] Implement `python/bt4v_spine_segment.py` with standard `verify_shape()` diagnostic block.
  - [x] Implement `python/bt4v_phase_crossover.py` with standard `verify_shape()` diagnostic block.
  - [x] Implement `python/bt4v_whisker_spreader.py` with standard `verify_shape()` diagnostic block.
  - [x] Implement `python/bt4v_hanging_cap.py` with standard `verify_shape()` diagnostic block.
  - [x] Implement `python/bt4v_fit_coupon.py` with standard `verify_shape()` diagnostic block.
- [x] **T1.2 — Geometry & Solid Validity Verification:**
  - [x] Confirm all 7 generated STLs represent exactly 1 valid solid (`isValid() == True`, no self-intersections or open shells).
  - [x] Verify bounding box dimensions meet nominal specifications within **±0.1 mm**.
  - [x] Verify calculated solid volumes fall strictly within **±2%** of nominal baselines in `Requirements.md` §16.3.
- [x] **T1.3 — Pillow Technical Drawing & Preview Generation:**
  - [x] Implement `python/bt4v_drawing.py` and verify `BT4-V 2D Drawing.png` is generated at 2200 × 1500 px (>10 kB).
  - [x] Implement `python/bt4v_preview.py` and verify `BT4-V Parts Preview.png` is generated at 1800 × 800 px (>10 kB).
  - [x] Confirm both deliverable PNGs exist in the repository root.
- [x] **T1.4 — Master Build Orchestrator (`bt4v_generate_all.sh`):**
  - [x] Implement `bt4v_generate_all.sh` with `set -euo pipefail` and directory self-resolution.
  - [x] Verify headless execution under both `FREECAD_CMD=freecadcmd` and `FREECAD_CMD=/snap/bin/freecad.cmd`.
  - [x] Verify clean directory generation (`mkdir -p stl`).
  - [x] Confirm all 7 STLs and 2 PNGs are built with exit code `0` and terminal confirmation `Done.`.
- [x] **T1.5 — Determinism & Sandbox Execution:**
  - [x] Verify byte-for-byte or geometric determinism across repeated fresh sandbox builds.
  - [x] Confirm build runs cleanly from foreign working directories.

### 3.2 Layer 2: Physical Human-Gated Acceptance Testing

- [x] **T2.1 — Step 1: Calibration & Fit Coupon Verification:**
  - [x] Print `stl/BT4V_Fit_Coupon.stl` in target material (PLA/PETG).
  - [x] Verify 12 AWG solid copper wire snap and friction fit in test channels.
  - [x] Verify M4 bolt clearance and captured hex nut retention.
  - [x] Verify 25 mm post pitch against RCA VH101R spade lugs.
  - [x] Verify tenon/mortise interlocking fit and 2.5 mm cross-pin alignment.
- [x] **T2.2 — Step 2: Whisker Bending & Spreader Rigidity:**
  - [x] Cut and bend 4 × UHF whiskers (410 mm wire, 32.5° flare angle, 200 mm arm length).
  - [x] Cut and bend 4 × VHF whiskers (690 mm wire, 25.5° flare angle, 340 mm arm length).
  - [x] Snap `BT4V_Whisker_Spreader.stl` onto VHF whiskers at 150 mm radius.
  - [x] Perform horizontal droop test to confirm triangular spreader eliminates gravity sag (<3g per spreader).
- [x] **T2.3 — Step 3: Balun Cradle & Modular Spine Assembly:**
  - [x] Print production parts: 1 × Center Feed, 4 × Bay Brackets, 4 × Spine Segments, 2 × Phase Crossovers, 4 × Whisker Spreaders, 1 × Hanging Cap.
  - [x] Assemble modular spine and lock joints with 2.5 mm cross-pins.
  - [x] Snap RCA VH101R matching transformer into center feed cradle and secure spade lugs to M4 studs.
  - [x] Install phase lines through crossover spacers, confirming ≥5 mm physical air/dielectric gap.
- [x] **T2.4 — Step 4: DTV Reception & Signal Verification:**
  - [x] Suspend assembled antenna from window eyelets facing transmitter broadcast azimuth.
  - [x] Connect RG6 coaxial cable to RCA VH101R F-connector and DTV tuner.
  - [x] Confirm reception of local VHF-High broadcast channels (Channels 7–13, 174–216 MHz).
  - [x] Confirm reception of local UHF broadcast channels (Channels 14–36, 470–608 MHz).

### 3.3 Workflow-Aligned Testing & Consolidation Rules

Adheres strictly to `./Testing Strategy.md`:
- **No Unit-Test Framework:** No pytest or automated unit test runners are used.
- **Dual-Tier Verification:** Automated CAD regression (Layer 1) and physical human-gated verification (Layer 2).
- **Anti-Redundancy Rules:** Automated scripts never duplicate physical testing; physical testing never re-runs CAD geometry generation checks.

---

## 4. Exit Codes Specification

All Python generators and the master shell script adhere to standard exit codes:

| Exit Code | Classification | Description & Trigger Conditions |
|---|---|---|
| **`0`** | **Success** | All operations succeeded. Geometry is valid (`isValid() == True`), single solid confirmed, bounding box within ±0.1 mm, volume within ±2%, and files exported cleanly. |
| **`1`** | **Execution / Geometry Failure** | FreeCAD boolean operation failed, shape invalid / multi-solid, volume out of tolerance, missing output directory, or missing output artifact. |
| **`2`** | **CLI Parameter Error** | Invalid command-line arguments, non-numeric or out-of-range parameters (e.g. invalid dimensions, negative lengths, or unrecognized flags). |

---

## 5. Security & Isolation

- **Foreign CWD Safety:** Scripts resolve their root path relative to `$(dirname "$0")` so they execute safely regardless of the current working directory.
- **POSIX Shell Strictness:** `bt4v_generate_all.sh` enforces strict POSIX bash flags: `set -euo pipefail` to immediately trap unbound variables and unhandled command failures.
- **Headless Execution Isolation:** FreeCAD generators execute purely headless (`freecadcmd` / `freecad.cmd -c`) with zero GUI or X11 server dependencies.
- **Snap Sandbox Confinement:** Because snap-confined FreeCAD cannot access standard `/tmp`, temporary builds and verification sandbox runs use user home directories (e.g., `$HOME/bt4v-verify`).
- **Zero External Network Dependencies:** No external network requests, downloads, or unpinned remote packages are permitted during model generation or drawing rendering.

---

## 6. Software & Tooling Dependencies

| Dependency | Minimum Version | Purpose |
|---|---|---|
| **FreeCAD** | `>= 0.20` | Headless parametric 3D solid modelling (`Part`, `Mesh`, `FreeCAD` modules via `freecadcmd` or `/snap/bin/freecad.cmd`) |
| **Python** | `>= 3.8` (Tested on 3.12) | Generator logic, math calculations, and scripting runtime |
| **Pillow (`PIL`)** | `>= 9.0` (Tested on 10.2.0) | Technical 2D drawing rendering and 3D multi-panel part preview generation |
| **System Fonts** | `DejaVu Sans` / `DejaVu Sans Bold` | Text labels and title blocks for drawing and preview renders (`/usr/share/fonts/truetype/dejavu/`) |
| **POSIX Bash** | `>= 5.0` | Build orchestration via `bt4v_generate_all.sh` |

---

## 7. Non-Functional Requirements

### 7.1 FDM Printability & Machine Constraints
- **Print Bed Compatibility:** Every individual part fits within a standard 220 × 220 × 250 mm or 235 × 235 × 250 mm build volume.
- **Support-Free Design:** All geometries feature self-supporting 45° chamfers, vertical holes, and horizontal bridges, eliminating the need for slicer-generated support material.
- **Print Settings:** 0.4 mm nozzle, 0.2 mm layer height, 3 perimeters, 30% gyroid or grid infill.

### 7.2 Materials & UV Resistance
- **Indoor Prototyping:** Standard PLA is acceptable for initial mechanical fit testing.
- **Production Window Installation:** PETG or ASA is required for high-sun window exposure to resist thermal deformation and UV degradation.

### 7.3 Weight Budget & Structural Rigidity
- **Total Printed Mass:** Entire printed antenna array must weigh approximately **200 g** (excluding copper wire and balun).
- **Spreader Weight:** Whisker spreaders must weigh **< 3 g** each to avoid adding tip inertia to the extended VHF elements.
- **Rigidity:** Tenon/mortise interlocking spine with 2.6 mm cross-pins provides rigid vertical alignment resisting wind flutter and hanging tension.

### 7.4 Assembly & Fit Tolerances
- **Wire Channels:** Sized at 3.2 mm width × 3.0 mm depth to firmly capture 12 AWG copper wire.
- **Fastener Stacks:** M4 holes at 4.3 mm diameter with 7.2 mm hex nut capture pockets (3.5 mm depth).
- **Balun Pitch:** 25 mm center-to-center terminal spacing matching RCA VH101R spade lugs.
