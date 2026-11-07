#!/usr/bin/env python3
"""
BT4-V 3D Printed Antenna — 3D Printable Parts Preview Generator (v0.1.0)

Generates the master 3D printable parts preview deliverable:
    'BT4-V Parts Preview.png' (1800 × 800 px) in the project root directory.

Technical Specifications & Requirements Baseline:
- Requirements Baseline: Requirements.md §5–§11, §12.2, §16.3
- Plan Baseline: Plan.md §3.1 (T1.3)
- Deliverable: Exactly 1800 x 800 px PNG image, >10 kB file size.
- Theme: High-contrast, clean modern rendering theme:
  Dark charcoal (#161B22) background, card containers (#21262D),
  crisp line art, shaded isometric 3D views for parts.

Visual & Technical Content:
1. Title banner: "BT4-V 3D PRINTED ANTENNA — 3D PRINTABLE PARTS PREVIEW",
   Revision v0.1.0, Total Print Mass ~200 g.
2. Multi-panel layout clearly showcasing all 8 printable BT4-V parts + assembly:
   - Part 1: Center Feed Hub (1 required, 40 × 24 × 70 mm, 28,500 mm³)
   - Part 2: Whisker Bay Bracket (4 required, 50 × 18 × 40 mm, 19,200 mm³)
   - Part 3: Spine Segment (4 required, 20 × 14 × 120 mm, 16,800 mm³)
   - Part 4: Phase Crossover Spacer (2 required, 35 × 12 × 30 mm, 6,100 mm³)
   - Part 5: Triangular Tine Spreader (4 required, 72 × 12 × 8 mm, 2,200 mm³)
   - Part 6: Bowtie Support Strut (8 required, 65 × 10 × 8 mm, 1,800 mm³)
   - Part 7: Top Hanging Cap (1 required, 44 × 18 × 30 mm, 7,400 mm³)
   - Part 8: Fit Calibration Coupon (1 required, 90 × 50 × 10 mm, 26,500 mm³)
   - Part 9: Modular Spine Assembly Stack (17 printed pieces total, ~200 g set)
3. Descriptive callout annotations, dimensions, and quantity badges on each panel.
4. Assembly locations along the spine indicated on each panel.
5. Print settings summary banner (PETG recommended, 0.2 mm layer height, 3 perimeters, 25-30% infill).

Usage:
    python3 python/bt4v_preview.py
"""

import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# -----------------------------------------------------------------------------
# DIRECTORY SELF-RESOLUTION & CONSTANTS
# -----------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == "python" else SCRIPT_DIR
OUTPUT_FILENAME = "BT4-V Parts Preview.png"
OUTPUT_PATH = os.path.join(PROJECT_ROOT, OUTPUT_FILENAME)

CANVAS_WIDTH = 1800
CANVAS_HEIGHT = 800
MIN_FILE_SIZE_BYTES = 10 * 1024  # >10 kB per Testing Strategy §2.4

# -----------------------------------------------------------------------------
# COLOR PALETTE (Clean Modern Dark Charcoal Theme)
# -----------------------------------------------------------------------------
COLOR_CANVAS_BG = (22, 27, 34)       # Dark charcoal #161B22
COLOR_BANNER_BG = (13, 17, 23)       # Dark header/footer banner #0D1117
COLOR_CARD_BG = (33, 38, 45)         # Card container #21262D
COLOR_CARD_BORDER = (48, 54, 61)     # Card border #30363D
COLOR_CARD_HDR = (26, 32, 40)        # Card header #1A2028
COLOR_CARD_STRIP = (20, 25, 31)      # Sub-header strip

# Text & Badges
COLOR_TEXT_WHITE = (240, 246, 252)   # Primary text #F0F6FC
COLOR_TEXT_CYAN = (121, 192, 255)    # Accent cyan #79C0FF
COLOR_TEXT_BLUE = (88, 166, 255)     # Primary blue #58A6FF
COLOR_TEXT_GOLD = (227, 179, 65)     # Highlight gold #E3B341
COLOR_TEXT_GREEN = (63, 185, 80)     # Verified green #3FB950
COLOR_TEXT_PURPLE = (188, 140, 255)  # Purple accent #BC8CFF
COLOR_TEXT_MUTED = (139, 148, 158)   # Secondary text #8B949E

# 3D Shading & Functional Colors
COLOR_PLASTIC_BASE = (48, 102, 170)  # Mid tone blue #3066AA
COLOR_PLASTIC_ACCENT = (58, 118, 192)# Lighter accent
COLOR_PLASTIC_EDGE = (120, 195, 255) # Crisp cyan edge outline #78C3FF
COLOR_CAVITY_FILL = (18, 30, 48)     # Dark recessed cavity
COLOR_CAVITY_EDGE = (70, 130, 200)   # Cavity rim outline
COLOR_COPPER = (255, 157, 66)        # 12 AWG copper wire #FF9D42
COLOR_COPPER_EDGE = (255, 195, 130)  # Copper highlight
COLOR_STEEL = (225, 235, 245)        # M4 hardware / cross-pins
COLOR_BALUN_BODY = (28, 40, 52)      # RCA VH101R balun body
COLOR_BALUN_ACCENT = (240, 136, 62)  # RCA orange label accent


# -----------------------------------------------------------------------------
# FONT LOADER WITH COMPREHENSIVE FALLBACKS
# -----------------------------------------------------------------------------
def load_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.ImageFont:
    """Loads best available TrueType font on Linux systems with graceful fallback."""
    if mono:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf" if bold else
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf" if bold else
            "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


# Fonts
FONT_TITLE = load_font(17, bold=True)
FONT_SUBTITLE = load_font(10, bold=False)
FONT_BADGE = load_font(9, bold=True)
FONT_CARD_TITLE = load_font(11, bold=True)
FONT_CARD_METRIC = load_font(9, bold=True, mono=True)
FONT_LOC_LABEL = load_font(8, bold=True)
FONT_LOC_VALUE = load_font(8, bold=False)
FONT_CALLOUT = load_font(8, bold=True)
FONT_CALLOUT_SUB = load_font(7, bold=False)
FONT_FOOTER_HDR = load_font(8, bold=True)
FONT_FOOTER_TXT = load_font(8, bold=False)
FONT_BANNER_HDR = load_font(9, bold=True)
FONT_BANNER_TXT = load_font(8, bold=False)


