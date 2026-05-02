"""Generate competitive analysis charts from competitors.csv and analysis.md."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

from palette import BRAND, HEATMAP_CMAP, CELL_TEXT_COLOR, CELL_LABEL, FOOTNOTE

OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

COLORS = BRAND   # alias — charts reference COLORS throughout
TOOLS = ["Notion AI", "Jasper", "Copy.ai", "Writesonic"]

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# ─────────────────────────────────────────────────────────────────────────────
# Chart 1 — Pricing Comparison (grouped: entry vs mid-tier, annual)
# ─────────────────────────────────────────────────────────────────────────────

entry_prices = {"Notion AI": 0,  "Jasper": 59,  "Copy.ai": 24,  "Writesonic": 79}
mid_prices   = {"Notion AI": None, "Jasper": None, "Copy.ai": 1000, "Writesonic": 199}
entry_labels = {"Notion AI": "Free",    "Jasper": "Pro $59",  "Copy.ai": "Chat $24",    "Writesonic": "Starter $79"}
mid_labels   = {"Notion AI": "Undisclosed", "Jasper": "Custom",   "Copy.ai": "Growth $1,000", "Writesonic": "Basic $199"}

fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(TOOLS))
bar_w = 0.35

entry_bars = ax.bar(
    x - bar_w / 2,
    [entry_prices[t] for t in TOOLS],
    width=bar_w,
    label="Entry-level tier (annual)",
    color=[COLORS[t] for t in TOOLS],
    alpha=0.9,
    edgecolor="white",
)
mid_vals = [mid_prices[t] if mid_prices[t] is not None else 0 for t in TOOLS]
mid_bars = ax.bar(
    x + bar_w / 2,
    mid_vals,
    width=bar_w,
    label="Mid-tier (annual)",
    color=[COLORS[t] for t in TOOLS],
    alpha=0.45,
    edgecolor="white",
    hatch="///",
)

# Value labels on entry bars
for bar, tool in zip(entry_bars, TOOLS):
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        h + 12,
        entry_labels[tool],
        ha="center", va="bottom", fontsize=8.5, fontweight="bold",
    )

# Value labels on mid bars
for bar, tool in zip(mid_bars, TOOLS):
    h = bar.get_height()
    label = mid_labels[tool]
    if h == 0:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            18,
            label,
            ha="center", va="bottom", fontsize=7.5, color="gray", style="italic",
        )
    else:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + 12,
            label,
            ha="center", va="bottom", fontsize=8.5,
        )

ax.set_xticks(x)
ax.set_xticklabels(TOOLS, fontsize=11, fontweight="bold")
ax.set_ylabel("Price per month, USD (annual billing)", fontsize=10)
ax.set_title(
    "Pricing Comparison: Entry vs Mid-Tier (Published Annual Prices)",
    fontsize=13, fontweight="bold", pad=16,
)
ax.set_ylim(0, 1200)
ax.legend(fontsize=9, loc="upper left")
ax.text(
    0.99, 0.97,
    "Jasper/Notion mid-tier is custom pricing (contact sales)\nCopy.ai has no monthly-billing option above Chat",
    transform=ax.transAxes, ha="right", va="top", fontsize=7.5, color="gray", style="italic",
)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pricing_comparison.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved pricing_comparison.png")

# ─────────────────────────────────────────────────────────────────────────────
# Chart 2 — Feature Coverage Heatmap
# ─────────────────────────────────────────────────────────────────────────────

features = [
    "AI Writing / Generation",
    "Multi-model Access",
    "Brand Voice Management",
    "Agentic Workflows",
    "SEO / AI Search Visibility",
    "Image Generation",
    "Workspace / Notes / DB",
    "Plagiarism Checker",
    "API / Developer Access",
    "Transparent Self-serve Pricing",
]

# Rows = features, Cols = tools  (1=yes, 0.5=partial, 0=no)
matrix = np.array([
    [1,   1,   1,   1  ],  # AI Writing
    [0,   0,   1,   0  ],  # Multi-model
    [0,   1,   0,   0  ],  # Brand Voice
    [1,   1,   1,   0  ],  # Agentic
    [0,   0,   0,   1  ],  # SEO
    [0,   1,   0,   0  ],  # Image Gen
    [1,   0,   0,   0  ],  # Workspace
    [0,   1,   0,   0  ],  # Plagiarism
    [0.5, 0.5, 0.5, 0  ],  # API
    [0.5, 1,   0.5, 1  ],  # Transparent pricing
])

fig, ax = plt.subplots(figsize=(9, 7))

im = ax.imshow(matrix.T, cmap=HEATMAP_CMAP, aspect="auto", vmin=0, vmax=1)

ax.set_xticks(range(len(features)))
ax.set_xticklabels(features, rotation=38, ha="right", fontsize=9)
ax.set_yticks(range(len(TOOLS)))
ax.set_yticklabels(TOOLS, fontsize=11, fontweight="bold")

for i in range(len(features)):
    for j in range(len(TOOLS)):
        val = matrix[i, j]
        ax.text(
            i, j, CELL_LABEL[val],
            ha="center", va="center",
            fontsize=8.5, fontweight="bold",
            color=CELL_TEXT_COLOR[val],
        )

ax.set_title("Feature Coverage Heatmap", fontsize=13, fontweight="bold", pad=16)

cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
cbar.set_ticks([0, 0.5, 1])
cbar.set_ticklabels(["No", "Partial", "Yes"], fontsize=9)
cbar.ax.tick_params(labelcolor="#444444")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "feature_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved feature_heatmap.png")

# ─────────────────────────────────────────────────────────────────────────────
# Chart 3 — Positioning Map: Price vs Feature Richness
# ─────────────────────────────────────────────────────────────────────────────

# Feature richness = column sums of matrix (out of 10)
richness = matrix.sum(axis=0)  # [Notion, Jasper, Copy.ai, Writesonic]

# Entry-level paid annual price (Notion estimated ~$15 — AI bundled in workspace plan)
pos_prices = {"Notion AI": 15, "Jasper": 59, "Copy.ai": 24, "Writesonic": 79}

fig, ax = plt.subplots(figsize=(9, 7))

# Quadrant shading
mid_x = 50
mid_y = 4.5
ax.axvspan(0,    mid_x, ymin=0, ymax=0.5, alpha=0.04, color="blue")
ax.axvspan(mid_x, 110,  ymin=0, ymax=0.5, alpha=0.04, color="red")
ax.axvspan(0,    mid_x, ymin=0.5, ymax=1, alpha=0.04, color="green")
ax.axvspan(mid_x, 110,  ymin=0.5, ymax=1, alpha=0.04, color="orange")

ax.axvline(mid_x, color="#cccccc", linestyle="--", linewidth=1.2, zorder=1)
ax.axhline(mid_y, color="#cccccc", linestyle="--", linewidth=1.2, zorder=1)

# Quadrant labels
ax.text(2,    mid_y + 0.15, "Affordable &\nFeature-rich",  fontsize=8, color="#555", style="italic")
ax.text(mid_x + 2, mid_y + 0.15, "Premium &\nFeature-rich",  fontsize=8, color="#555", style="italic")
ax.text(2,    2.3,           "Affordable &\nFocused",        fontsize=8, color="#555", style="italic")
ax.text(mid_x + 2, 2.3,     "Premium &\nFocused",           fontsize=8, color="#555", style="italic")

# Plot tools
label_offsets = {
    "Notion AI":  (-1,  0.22),
    "Jasper":     ( 2,  0.22),
    "Copy.ai":    (-1, -0.38),
    "Writesonic": ( 2, -0.38),
}

for tool in TOOLS:
    px = pos_prices[tool]
    py = richness[TOOLS.index(tool)]
    color = COLORS[tool]
    ax.scatter(px, py, s=500, color=color, zorder=5, edgecolors="white", linewidths=2.5)
    dx, dy = label_offsets[tool]
    ax.annotate(
        f"{tool}\n({py:.1f}/10)",
        (px, py),
        xytext=(px + dx, py + dy),
        fontsize=10, fontweight="bold", color=color,
        arrowprops=dict(arrowstyle="-", color=color, lw=0.8),
    )

ax.set_xlim(0, 100)
ax.set_ylim(2, 7.5)
ax.set_xlabel("Entry-Level Annual Price / Month (USD)", fontsize=11)
ax.set_ylabel("Feature Richness Score (out of 10)", fontsize=11)
ax.set_title("Positioning Map: Price vs Feature Richness", fontsize=13, fontweight="bold", pad=16)
ax.text(
    0.02, 0.02,
    "Notion AI price estimated (~$15/mo) — AI bundled in workspace subscription",
    transform=ax.transAxes, fontsize=7.5, color="gray", style="italic",
)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "positioning_map.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved positioning_map.png")

print("\nAll 3 charts saved to outputs/")
