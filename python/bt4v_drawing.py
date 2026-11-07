#!/usr/bin/env python3
"""
BT4-V 3D Printed Antenna — 2D Technical Drawing Generator (v0.3.0)

Generates the master engineering 2D technical drawing deliverable:
    'BT4-V 2D Drawing.png' (2200 × 1500 px) in the project root directory.

Technical Specifications & Requirements Baseline:
- Requirements Baseline: Requirements.md §3, §4, §12.1, §14, §16.3
- Plan Baseline: Plan.md §3.1 (T1.3)
- Deliverable: Exactly 2200 x 1500 px PNG image, >10 kB file size.
- Theme: High-contrast blueprint/engineering theme (#0B1D3A dark blue canvas,
  crisp white and cyan line art, copper element callouts, dimension lines,
  and formal ASME/ISO style title block).

Drawing Content:
1. Master Title Banner: BT4-V 4-BAY BOWTIE + VHF INDOOR WINDOW TV ANTENNA
2. Front Elevation View (Scale 1:1.4):
   - 4 vertically stacked bays at 130 mm pitch (390 mm active span, ~560 mm overall height)
   - Top Bay 1 (VHF-High, 680 mm tip-to-tip span, 25.5° flare angle, triangular tine spreaders at 150 mm radius)
   - Bay 2 (UHF, 400 mm tip-to-tip span, 32.5° flare angle)
   - Center Feed Hub (RCA VH101R matching transformer cradle, 25 mm C-to-C feed terminals, downward 75Ω F-connector)
   - Bay 3 (UHF, 400 mm tip-to-tip span, 32.5° flare angle)
   - Bottom Bay 4 (VHF-High, 680 mm tip-to-tip span, 25.5° flare angle, triangular tine spreaders at 150 mm radius)
   - 2 vertical 12 AWG copper phase lines (25 mm spacing) with 2 crossover transposition spacers
     between Bays 1–2 and Bays 3–4 (180° phase inversion)
   - Top Hanging Cap with dual anti-rotation eyelets (30 mm pitch, Ø5.0 mm)
   - Comprehensive engineering dimension callouts, leader lines, and flare arcs.
3. Side Profile View (Scale 1:1.4):
   - Vertically aligned orthographic projection with front elevation
   - Modular spine profile, I-beam ribs, whisker clamp hardware (M4 bolts & nuts)
   - Crossover clips on spine
   - RCA VH101R commercial balun mounting in Center Feed cradle with downward F-connector
   - 75Ω RG6 coaxial cable drop with zip-tie strain relief
   - Top hanging cap side yoke with suspension wire
4. Channel Mapping & Electrical Performance Table:
   - RF 8 (VHF-Hi 183 MHz, KEYC-DT CBS / KMNF-CD NBC)
   - RF 12 (VHF-Hi 207 MHz, KEYC-DT FOX / KEYC-HD CBS)
   - RF 14 (UHF 473 MHz, KMNF-LD NBC/CW / KSTPDT ABC)
   - RF 26 (UHF 545 MHz, KSTP-TV ABC / TPT 2 PBS)
   - RF 33 (UHF 587 MHz, Pioneer PBS / KMNFLD1 NBC)
   - Performance Targets: VHF-Hi Gain 5.5 dBi, UHF Gain 8.5 dBi, 300:75 Ω match via RCA VH101R, SWR < 2.0:1
5. Assembly, Wire-Bending & Hardware Specifications:
   - 12 AWG solid copper wire cut lengths: 4 × VHF (690 mm), 4 × UHF (410 mm), 2 × Phase lines (580 mm), total ~5.6 m
   - Hardware: 10 × M4 bolts/nuts, 10 × 2.5 mm cross-pins, RCA VH101R balun
   - 3D Printed Parts BOM (Center Feed, Bay Brackets, Spine Segments, Crossovers, Spreaders, Hanging Cap, Fit Coupon)
6. General Engineering Notes & Fabrication Instructions:
   - 3D printing parameters (0.2 mm layer, PETG/PLA, 4 perimeters, 25% infill)
   - Wire fabrication, bending templates, droop mitigation
   - Balun installation and window mounting spacing (≥0.5 m from metal insect screens)
7. Formal Engineering Title Block:
   - Revision v0.3.0, Scale, Date, Author, Third-Angle Projection symbol, L1 verification badge.

Usage:
    python3 python/bt4v_drawing.py
"""

import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# -----------------------------------------------------------------------------
# DIRECTORY SELF-RESOLUTION & CONSTANTS
# -----------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_FILENAME = "BT4-V 2D Drawing.png"
OUTPUT_PATH = os.path.join(PROJECT_ROOT, OUTPUT_FILENAME)

CANVAS_WIDTH = 2200
CANVAS_HEIGHT = 1500
MIN_FILE_SIZE_BYTES = 10 * 1024  # >10 kB per Testing Strategy §2.4

# -----------------------------------------------------------------------------
# COLOR PALETTE (High-Contrast Engineering Blueprint Theme)
# -----------------------------------------------------------------------------
COLOR_BG = (11, 29, 58)             # Deep blueprint dark blue #0B1D3A
COLOR_GRID_MINOR = (17, 40, 75)     # Blueprint fine grid
COLOR_GRID_MAJOR = (24, 52, 94)     # Blueprint major grid
COLOR_FRAME_OUTER = (59, 117, 196)  # Outer border #3B75C4
COLOR_FRAME_INNER = (31, 74, 128)   # Inner border
COLOR_PANEL_BG = (13, 34, 66)       # Subtle panel background
COLOR_PANEL_BORDER = (38, 86, 150)  # Panel bounding box
COLOR_HEADER_BG = (20, 52, 98)      # Panel header fill
COLOR_ROW_ALT = (16, 42, 80)        # Alternating table row fill

# Functional & Schematic Elements
COLOR_PLASTIC_FILL = (24, 60, 110)      # 3D printed components fill
COLOR_PLASTIC_OUTLINE = (92, 168, 255)  # 3D printed components stroke #5CA8FF
COLOR_PLASTIC_DETAIL = (48, 106, 184)   # Internal ribs / tenons
COLOR_COPPER = (255, 157, 66)           # 12 AWG copper conductors #FF9D42
COLOR_COPPER_REAR = (180, 100, 36)      # Transposed copper phase line (rear)
COLOR_HARDWARE = (225, 232, 245)        # M4 screws, captive nuts, cross-pins
COLOR_BALUN_BODY = (28, 46, 68)         # RCA VH101R balun casing
COLOR_BALUN_ACCENT = (144, 164, 174)    # RCA balun label/hardware
COLOR_COAX = (33, 43, 54)               # RG6 coax jacket
COLOR_COAX_HL = (100, 120, 140)         # RG6 coax highlight
COLOR_EYELET_RING = (120, 180, 255)     # Suspension cord / eyelets

# Annotation & Typography
COLOR_DIM_LINE = (79, 195, 247)         # Dimension lines & leader arrows #4FC3F7
COLOR_DIM_TEXT = (225, 245, 254)        # Dimension text pill fill / text
COLOR_CENTERLINE = (74, 144, 226)       # Centerline axis #4A90E2
COLOR_PROJECTION = (100, 160, 235)      # Orthographic projection lines
COLOR_TEXT_WHITE = (255, 255, 255)      # Primary titles and headings
COLOR_TEXT_CYAN = (129, 212, 250)       # Subheadings & emphasis #81D4FA
COLOR_TEXT_GOLD = (255, 183, 77)        # Electrical & callout highlights #FFB74D
COLOR_TEXT_GREEN = (129, 199, 132)      # Approved / pass status badges
COLOR_TEXT_MUTED = (165, 190, 220)      # Body descriptions & secondary specs


# -----------------------------------------------------------------------------
# FONT LOADER WITH COMPREHENSIVE FALLBACKS
# -----------------------------------------------------------------------------
def load_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.ImageFont:
    """Loads best available TrueType font on Linux/Unix systems with graceful fallback."""
    if mono:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf" if bold else
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf" if bold else
            "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
            "/usr/share/fonts/truetype/ubuntu/UbuntuMono[wght].ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
            "/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf",
        ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


# Font instances
FONT_MAIN_TITLE = load_font(23, bold=True)
FONT_MAIN_SUB = load_font(12, bold=False)
FONT_PANEL_HDR = load_font(14, bold=True)
FONT_SUBHDR = load_font(12, bold=True)
FONT_REGULAR = load_font(11, bold=False)
FONT_BOLD = load_font(11, bold=True)
FONT_SMALL = load_font(9, bold=False)
FONT_SMALL_BOLD = load_font(9, bold=True)
FONT_TINY = load_font(8, bold=False)
FONT_MONO = load_font(10, bold=False, mono=True)
FONT_MONO_BOLD = load_font(10, bold=True, mono=True)


# -----------------------------------------------------------------------------
# GRAPHICS PRIMITIVES & ANNOTATION UTILITIES
# -----------------------------------------------------------------------------
def draw_arrowhead(draw: ImageDraw.ImageDraw, x: float, y: float, angle_rad: float,
                   size: float = 7.0, color: tuple = COLOR_DIM_LINE):
    """Draws a solid filled engineering arrowhead pointing in angle_rad direction."""
    tip = (x, y)
    spread = 0.42  # radians (~24 degrees)
    left = (
        x - size * math.cos(angle_rad - spread),
        y - size * math.sin(angle_rad - spread)
    )
    right = (
        x - size * math.cos(angle_rad + spread),
        y - size * math.sin(angle_rad + spread)
    )
    draw.polygon([tip, left, right], fill=color)


