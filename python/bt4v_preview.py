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
2. Multi-panel layout clearly showcasing all 7 printable BT4-V parts:
   - Part 1: Center Feed Hub (1 required, 40 × 24 × 70 mm, 28,500 mm³)
     Highlighting: RCA VH101R balun cradle, 25 mm feed terminals, M4 nut pockets, tenon/mortise.
   - Part 2: Whisker Bay Bracket (4 required, 50 × 18 × 40 mm, 19,200 mm³)
     Highlighting: dual flare guide (25.5° / 32.5°), apex clamping holes, phase line channels.
   - Part 3: Spine Segment (4 required, 20 × 14 × 120 mm, 16,800 mm³)
     Highlighting: I-beam profile, 110 mm active length, wire grooves, tenon/mortise interlocks.
   - Part 4: Phase Crossover Spacer (2 required, 35 × 12 × 30 mm, 6,100 mm³)
     Highlighting: dual diagonal crossing channels, snap clip, ≥5 mm dielectric separation.
   - Part 5: Triangular Tine Spreader (4 required, 72 × 12 × 8 mm, 2,200 mm³)
     Highlighting: 66 mm C-to-C snap jaws, ribbed truss (<3 g mass).
   - Part 6: Top Hanging Cap (1 required, 44 × 18 × 30 mm, 7,400 mm³)
     Highlighting: dual Ø5 mm suspension eyelets, female mortise.
   - Part 7: Fit Calibration Coupon (1 required, 90 × 50 × 10 mm, 26,500 mm³)
     Highlighting: 12 AWG friction slots, snap cavities, M4 nut pocket, tenon/mortise fit.
   - Panel 8: Modular Spine Assembly Stack (17 printed pieces total, ~200 g set)
     Highlighting: 560 mm spine array, 130 mm pitch, 10 cross-pins, balun & crossovers.
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
# 3D MODEL BUILDERS FOR THE 8 PANELS
# -----------------------------------------------------------------------------
def build_center_feed_hub() -> Mesh3D:
    """1. Center Feed Hub: 40 × 24 × 70 mm, Balun cradle, 25 mm feed posts, M4 nut pockets."""
    m = Mesh3D()
    # Main housing
    m.add_box(-20, -12, -35, 40, 24, 70, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    # Top tenon
    m.add_box(-7, -5, 35, 14, 10, 10, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    # Pin hole in tenon
    m.add_cylinder_y(0, -5.5, -4.5, 40, 1.3, sides=8, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_PLASTIC_EDGE)
    # Balun cradle cavity in front
    m.add_cavity(-13, -12.1, -18, 26, 8, 36, COLOR_CAVITY_FILL, (80, 150, 220))
    # Balun body seated inside
    m.add_box(-11, -10.5, -15, 22, 7, 30, COLOR_BALUN_BODY, COLOR_BALUN_ACCENT, bias=-10.0)
    # F-connector cylinder pointing down
    m.add_cylinder_z(0, -7, -26, -15, 4.5, sides=12, base_col=COLOR_STEEL, edge_col=(200, 215, 230), bias=-12.0)
    # Feed terminal bosses
    m.add_box(-15, -12.1, 20, 5, 4, 11, COLOR_PLASTIC_ACCENT, (130, 200, 255), bias=-2.0)
    m.add_box(10, -12.1, 20, 5, 4, 11, COLOR_PLASTIC_ACCENT, (130, 200, 255), bias=-2.0)
    # M4 studs & brass washers
    m.add_cylinder_y(-12.5, -13.5, -11.5, 25.5, 2.2, sides=10, base_col=COLOR_STEEL, edge_col=COLOR_TEXT_WHITE, bias=-12.0)
    m.add_cylinder_y(12.5, -13.5, -11.5, 25.5, 2.2, sides=10, base_col=COLOR_STEEL, edge_col=COLOR_TEXT_WHITE, bias=-12.0)
    # Copper spade lugs connecting balun to posts
    m.add_box(-13.5, -12.8, 15, 2, 1, 10.5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-13.0)
    m.add_box(11.5, -12.8, 15, 2, 1, 10.5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-13.0)
    # Vertical phase line grooves & 12 AWG copper lines
    m.add_box(-14, -12.5, -35, 3, 1.2, 70, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(11, -12.5, -35, 3, 1.2, 70, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    # Coax zip-tie strain relief slot
    m.add_cavity(-8, -12.2, -26, 16, 2, 3, COLOR_CAVITY_FILL, (70, 120, 180), bias=-8.0)
    return m


def build_whisker_bay_bracket() -> Mesh3D:
    """2. Whisker Bay Bracket: 50 × 18 × 40 mm, dual flare guides, apex clamp, phase channels."""
    m = Mesh3D()
    # Central spine body
    m.add_box(-12, -9, -20, 24, 18, 40, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    # Top tenon
    m.add_box(-7, -5, 20, 14, 10, 10, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cylinder_y(0, -5.5, -4.5, 25, 1.3, sides=8, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_PLASTIC_EDGE)
    # Left flared wing
    m.add_box(-25, -9, -15, 13, 18, 30, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    # Right flared wing
    m.add_box(12, -9, -15, 13, 18, 30, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    # Vertical phase line channels with copper wire
    m.add_box(-14, -9.5, -20, 3, 1.2, 40, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(11, -9.5, -20, 3, 1.2, 40, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    # Whisker V-wires
    m.add_box(-28, -9.6, 6, 16, 1.4, 2.5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-7.0)
    m.add_box(-28, -9.6, -8.5, 16, 1.4, 2.5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-7.0)
    m.add_box(12, -9.6, 6, 16, 1.4, 2.5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-7.0)
    m.add_box(12, -9.6, -8.5, 16, 1.4, 2.5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-7.0)
    # Apex M4 clamping bolts
    m.add_cylinder_y(-12.5, -10.5, -9.0, 0, 3.2, sides=10, base_col=COLOR_STEEL, edge_col=COLOR_TEXT_WHITE, bias=-12.0)
    m.add_cylinder_y(12.5, -10.5, -9.0, 0, 3.2, sides=10, base_col=COLOR_STEEL, edge_col=COLOR_TEXT_WHITE, bias=-12.0)
    # Mortise indicator at bottom (-Z)
    m.add_cavity(-7, -5, -20.1, 14, 10, 8, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-10.0)
    return m


def build_spine_segment() -> Mesh3D:
    """3. Spine Segment: 20 × 14 × 120 mm, I-beam cross section, 110 mm active length."""
    m = Mesh3D()
    # Front flange
    m.add_box(-10, -7, -55, 20, 2.8, 110, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    # Rear flange
    m.add_box(-10, 4.2, -55, 20, 2.8, 110, (38, 85, 145), (100, 175, 240))
    # Central web
    m.add_box(-3.5, -4.2, -55, 7, 8.4, 110, COLOR_PLASTIC_ACCENT, COLOR_PLASTIC_EDGE)
    # Top tenon
    m.add_box(-7, -5, 55, 14, 10, 10, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cylinder_y(0, -5.5, -4.5, 60, 1.3, sides=8, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_PLASTIC_EDGE)
    # Bottom cross-pin hole
    m.add_cylinder_y(0, -7.2, -6.5, -48, 1.3, sides=8, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_PLASTIC_EDGE, bias=-6.0)
    # Front parallel wire grooves & copper phase lines
    m.add_box(-8.5, -7.5, -55, 2.8, 1.2, 110, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(5.7, -7.5, -55, 2.8, 1.2, 110, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    # Intermediate stiffening ribs along web
    for rz in [-30, 0, 30]:
        m.add_box(-10, -4.2, rz - 2, 20, 8.4, 4, (44, 95, 160), COLOR_PLASTIC_EDGE, bias=-2.0)
    return m


def build_phase_crossover_spacer() -> Mesh3D:
    """4. Phase Crossover Spacer: 35 × 12 × 30 mm, dual diagonal crossing channels, snap clip."""
    m = Mesh3D()
    # Main block
    m.add_box(-17.5, -6, -15, 35, 8, 30, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    # Rear snap clip jaws
    m.add_box(-12, 2, -12, 24, 5, 24, COLOR_PLASTIC_ACCENT, (130, 200, 255))
    m.add_cavity(-8, 2.1, -12.1, 16, 5, 24.2, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-8.0)
    # Front diagonal wire channel (crosses from top-left to bottom-right)
    for i, t in enumerate([-12, -8, -4, 0, 4, 8, 12]):
        wx = -12.5 + (25.0 * (t + 12) / 24.0)
        wz = 12.0 - (24.0 * (t + 12) / 24.0)
        m.add_box(wx - 2, -6.6, wz - 2.5, 4, 1.4, 5, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-10.0)
    # Rear diagonal channel (crosses top-right to bottom-left on offset plane Y = 0)
    for i, t in enumerate([-12, -8, -4, 0, 4, 8, 12]):
        wx = 12.5 - (25.0 * (t + 12) / 24.0)
        wz = 12.0 - (24.0 * (t + 12) / 24.0)
        m.add_box(wx - 2, -0.2, wz - 2.5, 4, 1.4, 5, (200, 110, 40), (220, 140, 70), bias=-3.0)
    # Dielectric separator center ridge
    m.add_box(-16, -3.5, -14, 32, 3, 28, (52, 112, 185), (140, 210, 255), bias=-1.0)
    return m


def build_triangular_tine_spreader() -> Mesh3D:
    """5. Triangular Tine Spreader: 72 × 12 × 8 mm, 66 mm C-to-C snap jaws, ribbed truss."""
    m = Mesh3D()
    # Main horizontal beam
    m.add_box(-33, -3, -3, 66, 6, 6, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    # Top and bottom stiffener ribs
    m.add_box(-33, -1.5, 3, 66, 3, 1.5, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_box(-33, -1.5, -4.5, 66, 3, 1.5, (38, 85, 145), (100, 175, 240))
    # Left snap jaw at X = -33.0 (66 mm C-to-C)
    m.add_box(-36, -6, -4, 6, 12, 8, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cavity(-35, -3, -4.1, 4, 6, 8.2, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-6.0)
    # Copper wire passing through left jaw
    m.add_box(-34.5, -8, -1.5, 3, 16, 3, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-12.0)
    # Right snap jaw at X = +33.0
    m.add_box(30, -6, -4, 6, 12, 8, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cavity(31, -3, -4.1, 4, 6, 8.2, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-6.0)
    # Copper wire passing through right jaw
    m.add_box(31.5, -8, -1.5, 3, 16, 3, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-12.0)
    # Lightweight truss pockets along beam
    for px in [-22, -11, 0, 11, 22]:
        m.add_cavity(px - 3.5, -3.1, -1.8, 7, 2, 3.6, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-4.0)
    return m


def build_top_hanging_cap() -> Mesh3D:
    """6. Top Hanging Cap: 44 × 18 × 30 mm, dual Ø5 mm eyelets, female mortise."""
    m = Mesh3D()
    # Main base yoke
    m.add_box(-22, -9, -15, 44, 18, 18, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    # Female mortise cavity at bottom
    m.add_cavity(-7, -5, -15.1, 14, 10, 10, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-8.0)
    # Cross-pin hole through bottom
    m.add_cylinder_y(0, -9.2, -8.5, -10, 1.3, sides=8, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_PLASTIC_EDGE, bias=-5.0)
    # Left eyelet ear at X = -15.0
    m.add_box(-19, -4.5, 3, 8, 9, 12, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cylinder_y(-15, -4.6, 4.6, 9, 2.5, sides=12, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_TEXT_WHITE, bias=-10.0)
    # Right eyelet ear at X = +15.0 (30.0 mm C-to-C pitch)
    m.add_box(11, -4.5, 3, 8, 9, 12, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cylinder_y(15, -4.6, 4.6, 9, 2.5, sides=12, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_TEXT_WHITE, bias=-10.0)
    # Suspension nylon cord passing through eyelets
    m.add_box(-17, -0.8, 8, 34, 1.6, 2, (180, 220, 255), COLOR_TEXT_WHITE, bias=-14.0)
    return m


def build_fit_calibration_coupon() -> Mesh3D:
    """7. Fit Calibration Coupon: 90 × 50 × 10 mm, friction slots, snap cavities, nut pocket, joints."""
    m = Mesh3D()
    # Main test plate
    m.add_box(-45, -25, -5, 90, 50, 10, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    # Feature 1: 4 × Friction test slots (2.8, 3.0, 3.2, 3.4 mm)
    for idx, (sx, sw) in enumerate([(-36, 2.8), (-30, 3.0), (-24, 3.2), (-18, 3.4)]):
        m.add_cavity(sx - sw / 2, -18, 2.0, sw, 36, 3.1, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-6.0)
    # Test wire seated in 3.2 mm slot
    m.add_box(-24 - 1.3, -20, 2.5, 2.6, 40, 2.6, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-10.0)
    # Feature 2: 2 × Snap cavities (2.2 & 2.4 mm mouths)
    m.add_cavity(-10 - 1.1, -16, 1.5, 2.2, 32, 3.6, COLOR_CAVITY_FILL, (80, 160, 230), bias=-6.0)
    m.add_cavity(-4 - 1.2, -16, 1.5, 2.4, 32, 3.6, COLOR_CAVITY_FILL, (80, 160, 230), bias=-6.0)
    # Feature 3: M4 hardware stack: 4.3 mm hole & 7.2 mm hex nut pocket
    m.add_cylinder_z(9, 0, 1.5, 5.2, 2.2, sides=12, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_TEXT_WHITE, bias=-8.0)
    m.add_cylinder_z(9, 0, 3.2, 5.2, 4.2, sides=6, base_col=COLOR_STEEL, edge_col=COLOR_TEXT_WHITE, bias=-12.0)
    # Feature 4: Sample tenon & mortise joint test
    m.add_box(24, -14, 5, 14, 10, 8, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_cylinder_y(31, -14.2, -13.5, 9, 1.3, sides=8, base_col=COLOR_CAVITY_FILL, edge_col=COLOR_PLASTIC_EDGE)
    m.add_cavity(24, 4, 0, 14, 10, 5.1, COLOR_CAVITY_FILL, COLOR_CAVITY_EDGE, bias=-8.0)
    # Feature 5: 25.0 mm pitch balun test studs
    m.add_cylinder_z(20, -20, 5, 10, 2.5, sides=10, base_col=COLOR_PLASTIC_ACCENT, edge_col=(140, 210, 255))
    m.add_cylinder_z(45, -20, 5, 10, 2.5, sides=10, base_col=COLOR_PLASTIC_ACCENT, edge_col=(140, 210, 255))
    return m


def build_spine_assembly_stack() -> Mesh3D:
    """8. Spine Assembly & System Stack: Full 560 mm vertical array with balun, crossovers, and bays."""
    m = Mesh3D()
    # Top Hanging cap
    m.add_box(-8, -4, 62, 16, 8, 10, COLOR_PLASTIC_ACCENT, (140, 210, 255))
    m.add_box(-6, -2, 72, 3, 4, 5, COLOR_PLASTIC_ACCENT, COLOR_TEXT_WHITE)
    m.add_box(3, -2, 72, 3, 4, 5, COLOR_PLASTIC_ACCENT, COLOR_TEXT_WHITE)
    # Bay 1 (VHF)
    m.add_box(-12, -4, 46, 24, 8, 16, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-26, -4.5, 54, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-26, -4.5, 42, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, 54, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, 42, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    # Spine Segment 1 + Crossover 1
    m.add_box(-5, -3, 30, 10, 6, 16, (40, 90, 150), COLOR_PLASTIC_EDGE)
    m.add_box(-7, -4.5, 34, 14, 3, 8, COLOR_PLASTIC_ACCENT, (140, 210, 255), bias=-3.0)
    # Bay 2 (UHF)
    m.add_box(-12, -4, 14, 24, 8, 16, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-22, -4.5, 20, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-22, -4.5, 12, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, 20, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, 12, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    # Spine Segment 2
    m.add_box(-5, -3, 2, 10, 6, 12, (40, 90, 150), COLOR_PLASTIC_EDGE)
    # Center Feed Hub at center (Z = -14..+2)
    m.add_box(-10, -5, -14, 20, 10, 16, (52, 115, 185), (140, 210, 255), bias=-2.0)
    m.add_box(-6, -5.5, -11, 12, 4, 10, COLOR_BALUN_BODY, COLOR_BALUN_ACCENT, bias=-6.0)
    # F-connector
    m.add_cylinder_z(0, -3.5, -18, -14, 2.5, sides=8, base_col=COLOR_STEEL, edge_col=COLOR_TEXT_WHITE, bias=-8.0)
    # Spine Segment 3
    m.add_box(-5, -3, -26, 10, 6, 12, (40, 90, 150), COLOR_PLASTIC_EDGE)
    # Bay 3 (UHF)
    m.add_box(-12, -4, -42, 24, 8, 16, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-22, -4.5, -36, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-22, -4.5, -44, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, -36, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, -44, 10, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    # Spine Segment 4 + Crossover 2
    m.add_box(-5, -3, -58, 10, 6, 16, (40, 90, 150), COLOR_PLASTIC_EDGE)
    m.add_box(-7, -4.5, -54, 14, 3, 8, COLOR_PLASTIC_ACCENT, (140, 210, 255), bias=-3.0)
    # Bay 4 (VHF)
    m.add_box(-12, -4, -74, 24, 8, 16, COLOR_PLASTIC_BASE, COLOR_PLASTIC_EDGE)
    m.add_box(-26, -4.5, -66, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(-26, -4.5, -78, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, -66, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    m.add_box(12, -4.5, -78, 14, 1, 2, COLOR_COPPER, COLOR_COPPER_EDGE, bias=-5.0)
    # Continuous vertical copper phase lines
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
    bw = max(tw, sw) + 10
    bh = th + sh + 7

    # Anchor dot at feature
    draw.ellipse([(tx - 2.5, ty - 2.5), (tx + 2.5, ty + 2.5)], fill=color, outline=COLOR_TEXT_WHITE)
    # Leader line to box center
    cx = bx + bw / 2
    cy = by + bh / 2
    draw.line([(tx, ty), (cx, cy)], fill=color, width=1)
    # Rounded badge pill
    draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=3, fill=(18, 24, 32), outline=color, width=1)
    draw.text((bx + 5, by + 3), text, fill=COLOR_TEXT_WHITE, font=FONT_CALLOUT)
    if subtext:
        draw.text((bx + 5, by + 3 + th + 2), subtext, fill=COLOR_TEXT_MUTED, font=FONT_CALLOUT_SUB)


def draw_card(draw: ImageDraw.ImageDraw, x0: int, y0: int, width: int, height: int,
              part_num: str, title: str, subtitle: str, qty_text: str, qty_color: tuple,
              location_str: str, mesh: Mesh3D, camera: Camera, mesh_scale: float,
              callouts: list, footer_bullets: list):
    """Draws a complete component card with header, badges, 3D viewport, and footer specs."""
    x1 = x0 + width
    y1 = y0 + height

    # 1. Main Container
    draw.rounded_rectangle([(x0, y0), (x1, y1)], radius=6, fill=COLOR_CARD_BG, outline=COLOR_CARD_BORDER, width=1)

    # 2. Card Header
    hdr_h = 36
    draw.rounded_rectangle([(x0, y0), (x1, y0 + hdr_h)], radius=6, fill=COLOR_CARD_HDR)
    draw.rectangle([(x0, y0 + hdr_h - 6), (x1, y0 + hdr_h)], fill=COLOR_CARD_HDR)
    draw.line([(x0, y0 + hdr_h), (x1, y0 + hdr_h)], fill=COLOR_CARD_BORDER, width=1)

    # Title & Subtitle
    draw.text((x0 + 10, y0 + 5), f"{part_num}. {title}", fill=COLOR_TEXT_WHITE, font=FONT_CARD_TITLE)
    draw.text((x0 + 10, y0 + 20), subtitle, fill=COLOR_TEXT_CYAN, font=FONT_CARD_METRIC)

    # Qty Badge Pill (Top Right)
    q_box = FONT_BADGE.getbbox(qty_text)
    qw = q_box[2] - q_box[0] + 12
    qh = q_box[3] - q_box[1] + 6
    qx = x1 - qw - 10
    qy = y0 + 7
    draw.rounded_rectangle([(qx, qy), (qx + qw, qy + qh)], radius=4, fill=(18, 25, 33), outline=qty_color, width=1)
    draw.text((qx + 6, qy + 2), qty_text, fill=qty_color, font=FONT_BADGE)

    # 3. Location Strip
    loc_h = 20
    loc_y = y0 + hdr_h
    draw.rectangle([(x0, loc_y), (x1, loc_y + loc_h)], fill=COLOR_CARD_STRIP)
    draw.line([(x0, loc_y + loc_h), (x1, loc_y + loc_h)], fill=COLOR_CARD_BORDER, width=1)

    loc_lbl = "LOCATION:"
    lbl_box = FONT_LOC_LABEL.getbbox(loc_lbl)
    lbl_w = lbl_box[2] - lbl_box[0]
    draw.text((x0 + 10, loc_y + 4), loc_lbl, fill=COLOR_TEXT_GOLD, font=FONT_LOC_LABEL)
    draw.text((x0 + 14 + lbl_w, loc_y + 4), location_str, fill=COLOR_TEXT_WHITE, font=FONT_LOC_VALUE)

    # 4. 3D Mesh Viewport
    view_cy = y0 + hdr_h + loc_h + 100
    view_cx = x0 + width / 2
    mesh.render(draw, camera, view_cx, view_cy, mesh_scale)

    # 5. Callouts
    for callout in callouts:
        t3d, (rbx, rby), c_title, c_sub, c_col = callout
        tu, tv, _ = camera.project(t3d[0], t3d[1], t3d[2], view_cx, view_cy, mesh_scale)
        bx = x0 + rbx
        by = y0 + rby
        draw_callout_pill(draw, tu, tv, bx, by, c_title, c_sub, color=c_col)

    # 6. Technical Specifications Footer
    ftr_h = 60
    ftr_y = y1 - ftr_h
    draw.rectangle([(x0, ftr_y), (x1, y1)], fill=COLOR_CARD_HDR)
    draw.line([(x0, ftr_y), (x1, ftr_y)], fill=COLOR_CARD_BORDER, width=1)
    draw.text((x0 + 10, ftr_y + 5), "KEY TECHNICAL & FABRICATION SPECIFICATIONS:", fill=COLOR_TEXT_CYAN, font=FONT_FOOTER_HDR)

    line_y = ftr_y + 19
    for bullet in footer_bullets:
        draw.text((x0 + 10, line_y), "•", fill=COLOR_TEXT_BLUE, font=FONT_FOOTER_HDR)
        draw.text((x0 + 20, line_y), bullet, fill=COLOR_TEXT_MUTED, font=FONT_FOOTER_TXT)
        line_y += 13


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
    draw.rectangle([(16, 8), (CANVAS_WIDTH - 16, 56)], fill=COLOR_BANNER_BG, outline=COLOR_CARD_BORDER, width=1)
    draw.text((28, 14), "BT4-V 3D PRINTED ANTENNA — 3D PRINTABLE PARTS PREVIEW", fill=COLOR_TEXT_WHITE, font=FONT_TITLE)
    draw.text((28, 36), "Revision v0.1.0  |  Total Print Mass ~200 g (PETG/PLA)  |  7 Modular Components  |  100% FreeCAD CSG Parametric Models",
              fill=COLOR_TEXT_CYAN, font=FONT_SUBTITLE)

    # Top Right Badges
    badges = [
        ("REVISION v0.1.0", COLOR_TEXT_GOLD),
        ("7 PRINTABLE PARTS", COLOR_TEXT_GREEN),
        ("ASME Y14.5M CAD", COLOR_TEXT_BLUE)
    ]
    bx = CANVAS_WIDTH - 28
    for b_text, b_col in reversed(badges):
        bb = FONT_BADGE.getbbox(b_text)
        bw = bb[2] - bb[0] + 14
        bh = bb[3] - bb[1] + 8
        bx -= bw
        draw.rounded_rectangle([(bx, 18), (bx + bw, 18 + bh)], radius=4, fill=(18, 25, 33), outline=b_col, width=1)
        draw.text((bx + 7, 21), b_text, fill=b_col, font=FONT_BADGE)
        bx -= 10

    # 2. Bottom Print Settings Summary Banner
    b_top = 744
    draw.rectangle([(16, b_top), (CANVAS_WIDTH - 16, 792)], fill=COLOR_BANNER_BG, outline=COLOR_CARD_BORDER, width=1)
    draw.text((26, b_top + 5), "RECOMMENDED 3D PRINT SPECIFICATIONS & FABRICATION GUIDELINES:", fill=COLOR_TEXT_GOLD, font=FONT_BANNER_HDR)
    draw.text((26, b_top + 20),
              "• Material: PETG (recommended for UV/outdoor durability) or UV-stable PLA   • Layer Height: 0.20 mm   • Perimeters: 3–4 Walls (≥1.2 mm shell)   • Infill: 25–30% Gyroid or Grid   • Solid Layers: 4 Top / 4 Bottom",
              fill=COLOR_TEXT_MUTED, font=FONT_BANNER_TXT)
    draw.text((26, b_top + 33),
              "• Print Orientation: Flat on bed (0 supports required across all parts)   • Nozzle: 0.40 mm   • Bed Compatibility: Fits standard 220×220 or 235×235 mm build plates   • Total Antenna BOM: 17 pieces (~200 g)",
              fill=COLOR_TEXT_CYAN, font=FONT_BANNER_TXT)

    # Camera Instances
    cam_standard = Camera(eye=(85.0, -110.0, 75.0), target=(0.0, 0.0, 0.0))
    cam_flat = Camera(eye=(70.0, -90.0, 110.0), target=(0.0, 0.0, 0.0))
    cam_tall = Camera(eye=(100.0, -120.0, 50.0), target=(0.0, 0.0, 0.0))

    # Cards Geometry Setup (4 Columns × 2 Rows)
    card_w = 433
    card_h = 331
    col_x = [16, 461, 906, 1351]
    row_y = [64, 405]

    # --- CARD 1: CENTER FEED HUB ---
    c1_callouts = [
        ((0, -12, 0), (10, 60), "RCA VH101R Cradle", "Contoured 300:75Ω Balun Cavity", COLOR_TEXT_BLUE),
        ((-12.5, -12, 24), (255, 60), "25 mm Feed Posts", "M4 Studs & Brass Spade Terminals", COLOR_TEXT_GOLD),
        ((0, 0, 40), (10, 208), "Spine Joint System", "+Z Tenon & -Z Mortise (Ø2.6 mm Pin)", COLOR_TEXT_CYAN),
        ((0, -12, -26), (255, 208), "Coax Strain Relief", "4.0 × 2.0 mm Zip-Tie Loop Slot", COLOR_TEXT_PURPLE)
    ]
    c1_bullets = [
        "Houses commercial RCA VH101R balun directly between Bay 2 and Bay 3.",
        "25 mm feed terminals mate with 12 AWG copper phase lines and balun spade lugs.",
        "Captive M4 hex nut pockets eliminate loose hardware during spine assembly."
    ]
    draw_card(draw, col_x[0], row_y[0], card_w, card_h,
              "01", "CENTER FEED HUB", "stl/BT4V_Center_Feed.stl  •  40 × 24 × 70 mm  •  28,500 mm³",
              "1 REQUIRED", COLOR_TEXT_GREEN, "Spine Center — Between Bay 2 & Bay 3 (Z = 0 mm)",
              build_center_feed_hub(), cam_standard, 1.65, c1_callouts, c1_bullets)

    # --- CARD 2: WHISKER BAY BRACKET ---
    c2_callouts = [
        ((-20, -9, 8), (10, 60), "Dual Flare Guides", "Molded 25.5° VHF & 32.5° UHF V-Slots", COLOR_TEXT_BLUE),
        ((-12.5, -10, 0), (255, 60), "Apex Clamping Ports", "2 × M4 Bolt Holes with Nut Pockets", COLOR_TEXT_GOLD),
        ((0, 0, 25), (10, 208), "Modular Spine Tenon", "14 × 10 × 10 mm Symmetrical Interlock", COLOR_TEXT_CYAN),
        ((11, -9, -10), (255, 208), "Phase Line Channels", "Dual 3.2 × 3.0 mm Wire Routing Grooves", COLOR_TEXT_PURPLE)
    ]
    c2_bullets = [
        "Universal whisker mount for all 4 bays (supports VHF 25.5° and UHF 32.5° flare).",
        "Clamps whisker apex and vertical phase line together via M4 bolts and captive nuts.",
        "Symmetrical top tenon and bottom mortise maintain strict vertical spine alignment."
    ]
    draw_card(draw, col_x[1], row_y[0], card_w, card_h,
              "02", "WHISKER BAY BRACKET", "stl/BT4V_Bay_Bracket.stl  •  50 × 18 × 40 mm  •  19,200 mm³",
              "4 REQUIRED", COLOR_TEXT_GREEN, "Bays 1, 2, 3, & 4 (130 mm Array Pitch)",
              build_whisker_bay_bracket(), cam_standard, 2.05, c2_callouts, c2_bullets)

    # --- CARD 3: SPINE SEGMENT ---
    c3_callouts = [
        ((-10, 0, 15), (10, 60), "I-Beam Cross-Section", "Rigid Flanges Maximize Bending Stiffness", COLOR_TEXT_BLUE),
        ((0, 0, 0), (265, 60), "110 mm Active Length", "Spaces Adjacent Bays at Exact 130 mm Pitch", COLOR_TEXT_GOLD),
        ((0, 0, 60), (10, 208), "Interlocking Tenon/Mortise", "2.6 mm Cross-Pin Locking Alignment Holes", COLOR_TEXT_CYAN),
        ((5.7, -7, -20), (265, 208), "Parallel Wire Grooves", "25 mm Pitch 12 AWG Phase Line Seating", COLOR_TEXT_PURPLE)
    ]
    c3_bullets = [
        "Connects modular bay brackets into an ultra-rigid 560 mm vertical array spine.",
        "Engineered I-beam web reduces print weight while resisting window gravitational sag.",
        "Prints flat without supports; 100% bed compatible with 220×220 mm build plates."
    ]
    draw_card(draw, col_x[2], row_y[0], card_w, card_h,
              "03", "SPINE SEGMENT", "stl/BT4V_Spine_Segment.stl  •  20 × 14 × 120 mm  •  16,800 mm³",
              "4 REQUIRED", COLOR_TEXT_GREEN, "Inter-Bay Struts (Bays 1–2, 2–Feed, Feed–3, 3–4)",
              build_spine_segment(), cam_tall, 1.35, c3_callouts, c3_bullets)

    # --- CARD 4: PHASE CROSSOVER SPACER ---
    c4_callouts = [
        ((-8, -6, 8), (10, 60), "180° Transposition", "Dual Diagonal Crossing Wire Channels", COLOR_TEXT_BLUE),
        ((0, -2, 0), (255, 60), "Dielectric Separation", "≥5.0 mm Plastic Barrier Prevents Arcing", COLOR_TEXT_GOLD),
        ((0, 5, 0), (10, 208), "Strut Snap-Fit Clip", "2.4 mm Retaining Mouth Grips Spine Beam", COLOR_TEXT_CYAN),
        ((8, 0, 8), (255, 208), "Dual-Plane Routing", "Front / Rear Isolated Conductor Cavities", COLOR_TEXT_PURPLE)
    ]
    c4_bullets = [
        "Inverts RF phase 180° between Bay pairs (1–2 and 3–4) for in-phase array combination.",
        "Integrated snap clip mounts securely over spine strut without screws or adhesives.",
        "Guarantees minimum 5.0 mm dielectric spacing between 12 AWG phase conductors."
    ]
    draw_card(draw, col_x[3], row_y[0], card_w, card_h,
              "04", "PHASE CROSSOVER SPACER", "stl/BT4V_Phase_Crossover.stl  •  35 × 12 × 30 mm  •  6,100 mm³",
              "2 REQUIRED", COLOR_TEXT_GREEN, "Between Bays 1–2 & Bays 3–4 (Spine Clip-On)",
              build_phase_crossover_spacer(), cam_standard, 2.50, c4_callouts, c4_bullets)

    # --- CARD 5: TRIANGULAR TINE SPREADER ---
    c5_callouts = [
        ((-33, 0, 0), (10, 60), "66 mm Snap Jaws", "Matches 25.5° VHF Flare at 150 mm Radius", COLOR_TEXT_BLUE),
        ((-33, -3, 0), (255, 60), "C-Clip Wire Lock", "2.2 mm Throat Over 3.2 mm Wire Cavity", COLOR_TEXT_GOLD),
        ((0, 0, 0), (10, 208), "Ribbed Truss Section", "High Rigidity Structure (<3.0 g Mass)", COLOR_TEXT_CYAN),
        ((33, 0, 0), (255, 208), "Anti-Droop Geometry", "Preserves True Planar VHF Bowtie Geometry", COLOR_TEXT_PURPLE)
    ]
    c5_bullets = [
        "Snaps onto extended 340 mm VHF whiskers to completely eliminate gravity droop.",
        "Forms a rigid planar triangle across upper and lower tines of Bays 1 and 4.",
        "Tool-free friction clip installation requires no hardware or glue."
    ]
    draw_card(draw, col_x[0], row_y[1], card_w, card_h,
              "05", "TRIANGULAR TINE SPREADER", "stl/BT4V_Whisker_Spreader.stl  •  72 × 12 × 8 mm  •  2,200 mm³",
              "4 REQUIRED", COLOR_TEXT_GREEN, "VHF Whiskers (Bays 1 & 4) at 150 mm Radius",
              build_triangular_tine_spreader(), cam_flat, 2.30, c5_callouts, c5_bullets)

    # --- CARD 6: TOP HANGING CAP ---
    c6_callouts = [
        ((-15, 0, 9), (10, 60), "Dual Ø5.0 mm Eyelets", "30.0 mm C-to-C Suspension Spacing", COLOR_TEXT_BLUE),
        ((0, 0, 8), (255, 60), "Anti-Rotation Yoke", "Prevents Twisting When Suspended on Window", COLOR_TEXT_GOLD),
        ((0, 0, -10), (10, 208), "Female Mortise Joint", "Internal Cavity Mates to Bay 1 Top Tenon", COLOR_TEXT_CYAN),
        ((0, -9, -10), (255, 208), "Cross-Pin Locking Hole", "2.6 mm Hole for Permanent Retention Pin", COLOR_TEXT_PURPLE)
    ]
    c6_bullets = [
        "Terminates top of antenna spine and provides dual suspension anchor points.",
        "Dual 30 mm eyelet spread eliminates twisting against window glass surfaces.",
        "Accommodates nylon hanging cord, stainless picture wire, or window suction hooks."
    ]
    draw_card(draw, col_x[1], row_y[1], card_w, card_h,
              "06", "TOP HANGING CAP", "stl/BT4V_Hanging_Cap.stl  •  44 × 18 × 30 mm  •  7,400 mm³",
              "1 REQUIRED", COLOR_TEXT_GREEN, "Top Spine Termination (Mates to Bay 1 Tenon)",
              build_top_hanging_cap(), cam_standard, 2.50, c6_callouts, c6_bullets)

    # --- CARD 7: FIT CALIBRATION COUPON ---
    c7_callouts = [
        ((-24, 0, 2), (10, 60), "12 AWG Friction Channels", "2.8, 3.0, 3.2, 3.4 mm Test Fit Widths", COLOR_TEXT_BLUE),
        ((-7, 0, 2), (255, 60), "Snap Retention Cavities", "2.2 & 2.4 mm Throats Over 3.3 mm Round", COLOR_TEXT_GOLD),
        ((9, 0, 3), (10, 208), "M4 Pocket Stack", "4.3 mm Clearance Hole & 7.2 mm Nut Hex", COLOR_TEXT_CYAN),
        ((31, -14, 5), (255, 208), "Joint & Balun Studs", "Sample Tenon/Mortise & 25 mm Balun Pitch", COLOR_TEXT_PURPLE)
    ]
    c7_bullets = [
        "CRITICAL: Print first to verify slicer extrusion tolerances before production parts.",
        "Tests 12 AWG wire snap retention, M4 captured hex nuts, and tenon/mortise fit.",
        "Prevents wasted filament by guaranteeing 100% first-pass assembly success."
    ]
    draw_card(draw, col_x[2], row_y[1], card_w, card_h,
              "07", "FIT CALIBRATION COUPON", "stl/BT4V_Fit_Coupon.stl  •  90 × 50 × 10 mm  •  26,500 mm³",
              "PRINT FIRST", COLOR_TEXT_GOLD, "Pre-Print Calibration & Tolerance Bench Test",
              build_fit_calibration_coupon(), cam_flat, 1.85, c7_callouts, c7_bullets)

    # --- CARD 8: MODULAR SPINE ASSEMBLY STACK ---
    c8_callouts = [
        ((0, 0, 65), (10, 60), "Top Suspension Cap", "Hangs on Window via Dual Ø5 mm Eyelets", COLOR_TEXT_BLUE),
        ((0, 0, 46), (255, 60), "4-Bay Bowtie Array", "Bays 1 & 4 (VHF), Bays 2 & 3 (UHF)", COLOR_TEXT_GOLD),
        ((0, -5, -8), (10, 208), "Center Balun Feed Hub", "RCA VH101R 4:1 Matching Unit at Z = 0 mm", COLOR_TEXT_CYAN),
        ((0, -4, 34), (255, 208), "Transposition Spacers", "2 × 180° Phase Crossovers on 12 AWG Lines", COLOR_TEXT_PURPLE)
    ]
    c8_bullets = [
        "10 modular joints locked with 2.5 mm cross-pins (or M2.5 screws) into a 560 mm spine.",
        "Exact 130 mm bay pitch maintains optimum VHF-Hi & UHF collinear array gain.",
        "Complete 3D printed bill of materials: 17 pieces total, ~200 g print mass."
    ]
    draw_card(draw, col_x[3], row_y[1], card_w, card_h,
              "08", "MODULAR SPINE ASSEMBLY", "Complete Antenna Backbone  •  560 mm Height  •  ~200 g Set",
              "17 PIECES TOTAL", COLOR_TEXT_PURPLE, "Full Modular Backbone & Array Architecture",
              build_spine_assembly_stack(), cam_standard, 1.35, c8_callouts, c8_bullets)

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

    print("[PASS] Verification successful: 1800x800 px, >10 kB, all 7 parts + assembly rendered.")
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
