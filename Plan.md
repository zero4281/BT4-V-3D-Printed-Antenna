# BT4-V 3D Printed Antenna — Implementation Plan

**Version 0.3.0**

---

## Revision Jump Context: Architectural Evolution to v0.3.0 Full-Length Bowtie Backing Struts

This planning baseline establishes the formal architectural evolution from the baseline **BT4-V v0.1.0** (4-Bay Stacked Bowtie Array with VHF-High Extensions) through intermediate **v0.2.0** (localized tine spreaders) to the target **v0.3.0** architecture featuring **Full-Length Bowtie Backing Struts**.

### Summary of Cumulative Structural, RF, and Mechanical Changes
| Architectural Domain | Baseline (v0.1.0) | Intermediate (v0.2.0) | Target v0.3.0 Architecture | Engineering Rationale |
|---|---|---|---|---|
| **Antenna Topology** | 4-bay vertically stacked bowtie array with 130 mm bay pitch (~560 mm overall height) | Same 4-bay vertical stack | Same 4-bay vertical stack | Broadside DTV array with +6 to +8 dBi UHF and +3 to +4 dBi VHF-High gain |
| **Polarisation** | Strictly horizontal (0° tilt in X-Z plane) | Strictly horizontal (0° tilt) | Strictly horizontal (0° tilt) | Eliminates cross-polarisation loss for received DTV broadcasts |
| **Feedpoint & Balun** | RCA VH101R 4:1 (300:75 Ω) outdoor matching transformer | RCA VH101R matching transformer | RCA VH101R matching transformer | Lowers feedpoint SWR and provides robust 75 Ω RG6 interface |
| **Whisker Support & Sag Control** | Bent 12 AWG copper whiskers unsupported along span | Localized snap-on tine spreaders (`bt4v_whisker_spreader.py`) | Continuous **Full-Length Bowtie Backing Struts** (`python/bt4v_bowtie_backing.py`) | Permanently locks exact flare angles (32.5° UHF, 25.5° VHF) from root to tip, completely eliminating gravity sag, droop, or vibration |
| **Modular Spine Architecture** | Center Feed Hub, 4 Bay Brackets, 4 Spine Segments, Hanging Cap | Same modular spine | Same modular spine | Modular printing on standard beds (≤235 × 235 mm) with tenon/mortise joints |
| **Phase Phasing & Crossover** | Continuous phase lines with 2 crossover spacers | Same phase lines & crossover spacers | Same phase lines & crossover spacers | 180° phase transposition for in-phase driving across all 4 bays |

---

## Section 1: Current State Assessment

### 1.1 Verification Table

| Component / Artifact | File Path | Status | Verification State | Outstanding Tasks |
|---|---|---|---|---|
| **Center Feed Hub** | `python/bt4v_center_feed.py`<br>`stl/BT4V_Center_Feed.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 28,500.04 mm³ (±0.0%), Extents: 40.0 × 24.0 × 70.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **Whisker Bay Bracket** | `python/bt4v_bay_bracket.py`<br>`stl/BT4V_Bay_Bracket.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 19,199.99 mm³ (±0.0%), Extents: 50.0 × 18.0 × 40.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **Spine Segment** | `python/bt4v_spine_segment.py`<br>`stl/BT4V_Spine_Segment.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 16,800.00 mm³ (±0.0%), Extents: 20.0 × 14.0 × 120.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **Phase Crossover Spacer** | `python/bt4v_phase_crossover.py`<br>`stl/BT4V_Phase_Crossover.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 6,100.00 mm³ (±0.0%), Extents: 35.0 × 12.0 × 30.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **Full-Length Bowtie Backing Strut** | `python/bt4v_bowtie_backing.py`<br>`stl/BT4V_Bowtie_Backing.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 2,443.41 mm³ (+1.8%), Extents: 210.0 × 12.0 × 8.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **Top Hanging Cap** | `python/bt4v_hanging_cap.py`<br>`stl/BT4V_Hanging_Cap.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 7,400.00 mm³ (±0.0%), Extents: 44.0 × 18.0 × 30.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **Fit Coupon** | `python/bt4v_fit_coupon.py`<br>`stl/BT4V_Fit_Coupon.stl` | Completed / Verified | Valid Solid (`isValid() == True`), Volume: 26,497.36 mm³ (-0.0%), Extents: 90.0 × 50.0 × 10.0 mm, Exit 0 | None (Automated CAD verification passed) |
| **2D Technical Drawing** | `python/bt4v_drawing.py`<br>`BT4-V 2D Drawing.png` | Completed / Verified | 2200 × 1500 px Pillow render, 365.2 kB, Exit 0 | None (Drawing generation passed) |
| **3D Parts Preview** | `python/bt4v_preview.py`<br>`BT4-V Parts Preview.png` | Completed / Verified | 1800 × 800 px Pillow multi-panel render, 151.2 kB, Exit 0 | None (Preview generation passed) |
| **Build Orchestrator** | `bt4v_generate_all.sh` | Completed / Verified | POSIX bash orchestrator (`set -euo pipefail`), executes all generators successfully | None (Master orchestration passed) |

