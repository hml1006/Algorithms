import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def euclidean_steps(a, b):
    """返回辗转相除法每一步的 (被除数, 除数, 商, 余数)"""
    steps = []
    while b != 0:
        q = a // b
        r = a % b
        steps.append((a, b, q, r))
        a, b = b, r
    return steps, a  # a 就是 gcd

def draw_squares(ax, a, b, colors, offset_x=0, offset_y=0, depth=0, direction='h', container_h=None):
    """递归绘制矩形分割为正方形的过程
    
    direction='h': 水平切割——沿x轴方向从左到右切出正方形
    direction='v': 垂直切割——沿y轴方向从下到上切出正方形
    container_h: 嵌套布局时，指定容器高度，使子矩形填充整个容器
    """
    if b == 0:
        return
    q = a // b
    r = a % b
    color = colors[depth % len(colors)]
    # 嵌套布局时使用容器高度，否则使用当前矩形高度
    h = container_h if container_h is not None else b

    if direction == 'h':
        # ===== 水平切割：矩形宽a、高b，从左到右排列 q 个 b×h 矩形 =====
        for i in range(q):
            square = patches.Rectangle(
                (offset_x + i * b, offset_y), b, h,
                linewidth=1.5, edgecolor='black',
                facecolor=color, alpha=0.7, zorder=2
            )
            ax.add_patch(square)
            if b >= 8:
                # 文本居中显示在矩形中心
                ax.text(offset_x + i * b + b / 2, offset_y + h / 2, f'{b}',
                        ha='center', va='center', fontsize=10, fontweight='bold')

        # 标注本组正方形
        if q > 0:
            mid_x = offset_x + q * b / 2
            ax.annotate('', xy=(offset_x, offset_y - 1), xytext=(offset_x + q * b, offset_y - 1),
                        arrowprops=dict(arrowstyle='<->', color='gray', lw=1.2))
            label = f'{q} 个 {b}'
            ax.text(mid_x, offset_y - 3.5, label,
                    ha='center', va='top', fontsize=8, color='gray', style='italic')

        # 剩余部分：r×h（宽r、高h），下一层需垂直切割
        if r > 0:
            if container_h is None:
                # 非嵌套时绘制剩余区域虚线矩形
                rem_rect = patches.Rectangle(
                    (offset_x + q * b, offset_y), r, h,
                    linewidth=2, edgecolor='#E74C3C',
                    facecolor='none', linestyle='--', zorder=3
                )
                ax.add_patch(rem_rect)
                ax.text(offset_x + q * b + r / 2, offset_y + h / 2, f'{r}',
                        ha='center', va='center', fontsize=10, fontweight='bold', color='#E74C3C')
                ax.annotate(f'剩余 {r}×{b}',
                            xy=(offset_x + q * b + r / 2, offset_y + h + 2),
                            ha='center', fontsize=8, color='#E74C3C')
            if container_h is not None:
                # 嵌套布局时：剩余区域直接绘制为矩形，不再递归切割
                # 使用父级颜色（蓝色），并在其上标注剩余值 r
                parent_color = colors[(depth - 1) % len(colors)]
                rem_rect = patches.Rectangle(
                    (offset_x + q * b, offset_y), r, h,
                    linewidth=1.5, edgecolor='black',
                    facecolor=parent_color, alpha=0.7, zorder=2
                )
                ax.add_patch(rem_rect)
                if r >= 4:
                    ax.text(offset_x + q * b + r / 2, offset_y + h / 2, f'{r}',
                            ha='center', va='center', fontsize=10, fontweight='bold',
                            color='white')
            else:
                # 递归：垂直切割（旋转90°）
                draw_squares(ax, b, r, colors, offset_x + q * b, offset_y, depth + 1, 'v')
        else:
            mid = offset_x + q * b / 2
            ax.annotate(f'✔ GCD = {b}',
                        xy=(mid, offset_y + b / 2),
                        xytext=(mid, offset_y + b + 8),
                        ha='center', fontsize=11, fontweight='bold', color='#27AE60',
                        arrowprops=dict(arrowstyle='->', color='#27AE60', lw=1.5))

    else:  # direction == 'v'
        # ===== 垂直切割：矩形宽b、高a，从下到上排列 q 个 b×b 正方形 =====
        for i in range(q):
            square = patches.Rectangle(
                (offset_x, offset_y + i * b), b, b,
                linewidth=1.5, edgecolor='black',
                facecolor=color, alpha=0.7, zorder=2
            )
            ax.add_patch(square)
            # 嵌套布局时，最后一个正方形上的文本被内部切割替代，不显示
            if b >= 8 and not (i == q - 1 and r > 0):
                ax.text(offset_x + b / 2, offset_y + i * b + b / 2, f'{b}',
                        ha='center', va='center', fontsize=10, fontweight='bold')

        # 标注本组正方形
        if q > 0:
            mid_y = offset_y + q * b / 2
            ax.annotate('', xy=(offset_x - 1, offset_y), xytext=(offset_x - 1, offset_y + q * b),
                        arrowprops=dict(arrowstyle='<->', color='gray', lw=1.2))
            label = f'{q} 个 {b}'
            ax.text(offset_x - 3.5, mid_y, label,
                    ha='right', va='center', fontsize=8, color='gray', style='italic', rotation=90)

        # 剩余部分：b×r（宽b、高r）
        if r > 0:
            # 在正方形上方区域添加文本 r（剩余量）
            text_x = offset_x + b / 2
            text_y = offset_y + q * b + r / 2
            ax.text(text_x, text_y, f'{r}',
                    ha='center', va='center', fontsize=10, fontweight='bold', color='#E74C3C')
            # 嵌套布局：在最后一个正方形内部递归，填满整个正方形
            # 这样能更直观地反映递归关系：gcd(a,b) = gcd(b, r)
            # 传入 container_h=b 使嵌套矩形填满父正方形的整个高度
            draw_squares(ax, b, r, colors, offset_x, offset_y + (q - 1) * b, depth + 1, 'h', container_h=b)
        else:
            mid = offset_y + q * b / 2
            ax.annotate(f'✔ GCD = {b}',
                        xy=(offset_x + b / 2, mid),
                        xytext=(offset_x + b + 8, mid),
                        va='center', fontsize=11, fontweight='bold', color='#27AE60',
                        arrowprops=dict(arrowstyle='->', color='#27AE60', lw=1.5))

