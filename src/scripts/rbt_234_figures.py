# -*- coding: utf-8 -*-
"""生成红黑树与 2-3-4 树完全对应的讲解用 SVG 图片"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'wqy-microhei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


def draw_bt_node(ax, cx, cy, r, key, color):
    """画一个二叉查找树圆节点。color: 'R'(红) 或 'B'(黑)"""
    fc = '#d64541' if color == 'R' else '#2c3e50'
    ring = 'none'
    ax.add_patch(plt.Circle((cx, cy), r, facecolor=fc, edgecolor=ring, lw=2, zorder=3))
    ax.text(cx, cy, str(key), ha='center', va='center', color='white',
            fontsize=12, fontweight='bold', zorder=5)


def draw_234_box(ax, x, y, w, h, keys, label=None):
    """画一个 2-3-4 多键节点（圆角矩形），keys 是键列表"""
    box = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                         boxstyle='round,pad=0,rounding_size=4',
                         facecolor='#eaf2f8', edgecolor='#2980b9', lw=2, zorder=3)
    ax.add_patch(box)
    n = len(keys)
    ih = min(20, h - 8)          # 内键块高度，保证不溢出盒边界
    iw = max(6, (w - 14) / n)    # 每个内键块宽度
    for i, k in enumerate(keys):
        left = x - w / 2 + 5 + i * (w - 10) / n
        inner = FancyBboxPatch((left, y - ih / 2), iw, ih,
                               boxstyle='round,pad=0,rounding_size=2',
                               facecolor='white', edgecolor='#2980b9', lw=1.2, zorder=4)
        ax.add_patch(inner)
        ax.text(left + iw / 2 - 2.5, y, str(k), ha='center', va='center',
                fontsize=12, fontweight='bold', color='#1a5276', zorder=5)
    if label:
        ax.text(x, y - h / 2 - 14, label, ha='center', va='center', fontsize=11, color='#555555')


def connect(ax, p1, p2, color='#888888', style='-|>', lw=1.8):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=16,
                                 color=color, lw=lw, zorder=2))


def draw_edge(ax, n1, n2, color='#999999', lw=2):
    ax.plot([n1[0], n2[0]], [n1[1], n2[1]], color=color, lw=lw, zorder=1)


# ---------------- 图一：2/3/4 节点 → 红黑编码（含 3 节点两种形态） ----------------
def fig_node_mapping():
    # 用 2×2 子图网格：每个示例独立坐标系，完全杜绝跨格重叠
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), dpi=150)
    for a in axes.flat:
        a.set_xlim(0, 60); a.set_ylim(0, 95); a.axis('off')

    def draw_cell(ax, box_keys, box_label, rtree, caption):
        cx = 30
        # 2-3-4 盒：x 7..53，y 45..75（宽 46 足够放下多键块，互不重叠）
        draw_234_box(ax, cx, 60, 46, 30, box_keys)
        # 标签放在盒上方
        ax.text(cx, 86, box_label, ha='center', fontsize=12, color='#555555')
        # 红黑树表示在盒下方：父在 cx，孩子在其左右，同一水平线
        base = 22
        for off, key, col in rtree:
            draw_bt_node(ax, cx + off, base, 4.5, key, col)
            edge_col = '#e74c3c' if col == 'R' else '#2c3e50'
            ax.plot([cx, cx + off], [base, base], color=edge_col, lw=2.5, zorder=1)
        # 从盒底到黑父节点的转换箭头
        connect(ax, (cx, 45), (cx, 27), color='#2980b9', style='-|>')
        # 说明文字放在红黑节点下方
        ax.text(cx, 10, caption, ha='center', fontsize=10, color='#1a5276')

    # 2-节点 -> 黑节点
    draw_cell(axes[0, 0], [20], '2-节点', [(0, 20, 'B')], '单一黑节点')
    # 3-节点（键在父左，红孩子向左）-> 黑 + 红左孩子
    draw_cell(axes[0, 1], [10, 30], '3-节点（键在父左）',
              [(-12, 10, 'R'), (0, 30, 'B')], '黑 30 + 红左孩子 10')
    # 3-节点（键在父右，红孩子向右）-> 黑 + 红右孩子
    draw_cell(axes[1, 0], [10, 30], '3-节点（键在父右）',
              [(0, 10, 'B'), (12, 30, 'R')], '黑 10 + 红右孩子 30')
    # 4-节点 -> 黑 + 双红
    draw_cell(axes[1, 1], [10, 30, 60], '4-节点',
              [(-12, 10, 'R'), (0, 30, 'B'), (12, 60, 'R')], '黑 30 + 双红孩子')
    fig.savefig('images/rbt_234_node_mapping.svg', bbox_inches='tight')
    plt.close(fig)
    print('saved rbt_234_node_mapping.svg')


# ---------------- 图二：红黑树五条性质 ↔ 2-3-4 三条约束 ----------------
def fig_property_map():
    fig, ax = plt.subplots(figsize=(13, 4.2), dpi=150)
    ax.set_xlim(0, 130); ax.set_ylim(0, 30); ax.axis('off')

    red = [
        ('红黑树性质', '2-3-4 树对应意义'),
        ('① 节点非红即黑', '多键节点有固定二进制编码'),
        ('② 根为黑', '根节点无气泡上行（不表示父键）'),
        ('④ 红节点子节点皆黑', '多键节点中两键必然夹着父键'),
        ('⑤ 每路径黑数相同', '所有叶子同层（天然平衡）'),
        ('③ 叶(NIL)皆黑', '空子树视为黑色空占位'),
    ]
    y0 = 26
    for i, (a, b) in enumerate(red):
        yy = y0 - i * 5
        if i == 0:
            ax.text(30, yy + 1.6, a + '  ═══  ' + b, ha='center', fontsize=12,
                    fontweight='bold', color='#1a5276')
        else:
            ax.text(30, yy, f'{a}  ⇌  {b}', ha='center', fontsize=11, color='#2c3e50')

    # 右侧红/黑图例
    draw_bt_node(ax, 104, 24, 4, '', 'R')
    ax.text(104, 18, '红 = 与父构成\n同一多键节点', ha='center', fontsize=9, color='#555555')
    draw_bt_node(ax, 104, 10, 4, '', 'B')
    ax.text(104, 4, '黑 = 独立节点(层级)', ha='center', fontsize=9, color='#555555')

    fig.savefig('images/rbt_234_property_map.svg', bbox_inches='tight')
    plt.close(fig)
    print('saved rbt_234_property_map.svg')


# ---------------- 图三：插入修复 ↔ 2-3-4 分裂提升 ----------------
def fig_insert_repair():
    fig, ax = plt.subplots(figsize=(13, 9.6), dpi=150)
    ax.set_xlim(0, 130); ax.set_ylim(0, 64); ax.axis('off')

    # 每行标题
    rows = [
        ('情形 1：叔叔是红色 → 全变色（对应 2-3-4 的 4-节点“上溢分裂”）',
         58, 'R', 'R', 'R', 'R'),
        ('情形 2 + 3：叔叔是黑色 → 旋转 + 变色（对应 2-3-4 的 3-节点扩容后分裂）',
         38, 'R', 'R', 'R', 'B'),
    ]
    for title, yc, c_new, c_p, c_u, c_g in rows:
        ax.text(65, yc + 8.5, title, ha='center', fontsize=11, fontweight='bold', color='#1a5276')

    # ---- 行1 情形1：父叔皆红，爷黑 ----
    ax.text(22, 56, '红黑树（插入前）', ha='center', fontsize=10, color='#2c3e50')
    g = (22, 52); p = (14, 44); u = (30, 44); z = (10, 36)
    draw_edge(ax, g, p); draw_edge(ax, g, u); draw_edge(ax, p, z)
    draw_bt_node(ax, *g, 4, 60, 'B')
    draw_bt_node(ax, *p, 4, 40, 'R')
    draw_bt_node(ax, *u, 4, 80, 'R')
    draw_bt_node(ax, *z, 4, 50, 'R')
    ax.text(22, 33, '插入后叔叔(80)为红，\n祖父(60)夹在中间', ha='center', fontsize=9, color='#555555')

    # 左侧 2-3-4 语义
    ax.text(65, 41.5, '对应 2-3-4：4-节点\n(40 | 50 | 60 | 80) 插入 50 后\n5 个键“上溢”分裂，中键 60 提升',
            ha='center', fontsize=9, color='#7d3c98', bbox=dict(boxstyle='round,pad=0.4',
            facecolor='#f4ecf7', edgecolor='#7d3c98'))

    ax.text(108, 56, '红黑树（变色后）', ha='center', fontsize=10, color='#2c3e50')
    g2 = (108, 52); p2 = (100, 44); u2 = (118, 44); z2 = (94, 36)
    draw_edge(ax, g2, p2); draw_edge(ax, g2, u2); draw_edge(ax, p2, z2)
    draw_bt_node(ax, *g2, 4, 60, 'R')   # 祖父变红
    draw_bt_node(ax, *p2, 4, 40, 'B')   # 父变黑
    draw_bt_node(ax, *u2, 4, 80, 'B')   # 叔变黑
    draw_bt_node(ax, *z2, 4, 50, 'R')   # 新节点仍为红（其父变黑后已合法）
    ax.text(108, 33, '父(40)、叔(80)变黑，祖父(60)变红继续向上检查；\n被插入的新节点 50 保持红色', ha='center', fontsize=9, color='#555555')

    # ---- 行2 情形2+3：叔叔黑 ----
    ax.text(22, 35.5, '红黑树：叔叔为黑', ha='center', fontsize=10, color='#2c3e50')
    g = (22, 30); p = (14, 22); z = (10, 14)
    draw_edge(ax, g, p); draw_edge(ax, g, (30, 30)); draw_edge(ax, p, z)
    draw_bt_node(ax, *g, 4, 60, 'B')
    draw_bt_node(ax, *p, 4, 40, 'R')
    draw_bt_node(ax, 30, 30, 4, 80, 'B')
    draw_bt_node(ax, *z, 4, 50, 'R')

    ax.text(65, 23.5, '对应 2-3-4：3-节点\n(40|60) 插入 50，扩容成\n4-节点 (40|50|60)，随后\n分裂、中键 50 提升',
            ha='center', fontsize=9, color='#7d3c98', bbox=dict(boxstyle='round,pad=0.4',
            facecolor='#f4ecf7', edgecolor='#7d3c98'))

    ax.text(108, 35.5, '红黑树：旋转(LR)+变色', ha='center', fontsize=10, color='#2c3e50')
    g2 = (108, 30); p2 = (100, 22); z2 = (108, 16)
    draw_edge(ax, g2, p2); draw_edge(ax, g2, (116, 30)); draw_edge(ax, p2, z2)
    draw_bt_node(ax, *g2, 4, 60, 'R')
    draw_bt_node(ax, *p2, 4, 50, 'B')
    draw_bt_node(ax, *z2, 4, 40, 'R')
    draw_bt_node(ax, 116, 30, 4, 80, 'B')
    ax.text(108, 13, '50 提升为父(黑)，60 与 40\n变红挂在两侧（=4-节点分裂）', ha='center', fontsize=9, color='#555555')

    fig.savefig('images/rbt_234_insert_repair.svg', bbox_inches='tight')
    plt.close(fig)
    print('saved rbt_234_insert_repair.svg')


def draw_node(ax, x, y, r, key, color='black'):
    """画一个带颜色标签的圆节点（key 可为 str/数字，color: R/B）"""
    fc = '#d64541' if color == 'R' else '#2c3e50'
    ax.add_patch(plt.Circle((x, y), r, facecolor=fc, edgecolor='none', lw=2, zorder=3))
    ax.text(x, y, str(key), ha='center', va='center', color='white',
            fontsize=16, fontweight='bold', zorder=5)


def draw_subtree(ax, x, y, label, color='#95a5a6'):
    """画一个表示整棵子树的灰色小三角，label 填在下方"""
    tri = plt.Polygon([(x, y + 7), (x - 9, y - 7), (x + 9, y - 7)],
                      closed=True, facecolor=color, edgecolor='#7f8c8d', lw=1, zorder=2, alpha=0.55)
    ax.add_patch(tri)
    ax.text(x, y - 12, label, ha='center', va='center', fontsize=11,
            color='#7f8c8d', fontstyle='italic')


def draw_lr_link(ax, x1, y1, x2, y2, color='#7f8c8d', lw=2):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, zorder=1)


# ---------------- 图五：左旋 / 右旋的逐步细节（父-子关系 + 子树 α/β/γ） ----------------
def fig_rotation_demo():
    fig, axes = plt.subplots(2, 2, figsize=(13, 7.4), dpi=150)
    for a in axes.flat:
        a.set_xlim(0, 100); a.set_ylim(0, 90); a.axis('off')

    # 标题
    axes[0, 0].text(50, 86, '左旋  —  旋转前', ha='center', fontsize=13, fontweight='bold', color='#1a5276')
    axes[0, 1].text(50, 86, '左旋  —  旋转后', ha='center', fontsize=13, fontweight='bold', color='#1a5276')
    axes[1, 0].text(50, 86, '右旋  —  旋转前', ha='center', fontsize=13, fontweight='bold', color='#1a5276')
    axes[1, 1].text(50, 86, '右旋  —  旋转后', ha='center', fontsize=13, fontweight='bold', color='#1a5276')

    # 左旋前：P -[x]- (α, y[β,γ])
    a = axes[0, 0]
    P = (50, 72); x = (26, 42); y = (80, 42)
    draw_lr_link(a, *P, *x); draw_lr_link(a, *x, *(10, 12)); draw_lr_link(a, *x, *y)
    draw_lr_link(a, *y, *(62, 12)); draw_lr_link(a, *y, *(98, 12))
    draw_node(a, *P, 7, 'P·祖父', 'B')
    draw_node(a, *x, 7, 'x', 'B')
    draw_node(a, *y, 7, 'y', 'R')
    draw_subtree(a, 10, 22, 'α', color='#bdc3c7')
    draw_subtree(a, 62, 22, 'β', color='#b8c6d7')
    draw_subtree(a, 98, 22, 'γ', color='#b8c6d7')
    a.text(50, -2, 'y 是 x 的右孩子；x 借“同一父键 δ”，旋转后 y 上移接替 x',
           ha='center', fontsize=9, color='#7f8c8d')

    # 左旋后：P -[y]- (x[α,β], γ)；x 变 y 左孩子，β（y 原左子树）过继给 x 当右孩子
    a = axes[0, 1]
    P = (50, 72); y = (52, 42); x = (26, 42)
    draw_lr_link(a, *P, *y); draw_lr_link(a, *y, *x); draw_lr_link(a, *y, *(84, 42))
    draw_lr_link(a, *x, *(10, 12)); draw_lr_link(a, *x, *(46, 12))
    draw_lr_link(a, *(84, 42), *(98, 12))
    draw_node(a, *P, 7, 'P·祖父', 'B')
    draw_node(a, *y, 7, 'y', 'B')
    draw_node(a, *x, 7, 'x', 'R')
    draw_subtree(a, 10, 22, 'α', color='#bdc3c7')
    draw_subtree(a, 46, 22, 'β', color='#b8c6d7')
    draw_subtree(a, 98, 22, 'γ', color='#b8c6d7')
    a.text(50, -2, 'y 升至 x 位置；β 过继给 x 当右孩子。即“3-节点扩容后中键的位置变化”',
           ha='center', fontsize=9, color='#7f8c8d')

    # 右旋前：P -[x]- (y[α,β], γ)；y 是 x 左孩子
    a = axes[1, 0]
    P = (50, 70); x = (76, 40); y = (22, 40)
    draw_lr_link(a, *P, *x); draw_lr_link(a, *x, *y); draw_lr_link(a, *x, *(96, 8))
    draw_lr_link(a, *y, *(4, 8)); draw_lr_link(a, *y, *(40, 8))
    draw_node(a, *P, 7, 'P·祖父', 'B')
    draw_node(a, *x, 7, 'x', 'B')
    draw_node(a, *y, 7, 'y', 'R')
    draw_subtree(a, 4, 18, 'α', color='#b8c6d7')
    draw_subtree(a, 40, 18, 'β', color='#b8c6d7')
    draw_subtree(a, 96, 12, 'γ', color='#bdc3c7')
    a.text(50, -2, 'y 是 x 的左孩子；旋转后 y 上移接替 x',
           ha='center', fontsize=9, color='#7f8c8d')

    # 右旋后：P -[y]- (α, x[β,γ])；x 变 y 右孩子，β（y 原右子树）过继给 x 当左孩子
    a = axes[1, 1]
    P = (50, 70); y = (48, 40); x = (76, 40)
    draw_lr_link(a, *P, *y); draw_lr_link(a, *y, *(18, 40)); draw_lr_link(a, *y, *x)
    draw_lr_link(a, *x, *(56, 8)); draw_lr_link(a, *x, *(96, 8))
    draw_lr_link(a, *(18, 40), *(4, 8))
    draw_node(a, *P, 7, 'P·祖父', 'B')
    draw_node(a, *y, 7, 'y', 'B')
    draw_node(a, *x, 7, 'x', 'R')
    draw_subtree(a, 4, 18, 'α', color='#b8c6d7')
    draw_subtree(a, 56, 18, 'β', color='#b8c6d7')
    draw_subtree(a, 96, 12, 'γ', color='#bdc3c7')
    a.text(50, -2, 'x 升至 y 位置；β 过继给 x 当左孩子',
           ha='center', fontsize=9, color='#7f8c8d')

    fig.savefig('images/rbt_rotation_demo.svg', bbox_inches='tight')
    plt.close(fig)
    print('saved rbt_rotation_demo.svg')


# ---------------- 图六：一次完整插入 10,20,30 的分步过程（对应 2-3-4 分裂） ----------------
def fig_insert_steps():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.6), dpi=150)
    for a in axes.flat:
        a.set_xlim(0, 100); a.set_ylim(0, 90); a.axis('off')

    # 格0：插入 30 后出现连续红（20、30 都是红）
    a = axes[0]
    a.text(50, 84, 'STEP 1：新键 30 插入',
           ha='center', fontsize=12, fontweight='bold', color='#1a5276')
    node10 = (20, 42); node20 = (50, 42); node30 = (80, 42)
    draw_lr_link(a, node10[0], node10[1], node20[0], node20[1], color='#e74c3c')
    draw_lr_link(a, node20[0], node20[1], node30[0], node30[1], color='#e74c3c')
    draw_node(a, *node10, 8, '10', 'B')
    draw_node(a, *node20, 8, '20', 'R')
    draw_node(a, *node30, 8, '30', 'R')
    a.text(50, 62, '2-3-4：10｜20｜30 一个满键节点',
           ha='center', fontsize=9, color='#8e44ad')
    a.text(50, -2, '“连续红”(20,30) = 双子接近满键，\
即将“上溢”', ha='center', fontsize=9, color='#7f8c8d', wrap=True)

    # 格1：中键 20 上提 / 旋转变色
    a = axes[1]
    a.text(50, 84, 'STEP 2：旋转 + 变色',
           ha='center', fontsize=12, fontweight='bold', color='#1a5276')
    c20 = (50, 48); c10 = (26, 24); c30 = (74, 24)
    draw_lr_link(a, c20[0], c20[1], c10[0], c10[1], color='#2c3e50')
    draw_lr_link(a, c20[0], c20[1], c30[0], c30[1], color='#2c3e50')
    draw_node(a, *c20, 8, '20', 'B')
    draw_node(a, *c10, 8, '10', 'R')
    draw_node(a, *c30, 8, '30', 'R')
    a.text(50, 64, '2-3-4：中键 20 被“顶上去”，两侧变成红孩子',
           ha='center', fontsize=9, color='#8e44ad')
    a.text(50, -2, '中键变黑、两侧变红 = 节点分裂瞬间',
           ha='center', fontsize=9, color='#7f8c8d')

    # 格2：得到合法红黑树
    a = axes[2]
    a.text(50, 84, 'STEP 3：合法红黑树',
           ha='center', fontsize=12, fontweight='bold', color='#1a5276')
    c20 = (50, 50); c10 = (24, 24); c30 = (76, 24)
    draw_lr_link(a, c20[0], c20[1], c10[0], c10[1], color='#2c3e50')
    draw_lr_link(a, c20[0], c20[1], c30[0], c30[1], color='#2c3e50')
    draw_node(a, *c20, 8, '20', 'B')
    draw_node(a, *c10, 8, '10', 'R')
    draw_node(a, *c30, 8, '30', 'R')
    a.text(50, 34, '黑高 1，两路黑节点数相同 → 性质 ⑤成立',
           ha='center', fontsize=9, color='#2c3e50')
    a.text(50, -2, '最终根 20 为黑，叶 10 / 30 为红',
           ha='center', fontsize=9, color='#7f8c8d')

    fig.savefig('images/rbt_insert_steps.svg', bbox_inches='tight')
    plt.close(fig)
    print('saved rbt_insert_steps.svg')


if __name__ == '__main__':
    fig_node_mapping()
    fig_property_map()
    fig_insert_repair()
    fig_rotation_demo()
    fig_insert_steps()