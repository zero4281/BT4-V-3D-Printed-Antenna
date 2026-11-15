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
5. [Step 3: Full-Length Bowtie Backing Strut Installation](#5-step-3-full-length-bowtie-backing-strut-installation)
6. [Step 4: Modular Spine Assembly](#6-step-4-modular-spine-assembly)
7. [Step 5: Phase Line Routing & Crossover Installation](#7-step-5-phase-line-routing--crossover-installation)
8. [Step 6: Bay Bracket, Whisker, & Balun Assembly](#8-step-6-bay-bracket-whisker--balun-assembly)
9. [Step 7: Window Suspension & Tuning](#9-step-7-window-suspension--tuning)
10. [Troubleshooting & Maintenance](#10-troubleshooting--maintenance)

---

## 1. Overview & Prerequisites

The **BT4-V** is an ultra-lightweight (~235 g total printed mass), high-performance 4-bay bowtie digital television (DTV) antenna with integrated VHF-High coverage. It features a modular 3D-printed vertical spine at an exact **130.0 mm** bay pitch, continuous interlocking full-length bowtie backing struts across all 16 whisker arms to eliminate gravity sag, and direct clip-in integration for an RCA VH101R matching transformer.

### Required Tools & Materials
- **3D Printer:** Minimum build volume 220 × 220 mm or 235 × 235 × 250 mm.
- **Filament:** PETG (recommended for sunny window deployment) or PLA (indoor use).
- **Wire:** 12 AWG solid copper wire (bare conductor Ø2.05 mm, THHN insulated outer ~3.0 mm). Approximately 5.6 metres total.
- **Hardware:** 10 × M4 × 20 mm hex-head bolts, hex nuts, and flat washers.
- **Spine Pins:** 8–10 × Ø2.5 mm cross-pins, trimmed finish nails, or M2.5 × 12 mm screws (7 active spine joints + spares).
- **Balun:** RCA Outdoor Matching Transformer (VH101R) 300:75 Ω 4:1.
- **Feedline:** Standard 75 Ω RG6 coaxial cable with male F-connectors.
- **Hand Tools:** Wire cutters, wire strippers, pliers, metric hex key / driver.

---

## 2. Print Quantities & Slicing Settings

Before assembly, print the required quantities from the `stl/` directory. All parts are designed to be printed **flat on the build plate without supports**.

| Part Name | STL File | Qty Required | Extents (X × Y × Z mm) | Slicing / Print Notes |
|---|---|---|---|---|
| **Center Feed Hub** | `BT4V_Center_Feed.stl` | **1** | 40.0 × 24.0 × 110.0 | Print flat on rear face; 3 perimeters, 30% gyroid infill. |
| **Whisker Bay Bracket** | `BT4V_Bay_Bracket.stl` | **4** | 50.0 × 18.0 × 40.0 | Print flat on rear face; 3 perimeters, 30% gyroid infill. |
| **Spine Segment** | `BT4V_Spine_Segment.stl` | **2** | 30.0 × 14.0 × 110.0 | Print flat on rear face; 3 perimeters, 30% gyroid infill. |
| **Phase Crossover Spacer** | `BT4V_Phase_Crossover.stl` | **2** | 35.0 × 12.0 × 30.0 | Print flat; 3 perimeters, 30% infill. |
| **Full-Length Bowtie Backing Strut** | `BT4V_Bowtie_Backing.stl` | **24** | 180.0 × 12.0 × 8.0 | Print flat on base; 3 perimeters, 30% infill (1/arm UHF [8], 2/arm VHF [16]). |
| **Top Hanging Cap** | `BT4V_Hanging_Cap.stl` | **1** | 44.0 × 18.0 × 30.0 | Print flat; 3 perimeters, 30% infill. |
| **Fit Calibration Coupon** | `BT4V_Fit_Coupon.stl` | **1** *(Optional)* | 90.0 × 50.0 × 10.0 | Print first to test printer tolerances. |

---

## 3. Step 1: Pre-Print Tolerance Verification (Fit Coupon)

1. Print `stl/BT4V_Fit_Coupon.stl` using your target print profile.
2. Test **12 AWG wire fit** in the 2.8–3.4 mm friction channels and the 2.2 / 2.4 mm C-clip snap channels. The wire should snap in firmly with positive retention.
3. Verify **M4 hardware** — M4 bolts should pass smoothly through 4.3 mm clearance holes, and M4 hex nuts should seat snugly into the 7.2 mm hex pockets.
4. Verify **interlocking spine tenon/mortise joints**, **backing strut socket**, and 2.5 mm cross-pin alignment holes.
5. If tolerances are too tight or loose due to printer flow rate calibration, adjust your slicer horizontal expansion or flow rate and re-print before producing full production parts.

---

## 4. Step 2: Wire Preparation & Bending

Cut all wire lengths from 12 AWG solid copper wire and deburr ends:
- **VHF-High Whiskers (Bays 1 & 4):** Cut **4 lengths at 690 mm each**. Bend each wire at its midpoint around an M4 bolt to a **25.5° flare angle** (yielding two 340 mm arms from apex to tip, ~680 mm total tip-to-tip span, 150 mm tine spread).
- **UHF Whiskers (Bays 2 & 3):** Cut **4 lengths at 410 mm each**. Bend each wire at its midpoint around an M4 bolt to a **32.5° flare angle** (yielding two 200 mm arms from apex to tip, ~400 mm total tip-to-tip span, 115 mm tine spread).
- **Phase Lines:** Cut **2 straight lengths at ~580 mm each** for the vertical 25.0 mm pitch spine bus.

---

## 5. Step 3: Full-Length Bowtie Backing Strut Installation

1. Take the 24 printed `BT4V_Bowtie_Backing` struts (`180 mm` total length, `170 mm` active span).
2. **For the 4 UHF V-Whiskers (8 arms @ 200 mm each, Bays 2 & 3):**
   - Snap **1 backing strut** onto each upper and lower arm (8 struts total). Combined with the `15 mm` supported inside the Bay Bracket wing channel, a single strut supports the entire `200 mm` UHF arm to its tip.
3. **For the 4 VHF-High V-Whiskers (8 arms @ 340 mm each, Bays 1 & 4):**
   - Interlock **2 backing struts** end-to-end for each arm by inserting the outer strut's male root tenon (`-X`) into the inner strut's female tip mortise (`+X`).
   - Snap the daisy-chained pair onto each upper and lower VHF arm (16 struts total). Combined with the `15 mm` inside the Bay Bracket wing channel, the two interlocked struts support the full `340 mm` VHF arm from root to tip.
4. **Purpose:** The C-clip snap channel (`2.4 mm` throat into `3.2 mm` circular cavity) grips the 12 AWG wire along its entire length, permanently locking exact flare angles (`32.5°` UHF, `25.5°` VHF) and eliminating gravity sag or vibration.

---

## 6. Step 4: Modular Spine Assembly

1. Arrange the 8 modular spine components vertically from top to bottom (yielding an exact **130.0 mm** center-to-center pitch between all adjacent bays):
   - **Top Hanging Cap** (`BT4V_Hanging_Cap.stl`)
   - **Bay Bracket 1** (VHF-High, top — `Z = +195.0 mm`)
   - **Spine Segment 1** (`100.0 mm` active length between Bays 1 & 2)
   - **Bay Bracket 2** (UHF, upper-center — `Z = +65.0 mm`)
   - **Center Feed Hub** (`100.0 mm` active length directly between Bays 2 & 3 — feedpoint at `Z = 0.0 mm`)
   - **Bay Bracket 3** (UHF, lower-center — `Z = -65.0 mm`)
   - **Spine Segment 2** (`100.0 mm` active length between Bays 3 & 4)
   - **Bay Bracket 4** (VHF-High, bottom — `Z = -195.0 mm`)
2. Slide each male tenon (+Z) into the corresponding female mortise (-Z) of the adjacent component.
3. Lock all 7 spine joints securely by inserting a **Ø2.5 mm cross-pin** (or trimmed finish nail / M2.5 × 12 mm screw) through each cross-pin hole.

---

## 7. Step 5: Phase Line Routing & Crossover Installation

1. Lay the two straight vertical 12 AWG phase-line wires into the parallel wire routing grooves running down the front face of the Bay Brackets, Spine Segments, and Center Feed Hub (spaced **25.0 mm** center-to-center straight through).
2. Snap the **2 Phase Crossover Spacers** (`BT4V_Phase_Crossover.stl`) onto the mid-span waist of Spine Segment 1 (between Bays 1–2) and Spine Segment 2 (between Bays 3–4).
3. Route the phase lines through the diagonal crossing channels on the spacers.
4. **Phase Transposition:** The crossovers invert the phase lines by 180° between the outer VHF bays and inner UHF bays, ensuring all four bays drive in exact electrical phase.
5. Verify that the crossover spacers maintain **≥5.0 mm physical air/dielectric gap** between crossing conductors to prevent electrical shorting.

---

## 8. Step 6: Bay Bracket, Whisker, & Balun Assembly

1. **Whisker & Backing Strut Mounting:** Seat the apex of each prepared V-whisker into its Bay Bracket (`Z = 15.0 mm`), and plug the inner root tenons of the upper and lower backing struts into the 4 lateral sockets on each Bay Bracket.
2. **Clamping:** Insert **M4 × 20 mm bolts** with flat washers through the front clamp posts, clamping the whisker apex directly against the vertical phase line, and thread them into M4 hex nuts captured in the rear hex pockets. Tighten securely for low-resistance electrical contact.
3. **Center Feed & Balun:**
   - Snap the **RCA VH101R matching transformer** firmly into the custom cavity cradle on the Center Feed Hub.
   - Secure the transformer's spade lugs directly to the M4 terminal studs (`Z = 50.0 mm`) on the Center Feed Hub using M4 bolts, washers, and captured nuts (clamping both phase lines and balun lugs simultaneously).
   - Secure the RG6 coaxial cable strain relief using a zip-tie through the lower slot on the Center Feed Hub.

---

## 9. Step 7: Window Suspension & Tuning

1. **Hanging:** Attach nylon cord, picture wire, or suction-cup window hooks through the **dual Ø5.0 mm suspension eyelets** (`30.0 mm` spacing) on the Top Hanging Cap.
2. **Azimuth Alignment:** Hang the antenna against an indoor glass window facing directly toward the local broadcast transmitter towers.
3. **Screen Clearance:** Maintain at least **0.5 metres (50 cm) of separation** between the antenna whiskers and any metallic window insect screens to prevent UHF attenuation.
4. **Coaxial Connection:** Connect your 75 Ω RG6 coaxial cable from the television tuner to the downward-facing F-connector on the RCA VH101R balun.
5. **Channel Scan:** Run a digital television (DTV) channel scan on your TV or converter box to verify reception across both VHF-High (Channels 7–13) and UHF (Channels 14–36) bands.

---

## 10. Troubleshooting & Maintenance

- **Weak VHF Reception:** Ensure the outer V-whiskers on Bays 1 and 4 have their full 340 mm arm length and 25.5° flare angle locked securely by the daisy-chained backing struts.
- **SWR / Impedance Mismatch:** Check that all M4 terminal connections on the bay brackets and center feed are fully tightened and free of insulation or oxidation at the contact point.
- **Thermal Warping:** If deployed in direct, intense sunlight behind un-tinted glass, ensure parts are printed in **PETG or ASA** rather than standard PLA.
