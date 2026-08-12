#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""共享 matplotlib 样式：中文字体 + 统一配色"""
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 注册中文字体（Noto Sans CJK / Noto Serif CJK）
for fp in [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    "/usr/share/fonts/truetype/arphic/uming.ttc",
]:
    try:
        font_manager.fontManager.addfont(fp)
    except Exception:
        pass

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Noto Sans CJK SC", "Noto Sans CJK", "AR PL UMing CN", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.dpi": 110,
    "savefig.facecolor": "white",
    "axes.edgecolor": "#cccccc",
    "axes.linewidth": 0.8,
    "axes.grid": True,
    "grid.color": "#eeeeee",
    "grid.linewidth": 0.6,
})

# 统一配色（友好、高对比）
PALETTE = {
    "blue":   "#4C72B0",
    "orange": "#DD8452",
    "green":  "#55A868",
    "red":    "#C44E52",
    "purple": "#8172B3",
    "brown":  "#937860",
    "cyan":   "#64B5CD",
    "dark":   "#2a2a2a",
}