def add_equation_annotation(ax, a, b, q, r, offset_x=0, offset_y=0):
    """在矩形上方标注核心等式 a = b×q + r"""
    x = offset_x + a / 2
    y = b + 5 + offset_y
    eq_text = f'{a} = {b} × {q} + {r}'
    ax.text(x, y, eq_text, fontsize=11, fontweight='bold',
            ha='center', va='bottom', color='#2C3E50',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor='#3498DB', alpha=0.9))

def draw_proof_diagram(ax2, a, b, q, r):
    """在右面板绘制双向推导证明图"""
    # 使用 ax2 的坐标 (0-1 范围)
    # 三个框 + 两个箭头 + 推导细节

    box_style = dict(boxstyle='round,pad=0.4', facecolor='#EBF5FB',
                     edgecolor='#3498DB', linewidth=1.5)
    box_style2 = dict(boxstyle='round,pad=0.4', facecolor='#E8F8F5',
                      edgecolor='#1ABC9C', linewidth=1.5)
    box_style3 = dict(boxstyle='round,pad=0.4', facecolor='#FEF9E7',
                      edgecolor='#F39C12', linewidth=1.5)

    # 框 1: d|a, d|b
    ax2.text(0.20, 0.74, 'd 整除 a 和 b\n(d | a, d | b)',
             fontsize=9, ha='center', va='center', color='#2C3E50',
             transform=ax2.transAxes, bbox=box_style)

    # 框 2: d|b, d|r
    ax2.text(0.20, 0.54, 'd 整除 b 和 r\n(d | b, d | r)',
             fontsize=9, ha='center', va='center', color='#2C3E50',
             transform=ax2.transAxes, bbox=box_style2)

    # 框 3: d|a, d|b (回到起点)
    ax2.text(0.20, 0.34, 'd 整除 a 和 b\n(d | a, d | b)',
             fontsize=9, ha='center', va='center', color='#2C3E50',
             transform=ax2.transAxes, bbox=box_style3)

    # 箭头 1: 框1 → 框2
    ax2.annotate('', xy=(0.20, 0.58), xytext=(0.20, 0.70),
                 transform=ax2.transAxes,
                 arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=2))

    # 推导细节 (框1 → 框2)
    ax2.text(0.38, 0.65, f'由于 r = {a} - {b}×{q} = {r}，',
             fontsize=7.5, color='#E74C3C', transform=ax2.transAxes,
             fontweight='bold')
    ax2.text(0.38, 0.605, '根据整除性质：若 d|a 且 d|b，则',
             fontsize=7, color='#34495E', transform=ax2.transAxes)
    ax2.text(0.38, 0.575, 'd 整除它们的任意线性组合：',
             fontsize=7, color='#34495E', transform=ax2.transAxes)

    # 代数推导框
    derivation_lines = [
        'd | a  →  a = d × m  (m 是整数)',
        'd | b  →  b = d × n  (n 是整数)',
        '',
        f'r = a - b×q',
        f'  = d×m - d×n×q',
        f'  = d × (m - n×q)',
        '∴ d | r  (d 整除 r)',
    ]
    deriv_text = '\n'.join(derivation_lines)
    ax2.text(0.42, 0.575, deriv_text, fontsize=6.5, color='#2C3E50',
             transform=ax2.transAxes, va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                       edgecolor='#E74C3C', alpha=0.85))

    # 箭头 2: 框2 → 框3 (反向推导 - 关键！)
    ax2.annotate('', xy=(0.20, 0.38), xytext=(0.20, 0.50),
                 transform=ax2.transAxes,
                 arrowprops=dict(arrowstyle='->', color='#27AE60', lw=2))

    # 强调：这是关键方向
    ax2.text(0.38, 0.455, '★ 关键：这里证明 (b,r) 的公约数',
             fontsize=7.5, color='#27AE60', transform=ax2.transAxes,
             fontweight='bold')
    ax2.text(0.38, 0.435, '不可能超出 (a,b) 的范围',
             fontsize=7.5, color='#27AE60', transform=ax2.transAxes,
             fontweight='bold')

    # 反向推导细节
    nq = b * q  # b×q 的值
    rev_derivation_lines = [
        f'因为 a = b×q + r',
        f'    = {b}×{q} + {r}',
        '',
        '若 d|b 且 d|r →',
        '  b = d×n, r = d×k',
        '  a = d×n×q + d×k',
        f'    = d × ({nq} + k)',
        '∴ d | a',
    ]
    rev_deriv_text = '\n'.join(rev_derivation_lines)
    ax2.text(0.42, 0.455, rev_deriv_text, fontsize=6.5, color='#2C3E50',
             transform=ax2.transAxes, va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                       edgecolor='#27AE60', alpha=0.85))

    # 双向箭头标注
    ax2.text(0.06, 0.54, '⇔', fontsize=16, fontweight='bold',
             color='#8E44AD', transform=ax2.transAxes)

    # 结论
    ax2.text(0.20, 0.28, '结论：两个方向都成立，d 是 (a,b) 的公约数 ⇔ d 是 (b,r) 的公约数\n'
                        '所以 (a,b) 和 (b,r) 的公约数集合完全相同，没有公约数被跳过！',
             fontsize=7.5, ha='center', color='#8E44AD', fontweight='bold',
             transform=ax2.transAxes,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4ECF7',
                       edgecolor='#8E44AD'))

    # 递归链条说明
    ax2.text(0.20, 0.22, '该证明对每一步递归都独立成立：\n'
                        '第1步: (100,36)→(36,28) 用 100=36×2+28\n'
                        '第2步: (36,28)→(28,8) 用 36=28×1+8\n'
                        '第3步: (28,8)→(8,4) 用 28=8×3+4\n'
                        '每步独立证明，互不依赖，传递性保证全程不变',
             fontsize=6.5, ha='center', color='#2C3E50',
             transform=ax2.transAxes,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#F5F5F5',
                       edgecolor='#BDC3C7'))


