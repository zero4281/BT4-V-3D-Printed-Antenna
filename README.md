# BT4-V 3D Printed Antenna — 4-Bay Bowtie + VHF-High

**Version:** 0.3.0  
**Project:** BT4-V 3D Printed Antenna  
**Primary Output:** FreeCAD-generated STL parts, 2D technical drawing, and part preview rendering  

---

## 1. Overview

**BT4-V** is a high-performance, 4-bay bowtie digital television (DTV) antenna with integrated VHF-High coverage, engineered for 3D-printed fabrication and indoor window suspension.

The antenna combines:
- **Four co-phased bowtie bays** arranged vertically along a modular 3D-printed spine.
- **Strictly horizontal polarisation (0° tilt across all elements)**, eliminating cross-polarisation loss.
- **Dual-band coverage:** The inner two bays (Bays 2 and 3) are tuned for high-gain broadband UHF reception (470–608 MHz, channels 14–36), while the outer two bays (Bays 1 and 4, top and bottom) feature extended whiskers tuned for VHF-High reception (174–216 MHz, channels 7–13).
- **Full-Length Bowtie Backing Struts:** Continuous 3D-printed snap-fit backing struts running from bay bracket root to wire tip, permanently locking exact flare angles (32.5° UHF, 25.5° VHF) and completely eliminating gravity sag, droop, or vibration.
- **RCA VH101R Matching Transformer Integration:** A commercial 300:75 Ω outdoor matching transformer (4:1 balun) mounts directly to the center feed bracket via its screw lugs, providing a female F-connector output for direct 75 Ω RG6 coaxial feed to the television.

BT4-V delivers +6 to +8 dBi forward gain across UHF and +3 to +4 dBi across VHF-High in an ultra-lightweight (~210 g), flat, modular form factor fitting a standard window (<600 mm height).

---

## 2. Repository Structure

```
BT4-V-Antenna/
├── README.md                     # This document
├── Requirements.md               # Authoritative functional baseline
├── Plan.md                       # Implementation plan and task tracking
├── Testing Strategy.md           # Verification procedures and test baselines
├── Bugs.md                       # Issue tracker
├── ASSEMBLY.md                   # Step-by-step physical assembly & build guide
├── BT4-V BOM.md                  # Bill of materials and hardware stack
├── Update.md                     # Gap assessment and migration tracking
├── bt4v_generate_all.sh          # Headless build orchestrator
│
├── BT4-V 2D Drawing.png          # Generated technical drawing
├── BT4-V Parts Preview.png       # Generated 3D part rendering preview
│
├── python/                       # FreeCAD and Pillow generators
│   ├── bt4v_center_feed.py       # Center feed hub with RCA balun cradle
│   ├── bt4v_bay_bracket.py       # Whisker mounting bracket (Bays 1–4)
│   ├── bt4v_spine_segment.py     # Interlocking modular vertical spine struts
│   ├── bt4v_phase_crossover.py   # Phase-line crossover insulator / guide
│   ├── bt4v_bowtie_backing.py    # Full-length bowtie backing strut
│   ├── bt4v_hanging_cap.py       # Top hanging cap with suspension eyelets
│   ├── bt4v_fit_coupon.py        # Pre-print tolerance and snap-fit coupon
│   ├── bt4v_drawing.py           # 2D technical drawing generator (Pillow)
│   └── bt4v_preview.py           # 3D part preview generator (Pillow)
│
└── stl/                          # Generated 3D printable meshes (git-ignored)
    ├── BT4V_Center_Feed.stl
    ├── BT4V_Bay_Bracket.stl
    ├── BT4V_Spine_Segment.stl
    ├── BT4V_Phase_Crossover.stl
    ├── BT4V_Bowtie_Backing.stl
    ├── BT4V_Hanging_Cap.stl
    └── BT4V_Fit_Coupon.stl
```

`stl/` is git-ignored. Never hand-edit an STL file — modify the Python generators and regenerate.

---

## 3. Requirements & Dependencies

| Dependency | Minimum Version | Notes |
|---|---|---|
| **FreeCAD** | `>= 0.20` | Headless parametric 3D solid modelling (`Part`, `Mesh`) |
| **Python** | `>= 3.8` (Tested on 3.12) | Generator logic and math |
| **Pillow (`PIL`)** | `>= 9.0` (Tested on 10.2.0) | 2D technical drawing and 3D preview rendering |
| **System Fonts** | `DejaVu Sans` / `DejaVu Sans Bold` | Text rendering on deliverables |
| **POSIX Bash** | `>= 5.0` | Build orchestration (`bt4v_generate_all.sh`) |
| **3D Printer** | $\ge 235 \times 235 \times 250\text{ mm}$ | PETG or PLA recommended |

---

## 4. Build Orchestration

To regenerate all STL models and PNG drawings from clean source:

```bash
FREECAD_CMD=/snap/bin/freecad.cmd ./bt4v_generate_all.sh
```

On native Linux FreeCAD builds providing `freecadcmd`:
```bash
FREECAD_CMD=freecadcmd ./bt4v_generate_all.sh
```

---

## 5. Documentation

- `Requirements.md`: Authoritative engineering specification.
- `Plan.md`: Implementation status and task tracking.
- `Testing Strategy.md`: Verification procedures and build regression criteria.
- `ASSEMBLY.md`: Step-by-step physical assembly, wire preparation, and installation guide.
- `BT4-V BOM.md`: Complete bill of materials, fasteners, and print settings.
- `Update.md`: Gap assessment and migration tracking.

---

## 6. License & Proprietary Notice

**Proprietary — all rights reserved.** Copyright © 2026 zero4281. All rights reserved.
