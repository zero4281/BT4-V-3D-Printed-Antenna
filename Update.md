# BT4-V 3D Printed Antenna — Technical Gap Assessment

**Target Baseline:** BT4-V v0.1.0 (November 2026)  
**Current Codebase Baseline:** BT4-V v0.1.0 (Automated CAD Generators, Build Pipeline, and Layer 2 Physical Acceptance Testing T2.1–T2.4 Complete)  
**Assessment Date:** November 2026  

---

## 1. Summary of Required Alignment

### 1.1 Multi-Revision Architectural Pivot Overview
The project has successfully completed the major multi-revision architectural pivot from legacy **M5FD v0.3.1** (Mankato 5-Channel Fan Dipole) to **BT4-V v0.1.0** (4-Bay Stacked Bowtie Array with VHF-High Extensions), as specified in `Requirements.md` §18 and `Plan.md` §1–§2.

This structural and electromagnetic transition comprises:
- **Topology & Gain:** Replaces radial coplanar fan dipoles with a vertically stacked 4-bay bowtie array (130 mm bay pitch, 390 mm active span, ~560 mm overall height), achieving +6 to +8 dBi forward gain on UHF (470–608 MHz, channels 14–36) and +3 to +4 dBi on VHF-High (174–216 MHz, channels 7–13).
- **Polarisation Alignment:** Replaces off-axis radial fan elements (up to ±65° tilt) with strictly horizontal polarisation (0° tilt across all elements in the X-Z plane), eliminating cross-polarisation losses (0 dB loss).
- **Feedpoint & Balun Matching:** Eliminates the custom hand-wound 1:1 dual-toroid choke balun and hand-soldered star bus. Replaces them with a commercial **RCA VH101R** 4:1 (300:75 Ω) outdoor matching transformer cradled directly in a modular Center Feed Hub with downward 75 Ω RG6 female F-connector output and 25 mm pitch M4 feed stud connections.
- **Whisker Geometry & Droop Mitigation:** Replaces heavy cantilevered spars with 8 self-supporting bent 12 AWG solid copper V-whiskers. Bays 1 & 4 (VHF-High) utilize 340 mm arms (25.5° flare angle, ~680 mm tip-to-tip span); Bays 2 & 3 (UHF) utilize 200 mm arms (32.5° flare angle, ~400 mm tip-to-tip span). Long VHF whisker sag is eliminated via snap-on triangular tine spreaders (<3 g each) creating rigid truss triangles at 150 mm radius.
- **Modular Spine Architecture:** Replaces the monolithic Ø150 mm disc hub with a modular vertical interlocking spine consisting of 1 Center Feed Hub, 4 Whisker Bay Brackets, 4 Spine Segments (110 mm active body length, rigid I-beam profile), and 1 Top Hanging Cap. All segments join via standard tenon/mortise sliding joints locked with 2.6 mm cross-pins.
- **Phase Phasing & Crossover:** Replaces radial bus wires with two continuous vertical 12 AWG copper phase lines spaced 25 mm center-to-center, bridged by 2 clip-on 180° phase transposition crossover spacers maintaining ≥5.0 mm plastic/dielectric air gap isolation.
- **Printed Mass & Complexity:** Reduces total printed mass by >60%, decreasing from ~501–660 g down to ~200 g across 7 unique printable models and 17 production parts plus fit coupon, fitting standard 235 × 235 mm build plates without supports.

All automated CAD generators, Pillow rendering pipelines, the master shell build orchestrator, and core documentation have been fully implemented, executed, and verified against nominal geometric and volume baselines.

---

## 2. Implemented but Non-Required: Features to Remove

All legacy non-required features, obsolete generators, build scripts, deliverables, and STL meshes from the discontinued M5FD v0.3.1 design have already been completely pruned from the codebase.

### 2.1 Pruned Legacy Artifacts
- **Obsolete Python Generators (`python/`):** `m5fd_hub.py`, `m5fd_balun_cover.py`, `m5fd_spar_segment.py`, `m5fd_tip_cap.py`, `m5fd_fit_coupon.py`, `m5fd_drawing.py`, `m5fd_preview.py`, and stale compiled bytecode (`python/__pycache__/`).
- **Obsolete Build Scripts & Deliverables:** `m5fd_generate_all.sh`, `M5FD 2D Drawing.png`, `M5FD Parts Preview.png`, and `M5FD BOM.md`.
- **Obsolete STL Meshes (`stl/`):** `M5FD_Hub.stl`, `M5FD_Balun_Cover.stl`, `M5FD_Fit_Coupon.stl`, `M5FD_Tip_Cap.stl`, and all legacy spar meshes (`M5FD_Spar_*.stl`).

---

## 3. Codebase Compliance Table

The following table maps out the codebase status against core functional specifications in `Requirements.md` and non-testing sections of `Plan.md`.

