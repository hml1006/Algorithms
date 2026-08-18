# 第十层 OI/ACM 竞赛：OI 极难综合题库

## 13. OI 极难综合题库

本部分是第 12 章「OI/ACM 竞赛高级专题」的配套综合练习，覆盖 LCT、树链剖分、可持久化线段树（主席树）、莫队、珂朵莉树、舞蹈链/精确覆盖、差分约束、线性基、生成函数/多项式（FFT/NTT）、杜教筛/Min_25 筛、回文自动机、后缀自动机（SAM）等高级数据结构与算法，共 10 道代表性竞赛题，按难度从低到高排列，多为 ⭐⭐⭐（困难）级别。

---

### 13.1 数据结构进阶（树链剖分 · 主席树 · LCT）

#### 13.1.1 例 1：「模板」树链剖分 / 树上路径加与路径和（树链剖分 + 线段树）⭐⭐⭐

> **知识点**：树链剖分 + 线段树｜**难度**：⭐⭐⭐（困难）｜**类型**：OI/竞赛

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
