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
- **Four co-phased bowtie bays** arranged vertically along a modular 3D-printed spine at an exact 130.0 mm center-to-center pitch.
- **Strictly horizontal polarisation (0° tilt across all elements)**, eliminating cross-polarisation loss.
- **Dual-band coverage:** The inner two bays (Bays 2 and 3) are tuned for high-gain broadband UHF reception (470–608 MHz, channels 14–36), while the outer two bays (Bays 1 and 4, top and bottom) feature extended whiskers tuned for VHF-High reception (174–216 MHz, channels 7–13).
- **Full-Length Bowtie Backing Struts:** Continuous 3D-printed C-clip snap-fit interlocking backing struts running behind every V-whisker arm from bay bracket root to wire tip (1 strut per 200 mm UHF arm; 2 daisy-chained struts per 340 mm VHF arm), permanently locking exact flare angles (32.5° UHF, 25.5° VHF) and completely eliminating gravity sag, droop, or vibration.
- **RCA VH101R Matching Transformer Integration:** A commercial 300:75 Ω outdoor matching transformer (4:1 balun) mounts directly to the center feed hub via its screw lugs, providing a female F-connector output for direct 75 Ω RG6 coaxial feed to the television.

BT4-V delivers +6 to +8 dBi forward gain across UHF and +3 to +4 dBi across VHF-High in an ultra-lightweight (~235 g), flat, modular form factor fitting a standard window (<600 mm height). Detailed build instructions and material inventories are provided in `ASSEMBLY.md` and `BT4-V BOM.md`.

---

## 2. Project Structure