def visualize_euclidean(a, b, save_path=None):
    """可视化辗转相除法的几何解释 + 数学证明"""
    steps, gcd = euclidean_steps(a, b)

    # 创建画布
    fig = plt.figure(figsize=(14, 7.8))
    gs = fig.add_gridspec(1, 2, width_ratios=[3, 2], wspace=0.3)

    # ========== 左图：矩形分割 ==========
    ax1 = fig.add_subplot(gs[0])
    colors = ['#F39C12', '#3498DB', '#2ECC71', '#9B59B6', '#E74C3C', '#1ABC9C']

    draw_squares(ax1, a, b, colors)

    # 外框
    outer = patches.Rectangle((0, 0), a, b, linewidth=2.5,
                               edgecolor='black', facecolor='none', zorder=4)
    ax1.add_patch(outer)

    # 在矩形上方标注第一步的等式
    first_a, first_b, first_q, first_r = steps[0]
    add_equation_annotation(ax1, first_a, first_b, first_q, first_r, 0)

    ax1.set_xlim(-2, a + 18)
    ax1.set_ylim(-6, b + 16)
    ax1.set_aspect('equal')
    ax1.set_title(f'矩形分割法求 GCD({a}, {b})', fontsize=14, fontweight='bold', pad=12)
    ax1.set_xlabel(f'宽 = {a}')
    ax1.set_ylabel(f'高 = {b}')
    ax1.grid(True, alpha=0.15)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # ========== 右图：为什么递归求出的就是最大公约数 ==========
    ax2 = fig.add_subplot(gs[1])
    ax2.axis('off')

    # 标题
    ax2.text(0.5, 0.97, '为什么递归求出的就是最大公约数？', fontsize=13,
             fontweight='bold', ha='center', transform=ax2.transAxes,
             color='#2C3E50')

    # 核心公式
    ax2.text(0.5, 0.92, 'gcd(a, b) = gcd(b, a % b)',
             fontsize=12, ha='center', color='#2980B9',
             transform=ax2.transAxes,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#EBF5FB', edgecolor='#85C1E9'))

    # ===== 条件①：公约数没有被跳过（可视化证明） =====
    first_a, first_b, first_q, first_r = steps[0]
    draw_proof_diagram(ax2, first_a, first_b, first_q, first_r)

    # ===== 条件②：数列严格递减 =====
    y = 0.15
    ax2.text(0.08, y, '② 数列严格递减（保证终止）', fontsize=8, fontweight='bold',
             transform=ax2.transAxes, color='#C0392B')
    y -= 0.02
    p2_lines = [
        '余数 r = a % b 一定小于除数 b（0 ≤ r < b）',
        '每一步的除数严格递减，非负整数不能无限递减',
        '∴ 必然在有限步内到达 0',
    ]
    for line in p2_lines:
        ax2.text(0.12, y, line, fontsize=7, color='#34495E',
                 transform=ax2.transAxes)
        y -= 0.018

    # ===== 条件③：边界条件 =====
    y -= 0.003
    ax2.text(0.08, y, '③ gcd(x, 0) = x（边界条件）', fontsize=8, fontweight='bold',
             transform=ax2.transAxes, color='#C0392B')
    y -= 0.02
    p3_lines = [
        '余数 0 时最后一步是 gcd(g, 0)，任何数整除 0',
        'g 的最大约数是 g 本身 → gcd(g, 0) = g',
    ]
    for line in p3_lines:
        ax2.text(0.12, y, line, fontsize=7, color='#34495E',
                 transform=ax2.transAxes)
        y -= 0.018

    # ===== 完整逻辑链 =====
    y -= 0.005
    ax2.text(0.08, y, '完整逻辑链', fontsize=8, fontweight='bold',
             transform=ax2.transAxes, color='#2C3E50')
    y -= 0.02

    # 构建链条
    chain_parts = []
    for i, (ca, cb, q, r) in enumerate(steps):
        chain_parts.append(f'gcd({ca},{cb})')
    chain_parts.append(f'gcd({gcd},0)')
    chain_parts.append(f'{gcd}')
    chain_str = ' = '.join(chain_parts)
    ax2.text(0.10, y, chain_str, fontsize=6.5, color='#E74C3C',
             transform=ax2.transAxes, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#FDEDEC',
                       edgecolor='#E74C3C'))
    y -= 0.035

    # 每一步的公约数集合验证（简洁版）
    def get_common_divisors(x, y):
        limit = min(abs(x), abs(y)) if y != 0 else abs(x)
        return sorted([d for d in range(1, limit + 1) if x % d == 0 and y % d == 0])

    for i, (ca, cb, q, r) in enumerate(steps):
        if r > 0:
            divs = get_common_divisors(ca, cb)
            line = f'  Step {i+1}: 公约数 {set(divs)} → ✓'
            ax2.text(0.08, y, line, fontsize=6.5, color='#27AE60',
                     transform=ax2.transAxes, fontweight='bold')
            y -= 0.016
        else:
            line = f'  Step {i+1}: 余数=0 → gcd({cb},0) = {cb}'
            ax2.text(0.08, y, line, fontsize=6.5, color='#E74C3C',
                     transform=ax2.transAxes, fontweight='bold')
            y -= 0.016

    y -= 0.008
    ax2.text(0.08, y, f'  最终结果：GCD({a}, {b}) = {gcd}', fontsize=10,
             fontweight='bold', color='#E74C3C', transform=ax2.transAxes)

    plt.suptitle('辗转相除法（欧几里得算法）—— 为什么递归求出的就是最大公约数？', fontsize=14,
                 fontweight='bold')
    plt.subplots_adjust(left=0.04, right=0.98, top=0.90, bottom=0.04, wspace=0.25)

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
        print(f'✅ 图片已保存: {save_path}')
    plt.show()


if __name__ == '__main__':
    # 用多步例子：GCD(100, 36) = 4，演示完整的辗转相除过程
    visualize_euclidean(100, 36, 'src/images/euclidean_algorithm.png')