def draw_dashed_line(draw: ImageDraw.ImageDraw, x1: float, y1: float, x2: float, y2: float,
                     color: tuple, dash: float = 6.0, gap: float = 4.0, width: int = 1):
    """Draws a dashed line from (x1, y1) to (x2, y2)."""
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    if dist < 1e-4:
        return
    ux = dx / dist
    uy = dy / dist
    traveled = 0.0
    drawing = True
    while traveled < dist:
        seg = min(dash if drawing else gap, dist - traveled)
        nx = x1 + (traveled + seg) * ux
        ny = y1 + (traveled + seg) * uy
        if drawing:
            draw.line([(x1 + traveled * ux, y1 + traveled * uy), (nx, ny)], fill=color, width=width)
        traveled += seg
        drawing = not drawing


def draw_centerline(draw: ImageDraw.ImageDraw, x1: float, y1: float, x2: float, y2: float,
                    color: tuple = COLOR_CENTERLINE, width: int = 1):
    """Draws an ASME standard centerline (long-dash, short-dash, long-dash)."""
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    if dist < 1e-4:
        return
    ux = dx / dist
    uy = dy / dist
    pattern = [(16.0, True), (5.0, False), (4.0, True), (5.0, False)]
    pat_idx = 0
    traveled = 0.0
    while traveled < dist:
        seg_len, is_line = pattern[pat_idx]
        actual_seg = min(seg_len, dist - traveled)
        if is_line:
            draw.line([
                (x1 + traveled * ux, y1 + traveled * uy),
                (x1 + (traveled + actual_seg) * ux, y1 + (traveled + actual_seg) * uy)
            ], fill=color, width=width)
        traveled += actual_seg
        pat_idx = (pat_idx + 1) % len(pattern)


def draw_dim_h(draw: ImageDraw.ImageDraw, x1: float, x2: float, y: float, text: str,
               ext_y1: float = None, ext_y2: float = None, font: ImageFont.ImageFont = FONT_BOLD,
               color: tuple = COLOR_DIM_LINE, text_color: tuple = COLOR_DIM_TEXT):
    """Draws a horizontal engineering dimension with extension lines, arrows, and masked text."""
    if x1 > x2:
        x1, x2 = x2, x1
    # Extension lines
    if ext_y1 is not None and ext_y2 is not None:
        draw.line([(x1, ext_y1), (x1, ext_y2)], fill=color, width=1)
        draw.line([(x2, ext_y1), (x2, ext_y2)], fill=color, width=1)
    # Dimension line
    draw.line([(x1, y), (x2, y)], fill=color, width=1)
    # Inward arrows
    draw_arrowhead(draw, x1, y, 0.0, size=7.0, color=color)
    draw_arrowhead(draw, x2, y, math.pi, size=7.0, color=color)
    # Text with mask pill
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    cx = (x1 + x2) / 2
    pad = 4
    mask_box = [cx - tw / 2 - pad, y - th / 2 - pad, cx + tw / 2 + pad, y + th / 2 + pad]
    draw.rectangle(mask_box, fill=COLOR_BG)
    draw.text((cx - tw / 2, y - th / 2 - 1), text, fill=text_color, font=font)


def draw_dim_v(draw: ImageDraw.ImageDraw, y1: float, y2: float, x: float, lines,
               ext_x1: float = None, ext_x2: float = None, font: ImageFont.ImageFont = FONT_BOLD,
               color: tuple = COLOR_DIM_LINE, text_color: tuple = COLOR_DIM_TEXT,
               text_offset_x: float = 0.0, text_offset_y: float = 0.0):
    """Draws a vertical engineering dimension with stacked text centered or offset."""
    if y1 > y2:
        y1, y2 = y2, y1
    # Extension lines
    if ext_x1 is not None and ext_x2 is not None:
        draw.line([(ext_x1, y1), (ext_x2, y1)], fill=color, width=1)
        draw.line([(ext_x1, y2), (ext_x2, y2)], fill=color, width=1)
    # Dimension line
    draw.line([(x, y1), (x, y2)], fill=color, width=1)
    # Inward arrows
    draw_arrowhead(draw, x, y1, math.pi / 2, size=7.0, color=color)
    draw_arrowhead(draw, x, y2, -math.pi / 2, size=7.0, color=color)

    if isinstance(lines, str):
        lines = [lines]

    line_bboxes = [draw.textbbox((0, 0), line, font=font) for line in lines]
    max_tw = max((b[2] - b[0]) for b in line_bboxes)
    line_height = max((b[3] - b[1]) for b in line_bboxes) + 2
    total_th = len(lines) * line_height

    cy = (y1 + y2) / 2 + text_offset_y
    cx = x + text_offset_x
    pad = 3
    mask_box = [cx - max_tw / 2 - pad, cy - total_th / 2 - pad, cx + max_tw / 2 + pad, cy + total_th / 2 + pad]
    draw.rectangle(mask_box, fill=COLOR_BG)

    start_y = cy - total_th / 2
    for i, line in enumerate(lines):
        b = line_bboxes[i]
        lw = b[2] - b[0]
        draw.text((cx - lw / 2, start_y + i * line_height), line, fill=text_color, font=font)


def draw_leader_callout(draw: ImageDraw.ImageDraw, tip_x: float, tip_y: float,
                        knee_x: float, knee_y: float, arm_x: float, lines,
                        font: ImageFont.ImageFont = FONT_BOLD, color: tuple = COLOR_DIM_LINE,
                        text_color: tuple = COLOR_DIM_TEXT):
    """Draws a leader callout line pointing to a feature with arrow, knee, horizontal shelf, and text."""
    if isinstance(lines, str):
        lines = [lines]
    angle = math.atan2(knee_y - tip_y, knee_x - tip_x)
    draw_arrowhead(draw, tip_x, tip_y, angle + math.pi, size=7.0, color=color)
    draw.line([(tip_x, tip_y), (knee_x, knee_y)], fill=color, width=1)
    draw.line([(knee_x, knee_y), (arm_x, knee_y)], fill=color, width=1)

    line_bboxes = [draw.textbbox((0, 0), l, font=font) for l in lines]
    lh = max((b[3] - b[1]) for b in line_bboxes) + 2
    total_h = len(lines) * lh

    if arm_x >= knee_x:
        tx = knee_x + 5
    else:
        tx = arm_x + 5

    ty = knee_y - total_h - 2
    for i, line in enumerate(lines):
        draw.text((tx, ty + i * lh), line, fill=text_color, font=font)


def draw_table(draw: ImageDraw.ImageDraw, x: int, y: int, widths: list, headers: list,
               rows: list, row_height: int = 22, header_height: int = 25,
               alignments: list = None, header_bg: tuple = COLOR_HEADER_BG,
               font_hdr: ImageFont.ImageFont = FONT_SUBHDR, font_row: ImageFont.ImageFont = FONT_REGULAR):
    """Draws a crisp bordered engineering table with alternating row highlights."""
    total_w = sum(widths)
    total_h = header_height + len(rows) * row_height
    if alignments is None:
        alignments = ['left'] * len(widths)

    # Outer border and header background
    draw.rectangle([x, y, x + total_w, y + header_height], fill=header_bg, outline=COLOR_PANEL_BORDER)

    # Header text
    col_x = x
    for i, (hdr, w) in enumerate(zip(headers, widths)):
        bbox = draw.textbbox((0, 0), hdr, font=font_hdr)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        ty = y + (header_height - th) / 2 - 1
        align = alignments[i]
        if align == 'center':
            tx = col_x + (w - tw) / 2
        elif align == 'right':
            tx = col_x + w - tw - 6
        else:
            tx = col_x + 6
        draw.text((tx, ty), hdr, fill=COLOR_TEXT_WHITE, font=font_hdr)
        if i > 0:
            draw.line([(col_x, y), (col_x, y + total_h)], fill=COLOR_PANEL_BORDER, width=1)
        col_x += w

    # Rows
    cur_y = y + header_height
    for r_idx, row in enumerate(rows):
        row_bg = COLOR_ROW_ALT if (r_idx % 2 == 1) else COLOR_PANEL_BG
        draw.rectangle([x, cur_y, x + total_w, cur_y + row_height], fill=row_bg, outline=COLOR_PANEL_BORDER)

        col_x = x
        for c_idx, (val, w) in enumerate(zip(row, widths)):
            val_str = str(val)
            text_color = COLOR_TEXT_WHITE
            if "VHF" in val_str or "680" in val_str:
                text_color = COLOR_TEXT_GOLD
            elif "UHF" in val_str or "400" in val_str:
                text_color = COLOR_TEXT_CYAN
            elif "dBi" in val_str:
                text_color = COLOR_TEXT_GREEN
            elif "PETG" in val_str or "STL" in val_str or ".stl" in val_str:
                text_color = COLOR_TEXT_CYAN
            elif "12 AWG" in val_str or "Copper" in val_str:
                text_color = COLOR_COPPER

            bbox = draw.textbbox((0, 0), val_str, font=font_row)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            ty = cur_y + (row_height - th) / 2 - 1
            align = alignments[c_idx]
            if align == 'center':
                tx = col_x + (w - tw) / 2
            elif align == 'right':
                tx = col_x + w - tw - 6
            else:
                tx = col_x + 6
            draw.text((tx, ty), val_str, fill=text_color, font=font_row)
            if c_idx > 0:
                draw.line([(col_x, cur_y), (col_x, cur_y + row_height)], fill=COLOR_PANEL_BORDER, width=1)
            col_x += w
        cur_y += row_height

    # Final perimeter
    draw.rectangle([x, y, x + total_w, y + total_h], outline=COLOR_PANEL_BORDER, width=1)
    return total_h


