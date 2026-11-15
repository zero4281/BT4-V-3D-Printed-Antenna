# BT4-V 3D Printed Antenna — Bill of Materials (BOM)

**Version:** 0.3.0  
**Project:** BT4-V 3D Printed Antenna  
**Primary Output:** Complete printed parts inventory, raw materials, fasteners, and commercial hardware stack  

---

## 1. 3D Printed Parts Inventory

All 3D printed parts are designed for FDM fabrication without supports using standard 220 × 220 mm or 235 × 235 × 250 mm print beds. Total production printed mass is approximately **235 grams** across **34 production parts** (plus optional calibration coupon).

| Item | Part Name | STL File | Qty | Extents (X × Y × Z mm) | Nominal Volume | Target Mass | Material & Slicing Notes |
|---|---|---|---|---|---|---|---|
| **1** | Center Feed Hub | `BT4V_Center_Feed.stl` | **1** | 40.0 × 24.0 × 110.0 | 42,000 mm³ | ~52 g | PETG/PLA, 3 perimeters, 30% infill |
| **2** | Whisker Bay Bracket | `BT4V_Bay_Bracket.stl` | **4** | 50.0 × 18.0 × 40.0 | 19,200 mm³ | ~24 g each (96 g total) | PETG/PLA, 3 perimeters, 30% infill |
| **3** | Spine Segment | `BT4V_Spine_Segment.stl` | **2** | 30.0 × 14.0 × 110.0 | 21,000 mm³ | ~26 g each (52 g total) | PETG/PLA, 3 perimeters, 30% infill |
| **4** | Phase Crossover Spacer | `BT4V_Phase_Crossover.stl` | **2** | 35.0 × 12.0 × 30.0 | 6,100 mm³ | ~7.5 g each (15 g total) | PETG/PLA, 3 perimeters, 30% infill |
| **5** | Full-Length Bowtie Backing Strut | `BT4V_Bowtie_Backing.stl` | **24** | 180.0 × 12.0 × 8.0 | 2,200 mm³ | ~2.7 g each (65 g total) | 1/arm UHF (8 pcs) + 2/arm VHF (16 pcs) |
| **6** | Top Hanging Cap | `BT4V_Hanging_Cap.stl` | **1** | 44.0 × 18.0 × 30.0 | 7,400 mm³ | ~9 g | PETG/PLA, 3 perimeters, 30% infill |
| **Total** | **Complete Production Set** | — | **34 parts** | — | **~189,000 mm³** | **~235 g** | **PLA (indoor) or PETG/ASA (sunny window)** |
| **7** | Fit Calibration Coupon *(Optional)* | `BT4V_Fit_Coupon.stl` | **1** | 90.0 × 50.0 × 10.0 | 26,500 mm³ | ~32 g | Print first to verify printer tolerances |

---

## 2. Raw Conductors & Wire Stack

| Item | Description | Spec / Dimensions | Total Qty Required | Source / Notes |
|---|---|---|---|---|
| **1** | **VHF Whiskers** | 12 AWG solid copper wire | 4 lengths @ 690 mm | Cut, deburred, bent to 25.5° flare angle (Bays 1 & 4; 340 mm arms) |
| **2** | **UHF Whiskers** | 12 AWG solid copper wire | 4 lengths @ 410 mm | Cut, deburred, bent to 32.5° flare angle (Bays 2 & 3; 200 mm arms) |
| **3** | **Phase Lines** | 12 AWG solid copper wire | 2 lengths @ ~580 mm | Straight vertical spine bus lines (25.0 mm center-to-center pitch) |
| **Total Wire** | **12 AWG Solid Copper (THHN / Bare)** | Ø2.05 mm bare conductor | **~5.6 metres** | Standard electrical building wire (strip THHN at clamping points) |

---

## 3. Fasteners & Mechanical Hardware

| Item | Description | Size / Dimensions | Qty | Purpose |
|---|---|---|---|---|
| **1** | Hex-Head Bolts | M4 × 20 mm stainless or zinc steel | **10 pcs** | Whisker apex clamping (8) and center feed terminal posts (2) |
| **2** | Hex Nuts | M4 standard hex nut (7.2 mm across flats) | **10 pcs** | Captured in rear hex pockets of bay brackets and center feed |
| **3** | Flat Washers | M4 stainless steel flat washer | **10 pcs** | Load distribution under bolt heads and phase lines |
| **4** | Spine Cross-Pins | Ø2.5 mm pins, finish nails, or M2.5 × 12 mm screws | **8–10 pcs** | Locks the 7 tenon/mortise spine joints (plus spares) |

---

## 4. Commercial RF & Electrical Components

| Item | Component Description | Model / Part # | Qty | Function & Integration |
|---|---|---|---|---|
| **1** | **Matching Transformer (Balun)** | RCA Outdoor Matching Transformer | **RCA VH101R** | **1** | 300 Ω balanced (antenna feedpoint) to 75 Ω unbalanced (RG6 coaxial downlead), ratio 4:1. Spade lugs mount directly to center feed M4 studs. |
| **2** | **Coaxial Feedline** | RG6 75 Ω Coaxial Cable | Standard RG6 | As required | Connects balun F-connector to television or digital tuner. |
| **3** | **Window Mounting** | Suction-cup hooks / nylon hanging cord | Rated ≥1 kg | **1 set** | Suspends antenna from top hanging cap eyelets against window glass. |

---

## 5. Recommended 3D Printing Profile Summary

- **Nozzle Diameter:** 0.4 mm
- **Layer Height:** 0.2 mm
- **Wall / Perimeter Count:** 3 perimeters (ensures solid structural strength for C-clip wire channels and tenons)
- **Infill Density:** 30%
- **Infill Pattern:** Gyroid or Grid
- **Support Material:** None required (all overhangs and snap channels are self-supporting and bridge-free).
- **Bed Adhesion:** Skirt or Brim.
