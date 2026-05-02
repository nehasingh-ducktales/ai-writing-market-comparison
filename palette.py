"""
Central colour palette for all FirstGammaClaude charts.
Import this in any chart script to keep visuals consistent.
"""

from matplotlib.colors import LinearSegmentedColormap

# ── Competitor brand colours ──────────────────────────────────────────────────
BRAND = {
    "Notion AI":  "#3D3D3D",   # charcoal
    "Jasper":     "#D4622A",   # warm terracotta
    "Copy.ai":    "#6047B8",   # muted indigo
    "Writesonic": "#2A9D74",   # soft teal
}

# ── Heatmap: soothing 3-stop gradient ────────────────────────────────────────
# No → soft peach  |  Partial → warm cream  |  Yes → soft mint
HEATMAP_STOPS = ["#FADADD", "#FFF3CD", "#C8EFE0"]

HEATMAP_CMAP = LinearSegmentedColormap.from_list(
    "soothing", HEATMAP_STOPS, N=256
)

# Text colour printed inside each heatmap cell — dark enough to read on pastels
CELL_TEXT_COLOR = {
    0:   "#8B2E20",   # dark rust on peach
    0.5: "#7A5200",   # dark amber on cream
    1:   "#1A5C3A",   # dark forest on mint
}

CELL_LABEL = {0: "No", 0.5: "Partial", 1: "Yes"}

# ── General chart chrome ──────────────────────────────────────────────────────
FOOTNOTE = "#999999"
SPINE    = "#DDDDDD"
GRIDLINE = "#EEEEEE"