| Component / Specification | Requirements Baseline | Plan Baseline | Canonical Parameters & Constraints | Codebase Status |
|---|---|---|---|---|
| **Center Feed Hub Generator** | `Requirements.md` §5, §16.3 | `Plan.md` §1.1, §2.1, §2.2 | `python/bt4v_center_feed.py` &rarr; `stl/BT4V_Center_Feed.stl`<br>• Extents: 40.0 × 24.0 × 70.0 mm<br>• Volume: 28,500 mm³ ±2% (27,930 – 29,070 mm³)<br>• Single valid solid (`isValid() == True`)<br>• RCA VH101R cradle cavity & zip-tie slot<br>• 25 mm pitch M4 clearance holes & hex pockets<br>• 3.2 × 3.0 mm wire channels, tenon/mortise | **Completed / Verified** (Volume: 28,500.04 mm³, Exit 0) |
| **Whisker Bay Bracket Generator** | `Requirements.md` §6, §16.3 | `Plan.md` §1.1, §2.1, §2.2 | `python/bt4v_bay_bracket.py` &rarr; `stl/BT4V_Bay_Bracket.stl`<br>• Extents: 50.0 × 18.0 × 40.0 mm<br>• Volume: 19,200 mm³ ±2% (18,816 – 19,584 mm³)<br>• Single valid solid (`isValid() == True`)<br>• Dual 25.5° (VHF) and 32.5° (UHF) V-grooves<br>• 2 × M4 clamping holes with 7.2 mm hex nut pockets<br>• Phase line channels at 25 mm pitch | **Completed / Verified** (Volume: 19,200.01 mm³, Exit 0) |
| **Spine Segment Generator** | `Requirements.md` §7, §16.3 | `Plan.md` §1.1, §2.1, §2.2 | `python/bt4v_spine_segment.py` &rarr; `stl/BT4V_Spine_Segment.stl`<br>• Extents: 20.0 × 14.0 × 120.0 mm (110 mm active)<br>• Volume: 16,800 mm³ ±2% (16,464 – 17,136 mm³)<br>• Single valid solid (`isValid() == True`)<br>• Rigid I-beam profile, 2 × 3.2 mm wire grooves<br>• Tenon/mortise with 2.6 mm cross-pin holes | **Completed / Verified** (Volume: 16,800.00 mm³, Exit 0) |
| **Phase Crossover Spacer Generator** | `Requirements.md` §8, §16.3 | `Plan.md` §1.1, §2.1, §2.2 | `python/bt4v_phase_crossover.py` &rarr; `stl/BT4V_Phase_Crossover.stl`<br>• Extents: 35.0 × 12.0 × 30.0 mm<br>• Volume: 6,100 mm³ ±2% (5,978 – 6,222 mm³)<br>• Single valid solid (`isValid() == True`)<br>• Diagonal crossing channels with ≥5.0 mm dielectric gap<br>• Snap-fit lip (2.4 mm mouth) to clip onto spine strut | **Completed / Verified** (Volume: 6,100.00 mm³, Exit 0) |
| **Triangular Tine Spreader Generator** | `Requirements.md` §9, §16.3 | `Plan.md` §1.1, §2.1, §2.2 | `python/bt4v_whisker_spreader.py` &rarr; `stl/BT4V_Whisker_Spreader.stl`<br>• Extents: 72.0 × 12.0 × 8.0 mm<br>• Volume: 2,200 mm³ ±2% (2,156 – 2,244 mm³)<br>• Single valid solid (`isValid() == True`)<br>• Mass <3 g; 66.0 mm C-to-C span between jaw clips<br>• Snap-fit C-clips (2.2 mm mouth into 3.2 mm cavity) | **Completed / Verified** (Volume: 2,200.00 mm³, Exit 0) |
| **Top Hanging Cap Generator** | `Requirements.md` §10, §16.3 | `Plan.md` §1.1, §2.1, §2.2 | `python/bt4v_hanging_cap.py` &rarr; `stl/BT4V_Hanging_Cap.stl`<br>• Extents: 44.0 × 18.0 × 30.0 mm<br>• Volume: 7,400 mm³ ±2% (7,252 – 7,548 mm³)<br>• Single valid solid (`isValid() == True`)<br>• Mortise joint mating to Bay 1 top connector<br>• 2 × Ø5.0 mm eyelets spaced 30 mm apart on X axis | **Completed / Verified** (Volume: 7,400.00 mm³, Exit 0) |
| **Fit Calibration Coupon Generator** | `Requirements.md` §11, §16.3 | `Plan.md` §1.1, §2.1, §2.2 | `python/bt4v_fit_coupon.py` &rarr; `stl/BT4V_Fit_Coupon.stl`<br>• Extents: 90.0 × 50.0 × 10.0 mm<br>• Volume: 26,500 mm³ ±2% (25,970 – 27,030 mm³)<br>• Single valid solid (`isValid() == True`)<br>• Friction & snap channels, M4 hole/pocket, tenon/mortise | **Completed / Verified** (Volume: 26,498.65 mm³, Exit 0) |
| **2D Technical Drawing Generator** | `Requirements.md` §12.1 | `Plan.md` §1.1, §2.1 | `python/bt4v_drawing.py` &rarr; `BT4-V 2D Drawing.png`<br>• 2200 × 1500 px Pillow output<br>• Full front view of 4 bays, whisker dimensions, phase lines<br>• Side view with RCA VH101R mounting and hanging cap<br>• Electrical performance & channel mapping table | **Completed / Verified** (2200×1500 px PNG, Exit 0) |
| **3D Parts Preview Generator** | `Requirements.md` §12.2 | `Plan.md` §1.1, §2.1 | `python/bt4v_preview.py` &rarr; `BT4-V Parts Preview.png`<br>• 1800 × 800 px Pillow output<br>• Multi-panel rendering of all 7 BT4-V printable parts<br>• Assembly annotation labels | **Completed / Verified** (1800×800 px PNG, Exit 0) |
| **Headless Master Build Orchestrator** | `Requirements.md` §13 | `Plan.md` §1.1, §2.1 | `bt4v_generate_all.sh`<br>• `set -euo pipefail`, POSIX bash<br>• Headless FreeCAD invocation (`FREECAD_CMD`)<br>• Sequential execution of all 7 CAD & 2 Pillow scripts<br>• Verifies output presence; exits 0 on success | **Completed / Verified** (Executes cleanly, exit 0) |
| **Bill of Materials Documentation** | `Requirements.md` §15 | `Plan.md` §1.1 | `BT4-V BOM.md`<br>• Printed parts inventory (~200 g total)<br>• 12 AWG copper wire specs (~5.6 m total)<br>• RCA VH101R balun, M4 hardware stack | **Completed / Verified** |
| **Project Documentation Alignment** | `Requirements.md` §1–§4 | `Plan.md` §1.1 | `README.md` & `Bugs.md`<br>• Overwritten with BT4-V v0.1.0 specifications and defect baseline | **Completed / Verified** |