# -----------------------------------------------------------------------------
# 3D ISOMETRIC / ORTHOGRAPHIC CAMERA & LIGHTING ENGINE
# -----------------------------------------------------------------------------
class Camera:
    """Orthographic 3D look-at camera with Lambertian directional lighting."""
    def __init__(self, eye=(85.0, -110.0, 75.0), target=(0.0, 0.0, 0.0)):
        fx = target[0] - eye[0]
        fy = target[1] - eye[1]
        fz = target[2] - eye[2]
        flen = math.sqrt(fx * fx + fy * fy + fz * fz)
        self.fx, self.fy, self.fz = fx / flen, fy / flen, fz / flen

        # Camera Right = normalize(Forward x WorldUp(0,0,1))
        rx = self.fy * 1.0
        ry = -self.fx * 1.0
        rz = 0.0
        rlen = math.sqrt(rx * rx + ry * ry)
        self.rx, self.ry, self.rz = rx / rlen, ry / rlen, rz / rlen

        # Camera Up = Camera Right x Forward
        self.ux = self.ry * self.fz - self.rz * self.fy
        self.uy = self.rz * self.fx - self.rx * self.fz
        self.uz = self.rx * self.fy - self.ry * self.fx
        self.target = target

    def project(self, x: float, y: float, z: float, cx: float, cy: float, scale: float):
        vx = x - self.target[0]
        vy = y - self.target[1]
        vz = z - self.target[2]
        u = cx + scale * (vx * self.rx + vy * self.ry + vz * self.rz)
        v = cy - scale * (vx * self.ux + vy * self.uy + vz * self.uz)
        depth = vx * self.fx + vy * self.fy + vz * self.fz
        return u, v, depth


