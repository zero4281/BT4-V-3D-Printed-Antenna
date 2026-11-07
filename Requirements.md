# BT4-V 3D Printed Antenna — Software & Hardware Requirements

**Version:** 0.3.0  
**Date:** November 2026  
**Project:** BT4-V 3D Printed Antenna  
**Primary Output:** FreeCAD-generated STL parts, 2D technical drawing, part preview rendering, assembly guide, and bill of materials  

---

## Table of Contents

1. [Overview](#1-overview)
2. [Project Structure](#2-project-structure)
3. [Authoritative Input Data](#3-authoritative-input-data)
4. [System Architecture & RF Design](#4-system-architecture--rf-design)
5. [Center Feed Hub Generator (bt4v_center_feed.py)](#5-center-feed-hub-generator-bt4v_center_feedpy)
6. [Whisker Bay Bracket Generator (bt4v_bay_bracket.py)](#6-whisker-bay-bracket-generator-bt4v_bay_bracketpy)
7. [Spine Segment Generator (bt4v_spine_segment.py)](#7-spine-segment-generator-bt4v_spine_segmentpy)
8. [Phase Crossover Spacer Generator (bt4v_phase_crossover.py)](#8-phase-crossover-spacer-generator-bt4v_phase_crossoverpy)
9. [Full-Length Bowtie Backing Strut Generator (bt4v_bowtie_backing.py)](#9-full-length-bowtie-backing-strut-generator-bt4v_bowtie_backingpy)
10. [Top Hanging Cap Generator (bt4v_hanging_cap.py)](#10-top-hanging-cap-generator-bt4v_hanging_cappy)
11. [Fit Coupon Generator (bt4v_fit_coupon.py)](#11-fit-coupon-generator-bt4v_fit_couponpy)
12. [Drawing & Preview Generators](#12-drawing--preview-generators)
13. [Build Orchestration (bt4v_generate_all.sh)](#13-build-orchestration-bt4v_generate_allsh)
14. [Assembly, Wiring & Installation (ASSEMBLY.md)](#14-assembly-wiring--installation-assemblymd)
15. [Bill of Materials (BT4-V BOM.md)](#15-bill-of-materials-bt4-v-bommd)
16. [Non-Functional Requirements](#16-non-functional-requirements)
17. [Out of Scope](#17-out-of-scope)
18. [Revision History](#18-revision-history)

---

## 1. Overview

**BT4-V** is a high-performance, 4-bay bowtie digital television (DTV) antenna with integrated VHF-High coverage, engineered for 3D-printed fabrication and indoor window suspension.

The antenna combines:
- **Four co-phased bowtie bays** arranged vertically along a modular 3D-printed spine.
- **Strictly horizontal polarisation (0° tilt across all elements)**, eliminating cross-polarisation loss.
- **Dual-band coverage:** The inner two bays (Bays 2 and 3) are tuned for high-gain broadband UHF reception (470–608 MHz, channels 14–36), while the outer two bays (Bays 1 and 4, top and bottom) feature extended whiskers tuned for VHF-High reception (174–216 MHz, channels 7–13).
- **Full-Length Bowtie Backing Struts:** Continuous 3D-printed snap-fit backing struts running from bay bracket root to wire tip, permanently locking exact flare angles (32.5° UHF, 25.5° VHF) and completely eliminating gravity sag, droop, or vibration.
- **RCA VH101R Matching Transformer Integration:** A commercial 300:75 Ω outdoor matching transformer (4:1 balun) mounts directly to the center feed bracket via its screw lugs, providing a female F-connector output for direct 75 Ω RG6 coaxial feed to the television.

BT4-V delivers +6 to +8 dBi forward gain across UHF and +3 to +4 dBi across VHF-High in an ultra-lightweight (~210 g), flat, modular form factor fitting a standard window (<600 mm height). Detailed build instructions and material inventories are provided in `ASSEMBLY.md` and `BT4-V BOM.md`.

---

## 2. Project Structure

```
BT4-V-Antenna/
├── Requirements.md                   # This document — authoritative functional baseline
├── Plan.md                           # Implementation plan and task tracking
├── Testing Strategy.md               # Verification procedures and test baselines
├── Bugs.md                           # Issue tracker
├── ASSEMBLY.md                       # Step-by-step physical assembly & build guide
├── BT4-V BOM.md                      # Bill of materials and hardware stack
├── Update.md                         # Gap assessment and migration tracking
├── bt4v_generate_all.sh              # Headless build orchestrator
│
├── BT4-V 2D Drawing.png              # Generated technical drawing
├── BT4-V Parts Preview.png           # Generated 3D part rendering preview
│
├── TV Channels.ods                   # Reference frequency and station data
├── Project Photos/                   # Photographic references and documentation
│
├── python/                           # FreeCAD and Pillow generators
│   ├── bt4v_center_feed.py           # Center feed hub with RCA balun cradle
│   ├── bt4v_bay_bracket.py           # Whisker mounting bracket (Bays 1–4)
│   ├── bt4v_spine_segment.py         # Interlocking modular vertical spine struts
│   ├── bt4v_phase_crossover.py       # Phase-line crossover insulator / guide
│   ├── bt4v_bowtie_backing.py        # Full-length bowtie backing strut
│   ├── bt4v_hanging_cap.py           # Top hanging cap with suspension eyelets
│   ├── bt4v_fit_coupon.py            # Pre-print tolerance and snap-fit coupon
│   ├── bt4v_drawing.py               # 2D technical drawing generator (Pillow)
│   └── bt4v_preview.py               # 3D part preview generator (Pillow)
│
└── stl/                              # Generated 3D printable meshes (git-ignored)
    ├── BT4V_Center_Feed.stl
    ├── BT4V_Bay_Bracket.stl
    ├── BT4V_Spine_Segment.stl
    ├── BT4V_Phase_Crossover.stl
    ├── BT4V_Bowtie_Backing.stl
    ├── BT4V_Hanging_Cap.stl
    └── BT4V_Fit_Coupon.stl
```

All build scripts are executed from the repository root. FreeCAD generators write STL files to `stl/`. The 2D drawing and preview generators output PNG images to the repository root.

---

## 3. Authoritative Input Data

### 3.1 Frequency & Market Coverage

The BT4-V antenna is engineered for universal broadband digital television (DTV) reception across standard VHF-High and UHF broadcast bands:

| Service / Band | RF Channel Range | Frequency Range (MHz) | Target Antenna Elements | Nominal Gain | Polarisation |
|---|---|---|---|---|---|
| **VHF-High** | Channels 7–13 | 174–216 MHz | Bay 1 & 4 (VHF Extended Whiskers) | ~3 to 4 dBi | Horizontal (0° tilt) |
| **UHF** | Channels 14–36 | 470–608 MHz | Bays 2 & 3 (UHF Bowtie Whiskers) | ~6 to 8 dBi | Horizontal (0° tilt) |

The antenna operates broadband across any range of TV channels within these frequency bands without requiring location-specific modifications.

### 3.2 Wire Material Specification

- **Conductor:** 12 AWG solid copper wire (nominal bare conductor diameter 2.05 mm; insulated THHN OD ~3.0 mm).
- **Insulation Treatment:** Wire may be installed with THHN insulation intact or stripped. Channels and clamping pockets accommodate up to 3.2 mm diameter.
- **Phase Lines:** Two continuous lengths of 12 AWG copper wire running vertically along the spine, spaced ~25 mm center-to-center.

### 3.3 Units and Coordinate Conventions

- All dimensions are in millimetres.
- Coordinates follow standard FreeCAD convention: +Z is vertical along the antenna spine, +X is horizontal along the whisker span, and +Y is perpendicular to the antenna plane (front-to-back).

---

## 4. System Architecture & RF Design

### 4.1 Topology & Operating Principle

BT4-V is an array of four stacked bowtie dipoles fed with parallel balanced phase lines:
- **Bays:** Numbered 1 to 4 from top to bottom.
- **Vertical Spacing:** 130 mm center-to-center pitch between adjacent bay brackets.
  - Total active center-to-center height = 3 × 130 mm = 390 mm.
  - Overall height including whisker vertical flare = ~560 mm (well within the ≤600 mm window envelope).
- **Polarisation:** Pure horizontal. All whiskers lie in the X-Z plane, achieving 0 dB cross-polarisation loss.
- **Gain:** Bi-directional broadside pattern (equal front and back reception). Forward gain is ~6 to ~8 dBi on UHF and ~3 to ~4 dBi on VHF-High.

### 4.2 Element Dimensions

| Element | Bays | Arm Length (Apex to Tip) | Tine Spread (Tip to Tip) | Total Span (Left to Right) | Flare Angle | Target Band |
|---|---|---|---|---|---|---|
| **VHF-High Whiskers** | 1 & 4 (Top & Bottom) | 340 mm | 150 mm | ~680 mm | ~25.5° | 174–216 MHz (RF 8, 12) |
| **UHF Whiskers** | 2 & 3 (Center) | 200 mm | 115 mm | ~400 mm | ~32.5° | 470–608 MHz (RF 14, 26, 33) |

Each bay consists of two V-shaped whiskers (left and right), forming a bowtie. A total of 8 bent V-whiskers are used (4 VHF arms, 4 UHF arms).

### 4.3 Phase Lines & Crossover Phasing

- Two parallel vertical 12 AWG wires connect the four bays.
- **Crossover Transposition:** Phase lines cross over (transposition) between Bay 1 and Bay 2, and between Bay 3 and Bay 4. This 180° phase inversion ensures that all four bays are driven in electrical phase.
- **Crossover Spacing:** Crossover clips maintain ≥5 mm separation between the crossing wires to prevent contact and capacitive shorting.
- **Center Feed:** The antenna is fed at the physical midpoint between Bay 2 and Bay 3.

### 4.4 Balun & Matching Transformer

- **Model:** RCA Outdoor Matching Transformer VH101R.
- **Impedance Transformation:** 300 Ω balanced (antenna feedpoint) to 75 Ω unbalanced (coaxial downlead), ratio 4:1.
- **Mounting:** The transformer body cradles securely in the center feed bracket. The two spade lugs connect to M4 feed studs clamping the phase lines.
- **Output:** Downward-facing integrated female F-connector accepting standard RG6 coax.

---

## 5. Center Feed Hub Generator (`bt4v_center_feed.py`)

### 5.1 Purpose & Output

Generates the central structural and electrical hub located between Bay 2 and Bay 3, exported as **`stl/BT4V_Center_Feed.stl`**.

### 5.2 Geometry & Features

| Feature | Requirement |
|---|---|
| Body Dimensions | 70 mm (Z) × 40 mm (X) × 24 mm (Y) |
| Balun Cradle | Custom cavity contour to securely hold the RCA VH101R transformer body |
| Terminal Spacing | 25 mm center-to-center terminal posts for the phase-line feed connections |
| Hardware Ports | 2 × M4 bolt clearance holes (4.3 mm) with captured hex nut pockets (7.2 mm across flats × 3.5 mm deep) |
| Wire Channels | 3.2 mm wide × 3.0 mm deep vertical wire routing channels for phase lines |
| Spine Joints | Interlocking tenon/mortise interfaces at +Z and -Z ends to mate with `bt4v_spine_segment.py` |
| Coax Strain Relief | Integrated zip-tie loop slot (4.0 × 2.0 mm) below the balun cradle |

### 5.3 Diagnostic & Validation Requirements

- Print bounding box, volume, solid count, and validity.
- The output must be **one valid solid** (`Valid: True`) with volume approximately **28,500 mm³ (±2%)**.

---

## 6. Whisker Bay Bracket Generator (`bt4v_bay_bracket.py`)

### 6.1 Purpose & Output

Generates the whisker mounting bracket used at each of the four bays (Bays 1, 2, 3, and 4), exported as **`stl/BT4V_Bay_Bracket.stl`**. Quantity required: **4**.

### 6.2 Geometry & Features

| Feature | Requirement |
|---|---|
| Body Dimensions | 40 mm (Z) × 50 mm (X) × 18 mm (Y) |
| Integrated Angle-Locking Wings | Extended lateral support wings molding exact required flare angles (25.5° VHF, 32.5° UHF) directly into wing channels to act as a permanent built-in alignment jig |
| Dual Snap-Lock C-Clips | Enclosed snap-in wire retention C-clips (2.2 mm snap mouth into 3.2 mm circular wire cavity) at apex and wing tips with positive stop shoulders to mechanically lock 12 AWG wire against bumps or displacement |
| Whisker Flare Guide | Supports both 32.5° (UHF) and 25.5° (VHF) whisker angles with rounded lead-in apex |
| Apex Clamp Posts | 2 × M4 through-holes (4.3 mm) with rear hex nut pockets (7.2 mm across flats) |
| Phase Line Channels | Vertical guide channels (3.2 × 3.0 mm) spaced 25 mm apart to seat phase lines against whisker apex |
| Spine Interlock | Symmetrical interlocking tenon/mortise connectors on top (+Z) and bottom (-Z) |
| Support Mounting Pockets | Integrated mounting slots/shoulders to lock the inner ends of the `bt4v_bowtie_support.py` support struts |

### 6.3 Diagnostic & Validation Requirements

- Bounding box extents: 50 × 18 × 40 mm (±0.1 mm).
- Single valid solid, volume approximately **19,200 mm³ (±2%)**.

---

## 7. Spine Segment Generator (`bt4v_spine_segment.py`)

### 7.1 Purpose & Output

Generates the modular vertical spine strut that spaces adjacent bay brackets at the exact 130 mm pitch, exported as **`stl/BT4V_Spine_Segment.stl`**. Quantity required: **4** (between Bay 1–2, Bay 2–Feed, Feed–Bay 3, and Bay 3–4).

### 7.2 Geometry & Features

| Feature | Requirement |
|---|---|
| Length | 110 mm active body length (yields 130 mm bay center-to-center pitch when assembled with brackets) |
| Cross Section | 20 mm (X) × 14 mm (Y) rigid I-beam or trussed profile to minimize weight while preventing bending |
| Phase Line Grooves | 2 × parallel 3.2 mm wire grooves spaced 25 mm apart on front face |
| Joint Ends | Male tenon (+Z) and female mortise (-Z) with 2.6 mm cross-pin locking holes |
| Bed Fit | Fits easily within 235 × 235 mm build plate printed flat |

### 7.3 Diagnostic & Validation Requirements

- Single valid solid, volume approximately **16,800 mm³ (±2%)**.

---

## 8. Phase Crossover Spacer Generator (`bt4v_phase_crossover.py`)

### 8.1 Purpose & Output

Generates the clip-on phase transposition spacer placed between Bay 1–2 and Bay 3–4, exported as **`stl/BT4V_Phase_Crossover.stl`**. Quantity required: **2**.

### 8.2 Geometry & Features

| Feature | Requirement |
|---|---|
| Dimensions | 30 mm (Z) × 35 mm (X) × 12 mm (Y) |
| Crossing Channels | Two diagonal crossing 3.2 mm wire channels on separate planes (front and back) |
| Dielectric Separation | Minimum 5.0 mm plastic/air gap between crossing wires to prevent contact/arcing |
| Retention | Snap-fit snap lip (2.4 mm mouth) to clip securely onto spine strut |

### 8.3 Diagnostic & Validation Requirements

- Single valid solid, volume approximately **6,100 mm³ (±2%)**.

---

## 9. Full-Length Bowtie Backing Strut Generator (`bt4v_bowtie_backing.py`)

### 9.1 Purpose & Output

Generates the continuous snap-fit backing strut running from bay bracket root to wire tip, exported as **`stl/BT4V_Bowtie_Backing.stl`**. Quantity required: **8** (2 per bay across Bays 1–4, supporting upper and lower V-whiskers).

### 9.2 Geometry & Features

| Feature | Requirement |
|---|---|
| Purpose | Permanently locks exact flare angles (32.5° UHF, 25.5° VHF) from root to tip and completely eliminates gravity sag, droop, or vibration |
| Channel & Length | Continuous 3.2 mm wire retention channel along a 210 mm span |
| Strut Profile | Ribbed truss profile (12.0 mm wide × 8.0 mm high) for maximum rigidity at minimum mass (~2.5 g each) |

### 9.3 Diagnostic & Validation Requirements

- Single valid solid, volume approximately **2,400 mm³ (±2%)**.

---

## 10. Top Hanging Cap Generator (`bt4v_hanging_cap.py`)

### 11.1 Purpose & Output

Generates the top termination cap locking onto the top of Bay 1, exported as **`stl/BT4V_Hanging_Cap.stl`**. Quantity required: **1**.

### 11.2 Geometry & Features

| Feature | Requirement |
|---|---|
| Body | Terminal cap with mortise joint mating to Bay 1 top connector |
| Suspension Points | 2 × Ø5.0 mm eyelets spaced 30 mm apart along the X axis |
| Hanging Options | Accommodates nylon cord, picture wire, or window suction-cup hooks |
| Anti-Rotation | Dual-point suspension prevents antenna twisting when hung against a window |

### 11.3 Diagnostic & Validation Requirements

- Single valid solid, volume approximately **7,400 mm³ (±2%)**.

---

## 12. Fit Coupon Generator (`bt4v_fit_coupon.py`)

### 12.1 Purpose & Output

Generates a pre-print calibration and fit-test coupon, exported as **`stl/BT4V_Fit_Coupon.stl`**. Printed first to verify printer dimensional accuracy before production parts.

### 12.2 Required Features

The coupon measures approximately **90 × 50 × 10 mm** and tests:
1. **Friction channels:** 2.8, 3.0, 3.2, 3.4 mm widths for 12 AWG wire fit.
2. **Snap channels:** 2.2 and 2.4 mm mouths over a 3.3 mm round cavity.
3. **M4 hardware stack:** 4.3 mm clearance hole with 7.2 mm hex nut capture pocket (3.5 mm deep).
4. **Spine interlock joint:** Male tenon and female mortise sample with 2.6 mm cross-pin hole.
5. **Balun lug spacing:** 25 mm pitch test studs for RCA VH101R spade lugs.
6. **Support strut snap jaws:** Test snap jaw fit for `bt4v_bowtie_support.py`.

### 12.3 Diagnostic & Validation Requirements

- Single valid solid, volume approximately **26,500 mm³ (±2%)**.

---

## 13. Drawing & Preview Generators

### 13.1 2D Technical Drawing (`bt4v_drawing.py`)

Generates **`BT4-V 2D Drawing.png`** (2200 × 1500 px) using Pillow:
- Title block: "BT4-V 3D PRINTED ANTENNA — 4-BAY BOWTIE + VHF".
- Full front view of the 4 bays, whisker dimensions (UHF 400 mm, VHF 680 mm span), phase lines, crossovers, triangular tine spreaders, and mid-span bowtie support struts.
- Side view showing spine profile, RCA VH101R balun mounting, and hanging eyelets.
- Channel mapping & electrical performance table.
- Detailed assembly and wire-bending notes.

### 13.2 3D Parts Preview (`bt4v_preview.py`)

Generates **`BT4-V Parts Preview.png`** (1800 × 800 px) using Pillow:
- Multi-panel visual rendering of the generated STL models (Center Feed, Bay Bracket, Spine Segment, Crossover, Whisker Spreader, Bowtie Support, and Hanging Cap).
- Labels indicating assembly locations along the spine.

---

## 14. Build Orchestration (`bt4v_generate_all.sh`)

### 14.1 Purpose & Behavior

A single headless bash script that generates every STL and PNG artifact from clean source:
- Sets `set -euo pipefail`.
- Uses `FREECAD_CMD` (defaults to `/snap/bin/freecad.cmd` or `freecadcmd`).
- `mkdir -p stl` prior to export.
- Executes all Python generators in sequence:
  1. `python/bt4v_center_feed.py`
  2. `python/bt4v_bay_bracket.py`
  3. `python/bt4v_spine_segment.py`
  4. `python/bt4v_phase_crossover.py`
  5. `python/bt4v_whisker_spreader.py`
  6. `python/bt4v_bowtie_support.py`
  7. `python/bt4v_hanging_cap.py`
  8. `python/bt4v_fit_coupon.py`
  9. `python/bt4v_drawing.py`
  10. `python/bt4v_preview.py`
- Verifies that all 8 STLs exist in `stl/` and both PNGs exist in root.
- Exits with status `0` on complete success, or non-zero on any failure.

---

## 15. Assembly, Wiring & Installation

### 15.1 Whisker Bending & Wire Preparation

1. **Cut lengths:**
   - 4 × VHF whisker wires: 690 mm each (allows 340 mm per arm + 10 mm apex bend).
   - 4 × UHF whisker wires: 410 mm each (allows 200 mm per arm + 10 mm apex bend).
   - 2 × Phase line wires: ~580 mm each.
2. **Bending & Support Assembly:**
   - Bend each whisker wire at its midpoint: VHF to 25.5° flare angle; UHF to 32.5° flare angle.
   - Snap a **Triangular Tine Spreader** onto each of the 4 VHF whiskers at 150 mm from apex.
   - Snap **Mid-Span Bowtie Support Struts** (2 per bay, 8 total) between the bay brackets and the upper/lower whisker arms to rigidly hold them at their exact flare angles without manual holding.

### 15.2 Spine Assembly & Wiring

1. Assemble the central spine by interlocking the Center Feed, 4 Spine Segments, and 4 Bay Brackets, capped by the Hanging Cap at top. Lock joints with 2.5 mm cross-pins or M2.5 screws.
2. Lay the two vertical 12 AWG phase lines into the spine guide grooves.
3. Install the two **Phase Crossover Spacers** between Bays 1–2 and Bays 3–4, crossing the phase lines without electrical contact.
4. Seat the whisker apexes into the bay brackets. Clamp whisker apexes and phase lines together using M4 bolts, washers, and nuts.
5. Snap the **RCA VH101R** transformer into the center feed cradle. Secure its spade lugs to the center feed M4 terminal studs.

### 15.3 Installation & Tuning

- **Hanging:** Suspend from top hanging cap eyelets against an indoor window facing the transmitter towers.
- **Connection:** Connect standard 75 Ω RG6 coaxial cable to the RCA VH101R F-connector.
- **Metal Screens:** Maintain at least 0.5 m spacing from metallic window insect screens to prevent UHF attenuation.

---

## 16. Bill of Materials

| Item | Description | Qty |
|---|---|---|
| **Printed Parts** | Center Feed, 4 × Bay Brackets, 4 × Spine Segments, 2 × Crossovers, 4 × Spreaders, 8 × Bowtie Supports, 1 × Hanging Cap, 1 × Coupon (PLA/PETG, ~210 g total) | 1 set |
| **Wire** | 12 AWG solid copper wire (THHN) — approx. 5.6 metres total | 1 roll |
| **Balun** | RCA Outdoor Matching Transformer VH101R (300:75 Ω 4:1) | 1 |
| **Hardware** | M4 × 20 mm hex-head bolts, M4 nuts, M4 flat washers | 10 sets |
| **Cross-pins** | 2.5 mm pins, trimmed finish nails, or M2.5 × 12 mm screws | 10 |
| **Feedline** | 75 Ω RG6 coaxial cable with male F-connectors | As required |

---

## 17. Non-Functional Requirements

### 17.1 FDM Printing Constraints

- **Bed Size:** All parts fit standard 235 × 235 × 250 mm print volume.
- **Nozzle & Profile:** 0.4 mm nozzle, 0.2 mm layer height, 3 perimeters, 30% gyroid or grid infill.
- **Material:** PLA for initial indoor prototyping; PETG or ASA recommended for high-sun window exposure.
- **No Supports Required:** All parts designed with bridge-free geometries and self-supporting chamfers.

### 17.2 Software Dependencies

- FreeCAD (>= 0.20) with Python 3 API (`Part`, `Mesh` modules).
- Python 3 with Pillow (`PIL`) for drawing and preview generation.
- DejaVu Sans fonts at `/usr/share/fonts/truetype/dejavu/`.
- POSIX-compliant bash shell.

### 17.3 Exit Codes & Verification Baseline

- All Python scripts must return exit code `0` on success and non-zero on failure.
- Geometry verification baseline:

| Part | Nominal BBox (mm) | Nominal Volume (mm³) | Tolerance |
|---|---|---|---|
| `stl/BT4V_Center_Feed.stl` | 70 × 40 × 24 | 28,500 | ±2% |
| `stl/BT4V_Bay_Bracket.stl` | 50 × 18 × 40 | 19,200 | ±2% |
| `stl/BT4V_Spine_Segment.stl` | 20 × 14 × 120 | 16,800 | ±2% |
| `stl/BT4V_Phase_Crossover.stl` | 35 × 12 × 30 | 6,100 | ±2% |
| `stl/BT4V_Whisker_Spreader.stl` | 72 × 12 × 8 | 2,200 | ±2% |
| `stl/BT4V_Bowtie_Support.stl` | 65 × 10 × 8 | 1,800 | ±2% |
| `stl/BT4V_Hanging_Cap.stl` | 44 × 18 × 30 | 7,400 | ±2% |
| `stl/BT4V_Fit_Coupon.stl` | 90 × 50 × 10 | 26,500 | ±2% |

---

## 18. Out of Scope

- Active powered preamps or motorized rotators.
- Heavy metallic reflector screens (design is optimized for lightweight window hanging).
- Custom winding of RF baluns (commercial RCA VH101R is used directly).
- Outdoor mast mounting hardware beyond lightweight window suspension.

---

## 19. Revision History

| Version | Date | Description |
|---|---|---|
| **0.1.0** | November 2026 | Initial project baseline for **BT4-V 3D Printed Antenna**. |
| **0.2.0** | November 2026 | Added specification for **Mid-Span Bowtie Support Struts** (`bt4v_bowtie_support.py`) to eliminate manual hand-positioning difficulty and lock bowtie arms rigidly in place. |