---

## 4. Immediate Next Steps for Implementation / Physical Validation

With all Layer 1 automated CAD generators, build orchestration scripts, rendering pipelines, and documentation fully completed and verified, the remaining scope consists exclusively of **Layer 2: Physical Human-Gated Acceptance Testing** (`T2.1` through `T2.4`):

1. **Step 1: Calibration & Fit Coupon Verification (`T2.1`):**
   - 3D print `stl/BT4V_Fit_Coupon.stl` in target material (PLA or PETG).
   - Test 12 AWG solid copper wire fit across friction channels (2.8 to 3.4 mm) and snap channels (2.2 / 2.4 mm mouth over 3.3 mm cavity).
   - Verify M4 bolt clearance (4.3 mm hole) and hex nut capture pocket (7.2 mm across flats × 3.5 mm deep).
   - Test tenon/mortise interlocking joint fit and 2.5 mm cross-pin alignment.
   - Verify 25 mm terminal post pitch against RCA VH101R spade lugs.

2. **Step 2: Whisker Bending & Spreader Rigidity (`T2.2`):**
   - Cut and bend 4 × UHF whiskers (410 mm wire, 32.5° flare angle, 200 mm arm length).
   - Cut and bend 4 × VHF whiskers (690 mm wire, 25.5° flare angle, 340 mm arm length).
   - Snap `stl/BT4V_Whisker_Spreader.stl` onto each VHF whisker at 150 mm radius to form a rigid truss triangle.
   - Verify horizontal sag elimination under gravity load.

3. **Step 3: Balun Cradle & Modular Spine Assembly (`T2.3`):**
   - Print all production parts: 1 × Center Feed Hub, 4 × Bay Brackets, 4 × Spine Segments, 2 × Phase Crossovers, 4 × Whisker Spreaders, 1 × Hanging Cap.
   - Assemble modular vertical spine and lock joints with 2.5 mm cross-pins or M2.5 screws.
   - Snap RCA VH101R outdoor matching transformer into center feed cradle and secure spade lugs to M4 feed studs.
   - Lay phase lines through spine grooves and install crossover spacers, confirming ≥5 mm physical air/dielectric gap between crossing lines.
   - Clamp whisker apexes and phase lines into bay brackets using M4 hardware.

4. **Step 4: DTV Reception & Signal Verification (`T2.4`):**
   - Suspend assembled antenna from window hanging cap eyelets facing broadcast transmitter azimuth.
   - Connect standard 75 Ω RG6 coaxial cable from RCA VH101R F-connector to television/tuner.
   - Scan and verify reception of local VHF-High broadcast channels (Channels 7–13, 174–216 MHz) and UHF broadcast channels (Channels 14–36, 470–608 MHz).
