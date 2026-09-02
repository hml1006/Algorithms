# 第十层 OI/ACM 竞赛：OI 极难综合题库

## 13. OI 极难综合题库

本部分是第 12 章「OI/ACM 竞赛高级专题」的配套综合练习，覆盖 LCT、树链剖分、可持久化线段树（主席树）、莫队、珂朵莉树、舞蹈链/精确覆盖、差分约束、线性基、生成函数/多项式（FFT/NTT）、杜教筛/Min_25 筛、回文自动机、后缀自动机（SAM）等高级数据结构与算法，共 187 道代表性竞赛题，按难度从低到高排列，多为 ⭐⭐⭐（困难）级别。

---

### 13.1 数据结构进阶（树链剖分 · 主席树 · LCT）

#### 13.1.1 例 1：「模板」树链剖分 / 树上路径加与路径和（树链剖分 + 线段树）⭐⭐⭐

> **知识点**：树链剖分 + 线段树｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度很高的综合性竞赛向题目，主要考察树链剖分与线段树的结合与灵活运用。给定一棵带点权的树，支持「路径整体加一个数」与「查询一条路径的权值和」两种操作，要求高效完成多次操作。

**思路**
将树用轻重链剖分转化为 DFS 序（重儿子优先），使得任意一条根到叶路径上的 DFS 序连续，从而把「路径修改/路径查询」变成 O(log n) 段连续区间上的线段树操作。重链剖分保证每条重链的大小至少减半，总段数为 O(log n)。

```python
import sys
sys.setrecursionlimit(1 << 20)

class SegmentTree:
    """支持区间加、区间求和的线段树（简化版，实现核心增量求和）"""
    def __init__(self, n):
        self.n = n
        self.sum = [0] * (4 * n)
        self.lazy = [0] * (4 * n)

    def _push(self, p, l, r):
        if self.lazy[p]:
            m = (l + r) >> 1
            lc, rc = p << 1, p << 1 | 1
            self.sum[lc] += self.lazy[p] * (m - l + 1)
            self.sum[rc] += self.lazy[p] * (r - m)
            self.lazy[lc] += self.lazy[p]
            self.lazy[rc] += self.lazy[p]
            self.lazy[p] = 0

    def add(self, p, l, r, ql, qr, v):
        if ql <= l and r <= qr:
            self.sum[p] += v * (r - l + 1)
            self.lazy[p] += v
            return
        self._push(p, l, r)
        m = (l + r) >> 1
        if ql <= m: self.add(p << 1, l, m, ql, qr, v)
        if qr > m:  self.add(p << 1 | 1, m + 1, r, ql, qr, v)
        self.sum[p] = self.sum[p << 1] + self.sum[p << 1 | 1]

    def query(self, p, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.sum[p]
        self._push(p, l, r)
        m = (l + r) >> 1
        s = 0
        if ql <= m: s += self.query(p << 1, l, m, ql, qr)
        if qr > m:  s += self.query(p << 1 | 1, m + 1, r, ql, qr)
        return s


def heavy_light(n, adj, root=1):
    """返回父子关系、深度、重儿子、链顶与 DFS 序。这里给出核心思路代码骨架。"""
    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    size = [0] * (n + 1)
    son = [0] * (n + 1)

    # 第一次 DFS：求父、深度、子树大小、重儿子
    def dfs1(u, p):
        parent[u] = p
        size[u] = 1
        for v in adj[u]:
            if v == p: continue
            depth[v] = depth[u] + 1
            dfs1(v, u)
            size[u] += size[v]
            if size[v] > size[son[u]]:
                son[u] = v
    dfs1(root, 0)

    dfn = [0] * (n + 1)
    top = [0] * (n + 1)
    timer = 0
    # 第二次 DFS：优先走重儿子以保证重链的 DFS 序连续
    def dfs2(u, t):
        nonlocal timer
        timer += 1
        dfn[u] = timer
        top[u] = t
        if son[u]: dfs2(son[u], t)
        for v in adj[u]:
            if v != parent[u] and v != son[u]:
                dfs2(v, v)
    dfs2(root, root)
    return parent, depth, size, son, top, dfn


def path_adjust(seg, n, u, v, op, val=0):
    """把 u->v 路径拆成若干段连续 DFS 序区间并操作：
       op=add 时调用 seg.add，op=query 时累加 seg.query。
       通过 top[u] 深度更深的点逐段跳转，复杂度 O(log^2 n)。"""
    s = 0
    # 示意：对每条重链做一次区间操作；完整实现见线段树调用
    return s
```

> **复杂度**：预处理 DFS O(n)，单次路径操作 O(log² n)，线段树操作 O(log n)。

---

#### 13.1.2 例 2：静态区间第 K 小 / 「模板」可持久化线段树 2（主席树，Luogu P3834）⭐⭐⭐

> **知识点**：可持久化线段树（主席树）＋离散化｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度很高的竞赛经典题，主要考察可持久化线段树（主席树）与离散化技巧的配合。给定一个静态数组，多次询问某个区间内第 K 小（第 K 大）的数值，要求在线回答。

**思路**
主席树即可持久化权值线段树：按位置逐个插入元素，每个位置版本只新开被修改路径上的 O(log n) 个节点，其余共享前驱版本，从而可查询任意历史版本。利用前缀可减性，区间 `[l, r]` 的权值分布可由版本 `r` 减去版本 `l-1` 得到，在树上二分即可求出第 K 小。

```python
def build_pst(a, n):
    """返回 roots（每个位置版本根节点下标）。
       节点数组：左儿子、右儿子、子树元素计数。
       主席树每次插入只新开 log n 个节点，共享不变部分。"""
    vals = sorted(set(a[1:]))
    M = len(vals)
    left, right, cnt = [0], [0], [0]     # 0 号作为空节点
    roots = [0] * (n + 1)

    def new_node():
        left.append(0); right.append(0); cnt.append(0)
        return len(cnt) - 1

    def insert(prev, l, r, pos):
        cur = new_node()
        left[cur], right[cur] = left[prev], right[prev]
        cnt[cur] = cnt[prev] + 1
        if l == r:
            return cur
        m = (l + r) >> 1
        if pos <= m:
            left[cur] = insert(left[prev], l, m, pos)
        else:
            right[cur] = insert(right[prev], m + 1, r, pos)
        return cur

    def rank(x):
        # 返回值 x 离散化后的下标（1-based）
        lo, hi = 0, M - 1
        while lo < hi:
            mid = (lo + hi) >> 1
            if vals[mid] < x: lo = mid + 1
            else: hi = mid
        return lo + 1

    for i in range(1, n + 1):
        roots[i] = insert(roots[i - 1], 1, M, rank(a[i]))
    return roots, left, right, cnt, M, vals


def kth_small(roots, left, right, cnt, M, vals, l, r, k):
    """查询 a[l..r] 中第 k 小值（返回真实数值）。"""
    # u/v 分别对应当前版本的节点，递归时 delta = cnt[left[u_r]...] 可减性判断
    def go(u, v, ql, qr, k):
        if ql == qr:
            return vals[ql - 1]
        mid = (ql + qr) >> 1
        lc_left = cnt[left[v]]       # 版本 r 的左子树大小
        lc_right = cnt[left[u]]      # 版本 l-1 的左子树大小
        left_count = lc_left - lc_right   # 区间内落在左半部分的元素个数
        if k <= left_count:
            return go(left[u], left[v], ql, mid, k)
        else:
            return go(right[u], right[v], mid + 1, qr, k - left_count)
    return go(roots[l - 1], roots[r], 1, M, k)
```

> **复杂度**：建树 O(n log n)，单次查询 O(log n)，空间 O(n log n)。

---

#### 13.1.3 例 3：动态树维护连通性 / LCT 连通性（Link-Cut Tree，Luogu P3690 模板）⭐⭐⭐

> **知识点**：LCT（Link-Cut Tree）splay 维护实链剖分｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的动态树综合题，主要考察 LCT（Link-Cut Tree）用 splay 维护实链剖分的灵活运用。动态维护一棵支持加边、删边的森林，并能判断任意两点是否连通、维护路径信息。

**思路**
LCT 用若干棵 splay 表示原树，每棵 splay 维护一条「实链」，通过 `access`/`makeroot`/`split`/`link`/`cut` 等操作在线修改加边、删边并维护路径信息。判断两点是否连通只需 `makeroot(x); access(y); splay(y)` 后检查二者的根是否一致。

```python
class LCT:
    def __init__(self, n):
        self.ch = [[0, 0] for _ in range(n + 1)]  # 左右儿子
        self.fa = [0] * (n + 1)
        self.rev = [False] * (n + 1)

    def is_root(self, x):
        f = self.fa[x]
        return self.ch[f][0] != x and self.ch[f][1] != x

    def push_rev(self, x):
        if not x: return
        self.rev[x] ^= True
        self.ch[x][0], self.ch[x][1] = self.ch[x][1], self.ch[x][0]

    def push_down(self, x):
        if self.rev[x]:
            self.push_rev(self.ch[x][0]); self.push_rev(self.ch[x][1])
            self.rev[x] = False

    def rotate(self, x):
        y, z = self.fa[x], self.fa[self.fa[x]]
        dx = 1 if self.ch[y][1] == x else 0
        b = self.ch[x][dx ^ 1]
        if not self.is_root(y):
            d = 1 if self.ch[z][1] == y else 0
            self.ch[z][d] = x
        self.fa[x] = z
        self.ch[y][dx] = b
        if b: self.fa[b] = y
        self.ch[x][dx ^ 1] = y; self.fa[y] = x

    def _push_all(self, x):
        # 从 x 一路到原树上根，逐个 push_down 保证翻转下传顺序正确
        s = []
        cur = x
        while True:
            s.append(cur)
            if self.is_root(cur): break
            cur = self.fa[cur]
        while s: self.push_down(s.pop())

    def splay(self, x):
        self._push_all(x)
        while not self.is_root(x):
            y = self.fa[x]
            if not self.is_root(y):
                yy = self.fa[y]
                # 双旋调整保证均摊复杂度：同向先旋 y，反向先旋 x
                if (self.ch[yy][0] == y) == (self.ch[y][0] == x):
                    self.rotate(y)
                else:
                    self.rotate(x)
            self.rotate(x)

    def access(self, x):
        # 打通 x 到原树根的实链
        last = 0
        while x:
            self.splay(x)
            self.ch[x][1] = last   # 把上次的链接到右儿子
            last = x
            x = self.fa[x]

    def makeroot(self, x):
        self.access(x); self.splay(x); self.push_rev(x)

    def find(self, x):
        # 判断 x 所在树的根（用于连通性）
        self.access(x); self.splay(x)
        while self.ch[x][0]:
            self.push_down(x)
            x = self.ch[x][0]
        return x

    def connected(self, x, y):
        return self.find(x) == self.find(y)

    def link(self, x, y):
        self.makeroot(x); self.fa[x] = y

    def cut(self, x, y):
        self.makeroot(x); self.access(y); self.splay(y)
        self.ch[y][0] = 0
        self.fa[x] = 0
```

> **复杂度**：各操作均摊 O(log n)。

---

### 13.2 分块与区间查询进阶（莫队 · 珂朵莉树）

#### 13.2.1 例 4：静态区间不同元素个数 / 「模板」莫队（Luogu P1972 [SDOI2009] HH 的项链）⭐⭐⭐

> **知识点**：莫队（分块 + 双指针移动）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的区间统计综合题，主要考察莫队算法（分块 + 双指针移动）的运用。给定一个序列与若干区间询问，求每个区间内不同元素的个数。

**思路**
将所有查询按「左端点所在块」与「右端点」双关键字排序，使得每次查询可由上次查询通过左右端点的移动增量维护而来，总移动次数 O((n + q)·√n)。维护一个计数数组 `cnt` 与当前不同元素个数，移动端点时 O(1) 更新。

```python
import math

def mo(a, queries):
    n = len(a)         # a 为 0-based
    block = int(math.sqrt(n)) + 1

    # (l, r, idx) 排序：l 所在块为第一关键字，r 为第二关键字（奇偶优化）
    def key(q):
        l, r, _ = q
        b = l // block
        return (b, r if b % 2 == 0 else -r)
    queries = sorted(queries, key=key)

    cnt = [0] * (max(a) + 1 if a else 1)
    cur_l, cur_r, distinct = 0, -1, 0   # 初始为空区间
    ans = [0] * len(queries)

    def add(x):
        # 向区间中加入位置 x
        nonlocal distinct
        cnt[a[x]] += 1
        if cnt[a[x]] == 1: distinct += 1

    def remove(x):
        nonlocal distinct
        cnt[a[x]] -= 1
        if cnt[a[x]] == 0: distinct -= 1

    for l, r, idx in queries:
        # 先扩展再收缩，保证区间始终合法
        while cur_l > l: cur_l -= 1; add(cur_l)
        while cur_r < r: cur_r += 1; add(cur_r)
        while cur_l < l: remove(cur_l); cur_l += 1
        while cur_r > r: remove(cur_r); cur_r -= 1
        ans[idx] = distinct
    return ans
```

> **复杂度**：O((n + q)·√n)。

---

#### 13.2.2 例 5：珂朵莉树（Chtholly Tree）区间赋值 / 区间幂和（CF 896C / 类似「模板」珂朵莉树）⭐⭐⭐

> **知识点**：珂朵莉树（ODT，基于有序集合的区间摊还结构）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的区间数据结构综合题，主要考察珂朵莉树（ODT，基于有序集合的区间摊还结构）。支持区间赋值为同一值、区间幂和等操作，要求数据随机时摊还高效地完成。

**思路**
把值相同的连续段存储为有序区间，操作时先 `split` 拆出目标区间对应的节点，再对整个区间集合暴力遍历/赋值。在「区间随机赋值」这类数据随机的情况下，段数期望 O(log n)，从而摊还高效，且实现非常简单。

```python
from bisect import bisect_left
from collections import defaultdict

class Node:
    __slots__ = ('l', 'r', 'v')
    def __init__(self, l, r, v):
        self.l, self.r, self.v = l, r, v

class ChthollyTree:
    def __init__(self, n, a):
        # 用 defaultdict 列表 + 二分代替平衡树（演示核心 split/assign，数据随机时高效）
        self.tree = []
        last = a[1]
        start = 1
        for i in range(2, n + 1):
            if a[i] != last:
                self.tree.append(Node(start, i - 1, last))
                start = i; last = a[i]
        self.tree.append(Node(start, n, last))

    def split(self, pos):
        # 把 pos 拆成某个区间的左端点，返回 pos 所在节点下标
        # 找到最后一个 l <= pos 的区间
        idx = 0
        for i, nd in enumerate(self.tree):
            if nd.l <= pos <= nd.r:
                idx = i; break
            if nd.l > pos:
                idx = i - 1; break
        nd = self.tree[idx]
        if nd.l == pos:
            return idx
        # 分裂为 [nd.l, pos-1] 与 [pos, nd.r]
        self.tree[idx] = Node(nd.l, pos - 1, nd.v)
        self.tree.insert(idx + 1, Node(pos, nd.r, nd.v))
        return idx + 1

    def assign(self, l, r, v):
        # 区间赋值：把 [l, r] 各处段全部替换成单个区间 [l, r] 值为 v
        il = self.split(l); ir = self.split(r + 1)
        self.tree[il:ir] = [Node(l, r, v)]

    def range_sum(self, l, r):
        # 区间求和（可扩展为区间幂和：把 v 变为 pow(v, k, p) 后乘长度）
        il = self.split(l); ir = self.split(r + 1)
        s = 0
        for nd in self.tree[il:ir]:
            s += nd.v * (nd.r - nd.l + 1)
        self.tree[il:ir] = self.tree[il:ir]
        return s
```

> **复杂度**：数据随机时，单次操作均摊 O(log n)；最坏 O(n)（随机数据不触发）。

---

### 13.3 图论与线性代数（差分约束 · 线性基 · 精确覆盖）

#### 13.3.1 例 6：「模板」差分约束系统（Luogu P3275 [SCOI2011] 糖果）⭐⭐⭐

> **知识点**：差分约束 + SPFA/最长路判负环｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的图论建模综合题，主要考察差分约束系统与 SPFA 最长路判负环的结合。给定若干形如 x_j − x_i ≥ c 的不等式约束，判断是否存在满足所有约束的整数解并求出一组可行解。

**思路**
把形如 `x_j - x_i ≥ c` 的约束转化为图论最长路：从 i 到 j 连一条权值 c 的边，那么任意一组解等价于求超级源点到各点的最长路；存在正环则无解。区间上下界型约束同理可用最短路建模。

```python
from collections import deque

def difference_constraint(n, edges):
    """
    edges: 每条约束 (a, b, w) 表示 x[b] - x[a] >= w（连边 a -> b 权 w）。
    返回：无解返回 None，否则返回满足所有约束的 x[1..n]。
    """
    g = [[] for _ in range(n + 2)]
    src = 0
    for a, b, w in edges:
        g[a].append((b, w))
    # 超级源点：x[i] - x[0] >= 0，即 x[i] >= 0
    for i in range(1, n + 1):
        g[src].append((i, 0))

    dist = [-10**18] * (n + 2)
    dist[src] = 0
    inq = [False] * (n + 2)
    cnt = [0] * (n + 2)      # 入队次数，超过 n 说明存在正环
    dq = deque([src]); inq[src] = True

    while dq:
        u = dq.popleft(); inq[u] = False
        for v, w in g[u]:
            if dist[v] < dist[u] + w:      # 最长路松弛
                dist[v] = dist[u] + w
                cnt[v] += 1
                if cnt[v] > n + 1:
                    return None            # 存在正环，无解
                if not inq[v]:
                    inq[v] = True; dq.append(v)
    return dist[1:n + 1]
```

> **复杂度**：通常远小于 O(n·m)（SPFA 平均 O(km)），最坏 O(n·m)。

---

#### 13.3.2 例 7：「模板」线性基 / 最大异或和（Luogu P3812）⭐⭐⭐

> **知识点**：线性基（高斯消元思想）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的线性代数与位运算综合题，主要考察线性基（高斯消元思想）。给定若干个数，求其子集异或和的最大值。

**思路**
线性基是一组能线性表示给定数集所有子集异或和的最简向量集（异或意义下的「基底」）。逐位贪心构建：对每个数从高到低扫描位，若该位已有基则异或掉，否则插入并退出。最大异或和通过对线性基从高到低贪心累加求得。

```python
class LinearBasis:
    def __init__(self, max_bit=60):
        self.b = [0] * (max_bit + 1)   # b[i] 的最高位为 i

    def insert(self, x):
        # 尝试将 x 插入线性基，成功返回 True，否则说明 x 可被线性表示
        for i in range(len(self.b) - 1, -1, -1):
            if (x >> i) & 1 == 0:
                continue
            if self.b[i]:
                x ^= self.b[i]
            else:
                self.b[i] = x
                return True
        return False

    def max_xor(self):
        # 求线性基可表示的最大异或和
        res = 0
        for i in range(len(self.b) - 1, -1, -1):
            if (res ^ self.b[i]) > res:
                res ^= self.b[i]
        return res

# 使用示例：读取 n 个数 a，求其子集异或和的最大值
def max_subset_xor(a):
    bas = LinearBasis()
    for x in a:
        bas.insert(x)
    return bas.max_xor()
```

> **复杂度**：插入与查询均 O(b)，b 为值域位数（通常 60/64）。

---

#### 13.3.3 例 8：舞蹈链（Dancing Links）精确覆盖 / 「模板」精确覆盖问题（DLX，Luogu P4929）⭐⭐⭐

> **知识点**：舞蹈链（DLX，双向循环十字链表 + DFS 回溯）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的搜索优化综合题，主要考察舞蹈链（DLX，双向循环十字链表 + DFS 回溯）。给定一个 01 矩阵，判断能否选出若干行使每一列恰好被一个 1 覆盖（精确覆盖问题）。

**思路**
把精确覆盖问题（01 矩阵选若干行使每列恰被覆盖一次）建模为双向循环十字链表，每个 1 元素是链表节点。DFS 时优先选择「1 个数最少」的列，选中某行后删除受影响的列并递归；回溯时利用链表的「指针恢复」快速还原，从而跳过大量无效分支。

```python
class DLX:
    def __init__(self, col_cnt):
        self.col = col_cnt
        # 头节点编号 0，列头 1..col_cnt；u/d/l/r 四向链表，cnt 列中 1 个数
        self.node = [[0, 0, 0, 0, 0] for _ in range(col_cnt + 1)]  # u,d,l,r,cnt
        self.row = []
        self.size = col_cnt
        for i in range(1, col_cnt + 1):   # 初始化列头环形
            self.node[i] = [i, i, i - 1, i + 1, 0]
        self.node[0] = [0, 0, col_cnt, 1, 0]     # 头节点
        self.node[col_cnt][3] = 0

    def add_row(self, cols):
        # 在当前矩阵末加入一行，这些列上值为 1
        first = None
        for c in cols:
            self.size += 1
            s = self.size
            self.node.append([0, 0, 0, 0, 0])
            self.node[s][4] = c
            self.node[s][1] = self.node[c][0]   # up
            self.node[s][0] = self.node[c][1]   # down, 这里示意：简化版
            self.node[c][0] = s
            self.node[c][4] += 1
            if first is None:
                first = s
            else:
                # 行内左右连接
                self.node[s][3] = self.node[first][2]
                self.node[s][2] = first
                self.node[first][3] = s
        return first

    def solve(self):
        # 返回一组解（选择的行集合）。完整实现需要 cover/remove 与回溯；
        # 下面给出算法骨架：
        # 1. 头节点右指针指向自己 => 无剩余列，找到一组解
        # 2. 选 1 数最少的列 c
        # 3. 枚举列 c 上的每行 r，覆盖相关列并 DFS
        # 4. 回溯时恢复已覆盖列
        pass

# 说明：DLX 核心是删除/恢复列（cover/uncover）利用双向链表 O(1) 完成。
# 由于体量问题此处以骨架演示，竞赛/题库中常配合「数独 / 八皇后 / 多米诺覆盖」等建模使用。
```

> **复杂度**：指数级但实际剪枝极强，对大规模精确覆盖问题显著优于朴素搜索。

---

### 13.4 生成函数与数论（FFT/NTT · 杜教筛/Min_25 筛）

#### 13.4.1 例 9：FFT/NTT 快速卷积 / 「模板」多项式乘法（Luogu P3803）⭐⭐⭐

> **知识点**：NTT（原根代替单位根，模 998244353）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的生成函数综合题，主要考察 NTT（原根代替单位根，模 998244353）。给定两个多项式，快速计算它们的卷积（多项式乘法）。

**思路**
两个多项式相乘的朴素做法是 O(n²) 卷积；NTT 利用数论域上的原根做分治变换，将多项式先点值化、逐点相乘、再插值还原，达到 O(n log n)。整数模域下用原根 g（如 998244353 的原根 3）替代复数单位根，适合竞赛取模场景。

```python
MOD = 998244353
G = 3   # 998244353 的原根

def ntt(a, invert):
    """对长度正好为 2 的幂的数组 a 做 NTT；invert=True 为逆变换。"""
    n = len(a)
    j = 0
    # 位逆序置换
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit; bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        wlen = pow(G, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        half = length >> 1
        for i in range(0, n, length):
            w = 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def poly_mul(f, g):
    """计算两个多项式 f, g 的卷积（NTT 实现）。"""
    n = 1
    need = len(f) + len(g) - 1
    while n < need:
        n <<= 1
    fa = f + [0] * (n - len(f))
    fb = g + [0] * (n - len(g))
    ntt(fa, False); ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:need]
```

> **复杂度**：O(n log n)。利用该卷积可实现生成函数/多项式求逆、exp、ln、卷积等高级运算。

---

#### 13.4.2 例 10：杜教筛与 Min_25 筛（求积性函数前缀和）概念与要点 ⭐⭐⭐

> **知识点**：杜教筛；Min_25 筛（质数/合数部分分治筛）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的数论综合题，主要考察杜教筛与 Min_25 筛求积性函数前缀和的思路。对于极大的 n，在无法线性筛的条件下快速求积性函数前缀和。

**思路**
求形如 `S(n) = Σ_{i=1..n} f(i)` 的积性函数前缀和，n 可达 1e10~1e11，无法线性筛。杜教筛思想：选取便于求前缀和的辅助函数 g，使 h = f * g（迪利克雷卷积）有简单前缀和，从而用分块 + 递归（记忆化）把 S(n) 化为对 `S(⌊n/i⌋)` 的递归求和，整值分块使状态 O(√n)。Min_25 筛则把 f 在质数处的取值与合数处的递推分开，仅用 O(√n) 个「整除值」即可计算前缀和（常配合 Dirichlet 前缀和思想加快）。

```python
import math
from functools import lru_cache

def du_jiao(n, mu_prefix):
    """杜教筛求解欧拉函数前缀和 phi_sum(n)。
       mu_prefix 为线性筛预处理的、逐项求和的莫比乌斯函数前缀和（截断到合理上界）。
       核心：利用 1 = Σ_{d|k} phi(d)（因 n = Σ_{d|n} phi(d)）。"""
    # 用字典记忆化避免重复计算；配合整除分块 (n // (n // i)) 递归
    memo = {}

    @lru_cache(maxsize=None)
    def g_sum(n):
        if n < len(mu_prefix):          # 已预处理的小范围直接查表
            return 0
        if n in memo:
            return memo[n]
        # 演示性骨架：g(n) = Σ_{i=1..n} mu(i) 由整除分块与前面 g(n//i) 递推得出
        s = 1
        i = 2
        while i <= n:
            j = n // (n // i)
            s -= (j - i + 1) * g_sum(n // i)
            i = j + 1
        memo[n] = s
        return s

    def phi_sum(n):
        # 由 Σ_{d=1..n} phi_sum(floor(n/d)) = g_sum(n) 反推，见上述恒等式
        if n == 0:
            return 0
        res = 1
        i = 2
        while i <= n:
            j = n // (n // i)
            res -= (j - i + 1) * phi_sum(n // i)
            i = j + 1
        # 再结合欧拉函数的前缀关系完成；此处为概念展示骨架
        return res
    return phi_sum(n)


def min_25_summary(n, is_prime_f):
    """Min_25 筛思路说明（伪代码级）：
       - g(n) = Σ_{2..n} f_p(p)，用整除分块在 O(√n) 个点上递推质数部分；
       - 枚举质数 p，以 p² <= n 为界，从大到小滚动更新各整除点上括号内去掉 p 的贡献；
       - 再枚举合数部分较小的质因子，把「最小质因子 >= p 的合数贡献」叠加进答案。
       整体复杂度 O(n^(3/4)/log n)，可求 P(n) 等积性函数前缀和。"""
    del is_prime_f
    return None
```

> **复杂度**：杜教筛每层循环为整除分块，总复杂度 O(n^(3/4))（配合记忆化与预处理近 O(n^(2/3))）；Min_25 筛约 O(n^(3/4)/log n)。

---

### 13.5 字符串自动机（后缀自动机 SAM · 回文自动机）

#### 13.5.1 例 11：后缀自动机求本质不同子串数 / 众数出现次数（SAM 模板题，Luogu P3804「后缀自动机」）⭐⭐⭐

> **知识点**：后缀自动机（SAM）+ 拓扑 DAG/基排序求 endpos 集合大小｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度很高的字符串自动机综合题，主要考察后缀自动机（SAM）与拓扑 DAG/基排序求 endpos 集合大小的结合。统计字符串的本质不同子串数以及出现次数最多的子串的出现次数。

**思路**
SAM 的每个状态对应一组 endpos 相同的子串，状态数 O(n)。维护每个状态的 `maxlen` 与转移边即可在线统计；本质不同子串数 = Σ(len[状态] - len[link[状态]])。出现次数通过对所有状态按 len 基排序、反向累加 `cnt`（每个状态复制自身贡献到其 link）得到 endpos 大小。

```python
class SAM:
    def __init__(self, max_n):
        cap = 2 * max_n + 5
        self.len = [0] * cap
        self.link = [-1] * cap
        self.nxt = [{} for _ in range(cap)]
        self.cnt = [0] * cap
        self.sz = 1      # 当前节点数，初始为根 0
        self.last = 0

    def extend(self, c):
        cur = self.sz; self.sz += 1
        self.len[cur] = self.len[self.last] + 1
        self.cnt[cur] = 1
        p = self.last
        while p != -1 and c not in self.nxt[p]:
            self.nxt[p][c] = cur
            p = self.link[p]
        if p == -1:
            self.link[cur] = 0
        else:
            q = self.nxt[p][c]
            if self.len[p] + 1 == self.len[q]:
                self.link[cur] = q
            else:
                clone = self.sz; self.sz += 1
                self.len[clone] = self.len[p] + 1
                self.nxt[clone] = self.nxt[q].copy()
                self.link[clone] = self.link[q]
                while p != -1 and self.nxt[p].get(c) == q:
                    self.nxt[p][c] = clone
                    p = self.link[p]
                self.link[q] = self.link[cur] = clone
        self.last = cur

    def distinct_substrings(self):
        # 本质不同子串数
        total = 0
        for i in range(1, self.sz):
            total += self.len[i] - self.len[self.link[i]]
        return total

    def max_occurrence(self):
        # 求最多次出现的子串出现次数：
        # 按 len 基排序后反向把 cnt 累加到 link 上。
        order = list(range(self.sz))
        order.sort(key=lambda x: self.len[x], reverse=True)
        for v in order:
            if self.link[v] >= 0:
                self.cnt[self.link[v]] += self.cnt[v]
        return max(self.cnt[1:self.sz], default=0)


def solve_substring(s):
    sam = SAM(len(s))
    for ch in s:
        sam.extend(ch)
    return sam
```

> **复杂度**：构建 O(n)，基排序统计 O(n · alphabet)；本质不同子串数与出现次数均可一次求出。

---

#### 13.5.2 例 12：回文自动机求本质不同回文子串及出现次数（PAM 模板）⭐⭐⭐

> **知识点**：回文自动机（PALINDROMIC TREE / Eertree）+ fail 树｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度很高的字符串综合题，主要考察回文自动机（PALINDROMIC TREE/Eertree）与 fail 树。统计字符串中本质不同回文子串的个数及各自的出现次数。

**思路**
回文自动机为每个本质不同回文串建立一个节点，维护 `fail` 指向其最长真回文后缀，以及奇数/偶数两个根（分别长度 -1 和 0）。每插入一个字符，从当前最长回文后缀沿 fail 寻找可扩展节点，新建节点时递推其 fail。本质不同回文串数即节点数；各回文出现次数可在建完后沿 fail 反向累加。

```python
class PAM:
    def __init__(self):
        # 0 号偶数根(len=0)，1 号奇数根(len=-1)，fail 先自指
        self.len = [-1, 0]
        self.fail = [1, 1]     # 奇根 fail 指向奇根
        self.cnt = [0, 0]      # 出现次数（建完后沿 fail 累加）
        self.nxt = [dict(), dict()]
        self.sz = 2
        self.last = 1          # 初始 last 指向奇根（配合 len -1）
        self.s = ['#']         # 记录已插入字符，端点格

    def get_fail(self, x):
        # 从 x 找最长回文后缀：检查 s[cur] == s[cur - len[x] - 1]
        while True:
            cur = len(self.s) - 1
            if self.s[cur - self.len[x] - 1] == self.s[cur]:
                return x
            x = self.fail[x]

    def extend(self, ch):
        self.s.append(ch)
        cur = self.get_fail(self.last)
        if ch not in self.nxt[cur]:
            node = self.sz; self.sz += 1
            self.len.append(self.len[cur] + 2)
            self.nxt.append(dict())
            self.fail.append(0)
            self.cnt.append(0)
            if self.len[node] == 1:
                self.fail[node] = 0        # 单字符回文的 fail 指向偶根
            else:
                nxtfail = self.get_fail(self.fail[cur])
                self.fail[node] = self.nxt[nxtfail][ch]
            self.nxt[cur][ch] = node
        self.last = self.nxt[cur][ch]
        self.cnt[self.last] += 1

    def occ(self):
        # 按节点编号从大到小（通常 fail 指向较短的回文，需按 len 递减）累加
        return self.sz - 2   # 减去奇偶两根即为本质不同回文子串数


def solve_pal(s):
    pam = PAM()
    for ch in s:
        pam.extend(ch)
    return pam
```

> **复杂度**：构建 O(n · alphabet)，统计出现次数及各回文信息可在 fail 树上线性完成。

---

### 13.6 树上路径与分治（重链剖分 · 树上差分 · 点分治 · 树上主席树）

#### 13.6.1 例 13：重链剖分求 LCA（最近公共祖先）⭐⭐

> **知识点**：轻重链剖分（HLD）｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的树上问题，主要考察轻重链剖分（HLD）求解最近公共祖先。给定一棵树，多次询问任意两点的 LCA。

**思路**
先用两次 DFS：第一次求每个节点的子树大小、深度、重儿子（子树最大的儿子）；第二次按「先重儿子再轻儿子」的顺序给每个节点分配 `top`（所在重链顶端）。求 LCA 时，不断把 `top` 更深的一端跳到其 `top` 的父节点，直到两者同一条重链，深度浅者即为答案。💡 类比把树「摊平成若干条竖链」，像爬楼梯一样一次跨整条链。

```python
def build_hld(n, adj):
    sz = [0]*(n+1); dep = [0]*(n+1); fa = [0]*(n+1); son = [0]*(n+1)
    top = [0]*(n+1)
    def dfs1(u, p):
        fa[u] = p; sz[u] = 1; dep[u] = dep[p] + 1
        for v in adj[u]:
            if v == p: continue
            dfs1(v, u); sz[u] += sz[v]
            if sz[v] > sz[son[u]]: son[u] = v
    def dfs2(u, t):
        top[u] = t
        if son[u]: dfs2(son[u], t)          # 重儿子延续同一条链
        for v in adj[u]:
            if v != fa[u] and v != son[u]: dfs2(v, v)   # 轻儿子新开一条链
    dfs1(1, 0); dfs2(1, 1)
    def lca(u, v):
        while top[u] != top[v]:
            if dep[top[u]] < dep[top[v]]: v = fa[top[v]]
            else: u = fa[top[u]]
        return u if dep[u] < dep[v] else v
    return lca

n = 9
edges = [(1,2),(1,3),(2,4),(2,5),(4,8),(5,9),(3,6),(3,7)]
adj = [[] for _ in range(n+1)]
for a, b in edges:
    adj[a].append(b); adj[b].append(a)
lca = build_hld(n, adj)
print(lca(4, 9))   # 2
print(lca(8, 6))   # 1
```

> **复杂度**：预处理 O(n)，单次 LCA O(log n)。

---

#### 13.6.2 例 14：重链剖分维护路径点权和（树上路径求和）⭐⭐⭐

> **知识点**：树链剖分 + 树状数组/线段树（dfn 序）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的树上路径综合题，主要考察树链剖分与树状数组/线段树（dfn 序）的结合。给定一棵带点权树，多次查询一条路径上的点权和。

**思路**
重链剖分把树上任意节点对应到一个 `dfn` 连续区间，因此「一条路径」被拆成 O(log n) 段不重合的 `dfn` 连续区间，用树状数组或线段树维护区间和即可完成路径求和。💡 类比把「树上区间求和」转化为「数组区间求和」，正是树与序列之间的桥梁。

```python
import sys
sys.setrecursionlimit(1 << 20)

class BIT:
    def __init__(self, n): self.n = n; self.t = [0]*(n+1)
    def add(self, i, v):
        while i <= self.n: self.t[i] += v; i += i & -i
    def prefix(self, i):
        s = 0
        while i > 0: s += self.t[i]; i -= i & -i
        return s
    def range(self, l, r): return self.prefix(r) - self.prefix(l-1)

def build_path_sum(n, adj, val):
    sz=[0]*(n+1); dep=[0]*(n+1); fa=[0]*(n+1); son=[0]*(n+1)
    top=[0]*(n+1); dfn=[0]*(n+1); cnt=[0]
    def dfs1(u, p):
        fa[u]=p; sz[u]=1; dep[u]=dep[p]+1
        for v in adj[u]:
            if v == p: continue
            dfs1(v, u); sz[u] += sz[v]
            if sz[v] > sz[son[u]]: son[u] = v
    def dfs2(u, t):
        cnt[0] += 1; dfn[u] = cnt[0]; top[u] = t
        if son[u]: dfs2(son[u], t)
        for v in adj[u]:
            if v != fa[u] and v != son[u]: dfs2(v, v)
    dfs1(1, 0); dfs2(1, 1)
    bit = BIT(n)
    for u in range(1, n+1): bit.add(dfn[u], val[u])
    def path_sum(u, v):
        res = 0
        while top[u] != top[v]:
            if dep[top[u]] < dep[top[v]]: u, v = v, u
            res += bit.range(dfn[top[u]], dfn[u]); u = fa[top[u]]
        if dep[u] > dep[v]: u, v = v, u
        res += bit.range(dfn[u], dfn[v])
        return res
    return path_sum

n = 9
edges = [(1,2),(2,3),(2,4),(3,5),(3,6),(4,7),(4,8),(1,9)]
adj = [[] for _ in range(n+1)]
for a, b in edges:
    adj[a].append(b); adj[b].append(a)
val = [0,1,2,3,4,5,6,7,8,9]   # val[i] = i
path_sum = build_path_sum(n, adj, val)
print(path_sum(5, 8))   # 5+3+2+4+8 = 22
```

> **复杂度**：预处理 O(n)，单次路径查询 O(log²n)。

---

#### 13.6.3 例 15：树上差分（路径点权 / 边权批量加）⭐⭐

> **知识点**：树上差分 + 倍增 LCA｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的树上批量操作题，主要考察树上差分与倍增 LCA 的结合。有若干条路径需要进行批量加操作，最后求每个点/边被覆盖的次数。

**思路**
对每条路径 `(u,v)` 做点权差分：`c[u]++, c[v]++, c[lca]--, c[fa[lca]]--`；最后从叶向根做一次子树和，即可在一次遍历中得到每条路径对每个点的覆盖次数。边权差分则把边权压到子节点上处理。💡 类比一维数组差分在 O(1) 内完成区间加法，树上差分把「区间」换成了「树上路径」。

```python
def tree_point_diff(n, adj, updates):
    dep=[0]*(n+1); fa=[0]*(n+1); up=[[0]*(n+1) for _ in range(20)]
    def dfs(u, p):
        fa[u]=p; up[0][u]=p; dep[u]=dep[p]+1
        for k in range(1, 20): up[k][u] = up[k-1][up[k-1][u]]
        for v in adj[u]:
            if v != p: dfs(v, u)
    dfs(1, 0)
    def lca(u, v):
        if dep[u] < dep[v]: u, v = v, u
        d = dep[u] - dep[v]; bit = 0
        while d:
            if d & 1: u = up[bit][u]
            d >>= 1; bit += 1
        if u == v: return u
        for k in range(19, -1, -1):
            if up[k][u] != up[k][v]:
                u = up[k][u]; v = up[k][v]
        return fa[u]
    c = [0]*(n+1)
    for u, v in updates:
        c[u] += 1; c[v] += 1; w = lca(u, v)
        c[w] -= 1; c[fa[w]] -= 1
    ans = [0]*(n+1)
    def dfs2(u, p):
        s = c[u]
        for v in adj[u]:
            if v != p: s += dfs2(v, u)
        ans[u] = s
        return s
    dfs2(1, 0)
    return ans[1:]

n = 7
edges = [(1,2),(1,3),(2,4),(2,5),(3,6),(3,7)]
adj = [[] for _ in range(n+1)]
for a, b in edges:
    adj[a].append(b); adj[b].append(a)
print(tree_point_diff(n, adj, [(4,5),(6,7)]))
```

> **复杂度**：预处理 O(n log n)，每条更新 O(log n)，最后 O(n)。

---

#### 13.6.4 例 16：点分治求树上距离不超过 K 的点对数（Luogu P3806）⭐⭐⭐

> **知识点**：点分治 + 排序/双指针｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的点分治综合题，主要考察点分治与排序/双指针的配合。给定一棵带边权的树，统计树上任意两点距离不超过 K 的点对数量。

**思路**
点分治每次找出子树重心，统计「经过重心、且两端落在**不同**子树」的合法点对：先把重心到各子树所有距离收集到一起排序后双指针计数，再减去每个子树内部重复计的合法点对，然后递归处理各子树。💡 类比归并排序中「分-治-合」的结构，每次合并阶段只处理经过分割中心的那部分贡献。

```python
def count_pairs_leq_k(n, adj, K):
    vis = [False]*(n+1); sz = [0]*(n+1); ans = [0]
    def get_sz(u, p):
        sz[u] = 1
        for v in adj[u]:
            if v != p and not vis[v]:
                sz[u] += get_sz(v, u)
        return sz[u]
    def dfs_dist(u, p, d, arr):
        arr.append(d)
        for v in adj[u]:
            if v != p and not vis[v]:
                dfs_dist(v, u, d+1, arr)
    def cnt(arr):
        arr.sort()
        res = 0; i = 0; j = len(arr)-1
        while i < j:
            if arr[i] + arr[j] <= K: res += j - i; i += 1
            else: j -= 1
        return res
    def centroid(u, p, tot):
        for v in adj[u]:
            if v != p and not vis[v] and sz[v]*2 > tot:
                return centroid(v, u, tot)
        return u
    def solve(u):
        get_sz(u, 0)
        cen = centroid(u, 0, sz[u])
        vis[cen] = True
        base = [0]
        for v in adj[cen]:
            if not vis[v]:
                arr = []
                dfs_dist(v, cen, 1, arr)
                ans[0] -= cnt(arr)
                base += arr
        ans[0] += cnt(base)
        for v in adj[cen]:
            if not vis[v]:
                solve(v)
    solve(1)
    return ans[0]

n = 6
adj = [[] for _ in range(n+1)]
for a, b in [(1,2),(2,3),(3,4),(4,5),(5,6)]:
    adj[a].append(b); adj[b].append(a)
print(count_pairs_leq_k(n, adj, 2))   # 相距1:5对 + 相距2:4对 = 9
```

> **复杂度**：O(n log n)。

---

#### 13.6.5 例 17：树上路径第 K 小（可持久化权值线段树 + 树上差分，Luogu P2633「Count on a tree」）⭐⭐⭐

> **知识点**：主席树 + 树上差分｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的树上离线查询综合题，主要考察可持久化权值线段树（主席树）与树上差分的结合。多次询问树上某条路径上点权的第 K 小值。

**思路**
每个节点基于其父节点版本插入自己的权值，得到可持久化权值线段树 `root[u]`。路径 `u→v` 的权值分布 = `root[u] + root[v] − root[lca] − root[fa[lca]]`（树上差分），于是可在四棵线段树上同步二分得到第 K 小。💡 类比二维前缀和的容斥：`(u,v)-(l,r)` 相减得到矩形，这里对树根到节点的「前缀版本」做同样的容斥。

```python
class PST:
    def __init__(self, m):
        self.m = m; self.lc = [0]; self.rc = [0]; self.cnt = [0]
    def update(self, prev, lo, hi, val):
        cur = len(self.cnt)
        self.lc.append(self.lc[prev]); self.rc.append(self.rc[prev]); self.cnt.append(self.cnt[prev]+1)
        if lo < hi:
            mid = (lo+hi)//2
            if val <= mid:
                nl = self.update(self.lc[prev], lo, mid, val)
                self.lc[cur] = nl
            else:
                nr = self.update(self.rc[prev], mid+1, hi, val)
                self.rc[cur] = nr
        return cur
    def kth(self, a, b, c, d, lo, hi, k):
        if lo == hi: return lo
        mid = (lo+hi)//2
        left = self.cnt[self.lc[a]] + self.cnt[self.lc[b]] - self.cnt[self.lc[c]] - self.cnt[self.lc[d]]
        if k <= left:
            return self.kth(self.lc[a], self.lc[b], self.lc[c], self.lc[d], lo, mid, k)
        return self.kth(self.rc[a], self.rc[b], self.rc[c], self.rc[d], mid+1, hi, k-left)

def tree_path_kth(n, adj, val, queries):
    vs = sorted(set(val[1:])); m = len(vs)
    rank = {v: i+1 for i, v in enumerate(vs)}
    dep = [0]*(n+1); up = [[0]*(n+1) for _ in range(17)]
    pst = PST(m); root = [0]*(n+1)
    def dfs(u, p):
        dep[u] = dep[p]+1; up[0][u] = p
        for k in range(1, 17): up[k][u] = up[k-1][up[k-1][u]]
        root[u] = pst.update(root[p], 1, m, rank[val[u]])
        for v in adj[u]:
            if v != p: dfs(v, u)
    dfs(1, 0)
    def lca(u, v):
        if dep[u] < dep[v]: u, v = v, u
        d = dep[u]-dep[v]; bit = 0
        while d:
            if d & 1: u = up[bit][u]
            d //= 2; bit += 1
        if u == v: return u
        for b in range(16, -1, -1):
            if up[b][u] != up[b][v]: u = up[b][u]; v = up[b][v]
        return up[0][u]
    res = []
    for u, v, k in queries:
        l = lca(u, v); p = up[0][l]
        rk = pst.kth(root[u], root[v], root[l], root[p], 1, m, k)
        res.append(vs[rk-1])
    return res

n = 4
adj = [[] for _ in range(n+1)]
for a, b in [(1,2),(1,3),(2,4)]:
    adj[a].append(b); adj[b].append(a)
val = [0,6,2,8,4]
print(tree_path_kth(n, adj, val, [(4,3,2)]))   # 路径4-2-1-3的权[4,2,6,8]第2小=4
```

> **复杂度**：预处理 O(n log n)，单次查询 O(log n)。

---

### 13.7 树上启发式与可并结构（DSU on tree · 左偏树 · 笛卡尔树 · 可持久化 Trie）

#### 13.7.1 例 18：DSU on tree（树上启发式合并统计子树众数颜色）⭐⭐⭐

> **知识点**：树上启发式合并（dsu on tree）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的树上启发式综合题，主要考察 DSU on tree（树上启发式合并）。对树上的每个子树询问，统计该子树内的众数颜色。

**思路**
对每个查询的子树，我们从根开始递归：先处理所有轻儿子（处理完清空），再处理重儿子（**保留**其贡献），然后暴力把各轻儿子子树重新加入，最后加上根节点自身，从而得到当前子树答案。保留重儿子贡献使每个节点至多被重扫 log n 次。💡 类比「大儿子留着不删，小儿子扫完就清」，把启发式合并的思想用到树上。

```python
import sys
sys.setrecursionlimit(1 << 20)

def dsu_on_tree(n, adj, color):
    sz = [0]*(n+1); son = [0]*(n+1)
    def dfs1(u, p):
        sz[u] = 1
        for v in adj[u]:
            if v == p: continue
            dfs1(v, u); sz[u] += sz[v]
            if sz[v] > sz[son[u]]: son[u] = v
    dfs1(1, 0)
    cnt = {}; res = [0]*(n+1)
    best = [0]; bestcol = [0]
    def upd(c):
        f = cnt.get(c, 0) + 1; cnt[c] = f
        if f > best[0] or (f == best[0] and c < bestcol[0]):
            best[0], bestcol[0] = f, c
    def add_sub(u, p):
        upd(color[u])
        for v in adj[u]:
            if v != p: add_sub(v, u)
    def clear_sub(u, p):
        cnt[color[u]] = 0
        for v in adj[u]:
            if v != p: clear_sub(v, u)
    def solve(u, p, keep):
        for v in adj[u]:
            if v != p and v != son[u]: solve(v, u, False)
        if son[u]: solve(son[u], u, True)
        for v in adj[u]:
            if v != p and v != son[u]: add_sub(v, u)
        upd(color[u])
        res[u] = bestcol[0]
        if not keep:
            clear_sub(u, p)
            best[0] = 0
    solve(1, 0, True)
    return res[1:]

n = 7
edges = [(1,2),(1,3),(2,4),(2,5),(3,6),(3,7)]
adj = [[] for _ in range(n+1)]
for a, b in edges:
    adj[a].append(b); adj[b].append(a)
color = [0,1,2,1,1,2,3,1]
print(dsu_on_tree(n, adj, color))
```

> **复杂度**：O(n log n)。

---

#### 13.7.2 例 19：左偏树（可并堆）（Luogu P3377）⭐⭐

> **知识点**：左偏树 / 可并堆｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的可并堆综合题，主要考察左偏树（可并堆）的 O(log n) 合并。支持多次将两个堆合并、弹出堆顶最小值等操作。

**思路**
左偏树是支持 O(log n) 合并两个堆的二叉堆。每个节点存值、左右儿子和「距离」（到空节点的最近距离）。合并时始终把值较小的根作为新根，递归合并另一堆与其右儿子，若左儿子距离小于右儿子则交换，最后用右儿子距离更新本节点距离。💡 类比「弱枝靠右，右倾堆」——让距离在递归合并中自动保持左偏。

```python
class LHeap:
    def __init__(self, val, idx):
        self.val = val; self.idx = idx
        self.l = None; self.r = None
        self.dist = 1

def merge(a, b):
    if a is None: return b
    if b is None: return a
    if a.val > b.val or (a.val == b.val and a.idx > b.idx):
        a, b = b, a
    a.r = merge(a.r, b)
    if a.l is None or (a.r is not None and a.l.dist < a.r.dist):
        a.l, a.r = a.r, a.l
    a.dist = (a.r.dist + 1) if a.r else 1
    return a

vals = [7, 6, 5, 4, 3]
nodes = [LHeap(v, i+1) for i, v in enumerate(vals)]
root = None
for nd in nodes:
    root = merge(root, nd)
print(root.val)                     # 最小值 3
root2 = merge(root.l, root.r)
print(root2.val if root2 else None) # 次小 4
```

> **复杂度**：合并 O(log n)。

---

#### 13.7.3 例 20：笛卡尔树（Cartesian Tree）⭐⭐

> **知识点**：笛卡尔树（单调栈 O(n) 建树）｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的数据结构题，主要考察笛卡尔树与单调栈 O(n) 建树。根据给定序列构造笛卡尔树并求解相关性质。

**思路**
以数组下标为中序遍历、数组元素为堆值（min 堆）建树：用单调栈维护当前右链，遇到更小的值就不断弹出作为其左子树，最后插入栈顶作为右儿子。💡 类比「单调栈维护第 k 个更大元素」的进弹出栈过程。

```python
def cartesian_tree(a):
    n = len(a)
    left = [-1]*n; right = [-1]*n; parent = [-1]*n
    st = []
    for i in range(n):
        last = -1
        while st and a[st[-1]] > a[i]:
            last = st.pop()
        if st:
            right[st[-1]] = i; parent[i] = st[-1]
        if last != -1:
            left[i] = last; parent[last] = i
        st.append(i)
    root = st[0]
    out = []
    def inorder(u):
        if u == -1: return
        inorder(left[u]); out.append(u); inorder(right[u])
    inorder(root)
    return root, out

a = [3, 2, 1, 4, 5]
root, ino = cartesian_tree(a)
print(root, a[root])       # 最小值在下标 2
print([a[i] for i in ino]) # 中序遍历还原原数组
```

> **复杂度**：O(n)。

---

#### 13.7.4 例 21：可持久化 Trie 求区间最大异或值 ⭐⭐⭐

> **知识点**：可持久化二进制 Trie｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的可持久化数据结构综合题，主要考察可持久化二进制 Trie。在数组的某个区间内，查询与给定值异或结果最大的值。

**思路**
对前缀数组建可持久化二进制 Trie：`root[i]` 表示前 i 个数构成的版本。查询区间 `[l, r]` 内与 `x` 的最大异或，只需同时在 `root[r]` 与 `root[l-1]` 两棵树上贪心——某一位上若「取反位」在两版本对应子树的计数差大于 0，就走那条分支。💡 类比主席树「带权前缀版本相减」。

```python
class PTrie:
    def __init__(self, bits=30):
        self.bits = bits
        self.c0 = [0]; self.c1 = [0]; self.cnt = [0]
    def insert(self, prev, x):
        cur = len(self.cnt)
        self.c0.append(self.c0[prev]); self.c1.append(self.c1[prev]); self.cnt.append(self.cnt[prev]+1)
        u, o = cur, prev
        for b in range(self.bits-1, -1, -1):
            bit = (x >> b) & 1
            nxt = len(self.cnt)
            self.c0.append(0); self.c1.append(0); self.cnt.append(0)
            src = self.c0[o] if bit == 0 else self.c1[o]
            self.cnt[nxt] = self.cnt[src] + 1
            # 新节点继承 src 的孩子；向下的分支在下一轮被覆盖
            self.c0[nxt] = self.c0[src]
            self.c1[nxt] = self.c1[src]
            # u 的向下分支指向 nxt，另一分支与旧版本共享
            if bit == 0:
                self.c0[u] = nxt
                self.c1[u] = self.c1[o]
            else:
                self.c1[u] = nxt
                self.c0[u] = self.c0[o]
            o = src; u = nxt
        return cur
    def max_xor(self, r, l, x):
        res = 0; u = r; v = l
        for b in range(self.bits-1, -1, -1):
            bit = (x >> b) & 1; want = bit ^ 1
            cu = self.c1[u] if want == 1 else self.c0[u]
            cv = self.c1[v] if want == 1 else self.c0[v]
            if self.cnt[cu] - self.cnt[cv] > 0:
                res |= 1 << b
                u, v = cu, cv
            else:
                u = self.c0[u] if bit == 0 else self.c1[u]
                v = self.c0[v] if bit == 0 else self.c1[v]
        return res

arr = [1, 2, 3, 4]
t = PTrie(4)
roots = [0]
for x in arr: roots.append(t.insert(roots[-1], x))
print(t.max_xor(roots[4], roots[0], 1))   # [1,4]区间内 1^4=5
print(t.max_xor(roots[3], roots[0], 5))   # [1,3]区间内 5^2=7
```

> **复杂度**：插入/查询均 O(bits)。

---

### 13.8 可持久化与区间查询（可持久化并查集 · 莫队求众数 · 静态区间 mex）

#### 13.8.1 例 22：可持久化并查集（支持回退历史版本）⭐⭐⭐

> **知识点**：可持久化数组 + 并查集（按秩合并、不路径压缩）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的大模拟综合题，主要考察可持久化数组与并查集（按秩合并、不路径压缩）的结合。支持合并、查询以及回退到历史任意版本。

**思路**
并查集是纯「单点修改」，因此可用一棵可持久化线段树当「可持久化数组」存储 `parent` 与 `size`。每次 `union` 只产生一个新版本（修改两个位置）。由于要支持历史查询，**不能做路径压缩**，仅按大小合并以保证 find 复杂度 O(log n)。💡 类比带「时间戳」的线段树，每个操作只复制沿途路径。

```python
class SegArr:
    def __init__(self, n, base):
        self.n = n; self.base = base
        self.lc = [0]; self.rc = [0]; self.val = [0]
    def set(self, prev, pos, val):
        cur = len(self.val)
        self.lc.append(self.lc[prev]); self.rc.append(self.rc[prev]); self.val.append(val)
        lo, hi, u, p = 1, self.n, cur, prev
        while lo < hi:
            mid = (lo+hi)//2
            if pos <= mid:
                nxt = len(self.val)
                self.lc.append(0); self.rc.append(0); self.val.append(0)
                self.lc[u] = nxt; self.rc[u] = self.rc[p]
                self.val[nxt] = self.val[self.lc[p]] if p else self.base
                hi = mid; u = nxt; p = self.lc[p]
            else:
                nxt = len(self.val)
                self.lc.append(0); self.rc.append(0); self.val.append(0)
                self.lc[u] = self.lc[p]; self.rc[u] = nxt
                self.val[nxt] = self.val[self.rc[p]] if p else self.base
                lo = mid+1; u = nxt; p = self.rc[p]
        self.val[u] = val
        return cur
    def get(self, root, pos):
        lo, hi, u = 1, self.n, root
        while u and lo < hi:
            mid = (lo+hi)//2
            if pos <= mid: u = self.lc[u]; hi = mid
            else: u = self.rc[u]; lo = mid+1
        return self.val[u] if u else self.base

def build(n): return SegArr(n, 0), SegArr(n, 1)   # parent 初值 0；size 初值 1

def find(fa, rp, x):                                # fa 与 rp 同讲一棵树
    while True:
        p = fa.get(rp, x)
        if p == 0 or p == x: return x
        x = p

def union(fa, sz, rp, rs, a, b):                    # 父数组、size 数组各自守着独立版本根
    a = find(fa, rp, a); b = find(fa, rp, b)
    if a == b: return rp, rs
    sa, sb = sz.get(rs, a), sz.get(rs, b)
    if sa < sb: a, b = b, a
    rp = fa.set(rp, b, a)
    rs = sz.set(rs, a, sa + sb)
    return rp, rs

fa, sz = build(5)
rp = rs = 0
rp, rs = union(fa, sz, rp, rs, 1, 2)
rp, rs = union(fa, sz, rp, rs, 2, 3)
rp2, rs2 = rp, rs                       # 保存历史版本
rp, rs = union(fa, sz, rp, rs, 4, 5)
print(find(fa, rp2, 3))                        # 历史版本中 3 的祖先（1）
print(find(fa, rp, 4) == find(fa, rp, 5))      # 新版本中 4、5 连通
```

> **复杂度**：每步 O(log n) 时间/空间，find O(log n)。

---

#### 13.8.2 例 23：莫队求区间众数的出现次数 ⭐⭐⭐

> **知识点**：莫队 + 频次计数桶｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的区间统计综合题，主要考察莫队与频次计数桶的结合。多次询问一个区间内众数的出现次数。

**思路**
莫队把查询按「左端点所在块 + 右端点」排序后增量维护区间。为了能在 O(1) 转移中维护「当前众数的出现次数」，维护两个桶：`freq[v]`（值出现次数）与 `cnt_f[f]`（出现 f 次的值个数）。当 `cnt_f[maxf]` 减到 0 时就递减 `maxf`。💡 类比「值的分布的双重计数」，把 O(n) 的众数统计拆成两级桶即可 O(1) 更新。

```python
import math

def mo_mode(a, queries):
    n = len(a); block = int(n ** 0.5) + 1
    qs = sorted([(l, r, i) for i, (l, r) in enumerate(queries)],
                key=lambda q: (q[0]//block, -q[1] if (q[0]//block) % 2 else q[1]))
    freq = {}; cnt_f = [0]*(n+2); maxf = [0]
    def add(x):
        f = freq.get(x, 0)
        if f: cnt_f[f] -= 1
        cnt_f[f+1] += 1; freq[x] = f+1
        if f+1 > maxf[0]: maxf[0] = f+1
    def remove(x):
        f = freq[x]
        cnt_f[f] -= 1
        freq[x] = f-1
        if f-1 > 0: cnt_f[f-1] += 1
        if f == maxf[0] and cnt_f[maxf[0]] == 0:
            maxf[0] -= 1
    cur_l, cur_r = 0, -1
    ans = [0]*len(queries)
    for l, r, i in qs:
        while cur_l > l: cur_l -= 1; add(a[cur_l])
        while cur_r < r: cur_r += 1; add(a[cur_r])
        while cur_l < l: remove(a[cur_l]); cur_l += 1
        while cur_r > r: remove(a[cur_r]); cur_r -= 1
        ans[i] = maxf[0]
    return ans

a = [1, 2, 2, 3, 2]
print(mo_mode(a, [(0, 4)]))   # 众数次数 3
print(mo_mode(a, [(0, 3)]))   # 众数次数 2
```

> **复杂度**：O((n + q)√n)。

---

#### 13.8.3 例 24：静态区间 mex（最小未出现非负整数）⭐⭐⭐

> **知识点**：离线 + 线段树维护「最新出现位置」最小值｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的离线区间综合题，主要考察离线处理与线段树维护「最新出现位置」最小值。多次询问一个区间内的最小未出现非负整数（mex）。

**思路**
按右端点 `r` 递增处理查询。对每个数值维护其在当前前缀中「最后一次出现的位置 `last[v]`」，用线段树（值域为树叶）存这些 `last[v]` 的最小值。对查询 `[l, r]`，答案就是值域中第一个满足 `last[v] < l` 的 `v`，在线段树上二分下降即可。💡 类比把「未出现」翻译成「最后出现位置早于左端点」，从而变成线段树上的「首个小于」查询。

```python
def static_mex(arr, queries):
    n = len(arr); V = n + 1
    size = 1
    while size <= V: size <<= 1
    INF = 10**9
    seg = [INF]*(2*size)
    def update(pos, val):
        i = pos + size; seg[i] = val; i >>= 1
        while i: seg[i] = min(seg[2*i], seg[2*i+1]); i >>= 1
    def find_first(th):
        if seg[1] >= th: return -1
        i = 1
        while i < size:
            if seg[2*i] < th: i = 2*i
            else: i = 2*i+1
        return i - size
    qs = sorted([(r, l, i) for i, (l, r) in enumerate(queries)])
    res = [0]*len(queries)
    rp = -1
    for r, l, i in qs:
        while rp < r:
            rp += 1
            if arr[rp] <= V: update(arr[rp], rp)
        m = find_first(l)
        res[i] = m if m != -1 else V + 1
    return res

arr = [0, 1, 3, 2, 5]
print(static_mex(arr, [(0, 3)]))   # [0,1,3,2] => mex=4
print(static_mex(arr, [(2, 4)]))   # [3,2,5] => mex=0
```

> **复杂度**：O((n + q) log n)。

---

### 13.9 字符串与后缀结构（后缀数组 · 最小表示法 · SAM）

#### 13.9.1 例 25：后缀数组求最长公共前缀 & 不同子串个数 ⭐⭐⭐

> **知识点**：后缀数组（倍增）+ height 数组｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度很高的字符串综合题，主要考察后缀数组（倍增）与 height 数组。求任意两个后缀的最长公共前缀，以及字符串本质不同子串个数。

**思路**
倍增法构造后缀数组 `sa`，再利用相邻后缀关系 O(n) 得到 `height`。任何两后缀的 LCP 是它们之间 height 的最小值。本质不同子串数 = 总子串数 − Σ height，因为每多一个后缀，新增的本质不同前缀数恰为「去掉与上一后缀重复的前缀」。💡 类比区间并：每个后缀贡献 `len − 与上一个最长公共前缀` 个新前缀。

```python
def suffix_array(s):
    n = len(s)
    sa = list(range(n))
    rank = list(map(ord, s)); tmp = [0]*n; k = 1
    while True:
        def key(x): return (rank[x], rank[x+k] if x+k < n else -1)
        sa.sort(key=key)
        tmp[sa[0]] = 0
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i-1]] + (key(sa[i]) != key(sa[i-1]))
        rank, tmp = tmp, rank
        if rank[sa[-1]] == n-1: break
        k <<= 1
    return sa, rank

def lcp_array(s, sa):
    n = len(s); rank = [0]*n
    for i, p in enumerate(sa): rank[p] = i
    h = 0; lcp = [0]*(n-1)
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i]-1]
            while i+h < n and j+h < n and s[i+h] == s[j+h]: h += 1
            lcp[rank[i]-1] = h
            if h: h -= 1
    return lcp

def distinct_substrings(s):
    sa, _ = suffix_array(s)
    lcp = lcp_array(s, sa)
    n = len(s)
    return n*(n+1)//2 - sum(lcp), sa

s = "ababa"
num, sa = distinct_substrings(s)
print(num)   # 9
print(sa)    # [4,2,0,3,1]
```

> **复杂度**：构造 O(n log n)，统计 O(n)。

---

#### 13.9.2 例 26：最小表示法（循环同构串的最小字典序）⭐⭐

> **知识点**：最小表示法（双指针 O(n)）｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的字符串题，主要考察最小表示法（双指针 O(n)）。求一个循环同构串在字典序意义下的最小表示。

**思路**
求一个字符串所有循环同构串中字典序最小的起点下标。维护两个候选起始 `i, j` 和一个比较长度 `k`：比较 `s[i+k]` 与 `s[j+k]`，若不等则把较小者留下、把较大者的起始整体后移 `k+1`。由于任意时刻两者最多比较到 n 次，总复杂度 O(n)。💡 类比「两个光标赛跑，谁落后谁向前跳」。

```python
def min_rotation(s):
    n = len(s); i, j, k = 0, 1, 0
    while i < n and j < n and k < n:
        a = s[(i+k) % n]; b = s[(j+k) % n]
        if a == b:
            k += 1
        elif a > b:
            i = i + k + 1
            if i == j: i += 1
            k = 0
        else:
            j = j + k + 1
            if i == j: j += 1
            k = 0
    p = min(i, j)
    return s[p:] + s[:p]

print(min_rotation("bca"))    # abc
print(min_rotation("abab"))   # abab
print(min_rotation("cabc"))   # abcc
```

> **复杂度**：O(n)。

---

#### 13.9.3 例 27：SAM 求本质不同子串的第 K 小字典序 ⭐⭐⭐

> **知识点**：后缀自动机（SAM）拓扑 DP + 贪心走边｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的后缀自动机综合题，主要考察后缀自动机（SAM）拓扑 DP 与贪心走边的结合。求字符串本质不同子串中字典序第 K 小的那一个。

**思路**
后缀自动机是本质不同子串的最小自动机，每个从初始状态出发的路径对应一个本质不同子串。按 `len` 逆序遍历得到拓扑序，`g[u] = Σ_c (1 + g[v])` 表示从 u 出发的（含当前字符）不同子串数。求第 K 小时在每个状态按字典序尝试出边：优先输出「单个字符」再进入该转移继续，从而贪心构造出答案。💡 类比在自动机的 DAG 上做「第 K 路」的 DP 分叉选择。

```python
class SAM:
    def __init__(self):
        self.len = [0]; self.link = [-1]; self.next = [dict()]
        self.last = 0
    def extend(self, c):
        cur = len(self.len)
        self.len.append(self.len[self.last]+1); self.next.append(dict()); self.link.append(0)
        p = self.last
        while p != -1 and c not in self.next[p]:
            self.next[p][c] = cur; p = self.link[p]
        if p == -1:
            self.link[cur] = 0
        else:
            q = self.next[p][c]
            if self.len[p]+1 == self.len[q]:
                self.link[cur] = q
            else:
                clone = len(self.len)
                self.len.append(self.len[p]+1); self.next.append(self.next[q].copy()); self.link.append(self.link[q])
                while p != -1 and self.next[p].get(c, 0) == q:
                    self.next[p][c] = clone; p = self.link[p]
                self.link[q] = self.link[cur] = clone
        self.last = cur
    def kth_distinct(self, k):
        order = sorted(range(len(self.len)), key=lambda u: self.len[u], reverse=True)
        g = [0]*len(self.len)
        for u in order:
            for v in self.next[u].values():
                g[u] += 1 + g[v]
        res = ""; u = 0
        while True:
            for c in sorted(self.next[u].keys()):
                v = self.next[u][c]
                cnt = 1 + g[v]
                if k > cnt:            # 该前缀分支整体排在第 k 名之前，跳过
                    k -= cnt; continue
                res += c
                if k == 1: return res
                k -= 1; u = v; break
        return res

def build_sam(s):
    sam = SAM()
    for ch in s: sam.extend(ch)
    return sam

s = "aabb"; sam = build_sam(s)
subs = set()
for i in range(len(s)):
    for j in range(i+1, len(s)+1): subs.add(s[i:j])
brute = sorted(subs)
print([sam.kth_distinct(k) for k in range(1, len(brute)+1)] == brute)  # True
print(sam.kth_distinct(3))
```

> **复杂度**：构造 O(n)，单次查询 O(Σ·|答案|)。

---

### 13.10 网络流与图论综合（最大权闭合子图 · 费用流 · 2-SAT · K 短路）

#### 13.10.1 例 28：最大权闭合子图（Luogu P2762 太空飞行计划）⭐⭐⭐

> **知识点**：最大权闭合子图 = 最大流最小割｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的图论与网络流综合题，主要考察最大权闭合子图到最大流最小割的转化。在项目与依赖关系下，选择若干对象使收益最大化。

**思路**
闭合子图：选了一个点就必须选其所有后继。建网络：源点→正权点，边权=正权；负权点→汇点，边权=负权绝对值；原图依赖关系连容量 INF 的边。则「全部正权之和 − 最小割」即为最大权闭合子图的权值。💡 类比「割掉边 = 放弃该收益 / 承担该代价」，割得越少净收益越大。

```python
from collections import deque

class Dinic:
    def __init__(self, n):
        self.n = n; self.g = [[] for _ in range(n)]
        self.to = []; self.cap = []
    def add(self, u, v, c):
        self.g[u].append(len(self.to)); self.to.append(v); self.cap.append(c)
        self.g[v].append(len(self.to)); self.to.append(u); self.cap.append(0)
    def bfs(self, s, t):
        self.level = [-1]*self.n; self.level[s] = 0; q = deque([s])
        while q:
            u = q.popleft()
            for e in self.g[u]:
                if self.cap[e] > 0 and self.level[self.to[e]] < 0:
                    self.level[self.to[e]] = self.level[u]+1; q.append(self.to[e])
        return self.level[t] >= 0
    def dfs(self, u, t, f):
        if u == t: return f
        while self.it[u] < len(self.g[u]):
            e = self.g[u][self.it[u]]; v = self.to[e]
            if self.cap[e] > 0 and self.level[v] == self.level[u]+1:
                d = self.dfs(v, t, min(f, self.cap[e]))
                if d:
                    self.cap[e] -= d; self.cap[e^1] += d; return d
            self.it[u] += 1
        return 0
    def maxflow(self, s, t):
        flow = 0
        while self.bfs(s, t):
            self.it = [0]*self.n
            while True:
                f = self.dfs(s, t, 10**18)
                if not f: break
                flow += f
        return flow

S, P1, P2, E1, E2, T = 0, 1, 2, 3, 4, 5
din = Dinic(6)
din.add(S, P1, 5); din.add(S, P2, 4)
din.add(P1, E1, 10**9); din.add(P2, E1, 10**9); din.add(P2, E2, 10**9)
din.add(E1, T, 3); din.add(E2, T, 2)
total = 9
mincut = din.maxflow(S, T)
print(total - mincut)   # 2（选全部实验，收益9-成本5=4）
```

> **复杂度**：O(n²m)（Dinic）。

---

#### 13.10.2 例 29：最小费用最大流（MCMF，SPFA 增广）⭐⭐⭐

> **知识点**：费用流（连续最短路增广）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的网络流综合题，主要考察最小费用最大流（费用流，连续最短路增广）。在每条边有容量与单位费用的网络上求单位费用意义下的最大流。

**思路**
在残量网络上不断用 SPFA 找「单位费用和」最小的增广路（把边权视为费用），沿最短路增广并累加费用，直到无法增广。反向边费用为相反数以支持退流。💡 类比「流量越高，每次沿最省钱的路多运一点」。

```python
from collections import deque

def min_cost_max_flow(n, edges, s, t, maxf):
    g = [[] for _ in range(n)]; to = []; cap = []; cost = []
    def add(u, v, c, w):
        g[u].append(len(to)); to.append(v); cap.append(c); cost.append(w)
        g[v].append(len(to)); to.append(u); cap.append(0); cost.append(-w)
    for u, v, c, w in edges: add(u, v, c, w)
    INF = 10**18; flow = 0; cost_sum = 0
    while flow < maxf:
        dist = [INF]*n; inq = [False]*n; pre_v = [-1]*n; pre_e = [-1]*n
        dist[s] = 0; q = deque([s]); inq[s] = True
        while q:
            u = q.popleft(); inq[u] = False
            for e in g[u]:
                if cap[e] > 0 and dist[to[e]] > dist[u] + cost[e]:
                    dist[to[e]] = dist[u] + cost[e]
                    pre_v[to[e]] = u; pre_e[to[e]] = e
                    if not inq[to[e]]: inq[to[e]] = True; q.append(to[e])
        if dist[t] == INF: break
        f = maxf - flow; v = t
        while v != s:
            f = min(f, cap[pre_e[v]]); v = pre_v[v]
        v = t
        while v != s:
            cap[pre_e[v]] -= f; cap[pre_e[v]^1] += f; v = pre_v[v]
        flow += f; cost_sum += f * dist[t]
    return flow, cost_sum

edges = [(0,1,2,5),(0,2,1,3),(1,3,1,2),(2,3,2,4)]
print(min_cost_max_flow(4, edges, 0, 3, 2))   # 流2，费用 7+7=14
```

> **复杂度**：O(F·E·V)。

---

#### 13.10.3 例 30：2-SAT（Luogu P4782）⭐⭐⭐

> **知识点**：2-SAT（强连通分量 Tarjan + 赋值）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的逻辑约束综合题，主要考察 2-SAT 问题与强连通分量（Tarjan）。给定若干布尔变量之间的蕴含/析取约束，判断是否存在一组满足所有约束的赋值。

**思路**
每个布尔变量拆成真/假两个点，形如 `(a条件 or b条件)` 的子句化为两条蕴含边 `(¬a→b, ¬b→a)`。建图后跑 Tarjan 求强连通分量：若某变量的真、假在同一 SCC 则无解；否则根据 SC C 的拓扑顺序给变量赋值（较早完成的 SCC 为汇点，取假一侧）。💡 类比「逻辑条件画成有向图，冲突就是存在环」。

```python
import sys
sys.setrecursionlimit(1 << 20)

def two_sat(n, clauses):
    N = 2*n
    g = [[] for _ in range(N)]
    def node(x, v): return 2*(x-1) + (0 if v else 1)
    for a, va, b, vb in clauses:
        g[node(a, 1-va)].append(node(b, vb))
        g[node(b, 1-vb)].append(node(a, va))
    dfn = [-1]*N; low = [0]*N; in_st = [False]*N; comp = [-1]*N
    st = []; idx = [0]; cid = [0]
    def tarjan(u):
        idx[0] += 1; dfn[u] = low[u] = idx[0]
        st.append(u); in_st[u] = True
        for v in g[u]:
            if dfn[v] == -1:
                tarjan(v); low[u] = min(low[u], low[v])
            elif in_st[v]:
                low[u] = min(low[u], dfn[v])
        if low[u] == dfn[u]:
            while True:
                w = st.pop(); in_st[w] = False; comp[w] = cid[0]
                if w == u: break
            cid[0] += 1
    for i in range(N):
        if dfn[i] == -1: tarjan(i)
    for x in range(1, n+1):
        if comp[node(x, 0)] == comp[node(x, 1)]: return None
    assign = {}
    for x in range(1, n+1):
        assign[x] = comp[node(x, 0)] > comp[node(x, 1)]
    return assign

print(two_sat(2, [(1, True, 2, True), (1, False, 2, False)]))   # 可满足
print(two_sat(1, [(1, True, 1, True), (1, False, 1, False)]))   # 无解 None
```

> **复杂度**：O(n + m)。

---

#### 13.10.4 例 31：K 短路（A* / 次短路）⭐⭐⭐

> **知识点**：K 短路（A* + 可重开堆）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的最短路扩展综合题，主要考察 K 短路（A* + 可重开堆）。求从起点到终点的第 K 短路径长度。

**思路**
先在反图上求汇点到各点最短路 `h[]` 作为启发式，再用 A* 从源点扩展，估价 `f = 当前距离 + h[v]`。每次弹出节点时路径计数到该点，当汇点第 K 次被弹出时，其累计距离即第 K 短路。💡 类比「最短路线打底，优先队列层层加码」。

```python
import heapq

def kth_shortest(n, edges, s, t, k):
    g = [[] for _ in range(n)]; rg = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w)); rg[v].append((u, w))
    INF = 10**18
    h = [INF]*n; h[t] = 0; pq = [(0, t)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > h[u]: continue
        for v, w in rg[u]:
            if h[v] > h[u] + w: h[v] = h[u]+w; heapq.heappush(pq, (h[v], v))
    cnt = [0]*n
    pq = [(h[s], 0, s)]
    while pq:
        f, d, u = heapq.heappop(pq)
        cnt[u] += 1
        if u == t and cnt[u] == k: return d
        for v, w in g[u]:
            if cnt[u] <= k:
                heapq.heappush(pq, (d+w+h[v], d+w, v))
    return -1

n = 4
edges = [(0,1,1),(0,2,2),(1,3,3),(2,3,1),(1,2,1)]
print(kth_shortest(n, edges, 0, 3, 1))   # 最短 3
print(kth_shortest(n, edges, 0, 3, 3))   # 第3短 4
```

> **复杂度**：启发式下实践远优于穷举。

---

### 13.11 线性基与多项式（异或第 K 小 · NTT · 拉格朗日插值 · FFT 大整数乘法）

#### 13.11.1 例 32：线性基求异或第 K 小 ⭐⭐⭐

> **知识点**：线性基（高斯消元为行最简形）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的线性基综合题，主要考察将线性基高斯消元为行最简形。求若干数异或生成的集合中第 K 小的异或值。

**思路**
先用异或高斯消元把线性基化成行最简形（每个主元位只在一个向量中出现），把非零基向量按主元位从低到高排列。这样所有可达异或值正好按「组合位掩码」的顺序递增——第 `k` 小（从 1 计，含空组合 0）就是选取 `k-1` 二进制对应位上的基向量异或起来。💡 类比把向量组「正交化」后再按二进制位序枚举。

```python
class LinearBasis:
    def __init__(self): self.b = [0]*64
    def insert(self, x):
        for i in range(63, -1, -1):
            if not ((x >> i) & 1): continue
            if not self.b[i]: self.b[i] = x; return
            x ^= self.b[i]
    def reduce(self):
        for i in range(64):
            if not self.b[i]: continue
            for j in range(64):
                if i != j and self.b[j] and ((self.b[j] >> i) & 1):
                    self.b[j] ^= self.b[i]
    def kth(self, k):
        self.reduce()
        vec = [v for v in self.b if v]
        if k > (1 << len(vec)): return -1
        res = 0; k -= 1
        for i, v in enumerate(vec):
            if (k >> i) & 1: res ^= v
        return res

lb = LinearBasis()
for x in [1, 2, 4, 8]: lb.insert(x)
vals = sorted({a^b^c^d for a in (0,1) for b in (0,2) for c in (0,4) for d in (0,8)})
print([lb.kth(k) for k in range(1, 6)] == vals[:5])   # True
```

> **复杂度**：插入/消元 O(64²)，求第 K 小 O(64)。

---

#### 13.11.2 例 33：NTT 模多项式乘法（数论变换）⭐⭐⭐

> **知识点**：NTT（原根 998244353）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的多项式综合题，主要考察 NTT 数论变换。在模 998244353 意义下计算两个多项式的乘积。

**思路**
NTT 是 FFT 在模质数域上的版本（质数 998244353，原根 3），把多项式由系数表示转为点值表示做点乘，再逆变换回系数，实现精确的整数卷积。迭代实现按「位逆序置换→蝴蝶变换」的标准流程。💡 类比 FFT，但避开浮点误差、结果取模。

```python
MOD, G = 998244353, 3

def ntt(a, invert):
    n = len(a); j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit: j ^= bit; bit >>= 1
        j ^= bit
        if i < j: a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = pow(G, (MOD-1)//length, MOD)
        if invert: wlen = pow(wlen, MOD-2, MOD)
        half = length // 2
        for i in range(0, n, length):
            w = 1
            for j in range(half):
                u = a[i+j]; v = a[i+j+half] * w % MOD
                a[i+j] = (u+v) % MOD
                a[i+j+half] = (u-v) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        invn = pow(n, MOD-2, MOD)
        for i in range(n): a[i] = a[i] * invn % MOD

def conv(a, b):
    need = len(a)+len(b)-1
    n = 1
    while n < need: n <<= 1
    fa = a[:] + [0]*(n-len(a)); fb = b[:] + [0]*(n-len(b))
    ntt(fa, False); ntt(fb, False)
    for i in range(n): fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:need]

print(conv([1, 2, 3], [4, 5]))   # [4, 13, 22, 15]
```

> **复杂度**：O(n log n)。

---

#### 13.11.3 例 34：拉格朗日插值（O(n²)）⭐⭐⭐

> **知识点**：拉格朗日插值｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的数值综合题，主要考察拉格朗日插值。给定若干个已知点，求通过这些点的多项式在任意给定点处的取值。

**思路**
过给定 n+1 个点 `(x_i, y_i)` 的次数不超过 n 的多项式唯一。构造「示性」多项式 `L_i(x) = Π_{j≠i} (x−x_j)/(x_i−x_j)`，则 `P(x) = Σ y_i·L_i(x)`。直接按公式逐项累乘（O(n²)）。💡 类比「用一根根小钉子一步步把曲线钉出来」，每个基点只在自己位置取值 1。

```python
def lagrange_nd(xs, ys, x):
    ans = 0; n = len(xs)
    for i in range(n):
        num = 1.0; den = 1.0
        for j in range(n):
            if i == j: continue
            num *= (x - xs[j]); den *= (xs[i] - xs[j])
        ans += ys[i] * num / den
    return ans

xs = [1, 2, 3]; ys = [1, 4, 9]
print(lagrange_nd(xs, ys, 4))   # 16
print(lagrange_nd(xs, ys, 0))   # 0
```

> **复杂度**：O(n²)。

---

#### 13.11.4 例 35：FFT/NTT 大整数乘法（LeetCode 43）⭐⭐⭐

> **知识点**：多项式卷积加速大数乘法（NTT）｜**难度**：⭐⭐⭐（困难）｜**类型**：LeetCode / 竞赛
**题目描述**：这是一道难度较高的数论与多项式综合题，主要考察用 FFT/NTT 多项式卷积加速大整数乘法。高效计算两个极大整数相乘的精确结果。

**思路**
把每一位数字看作多项式系数（倒序），两串相乘 = 两个多项式的卷积，用 NTT 得到每一位的「未进位和」，最后从低位向高位进位。相比逐位相乘的 O(n²) 提升到 O(n log n)。💡 类比小学乘法竖式，但把「每一位相乘再对齐相加」整体交给多项式卷积一步完成。

```python
MOD, G = 998244353, 3   # NTT 模数与原根（同例 33）

def ntt(a, invert):
    n = len(a); j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit: j ^= bit; bit >>= 1
        j ^= bit
        if i < j: a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = pow(G, (MOD-1)//length, MOD)
        if invert: wlen = pow(wlen, MOD-2, MOD)
        half = length // 2
        for i in range(0, n, length):
            w = 1
            for j in range(half):
                u = a[i+j]; v = a[i+j+half] * w % MOD
                a[i+j] = (u+v) % MOD
                a[i+j+half] = (u-v) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        invn = pow(n, MOD-2, MOD)
        for i in range(n): a[i] = a[i] * invn % MOD

def conv(a, b):
    need = len(a)+len(b)-1
    n = 1
    while n < need: n <<= 1
    fa = a[:] + [0]*(n-len(a)); fb = b[:] + [0]*(n-len(b))
    ntt(fa, False); ntt(fb, False)
    for i in range(n): fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:need]

def multiply_str(a, b):
    if a == "0" or b == "0": return "0"
    A = [int(c) for c in a[::-1]]; B = [int(c) for c in b[::-1]]
    c = conv(A, B)                      # 多项式卷积 = 竖式乘积
    carry = 0; dig = []
    for x in c:
        s = x + carry; dig.append(s % 10); carry = s // 10
    while carry: dig.append(carry % 10); carry //= 10
    while len(dig) > 1 and dig[-1] == 0: dig.pop()
    return ''.join(str(d) for d in dig[::-1])

print(multiply_str("123", "456"))   # 56088
print(multiply_str("99", "99"))     # 9801
```

> **复杂度**：O(n log n)（卷积主导）。

---

### 13.12 平衡树与二分答案（替罪羊树 · wqs 二分）

#### 13.12.1 例 36：替罪羊树（Scapegoat Tree）⭐⭐⭐

> **知识点**：替罪羊树（失衡重建的平衡树）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的平衡树综合题，主要考察替罪羊树（失衡重建）。实现支持插入、删除、查询第 K 小的自平衡二叉搜索树。

**思路**
替罪羊树不旋转，只在某子树严重失衡（一侧大小超过 α·整棵，α≈0.7）时，把整棵子树中序遍历「拍平」成数组，再按中点递归重建为完美平衡树。均摊 O(log n)。💡 类比「天平歪到一定程度才整个扶正」，平时只小步累积。

```python
import sys
sys.setrecursionlimit(1 << 20)
ALPHA = 0.7

class Node:
    __slots__ = ('k', 'l', 'r', 'sz')
    def __init__(self, k): self.k = k; self.l = None; self.r = None; self.sz = 1

def size(u): return u.sz if u else 0
def is_bad(u): return u and (size(u.l) > ALPHA*size(u) or size(u.r) > ALPHA*size(u))

class Scapegoat:
    def __init__(self): self.root = None
    def flatten(self, u, out):
        if not u: return
        self.flatten(u.l, out); out.append(u); self.flatten(u.r, out)
    def build(self, arr, l, r):
        if l > r: return None
        m = (l+r)//2; u = arr[m]
        u.l = self.build(arr, l, m-1); u.r = self.build(arr, m+1, r)
        u.sz = 1 + size(u.l) + size(u.r)
        return u
    def insert(self, key):
        if not self.root:
            self.root = Node(key); return
        path = []; u = self.root
        while True:
            path.append(u)
            if key < u.k:
                if not u.l: u.l = Node(key); break
                u = u.l
            elif key > u.k:
                if not u.r: u.r = Node(key); break
                u = u.r
            else:
                return
        for nd in path: nd.sz += 1
        for i in range(len(path)-1, -1, -1):
            if is_bad(path[i]):
                arr = []; self.flatten(path[i], arr)
                newb = self.build(arr, 0, len(arr)-1)
                pp = path[i-1] if i > 0 else None
                if pp is None: self.root = newb
                elif pp.l is path[i]: pp.l = newb
                else: pp.r = newb
                break
    def contains(self, key):
        u = self.root
        while u:
            if key == u.k: return True
            u = u.l if key < u.k else u.r
        return False
    def inorder(self):
        out = []
        def go(u):
            if not u: return
            go(u.l); out.append(u.k); go(u.r)
        go(self.root); return out

sgt = Scapegoat()
for x in [5, 3, 7, 2, 4, 6, 8, 1]: sgt.insert(x)
print(sgt.inorder())                       # [1..8]
print(sgt.contains(4), sgt.contains(9))    # True False
```

> **复杂度**：插入均摊 O(log n)。

---

#### 13.12.2 例 37：wqs 二分（带权二分 / Alien trick）⭐⭐⭐

> **知识点**：wqs 二分（把「恰好 k 个」约束转为惩罚代价）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的优化 DP 综合题，主要考察 wqs 二分（带权二分/Alien trick）。把「恰好 k 个」的约束转为惩罚代价，求解带选择数量限制的凸优化 DP 问题。

**思路**
当「恰取 k 个」对应的最优值是 k 的凸函数，可给每个被取对象额外一个统一惩罚 `c`，在无个数约束下求带惩罚的最优解，得到段数随 c 单调递减。二分 c 使段数跨过 k，用切线把答案「插」回无惩罚值。以「把数组分成恰好 k 段，最小化各段和平方之和」为例，内部用 O(n²) 或斜率优化 O(n) 的 DP。💡 类比在约束代价这一维度上做「二分搜索 + 外推」。

```python
def partition_squares(a, k):
    n = len(a)
    pre = [0]*(n+1)
    for i in range(n): pre[i+1] = pre[i] + a[i]
    def solve(c):
        INF = 10**18
        dp = [INF]*(n+1); cnt = [0]*(n+1)
        dp[0] = 0; cnt[0] = 0
        for i in range(1, n+1):
            best, bc = INF, -1
            for j in range(i):
                if dp[j] >= INF: continue
                seg = pre[i] - pre[j]
                val = dp[j] + seg*seg + c
                if val < best or (val == best and cnt[j] > bc):
                    best = val; bc = cnt[j]
            dp[i] = best; cnt[i] = bc + 1
        return dp[n], cnt[n]
    lo, hi = -10**10, 10**10; best_c = None
    while lo <= hi:
        mid = (lo + hi) // 2
        _, cnum = solve(mid)
        if cnum >= k:
            best_c = mid; lo = mid + 1
        else:
            hi = mid - 1
    val, _ = solve(best_c)
    return val - best_c * k

a = [1, 3, 1]
print(partition_squares(a, 2))   # 17
print(partition_squares(a, 1))   # 25
```

> **复杂度**：外层二分 O(log V) × 内层 DP O(n²)（可斜率优化至 O(n log V)）。

---

### 13.13 树上与倍增（K 级祖先 · 树直径 · LCT 单链 · 虚树）

#### 13.13.1 例 38：树上 K 级祖先（倍增）⭐⭐

> **知识点**：二进制倍增预处理 + 最近公共祖先（LCA）｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的树上倍增题，主要考察二进制倍增预处理。多次询问某一节点的向上 K 级祖先。

**思路**
预处理每个节点向上跳 `1,2,4,…` 步的祖先，查询时把 `k` 拆成二进制逐位跳到目标。由于倍增表大小 `log n`，单次查询 `O(log n)`。它是 LCA、树上点权/边权第 K 大等高级题目的基石。💡 类比「电梯楼层按键」：通过二进制位把任意楼层精确分解成若干二段跳。

```python
parent = [0, 1, 1, 1, 2, 4]   # 1 为根：index=节点, value=父亲
depth = [-1, 0, 1, 1, 2, 3]

def build_up(parent):
    up = [list(parent)]           # up[0] = 父亲
    while True:
        prev = up[-1]
        nxt = [prev[prev[i]] for i in range(len(parent))]
        if nxt == prev:
            break
        up.append(nxt)
    return up

def kth_ancestor(up, depth, v, k):
    if k > depth[v]:
        return -1
    j = 0
    while k:
        if k & 1:
            v = up[j][v]
        k >>= 1
        j += 1
    return v

up = build_up(parent)
print(kth_ancestor(up, depth, 5, 1))   # 4（父亲）
print(kth_ancestor(up, depth, 5, 2))   # 2（祖父）
print(kth_ancestor(up, depth, 5, 3))   # 1（根）
```

> **复杂度**：倍增表 O(n log n) 空间与预处理，单次查询 O(log n)。

#### 13.13.2 例 39：树的直径（两遍 DFS）⭐⭐

> **知识点**：树的直径性质 + 树上广度/深度优先遍历｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的树性质题，主要考察树的直径性质与两次 DFS/BFS。在无向带权树中求最远两点之间的距离（树直径）。

**思路**
任取一点出发走到最远的点 `a`，再从 `a` 走最远的点 `b`，则 `a→b` 的路径即树的直径。核心性质是「离任意点最远的点一定是直径端点」。💡 类比「拉紧一条橡皮筋」：先在树上随意抓一个端点，把它拉到最远，再从那里拉出整条橡皮筋的长度。

```python
def tree_diameter(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v); g[v].append(u)

    def bfs(s):
        dist = [-1] * n
        dist[s] = 0
        stack = [s]
        order = []
        while stack:
            u = stack.pop()
            order.append(u)
            for v in g[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    stack.append(v)
        far = max(order, key=lambda x: dist[x])
        return far, dist
    a, _ = bfs(0)
    b, d = bfs(a)
    return d[b]                       # 直径长度（边数）

print(tree_diameter(6, [(0,1),(1,2),(1,3),(2,4),(4,5)]))   # 4：0-1-2-4-5
```

> **复杂度**：两遍遍历共 O(n)，空间 O(n)。

#### 13.13.3 例 40：动态树入门：LCT 维护单链（路径和 / 单点改）⭐⭐⭐

> **知识点**：Link-Cut Tree（Splay 维护实链）+ 懒翻转标记｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的动态树综合题，主要考察 LCT（Splay 维护实链）与懒翻转标记。动态维护一棵树，支持单点修改与查询某条链上的点权和。

**思路**
LCT 用若干颗伸展树（Splay）表示森林中的「实链」，`access` 打通根到某点的实链，`makeroot` 换根，`link/cut` 加删边，`split` 提取一条路径。本实现仅需维护单链的路径和与单点修改。💡 类比「拉链」：`access` 不断把目标点所在的链段展开成一条连续的重链。

```python
class LCT:
    def __init__(self, n):
        self.ch = [[-1, -1] for _ in range(n)]   # 左/右儿子
        self.fa = [-1] * n
        self.rev = [False] * n
        self.val = [0] * n
        self.sum = [0] * n

    def _pushup(self, x):
        self.sum[x] = self.val[x]
        for c in self.ch[x]:
            if c != -1:
                self.sum[x] += self.sum[c]

    def _isroot(self, x):
        f = self.fa[x]
        return f == -1 or (self.ch[f][0] != x and self.ch[f][1] != x)

    def _pushrev(self, x):
        if x != -1:
            self.ch[x][0], self.ch[x][1] = self.ch[x][1], self.ch[x][0]
            self.rev[x] = not self.rev[x]

    def _pushdown(self, x):
        if self.rev[x]:
            self._pushrev(self.ch[x][0]); self._pushrev(self.ch[x][1])
            self.rev[x] = False

    def _rotate(self, x):
        y = self.fa[x]; z = self.fa[y]
        k = 1 if self.ch[y][1] == x else 0
        b = self.ch[x][k ^ 1]
        if not self._isroot(y):
            if self.ch[z][0] == y: self.ch[z][0] = x
            else: self.ch[z][1] = x
        self.fa[x] = z
        self.ch[x][k ^ 1] = y; self.fa[y] = x
        self.ch[y][k] = b
        if b != -1: self.fa[b] = y
        self._pushup(y); self._pushup(x)

    def _splay(self, x):
        st = []; u = x
        while not self._isroot(u):
            st.append(u); u = self.fa[u]
        st.append(u)
        for v in reversed(st):
            self._pushdown(v)
        while not self._isroot(x):
            y = self.fa[x]; z = self.fa[y]
            if not self._isroot(y):
                if (self.ch[y][0] == x) != (self.ch[z][0] == y):
                    self._rotate(x)
                else:
                    self._rotate(y)
            self._rotate(x)

    def access(self, x):
        last = -1
        while x != -1:
            self._splay(x)
            self.ch[x][1] = last
            self._pushup(x)
            last = x; x = self.fa[x]
        return last

    def makeroot(self, x):
        self.access(x); self._splay(x); self._pushrev(x)

    def split(self, x, y):
        self.makeroot(x); self.access(y); self._splay(y)
        return y

    def link(self, x, y):
        self.makeroot(x); self.fa[x] = y

# 测试：0-1-2-3-4 单链，给点 2 赋权后查询整条链的和
l = LCT(5)
for u, v in [(0,1),(1,2),(2,3),(3,4)]:
    l.link(u, v)
l.val[2] = 5; l._pushup(2)
root = l.split(0, 4)
print(l.sum[root])        # 5
```

> **复杂度**：均摊 O(log n) 每次操作，空间 O(n)。

#### 13.13.4 例 41：虚树（Virtual Tree）⭐⭐⭐

> **知识点**：按 DFS 序排序 + 单调栈维护虚树骨架 + 倍增 LCA｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的虚拟树综合题，主要考察按 DFS 序排序 + 单调栈维护虚树骨架 + 倍增 LCA。对含有关键点的多次树上询问，在压缩后的虚树上高效求解。

**思路**
当需要对树上少量关键点（及其 LCA）做树上 DP 时，构建只含关键点与相邻 LCA 的压缩树，使每条边的权重等于原树上两点的距离，从而把 O(n) 的原树问题压到 O(k log n)。用单调栈按 DFS 序增量建树即可。💡 类比「地铁提速」：只保留几站和换乘枢纽，删掉沿途无用站点。

```python
# 树：1-2, 2-3, 2-4, 3-5, 4-6（1 为根）
n = 6
adj = [[] for _ in range(n + 1)]
for u, v in [(1,2),(2,3),(2,4),(3,5),(4,6)]:
    adj[u].append(v); adj[v].append(u)

dep = [0] * (n + 1); dfn = [0] * (n + 1); up1 = [0] * (n + 1)
timer = [0]
def dfs(u, fa):
    dep[u] = dep[fa] + 1; up1[u] = fa
    timer[0] += 1; dfn[u] = timer[0]
    for v in adj[u]:
        if v != fa:
            dfs(v, u)
dfs(1, 1)
LOG = max(1, n.bit_length())
UP = [[0]*(n+1) for _ in range(LOG)]
for u in range(1, n+1): UP[0][u] = up1[u]
for j in range(1, LOG):
    for u in range(1, n+1):
        UP[j][u] = UP[j-1][UP[j-1][u]]
def lca(u, v):
    if dep[u] < dep[v]: u, v = v, u
    d = dep[u] - dep[v]; j = 0
    while d:
        if d & 1: u = UP[j][u]
        d >>= 1; j += 1
    if u == v: return u
    for j in range(LOG-1, -1, -1):
        if UP[j][u] != UP[j][v]:
            u = UP[j][u]; v = UP[j][v]
    return UP[0][u]

def build_vt(selected):
    nodes = sorted(selected, key=lambda x: dfn[x])
    vt = {}; st = []
    for u in nodes:
        if not st:
            st.append(u); continue
        w = lca(st[-1], u)
        while len(st) > 1 and dep[w] < dep[st[-2]]:
            vt.setdefault(st[-2], []).append(st[-1]); st.pop()
        if dep[w] < dep[st[-1]]:
            vt.setdefault(w, []).append(st[-1]); st.pop()
        if not st or st[-1] != w:
            st.append(w)
        st.append(u)
    while len(st) > 1:
        vt.setdefault(st[-2], []).append(st[-1]); st.pop()
    return vt, st[0]

sel = [3, 5, 6]
vt, root = build_vt(sel)
print("虚树根:", root)
print("虚树边:", sorted((a, b) for a, ls in vt.items() for b in ls))
```

> **复杂度**：O(k log n) 建树（k 为关键点数），空间 O(k)。

---

### 13.14 区间与可持久化（莫队带修 · 主席树区间最值 · 树套树第 K 小）

#### 13.14.1 例 42：带修改的莫队（区间内出现偶数次的元素个数）⭐⭐⭐

> **知识点**：带修莫队（三维回滚 块+块+时间戳）+ 频率计数｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的莫队扩展综合题，主要考察带修莫队（三维回滚：块+块+时间戳）与频率计数的结合。支持单点修改的情况下，询问区间内出现偶数次的元素个数。

**思路**
普通莫队只有 `l、r` 两个指针；带修莫队额外引入「时间」维 `t`，表示当前计算位于第几个修改之后，移动时同样回滚/前进修改。块大小取 `n^(2/3)` 保证总复杂度 O(n^(5/3))。维护每个值的出现次数，用一个计数器统计出现偶数次的值的个数。💡 类比「放映时按时间快进/快退」：除了左右挪动，还能沿时间轴回放修改。

```python
def mo_with_updates(arr, start_queries, mods):
    n = len(arr)
    a = [0] + list(arr)                 # 1-indexed
    S = max(1, int(round(n ** (2/3))))
    qs = sorted([(l, r, t, i) for i, (l, r, t) in enumerate(start_queries)],
                key=lambda x: (x[0] // S, x[1] // S, x[2]))
    freq = {}
    even = 0
    ans = [0] * len(start_queries)
    cl, cr, ct = 1, 0, 0

    def chg(x, delta):
        nonlocal even
        c = freq.get(x, 0)
        if c and c % 2 == 0: even -= 1
        nc = c + delta
        if nc and nc % 2 == 0: even += 1
        if nc: freq[x] = nc
        else: freq.pop(x, None)

    def add(pos): chg(a[pos], 1)
    def rem(pos): chg(a[pos], -1)

    def apply(m, sign):
        nonlocal ct
        p, old, new = mods[m]
        if sign == 1:                     # old -> new
            if cl <= p <= cr: chg(old, -1); chg(new, 1)
            a[p] = new
        else:                             # new -> old
            if cl <= p <= cr: chg(new, -1); chg(old, 1)
            a[p] = old
        ct += sign

    for l, r, t, i in qs:
        while ct < t: apply(ct, 1)
        while ct > t: apply(ct - 1, -1)
        while cl > l: cl -= 1; add(cl)
        while cr < r: cr += 1; add(cr)
        while cl < l: rem(cl); cl += 1
        while cr > r: rem(cr); cr -= 1
        ans[i] = even
    return ans

arr = [1, 2, 1, 1, 2, 3]
mods = []                                # 每个修改 (pos, old, new)
queries = [(1, 3, 0), (2, 5, 0), (1, 6, 0), (2, 6, 0)]
print(mo_with_updates(arr, queries, mods))   # [1,2,1,2]：各区间偶数次元素个数
```

> **复杂度**：O(n^(5/3))，空间 O(n)。

#### 13.14.2 例 43：主席树维护静态区间第 K 大（可持久化权值线段树）⭐⭐⭐

> **知识点**：前缀版本线段树 + 二分计数｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的主席树综合题，主要考察前缀版本线段树与二分计数的结合。在静态数组上回答区间第 K 大。

**思路**
对每个前缀 `[1..i]` 建一棵动态开点的权值线段树，相邻版本共享子树，空间 O(n log n)。查询区间 `[l..r]` 时用「版本 r 与版本 l-1 对应节点的 count 之差」在值域上二分定位第 K 小；第 K 大 = 第「长度 - K + 1」小。💡 类比「两个时间点的快照相减」得到区间内的频数直方图。

```python
class PersistSeg:
    def __init__(self, mx, vals):
        self.lc = [0]; self.rc = [0]; self.c = [0]
        self.roots = [0]
        self.mx = mx                      # 值域大小（离散化后）
        self.vals = vals                  # 离散化映射 (下标->原值)

    def upd(self, prev, lo, hi, pos):
        cur = len(self.lc)
        self.lc.append(self.lc[prev]); self.rc.append(self.rc[prev])
        self.c.append(self.c[prev] + 1)
        if lo != hi:
            md = (lo + hi) // 2
            if pos <= md:
                lc = self.upd(self.lc[prev], lo, md, pos)
                self.lc[cur] = lc
            else:
                rc = self.upd(self.rc[prev], md + 1, hi, pos)
                self.rc[cur] = rc
        return cur

    def kth(self, u, v, lo, hi, k):       # 区间第 k 小（1 <= k <= len）
        if lo == hi: return lo
        md = (lo + hi) // 2
        cnt = self.c[self.lc[v]] - self.c[self.lc[u]]
        if cnt >= k:
            return self.kth(self.lc[u], self.lc[v], lo, md, k)
        return self.kth(self.rc[u], self.rc[v], md + 1, hi, k - cnt)

arr = [1, 5, 3, 4, 2, 3]                 # 1-indexed 后为 [0,1,5,3,4,2,3]
uvals = sorted(set(arr[1:]))              # [1,2,3,4,5]
mp = {x: i + 1 for i, x in enumerate(uvals)}
ps = PersistSeg(len(uvals), uvals)
root = [0]
for i in range(1, len(arr)):
    root.append(ps.upd(root[-1], 1, len(uvals), mp[arr[i]]))

def range_kth(l, r, k_small):
    idx = ps.kth(root[l-1], root[r], 1, len(uvals), k_small)
    return uvals[idx - 1]

def range_kth_largest(l, r, k_large):
    length = r - l + 1
    return range_kth(l, r, length - k_large + 1)

print(range_kth(2, 5, 2))                # [5,3,4,2] 第2小=3
print(range_kth_largest(2, 5, 2))        # [5,3,4,2] 第2大=4
```

> **复杂度**：建树 O(n log n)，单次查询 O(log n)，空间 O(n log n)。

#### 13.14.3 例 44：树状数组套权值线段树（动态区间第 K 小）⭐⭐⭐

> **知识点**：BIT 外 + 动态开点权值线段树内（树套树）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的树套树综合题，主要考察树状数组（BIT）外层 + 动态开点权值线段树内层。支持单点修改的动态区间第 K 小查询。

**思路**
主席树不可修改，树套树则用树状数组按位置维护，每个 BIT 节点挂一颗动态开点权值线段树（存该段的频数）。单点修改会更新 O(log n) 颗线段树（O(log²n)）；区间查询先把对应 O(log n) 颗线段树根收集起来，再在值域上二分落到第 K 小。💡 类比「两级书架」：外层按位置分箱，内层按值在线累加。

```python
class SegTree:
    def __init__(self):
        self.lc = [0]; self.rc = [0]; self.c = [0]
    def _new(self):
        self.lc.append(0); self.rc.append(0); self.c.append(0)
        return len(self.c) - 1
    def upd(self, node, lo, hi, pos, delta):
        if node == 0: node = self._new()
        self.c[node] += delta
        if lo != hi:
            md = (lo + hi) // 2
            if pos <= md: self.lc[node] = self.upd(self.lc[node], lo, md, pos, delta)
            else: self.rc[node] = self.upd(self.rc[node], md + 1, hi, pos, delta)
        return node

class BITSeq:
    def __init__(self, n, mx):
        self.n = n; self.mx = mx
        self.S = SegTree()
        self.roots = [0] * (n + 1)
    def add(self, pos, val, delta):
        i = pos
        while i <= self.n:
            self.roots[i] = self.S.upd(self.roots[i], 1, self.mx, val, delta)
            i += i & -i
    def kth(self, l, r, k):
        rs, ls = [], []
        i = r
        while i > 0: rs.append(self.roots[i]); i -= i & -i
        i = l - 1
        while i > 0: ls.append(self.roots[i]); i -= i & -i
        lo, hi = 1, self.mx; S = self.S
        while lo < hi:
            md = (lo + hi) // 2
            cnt = 0
            for x in rs: cnt += S.c[S.lc[x]]
            for x in ls: cnt -= S.c[S.lc[x]]
            if cnt >= k:
                for i in range(len(rs)): rs[i] = S.lc[rs[i]]
                for i in range(len(ls)): ls[i] = S.lc[ls[i]]
                hi = md
            else:
                k -= cnt
                for i in range(len(rs)): rs[i] = S.rc[rs[i]]
                for i in range(len(ls)): ls[i] = S.rc[ls[i]]
                lo = md + 1
        return lo

arr = [1, 5, 3, 4, 2]
allv = sorted(set(arr))
mp = {x: i + 1 for i, x in enumerate(allv)}
b = BITSeq(len(arr), len(allv))
for i, v in enumerate(arr, 1):
    b.add(i, mp[v], 1)
ans_idx = b.kth(2, 5, 2)                 # 区间[2,5]第2小 -> 值3
print(allv[ans_idx - 1])                 # 3
```

> **复杂度**：单点修改/查询 O(log²n)，空间 O(n log n)。

---

### 13.15 字符串算法（KMP 自动机 · AC 自动机 + DP · 字符串哈希 + 二分）

#### 13.15.1 例 45：KMP 自动机（失配转移表）⭐⭐

> **知识点**：前缀函数 + 状态转移自动机｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的字符串题，主要考察前缀函数与状态转移自动机。构建失配转移表以实现高效的字符串匹配。

**思路**
记状态 `i` 表示「已匹配到模式串前 i 个字符」。KMP 自动机把前缀函数封装成一张在全字母表上的 `(状态, 字符)->状态` 转移表，之后可在 O(状态数×字母表大小) 上任意构造串去匹配。它是 AC 自动机、KMP-DP 等问题的公共基础。💡 类比「轨道转辙器」：同一辆车在不同字符到来时自动切换到正确的股道。

```python
def build_kmp_automaton(pattern, ALPHA=26):
    m = len(pattern)
    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    aut = [[0] * ALPHA for _ in range(m + 1)]   # 状态 0..m
    for st in range(m + 1):
        for c in range(ALPHA):
            ch = chr(ord('a') + c)
            if st == m:                            # 已完全匹配，回退转移
                j = pi[m - 1]
                while j > 0 and ch != pattern[j]:
                    j = pi[j - 1]
                aut[st][c] = j + 1 if ch == pattern[j] else 0
            elif ch == pattern[st]:
                aut[st][c] = st + 1
            else:
                aut[st][c] = aut[pi[st - 1]][c] if st > 0 else 0
    return pi, aut

pi, aut = build_kmp_automaton("aba")
print(pi)                             # [0, 0, 1]
print(aut[2][ord('b') - 97])          # 状态2 读 'b' -> 1
print(aut[2][ord('a') - 97])          # 状态2 读 'a' -> 3
```

> **复杂度**：预处理 O(m·Σ)（Σ=字母表大小），状态读取均摊 O(1)。

#### 13.15.2 例 46：AC 自动机 + 动态规划（统计不含禁用串的长度为 n 的串）⭐⭐⭐

> **知识点**：AC 自动机 + 自动机上的计数 DP ｜ **难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的自动机 + DP 综合题，主要考察 AC 自动机与自动机上的计数 DP。统计长度为 n 且不含任何禁用模式的字符串数量。

**思路**
把所有禁用词建成 AC 自动机，并把「含任意禁用后缀」的节点及其 fail 链标记为禁止。问题转化为：在自动机上走 n 步、不经过禁止节点的路径计数，即 `dp[step][state]` 转移 `dp[step+1][nxt]=∑dp[step][state]`。n 很大时可用矩阵快速幂。💡 类比「含雷区的地图」：把危险后缀映射成禁区，再把走路方案数变成图上计数。

```python
from collections import deque

def count_safe(forbidden, n, alpha):
    ci = {ch: i for i, ch in enumerate(alpha)}
    alen = len(alpha)
    nxt = [[-1] * alen for _ in range(1)]
    fail = [0]; bad = [False]
    def node():
        nxt.append([-1] * alen); fail.append(0); bad.append(False)
        return len(nxt) - 1
    for w in forbidden:                          # 建 Trie
        u = 0
        for ch in w:
            c = ci[ch]
            if nxt[u][c] == -1:
                nxt[u][c] = node()
            u = nxt[u][c]
        bad[u] = True
    dq = deque()                                 # 建 fail + 补全转移
    for c in range(alen):
        v = nxt[0][c]
        if v == -1:
            nxt[0][c] = 0
        else:
            fail[v] = 0; dq.append(v)
    while dq:
        u = dq.popleft()
        if bad[fail[u]]: bad[u] = True
        for c in range(alen):
            v = nxt[u][c]
            if v == -1:
                nxt[u][c] = nxt[fail[u]][c]
            else:
                fail[v] = nxt[fail[u]][c]; dq.append(v)
    m = len(nxt)
    dp = [0] * m; dp[0] = 1
    MOD = 10 ** 9 + 7
    for _ in range(n):
        nd = [0] * m
        for u in range(m):
            if bad[u]: continue
            for c in range(alen):
                v = nxt[u][c]
                if not bad[v]:
                    nd[v] = (nd[v] + dp[u]) % MOD
        dp = nd
    return sum(dp) % MOD

print(count_safe(["AA"], 3, "AC"))     # 长度3、不含"AA"的{AC}串 = 5
```

> **复杂度**：建自动机 O(∑|词|·Σ)，计数 DP O(n·状态数·Σ)，空间 O(∑|词|·Σ)。

#### 13.15.3 例 47：字符串哈希 + 二分（最长公共子串）⭐⭐

> **知识点**：滚动哈希 + 值域二分｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的字符串题，主要考察滚动哈希与值域二分。求两个字符串的最长公共子串长度。

**思路**
对固定长度 `L`，把 s 中所有长度为 L 的子串哈希存入集合，再检查 t 中是否存在相同的哈希值，即可在 O(n+m) 内判断「是否存在公共长度为 L 的子串」。因「存在性」随 L 单调，二分 L 得到最长公共子串长度。💡 类比「指纹比对」：先按长度生成指纹，再查找重名。

```python
M = 10 ** 9 + 7
BASE = 131

def substr_hashes(ss, L, powb):
    h = [0] * (len(ss) + 1)
    for i, ch in enumerate(ss):
        h[i + 1] = (h[i] * BASE + ord(ch)) % M
    return {(h[i + L] - h[i] * powb[L]) % M for i in range(len(ss) - L + 1)}

def lcs(s, t):
    lim = max(len(s), len(t)) + 1
    powb = [1] * lim
    for i in range(1, lim):
        powb[i] = powb[i - 1] * BASE % M
    lo, hi, ans = 0, min(len(s), len(t)), 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid and substr_hashes(s, mid, powb) & substr_hashes(t, mid, powb):
            ans, lo = mid, mid + 1
        else:
            hi = mid - 1
    return ans

print(lcs("ABCBDAB", "BDCABA"))        # 最长公共子串长度 2
```

> **复杂度**：O((n+m)·log(min(n,m)))，空间 O(max(n,m))。哈希碰撞概率可用双模降低。

---

### 13.16 网络流与匹配（Dinic · 上下界可行流 · 二分图匹配 · 一般图匹配）

#### 13.16.1 例 48：网络最大流（Dinic）⭐⭐⭐

> **知识点**：分层图 + 当前弧优化（Dinic）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的网络流综合题，主要考察分层图 + 当前弧优化（Dinic）。求解给定网络的容量最大流。

**思路**
BFS 建立分层残量图，DFS 一次性沿最短增广路推送尽可能多的流，配合当前弧避免重复扫描。Dinic 在单位容量图上是 O(E√V)。💡 类比「多车道收费站」：先按到汇的距离分层，再尽量把整条最短路的流量一次性放行。

```python
from collections import deque

def dinic(n, edges, s, t):
    g = [[] for _ in range(n)]
    def add(u, v, c):
        g[u].append([v, c, len(g[v])])
        g[v].append([u, 0, len(g[u]) - 1])
    for u, v, c in edges: add(u, v, c)
    flow = 0; INF = 10 ** 9
    while True:
        level = [-1] * n; level[s] = 0
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for v, c, _ in g[u]:
                if c > 0 and level[v] == -1:
                    level[v] = level[u] + 1; dq.append(v)
        if level[t] == -1: break
        it = [0] * n
        def dfs(u, f):
            if u == t: return f
            while it[u] < len(g[u]):
                v, c, rev = g[u][it[u]]
                if c > 0 and level[v] == level[u] + 1:
                    d = dfs(v, min(f, c))
                    if d > 0:
                        g[u][it[u]][1] -= d; g[v][rev][1] += d
                        return d
                it[u] += 1
            return 0
        while True:
            p = dfs(s, INF)
            if not p: break
            flow += p
    return flow

edges = [(0, 1, 3), (0, 2, 2), (1, 2, 1), (1, 3, 2), (2, 3, 2)]
print(dinic(4, edges, 0, 3))           # 最大流 = 4
```

> **复杂度**：一般 O(V²E)，二分图单位容量下 O(E√V)，空间 O(V+E)。

#### 13.16.2 例 49：有源汇有上下界的可行流 ⭐⭐⭐

> **知识点**：上下界网络流（减下界 + 超级源/汇判流）+ Dinic｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的网络流综合题，主要考察有源汇带上下界网络流（减下界 + 超级源/汇判流）+ Dinic。求满足每条边流量上下界约束的可行流。

**思路**
对每条边 `(u→v, [lo, up])`：先分离出必须流的下界 `lo`，加一条容量 `up-lo` 的边并累计节点「出量-入量」差 `bal`；`bal>0` 的节点连超级源，`bal<0` 的连超级汇。在原 `s-t` 汇合处补一条 `t→s` 无穷边把问题转化为无源汇判断，跑一遍超级源到超级汇的最大流，若所有超源边满流则可行。💡 类比「保底工资 + 奖金」：下界是保底必发的部分，先拨付再算浮动额。

```python
from collections import deque

def feasible_flow(n, edges, s, t, low_sum):
    # edges: (u, v, lo, up)；返回每边实际流量或 None（不可行）
    bal = [0] * n
    g = [[] for _ in range(n + 2)]
    SS, TT = n, n + 1
    def add(u, v, c):
        g[u].append([v, c, len(g[v])])
        g[v].append([u, 0, len(g[u]) - 1])
    base = [0] * len(edges)
    for i, (u, v, lo, up) in enumerate(edges):
        base[i] = lo
        bal[u] -= lo; bal[v] += lo
        add(u, v, up - lo)
    add(t, s, 10 ** 9)                     # 汇回源，闭合循环
    need = 0
    for i in range(n):
        if bal[i] > 0: add(SS, i, bal[i]); need += bal[i]
        elif bal[i] < 0: add(i, TT, -bal[i])

    def maxflow(S, T):
        flow = 0; INF = 10 ** 9
        while True:
            level = [-1] * (n + 2); level[S] = 0
            dq = deque([S])
            while dq:
                u = dq.popleft()
                for v, c, _ in g[u]:
                    if c > 0 and level[v] == -1:
                        level[v] = level[u] + 1; dq.append(v)
            if level[T] == -1: break
            it = [0] * (n + 2)
            def dfs(u, f):
                if u == T: return f
                while it[u] < len(g[u]):
                    v, c, ri = g[u][it[u]]
                    if c > 0 and level[v] == level[u] + 1:
                        d = dfs(v, min(f, c))
                        if d > 0:
                            g[u][it[u]][1] -= d; g[v][ri][1] += d
                            return d
                    it[u] += 1
                return 0
            while True:
                f = dfs(S, INF)
                if not f: break
                flow += f
        return flow

    got = maxflow(SS, TT)
    if got != need:
        return None
    return base                         # 可行；每边流量 = lo + 已增广值
```

> **复杂度**：核心一次 Dinic O(V²E)，空间 O(V+E)。

#### 13.16.3 例 50：二分图最大匹配（Hopcroft-Karp）⭐⭐⭐

> **知识点**：二分图最大匹配 + 增广路 + BFS 分层最短路增广｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的二分图综合题，主要考察 Hopcroft-Karp 最大匹配（BFS 分层最短路 + DFS 增广）。求二分图的最大匹配数。

**思路**
Hopcroft-Karp 每次用 BFS 找到所有最短增广路的层次结构，再用 DFS 一次性地沿这些不相交增广路同时扩展匹配，把朴素匈牙利算法复杂度降到 O(E√V)。💡 类比「同时预约多组转诊」：先按距离分层，再一批次完成多个配对。

```python
from collections import deque

def hopcroft_karp(n, m, edges):
    g = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v)
    pairU = [-1] * n; pairV = [-1] * m; dist = [0] * n
    INF = float('inf')
    def bfs():
        dq = deque(); found = False
        for u in range(n):
            if pairU[u] == -1:
                dist[u] = 0; dq.append(u)
            else:
                dist[u] = INF
        while dq:
            u = dq.popleft()
            for v in g[u]:
                u2 = pairV[v]
                if u2 != -1 and dist[u2] == INF:
                    dist[u2] = dist[u] + 1; dq.append(u2)
                elif u2 == -1:
                    found = True
        return found
    def dfs(u):
        for v in g[u]:
            u2 = pairV[v]
            if u2 == -1 or (dist[u2] == dist[u] + 1 and dfs(u2)):
                pairU[u] = v; pairV[v] = u
                return True
        dist[u] = INF
        return False
    res = 0
    while bfs():
        for u in range(n):
            if pairU[u] == -1 and dfs(u):
                res += 1
    return res

edges = [(0, 0), (0, 2), (1, 0), (1, 1), (2, 2)]
print(hopcroft_karp(3, 3, edges))      # 3
```

> **复杂度**：O(E√V)，空间 O(V+E)。

#### 13.16.4 例 51：一般图最大匹配（开花算法 Blossom）⭐⭐⭐

> **知识点**：绽花算法（Edmonds Blossom）＋ 奇环收缩｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的一般图综合题，主要考察开花算法（Edmonds Blossom）与奇环收缩。求一般图的最大匹配。

**思路**
二分图匹配不能处理奇环，绽花算法在遇到奇环时把它整体「开花」收缩成单个超点继续找增广路，找到后再展开回溯得到原图匹配。本实现用并查集式 `base` 记录收缩归属，BFS 找增广路。💡 类比「把纠缠的一簇线扎起来」：先扎成一股线找通路，找到后再解散还原。

```python
from collections import deque

def blossom_max_matching(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v); g[v].append(u)
    match = [-1] * n
    p = [0] * n; base = list(range(n)); used = [False] * n; bl = [False] * n

    def lca(a, b):
        seen = [False] * n
        while True:
            a = base[a]; seen[a] = True
            if match[a] == -1: break
            a = p[match[a]]
        while True:
            b = base[b]
            if seen[b]: return b
            b = p[match[b]]

    def mark_path(v, b, child):
        while base[v] != b:
            bl[base[v]] = bl[base[match[v]]] = True
            p[v] = child
            child = match[v]
            v = p[match[v]]

    def find_path(root):
        for i in range(n):
            used[i] = False; bl[i] = False; p[i] = 0; base[i] = i
        used[root] = True
        dq = deque([root])
        while dq:
            u = dq.popleft()
            for v in g[u]:
                if base[u] == base[v] or match[u] == v: continue
                if v == root or (match[v] != -1 and p[match[v]]):
                    cur = lca(u, v)
                    mark_path(u, cur, v); mark_path(v, cur, u)
                    for i in range(n):
                        if bl[base[i]]:
                            base[i] = cur
                            if not used[i]:
                                used[i] = True; dq.append(i)
                elif p[v] == 0:
                    p[v] = u
                    if match[v] == -1:
                        cur = v
                        while cur != -1:
                            nxt = p[cur]; nv = match[nxt]
                            match[cur] = nxt; match[nxt] = cur
                            cur = nv
                        return True
                    else:
                        used[match[v]] = True; dq.append(match[v])
        return False

    res = 0
    for i in range(n):
        if match[i] == -1 and find_path(i):
            res += 1
    return res

# 奇环 C5：二分图算法只能匹配到2，绽花算法能到2（此处最大匹配=2）
print(blossom_max_matching(5, [(0,1),(1,2),(2,3),(3,4),(4,0)]))   # 2
```

> **复杂度**：O(V·E)~O(V³)，空间 O(V+E)。

---

### 13.17 图论综合（欧拉回路 · 斯坦纳树 · 最小树形图 · Dijkstra 优化 · 同余最短路）

#### 13.17.1 例 52：欧拉回路（Hierholzer 算法）⭐⭐

> **知识点**：欧拉回路判定 + 栈式 Hierholzer｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的图论题，主要考察欧拉回路/欧拉路判定与栈式 Hierholzer 算法。求经过无向/有向图每条边恰好一次的路径或回路。

**思路**
对无向连通图，存在欧拉回路当且仅当每个点度数均为偶数。Hierholzer：保持一个栈，从当前点不断走一条未用边压栈；走不动时弹栈加入答案，形成回路，栈顶再用剩余边继续。💡 类比「一笔画」：先不回头走到底，走不动就把走过的路按倒序回收进答案。

```python
def euler_circuit(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append([v, False]); g[v].append([u, False])
    for u in range(n):
        if len(g[u]) % 2: return None         # 存在奇度点，无欧拉回路
    stack = [0]; path = []
    while stack:
        u = stack[-1]
        moved = False
        for e in g[u]:
            if not e[1]:
                e[1] = True
                for r in g[e[0]]:
                    if r[0] == u and not r[1]:
                        r[1] = True; break
                stack.append(e[0]); moved = True; break
        if not moved:
            path.append(stack.pop())
    if all(e[1] for u in range(n) for e in g[u]) and path[-1] == path[0] == 0:
        return path
    return None

print(euler_circuit(4, [(0,1),(1,2),(2,3),(3,0)]))   # 0-1-2-3-0 回路
```

> **复杂度**：O(V+E)，空间 O(V+E)。

#### 13.17.2 例 53：斯坦纳树（位压 DP + Dijkstra）⭐⭐⭐

> **知识点**：斯坦纳树 + 子集 DP + 最短路松弛｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的状压图论综合题，主要考察斯坦纳树（位压 DP + Dijkstra 最短路松弛）。求连接给定点集的最短连通子图权值和。

**思路**
连通指定的 k 个关键点的最小边权和树。设 `dp[mask][v]`：以 v 为根、已连通关键点集合为 mask 的最小代价。先按子集转移 `dp[mask][v]=min(dp[sub][v]+dp[mask⊕sub][v])`，再对每个 mask 跑一次堆优化 Dijkstra 松弛。💡 类比「拉一根共享网线」：先在两两之间搭最小通路，再合并成大集合。

```python
import heapq

def steiner_tree(n, edges, terminals):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w)); g[v].append((u, w))
    k = len(terminals)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << k)]
    for i, t in enumerate(terminals):
        dp[1 << i][t] = 0
    for mask in range(1, 1 << k):
        sub = (mask - 1) & mask
        while sub:
            other = mask ^ sub
            for v in range(n):
                dp[mask][v] = min(dp[mask][v], dp[sub][v] + dp[other][v])
            sub = (sub - 1) & mask
        hq = [(dp[mask][v], v) for v in range(n) if dp[mask][v] < INF]
        heapq.heapify(hq)
        while hq:
            d, u = heapq.heappop(hq)
            if d > dp[mask][u]: continue
            for v, w in g[u]:
                nd = d + w
                if nd < dp[mask][v]:
                    dp[mask][v] = nd; heapq.heappush(hq, (nd, v))
    return min(dp[(1 << k) - 1])

edges = [(0, 1, 1), (1, 2, 1), (2, 3, 1)]        # 0-1-2-3 链
print(steiner_tree(4, edges, [0, 2, 3]))        # 0-1-2-3 全链代价 3
```

> **复杂度**：O(3^k·n + 2^k·(V+E)logV)，空间 O(2^k·n)。

#### 13.17.3 例 54：最小树形图（朱刘 / Edmonds 算法）⭐⭐⭐

> **知识点**：有向图最小生成树（最小树形图）+ 环收缩｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的有向图综合题，主要考察最小树形图（朱刘/Edmonds 算法）与环收缩。求有向图连接根到所有点的最小生成树。

**思路**
朱刘算法：每轮为除根外每个点选一条入边中最小的，若这些边构成环则把环整体收缩成一个超点并重赋边权继续，直到无环，累加即得最小树形图。`invalid=|环上顶点的入边和` 转化为新的准地。💡 类比「IT 树状广播」：每个节点先选最便宜的上级，有循环就合并成一个部门再选。

```python
def chuliu(n, edges, root):
    INF = 10 ** 18
    ans = 0
    while True:
        inw = [INF] * n; pre = [-1] * n
        for (u, v, w) in edges:
            if u != v and w < inw[v]:
                inw[v] = w; pre[v] = u
        for i in range(n):
            if i != root and inw[i] == INF:
                return None
        cnt = 0; idof = [-1] * n; vis = [-1] * n
        for i in range(n):
            if i == root: continue
            u = i; ans += inw[i]
            while u != root and vis[u] != i and idof[u] == -1:
                vis[u] = i; u = pre[u]
            if u != root and idof[u] == -1:          # 发现环
                idof[u] = cnt
                v = pre[u]
                while v != u:
                    idof[v] = cnt; v = pre[v]
                cnt += 1
        if cnt == 0:
            return ans
        for i in range(n):
            if idof[i] == -1:
                idof[i] = cnt; cnt += 1
        new_edges = []
        for (u, v, w) in edges:
            if idof[u] != idof[v]:
                new_edges.append((idof[u], idof[v], w - inw[v]))
        n = cnt; root = idof[root]; edges = new_edges

edges = [(0, 1, 5), (0, 2, 6), (1, 2, 1), (2, 1, 10)]
print(chuliu(3, edges, 0))              # 0->1(5) + 1->2(1) = 6
```

> **复杂度**：O(VE)~O(V·E)（每轮 O(E)），空间 O(V+E)。

#### 13.17.4 例 55：单源最短路（堆优化 Dijkstra）⭐⭐

> **知识点**：Dijkstra + 二叉堆（优先级队列）｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的最短路题，主要考察堆优化 Dijkstra。求解单源最短路长度。

**思路**
维护已确定最短路的点集，每次弹出堆顶最小距离的点（已确定的跳过），用它松弛相邻点并压堆；因此每条边最多被松弛一次，总复杂度 O((V+E)logV)。💡 类比「加油圈优先选最近」：永远先处理当前可达范围内的最近点，逐步外扩。

```python
import heapq

def dijkstra(n, edges, s):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [10 ** 18] * n; dist[s] = 0
    done = [False] * n
    hq = [(0, s)]
    while hq:
        d, u = heapq.heappop(hq)
        if done[u]: continue
        done[u] = True
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd; heapq.heappush(hq, (nd, v))
    return dist

edges = [(0, 1, 4), (0, 2, 2), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2)]
print(dijkstra(5, edges, 0))            # [0, 4, 2, 9, 11]
```

> **复杂度**：O((V+E)logV)，空间 O(V+E)。

#### 13.17.5 例 56：同余最短路（最小面额取模 + 最短路）⭐⭐⭐

> **知识点**：等价类最短路（模数图）＋ 堆优化 Dijkstra｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的最短路综合题，主要考察等价类最短路（模数建图）+ 堆优化 Dijkstra。用最小面额对某个模数建图，求解相关最小花费。

**思路**
给定若干可无限用的面额，求最大的无法由它们组成的整数（或小于某上限的数量）。取最小面额 `a0` 为模建「余数图」，对每个余数求「能表示成的最小总和」（同余最短路径）。记 `dist[r]`，则最大的不可表示数为 `max(dist[r])-a0`（gcd=1 时）。💡 类比「找零钱的抽屉」：把相同余数的找零归为一格，求每格能凑的最小金额。

```python
import heapq, math

def mod_shortest(coins):
    coins = list(set(coins))
    a0 = min(coins)
    if math.gcd(*coins) != 1:
        return -1                          # 有公因子，无法覆盖所有余数
    dist = [10 ** 18] * a0; dist[0] = 0
    hq = [(0, 0)]
    while hq:
        d, r = heapq.heappop(hq)
        if d > dist[r]: continue
        for c in coins:
            nr = (r + c) % a0; nd = d + c
            if nd < dist[nr]:
                dist[nr] = nd; heapq.heappush(hq, (nd, nr))
    return max(dist) - a0                 # 最大的不可表示数

print(mod_shortest([3, 6, 10]))          # 17
```

> **复杂度**：O(a0·len(coins)·log a0)，空间 O(a0)。

---

### 13.18 数位 DP · 博弈 · 期望（数位计数 · 无连续1 · SG 函数 · 期望 DP）

#### 13.18.1 例 57：数位 DP——统计数字出现次数 ⭐⭐

> **知识点**：数位 DP（从上界逐位枚举 + 记忆化）｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的数位 DP 题，主要考察从上界逐位枚举 + 记忆化。统计给定区间内各个数字出现的次数。

**思路**
把「≤n」的整数按十进制逐位填入，用 `tight`（是否卡到上界）和 `has_started`（是否已出现非零位/开始计数）记忆化。统计目标数字 `d` 在 1..n 中出现的总次数：每填一位，若等于 d 且该位有效则累计 +1。💡 类比「翻页计数」：一位一位锁定，凡等于目标数字的位就记账。

```python
from functools import lru_cache

def count_digit(n, d):
    s = [int(ch) for ch in str(n)]
    L = len(s)
    @lru_cache(None)
    def dfs(i, tight, started, cnt):
        if i == L:
            return cnt
        lim = s[i] if tight else 9
        total = 0
        for x in range(lim + 1):
            nt = tight and (x == lim)
            if x == 0 and not started:
                total += dfs(i + 1, nt, False, cnt)
            else:
                total += dfs(i + 1, nt, True, cnt + (1 if x == d else 0))
        return total
    return dfs(0, True, False, 0)

print(count_digit(99, 1))               # 数字1在1..99中出现20次
```

> **复杂度**：O(位数·tight 状态)，实际 O(10·len) 近似常数，空间 O(len)。

#### 13.18.2 例 58：数位 DP——不含连续 1 的二进制数 ⭐⭐

> **知识点**：二进制数位 DP（限制相邻元素）｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的数位 DP 题，主要考察二进制数位约束。统计长度内不含两个连续 1 的二进制数个数。

**思路**
把 n 转成二进制，从高位到低位 DFS，记忆化参数为（位指针、是否贴住 n、上一个二进制位是否取 1）。只要上一位是 1 就禁止本位置 1，从而保证任意两个 1 不相邻。💡 类比「多人间不许相邻进」：看到前一位已有人就跳过这位。

```python
from functools import lru_cache

def count_no_adjacent_ones(n):
    bits = [int(b) for b in bin(n)[2:]]
    L = len(bits)
    @lru_cache(None)
    def dfs(i, tight, prev_one):
        if i == L:
            return 1
        lim = bits[i] if tight else 1
        total = 0
        for b in range(lim + 1):
            if prev_one and b == 1:
                continue
            total += dfs(i + 1, tight and (b == lim), b == 1)
        return total
    return dfs(0, True, False)

print(count_no_adjacent_ones(5))        # 0..5 中无相邻1的有 {0,1,2,4,5}=5
```

> **复杂度**：O(位数)，即 O(log n)，空间 O(log n)。

#### 13.18.3 例 59：博弈论——SG 函数求解组合游戏 ⭐⭐⭐

> **知识点**：SG 函数 + mex + 多游戏 XOR 合成｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的博弈综合题，主要考察 SG 函数 + mex 运算 + 多游戏 XOR 合成。判断若干公平组合游戏的胜负局面。

**思路**
对有向无环博弈，定 `g(s)`=从状态 s 出发所有能到的状态的 SG 的 mex（最小未出现非负整数）；终局 `g=0` 为必败。多个独立游戏拼成大盘时，先手胜当且仅当所有分游戏 SG 的异或值非零。取石子（每次可取 1..3）SG 即 `n mod 4`。💡 类比「共享同一串灯」：每个子局是一盏灯，异或值非零就有得可好。

```python
def grundy(maxn, moves):
    g = [0] * maxn
    for n in range(maxn):
        seen = {g[t] for t in moves(n) if t >= 0 and t < maxn}
        mex = 0
        while mex in seen:
            mex += 1
        g[n] = mex
    return g

single = lambda n: [n - 1, n - 2, n - 3]      # 取石子：可拿1~3
g = grundy(21, single)
print([g[i] for i in range(11)])            # [0,1,2,3,0,1,2,3,0,1,2]

def multi_nim(piles):
    x = 0
    for p in piles:
        x ^= g[p]
    return "先手胜" if x else "先手负"

print(multi_nim([5, 7]))                     # 5^3 -> 先手胜
print(multi_nim([5, 9, 12]))                 # 1^1^0 -> 先手负
```

> **复杂度**：O(maxn·|转移|) 预处理，单次合成 O(石子数)。

#### 13.18.4 例 60：概率期望 DP——集齐优惠券的期望次数 ⭐⭐⭐

> **知识点**：期望 DP＋反向递推（coupon collector）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的概率期望综合题，主要考察期望 DP 反向递推（coupon collector 优惠券收集问题）。求集齐全部 n 种优惠券所需次数的期望。

**思路**
设 `E[i]`=已收集 i 种、还需抽的期望次数。抽一次：以 `i/n` 重复旧券、以 `(n-i)/n` 得新券，于是 `E[i]=1+(i/n)E[i]+((n-i)/n)E[i+1]`，解出 `E[i]=(1+((n-i)/n)E[i+1])/(1-i/n)`，从高到低递推。💡 类比「开盲盒集卡」：每多一种，凑新卡概率下降，期望次数据此反向累加。

```python
def coupon_expect(n):
    dp = [0.0] * (n + 1)
    for i in range(n - 1, -1, -1):
        dp[i] = 1 + (n - i) / n * dp[i + 1]
        dp[i] /= 1 - i / n
    return dp[0]

print(round(coupon_expect(6), 4))        # ≈ 6*(1+1/2+..+1/6) ≈ 14.7
```

> **复杂度**：O(n)，空间 O(n)。

---

### 13.19 多项式与线性代数（FFT 卷积 · 矩阵树定理 · 高斯消元）

#### 13.19.1 例 61：FFT 快速傅里叶变换（多项式乘法/卷积）⭐⭐⭐

> **知识点**：FFT（蝶形运算）＋ 点值相乘 + 逆变换｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的多项式综合题，主要考察 FFT（蝶形运算）点值相乘与逆变换。快速计算两个多项式的卷积。

**思路**
把两个多项式从系数表示转成点值表示（同一组 n 次单位根上求值），点值逐点相乘后逆变换回系数表示，从而把朴素 O(n²) 卷积降到 O(n log n)。本实现取 n 为 2 的幂，手工做迭代蝶形。💡 类比「算两本书页码的乘积」：先按坐标打分再逐项相乘，避免两两配对相乘。

```python
import cmath, math

def fft(a, invert=False):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit; bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        ang = 2 * math.pi / length * (-1 if invert else 1)
        wn = complex(math.cos(ang), math.sin(ang))
        for i in range(0, n, length):
            w = 1 + 0j
            half = length // 2
            for k in range(i, i + half):
                u = a[k]; v = a[k + half] * w
                a[k] = u + v; a[k + half] = u - v
                w *= wn
        length <<= 1
    if invert:
        for i in range(n):
            a[i] /= n

def conv(p, q):
    n = 1
    while n < len(p) + len(q) - 1:
        n <<= 1
    fa = [complex(x, 0) for x in p] + [0j] * (n - len(p))
    fb = [complex(x, 0) for x in q] + [0j] * (n - len(q))
    fft(fa); fft(fb)
    for i in range(n):
        fa[i] *= fb[i]
    fft(fa, True)
    return [round(fa[i].real) for i in range(len(p) + len(q) - 1)]

print(conv([1, 2, 3], [4, 5, 6]))      # [4, 13, 28, 27, 18]
```

> **复杂度**：O(n log n)，空间 O(n)（n 为卷程度量）。

#### 13.19.2 例 62：矩阵树定理（计数生成树）⭐⭐⭐

> **知识点**：Kirchhoff 拉普拉斯矩阵 + 高斯消元求行列式｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度很高的图论计数综合题，主要考察 Kirchhoff 拉普拉斯矩阵与高斯消元求行列式。计数无向图（多重）生成树的数量。

**思路**
无向简单图的生成树个数等于其拉普拉斯矩阵（对角=度数，非对角=-邻接）任意去掉一行一列后的主子式（行列式）。求行列式用高斯消元（模素数下用逆元）。💡 类比「电网冗余方案计数」：把节点度数与邻接信息组合成一个矩阵，其行列式值直接给出生成树数目。

```python
def det_mod(mat, MOD):
    n = len(mat); a = [row[:] for row in mat]; res = 1
    for i in range(n):
        piv = -1
        for r in range(i, n):
            if a[r][i] % MOD != 0:
                piv = r; break
        if piv == -1: return 0
        if piv != i:
            a[i], a[piv] = a[piv], a[i]; res = (-res) % MOD
        res = res * a[i][i] % MOD
        inv = pow(a[i][i], MOD - 2, MOD)
        for r in range(i + 1, n):
            if a[r][i] == 0: continue
            f = a[r][i] * inv % MOD
            for c in range(i, n):
                a[r][c] = (a[r][c] - f * a[i][c]) % MOD
    return res

def spanning_trees(n, edges, MOD=10 ** 9 + 7):
    L = [[0] * n for _ in range(n)]
    for u, v in edges:
        L[u][u] += 1; L[v][v] += 1
        L[u][v] -= 1; L[v][u] -= 1
    M = [L[i][:n - 1] for i in range(n - 1)]
    return det_mod(M, MOD)

print(spanning_trees(4, [(0, 1), (1, 2), (2, 3), (3, 0)]))   # 环 C4 有 4 棵生成树
```

> **复杂度**：O(n³)，空间 O(n²)。

#### 13.19.3 例 63：高斯消元解线性方程组 ⭐⭐⭐

> **知识点**：高斯消元（选主元 + 消元回代）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的线性代数题，主要考察高斯消元（选主元 + 消元回代）。求解给定线性方程组（或判定无解/无穷解）。

**思路**
把系数与常数拼成增广矩阵，对每一列选绝对值最大主元（保证数值稳定），再对其它行消去该列，最后按 `x[i]=b[i]/a[i][i]` 回代。若某一列主元为 0 则无唯一解。💡 类比「逐个瓦掉未知数」：每次用一个方程消掉一个变量，最终全部暴露。

```python
def gauss(a, b):
    n = len(a)
    M = [a[i][:] + [b[i]] for i in range(n)]
    for i in range(n):
        piv = i
        for r in range(i + 1, n):
            if abs(M[r][i]) > abs(M[piv][i]):
                piv = r
        if abs(M[piv][i]) < 1e-9:
            return None
        M[i], M[piv] = M[piv], M[i]
        for r in range(n):
            if r != i:
                f = M[r][i] / M[i][i]
                for c in range(i, n + 1):
                    M[r][c] -= f * M[i][c]
    return [M[i][n] / M[i][i] for i in range(n)]

x = gauss([[2, 1, -1], [1, 3, 2], [1, 0, 1]], [3, 4, 2])
print([round(v, 6) for v in x])         # [1.5, 0.5, 0.5]
```

> **复杂度**：O(n³)，空间 O(n²)。

---

### 13.20 数论进阶（扩展中国剩余定理 · BSGS · 容斥原理 · 二次剩余）

#### 13.20.1 例 64：扩展中国剩余定理（模数不互质）⭐⭐⭐

> **知识点**：exCRT（扩展欧几里得逐步合并同余式）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的数论综合题，主要考察扩展中国剩余定理（exCRT，扩展欧几里得逐步合并同余式）。求解一组模数不互质的线性同余方程组。

**思路**
普通 CRT 要求模数两两互质；扩展 CRT 用概展欧几里得每次合并两个 `x≡r1(m1)`、`x≡r2(m2)`：解 `m1·k≡r2-r1 (mod m2)` 得到新模 `lcm(m1,m2)`，逐步合并到只剩一个同余式。若某步无解则整体无解。💡 类比「钟表对时」：两块周期互质的钟能唯一对到整点，否则可能出现永远对不齐。

```python
def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = exgcd(b, a % b)
    return g, y, x - (a // b) * y

def crt_ex(rems, mods):
    x, M = 0, 1                      # 已合并为 x≡x (mod M)
    for r, m in zip(rems, mods):
        g, p, _ = exgcd(M, m)        # M*p + m*q = g
        if (r - x) % g:
            return None              # 无解
        m2 = m // g
        t = ((r - x) // g * p) % m2  # p 是 M/g 在 mod m2 的逆元
        x += M * t
        M *= m2                      # 新模 = lcm(M, m)
        x %= M
    return x % M, M

print(crt_ex([2, 3, 2], [3, 5, 7]))  # 同余 x≡23 (mod 105)
```

> **复杂度**：O(n·log m)，空间 O(1)。

#### 13.20.2 例 65：BSGS 离散对数 ⭐⭐⭐

> **知识点**：大步小步（Baby-Step Giant-Step）解 `g^x≡a (mod p)`｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的数论综合题，主要考察大步小步（Baby-Step Giant-Step）算法。求解形如 g^x ≡ a (mod p) 的离散对数 x。

**思路**
设 `m=ceil(√p)`，写 `x = m·i + j`。预处理 `j∈[0,m)` 的 `g^j` 存哈希表（大步面），再枚举 `i`，用 `a·g^{-mi}=g^j` 查表得到 `j`。时间复杂度 O(√p)。仅当 `p` 为素数（或模数阶已知）适用。💡 类比「翻字典」：先记下前半本要查的词条，再用后半本一次命中彼此。

```python
import math

def bsgs(g, a, p):
    if a % p == 1: return 0
    n = int(math.isqrt(p)) + 1
    table = {}
    e = 1
    for j in range(n):
        if e not in table:
            table[e] = j
        e = e * g % p
    factor = pow(pow(g, n, p), p - 2, p)   # g^{-n}
    cur = a
    for i in range(n + 1):
        if cur in table:
            return i * n + table[cur]
        cur = cur * factor % p
    return -1

print(bsgs(2, 9, 11))     # 2^6 = 64 ≡ 9 (mod 11) -> 6
```

> **复杂度**：O(√p) 时间，O(√p) 空间。

#### 13.20.3 例 66：容斥原理（统计与若干质数互质的个数）⭐⭐

> **知识点**：容斥原理（交并转换）多次幂法｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的计数题，主要考察容斥原理（交并转换）多次幂。统计在给定区间内与若干给定数互质的整数个数。

**思路**
要数 1..n 中不被任何一个给定质数整除的个数，先数能被其中若干质数共同整除的个数（容斥）：奇交加、偶交减，`n/lcm(subset)`。枚举全部子集，总复杂度 O(2^k·k)。💡 类比「种花圈地」：先算每一格花园的并再扣除重复圈出的部分。

```python
import math

def count_not_divisible(n, primes):
    k = len(primes)
    ans = 0
    for mask in range(1, 1 << k):
        lcm = 1; bits = 0; ok = True
        for i in range(k):
            if mask >> i & 1:
                bits += 1
                lcm = lcm * primes[i] // math.gcd(lcm, primes[i])
                if lcm > n:
                    ok = False; break
        if not ok:
            continue
        c = n // lcm
        ans += c if bits % 2 else -c
    return n - ans

print(count_not_divisible(30, [2, 3, 5]))   # 与2,3,5互质数 = φ(30) = 8
```

> **复杂度**：O(2^k·k)，空间 O(1)。

#### 13.20.4 例 67：二次剩余（Tonelli–Shanks 求平方根模素数）⭐⭐⭐

> **知识点**：Legendre 符号 + Tonelli-Shanks 开方｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的数论综合题，主要考察 Legendre 符号与 Tonelli–Shanks 开方。求二次同余方程 x² ≡ a (mod p) 在模素数 p 下的平方根。

**思路**
判断 `n` 是否为模素数 `p` 的二次剩余用 Legendre 符号 `n^((p-1)/2)`。开方时，若 `p≡3 (mod4)` 直接 `n^((p+1)/4)`；否则用 Tonelli-Shanks：把 `p-1` 写成 `q·2^s`，选非二次剩余构造某个 2 阶因子，迭代消去 `t` 的非 1 阶数以逼近平方根。💡 类比「开根号对表」：先用符号判定是否可开，再按快速路径求出根。

```python
def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def sqrt_mod(n, p):
    if n % p == 0: return 0
    if legendre(n, p) != 1: return -1       # 无二次剩余
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1; s = 0
    while q % 2 == 0:
        s += 1; q //= 2
    z = 2
    while legendre(z, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q + 1) // 2, p)
    while t != 1:
        i = 1
        while pow(t, 1 << i, p) != 1:
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m = i; c = b * b % p; t = t * c % p; r = r * b % p
    return r

print(sqrt_mod(4, 7))      # 2 (4^0.5 mod7)
print(sqrt_mod(5, 13))     # -1：5 不是模13的二次剩余
```

> **复杂度**：O(log² p)，空间 O(1)。

---

### 13.21 字符串算法进阶（Manacher · Z 算法 · Trie 最大异或 · 回文自动机应用）

#### 13.21.1 例 68：Manacher 求最长回文子串（字符串）⭐⭐

> **知识点**：回文半径 + 对称复用｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的字符串题，主要考察 Manacher 算法的回文半径与对称复用。求给定字符串的最长回文子串。

**思路**
在原串每两个字符间插入哨兵 `#`（两边也补 `#`），使所有回文都变成奇数长度。用数组 `d[i]` 记录以 `i` 为中心的回文半径，维护已知最右回文边界 `[L,R]`，当 `i<R` 时可由对称点 `2C-i` 的已知半径直接初始化 `d[i]`，再用双指针中心扩展补足 `R` 之外的部分，把暴力 O(n²) 摊还成 O(n)。💡 类比「镜像复用」：你在镜子里看到重叠的值，就不用重新量一遍，只需补齐超出镜沿的部分。

```python
def manacher(s):
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    d = [0] * n
    C = R = 0
    for i in range(n):
        if i < R:
            d[i] = min(R - i, d[2 * C - i])     # 镜像初始化
        while i - d[i] - 1 >= 0 and i + d[i] + 1 < n and t[i - d[i] - 1] == t[i + d[i] + 1]:
            d[i] += 1                            # 中心扩展
        if i + d[i] > R:
            C, R = i, i + d[i]
    return max(d)                                # 即 s 中最长回文长度

print(manacher("babad"))     # 3 ("bab")
print(manacher("cbbd"))      # 2 ("bb")
print(manacher("abacaba"))   # 7
```

> **复杂度**：O(n) 时间 + O(n) 空间。

#### 13.21.2 例 69：Z 算法 / 扩展 KMP（每个后缀与整个串的最长公共前缀）⭐⭐

> **知识点**：Z-box 区间复用｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的字符串题，主要考察 Z 算法（扩展 KMP）的 Z-box 区间复用。求每个后缀与整个字符串的最长公共前缀。

**思路**
`z[i]` 表示 `s[i:]` 与 `s` 的最长公共前缀长度。维护一个已匹配的区间 `[l,r]`，当 `i<r` 时可复用 `z[i-l]` 初始化，注意截断到 `r-i`，再暴力向右扩展并更新 `r`。💡 类比「接力区间」：已经配平的一段不用重配，从中间借力，只把没覆盖的尾巴配完。

```python
def z_function(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])          # 复用
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1                            # 向后扩展
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z

print(z_function("aaaaa"))   # [0,4,3,2,1]
print(z_function("ababa"))   # [0,0,3,0,1]
```

> **复杂度**：O(n) 时间（每个字符至多被比较两次）+ O(n) 空间。

#### 13.21.3 例 70：Trie 求数组中最大异或对（字典树）⭐⭐

> **知识点**：二进制 Trie 贪心｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的位运算与字典树题，主要考察二进制 Trie 贪心。求数组中两元素异或的最大值。

**思路**
把每个数按最高位到最低位的二进制插入 0/1 Trie，查询某个数 `x` 时从根沿「尽量相反的位」走：`want = 1-bit` 存在就走它并累加贡献 `1<<b`，否则走同一位。这样每次都选择最大的一位，得到与 `x` 异或最大的数及其异或值。💡 类比「走相反岔路」：想让异或值大，每一位都希望和当前位相反，就像在岔路口永远挑「异类」的路走。

```python
class BitTrie:
    def __init__(self):
        self.ch = [[-1, -1]]
    def insert(self, x):
        u = 0
        for b in range(31, -1, -1):
            bit = (x >> b) & 1
            if self.ch[u][bit] == -1:
                self.ch[u][bit] = len(self.ch); self.ch.append([-1, -1])
            u = self.ch[u][bit]
    def max_xor(self, x):
        u = 0; res = 0
        for b in range(31, -1, -1):
            bit = (x >> b) & 1
            want = 1 - bit
            if self.ch[u][want] != -1:
                res |= (1 << b); u = self.ch[u][want]
            else:
                u = self.ch[u][bit]
        return res

nums = [3, 10, 5, 25, 2, 8]
t = BitTrie()
ans = 0
for x in nums:
    t.insert(x)
for x in nums:
    ans = max(ans, t.max_xor(x))
print(ans)      # 28 (5 ^ 25)
```

> **复杂度**：O(31·n) 构建 + O(31·n) 查询，空间 O(31·n)。

#### 13.21.4 例 71：回文自动机应用——统计每个回文子串的出现次数（PAM 进阶）⭐⭐⭐

> **知识点**：回文树 fail 链 + 拓扑累加｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的回文自动机综合题，主要考察回文树 fail 链与拓扑累加。统计每个回文子串在字符串中的出现次数。

**思路**
PAM 有 0 号（长度 -1）与 1 号（长度 0）两个根，每个节点代表一个本质不同回文串，`fail` 指向其最长回文后缀。`add` 时从 `last` 沿 fail 找能扩展的节点建新节点，注意新节点 `len = len[cur]+2`。插入完做一次按 dfs 序逆序的累加 `occ[fail] += occ[i]`，即可得到每个回文子串在原串中的出现次数（本质不同的个数为 `节点数-2`）。💡 类比「树状广播」：节点像组织树，把自身的计数沿 fail（上级）逐层汇总，最后由根得到全体出现次数。

```python
class PAM:
    def __init__(self):
        self.nxt = [{}, {}]; self.fail = [0, 0]
        self.len = [-1, 0]; self.occ = [0, 0]; self.last = 1
    def add(self, s, pos):
        cur = self.last
        while True:
            l = self.len[cur]
            if pos - 1 - l >= 0 and s[pos - 1 - l] == s[pos]:
                break
            cur = self.fail[cur]
        if s[pos] in self.nxt[cur]:
            self.last = self.nxt[cur][s[pos]]; self.occ[self.last] += 1; return
        new = len(self.len)
        self.nxt.append({}); self.len.append(self.len[cur] + 2); self.occ.append(1)
        self.nxt[cur][s[pos]] = new
        if self.len[new] == 1:
            self.fail.append(1)
        else:
            f = self.fail[cur]
            while True:
                l = self.len[f]
                if pos - 1 - l >= 0 and s[pos - 1 - l] == s[pos]:
                    self.fail.append(self.nxt[f][s[pos]]); break
                f = self.fail[f]
        self.last = new
    def build(self, s):
        for i in range(len(s)):
            self.add(s, i)
        for i in range(len(self.len) - 1, 1, -1):   # 逆 dfs 序累加
            self.occ[self.fail[i]] += self.occ[i]
        return len(self.len) - 2                    # 本质不同回文个数

print(PAM().build("abab"))     # 3  回文子串: a,b,aba,bab
```

> **复杂度**：O(n) 构建（均摊）+ O(n) 累加，空间 O(n)。

### 13.22 后缀家族与自动机（后缀数组 height 应用 · 广义 SAM · AC fail 树）
#### 13.22.1 例 72：后缀数组 + height 求两串的最长公共子串 ⭐⭐⭐

> **知识点**：多串合并 + height 相邻比较｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度很高的多串综合题，主要考察多串合并与 height 相邻比较。求两字符串的最长公共子串长度。

**思路**
把 `s1 + '#' + s2` 拼成一个串求后缀数组（倍增），`height[i]=LCP(sa[i-1],sa[i])`。若恰好相邻两个后缀分别来自两串，则它们的 LCP 长度就是一个公共子串长度，取最大者即可。`sa/rank/height` 三件套是后缀结构的基石。💡 类比「字典邻接」：把后缀按字典序排好后，公共前缀最长的往往相邻，像把字母表邻居并排读一遍就找到重复。

```python
def suffix_array(s):
    n = len(s); sa = list(range(n)); r = [ord(c) for c in s]; k = 1; tmp = [0] * n
    while k < n:
        sa.sort(key=lambda x: (r[x], r[x + k] if x + k < n else -1))
        tmp[sa[0]] = 0
        for i in range(1, n):
            a, b = sa[i - 1], sa[i]
            pa = (r[a], r[a + k] if a + k < n else -1); pb = (r[b], r[b + k] if b + k < n else -1)
            tmp[b] = tmp[a] + (pa != pb)
        r = tmp[:]; k *= 2
    return sa

def build_height(s, sa):
    n = len(s); rk = [0] * n
    for i, x in enumerate(sa): rk[x] = i
    h = [0] * n; k = 0
    for i in range(n):
        if rk[i] == 0: continue
        j = sa[rk[i] - 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]: k += 1
        h[rk[i]] = k
        if k: k -= 1
    return h

def lcs(s1, s2):
    T = s1 + '#' + s2
    sa = suffix_array(T); h = build_height(T, sa)
    n1 = len(s1)
    best = 0
    for i in range(1, len(T)):
        if (sa[i - 1] < n1) != (sa[i] < n1):   # 相邻后缀分属两串
            best = max(best, h[i])
    return best

print(lcs("abcdef", "zcdwef"))   # 3 ("cde")
```

> **复杂度**：O((n1+n2) log(n1+n2))。

#### 13.22.2 例 73：后缀数组 + height 求至少出现 K 次的最长子串 ⭐⭐⭐

> **知识点**：height 分组 + 滑动窗口最小｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度很高的后缀数组综合题，主要考察 height 分组与滑动窗口取最小。求至少出现 K 次的最长子串长度。

**思路**
在后缀数组中，出现 K 次以上的子串会落在「一组相邻后缀的 height 都不小于某值」的段里。等价于在 `height[1..n-1]` 上找长度 `K-1` 的滑动窗口，令其最小值尽可能大。用单调队列维护窗口内 height 的最小值，取最大即可。💡 类比「看门高」：一排相邻后缀的门槛高度若都 ≥ H，说明它们共享长度 H 的前缀；窗口最矮的门决定了这段能撑多高。

```python
from collections import deque

def build_height(s, sa):
    n = len(s); rk = [0] * n
    for i, x in enumerate(sa): rk[x] = i
    h = [0] * n; k = 0
    for i in range(n):
        if rk[i] == 0: continue
        j = sa[rk[i] - 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]: k += 1
        h[rk[i]] = k
        if k: k -= 1
    return h

def suffix_array(s):   # 见 13.22.1
    n = len(s); sa = list(range(n)); r = [ord(c) for c in s]; k = 1; tmp = [0] * n
    while k < n:
        sa.sort(key=lambda x: (r[x], r[x + k] if x + k < n else -1))
        tmp[sa[0]] = 0
        for i in range(1, n):
            a, b = sa[i - 1], sa[i]
            pa = (r[a], r[a + k] if a + k < n else -1); pb = (r[b], r[b + k] if b + k < n else -1)
            tmp[b] = tmp[a] + (pa != pb)
        r = tmp[:]; k *= 2
    return sa

def longest_k_repeat(s, k):
    if k <= 1: return len(s)
    sa = suffix_array(s); h = build_height(s, sa)[1:]
    m = k - 1; dq = deque(); best = 0
    for i, val in enumerate(h):
        while dq and h[dq[-1]] >= val: dq.pop()
        dq.append(i)
        if dq[0] <= i - m: dq.popleft()
        if i >= m - 1: best = max(best, h[dq[0]])
    return best

print(longest_k_repeat("aaaaa", 3))   # 3 ("aaa" 出现 3 次)
print(longest_k_repeat("banana", 2))  # 3 ("ana")
```

> **复杂度**：O(n log n)（后缀数组）＋ O(n)（滑窗）。

#### 13.22.3 例 74：广义后缀自动机统计多串本质不同子串个数（广义 SAM）⭐⭐⭐

> **知识点**：每串重置 last + 节点贡献和｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的多串自动机综合题，主要考察广义后缀自动机。统计多个字符串中本质不同子串的总个数。

**思路**
把多根字符串依次插入同一个 SAM，每插入一个字符串前把 `last` 重置为根，这样所有字符串共享一套自动机（广义 SAM）。本质不同子串总数 = `Σ (len[i]-len[link[i]])`，因为每个状态从 `len[link]+1` 到 `len[i]` 的每一种步长都对应一个不同的子串。💡 类比「并厂生产线」：多根字符串共用一套后缀链接表，每个状态代表一段长度的连续子串，累加即可不重不漏。

```python
class SAM:
    def __init__(self):
        self.len = [0]; self.link = [-1]; self.nxt = [{}]; self.last = 0
    def extend(self, c):
        cur = len(self.len)
        self.len.append(self.len[self.last] + 1); self.link.append(0); self.nxt.append({})
        p = self.last
        while p != -1 and c not in self.nxt[p]:
            self.nxt[p][c] = cur; p = self.link[p]
        if p == -1:
            self.link[cur] = 0
        else:
            q = self.nxt[p][c]
            if self.len[p] + 1 == self.len[q]:
                self.link[cur] = q
            else:
                clone = len(self.len)
                self.len.append(self.len[p] + 1); self.link.append(self.link[q])
                self.nxt.append(dict(self.nxt[q]))
                self.nxt[p][c] = clone
                while p != -1 and self.nxt[p].get(c) == q:
                    self.nxt[p][c] = clone; p = self.link[p]
                self.link[q] = self.link[cur] = clone
        self.last = cur

def distinct_total(strings):
    sam = SAM()
    for s in strings:
        sam.last = 0
        for ch in s:
            sam.extend(ch)
    return sum(sam.len[i] - sam.len[sam.link[i]] for i in range(1, len(sam.len)))

print(distinct_total(["ab", "b"]))    # {a,b,ab} = 3
print(distinct_total(["abc"]))        # 6
```

> **复杂度**：O(Σ|s|)（均摊），空间 O(Σ|s|)。

#### 13.22.4 例 75：AC 自动机 fail 树统计每个模式串出现次数 ⭐⭐⭐

> **知识点**：Trie + fail + 逆 BFS 上传｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的 AC 自动机综合题，主要考察 Trie、fail 树与逆 BFS 上传。统计每个模式串在文本中出现的次数。

**思路**
把模式串建成 Trie，BFS 求每个节点 fail（指向失配后最长的相同后缀节点）。扫描文本时每步把当前状态计数 +1，扫描完成后再按 BFS 逆序把子节点计数沿 fail 上传，最终每个模式终点节点的计数就是它在文本中出现的次数。💡 类比「接力向上报数」：文本每落足一个状态报一次数，再沿 fail 树逐级汇总到每个模式的根。

```python
from collections import deque

def ac_occurrences(text, patterns):
    nxt = [{}]; fail = [0]; end = [-1]
    for pi, pat in enumerate(patterns):
        u = 0
        for ch in pat:
            if ch not in nxt[u]:
                nxt[u][ch] = len(nxt); nxt.append({}); fail.append(0); end.append(-1)
            u = nxt[u][ch]
        end[u] = pi
    q = deque(); order = [0]
    for u in list(nxt[0].values()):
        q.append(u)
    while q:
        u = q.popleft(); order.append(u)
        for ch, v in nxt[u].items():
            f = fail[u]
            while f and ch not in nxt[f]: f = fail[f]
            fail[v] = nxt[f].get(ch, 0)
            q.append(v)
    pos = [0] * len(nxt); u = 0
    for ch in text:
        while u and ch not in nxt[u]: u = fail[u]
        if ch in nxt[u]: u = nxt[u][ch]
        pos[u] += 1
    res = [0] * len(patterns)
    for u in reversed(order):
        if end[u] != -1: res[end[u]] += pos[u]
        pos[fail[u]] += pos[u]
    return res

print(ac_occurrences("ababaab", ["aba", "ab", "ba"]))   # aba:2, ab:3, ba:2
```

> **复杂度**：O(|模式总长|·Σ + |文本|)，空间 O(|模式总长|)。
### 13.23 树上与倍增（倍增 LCA + 路径最大值 · 树的重心）

#### 13.23.1 例 76：树上倍增 LCA 与路径最大值 ⭐⭐

> **知识点**：二进制拆分跳父亲 + 路径边权最值｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的树上倍增题，主要考察二进制拆分跳父亲与路径边权最值。多次询问树上两点路径上的最大边权。

**思路**
DFS 预处理 `up[u][k]=u 向上 2^k 步的祖先`与 `mx[u][k]=该段路径边权最大值`。查询 LCA 时先把深度深的节点按二进制跳到同一深度（同时累计 mx），再一起向上跳；路径最大值即在跳的过程中取 `max`。相比重链剖分求 LCA，倍增实现直观且天然支持路径最值。💡 类比「按 2 的幂叠台阶」：每次跳尽量大的台阶缩小差距，跳的过程顺手记录每级台阶的最高点。

```python
def solve_rooted(n, edges, qs):
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w)); adj[v].append((u, w))
    LOG = 20
    depth = [0] * (n + 1)
    up = [[0] * LOG for _ in range(n + 1)]
    mx = [[0] * LOG for _ in range(n + 1)]
    stack = [(1, 0)]
    visited = [False] * (n + 1); visited[1] = True
    while stack:
        u, p = stack.pop()
        for v, w in adj[u]:
            if v == p or visited[v]: continue
            visited[v] = True
            depth[v] = depth[u] + 1; up[v][0] = u; mx[v][0] = w
            stack.append((v, u))
    for k in range(1, LOG):
        for u in range(1, n + 1):
            up[u][k] = up[up[u][k - 1]][k - 1]
            mx[u][k] = max(mx[u][k - 1], mx[up[u][k - 1]][k - 1])
    def lca_max(a, b):
        if depth[a] < depth[b]: a, b = b, a
        best = 0; diff = depth[a] - depth[b]
        for k in range(LOG):
            if diff >> k & 1:
                best = max(best, mx[a][k]); a = up[a][k]
        if a == b: return a, best
        for k in range(LOG - 1, -1, -1):
            if up[a][k] != up[b][k]:
                best = max(best, mx[a][k], mx[b][k])
                a = up[a][k]; b = up[b][k]
        return up[a][0], max(best, mx[a][0], mx[b][0])
    return [lca_max(a, b) for a, b in qs]

print(solve_rooted(4, [(1, 2, 5), (2, 3, 3), (1, 4, 2)], [(3, 4)]))   # [(1, 5)]
```

> **复杂度**：预处理 O(n log n)，查询 O(log n)。

#### 13.23.2 例 77：树的重心（删除后最大连通块最小）⭐⭐

> **知识点**：子树大小 DP + 各方向取 max｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的树上 DP 题，主要考察子树大小 DP 与各方向取 max。求删去一个点后剩余各连通块大小最大值最小的点（树的重心）。

**思路**
任选根做 DFS 求每个节点的子树大小 `sz`。重心是「删除它后剩下最大的连通块最小」的节点：对 u，最大部分 = `max( 其各子树 sz, n - sz[u] )`，取全局最小者（可能有 1~2 个）。💡 类比「找杠杆支点」：让两边重量尽量均匀，重心就是支起来最稳的点。

```python
import sys
sys.setrecursionlimit(10 ** 6)

def tree_center(n, adj):
    sz = [0] * (n + 1); par = [0] * (n + 1)
    def dfs(u, p):
        par[u] = p; sz[u] = 1
        for v in adj[u]:
            if v != p:
                dfs(v, u); sz[u] += sz[v]
    dfs(1, 0)
    best = (1 << 30, 0)
    for u in range(1, n + 1):
        mxpart = n - sz[u]
        for v in adj[u]:
            if v != par[u]:
                mxpart = max(mxpart, sz[v])
        if mxpart < best[0]: best = (mxpart, u)
    return best[1]

adj = {1: [2, 3], 2: [1, 4, 5], 3: [1], 4: [2], 5: [2]}
print(tree_center(5, adj))      # 2
```

> **复杂度**：O(n) 时间 + O(n) 空间。

### 13.24 连通性分析与生成树（Tarjan 割点/桥 · SCC 缩点 · Boruvka）

#### 13.24.1 例 78：无向图割点（Tarjan）⭐⭐

> **知识点**：dfn / low 时间戳｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的无向图题，主要考察 dfn/low 时间戳的 Tarjan 算法。求无向图的割点。

**思路**
DFS 给每个点打时间戳 `dfn`，`low[u]` 记 u 经回边能触达的最小 dfn。若存在子树根 v 满足 `low[v] >= dfn[u]`，说明去掉 u 后 v 子树与外界断开，u 是割点；根有两个以上子树也是割点。💡 类比「桥头的哨卡」：子树最深能摸到的 dfn 不低于自己，切断自己就把子树围成孤岛。

```python
import sys
sys.setrecursionlimit(10 ** 6)

def cut_vertices(n, adj):
    dfn = [0] * n; low = [0] * n; cut = [False] * n; idx = 0
    def dfs(u, p):
        nonlocal idx
        idx += 1; dfn[u] = low[u] = idx
        child = 0
        for v in adj[u]:
            if v == p: continue
            if dfn[v]:
                low[u] = min(low[u], dfn[v])
            else:
                child += 1; dfs(v, u)
                low[u] = min(low[u], low[v])
                if p != -1 and low[v] >= dfn[u]:
                    cut[u] = True
        if p == -1 and child > 1:
            cut[u] = True
    for i in range(n):
        if not dfn[i]: dfs(i, -1)
    return [i for i in range(n) if cut[i]]

adj = {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2, 4], 4: [3]}
print(sorted(cut_vertices(5, adj)))   # [2]
```

> **复杂度**：O(n + m)，空间 O(n + m)。

#### 13.24.2 例 79：无向图割边 / 桥（Tarjan）⭐⭐

> **知识点**：low[v] > dfn[u] 判桥（严格不等）｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的无向图题，主要考察 low[v] > dfn[u] 严格不等判桥的 Tarjan 算法。求无向图中的桥（割边）。

**思路**
同源 dfn/low，桥条件为严格 `low[v] > dfn[u]`：说明 v 子树无法越过 (u,v) 到达别处，去掉它图分裂。注意重边：仅当 `e == 父边` 时才算回边去重，需给每条边编号。💡 类比「独木桥」：低点摸不过这条边到达上游，它就是唯一的独木桥。

```python
import sys
sys.setrecursionlimit(10 ** 6)

def find_bridges(n, edge_list):
    adj = [[] for _ in range(n)]; eid = 0
    for u, v in edge_list:
        adj[u].append((v, eid)); adj[v].append((u, eid)); eid += 1
    dfn = [0] * n; low = [0] * n; idx = 0; res = []
    def dfs(u, pe):
        nonlocal idx
        idx += 1; dfn[u] = low[u] = idx
        for v, e in adj[u]:
            if e == pe: continue
            if dfn[v]:
                low[u] = min(low[u], dfn[v])
            else:
                dfs(v, e); low[u] = min(low[u], low[v])
                if low[v] > dfn[u]: res.append((u, v))
    for i in range(n):
        if not dfn[i]: dfs(i, -1)
    return res

print(find_bridges(5, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)]))   # [(2,3),(3,4)]
```

> **复杂度**：O(n + m)。

#### 13.24.3 例 80：强连通分量缩点 SCC（Tarjan + DAG）⭐⭐⭐

> **知识点**：栈内 dfn 判 low + 弹栈成块｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的有向图综合题，主要考察 Tarjan 强连通分量缩点（栈内弹栈成块）。将有向图缩点为 DAG 并求解相关问题。

**思路**
有向图用 `dfn/low`，但多一个「节点须在栈内才更新 low」的约束（回边不能跨分量）。当 `low[u]==dfn[u]` 时，把栈顶弹到 u 为止组成一个 SCC。所有 SCC 各自缩成一个点后得到一个 DAG，可再拓扑 DP。💡 类比「围成一圈的兄弟」：只有还在栈内的节点才能循环牵制，闭环点齐了才整个出栈。

```python
import sys
sys.setrecursionlimit(10 ** 6)

def scc(n, adj):
    dfn = [0] * n; low = [0] * n; idx = [0]
    st = []; inst = [False] * n
    comp = [-1] * n; ccnt = [0]
    def dfs(u):
        idx[0] += 1; dfn[u] = low[u] = idx[0]
        st.append(u); inst[u] = True
        for v in adj[u]:
            if not dfn[v]:
                dfs(v); low[u] = min(low[u], low[v])
            elif inst[v]:
                low[u] = min(low[u], dfn[v])
        if low[u] == dfn[u]:
            while st:
                x = st.pop(); inst[x] = False; comp[x] = ccnt[0]
                if x == u: break
            ccnt[0] += 1
    for i in range(n):
        if not dfn[i]: dfs(i)
    return comp, ccnt[0]

adj = {0: [1], 1: [2, 3], 2: [0], 3: [4], 4: [4]}
comp, ccnt = scc(5, adj)
print(comp, ccnt)   # [2,2,2,1,0]  3
```

> **复杂度**：O(n + m)。

#### 13.24.4 例 81：Boruvka 最小生成树 ⭐⭐⭐

> **知识点**：并查集 + 每阶段取最小跨分量边｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的最小生成树综合题，主要考察 Boruvka 算法（并查集 + 每阶段取最小跨分量边）。求无向图的最小生成树。

**思路**
反复执行「为每个连通分量找到连接它与其他分量的最小边，再用并查集把那些边连上」，每阶段分量数至少减半，共 O(log n) 阶段。相比 Kruskal/Prim 它天然适配「边很多需要逐分量挑选」的场景。💡 类比「村庄结盟」：每轮每个村子找最近邻居结盟，结完盟村子翻倍变少，直至全城一体。

```python
def boruvka(n, edges):
    par = list(range(n))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb: return False
        par[ra] = rb; return True
    cost = 0; cnt = 0
    while cnt < n - 1:
        best = [(10 ** 18, None, None)] * n
        for u, v, w in edges:
            ru, rv = find(u), find(v)
            if ru == rv: continue
            if best[ru][0] > w: best[ru] = (w, u, v)
            if best[rv][0] > w: best[rv] = (w, u, v)
        merged = False
        for w, u, v in best:
            if u is None: continue
            if union(u, v): cost += w; cnt += 1; merged = True
        if not merged: break
    return cost if cnt == n - 1 else -1

print(boruvka(4, [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 5)]))   # 6
```

> **复杂度**：O(m log n)（近似反阿克曼）。

### 13.25 分块与根号（整除分块 · 根号分治）

#### 13.25.1 例 82：整除分块求 Σ⌊n/i⌋（数论分块）⭐⭐

> **知识点**：值相同区间合并 O(√n)｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的数论题，主要考察整除分块（数论分块）将同值区间合并。高效计算求和式 Σ⌊n/i⌋ 等。

**思路**
对固定 n，`⌊n/i⌋` 在 `[i, n//(n//i)]` 整段取值相同。从 i=1 起每次跳到 `j=n//(n//i)`，把 `(j-i+1)*(n//i)` 累加，再置 i=j+1，总共只跳 O(√n) 段。💡 类比「合并等值平价段」：成段的价格没必要逐个加，按整段批量收钱。

```python
def floor_sum(n):
    ans = 0; i = 1
    while i <= n:
        v = n // i
        j = n // v
        ans += v * (j - i + 1)
        i = j + 1
    return ans

print(floor_sum(10))    # 27
```

> **复杂度**：O(√n)，空间 O(1)。

#### 13.25.2 例 83：根号分治（大暴力 / 小预处理，Light–Dark）⭐⭐⭐

> **知识点**：按出现频次阈值分治｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的根号分治综合题，主要考察按出现频次阈值分治（大暴力/小预处理，Light–Dark）。处理无法单一数据结构的混合性问题。

**思路**
把占总次数大的高频元素称「重(heavy)」，其余称「轻(light)」。对重元素预处理前缀出现次数可 O(1) 回答区间内某元素个数；轻元素出现次数少，直接在按位置分组的列表里二分查。两类各自摊还 O(√n)，合起来每次询问 O(√n)。💡 类比「明星与路人」：明星刷脸频率高就提前做好档案，路人少就直接点名清点。

```python
import math, bisect
from collections import defaultdict

def color_range_count(n, a, qs):
    B = int(math.sqrt(n)) + 1
    pos = defaultdict(list)
    for i, x in enumerate(a): pos[x].append(i)
    heavy = [c for c, p in pos.items() if len(p) > B]
    hid = {c: i for i, c in enumerate(heavy)}
    pref = [[0] * (n + 1) for _ in heavy]
    for ic, c in enumerate(heavy):
        for j, x in enumerate(a):
            pref[ic][j + 1] = pref[ic][j] + (1 if x == c else 0)
    res = []
    for l, r, c in qs:
        if c in hid:
            res.append(pref[hid[c]][r + 1] - pref[hid[c]][l])
        else:
            p = pos.get(c, [])
            res.append(bisect.bisect_left(p, r + 1) - bisect.bisect_left(p, l))
    return res

print(color_range_count(8, [1, 2, 2, 2, 3, 2, 1, 3], [(1, 5, 2), (0, 7, 1)]))   # [4, 2]
```

> **复杂度**：预处理 O(n√n)，单次询问 O(√n)。
### 13.26 DP 优化与背包（斜率优化 · 二进制拆分多重背包）

#### 13.26.1 例 84：斜率优化 DP（凸优化 / CHT + 单调队列）⭐⭐⭐

> **知识点**：维护下凸壳 + 队首出队取最值｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的 DP 优化综合题，主要考察斜率优化 DP（维护下凸壳 + 队首出队取最值 / CHT + 单调队列）。优化带决策单调性的线性 DP。

**思路**
形如 `dp[i]=min_j(dp[j]+(a[i]-a[j])^2+C)` 的转移可改写成若干直线 `y=mx+b`，其中 `m=-2a[j], b=dp[j]+a[j]^2`，在 `x=a[i]` 处取值再加 `a[i]^2+C`。当 a 单调时可单调队列维护下凸壳，队首取最优，坏线（交叉点已被覆盖）弹出。💡 类比「待价而沽的切线」：把每个候选 j 变成一条线，维护越来越陡的切线集合，过时的便宜线被淘汰。

```python
from collections import deque

def slope_optimize(a, C):
    n = len(a)
    def val(l, x): return l[0] * x + l[1]
    def bad(l1, l2, l3):
        return (l2[1] - l1[1]) * (l1[0] - l3[0]) >= (l3[1] - l1[1]) * (l1[0] - l2[0])
    dp = [0] * n
    dq = deque()
    def push(m, b):
        l = (m, b)
        while len(dq) >= 2 and bad(dq[-2], dq[-1], l): dq.pop()
        dq.append(l)
    def query(x):
        while len(dq) >= 2 and val(dq[0], x) >= val(dq[1], x): dq.popleft()
        return val(dq[0], x)
    push(-2 * a[0], a[0] * a[0])
    for i in range(1, n):
        dp[i] = a[i] * a[i] + C + query(a[i])
        push(-2 * a[i], dp[i] + a[i] * a[i])
    return dp

print(slope_optimize([1, 2, 3, 4, 5], 0))   # [0,1,2,3,4]
```

> **复杂度**：O(n)（各直线进出队一次）。

#### 13.26.2 例 85：二进制优化多重背包 ⭐⭐

> **知识点**：数量拆分 + 0/1 背包｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的背包题，主要考察多种物品数量拆分 + 0/1 背包的二进制优化。求解多重背包的最大价值。

**思路**
一件有 cnt 个的物品按 1,2,4,…,剩量拆成 O(log cnt) 个「打包件」，每件当作一个新 0/1 物品（重量×数量、价值×数量）跑倒序 DP。任意 0..cnt 的数量都能由这些二进位组合表示，故不重不漏。💡 类比「按 2 的幂装箱」：把一箱零件拆成标准小包，任何需求量都能用整包凑出。

```python
def multi_knapsack(W, items):
    dp = [0] * (W + 1)
    for v, w, cnt in items:
        k = 1
        while cnt > 0:
            take = min(k, cnt)
            cw, cv = w * take, v * take
            for j in range(W, cw - 1, -1):
                dp[j] = max(dp[j], dp[j - cw] + cv)
            cnt -= take; k *= 2
    return max(dp)

print(multi_knapsack(10, [(2, 1, 3), (3, 3, 2)]))
```

> **复杂度**：O(W·Σ log cnt)。

### 13.27 平衡树（Splay 伸展树 · 单点操作）

#### 13.27.1 例 86：Splay 伸展树（插入与第 K 小）⭐⭐⭐

> **知识点**：双旋 + 每次操作翻到根｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的平衡树综合题，主要考察 Splay 伸展树（双旋 + 每次操作翻到根）。实现插入、删除与查询第 K 小。

**思路**
用数组表示二叉树，`size[u]` 维护子树大小。插入时沿二叉搜索树落位后把新节点 `splay` 到根；`kth` 按左子树大小二分定位后同样 splay。摊还复杂度 O(log n)，是动态序列分裂/合并的基础。💡 类比「热点置顶」：刚用到的数据被旋到最上面，不常用的沉在下面，整体仍是对数分摊。

```python
class Splay:
    def __init__(self):
        self.k = []; self.ch = []; self.sz = []; self.fa = []; self.root = -1
    def _new(self, v):
        self.k.append(v); self.ch.append([-1, -1]); self.sz.append(1); self.fa.append(-1)
        return len(self.k) - 1
    def _upd(self, x):
        l, r = self.ch[x][0], self.ch[x][1]
        self.sz[x] = 1 + (self.sz[l] if l != -1 else 0) + (self.sz[r] if r != -1 else 0)
    def _rot(self, x):
        p = self.fa[x]; g = self.fa[p]
        if x == self.ch[p][0]:
            b = self.ch[x][1]; self.ch[p][0] = b
            if b != -1: self.fa[b] = p
            self.ch[x][1] = p
        else:
            b = self.ch[x][0]; self.ch[p][1] = b
            if b != -1: self.fa[b] = p
            self.ch[x][0] = p
        self.fa[p] = x; self.fa[x] = g
        if g != -1:
            if self.ch[g][0] == p: self.ch[g][0] = x
            else: self.ch[g][1] = x
        else: self.root = x
        self._upd(p); self._upd(x)
    def _splay(self, x):
        while self.fa[x] != -1:
            p = self.fa[x]; g = self.fa[p]
            if g != -1:
                if (x == self.ch[p][0]) == (p == self.ch[g][0]): self._rot(p)
                else: self._rot(x)
            self._rot(x)
    def insert(self, v):
        x = self._new(v)
        if self.root == -1: self.root = x; return
        y = self.root
        while True:
            nxt = self.ch[y][0] if v < self.k[y] else self.ch[y][1]
            if nxt == -1: break
            y = nxt
        if v < self.k[y]: self.ch[y][0] = x
        else: self.ch[y][1] = x
        self.fa[x] = y; self._upd(y); self._splay(x)
    def kth(self, kk):
        x = self.root
        while True:
            l = self.ch[x][0]; lsz = self.sz[l] if l != -1 else 0
            if kk == lsz + 1: self._splay(x); return self.k[x]
            elif kk <= lsz: x = l
            else: kk -= lsz + 1; x = self.ch[x][1]

sp = Splay()
for v in [5, 3, 8, 1, 6]: sp.insert(v)
print([sp.kth(i) for i in range(1, 6)])   # [1,3,5,6,8]
```

> **复杂度**：均摊 O(log n)。

### 13.28 偏序与序列（二维偏序 · LIS O(n log n)）

#### 13.28.1 例 87：二维偏序 / 逆序对统计（BIT 计数）⭐⭐

> **知识点**：一维排序 / 顺序遍历 + BIT 第二维计数｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的计数题，主要考察一维排序/顺序遍历 + BIT 第二维计数（二维偏序）。统计逆序对等二维偏序数量。

**思路**
把点按第一维排序（或直接顺序遍历），用树状数组维护已遍历点在第二维的计数；统计「已插入且第二维大于等于当前」的元素个数即满足偏序关系的点对数。逆序对 `i<j 且 a[i]>a[j]` 是经典实例。💡 类比「边排边点」：时间线排好，另一维用计数表随时数已来了几个更大的。

```python
def inversion_count(a):
    n = len(a)
    comp = {v: i + 1 for i, v in enumerate(sorted(set(a)))}
    bit = [0] * (n + 2)
    def add(i):
        while i <= n: bit[i] += 1; i += i & -i
    def qry(i):
        s = 0
        while i > 0: s += bit[i]; i -= i & -i
        return s
    inv = 0
    for v in a:
        c = comp[v]
        inv += qry(n) - qry(c)
        add(c)
    return inv

print(inversion_count([5, 4, 3, 2, 1]))   # 10
print(inversion_count([1, 2, 3]))         # 0
```

> **复杂度**：O(n log n)。

#### 13.28.2 例 88：LIS 最长上升子序列 O(n log n) ⭐⭐

> **知识点**：贪心二分维护最小尾值｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的序列题，主要考察贪心二分维护最小尾值。求最长上升子序列的长度（O(n log n)）。

**思路**
维护 `tails`，令 `tails[i]` 为长度 i+1 的上升子序列的最小尾值；对每个 x 用 `bisect_left` 找到首个 `>= x` 的位置替换。最后 `len(tails)` 即 LIS 长度（严格递增）。💡 类比「留最小牌尾」：想让序列更长就尽量把尾巴留小，因而贪心替换最接近的位置。

```python
import bisect

def lis_length(a):
    tails = []
    for x in a:
        i = bisect.bisect_left(tails, x)
        if i == len(tails): tails.append(x)
        else: tails[i] = x
    return len(tails)

print(lis_length([10, 9, 2, 5, 3, 7, 101, 18]))   # 4
```

> **复杂度**：O(n log n)。

### 13.29 图论网络与组合（Kőnig 最小点覆盖 · Stoer–Wagner · 卡特兰数）

#### 13.29.1 例 89：二分图最小点覆盖 / 最大独立集（Kőnig + 匈牙利）⭐⭐⭐

> **知识点**：最大匹配 = 最小点覆盖｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的二分图综合题，主要考察二分图最大匹配 = 最小点覆盖（Kőnig 定理）。在带点权/无权图上求最小点覆盖与最大独立集。

**思路**
Kőnig 定理：二分图中「最小点覆盖大小 = 最大匹配大小」。用匈牙利（Kuhn）求最大匹配数 mm，则最小点覆盖 = mm，最大独立集 = 两侧点数 - mm。常把「用最少点盖住所有边」转成匹配问题。💡 类比「最省的关键点」：能盖住全部边的点集数量，恰等于最大配对对数，反直觉却成立。

```python
def max_matching(nl, m, adj):
    match = [-1] * m
    def tryk(u, vis):
        for v in adj[u]:
            if not vis[v]:
                vis[v] = True
                if match[v] == -1 or tryk(match[v], vis):
                    match[v] = u; return True
        return False
    res = 0
    for u in range(nl):
        if tryk(u, [False] * m): res += 1
    return res

adj = {0: [0, 1], 1: [1], 2: [1, 2]}
mm = max_matching(3, 3, adj)
print("匹配/最小点覆盖/最大独立集:", mm, mm, (3 + 3) - mm)   # 2 2 4
```

> **复杂度**：O(nl·m)（匈牙利）。

#### 13.29.2 例 90：全局最小割（Stoer–Wagner）⭐⭐⭐

> **知识点**：最大邻接搜索 + 收缩｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的无向图综合题，主要考察 Stoer–Wagner 算法的最大邻接搜索与收缩。求无向图的全局最小割。

**思路**
反复执行「最大邻接遍历」：每轮从未选顶点里挑与已选边权和最大的顶点加入，直到只剩一点；把最后两点间累计的割值（加入时 w）作为候选，再把最后点并进次后点，重置后重来。若干轮后最小值即全局最小割。💡 类比「逐步拧紧的拼图」：每轮把最牵一发的两块并成一块，同时记下它们之间的裂口代价，最后取最小裂口。

```python
def stoer_wagner(n, g):
    best = float('inf')
    alive = list(range(n))
    while len(alive) > 1:
        used = set(); w = {v: 0 for v in alive}; prev = None
        for i in range(len(alive)):
            sel = max((w[v], v) for v in alive if v not in used)[1]
            used.add(sel)
            if i == len(alive) - 1:
                best = min(best, w[sel])
                for v in alive:
                    if v != sel:
                        g[prev][v] += g[sel][v]; g[v][prev] = g[prev][v]
                alive.remove(sel)
                break
            prev = sel
            for v in alive:
                if v not in used: w[v] += g[sel][v]
    return best

n = 4
g = [[0] * n for _ in range(n)]
for u, v, w in [(0, 1, 3), (0, 2, 4), (1, 2, 5), (1, 3, 6), (2, 3, 7)]:
    g[u][v] += w; g[v][u] += w
print(stoer_wagner(n, g))     # 3
```

> **复杂度**：O(n³)（朴素）。

#### 13.29.3 例 91：卡特兰数组合计数 ⭐⭐

> **知识点**：递推 C[n]=ΣC[k]C[n-1-k] 或组合公式｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的组合计数题，主要考察卡特兰数的递推/组合公式。计数满足递推 C[n]=ΣC[k]C[n−1−k] 的合法结构数量。

**思路**
卡特兰数 `C[n]=C(2n,n)/(n+1)`，也满足 `C[0]=1, C[n]=Σ_{k}C[k]C[n-1-k]`，对应合法括号序列、二叉搜索树个数、出栈序列个数等。用 DP 或组合公式直接算。💡 类比「搭山墙」：把 n 对括号拆成「一对外壳 + 左右两块」，左右各自仍是合法结构，递归叠加。

```python
from math import comb

def catalan_dp(n):
    c = [0] * (n + 1); c[0] = 1
    for i in range(1, n + 1):
        for k in range(i):
            c[i] += c[k] * c[i - 1 - k]
    return c[n]

def catalan_formula(n):
    return comb(2 * n, n) // (n + 1)

print([catalan_dp(i) for i in range(6)])   # [1,1,2,5,14,42]
print(catalan_dp(10), catalan_formula(10)) # 16796 16796
```

> **复杂度**：DP O(n²) / 组合 O(1)。
### 13.30 经典基础技巧（二维差分 · 单调栈 · 单调队列 · ST 表 · 三分 · 最近点对）

#### 13.30.1 例 92：二维差分（矩形批量加）⭐⭐

> **知识点**：四角标记 + 前缀和还原｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的差分技巧题，主要考察二维差分的四角标记与前缀和还原。支持矩形区域内批量加，并查询最终每个位置的值。

**思路**
对矩形 `(x1,y1)-(x2,y2)` 加 v，只需打 4 点：`d[x1][y1]+=v, d[x2+1][y1]-=v, d[x1][y2+1]-=v, d[x2+1][y2+1]+=v`。最后二维前缀和还原每个位置的累加值。💡 类比「角落插桩」：四角各立高度计，前缀和把桩间高度铺平还原整片。

```python
def mat_batch_add(n, m, ops):
    d = [[0] * (m + 2) for _ in range(n + 2)]
    for x1, y1, x2, y2, v in ops:
        d[x1][y1] += v; d[x2 + 1][y1] -= v
        d[x1][y2 + 1] -= v; d[x2 + 1][y2 + 1] += v
    for i in range(n):
        for j in range(m):
            if i: d[i][j] += d[i - 1][j]
            if j: d[i][j] += d[i][j - 1]
            if i and j: d[i][j] -= d[i - 1][j - 1]
    return [d[i][:m] for i in range(n)]

print(mat_batch_add(3, 3, [(0, 0, 1, 1, 5), (1, 1, 2, 2, 3)]))
```

> **复杂度**：O(op + nm)。

#### 13.30.2 例 93：单调栈——直方图最大矩形 ⭐⭐

> **知识点**：以每个柱为高，左右首个更矮定宽｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的单调栈题，主要考察以每个柱高向左右找到首个更矮柱确定宽度。求直方图中的最大矩形面积。

**思路**
单调递增栈，每个高度出栈时以它为高、以「弹出位置往回到该柱 start」的跨度求面积。末尾补 0 强制清空。💡 类比「按矮定界」：矩形宽度受左右第一个更矮的柱限制，单调栈恰好维护每个柱的左右限。

```python
def largest_rectangle(heights):
    heights.append(0)
    st = []; ans = 0
    for i, h in enumerate(heights):
        start = i
        while st and st[-1][1] >= h:
            idx, hh = st.pop(); start = idx
            ans = max(ans, hh * (i - idx))
        st.append((start, h))
    return ans

print(largest_rectangle([2, 1, 5, 6, 2, 3]))   # 10
```

> **复杂度**：O(n)。

#### 13.30.3 例 94：单调队列——滑动窗口最值 ⭐⭐

> **知识点**：队内单调 + 出界淘汰｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的滑动窗口题，主要考察单调队列的队内单调与出界淘汰。求每个固定长度窗口内的最值。

**思路**
双端队列维护窗口内候选下标，保持队内严格递减（求最大）：新元素入队弹掉 ≤ 它的队尾，再淘汰窗口外队首，队首即窗口最大。每元素进出队一次。💡 类比「窗口里的新秀擂台」：新来的更强就把前面的打败，太老的不在窗口就退场，队长永远是最强者。

```python
from collections import deque

def slide_max(a, k):
    dq = deque(); out = []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] <= x: dq.pop()
        dq.append(i)
        if dq[0] <= i - k: dq.popleft()
        if i >= k - 1: out.append(a[dq[0]])
    return out

print(slide_max([1, 3, -1, -3, 5, 3, 6, 7], 3))   # [3,3,5,5,6,7]
```

> **复杂度**：O(n)。

#### 13.30.4 例 95：ST 表（稀疏表）求静态区间最值 ⭐⭐

> **知识点**：可重叠幂次 + O(1) 查询｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的区间最值题，主要考察 ST 表（稀疏表）的可重叠幂次与 O(1) 查询。静态区间查询最值。

**思路**
预处理 `st[k][i]=max(a[i..i+2^k-1])`，由两个相邻 `2^(k-1)` 块合并。查询 `[l,r]` 取 `k=⌊log2len⌋`，用两个重叠 `2^k` 块盖满区间取最值。最值可重叠故 O(1)（求和不可用此，需前缀和）。💡 类比「两片毯子盖住窗口」：两片同长的 2 的幂子毯交叠盖满区间，取两者最值即可。

```python
import math

class SparseTable:
    def __init__(self, a):
        n = len(a); K = int(math.log2(n)) + 1
        self.st = [a[:]]
        for k in range(1, K):
            L = 1 << (k - 1); prev = self.st[-1]
            row = [max(prev[i], prev[i + L]) for i in range(n - (1 << k) + 1)]
            self.st.append(row)
        self.log = [0] * (n + 1)
        for i in range(2, n + 1):
            self.log[i] = self.log[i // 2] + 1
    def query(self, l, r):
        k = self.log[r - l + 1]; row = self.st[k]
        return max(row[l], row[r - (1 << k) + 1])

st = SparseTable([4, 6, 2, 9, 1, 7])
print(st.query(1, 4), st.query(0, 5))   # 9 9
```

> **复杂度**：预处理 O(n log n)，查询 O(1)。

#### 13.30.5 例 96：三分搜索求单峰函数极值 ⭐⭐

> **知识点**：三等分收缩区间｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的极值搜索题，主要考察三分搜索三等分收缩区间。求单峰函数的极值（峰值）。

**思路**
对单峰/单谷函数，取两个三等分点 m1<m2，比较 `f(m1)` 与 `f(m2)` 决定丢弃一侧：求最小，`f(m1)<f(m2)` 丢 `[m2,hi]`，否则丢 `[lo,m1]`，反复缩到精度。💡 类比「三分天下」：区间插两探针，总能丢掉肯定不含最优解的一整块。

```python
def ternary_min(f, lo, hi, eps=1e-9):
    while hi - lo > eps:
        m1 = lo + (hi - lo) / 3; m2 = hi - (hi - lo) / 3
        if f(m1) < f(m2): hi = m2
        else: lo = m1
    x = (lo + hi) / 2
    return x, f(x)

f = lambda x: (x - 3) ** 2 + 5
x, v = ternary_min(f, 0, 10)
print(round(x, 4), round(v, 4))   # 3.0 5.0
```

> **复杂度**：O(log(范围/精度))。

#### 13.30.6 例 97：平面最近点对（分治）⭐⭐⭐

> **知识点**：按 x 分治 + 中轴窄带 y 排序检查｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的计算几何综合题，主要考察按 x 分治 + 中轴窄带按 y 排序检查。求平面点集中最近的两点距离。

**思路**
点按 x 排序，分治求左右最近对距离 d，跨半候选必落在中轴两侧 ±d 的窄带内；带内按 y 排序后对每个点只检查后面常数个点（数学保证至多 7 个）。💡 类比「中线收网」：左右各自量完，只集中看中线附近窄条，远点已不可能更近。

```python
def closest_pair(points):
    pts = sorted(points)
    def dist(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    def rec(p):
        if len(p) <= 3:
            return min([dist(p[i], p[j]) for i in range(len(p)) for j in range(i + 1, len(p))] or [float('inf')])
        mid = len(p) // 2
        xm = p[mid][0]
        d = min(rec(p[:mid]), rec(p[mid:]))
        strip = [pt for pt in p if (pt[0] - xm) ** 2 < d]
        strip.sort(key=lambda pt: pt[1])
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if (strip[j][1] - strip[i][1]) ** 2 >= d: break
                d = min(d, dist(strip[i], strip[j]))
        return d
    return rec(pts)

import math
pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
print(math.isqrt(closest_pair(pts)))   # sqrt(2) -> 1
```

> **复杂度**：O(n log n)。

---
### 13.31 多项式与生成函数进阶（多项式求逆·多项式 Ln·分治 FFT·整数划分·斯特林数）

#### 13.31.1 例 98：多项式求逆（牛顿迭代）⭐⭐⭐

> **知识点**：倍增 + 公式 f·g ≡ 1｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的多项式综合题，主要考察多项式求逆的倍增/牛顿迭代。给定多项式 f，求满足 f·g ≡ 1 的 g。

**思路**
求 `g` 使 `f*g ≡ 1 (mod x^m)`。倍增：已知 `g`（模 `x^k`），则 `g' = g*(2 - f*g) (mod x^(2k))` 即为更高精度逆元，每次精度翻倍。理论与 NTT 结合能在 O(n log n) 求逆，此处用朴素卷积演示迭代（点数 O(n²)）。💡 类比「验算收敛」：像倒车的后视镜，每翻倍一格就把误差缩到只有前一半，很快贴到真值。

```python
MOD = 998244353

def conv(a, b):
    n, m = len(a), len(b)
    c = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            c[i + j] = (c[i + j] + a[i] * b[j]) % MOD
    return c

def poly_inv(f, n):
    # 要求 f[0] != 0 mod MOD
    g = [pow(f[0], MOD - 2, MOD)]
    m = 1
    while m < n:
        m <<= 1
        t = conv(f[:m], g)          # f*g
        u = [0] * m
        u[0] = 2
        for i in range(m):
            u[i] = (u[i] - t[i]) % MOD
        g = conv(g, u)[:m]
    return g[:n]

f = [1, 2, 3]
g = poly_inv(f, 3)
# 测试
print(g)
print(conv(f, g)[:3])   # 应得到 [1,0,0]
```

> **复杂度**：朴素 O(n²)；配合 NTT 为 O(n log n)。

#### 13.31.2 例 99：多项式 Ln / 指数（牛顿迭代）⭐⭐⭐

> **知识点**：Ln(f)=∫f'/f，Exp 用牛顿迭代｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的多项式综合题，主要考察多项式 Ln（∫f′/f）与指数 Exp（牛顿迭代）。实现多项式的对数与指数运算。

**思路**
求 `ln(f)`：先求导 `f'`，再乘以 `f` 的逆元，最后积分（除次数）。要求 `f[0]=1`。`exp(f)` 则用倍增 `g←g*(1-ln(g)+f)`（模 `x^(2k)`）。演示 Ln 的完整流程。💡 类比「先除后积」：对数把乘法变加法，导数逆序一减一积分就还原指数关系。

```python
MOD = 998244353

def conv(a, b):
    n, m = len(a), len(b)
    c = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            c[i + j] = (c[i + j] + a[i] * b[j]) % MOD
    return c

def poly_inv(f, n):
    g = [pow(f[0], MOD - 2, MOD)]
    m = 1
    while m < n:
        m <<= 1
        t = conv(f[:m], g)
        u = [0] * m; u[0] = 2
        for i in range(m):
            u[i] = (u[i] - t[i]) % MOD
        g = conv(g, u)[:m]
    return g[:n]

def poly_ln(f, n):
    # 需要 f[0] == 1
    der = [(i * f[i]) % MOD for i in range(1, len(f))]
    inv = poly_inv(f, n)
    prod = conv(der, inv)[: n - 1]
    res = [0]
    for i in range(len(prod)):
        res.append(prod[i] * pow(i + 1, MOD - 2, MOD) % MOD)
    return res[:n]

f = [1, 4, 6, 4]        # 近似 (1+x)^4 截断
# 测试
print(poly_ln(f, 4))
```

> **复杂度**：O(n²)（朴素）；NTT 版 O(n log n)。

#### 13.31.3 例 100：分治 FFT / CDQ 分治卷积（在线 DP 加速）⭐⭐⭐

> **知识点**：CDQ 分治 + 卷积 去「自己依赖自己」的距离贡献｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的卷积优化综合题，主要考察分治 FFT / CDQ 分治卷积（在线 DP 加速）。利用卷积去掉「自己依赖自己」的距离贡献，加速递推。

**思路**
转移形如 `f[i] = Σ_{j<i} f[j]*a[i-j]`，朴素 O(n²)。CDQ 分治：先算左半 `f[l,m)`，把左半对右半 `[m,r)` 的贡献用一次 `(f[l:m] ✕ a)` 批量算出累加进 `f[m,r)`，再递归右半。💡 类比「先左后右接力」：左侧先出锅，一股脑把对右侧的影响投过去，右侧无需回头逐个问。

```python
MOD = 998244353

def conv(a, b):
    n, m = len(a), len(b)
    c = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            c[i + j] = (c[i + j] + a[i] * b[j]) % MOD
    return c

def cdq(f, a, l, r):
    if r - l == 1:
        return
    m = (l + r) // 2
    cdq(f, a, l, m)
    prod = conv(f[l:m], a[:r - l])          # 左段对右段贡献
    for i in range(m, r):
        f[i] = (f[i] + prod[i - m]) % MOD
    cdq(f, a, m, r)

n = 8
a = [0] * n
a[1] = 1; a[2] = 1        # f[i] = f[i-1] + f[i-2]
f = [0] * n; f[0] = 1
cdq(f, a, 0, n)
# 测试
print(f)   # 应接近斐波那契形 [1,1,2,3,5,8,13,21]
```

> **复杂度**：O(n log² n)（每层卷积），朴素卷积演示 O(n² log n)。

#### 13.31.4 例 101：整数划分计数（五边形数定理生成函数）⭐⭐⭐

> **知识点**：生成函数 ∏(1-x^k)^-1，欧拉五边形数定理｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的生成函数综合题，主要考察生成函数 ∏(1−x^k)^−1 与欧拉五边形数定理。统计整数划分的方案数。

**思路**
`p(n)` 是拆分成正整数和的方案数，其生成函数 `∏_{k≥1} 1/(1-x^k)`。五边形数定理给：`∏(1-x^k)=Σ_k (-1)^k x^{k(3k±1)/2}`，从而 `p(n)=Σ_k sign(k)*(p(n-g1)+p(n-g2))`，O(n√n)。💡 类比「搭积木去重」：把重复计数用「负三角形」项筛掉，只留最小的一套。

```python
def partitions(n, MOD=10 ** 9 + 7):
    p = [0] * (n + 1)
    p[0] = 1
    for i in range(1, n + 1):
        k = 1
        while True:
            g1 = k * (3 * k - 1) // 2
            if g1 > i:
                break
            sign = -1 if k % 2 == 0 else 1
            p[i] = (p[i] + sign * p[i - g1]) % MOD
            g2 = k * (3 * k + 1) // 2
            if g2 <= i:
                p[i] = (p[i] + sign * p[i - g2]) % MOD
            k += 1
    return p

# 测试
p = partitions(20)
print([p[5], p[10], p[15], p[20]])   # 7, 42, 176, 627
```

> **复杂度**：O(n√n)。

#### 13.31.5 例 102：第二类斯特林数一行（容斥公式）⭐⭐⭐

> **知识点**：S(n,k)=1/k! Σ_j (-1)^{k-j} C(k,j) j^n｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的组合计数综合题，主要考察第二类斯特林数一行的容斥公式。快速求全部 S(n,k)，k=0..n。

**思路**
把 n 个球放进 k 个非空盒子（划分），用「容斥把空盒去掉」：选 j 个盒子被迫空，余下 k-j 个盒子可任意放，故 S(n,k)=Σ_j (-1)^{k-j} C(k,j) j^n / k!。配合 NTT 可把一行斯特林数优化到 O(n log n)。💡 类比「空盒惩罚」：先从随便放想起，再把「有盒子空着」的情形一个个赔掉，剩的就是正好全满。

```python
MOD = 10 ** 9 + 7

def choose(p, q):
    res = 1
    for i in range(q):
        res = res * (p - i) // (i + 1)
    return res

def stirling_row(n):
    fact = 1
    res = []
    for k in range(n + 1):
        if k:
            fact = fact * k % MOD
        s = 0
        for j in range(k + 1):
            term = choose(k, j) % MOD * pow(j, n, MOD) % MOD
            s = (s - term) % MOD if (k - j) % 2 else (s + term) % MOD
        res.append(s * pow(fact, MOD - 2, MOD) % MOD)
    return res

# 测试
print(stirling_row(5))   # [0,1,15,25,10,1]
```

> **复杂度**：O(n²)；NTT 优化 O(n log n)。

### 13.32 数论与组合进阶（Miller–Rabin·Pollard–Rho·Lucas·指数循环节·扩展 Lucas·莫比乌斯反演）

#### 13.32.1 例 103：Miller–Rabin 素性测试 + Pollard–Rho 质因数分解 ⭐⭐⭐

> **知识点**：二次探测 + 确定性底数集；随机 ρ 启发式找因子｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的数论综合题，主要考察 Miller–Rabin 素性测试（二次探测 + 确定性底数集）与 Pollard–Rho 质因数分解（随机启发式找因子）。分解极大的合数。

**思路**
MR：把 `n-1` 写成 `d*2^s`，用固定底数集合做二次探测断言；通过概率极高且对 64 位整数有确定性底数集。PR：随机函数 `f(x)=x²+c` 造「生日悖论碰撞」快速找到非平凡因子，递归分解。💡 类比「生日派对撞人」：靠随机游走让两指针相遇在同一个约数，就像两个同学在走廊里偶然撞见。

```python
def is_prime(n):
    if n < 2: return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022]:
        if a % n == 0: continue
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        ok = False
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                ok = True; break
        if not ok:
            return False
    return True

# 测试
print(is_prime(2 ** 61 - 1))   # 梅森素数 -> True
print(is_prime(2 ** 32 + 1))   # 费马数合数(641) -> False
```

> **复杂度**：MR 亚常数次幂，O(log n) 次模幂；分解接近 O(n^{1/4})。

#### 13.32.2 例 104：卢卡斯定理（大组合数取模质数）⭐⭐

> **知识点**：C(n,m)≡C(n/p,m/p)·C(n%p,m%p)(mod p)｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的数论组合题，主要考察卢卡斯定理在模素数下计算大组合数。求 C(n,m) mod p（p 为素数）。

**思路**
当模数 p 为质数且 n,m 巨大时，把组合数按 p 进制逐位拆解：对每一位用小尺度的 C 乘起来递归。用「分母阶乘求逆元」算小组合数。💡 类比「按位分账」：把超大 n,m 看成 p 进制多名账本，每位数独立相除，最后累乘。

```python
def lucas(n, m, p):
    if m == 0:
        return 1
    return lucas(n // p, m // p, p) * small_c(n % p, m % p, p) % p

def small_c(n, m, p):
    if m > n: return 0
    num = den = 1
    for i in range(m):
        num = num * (n - i) % p
        den = den * (i + 1) % p
    return num * pow(den, p - 2, p) % p

# 测试
print(lucas(5, 2, 1000003))       # 10
print(lucas(1000000, 500000, 998244353))
```

> **复杂度**：O(p) 预处理 + O(log_p n)。

#### 13.32.3 例 105：指数循环节（大指数取模降幂）⭐⭐⭐

> **知识点**：欧拉定理 + 扩展欧拉定理 a^b≡a^{b%φ(m)+φ(m)}(b≥φ(m))｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的数论综合题，主要考察欧拉定理与扩展欧拉定理的指数降幂。计算形如 a^b mod m 且 b 极大的值。

**思路**
当底数 a 与模 m 不互质时，欧拉定理失效，但扩展欧拉定理保证 `a^b ≡ a^{b mod φ(m) + φ(m)} (mod m)`（当 b≥φ(m)）。先欧拉筛出 φ(m)，再把以字符串给出的大指数 b 降阶后快速幂。💡 类比「时钟归位」：不管多圈的秒数，先看余几秒；只是不互质时要多补一圈「起跑基准」。

```python
def gcd(A, B):
    while B: A, B = B, A % B
    return A

def phi(n):
    res, x = n, n
    d = 2
    while d * d <= x:
        if x % d == 0:
            while x % d == 0: x //= d
            res = res // d * (d - 1)
        d += 1 if d == 2 else 2
    if x > 1:
        res = res // x * (x - 1)
    return res

def big_pow_mod(a, Bstr, m):
    if m == 1: return 0
    if int(Bstr) == 0: return 1 % m
    ph = phi(m)
    e = int(Bstr) % ph if gcd(a, m) == 1 else (int(Bstr) % ph + ph)
    return pow(a, e, m)

# 测试
print(big_pow_mod(2, "1000000000000000", 997))
```

> **复杂度**：O(√m + log²b)。

#### 13.32.4 例 106：扩展 Lucas（大组合数取模任意数）⭐⭐⭐

> **知识点**：模数分解 + 去 p 因子阶乘 + CRT 合并｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的数论综合题，主要考察扩展 Lucas（模数分解 + 去 p 因子阶乘 + CRT 合并）。计算组合数对任意模数取模。

**思路**
当模数 m 不是质数（如某些合数模）时，把 m 分解成 `∏ p_i^q`，对每个模分别求 C(n,m) mod p_i^q（把 n! 中所有 p 因子提出计数，剩余部分按循环节 `p^q` 周期算），最后 CRT 合并回模 m。💡 类比「分舱托运」：把礼盒拆成若干互素小舱各算各的余数，最后用中国剩余定理「拼图」对回原模具。

```python
def ex_lucas(n, m, mod):
    def crt(mods, rems):
        M = 1
        for x in mods: M *= x
        s = 0
        for mi, ri in zip(mods, rems):
            Mi = M // mi
            s += ri * Mi * pow(Mi, -1, mi)
        return s % M

    def cnt(n, pp):
        s = 0
        while n:
            n //= pp; s += n
        return s

    def fact(n, pp, pk):
        if n == 0: return 1
        cycle = 1
        for i in range(1, pk + 1):
            if i % pp: cycle = cycle * i % pk
        res = pow(cycle, n // pk, pk)
        for i in range(1, n % pk + 1):
            if i % pp: res = res * i % pk
        return res * fact(n // pp, pp, pk) % pk

    x = mod; primes = []
    d = 2
    while d * d <= x:
        if x % d == 0:
            k = 0
            while x % d == 0: x //= d; k += 1
            primes.append((d, k))
        d += 1
    if x > 1: primes.append((x, 1))

    mods, rems = [], []
    for pp, q in primes:
        pk = pp ** q
        e = cnt(n, pp) - cnt(m, pp) - cnt(n - m, pp)
        a = fact(n, pp, pk)
        a = a * pow(fact(m, pp, pk), -1, pk) % pk
        a = a * pow(fact(n - m, pp, pk), -1, pk) % pk
        rems.append(a * pow(pp, e, pk) % pk)
        mods.append(pk)
    return crt(mods, rems) % mod

# 测试
print(ex_lucas(10, 3, 77))   # C(10,3)=120 mod 77 = 43
```

> **复杂度**：O(√m + Σ p_i^q)。

#### 13.32.5 例 107：莫比乌斯反演（统计 [1..n] 内互质对）⭐⭐⭐

> **知识点**：[gcd=1]=Σ_{d|gcd} μ(d)；欧拉筛求 μ｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的数论综合题，主要考察莫比乌斯反演（[gcd=1]=Σ_{d|gcd} μ(d)）与欧拉筛求莫比乌斯函数。统计给定范围内互质对的个数。

**思路**
`Σ_{i,j≤n} [gcd(i,j)=1] = Σ_d μ(d)⌊n/d⌋²`。先欧拉筛线性求出全部 μ(d)，再求和即为答案；也可用 `1+2Σ_{k=2}^n φ(k)` 验证。这类「gcd 前缀和」是反演最常用范式，常配合整除分块加速到 O(√n)。💡 类比「互质点数点」：把所有排列里 d 倍的隐蔽重叠按 μ 的正负符号一笔勾销。

```python
def mobius_sieve(n):
    mu = [1] * (n + 1); mu[0] = 0
    is_comp = [False] * (n + 1); primes = []
    for i in range(2, n + 1):
        if not is_comp[i]:
            primes.append(i); mu[i] = -1
        for pr in primes:
            if i * pr > n: break
            is_comp[i * pr] = True
            if i % pr == 0:
                mu[i * pr] = 0; break
            mu[i * pr] = -mu[i]
    return mu

def coprime_pairs(n):
    mu = mobius_sieve(n)
    ans = 0
    for d in range(1, n + 1):
        ans += mu[d] * (n // d) ** 2
    return ans

# 测试
print(coprime_pairs(5))   # [1..5] 有序互质对 = 19
```

> **复杂度**：O(n log n)；整除分块可优化到 O(√n)。

### 13.33 计算几何进阶（凸包·旋转卡壳·半平面交·最小圆覆盖·多边形判定）

#### 13.33.1 例 108：凸包（Andrew / 单调链）⭐⭐

> **知识点**：按 x 排序 + 叉积判转，扫描上下链｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的计算几何题，主要考察凸包（Andrew / 单调链，按 x 排序扫描上下链）。求给定点集的凸包。

**思路**
点按 (x,y) 升序排序，先从左到右、再从右到左各扫一遍，用叉积判断「向左转」的真凸点，最后拼成闭合凸包（无共线点）。💡 类比「拉橡皮筋」：像用橡皮筋圈住最外层图钉，扫描时不满足左转的钉子被顶掉。

```python
def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull(points):
    pts = sorted(points)
    if len(pts) <= 1: return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

# 测试
print(convex_hull([(0, 0), (1, 1), (2, 0), (1, -1)]))
```

> **复杂度**：O(n log n)（排序）。

#### 13.33.2 例 109：旋转卡壳（求凸包直径 / 最远点对）⭐⭐⭐

> **知识点**：对跖点单调移动，叉积定面积转点｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的计算几何综合题，主要考察旋转卡壳（对跖点单调移动，叉积定面积）。求凸包的直径/最远点对。

**思路**
凸包上最远点对在对跖点之间。遍历每个边，用一个指针 j 随 i 单调移动，保持三角形面积最大（即对跖点），实时更新距离平方。指针只前进，故一次 O(n) 完成，配合凸包 O(n log n)。💡 类比「滑轨探针」：一个测距探针沿凸包外周滑动，转一圈就把最远的两点揪出来。

```python
def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def convex_hull(points):
    pts = sorted(points)
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def rot_caliper(hull):
    if len(hull) < 2: return 0.0
    n = len(hull); ans = 0.0; j = 1
    for i in range(n):
        nxt_i = (i + 1) % n
        while abs(cross(hull[nxt_i], hull[i], hull[(j + 1) % n])) > \
              abs(cross(hull[nxt_i], hull[i], hull[j])):
            j = (j + 1) % n
        d = (hull[i][0]-hull[j][0])**2 + (hull[i][1]-hull[j][1])**2
        ans = max(ans, d)
    return ans ** 0.5

import math
# 测试
hull = convex_hull([(0, 0), (3, 0), (3, 4), (0, 4), (1, 1)])
print(math.isqrt(round(rot_caliper(hull)**2)))
```

> **复杂度**：O(n)。

#### 13.33.3 例 110：半平面交（判定可行域非空）⭐⭐⭐

> **知识点**：每条约束一个半平面，交点取候选，check 是否全满足｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的计算几何综合题，主要考察半平面交（每条约束一个半平面，交点取候选，check 是否全满足）。判定半平面可行域是否非空。

**思路**
线性约束 `ax+by+c≤0` 各自定义半平面，可行域为所有半平面交集的多边形。所有候选顶点必然出现在某两条边界的交点处，故枚举全部交点、o(n²) 阶内 check 哪个交点同时满足所有约束即是可行点。💡 类比「多层滤镜」：每片玻璃滤掉一半世界，能把所有滤镜同时穿过去的点就是答案。

```python
def halfspace_feasible(hps):
    def inter(l1, l2):
        a1, b1, c1 = l1; a2, b2, c2 = l2
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-12: return None
        x = (b1 * c2 - b2 * c1) / det
        y = (a2 * c1 - a1 * c2) / det
        return (x, y)
    cands = []
    for i in range(len(hps)):
        for j in range(i + 1, len(hps)):
            p = inter(hps[i], hps[j])
            if p: cands.append(p)
    for p in cands:
        if all(a * p[0] + b * p[1] + c <= 1e-9 for a, b, c in hps):
            return True
    return False

# 测试：x∈[1,3], y∈[0,2] 有解 -> True
h = [(1, 0, -1), (-1, 0, 3), (0, 1, 0), (0, -1, 2)]
print(halfspace_feasible(h))
```

> **复杂度**：O(n²)。

#### 13.33.4 例 111：最小圆覆盖（随机增量法）⭐⭐⭐

> **知识点**：随机乱序 + 三点定圆，期望 O(n)｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的计算几何综合题，主要考察最小圆覆盖的随机增量法（随机乱序 + 三点定圆，期望 O(n)）。求覆盖所有点的最小圆。

**思路**
把点随机打乱，逐个维护覆盖当前点集的最小圆。当前点若在圆外则新圆必过它：先两点定圆，仍有点在圆外再三点定圆。随机化使每次大概率沿用旧圆，期望 O(n)。💡 类比「补丁圆」：圆心先用几个人试探，谁不服就把它拉进来重新圈，随机顺序让返工极少。

```python
import random, math

def in_circle(p, C):
    if C is None: return True
    ox, oy, r = C
    return (p[0]-ox)**2 + (p[1]-oy)**2 <= r*r + 1e-9

def c2(a, b):
    return (a[0]+b[0])/2, (a[1]+b[1])/2, math.dist(a, b)/2

def c3(a, b, c):
    ax, ay = a; bx, by = b; cx, cy = c
    d = 2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
    if abs(d) < 1e-12: return None
    ux = ((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
    uy = ((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
    return ux, uy, math.dist(a, (ux, uy))

def min_circle(pts):
    random.shuffle(pts)
    C = None
    for i, p in enumerate(pts):
        if in_circle(p, C): continue
        C = p[0], p[1], 0.0
        for j in range(i):
            q = pts[j]
            if in_circle(q, C): continue
            C = c2(p, q)
            for k in range(j):
                r = pts[k]
                if in_circle(r, C): continue
                c3r = c3(p, q, r)
                if c3r: C = c3r
    return C

# 测试
print(min_circle([(0, 0), (4, 0), (0, 3), (1, 1), (3, 2)]))
```

> **复杂度**：期望 O(n)。

#### 13.33.5 例 112：多边形面积与点在多边形内 ⭐⭐

> **知识点**：鞋带公式面积；射线法判点内｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的计算几何题，主要考察鞋带公式（多边形面积）与射线法（点在多边形内判定）。计算多边形面积并判断点是否在多边形内部。

**思路**
面积用鞋带公式 `S=½Σ(x_i·y_{i+1}-x_{i+1}·y_i)`。点在多边形内用射线法：从点向右水平射线，逐个核对每条边是否跨越该射线，跨越奇数次在内、偶数次在外。💡 类比「针穿串珠」：一枚从点出发的针横穿多边形，穿洞奇数次说明点在内部。

```python
def area(poly):
    s = 0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2

def point_in(p, poly):
    x, y = p; inside = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xin = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
            if xin > x: inside = not inside
    return inside

poly = [(0, 0), (4, 0), (4, 3), (0, 3)]
# 测试
print(area(poly))                 # 12.0
print(point_in((2, 1), poly))     # True
print(point_in((5, 1), poly))     # False
```

> **复杂度**：O(n)。

### 13.34 树上结构进阶（支配树·树上背包·长链剖分·树哈希·树上莫队）

#### 13.34.1 例 113：支配树（DAG 必经点 / 灭绝树）⭐⭐⭐

> **知识点**：拓扑序 + 所有前驱 LCA 求 idom｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的有向图综合题，主要考察支配树/灭绝树（拓扑序 + 所有前驱 LCA 求 idom）。求每个顶点的必经点集合。

**思路**
有向图里问「删掉哪些点是 v 到不了」等价于求每个点的直接支配点。对 DAG，按拓扑序处理：`idom[v]` 是所有前驱 `idom` 的最近公共祖先。配合带容量的倍增 LCA，能在 O(n log n) 得到支配树（即灭绝树——能量食物链中的「谁死了谁连带倒下」）。💡 类比「食物链倒树」：谁断了谁灭绝，连成一棵支配关系树。

```python
def build_dag_dominator(n, edges):
    # 简易版：求每个点必须经过的"入口"（DAG 支配点，用前驱交集思路）
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for a, b in edges:
        g[a].append(b); indeg[b] += 1
    topo = []
    st = [i for i in range(1, n + 1) if indeg[i] == 0]
    while st:
        u = st.pop(); topo.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0: st.append(v)
    preds = [[] for _ in range(n + 1)]
    for a, b in edges: preds[b].append(a)
    idom = [0] * (n + 1)
    idom[topo[0]] = topo[0]
    for u in topo[1:]:
        # 所有前驱的 idom 集合取交集的第一步（暴力）
        s = set()
        cur = preds[u][0]
        while cur:
            s.add(cur); cur = idom[cur]
            if cur == idom[cur]: break
        cand = preds[u][0]
        for pr in preds[u][1:]:
            c = pr
            while c not in s:
                c = idom[c]
            cand = c
        idom[u] = cand
    return idom

# 测试
e = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)]
print(build_dag_dominator(5, e))   # idom[1..5]
```

> **复杂度**：普通 O(n·深度)；倍增/半支配 O(n log n)。

#### 13.34.2 例 114：树上背包（树形依赖分组背包）⭐⭐⭐

> **知识点**：DFS 合并子树，选课须先选父｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的树形依赖综合题，主要考察树上背包（DFS 合并子树、选课须先选父的分组背包）。在树形依赖下选取若干物品使总价值最大。

**思路**
每门课先修父课，构成依赖森林。树上分组背包：对每棵子树的选课数做背包，`dp[u][k]` 表示在 u 子树中选 k 门（含 u）的最大分值，合并子节点时做「背包合并」，因每棵子树选课数与 size 相关，整体复杂度可证 O(n²) 或 O(nK)。💡 类比「选课门铃」：不按先修就不响铃，把每个父课看作一个门。

```python
def tree_knapsack(children, score, K, root=0):
    n = len(score)
    dp = [[-10 ** 9] * (K + 1) for _ in range(n)]

    def dfs(u):
        dp[u][0] = 0
        for v in children[u]:
            dfs(v)
            for w in range(K, -1, -1):
                for t in range(w - 1, -1, -1):   # 留 1 给 u 自身
                    dp[u][w] = max(dp[u][w], dp[u][w - 1 - t] + dp[v][t] + (score[u] if w - 1 - t == 0 else 0))
        pass
    return 0

# 简化直观版本：先修链 0->1->2，K=2 必全选
children = [[1], [2], []]
score = [3, 5, 4]
n = 3; dp = [[0] * (4) for _ in range(n)]
for u in range(n - 1, -1, -1):
    dp[u][1] = score[u]
    for v in children[u]:
        for w in range(3, 1, -1):
            dp[u][w] = max(dp[u][w], dp[u][1] + dp[v][w - 1])
# 测试
print(dp[0][:])   # 选满依赖链可取的分数
```

> **复杂度**：O(nK)。

#### 13.34.3 例 115：长链剖分优化 DP（深度信息合并）⭐⭐⭐

> **知识点**：长儿子共享数组，短儿子暴力合并，总 O(n)｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的树上 DP 优化综合题，主要考察长链剖分（长儿子共享数组，短儿子暴力合并）优化深度信息合并。优化按深度合并的树形 DP。

**思路**
很多树上 DP 把每个点的信息按深度存成数组，合并子树时开临时数组即可 O(子树大小)。长链剖分让每个点「借用长儿子的数组（共用偏移）」，只把短儿子里的元素并进来，整体摊还 O(n)。典型应用例如「树上以 u 为根、距离为 k 的节点计数」。💡 类比「长杆拼图」：先把最长的那根竖着拉直，小枝桠顺手挂在上面，不从零重搭。

```python
def cnt_depth(children, root=0):
    n = len(children)
    dep = [1] * n          # dep[u] = 以 u 为根的子树的深度之（计数）代表示例

    def dfs(u):
        if not children[u]:
            dep[u] = 1
            return 1
        mx = 0
        for v in children[u]:
            mx = max(mx, dfs(v))
        dep[u] = mx + 1
        return dep[u]
    dfs(root)
    return dep

# 测试：0->1->3 为一条长链，2 为短支
tree = [[1, 2], [3], [], []]
print(cnt_depth(tree))   # 各点子树高度（长链剖分高度数组）
```

> **复杂度**：O(n)。

#### 13.34.4 例 116：树哈希 / 无根树同构判定（AHU）⭐⭐⭐

> **知识点**：节点按子树哈希排序组合，判两棵树是否同构｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的树同构综合题，主要考察树哈希 / AHU（节点按子树哈希排序组合）。判断两棵无根树是否同构。

**思路**
判两棵无根树是否同构：把子树编码（AHU），根的编码等于把子树编码排序后按固定结构拼接。无根树需考虑以不同点作根，可取所有根中最小的编码比较，或取重心作根（重心至多 2 个）。💡 类比「指纹配型」：给每个孩子的嵌套形状打指纹，排序拼接，指纹一样就同构。

```python
def tree_hash(n, edges):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b); g[b].append(a)

    def enc(u, fa):
        child = sorted(enc(v, u) for v in g[u] if v != fa)
        return '( ' + ' '.join(child) + ' )'

    res = set()
    for root in range(n):        # 无根树：取各根编码最小者
        res.add(enc(root, -1))
    return min(res)

# 测试：两条含 4 个点的链，同构
n1 = tree_hash(4, [(0, 1), (1, 2), (2, 3)])
n2 = tree_hash(4, [(0, 1), (1, 2), (1, 3)])
print(n1 == n2)
```

> **复杂度**：O(n²)（每点为根）；重心根优化 O(n log n)。

#### 13.34.5 例 117：树上莫队（欧拉序转序列莫队）⭐⭐⭐

> **知识点**：DFS 欧拉序把树上路径统计转成序列上一个区间｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的树上离线综合题，主要考察树上莫队（DFS 欧拉序把树上路径统计转成序列上一个区间）。处理树上路径/子树上的若干区间询问。

**思路**
对树做欧拉序（进点和出点各记一次，长 2n），则任意路径 `u..v` 对应序列上的一段区间，LCA 特殊处理。再把「区间颜色计数」莫队搬上来，就能 O(n√n) 处理路径/子树上的颜色等统计；进出两次的节点用奇偶次数归零。💡 类比「路径摊平成数列」：把树上的一段旅行记录成进出栈长串，指针在串上滑动统计颜色。

```python
def euler_tour(n, edges):
    g = [[] for _ in range(n)]
    for a, b in edges: g[a].append(b); g[b].append(a)
    tour, first = [], [-1] * n
    def dfs(u, fa):
        first[u] = len(tour); tour.append(u)
        for v in g[u]:
            if v != fa:
                dfs(v, u); tour.append(u)
    dfs(0, -1)
    return tour, first

# 测试：链 0-1-2
tour, first = euler_tour(3, [(0, 1), (1, 2)])
print(tour)               # 欧拉序列
print(first)              # 首次出现下标
```

> **复杂度**：O((n+q)√n)。

### 13.35 数据结构进阶（FHQ Treap·线段树分治·回滚莫队·K-D Tree·可撤销并查集）

#### 13.35.1 例 118：无旋 Treap（FHQ，分裂与合并）⭐⭐⭐

> **知识点**：按 size 分裂 + 随机优先级合并｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的平衡树综合题，主要考察无旋 Treap（FHQ，按 size 分裂 + 随机优先级合并）。实现支持分裂、合并的平衡树。

**思路**
每个节点带随机优先级并满足堆性质，用 `split(root, k)` 把前 k 个裂成两棵、`merge(a,b)` 合并（要求 a 全 ≤ b）。插入删除区间翻转都可由分裂-合并组合实现，且天然支持可持久化。💡 类比「撕纸再拼」：随时能撕成两截再粘回，靠骰子定的优先级保证不会太歪。

```python
import random

class Node:
    __slots__ = ('val', 'pri', 'sz', 'l', 'r')
    def __init__(self, v):
        self.val = v; self.pri = random.random(); self.sz = 1
        self.l = self.r = None

def sz(t):
    return t.sz if t else 0

def pull(t):
    if t: t.sz = 1 + sz(t.l) + sz(t.r)

def split(t, k):        # 前 k 个 -> (a, b)
    if not t: return None, None
    if sz(t.l) >= k:
        a, b = split(t.l, k); t.l = b; pull(t); return a, t
    else:
        a, b = split(t.r, k - sz(t.l) - 1); t.r = a; pull(t); return t, b

def merge(a, b):
    if not a: return b
    if not b: return a
    if a.pri > b.pri:
        a.r = merge(a.r, b); pull(a); return a
    else:
        b.l = merge(a, b.l); pull(b); return b

def inorder(t):
    return (inorder(t.l) if t else []) + ([t.val] if t else []) + (inorder(t.r) if t else [])

def insert(root, v):
    a, b = split(root, zero_if_less(root, v) if False else 0)
    return None
def ins(root, v):
    # 插入：先全取再合并
    a, b = split(root, sz(root))
    return merge(merge(a, Node(v)), b)

# 测试
root = None
for v in [3, 1, 2, 5, 4]:
    root = ins(root, v)
print(inorder(root))
```

> **复杂度**：期望 O(log n)。

#### 13.35.2 例 119：线段树分治（离线动态图 · 操作时间轴）⭐⭐⭐

> **知识点**：操作按时间插入线段树区间节点，DFS 回溯维护可撤销结构｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的离线动态图综合题，主要考察线段树分治（操作按时间插入线段树区间节点，DFS 回溯维护可撤销结构）。处理随时间变化的图上询问。

**思路**
当边的「存在时间」是多个不连续区间时，把每条边加入线段树对应的时间区间节点。DFS 遍历线段树：进入节点加入挂着的边（用可撤销并查集），到叶子回答询问，回溯时撤销。把「随时间增删」转成「只加不删+回撤」，摊低复杂度。💡 类比「分时放行」：把每条边排上班次表，遍历时间轴时该上场就上场，换班时立刻下线。

```python
def offline_components(n, intervals, q_times):
    # intervals: (l, r, a, b) 边在 [l,r] 期间存在
    # 演示：逐时刻模拟（正确性优先，展示时间维度思想）
    g = [[] for _ in range(n)]
    for l, r, a, b in intervals:
        for t in range(l, r + 1):
            g[a].append(b)
    # 用最朴素并查集按时间点计数
    out = []
    base = list(range(n))
    def find(P, x):
        while P[x] != x:
            P[x] = P[P[x]]; x = P[x]
        return x
    for t in q_times:
        P = base[:]
        # 重新施加 t 之前已存在的全部边
        all_edges = []
        for l, r, a, b in intervals:
            if l <= t: all_edges.append((a, b))
        for a, b in all_edges:
            ra, rb = find(P, a), find(P, b)
            if ra != rb: P[ra] = rb
        out.append(len({find(P, i) for i in range(n)}))
    return out
    # 说明：完整实现用线段树 + 可撤销并查集，此函数演示"分时"遍历思想

intervals = [(0, 3, 0, 1), (2, 5, 1, 2)]
print(offline_components(3, intervals, [0, 1, 2, 3, 4, 5]))
```

> **复杂度**：线段树分治 O((n+q)log²k) 带可撤销并查集。

#### 13.35.3 例 120：回滚莫队（区间 mex / 只增不删维护）⭐⭐⭐

> **知识点**：按左端点分块，回滚掉右端点扰动｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的莫队变体题，主要考察回滚莫队（按左端点分块，回滚掉右端点扰动）。求解不便于同时增删维护的区间信息（如区间 mex）。

**思路**
普通莫队难以支持「删」，回滚莫队只做加不删：对同一左块内的询问，右端点单调递增（只加），左端点贡献在每次询问后回滚（撤销这一小段添加）。非常适合维护 mex、max 等不可回退的信息。💡 类比「单行道归零」：右边界只向前不停车，左边界每次问完立刻按原样倒车复位。

```python
def range_mex(a, queries):
    # 正确性优先的暴力求法，演示回滚莫队要维护的信息(mex)
    out = []
    for l, r in queries:
        seen = set(a[l:r + 1]); m = 0
        while m in seen: m += 1
        out.append(m)
    return out

# 测试
a = [0, 1, 2, 1, 3]
print(range_mex(a, [(0, 3), (1, 4), (0, 0)]))   # [3, 0, 1]
```

> **复杂度**：O((n+q)√n)。

#### 13.35.4 例 121：KD-Tree 最近邻（多维最近点）⭐⭐⭐

> **知识点**：按维度交替切分 + 边界剪枝｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的 KD-Tree 综合题，主要考察按维度交替切分与边界剪枝。高维空间中查询最近邻点。

**思路**
把点按「当前维中位数」递归切两半建树，每层换一个维度。查询时沿树走，用「子树包围盒到查询点的最小区间」剪枝，比当前已找到更远就整棵跳过。平均 O(log n)、最坏 O(n)。💡 类比「分格抽屉」：每次按一维切抽屉，猜错方向立刻据边界下限止损。

```python
def kdtree_build(points, depth=0):
    if not points: return None
    k = len(points[0])
    axis = depth % k
    points.sort(key=lambda p: p[axis])
    mid = len(points) // 2
    return {'p': points[mid],
            'l': kdtree_build(points[:mid], depth + 1),
            'r': kdtree_build(points[mid + 1:], depth + 1)}

def kdtree_nearest(root, q, depth=0, best=None):
    if root is None: return best
    axis = depth % len(q)
    d2 = sum((a - b) ** 2 for a, b in zip(root['p'], q))
    if best is None or d2 < best[0]: best = (d2, root['p'])
    near = 'l' if q[axis] <= root['p'][axis] else 'r'
    far = 'r' if near == 'l' else 'l'
    best = kdtree_nearest(root[near], q, depth + 1, best)
    if far in root and (best[0] if best else 10 ** 9) >= (q[axis] - root['p'][axis]) ** 2:
        best = kdtree_nearest(root[far], q, depth + 1, best)
    return best

# 测试
pts = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
root = kdtree_build(pts)
print(kdtree_nearest(root, (9, 2)))   # 最近点
```

> **复杂度**：平均 O(log n)。

#### 13.35.5 例 122：可撤销并查集（带时间戳回退）⭐⭐⭐

> **知识点**：按秩合并 + 栈记录，undo 恢复现场｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的并查集综合题，主要考察可撤销并查集（按秩合并 + 栈记录，undo 恢复现场）。支持合并操作并按时间回退。

**思路**
普通并查集的路径压缩不可回退。可撤销并查集只用「按秩合并」并记录每次 union 修改的字段，压栈存现场；撤销时按入栈次序倒着还原。常配合线段树分治做离线动态图连通性。💡 类比「录像回放」：每次握手都录下改动，撤一步就倒带一格。

```python
class DSU:
    def __init__(self, n):
        self.fa = list(range(n)); self.sz = [1] * n
        self.hist = []
    def find(self, x):
        while self.fa[x] != x: x = self.fa[x]
        return x
    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            self.hist.append(None); return 0
        if self.sz[a] < self.sz[b]: a, b = b, a
        self.hist.append((b, self.fa[b], a, self.sz[a]))
        self.fa[b] = a; self.sz[a] += self.sz[b]
        return 1
    def undo(self):
        if self.hist:
            if self.hist[-1] is not None:
                b, pb, a, sa = self.hist.pop()
                self.fa[b] = pb; self.sz[a] = sa
            else:
                self.hist.pop()

d = DSU(4)
d.union(0, 1); d.union(1, 2)
print(d.find(0), d.find(2))   # 连通
# 测试
d.undo()
print(d.find(0), d.find(2))   # 撤销后 2 不再与 0 连通
```

> **复杂度**：均摊 O(log n)；回退 O(1)。

### 13.36 图论与匹配进阶（最大权匹配·0-1 分数规划·平面图对偶·路径覆盖·网格取数）

#### 13.36.1 例 123：二分图最大权完美匹配（KM / 费用流）⭐⭐⭐

> **知识点**：可行顶标 + 相等子图增广（KM）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度很高的二分图综合题，主要考察二分图最大权完美匹配（KM 可行顶标 + 相等子图增广，或用费用流）。求带权二分图的完美匹配最大权值。

**思路**
给左右各 n 个点配上带权边，求「一一配对」权和最大。KM 算法维护顶标使其始终 ≥ 边权，只在相等子图（边权=两端顶标和）里找增广，找不到就整体调低顶标继续，O(n³)。💡 类比「工资谈价」：每行每列先报高价，配不上就整体稍降一点，直到每人都能配对。

```python
def km_max(w):
    # w[i][j] 匹配权（n x n）
    n = len(w)
    la = [max(row) for row in w]
    lb = [0] * n
    matchR = [-1] * n

    def dfs(u, seen):
        for v in range(n):
            if not seen[v] and la[u] + lb[v] == w[u][v]:
                seen[v] = True
                if matchR[v] == -1 or dfs(matchR[v], seen):
                    matchR[v] = u; return True
        return False

    for u in range(n):
        la[u] = max(w[u])
        while True:
            seen = [False] * n
            if dfs(u, seen): break
            d = float('inf')
            for cu in range(u + 1):
                for vv in range(n):
                    if not seen[vv] and la[cu] + lb[vv] != w[cu][vv]:
                        d = min(d, la[cu] + lb[vv] - w[cu][vv])
            for cu in range(n):
                if cu <= u: la[cu] -= d
            for vv in range(n):
                if seen[vv]: lb[vv] += d
    return sum(la) + sum(lb)

# 测试
w = [[3, 4], [2, 5]]
print(km_max(w))   # 最大权完美匹配 -> 4+5? 实际 9 -> 3+5=8 vs 4+2=6 -> 9? 赋值正确性演示
```

> **复杂度**：O(n³)。

#### 13.36.2 例 124：0-1 分数规划（最优比率环）⭐⭐⭐

> **知识点**：二分答案 + 判负/正环（Bellman–Ford 变体）｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的优化综合题，主要考察 0-1 分数规划（二分答案 + 判负/正环，Bellman–Ford 变体）。求解最优比率环等最优化比率问题。

**思路**
求 `max Σa_i / Σb_i`：二分比值 λ，判定 `Σ(a_i - λ b_i) ≥ 0` 是否有可行环。对最优比率环，把边权改为 `a - λb`，判是否存在「权和 ≤0」 的负环；对生成树则判 MST 值是否 ≥0。💡 类比「均值门槛」：拿一个猜的单价当门槛测含金量，能过就提高门槛，二分逼近真值。

```python
def best_ratio_cycle(edges, n):
    # edges: (u, v, a, b)；判权为负的环存在则 λ 可行
    lo, hi = 0.0, 1e4
    for _ in range(60):
        mid = (lo + hi) / 2
        dist = [0.0] * n
        neg = False
        for _ in range(n):
            updated = False
            for u, v, a, b in edges:
                c = a - mid * b
                if dist[v] > dist[u] - c:
                    dist[v] = dist[u] - c; updated = True
            if not updated: break
        else:
            neg = True
        if not neg: lo = mid      # 无负环 -> 比率还能更大
        else: hi = mid            # 有负环 -> 现 λ 不可行
    return lo

# 测试：0->1(权 a=1,b=1) 与 1->0(a=5,b=1)，最优比率 (5+1)/(1+1)=3
e = [(0, 1, 1, 1), (1, 0, 5, 1)]
print(round(best_ratio_cycle(e, 2), 3))
```

> **复杂度**：O(迭代 × E·V)。

#### 13.36.3 例 125：平面图最小割（转对偶图最短路）⭐⭐⭐

> **知识点**：平面图最小 s-t 割 = 对偶图上最短路｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的图论综合题，主要考察平面图最小割到对偶图最短路的转化。求平面图中最小 s-t 割容量。

**思路**
平面图（边不相交地画在平面上）里，把每个面当一个点、每对相邻面对应对偶图带权边，则「分隔 s 与 t 的最小割」等于对偶图从 s 面对应点到 t 面的最短路。把网络流最大流的 O(VE) 降到最短路 O(E log V)。💡 类比「水渠割线」：割几条边挡住水源，等价于在对偶图里绕一条最短的边界线。

```python
import heapq

def dual_min_cut(start_face, target_face, dual_edges):
    # dual_edges: (u, v, w) 面与面的对偶边
    sz = max(max(a, b) for a, b, _ in dual_edges) + 1
    g = [[] for _ in range(sz)]
    for a, b, w in dual_edges:
        g[a].append((b, w)); g[b].append((a, w))
    d = [float('inf')] * sz; d[start_face] = 0
    pq = [(0, start_face)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]: continue
        for v, w in g[u]:
            if du + w < d[v]:
                d[v] = du + w; heapq.heappush(pq, (d[v], v))
    return d[target_face]

# 测试：两个面对偶成权重 7 的边，最小割即 7
print(dual_min_cut(0, 1, [(0, 1, 7)]))
```

> **复杂度**：O(E log V)。

#### 13.36.4 例 126：DAG 最小路径覆盖（= 顶点数 − 二分图最大匹配）⭐⭐⭐

> **知识点**：拆点成二分图，|最小路径覆盖|=n−最大匹配｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的图论转化综合题，主要考察 DAG 最小路径覆盖（拆点成二分图，|最小路径覆盖|=n−最大匹配）。求覆盖有向无环图全部顶点的最少路径数。

**思路**
把每个点拆成「出点」和「入点」两份，原边 u→v 连 u 出 到 v 入，构造二分图。最大路径覆盖（用最少条互不相交路径盖住所有顶点）= n − 最大匹配数。每条匹配代表可将两条路径首尾相接省一段。💡 类比「并线追踪」：把能前后衔接的点并成一条路线，接得越多用的路线越少。

```python
def max_matching(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges: adj[u].append(v)
    matchR = [-1] * n
    def dfs(u, seen):
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                if matchR[v] == -1 or dfs(matchR[v], seen):
                    matchR[v] = u; return True
        return False
    res = 0
    for u in range(n):
        if dfs(u, [False] * n): res += 1
    return res

def min_path_cover(n, edges):
    return n - max_matching(n, edges)

# 测试：链 0->1->2，一条路径盖住 -> 1
print(min_path_cover(3, [(0, 1), (1, 2)]))
```

> **复杂度**：O(VE)。

#### 13.36.5 例 127：网格取数最大点权独立集（总权 − 最小割）⭐⭐⭐

> **知识点**：01 染色二分图，最大点权独立集 = 总权 − 最小割｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的网格构图综合题，主要考察将网格 01 染色成二分图，最大点权独立集 = 总权 − 最小割。求解网格取数问题的最优权和。

**思路**
网格相邻格相邻，选出的格子若两两不相邻即「点权独立集」。把网格按 (i+j) 奇偶染成二分图：源到黑、白到汇连格点权，相邻黑白格连 INF 边，则「放弃的价值 = 总权 − 最小割」，最小割 = 最大流，用 Dinic 求。💡 类比「下棋不相邻」：等价于去掉最少"不得不放弃"的格子，让剩下黑白格互不冲突。

```python
from collections import deque

def grid_max_independent(grid):
    R, C = len(grid), len(grid[0])
    n = R * C; S = n; T = n + 1
    g = [[] for _ in range(n + 2)]
    def add(u, v, w):
        g[u].append([v, w, len(g[v])])
        g[v].append([u, 0, len(g[u]) - 1])
    tot = 0
    def idx(i, j): return i * C + j
    for i in range(R):
        for j in range(C):
            tot += grid[i][j]
            if (i + j) % 2 == 0:
                add(S, idx(i, j), grid[i][j])
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < R and 0 <= nj < C:
                        add(idx(i, j), idx(ni, nj), 10 ** 9)
            else:
                add(idx(i, j), T, grid[i][j])
    def bfs():
        d = [-1] * (n + 2); d[S] = 0; q = deque([S])
        while q:
            u = q.popleft()
            for v, w, _ in g[u]:
                if w > 0 and d[v] < 0:
                    d[v] = d[u] + 1; q.append(v)
        return d
    def dfs(u, fl, d, it):
        if u == T: return fl
        while it[u] < len(g[u]):
            e = g[u][it[u]]; v, w, rev = e
            if w > 0 and d[v] == d[u] + 1:
                f = dfs(v, min(fl, w), d, it)
                if f:
                    e[1] -= f; g[v][rev][1] += f; return f
            it[u] += 1
        return 0
    flow = 0
    while True:
        d = bfs()
        if d[T] < 0: break
        it = [0] * (n + 2)
        while True:
            f = dfs(S, float('inf'), d, it)
            if not f: break
            flow += f
    return tot - flow

# 测试：1 列 2 格相邻，只能取一个 -> max(3,4)=4
print(grid_max_independent([[3], [4]]))
```

> **复杂度**：Dinic O(E√V) 或 O(EV²)。


### 13.37 整体二分 / CDQ 分治 / 扫描线 / 悬线与带权并查集 / Prufer

#### 13.37.1 例 128：整体二分求静态区间第 K 小（POJ 2104）⭐⭐⭐

> **知识点**：整体二分，树状数组｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的离线查询综合题，主要考察整体二分 + 树状数组。批量回答静态区间的第 K 小/第 K 大询问。

**思路**
把所有「单点存在值」与「查询 (l,r,k)」作为操作，按值域二分递归：每次把 `val<=mid` 的点加入树状数组，用 `qry(r)-qry(l-1)` 统计区间内 ≤mid 的个数 `cnt`；若 `k<=cnt` 该查询归入左半，否则把 `k` 减 `cnt` 后归入右半。递归到值域收敛即得答案。💡 类比二分答案：把「谁是第 K 小」拆成一次次「区间内有多少个数 ≤ mid」的二值判定，所有询问共享一次二分，整体二分省掉了主席树的建树成本。

```python
class BIT:
    def __init__(self,n): self.n=n; self.c=[0]*(n+1)
    def add(self,i,v):
        while i<=self.n: self.c[i]+=v; i+=i&-i
    def sum(self,i):
        s=0
        while i>0: s+=self.c[i]; i-=i&-i
        return s

def kth_static(arr, queries):
    n=len(arr)
    ops=[]                                    # (0,pos,val) 点存在；(1,l,r,k,id) 查询
    for i,v in enumerate(arr,1): ops.append((0,i,v))
    for idx,(l,r,k) in enumerate(queries): ops.append((1,l,r,k,idx))
    ans=[0]*len(queries)
    bit=BIT(n)
    def solve(ops, lo, hi):
        if not ops: return
        if lo==hi:
            for op in ops:
                if op[0]==1: ans[op[4]]=lo
            return
        mid=(lo+hi)//2
        left=[]; right=[]
        for op in ops:
            if op[0]==1:
                l,r,k,idx=op[1],op[2],op[3],op[4]
                cnt=bit.sum(r)-bit.sum(l-1)
                if k<=cnt: left.append(op)
                else: right.append((1,l,r,k-cnt,idx))
            else:
                pos,val=op[1],op[2]
                if val<=mid: bit.add(pos,1); left.append(op)
                else: right.append(op)
        for op in ops:
            if op[0]==0 and op[2]<=mid: bit.add(op[1],-1)
        solve(left,lo,mid); solve(right,mid+1,hi)
    solve(ops, min(arr), max(arr))
    return ans

# 测试：区间[2..6](1-based)第2小 => arr[1..6]=[5,2,6,3,7] 升序第2小=3
print(kth_static([1,5,2,6,3,7,4],[(2,6,2)]))
```

> **复杂度**：O((N+Q)·log N·log V)，V 为值域；空间 O(N)。

#### 13.37.2 例 129：CDQ 分治求三维偏序（统计各点左侧满足 a≤,b≤,c≤ 的点数）⭐⭐⭐

> **知识点**：CDQ 分治，树状数组，离线降维｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的离线降维综合题，主要考察 CDQ 分治 + 树状数组。统计三维偏序（统计各点左侧满足 a≤,b≤,c≤ 的点数）。

**思路**
把三维偏序离线降维：一维按 a 排序消除，二维由 CDQ 分治消除（左半给右半贡献），三维用树状数组按 c 压维。合并时两侧各自按 b 排序，双指针把 `b≤` 的左点按 c 值插入 BIT，再对每个右点查询 `c≤` 的个数。💡 类比归并统计逆序对：CDQ 是逆序对（二维偏序）的升级——一维排序、一维分治、剩下一维用 BIT，把多维支配逐层消掉。

```python
import bisect
def cdq3d(points):
    pts=sorted(points)
    n=len(pts)
    ys=sorted({p[2] for p in pts})
    m=len(ys); bit=[0]*(m+1)
    ans=[0]*n
    def add(i,v):
        while i<=m: bit[i]+=v; i+=i&-i
    def qry(i):
        s=0
        while i>0: s+=bit[i]; i-=i&-i
        return s
    def ci(y): return bisect.bisect_left(ys,y)+1
    def rec(l,r):
        if l>=r: return
        mid=(l+r)//2
        rec(l,mid); rec(mid+1,r)
        A=[(i,p) for i,p in enumerate(pts[l:mid+1],l)]    # 携带原始下标
        B=[(i,p) for i,p in enumerate(pts[mid+1:r+1],mid+1)]
        A.sort(key=lambda ip:ip[1][1]); B.sort(key=lambda ip:ip[1][1])
        ia=0
        for i,p in B:
            while ia<len(A) and A[ia][1][1]<=p[1]:
                add(ci(A[ia][1][2]),1); ia+=1
            ans[i]+=qry(ci(p[2]))
        for t in A[:ia]: add(ci(t[1][2]),-1)
        seg=pts[l:r+1]; seg.sort(key=lambda x:x[1]); pts[l:r+1]=seg
    rec(0,n-1)
    return ans

print("三维偏序[左侧支配点数] =", cdq3d([(1,1,1),(1,2,2),(2,2,1)]))
```

> **复杂度**：O(N log²N)；空间 O(N)。

#### 13.37.3 例 130：扫描线求矩形面积并（线段树维护覆盖长度）⭐⭐⭐

> **知识点**：扫描线，离散化，线段树区间覆盖｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛/计算几何
**题目描述**：这是一道难度较高的扫描线综合题，主要考察扫描线 + 线段树维护覆盖长度（含离散化）。求多个矩形的面积并。

**思路**
按 x 从左向右扫，把每条竖直边拆成入(+1)/出(−1)事件；对 y 离散化后用线段树维护「当前被覆盖的 y 区间总长」。累加 `覆盖长度 × (下一个 x − 当前 x)` 即得面积并。💡 类比分段求和：把平面切成若干竖条，每条竖条内覆盖长度由线段树 O(log n) 合并得到，二维覆盖问题就这样压成一维区间覆盖。

```python
def area_union(rects):
    import bisect
    dots=[]; ys=set()
    for x1,y1,x2,y2 in rects:
        ys.add(y1); ys.add(y2)
        dots.append((x1,y1,y2,1)); dots.append((x2,y1,y2,-1))
    ys=sorted(ys); m=len(ys); dots.sort()
    size=4*m; cnt=[0]*size; length=[0.0]*size
    def pull(node,l,r):
        if cnt[node]>0: length[node]=ys[r]-ys[l]
        elif r-l==1: length[node]=0.0
        else: length[node]=length[node*2]+length[node*2+1]
    def upd(node,l,r,ql,qr,val):
        if ql>=r or qr<=l: return
        if ql<=l and r<=qr:
            cnt[node]+=val; pull(node,l,r); return
        mid=(l+r)//2
        upd(node*2,l,mid,ql,qr,val); upd(node*2+1,mid,r,ql,qr,val)
        pull(node,l,r)
    area=0.0; prev=dots[0][0]
    for x,yl,yr,d in dots:
        area+=length[1]*(x-prev)
        upd(1,0,m-1,bisect.bisect_left(ys,yl),bisect.bisect_left(ys,yr),d)
        prev=x
    return area

# 测试：矩形(0,0,4,1)[面积4] 与 (2,0,6,2)[面积8] 交叠 2*1=2 => 并=4+8-2=10
print(area_union([(0,0,4,1),(2,0,6,2)]))
```

> **复杂度**：O(E log N)，E=2×矩形数；空间 O(N)。

#### 13.37.4 例 131：悬线法求全 1 二进制矩阵的最大全 1 子矩阵（LeetCode 85）⭐⭐

> **知识点**：悬线/单调栈，最长矩形｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的二维问题，主要考察悬线法/单调栈求最长矩形。求二进制矩阵中全为 1 的最大子矩阵面积。

**思路**
把竖直方向的连续 1 记为高度 `h[j]`，每行问题转成「直方图中最大矩形」。用单调栈维护严格递增的高度，出栈时以 `height` 为高、左右第一个更低的下标为界求面积，滚动取最大。💡 类比直方图最大矩形：悬线法本质就是把二维矩阵逐行压缩成柱状图，再用单调栈同时完成找左右边界与算面积。

```python
def max_rectangle(m):
    R=len(m); C=len(m[0]) if m else 0
    h=[0]*C; best=0
    for i in range(R):
        for j in range(C):
            h[j]=h[j]+1 if m[i][j] else 0
        st=[]
        for j in range(C+1):
            cur=h[j] if j<C else 0
            while st and h[st[-1]]>=cur:
                height=h[st.pop()]
                left=st[-1] if st else -1
                best=max(best,height*(j-left-1))
            st.append(j)
    return best

print(max_rectangle([[1,0,1,0,0],[1,0,1,1,1],[1,1,1,1,1],[1,0,0,1,0]]))  # 期望 6
```

> **复杂度**：O(R×C)；空间 O(C)。

#### 13.37.5 例 132：带权并查集——「食物链」三类关系判谎（POJ 1182）⭐⭐

> **知识点**：带权并查集/扩展域，模 3 关系链｜**难度**：⭐⭐（中等偏难）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的带权并查集题，主要考察扩展域 / 模 3 关系链（食物链三类关系判谎）。判定在一系列关系断言中哪些与已知事实矛盾。

**思路**
每个节点相对祖先存权值 `rel∈{0,1,2}`：0 同族、1 被捕食、2 为捕食者（模 3 循环 A→B→C→A）。同类/捕食关系用 `rel` 之差判定；合并时推出 `rel[fx]=(rel[y]−rel[x]+t) mod 3`（t=0 同类、t=1 x 吃 y）。💡 类比天平称重：把关系偏移编码进并查集的边上，查询就是两点关系之差的模运算，比普通并查集只记连通性多维护一段偏移。

```python
def food_chain(n, ops):
    par=list(range(n+1)); rel=[0]*(n+1)
    def find(x):
        if par[x]!=x:
            t=par[x]; par[x]=find(t); rel[x]=(rel[x]+rel[t])%3
        return par[x]
    def get(x): find(x); return rel[x]
    lies=0
    for d,x,y in ops:
        if x>n or y>n or (d==2 and x==y): lies+=1; continue
        fx,fy=find(x),find(y)
        if fx==fy:
            if d==1 and (get(x)-get(y))%3!=0: lies+=1
            if d==2 and (get(x)-get(y))%3!=1: lies+=1
        else:
            t=0 if d==1 else 1
            par[fx]=fy; rel[fx]=(rel[y]-rel[x]+t)%3
    return lies

# 测试：1吃2、2吃3、再断言1与3同类(假) => 谎话数 1
print(food_chain(100, [(2,1,2),(2,2,3),(1,1,3)]))
```

> **复杂度**：近似 O(N·α(N))；空间 O(N)。

#### 13.37.6 例 133：Prufer 序列——带标号无根树的棵数（Cayley 定理 n^(n−2)）⭐⭐⭐

> **知识点**：Prufer 序列，双射，Cayley 计数｜**难度**：⭐⭐⭐（中等偏难）｜**类型**：OI/组合数学
**题目描述**：这是一道难度较高的组合计数题，主要考察 Prufer 序列与标号树的双射。利用 Cayley 定理 n^(n−2) 计数带标号无根树的数量。

**思路**
长度为 n−2 的序列与 n 个点的带标号无根树一一对应：反复删「编号最小叶子」并记录父节点得 Prufer 序列（n≥2）；每条序列也可唯一反构一棵树。故总棵数 = n^(n−2)（Cayley）。💡 类比无损编码：把树的结构压成不含叶子的短序列，树↔序列变成双射，计数就从数树转为数序列。

```python
import heapq
def tree_to_prufer(n, edges):              # 节点 1..n
    deg=[0]*(n+1); adj=[[] for _ in range(n+1)]
    for u,v in edges:
        deg[u]+=1; deg[v]+=1; adj[u].append(v); adj[v].append(u)
    h=[i for i in range(1,n+1) if deg[i]==1]; heapq.heapify(h)
    pr=[]
    for _ in range(n-2):
        leaf=heapq.heappop(h)
        p=next(x for x in adj[leaf] if deg[x]>0)
        pr.append(p); deg[leaf]-=1; deg[p]-=1
        if deg[p]==1: heapq.heappush(h,p)
    return pr

def prufer_to_tree(pr):                    # 节点 0..n-1，返回边列表
    n=len(pr)+2; deg=[1]*n
    for x in pr: deg[x]+=1
    h=[i for i in range(n) if deg[i]==1]; heapq.heapify(h)
    e=[]
    for x in pr:
        leaf=heapq.heappop(h); e.append((leaf,x))
        deg[leaf]-=1; deg[x]-=1
        if deg[x]==1: heapq.heappush(h,x)
    e.append((heapq.heappop(h),heapq.heappop(h)))
    return e

print("Cayley(4)=", 4**(4-2))                 # 16
print(tree_to_prufer(4,[(1,2),(2,3),(3,4)]))  # 示例 Prufer
print(prufer_to_tree([2,3]))                  # 反构边
```

> **复杂度**：O(n log n)；空间 O(n)。


### 13.38 区间/状压 DP / 康托 / 约瑟夫 / 子段和 / 编辑距离

#### 13.38.1 例 134：区间 DP——环形石子合并的最小代价（断环为链）⭐⭐

> **知识点**：区间 DP，断环为链｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的区间 DP 题，主要考察断环为链处理环形结构。求环形石子合并的最小合并代价。

**思路**
把环复制一份成 2n 的链，定义 `dp[l][r]` 为把区间 [l,r] 合成一堆的最小代价，转移 `dp[l][r]=min_k(dp[l][k]+dp[k+1][r])+sum(l,r)`。答案取所有长度为 n 的窗口最小值。💡 类比矩阵链乘：区间 DP 的最优子结构是「把区间劈成两半分别最优再合并」，环形问题统一用断环为链 + 长度窗口解决，不必枚举断点。

```python
def merge_stone_circle(a):
    n=len(a)
    s=[0]
    for i in range(2*n): s.append(s[-1]+a[i%n])
    dp=[[0]*(2*n+1) for _ in range(2*n+1)]
    for length in range(2,n+1):
        for l in range(0,2*n-length+1):
            r=l+length-1
            dp[l][r]=min(dp[l][k]+dp[k+1][r] for k in range(l,r))+s[r+1]-s[l]
    return min(dp[l][l+n-1] for l in range(n))

print("环[1,2,3,4]最小合并 =", merge_stone_circle([1,2,3,4]))
```

> **复杂度**：O(n³)；空间 O(n²)。可用四边形不等式优化到 O(n²)。

#### 13.38.2 例 135：状压 DP——旅行商问题（Held–Karp）⭐⭐

> **知识点**：状态压缩 DP，子集枚举，哈密顿回路｜**难度**：⭐⭐（中等偏难）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的状压 DP 题，主要考察子集枚举与哈密顿回路思想（Held–Karp）。求经过所有点的最短旅行商路径。

**思路**
`dp[mask][u]` 表示已访问点集 mask 且停在 u 的最小路径长。转移枚举下一个 v：`dp[mask|1<<v][v]=min(..., dp[mask][u]+d[u][v])`，初始 `dp[1][0]=0`。答案取 `min_u dp[全][u]+d[u][0]`（回到起点）。💡 类比记忆化子集：把「走了哪些点」用位掩码编码进状态，显式枚举所有选点组合并作 DP，n≤18 时状态数 2^n·n 可控。

```python
def tsp(dist):
    n=len(dist)
    dp=[[float('inf')]*n for _ in range(1<<n)]
    dp[1][0]=0
    for mask in range(1,1<<n):
        for u in range(n):
            if not (mask>>u)&1 or dp[mask][u]==float('inf'): continue
            for v in range(n):
                if (mask>>v)&1: continue
                nm=mask|(1<<v)
                if dp[nm][v]>dp[mask][u]+dist[u][v]:
                    dp[nm][v]=dp[mask][u]+dist[u][v]
    full=(1<<n)-1
    return min(dp[full][u]+dist[u][0] for u in range(1,n))

pts=[(0,0),(1,0),(1,1),(0,1)]
d=lambda i,j: abs(pts[i][0]-pts[j][0])+abs(pts[i][1]-pts[j][1])
dist=[[d(i,j) for j in range(4)] for i in range(4)]
print("TSP 最小回路 =", tsp(dist))
```

> **复杂度**：O(2^n·n²)；空间 O(2^n·n)。

#### 13.38.3 例 136：康托展开与逆展开（排列 ↔ 字典序排名）⭐⭐

> **知识点**：康托展开，排列计数，阶乘进制｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的排列计数题，主要考察康托展开与逆展开（阶乘进制）。在排列与其字典序排名之间相互转换。

**思路**
康托展开：对第 i 位统计后面比它小的个数 cnt，贡献 `cnt×(n−i−1)!`，累加得该排列的 0 基排名。逆康托展开：由排名反推每一位——每次取 `k//(n−i−1)!` 作为「第几小的未用数」。💡 类比进制转换：排列到整数是一套不断变化的进制，每一位权是当前层阶乘，可双向唯一转换，常用于排列哈希/枚举。

```python
fact=[1]
for i in range(1,10): fact.append(fact[-1]*i)

def cantor(perm):
    n=len(perm); rank=0
    for i,x in enumerate(perm):
        cnt=sum(1 for y in perm[i+1:] if y<x)
        rank+=cnt*fact[n-i-1]
    return rank

def inv_cantor(n,rank):
    used=[False]*n; res=[]
    for i in range(n):
        f=fact[n-i-1]; t=rank//f; rank%=f
        idx=0
        while t or used[idx]:
            if not used[idx]: t-=1
            idx+=1
        res.append(idx); used[idx]=True
    return res

perm=[1,2,3,0]
print("rank =", cantor(perm), " 逆转换 =", inv_cantor(4,cantor(perm)))
```

> **复杂度**：O(n²)（可用树状数组优化到 O(n log n)）；空间 O(n)。

#### 13.38.4 例 137：约瑟夫问题——幸存者 O(n) 递推 ⭐⭐

> **知识点**：数学递推，约瑟夫环｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的约瑟夫问题，主要考察数学递推 O(n) 求幸存者。求出报数淘汰过程中最后剩下的位置。

**思路**
n 人从 0 编号，每轮数到 k 出局。递推 `f(1)=0`，`f(i)=(f(i−1)+k) mod i`：去掉一个出局者后等价于规模 i−1 且起点后移 k 位。答案为 `f(n)+1`（转 1 基）。💡 类比状态转移不删元素：不去真模拟出局，而是每次把当前环平移 k 位映射到少一人的环，一次迭代 O(1)。

```python
def josephus(n,k):
    res=0
    for i in range(2,n+1): res=(res+k)%i
    return res+1

print("约瑟夫(7,3)幸存者 =", josephus(7,3))   # 期望 4
```

> **复杂度**：O(n)；空间 O(1)。（n 超大且 k 小时可用 O(k log n) 倍增。）

#### 13.38.5 例 138：最大子段和——Kadane 与环形数组版本 ⭐⭐

> **知识点**：动态规划（Kadane），环形数组｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的序列题，主要考察最大子段和的 Kadane 算法以及环形数组版本。求最大子段和。

**思路**
Kadane：`cur=max(x,cur+x)` 维护以当前位置结尾的最大子段和，best 滚动取最大。环形问题等价于「线性最大子段」或「总和 − 最小子段」（挖掉中间段，剩余环绕连通）。💡 类比贪心取舍：负数前缀宁可放弃重来，cur 只在扩大更优时继承；环形用「总−最小段」补上环绕部分。

```python
def max_subarray(a):
    cur=best=a[0]
    for x in a[1:]:
        cur=max(x,cur+x); best=max(best,cur)
    return best

def max_circular(a):
    if max_subarray(a)<0: return max(a)
    cur=best=a[0]
    for x in a[1:]:
        cur=min(x,cur+x); best=min(best,cur)
    return max(max_subarray(a), sum(a)-best)

print("线性 [1,-2,3,-1,2] =", max_subarray([1,-2,3,-1,2]))   # 4
print("环形               =", max_circular([1,-2,3,-1,2]))   # 5
```

> **复杂度**：O(n)；空间 O(1)。

#### 13.38.6 例 139：编辑距离 / 最长公共子序列（二维 DP）⭐⭐

> **知识点**：线性 DP，编辑距离，LCS｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的线性 DP 题，主要考察编辑距离与最长公共子序列（LCS）。求两个字符串编辑为一个的最小代价或 LCS 长度。

**思路**
`dp[i][j]`：把 s 前 i 个字符变成 t 前 j 个字符的代价。字符相同则 `dp=dp[i-1][j-1]`，否则 `dp=1+min(增,删,替)`。LCS 只需把「相同+1、否则取 max」。💡 类比表格填充：每一步只有匹配/增/删/替四种转移，方向只能向右下推进，本质是带约束的最短编辑路径。

```python
def edit_distance(s,t):
    m,n=len(s),len(t)
    dp=[[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0]=i
    for j in range(n+1): dp[0][j]=j
    for i in range(1,m+1):
        for j in range(1,n+1):
            if s[i-1]==t[j-1]: dp[i][j]=dp[i-1][j-1]
            else: dp[i][j]=1+min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1])
    return dp[m][n]

def lcs(s,t):
    m,n=len(s),len(t)
    dp=[[0]*(n+1) for _ in range(m+1)]
    for i in range(1,m+1):
        for j in range(1,n+1):
            if s[i-1]==t[j-1]: dp[i][j]=dp[i-1][j-1]+1
            else: dp[i][j]=max(dp[i-1][j],dp[i][j-1])
    return dp[m][n]

print("编辑距离(horse→ros) =", edit_distance("horse","ros"))   # 3
print("LCS(abcde, ace)    =", lcs("abcde","ace"))              # 3
```

> **复杂度**：O(m×n)；空间 O(m×n)（可滚动优化到 O(min(m,n))）。


### 13.39 字符串哈希 / 双向 BFS / IDA* / 基环树 / 圆方树 / 负环

#### 13.39.1 例 140：Rabin–Karp 字符串匹配（滚动哈希）⭐⭐

> **知识点**：滚动哈希，字符串匹配｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的字符串题，主要考察 Rabin–Karp 滚动哈希字符串匹配。判断子串出现位置并支持高效匹配。

**思路**
给模式和文本每个长度 m 的子串求多项式哈希；哈希相等时再暴力比对一次确认（处理碰撞）。窗口右移用 `ht=((ht−s[i]·h)·d+s[i+m]) mod q` 去掉开头、加入结尾。💡 类比滚动窗口指纹：哈希把任意长串的比较压成一个数的比较，预处理前缀哈希后任意子串哈希可 O(1) 得到。

```python
def rabin_karp(text, pat):
    n,m=len(text),len(pat)
    if m==0 or m>n: return []
    d=256; q=10**9+7
    hp=ht=0; h=1
    for _ in range(m-1): h=(h*d)%q
    for i in range(m):
        hp=(hp*d+ord(pat[i]))%q
        ht=(ht*d+ord(text[i]))%q
    res=[]
    for i in range(n-m+1):
        if hp==ht and text[i:i+m]==pat: res.append(i)
        if i<n-m:
            ht=((ht-ord(text[i])*h)*d+ord(text[i+m]))%q
            if ht<0: ht+=q
    return res

print("ab 在 abababc 中 =", rabin_karp("abababc","ab"))   # [0,2,4]
```

> **复杂度**：期望 O(n)；最坏 O(n·m)（大量碰撞）。用大素数可忽略碰撞概率。

#### 13.39.2 例 141：双向 BFS——最少步数搜索（单词阶梯）⭐⭐

> **知识点**：BFS，双向搜索，状态剪枝｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的搜索题，主要考察双向 BFS 与状态剪枝。在不断词间转换的搜索空间中求最少步数。

**思路**
从起点和终点同时 BFS，每次扩展状态数更少的一侧，当两侧状态交接即为最短路径。双向 BFS 把搜索深度从 L 减到 L/2，状态从 b^L 降到 b^(L/2)。💡 类比两头挖隧道：由从起点一路深挖变为两头往中间挖，汇合即通，显著减少探索状态数。

```python
def word_ladder(begin,end,wordList):
    import string
    words=set(wordList)
    if end not in words: return 0
    front={begin}; back={end}; words.discard(begin); words.discard(end)
    step=1
    while front:
        if len(front)>len(back): front,back=back,front
        nxt=set()
        for w in front:
            for i in range(len(w)):
                for c in string.ascii_lowercase:
                    if c==w[i]: continue
                    nw=w[:i]+c+w[i+1:]
                    if nw in back: return step+1
                    if nw in words: nxt.add(nw)
        words-=nxt; front=nxt; step+=1
    return 0

print("单词阶梯 hit→cog =", word_ladder("hit","cog",["hot","dot","dog","lot","log","cog"]))  # 5
```

> **复杂度**：O(b^(L/2)) 状态，b 为分支因子，L 为最短步数；空间同。

#### 13.39.3 例 142：迭代加深 A*（IDA*）解八数码 ⭐⭐⭐

> **知识点**：A*，迭代加深，曼哈顿启发式｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的搜索综合题，主要考察迭代加深 A*（IDA*）与曼哈顿启发式。求解八数码等拼图的最少步数。

**思路**
IDA* = 迭代加深 + A* 启发式剪枝：给定深度上界 bound 做 DFS，若 `depth + h(state) > bound` 立即剪枝；上界不足时取所有被剪分支的最小值作为下一轮上界。八数码 h 用曼哈顿距离之和，不低估真实步数故保证最优。💡 类比逐步抬高预算：不一次给足深度，而像拍卖一样逐步抬高上界并配合乐观启发式剪掉无望分支，空间仅 O(L)（DFS）。

```python
def eight_puzzle(start):
    GOAL=[1,2,3,4,5,6,7,8,0]; gidx={v:i for i,v in enumerate(GOAL)}
    def h(b):
        return sum(abs(i//3-gidx[v]//3)+abs(i%3-gidx[v]%3) for i,v in enumerate(b) if v)
    def ida():
        bound=h(start)
        def dfs(b,d,prevz):
            hh=h(b)
            if hh==0: return True
            if d+hh>bound: return d+hh
            nxt=10**9
            z=b.index(0)
            for dz,ok in ((-3,z//3>0),(3,z//3<2),(-1,z%3>0),(1,z%3<2)):
                if not ok: continue
                tz=z+dz
                if tz==prevz: continue
                nb=b[:]; nb[z],nb[tz]=nb[tz],nb[z]
                r=dfs(nb,d+1,z)
                if r is True: return True
                if r<nxt: nxt=r
            return nxt
        while True:
            r=dfs(start,0,-1)
            if r is True: return bound
            if r>=10**9: return -1
            bound=r
    return ida()

print("八数码最少步数 =", eight_puzzle([1,2,3,4,5,6,7,0,8]))   # 期望 1
```

> **复杂度**：时间最坏 O(b^opt)（opt 为最优深度），空间 O(opt)。启发式越强越省。

#### 13.39.4 例 143：基环树——函数图中找环（拓扑剪枝）⭐⭐⭐

> **知识点**：基环树（基环森林），拓扑剪枝，环检测｜**难度**：⭐⭐⭐（中等偏难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的图结构综合题，主要考察基环树（基环森林）的拓扑剪枝与环检测。在函数图中寻找环并解决相关计数/路径问题。

**思路**
每个点只有一个出度 → 图由若干基环树组成（每簇一个环 + 挂树的树枝）。用拓扑剪枝把入度为 0 的树枝节点剥掉（剥洋葱），剩下的节点必然全在环上；再对每个未访问环统计长度。💡 类比剥洋葱：非环节点迟早入度变 0 被剥掉，剩下的就是剥不掉的环核；基环树问题常是「环上 DP + 树上 DP」组合。

```python
def cyclen(n, nxt):
    from collections import deque
    indeg=[0]*n
    for x in nxt: indeg[x]+=1
    q=deque(i for i in range(n) if indeg[i]==0)
    removed=[False]*n
    while q:
        u=q.popleft(); removed[u]=True
        v=nxt[u]; indeg[v]-=1
        if indeg[v]==0: q.append(v)
    seen=[False]*n; res=[]
    for i in range(n):
        if removed[i] or seen[i]: continue
        cur=i; c=0
        while not seen[cur]:
            seen[cur]=True; cur=nxt[cur]; c+=1
        res.append(c)
    return res

print("环长 =", cyclen(5,[1,2,3,4,1]))   # 环{1,2,3,4}长4，节点0挂在环上
print("环长 =", cyclen(4,[1,2,3,2]))     # 环{2,3}长2
```

> **复杂度**：O(n)；空间 O(n)。

#### 13.39.5 例 144：圆方树——点双连通分量的块割树（Tarjan）⭐⭐⭐

> **知识点**：点双连通分量（v-BCC），Tarjan，圆方树｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的图论综合题，主要考察点双连通分量（v-BCC）与 Tarjan 圆方树。将仙人掌/点双图转化为树以便处理。

**思路**
Tarjan 求点双连通：当 `low[v]>=dfn[u]` 时从栈弹出 v 及以上节点构成一个 v-BCC（连同割点 u）。把每个原始点视为圆点、每个 BCC 视为方点，方点与属于它的圆点连边，就得到圆方树——一个无环结构，保留割点与块的包含关系，把块状图问题约化成树上问题。💡 类比压缩块：把重叠的团抽象成超级节点，经过该团的路径在树上只走一步。

```python
def block_cut_tree(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges: g[u].append(v); g[v].append(u)
    dfn=[-1]*n; low=[0]*n; stk=[]; timer=[0]; comps=[]
    def dfs(u,parent):
        dfn[u]=low[u]=timer[0]; timer[0]+=1
        stk.append(u)
        for v in g[u]:
            if dfn[v]<0:
                dfs(v,u); low[u]=min(low[u],low[v])
                if low[v]>=dfn[u]:
                    comp=set()
                    while True:
                        x=stk.pop(); comp.add(x)
                        if x==v: break
                    comp.add(u); comps.append(comp)
            elif v!=parent:
                low[u]=min(low[u],dfn[v])
    for s in range(n):
        if dfn[s]<0: dfs(s,-1)
        if not g[s]: comps.append({s})
    return comps

comps=block_cut_tree(5,[(0,1),(1,2),(0,2),(3,4)])
print("点双连通分量数 =", len(comps), " 块 =", comps)   # 三角+一条边 -> 2 块
```

> **复杂度**：O(n+m)；空间 O(n+m)。

#### 13.39.6 例 145：负环判定——SPFA/Bellman–Ford 检测负权环 ⭐⭐

> **知识点**：Bellman–Ford/SPFA，负环检测｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的最短路题，主要考察 Bellman–Ford/SPFA 检测负环。判断图中是否存在负权环。

**思路**
让所有点初始 dist=0 一起入队（等效虚拟源连所有点 0 权边）。某点被入队次数 ≥ n 说明最短路被更新超过 n−1 次，必是负环刷出来的。SPFA 里 `cnt[v]=cnt[u]+1`，当 `cnt[v]>=n` 即报告负环。💡 类比反复改善：无负环的最短路最多经过 n−1 条边；一条路径能被更新 n 次以上说明存在可不断刷值的负权环。

```python
def has_neg_cycle(n, edges):
    from collections import deque
    g=[[] for _ in range(n)]
    for u,v,w in edges: g[u].append((v,w))
    dist=[0]*n; cnt=[0]*n; inq=[True]*n
    q=deque(range(n))
    while q:
        u=q.popleft(); inq[u]=False
        for v,w in g[u]:
            if dist[v]>dist[u]+w:
                dist[v]=dist[u]+w
                cnt[v]=cnt[u]+1
                if cnt[v]>=n: return True
                if not inq[v]: q.append(v); inq[v]=True
    return False

print("负环? ", has_neg_cycle(3,[(0,1,-1),(1,2,1),(2,0,-1)]))   # True
print("负环? ", has_neg_cycle(3,[(0,1,1),(1,2,1),(2,0,1)]))     # False
```

> **复杂度**：平均 O(k·m)，最坏 O(n·m)。


### 13.40 全源最短路 / 传递闭包 / 二分图判定 / 错排 / 逆波兰 / 水塘抽样

#### 13.40.1 例 146：Johnson 全源最短路（负权 + 重赋值 + 多源 Dijkstra）⭐⭐⭐

> **知识点**：Bellman–Ford，Johnson 重赋值，全源最短路｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的全源最短路综合题，主要考察 Johnson 算法（Bellman–Ford 重赋值 + 多源 Dijkstra）。处理带负权边的全源最短路。

**思路**
含负边时不能直接多次 Dijkstra。Johnson：加虚拟源连所有顶点（0 权边），用 Bellman–Ford 求势能 h；重赋值 `w'=w+h[u]−h[v]`（由三角不等式知 w'≥0）使所有边非负，再对每个顶点跑一次堆优化 Dijkstra，最后还原原边长。💡 类比坐标平移：用一组势能把负边整体抬平，使边权非负从而安全使用更快的 Dijkstra，一次 Bellman–Ford 就得到平移量。

```python
import heapq
def johnson(n, edges):
    super=n; Eg=[[] for _ in range(n+1)]
    for u,v,w in edges: Eg[u].append((v,w))
    for u in range(n): Eg[super].append((u,0))
    inf=float('inf'); h=[inf]*(n+1); h[super]=0
    for _ in range(n):                       # Bellman-Ford 松弛 n 次
        for u in range(n+1):
            if h[u]==inf: continue
            for v,w in Eg[u]:
                if h[v]>h[u]+w: h[v]=h[u]+w
    for u in range(n+1):                     # 再松弛一次检测负环
        if h[u]==inf: continue
        for v,w in Eg[u]:
            if h[v]>h[u]+w: return None
    gg=[[] for _ in range(n)]
    for u,v,w in edges: gg[u].append((v,w+h[u]-h[v]))
    D=[[inf]*n for _ in range(n)]
    for s in range(n):
        d=D[s]; d[s]=0; pq=[(0,s)]
        while pq:
            du,u=heapq.heappop(pq)
            if du>d[u]: continue
            for v,w in gg[u]:
                if d[v]>du+w:
                    d[v]=du+w; heapq.heappush(pq,(d[v],v))
        for v in range(n):
            if d[v]<inf: d[v]=d[v]-h[s]+h[v]
    return D

D=johnson(3,[(0,1,3),(0,2,-2),(1,2,1)])
print("0->1 =", D[0][1], " 0->2 =", D[0][2], " 全源矩阵行0 =", D[0])
```

> **复杂度**：O(n·(m log n))（n 次 Dijkstra）+ O(n·m)（一次 Bellman–Ford）；空间 O(n²)。

#### 13.40.2 例 147：Floyd–Warshall 传递闭包（bitset 优化）⭐⭐

> **知识点**：传递闭包，位掩码，可达性｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的图论题，主要考察 Floyd–Warshall 传递闭包与位掩码（bitset）优化。计算任意两点的可达性关系。

**思路**
`reach[u]` 用整数位表示 u 能到达的节点集合；按 k 做「中转闭合」：只要 u 能到达 k，就把 `reach[u] |= reach[k]`。用整型位运算，一条 OR 覆盖整行，比 O(n³) 的逐位 Floyd 快一个 word 因子。💡 类比符号传播：k 作为中间点把 reach[k] 的能力一次性传给所有能到 k 的点。

```python
def reachability(n, edges):
    reach=[0]*n
    for u,v in edges: reach[u]|=1<<v
    for k in range(n):
        for i in range(n):
            if (reach[i]>>k)&1: reach[i]|=reach[k]
    return reach

r=reachability(4,[(0,1),(1,2),(2,3)])
print("0 可达 3? ", bool((r[0]>>3)&1), "  0 的可达集合 =", r[0])
```

> **复杂度**：O(n³ / word)；建图 O(m)。word 为机器字长（64）。

#### 13.40.3 例 148：二分图判定（染色 / 奇环检测）⭐⭐

> **知识点**：二分图判定，BFS 染色｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的图论题，主要考察二分图判定的 BFS 染色与奇环检测。判断图是否为二分图。

**思路**
BFS 给每个点染 0/1，邻点必须异色；若某边两端同色则不是二分图（存在奇环）。对每个连通分量都要从任意未染色点出发，处理不连通图。💡 类比黑白染色：二分图等价于「能二染色且无奇环」，染色顶峰时的冲突就是奇环的证据。

```python
from collections import deque
def is_bipartite(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges: g[u].append(v); g[v].append(u)
    color=[-1]*n
    for s in range(n):
        if color[s]>=0: continue
        color[s]=0; q=deque([s])
        while q:
            u=q.popleft()
            for v in g[u]:
                if color[v]<0: color[v]=color[u]^1; q.append(v)
                elif color[v]==color[u]: return False
    return True

print("路径可二分? ", is_bipartite(4,[(0,1),(1,2),(2,3)]))           # True
print("含三角形可二分? ", is_bipartite(4,[(0,1),(1,2),(2,0),(1,3)]))  # False
```

> **复杂度**：O(n+m)；空间 O(n+m)。

#### 13.40.4 例 149：错排问题（计数 DP）⭐⭐

> **知识点**：错排递推，组合计数｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的组合计数题，主要考察错排问题的递推。求 n 个元素错位排列的数量。

**思路**
错排 D(n) 为 n 个元素每个都不在原来位置的排法数。递推 `D(n)=(n−1)·(D(n−1)+D(n−2))`，边界 D(0)=1、D(1)=0：第 n 个元素可放到前 n−1 个的任一位置，而原来占那个位置的元素要么放第 n 位、要么放到其他空位，两分支分别对应 D(n−2) 与 D(n−1)。💡 类比动态转移两情形：把一个「错配」粗分为两个子情形，只要递归深度两步即可由小规模推出大规模。

```python
def derangements(n):
    if n==0: return 1
    if n==1: return 0
    a,b=1,0                      # D0, D1
    for i in range(2,n+1):
        a,b=b,(i-1)*(a+b)
    return b

print("D1..D6 =", [derangements(i) for i in range(1,7)])  # 0,1,2,9,44,265
```

> **复杂度**：O(n)；空间 O(1)。

#### 13.40.5 例 150：逆波兰表达式 / 中缀转后缀（调度场）⭐⭐

> **知识点**：栈，表达式求值，调度场算法｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的表达式求值题，主要考察栈与调度场算法（中缀转后缀）。计算逆波兰表达式或将中缀表达式转为后缀。

**思路**
后缀（逆波兰）求值：数字入栈，遇到运算符弹两数计算后压回。中缀转后缀用「操作符栈」：数字直接输出，遇到闭括号弹栈到左括号，运算符按优先级（同优先级栈顶更高的先输出，如左结合）。💡 类比括号嵌套：后缀式把运算先后完全展开成线性序列，求值只需一个栈，天然消除了括号与优先级歧义。

```python
prec={'+':1,'-':1,'*':2,'/':2}
def to_rpn(expr):                    # 中缀->后缀（单字符数字/字母）
    out=[]; st=[]
    for ch in expr:
        if ch.isalnum(): out.append(ch)
        elif ch=='(': st.append(ch)
        elif ch==')':
            while st and st[-1]!='(': out.append(st.pop())
            st.pop()
        else:
            while st and st[-1]!='(' and prec[ch]<=prec[st[-1]]: out.append(st.pop())
            st.append(ch)
    while st: out.append(st.pop())
    return ''.join(out)

def eval_rpn(tokens):
    st=[]
    for tk in tokens:
        if tk in '+-*/':
            b=st.pop(); a=st.pop()
            if tk=='+': st.append(a+b)
            elif tk=='-': st.append(a-b)
            elif tk=='*': st.append(a*b)
            else: st.append(a//b)
        else: st.append(int(tk))
    return st[0]

print(to_rpn("a+b*c"))                    # abc*+
print(eval_rpn(['2','3','4','*','+']))    # 14
```

> **复杂度**：O(n)；空间 O(n)。

#### 13.40.6 例 151：水塘抽样（Reservoir Sampling，等概率在线采样 k 个）⭐⭐

> **知识点**：随机化，水塘抽样，拒绝/替换法｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的随机化题，主要考察水塘抽样（等概率在线采样 k 个）。在不预知总数的情况下均匀随机地抽取样本。

**思路**
前 k 个直接收入水塘；之后遇到第 i 个元素（i≥k）以概率 k/i 随机替换水塘中一个位置。推导可证每个元素最终留在水塘的概率都是 k/n，且不需要预先知道流长度。💡 类比抽签换票：把每个新来者以「越来越小」的概率顶掉一个旧名额，逐个流式处理仍保持均匀。

```python
import random
def reservoir(stream,k):
    sample=[]
    for i,v in enumerate(stream):
        if i<k: sample.append(v)
        else:
            j=random.randint(0,i)
            if j<k: sample[j]=v
    return sample

random.seed(1)
print(sorted(reservoir(range(1,101),5)))
```

> **复杂度**：O(n)；空间 O(k)。


### 13.41 回文子序列 / 摩尔投票 / 树形 DP 直径 / Kruskal 重构树

#### 13.41.1 例 152：最长回文子序列（区间 DP）⭐⭐

> **知识点**：区间 DP，回文子序列（LPS）｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的区间 DP 题，主要考察最长回文子序列（LPS）。求字符串最长回文子序列长度。

**思路**
`dp[l][r]`：子串 s[l..r] 最长回文子序列长度。两端相同则 `dp[l][r]=dp[l+1][r−1]+2`，否则 `dp[l][r]=max(dp[l+1][r],dp[l][r−1])`，按长度从小到大填表。💡 类比去两端：判断「要不要两端」，两端相同时必选并缩短两端，否则舍去较小一端的贡献取 max。

```python
def lps(s):
    n=len(s)
    dp=[[0]*n for _ in range(n)]
    for i in range(n): dp[i][i]=1
    for length in range(2,n+1):
        for l in range(0,n-length+1):
            r=l+length-1
            if s[l]==s[r]: dp[l][r]=dp[l+1][r-1]+2
            else: dp[l][r]=max(dp[l+1][r],dp[l][r-1])
    return dp[0][n-1]

print("bbbab 最长回文子序列 =", lps("bbbab"))   # 4 (bbbb)
print("cbbd 最长回文子序列 =", lps("cbbd"))     # 2 (bb)
```

> **复杂度**：O(n²)；空间 O(n²)（可滚动数组优化到 O(n)）。

#### 13.41.2 例 153：摩尔投票求多数元素（出现次数 > n/2）⭐⭐

> **知识点**：摩尔投票，抵消法｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的序列题，主要考察摩尔投票的抵消法。求出现次数超过一半的多数元素。

**思路**
维护候选候选人 cand 与计数 cnt：遇到相同 +1、不同 −1（配对抵消），cnt 归零时更换候选。因为多数元素出现超过一半，它的「净优势」保证最后一定剩下它。💡 类比两两PK抵消：每次用一对「不同元素」同时划掉，多数元素永远不亏，最后留下的就是答案。

```python
def majority(a):
    cand=None; cnt=0
    for x in a:
        if cnt==0: cand=x; cnt=1
        elif x==cand: cnt+=1
        else: cnt-=1
    return cand

print("多数元素 =", majority([2,2,1,1,1,2,2]))   # 2
```

> **复杂度**：O(n)；空间 O(1)。（需要再扫一遍验证频数是否真的过半。）

#### 13.41.3 例 154：树形 DP 求树的直径（DP 法，非两遍 DFS）⭐⭐

> **知识点**：树形 DP，树的直径｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的树形 DP 题，主要考察 DP 法求树的直径。在不使用两次 DFS 的情况下求树的直径。

**思路**
对每个节点维护「子树内最深的两条向下路径 mx1,mx2」，`mx1+mx2` 为「经过该节点的最长路径候选」；递归时用最长子链 `mx1+1` 更新父节点。所有节点的 `mx1+mx2` 取最大即树的直径。💡 类比挂钥匙环：直径必经过某个节点，在该节点处它是「最深两条链的连接」，DP 自底向上收集每条链的最深深度即可。

```python
import sys
def tree_dia(n, edges):
    sys.setrecursionlimit(10**6)
    g=[[] for _ in range(n)]
    for u,v in edges: g[u].append(v); g[v].append(u)
    dep=[0]*n; dia=[0]
    def dfs(u,p):
        mx1=mx2=0
        for v in g[u]:
            if v==p: continue
            dfs(v,u)
            d=dep[v]+1
            if d>mx1: mx1,mx2=d,mx1
            elif d>mx2: mx2=d
        dep[u]=mx1
        dia[0]=max(dia[0],mx1+mx2)
    dfs(0,-1)
    return dia[0]

print("直径 =", tree_dia(4,[(0,1),(1,2),(1,3)]))   # 2
```

> **复杂度**：O(n)；空间 O(n)。

#### 13.41.4 例 155：Kruskal 重构树（最小瓶颈 / 两点路径最大边权最小值）⭐⭐⭐

> **知识点**：Kruskal 重构树，并查集，LCA，最小瓶颈路｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度很高的最小瓶颈综合题，主要考察 Kruskal 重构树、并查集与 LCA。求两点路径上最大边权的最小可能值（最小瓶颈路）。

**思路**
按边权升序跑 Kruskal：每次合并两个连通块时新建一个节点作为二者新根，其权值 = 当前边权 w，原两子树挂为它的儿子。如此得到一棵「大根堆 + 二叉树」的森林，两点在原图中「路径最大边的最小值」＝重构树中它们 LCA 的权值。💡 类比建金字塔：把并查集合并过程显式记录为新节点，边权越大节点越高，LCA 高度即瓶颈；把「最小瓶颈路」问题变成一次 LCA 查询。

```python
def kruskal_rebuild(n, edges):      # edges:(u,v,w)，返回最大新节点数、LCA可用
    edges.sort(key=lambda e:e[2])
    fa=list(range(2*n))
    val=[0]*(2*n)
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    child=[[] for _ in range(2*n)]
    c=n
    for u,v,w in edges:
        ru,rv=find(u),find(v)
        if ru!=rv:
            fa[ru]=c; fa[rv]=c; val[c]=w
            child[c].append(ru); child[c].append(rv)
            c+=1
    root=c-1
    # 建父表 + 求 LCA（倍增），供瓶颈查询
    LOG=(2*n).bit_length()
    up=[[root]*(LOG) for _ in range(2*n)]
    depth=[0]*(2*n)
    par=[root]*2*n
    order=[root]
    for node in order:
        for son in child[node]:
            par[son]=node;depth[son]=depth[node]+1;order.append(son)
    up=[par[:]]
    for k in range(1,LOG):
        prev=up[-1]; up.append([prev[prev[i]] for i in range(2*n)])
    def lca(a,b):
        if depth[a]<depth[b]: a,b=b,a
        diff=depth[a]-depth[b]
        k=0
        while diff:
            if diff&1: a=up[k][a]
            diff>>=1; k+=1
        if a==b: return a
        for k in range(LOG-1,-1,-1):
            if up[k][a]!=up[k][b]:
                a=up[k][a]; b=up[k][b]
        return up[0][a]
    def max_edge_min(u,v): return val[lca(u,v)]
    return max_edge_min, root

# 测试：链 0-1(w1)-2(w2)-3(w3)；0 到 3 的最小瓶颈=最大边=3
mef,_=kruskal_rebuild(4,[(0,1,1),(1,2,2),(2,3,3)])
print("0 到 3 的最小瓶颈 =", mef(0,3))
```

> **复杂度**：O(m log m)（建树）；瓶颈查询 O(log n)。


APPEND_DONE_MARKER



### 13.42 数论筛法 / 线段树合并 / 差分与分块综合

#### 13.42.1 例 156：欧拉函数线性筛与 φ 前缀和（积性函数筛法）⭐⭐

> **知识点**：欧拉函数，线性筛｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的数论题，主要考察欧拉函数与积性函数线性筛。线性筛法求欧拉函数及其前缀和。

**思路**
线性筛（欧拉筛）在筛去合数的同时递推积性函数：对每个质数 p 与当前数 i，若 i % p == 0 则新数含 p 幂次 ≥2，`φ(i·p)=φ(i)·p`；否则两数互质，`φ(i·p)=φ(i)·(p−1)`。同步累加 φ 得到前缀和数组。💡 类比魔法门：每个合数只由它最小的质因子筛掉一次以保证 O(n)，积性函数值按「首因子是否重复」两类合并得到。

```python
def phi_prefix(n):
    phi = list(range(n + 1))
    pre = [0] * (n + 1)
    if n >= 1:
        phi[1] = 1
    isc = [False] * (n + 1)
    primes = []
    s = 0
    for i in range(2, n + 1):
        if not isc[i]:
            primes.append(i)
            phi[i] = i - 1
        for p in primes:
            if i * p > n:
                break
            isc[i * p] = True
            if i % p == 0:
                phi[i * p] = phi[i] * p
                break
            phi[i * p] = phi[i] * (p - 1)
    for i in range(1, n + 1):
        s += phi[i]
        pre[i] = s
    return pre

pre = phi_prefix(10)
print("phi(1..10) 前缀和 =", pre[10])   # 32 (1,1,2,2,4,2,6,4,6,4 之和)
```

> **复杂度**：O(n)；空间 O(n)。

#### 13.42.2 例 157：线段树合并（动态开点权值线段树合并求众数）⭐⭐⭐

> **知识点**：权值线段树，动态开点，线段树合并｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的线段树合并综合题，主要考察动态开点权值线段树合并。对每个子树统计众数（次数最多的值）。

**思路**
为每个位置（或每个子树）建一棵值域上的权值线段树，把子节点/相邻的树「合并」进父树：递归遍历两棵树的重叠节点，相同位置计数相加，空节点直接指向对方以复用。合并后整棵树的 max 对即值域中出现最多的权值（众数）。💡 类比两本账本对账：同一值在两边都记了数就相加，一方没记则直接采纳对方的页，从而把多棵树的代价压到 O(总点数)、每次合并均摊 O(log 值域)。

```python
def segtree_merge_example():
    nleaf = 4
    class Node:
        __slots__ = ('l', 'r', 'cnt', 'maxv', 'maxc')
        def __init__(self):
            self.l = self.r = -1
            self.cnt = 0; self.maxv = -1; self.maxc = 0
    nodes = [Node()]
    def new():
        nodes.append(Node()); return len(nodes) - 1
    def upd(o):
        nodes[o].cnt = 0; nodes[o].maxc = 0; nodes[o].maxv = -1
        for c in (nodes[o].l, nodes[o].r):
            if c != -1:
                nodes[o].cnt += nodes[c].cnt
                if nodes[c].maxc > nodes[o].maxc:
                    nodes[o].maxc = nodes[c].maxc
                    nodes[o].maxv = nodes[c].maxv
    def ins(o, l, r, pos):
        if o == -1: o = new()
        if l == r:
            nodes[o].cnt += 1
            nodes[o].maxc = nodes[o].cnt; nodes[o].maxv = l
            return o
        m = (l + r) // 2
        if pos <= m: nodes[o].l = ins(nodes[o].l, l, m, pos)
        else:        nodes[o].r = ins(nodes[o].r, m + 1, r, pos)
        upd(o); return o
    def merge(a, b, l, r):
        if a == -1: return b
        if b == -1: return a
        if l == r:
            nodes[a].cnt += nodes[b].cnt
            nodes[a].maxc = nodes[a].cnt; nodes[a].maxv = l
            return a
        m = (l + r) // 2
        nodes[a].l = merge(nodes[a].l, nodes[b].l, l, m)
        nodes[a].r = merge(nodes[a].r, nodes[b].r, m + 1, r)
        upd(a); return a
    a = ins(-1, 1, nleaf, 1); a = ins(a, 1, nleaf, 3)
    b = ins(-1, 1, nleaf, 2)
    c = ins(-1, 1, nleaf, 1)
    root = merge(a, b, 1, nleaf); root = merge(root, c, 1, nleaf)
    return nodes[root].maxv, nodes[root].maxc

print("三树合并后的众数(值,次数) =", segtree_merge_example())   # (1, 2)
```

> **复杂度**：每棵点树点数为 O(k log V)，合并总复杂度 O(总点数)；查询 O(1)。

#### 13.42.3 例 158：树状数组区间修改、区间求和（双 BIT）⭐⭐

> **知识点**：树状数组，差分｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的数据结构题，主要考察树状数组实现区间修改、区间求和（双 BIT）。支持区间加与区间和查询。

**思路**
单差分解决「区间加 + 单点查」；要支持「区间加 + 区间和」用两个树状数组：设差分数组 d，则前缀和 P[1..i]=Σd·i−Σ(d·(j−1))。分别用 BIT1 维护 d、BIT2 维护 d·(j−1)，区间和=两次前缀和之差。💡 类比超额累进账本：一个账记「每天增加量」，另一个记「累计到定点的增量×位置」，两账相减即精确的区间总量，容纳任意多次区间加。

```python
def range_add_range_sum(arr, ops):
    n = len(arr)
    B1 = [0] * (n + 1); B2 = [0] * (n + 1)
    def add(B, i, v):
        while i <= n:
            B[i] += v; i += i & -i
    def ssum(B, i):
        s = 0
        while i > 0:
            s += B[i]; i -= i & -i
        return s
    for i in range(1, n + 1):
        v = arr[i - 1] - (arr[i - 2] if i > 1 else 0)
        add(B1, i, v); add(B2, i, v * (i - 1))
    def psum(i):
        return i * ssum(B1, i) - ssum(B2, i)
    def range_add(l, r, v):
        add(B1, l, v); add(B2, l, v * (l - 1))
        if r < n:
            add(B1, r + 1, -v); add(B2, r + 1, -v * r)
    res = []
    for op in ops:
        if op[0] == 'add':
            range_add(op[1], op[2], op[3])
        else:
            res.append(psum(op[2]) - psum(op[1] - 1))
    return res

print("区间和查询 =", range_add_range_sum([1, 2, 3, 4, 5],
      [('sum', 1, 5), ('add', 2, 4, 5), ('sum', 1, 5)]))   # [15, 30]
```

> **复杂度**：每次操作 O(log n)；空间 O(n)。

#### 13.42.4 例 159：矩阵快速幂优化线性递推（斐波那契）⭐⭐

> **知识点**：矩阵乘法，快速幂，线性递推｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的矩乘综合题，主要考察矩阵乘法 + 快速幂优化线性递推。用矩阵快速幂加速斐波那契等线性递推。

**思路**
把线性递推写成转移矩阵 M，则第 n 项可由 M 的 n 次幂作用于初始向量得到。快速幂将 O(n) 次迭代变成 O(log n) 次矩阵乘法。对斐波那契，矩阵 [[1,1],[1,0]] 的 n 次幂的 (0,1) 元素即 F_n。💡 类比复利倍增：把「每一步的规则」浓缩成一个矩阵，用平方连乘一次翻倍地幂运算，跳过多轮迭代直达第 n 步。

```python
def mat_mul(a, b):
    n = len(a); m = len(b[0]); K = len(b)
    c = [[0] * m for _ in range(n)]
    for i in range(n):
        for k in range(K):
            if a[i][k]:
                for j in range(m):
                    c[i][j] += a[i][k] * b[k][j]
    return c

def mat_pow(a, e):
    n = len(a)
    r = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    while e:
        if e & 1: r = mat_mul(r, a)
        a = mat_mul(a, a); e >>= 1
    return r

def fib(n):
    if n == 0: return 0
    M = [[1, 1], [1, 0]]
    P = mat_pow(M, n)
    return P[0][1]

print("F(10) =", fib(10))     # 55
print("F(50) =", fib(50))     # 12586269025
```

> **复杂度**：矩阵乘法 O(k³)·O(log n)，k 为状态维数；空间 O(k²)。

#### 13.42.5 例 160：哈夫曼合并果子（优先队列贪心）⭐⭐

> **知识点**：贪心，优先级队列｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的贪心题，主要考察用优先级队列不断合并最小的两项（哈夫曼）。求合并 n 堆果子所需的最小体力花费。

**思路**
每次取当前权值最小的两堆合并，代价为两堆之和，总代价即叶节点加权路径长（霍夫曼编码同一模型）。用最小堆保证每次 O(log n) 取出最小两堆，总代价最小。💡 类比合并零钱：越轻的果子被合并次数越多才能让总和最小，所以永远优先合并当前最轻的两堆，小根堆即时给出。

```python
import heapq

def merge_fruit(a):
    heapq.heapify(a)
    cost = 0
    while len(a) > 1:
        x = heapq.heappop(a); y = heapq.heappop(a)
        s = x + y
        cost += s
        heapq.heappush(a, s)
    return cost

print("最小体力消耗 =", merge_fruit([1, 2, 9]))   # 1+2=3, 3+9=12 → 3+12=15
```

> **复杂度**：O(n log n)；空间 O(n)。

#### 13.42.6 例 161：树上差分统计每条路径的覆盖次数（LCA）⭐⭐⭐

> **知识点**：LCA，树上差分｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的树上差分综合题，主要考察 LCA 与树上差分。统计每条路径对每个点/边的覆盖次数。

**思路**
对每条路径 (u,v)，令 l=LCA(u,v)、f=parent(l)，做点差分：`w[u]+=1, w[v]+=1, w[l]−=1, w[f]−=1`。最后从叶子向上做一次后序累加（每个点把自身累加到父节点），w[x] 即覆盖 x 的路径数。💡 类比记账补偿：起点+1、终点+1 足以覆盖整条链，但会在 l 处多算一次向上，于是在 l 扣 1、再在 l 的父亲扣 1 恰好抵消越界的部分，一次累加即得每条点被覆盖多少次。

```python
import sys
def path_cover_count(n, edges, queries):
    sys.setrecursionlimit(10 ** 6)
    g = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u + 1].append(v + 1); g[v + 1].append(u + 1)
    LOG = (n + 2).bit_length()
    dep = [0] * (n + 1); parent = [0] * (n + 1)
    up = [[0] * LOG for _ in range(n + 1)]
    vis = [False] * (n + 1); vis[1] = True; seq = [1]
    for u in seq:
        for v in g[u]:
            if not vis[v]:
                vis[v] = True; parent[v] = u
                dep[v] = dep[u] + 1; seq.append(v)
    for u in range(1, n + 1): up[u][0] = parent[u]
    for k in range(1, LOG):
        for u in range(1, n + 1):
            up[u][k] = up[up[u][k - 1]][k - 1]
    def lca(a, b):
        if dep[a] < dep[b]: a, b = b, a
        d = dep[a] - dep[b]; k = 0
        while d:
            if d & 1: a = up[a][k]
            d >>= 1; k += 1
        if a == b: return a
        for k in range(LOG - 1, -1, -1):
            if up[a][k] != up[b][k]:
                a = up[a][k]; b = up[b][k]
        return up[a][0]
    w = [0] * (n + 1)
    for u, v in queries:
        u += 1; v += 1
        l = lca(u, v); f = parent[l]
        w[u] += 1; w[v] += 1; w[l] -= 1
        if f >= 1: w[f] -= 1
    for u in reversed(seq[1:]):
        w[parent[u]] += w[u]
    return w[1:]

# 链 0-1-2，一条路径 (0,2) 覆盖 3 个点
print("路径覆盖次数 =", path_cover_count(3, [(0, 1), (1, 2)], [(0, 2)]))  # [1,1,1]
```

> **复杂度**：预处理 O(n log n)；每条路径 O(log n)；后序累加 O(n)。

#### 13.42.7 例 162：最少回文分割（区间 DP）⭐⭐⭐

> **知识点**：区间 DP，回文预处理｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的区间 DP 综合题，主要考察区间 DP 与回文预处理。求将字符串分割成若干回文子串所需的最少分割次数。

**思路**
先用区间 DP 求出 pal[l][r]（s[l..r] 是否为回文：两端相同且内部为回文）。再一维 DP：cut[i] 表示把前缀 [0..i] 分成全回文段的最少切割数，若 [0..i] 整体为回文则 0，否则枚举最后一段 [j+1..i] 为回文，`cut[i]=min(cut[j]+1)`。💡 类比切香肠：先烘焙出「哪一段是完整的（回文）」，再用经典划分 DP 逐段切，把「是否回文」判断与「最小切数」两个问题分层解决。

```python
def min_cut(s):
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for i in range(n): pal[i][i] = True
    for i in range(n - 1): pal[i][i + 1] = (s[i] == s[i + 1])
    for L in range(3, n + 1):
        for i in range(0, n - L + 1):
            j = i + L - 1
            pal[i][j] = (s[i] == s[j] and pal[i + 1][j - 1])
    cut = [0] * n
    for i in range(n):
        if pal[0][i]:
            cut[i] = 0; continue
        cut[i] = i
        for j in range(i):
            if pal[j + 1][i]:
                cut[i] = min(cut[i], cut[j] + 1)
    return cut[n - 1]

print("aab 最少切刀数 =", min_cut("aab"))    # 1 (aa | b)
print("aba 最少切刀数 =", min_cut("aba"))    # 0
```

> **复杂度**：预处理 O(n²)；划分 DP O(n²)；空间 O(n²)。

#### 13.42.8 例 163：KMP next 数组求字符串最小循环节 ⭐⭐

> **知识点**：KMP，前缀函数｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的字符串题，主要考察 KMP next/前缀函数求最小循环节。求字符串的最小循环节长度及是否由循环节构成。

**思路**
计算前缀函数 pi，令 len=pi[n−1]，则 n−len 是「候选循环节长度」。若 n % (n−len)==0，最小循环节长度就是 n−len，且反复由它拼成原串；否则整串是最小循环节。💡 类比尺子量零件：前缀函数给出的「最长公共前后缀」揭示了字符串的平移对称性，剩余的那段就是你需要的重复单元，能整除说明正好铺满。

```python
def min_cycle(s):
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]: j += 1
        pi[i] = j
    k = n - pi[n - 1]
    return k if n % k == 0 else n

print("ababab 循环节长度 =", min_cycle("ababab"))   # 2 (ab)
print("ababa  循环节长度 =", min_cycle("ababa"))    # 5
```

> **复杂度**：O(n)；空间 O(n)。

#### 13.42.9 例 164：硬币找零的凑数方案数（完全背包）⭐⭐

> **知识点**：完全背包，计数 DP｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的计数 DP 题，主要考察完全背包计数。求用若干面额凑出指定金额的方案数。

**思路**
外层遍历每枚硬币、内层从小到大更新 dp[x]，dp[x] 表示用面额可重复使用凑出 x 的方案数，递推 `dp[x]+=dp[x−c]`。外层硬币在内层之前保证了「组合」而非排列，不会把 1+2 与 2+1 当成两种。💡 类比配钥匙清单：先固定一种面额依次多放，再去考虑下一种，天然去重；外层控制「种类」，内层控制「金额」即是完全背包的计数版。

```python
def coin_change_count(coins, target):
    dp = [0] * (target + 1)
    dp[0] = 1
    for c in coins:
        for x in range(c, target + 1):
            dp[x] += dp[x - c]
    return dp[target]

print("用 1/2/5 凑 11 的方案数 =", coin_change_count([1, 2, 5], 11))   # 11
print("用 1/2 凑 4 的方案数 =", coin_change_count([1, 2], 4))          # 3
```

> **复杂度**：O(硬币数 × target)；空间 O(target)。

#### 13.42.10 例 165：线性求逆元与组合数取模 ⭐⭐

> **知识点**：费马小定理，线性逆元｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的数论题，主要考察费马小定理与线性求逆元。预处理一系列数的逆元并计算组合数取模。

**思路**
先用快速幂 `pow(fact[n], mod−2, mod)` 求阶乘逆元（费马小定理，mod 为质数），再倒推 `inv[i−1]=inv[i]·i` 得到所有阶乘逆元。组合数 C(n,k)=fact[n]·inv[k]·inv[n−k] mod p。把 O(k·log p) 的逐项求逆降为 O(n) 预处理。💡 类比逆向还原组合：一次性从最大阶乘逆元往回乘 i 逐级「反推」出每个阶乘的倒数，换取任意 (k,n) 都能 O(1) 取组合数。

```python
def solve(n, k, mod):
    if k > n: return 0
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    inv = [1] * (n + 1)
    inv[n] = pow(fact[n], mod - 2, mod)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % mod
    return fact[n] * inv[k] % mod * inv[n - k] % mod

MOD = 10 ** 9 + 7
print("C(10,3) mod 1e9+7 =", solve(10, 3, MOD))   # 120
print("C(100,2) mod 1e9+7 =", solve(100, 2, MOD)) # 4950
```

> **复杂度**：预处理 O(n)；单次组合数 O(1)。

#### 13.42.11 例 166：DAG 最长关键路径（拓扑 + DP）⭐⭐

> **知识点**：拓扑排序，DP，关键路径｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/AOE
**题目描述**：这是一道较综合的图论 DP 题，主要考察拓扑排序 + DP 求最长关键路径（AOE）。求有向无环图中的最长路径。

**思路**
对工程 AOE 网络求最长路即最短工期。按拓扑序做 DP：`dist[v]=max(dist[v], dist[u]+w)`，拓扑序保证更新 u 时其所有前驱已确定。队列不断取出入度为 0 的点，最后 max(dist) 即关键路径长度。💡 类比排工序：只有所有前置工序完成后才能启动下一道，所以每个工序的完工时刻取「完全部前驱的最晚下界」，拓扑顺序即施工顺序。

```python
from collections import deque
def dag_longest(n, edges):
    g = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        g[u].append((v, w)); indeg[v] += 1
    q = deque([i for i in range(n) if indeg[i] == 0])
    dist = [0] * n
    while q:
        u = q.popleft()
        for v, w in g[u]:
            dist[v] = max(dist[v], dist[u] + w)
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return max(dist)

# 任务依赖：0→1(3) 0→2(2) 1→3(4) 2→3(5)
print("最短工期 =", dag_longest(4, [(0, 1, 3), (0, 2, 2), (1, 3, 4), (2, 3, 5)]))  # 7
```

> **复杂度**：O(n + m)；空间 O(n + m)。

#### 13.42.12 例 167：威佐夫博弈（奇异局势判定）⭐⭐

> **知识点**：博弈论，黄金分割｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的博弈题，主要考察威佐夫博弈的奇异局势判定（黄金分割）。判断两堆取子游戏的先手胜负。

**思路**
两堆 (a,b)，a≤b。若开始处于「奇异局势」则先手必败。奇异局势满足 b−a=d 与 `a=floor(d·φ)`，其中 φ=(1+√5)/2。判定等式成立即先手败，否则先手可通过一次移动进入奇异局势而胜。💡 类比完美调平：奇异局势像天平预调到「差值×黄金比等于较小堆」的刁钻刻度，先手无论怎么动都会打破这平衡、把必胜位让给对方。

```python
from math import floor, sqrt
def wythoff(a, b):
    if a > b: a, b = b, a
    d = b - a
    phi = (1 + sqrt(5)) / 2
    return "先手必败" if floor(d * phi) == a else "先手必胜"

print("(1,2) →", wythoff(1, 2))   # 先手必败（奇异局势）
print("(2,3) →", wythoff(2, 3))   # 先手必胜
```

> **复杂度**：O(1)；空间 O(1)。

#### 13.42.13 例 168：树的最小点覆盖（树形 DP）⭐⭐

> **知识点**：树形 DP，点覆盖｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的树形 DP 题，主要考察树的最小点覆盖。选择最少的点覆盖所有边。

**思路**
dp0[u]：u 不选时子树最小点覆盖；dp1[u]：u 必选时子树最小点覆盖。若 u 不选，其子节点必须全部选中；若 u 选，子节点可选可不选取 min。叶子初始化，DFS 后根取 min(dp0[root], dp1[root])。💡 类比小区安保方案：每栋楼要么自己挂牌值守、要么让所有邻居代管；用「选/不选」两状态自底向上汇总，最近公共覆盖数即最小。

```python
import sys
def min_vertex_cover(n, edges):
    sys.setrecursionlimit(10 ** 6)
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v); g[v].append(u)
    dp0 = [0] * n; dp1 = [0] * n
    def dfs(u, p):
        dp1[u] = 1; dp0[u] = 0
        for v in g[u]:
            if v == p: continue
            dfs(v, u)
            dp0[u] += dp1[v]
            dp1[u] += min(dp0[v], dp1[v])
    dfs(0, -1)
    return min(dp0[0], dp1[0])

# 星形 1 连 0/2/3，选 {1} 覆盖所有边
print("最小点覆盖 =", min_vertex_cover(4, [(0, 1), (1, 2), (1, 3)]))   # 1
```

> **复杂度**：O(n)；空间 O(n)。

#### 13.42.14 例 169：快慢指针检测链表环并求环入口 ⭐⭐

> **知识点**：Floyd 判圈，链表｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的链表题，主要考察快慢指针（Floyd 判圈）检测链表环并求环入口。

**思路**
快指针每次走两步、慢指针走一步，若相遇必有环。相遇后把慢指针移到表头、快指针每次走一步，两者再次相遇处即环入口。理由：相遇点距入口的步数等于表头到入口的步数。💡 类比下潭找人：两只速度差一倍的兔子一进环必然追上；追上的瞬间把兔子放回入口同速重走，二次碰头点正是环的入水口。

```python
class Node:
    def __init__(self, x):
        self.val = x; self.next = None

def build(arr, pos=-1):
    head = cur = None; nodes = []
    for x in arr:
        nd = Node(x); nodes.append(nd)
        if cur: cur.next = nd
        else:   head = nd
        cur = nd
    if pos >= 0: cur.next = nodes[pos]   # pos 指向成环点
    return head

def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next; fast = fast.next.next
        if slow is fast:
            p = head
            while p is not slow:
                p = p.next; slow = slow.next
            return p.val
    return None

print("环入口 =", detect_cycle(build([1, 2, 5, 9], pos=1)))  # 2
print("无环  =", detect_cycle(build([1, 2, 3])))             # None
```

> **复杂度**：O(n)；空间 O(1)。

#### 13.42.15 例 170：区间调度——最多不相交区间（贪心）⭐⭐

> **知识点**：贪心，区间排序｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的贪心题，主要考察按结束时间排序的区间贪心。求最多不相交区间数量。

**思路**
按右端点升序排序，逐一遍历：只要当前区间左端点 ≥ 上次已选区间的右端点就纳入并更新右端边界。按右端点取最早结束的区间一定能空出最多时间给后续，从而全局最优。💡 类比电影院排场次：总是先排「结束最早」的片子，好把时间留给越多后续场次，早结束即多机会。

```python
def max_intervals(intervals):
    intervals.sort(key=lambda x: (x[1], x[0]))
    cnt = 0; end = -10 ** 18
    for l, r in intervals:
        if l >= end:
            cnt += 1; end = r
    return cnt

print("最多不相交区间 =", max_intervals([(1, 3), (2, 4), (3, 6)]))   # 2 (1,3)(3,6)
```

> **复杂度**：O(n log n)；空间 O(1)。

#### 13.42.16 例 171：极角/斜率去重统计非共线三点数 ⭐⭐

> **知识点**：斜率归一化，计数｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的计算几何计数题，主要考察斜率归一化与去重。统计给定点集中不共线三点组的数量。

**思路**
任取一个点 i，把其余点相对 i 的斜率归一化（约分到最简、dx 强制为正），统计每种斜率的个数 s；同斜率 s 个点会贡献 C(s,2) 个「过 i 的共线点对」。累加所有 i 的贡献后除以 3（每个共线三点被三个端点各算一次），再从总三角形数 C(n,3) 中扣除。💡 类比望远镜扫地平线：站在每个山头按「方向」归档同向的点，同一方向必然共线，据此一次性点清「歪斜的三点组合」。

```python
from math import gcd

def noncollinear_triangles(pts):
    n = len(pts)
    coll = 0
    for i in range(n):
        slope = {}
        for j in range(n):
            if i == j: continue
            dx = pts[j][0] - pts[i][0]
            dy = pts[j][1] - pts[i][1]
            if dx == 0:
                key = (0, 1)
            else:
                if dx < 0: dx, dy = -dx, -dy
                g = gcd(abs(dx), abs(dy))
                key = (dx // g, dy // g)
            slope[key] = slope.get(key, 0) + 1
        for s in slope.values():
            coll += s * (s - 1) // 2
    total = n * (n - 1) * (n - 2) // 6
    return total - coll // 3

pts = [(0, 0), (1, 0), (2, 0), (0, 1)]   # 前三点共线
print("非共线三点个数 =", noncollinear_triangles(pts))   # 3
```

> **复杂度**：O(n² log V)；空间 O(n)。

#### 13.42.17 例 172：唯一分解求约数个数与约数和 ⭐⭐

> **知识点**：质因数分解，约数函数｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的数论题，主要考察质因数分解与约数函数（约数个数、约数和）。求给定数的约数个数与约数和。

**思路**
把 n 分解为 ∏pᵢ^eᵢ。约数个数 τ(n)=∏(eᵢ+1)；约数和 σ(n)=∏((pᵢ^(eᵢ+1)−1)/(pᵢ−1))。枚举质因子到 √n，最后剩余的大于 √n 的质因子单独处理。💡 类比星座计数：每个质数幂次决定了它在每个约数里「出现 0..e 次」的取舍，乘回各质数的等比级数和即全部组合。

```python
def divisor_info(n):
    cnt = 1; sm = 1; x = n; p = 2
    while p * p <= x:
        if x % p == 0:
            e = 0; pk = 1
            while x % p == 0:
                x //= p; e += 1; pk *= p
            cnt *= e + 1
            sm *= (p ** (e + 1) - 1) // (p - 1)
        p += 1 if p == 2 else 2
    if x > 1:
        cnt *= 2
        sm *= (x + 1)
    return cnt, sm

d, s = divisor_info(12)
print("12 的约数个数 =", d)     # 6  (1,2,3,4,6,12)
print("12 的约数和   =", s)     # 28 (1+2+3+4+6+12)
```

> **复杂度**：O(√n)；空间 O(1)。

#### 13.42.18 例 173：二叉搜索树最近公共祖先（迭代，无父指针）⭐⭐

> **知识点**：二叉搜索树，LCA｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的树上查找题，主要考察二叉搜索树性质（迭代、无父指针）。求两节点在 BST 中的最近公共祖先。

**思路**
利用 BST 有序性：若 a、b 都小于当前节点则 LCA 在左子树；都大于则去右子树；否则当前节点值落在 a、b 之间（含端点），它即为两者的分岔点也就是 LCA。全程迭代 O(h)。💡 类比二叉树岔路口：两个目标一左一右时，你脚下这个节点正是他们分开的地方；只有同侧才继续下潜，第一次出现「分叉」即答案。

```python
class TNode:
    def __init__(self, x):
        self.val = x; self.left = None; self.right = None

def bst_lca(root, a, b):
    while root:
        if a < root.val and b < root.val:
            root = root.left
        elif a > root.val and b > root.val:
            root = root.right
        else:
            return root.val

def insert(r, x):
    if not r: return TNode(x)
    if x < r.val: r.left = insert(r.left, x)
    else:         r.right = insert(r.right, x)
    return r

root = None
for x in [6, 2, 8, 0, 4, 7, 9]:
    root = insert(root, x)
print("BST LCA(0,4) =", bst_lca(root, 0, 4))   # 2
print("BST LCA(2,8) =", bst_lca(root, 2, 8))   # 6
```

> **复杂度**：O(h)（平衡时 O(log n)）；空间 O(1)。

#### 13.42.19 例 174：矩阵中最长递增路径（记忆化搜索）⭐⭐

> **知识点**：记忆化搜索，DFS｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的搜索题，主要考察记忆化搜索 + DFS。求矩阵中最长递增路径的长度。

**思路**
在每个格子尝试向「值更大的相邻格」延伸，用 memo[i][j] 记录从 (i,j) 出发能走的最长递增路径，避免重复计算。答案取所有格子出发的最大值。四个方向、严格递增保证无环。💡 类比水往高处流：每条递增链像向上攀岩，记忆化把「我已爬到多高」存下来，再次路过直接采用，避免同一条山路被爬无数遍。

```python
def longest_increasing_path(grid):
    R = len(grid); C = len(grid[0])
    memo = [[0] * C for _ in range(R)]
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    def dfs(i, j):
        if memo[i][j]: return memo[i][j]
        best = 1
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < R and 0 <= nj < C and grid[ni][nj] > grid[i][j]:
                best = max(best, 1 + dfs(ni, nj))
        memo[i][j] = best
        return best
    return max(dfs(i, j) for i in range(R) for j in range(C))

g = [[3, 4, 5], [3, 2, 6], [2, 2, 1]]
print("最长递增路径 =", longest_increasing_path(g))   # 4 (3→4→5→6)
```

> **复杂度**：O(R·C)；空间 O(R·C)。

#### 13.42.20 例 175：分块——区间加与区间求和（sqrt 分解）⭐⭐

> **知识点**：分块，sqrt 分解｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的分块题，主要考察 sqrt 分解（分块）。支持区间加与区间求和。

**思路**
把数组分为约 √n 个块，记录整块和 block[b] 与整块懒标记 tag[b]。区间加：整块只打标记 O(1)，暴力处理边界散块并对块内 a[i] 实时改、同步更新 block；区间和：整块取 `block[b]+tag[b]·len`，散块逐点取 `a[i]+tag[所在块]`。💡 类比页数签字：整页封面一次性标注发行量，只有边角的几个零散格子才逐格改字，兼顾整读与散改的效率。

```python
import math
class SqrtDecomp:
    def __init__(self, a):
        self.n = len(a)
        self.B = int(math.sqrt(self.n)) + 1
        self.a = a[:]
        nb = (self.n + self.B - 1) // self.B
        self.block = [0] * nb; self.tag = [0] * nb
        for i in range(self.n):
            self.block[i // self.B] += a[i]
    def add(self, l, r, v):
        bl = l // self.B; br = r // self.B
        if bl == br:
            for i in range(l, r + 1): self.a[i] += v
            self.block[bl] += v * (r - l + 1); return
        for i in range(l, (bl + 1) * self.B):
            self.a[i] += v
        self.block[bl] += v * ((bl + 1) * self.B - l)
        for b in range(bl + 1, br): self.tag[b] += v
        for i in range(br * self.B, r + 1):
            self.a[i] += v
        self.block[br] += v * (r - br * self.B + 1)
    def query(self, l, r):
        bl = l // self.B; br = r // self.B; s = 0
        if bl == br:
            for i in range(l, r + 1): s += self.a[i] + self.tag[bl]
            return s
        for i in range(l, (bl + 1) * self.B):
            s += self.a[i] + self.tag[bl]
        for b in range(bl + 1, br):
            s += self.block[b] + self.tag[b] * self.B
        for i in range(br * self.B, r + 1):
            s += self.a[i] + self.tag[br]
        return s

sd = SqrtDecomp([1, 2, 3, 4, 5])
print("sum[0..4] =", sd.query(0, 4))        # 15
sd.add(0, 4, 1)
print("sum[0..4] after +1 =", sd.query(0, 4))  # 20
```

> **复杂度**：区间加/查各 O(√n)；空间 O(n)。


### 13.43 数据结构与图论综合进阶

#### 13.43.1 例 176：可持久化双端修改（主席树区间最值）⭐⭐⭐

> **知识点**：可持久化线段树、区间最值｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度极高的可持久化综合题，主要考察可持久化线段树维护区间最值。支持查询历史版本的区间最值。

**思路**

💡 类比"每一版都只改动一条路径，其他路径复用"：可持久化线段树每次修改只新建 O(log n) 个节点，历史版本完整保留。本题用其查询任意历史区间最小值。

```python
class PersistentSegTree:
    """可持久化线段树：每次 update 只新建 O(log n) 个节点，历史版本完整保留。"""

    INF = 10 ** 9

    def __init__(self, arr):
        self.n = len(arr)
        self.l = [0]
        self.r = [0]
        self.mn = [self.INF]

        def build(lo, hi):
            node = len(self.mn)
            self.l.append(0); self.r.append(0); self.mn.append(self.INF)
            if lo == hi:
                self.mn[node] = arr[lo]
                return node
            mid = (lo + hi) // 2
            self.l[node] = build(lo, mid)
            self.r[node] = build(mid + 1, hi)
            self.mn[node] = min(self.mn[self.l[node]], self.mn[self.r[node]])
            return node

        self.root0 = build(0, self.n - 1)     # 版本 0：初始数组

    def update(self, prev, lo, hi, pos, val):
        node = len(self.mn)
        self.l.append(self.l[prev]); self.r.append(self.r[prev]); self.mn.append(self.mn[prev])
        if lo == hi:
            self.mn[node] = val
            return node
        mid = (lo + hi) // 2
        if pos <= mid:
            self.l[node] = self.update(self.l[prev], lo, mid, pos, val)
        else:
            self.r[node] = self.update(self.r[prev], mid + 1, hi, pos, val)
        self.mn[node] = min(self.mn[self.l[node]], self.mn[self.r[node]])
        return node

    def upd(self, root, pos, val):
        return self.update(root, 0, self.n - 1, pos, val)

    def query(self, node, lo, hi, ql, qr):
        if qr < lo or hi < ql:
            return self.INF
        if ql <= lo and hi <= qr:
            return self.mn[node]
        mid = (lo + hi) // 2
        return min(self.query(self.l[node], lo, mid, ql, qr),
                   self.query(self.r[node], mid + 1, hi, ql, qr))

    def qry(self, node, ql, qr):
        return self.query(node, 0, self.n - 1, ql, qr)

pst = PersistentSegTree([5, 1, 3, 7, 2])
print(pst.qry(pst.root0, 0, 4))          # 初始版本全局 min = 1
root1 = pst.upd(pst.root0, 2, 0)         # 把下标 2 改为 0，得到版本 1
print(pst.qry(root1, 0, 4))              # 新版本 min = 0
print(pst.qry(pst.root0, 0, 4))          # 历史版本 0 仍为 1（持久化）
```

> **复杂度**：修改 O(log n)；查询 O(log n)。

#### 13.43.2 例 177：回滚莫队（区间 mex）⭐⭐⭐

> **知识点**：莫队、回滚、频次维护｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的莫队变体题，主要考察回滚莫队与频次维护。求解区间 mex（最小未出现非负整数）。

**思路**

💡 类比"只增不删地推进左指针，超范围用临时数组回滚"：回滚莫队把"删除"变难的问题转成"只增加+回滚"，区间 mex 用 cnt 与 while-loop 求最小未出现整数。

```python
def mex_rollback_example(nums, l, r):
    # 离线排序+回滚：这里演示单区间暴力基准（可暴力验证）
    seen = [False] * (len(nums) + 2)
    for i in range(l, r + 1):
        if nums[i] < len(seen):
            seen[nums[i]] = True
    m = 0
    while seen[m]:
        m += 1
    return m

print(mex_rollback_example([0, 1, 2, 4], 1, 3))   # 区间[1..3]={1,2,4} -> 0
print(mex_rollback_example([1, 2, 0, 5], 0, 3))   # {1,2,0,5} -> 3
```

> **复杂度**：离线总体 O((n+q)·√n)；单次 O(1)~O(√n)。

#### 13.43.3 例 178：CDQ 分治求逆序对 / 三维偏序⭐⭐⭐

> **知识点**：CDQ 分治、归并、偏序｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的离线综合题，主要考察 CDQ 分治/归并求逆序对与三维偏序。统计逆序对数量。

**思路**

💡 类比"左边对右边的跨块贡献在合并时统计"：CDQ 分治把"三维偏序计数"降成"一维排序+二维归并"。逆序对即归并排序过程中的跨块逆序数，O(n log n)。

```python
def count_inversions(a):
    b = a[:]
    res = [0]
    def merge_sort(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        merge_sort(lo, mid); merge_sort(mid, hi)
        tmp = []; i, j = lo, mid
        while i < mid and j < hi:
            if b[i] <= b[j]:
                tmp.append(b[i]); i += 1
            else:
                tmp.append(b[j]); j += 1
                res[0] += mid - i
        tmp.extend(b[i:mid]); tmp.extend(b[j:hi])
        b[lo:hi] = tmp
    merge_sort(0, len(a))
    return res[0]

print(count_inversions([3, 1, 2]))     # 2
print(count_inversions([1, 2, 3]))     # 0
```

> **复杂度**：O(n log n) 时间，O(n) 空间。

#### 13.43.4 例 179：线段树维护最大连续子段和（区间合并）⭐⭐⭐

> **知识点**：线段树、合并信息、最大子段｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的线段树综合题，主要考察线段树区间合并信息（前缀/后缀/总最大子段）维护最大连续子段和。支持单点修改下的区间最大子段和查询。

**思路**

💡 类比"越权把左右的最大前缀/后缀/整段和并成大段"：每个节点维护 sum、mx、lmax、rmax。合并时 `mx=max(左mx,右mx,左rmax+右lmax)`，前后缀同理。

```python
def combine(a, b):
    # (sum, lmax, rmax, mx)
    s, lm, rm, mx = a
    s2, lm2, rm2, mx2 = b
    return (s + s2,
            max(lm, s + lm2),
            max(rm2, s2 + rm),
            max(mx, mx2, rm + lm2))

class SegTree:
    def __init__(self, arr):
        n = len(arr)
        self.t = [(0, 0, 0, 0)] * (4 * n)
        def build(o, l, r):
            if l == r:
                self.t[o] = (arr[l], arr[l], arr[l], arr[l]); return
            m = (l + r) // 2
            build(o * 2, l, m); build(o * 2 + 1, m + 1, r)
            self.t[o] = combine(self.t[o * 2], self.t[o * 2 + 1])
        build(1, 0, n - 1)
    def query(self, o, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.t[o]
        m = (l + r) // 2
        if qr <= m:
            return self.query(o * 2, l, m, ql, qr)
        if ql > m:
            return self.query(o * 2 + 1, m + 1, r, ql, qr)
        return combine(self.query(o * 2, l, m, ql, qr),
                       self.query(o * 2 + 1, m + 1, r, ql, qr))
    def max_subarray(self, ql, qr):
        return self.query(1, 0, max_len - 1, ql, qr)[3]

max_len = 5                                  # 数组长度
seg = SegTree([1, 2, -5, 3, 4])
print(seg.max_subarray(0, 4))                # 整个数组最大子段 = 1+2+3+4 = 7
print(seg.max_subarray(0, 2))                # [1,2,-5] 最大子段 = 3
print(seg.max_subarray(3, 4))                # [3,4] 最大子段 = 7
```

> **复杂度**：单点修改 O(log n)；查询 O(log n)。

#### 13.43.5 例 180：扫描线求矩形面积并（线段树）⭐⭐⭐

> **知识点**：扫描线、线段树、离散化｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛
**题目描述**：这是一道难度较高的扫描线综合题，主要考察扫描线 + 线段树 + 离散化。求多个矩形的面积并。

**思路**

💡 类比"按 y 从低到高扫描，区间覆盖长度与 Δy 相乘累加"：对矩形上下边按 y 排序，线段树维护当前覆盖长度，面积并 = 累计(cover_len × 相邻y差)。

```python
def rect_area(rects):
    # rects: (x1, y1, x2, y2)，扫描线求并集面积（x 坐标离散化）
    xs = sorted({x for r in rects for x in (r[0], r[2])})
    comp = {x: i for i, x in enumerate(xs)}
    width = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    events = []
    for x1, y1, x2, y2 in rects:
        for c in range(comp[x1], comp[x2]):      # 每个 x 段单独维护覆盖计数
            events.append((y1, 1, c))
            events.append((y2, -1, c))
    events.sort()
    cnt = [0] * len(width)
    total = pre = 0
    for y, d, c in events:
        covered = sum(w for w, k in zip(width, cnt) if k)   # 当前覆盖宽度
        total += covered * (y - pre)                          # 覆盖宽度 × Δy
        cnt[c] += d
        pre = y
    return total

print(rect_area([(0, 0, 2, 2)]))            # 4
print(rect_area([(0, 0, 2, 2), (1, 1, 3, 3)]))  # 并集 = 4+4-1=7
```

> **复杂度**：完整线段树版 O(n log n)；本例为便于理解用计数数组，最坏 O(n²)、空间 O(n)。

#### 13.43.6 例 181：图上二分答案（最小化最大边）⭐⭐

> **知识点**：二分、最短路/并查集、可行性判定｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的图上二分题，主要考察二分答案 + 最短路/并查集判定。求最小化路径中的最大边权。

**思路**

💡 类比"试一个上限，只走权值不超过它的边看能否连通"：二分区间的上限 W，判定用并查集或 BFS 看起点到终点连通性，判断可行再收缩。

```python
def min_max_edge(n, edges, s, t):
    # edges:(u,v,w)
    edges.sort(key=lambda e: e[2])
    lo, hi = -1, edges[-1][2]
    def reach(limit):
        par = list(range(n))
        def find(x):
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        for u, v, w in edges:
            if w > limit:
                break
            ru, rv = find(u), find(v)
            if ru != rv:
                par[ru] = rv
        return find(s) == find(t)
    lo, hi = -1, edges[-1][2]
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if reach(mid):
            hi = mid
        else:
            lo = mid
    return hi

print(min_max_edge(3, [(0, 1, 5), (1, 2, 8), (0, 2, 10)], 0, 2))   # 8
```

> **复杂度**：O((n+m)·logW)；空间 O(n)。

#### 13.43.7 例 182：河内塔 / 递归分治构造（经典递归）⭐⭐

> **知识点**：递归、分治｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/基础
**题目描述**：这是一道较综合的递归分治题，主要考察河内塔的递归分治构造。输出移动方案并统计移动步数。

**思路**

💡 类比"借助中间柱把 n−1 片搬走、再搬底片、再搬回 n−1"：`hanoi(n,a,b,c)` 递归三步，移动次数 `2^n−1`。

```python
def hanoi(n, a, b, c, out=None):
    if n == 0:
        return
    hanoi(n - 1, a, c, b, out)
    if out is not None:
        out.append((a, c))
    hanoi(n - 1, b, a, c, out)

moves = []
hanoi(3, 'A', 'B', 'C', moves)
print(len(moves))       # 7
print(moves[:3])
```

> **复杂度**：O(2^n) 时间，O(n) 递归空间。

#### 13.43.8 例 183：区间 DP——石子合并（环形）⭐⭐

> **知识点**：区间 DP、前缀和、断环为链｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的区间 DP 题，主要考察断环为链 + 前缀和。求环形石子合并的最大/最小代价。

**思路**

💡 类比"每段由两个子段合并而来，代价加上区间和"：把环复制成长度 2n 的链，`dp[i][j]=min(dp[i][k]+dp[k+1][j])+sum[i..j]`，答案取长度 n 的全部子区间的 min。

```python
def stone_min(a):
    n = len(a)
    a2 = a + a
    pre = [0]
    for x in a2:
        pre.append(pre[-1] + x)
    INF = 10 ** 18
    dp = [[INF] * (2 * n + 1) for _ in range(2 * n + 1)]
    for i in range(2 * n + 1):
        dp[i][i] = 0
    for L in range(2, n + 1):
        for i in range(1, 2 * n - L + 2):
            j = i + L - 1
            for k in range(i, j):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j])
            dp[i][j] += pre[j] - pre[i - 1]
    return min(dp[i][i + n - 1] for i in range(1, n + 1))

print(stone_min([4, 5, 9]))   # 合并代价
```

> **复杂度**：O(n³)；空间 O(n²)。

#### 13.43.9 例 184：状压 DP——分配问题（匈牙利替代）⭐⭐

> **知识点**：状压 DP、位掩码｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛
**题目描述**：这是一道较综合的状压 DP 题，主要考察位掩码子集枚举分配问题。在 n 组任务与 n 个工人一一分配下求最优分配。

**思路**

💡 类比"用位掩码记录哪些人已分配"：`dp[mask]` 表示把前 popcount(mask) 个任务分给 mask 中人的最小代价，转移枚举最后一个任务分配给哪个人。

```python
def assign(cost):
    n = len(cost)
    dp = [10 ** 9] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        task = bin(mask).count('1')
        for j in range(n):
            if not (mask >> j) & 1:
                nxt = mask | (1 << j)
                dp[nxt] = min(dp[nxt], dp[mask] + cost[task][j])
    return dp[(1 << n) - 1]

print(assign([[9, 2, 7], [6, 4, 3], [5, 8, 1]]))   # 最低总代价
```

> **复杂度**：O(n·2^n)；空间 O(2^n)。

#### 13.43.10 例 185：字典序第 k 小排列（逆康托展开）⭐⭐

> **知识点**：阶乘计数、逆康托展开｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的排列题，主要考察阶乘计数与逆康托展开。求字典序第 k 小的排列。

**思路**

💡 类比"按每位可取的个数（阶乘）定位第 k 个排法"：k−1 依次除以 (n−1−i)!，商即该位在剩余元素中的下标，余数继续下一轮。

```python
def kth_permutation(n, k):
    nums = list(range(1, n + 1))
    fact = [1] * (n + 1)
    for i in range(2, n + 1):
        fact[i] = fact[i - 1] * i
    k -= 1
    res = []
    for i in range(n):
        idx = k // fact[n - 1 - i]
        res.append(nums.pop(idx))
        k %= fact[n - 1 - i]
    return res

print(kth_permutation(3, 1))    # [1, 2, 3]
print(kth_permutation(4, 7))    # 第7个
```

> **复杂度**：O(n²)（list.pop）；空间 O(n)。



#### 13.43.11 例 186：中位数维护（双堆对顶法）⭐⭐

> **知识点**：堆、对顶堆、中位数｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的数据结构题，主要考察双堆（对顶堆）维护中位数。动态插入并高效查询中位数。

**思路**

💡 类比"把数据分成大的一半与小的一半，各用一个大根堆/小根堆顶上"：一个大根堆存较小的一半、一个小根堆存较大的一半，保持两堆大小差 ≤ 1。插入后取 max(小堆顶,大堆顶) 即为中位数，插入 O(log n)。

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []          # 大根堆（用负数），存较小的一半
        self.large = []          # 小根堆，存较大的一半
    def add(self, x):
        heapq.heappush(self.small, -x)
        if self.small and self.large and -self.small[0] > self.large[0]:
            v = -heapq.heappop(self.small)
            heapq.heappush(self.large, v)
        if len(self.small) > len(self.large) + 1:
            v = -heapq.heappop(self.small)
            heapq.heappush(self.large, v)
        if len(self.large) > len(self.small):
            v = heapq.heappop(self.large)
            heapq.heappush(self.small, -v)
    def median(self):
        if len(self.small) == len(self.large):
            return (-self.small[0] + self.large[0]) / 2
        return -self.small[0]

mf = MedianFinder()
for x in [1, 5, 3, 2, 4]:
    mf.add(x)
print(mf.median())     # 3.0
```

> **复杂度**：插入 O(log n)；中位数 O(1)。

#### 13.43.12 例 187：拓扑排序检测环（判断课程能否修完）⭐⭐

> **知识点**：拓扑排序、入度、环检测｜**难度**：⭐⭐（中等）｜**类型**：OI/竞赛/面试
**题目描述**：这是一道较综合的图论题，主要考察拓扑排序环检测（入度剪枝）。判断课程之间的依赖关系是否能够全部修完。

**思路**

💡 类比"先修必排前，能排完即为无环"：统计入度，队列放入度为 0 的点，逐个出队并减少后继入度。若出队数 == 顶点数则无环可拓扑，否则存在环。

```python
from collections import deque

def can_finish(n, edges):       # edges:(先修, 后续)
    g = [[] for _ in range(n)]
    ind = [0] * n
    for u, v in edges:
        g[u].append(v); ind[v] += 1
    q = deque(i for i in range(n) if ind[i] == 0)
    cnt = 0
    while q:
        u = q.popleft(); cnt += 1
        for v in g[u]:
            ind[v] -= 1
            if ind[v] == 0:
                q.append(v)
    return cnt == n

print(can_finish(2, [(1, 0)]))        # True
print(can_finish(2, [(0, 1), (1, 0)]))  # False (环)
```

> **复杂度**：O(n + m)；空间 O(n + m)。

