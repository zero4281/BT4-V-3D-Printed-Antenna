#!/usr/bin/env bash
# ==============================================================================
# BT4-V 3D Printed Antenna — Headless Master Build Orchestrator
#
# Generates all 8 STL assets and 2 PNG deliverables in strict
# sequence, enforcing solid validity and geometry constraints per
# Requirements.md (§13, §16.3) and Plan.md (§3.1, T1.4).
#
# Usage:
#   ./bt4v_generate_all.sh
# or:
#   FREECAD_CMD=/snap/bin/freecad.cmd ./bt4v_generate_all.sh
# or:
#   FREECAD_CMD=freecadcmd ./bt4v_generate_all.sh
# ==============================================================================

set -euo pipefail

# Self-resolve script directory
cd "$(dirname "$0")"

# Ensure output directory exists
mkdir -p stl

# ------------------------------------------------------------------------------
# Dynamic FreeCAD Binary Resolution
# ------------------------------------------------------------------------------
if [ -n "${FREECAD_CMD:-}" ]; then
    # Respect user-specified FREECAD_CMD
    if ! command -v "$FREECAD_CMD" >/dev/null 2>&1 && [ ! -x "$FREECAD_CMD" ]; then
        echo "ERROR: Specified FREECAD_CMD not found or not executable: $FREECAD_CMD" >&2
        exit 1
    fi
else
    # Auto-detect FreeCAD binary in PATH, then snap location
    if command -v freecadcmd >/dev/null 2>&1; then
        FREECAD_CMD="freecadcmd"
    elif [ -x /snap/bin/freecad.cmd ]; then
        FREECAD_CMD="/snap/bin/freecad.cmd"
    elif command -v freecad.cmd >/dev/null 2>&1; then
        FREECAD_CMD="$(command -v freecad.cmd)"
    else
        echo "ERROR: FreeCAD binary not found. Please install FreeCAD or set FREECAD_CMD." >&2
        exit 1
    fi
fi

PYTHON_CMD="${PYTHON_CMD:-python3}"
if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
    echo "ERROR: Python interpreter '$PYTHON_CMD' not found in PATH." >&2
    exit 1
fi

echo "================================================================================"
echo "BT4-V Master Build Orchestrator"
echo "FreeCAD binary : $FREECAD_CMD"
echo "Python binary  : $PYTHON_CMD"
echo "Workspace root : $(pwd)"
echo "================================================================================"

# ------------------------------------------------------------------------------
# Validation Function
# ------------------------------------------------------------------------------
require_output() {
    local target="$1"
    if [ ! -s "$target" ]; then
        echo "ERROR: Expected output artifact '$target' is missing or empty." >&2
        exit 1
    fi
}

# ------------------------------------------------------------------------------
# Step 1: Run 7 FreeCAD Parametric CAD Generators
# ------------------------------------------------------------------------------
CAD_GENERATORS=(
    "python/bt4v_center_feed.py:stl/BT4V_Center_Feed.stl"
    "python/bt4v_bay_bracket.py:stl/BT4V_Bay_Bracket.stl"
    "python/bt4v_spine_segment.py:stl/BT4V_Spine_Segment.stl"
    "python/bt4v_phase_crossover.py:stl/BT4V_Phase_Crossover.stl"
    "python/bt4v_hanging_cap.py:stl/BT4V_Hanging_Cap.stl"
    "python/bt4v_fit_coupon.py:stl/BT4V_Fit_Coupon.stl"
    "python/bt4v_bowtie_backing.py:stl/BT4V_Bowtie_Backing.stl"
)

for entry in "${CAD_GENERATORS[@]}"; do
    script="${entry%%:*}"
    target="${entry##*:}"
    echo ""
    echo "--------------------------------------------------------------------------------"
    echo "Executing CAD Generator: $script -> $target"
    echo "--------------------------------------------------------------------------------"
    rm -f "$target"
    "$FREECAD_CMD" "$script"
    require_output "$target"
    size=$(stat -c %s "$target")
    echo "Generated: $target ($size bytes)"
done

# ------------------------------------------------------------------------------
# Step 2: Run 2 Pillow Graphics Generators
# ------------------------------------------------------------------------------
GRAPHICS_GENERATORS=(
    "python/bt4v_drawing.py:BT4-V 2D Drawing.png"
    "python/bt4v_preview.py:BT4-V Parts Preview.png"
)

for entry in "${GRAPHICS_GENERATORS[@]}"; do
    script="${entry%%:*}"
    target="${entry##*:}"
    echo ""
    echo "--------------------------------------------------------------------------------"
    echo "Executing Graphics Generator: $script -> $target"
    echo "--------------------------------------------------------------------------------"
    rm -f "$target"
    "$PYTHON_CMD" "$script"
    require_output "$target"
    size=$(stat -c %s "$target")
    echo "Generated: $target ($size bytes)"
done

# ------------------------------------------------------------------------------
# Step 3: Terminal Confirmation & Artifact Summary
# ------------------------------------------------------------------------------
echo ""
echo "================================================================================"
echo "BT4-V Build Summary: All 9 artifacts generated successfully"
echo "================================================================================"
ARTIFACTS=(
    "stl/BT4V_Center_Feed.stl"
    "stl/BT4V_Bay_Bracket.stl"
    "stl/BT4V_Spine_Segment.stl"
    "stl/BT4V_Phase_Crossover.stl"
    "stl/BT4V_Hanging_Cap.stl"
    "stl/BT4V_Fit_Coupon.stl"
    "stl/BT4V_Bowtie_Backing.stl"
    "BT4-V 2D Drawing.png"
    "BT4-V Parts Preview.png"
)

for artifact in "${ARTIFACTS[@]}"; do
    require_output "$artifact"
    size=$(stat -c %s "$artifact")
    printf "  %-32s : %8d bytes\n" "$artifact" "$size"
done
echo "================================================================================"
echo "Done."