class Mesh3D:
    """3D polygon mesh container supporting depth-sorted shaded rendering."""
    def __init__(self):
        # List of (points_3d, normal_3d, base_color, edge_color, line_width, depth_bias)
        self.faces = []

    def add_face(self, pts, normal, base_col, edge_col=COLOR_PLASTIC_EDGE, lw=1, bias=0.0):
        self.faces.append((pts, normal, base_col, edge_col, lw, bias))

    def add_box(self, x0, y0, z0, dx, dy, dz, base_col=COLOR_PLASTIC_BASE, edge_col=COLOR_PLASTIC_EDGE, lw=1, bias=0.0):
        x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
        # Top (+Z)
        self.add_face([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], (0, 0, 1), base_col, edge_col, lw, bias)
        # Bottom (-Z)
        self.add_face([(x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (x1, y0, z0)], (0, 0, -1), base_col, edge_col, lw, bias)
        # Front (-Y)
        self.add_face([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], (0, -1, 0), base_col, edge_col, lw, bias)
        # Back (+Y)
        self.add_face([(x1, y1, z0), (x0, y1, z0), (x0, y1, z1), (x1, y1, z1)], (0, 1, 0), base_col, edge_col, lw, bias)
        # Right (+X)
        self.add_face([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], (1, 0, 0), base_col, edge_col, lw, bias)
        # Left (-X)
        self.add_face([(x0, y1, z0), (x0, y0, z0), (x0, y0, z1), (x0, y1, z1)], (-1, 0, 0), base_col, edge_col, lw, bias)

    def add_cavity(self, x0, y0, z0, dx, dy, dz, cav_col=COLOR_CAVITY_FILL, edge_col=COLOR_CAVITY_EDGE, lw=1, bias=-6.0):
        x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
        # Back of cavity facing viewer (normal = 0, -1, 0)
        self.add_face([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], (0, -1, 0), cav_col, edge_col, lw, bias)
        # Bottom of cavity facing up (normal = 0, 0, 1)
        self.add_face([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], (0, 0, 1), cav_col, edge_col, lw, bias)
        # Top of cavity facing down (normal = 0, 0, -1)
        self.add_face([(x0, y0, z1), (x0, y1, z1), (x1, y1, z1), (x1, y0, z1)], (0, 0, -1), cav_col, edge_col, lw, bias)
        # Left wall facing right (normal = 1, 0, 0)
        self.add_face([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], (1, 0, 0), cav_col, edge_col, lw, bias)
        # Right wall facing left (normal = -1, 0, 0)
        self.add_face([(x1, y1, z0), (x1, y0, z0), (x1, y0, z1), (x1, y1, z1)], (-1, 0, 0), cav_col, edge_col, lw, bias)

    def add_cylinder_z(self, cx, cy, z0, z1, radius, sides=12, base_col=COLOR_STEEL, edge_col=COLOR_PLASTIC_EDGE, bias=0.0):
        pts_bot = []
        pts_top = []
        for i in range(sides):
            th = 2.0 * math.pi * i / sides
            px = cx + radius * math.cos(th)
            py = cy + radius * math.sin(th)
            pts_bot.append((px, py, z0))
            pts_top.append((px, py, z1))
        self.add_face(pts_top, (0, 0, 1), base_col, edge_col, 1, bias)
        for i in range(sides):
            j = (i + 1) % sides
            th_mid = 2.0 * math.pi * (i + 0.5) / sides
            nx = math.cos(th_mid)
            ny = math.sin(th_mid)
            quad = [pts_bot[i], pts_bot[j], pts_top[j], pts_top[i]]
            self.add_face(quad, (nx, ny, 0), base_col, edge_col, 1, bias)

    def add_cylinder_y(self, cx, y0, y1, cz, radius, sides=12, base_col=COLOR_STEEL, edge_col=COLOR_PLASTIC_EDGE, bias=0.0):
        pts_front = []
        pts_back = []
        for i in range(sides):
            th = 2.0 * math.pi * i / sides
            px = cx + radius * math.cos(th)
            pz = cz + radius * math.sin(th)
            pts_front.append((px, y0, pz))
            pts_back.append((px, y1, pz))
        self.add_face(pts_front, (0, -1, 0), base_col, edge_col, 1, bias)
        for i in range(sides):
            j = (i + 1) % sides
            th_mid = 2.0 * math.pi * (i + 0.5) / sides
            nx = math.cos(th_mid)
            nz = math.sin(th_mid)
            quad = [pts_front[i], pts_front[j], pts_back[j], pts_back[i]]
            self.add_face(quad, (nx, 0, nz), base_col, edge_col, 1, bias)

    def render(self, draw: ImageDraw.ImageDraw, camera: Camera, cx: float, cy: float, scale: float,
               light_dir=(-0.4, -0.65, 0.65)):
        lx, ly, lz = light_dir
        llen = math.sqrt(lx * lx + ly * ly + lz * lz)
        lx, ly, lz = lx / llen, ly / llen, lz / llen

        rendered = []
        for pts, (nx, ny, nz), base_col, edge_col, lw, bias in self.faces:
            dot_cam = -(nx * camera.fx + ny * camera.fy + nz * camera.fz)
            if dot_cam > 0.001:
                poly2d = []
                d_sum = 0.0
                for px, py, pz in pts:
                    u, v, d = camera.project(px, py, pz, cx, cy, scale)
                    poly2d.append((u, v))
                    d_sum += d
                avg_depth = (d_sum / len(pts)) + bias
                dot_l = nx * lx + ny * ly + nz * lz
                bright = 0.36 + 0.64 * max(0.0, dot_l)
                col = (
                    min(255, max(0, int(base_col[0] * bright))),
                    min(255, max(0, int(base_col[1] * bright))),
                    min(255, max(0, int(base_col[2] * bright)))
                )
                rendered.append((avg_depth, poly2d, col, edge_col, lw))

        rendered.sort(key=lambda item: item[0], reverse=True)
        for _, poly, col, edge_col, lw in rendered:
            draw.polygon(poly, fill=col, outline=edge_col)


# -----------------------------------------------------------------------------
# 3D MODEL BUILDERS FOR THE 9 PANELS
# -----------------------------------------------------------------------------
def build_center_feed_hub() -> Mesh3D:
    """1. Center Feed Hub: 40 × 24 × 70 mm, Balun cradle, 25 mm feed posts, M4 nut pockets."""
    m = Mesh3D()
    m.add_box(-20, -12, -35, 40, 24, 70, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-7, -5, 35, 14, 10, 10, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cylinder_y(0, -5.5, -4.5, 40, 1.3, sides=8, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_PLASTIC_EDGE)
    m.add_cavity(-13, -12.1, -18, 26, 8, 36, COLOR_CAVITY_FILL, (80, 150, 220))
    m.add_box(-11, -10.5, -15, 22, 7, 30, COLOR_BALUN_BODY, COLOR_BALUN_ACCENT, bias=-10.0)
    m.add_cylinder_z(0, -7, -26, -15, 4.5, sides=12, base_col=COLOR_STEEL, edge_col=(200, 215, 230), bias=-12.0)
    m.add_box(-15, -12.1, 20, 5, 4, 11, COLOR_PLASTIC_ACCENT, (130, 200, 255), bias=-2.0)
    m.add_box(10, -12.1, 20, 5, 4, 11, COLOR_PLASTIC_ACCENT, (130, 200, 255), bias=-2.0)
    m.add_cylinder_y(-12.5, -13.5, -11.5, 25.5, 2.2, sides=10, base_col=COLOR_STEEL, edge_col=COLOR_TEXT_WHITE, bias=-12.0)
    m.add_cylinder_y(12.5, -13.5, -11.5, 25.5, 2.2, sides=10, base_col=COLOR_STEEL, edge_col=COLOR_TEXT_WHITE, bias=-12.0)
    m.add_box(-13.5, -12.8, 15, 2, 1, 10.5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-13.0)
    m.add_box(11.5, -12.8, 15, 2, 1, 10.5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-13.0)
    m.add_box(-14, -12.5, -35, 3, 1.2, 70, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(11, -12.5, -35, 3, 1.2, 70, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_cavity(-8, -12.2, -26, 16, 2, 3, COLOR_CAVITY_FILL, (70, 120, 180), bias=-8.0)
    return m


def build_whisker_bay_bracket() -> Mesh3D:
    """2. Whisker Bay Bracket: 50 × 18 × 40 mm, dual flare guides, apex clamp, phase channels."""
    m = Mesh3D()
    m.add_box(-12, -9, -20, 24, 18, 40, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-7, -5, 20, 14, 10, 10, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cylinder_y(0, -5.5, -4.5, 25, 1.3, sides=8, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_PLASTIC_EDGE)
    m.add_box(-25, -9, -15, 13, 18, 30, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(12, -9, -15, 13, 18, 30, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-14, -9.5, -20, 3, 1.2, 40, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(11, -9.5, -20, 3, 1.2, 40, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-28, -9.6, 6, 16, 1.4, 2.5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-7.0)
    m.add_box(-28, -9.6, -8.5, 16, 1.4, 2.5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-7.0)
    m.add_box(12, -9.6, 6, 16, 1.4, 2.5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-7.0)
    m.add_box(12, -9.6, -8.5, 16, 1.4, 2.5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-7.0)
    m.add_cylinder_y(-12.5, -10.5, -9.0, 0, 3.2, sides=10, base_col=COLOR_STEEL, edge_col=COLOR_TEXT_WHITE, bias=-12.0)
    m.add_cylinder_y(12.5, -10.5, -9.0, 0, 3.2, sides=10, base_col=COLOR_STEEL, edge_col=COLOR_TEXT_WHITE, bias=-12.0)
    m.add_cavity(-7, -5, -20.1, 14, 10, 8, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-10.0)
    return m


def build_spine_segment() -> Mesh3D:
    """3. Spine Segment: 20 × 14 × 120 mm, I-beam cross section, 110 mm active length."""
    m = Mesh3D()
    m.add_box(-10, -7, -55, 20, 2.8, 110, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-10, 4.2, -55, 20, 2.8, 110, (38, 85, 145), (100, 175, 240))
    m.add_box(-3.5, -4.2, -55, 7, 8.4, 110, COLOR_PLASTIC_ACCENT, COLOR_PLASTIC_EDGE)
    m.add_box(-7, -5, 55, 14, 10, 10, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cylinder_y(0, -5.5, -4.5, 60, 1.3, sides=8, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_PLASTIC_EDGE)
    m.add_cylinder_y(0, -7.2, -6.5, -48, 1.3, sides=8, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_PLASTIC_EDGE, bias=-6.0)
    m.add_box(-8.5, -7.5, -55, 2.8, 1.2, 110, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(5.7, -7.5, -55, 2.8, 1.2, 110, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    for rz in [-30, 0, 30]:
        m.add_box(-10, -4.2, rz - 2, 20, 8.4, 4, (44, 95, 160), COLOR_PLASTIC_EDGE, bias=-2.0)
    return m


def build_phase_crossover_spacer() -> Mesh3D:
    """4. Phase Crossover Spacer: 35 × 12 × 30 mm, dual diagonal crossing channels, snap clip."""
    m = Mesh3D()
    m.add_box(-17.5, -6, -15, 35, 8, 30, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-12, 2, -12, 24, 5, 24, COLOR_PLASTIC_ACCENT, (130, 200, 255))
    m.add_cavity(-8, 2.1, -12.1, 16, 5, 24.2, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-8.0)
    for i, t in enumerate([-12, -8, -4, 0, 4, 8, 12]):
        wx = -12.5 + (25.0 * (t + 12) / 24.0)
        wz = 12.0 - (24.0 * (t + 12) / 24.0)
        m.add_box(wx - 2, -6.6, wz - 2.5, 4, 1.4, 5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-10.0)
    for i, t in enumerate([-12, -8, -4, 0, 4, 8, 12]):
        wx = 12.5 - (25.0 * (t + 12) / 24.0)
        wz = 12.0 - (24.0 * (t + 12) / 24.0)
        m.add_box(wx - 2, -0.2, wz - 2.5, 4, 1.4, 5, (200, 110, 40), (220, 140, 70), bias=-3.0)
    m.add_box(-16, -3.5, -14, 32, 3, 28, (52, 112, 185), (140, 210, 255), bias=-1.0)
    return m


def build_triangular_tine_spreader() -> Mesh3D:
    """5. Triangular Tine Spreader: 72 × 12 × 8 mm, 66 mm C-to-C snap jaws, ribbed truss."""
    m = Mesh3D()
    m.add_box(-33, -3, -3, 66, 6, 6, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-33, -1.5, 3, 66, 3, 1.5, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_box(-33, -1.5, -4.5, 66, 3, 1.5, (38, 85, 145), (100, 175, 240))
    m.add_box(-36, -6, -4, 6, 12, 8, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cavity(-35, -3, -4.1, 4, 6, 8.2, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-6.0)
    m.add_box(-34.5, -8, -1.5, 3, 16, 3, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-12.0)
    m.add_box(30, -6, -4, 6, 12, 8, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cavity(31, -3, -4.1, 4, 6, 8.2, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-6.0)
    m.add_box(31.5, -8, -1.5, 3, 16, 3, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-12.0)
    for px in [-22, -11, 0, 11, 22]:
        m.add_cavity(px - 3.5, -3.1, -1.8, 7, 2, 3.6, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-4.0)
    return m


def build_bowtie_support_mesh() -> Mesh3D:
    """6. Bowtie Support Strut: 65 × 10 × 8 mm, snap jaw, ribbed truss strut."""
    m = Mesh3D()
    m.add_box(-32.5, -5, 0, 65, 10, 8, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-30, -3, 6.5, 60, 6, 1.5, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_box(-30, -3, 0, 60, 6, 1.5, (38, 85, 145), (100, 175, 240))
    m.add_box(25, -5, 0, 7.5, 10, 8, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cavity(27.5, -5.1, 1.5, 4, 10.2, 5, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-6.0)
    m.add_box(28.5, -6, 2.5, 2, 12, 3, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-12.0)
    for px in [-18, -8, 2, 12]:
        m.add_cavity(px - 2.5, -5.1, 2.0, 5, 10.2, 4, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-4.0)
    return m


def build_top_hanging_cap() -> Mesh3D:
    """7. Top Hanging Cap: 44 × 18 × 30 mm, dual Ø5 mm eyelets, female mortise."""
    m = Mesh3D()
    m.add_box(-22, -9, -15, 44, 18, 18, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_cavity(-7, -5, -15.1, 14, 10, 10, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-8.0)
    m.add_cylinder_y(0, -9.2, -8.5, -10, 1.3, sides=8, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_PLASTIC_EDGE, bias=-5.0)
    m.add_box(-19, -4.5, 3, 8, 9, 12, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cylinder_y(-15, -4.6, 4.6, 9, 2.5, sides=12, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_TEXT_WHITE, bias=-10.0)
    m.add_box(11, -4.5, 3, 8, 9, 12, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cylinder_y(15, -4.6, 4.6, 9, 2.5, sides=12, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_TEXT_WHITE, bias=-10.0)
    m.add_box(-17, -0.8, 8, 34, 1.6, 2, (180, 220, 255), COLOR_TEXT_WHITE, bias=-14.0)
    return m


def build_fit_calibration_coupon() -> Mesh3D:
    """8. Fit Calibration Coupon: 90 × 50 × 10 mm, friction slots, snap cavities, nut pocket, joints."""
    m = Mesh3D()
    m.add_box(-45, -25, -5, 90, 50, 10, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    for idx, (sx, sw) in enumerate([(-36, 2.8), (-30, 3.0), (-24, 3.2), (-18, 3.4)]):
        m.add_cavity(sx - sw / 2, -18, 2.0, sw, 36, 3.1, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-6.0)
    m.add_box(-24 - 1.3, -20, 2.5, 2.6, 40, 2.6, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-10.0)
    m.add_cavity(-10 - 1.1, -16, 1.5, 2.2, 32, 3.6, COLOR_CAVITY_FILL, (80, 160, 230), bias=-6.0)
    m.add_cavity(-4 - 1.2, -16, 1.5, 2.4, 32, 3.6, COLOR_CAVITY_FILL, (80, 160, 230), bias=-6.0)
    m.add_cylinder_z(9, 0, 1.5, 5.2, 2.2, sides=12, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_TEXT_WHITE, bias=-8.0)
    m.add_cylinder_z(9, 0, 3.2, 5.2, 4.2, sides=6, base_col=COLOR_STEEL, edge_col=COLOR_TEXT_WHITE, bias=-12.0)
    m.add_box(24, -14, 5, 14, 10, 8, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cylinder_y(31, -14.2, -13.5, 9, 1.3, sides=8, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_PLASTIC_EDGE)
    m.add_cavity(24, 4, 0, 14, 10, 5.1, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-8.0)
    m.add_cylinder_z(20, -20, 5, 10, 2.5, sides=10, base_col=COLOR_PLASTIC_ACCENT, edge_col=(140, 210, 255))
    m.add_cylinder_z(45, -20, 5, 10, 2.5, sides=10, base_col=COLOR_PLASTIC_ACCENT, edge_col=(140, 210, 255))
    return m


def build_spine_assembly_stack() -> Mesh3D:
    """9. Spine Assembly & System Stack: Full 560 mm vertical array with balun, crossovers, and bays."""
    m = Mesh3D()
    m.add_box(-8, -4, 62, 16, 8, 10, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_box(-6, -2, 72, 3, 4, 5, COLOR_PLASTIC_ACCENT, COLOR_TEXT_WHITE)
    m.add_box(3, -2, 72, 3, 4, 5, COLOR_PLASTIC_ACCENT, COLOR_TEXT_WHITE)
    m.add_box(-12, -4, 46, 24, 8, 16, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-26, -4.5, 54, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-26, -4.5, 42, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, 54, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, 42, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-5, -3, 30, 10, 6, 16, (40, 90, 150), COLOR_PLASTIC_EDGE)
    m.add_box(-7, -4.5, 34, 14, 3, 8, COLOR_PLASTIC_ACCENT, (140, 210, 255), bias=-3.0)
    m.add_box(-12, -4, 14, 24, 8, 16, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-22, -4.5, 20, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-22, -4.5, 12, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, 20, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, 12, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-5, -3, 2, 10, 6, 12, (40, 90, 150), COLOR_PLASTIC_EDGE)
    m.add_box(-10, -5, -14, 20, 10, 16, (52, 115, 185), (140, 210, 255), bias=-2.0)
    m.add_box(-6, -5.5, -11, 12, 4, 10, COLOR_BALUN_BODY, COLOR_BALUN_ACCENT, bias=-6.0)
    m.add_cylinder_z(0, -3.5, -18, -14, 2.5, sides=8, base_col=COLOR_STEEL, edge_col=COLOR_TEXT_WHITE, bias=-8.0)
    m.add_box(-5, -3, -26, 10, 6, 12, (40, 90, 150), COLOR_PLASTIC_EDGE)
    m.add_box(-12, -4, -42, 24, 8, 16, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-22, -4.5, -36, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-22, -4.5, -44, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, -36, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, -44, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-5, -3, -58, 10, 6, 16, (40, 90, 150), COLOR_PLASTIC_EDGE)
    m.add_box(-7, -4.5, -54, 14, 3, 8, COLOR_PLASTIC_ACCENT, (140, 210, 255), bias=-3.0)
    m.add_box(-12, -4, -74, 24, 8, 16, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-26, -4.5, -66, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-26, -4.5, -78, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, -66, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, -78, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-6.5, -4.8, -74, 1.8, 1, 146, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-4.0)
    m.add_box(4.7, -4.8, -74, 1.8, 1, 146, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-4.0)
    return m


# -----------------------------------------------------------------------------
# CALLOUT & CARD RENDERING UTILITIES
# -----------------------------------------------------------------------------
def draw_callout_pill(draw: ImageDraw.ImageDraw, tx: float, ty: float, bx: float, by: float,
                      text: str, subtext: str = None, color: tuple = COLOR_TEXT_BLUE):
    """Draws a callout with anchor dot, leader line, and rounded badge pill."""
    t_box = FONT_CALLOUT.getbbox(text)
    tw = t_box[2] - t_box[0]
    th = t_box[3] - t_box[1]
    sw = 0
    sh = 0
    if subtext:
        s_box = FONT_CALLOUT_SUB.getbbox(subtext)
        sw = s_box[2] - s_box[0]
        sh = s_box[3] - s_box[1] + 2
    bw = max(tw, sw) + 8
    bh = th + sh + 5

    draw.ellipse([(tx - 2.0, ty - 2.0), (tx + 2.0, ty + 2.0)], fill=color, outline=COLOR_TEXT_WHITE)
    cx = bx + bw / 2
    cy = by + bh / 2
    draw.line([(tx, ty), (cx, cy)], fill=color, width=1)
    draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=3, fill=(18, 24, 32), outline=color, width=1)
    draw.text((bx + 4, by + 2), text, fill=COLOR_TEXT_WHITE, font=FONT_CALLOUT)
    if subtext:
        draw.text((bx + 4, by + 2 + th + 1), subtext, fill=COLOR_TEXT_MUTED, font=FONT_CALLOUT_SUB)


def draw_card(draw: ImageDraw.ImageDraw, x0: int, y0: int, width: int, height: int,
              part_num: str, title: str, subtitle: str, qty_text: str, qty_color: tuple,
              location_str: str, mesh: Mesh3D, camera: Camera, mesh_scale: float,
              callouts: list, footer_bullets: list):
    """Draws a complete component card with header, badges, 3D viewport, and footer specs."""
    x1 = x0 + width
    y1 = y0 + height

    # 1. Main Container
    draw.rounded_rectangle([(x0, y0), (x1, y1)], radius=5, fill=COLOR_CARD_BG, outline=COLOR_CARD_BORDER, width=1)

    # 2. Card Header
    hdr_h = 28
    draw.rounded_rectangle([(x0, y0), (x1, y0 + hdr_h)], radius=5, fill=COLOR_CARD_HDR)
    draw.rectangle([(x0, y0 + hdr_h - 4), (x1, y0 + hdr_h)], fill=COLOR_CARD_HDR)
    draw.line([(x0, y0 + hdr_h), (x1, y0 + hdr_h)], fill=COLOR_CARD_BORDER, width=1)

    draw.text((x0 + 8, y0 + 3), f"{part_num}. {title}", fill=COLOR_TEXT_WHITE, font=FONT_CARD_TITLE)
    draw.text((x0 + 8, y0 + 15), subtitle, fill=COLOR_TEXT_CYAN, font=FONT_CARD_METRIC)

    # Qty Badge Pill (Top Right)
    q_box = FONT_BADGE.getbbox(qty_text)
    qw = q_box[2] - q_box[0] + 8
    qh = q_box[3] - q_box[1] + 3
    qx = x1 - qw - 8
    qy = y0 + 5
    draw.rounded_rectangle([(qx, qy), (qx + qw, qy + qh)], radius=3, fill=(18, 25, 33), outline=qty_color, width=1)
    draw.text((qx + 4, qy + 1), qty_text, fill=qty_color, font=FONT_BADGE)

    # 3. Location Strip
    loc_h = 18
    loc_y = y0 + hdr_h
    draw.rectangle([(x0, loc_y), (x1, loc_y + loc_h)], fill=COLOR_CARD_STRIP)
    draw.line([(x0, loc_y + loc_h), (x1, loc_y + loc_h)], fill=COLOR_CARD_BORDER, width=1)

    loc_lbl = "LOCATION:"
    lbl_box = FONT_LOC_LABEL.getbbox(loc_lbl)
    lbl_w = lbl_box[2] - lbl_box[0]
    draw.text((x0 + 8, loc_y + 3), loc_lbl, fill=COLOR_TEXT_GOLD, font=FONT_LOC_LABEL)
    draw.text((x0 + 12 + lbl_w, loc_y + 3), location_str, fill=COLOR_TEXT_WHITE, font=FONT_LOC_VALUE)

    # 4. 3D Mesh Viewport (Card height 220: header 28 + loc 18 = 46. Footer ~42. Remaining = 132 px)
    view_cy = y0 + hdr_h + loc_h + 66
    view_cx = x0 + width / 2
    mesh.render(draw, camera, view_cx, view_cy, mesh_scale)

    # 5. Callouts
    for callout in callouts:
        t3d, (rbx, rby), c_title, c_sub, c_col = callout
        tu, tv, _ = camera.project(t3d[0], t3d[1], t3d[2], view_cx, view_cy, mesh_scale)
        bx = x0 + rbx
        by = y0 + rby
        draw_callout_pill(draw, tu, tv, bx, by, c_title, c_sub, color=c_col)

    # 6. Technical Specifications Footer (2 bullet lines)
    ftr_h = 42
    ftr_y = y1 - ftr_h
    draw.rectangle([(x0, ftr_y), (x1, y1)], fill=COLOR_CARD_HDR)
    draw.line([(x0, ftr_y), (x1, ftr_y)], fill=COLOR_CARD_BORDER, width=1)
    draw.text((x0 + 8, ftr_y + 3), "KEY TECHNICAL SPECIFICATIONS:", fill=COLOR_TEXT_CYAN, font=FONT_FOOTER_HDR)

    line_y = ftr_y + 15
    for bullet in footer_bullets[:2]:
        draw.text((x0 + 8, line_y), "•", fill=COLOR_TEXT_BLUE, font=FONT_FOOTER_HDR)
        draw.text((x0 + 16, line_y), bullet, fill=COLOR_TEXT_MUTED, font=FONT_FOOTER_TXT)
        line_y += 12


# -----------------------------------------------------------------------------
# MASTER PREVIEW GENERATOR ROUTINE
# -----------------------------------------------------------------------------
def generate_preview():
    """Generates the master 1800 x 800 pixel BT4-V parts preview PNG image."""
    print("=" * 78)
    print("BT4-V 3D PRINTED ANTENNA — 3D PRINTABLE PARTS PREVIEW GENERATOR (v0.1.0)")
    print(f"Canvas: {CANVAS_WIDTH} × {CANVAS_HEIGHT} px  |  Target Output: {OUTPUT_PATH}")
    print("=" * 78)

    img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), COLOR_CANVAS_BG)
    draw = ImageDraw.Draw(img)

    # 1. Top Header Banner
    draw.rectangle([(12, 6), (CANVAS_WIDTH - 12, 50)], fill=COLOR_BANNER_BG, outline=COLOR_CARD_BORDER, width=1)
    draw.text((22, 11), "BT4-V 3D PRINTED ANTENNA — 3D PRINTABLE PARTS PREVIEW", fill=COLOR_TEXT_WHITE, font=FONT_TITLE)
    draw.text((22, 32), "Revision v0.1.0  |  Total Print Mass ~200 g (PETG/PLA)  |  8 Modular Components + Assembly  |  100% FreeCAD CSG",
              fill=COLOR_TEXT_CYAN, font=FONT_SUBTITLE)

    # Top Right Badges
    badges = [
        ("REVISION v0.1.0", COLOR_TEXT_GOLD),
        ("8 PARTS + ASSEMBLY", COLOR_TEXT_GREEN),
        ("ASME Y14.5M CAD", COLOR_TEXT_BLUE)
    ]
    bx = CANVAS_WIDTH - 22
    for b_text, b_col in reversed(badges):
        bb = FONT_BADGE.getbbox(b_text)
        bw = bb[2] - bb[0] + 12
        bh = bb[3] - bb[1] + 6
        bx -= bw
        draw.rounded_rectangle([(bx, 14), (bx + bw, 14 + bh)], radius=3, fill=(18, 25, 33), outline=b_col, width=1)
        draw.text((bx + 6, b_text and 17 or 17), b_text, fill=b_col, font=FONT_BADGE)
        bx -= 8

    # 2. Bottom Print Settings Summary Banner
    b_top = 746
    draw.rectangle([(12, b_top), (CANVAS_WIDTH - 12, 794)], fill=COLOR_BANNER_BG, outline=COLOR_CARD_BORDER, width=1)
    draw.text((22, b_top + 4), "RECOMMENDED 3D PRINT SPECIFICATIONS & FABRICATION GUIDELINES:", fill=COLOR_TEXT_GOLD, font=FONT_BANNER_HDR)
    draw.text((22, b_top + 17),
              "• Material: PETG (recommended for UV/outdoor durability) or UV-stable PLA   • Layer Height: 0.20 mm   • Perimeters: 3–4 Walls (≥1.2 mm shell)   • Infill: 25–30% Gyroid or Grid   • Solid Layers: 4 Top / 4 Bottom",
              fill=COLOR_TEXT_MUTED, font=FONT_BANNER_TXT)
    draw.text((22, b_top + 29),
              "• Print Orientation: Flat on bed (0 supports required across all parts)   • Nozzle: 0.40 mm   • Bed Compatibility: Fits standard 220×220 or 235×235 mm build plates   • Total Antenna BOM: 17 pieces (~200 g)",
              fill=COLOR_TEXT_CYAN, font=FONT_BANNER_TXT)

    # Camera Instances
    cam_standard = Camera(eye=(85.0, -110.0, 75.0), target=(0.0, 0.0, 0.0))
    cam_flat = Camera(eye=(70.0, -90.0, 110.0), target=(0.0, 0.0, 0.0))
    cam_tall = Camera(eye=(100.0, -120.0, 50.0), target=(0.0, 0.0, 0.0))

    # Cards Geometry Setup (3 Columns × 3 Rows = 9 Cards)
    card_w = 580
    card_h = 220
    col_x = [15, 610, 1205]
    row_y = [56, 288, 520]

    # --- CARD 1: CENTER FEED HUB ---
    c1_callouts = [
        ((0, -12, 0), (10, 38), "RCA VH101R Cradle", "Contoured Balun Cavity", COLOR_TEXT_BLUE),
        ((-12.5, -12, 24), (320, 38), "25 mm Feed Posts", "M4 Studs & Terminals", COLOR_TEXT_GOLD),
        ((0, 0, 40), (10, 145), "Spine Joint", "+Z Tenon & -Z Mortise", COLOR_TEXT_CYAN),
        ((0, -12, -26), (320, 145), "Strain Relief", "Zip-Tie Loop Slot", COLOR_TEXT_PURPLE)
    ]
    c1_bullets = [
        "Houses commercial RCA VH101R balun directly between Bay 2 and Bay 3.",
        "25 mm feed terminals mate with 12 AWG copper phase lines and balun spade lugs."
    ]
    draw_card(draw, col_x[0], row_y[0], card_w, card_h,
              "01", "CENTER FEED HUB", "stl/BT4V_Center_Feed.stl  •  40 × 24 × 70 mm  •  28,500 mm³",
              "1 REQUIRED", COLOR_TEXT_GREEN, "Spine Center — Between Bay 2 & Bay 3 (Z = 0 mm)",
              build_center_feed_hub(), cam_standard, 1.45, c1_callouts, c1_bullets)

    # --- CARD 2: WHISKER BAY BRACKET ---
    c2_callouts = [
        ((-20, -9, 8), (10, 38), "Dual Flare Guides", "25.5° VHF & 32.5° UHF V-Slots", COLOR_TEXT_BLUE),
        ((-12.5, -10, 0), (320, 38), "Apex Clamping", "2 × M4 Bolt Holes & Nuts", COLOR_TEXT_GOLD),
        ((0, 0, 25), (10, 145), "Spine Tenon", "Symmetrical Interlock", COLOR_TEXT_CYAN),
        ((11, -9, -10), (320, 145), "Phase Channels", "3.2 × 3.0 mm Wire Grooves", COLOR_TEXT_PURPLE)
    ]
    c2_bullets = [
        "Universal whisker mount supporting VHF (25.5°) and UHF (32.5°) flare angles.",
        "Clamps whisker apex and phase line together via M4 bolts and captive nuts."
    ]
    draw_card(draw, col_x[1], row_y[0], card_w, card_h,
              "02", "WHISKER BAY BRACKET", "stl/BT4V_Bay_Bracket.stl  •  50 × 18 × 40 mm  •  19,200 mm³",
              "4 REQUIRED", COLOR_TEXT_GREEN, "Bays 1, 2, 3, & 4 (130 mm Array Pitch)",
              build_whisker_bay_bracket(), cam_standard, 1.80, c2_callouts, c2_bullets)

    # --- CARD 3: SPINE SEGMENT ---
    c3_callouts = [
        ((-10, 0, 15), (10, 38), "I-Beam Profile", "Flanges Maximize Stiffness", COLOR_TEXT_BLUE),
        ((0, 0, 0), (320, 38), "110 mm Active Length", "Exact 130 mm Bay Pitch", COLOR_TEXT_GOLD),
        ((0, 0, 60), (10, 145), "Tenon/Mortise", "2.6 mm Cross-Pin Holes", COLOR_TEXT_CYAN),
        ((5.7, -7, -20), (320, 145), "Wire Grooves", "25 mm Pitch Phase Lines", COLOR_TEXT_PURPLE)
    ]
    c3_bullets = [
        "Connects modular bay brackets into an ultra-rigid 560 mm vertical array spine.",
        "I-beam web reduces print weight while resisting gravitational sag."
    ]
    draw_card(draw, col_x[2], row_y[0], card_w, card_h,
              "03", "SPINE SEGMENT", "stl/BT4V_Spine_Segment.stl  •  20 × 14 × 120 mm  •  16,800 mm³",
              "4 REQUIRED", COLOR_TEXT_GREEN, "Inter-Bay Struts (Bays 1–2, 2–Feed, Feed–3, 3–4)",
              build_spine_segment(), cam_tall, 1.15, c3_callouts, c3_bullets)

    # --- CARD 4: PHASE CROSSOVER SPACER ---
    c4_callouts = [
        ((-8, -6, 8), (10, 38), "180° Transposition", "Dual Diagonal Wire Channels", COLOR_TEXT_BLUE),
        ((0, -2, 0), (320, 38), "Dielectric Gap", "≥5.0 mm Plastic Barrier", COLOR_TEXT_GOLD),
        ((0, 5, 0), (10, 145), "Snap Clip", "Grips Spine Strut", COLOR_TEXT_CYAN),
        ((8, 0, 8), (320, 145), "Dual-Plane Routing", "Isolated Conductor Cavities", COLOR_TEXT_PURPLE)
    ]
    c4_bullets = [
        "Inverts RF phase 180° between bay pairs for in-phase array combination.",
        "Integrated snap clip mounts securely over spine strut without screws."
    ]
    draw_card(draw, col_x[0], row_y[1], card_w, card_h,
              "04", "PHASE CROSSOVER SPACER", "stl/BT4V_Phase_Crossover.stl  •  35 × 12 × 30 mm  •  6,100 mm³",
              "2 REQUIRED", COLOR_TEXT_GREEN, "Between Bays 1–2 & Bays 3–4 (Spine Clip-On)",
              build_phase_crossover_spacer(), cam_standard, 2.15, c4_callouts, c4_bullets)

    # --- CARD 5: TRIANGULAR TINE SPREADER ---
    c5_callouts = [
        ((-33, 0, 0), (10, 38), "66 mm Snap Jaws", "Matches 25.5° VHF Flare", COLOR_TEXT_BLUE),
        ((-33, -3, 0), (320, 38), "C-Clip Lock", "2.2 mm Throat Over Wire", COLOR_TEXT_GOLD),
        ((0, 0, 0), (10, 145), "Ribbed Truss", "<3.0 g Lightweight Mass", COLOR_TEXT_CYAN),
        ((33, 0, 0), (320, 145), "Anti-Sag Geometry", "Preserves Planar Geometry", COLOR_TEXT_PURPLE)
    ]
    c5_bullets = [
        "Snaps onto extended 340 mm VHF whiskers to completely eliminate gravity droop.",
        "Forms a rigid planar triangle across upper and lower tines of Bays 1 & 4."
    ]
    draw_card(draw, col_x[1], row_y[1], card_w, card_h,
              "05", "TRIANGULAR TINE SPREADER", "stl/BT4V_Whisker_Spreader.stl  •  72 × 12 × 8 mm  •  2,200 mm³",
              "4 REQUIRED", COLOR_TEXT_GREEN, "VHF Whiskers (Bays 1 & 4) at 150 mm Radius",
              build_triangular_tine_spreader(), cam_flat, 2.05, c5_callouts, c5_bullets)

    # --- CARD 6: BOWTIE SUPPORT STRUT ---
    c6_callouts = [
        ((29.5, 0, 4), (10, 38), "Snap Jaw (C-Clip)", "2.2 mm Mouth / 3.2 mm Cavity", COLOR_TEXT_BLUE),
        ((0, 0, 4), (320, 38), "Ribbed Truss Strut", "6.0 × 3.0 mm (~2.5 g mass)", COLOR_TEXT_GOLD),
        ((-8, 0, 4), (10, 145), "Lightening Windows", "Material & Weight Reduction", COLOR_TEXT_CYAN),
        ((-20, 0, 4), (320, 145), "Bracket Base", "Locks into Bay Bracket Pocket", COLOR_TEXT_PURPLE)
    ]
    c6_bullets = [
        "Bridges between central bay bracket and intermediate points on whisker arms.",
        "Locks bowtie arms at exact flare angles (32.5° UHF, 25.5° VHF) preventing drift/sag."
    ]
    draw_card(draw, col_x[2], row_y[1], card_w, card_h,
              "06", "BOWTIE SUPPORT STRUT", "stl/BT4V_Bowtie_Support.stl  •  65 × 10 × 8 mm  •  1,800 mm³",
              "8 REQUIRED", COLOR_TEXT_GREEN, "Mid-Span Whisker Brackets to Arms (Bays 1–4)",
              build_bowtie_support_mesh(), cam_standard, 2.10, c6_callouts, c6_bullets)

    # --- CARD 7: TOP HANGING CAP ---
    c7_callouts = [
        ((-15, 0, 9), (10, 38), "Dual Ø5.0 mm Eyelets", "30.0 mm C-to-C Spacing", COLOR_TEXT_BLUE),
        ((0, 0, 8), (320, 38), "Anti-Rotation Yoke", "Prevents Twisting on Window", COLOR_TEXT_GOLD),
        ((0, 0, -10), (10, 145), "Female Mortise", "Mates to Bay 1 Tenon", COLOR_TEXT_CYAN),
        ((0, -9, -10), (320, 145), "Cross-Pin Hole", "Ø2.6 mm Retention Pin", COLOR_TEXT_PURPLE)
    ]
    c7_bullets = [
        "Terminates top of antenna spine and provides dual suspension anchor points.",
        "Dual 30 mm eyelet spread eliminates twisting against window glass surfaces."
    ]
    draw_card(draw, col_x[0], row_y[2], card_w, card_h,
              "07", "TOP HANGING CAP", "stl/BT4V_Hanging_Cap.stl  •  44 × 18 × 30 mm  •  7,400 mm³",
              "1 REQUIRED", COLOR_TEXT_GREEN, "Top Spine Termination (Mates to Bay 1 Tenon)",
              build_top_hanging_cap(), cam_standard, 2.15, c7_callouts, c7_bullets)

    # --- CARD 8: FIT CALIBRATION COUPON ---
    c8_callouts = [
        ((-24, 0, 2), (10, 38), "12 AWG Friction Slots", "2.8 to 3.4 mm Test Widths", COLOR_TEXT_BLUE),
        ((-7, 0, 2), (320, 38), "Snap Cavities", "2.2 & 2.4 mm Throats", COLOR_TEXT_GOLD),
        ((9, 0, 3), (10, 155), "M4 Pocket Stack", "4.3 mm Hole & 7.2 mm Nut Hex", COLOR_TEXT_CYAN),
        ((31, -14, 5), (320, 155), "Joint & Balun Studs", "Sample Tenon & 25 mm Pitch", COLOR_TEXT_PURPLE)
    ]
    c8_bullets = [
        "CRITICAL: Print first to verify slicer extrusion tolerances before production parts.",
        "Tests wire snap retention, M4 captured hex nuts, and tenon/mortise fit."
    ]
    draw_card(draw, col_x[1], row_y[2], card_w, card_h,
              "08", "FIT CALIBRATION COUPON", "stl/BT4V_Fit_Coupon.stl  •  90 × 50 × 10 mm  •  26,500 mm³",
              "PRINT FIRST", COLOR_TEXT_GOLD, "Pre-Print Calibration & Tolerance Bench Test",
              build_fit_calibration_coupon(), cam_flat, 1.60, c8_callouts, c8_bullets)

    # --- CARD 9: MODULAR SPINE ASSEMBLY ---
    c9_callouts = [
        ((0, 0, 65), (10, 38), "Top Suspension Cap", "Hangs via Dual Ø5 mm Eyelets", COLOR_TEXT_BLUE),
        ((0, 0, 46), (320, 38), "4-Bay Bowtie Array", "VHF (1 & 4) & UHF (2 & 3)", COLOR_TEXT_GOLD),
        ((0, -5, -8), (10, 145), "Center Feed Hub", "RCA VH101R Balun at Z = 0 mm", COLOR_TEXT_CYAN),
        ((0, -4, 34), (320, 145), "Transposition Spacers", "2 × 180° Crossovers on Phase Bus", COLOR_TEXT_PURPLE)
    ]
    c9_bullets = [
        "10 modular joints locked with 2.5 mm cross-pins into a 560 mm rigid spine.",
        "Exact 130 mm bay pitch maintains optimum VHF-Hi & UHF collinear array gain."
    ]
    draw_card(draw, col_x[2], row_y[2], card_w, card_h,
              "09", "MODULAR SPINE ASSEMBLY", "Complete Antenna Backbone  •  560 mm Height  •  ~200 g Set",
              "17 PIECES TOTAL", COLOR_TEXT_PURPLE, "Full Modular Backbone & Array Architecture",
              build_spine_assembly_stack(), cam_standard, 1.15, c9_callouts, c9_bullets)

    # Save deliverable PNG
    img.save(OUTPUT_PATH, format="PNG", optimize=True)
    file_size = os.path.getsize(OUTPUT_PATH)
    print(f"Generated deliverable: {OUTPUT_PATH}")
    print(f"Image Resolution: {img.size[0]} × {img.size[1]} px")
    print(f"File Size: {file_size:,} bytes ({file_size / 1024:.1f} kB)")

    # Verification checks
    if img.size != (CANVAS_WIDTH, CANVAS_HEIGHT):
        raise ValueError(f"Canvas size mismatch: got {img.size}, expected ({CANVAS_WIDTH}, {CANVAS_HEIGHT})")
    if file_size < MIN_FILE_SIZE_BYTES:
        raise ValueError(f"File size too small: {file_size} bytes < {MIN_FILE_SIZE_BYTES} bytes")

    print("[PASS] Verification successful: 1800x800 px, >10 kB, all 8 parts + assembly rendered.")
    return True


if __name__ == "__main__":
    try:
        generate_preview()
        sys.exit(0)
    except Exception as e:
        print(f"[FAIL] Error generating preview: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
