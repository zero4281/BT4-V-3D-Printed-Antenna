# BT4-V 3D Printed Antenna — Assembly Guide & Build Instructions

**Version:** 0.3.0  
**Project:** BT4-V 3D Printed Antenna  
**Primary Output:** Complete physical assembly, wiring, and window installation guide  

---

## Table of Contents

1. [Overview & Prerequisites](#1-overview--prerequisites)
2. [Print Quantities & Slicing Settings](#2-print-quantities--slicing-settings)
3. [Step 1: Pre-Print Tolerance Verification (Fit Coupon)](#3-step-1-pre-print-tolerance-verification-fit-coupon)
4. [Step 2: Wire Preparation & Bending](#4-step-2-wire-preparation--bending)
5. [Step 3: Bowtie Backing Strut Installation](#5-step-3-bowtie-backing-strut-installation)
6. [Step 4: Modular Spine Assembly](#6-step-4-modular-spine-assembly)
7. [Step 5: Phase Line Routing & Crossover Installation](#7-step-5-phase-line-routing--crossover-installation)
8. [Step 6: Bay Bracket, Whisker, & Balun Assembly](#8-step-6-bay-bracket-whisker--balun-assembly)
9. [Step 7: Window Suspension & Tuning](#9-step-7-window-suspension--tuning)
10. [Troubleshooting & Maintenance](#10-troubleshooting--maintenance)

---

## 1. Overview & Prerequisites

The **BT4-V** is an ultra-lightweight (~210 g total printed mass), high-performance 4-bay bowtie digital television (DTV) antenna with integrated VHF-High coverage. It features a modular 3D-printed vertical spine, continuous full-length bowtie backing struts to eliminate gravity sag, and direct clip-in integration for an RCA VH101R matching transformer.

### Required Tools & Materials
- **3D Printer:** Minimum build volume 235 × 235 × 250 mm.
- **Filament:** PETG (recommended for sunny window deployment) or PLA (indoor use).
- **Wire:** 12 AWG solid copper wire (bare conductor Ø2.05 mm, THHN insulated outer ~3.0 mm). Approximately 5.6 metres total.
- **Hardware:** 10 × M4 × 20 mm hex-head bolts, nuts, and flat washers.
- **Spine Pins:** 10 × 2.5 mm cross-pins, trimmed finish nails, or M2.5 × 12 mm screws.
- **Balun:** RCA Outdoor Matching Transformer (VH101R) 300:75 Ω 4:1.
- **Feedline:** Standard 75 Ω RG6 coaxial cable with male F-connectors.
- **Hand Tools:** Wire cutters, wire strippers, pliers, metric hex key set.

---

## 2. Print Quantities & Slicing Settings

Before assembly, print the required quantities from the `stl/` directory. All parts are designed to be printed **flat on the build plate without supports**.

| Part Name | STL File | Qty Required | Slicing / Print Notes |
|---|---|---|---|
| **Center Feed Hub** | `BT4V_Center_Feed.stl` | **1** | Print flat on base; 3 perimeters, 30% gyroid infill. |
| **Whisker Bay Bracket** | `BT4V_Bay_Bracket.stl` | **4** | Print flat on base; 3 perimeters, 30% gyroid infill. |
| **Spine Segment** | `BT4V_Spine_Segment.stl` | **4** | Print flat along Z axis; 3 perimeters, 30% gyroid infill. |
| **Phase Crossover Spacer** | `BT4V_Phase_Crossover.stl` | **2** | Print flat; 3 perimeters, 30% infill. |
| **Full-Length Bowtie Backing Strut** | `BT4V_Bowtie_Backing.stl` | **8** | Print flat on side; 3 perimeters, 30% infill (2 per bay across Bays 1–4). |
| **Top Hanging Cap** | `BT4V_Hanging_Cap.stl` | **1** | Print flat; 3 perimeters, 30% infill. |
| **Fit Calibration Coupon** | `BT4V_Fit_Coupon.stl` | **1** *(Optional)* | Print first to test printer tolerances. |

---

## 3. Step 1: Pre-Print Tolerance Verification (Fit Coupon)

1. Print `stl/BT4V_Fit_Coupon.stl` using your target print profile.
2. Test **12 AWG wire fit** in the 3.0 mm and 3.2 mm friction/snap channels. The wire should snap in firmly with positive retention.
3. Verify **M4 hardware** — M4 bolts should pass smoothly through 4.3 mm clearance holes, and M4 hex nuts should seat snugly into the 7.2 mm hex pockets.
4. Verify **interlocking tenon/mortise joints** and 2.5 mm cross-pin alignment holes.
5. If tolerances are too tight or loose due to printer flow rate calibration, adjust your slicer horizontal expansion or flow rate and re-print before producing full production parts.

---

## 4. Step 2: Wire Preparation & Bending

Cut all wire lengths from 12 AWG solid copper wire and deburr ends:
- **VHF-High Whiskers (Bays 1 & 4):** Cut **4 lengths at 690 mm each**. Bend each wire exactly at its midpoint to a **25.5° flare angle** (yielding 340 mm arms from apex to tip, ~680 mm total tip-to-tip span).
- **UHF Whiskers (Bays 2 & 3):** Cut **4 lengths at 410 mm each**. Bend each wire exactly at its midpoint to a **32.5° flare angle** (yielding 200 mm arms from apex to tip, ~400 mm total tip-to-tip span).
- **Phase Lines:** Cut **2 lengths at ~580 mm each** for the vertical spine bus.

---

## 5. Step 3: Bowtie Backing Strut Installation

1. Take the 8 printed `BT4V_Bowtie_Backing` struts.
2. Snap one backing strut onto the upper V-arm and one onto the lower V-arm of each of the 4 bowtie whiskers (8 struts total).
3. The continuous snap-fit channel grips the 12 AWG wire from the bay bracket root all the way to the outer tip.
4. **Purpose:** This permanently locks the exact flare angles (32.5° for UHF, 25.5° for VHF) and completely eliminates gravity sag, droop, or high-wind vibration.

---

## 6. Step 4: Modular Spine Assembly

1. Arrange the modular spine components vertically from top to bottom:
   - **Top Hanging Cap** (`BT4V_Hanging_Cap.stl`)
   - **Bay Bracket 1** (VHF-High, top)
   - **Spine Segment 1**
   - **Bay Bracket 2** (UHF, upper-center)
   - **Center Feed Hub** (between Bays 2 & 3)
   - **Bay Bracket 3** (UHF, lower-center)
   - **Spine Segment 3**
   - **Bay Bracket 4** (VHF-High, bottom)
   - Bottom spine segments as required.
2. Slide each male tenon (+Z) into the corresponding female mortise (-Z) of the adjacent segment.
3. Lock each joint securely by inserting a **2.5 mm cross-pin** (or trimmed finish nail / M2.5 × 12 mm screw) through the cross-pin holes.

---

## 7. Step 5: Phase Line Routing & Crossover Installation

1. Lay the two vertical 12 AWG phase-line wires into the parallel wire routing grooves running down the front face of the spine segments and center feed hub (spaced 25 mm center-to-center).
2. Install the **2 Phase Crossover Spacers** (`BT4V_Phase_Crossover.stl`) between Bay 1–2 and Bay 3–4.
3. Snap the phase lines into the diagonal crossing channels on the spacers.
4. **Phase Transposition:** The crossovers invert the phase lines by 180° between outer VHF bays and inner UHF bays, ensuring all four bays drive in exact electrical phase.
5. Verify that the crossover spacers maintain **≥5.0 mm physical air/dielectric gap** between crossing conductors to prevent electrical shorting.

---

## 8. Step 6: Bay Bracket, Whisker, & Balun Assembly

1. **Whisker Mounting:** Seat the apex of each prepared V-whisker into the vertical slot of its respective Bay Bracket, directly against the phase lines.
2. **Clamping:** Insert **M4 × 20 mm bolts** through the front clamp posts, passing through the whisker apex and phase lines, and thread them into M4 nuts captured in the rear hex pockets. Tighten securely to ensure low-resistance electrical contact.
3. **Center Feed & Balun:**
   - Snap the **RCA VH101R matching transformer** firmly into the custom cavity cradle on the Center Feed Hub.
   - Secure the transformer’s spade lugs directly to the M4 terminal studs on the center feed hub using M4 nuts and washers (clamping both phase lines and balun lugs simultaneously).
   - Secure the RG6 coaxial cable strain relief using a zip-tie through the lower slot on the center feed hub.

---

## 9. Step 7: Window Suspension & Tuning

1. **Hanging:** Attach nylon cord, picture wire, or suction-cup window hooks through the **dual Ø5.0 mm suspension eyelets** on the Top Hanging Cap.
2. **Azimuth Alignment:** Hang the antenna against an indoor glass window facing directly toward the local broadcast transmitter towers.
3. **Screen Clearance:** Maintain at least **0.5 metres (50 cm) of separation** between the antenna whiskers and any metallic window insect screens to prevent UHF attenuation.
4. **Coaxial Connection:** Connect your 75 Ω RG6 coaxial cable from the television tuner to the downward-facing F-connector on the RCA VH101R balun.
5. **Channel Scan:** Run a digital television (DTV) channel scan on your TV or converter box to verify reception across both VHF-High (Channels 7–13) and UHF (Channels 14–36) bands.

---

## 10. Troubleshooting & Maintenance

- **Weak VHF Reception:** Ensure the outer V-whiskers on Bays 1 and 4 have their full 340 mm arm length and 25.5° flare angle locked securely by backing struts.
- **SWR / Impedance Mismatch:** Check that all M4 terminal connections on the bay brackets and center feed are fully tightened and free of oxidation.
- **Thermal Warping:** If deployed in direct, intense sunlight behind un-tinted glass, ensure parts are printed in **PETG or ASA** rather than standard PLA.