```
BT4-V-Antenna/
├── README.md                         # Project overview and quick-start guide
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
├── python/                           # FreeCAD and Pillow generators
│   ├── bt4v_center_feed.py           # Center feed hub with RCA balun cradle
│   ├── bt4v_bay_bracket.py           # Whisker mounting bracket (Bays 1–4)
│   ├── bt4v_spine_segment.py         # Interlocking modular vertical spine struts
│   ├── bt4v_phase_crossover.py       # Phase-line crossover insulator / guide
│   ├── bt4v_bowtie_backing.py        # Full-length interlocking bowtie backing strut
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
- **Insulation Treatment:** Wire may be installed with THHN insulation intact or stripped at clamping terminals. Channels and clamping pockets accommodate up to 3.2 mm diameter.
- **Phase Lines:** Two continuous straight lengths of 12 AWG copper wire (~580 mm each) running vertically along the spine, spaced 25.0 mm center-to-center across all spine components.

### 3.3 Units and Coordinate Conventions

- All dimensions are in millimetres.
- Coordinates follow standard FreeCAD convention: +Z is vertical along the antenna spine, +X is horizontal along the whisker span, and +Y is perpendicular to the antenna plane (front-to-back).

---

## 4. System Architecture & RF Design

### 4.1 Topology & Operating Principle

BT4-V is an array of four stacked bowtie dipoles fed with parallel balanced phase lines:
- **Bays:** Numbered 1 to 4 from top to bottom.
- **Vertical Spacing:** Exact 130.0 mm center-to-center pitch between adjacent bay brackets:
  - Each Bay Bracket has a 30.0 mm active vertical body (whisker apex centered at 15.0 mm).
  - Outer bay pairs (Bay 1–2 and Bay 3–4) are separated by 100.0 mm active Spine Segments (`15.0 + 100.0 + 15.0 = 130.0 mm`).
  - Inner bay pair (Bay 2–3) is separated by the 100.0 mm active Center Feed Hub (`15.0 + 100.0 + 15.0 = 130.0 mm`).
  - Total active center-to-center height = 3 × 130.0 mm = 390.0 mm.
  - Overall height including whisker vertical flare and hanging cap = ~560 mm (well within the ≤600 mm window envelope).
- **Polarisation:** Pure horizontal. All whiskers lie in the X-Z plane, achieving 0 dB cross-polarisation loss.
- **Gain:** Bi-directional broadside pattern (equal front and back reception). Forward gain is ~6 to ~8 dBi on UHF and ~3 to ~4 dBi on VHF-High.

### 4.2 Element Dimensions

| Element | Bays | Arm Length (Apex to Tip) | Tine Spread (Tip to Tip) | Total Span (Left to Right) | Flare Angle | Backing Struts per Arm |
|---|---|---|---|---|---|---|
| **VHF-High Whiskers** | 1 & 4 (Top & Bottom) | 340 mm | 150 mm | ~680 mm | 25.5° | 2 daisy-chained (16 total) |
| **UHF Whiskers** | 2 & 3 (Center) | 200 mm | 115 mm | ~400 mm | 32.5° | 1 strut (8 total) |

Each bay consists of two V-shaped whiskers (left and right), forming a bowtie (8 V-whiskers / 16 arms total across the 4 bays).

### 4.3 Phase Lines & Crossover Phasing

- Two parallel vertical 12 AWG wires connect the four bays at a constant 25.0 mm center-to-center spacing.
- **Crossover Transposition:** Phase lines cross over (transposition) between Bay 1 and Bay 2, and between Bay 3 and Bay 4. This 180° phase inversion ensures that all four bays are driven in electrical phase.
- **Crossover Spacing:** Crossover clips maintain ≥5.0 mm separation between the crossing wires to prevent contact and capacitive shorting.
- **Center Feed:** The antenna is fed at the exact physical midpoint (`Z = 50.0 mm`) of the Center Feed Hub between Bay 2 and Bay 3.

### 4.4 Balun & Matching Transformer

- **Model:** RCA Outdoor Matching Transformer VH101R.
- **Impedance Transformation:** 300 Ω balanced (antenna feedpoint) to 75 Ω unbalanced (coaxial downlead), ratio 4:1.
- **Mounting:** The transformer body cradles securely in the center feed bracket. The two spade lugs connect to M4 feed studs clamping the phase lines.
- **Output:** Downward-facing integrated female F-connector accepting standard RG6 coax.

---

## 5. Center Feed Hub Generator (`bt4v_center_feed.py`)

### 5.1 Purpose & Output

Generates the central structural and electrical hub located directly between Bay 2 and Bay 3, exported as **`stl/BT4V_Center_Feed.stl`**. Quantity required: **1**.

### 5.2 Geometry & Features

| Feature | Requirement |
|---|---|
| Body Dimensions | 40.0 mm (X) × 24.0 mm (Y) × 110.0 mm (Z) (100.0 mm active body + 10.0 mm tenon, yielding 130.0 mm Bay 2–3 pitch) |
| Balun Cradle | Custom cavity contour to securely hold the RCA VH101R transformer body |
| Terminal Spacing | 25.0 mm center-to-center terminal posts at `Z = 50.0 mm` (midpoint) for phase-line feed connections |
| Hardware Ports | 2 × M4 bolt clearance holes (4.3 mm) with captured hex nut pockets (7.2 mm across flats × 3.5 mm deep) |
| Wire Channels | Continuous 3.2 mm wide × 3.0 mm deep vertical wire routing channels spaced 25.0 mm apart |
| Spine Joints | Interlocking tenon (+Z) and mortise (-Z) interfaces with 2.6 mm cross-pin holes mating with Bay 2 and Bay 3 brackets |
| Coax Strain Relief | Integrated zip-tie loop slot (4.0 × 2.0 mm) below the balun cradle |

### 5.3 Diagnostic & Validation Requirements

- Print bounding box, volume, solid count, and validity.
- The output must be **one valid solid** (`Valid: True`) with volume approximately **42,000 mm³ (±2%)**.

---

## 6. Whisker Bay Bracket Generator (`bt4v_bay_bracket.py`)

### 6.1 Purpose & Output

Generates the whisker mounting bracket used at each of the four bays (Bays 1, 2, 3, and 4), exported as **`stl/BT4V_Bay_Bracket.stl`**. Quantity required: **4**.

### 6.2 Geometry & Features

| Feature | Requirement |
|---|---|
| Body Dimensions | 50.0 mm (X) × 18.0 mm (Y) × 40.0 mm (Z) (30.0 mm active body height + 10.0 mm tenon) |
| Whisker Flare Guide | Supports both 32.5° (UHF) and 25.5° (VHF) whisker angles centered symmetrically at `Z = 15.0 mm` with rounded lead-in apex |
| Apex Clamp Posts | 2 × M4 through-holes (4.3 mm) at `Z = 15.0 mm` with rear hex nut pockets (7.2 mm across flats × 3.5 mm deep) |
| Phase Line Channels | Vertical guide channels (3.2 × 3.0 mm) spaced 25.0 mm apart to seat phase lines against whisker apex |
| Spine Interlock | Symmetrical interlocking tenon (+Z) and mortise (-Z) connectors with 2.6 mm cross-pin holes |
| Backing Strut Sockets | 4 × integrated mounting sockets on lateral wings (upper and lower exit stations) to lock the root tenons of `bt4v_bowtie_backing.py` |

### 6.3 Diagnostic & Validation Requirements

- Bounding box extents: 50.0 × 18.0 × 40.0 mm (±0.1 mm).
- Single valid solid, volume approximately **19,200 mm³ (±2%)**.

---

## 7. Spine Segment Generator (`bt4v_spine_segment.py`)

### 7.1 Purpose & Output

Generates the modular vertical spine strut that spaces outer adjacent bay brackets at the exact 130.0 mm pitch, exported as **`stl/BT4V_Spine_Segment.stl`**. Quantity required: **2** (between Bay 1–2 and Bay 3–4).

### 7.2 Geometry & Features

| Feature | Requirement |
|---|---|
| Dimensions | 30.0 mm (X) × 14.0 mm (Y) × 110.0 mm (Z) (100.0 mm active body length + 10.0 mm tenon, yielding 130.0 mm bay center-to-center pitch) |
| Cross Section | 30.0 mm (X) × 14.0 mm (Y) rigid flanged I-beam profile with mid-span 20.0 mm waist recess for crossover clip mounting |
| Phase Line Grooves | 2 × parallel 3.2 × 3.0 mm wire grooves spaced 25.0 mm apart on front face (straight-through alignment with brackets and hub) |
| Joint Ends | Male tenon (+Z) and female mortise (-Z) with 2.6 mm cross-pin locking holes |
| Bed Fit | Fits easily within 235 × 235 mm build plate printed flat |

### 7.3 Diagnostic & Validation Requirements

- Single valid solid, volume approximately **21,000 mm³ (±2%)**.

---

## 8. Phase Crossover Spacer Generator (`bt4v_phase_crossover.py`)

### 8.1 Purpose & Output

Generates the clip-on phase transposition spacer placed at mid-span on Spine Segments 1 and 2 (between Bay 1–2 and Bay 3–4), exported as **`stl/BT4V_Phase_Crossover.stl`**. Quantity required: **2**.

### 8.2 Geometry & Features

| Feature | Requirement |
|---|---|
| Dimensions | 35.0 mm (X) × 12.0 mm (Y) × 30.0 mm (Z) |
| Crossing Channels | Two diagonal crossing 3.2 mm wire channels on separate planes (front and back) at 25.0 mm entry/exit pitch |
| Dielectric Separation | Minimum 5.0 mm plastic/air gap between crossing wires to prevent contact/arcing |
| Retention | Snap-fit lip (2.4 mm mouth) to clip securely onto the 20.0 mm mid-span waist of the spine strut |

### 8.3 Diagnostic & Validation Requirements

- Single valid solid, volume approximately **6,100 mm³ (±2%)**.

---

## 9. Full-Length Bowtie Backing Strut Generator (`bt4v_bowtie_backing.py`)

### 9.1 Purpose & Output

Generates the universal interlocking snap-fit backing strut running behind every V-whisker arm from bay bracket root to wire tip, exported as **`stl/BT4V_Bowtie_Backing.stl`**. Quantity required: **24** (1 strut per 200 mm UHF arm across Bays 2 & 3 [8 pcs]; 2 daisy-chained struts per 340 mm VHF arm across Bays 1 & 4 [16 pcs]).

### 9.2 Geometry & Features

| Feature | Requirement |
|---|---|
| Purpose | Permanently locks exact flare angles (32.5° UHF, 25.5° VHF) from root to tip across all 16 whisker arms and completely eliminates gravity sag, droop, or vibration |
| Dimensions & Span | 180.0 mm (X) × 12.0 mm (Y) × 8.0 mm (Z) (170.0 mm active span + 10.0 mm root/interlock tenon; fits 220×220 and 235×235 mm beds) |
| C-Clip Wire Channel | Continuous C-clip snap-fit wire retention channel (2.4 mm snap throat opening into 3.2 mm circular wire cavity) |
| Interlock Ends | Male tenon at root (-X) mating with Bay Bracket wing sockets, and female mortise socket at tip (+X) allowing a second strut to daisy-chain for 340 mm VHF arms |
| Strut Profile | Ribbed I-beam truss profile (12.0 mm wide × 8.0 mm high) with lightening windows for maximum rigidity at minimum mass (~2.7 g each) |

### 9.3 Diagnostic & Validation Requirements

- Single valid solid, volume approximately **2,200 mm³ (±2%)**.

---

## 10. Top Hanging Cap Generator (`bt4v_hanging_cap.py`)

### 10.1 Purpose & Output

Generates the top termination cap locking onto the top tenon of Bay 1, exported as **`stl/BT4V_Hanging_Cap.stl`**. Quantity required: **1**.

### 10.2 Geometry & Features

| Feature | Requirement |
|---|---|
| Dimensions | 44.0 mm (X) × 18.0 mm (Y) × 30.0 mm (Z) |
| Body | Terminal cap with female mortise joint and 2.6 mm cross-pin hole mating to Bay 1 top tenon |
| Suspension Points | 2 × Ø5.0 mm eyelets spaced 30.0 mm apart along the X axis |
| Hanging Options | Accommodates nylon cord, picture wire, or window suction-cup hooks |
| Anti-Rotation | Dual-point suspension prevents antenna twisting when hung against a window |

### 10.3 Diagnostic & Validation Requirements

- Single valid solid, volume approximately **7,400 mm³ (±2%)**.

---

## 11. Fit Coupon Generator (`bt4v_fit_coupon.py`)

### 11.1 Purpose & Output

Generates a pre-print calibration and fit-test coupon, exported as **`stl/BT4V_Fit_Coupon.stl`**. Printed first to verify printer dimensional accuracy before production parts.

### 11.2 Required Features

The coupon measures **90.0 × 50.0 × 10.0 mm** and tests:
1. **Friction channels:** 2.8, 3.0, 3.2, 3.4 mm widths for 12 AWG wire fit.
2. **Snap channels:** 2.2 and 2.4 mm C-clip mouths over a 3.3 mm round cavity.
3. **M4 hardware stack:** 4.3 mm clearance hole with 7.2 mm hex nut capture pocket (3.5 mm deep).
4. **Spine interlock joint:** Male tenon and female mortise sample with 2.6 mm cross-pin hole.
5. **Balun lug spacing:** 25.0 mm pitch test studs for RCA VH101R spade lugs.
6. **Backing strut socket:** Test mortise socket for `bt4v_bowtie_backing.py` root tenon fit.

### 11.3 Diagnostic & Validation Requirements

- Single valid solid, volume approximately **26,500 mm³ (±2%)**.

---

## 12. Drawing & Preview Generators

### 12.1 2D Technical Drawing (`bt4v_drawing.py`)

Generates **`BT4-V 2D Drawing.png`** (2200 × 1500 px) using Pillow:
- Title block: "BT4-V 3D PRINTED ANTENNA — 4-BAY BOWTIE + VHF".
- Full front view of the 4 bays at 130.0 mm pitch, whisker dimensions (UHF 400 mm, VHF 680 mm span), straight 25.0 mm phase lines, crossovers, and full-length interlocking bowtie backing struts across all 16 arms.
- Side view showing spine profile, RCA VH101R balun mounting, and hanging eyelets.
- Channel mapping & electrical performance table.
- Detailed assembly, wire-bending, and backing strut installation notes.

### 12.2 3D Parts Preview (`bt4v_preview.py`)

Generates **`BT4-V Parts Preview.png`** (1800 × 800 px) using Pillow:
- Multi-panel visual rendering of all 7 generated STL models (Center Feed, Bay Bracket, Spine Segment, Phase Crossover, Full-Length Bowtie Backing Strut, Hanging Cap, and Fit Coupon) plus the complete Modular Spine Assembly card.
- Labels indicating assembly locations along the spine and key technical specifications.

---

## 13. Build Orchestration (`bt4v_generate_all.sh`)

### 13.1 Purpose & Behavior

A single headless bash script that generates every STL and PNG artifact from clean source:
- Sets `set -euo pipefail`.
- Uses `FREECAD_CMD` (defaults to `freecadcmd` or `/snap/bin/freecad.cmd`).
- `mkdir -p stl` prior to export.
- Executes all 9 Python generators in sequence:
  1. `python/bt4v_center_feed.py`
  2. `python/bt4v_bay_bracket.py`
  3. `python/bt4v_spine_segment.py`
  4. `python/bt4v_phase_crossover.py`
  5. `python/bt4v_hanging_cap.py`
  6. `python/bt4v_fit_coupon.py`
  7. `python/bt4v_bowtie_backing.py`
  8. `python/bt4v_drawing.py`
  9. `python/bt4v_preview.py`
- Verifies that all 7 STLs exist in `stl/` and both PNGs exist in root.
- Exits with status `0` on complete success, or non-zero on any failure.

---

## 14. Assembly, Wiring & Installation (`ASSEMBLY.md`)

### 14.1 Whisker Bending & Wire Preparation

1. **Cut lengths:**
   - 4 × VHF whisker wires: 690 mm each (allows 340 mm per arm + 10 mm apex bend).
   - 4 × UHF whisker wires: 410 mm each (allows 200 mm per arm + 10 mm apex bend).
   - 2 × Phase line wires: ~580 mm each.
2. **Bending & Full-Length Backing Strut Assembly:**
   - Bend each whisker wire at its midpoint: VHF to 25.5° flare angle; UHF to 32.5° flare angle.
   - Snap **1 × Full-Length Bowtie Backing Strut** (`BT4V_Bowtie_Backing.stl`) onto each of the 8 UHF whisker arms (200 mm).
   - Snap **2 × daisy-chained Full-Length Bowtie Backing Struts** onto each of the 8 VHF whisker arms (340 mm), interlocking the outer strut's root tenon into the inner strut's tip mortise.
   - Lock the inner root tenons of all backing struts into the lateral wing sockets on the Bay Brackets.

### 14.2 Spine Assembly & Wiring

1. Assemble the central spine from top to bottom: Top Hanging Cap → Bay Bracket 1 → Spine Segment 1 → Bay Bracket 2 → Center Feed Hub → Bay Bracket 3 → Spine Segment 2 → Bay Bracket 4. Lock the 7 tenon/mortise joints with Ø2.5 mm cross-pins or M2.5 × 12 mm screws.
2. Lay the two vertical 12 AWG phase lines into the straight 25.0 mm pitch spine guide grooves.
3. Snap the two **Phase Crossover Spacers** onto the mid-span waist of Spine Segments 1 and 2 (between Bays 1–2 and Bays 3–4), crossing the phase lines with ≥5.0 mm dielectric separation.
4. Seat the whisker apexes into the bay brackets. Clamp whisker apexes and phase lines together using M4 × 20 mm bolts, washers, and captured hex nuts.
5. Snap the **RCA VH101R** transformer into the center feed cradle. Secure its spade lugs to the center feed M4 terminal studs.

### 14.3 Installation & Tuning

- **Hanging:** Suspend from top hanging cap eyelets against an indoor window facing the transmitter towers.
- **Connection:** Connect standard 75 Ω RG6 coaxial cable to the RCA VH101R F-connector and secure with a zip-tie through the strain relief slot.
- **Metal Screens:** Maintain at least 0.5 m spacing from metallic window insect screens to prevent UHF attenuation.

---

## 15. Bill of Materials (`BT4-V BOM.md`)

| Item | Description | Qty |
|---|---|---|
| **Printed Parts** | 1 × Center Feed, 4 × Bay Brackets, 2 × Spine Segments, 2 × Crossovers, 24 × Bowtie Backing Struts, 1 × Hanging Cap, 1 × Fit Coupon (PETG/PLA, ~235 g production set) | 1 set (34 pcs + coupon) |
| **Wire** | 12 AWG solid copper wire (THHN / bare) — approx. 5.6 metres total | 1 roll |
| **Balun** | RCA Outdoor Matching Transformer VH101R (300:75 Ω 4:1) | 1 |
| **Hardware** | M4 × 20 mm hex-head bolts, M4 hex nuts, M4 flat washers | 10 sets |
| **Cross-pins** | Ø2.5 mm pins, trimmed finish nails, or M2.5 × 12 mm screws (7 active + spares) | 8–10 pcs |
| **Feedline** | 75 Ω RG6 coaxial cable with male F-connectors | As required |

---

## 16. Non-Functional Requirements

### 16.1 FDM Printing Constraints

- **Bed Size:** All parts fit standard 220 × 220 mm or 235 × 235 × 250 mm print volumes printed flat.
- **Nozzle & Profile:** 0.4 mm nozzle, 0.2 mm layer height, 3 perimeters, 30% gyroid or grid infill.
- **Material:** PLA for initial indoor prototyping; PETG or ASA recommended for high-sun window exposure.
- **No Supports Required:** All parts designed with bridge-free geometries and self-supporting chamfers.

### 16.2 Software Dependencies

- FreeCAD (>= 0.20) with Python 3 API (`Part`, `Mesh` modules).
- Python 3 with Pillow (`PIL`) for drawing and preview generation.
- DejaVu Sans fonts at `/usr/share/fonts/truetype/dejavu/`.
- POSIX-compliant bash shell.

### 16.3 Exit Codes & Verification Baseline

- All Python scripts must return exit code `0` on success and non-zero (`1` or `2`) on failure.
- Geometry verification baseline:

| Part | Nominal BBox (X × Y × Z mm) | Nominal Volume (mm³) | Tolerance |
|---|---|---|---|
| `stl/BT4V_Center_Feed.stl` | 40.0 × 24.0 × 110.0 | 42,000 | ±2% |
| `stl/BT4V_Bay_Bracket.stl` | 50.0 × 18.0 × 40.0 | 19,200 | ±2% |
| `stl/BT4V_Spine_Segment.stl` | 30.0 × 14.0 × 110.0 | 21,000 | ±2% |
| `stl/BT4V_Phase_Crossover.stl` | 35.0 × 12.0 × 30.0 | 6,100 | ±2% |
| `stl/BT4V_Bowtie_Backing.stl` | 180.0 × 12.0 × 8.0 | 2,200 | ±2% |
| `stl/BT4V_Hanging_Cap.stl` | 44.0 × 18.0 × 30.0 | 7,400 | ±2% |
| `stl/BT4V_Fit_Coupon.stl` | 90.0 × 50.0 × 10.0 | 26,500 | ±2% |

---

## 17. Out of Scope

- Active powered preamps or motorized rotators.
- Heavy metallic reflector screens (design is optimized for lightweight window hanging).
- Custom winding of RF baluns (commercial RCA VH101R is used directly).
- Outdoor mast mounting hardware beyond lightweight window suspension.

---

## 18. Revision History

| Version | Date | Description |
|---|---|---|
| **0.1.0** | November 2026 | Initial project baseline for **BT4-V 3D Printed Antenna**. |
| **0.2.0** | November 2026 | Added specification for localized **Mid-Span Bowtie Support Struts** (`bt4v_bowtie_support.py`) to assist arm positioning. |
| **0.3.0** | November 2026 | Replaced localized tine spreaders and mid-span supports with universal interlocking **Full-Length Bowtie Backing Struts** (`bt4v_bowtie_backing.py`, 1 per UHF arm, 2 daisy-chained per VHF arm) and unified 130.0 mm bay pitch with straight-through 25.0 mm phase-line grooves. |