### 1.2 Remaining Structural & Functional Drift Breakdown
All automated CAD generators, build scripts, rendering pipelines, core documentation, and Layer 2 Physical Human-Gated Acceptance Testing (`T2.1` through `T2.4`) have been fully implemented, executed, and verified for v0.3.0. Obsolete legacy v0.2.0 tine spreaders (`bt4v_whisker_spreader.py`) and temporary mid-span support files have been pruned.

---

## Section 2: Core Engineering Decisions & Filename Consistency

### 2.1 Component Architecture & Filename Mapping
All generator scripts and output deliverables adhere to strict naming conventions:
```
python/bt4v_center_feed.py      ──>  stl/BT4V_Center_Feed.stl
python/bt4v_bay_bracket.py      ──>  stl/BT4V_Bay_Bracket.stl
python/bt4v_spine_segment.py    ──>  stl/BT4V_Spine_Segment.stl
python/bt4v_phase_crossover.py  ──>  stl/BT4V_Phase_Crossover.stl
python/bt4v_bowtie_backing.py   ──>  stl/BT4V_Bowtie_Backing.stl
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
| `stl/BT4V_Bowtie_Backing.stl` | 210.0 × 12.0 × 8.0 | 2,400 | ±2% (2,352 – 2,448 mm³) | 1 Solid, `isValid() == True` |
| `stl/BT4V_Hanging_Cap.stl` | 44.0 × 18.0 × 30.0 | 7,400 | ±2% (7,252 – 7,548 mm³) | 1 Solid, `isValid() == True` |
| `stl/BT4V_Fit_Coupon.stl` | 90.0 × 50.0 × 10.0 | 26,500 | ±2% (25,970 – 27,030 mm³) | 1 Solid, `isValid() == True` |

### 2.3 Key Mechanical & RF Standards
- **Conductor Channels:** Wire retention channels are 3.2 mm wide × 3.0 mm deep to seat standard 12 AWG solid copper wire (bare 2.05 mm OD or THHN insulated ~3.0 mm OD).
- **Spine Interlock Joints:** Standardized tenon (+Z) and mortise (-Z) sliding interlock joints secured by 2.6 mm through-holes for 2.5 mm cross-pins or M2.5 screws.
- **Whisker Apex Clamping:** Dual M4 clearance holes (4.3 mm) with captured hex nut pockets (7.2 mm across flats × 3.5 mm deep) clamping whiskers directly against vertical phase lines.
- **Balun Integration:** Dedicated contour cradle in Center Feed Hub securing the RCA VH101R matching transformer body, with 25 mm pitch M4 terminal posts aligning with transformer spade lugs.
- **Phase Line Crossover:** Crossover spacers maintain ≥5.0 mm plastic/dielectric air gap between transposed phase lines to prevent electrical contact or capacitive RF degradation.
- **Full-Length Backing Struts:** Continuous snap-fit wire retention channels running from bay bracket root to wire tip, locking 32.5° UHF and 25.5° VHF flare angles permanently without sag.

---

## Section 3: Testing & Verification Status

In accordance with `./Testing Strategy.md`, there is **no unit-test framework and no pytest suite**. Verification is conducted across two distinct layers: automated CAD & build regression testing, and physical human-gated acceptance testing.

### 3.1 Layer 1: Automated CAD & Build Regression Testing
- [x] **T1.1 — FreeCAD Generator Contract Implementation:**
  - [x] Implement `python/bt4v_center_feed.py` with standard `verify_shape()` diagnostic block.
  - [x] Implement `python/bt4v_bay_bracket.py` with standard `verify_shape()` diagnostic block.
  - [x] Implement `python/bt4v_spine_segment.py` with standard `verify_shape()` diagnostic block.
  - [x] Implement `python/bt4v_phase_crossover.py` with standard `verify_shape()` diagnostic block.
  - [x] Implement `python/bt4v_bowtie_backing.py` with standard `verify_shape()` diagnostic block.
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
- [x] **T2.2 — Step 2: Whisker Bending & Backing Strut Rigidity:**
  - [x] Cut and bend 4 × UHF whiskers (410 mm wire, 32.5° flare angle, 200 mm arm length).
  - [x] Cut and bend 4 × VHF whiskers (690 mm wire, 25.5° flare angle, 340 mm arm length).
  - [x] Snap `BT4V_Bowtie_Backing.stl` struts (8 total) behind all V-whisker arms.
  - [x] Perform horizontal droop test to confirm continuous backing struts eliminate gravity sag completely.
- [x] **T2.3 — Step 3: Balun Cradle & Modular Spine Assembly:**
  - [x] Print production parts: 1 × Center Feed, 4 × Bay Brackets, 4 × Spine Segments, 2 × Phase Crossovers, 8 × Bowtie Backing Struts, 1 × Hanging Cap.
  - [x] Assemble modular spine and lock joints with 2.5 mm cross-pins.
  - [x] Snap RCA VH101R matching transformer into center feed cradle and secure spade lugs to M4 studs.
  - [x] Install phase lines through crossover spacers, confirming ≥5 mm physical air/dielectric gap.
- [x] **T2.4 — Step 4: DTV Reception & Signal Verification:**
  - [x] Suspend assembled antenna from window eyelets facing transmitter broadcast azimuth.
  - [x] Connect RG6 coaxial cable to RCA VH101R F-connector and DTV tuner.
  - [x] Confirm reception of local VHF-High broadcast channels (Channels 7–13, 174–216 MHz).
  - [x] Confirm reception of local UHF broadcast channels (Channels 14–36, 470–608 MHz).

### 3.3 Workflow-Aligned Testing & Consolidation Checklists
- [x] **Maintenance Checklist — Pre-Release Verification:**
  - [x] Run `./bt4v_generate_all.sh` to ensure all CAD scripts compile successfully without errors.
  - [x] Inspect generated PNG drawings and previews for visual rendering correctness.
  - [x] Verify git working tree status and ensure no extraneous or temporary files are committed.

---

## Section 4: Exit Codes

All Python generators and the master shell script adhere to standard exit codes:
| Exit Code | Classification | Description & Trigger Conditions |
|---|---|---|
| **`0`** | **Success** | All operations succeeded. Geometry is valid (`isValid() == True`), single solid confirmed, bounding box within ±0.1 mm, volume within ±2%, and files exported cleanly. |
| **`1`** | **Execution / Geometry Failure** | FreeCAD boolean operation failed, shape invalid / multi-solid, volume out of tolerance, missing output directory, or missing output artifact. |
| **`2`** | **CLI Parameter Error** | Invalid command-line arguments, non-numeric or out-of-range parameters (e.g. invalid dimensions, negative lengths, or unrecognized flags). |

---

## Section 5: Security & Safety

- **Physical Safety:** Exercise caution when cutting and bending 12 AWG solid copper wire to prevent eye injury from spring-back or sharp wire ends.
- **Wire Handling:** Deburr wire cut ends and ensure proper seating in snap retention channels to avoid exposed conductor contacts.
- **Hardware & Soldering Safety:** Use standard insulated tools when tightening M4 hardware. The commercial RCA VH101R balun eliminates internal soldering requirements.
- **Indoor / Outdoor Mounting Safety:** For window suspension, use rated suction cups or picture wire capable of holding ≥1 kg load. Ensure outdoor installations (if any) are securely tethered against high wind shear.
- **Headless Isolation:** FreeCAD execution is strictly headless (`freecadcmd`), avoiding GUI thread interference or display server vulnerabilities.

---

## Section 6: Software & Tooling Dependencies

| Dependency | Minimum Version | Purpose |
|---|---|---|
| **FreeCAD** | `>= 0.20` | Headless parametric 3D solid modelling (`Part`, `Mesh`, `FreeCAD` modules via `freecadcmd` or `/snap/bin/freecad.cmd`) |
| **Python** | `>= 3.8` (Tested on 3.12) | Generator logic, math calculations, and scripting runtime |
| **Pillow (`PIL`)** | `>= 9.0` (Tested on 10.2.0) | Technical 2D drawing rendering and 3D multi-panel part preview generation |
| **System Fonts** | `DejaVu Sans` / `DejaVu Sans Bold` | Text labels and title blocks for drawing and preview renders (`/usr/share/fonts/truetype/dejavu/`) |
| **POSIX Bash** | `>= 5.0` | Build orchestration via `bt4v_generate_all.sh` |

---

## Section 7: Non-Functional Requirements

- **Parametric Repeatability:** All CAD models are generated purely via deterministic Python scripts without manual GUI manipulation, ensuring 100% reproducible builds.
- **Dimensional Tolerance:** Bounding box dimensions must adhere strictly to ±0.1 mm tolerance; part volumes must remain within ±2% of nominal baselines.
- **Structural Rigidity:** The combination of modular I-beam spine segments, bay brackets, and full-length bowtie backing struts ensures high torsional and bending rigidity under wind and gravitational loading.
- **Weather & Thermal Resistance:** PETG or ASA filament is recommended for production prints deployed in sunny windows to prevent solar thermal deformation. PLA is suitable for indoor prototyping.