# -----------------------------------------------------------------------------
# MAIN GENERATOR FUNCTION
# -----------------------------------------------------------------------------
def generate_drawing(output_path: str = OUTPUT_PATH) -> bool:
    """Generates the master 2200 x 1500 px 2D technical drawing PNG."""
    print(f"[bt4v_drawing] Initializing canvas: {CANVAS_WIDTH} x {CANVAS_HEIGHT} px...")
    img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # 1. Background Grid (Engineering Blueprint Grid)
    for x in range(0, CANVAS_WIDTH, 25):
        c = COLOR_GRID_MAJOR if (x % 100 == 0) else COLOR_GRID_MINOR
        draw.line([(x, 0), (x, CANVAS_HEIGHT)], fill=c, width=1)
    for y in range(0, CANVAS_HEIGHT, 25):
        c = COLOR_GRID_MAJOR if (y % 100 == 0) else COLOR_GRID_MINOR
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=c, width=1)

    # 2. Master Canvas Borders
    draw.rectangle([30, 30, CANVAS_WIDTH - 30, CANVAS_HEIGHT - 30], outline=COLOR_FRAME_OUTER, width=3)
    draw.rectangle([36, 36, CANVAS_WIDTH - 36, CANVAS_HEIGHT - 36], outline=COLOR_FRAME_INNER, width=1)

    # 3. Master Title Banner
    banner_box = [38, 38, CANVAS_WIDTH - 38, 92]
    draw.rectangle(banner_box, fill=(7, 21, 44), outline=COLOR_PANEL_BORDER, width=1)

    title_text = "BT4-V 3D PRINTED INDOOR WINDOW TV ANTENNA — 2D TECHNICAL SPECIFICATION"
    sub_text = "4-BAY HYBRID BOWTIE + EXTENDED VHF-HI RESONATORS  |  MODULAR SPINE & COMMERCIAL BALUN INTEGRATION  |  REV v0.3.0"
    draw.text((50, 44), title_text, fill=COLOR_TEXT_WHITE, font=FONT_MAIN_TITLE)
    draw.text((52, 72), sub_text, fill=COLOR_TEXT_CYAN, font=FONT_MAIN_SUB)

    # Badges in title banner
    doc_badge = "DWG NO: DWG-BT4V-001 | SHEET 1 OF 1"
    draw.rectangle([CANVAS_WIDTH - 360, 48, CANVAS_WIDTH - 50, 82], fill=COLOR_HEADER_BG, outline=COLOR_FRAME_OUTER)
    draw.text((CANVAS_WIDTH - 345, 57), doc_badge, fill=COLOR_TEXT_WHITE, font=FONT_MONO_BOLD)

    # -------------------------------------------------------------------------
    # PANEL REGIONS
    # -------------------------------------------------------------------------
    # Col 1: Front Elevation View (X: 42 to 1180, Y: 100 to 1235)
    # Col 2: Side Profile View   (X: 1195 to 1475, Y: 100 to 1235)
    # Col 3: Tables & Title Block (X: 1490 to 2162, Y: 100 to 1462)
    # Bottom Strip: General Fabrication Notes (X: 42 to 1475, Y: 1245 to 1462)

    # Draw Panel Backgrounds & Borders
    draw.rectangle([42, 100, 1180, 1235], fill=COLOR_PANEL_BG, outline=COLOR_PANEL_BORDER, width=1)
    draw.rectangle([1195, 100, 1475, 1235], fill=COLOR_PANEL_BG, outline=COLOR_PANEL_BORDER, width=1)
    draw.rectangle([42, 1245, 1475, 1462], fill=COLOR_PANEL_BG, outline=COLOR_PANEL_BORDER, width=1)

    # Headers for views
    draw.rectangle([42, 100, 1180, 130], fill=COLOR_HEADER_BG, outline=COLOR_PANEL_BORDER)
    draw.text((54, 106), "VIEW A: FRONT ELEVATION & SCHEMATIC ASSEMBLY (SCALE 1:1.4)", fill=COLOR_TEXT_WHITE, font=FONT_PANEL_HDR)

    draw.rectangle([1195, 100, 1475, 130], fill=COLOR_HEADER_BG, outline=COLOR_PANEL_BORDER)
    draw.text((1205, 106), "VIEW B: SIDE PROFILE", fill=COLOR_TEXT_WHITE, font=FONT_PANEL_HDR)

    # -------------------------------------------------------------------------
    # FRONT ELEVATION GEOMETRY (View A)
    # -------------------------------------------------------------------------
    SCALE = 1.4
    X_CENTER = 608.0    # Front view spine centerline X
    Y_CENTER = 655.0    # Feed hub midpoint Y (Z = 0)

    # Centerlines
    draw_centerline(draw, X_CENTER, 145, X_CENTER, 1210, color=COLOR_CENTERLINE, width=1)

    y_feed_ctr = Y_CENTER
    y_bay2 = Y_CENTER - 65.0 * SCALE     # 564.0
    y_bay1 = Y_CENTER - 195.0 * SCALE    # 382.0
    y_bay3 = Y_CENTER + 65.0 * SCALE     # 746.0
    y_bay4 = Y_CENTER + 195.0 * SCALE    # 928.0

    y_bay1_top = y_bay1 - 20.0 * SCALE   # 354.0
    y_cap_top = y_bay1_top - 30.0 * SCALE # 312.0
    y_cap_eyelet = y_bay1_top - 23.0 * SCALE # 321.8

    # 1. Spine Segments (Between brackets and feed hub)
    sw = 10.0 * SCALE
    draw.rectangle([X_CENTER - sw, y_bay1 + 20 * SCALE, X_CENTER + sw, y_bay2 - 20 * SCALE],
                   fill=COLOR_PLASTIC_FILL, outline=COLOR_PLASTIC_OUTLINE, width=2)
    draw.rectangle([X_CENTER - sw, y_bay2 + 20 * SCALE, X_CENTER + sw, y_feed_ctr - 35 * SCALE],
                   fill=COLOR_PLASTIC_FILL, outline=COLOR_PLASTIC_OUTLINE, width=2)
    draw.rectangle([X_CENTER - sw, y_feed_ctr + 35 * SCALE, X_CENTER + sw, y_bay3 - 20 * SCALE],
                   fill=COLOR_PLASTIC_FILL, outline=COLOR_PLASTIC_OUTLINE, width=2)
    draw.rectangle([X_CENTER - sw, y_bay3 + 20 * SCALE, X_CENTER + sw, y_bay4 - 20 * SCALE],
                   fill=COLOR_PLASTIC_FILL, outline=COLOR_PLASTIC_OUTLINE, width=2)

    # 2. Whisker Bay Brackets (4 bays)
    bw = 25.0 * SCALE
    bh = 20.0 * SCALE
    for y_b in [y_bay1, y_bay2, y_bay3, y_bay4]:
        draw.rectangle([X_CENTER - bw, y_b - bh, X_CENTER + bw, y_b + bh],
                       fill=COLOR_PLASTIC_FILL, outline=COLOR_PLASTIC_OUTLINE, width=2)
        draw.line([(X_CENTER - 6 * SCALE, y_b - bh), (X_CENTER - 6 * SCALE, y_b - bh - 8)], fill=COLOR_PLASTIC_DETAIL, width=1)
        draw.line([(X_CENTER + 6 * SCALE, y_b - bh), (X_CENTER + 6 * SCALE, y_b - bh - 8)], fill=COLOR_PLASTIC_DETAIL, width=1)
        for sign in [-1, 1]:
            hx = X_CENTER + sign * 12.5 * SCALE
            draw.ellipse([hx - 4, y_b - 4, hx + 4, y_b + 4], fill=COLOR_HARDWARE, outline=COLOR_TEXT_WHITE)
            draw.line([(hx - 3, y_b), (hx + 3, y_b)], fill=(40, 50, 60), width=1)

    # 3. Center Feed Hub
    cfw = 20.0 * SCALE
    cfh = 35.0 * SCALE
    draw.rectangle([X_CENTER - cfw, y_feed_ctr - cfh, X_CENTER + cfw, y_feed_ctr + cfh],
                   fill=COLOR_PLASTIC_FILL, outline=COLOR_PLASTIC_OUTLINE, width=2)

    # Balun cradle cavity representation
    draw.rectangle([X_CENTER - 15 * SCALE, y_feed_ctr - 22 * SCALE, X_CENTER + 15 * SCALE, y_feed_ctr + 24 * SCALE],
                   fill=COLOR_BALUN_BODY, outline=COLOR_BALUN_ACCENT, width=1)
    draw.text((X_CENTER - 22, y_feed_ctr - 7), "RCA BALUN", fill=COLOR_BALUN_ACCENT, font=FONT_TINY)

    # M4 Feed Terminals (25 mm spacing -> X = ±12.5 mm -> ±17.5 px at y_feed_ctr)
    for sign in [-1, 1]:
        tx = X_CENTER + sign * 12.5 * SCALE
        draw.ellipse([tx - 5, y_feed_ctr - 5, tx + 5, y_feed_ctr + 5], fill=COLOR_COPPER, outline=COLOR_HARDWARE, width=1)
        draw.line([(tx, y_feed_ctr - 5), (tx, y_feed_ctr - 12)], fill=COLOR_HARDWARE, width=2)

    # Downward coax connector from Center Feed
    draw.rectangle([X_CENTER - 5 * SCALE, y_feed_ctr + cfh, X_CENTER + 5 * SCALE, y_feed_ctr + cfh + 12],
                   fill=COLOR_BALUN_ACCENT, outline=COLOR_TEXT_WHITE, width=1)
    draw.line([(X_CENTER, y_feed_ctr + cfh + 12), (X_CENTER, y_feed_ctr + cfh + 50)], fill=COLOR_COAX, width=6)
    draw.line([(X_CENTER, y_feed_ctr + cfh + 12), (X_CENTER, y_feed_ctr + cfh + 50)], fill=COLOR_COAX_HL, width=2)

    # 4. Top Hanging Cap
    cw = 22.0 * SCALE
    draw.polygon([
        (X_CENTER - sw, y_bay1_top),
        (X_CENTER - cw, y_bay1_top - 12 * SCALE),
        (X_CENTER - cw, y_cap_top),
        (X_CENTER + cw, y_cap_top),
        (X_CENTER + cw, y_bay1_top - 12 * SCALE),
        (X_CENTER + sw, y_bay1_top)
    ], fill=COLOR_PLASTIC_FILL, outline=COLOR_PLASTIC_OUTLINE)

    for sign in [-1, 1]:
        ey_x = X_CENTER + sign * 15.0 * SCALE
        draw.ellipse([ey_x - 5, y_cap_eyelet - 5, ey_x + 5, y_cap_eyelet + 5],
                     fill=COLOR_BG, outline=COLOR_EYELET_RING, width=2)
        draw.line([(ey_x, y_cap_eyelet - 5), (ey_x, 155)], fill=COLOR_EYELET_RING, width=1)

    # 5. Phase Crossover Spacers (2 places: Bay 1–2 and Bay 3–4)
    y_xo1 = (y_bay1 + y_bay2) / 2.0  # 473.0
    y_xo2 = (y_bay3 + y_bay4) / 2.0  # 837.0
    xow = 17.5 * SCALE
    xoh = 15.0 * SCALE
    for y_xo in [y_xo1, y_xo2]:
        draw.rectangle([X_CENTER - xow, y_xo - xoh, X_CENTER + xow, y_xo + xoh],
                       fill=(28, 70, 130), outline=(110, 185, 255), width=2)
        draw.line([(X_CENTER - 12.5 * SCALE, y_xo - xoh), (X_CENTER + 12.5 * SCALE, y_xo + xoh)], fill=COLOR_PLASTIC_DETAIL, width=1)
        draw.line([(X_CENTER + 12.5 * SCALE, y_xo - xoh), (X_CENTER - 12.5 * SCALE, y_xo + xoh)], fill=COLOR_PLASTIC_DETAIL, width=1)

    # 6. Continuous 12 AWG Phase Lines with 180° Transpositions
    pl_x1 = X_CENTER - 12.5 * SCALE  # Left bus (590.5)
    pl_x2 = X_CENTER + 12.5 * SCALE  # Right bus (625.5)

    # Bay 1 to Crossover 1 top
    draw.line([(pl_x1, y_bay1), (pl_x1, y_xo1 - xoh)], fill=COLOR_COPPER, width=3)
    draw.line([(pl_x2, y_bay1), (pl_x2, y_xo1 - xoh)], fill=COLOR_COPPER, width=3)

    # Crossover 1 (Transposition: 180° phase flip)
    draw.line([(pl_x1, y_xo1 - xoh), (pl_x2, y_xo1 + xoh)], fill=COLOR_COPPER, width=3)
    draw_dashed_line(draw, pl_x2, y_xo1 - xoh, pl_x1, y_xo1 + xoh, color=COLOR_COPPER_REAR, dash=4, gap=3, width=3)

    # Crossover 1 bottom to Crossover 2 top (passing Bay 2, Center Feed, Bay 3)
    draw.line([(pl_x1, y_xo1 + xoh), (pl_x1, y_xo2 - xoh)], fill=COLOR_COPPER, width=3)
    draw.line([(pl_x2, y_xo1 + xoh), (pl_x2, y_xo2 - xoh)], fill=COLOR_COPPER, width=3)

    # Crossover 2 (Transposition: 180° phase flip)
    draw.line([(pl_x1, y_xo2 - xoh), (pl_x2, y_xo2 + xoh)], fill=COLOR_COPPER, width=3)
    draw_dashed_line(draw, pl_x2, y_xo2 - xoh, pl_x1, y_xo2 + xoh, color=COLOR_COPPER_REAR, dash=4, gap=3, width=3)

    # Crossover 2 bottom to Bay 4
    draw.line([(pl_x1, y_xo2 + xoh), (pl_x1, y_bay4)], fill=COLOR_COPPER, width=3)
    draw.line([(pl_x2, y_xo2 + xoh), (pl_x2, y_bay4)], fill=COLOR_COPPER, width=3)

    # 7. Bowtie Whiskers & Triangular Tine Spreaders
    vhf_dx = 340.0 * math.cos(math.radians(12.75)) * SCALE
    vhf_dy = 340.0 * math.sin(math.radians(12.75)) * SCALE

    uhf_dx = 200.0 * math.cos(math.radians(16.25)) * SCALE
    uhf_dy = 200.0 * math.sin(math.radians(16.25)) * SCALE

    spreader_dx = 150.0 * math.cos(math.radians(12.75)) * SCALE
    spreader_dy = 150.0 * math.sin(math.radians(12.75)) * SCALE

    def draw_bowtie(y_apex: float, dx: float, dy: float, is_vhf: bool):
        draw.line([(pl_x1, y_apex), (pl_x1 - dx, y_apex - dy)], fill=COLOR_COPPER, width=3)
        draw.line([(pl_x1, y_apex), (pl_x1 - dx, y_apex + dy)], fill=COLOR_COPPER, width=3)
        draw.ellipse([pl_x1 - 3, y_apex - 3, pl_x1 + 3, y_apex + 3], fill=COLOR_COPPER)

        draw.line([(pl_x2, y_apex), (pl_x2 + dx, y_apex - dy)], fill=COLOR_COPPER, width=3)
        draw.line([(pl_x2, y_apex), (pl_x2 + dx, y_apex + dy)], fill=COLOR_COPPER, width=3)
        draw.ellipse([pl_x2 - 3, y_apex - 3, pl_x2 + 3, y_apex + 3], fill=COLOR_COPPER)

        # Continuous backing struts (BT4V_Bowtie_Backing.stl): 2 per bay running continuously along upper and lower arms
        for sign in [-1, 1]:
            root_x = X_CENTER + sign * (bw - 2 * SCALE)
            tip_x = (pl_x1 if sign == -1 else pl_x2) + sign * (dx * 0.96)
            tip_y_up = y_apex - dy * 0.96
            tip_y_dn = y_apex + dy * 0.96
            # Upper arm backing strut
            draw.line([(root_x, y_apex - 2 * SCALE), (tip_x, tip_y_up - 2 * SCALE)], fill=COLOR_PLASTIC_FILL, width=5)
            draw.line([(root_x, y_apex - 2 * SCALE), (tip_x, tip_y_up - 2 * SCALE)], fill=COLOR_PLASTIC_OUTLINE, width=1)
            # Lower arm backing strut
            draw.line([(root_x, y_apex + 2 * SCALE), (tip_x, tip_y_dn + 2 * SCALE)], fill=COLOR_PLASTIC_FILL, width=5)
            draw.line([(root_x, y_apex + 2 * SCALE), (tip_x, tip_y_dn + 2 * SCALE)], fill=COLOR_PLASTIC_OUTLINE, width=1)

        if is_vhf:
            for sign in [-1, 1]:
                apex_x = pl_x1 if sign == -1 else pl_x2
                sx = apex_x + sign * spreader_dx
                sy_top = y_apex - spreader_dy
                sy_bot = y_apex + spreader_dy
                draw.rectangle([sx - 4, sy_top, sx + 4, sy_bot], fill=COLOR_PLASTIC_FILL, outline=COLOR_PLASTIC_OUTLINE, width=1)
                draw.rectangle([sx - 6, sy_top - 3, sx + 6, sy_top + 3], fill=COLOR_PLASTIC_OUTLINE)
                draw.rectangle([sx - 6, sy_bot - 3, sx + 6, sy_bot + 3], fill=COLOR_PLASTIC_OUTLINE)
                draw.line([(sx - 4, sy_top), (sx + 4, sy_bot)], fill=COLOR_PLASTIC_DETAIL, width=1)
                draw.line([(sx + 4, sy_top), (sx - 4, sy_bot)], fill=COLOR_PLASTIC_DETAIL, width=1)

    draw_bowtie(y_bay1, vhf_dx, vhf_dy, is_vhf=True)   # Bay 1 (VHF-High)
    draw_bowtie(y_bay2, uhf_dx, uhf_dy, is_vhf=False)  # Bay 2 (UHF)
    draw_bowtie(y_bay3, uhf_dx, uhf_dy, is_vhf=False)  # Bay 3 (UHF)
    draw_bowtie(y_bay4, vhf_dx, vhf_dy, is_vhf=True)   # Bay 4 (VHF-High)

    # -------------------------------------------------------------------------
    # FRONT VIEW DIMENSIONS & CALLOUTS (Harmonious Layout, Zero Overlaps)
    # -------------------------------------------------------------------------
    vhf_left_x = pl_x1 - vhf_dx   # ~126 px
    vhf_right_x = pl_x2 + vhf_dx  # ~1090 px
    uhf_left_x = pl_x1 - uhf_dx   # ~322 px
    uhf_right_x = pl_x2 + uhf_dx  # ~894 px

    # 1. Bay 1 VHF Span Dimension (Horizontal, top)
    draw_dim_h(draw, vhf_left_x, vhf_right_x, 185.0,
               "680.0 mm (VHF-HI TIP-TO-TIP SPAN)",
               ext_y1=y_bay1 - vhf_dy - 5, ext_y2=178.0)

    # 2. Bay 2 UHF Span Dimension (Horizontal, below Bay 2)
    draw_dim_h(draw, uhf_left_x, uhf_right_x, y_feed_ctr - 55.0,
               "400.0 mm (UHF SPAN)",
               ext_y1=y_bay2 + uhf_dy + 4, ext_y2=y_feed_ctr - 48.0)

    # 3. Hanging Cap Eyelet Pitch (Horizontal)
    draw_dim_h(draw, X_CENTER - 15.0 * SCALE, X_CENTER + 15.0 * SCALE, y_cap_top - 18.0,
               "30.0 mm",
               ext_y1=y_cap_eyelet - 5, ext_y2=y_cap_top - 22.0)

    # 4. Phase Line Spacing (Horizontal, at Bay 3/Feed)
    draw_dim_h(draw, pl_x1, pl_x2, y_feed_ctr + 55.0,
               "25.0 mm",
               ext_y1=y_feed_ctr + 25.0, ext_y2=y_feed_ctr + 62.0)

    # 5. VHF Tip-to-Tip Tine Spread (Vertical, left of Bay 1 tip)
    draw_dim_v(draw, y_bay1 - vhf_dy, y_bay1 + vhf_dy, 104.0,
               ["150 mm", "TINE", "SPREAD"],
               ext_x1=vhf_left_x - 5, ext_x2=97.0, font=FONT_SMALL_BOLD, text_offset_x=0.0)

    # 6. UHF Tip-to-Tip Tine Spread (Vertical, left of Bay 2 tip)
    draw_dim_v(draw, y_bay2 - uhf_dy, y_bay2 + uhf_dy, 290.0,
               ["115 mm", "SPREAD"],
               ext_x1=uhf_left_x - 5, ext_x2=283.0, font=FONT_SMALL_BOLD, text_offset_x=0.0)

    # 7. Active Bay Pitch Dimensions (Vertical, right side at X = 1098)
    dim_pitch_x = 1098.0
    draw_dim_v(draw, y_bay1, y_bay2, dim_pitch_x,
               ["130 mm", "PITCH"],
               ext_x1=X_CENTER + bw + 4, ext_x2=dim_pitch_x + 6, font=FONT_SMALL_BOLD, text_offset_x=0.0)
    # Stagger middle pitch dimension vertically so it does not align horizontally with the 390 mm total active span
    draw_dim_v(draw, y_bay2, y_bay3, dim_pitch_x,
               ["130 mm", "PITCH"],
               ext_x1=X_CENTER + bw + 4, ext_x2=dim_pitch_x + 6, font=FONT_SMALL_BOLD, text_offset_x=0.0, text_offset_y=-35.0)
    draw_dim_v(draw, y_bay3, y_bay4, dim_pitch_x,
               ["130 mm", "PITCH"],
               ext_x1=X_CENTER + bw + 4, ext_x2=dim_pitch_x + 6, font=FONT_SMALL_BOLD, text_offset_x=0.0)

    # 8. Total Active Bay Span (Vertical, further right at X = 1158)
    dim_total_span_x = 1158.0
    draw_dim_v(draw, y_bay1, y_bay4, dim_total_span_x,
               ["390 mm", "ACTIVE", "BAY SPAN"],
               ext_x1=dim_pitch_x + 8, ext_x2=dim_total_span_x + 6, font=FONT_SMALL_BOLD, text_offset_x=0.0)

    # 9. Overall Antenna Height Envelope (Far left at X = 74)
    draw_dim_v(draw, y_cap_top, y_bay4 + vhf_dy, 74.0,
               ["~560 mm", "OVERALL", "HEIGHT"],
               ext_x1=94.0, ext_x2=66.0, font=FONT_SMALL_BOLD, text_offset_x=0.0)

    # 10. Leader Callouts for features (Symmetrically distributed, perfectly isolated)
    # Bay 1 VHF Bowtie (pointing to upper left arm)
    draw_leader_callout(draw, vhf_left_x + 100, y_bay1 - vhf_dy * 0.7,
                        vhf_left_x + 140, y_bay1 - vhf_dy - 25, vhf_left_x + 360,
                        ["BAY 1: VHF-HI BOWTIE (680 mm SPAN)", "340 mm ARM | 25.5° FLARE"])

    # Bay 1 Triangular Tine Spreader (pointing to upper right spreader)
    spreader_r_x = pl_x2 + spreader_dx
    spreader_r_y = y_bay1 - spreader_dy
    draw_leader_callout(draw, spreader_r_x, spreader_r_y,
                        spreader_r_x + 35, spreader_r_y - 25, spreader_r_x + 230,
                        ["TRIANGULAR TINE SPREADER", "R = 150 mm (DROOP MITIGATION)"])

    # Full-Length Backing Strut (pointing to upper left backing strut on Bay 1)
    sup_call_x = pl_x1 - vhf_dx * 0.5
    sup_call_y = y_bay1 - vhf_dy * 0.5
    draw_leader_callout(draw, sup_call_x, sup_call_y,
                        sup_call_x - 35, sup_call_y - 30, sup_call_x - 225,
                        ["FULL-LENGTH BACKING STRUT", "BT4V_Bowtie_Backing.stl (210×12×8 mm)", "QTY: 8 (2 PER BAY) | VOL: 2,400 mm³"])

    # Phase Crossover 1 (pointing to Crossover 1 from the left)
    draw_leader_callout(draw, X_CENTER - xow, y_xo1,
                        X_CENTER - xow - 35, y_xo1 - 15, X_CENTER - xow - 215,
                        ["180° PHASE CROSSOVER", ">=5.0 mm DIELECTRIC ISOLATION"])

    # Bay 2 UHF Bowtie (pointing to right arm)
    draw_leader_callout(draw, uhf_right_x - 50, y_bay2 - uhf_dy * 0.5,
                        uhf_right_x + 30, y_bay2 - 40, uhf_right_x + 185,
                        ["BAY 2: UHF BOWTIE (400 mm SPAN)", "200 mm ARM | 32.5° FLARE"])

    # Center Feed Hub (pointing to Hub from the right side)
    draw_leader_callout(draw, X_CENTER + cfw, y_feed_ctr,
                        X_CENTER + cfw + 40, y_feed_ctr, X_CENTER + cfw + 235,
                        ["CENTER FEED HUB (300Ω BALANCED)", "RCA VH101R BALUN / 25 mm STUDS"])

    # Bay 3 UHF Bowtie (pointing to right arm)
    draw_leader_callout(draw, uhf_right_x - 50, y_bay3 + uhf_dy * 0.5,
                        uhf_right_x + 30, y_bay3 + 40, uhf_right_x + 185,
                        ["BAY 3: UHF BOWTIE (400 mm SPAN)", "200 mm ARM | 32.5° FLARE"])

    # Phase Crossover 2 (pointing to Crossover 2 from the left)
    draw_leader_callout(draw, X_CENTER - xow, y_xo2,
                        X_CENTER - xow - 35, y_xo2 + 15, X_CENTER - xow - 215,
                        ["180° PHASE CROSSOVER", "TRANSPOSED 12 AWG PHASE BUS"])

    # Bay 4 VHF Bowtie (pointing to lower left arm)
    draw_leader_callout(draw, vhf_left_x + 100, y_bay4 + vhf_dy * 0.7,
                        vhf_left_x + 140, y_bay4 + vhf_dy + 30, vhf_left_x + 360,
                        ["BAY 4: VHF-HI BOWTIE (680 mm SPAN)", "340 mm ARM | 25.5° FLARE"])

    # Bay 4 Triangular Tine Spreader (pointing to lower right spreader)
    spreader_r4_x = pl_x2 + spreader_dx
    spreader_r4_y = y_bay4 + spreader_dy
    draw_leader_callout(draw, spreader_r4_x, spreader_r4_y,
                        spreader_r4_x + 35, spreader_r4_y + 25, spreader_r4_x + 230,
                        ["TRIANGULAR TINE SPREADER", "R = 150 mm (DROOP MITIGATION)"])

    # Flare angle indicators (arcs)
    draw.arc([pl_x2 + 20, y_bay1 - 25, pl_x2 + 70, y_bay1 + 25], start=-15, end=15, fill=COLOR_DIM_LINE, width=1)
    draw.text((pl_x2 + 75, y_bay1 - 6), "25.5°", fill=COLOR_TEXT_CYAN, font=FONT_SMALL_BOLD)

    draw.arc([pl_x2 + 20, y_bay2 - 25, pl_x2 + 70, y_bay2 + 25], start=-20, end=20, fill=COLOR_DIM_LINE, width=1)
    draw.text((pl_x2 + 75, y_bay2 - 6), "32.5°", fill=COLOR_TEXT_CYAN, font=FONT_SMALL_BOLD)

    # -------------------------------------------------------------------------
    # SIDE PROFILE VIEW (View B)
    # -------------------------------------------------------------------------
    X_SIDE_CTR = 1335.0  # Spine side profile centerline X

    # Orthographic Projection Lines (contained, non-overlapping)
    proj_ys = [y_cap_top, y_bay1, y_xo1, y_bay2, y_feed_ctr, y_bay3, y_xo2, y_bay4, y_bay4 + vhf_dy]
    for py in proj_ys:
        draw_dashed_line(draw, 1170, py, 1178, py, color=COLOR_PROJECTION, dash=2, gap=2, width=1)
        draw_dashed_line(draw, 1198, py, 1260, py, color=COLOR_PROJECTION, dash=3, gap=3, width=1)

    draw_centerline(draw, X_SIDE_CTR, 145, X_SIDE_CTR, 1210, color=COLOR_CENTERLINE, width=1)

    x_front_face = X_SIDE_CTR + 7.0 * SCALE   # Front face where phase lines & whiskers sit
    x_rear_spine = X_SIDE_CTR - 7.0 * SCALE   # Rear face of 14 mm spine strut

    # 1. Continuous Modular Spine Profile (14 mm depth)
    draw.rectangle([x_rear_spine, y_bay1_top, x_front_face, y_bay4 + 20 * SCALE],
                   fill=COLOR_PLASTIC_FILL, outline=COLOR_PLASTIC_DETAIL, width=1)

    # 2. Bay Brackets Side Profile (18 mm depth)
    x_rear_bracket = x_front_face - 18.0 * SCALE
    for y_b in [y_bay1, y_bay2, y_bay3, y_bay4]:
        draw.rectangle([x_rear_bracket, y_b - bh, x_front_face, y_b + bh],
                       fill=COLOR_PLASTIC_FILL, outline=COLOR_PLASTIC_OUTLINE, width=2)
        draw.rectangle([x_front_face, y_b - 3, x_front_face + 5, y_b + 3], fill=COLOR_HARDWARE)
        draw.line([(x_rear_bracket, y_b), (x_front_face, y_b)], fill=COLOR_HARDWARE, width=2)
        draw.rectangle([x_rear_bracket - 4, y_b - 4, x_rear_bracket, y_b + 4], fill=COLOR_HARDWARE)
        draw.ellipse([x_front_face + 3, y_b - 3, x_front_face + 9, y_b + 3], fill=COLOR_COPPER)

    # 3. Center Feed Hub Side Profile (24 mm depth)
    x_rear_feed = x_front_face - 24.0 * SCALE
    draw.rectangle([x_rear_feed, y_feed_ctr - cfh, x_front_face, y_feed_ctr + cfh],
                   fill=COLOR_PLASTIC_FILL, outline=COLOR_PLASTIC_OUTLINE, width=2)

    # Balun cradle cavity & RCA VH101R transformer body mounted on rear
    x_balun_rear = x_rear_feed - 14.0 * SCALE
    draw.rectangle([x_balun_rear, y_feed_ctr - 22 * SCALE, x_rear_feed, y_feed_ctr + 24 * SCALE],
                   fill=COLOR_BALUN_BODY, outline=COLOR_BALUN_ACCENT, width=2)
    draw.text((x_balun_rear + 4, y_feed_ctr - 7), "VH101R", fill=COLOR_BALUN_ACCENT, font=FONT_TINY)

    # Downward 75-ohm F-connector and RG6 coaxial downlead
    f_conn_x = (x_balun_rear + x_rear_feed) / 2
    draw.rectangle([f_conn_x - 4, y_feed_ctr + 24 * SCALE, f_conn_x + 4, y_feed_ctr + 24 * SCALE + 14],
                   fill=COLOR_BALUN_ACCENT, outline=COLOR_TEXT_WHITE)
    coax_pts = [
        (f_conn_x, y_feed_ctr + 24 * SCALE + 14),
        (f_conn_x, y_feed_ctr + 24 * SCALE + 60),
        (f_conn_x - 8, y_feed_ctr + 24 * SCALE + 120),
        (f_conn_x - 10, y_bay4 + 100)
    ]
    for i in range(len(coax_pts) - 1):
        draw.line([coax_pts[i], coax_pts[i+1]], fill=COLOR_COAX, width=6)
        draw.line([coax_pts[i], coax_pts[i+1]], fill=COLOR_COAX_HL, width=2)
    draw.rectangle([f_conn_x - 6, y_feed_ctr + 24 * SCALE + 40, f_conn_x + 6, y_feed_ctr + 24 * SCALE + 44], fill=COLOR_TEXT_GOLD)

    # 4. Top Hanging Cap Side Profile
    draw.polygon([
        (x_rear_bracket, y_bay1_top),
        (x_rear_bracket, y_cap_top),
        (x_front_face, y_cap_top),
        (x_front_face, y_bay1_top)
    ], fill=COLOR_PLASTIC_FILL, outline=COLOR_PLASTIC_OUTLINE)
    draw.ellipse([X_SIDE_CTR - 4, y_cap_eyelet - 4, X_SIDE_CTR + 4, y_cap_eyelet + 4],
                 fill=COLOR_BG, outline=COLOR_EYELET_RING, width=2)
    draw.line([(X_SIDE_CTR, y_cap_eyelet - 4), (X_SIDE_CTR, 155)], fill=COLOR_EYELET_RING, width=1)

    # 5. Side View Dimensions & Callouts (Self-contained in View B)
    draw_dim_h(draw, x_rear_feed, x_front_face, y_feed_ctr - cfh - 15,
               "24 mm FEED", ext_y1=y_feed_ctr - cfh - 2, ext_y2=y_feed_ctr - cfh - 20, font=FONT_SMALL_BOLD)

    draw_dim_h(draw, x_rear_bracket, x_front_face, y_bay2 - bh - 15,
               "18 mm BRKT", ext_y1=y_bay2 - bh - 2, ext_y2=y_bay2 - bh - 20, font=FONT_SMALL_BOLD)

    draw_dim_h(draw, x_rear_spine, x_front_face, y_xo1 - xoh - 10,
               "14 mm STRUT", ext_y1=y_xo1 - xoh - 2, ext_y2=y_xo1 - xoh - 15, font=FONT_SMALL_BOLD)

    # Balun callout (contained within View B left margin)
    draw_leader_callout(draw, x_balun_rear, y_feed_ctr - 5,
                        x_balun_rear - 15, y_feed_ctr - 25, x_balun_rear - 68,
                        ["RCA VH101R", "BALUN"], font=FONT_SMALL_BOLD)

    # Coax downlead callout (pointing to right side of View B)
    draw_leader_callout(draw, f_conn_x, y_feed_ctr + 24 * SCALE + 50,
                        f_conn_x + 30, y_feed_ctr + 24 * SCALE + 65, f_conn_x + 115,
                        ["75Ω RG6 COAX", "STRAIN RELIEF"], font=FONT_SMALL_BOLD)

    # -------------------------------------------------------------------------
    # RIGHT COLUMN: TABLES & TITLE BLOCK (Col 3, X: 1490 to 2162)
    # -------------------------------------------------------------------------
    # 1. CHANNEL MAPPING & RF PERFORMANCE TABLE (Y: 100 to 570)
    p1_box = [1490, 100, 2162, 575]
    draw.rectangle(p1_box, fill=COLOR_PANEL_BG, outline=COLOR_PANEL_BORDER, width=1)
    draw.rectangle([1490, 100, 2162, 130], fill=COLOR_HEADER_BG, outline=COLOR_PANEL_BORDER)
    draw.text((1502, 106), "1. CHANNEL MAPPING & TARGET RF PERFORMANCE", fill=COLOR_TEXT_WHITE, font=FONT_PANEL_HDR)

    tbl1_headers = ["Band / Service", "RF Ch Range", "Frequency Range", "Resonator Bay Element", "Nom Gain", "VSWR", "Polarisation"]
    tbl1_widths = [110, 84, 110, 166, 68, 60, 68]
    tbl1_rows = [
        ["VHF-High TV", "Ch 7–13", "174–216 MHz", "Bay 1 & 4 (680 mm VHF)", "~3-4 dBi", "<2.0:1", "Horizontal"],
        ["UHF TV (Low)", "Ch 14–26", "470–542 MHz", "Bay 2 & 3 (400 mm UHF)", "~6-8 dBi", "<2.0:1", "Horizontal"],
        ["UHF TV (High)", "Ch 27–36", "542–608 MHz", "Bay 2 & 3 (400 mm UHF)", "~6-8 dBi", "<2.0:1", "Horizontal"],
        ["Balanced Feed", "300 Ω Bus", "174–608 MHz", "Center Feed & Crossovers", "—", "<1.5:1", "Balanced"],
        ["Coaxial Out", "75 Ω Unbal.", "174–608 MHz", "RCA VH101R Balun / RG6", "—", "<2.0:1", "Unbalanced"]
    ]
    tbl1_align = ['left', 'center', 'center', 'left', 'center', 'center', 'center']
    tbl1_h = draw_table(draw, 1494, 135, tbl1_widths, tbl1_headers, tbl1_rows,
                        row_height=23, header_height=26, alignments=tbl1_align,
                        font_hdr=FONT_SUBHDR, font_row=FONT_REGULAR)

    # RF Performance Parameters Sub-Box
    rf_sub_y = 135 + tbl1_h + 10
    draw.rectangle([1494, rf_sub_y, 2158, 565], fill=(10, 26, 52), outline=COLOR_PANEL_BORDER)
    draw.rectangle([1494, rf_sub_y, 2158, rf_sub_y + 22], fill=COLOR_HEADER_BG, outline=COLOR_PANEL_BORDER)
    draw.text((1502, rf_sub_y + 3), "ELECTRICAL & RF SYSTEM PERFORMANCE SPECIFICATIONS", fill=COLOR_TEXT_CYAN, font=FONT_SUBHDR)

    rf_specs = [
        ("Broadband Frequency Coverage:", "VHF-High (Ch 7–13, 174–216 MHz) & UHF (Ch 14–36, 470–608 MHz)"),
        ("Forward Broadside Gain:", "VHF-High: ~5.5 dBi | UHF: ~8.5 dBi (Equal front & back reception)"),
        ("Nominal Feedpoint Impedance:", "300 Ω Balanced transformed to 75 Ω Unbalanced via RCA VH101R"),
        ("Voltage Standing Wave Ratio:", "VSWR < 2.0:1 across entire VHF-Hi and UHF operating passband"),
        ("Polarisation & Pattern:", "Pure Horizontal (0° X-Pol Loss) | Symmetrical 8-figure bidirectional"),
        ("Array Feed Topology:", "Midpoint Balanced Feed between Bays 2 & 3; 180° crossover transposition"),
        ("Active Structural Envelope:", "390 mm Active Bay Span, ~560 mm Overall Height (Window envelope <=600 mm)")
    ]
    spec_cur_y = rf_sub_y + 28
    for label, val in rf_specs:
        draw.text((1504, spec_cur_y), label, fill=COLOR_TEXT_WHITE, font=FONT_SMALL_BOLD)
        draw.text((1710, spec_cur_y), val, fill=COLOR_TEXT_CYAN, font=FONT_SMALL)
        spec_cur_y += 18

    # 2. ASSEMBLY, WIRE-BENDING & HARDWARE SPECIFICATIONS (Y: 585 to 1095)
    p2_box = [1490, 585, 2162, 1095]
    draw.rectangle(p2_box, fill=COLOR_PANEL_BG, outline=COLOR_PANEL_BORDER, width=1)
    draw.rectangle([1490, 585, 2162, 615], fill=COLOR_HEADER_BG, outline=COLOR_PANEL_BORDER)
    draw.text((1502, 591), "2. ASSEMBLY, WIRE-BENDING & BILL OF MATERIALS (BOM)", fill=COLOR_TEXT_WHITE, font=FONT_PANEL_HDR)

    # Table 2A: Wire Bending Schedule
    draw.text((1502, 622), "A. 12 AWG SOLID COPPER WIRE CUTTING & FORMING SCHEDULE", fill=COLOR_TEXT_GOLD, font=FONT_SUBHDR)
    tbl2a_headers = ["Conductor Element", "Qty", "Cut Length", "Arm Length", "Flare Angle", "Finished Span"]
    tbl2a_widths = [190, 40, 94, 150, 90, 100]
    tbl2a_rows = [
        ["VHF-High Whiskers", "4", "690 mm", "340 mm + 10 mm apex", "25.5°", "680 mm (150 mm Tine)"],
        ["UHF Whiskers", "4", "410 mm", "200 mm + 10 mm apex", "32.5°", "400 mm (115 mm Tine)"],
        ["Spine Phase Lines", "2", "580 mm", "Continuous vertical bus", "—", "25.0 mm C-to-C"]
    ]
    tbl2a_align = ['left', 'center', 'right', 'left', 'center', 'center']
    tbl2a_h = draw_table(draw, 1494, 642, tbl2a_widths, tbl2a_headers, tbl2a_rows,
                         row_height=22, header_height=24, alignments=tbl2a_align,
                         font_hdr=FONT_SUBHDR, font_row=FONT_REGULAR)

    # Table 2B: Fasteners & Balun Hardware
    draw.text((1502, 642 + tbl2a_h + 8), "B. FASTENERS, JOINING HARDWARE & BALUN COMPONENT", fill=COLOR_TEXT_GOLD, font=FONT_SUBHDR)
    tbl2b_headers = ["Hardware Item", "Qty", "Specification", "Application & Mounting Location"]
    tbl2b_widths = [160, 40, 194, 270]
    tbl2b_rows = [
        ["Machine Screws", "10", "M4 x 16 mm Stainless Pan Head", "Whisker apex clamps (8) & Balun feed studs (2)"],
        ["Captive Hex Nuts", "10", "M4 Stainless Steel (7.2 mm AF)", "Retained in rear captive pockets of brackets & hub"],
        ["Joint Cross-Pins", "10", "Ø2.5 mm x 18 mm / M2.5 screws", "Secures tenon/mortise modular spine interlocks"],
        ["Commercial Balun", "1", "RCA VH101R 300:75Ω Outdoor", "Snaps into center cradle; spade lugs to M4 studs"]
    ]
    tbl2b_align = ['left', 'center', 'left', 'left']
    tbl2b_h = draw_table(draw, 1494, 642 + tbl2a_h + 28, tbl2b_widths, tbl2b_headers, tbl2b_rows,
                         row_height=21, header_height=23, alignments=tbl2b_align,
                         font_hdr=FONT_SUBHDR, font_row=FONT_REGULAR)

    # Table 2C: 3D Printed Structural BOM
    draw.text((1502, 642 + tbl2a_h + 28 + tbl2b_h + 8), "C. 3D PRINTED STRUCTURAL COMPONENTS (PETG / PLA)", fill=COLOR_TEXT_GOLD, font=FONT_SUBHDR)
    tbl2c_headers = ["Component Name", "STL Deliverable File", "Qty", "Bounding Extents", "Volume"]
    tbl2c_widths = [174, 180, 40, 170, 100]
    tbl2c_rows = [
        ["Center Feed Hub", "BT4V_Center_Feed.stl", "1", "40.0 x 24.0 x 70.0 mm", "28,500 mm³"],
        ["Whisker Bay Bracket", "BT4V_Bay_Bracket.stl", "4", "50.0 x 18.0 x 40.0 mm", "19,200 mm³"],
        ["Modular Spine Segment", "BT4V_Spine_Segment.stl", "4", "20.0 x 14.0 x 120.0 mm", "16,800 mm³"],
        ["Phase Crossover Spacer", "BT4V_Phase_Crossover.stl", "2", "35.0 x 12.0 x 30.0 mm", "6,100 mm³"],
        ["Full-Length Backing Strut", "BT4V_Bowtie_Backing.stl", "8", "210.0 x 12.0 x 8.0 mm", "2,400 mm³"],
        ["Top Hanging Cap", "BT4V_Hanging_Cap.stl", "1", "44.0 x 18.0 x 30.0 mm", "7,400 mm³"],
        ["Fit Calibration Coupon", "BT4V_Fit_Coupon.stl", "1", "90.0 x 50.0 x 10.0 mm", "26,500 mm³"]
    ]
    tbl2c_align = ['left', 'left', 'center', 'center', 'right']
    draw_table(draw, 1494, 642 + tbl2a_h + 28 + tbl2b_h + 28, tbl2c_widths, tbl2c_headers, tbl2c_rows,
               row_height=20, header_height=22, alignments=tbl2c_align,
               font_hdr=FONT_SUBHDR, font_row=FONT_REGULAR)

    # 3. FORMAL ENGINEERING TITLE BLOCK (Y: 1105 to 1462)
    p3_box = [1490, 1105, 2162, 1462]
    draw.rectangle(p3_box, fill=(8, 22, 45), outline=COLOR_FRAME_OUTER, width=2)

    # Top cell: Main Title
    draw.rectangle([1490, 1105, 2162, 1165], fill=(14, 38, 76), outline=COLOR_PANEL_BORDER, width=1)
    draw.text((1504, 1113), "BT4-V 3D PRINTED ANTENNA — 4-BAY BOWTIE + VHF", fill=COLOR_TEXT_WHITE, font=FONT_PANEL_HDR)
    draw.text((1504, 1138), "SYSTEM SPECIFICATION & GENERAL ASSEMBLY TECHNICAL DRAWING", fill=COLOR_TEXT_CYAN, font=FONT_REGULAR)

    # Grid partitions for Title Block
    draw.line([(1700, 1165), (1700, 1410)], fill=COLOR_PANEL_BORDER, width=1)
    draw.line([(1910, 1165), (1910, 1410)], fill=COLOR_PANEL_BORDER, width=1)

    # Col A:
    draw.text((1502, 1175), "DRAWING NUMBER:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1502, 1190), "DWG-BT4V-001", fill=COLOR_TEXT_WHITE, font=FONT_BOLD)

    draw.text((1502, 1215), "REVISION:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1502, 1230), "v0.3.0 (INITIAL RELEASE)", fill=COLOR_TEXT_GOLD, font=FONT_BOLD)

    draw.text((1502, 1255), "SYSTEM SHEET:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1502, 1270), "SHEET 1 OF 1 (COMPLETE)", fill=COLOR_TEXT_WHITE, font=FONT_BOLD)

    draw.text((1502, 1295), "CANVAS RESOLUTION:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1502, 1310), "2200 x 1500 PIXELS", fill=COLOR_TEXT_CYAN, font=FONT_MONO_BOLD)

    draw.text((1502, 1335), "CLASSIFICATION:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1502, 1350), "OPEN SOURCE HARDWARE", fill=COLOR_TEXT_WHITE, font=FONT_SMALL_BOLD)

    draw.text((1502, 1375), "CAD ENVIRONMENT:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1502, 1390), "FreeCAD Part API / Python 3", fill=COLOR_TEXT_CYAN, font=FONT_SMALL)

    # Col B:
    draw.text((1712, 1175), "DRAWING SCALE:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1712, 1190), "1:1.4 (ELEVATION VIEWS)", fill=COLOR_TEXT_WHITE, font=FONT_BOLD)

    draw.text((1712, 1215), "LINEAR UNITS / ANGLES:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1712, 1230), "MILLIMETERS [mm] / DEGREES [°]", fill=COLOR_TEXT_WHITE, font=FONT_BOLD)

    draw.text((1712, 1255), "ORTHOGRAPHIC PROJECTION:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1712, 1270), "THIRD ANGLE PROJECTION", fill=COLOR_TEXT_WHITE, font=FONT_SMALL_BOLD)

    # Standard Third-Angle Projection Symbol
    sym_y = 1320
    draw.ellipse([1740 - 10, sym_y - 10, 1740 + 10, sym_y + 10], outline=COLOR_TEXT_CYAN, width=1)
    draw.ellipse([1740 - 5, sym_y - 5, 1740 + 5, sym_y + 5], outline=COLOR_TEXT_CYAN, width=1)
    draw.line([(1725, sym_y), (1755, sym_y)], fill=COLOR_CENTERLINE, width=1)
    draw.line([(1740, sym_y - 15), (1740, sym_y + 15)], fill=COLOR_CENTERLINE, width=1)

    draw.polygon([
        (1770, sym_y - 10),
        (1795, sym_y - 5),
        (1795, sym_y + 5),
        (1770, sym_y + 10)
    ], outline=COLOR_TEXT_CYAN, width=1)
    draw.line([(1760, sym_y), (1805, sym_y)], fill=COLOR_CENTERLINE, width=1)

    draw.text((1712, 1365), "SURFACE FINISH / INFILL:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1712, 1380), "0.20 mm Layer / 25% Gyroid", fill=COLOR_TEXT_WHITE, font=FONT_SMALL)

    # Col C:
    draw.text((1922, 1175), "AUTHOR / DESIGN TEAM:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1922, 1190), "OpenCode BT4-V Engineering", fill=COLOR_TEXT_WHITE, font=FONT_BOLD)

    draw.text((1922, 1215), "RELEASE DATE:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1922, 1230), "2026-11-07", fill=COLOR_TEXT_WHITE, font=FONT_BOLD)

    draw.text((1922, 1255), "TARGET MATERIAL:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1922, 1270), "PETG (UV Stable) / Copper 12 AWG", fill=COLOR_TEXT_GOLD, font=FONT_BOLD)

    draw.text((1922, 1295), "MANUFACTURING TOLERANCES:", fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
    draw.text((1922, 1310), "3D Print: ±0.1 mm | Solid Vol: ±2%", fill=COLOR_TEXT_CYAN, font=FONT_SMALL)
    draw.text((1922, 1324), "Wire Cut: ±1.0 mm | Flare: ±0.5°", fill=COLOR_TEXT_CYAN, font=FONT_SMALL)

    # Status approval badge
    draw.rectangle([1922, 1350, 2150, 1395], fill=(16, 48, 28), outline=COLOR_TEXT_GREEN, width=1)
    draw.text((1935, 1358), "STATUS: VERIFIED & APPROVED", fill=COLOR_TEXT_GREEN, font=FONT_BOLD)
    draw.text((1935, 1374), "PASSED LAYER 1 DYNAMIC CHECKS", fill=COLOR_TEXT_WHITE, font=FONT_SMALL)

    # Bottom Copyright & Notice Bar
    draw.rectangle([1490, 1410, 2162, 1462], fill=(10, 26, 52), outline=COLOR_PANEL_BORDER, width=1)
    draw.text((1504, 1422), "NOTICE: SPECIFICATIONS ARE AUTHORITATIVE PER REQUIREMENTS.MD (§3–§16).", fill=COLOR_TEXT_MUTED, font=FONT_TINY)
    draw.text((1504, 1438), "ALL RECEPTIVE ELEMENTS OPTIMIZED FOR UNIVERSAL VHF-HIGH & UHF DTV STANDARDS.", fill=COLOR_TEXT_MUTED, font=FONT_TINY)

    # -------------------------------------------------------------------------
    # BOTTOM STRIP: GENERAL FABRICATION NOTES (X: 42 to 1475, Y: 1245 to 1462)
    # -------------------------------------------------------------------------
    draw.rectangle([42, 1245, 1475, 1275], fill=COLOR_HEADER_BG, outline=COLOR_PANEL_BORDER)
    draw.text((54, 1251), "GENERAL ENGINEERING, FABRICATION & ASSEMBLY INSTRUCTIONS", fill=COLOR_TEXT_WHITE, font=FONT_PANEL_HDR)

    # 3 Structured Instruction Columns
    draw.line([(505, 1275), (505, 1462)], fill=COLOR_PANEL_BORDER, width=1)
    draw.line([(985, 1275), (985, 1462)], fill=COLOR_PANEL_BORDER, width=1)

    # Column 1 Notes
    draw.text((56, 1282), "1. 3D PRINTING & MATERIAL STANDARDS", fill=COLOR_TEXT_GOLD, font=FONT_SUBHDR)
    col1_notes = [
        "• Material: Print with PETG (recommended for UV and indoor window thermal",
        "  stability) or high-temp PLA. Bed adhesion: PEI sheet with brim.",
        "• Slicer Configuration: 0.20 mm layer height, 4 perimeter walls, 5 top/bottom",
        "  solid layers, and 25% gyroid infill for rigid load transfer.",
        "• Calibration Coupon: Print BT4V_Fit_Coupon.stl first to verify 12 AWG wire snap,",
        "  M4 nut pocket clearance, 25 mm feed pitch, and tenon/mortise interlocking.",
        "• Cross-Pin Locking: Lock modular spine tenon joints with Ø2.5 mm cross-pins."
    ]
    ny = 1302
    for line in col1_notes:
        draw.text((56, ny), line, fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
        ny += 16

    # Column 2 Notes
    draw.text((520, 1282), "2. WIRE BENDING & PHASE TRANSPOSITION", fill=COLOR_TEXT_GOLD, font=FONT_SUBHDR)
    col2_notes = [
        "• Conductor: 12 AWG solid copper wire (nominal conductor diameter 2.05 mm).",
        "  Strip THHN insulation at terminal clamping zones or use bare copper.",
        "• Whisker Forming: Bend at midpoint around M4 stud; align to 25.5° flare angle",
        "  for VHF (690 mm wire) and 32.5° flare angle for UHF (410 mm wire).",
        "• Crossover Transposition: Install Phase Crossover Spacers between Bays 1–2",
        "  and Bays 3–4 (180° inversion). Ensures >=5.0 mm solid dielectric isolation.",
        "• Anti-Droop Spreaders: Snap Triangular Tine Spreaders onto VHF whiskers at",
        "  150 mm radius from apex. Eliminates gravitational sag and wind flutter."
    ]
    ny = 1302
    for line in col2_notes:
        draw.text((520, ny), line, fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
        ny += 16

    # Column 3 Notes
    draw.text((1000, 1282), "3. BALUN INTEGRATION & INDOOR MOUNTING", fill=COLOR_TEXT_GOLD, font=FONT_SUBHDR)
    col3_notes = [
        "• Matching Balun: Snap commercial RCA VH101R 4:1 matching transformer into",
        "  Center Feed cradle; clamp spade lugs under M4 feed studs and washers.",
        "• Coaxial Downlead: Connect 75 Ω RG6 coaxial cable to downward-facing",
        "  female F-connector. Secure cable with zip-tie through strain relief slot.",
        "• Anti-Rotation Hanging: Suspend from top hanging cap dual eyelets using",
        "  monofilament nylon cord or picture wire against an indoor window glass.",
        "• Metal Clearance: Ensure antenna is positioned at least 0.5 m away from",
        "  metallic window insect screens to prevent UHF signal attenuation."
    ]
    ny = 1302
    for line in col3_notes:
        draw.text((1000, ny), line, fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
        ny += 16

    # -------------------------------------------------------------------------
    # EXPORT & VERIFICATION
    # -------------------------------------------------------------------------
    print(f"[bt4v_drawing] Saving 2D technical drawing to: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", optimize=True)

    # Verify deliverable file
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Export failed: {output_path} does not exist.")

    file_size = os.path.getsize(output_path)
    with Image.open(output_path) as chk_img:
        dims = chk_img.size

    print(f"[bt4v_drawing] Verification Results:")
    print(f"  - File: {output_path}")
    print(f"  - Dimensions: {dims[0]} x {dims[1]} px (Expected: {CANVAS_WIDTH} x {CANVAS_HEIGHT})")
    print(f"  - File Size: {file_size:,} bytes ({file_size / 1024:.1f} kB)")

    if dims != (CANVAS_WIDTH, CANVAS_HEIGHT):
        raise ValueError(f"Image dimension mismatch: got {dims}, expected ({CANVAS_WIDTH}, {CANVAS_HEIGHT})")

    if file_size < MIN_FILE_SIZE_BYTES:
        raise ValueError(f"Image file size too small: {file_size} bytes (minimum {MIN_FILE_SIZE_BYTES} bytes)")

    print("[bt4v_drawing] 2D technical drawing generation complete: SUCCESS (Exit 0)")
    return True


if __name__ == "__main__":
    try:
        success = generate_drawing()
        sys.exit(0 if success else 1)
    except Exception as exc:
        print(f"[bt4v_drawing] ERROR: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
