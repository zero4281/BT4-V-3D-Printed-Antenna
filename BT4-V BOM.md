# BT4-V 3D Printed Antenna — Bill of Materials (BOM)

**Version:** 0.3.0  
**Project:** BT4-V 3D Printed Antenna  
**Primary Output:** Complete printed parts inventory, raw materials, fasteners, and commercial hardware stack  

---

## 1. 3D Printed Parts Inventory

All 3D printed parts are designed for FDM fabrication without supports using standard 235 × 235 × 250 mm print beds. Total printed mass is approximately **210 grams**.

| Item | Part Name | STL File | Qty | Target Mass | Material & Slicing Notes |
|---|---|---|---|---|---|
| **1** | Center Feed Hub | `BT4V_Center_Feed.stl` | **1** | ~32 g | PETG/PLA, 3 perimeters, 30% infill |
| **2** | Whisker Bay Bracket | `BT4V_Bay_Bracket.stl` | **4** | ~22 g each (88 g total) | PETG/PLA, 3 perimeters, 30% infill |
| **3** | Spine Segment | `BT4V_Spine_Segment.stl` | **4** | ~14 g each (56 g total) | PETG/PLA, 3 perimeters, 30% infill |
| **4** | Phase Crossover Spacer | `BT4V_Phase_Crossover.stl` | **2** | ~6 g each (12 g total) | PETG/PLA, 3 perimeters, 30% infill |
| **5** | Full-Length Bowtie Backing Strut | `BT4V_Bowtie_Backing.stl` | **8** | ~2.5 g each (20 g total) | PETG/PLA, 3 perimeters, 30% infill |
| **6** | Top Hanging Cap | `BT4V_Hanging_Cap.stl` | **1** | ~8 g | PETG/PLA, 3 perimeters, 30% infill |
| **7** | Fit Calibration Coupon | `BT4V_Fit_Coupon.stl` | **1** *(Optional)* | ~28 g | Print first to verify printer tolerances |
| **Total** | **Complete Production Set** | — | **20 parts** | **~216 g** | **PLA (indoor) or PETG/ASA (sunny window)** |

---

## 2. Raw Conductors & Wire Stack

| Item | Description | Spec / Dimensions | Total Qty Required | Source / Notes |
|---|---|---|---|---|
| **1** | **VHF Whiskers** | 12 AWG solid copper wire | 4 lengths @ 690 mm | Cut, deburred, bent to 25.5° flare angle (Bays 1 & 4) |
| **2** | **UHF Whiskers** | 12 AWG solid copper wire | 4 lengths @ 410 mm | Cut, deburred, bent to 32.5° flare angle (Bays 2 & 3) |
| **3** | **Phase Lines** | 12 AWG solid copper wire | 2 lengths @ ~580 mm | Vertical spine bus lines (25 mm center-to-center pitch) |
| **Total Wire** | **12 AWG Solid Copper (THHN / Bare)** | Ø2.05 mm bare conductor | **~5.6 metres** | Standard electrical building wire (THHN insulation optional) |

---

## 3. Fasteners & Mechanical Hardware

| Item | Description | Size / Dimensions | Qty | Purpose |
|---|---|---|---|---|
| **1** | Hex-Head Bolts | M4 × 20 mm stainless or zinc steel | **10 sets** | Whisker apex clamping and center feed terminal posts |
| **2** | Hex Nuts | M4 standard hex nut (7.2 mm across flats) | **10 pcs** | Captured in rear hex pockets of bay brackets and center feed |
| **3** | Flat Washers | M4 stainless steel flat washer | **10 pcs** | Load distribution under bolt heads and phase lines |
| **4** | Spine Cross-Pins | 2.5 mm diameter pins, finish nails, or M2.5 × 12 mm screws | **10 pcs** | Locks tenon/mortise spine segment joints |

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
- **Wall / Perimeter Count:** 3 perimeters (ensures solid structural strength for wire clamping jaws)
- **Infill Density:** 30%
- **Infill Pattern:** Gyroid or Grid
- **Support Material:** None required (all overhangs and snap channels are self-supporting and bridge-free).
- **Bed Adhesion:** Skirt or Brim (recommended for tall narrow parts like spine segments).
