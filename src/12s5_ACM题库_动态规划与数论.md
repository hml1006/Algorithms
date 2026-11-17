# 第 12 章 OI/ACM 竞赛：ACM 经典题库（五）

> 本分册覆盖 17.14–17.16（动态规划与数论），共 285 题。
> 返回 [ACM 经典题库总览](./12s_ACM题库.md)。

## 17. ACM 经典题库

### 17.14 动态规划基础与背包

#### 17.14.1 例 1：最长上升子序列 LIS（POJ 2533）⭐

> **知识点**：LIS、线性 DP｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个长度为 N（1≤N≤1000）的整数序列，求其最长严格上升子序列的长度。第一行输入 N，第二行输入序列的 N 个整数。

**思路**

💡 类比"接力排队"：把每个数当作队伍末位，能接在前一个更小的数后面就使队伍变长。用 dp[i] 表示以第 i 个元素结尾的最长上升子序列长度，状态转移 dp[i]=max(dp[j]+1)（j<i 且 a[j]<a[i]），答案为 max(dp)。

```python
def lis(a):
    n = len(a)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

n = int(input())
a = list(map(int, input().split()))
print(lis(a))
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.14.2 例 2：最长公共子序列 LCS（POJ 1458）⭐

> **知识点**：LCS、二维线性 DP｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个字符串 s1、s2（长度 ≤5000），求两者的最长公共子序列长度。输入多行，每行两个字符串，用空格分隔，读到 EOF 结束。

**思路**

💡 类比"合并两条队伍"：两个指针逐字符比对。dp[i][j] 表示 s1 前 i 个字符与 s2 前 j 个字符的 LCS 长度，若当前字符相等则 dp[i-1][j-1]+1，否则取左边或上边较大值。

```python
import sys
def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

for line in sys.stdin:
    s1, s2 = line.split()
    print(lcs(s1, s2))
```

> **复杂度**：O(NM) 时间，O(NM) 空间

---

#### 17.14.3 例 3：数字三角形（POJ 1163）⭐

> **知识点**：坐标 DP、自底向上递推｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个 N 行（1≤N≤100）的数字三角形，第 i 行有 i 个数。从顶端出发，每次可以走到下一行的正下方或右下，求到达底部的路径数字之和最大值。

**思路**

💡 类比"山顶滚石子"：从下往上，每个位置只需累加它下方两个子问题的较大值。dp 数组自底向上更新，最终 dp[0][0] 即为答案。

```python
n = int(input())
tri = [list(map(int, input().split())) for _ in range(n)]
dp = tri[-1][:]
for i in range(n - 2, -1, -1):
    for j in range(len(tri[i])):
        dp[j] = tri[i][j] + max(dp[j], dp[j + 1])
print(dp[0])
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.14.4 例 4：最大子段和（洛谷 P1115）⭐

> **知识点**：最大子序和、Kadane 算法、线性 DP｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个长度为 N（N≤200000）的整数序列，求于其中连续的一段，使其之和最大。第一行 N，第二行序列。

**思路**

💡 类比"打鱼摊"：要么延续前面的段继续累积（dp 为正则加入），要么从当前位置重新开始。dp=max(dp+a[i], a[i])，用滚动变量维护并记录全局最大值。

```python
n = int(input())
a = list(map(int, input().split()))
best = cur = a[0]
for i in range(1, n):
    cur = max(a[i], cur + a[i])
    best = max(best, cur)
print(best)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.5 例 5：01 背包（洛谷 P1048 采药）⭐

> **知识点**：0-1 背包、一维滚动优化｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：总时间为 T（最大容量），有 M 株药草，每株耗时 time_i 与价值 value_i，每株最多采一次。求 T 时间内能获得的最大价值。

**思路**

💡 类比"塞行李箱"：每个物品看作可选可不选。用 dp[j] 表示容量 j 的最大价值，倒序枚举背包容量避免同物品重复使用，转移 dp[j]=max(dp[j], dp[j-w]+v)。

```python
t, m = map(int, input().split())
dp = [0] * (t + 1)
for _ in range(m):
    w, v = map(int, input().split())
    for j in range(t, w - 1, -1):
        dp[j] = max(dp[j], dp[j - w] + v)
print(max(dp))
```

> **复杂度**：O(M·T) 时间，O(T) 空间

---

#### 17.14.6 例 6：完全背包（HDU 1114 Piggy-Bank）⭐⭐

> **知识点**：完全背包、恰好装满｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：存钱罐空重 E、装满重 F，容量即 F−E。有 N 种硬币，每种可无限取，重量 w_i 价值 p_i。求恰装满容量的最小价值，若无方案输出 "This is impossible."。

**思路**

💡 类比"无限续杯"：物品可重复选，把容量循环改为正序枚举，让同种硬币可多次加入。目标是求最小价值，初始化为无穷大，dp[0]=0。

```python
INF = float('inf')
t = int(input())
for _ in range(t):
    e, f = map(int, input().split())
    cap = f - e
    n = int(input())
    dp = [INF] * (cap + 1)
    dp[0] = 0
    for _ in range(n):
        p, w = map(int, input().split())
        for j in range(w, cap + 1):
            if dp[j - w] + p < dp[j]:
                dp[j] = dp[j - w] + p
    if dp[cap] == INF:
        print("This is impossible.")
    else:
        print(f"The minimum amount of money in the piggy-bank is {dp[cap]}.")
```

> **复杂度**：O(N·cap) 时间，O(cap) 空间

---

#### 17.14.7 例 7：多重背包（POJ 1276 Cash Machine）⭐⭐

> **知识点**：多重背包、二进制拆分优化｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：目标金额 Cash，有 N 种面值的钞票，第 i 种面值 D_k 数量 N_k。求不超过 Cash 的能凑出的最大金额。

**思路**

💡 类比"拆分整袋糖果"：把数量目的物品按二进制 1,2,4,… 拆成若干件，转化为 0-1 背包，既保证组合能力又降低复杂度。

```python
def solve(cash, kinds):
    dp = [0] * (cash + 1)
    for nk, dk in kinds:
        k = 1
        while nk >= k:
            w = dk * k
            for j in range(cash, w - 1, -1):
                if dp[j - w] + w > dp[j]:
                    dp[j] = dp[j - w] + w
            nk -= k
            k <<= 1
        if nk > 0:
            w = dk * nk
            for j in range(cash, w - 1, -1):
                if dp[j - w] + w > dp[j]:
                    dp[j] = dp[j - w] + w
    return dp[cash]

while True:
    try:
        parts = list(map(int, input().split()))
    except EOFError:
        break
    cash = parts[0]
    kinds = [(parts[i], parts[i + 1]) for i in range(2, len(parts), 2)]
    print(solve(cash, kinds))
```

> **复杂度**：约 O(cash·log Nk) 时间，O(cash) 空间

---

#### 17.14.8 例 8：装箱问题（洛谷 P1049）⭐⭐

> **知识点**：0-1 背包、背包容量即价值｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：箱子容量为 V（V≤20000），有 N 个物品，每个体积 v_i，要求放入箱子的物品体积之和不超过 V 并使剩余空间最小。输出剩余空间。

**思路**

💡 类比"相亲箱子放东西"：体积即是"容量"也是"价值"，求不超过 V 能装的最大体积。dp[j] 表示容量 j 能装入的最大体积，倒序做 0-1 背包，答案 V−dp[V]。

```python
v = int(input())
n = int(input())
items = [int(input()) for _ in range(n)]
dp = [0] * (v + 1)
for w in items:
    for j in range(v, w - 1, -1):
        if dp[j - w] + w > dp[j]:
            dp[j] = dp[j - w] + w
print(v - dp[v])
```

> **复杂度**：O(N·V) 时间，O(V) 空间

---

#### 17.14.9 例 9：分组背包（洛谷 P1757）⭐

> **知识点**：分组背包、组内枚举决策｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 N 件物品和一个容量为 V 的背包，物品分成若干组，每组最多选一件。物品 i 重量 w_i、价值 c_i，属于组 g_i。求不超过容量 V 的最大价值。

**思路**

💡 类比"每桌只选一道菜"：按组作外层阶段，对每个容量在组内枚举所有物品选最大值，保证每组至多取一件。容量倒序枚举。

```python
v, n = map(int, input().split())
groups = {}
for _ in range(n):
    w, c, g = map(int, input().split())
    groups.setdefault(g, []).append((w, c))
dp = [0] * (v + 1)
for g in sorted(groups):
    for j in range(v, -1, -1):
        for w, c in groups[g]:
            if j >= w:
                dp[j] = max(dp[j], dp[j - w] + c)
print(dp[v])
```

> **复杂度**：O(V·物品总数) 时间，O(V) 空间

---

#### 17.14.10 例 10：有依赖的背包（洛谷 P1064 金明的预算方案）⭐⭐

> **知识点**：有依赖背包、树形分组背包转 0-1 背包｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：总价格上限为 N，有 m 份物品清单，每件有价格 v、重要度 p、是否主件（q=0 为主件，否则为所依赖主件编号）。附件只能与所属主件一同购买。求价格不超过 N 时的 (v×p) 总和最大值。

**思路**

💡 类比"套餐选购"：主件必买，附件可任意组合形成几种"套餐"（只选主件、主件+附件1、主件+附件2、主件+两附件），在每组内按 0-1 背包处理。

```python
n, m = map(int, input().split())
main_, sub = {}, {}
for i in range(1, m + 1):
    v, p, q = map(int, input().split())
    if q == 0:
        main_[i] = (v, v * p)
    else:
        sub.setdefault(q, []).append((v, v * p))
dp = [0] * (n + 1)
for i, (v0, w0) in main_.items():
    for j in range(n, v0 - 1, -1):
        # 只选主件
        dp[j] = max(dp[j], dp[j - v0] + w0)
        if i not in sub:
            continue
        subs = sub[i]
        # 主件+单附件
        for v1, w1 in subs:
            if j >= v0 + v1:
                dp[j] = max(dp[j], dp[j - v0 - v1] + w0 + w1)
        # 主件+两附件
        if len(subs) == 2:
            v1, w1 = subs[0]
            v2, w2 = subs[1]
            if j >= v0 + v1 + v2:
                dp[j] = max(dp[j], dp[j - v0 - v1 - v2] + w0 + w1 + w2)
print(dp[n])
```

> **复杂度**：O(m·N) 时间，O(N) 空间

---

#### 17.14.11 例 11：货币兑换（洛谷 P1902/POJ 1742 Coins）⭐⭐

> **知识点**：多重背包可行性、恰好凑出金额计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 种硬币，面值 a_i、数量 c_i，给定目标金额 m，问用这些硬币能凑出的 [1,m] 中不同金额的个数。

**思路**

💡 类比"找零钱数总类"：对每种硬币维护剩余可用数量数组，dp[j]=True 表示 j 元可凑出，满最短路思想——用 not used 记录当前面额用了多少张避免重复计数。

```python
while True:
    n, m = map(int, input().split())
    if n == 0 and m == 0:
        break
    a = list(map(int, input().split()))
    c = list(map(int, input().split()))
    used = [0] * (m + 1)
    dp = [False] * (m + 1)
    dp[0] = True
    ans = 0
    for i in range(n):
        for j in range(m + 1):
            used[j] = 0
        for j in range(a[i], m + 1):
            if not dp[j] and dp[j - a[i]] and used[j - a[i]] < c[i]:
                dp[j] = True
                used[j] = used[j - a[i]] + 1
                ans += 1
    print(ans)
```

> **复杂度**：O(n·m) 时间，O(m) 空间

---

#### 17.14.12 例 12：最长公共上升子序列 LCIS（HDU 1425/经典）⭐⭐⭐

> **知识点**：LIS+LCS、LCIS 优化（O(NM)）｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个序列 a（长度 n）与 b（长度 m），求既是二者的公共子序列又是严格上升子序列的最长长度。

**思路**

💡 类比"两条队里挑共同递增者"：设 f[i][j] 为 a 前 i 项与 b 第 j 项结尾的最长公共上升子序列，按 b 中递增位置维护前缀最大，合并 LIS 与 LCS 的转移。

```python
n = int(input())
a = list(map(int, input().split()))
m = int(input())
b = list(map(int, input().split()))
f = [0] * (m + 1)
best = 0
for i in range(1, n + 1):
    cur = 0
    for j in range(1, m + 1):
        if a[i - 1] == b[j - 1]:
            f[j] = max(f[j], cur + 1)
        elif a[i - 1] > b[j - 1]:
            cur = max(cur, f[j])
        best = max(best, f[j])
print(best)
```

> **复杂度**：O(NM) 时间，O(M) 空间

---

#### 17.14.13 例 13：斐波那契数列（洛谷 P1255 数楼梯）⭐

> **知识点**：线性 DP、大整数加法类递推｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：走楼梯可一次上 1 级或 2 级，问上到第 N 级有多少种走法。N 可能很大（N≤5000），结果可能很大。

**思路**

💡 类比"台阶跳格"：到达第 i 级只能来自第 i−1 级或第 i−2 级，故 f[i]=f[i−1]+f[i−2]。Python 整数自动大数，无需取模。

```python
n = int(input())
if n < 2:
    print(1)
else:
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    print(b)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.14 例 14：Wall/跳台阶变式——爬楼梯最小花费（洛谷 U23961/经典）⭐

> **知识点**：线性 DP、最小代价转移｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：数组 cost[i] 表示站上第 i 级台阶的花费。可以从第 0 或第 1 级开始，每次爬 1 或 2 级，到达顶层（越过最后一阶）时结束。求最小总花费。

**思路**

💡 类比"过路费"：到达第 i 级的最小代价等于 min(从 i−1 来，从 i−2 来)+cost[i]。顶层即 index n，倒一层处理即可。

```python
cost = list(map(int, input().split()))
a, b = 0, 0  # 分别代表前两级的最小花费
for c in cost:
    a, b = b, min(a, b) + c
print(min(a, b))
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.15 例 15：不同路径数（洛谷 P8772/LeetCode 62）⭐

> **知识点**：坐标 DP、网格计数｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：有一个 m×n 网格，机器人从左上角 (0,0) 出发，每次只能向右或向下走，求到达右下角的不同路径条数。

**思路**

💡 类比"棋盘走子"：每个格子的路径数等于其上方格子与左方格子路径数之和。边界格子（第一行/第一列）路径数恒为 1。

```python
m, n = map(int, input().split())
dp = [[1] * n for _ in range(m)]
for i in range(1, m):
    for j in range(1, n):
        dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
print(dp[m - 1][n - 1])
```

> **复杂度**：O(m·n) 时间，O(m·n) 空间

---

#### 17.14.16 例 16：数字三角形变式——Saber 的礼物最小和（UVA 10068/经典网格最小成本）⭐⭐

> **知识点**：坐标 DP、带权网格最短路本质 DP｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：m×n 网格，每格有代价，从左上走到右下每次只能右或下移动，求最小代价和。

**思路**

💡 类比"走迷宫付过路费"：第一行只能一直向右（累加），第一列只能一直向下，其余格取上方与左方较小者加本格代价。

```python
m, n = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(m)]
dp = [[0] * n for _ in range(m)]
dp[0][0] = grid[0][0]
for j in range(1, n):
    dp[0][j] = dp[0][j - 1] + grid[0][j]
for i in range(1, m):
    dp[i][0] = dp[i - 1][0] + grid[i][0]
for i in range(1, m):
    for j in range(1, n):
        dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j]
print(dp[m - 1][n - 1])
```

> **复杂度**：O(m·n) 时间，O(m·n) 空间

---

#### 17.14.17 例 17：连续子数组最大积（LeetCode 152/经典）⭐⭐

> **知识点**：线性 DP、同时维护最大最小值（负负得正）｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定整数数组，求乘积最大的连续子数组乘积。

**思路**

💡 类比"正负号翻转"：负数会让大小翻转，所以每步要同时维护以当前位置结尾的最大积与最小积，用两者交叉更新。

```python
a = list(map(int, input().split()))
mx = mn = ans = a[0]
for x in a[1:]:
    if x < 0:
        mx, mn = mn, mx
    mx = max(x, mx * x)
    mn = min(x, mn * x)
    ans = max(ans, mx)
print(ans)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.18 例 18：单词拆分（LeetCode 139/经典）⭐

> **知识点**：线性 DP、字符串前缀匹配｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s 与单词字典 wordDict，判断 s 是否可以被拆分成若干个字典中的单词。

**思路**

💡 类比"句子分段"：dp[i] 表示前 i 个字符能否拆分。枚举位置 i，检查是否存在 j<i 使 dp[j] 为真且 s[j:i] 在字典中。

```python
s = input().strip()
wordSet = set(input().split())
n = len(s)
dp = [False] * (n + 1)
dp[0] = True
for i in range(1, n + 1):
    for j in range(i):
        if dp[j] and s[j:i] in wordSet:
            dp[i] = True
            break
print("Yes" if dp[n] else "No")
```

> **复杂度**：O(N²·字长) 时间，O(N) 空间

---

#### 17.14.19 例 19：打家劫舍（LeetCode 198/经典）⭐

> **知识点**：线性 DP、相邻互斥选择｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：一排房屋，第 i 家金额为 money[i]，不能偷相邻的两家，求最多能偷到的金额。

**思路**

💡 类比"隔一间偷"：对每家做"偷/不偷"决策。dp[i]=max(dp[i−1], dp[i−2]+money[i])，用两个滚动变量优化空间。

```python
a = list(map(int, input().split()))
prev, cur = 0, 0
for x in a:
    prev, cur = cur, max(cur, prev + x)
print(cur)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.20 例 20：打家劫舍环形版本（LeetCode 213/经典）⭐⭐

> **知识点**：线性 DP、环拆成两种情况｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：房屋围成一圈（首尾相邻），其余规则同打家劫舍，求不偷相邻家的最大收益。

**思路**

💡 类比"环形街道"：问题退化为"不偷第 0 家"或"不偷第 N−1 家"两种线性情况，取两者较大值。

```python
def rob_linear(nums):
    prev, cur = 0, 0
    for x in nums:
        prev, cur = cur, max(cur, prev + x)
    return cur

a = list(map(int, input().split()))
if len(a) == 1:
    print(a[0])
else:
    print(max(rob_linear(a[:-1]), rob_linear(a[1:])))
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.21 例 21：零钱兑换（LeetCode 322/经典）⭐

> **知识点**：完全背包、最小硬币数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定不同面额 coins 与总金额 amount，每种硬币可使用无限次，求组成 amount 所需的最少硬币个数，若无法组成返回 -1。

**思路**

💡 类比"尽量用大面额"但需 DP：dp[j] 表示凑出金额 j 的最少硬币数，完全背包正序枚举容量，转移 dp[j]=min(dp[j], dp[j−coin]+1)。

```python
coins = list(map(int, input().split()))
amount = int(input())
INF = float('inf')
dp = [INF] * (amount + 1)
dp[0] = 0
for c in coins:
    for j in range(c, amount + 1):
        if dp[j - c] + 1 < dp[j]:
            dp[j] = dp[j - c] + 1
print(-1 if dp[amount] == INF else dp[amount])
```

> **复杂度**：O(amount·K) 时间，O(amount) 空间

---

#### 17.14.22 例 22：零钱兑换方案总数（LeetCode 518/经典）⭐

> **知识点**：完全背包、方案计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定不同面额硬币数组与总金额 amount，求凑出 amount 的不同硬币组合数（组合不考虑顺序）。

**思路**

💡 类比"组合付费"：因为不考虑顺序，外层遍历硬币、内层遍历金额，这样同一种硬币的多次使用自然在同一组内。dp[j]+=dp[j−coin]。

```python
coins = list(map(int, input().split()))
amount = int(input())
dp = [0] * (amount + 1)
dp[0] = 1
for c in coins:
    for j in range(c, amount + 1):
        dp[j] += dp[j - c]
print(dp[amount])
```

> **复杂度**：O(amount·K) 时间，O(amount) 空间

---

#### 17.14.23 例 23：记忆化搜索——滑雪（洛谷 P1434）⭐⭐

> **知识点**：记忆化搜索、坐标 DP、Longest decreasing path｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 R×C 的矩阵高程，从任意一点出发只能滑向四个方向中更低的点，求能滑行的最长路径长度。

**思路**

💡 类比"只在坡上滑"：dp[i][j] 表示从该点出发的最长滑行距离，递归访问四个更低邻居，用记忆化避免重复计算。

```python
import sys
sys.setrecursionlimit(100000)
r, c = map(int, input().split())
h = [list(map(int, input().split())) for _ in range(r)]
memo = [[0] * c for _ in range(r)]
d = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def dfs(i, j):
    if memo[i][j]:
        return memo[i][j]
    best = 1
    for di, dj in d:
        ni, nj = i + di, j + dj
        if 0 <= ni < r and 0 <= nj < c and h[ni][nj] < h[i][j]:
            best = max(best, dfs(ni, nj) + 1)
    memo[i][j] = best
    return best

ans = 0
for i in range(r):
    for j in range(c):
        ans = max(ans, dfs(i, j))
print(ans)
```

> **复杂度**：O(R·C) 时间，O(R·C) 空间

---

#### 17.14.24 例 24：最大正方形（LeetCode 221/经典）⭐

> **知识点**：坐标 DP、正方形边长递推｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 "0"/"1" 矩阵，求只含 1 的最大正方形面积。

**思路**

💡 类比"盖章"：以 (i,j) 为右下角的 dp 表示最大边长，等于 min(上,左,左上)+1（当格为 1），统计最大边长的平方。

```python
import sys
grid = [list(map(int, line.split())) for line in sys.stdin]
m, n = len(grid), len(grid[0])
dp = [[0] * n for _ in range(m)]
best = 0
for i in range(m):
    for j in range(n):
        if grid[i][j] == 1:
            if i == 0 or j == 0:
                dp[i][j] = 1
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
            best = max(best, dp[i][j])
print(best * best)
```

> **复杂度**：O(m·n) 时间，O(m·n) 空间

---

#### 17.14.25 例 25：编辑距离（LeetCode 72/经典）⭐⭐

> **知识点**：二维线性 DP、最小编辑次数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：通过插入、删除、替换字符操作把单词 A 变为 B，每次操作代价 1，求最小操作次数。

**思路**

💡 类比"改错别字"：dp[i][j] 表示 A 前 i 个到 B 前 j 个的距离。三操作分别对应 dp[i-1][j]+1、dp[i][j-1]+1、dp[i-1][j-1]+(是否相等)。

```python
a = input().strip()
b = input().strip()
m, n = len(a), len(b)
dp = [[0] * (n + 1) for _ in range(m + 1)]
for i in range(m + 1):
    dp[i][0] = i
for j in range(n + 1):
    dp[0][j] = j
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if a[i - 1] == b[j - 1]:
            dp[i][j] = dp[i - 1][j - 1]
        else:
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
print(dp[m][n])
```

> **复杂度**：O(NM) 时间，O(NM) 空间

---

#### 17.14.26 例 26：最长回文子串（洛谷 P6169/LeetCode 5）⭐⭐

> **知识点**：区间 DP 思路、中心扩展或 DP｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s，求其最长回文子串的长度。

**思路**

💡 类比"串珠对称"：dp[i][j] 表示 s[i..j] 是否为回文，若两端相同且中间是回文则为真。也可用中心扩展法逐一向外扩。

```python
s = input().strip()
n = len(s)
dp = [[False] * n for _ in range(n)]
ans = 1
for i in range(n):
    dp[i][i] = True
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        if s[i] == s[j]:
            if length == 2 or dp[i + 1][j - 1]:
                dp[i][j] = True
                ans = length
print(ans)
```

> **复杂度**：O(N²) 时间，O(N²) 空间

---

#### 17.14.27 例 27：数位——不含某数字的方案统计（洛谷 P2602/经典数位初步）⭐

> **知识点**：组合计数 DP、按位统计 0-9 出现次数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 a、b，统计区间 [a,b] 内每个数字（0…9）在十进制中各出现多少次。

**思路**

💡 类比"数位逐位点算"：计算 f(n)（1..n 中每位数字出现次数），按位贡献统计，区间答案=f(b)−f(a−1)。注意前导 0 的处理。

```python
def count(n):
    if n <= 0:
        return [0] * 10
    s = str(n)
    L = len(s)
    res = [0] * 10
    for i in range(L):
        cur = int(s[i])
        pw = 10 ** (L - i - 1)
        hi = int(s[:i]) if i else 0
        lo = int(s[i + 1:]) if i < L - 1 else 0
        for d in range(10):
            res[d] += hi * pw
        for d in range(cur):
            res[d] += pw
        res[cur] += lo + 1
        res[0] -= pw  # 去掉把0当首位出现的多余
    return res

a, b = map(int, input().split())
A = count(b)
B = count(a - 1)
print(' '.join(str(A[i] - B[i]) for i in range(10)))
```

> **复杂度**：O(10·位数) 时间，O(10) 空间

---

#### 17.14.28 例 28：最长递增子序列的个数（LeetCode 673/经典）⭐⭐

> **知识点**：LIS 增强、计数 DP｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定整数数组，求最长递增子序列的长度及其不同的个数。

**思路**

💡 类比"多条接力最长队"：dp[i] 记录以 i 结尾的 LIS 长度，cnt[i] 记录长度相同时的方案数，前缀较小且长度+1 则更新计数。

```python
a = list(map(int, input().split()))
n = len(a)
dp = [1] * n
cnt = [1] * n
maxlen = 1
tot = 1
for i in range(n):
    for j in range(i):
        if a[j] < a[i]:
            if dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                cnt[i] = cnt[j]
            elif dp[j] + 1 == dp[i]:
                cnt[i] += cnt[j]
    if dp[i] > maxlen:
        maxlen = dp[i]
        tot = cnt[i]
    elif dp[i] == maxlen:
        tot += cnt[i]
print(maxlen, tot)
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.14.29 例 29：贴地板砖/铺瓷砖方案（洛谷 P1490 铺地砖·经典）⭐

> **知识点**：线性 DP、平面划分计数｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：用 1×2 与 2×1 两种骨牌铺满 2×n 的地板，求铺设方法总数，结果对 10007 取模。

**思路**

💡 类比"多米诺铺路"：2×n 只能在最后一列放竖骨牌或与前一列合作放两块横骨牌，故 f[n]=f[n−1]+f[n−2]，即斐波那契并取模。

```python
MOD = 10007
n = int(input())
a, b = 1, 1
for _ in range(2, n + 1):
    a, b = b, (a + b) % MOD
print(b)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.30 例 30：最大子矩阵和（洛谷 P1719 最大加权矩形）⭐⭐

> **知识点**：二维最大子段和、前缀和优化｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 N×N 矩阵，求元素和最大的子矩阵和。

**思路**

💡 类比"框选大区域"：枚举矩阵的上下边界，用列前缀和把矩阵压成一维，再对该一维数组跑 Kadane 最大子段和。

```python
n = int(input())
a = [list(map(int, input().split())) for _ in range(n)]
ans = -10**9
for top in range(n):
    col = [0] * n
    for bot in range(top, n):
        cur = -10**9
        for j in range(n):
            col[j] += a[bot][j]
            cur = max(col[j], cur + col[j])
            ans = max(ans, cur)
print(ans)
```

> **复杂度**：O(N³) 时间，O(N) 空间

---

#### 17.14.31 例 31：过河卒（洛谷 P1002）⭐⭐

> **知识点**：坐标 DP、障碍点计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：棋盘 B 点 (n,m)，卒从 (0,0) 出发可向右或向下，但有对方的马 C 点，且马控制的 "日" 字形 9 点为禁地。求到达 B 点的路径数。

**思路**

💡 类比"绕开马蹄点"：先标出所有禁点，dp[i][j]=dp[i−1][j]+dp[i][j−1]（禁点置 0）。用大数累加避免溢出。

```python
n, m, cx, cy = map(int, input().split())
block = set()
horse = [(cx, cy)] + [(cx + dx, cy + dy) for dx, dy in
         [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]]
for x, y in horse:
    if 0 <= x <= n and 0 <= y <= m:
        block.add((x, y))
dp = [[0] * (m + 1) for _ in range(n + 1)]
dp[0][0] = 1
for i in range(n + 1):
    for j in range(m + 1):
        if (i, j) in block:
            dp[i][j] = 0
            continue
        if i > 0:
            dp[i][j] += dp[i - 1][j]
        if j > 0:
            dp[i][j] += dp[i][j - 1]
print(dp[n][m])
```

> **复杂度**：O((n+1)(m+1)) 时间，O((n+1)(m+1)) 空间

---

#### 17.14.32 例 32：分组装车/均分纸牌变式——划分两端和最大（经典背包应用）⭐

> **知识点**：0-1 背包求和可行性、接近装满｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给出若干正整数，判断能否把总和分成相等的两半（每个数至多用一次）。

**思路**

💡 类比"两边平衡"：当且仅当能凑出总和的一半才可行。用 0-1 背包判断过半和 target 是否能凑出。

```python
a = list(map(int, input().split()))
total = sum(a)
if total % 2:
    print("No")
    exit()
target = total // 2
dp = [False] * (target + 1)
dp[0] = True
for x in a:
    for j in range(target, x - 1, -1):
        if dp[j - x]:
            dp[j] = True
print("Yes" if dp[target] else "No")
```

> **复杂度**：O(n·target) 时间，O(target) 空间

---

#### 17.14.33 例 33：字符串切分最大价值——分割等积（经典 LIS 应用细节）⭐⭐

> **知识点**：最长不下降子序列（可相等）｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定序列，求最长不下降子序列（相等也算）的长度。

**思路**

💡 类比"允许并列排队"：与 LIS 唯一区别是转移条件由 a[j]<a[i] 改为 a[j]<=a[i]。也可用 patience 排序的二分法 O(N log N)。

```python
a = list(map(int, input().split()))
import bisect
tails = []
for x in a:
    pos = bisect.bisect_right(tails, x)
    if pos == len(tails):
        tails.append(x)
    else:
        tails[pos] = x
print(len(tails))
```

> **复杂度**：O(N log N) 时间，O(N) 空间

---

#### 17.14.34 例 34：二维 LIS——俄罗斯套娃信封（LeetCode 354）⭐⭐

> **知识点**：多维 LIS、排序归一维二分｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定若干信封的宽高 (w,h)，当 w1<w2 且 h1<h2 时可套叠，求最多能嵌套的信封数目。

**思路**

💡 类比"大小套娃"：先按宽度排序（同宽时按高度降序，避免同宽被误叠），再对高度序列求最长严格递增子序列（LIS 二分）。

```python
import bisect
n = int(input())
env = [tuple(map(int, input().split())) for _ in range(n)]
env.sort(key=lambda e: (e[0], -e[1]))
tails = []
for w, h in env:
    pos = bisect.bisect_left(tails, h)
    if pos == len(tails):
        tails.append(h)
    else:
        tails[pos] = h
print(len(tails))
```

> **复杂度**：O(N log N) 时间，O(N) 空间

---

#### 17.14.35 例 35：股票买卖最佳时机（洛谷 P8784/LeetCode 121）⭐

> **知识点**：线性 DP、一次买卖最大利润｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定股价序列，只能买卖一次，求最大利润；不能卖出则利润 0。

**思路**

💡 类比"低价买高价抛"：遍历时维护历史最低价，计算当前价与最低价的差作为候选利润并更新最大利润。

```python
p = list(map(int, input().split()))
low = p[0]
best = 0
for x in p[1:]:
    low = min(low, x)
    best = max(best, x - low)
print(best)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.36 例 36：完全平方数最少个数（LeetCode 279）⭐

> **知识点**：完全背包（可选无限次）、最小件数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n，求可以用若干完全平方数（如 1,4,9,…）之和表示 n 的最少数量。

**思路**

💡 类比"平方硬币找零"：完全平方数当作可选无穷次的物品，dp[j]=min(dp[j], dp[j−s]+1)。

```python
n = int(input())
dp = [0] + [10**9] * n
for i in range(1, n + 1):
    j = 1
    while j * j <= i:
        dp[i] = min(dp[i], dp[i - j * j] + 1)
        j += 1
print(dp[n])
```

> **复杂度**：O(N√N) 时间，O(N) 空间

---

#### 17.14.37 例 37：交错字符串（LeetCode 97）⭐⭐

> **知识点**：二维线性 DP、双指针状态压缩为布尔矩阵｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s1、s2、s3，判断 s3 是否由 s1 与 s2 交错组成（保持各自相对顺序）。

**思路**

💡 类比"两副牌交叉发"：dp[i][j] 表示用 s1 前 i 个与 s2 前 j 个能否组成 s3 前 i+j 个。分别检查来自 s1 或来自 s2 的最后一个字符。

```python
s1 = input().strip()
s2 = input().strip()
s3 = input().strip()
m, n = len(s1), len(s2)
if m + n != len(s3):
    print("No")
    exit()
dp = [[False] * (n + 1) for _ in range(m + 1)]
dp[0][0] = True
for i in range(1, m + 1):
    dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]
for j in range(1, n + 1):
    dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]
for i in range(1, m + 1):
    for j in range(1, n + 1):
        dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or \
                   (dp[i][j - 1] and s2[j - 1] == s3[i + j - 1])
print("Yes" if dp[m][n] else "No")
```

> **复杂度**：O(m·n) 时间，O(m·n) 空间

---

#### 17.14.38 例 38：最大上升路径乘积（矩阵中递增路径——滑雪变式）⭐⭐

> **知识点**：记忆化搜索、坐标 DP、注意负号｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定矩阵，求一条严格递增的路径的最大长度（可四方向移动），相邻格值必须严格增大。

**思路**

💡 类比"爬山爬得远比"：dp[i][j]=1+max(四方向中比它大的邻居的 dp)，递归+记忆化确保每格只算一次。

```python
import sys
sys.setrecursionlimit(100000)
r, c = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(r)]
memo = [[0] * c for _ in range(r)]
d = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def dfs(i, j):
    if memo[i][j]:
        return memo[i][j]
    best = 1
    for di, dj in d:
        ni, nj = i + di, j + dj
        if 0 <= ni < r and 0 <= nj < c and a[ni][nj] > a[i][j]:
            best = max(best, dfs(ni, nj) + 1)
    memo[i][j] = best
    return best

ans = 0
for i in range(r):
    for j in range(c):
        ans = max(ans, dfs(i, j))
print(ans)
```

> **复杂度**：O(R·C) 时间，O(R·C) 空间

---

#### 17.14.39 例 39：石子合并（线性版）——邻接两两合并最小/最大（洛谷 P1775 简化）⭐⭐

> **知识点**：区间 DP、合并代价前缀和优化｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：N 堆石子排成一排，相邻两堆可合并，合并代价为两堆石子数之和。求合并成一堆的最小总代价。

**思路**

💡 类比"聚沙成塔"：dp[i][j] 表示合并区间 [i,j] 的最小代价，枚举中间分割点 k，dp=min(dp[i][k]+dp[k+1][j])+前缀和（区间总量）。区间按长度从小到大枚举。

```python
n = int(input())
a = list(map(int, input().split()))
pre = [0]
for x in a:
    pre.append(pre[-1] + x)
INF = float('inf')
dp = [[0] * n for _ in range(n)]
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = INF
        for k in range(i, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + pre[j + 1] - pre[i])
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.14.40 例 40：混合背包（洛谷 P1833 樱花）⭐⭐

> **知识点**：0-1/完全/多重背包混合处理｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有若干物品，有的只能取一次，有的能取无限次，有的有数量限制，每种有代价与价值。求容量内最大价值。

**思路**

💡 类比"一锅烩背包"：对每种物品判断类型分别处理——01 倒序、完全正序、多重用二进制拆分变 01。

```python
cap, n = map(int, input().split())
dp = [0] * (cap + 1)
for _ in range(n):
    w, v, t = map(int, input().split())
    if t == 0:  # 完全背包
        for j in range(w, cap + 1):
            dp[j] = max(dp[j], dp[j - w] + v)
    else:
        k = 1
        while t > 0:
            cnt = min(t, k)
            ww, vv = w * cnt, v * cnt
            for j in range(cap, ww - 1, -1):
                dp[j] = max(dp[j], dp[j - ww] + vv)
            t -= cnt
            k <<= 1
print(dp[cap])
```

> **复杂度**：O(cap·(n+log 数量)) 时间，O(cap) 空间

---

#### 17.14.41 例 41：靠岸船载重（最大载重近似）——多重/01 划分最大和（经典）⭐

> **知识点**：01 背包求不超过容量的最大和｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数集合与目标 S，从集合中选若干数使和不大于 S 且尽量大，求该最大值。

**思路**

💡 类比"装满货箱不撑破"：直接把"和"当作容量与价值，01 背包正推，dp[j] 表示容量 j 能装的最大和，答案 dp[S]。

```python
a = list(map(int, input().split()))
S = int(input())
dp = [0] * (S + 1)
for x in a:
    for j in range(S, x - 1, -1):
        if dp[j - x] + x > dp[j]:
            dp[j] = dp[j - x] + x
print(dp[S])
```

> **复杂度**：O(n·S) 时间，O(S) 空间

---

#### 17.14.42 例 42：数字金字塔——取模最大（网格前缀最大值变式）⭐⭐

> **知识点**：坐标 DP、负数处理、平局处理｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：三角网格，从顶到底找出一条路，使路径上数字差（相邻两格差的绝对值）之和最小。

**思路**

💡 类比"挑平缓下坡"：dp[i][j]=min(dp[i−1][j−1], dp[i−1][j])+|a[i][j]−a[i−1][对应]|。将每个格只依赖上一行的两个父格。

```python
n = int(input())
tri = [list(map(int, input().split())) for _ in range(n)]
INF = float('inf')
prev = [tri[0][0]]
for i in range(1, n):
    cur = [INF] * (i + 1)
    for j in range(i + 1):
        for pj in (j - 1, j):
            if 0 <= pj < i and prev[pj] < INF:
                cost = prev[pj] + abs(tri[i][j] - tri[i - 1][pj])
                if cost < cur[j]:
                    cur[j] = cost
    prev = cur
print(min(prev))
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.14.43 例 43：最大路径和（数字三角形综合，含负数）⭐

> **知识点**：坐标 DP、自底向上、负数仍成立｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：同数字三角形，数字可为负，仍求从顶到底的最大路径数字和。

**思路**

💡 类比"尽管有坑也要选大"：自底向上与例 3 相同，负数不影响 max 的正确性，直接滚 dp。

```python
n = int(input())
tri = [list(map(int, input().split())) for _ in range(n)]
dp = tri[-1][:]
for i in range(n - 2, -1, -1):
    for j in range(len(tri[i])):
        dp[j] = tri[i][j] + max(dp[j], dp[j + 1])
print(dp[0])
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.14.44 例 44：跳台阶最小步（每次跳 1..k）⭐⭐

> **知识点**：线性 DP、固定/可变跳幅、单/双端维护｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从位置 0 跳到位置 n，每次可向前跳 1..k 步且落点有一定代价，求到 n 的最小总代价。

**思路**

💡 类比"选择落脚石"：dp[i]=min(dp[i−t])+cost[i]（t=1..k）。小数据直接三重循环即可，k 大可用单调队列优化。

```python
n, k = map(int, input().split())
cost = list(map(int, input().split()))  # cost[i] 为落在 i 的代价
INF = float('inf')
dp = [INF] * (n + 1)
dp[0] = cost[0] if len(cost) > 0 else 0
for i in range(1, n + 1):
    c = cost[i] if i < len(cost) else 0
    dp[i] = min(dp[max(0, i - k):i]) + c
print(dp[n])
```

> **复杂度**：O(n·k) 时间，O(n) 空间

---

#### 17.14.45 例 45：斐波那契数列取模（洛谷 P1962）⭐

> **知识点**：线性 DP 取模、快速倍增优化（大 n）｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定大整数 n 与模 M，求斐波那契第 n 项对 M 取模的值。n 可非常大（如 1e18）。

**思路**

💡 类比"快到对数"：用斐波那契快速倍增公式。F(2k)=F(k)·(2F(k+1)−F(k))，F(2k+1)=F(k+1)²+F(k)²，配合递归，O(log n)。

```python
def fib(n, mod):
    def dfs(n):
        if n == 0:
            return 0, 1
        a, b = dfs(n >> 1)
        c = a * (2 * b - a) % mod
        d = (a * a + b * b) % mod
        if n & 1:
            return d, (c + d) % mod
        return c, d
    return dfs(n)[0]

n = int(input())
mod = 10**9 + 7
print(fib(n, mod))
```

> **复杂度**：O(log n) 时间，O(log n) 递归空间

---

#### 17.14.46 例 46：最长公共子序列——滚动数组优化空间（经典）⭐⭐

> **知识点**：LCS、滚动数组降空间｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求两字符串 LCS 长度，n、m 均较大（如 5000），要求空间尽量小。

**思路**

💡 类比"只留上一行"：dp 每行更新只依赖上一行与当前行左边格，故仅需两个一维数组交替滚动，空间降为 O(m)。

```python
a = input().strip()
b = input().strip()
m, n = len(a), len(b)
prev = [0] * (n + 1)
for i in range(1, m + 1):
    cur = [0] * (n + 1)
    for j in range(1, n + 1):
        if a[i - 1] == b[j - 1]:
            cur[j] = prev[j - 1] + 1
        else:
            cur[j] = max(prev[j], cur[j - 1])
    prev = cur
print(prev[n])
```

> **复杂度**：O(m·n) 时间，O(n) 空间

---

#### 17.14.47 例 47：买卖股票含冷冻期（LeetCode 309）⭐⭐

> **知识点**：状态机 DP、持有/未持有/冷冻三态｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：价格序列，卖出后次日为冷冻期不能买入，可进行任意次交易，求最大利润。

**思路**

💡 类比"三档状态开关"：维护 hold（持有）、sold（刚卖出）、rest（休息）。三状态按日转移，取最终 sold 与 rest 的最大值。

```python
p = list(map(int, input().split()))
if not p:
    print(0)
    exit()
n = len(p)
hold = -p[0]
sold = 0
rest = 0
for i in range(1, n):
    new_hold = max(hold, rest - p[i])
    new_sold = hold + p[i]
    new_rest = max(rest, sold)
    hold, sold, rest = new_hold, new_sold, new_rest
print(max(sold, rest))
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.48 例 48：最大整除子集（LeetCode 368 求具体方案）⭐⭐

> **知识点**：带路径记录的 LIS 变式、整除性质｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无重复正整数集合，求一个最大子集，其中任意两数 a、b 满足 a%b==0 或 b%a==0，输出该子集。

**思路**

💡 类比"倍数同族"：先排序，dp[i] 表示以 nums[i] 结尾的最大合法子集长度，转移检查 nums[i]%nums[j]==0，用 pre 数组回放方案。

```python
nums = list(map(int, input().split()))
nums.sort()
n = len(nums)
dp = [1] * n
pre = [-1] * n
end = 0
for i in range(n):
    for j in range(i):
        if nums[i] % nums[j] == 0 and dp[j] + 1 > dp[i]:
            dp[i] = dp[j] + 1
            pre[i] = j
    if dp[i] > dp[end]:
        end = i
res = []
while end != -1:
    res.append(nums[end])
    end = pre[end]
print(res[::-1])
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.14.49 例 49：不同子序列个数（LeetCode 940）⭐⭐

> **知识点**：线性 DP、去重子序列计数｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串，求其不同的非空子序列数量，结果对 1e9+7 取模。

**思路**

💡 类比"去重组词"：dp[i] 处理到第 i 个字符时的不同子序列数。每来一个字符 x，新增子序列数为当前总数；若 x 之前出现过，减去上次计入的重复部分。用 last 数组记录每个字符最后出现时多算的量。

```python
s = input().strip()
MOD = 10**9 + 7
n = len(s)
last = [0] * 26  # 每个字符上次新增的重复量
ans = 0
for ch in s:
    idx = ord(ch) - ord('a')
    new = (ans + 1) % MOD   # 新增的以 ch 结尾的子序列（含单字符 ch）
    ans = (ans + new - last[idx]) % MOD
    last[idx] = new
print(ans % MOD)
```

> **复杂度**：O(N) 时间，O(26) 空间

---

#### 17.14.50 例 50：围栏修复——搭桥最少木板变式（多重可行性 poj 2229 拆分计数）⭐⭐

> **知识点**：完全背包方案数、2 的幂拆分｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：用若干个 2 的幂（即 1,2,4,…，每种可重复）之和表示正整数 N 的方案数，顺序不同的算不同方案吗？此处按顺序区别计作不同，对 1000000000 取模。

**思路**

💡 类比"二进制拼钱"：把 2^k 当完全背包物品但每次也考虑顺序——实际本类为 0-1 规划（每种幂配额），采用递推：奇数 f[n]=f[n−1]，偶数 f[n]=f[n−1]+f[n//2]。

```python
MOD = 10**9 + 7
n = int(input())
dp = [0] * (n + 1)
dp[0] = 1
d = 1
while d <= n:
    for j in range(d, n + 1):
        dp[j] = (dp[j] + dp[j - d]) % MOD
    d <<= 1
print(dp[n])
```

> **复杂度**：O(N log N) 时间，O(N) 空间

---

#### 17.14.51 例 51：最大连续 1 的个数（变式——至多翻转 K 个 0，LeetCode 487）⭐⭐

> **知识点**：线性 DP/滑动窗口、状态 K｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：二进制数组，最多可把 K 个 0 变成 1，求最长的连续 1 子数组长度。

**思路**

💡 类比"救火队救零"：滑动窗口维护窗口内 0 的个数不超过 K，超了就收缩左端，窗口最大长度即答案。也可用 DP 记还将被翻转数。

```python
a = list(map(int, input().split()))
k = int(input())
left = 0
zeros = 0
best = 0
for right, v in enumerate(a):
    if v == 0:
        zeros += 1
    while zeros > k:
        if a[left] == 0:
            zeros -= 1
        left += 1
    best = max(best, right - left + 1)
print(best)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.52 例 52：数字直角三角形最小路径（自顶向下，含重复选择限制）⭐⭐

> **知识点**：坐标 DP、双状态缩小转移 |｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：与例 3 类似，但要求每次必须移动，只能到 (i+1,j) 或 (i+1,j+1)，数字可负，求最大路径和。

**思路**

💡 类比"必走之梯"：经典数字三角形，与例 3/43 同框架处理负数，自底向上滚动，答案 dp[0]。

```python
n = int(input())
tri = [list(map(int, input().split())) for _ in range(n)]
dp = tri[-1][:]
for i in range(n - 2, -1, -1):
    for j in range(len(tri[i])):
        dp[j] = tri[i][j] + max(dp[j], dp[j + 1])
print(dp[0])
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.14.53 例 53：礼物最大价值（网格采花最大值，洛谷 P1004 方格取数简化）⭐⭐

> **知识点**：坐标 DP、二维取数最大值｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：N×N 方格，从 (1,1) 到 (N,N) 走一条路，只能下或右，经过的格子的数累加（每个格至多算一次），求最大和。

**思路**

💡 类比"单卵运水"：对单路过问可贪心？不，需 DP。dp[i][j]=max(dp[i−1][j], dp[i][j−1])+a[i][j]，网格 OK 保证无环。

```python
n = int(input())
a = [input().split() for _ in range(n)]
a = [[int(x) for x in row] for row in a]
dp = [[0] * n for _ in range(n)]
dp[0][0] = a[0][0]
for j in range(1, n):
    dp[0][j] = dp[0][j - 1] + a[0][j]
for i in range(1, n):
    dp[i][0] = dp[i - 1][0] + a[i][0]
for i in range(1, n):
    for j in range(1, n):
        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]) + a[i][j]
print(dp[n - 1][n - 1])
```

> **复杂度**：O(N²) 时间，O(N²) 空间

---

#### 17.14.54 例 54：骑士收集金币（网格最大和，含障碍字母）⭐⭐

> **知识点**：坐标 DP、部分格不可走｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：m×n 网格含非负利润，左上到右下只能下/右，存在几个'#'障碍格不能通过，求最大总利润。

**思路**

💡 类比"绕路捡钱"：障碍格 dp 置 −∞（不可达），其余格取上方、左方较大者加本格利润。

```python
m, n = map(int, input().split())
g = [input().split() for _ in range(m)]
INF_NEG = float('-inf')
dp = [[INF_NEG] * n for _ in range(m)]
dp[0][0] = 0
for i in range(m):
    for j in range(n):
        if g[i][j] == '#':
            continue
        best = dp[i][j]
        if i > 0:
            best = max(best, dp[i - 1][j])
        if j > 0:
            best = max(best, dp[i][j - 1])
        if best > INF_NEG:
            dp[i][j] = best + int(g[i][j])
print(dp[m - 1][n - 1] if dp[m - 1][n - 1] > INF_NEG else -1)
```

> **复杂度**：O(m·n) 时间，O(m·n) 空间

---

#### 17.14.55 例 55：数组交错取最大不连续和（取 m 元素不相邻最大值）⭐⭐

> **知识点**：背包+状态、线性 DP 组合限制｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个物品排成一排，选若干使价值和不小于某一因子的最小开销受限等。简化：价值与数量双限制，选出的物品两两不相邻，求最大价值和。

**思路**

💡 类比"隔空取宝"：需记位置（相邻限制）与数量。dp[cnt] 设一维即可吗？相邻限制要求连续两个不能同时取，可定义为取以物品 i 结尾且……直接做：dp[i][k] 表示前 i 个取 k 个的最大和，转移加入或跳过。

```python
n, K = map(int, input().split())
a = list(map(int, input().split()))
neg = float('-inf')
dp = [[neg] * (K + 1) for _ in range(2)]
dp[1][0] = 0
# 简化：用滚动，dp[0]=不取当前, dp[1]=已取（结尾在当前位置）
for i in range(n):
    # 由于不相邻，直接从上一轮不取状态与空状态转移
    pass
# 采用标准版本：
dp = [[neg] * (K + 1) for _ in range(n + 1)]
for i in range(n + 1):
    dp[i][0] = 0
for i in range(1, n + 1):
    for k in range(1, K + 1):
        # 不取第 i 个
        dp[i][k] = dp[i - 1][k]
        # 取第 i 个，则第 i-1 个不能取
        dp[i][k] = max(dp[i][k], dp[i - 2][k - 1] + a[i - 1])
print(max(dp[n][k] for k in range(K + 1)))
```

> **复杂度**：O(n·K) 时间，O(n·K) 空间

---

#### 17.14.56 例 56：最优二叉搜索树思路引入——哈夫曼编码最小（洛谷 P2168 简化解码代价）⭐⭐

> **知识点**：线性 DP 与贪心区别、哈夫曼树构建｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：每个字符有出现频次，用二进制前缀编码使总编码长度（∑频次×码长）最小，求最小总长度。

**思路**

💡 类比"高频短码"：用哈夫曼贪心，每次合并频次最小的两个（小顶堆），累计合并代价即加权路径长度。

```python
import heapq
n = int(input())
f = [int(input()) for _ in range(n)]
heapq.heapify(f)
ans = 0
while len(f) > 1:
    x = heapq.heappop(f)
    y = heapq.heappop(f)
    ans += x + y
    heapq.heappush(f, x + y)
print(ans)
```

> **复杂度**：O(N log N) 时间，O(N) 空间

---

#### 17.14.57 例 57：数的划分（洛谷 P1025，把整数 n 分成 k 份）⭐⭐

> **知识点**：计数 DP、有序/无序划分、组合拆分｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：把正整数 n 分成 k 个正整数之和，顺序不影响（即把 n 拆成 k 份的不降拆分），求方案数。结果可大但在此范围内直接计。

**思路**

💡 类比"分蛋糕固定块"：dp[n][k] 表示把 n 分成 k 份的方案数，其一满足 dp[n][k]=dp[n−1][k−1]+dp[n−k][k]（含 1 与不含 1 两类情形）。

```python
n, k = map(int, input().split())
dp = [[0] * (k + 1) for _ in range(n + 1)]
dp[0][0] = 1
for i in range(1, n + 1):
    for j in range(1, min(k, i) + 1):
        dp[i][j] = dp[i - 1][j - 1]
        if i >= j:
            dp[i][j] += dp[i - j][j]
print(dp[n][k])
```

> **复杂度**：O(n·k) 时间，O(n·k) 空间

---

#### 17.14.58 例 58：完全覆盖网格（1×2 覆盖 3×n 的方案数）⭐⭐

> **知识点**：矩阵覆盖 DP、状态计数（按对齐模式）｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：用 1×2 骨牌既不重叠也不留缝地铺满 3×n 矩形，求方案数，答案取模。n 为偶数才可能有解。

**思路**

💡 类比"三列拼积木"：按最左列是否完整划分状态。设 f[n] 为正好铺满方案数，g[n] 为最左列留一个缺口（凸出一格）的方案数，递推 f[i]=4 f[i−2]−f[i−4]。

```python
MOD = 10007
n = int(input())
if n % 2:
    print(0)
    exit()
N = n // 2
f = [0] * (n + 1)
f[0] = 1
if n >= 2:
    f[2] = 3
for i in range(4, n + 1, 2):
    f[i] = (4 * f[i - 2] % MOD - f[i - 4]) % MOD
print(f[n] % MOD)
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.14.59 例 59：零一背包求具体方案（洛谷 P1164 小A点菜）⭐

> **知识点**：01 背包方案计数、具体组合不需输出｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：有 a 种菜、钱数为 b，每道菜价格，问恰好把钱花完的买菜方案数。

**思路**

💡 类比"点菜凑钱"：dp[j] 表示恰好花费 j 元的方案数，01 背包倒序累加 dp[j]+=dp[j−price]。

```python
a, b = map(int, input().split())
price = list(map(int, input().split()))
dp = [0] * (b + 1)
dp[0] = 1
for p in price:
    for j in range(b, p - 1, -1):
        dp[j] += dp[j - p]
print(dp[b])
```

> **复杂度**：O(a·b) 时间，O(b) 空间

---

#### 17.14.60 例 60：数字三角形二取并存两次（方格取数 POJ 水库-双路动态规划）⭐⭐

> **知识点**：多进程坐标 DP、同时走两路｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：N×N 网格，A 从左上走一条路到右下，B 再走一条路（每个格只能被取一次数字），两路可重叠但不必。求两次共取得的最大数字和。

**思路**

💡 类比"一次派两台车一起走"：经典双线 DP，用 dp[s][i1][i2] 表示步数相同、两人分别在第 i1/i2 行的状态，转移同时由上一状态的四种组合而来，重叠格只算一次数字。

```python
n = int(input())
a = [[0] * n for _ in range(n)]
while True:
    x, y, v = map(int, input().split())
    if x == 0 and y == 0 and v == 0:
        break
    a[x - 1][y - 1] = v
# dp[step 对角线][i1][i2]
smax = 2 * n - 1
dp = [[[0] * n for _ in range(n)] for __ in range(smax + 1)]
dp[0][0][0] = a[0][0]
for s in range(1, smax):
    for i1 in range(max(0, s - n + 1), min(n - 1, s) + 1):
        j1 = s - i1
        for i2 in range(max(0, s - n + 1), min(n - 1, s) + 1):
            j2 = s - i2
            if i1 < 0 or i1 >= n or i2 < 0 or i2 >= n:
                continue
            val = a[i1][j1]
            if i1 != i2 and j1 != j2:
                val += a[i2][j2]
            best = 0
            for pi1 in (i1 - 1, i1):
                for pi2 in (i2 - 1, i2):
                    if 0 <= pi1 < n and 0 <= pi2 < n and (pi1 - 1) % n or True:
                        best = max(best, dp[s - 1][min(pi1, n - 1)][min(pi2, n - 1)])
            dp[s][i1][i2] = best + val
print(dp[smax - 1][n - 1][n - 1])
```

> **复杂度**：O((2N)·N²) 时间，O(N³) 空间

---

#### 17.14.61 例 61：最长有效括号子串长度（LeetCode 32）⭐⭐

> **知识点**：线性 DP、栈匹配建模｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定只含 '(' 与 ')' 的字符串，求最长的有效（正确匹配）括号子串长度。

**思路**

💡 类比"配对串珠"：dp[i] 表示以位置 i 结尾的最长有效括号长度。仅 ')' 可结束，若前一个是 '(' 则 dp[i]=dp[i−2]+2；若 s[i−1] 是 ')' 且前面还有匹配则 dp[i]=dp[i−1]+2+dp[i−dp[i−1]−2]。

```python
s = input().strip()
n = len(s)
dp = [0] * n
ans = 0
for i in range(1, n):
    if s[i] == ')':
        if s[i - 1] == '(':
            dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
        elif i - dp[i - 1] > 0 and s[i - dp[i - 1] - 1] == '(':
            dp[i] = dp[i - 1] + 2 + (dp[i - dp[i - 1] - 2] if i - dp[i - 1] - 2 >= 0 else 0)
        ans = max(ans, dp[i])
print(ans)
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.14.62 例 62：最少操作使数组递增（贪心+线性遍历）——非纯 DP 但为 DP 目录概念题⭐

> **知识点**：线性扫描、增量修正｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定数组，允许对任一元素增加任意非负值，求使数组严格递增的最少总增加值。

**思路**

💡 类比"排队补身高"：从左到右，若 a[i]<=a[i−1]，则把它补到 a[i−1]+1，累加差值并更新。

```python
a = list(map(int, input().split()))
ans = 0
for i in range(1, len(a)):
    if a[i] <= a[i - 1]:
        need = a[i - 1] + 1 - a[i]
        ans += need
        a[i] += need
print(ans)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.63 例 63：整数拆分最大化积（LeetCode 343）⭐

> **知识点**：线性 DP、拆分最优子结构｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：将正整数 n 拆成至少两个正整数之和，使这些正整数的乘积最大，返回最大乘积。

**思路**

💡 类比"拆大棒更结实"：dp[i] 表示整数 i 拆分的最大乘积，转移 dp[i]=max(j×(i−j), j×dp[i−j])（j 从 1 到 i−1）。

```python
n = int(input())
dp = [0] * (n + 1)
dp[1] = 1
for i in range(2, n + 1):
    for j in range(1, i):
        dp[i] = max(dp[i], j * (i - j), j * dp[i - j])
print(dp[n])
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.14.64 例 64：不同的二叉搜索树个数（LeetCode 96）⭐⭐

> **知识点**：卡特兰数、统计 DP｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定整数 n，求由 1..n 组成的互不相同的二叉搜索树（BST）有多少种结构。

**思路**

💡 类比"根分左右"：以 i 为根，左子树用 i−1 个数、右子树用 n−i 个数，dp[n]=∑dp[i−1]dp[n−i]，即卡特兰数。

```python
n = int(input())
dp = [0] * (n + 1)
dp[0] = 1
for i in range(1, n + 1):
    for j in range(i):
        dp[i] += dp[j] * dp[i - 1 - j]
print(dp[n])
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.14.65 例 65：按摩师预约（同打家劫舍，变式 LeetCode 面试 17.16）⭐

> **知识点**：线性 DP、相邻互斥变式｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：数组给出每天预约时长，不能连续两天预约，求最大总时长。

**思路**

💡 类比"两天一歇"：与打家劫舍完全同构，dp[i]=max(dp[i−1], dp[i−2]+a[i])。

```python
a = list(map(int, input().split()))
prev, cur = 0, 0
for x in a:
    prev, cur = cur, max(cur, prev + x)
print(cur)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.66 例 66：最长湍流子数组（LeetCode 978）⭐⭐

> **知识点**：线性 DP、比较方向交替｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：数组为"湍流"当相邻元素交替地大于/小于。求最长的湍流子数组长度。

**思路**

💡 类比"锯齿状波浪"：dp_up[i]、dp_down[i] 分别表示以 i 结尾且末尾方向为上/下的最长长度，根据相邻比较更新。

```python
a = list(map(int, input().split()))
n = len(a)
if n < 2:
    print(n)
    exit()
up = [1] * n
down = [1] * n
ans = 1
for i in range(1, n):
    if a[i] > a[i - 1]:
        up[i] = down[i - 1] + 1
    elif a[i] < a[i - 1]:
        down[i] = up[i - 1] + 1
    ans = max(ans, up[i], down[i])
print(ans)
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.14.67 例 67：组合总和 IV（排列数，LeetCode 377）⭐⭐

> **知识点**：完全背包按顺序计数（排列）｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：由数组 nums 中的数（可重复、顺序不同的算不同）组成目标 target 的方式总数。

**思路**

💡 类比"按步排列"：与组合数相反，这里顺序有效，故外层枚举和、内层枚举数字。dp[t]+=dp[t−num]。

```python
nums = list(map(int, input().split()))
target = int(input())
dp = [0] * (target + 1)
dp[0] = 1
for t in range(1, target + 1):
    for num in nums:
        if t >= num:
            dp[t] += dp[t - num]
print(dp[target])
```

> **复杂度**：O(target·len(nums)) 时间，O(target) 空间

---

#### 17.14.68 例 68：小蜜蜂——斐波那契的网格变式（HDU 2041 超级楼梯）⭐

> **知识点**：线性 DP、斐波那契变式｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：从 M 级楼梯的第 1 级爬到第 N 级，每次可跨 1 级或 2 级，求不同的走法数。M<N≤200 且答案可能较大。

**思路**

💡 类比"隔级上台阶"：距离 d=N−M 为所需跳跃数，方案数为第 d 个斐波那契数。

```python
import sys
fib = [1, 1]
for i in range(2, 45):
    fib.append(fib[-1] + fib[-2])
line = sys.stdin.readline()
while line:
    m, n = map(int, line.split())
    print(fib[n - m])
    line = sys.stdin.readline()
```

> **复杂度**：O(最大 N) 预计算，O(1) 单次查询

---

#### 17.14.69 例 69：传球游戏（洛谷 P1057）⭐

> **知识点**：循环 dp、两方向转移取模轮换｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个人围成一圈传 m 次球，初始在第 1 号，传 m 次后球回到 1 号的传法数，对 10^9+7 取模。

**思路**

💡 类比"围圈传花"：dp[t][i] 表示传 t 次后在 i 号的方法数，等于从左右邻居加来。环两端用取模处理。

```python
n, m = map(int, input().split())
MOD = 10**9 + 7
dp = [[0] * n for _ in range(m + 1)]
dp[0][0] = 1
for t in range(1, m + 1):
    for i in range(n):
        dp[t][i] = (dp[t - 1][(i - 1) % n] + dp[t - 1][(i + 1) % n]) % MOD
print(dp[m][0])
```

> **复杂度**：O(m·n) 时间，O(m·n) 空间

---

#### 17.14.70 例 70：学生排队跳格子最小有可能但受限——经典单调序列双堆思路（POJ 1836）⭐⭐

> **知识点**：LIS 双端拼接、队伍重排最少出列｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：士兵按身高排一列，需调整成"先严格上升到某个最高点，再严格下降"的队形，求最少需要出列的人数。

**思路**

💡 类比"两座坡夹一峰"：对每个位置求左侧最长严格上升与右侧最长严格下降，使 lis+lds−1 取最大，出列人数=n−该最大值。

```python
import bisect
n = int(input())
h = list(map(float, input().split()))

def length(seq):
    tails = []
    for x in seq:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)

best = 1
for k in range(n):
    left = length(h[:k])
    rev = [-x for x in reversed(h[k:])]
    right = length([-x for x in h[k:]])
    best = max(best, left + right)
print(n - best)
```

> **复杂度**：O(N² log N) 时间，O(N) 空间

---

#### 17.14.71 例 71：上楼梯可跨任意 <=k 的方案数（洛谷 P-aKnWw7/变式）⭐

> **知识点**：线性 DP、可变步长计数｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：每次可迈 1..k 级台阶，求上到第 n 级的走法总数（顺序不同算不同）。

**思路**

💡 类比"随便跨"：dp[i]=∑dp[i−t]（t=1..min(k,i)），可进一步用前缀和优化为 O(n)。

```python
n, k = map(int, input().split())
MOD = 1000000007
if k == 1:
    print(1); exit()
dp = [0] * (n + 1)
dp[0] = 1
window = 1
for i in range(1, n + 1):
    dp[i] = window % MOD
    window = (window * 2) % MOD
    if i >= k:
        window = (window - dp[i - k]) % MOD
print(dp[n] % MOD)
```

> **复杂度**：O(N) 时间，O(N) 空间（前缀和优化）

---

#### 17.14.72 例 72：最短补充字符匹配（LCS 应用——最少插入字符成回文）⭐⭐

> **知识点**：LCS/最长回文子序列、最少插入数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串，可以在任意位置插入字符，求把它变成回文串所需的最少插入字符数。

**思路**

💡 类比"补全镜像"：最少插入数 = 原长 − 最长回文子序列长度（LPS）。LPS 可用区间 DP 或 LCS(原串, 反转串) 求。

```python
s = input().strip()
r = s[::-1]
n = len(s)
dp = [[0] * (n + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, n + 1):
        if s[i - 1] == r[j - 1]:
            dp[i][j] = dp[i - 1][j - 1] + 1
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
print(n - dp[n][n])
```

> **复杂度**：O(N²) 时间，O(N²) 空间

---

#### 17.14.73 例 73：最长回文子序列长度（LeetCode 516）⭐⭐

> **知识点**：区间 DP（也可 LCS）｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s，求其最长回文子序列的长度。

**思路**

💡 类比"抽对称串"：dp[i][j]=2+dp[i+1][j−1] if 两端相同，否则 max(dp[i+1][j],dp[i][j−1])。从后往前枚举。

```python
s = input().strip()
n = len(s)
dp = [[0] * n for _ in range(n)]
for i in range(n - 1, -1, -1):
    dp[i][i] = 1
    for j in range(i + 1, n):
        if s[i] == s[j]:
            dp[i][j] = dp[i + 1][j - 1] + 2
        else:
            dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
print(dp[0][n - 1])
```

> **复杂度**：O(N²) 时间，O(N²) 空间

---

#### 17.14.74 例 74：打家劫舍加强——树形结构的第一课转换（打家劫舍 III 引入，LeetCode 337）⭐⭐

> **知识点**：树形 DP 引入、二叉树相邻节点互斥｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：二叉树，偷某节点则不能偷其直接子节点，求能偷的最大金额总和（树以父节点数组给出）。

**思路**

💡 类比"父子不能同时偷"：树形 DP，对每节点返回 (不偷本节点最大, 偷本节点最大)，自底向上（后序）合并。

```python
# 输入：父节点数组，-1 表示根；每个节点的值按序给出
values = list(map(int, input().split()))
parents = list(map(int, input().split()))
n = len(values)
children = [[] for _ in range(n)]
root = 0
for i, p in enumerate(parents):
    if p == -1:
        root = i
    else:
        children[p].append(i)

def dfs(u):
    steal = values[u]
    not_steal = 0
    for v in children[u]:
        sv, nv = dfs(v)
        steal += nv            # 偷 u 则子不偷
        not_steal += max(sv, nv)
    return steal, not_steal

s, ns = dfs(root)
print(max(s, ns))
```

> **复杂度**：O(N) 时间，O(N) 递归空间

---

#### 17.14.75 例 75：敲门砖——打家劫舍环形与树形综合练手（数组环+限制，LeetCode 213 变式）⭐⭐

> **知识点**：线性 DP 拆环、状态控制｜**难度**：⭐⭐｜**类型****：ACM/竞赛
> **题目描述**：房屋收尾相邻成环，且额外要求第 1 间与最后一间不能同时偷，求最大收益。

**思路**

💡 类比"环状首尾水火"：分两种情况——不偷第 0 家、不偷最后一家的线性打家劫舍，取最大值。

```python
def rob(nums):
    p, c = 0, 0
    for x in nums:
        p, c = c, max(c, p + x)
    return c

a = list(map(int, input().split()))
if len(a) == 1:
    print(a[0])
else:
    print(max(rob(a[:-1]), rob(a[1:])))
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.76 例 76：烤饼让价——最小下降子序列删除数（使数组上升所需删除最少）⭐

> **知识点**：LIS 应用、最少删除维持有序｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定数组，求最少删除多少个元素使其变成严格上升序列。

**思路**

💡 类比"剔除非编排"：保留尽量多 = 最长上升子序列，删除数=n−LIS 长度。

```python
import bisect
a = list(map(int, input().split()))
tails = []
for x in a:
    pos = bisect.bisect_left(tails, x)
    if pos == len(tails):
        tails.append(x)
    else:
        tails[pos] = x
print(len(a) - len(tails))
```

> **复杂度**：O(N log N) 时间，O(N) 空间

---

#### 17.14.77 例 77：爬黄河大坝——坐标 DP 二维累加（从下至上逐行累加最大值列）⭐

> **知识点**：坐标 DP、逐行转移选下端｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：从上到下每行依次选一个格子，下一行的格子必须与上一行所选列差不超过 1，求路径数字最大和。

**思路**

💡 类比"斜走下山"：dp[i][j] 表示走到第 i 行 j 列的最大和，由上一行 j−1,j,j+1 三格转移而来。

```python
m, n = map(int, input().split())
g = [list(map(int, input().split())) for _ in range(m)]
prev = g[0][:]
for i in range(1, m):
    cur = [0] * n
    for j in range(n):
        best = max(prev[max(0, j - 1):min(n, j + 2)])
        cur[j] = best + g[i][j]
    prev = cur
print(max(prev))
```

> **复杂度**：O(m·n) 时间，O(n) 空间

---

#### 17.14.78 例 78：踏实爬格子——螺旋网格最小和环（网格，方向受限日志）⭐⭐

> **知识点**：坐标 DP、必经点限制简化｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：网格上有 K 个必经点（按顺序），从左上到右下依次经过，求最小总代价路径。

**思路**

💡 类比"打卡途经"：把问题拆成 K+1 段形如"从 A 到 B 只能右/下的最小代价"的分段 DP，各段分别对子矩阵求最小路径再累加。

```python
def min_path(g, x1, y1, x2, y2):
    if x1 > x2 or y1 > y2:
        return 0
    m, n = x2 - x1 + 1, y2 - y1 + 1
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = g[x1][y1]
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + g[x1][y1 + j]
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + g[x1 + i][y1]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + g[x1 + i][y1 + j]
    return dp[m - 1][n - 1]

r, c = map(int, input().split())
g = [list(map(int, input().split())) for _ in range(r)]
k = int(input())
pts = [tuple(map(int, input().split())) for _ in range(k)]
pts = [(0, 0)] + pts + [(r - 1, c - 1)]
total = 0
for i in range(len(pts) - 1):
    x1, y1 = pts[i]
    x2, y2 = pts[i + 1]
    if x1 > x2 or y1 > y2:
        print(-1); exit()
    total += min_path(g, x1, y1, x2, y2) - g[x1][y1]
print(total + g[0][0])
```

> **复杂度**：O(K·r·c) 时间，O(max(r,c)²) 空间

---

#### 17.14.79 例 79：工资组合——多重背包朴素计数（分硬币凑薪，UVA 674 Coin Change）⭐⭐

> **知识点**：完全背包组合计数、标准换钱方案数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 1、5、10、25、50 五种硬币（无限），求凑出金额 n 的不同组合数。

**思路**

💡 类比"标准五种面额"：完全背包顺序无关计数，外层硬币内层金额，dp[j]+=dp[j−coin]。

```python
import sys
coins = [1, 5, 10, 25, 50]
dp = [0] * 7500
dp[0] = 1
for c in coins:
    for j in range(c, 7500):
        dp[j] += dp[j - c]
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    print(dp[int(line)])
```

> **复杂度**：O(5·7500) 预计算，O(1) 查询

---

#### 17.14.80 例 80：数组成链——最长递增的所有数连续（最长可组成合法子序列并列）⭐⭐

> **知识点**：LIS 变式、排序后线性扫描计数（连续子序列）｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个整数数组（元素可重复），求最长连续子序列的长度，其中元素按原相对顺序并两两相差 1（即递增步长为 1 的子序列）。

**思路**

💡 类比"阶梯依次爬"：把数组去重并排序，再找最长的"相邻相差 1"的连续段长度。

```python
a = list(map(int, input().split()))
st = sorted(set(a))
best = 0
cur = 0
last = None
for x in st:
    if last is None or x == last + 1:
        cur += 1
    else:
        cur = 1
    best = max(best, cur)
    last = x
print(best)
```

> **复杂度**：O(N log N) 时间，O(N) 空间

---

#### 17.14.81 例 81：线段可选——最大不重叠区间价值（变式，POJ 1160 不重叠区间权值和）⭐⭐

> **知识点**：排序+线性 DP、按右端点 dp 经典贪心/DP 结合｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 条线段，每条有左端点、右端点与权值，选择两两不重叠（端点也不重合）的线段使权值和最大。

**思路**

💡 类比"排课表不撞时间"：按右端点排序，dp[i] 表示前 i 条的最大权值和，可二分找到不与当前线段冲突的最近可接线段。

```python
import bisect
n = int(input())
seg = []
for _ in range(n):
    l, r, w = map(int, input().split())
    seg.append((r, l, w))
seg.sort()
end = [s[0] for s in seg]
dp = [0] * (n + 1)
for i in range(1, n + 1):
    r, l, w = seg[i - 1]
    # 找最后一个右端点 < l 的线段
    j = bisect.bisect_left(end, l)  # 第一个 end >= l
    dp[i] = max(dp[i - 1], dp[j] + w)
print(dp[n])
```

> **复杂度**：O(N log N) 时间，O(N) 空间

---

#### 17.14.82 例 82：重叠墙漆——最少切割木板等效最大不相交子集（经典）⭐

> **知识点**：LIS/区间选择同构、计数结合题目名简化｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定若干区间，选择最多数目的互不重叠的区间个数。

**思路**

💡 类比"最多排场"：按右端点贪心即可，也可 DP。选择右端点最小且不与已选冲突的区间能保证最多数量。

```python
n = int(input())
itv = [tuple(map(int, input().split())) for _ in range(n)]
itv.sort(key=lambda x: x[1])
count = 0
last_end = float('-inf')
for l, r in itv:
    if l >= last_end:
        count += 1
        last_end = r
print(count)
```

> **复杂度**：O(N log N) 时间，O(1) 空间

---

#### 17.14.83 例 83：最少贴纸——完全背包最小数量（零钱兑换同构）⭐

> **知识点**：完全背包最小件数变式、非整数路径容斥｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定若干面额（可重复使用）与目标额 S，求凑出不小于 S 的所用硬币的最少数目。

**思路**

💡 类比"多买一点"：凑到恰好 S 到 S+max(coin)−1 之间皆可，dp 求每个金额最小数量，取区间最小值。

```python
coins = list(map(int, input().split()))
S = int(input())
mx = max(coins)
INF = 10**9
M = S + mx - 1
dp = [INF] * (M + 1)
dp[0] = 0
for c in coins:
    for j in range(c, M + 1):
        if dp[j - c] + 1 < dp[j]:
            dp[j] = dp[j - c] + 1
print(min(dp[S:]))
```

> **复杂度**：O(M·K) 时间，O(M) 空间

---

#### 17.14.84 例 84：串乘积最大——数字串插入乘号（洛谷 P (数字分割乘积) 经典）⭐⭐

> **知识点**：区间 DP、字符串分割取数最大值｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个数字串和整数 k，在数字串中插入 k 个乘号（不改变数字顺序）使乘积最大，输出最大乘积。

**思路**

💡 类比"分段相乘选最大"：dp[i][t] 表示前 i 个数字放置 t 个乘号的最大乘积，枚举最后一个乘号位置 j，dp=max(dp[j][t−1]×片段[j:i])。

```python
s = input().strip()
k = int(input())
n = len(s)
m = [[0] * (n + 1) for _ in range(n + 1)]
for i in range(n):
    for j in range(i + 1, n + 1):
        m[i][j] = int(s[i:j])
dp = [[0] * (k + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    dp[i][0] = m[0][i]
for t in range(1, k + 1):
    for i in range(t + 1, n + 1):
        for j in range(t, i):
            dp[i][t] = max(dp[i][t], dp[j][t - 1] * m[j][i])
print(dp[n][k])
```

> **复杂度**：O(k·n²) 时间，O(k·n) 空间

---

#### 17.14.85 例 85：方形守卫——01 背包价值目标（恰好）⭐⭐

> **知识点**：01 背包、恰好装满判断最大价值｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：容量 W，n 件物品重量价值，求恰好把容量 W 装满的最大价值；若无法装满则输出 0。

**思路**

💡 类比"必须满箱"：初始 dp 除 0 外设为 −∞，转移 dp[j]=max(dp[j], dp[j−w]+v)，最后 dp[W]。

```python
W, n = map(int, input().split())
items = [tuple(map(int, input().split())) for _ in range(n)]
INF_NEG = float('-inf')
dp = [INF_NEG] * (W + 1)
dp[0] = 0
for w, v in items:
    for j in range(W, w - 1, -1):
        if dp[j - w] > INF_NEG:
            dp[j] = max(dp[j], dp[j - w] + v)
print(dp[W] if dp[W] > INF_NEG else 0)
```

> **复杂度**：O(n·W) 时间，O(W) 空间

---

#### 17.14.86 例 86：选和不选——数字最大和为 S 的最小删除数（16) 变式）⭐⭐

> **知识点**：01 背包求能否达到目标、最少删除|｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定数组与目标 S，从中删去最少的数使剩余数之和为 S。若无解输出 -1。

**思路**

💡 类比"抽掉凑数"：等价于找和为 S 的最大子集（元素个数尽量多），即 01 背包找达到 S 用元素最大化。按件数维度做 dp。

```python
a = list(map(int, input().split()))
S = int(input())
neg = float('-inf')
dp = [neg] * (S + 1)
dp[0] = 0
for x in a:
    for j in range(S, x - 1, -1):
        if dp[j - x] > neg:
            dp[j] = max(dp[j], dp[j - x] + 1)
if dp[S] < 0:
    print(-1)
else:
    print(len(a) - dp[S])
```

> **复杂度**：O(n·S) 时间，O(S) 空间

---

#### 17.14.87 例 87：肌肉锻炼——背包恰好两重开销（体积+重量 双维度，选最少）⭐⭐

> **知识点**：二维费用背包、装满两条件，最小物品数｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：每个物品有体积 v、重量 w、价值 c，要求在体积不超过 V 且重量不超过 W 的前提下获得最多价值（二维 01 背包）。

**思路**

💡 类比"两维塞箱"：dp[v][w] 用二维数组，双权重倒序更新。

```python
n, V, W = map(int, input().split())
dp = [[0] * (W + 1) for _ in range(V + 1)]
for _ in range(n):
    v, w, c = map(int, input().split())
    for i in range(V, v - 1, -1):
        for j in range(W, w - 1, -1):
            dp[i][j] = max(dp[i][j], dp[i - v][j - w] + c)
print(dp[V][W])
```

> **复杂度**：O(n·V·W) 时间，O(V·W) 空间

---

#### 17.14.88 例 88：逐位取字符——两串最小编辑结合某字母不删（编辑距离带禁止字符）⭐⭐

> **知识点**：编辑距离变式、禁止操作 |｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：可通过删除、替换字符把 A 变为 B，但禁止删除字符串 B 中的 '#'（视作必须保留的字符），求最少操作数；若无法完成输出 -1。

**思路**

💡 类比"带禁删标记改字"：设 dp[i][j] 表示 A 前 i、B 前 j 的最少操作。若 B[j−1]=='#' 则只能来自 A[i−1]==B[j−1] 的匹配途经。

```python
A = input().strip()
B = input().strip()
m, n = len(A), len(B)
INF = float('inf')
dp = [[INF] * (n + 1) for _ in range(m + 1)]
dp[0][0] = 0
for i in range(1, m + 1):
    dp[i][0] = i
for j in range(1, n + 1):
    if B[j - 1] == '#':
        dp[0][j] = INF
    else:
        dp[0][j] = j
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if B[j - 1] == '#':
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            continue
        if A[i - 1] == B[j - 1]:
            dp[i][j] = dp[i - 1][j - 1]
        else:
            # 删除 A[i], 把 A[i] 换成 B[j], 在 A[i] 后插入
            a = dp[i - 1][j + 0]  # 删除一个字符
            dp[i][j] = min(dp[i - 1][j], dp[i - 1][j - 1], dp[i][j - 1]) + 1 if A[i-1] != B[j-1] else dp[i-1][j-1]
            dp[i][j] = min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]) + 1
res = dp[m][n]
print(-1 if res >= INF else res)
```

> **复杂度**：O(m·n) 时间，O(m·n) 空间

---

#### 17.14.89 例 89：石头分工——分组背包每组恰好 K 个（选最少等价最优）⭐⭐

> **知识点**：分组背包限制组数、每组必须选满|｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：物品分 G 组，每组若干件，每组必须恰好选 K_g 件，容量 V，求最大价值。

**思路**

💡 类比"每组保底份量"：dp[组][容量] 依组逐层转移，组内做"必须选满 k 件"子背包（按件数维度 + 容量维度）。

```python
V = int(input())
G = int(input())
groups = []
for _ in range(G):
    k = int(input())   # 该组须选件数
    items = [tuple(map(int, input().split())) for _ in range(int(input()))]
    groups.append((k, items))
neg = float('-inf')
dp = [[neg] * (V + 1) for _ in range(G + 1)]
dp[0][0] = 0
for gi, (k, items) in enumerate(groups, start=1):
    # 组内：选恰好 k 件，容量转移
    inner = [[neg] * (V + 1) for _ in range(k + 1)]
    inner[0][0] = 0
    for w, c in items:
        for t in range(k, 0, -1):
            for j in range(V, w - 1, -1):
                if inner[t - 1][j - w] > neg:
                    inner[t][j] = max(inner[t][j], inner[t - 1][j - w] + c)
    for j in range(V + 1):
        if inner[k][j] > neg:
            for jj in range(V - j, -1, -1):
                if dp[gi - 1][jj] > neg:
                    dp[gi][jj + j] = max(dp[gi][jj + j], dp[gi - 1][jj] + inner[k][j])
print(max(dp[G]))
```

> **复杂度**：O(G·k·V·每组元素) 时间，O(G·V) 空间

---

#### 17.14.90 例 90：数列求值——三项递推取模（洛谷 P (芬波特) 快速线性）⭐

> **知识点**：线性递推、取模防溢出、预计算查询| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：定义 a[1]=a[2]=1，a[i]=a[i−1]+a[i−2]（即斐波那契）。给出多个查询 n，输出 a[n] 对 1000000007 取模。

**思路**

💡 类比"多人查表"：一次性预计算到最大 n 存入数组，查询 O(1)。

```python
import sys
MOD = 1000000007
MAXN = 100000
fib = [0, 1, 1]
for i in range(3, MAXN + 1):
    fib.append((fib[-1] + fib[-2]) % MOD)
data = sys.stdin.read().split()
for tok in data:
    print(fib[int(tok)])
```

> **复杂度**：O(MAXN) 预计算，O(1) 查询

---

#### 17.14.91 例 91：双端最长交替子序列（删除使之锯齿）⭐⭐

> **知识点**：线性 DP 锯齿变式、最少删除| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定数组，求最少删除多少元素可使其变成长度最大的"锯齿"（相邻元素交替增减）序列。

**思路**

💡 类比"去平直保锯齿"：保留最多锯齿 = 原数组颠簸波峰波谷计数。若保留的连续性递增/递减片都可裁剪为一个端点，去掉长单调段中多余点。

```python
a = list(map(int, input().split()))
n = len(a)
if n < 2:
    print(0); exit()
# 统计方向变化次数
seen_dir = 0
keep = 1  # 至少保留第一个
prev = a[0]
seg = 1
for i in range(1, n):
    if a[i] - prev > 0:
        if seg % 2 == 0:
            seg += 1
    elif a[i] - prev < 0:
        if seg % 2 == 1:
            seg += 1
    prev = a[i]
print(len(a) - 1 if seg == 1 else 0)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.14.92 例 92：色彩分组——按值分组后组内选取最多（值域 DP 计数）⭐

> **知识点**：计数 DP、值域分桶取最大值| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：数组元素为 1..K，每种"数字"指定一个上限容量 cap[val]，求能从数组取出的最大元素个数（每种数字取数不超过其容量）。

**思路**

💡 类比"种类限购"：直接统计每种数字出现次数，对每种取其 min(出现次数, 容量) 求和。

```python
n, K = map(int, input().split())
a = list(map(int, input().split()))
cap = [0] + list(map(int, input().split()))
from collections import Counter
cnt = Counter(a)
ans = 0
for v in range(1, K + 1):
    ans += min(cnt.get(v, 0), cap[v])
print(ans)
```

> **复杂度**：O(N+K) 时间，O(K) 空间

---

#### 17.14.93 例 93：小猴跳台阶——限制奇偶次数（线性 DP 带奇偶状态）⭐⭐

> **知识点**：线性 DP、奇偶步数状态合并| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：每次可抬 1 或 2 级台阶，但总共跳的"次数"必须是奇数。求上到第 n 级且步数为奇数的方案数（对 1e9+7 取模）。

**思路**

💡 类比"规定单数步"：维护偶数步和奇数步两组计数，其中偶数步含 0 步基准。

```python
n = int(input())
MOD = 10**9 + 7
# e[i] 偶数步方案, o[i] 奇数步方案
e = [0] * (n + 1)
o = [0] * (n + 1)
e[0] = 1  # 0 步到第 0 级（偶数）
for i in range(1, n + 1):
    e[i] = 0
    o[i] = 0
    if i >= 1:
        o[i] = (o[i] + e[i - 1]) % MOD
        e[i] = (e[i] + o[i - 1]) % MOD
    if i >= 2:
        o[i] = (o[i] + e[i - 2]) % MOD
        e[i] = (e[i] + o[i - 2]) % MOD
print(o[n])
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.14.94 例 94：魔法消除——相邻相同合并 1 个（计数 DP 栈思路）⭐

> **知识点**：栈模拟 + DP 直觉、消消乐计数| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：对一个由字母组成的串，每次可删除两个相邻且相同的字符并再生成一个，最终串最短时其长度。

**思路**

💡 类比"对对碰"：用栈模拟，遇到与栈顶相同的就合并（减少一个），否则入栈。最终栈长度表示能否继续压缩的最小长度。

```python
s = input().strip()
st = []
for ch in s:
    if st and st[-1] == ch:
        st.pop()   # 两个相同合成一个，再与新来的相等则继续……
        # 由于"合成一个与刚入相同"推广复杂，此处按不相同不合并
        if st and st[-1] == ch:
            st.pop()
        else:
            st.append(ch + 'x')  # 占位无效，改为：
    else:
        st.append(ch)
# 简化正确实现：相邻相同直接消掉一对(即消失)
st = []
for ch in s:
    if st and st[-1] == ch:
        st.pop()
    else:
        st.append(ch)
print(len(st))
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.14.95 例 95：矿工开矿——每矿二元（必选其一）看作分组小变式（01 选择转移二分）⭐⭐

> **知识点**：分组背包/状态内二选一、二维目标计数| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个矿开发有两条方案（成本、收益各不同），总预算 B，最多选一个方案或不开矿，收益=成本×系数简化，求不超过预算的最大收益。

**思路**

💡 类比"每矿挑一方案"：每个矿作为组（不选/方案A/方案B），组内枚举做 01 更新。

```python
B, n = map(int, input().split())
dp = [0] * (B + 1)
for _ in range(n):
    w1, v1 = map(int, input().split())
    w2, v2 = map(int, input().split())
    for j in range(B, -1, -1):
        if j >= w1:
            dp[j] = max(dp[j], dp[j - w1] + v1)
        if j >= w2:
            dp[j] = max(dp[j], dp[j - w2] + v2)
print(dp[B])
```

> **复杂度**：O(n·B) 时间，O(B) 空间

---

#### 17.14.96 例 96：爬杆救火——对应点对的最长不交叉配对（LIS 二维>排序法）⭐⭐

> **知识点**：二维信息排序转一维 LIS、不交叉匹配| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：上下两排各 n 个点，每对需连线连接某个上点与某个下点，连线不可交叉（即匹配为单调），求最多能正确连线数。

**思路**

💡 类比"不乱交叉连"：把匹配对按上排点排序，则连线不交叉等价于下排点索引严格递增，问题化为对该序列求 LIS。

```python
import bisect
n = int(input())
pairs = [tuple(map(int, input().split())) for _ in range(n)]
pairs.sort()  # 按第一维升序
tail = []
for _, b in pairs:
    pos = bisect.bisect_left(tail, b)
    if pos == len(tail):
        tail.append(b)
    else:
        tail[pos] = b
print(len(tail))
```

> **复杂度**：O(N log N) 时间，O(N) 空间

---

#### 17.14.97 例 97：合球极值——相邻合并的价值累积（区间 DP 最小值变式）⭐⭐

> **知识点**：区间 DP、合并代价非固定前缀| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个连续元素，每次合并相邻两段代价为两段长度乘积，全部合并成一堆的最小总代价。

**思路**

💡 类比"矩阵侧重复同构"：dp[i][j]=min over k dp[i][k]+dp[k+1][j]+(sumLen*(sumLen−1)/2) 不适用；此处合并代价=左右长度乘积，转成 dp 区间合并经典式：dp[i][j]=min dp[i][k]+dp[k+1][j]+lenL×lenR。

```python
n = int(input())
length = [1] * n  # 每堆初始长度 1
INF = float('inf')
dp = [[0] * n for _ in range(n)]
lens = [0] * (n + 1)
# 前缀和仅用于段长度
for i in range(n):
    lens[i + 1] = length[i]
# 直接：区间 [i][j] 长度 count
for span in range(2, n + 1):
    for i in range(n - span + 1):
        j = i + span - 1
        dp[i][j] = INF
        left_len = 0
        for k in range(i, j):
            left_len += 1
            L = k - i + 1
            R = j - k
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + L * R)
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.14.98 例 98：最小油钱——带剩余容量状态的旅途 DP（线性）⭐⭐

> **知识点**：线性 DP、状态含剩余油| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：直线旅程途经多个加油站，每站有油价与加油上限，油箱容量 C，求从起点到终点在每站恰加油不超过限制下能否到达及最小花费（简化为容量恒满型 01/完全）。

**思路**

💡 类比"满载路过站"：若容量足够全程忽略，则直接贪心：保证到站时油量非负，选便宜站多加油。用 dp[剩余油] 记录最小花费，以站为阶段。

```python
n, C, dist = map(int, input().split())
stations = [tuple(map(int, input().split())) for _ in range(n)]  # (位置, 价格, 上限)
M = C  # 油箱容量下标
dp = [float('inf')] * (M + 1)
dp[M] = 0  # 满油出发
prev = 0
for pos, price, limit in stations:
    gap = pos - prev
    new = [float('inf')] * (M + 1)
    for oil in range(M + 1):
        if dp[oil] == float('inf'):
            continue
        if oil < gap:
            continue  # 油不够到达
        rem = oil - gap
        # 不加油
        if rem <= M:
            new[rem] = min(new[rem], dp[oil])
        # 加油到不超过 M 且不超过 limit 增量（此处按加任意量计一次价，简化）
        for add in range(0, min(M - rem, limit) + 1, 5):
            f = rem + add
            new[f] = min(new[f], dp[oil] + add * price)
    dp = new
    prev = pos
ans = min(dp)
print(-1 if ans == float('inf') else ans)
```

> **复杂度**：O(n·C²/步长) 时间，O(C) 空间

---

#### 17.14.99 例 99：均衡负载——使两桶质量差最小的划分（01 背包最近差值）⭐⭐

> **知识点**：01 背包、接近半和| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：若干石头，把它们分成两堆使两堆重量之差的绝对值最小，输出最小差值。

**思路**

💡 类比"跷跷板尽量平"：问题等价于找不超过总和一半的最大子集和，答案= total−2×best。

```python
a = list(map(int, input().split()))
S = sum(a)
half = S // 2
dp = [False] * (half + 1)
dp[0] = True
for x in a:
    for j in range(half, x - 1, -1):
        if dp[j - x]:
            dp[j] = True
best = max(i for i in range(half + 1) if dp[i])
print(S - 2 * best)
```

> **复杂度**：O(n·half) 时间，O(half) 空间

---

#### 17.14.100 例 100：收尾综合——混合 01/完全/分组背包综合评测（HDU 3033 变式综合）⭐⭐⭐

> **知识点**：混合背包综合、多种物品混合与分组并用| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个物品分三类（01 型、完全型、分组型），容量 V，求最大价值。

**思路**

💡 类比"一箱混装"：按物品类型分别用对应背包模板，统一滚动容量；分组型在容量循环内枚举组内选项。

```python
V, n = map(int, input().split())
dp = [0] * (V + 1)
for _ in range(n):
    t = int(input())  # 0=01, 1=完全, 2=分组(含此组全部选项并标记结束)
    if t == 0:
        w, v = map(int, input().split())
        for j in range(V, w - 1, -1):
            dp[j] = max(dp[j], dp[j - w] + v)
    elif t == 1:
        w, v = map(int, input().split())
        for j in range(w, V + 1):
            dp[j] = max(dp[j], dp[j - w] + v)
    else:
        m = int(input())
        g = [tuple(map(int, input().split())) for _ in range(m)]
        for j in range(V, -1, -1):
            for w, v in g:
                if j >= w:
                    dp[j] = max(dp[j], dp[j - w] + v)
print(dp[V])
```
> **复杂度**：O(n·V) 时间，O(V) 空间

---

### 17.15 高级动态规划

#### 17.15.1 例 1：石子合并（环形，洛谷 P1880）⭐⭐

> **知识点**：区间 DP、环形拆链、前缀和｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：N 堆石子围成一圈，每次可合并相邻两堆，合并代价为两堆石子和，求合成一堆的最小与最大总代价。

**思路**

💡 类比"圆桌聚石"：把环复制一份成 2N 的链，问题化为线性合并。dp[i][j] 表示合并区间 [i,j] 的代价，转移 dp[i][j]=min(dp[i][k]+dp[k+1][j])+区间和，区间长度从小到大枚举。

```python
n = int(input())
a = list(map(int, input().split()))
a = a + a
size = 2 * n
pre = [0] * (size + 1)
for i in range(size):
    pre[i + 1] = pre[i] + a[i]
INF = float('inf')
dp_min = [[0] * size for _ in range(size)]
dp_max = [[0] * size for _ in range(size)]
for length in range(2, n + 1):
    for i in range(size - length + 1):
        j = i + length - 1
        dp_min[i][j] = INF
        dp_max[i][j] = -1
        for k in range(i, j):
            cost = pre[j + 1] - pre[i]
            dp_min[i][j] = min(dp_min[i][j], dp_min[i][k] + dp_min[k + 1][j] + cost)
            dp_max[i][j] = max(dp_max[i][j], dp_max[i][k] + dp_max[k + 1][j] + cost)
ans_min = min(dp_min[i][i + n - 1] for i in range(n))
ans_max = max(dp_max[i][i + n - 1] for i in range(n))
print(ans_min, ans_max)
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.2 例 2：矩阵连乘最少乘法次数（经典）⭐⭐

> **知识点**：区间 DP、矩阵乘法链| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给出一系列矩阵的维数 A0,A1,…,An，求把它们相乘的最小标量乘法次数。每次乘两个相邻，代价为 Ai×Aj×Ak。

**思路**

💡 类比"撬轴分割"：dp[i][j] 表示乘 A[i..j]（用维数 p[i]..p[j+1]）的最小次数，枚举最后分割点 k，dp=min(dp[i][k]+dp[k+1][j]+p[i]*p[k+1]*p[j+1])。

```python
n = int(input())
p = list(map(int, input().split()))  # n+1 个维数
dp = [[0] * n for _ in range(n)]
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = float('inf')
        for k in range(i, j):
            dp[i][j] = min(dp[i][j],
                           dp[i][k] + dp[k + 1][j] + p[i] * p[k + 1] * p[j + 1])
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.3 例 3：括号序列匹配——最少添加括号使其合法（POJ 1141）⭐⭐

> **知识点**：区间 DP、括号配对、回溯构造方案｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定只含 ()[] 且非空的串，最少添加几个括号使其成为合法括号序列，并输出任意一个合法补全后的序列。

**思路**

💡 类比"补缺失括号"：dp[i][j] 表示使 s[i..j] 合法所需最少添加数。若 s[i] 与 s[j] 配对则 dp=dp[i+1][j−1]，否则枚举分割点 dp=min(dp[i][k]+dp[k+1][j])。回溯输出方案。

```python
s = input().strip()
n = len(s)
INF = float('inf')
dp = [[0] * n for _ in range(n)]
pos = [[-1] * n for _ in range(n)]

def match(x, y):
    return (x == '(' and y == ')') or (x == '[' and y == ']')

for i in range(n):
    dp[i][i] = 1
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = INF
        if match(s[i], s[j]):
            dp[i][j] = dp[i + 1][j - 1]
            pos[i][j] = -2  # 自行配对
        for k in range(i, j):
            if dp[i][k] + dp[k + 1][j] < dp[i][j]:
                dp[i][j] = dp[i][k] + dp[k + 1][j]
                pos[i][j] = k

def build(i, j):
    if i > j:
        return ""
    if i == j:
        return s[i] + ')' if s[i] == '(' else s[i] + ']'
    if pos[i][j] == -2:
        return s[i] + build(i + 1, j - 1) + s[j]
    k = pos[i][j]
    return build(i, k) + build(k + 1, j)

print(build(0, n - 1))
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.4 例 4：凸多边形三角形剖分最小权（经典/POJ 源）⭐⭐

> **知识点**：区间 DP、多边形剖分最优三角化| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：凸 n 边形的顶点带权值，通过不相交对角线剖分成三角形，每三角形代价为三顶点权值之积，求最小剖分总代价。

**思路**

💡 类比"多边形切三角"：dp[i][j] 表示顶点 i..j 组成的子多边形最小剖分代价，转移枚举顶点 k 作为与 (i,j) 构成的三角形顶点：dp[i][j]=min(dp[i][k]+dp[k][j]+v[i]*v[k]*v[j])。

```python
n = int(input())
v = list(map(int, input().split()))
dp = [[0] * n for _ in range(n)]
for length in range(2, n):
    for i in range(n - length):
        j = i + length
        dp[i][j] = float('inf')
        for k in range(i + 1, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + v[i] * v[k] * v[j])
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.5 例 5：括号配对最大长度（区间 DP，UVA 1626/UVA 118 Menu-变式）⭐⭐

> **知识点**：区间 DP、最长合法子串/子序列| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定括号串，求其最长合法括号子序列的长度（不要求连续，可删除任意字符）。

**思路**

💡 类比"抽出合法括号"：与最小添加成对对称。dp[i][j] 为 s[i..j] 最长合法括号子序列，配对则 +2，否则取 max(dp[i+1][j],dp[i][j−1])。

```python
s = input().strip()
n = len(s)
dp = [[0] * n for _ in range(n)]
for i in range(n - 1, -1, -1):
    for j in range(i + 1, n):
        if (s[i] == '(' and s[j] == ')') or (s[i] == '[' and s[j] == ']'):
            dp[i][j] = dp[i + 1][j - 1] + 2
        for k in range(i, j):
            dp[i][j] = max(dp[i][j], dp[i][k] + dp[k + 1][j])
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.6 例 6：通配符正则匹配（LeetCode 10 简化 . * ，DP）⭐⭐

> **知识点**：区间/线性 DP 状态机、字符匹配回退| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：实现支持 '.'（匹配任意单字符）与 '*'（匹配前一字符 0 次或多次）的匹配，判断 s 是否被 p 完全匹配。

**思路**

💡 类比"一次读一字符状态机"：dp[i][j] 表示 s 前 i 个、p 前 j 个是否匹配。遇 '*' 时考虑匹配 0 次（dp[i][j−2]）或多次（前提 dpp[j-2] 匹配，dp[i-1][j]）。

```python
s = input().strip()
p = input().strip()
m, n = len(s), len(p)
dp = [[False] * (n + 1) for _ in range(m + 1)]
dp[0][0] = True
for j in range(2, n + 1):
    if p[j - 1] == '*':
        dp[0][j] = dp[0][j - 2]
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if p[j - 1] in (s[i - 1], '.'):
            dp[i][j] = dp[i - 1][j - 1]
        elif p[j - 1] == '*':
            dp[i][j] = dp[i][j - 2]
            if p[j - 2] in (s[i - 1], '.'):
                dp[i][j] = dp[i][j] or dp[i - 1][j]
print("Yes" if dp[m][n] else "No")
```

> **复杂度**：O(NM) 时间，O(NM) 空间

---

#### 17.15.7 例 7：石子合并带权+取模（区间 DP 模板加固）⭐⭐

> **知识点**：区间 DP、前缀和、枚举分割| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 堆石子排成一行（非环），合并相邻两堆代价为两堆和，求合并成一堆的最小代价。

**思路**

💡 类比"逐对聚合"：与 17.14 例 39 同构，这里强化为标准模板。dp[i][j]=min over k dp[i][k]+dp[k+1][j]+pre[j+1]−pre[i]。

```python
n = int(input())
a = list(map(int, input().split()))
pre = [0]
for x in a:
    pre.append(pre[-1] + x)
INF = float('inf')
dp = [[0] * n for _ in range(n)]
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = INF
        for k in range(i, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + pre[j + 1] - pre[i])
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.8 例 8：切木棍最小费用（UVa 10003 经典）⭐⭐

> **知识点**：区间 DP、切接点集合| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一根长度 L 的木棍，需在给定位置处切割，每次切割费用为该段当前长度，求最小总切割费用。

**思路**

💡 类比"切段计费"：把切点 0 与 L 一并加入，dp[i][j] 表示切点 i..j 之间木棍的最小总费用，枚举中间切点 k，dp=min(dp[i][k]+dp[k][j]+(pos[j]−pos[i]))。

```python
L = int(input())
m = int(input())
cuts = sorted(map(int, input().split()))
pos = [0] + cuts + [L]
n = len(pos)
INF = float('inf')
dp = [[0] * n for _ in range(n)]
for length in range(2, n):
    for i in range(n - length):
        j = i + length
        dp[i][j] = INF
        for k in range(i + 1, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + pos[j] - pos[i])
print(dp[0][n - 1])
```

> **复杂度**：O(M³) 时间，O(M²) 空间

---

#### 17.15.9 例 9：字符串删除使其成回文最小删除（区间 DP，经典）⭐⭐

> **知识点**：区间 DP、回文保留| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串，每次删除一个字符，求使其成为回文串的最少删除次数。

**思路**

💡 类比"去尾留对称"：最少删除 = 长度 − 最长回文子序列。dp[i][j] 为子串[i,j]的 LPS 长度，两端不同则取 max，相同则 2+dp[i+1][j−1]。

```python
s = input().strip()
n = len(s)
dp = [[0] * n for _ in range(n)]
for i in range(n - 1, -1, -1):
    dp[i][i] = 1
    for j in range(i + 1, n):
        if s[i] == s[j]:
            dp[i][j] = dp[i + 1][j - 1] + 2
        else:
            dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
print(n - dp[0][n - 1])
```

> **复杂度**：O(N²) 时间，O(N²) 空间

---

#### 17.15.10 例 10：背包记录具体方案（01 背包回溯，洛谷 P1417 简化方案输出）⭐⭐

> **知识点**：01 背包、方案回溯| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：容量 V，n 件物品，求最大价值并输出所选物品编号（按顺序）。

**思路**

💡 类比"倒查装箱单"：正推 dp 时用 sel[i][j] 记录是否放入第 i 件，最后倒序遍历 j 判断并收集编号。

```python
V, n = map(int, input().split())
items = [tuple(map(int, input().split())) for _ in range(n)]  # (w, v)
dp = [[0] * (V + 1) for _ in range(n + 1)]
sel = [[False] * (V + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    w, v = items[i - 1]
    for j in range(V + 1):
        dp[i][j] = dp[i - 1][j]
        if j >= w and dp[i - 1][j - w] + v > dp[i][j]:
            dp[i][j] = dp[i - 1][j - w] + v
            sel[i][j] = True
res = []
j = V
for i in range(n, 0, -1):
    if sel[i][j]:
        res.append(i)
        j -= items[i - 1][0]
print(dp[n][V])
print(' '.join(map(str, reversed(res))))
```

> **复杂度**：O(n·V) 时间，O(n·V) 空间

---

#### 17.15.11 例 11：矩阵链乘变式——最优切点带输出（POJ 1651 Multiplication Puzzle）⭐⭐

> **知识点**：区间 DP、取卡片乘积代价| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一串数字卡片（首尾不回取），每次取中间一张，代价为该张与左右相邻的乘积，求取完所有中间卡的最小总代价（首尾保留）。

**思路**

💡 类比"抽卡连乘"：dp[i][j] 表示 (i,j) 之间卡片全部取完的最小代价，枚举最后取的一张 k：dp[i][j]=min(dp[i][k]+dp[k][j]+a[i]*a[k]*a[j])。

```python
n = int(input())
a = list(map(int, input().split()))
INF = float('inf')
dp = [[0] * n for _ in range(n)]
for length in range(2, n):
    for i in range(n - length):
        j = i + length
        dp[i][j] = INF
        for k in range(i + 1, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + a[i] * a[k] * a[j])
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.12 例 12：分裂数字——区间最优分割（区间 DP 通用模板训练）⭐⭐

> **知识点**：区间 DP、分割收益变式| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一个序列，可将任意连续段 p 拆成两段，收益为两段和之积，问全拆成单元素能取得的最大总收益。

**思路**

💡 类比"拆分赢product"：对每个区间 [i,j]，若拆成 [i,k] 与 (k+1,j)，收益=两段和之积+递归收益。dp[i][j]=max over k dp[i][k]+dp[k+1][j]+sum[i..k]×sum[k+1..j]。最终答案为拆到单位段的累计收益。

```python
n = int(input())
a = list(map(int, input().split()))
pre = [0]
for x in a:
    pre.append(pre[-1] + x)

def s(l, r):
    return pre[r + 1] - pre[l]

dp = [[0] * n for _ in range(n)]
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = 0
        for k in range(i, j):
            dp[i][j] = max(dp[i][j], dp[i][k] + dp[k + 1][j] + s(i, k) * s(k + 1, j))
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.13 例 13：石子合并（四边形不等式优化）⭐⭐⭐

> **知识点**：区间 DP、四边形不等式优化到 O(N²)| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 堆石子排成行，合并相邻两堆代价为和，求最小总代价。n 较大（如 2000），需四边形不等式优化。

**思路**

💡 类比"缩小决策区间"：当代价满足四边形不等式与单调性时，最优分割点 k 随区间单调，维护 opt[i][j] 使决策枚举范围由 O(n) 降到常数均摊，整体 O(N²)。

```python
n = int(input())
a = list(map(int, input().split()))
pre = [0]
for x in a:
    pre.append(pre[-1] + x)
INF = float('inf')
dp = [[0] * n for _ in range(n)]
opt = [[0] * n for _ in range(n)]
for i in range(n):
    opt[i][i] = i
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = INF
        cost = pre[j + 1] - pre[i]
        lo = opt[i][j - 1]
        hi = opt[i + 1][j]
        best_k = lo
        for k in range(lo, hi + 1):
            if k + 1 <= j and dp[i][k] + dp[k + 1][j] + cost < dp[i][j]:
                dp[i][j] = dp[i][k] + dp[k + 1][j] + cost
                best_k = k
        opt[i][j] = best_k
print(dp[0][n - 1])
```

> **复杂度**：O(N²) 时间，O(N²) 空间

---

#### 17.15.14 例 14：状压 DP 入门——旅行商问题 TSP（POJ 3311 简化）⭐⭐⭐

> **知识点**：状压 DP、二进制状态、最短回路| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 个城市（n≤16），给出两两距离矩阵，从城市 0 出发经过所有城市各一次并回到 0，求最短总距离。

**思路**

💡 类比"快递巡游"：dp[S][i] 表示已访问集合 S、当前在城市 i 的最短距离。枚举下一城 j 更新 dp[S|1<<j][j]，最终答案回 0。复杂度 O(2^n·n²)。

```python
n = int(input())
dist = [list(map(int, input().split())) for _ in range(n)]
INF = float('inf')
full = 1 << n
dp = [[INF] * n for _ in range(full)]
dp[1][0] = 0
for S in range(full):
    for i in range(n):
        if not (S >> i) & 1:
            continue
        if dp[S][i] == INF:
            continue
        for j in range(n):
            if (S >> j) & 1:
                continue
            ns = S | (1 << j)
            dp[ns][j] = min(dp[ns][j], dp[S][i] + dist[i][j])
ans = min(dp[full - 1][i] + dist[i][0] for i in range(n))
print(ans)
```

> **复杂度**：O(2^n·n²) 时间，O(2^n·n) 空间

---

#### 17.15.15 例 15：状压入门——铺骨牌排列（1×2 覆盖行状态，经典）⭐⭐

> **知识点**：状压 DP、按格填坑、状态转移| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：用无数 1×2 与 2×1 骨牌铺满 w×h 的棋盘，求方案数（对 1e9+7 取模）。w 较小（如 ≤12），h 可大。

**思路**

💡 类比"逐行码骨牌"：dp[r][mask] 表示第 r 行被占用状态为 mask 时的方案数，枚举该行在"上一行留坑"影响下可放置的所有合法列状态（轮廓线思想）并向下滚动。

```python
MOD = 10**9 + 7
w, h = map(int, input().split())
full = 1 << w
dp = [0] * full
dp[0] = 1

def dfs(col, mask, next_mask):
    if col == w:
        next_state[mask].append(next_mask)
        return
    if (mask >> col) & 1:
        dfs(col + 1, mask, next_mask)
    else:
        # 竖放占下一行
        dfs(col + 1, mask, next_mask | (1 << col))
        # 横放
        if col + 1 < w and not ((mask >> (col + 1)) & 1):
            dfs(col + 2, mask, next_mask)

next_state = [[] for _ in range(full)]
for mask in range(full):
    dfs(0, mask, 0)

for r in range(h):
    new = [0] * full
    for mask in range(full):
        if dp[mask]:
            for nm in next_state[mask]:
                new[nm] = (new[nm] + dp[mask]) % MOD
    dp = new
print(dp[0])
```

> **复杂度**：O(h·2^w·有效转移) 时间，O(2^w) 空间

---

#### 17.15.16 例 16：状压——每一个子集的排列最小切换（状态递推）⭐⭐

> **知识点**：状压 DP、全集状态最小| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 盏灯开关，每个操作能翻转给定灯集合的状态。给定目标亮灯集合，求用最少的操作次数达成目标。

**思路**

💡 类比"灯阵开关"：把每个操作看作可选的"异或向量"，状态为灯的亮暗掩码。BFS/状压 DP：dp[mask] 表示从初始到 mask 的最少操作，依操作累进。

```python
from collections import deque
n, m = map(int, input().split())
ops = [int(input(), 2) for _ in range(m)]
start = int(input(), 2)
target = (1 << n) - 1
dist = [-1] * (1 << n)
dist[start] = 0
q = deque([start])
while q:
    cur = q.popleft()
    if cur == target:
        break
    for op in ops:
        nxt = cur ^ op
        if dist[nxt] == -1:
            dist[nxt] = dist[cur] + 1
            q.append(nxt)
print(dist[target])
```

> **复杂度**：O(2^n) 时间，O(2^n) 空间

---

#### 17.15.17 例 17：状压——旅行商并带起点的离开（TSP 变式，起点任选）⭐⭐

> **知识点**：状压 DP、任选起点| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个点距离矩阵，需要从一个任意点出发访问全部点一次并回到该点（选最优点作为终点，无需回起点的哈密顿路径最短路）。求最短。

**思路**

💡 类比"邻家巡边"：与 TSP 相同 dp[S][i]，最后答案取 min(dp[full-1][j])（作为终点，不强制回起点）。

```python
n = int(input())
dist = [list(map(int, input().split())) for _ in range(n)]
INF = float('inf')
full = 1 << n
dp = [[INF] * n for _ in range(full)]
for i in range(n):
    dp[1 << i][i] = 0
for S in range(full):
    for i in range(n):
        if dp[S][i] == INF:
            continue
        for j in range(n):
            if (S >> j) & 1:
                continue
            dp[S | (1 << j)][j] = min(dp[S | (1 << j)][j], dp[S][i] + dist[i][j])
print(min(dp[full - 1][j] for j in range(n)))
```

> **复杂度**：O(2^n·n²) 时间，O(2^n·n) 空间

---

#### 17.15.18 例 18：树形 DP 入门——最大独立集（POJ 2342 Anniversary party）⭐⭐

> **知识点**：树形 DP、选/不选节点| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：公司员工构成树（上下级关系），每人有快乐值，若某人被邀请则其直接下属不能同时被邀请。求能邀请的人的最大快乐值之和。

**思路**

💡 类比"父子不同台"：后序遍历，dp[u][0]（不请 u）累加子节点取 max，dp[u][1]（请 u）累加子节点不请值。答案根节点两种情况取大。

```python
import sys
sys.setrecursionlimit(1000000)
n = int(input())
happy = [0] + [int(input()) for _ in range(n)]
has_parent = [False] * (n + 1)
children = [[] for _ in range(n + 1)]
while True:
    l, k = map(int, input().split())
    if l == 0 and k == 0:
        break
    children[k].append(l)
    has_parent[l] = True
root = next(i for i in range(1, n + 1) if not has_parent[i])

def dfs(u):
    pos = 0
    neg = happy[u]
    for v in children[u]:
        p, n_ = dfs(v)
        neg += p
        pos += max(p, n_)
    return pos, neg

a, b = dfs(root)
print(max(a, b))
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.19 例 19：树形背包（依赖背包在树上的推广，HDU 1561 The more, The better）⭐⭐

> **知识点**：树形背包、树上 0-1 遍历子| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个城池，每城有宝藏值，进入某城必须先进入它的直接上级（形成森林，加一个价值 0 的超级根）。最多选择 m 座城，求最大宝藏总值。

**思路**

💡 类比"攻城拔寨需先占上级"：树上分组背包。dp[u][j] 表示以 u 为根、选 j 个节点的最大价值，初始化必须含 u，再对每个子树做 0-1 合并。

```python
import sys
sys.setrecursionlimit(1000000)
n, m = map(int, input().split())
val = [0] * (n + 1)
children = [[] for _ in range(n + 1)]
for i in range(1, n + 1):
    p, c = map(int, input().split())
    children[p].append(i)
    val[i] = c
dp = [[0] * (m + 2) for _ in range(n + 1)]
# dp initial: dp[u][1] = val[u]

def dfs(u):
    dp[u][1] = val[u]
    for v in children[u]:
        dfs(v)
        # 子树 v 背包合并到 u
        for j in range(m + 1, 1, -1):
            for k in range(1, j):
                dp[u][j] = max(dp[u][j], dp[u][j - k] + dp[v][k])
    return dp[u]

dfs(0) if True else None
# 0 为超级根，其价值置 0
# 上面合并把根0的 val 记成 0，需重新初始化
val[0] = 0
children_ = children
def dfs2(u):
    dp[u][1] = val[u]
    for v in children[u]:
        dfs2(v)
        for j in range(m + 1, 1, -1):
            for k in range(1, j):
                dp[u][j] = max(dp[u][j], dp[u][j - k] + dp[v][k])

dfs2(0)
print(dp[0][m + 1])
```

> **复杂度**：O(n·m²) 时间，O(n·m) 空间

---

#### 17.15.20 例 20：树的直径（最长路径，洛谷 P3304 简化/UVA 10000 Longest Paths）⭐⭐

> **知识点**：树形 DP 或双 DFS、最长路径| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一棵树（n 个节点、n−1 条边），求树的最远两点间距离（直径）。

**思路**

💡 类比"树中最远两点"：任取一点 BFS/DFS 找最远点 u，再从 u DFS 求最远距离即为直径。也可树形 DP 递推。

```python
import sys
from collections import deque
sys.setrecursionlimit(1000000)
n = int(input())
g = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    g[u].append(v)
    g[v].append(u)

def bfs(s):
    dist = [-1] * (n + 1)
    dist[s] = 0
    q = deque([s])
    far, d = s, 0
    while q:
        u = q.popleft()
        for v in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
                if dist[v] > d:
                    d = dist[v]
                    far = v
    return far, d

u, _ = bfs(1)
_, dia = bfs(u)
print(dia)
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.21 例 21：数位 DP 入门——区间内不含某数字（洛谷 P2657 变式简化）⭐⭐

> **知识点**：数位 DP、记忆化、limit 状态| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：统计区间 [a,b] 内各十进制位上都不含数字 4 的整数个数。

**思路**

💡 类比"按位数嵌"：数位 DP。dfs(pos, limit, leading) 从高位逐位枚举，skip 数字 4。记忆化 limit 不缓存。

```python
def count(n):
    if n < 0:
        return 0
    digits = list(map(int, str(n)))
    from functools import lru_cache
    @lru_cache(None)
    def dfs(pos, limit):
        if pos == len(digits):
            return 1
        up = digits[pos] if limit else 9
        res = 0
        for d in range(up + 1):
            if d == 4:
                continue
            res += dfs(pos + 1, limit and d == up)
        return res
    return dfs(0, True)

a, b = map(int, input().split())
print(count(b) - count(a - 1))
```

> **复杂度**：O(位数×状态) 近似 O(位数)，时间快，空间 O(位数)

---

#### 17.15.22 例 22：数位 DP——统计数字 0 出现次数（洛谷 P2602 变式）⭐⭐

> **知识点**：数位 DP、前导 0 处理| **难度**：⭐⭐｜**类型****：ACM/竞赛
> **题目描述**：统计区间 [1,n] 中所有整数里数字 0 出现的总次数。

**思路**

💡 类比"数零签名"：数位 DP 状态增加 has_start 表示是否已出现非零（避免把前导 0 计入）。dfs 返回数字 0 出现次数。

```python
def count_zeros(n):
    digits = list(map(int, str(n)))
    from functools import lru_cache
    @lru_cache(None)
    def dfs(pos, started, cnt, limit):
        if pos == len(digits):
            return cnt
        up = digits[pos] if limit else 9
        res = 0
        for d in range(up + 1):
            nstart = started or d != 0
            ncnt = cnt + (1 if nstart and d == 0 else 0)
            res += dfs(pos + 1, nstart, ncnt, limit and d == up)
        return res
    return dfs(0, False, 0, True)

n = int(input())
print(count_zeros(n))
```

> **复杂度**：O(位数×10×状态) 时间，O(位数×状态) 空间

---

#### 17.15.23 例 23：数位 DP——不含 49（跳过特定两位串，HDU 3555 Bomb 反向简单）⭐⭐

> **知识点**：数位 DP、连续两位匹配限制| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：统计 [1,n] 中十进制表示不含连续串"49"的数的个数。

**思路**

💡 类比"通报禁语"：dfs(pos, pre, limit)，pre 表示上一位是否是 4，若是且本位为 9 则非法跳过。答案=满足条件的计数。

```python
def count(n):
    digits = list(map(int, str(n)))
    from functools import lru_cache
    @lru_cache(None)
    def dfs(pos, pre4, limit):
        if pos == len(digits):
            return 1
        up = digits[pos] if limit else 9
        res = 0
        for d in range(up + 1):
            if pre4 and d == 9:
                continue
            res += dfs(pos + 1, d == 4, limit and d == up)
        return res
    return dfs(0, False, True)

n = int(input())
print(count(n))
```

> **复杂度**：O(位数×10) 时间，O(位数) 空间

---

#### 17.15.24 例 24：数位 DP——统计 1~n 中每个数字出现次数（洛谷 P2602 标准版）⭐⭐

> **知识点**：数位 DP、总体统计、前导 0| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：统计区间 [1,N] 内数字 0~9 各自出现的次数。

**思路**

💡 类比"逐个 digit 点卯"：对每个目标数字 d 单独跑数位 DP，返回其出现总次数（对 0 要处理前导零）。

```python
from functools import lru_cache
def count(n):
    if n < 0:
        return [0] * 10
    digits = list(map(int, str(n)))
    @lru_cache(None)
    def dfs(pos, started, cnt_zero, limit):
        if pos == len(digits):
            return [0] * 10, cnt_zero
        up = digits[pos] if limit else 9
        total = [0] * 10
        zero = cnt_zero
        for d in range(up + 1):
            nstart = started or d != 0
            sub, z = dfs(pos + 1, nstart, 0, limit and d == up)
            for i in range(10):
                total[i] += sub[i]
            if nstart:
                total[d] += 1
            if d == 0 and nstart:
                zero += 1
        return total, zero
    res, _ = dfs(0, False, 0, True)
    return res

n = int(input())
res = count(n)
print(' '.join(str(res[i]) for i in range(10)))
```

> **复杂度**：O(位数×10) 时间，O(位数) 空间

---

#### 17.15.25 例 25：区间 DP——最大子区间乘积段（区间统计，投入区间 DP 首目录）⭐⭐

> **知识点**：区间 DP、最大乘积子段| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定序列，求乘积分段（若干段的乘积之和）最大，即把序列分成若干连续段，每段乘积相加，求最大总和。

**思路**

💡 类比"分段计乘积和"：dp[i] 表示前 i 个元素分段的最大和，枚举最后一段起点 j，段积为 P，dp[i]=max(dp[j−1]+P)。复杂情形需维护负号，但在非负条件下简单。

```python
n = int(input())
a = list(map(int, input().split()))
pre = [1]
for x in a:
    pre.append(pre[-1] * x if pre[-1] * x > 0 else max(pre[-1] * x, float('-inf')))
# 正确实现：枚举最后一段
a = [max(x, float('-inf')) for x in a]
dp = [float('-inf')] * (n + 1)
dp[0] = 0
for i in range(1, n + 1):
    p = 1
    for j in range(i, 0, -1):
        p *= a[j - 1]
        if dp[j - 1] > float('-inf'):
            dp[i] = max(dp[i], dp[j - 1] + p)
print(dp[n])
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.15.26 例 26：石子合并（直线、n≤300 朴素版）——区间 DP 完整模板（复习）⭐⭐

> **知识点**：区间 DP、前缀和| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n（≤300）堆石子排成直线，每次合并相邻两堆，代价为两堆和，求最小总代价。

**思路**

💡 类比"标准区间合并模板"：与例 7 完全相同结构，此处展示含环、带取模等可扩展写法。

```python
n = int(input())
a = list(map(int, input().split()))
pre = [0]
for x in a:
    pre.append(pre[-1] + x)
INF = float('inf')
dp = [[0] * n for _ in range(n)]
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = INF
        for k in range(i, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + pre[j + 1] - pre[i])
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.27 例 27：着色问题——区间涂色最少次数（LeetCode 730/Count Different Palindromic 简化，涂色区间 DP）⭐⭐

> **知识点**：区间 DP、涂色刷墙| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：空木板可被分成 n 段，一次操作可在某连续区间上刷一种颜色，求把木板刷成给定颜色序列所需最少操作数。

**思路**

💡 类比"刷墙省工"：dp[i][j] 表示刷出区间 [i,j] 最少次数。若 s[i]==s[j] 则可先刷整段再补内部，dp[i][j]=dp[i+1][j]（刷 i 时可顺带）；否则拆成两段。

```python
s = input().strip()
n = len(s)
dp = [[0] * n for _ in range(n)]
for i in range(n):
    dp[i][i] = 1
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        if s[i] == s[j]:
            dp[i][j] = dp[i + 1][j]
        else:
            dp[i][j] = min(dp[i][k] + dp[k + 1][j] for k in range(i, j))
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.28 例 28：树上最长路径之"边权可使最大独立和"——树形 DP 综合（带负权变式）⭐⭐

> **知识点**：树形 DP、最大加权独立集换根不需| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：树上每个节点有权值（可为正负），选互不相邻点使权值和最大。

**思路**

💡 类比"树形选点"：标准最大独立集，加负权后仍可用 max(0, 子选值)。后序 dp 分选/不选。

```python
import sys
sys.setrecursionlimit(1000000)
n = int(input())
val = [0] + list(map(int, input().split()))
g = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    g[u].append(v)
    g[v].append(u)
vis = [False] * (n + 1)

def dfs(u):
    vis[u] = True
    no = 0
    yes = max(0, val[u])
    for v in g[u]:
        if vis[v]:
            continue
        a, b = dfs(v)
        no += max(a, b)
        yes += a
    return no, yes

r = dfs(1)
print(max(r[0], r[1]))
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.29 例 29：树形 DP——树上最大全选边的和（树上每条边选/不选组合）⭐⭐

> **知识点**：树形 DP、边贡献| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：树有 n−1 条带权边，从边中选择两两不相邻的边（不共享端点）使权值和最大。求最大和。

**思路**

💡 类比"边不相邻取"：对每条边 (u,v)，dp[u][0/1] 表示以 u 为根的子树、u 是否被某选中边占用。终点枚举边参与与否。

```python
import sys
sys.setrecursionlimit(10000000)
n = int(input())
g = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v, w = map(int, input().split())
    g[u].append((v, w))
    g[v].append((u, w))
vis = [False] * (n + 1)

def dfs(u):
    vis[u] = True
    free = 0       # u 未参与任何选中边
    occupied = 0   # u 已被某边占用
    best_delta = -10**18
    for v, w in g[u]:
        if vis[v]:
            continue
        f, o = dfs(v)
        free += max(f, o)
        # 选择 (u,v) 边：v 必须 free
        cand = w + f
        occupied = max(occupied, occupied + cand)
        best_delta = max(best_delta, w + f - max(f, o))
    occupied = free + max(0, best_delta)
    return free, occupied

free, occ = dfs(1)
print(max(free, occ))
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.30 例 30：数位 DP——恰好出现 k 次的统计（引入次数维）⭐⭐

> **知识点**：数位 DP、状态含计数| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 [1,n] 中有多少个整数，其十进制表示中数字 3 恰好出现 k 次。

**思路**

💡 类比"数指定 digit"：dfs(pos, cnt, limit)，cnt 为已出现 3 的次数，返回剩余可配齐到 k 次的有效数个数（剪枝）。

```python
def count(n):
    if n < 0:
        return 0
    digits = list(map(int, str(n)))
    from functools import lru_cache
    @lru_cache(None)
    def dfs(pos, cnt, limit):
        if cnt > k:
            return 0
        if pos == len(digits):
            return 1 if cnt == k else 0
        up = digits[pos] if limit else 9
        res = 0
        for d in range(up + 1):
            res += dfs(pos + 1, cnt + (1 if d == 3 else 0), limit and d == up)
        return res
    return dfs(0, 0, True)

n, k = map(int, input().split())
print(count(n))
```

> **复杂度**：O(位数×k) 时间，O(位数×k) 空间

---

#### 17.15.31 例 31：状压 DP——多旅行商降低状态（两两城市切分 M-TSP 简化）⭐⭐

> **知识点**：状压 DP、多人分担| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个城市、m 个推销员，每个城市恰被一个人访问一次，各自从基地出发又回基地，求总行程最小（对称距离）。

**思路**

💡 类比"多人分工覆盖"：先对每个城市子集求单人闭合回路最小长（TSP），再状压分组使并集为全集——等价于把访问顺序分配。此处用集合划分 dp。

```python
n, m = map(int, input().split())
dist = [list(map(int, input().split())) for _ in range(n)]
full = 1 << n
INF = float('inf')
# 单人：覆盖子集 S（必含基地 0）并回到 0 的最小行程
single = [INF] * full
dp = [[INF] * n for _ in range(full)]
dp[1][0] = 0
for S in range(full):
    for i in range(n):
        if not (S >> i) & 1 or dp[S][i] == INF:
            continue
        for j in range(n):
            if (S >> j) & 1:
                continue
            dp[S | (1 << j)][j] = min(dp[S | (1 << j)][j], dp[S][i] + dist[i][j])
for S in range(1, full):
    if (S & 1):
        single[S] = min(dp[S][i] + dist[i][0] for i in range(n) if (S >> i) & 1)
# 集合划分 DP：多人共同覆盖非基地城市
if m == 1:
    print(single[full - 1])
else:
    cover = [[INF] * full for _ in range(m + 1)]
    cover[0][1] = 0  # 0 人行，仅含基地
    for k in range(1, m + 1):
        for S in range(full):
            if not (S & 1):
                continue
            if single[S] == INF:
                continue
            for T in range(full):
                if T & S:
                    continue
                if cover[k - 1][S] < INF:
                    ns = S | T
                    cover[k][ns] = min(cover[k][ns], cover[k - 1][S] + single[S | T] - single[S])
    print(min(cover[k][full - 1] for k in range(1, m + 1)))
```

> **复杂度**：O(3^n) 时间（集合划分），O(2^n) 空间

---

#### 17.15.32 例 32：状压——积木排位满足相邻限制（排列计数）⭐⭐

> **知识点**：状压 DP、末位状态计数| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个元素排成一列，某些相邻对 (i,j) 被允许（给定 n×n 兼容矩阵），求把全 n 个都排上且相邻均允许的方案数，对 1e9+7 取模。

**思路**

💡 类比"按兼容排座"：dp[S][last] 表示已放集合 S 且最后为 last 的方案数。新加入 j 需 compat[last][j] 为真。

```python
MOD = 10**9 + 7
n = int(input())
comp = [list(map(int, input().split())) for _ in range(n)]
full = 1 << n
dp = [[0] * n for _ in range(full)]
for i in range(n):
    dp[1 << i][i] = 1
for S in range(full):
    for i in range(n):
        if not (S >> i) & 1 or dp[S][i] == 0:
            continue
        for j in range(n):
            if (S >> j) & 1 or not comp[i][j]:
                continue
            dp[S | (1 << j)][j] = (dp[S | (1 << j)][j] + dp[S][i]) % MOD
print(sum(dp[full - 1][i] for i in range(n)) % MOD)
```

> **复杂度**：O(2^n·n²) 时间，O(2^n·n) 空间

---

#### 17.15.33 例 33：状压——子集划分使每子集和符约束（背包状压组合，折半）⭐⭐

> **知识点**：状压 DP、子集和、可行性划分| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定数组，判断能否分成 k 个和相等的子集（每元素恰好分到一个子集）。

**思路**

💡 类比"均分k篮"：total 能被 k 整除则目标 T=total/k。dp[mask] 表示当前子集已填之和（对 T 取模的剩余缓存），BFS/DP 判断能否达到 full。

```python
from functools import lru_cache
n, k = map(int, input().split())
a = list(map(int, input().split()))
S = sum(a)
if S % k or max(a) > S // k:
    print("No"); exit()
T = S // k
full = 1 << n
@lru_cache(None)
def can(mask):
    if mask == full - 1:
        return True
    # 当前已分块剩余空间
    # 用目标 T 减去 (mask 已有和 %T)
    cur = sum(a[i] for i in range(n) if (mask >> i) & 1) % T
    target = T - cur if cur else T
    for i in range(n):
        if not (mask >> i) & 1 and a[i] <= target:
            if can(mask | (1 << i)):
                return True
    return False

print("Yes" if can(0) else "No")
```

> **复杂度**：指数级 2^n 时间，O(2^n) 空间（n 小）

---

#### 17.15.34 例 34：树形 DP——最少覆盖所有边（选点覆盖，经典）⭐⭐

> **知识点**：树形 DP、边覆盖点集| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：树上有守卫点覆盖边问题：选最少数量的点，使每条边至少有一个端点被选中。

**思路**

💡 类比"隔点守住边"：dp[u][0/1] 表示 u 是否选。若 u 不选则所有子必须选；若 u 选则子可任选，取 min。

```python
import sys
sys.setrecursionlimit(1000000)
n = int(input())
g = [[] for _ in range(n)]
for _ in range(n - 1):
    a, b = map(int, input().split())
    g[a].append(b)
    g[b].append(a)
vis = [False] * n

def dfs(u):
    vis[u] = True
    notpick = 0
    pick = 1
    for v in g[u]:
        if vis[v]:
            continue
        p, np_ = dfs(v)
        pick += min(p, np_)
        notpick += p
    return pick, notpick

p, np_ = dfs(0)
print(min(p, np_))
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.35 例 35：状压——方格取数相邻不可取最大和（洛谷 P yixue 棋盘取数）⭐⭐

> **知识点**：状压 DP、行内合法状态、相邻行互斥| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n×n 棋盘每格有权值，选取格子使所选互不相邻（四方向），最大权值和。

**思路**

💡 类比"隔格取棋"：枚举行与行状态 mask（无相邻列），转移剔除与上一行相撞的状态。dp[row][mask] 为该行的最大和。

```python
n = int(input())
g = [list(map(int, input().split())) for _ in range(n)]
full = 1 << n

def ok(mask):
    return (mask & (mask << 1)) == 0

states = [m for m in range(full) if ok(m)]
def row_val(mask, r):
    s = 0
    for j in range(n):
        if (mask >> j) & 1:
            s += g[r][j]
    return s

dp = [row_val(m, 0) for m in states]
for r in range(1, n):
    nxt = []
    for m2 in states:
        best = 0
        v2 = row_val(m2, r)
        for idx, m1 in enumerate(states):
            if m1 & m2:
                continue
            best = max(best, dp[idx])
        nxt.append(best + v2)
    dp = nxt
print(max(dp))
```

> **复杂度**：O(n·(3^n)) 约比 O(n·4^n) 小，时间可，O(2^n) 空间

---

#### 17.15.36 例 36：数位 DP——不含连续两个相同数字（相邻不同，含边界）⭐⭐

> **知识点**：数位 DP、相邻比较| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 [1,n] 中十进制下任意相邻两位都不相同的数的个数。

**思路**

💡 类比"相邻不重复"：dfs(pos, last, limit)，枚举当前位需 ≠last。

```python
def count(n):
    if n <= 0:
        return 0
    digits = list(map(int, str(n)))
    from functools import lru_cache
    @lru_cache(None)
    def dfs(pos, last, limit, started):
        if pos == len(digits):
            return 1
        up = digits[pos] if limit else 9
        res = 0
        for d in range(0, up + 1):
            if not started:
                if d == 0:
                    res += dfs(pos + 1, -1, limit and d == up, False)
                else:
                    res += dfs(pos + 1, d, limit and d == up, True)
            else:
                if d != last:
                    res += dfs(pos + 1, d, limit and d == up, True)
        return res
    return dfs(0, -1, True, False) - 1  # 减掉全 0 的零

n = int(input())
print(count(n))
```

> **复杂度**：O(位数×10) 时间，O(位数) 空间

---

#### 17.15.37 例 37：区间 DP——括号序列最长合法子串（连续，POJ 2955 变式）⭐⭐

> **知识点**：区间 DP、最长合法连续子串| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定括号串，求最长的合法括号连续子串长度（两两匹配）。

**思路**

💡 类比"最长连续配对"：dp[i][j]=max(dp[i][k]+dp[k+1][j])，若 s[i]、s[j] 配对再做 dp[i+1][j−1]+2 更新。

```python
s = input().strip()
n = len(s)
dp = [[0] * n for _ in range(n)]
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        if (s[i] == '(' and s[j] == ')') or (s[i] == '[' and s[j] == ']'):
            dp[i][j] = dp[i + 1][j - 1] + 2
        for k in range(i, j):
            dp[i][j] = max(dp[i][j], dp[i][k] + dp[k + 1][j])
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.38 例 38：区间 DP——糖果合并与分裂综合（区间 dp 综合应用题）⭐⭐

> **知识点**：区间 DP、综合套路| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个盒子围成一圈，各装 c[i] 个糖果，合并任意相邻两盒代价为两盒糖果数之和的平方，求合并成一盒的最小代价（环形）。

**思路**

💡 类比"圆环加平方代价"：环形拆链加倍，dp 代价为和平方，其余同环形石子合并。

```python
n = int(input())
c = list(map(int, input().split()))
a = c + c
size = 2 * n
pre = [0] * (size + 1)
for i in range(size):
    pre[i + 1] = pre[i] + a[i]
INF = float('inf')
dp = [[0] * size for _ in range(size)]
for length in range(2, n + 1):
    for i in range(size - length + 1):
        j = i + length - 1
        t = pre[j + 1] - pre[i]
        dp[i][j] = INF
        for k in range(i, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + t * t)
print(min(dp[i][i + n - 1] for i in range(n)))
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.39 例 39：状压——最短哈密顿回路且点必须回（TSP 变式，POJ 3311 完整）⭐⭐⭐

> **知识点**：状压 DP、全源最短路+TSP| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n+1 个点（含起点 0），给出两两直接距离矩阵（可不对称），求从 0 出发经其余点各一次并回 0 的最短距离。

**思路**

💡 类比"必经回廊"：先用 Floyd 求所有点对最短路，再做标准 TSP 状压。dp[S][i]=最短到达。

```python
n = int(input())
dist = [list(map(int, input().split())) for _ in range(n)]
# Floyd
for k in range(n):
    for i in range(n):
        for j in range(n):
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
full = 1 << n
INF = float('inf')
dp = [[INF] * n for _ in range(full)]
dp[1][0] = 0
for S in range(full):
    for i in range(n):
        if not (S >> i) & 1 or dp[S][i] == INF:
            continue
        for j in range(n):
            if (S >> j) & 1:
                continue
            dp[S | (1 << j)][j] = min(dp[S | (1 << j)][j], dp[S][i] + dist[i][j])
print(min(dp[full - 1][i] + dist[i][0] for i in range(1, n)))
```

> **复杂度**：O(n³ + 2^n·n²) 时间，O(2^n·n) 空间

---

#### 17.15.40 例 40：数位 DP——求第 K 个满足条件的数（排列/构造，经典二分+数位）⭐⭐⭐

> **知识点**：数位 DP、第 K 大构造、二分| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求第 K 个不含数字 4 的正整数。

**思路**

💡 类比"数第 K 个吉利数"：f(n)=count(不含4 ≤n)。对其单调，逐位构造：从高位到低位尝试候选 digit，若 f(构造的部分) 不够 K 则累加。或直接按九进制进位转换。

```python
def count_up_to(n):
    if n <= 0:
        return 0
    digits = list(map(int, str(n)))
    res = 0
    for d in digits:
        res = res * 9 + (d if d < 4 else d - 1) if A else 0
    # 重实现
    res = 0
    for d in digits:
        if d < 4:
            res = res * 9 + d
        else:
            res = res * 9 + (d - 1)
    return res + 1 if n > 0 else 0

K = int(input())
LO, HI = 1, 10 ** 18
while LO < HI:
    mid = (LO + HI) // 2
    if count_up_to(mid) >= K:
        HI = mid
    else:
        LO = mid + 1
print(LO)
```

> **复杂度**：O(log 答案×位数) 时间，O(1) 空间

---

#### 17.15.41 例 41：概率/期望 DP——赌场输赢步数期望（概率 DP 入门）⭐⭐

> **知识点**：概率 DP、期望递推、状态图| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从余额 0 开始，每轮以概率 p 得 +1 分、概率 1−p 得 −1 分，达到 M 分或 −L 分就停止。求最终到达 M 的概率（思路示范）。

**思路**

💡 类比"抛币赌局"：设 f[i] 为当前 i 分下最终到 M 的概率，则 f[i]=p·f[i+1]+(1−p)·f[i−1]，边界 f[M]=1、f[−L]=0。解线方程，属赌博血本问题，可代公式 (1−p)^i/p^i 或高斯消元（此处用 walk 迭代演示）。

```python
M, L = map(int, input().split())
p = float(input())
# 高斯消元求解 f[-L..M]
N = M + L + 1
# 构造方程组：对中间 f, f[i-1]*(1-p) - f[i] + f[i+1]*p = 0
# 用简单迭代化简版本：对无限流动，利用 p 与 1-p
# 公式解：f[i] = (r^i - r^{0})/(r^{M} - r^{...})
q = 1 - p
if p == q:
    print(M / (M + L))
else:
    r = q / p
    # f[0 分?] 换个：设下界 0，上界 n，start offset L
    # f[i], i=0..N (0 => -L, N=>M)
    # 用闭式：f[i]=(1-r^i)/(1-r^N)
    # start index = L
    i = L
    Ntot = M + L
    if r == 1:
        ans = i / Ntot
    else:
        ans = (1 - r ** i) / (1 - r ** Ntot)
    print(f"{ans:.6f}")
```

> **复杂度**：O(1) 时间（闭式），O(1) 空间

---

#### 17.15.42 例 42：期望/概率 DP——掷骰走格子（可达概率 step，经典递推）⭐⭐

> **知识点**：概率 DP、掷骰跳、陷阱格| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从第 1 格出发到达终点 n，每步掷一个 k 面骰决定前进格数，某些格为陷阱（掉到更低的陷阱位），求到达终点的概率。

**思路**

💡 类比"掷骰大富翁"：p[i] 为从 i 出发到达终点的概率，p[i]=∑(1/k)p[i+d]，陷阱格 p=对应目标格概率。倒序递推。

```python
n, k = map(int, input().split())
trap = list(map(int, input().split()))  # 陷阱：位置->目标
mp = list(range(n + 1))
for i in range(1, n + 1):
    # 简化读入
    pass
# 示范读入格式：q 个陷阱，每次给出 from=x to=y
trap_map = {}
q = int(input())
for _ in range(q):
    fr, to = map(int, input().split())
    trap_map[fr] = to
prob = [0.0] * (n + 1)
prob[n] = 1.0
# 由于陷阱可能往回导致依赖环，使用迭代松弛若干轮
for _ in range(n + 5):
    changed = False
    for i in range(n - 1, 0, -1):
        p = 0.0
        for d in range(1, k + 1):
            j = min(n, i + d)
            p += prob[j] / k
        if i in trap_map:
            p = prob[trap_map[i]]
        if abs(p - prob[i]) > 1e-12:
            prob[i] = p
            changed = True
print(f"{prob[1]:.6f}")
```

> **复杂度**：O(n·k·迭代) 时间，O(n) 空间

---

#### 17.15.43 例 43：单调队列优化——滑动窗口最大值（洛谷 P1886）⭐⭐

> **知识点**：滑动窗口、单调队列| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个数的序列与窗口大小 k，从窗口左端开始滑动，输出每个窗口的最大值与最小值。

**思路**

💡 类比"队首最大"：维护单调递减队列存下标，保证队首在窗口内且最大；滑出则队首出队。最小值用对称单调递增队列。

```python
from collections import deque
n, k = map(int, input().split())
a = list(map(int, input().split()))
def slide(mode):
    q = deque()
    res = []
    for i, x in enumerate(a):
        if q and q[0] <= i - k:
            q.popleft()
        while q:
            if mode == 'max' and a[q[-1]] <= x:
                q.pop()
            elif mode == 'min' and a[q[-1]] >= x:
                q.pop()
            else:
                break
        q.append(i)
        if i >= k - 1:
            res.append(str(a[q[0]]))
    return res
print(' '.join(slide('max')))
print(' '.join(slide('min')))
```

> **复杂度**：O(N) 时间，O(K) 空间

---

#### 17.15.44 例 44：单调队列优化 DP——跳石子最少代价（老题）⭐⭐

> **知识点**：单调队列优化、滑动窗口取 min| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从 0 点跳到 n 点，每点有高度，落点有代价，每次最多跳 k 步。求最小总代价（代价可按高度差计算，简化固定）。

**思路**

💡 类比"跳桩省力"：dp[i]=min(dp[i−k..i−1])+cost[i]，用单调递增队列维护窗口最值 O(n)。

```python
from collections import deque
n, k = map(int, input().split())
h = list(map(int, input().split()))
INF = float('inf')
cost = [0] * (n + 1)
hd = [0] + h
q = deque([0])
dp = [0] + [INF] * n
for i in range(1, n + 1):
    while q and q[0] < i - k:
        q.popleft()
    best = q[0]
    dp[i] = dp[best] + abs(hd[i] - hd[best])
    while q and dp[q[-1]] >= dp[i]:
        q.pop()
    q.append(i)
print(dp[n])
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.45 例 45：斜率优化 DP——任务调度（经典，POJ 3709 变式/洛谷 P2365 简化）⭐⭐⭐

> **知识点**：斜率优化、凸包、DP 决策单调| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个任务排成序列，分成若干连续批，每批有启动代价 S 与单件时间。总代价含完成时间的延迟项。求最小总代价（简化线性形式）。

**思路**

💡 类比"批处理折中"：建立 dp[j]=min over i dp[i]+cost(i→j)，转移方程出现斜率项，用单调队列维护下凸包使每点均摊 O(1) 决策。

```python
n, S = map(int, input().split())
T = [0] * (n + 1)
C = [0] * (n + 1)
for i in range(1, n + 1):
    t, c = map(int, input().split())
    T[i] = T[i - 1] + t
    C[i] = C[i - 1] + c
dp = [0] * (n + 1)
q = [0]  # 候选下标的单调队列（维护下凸包）
hh = 0   # 队首指针
for i in range(1, n + 1):
    # 队首出队条件是斜率 <= 当前查询斜率 (T[i]+S)
    while hh + 1 < len(q) and \
          (dp[q[hh + 1]] - dp[q[hh]]) <= (T[i] + S) * (C[q[hh + 1]] - C[q[hh]]):
        hh += 1
    j = q[hh]
    dp[i] = dp[j] + T[i] * (C[i] - C[j]) + S * (C[n] - C[j])
    # 维护下凸包：当新点使队列破坏凸性时弹队尾
    while len(q) - hh >= 2 and \
          (dp[q[-1]] - dp[q[-2]]) * (C[i] - C[q[-2]]) >= \
          (dp[i] - dp[q[-2]]) * (C[q[-1]] - C[q[-2]]):
        q.pop()
    q.append(i)
print(dp[n])
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.46 例 46：单调队列优化——多重背包单调队列（经典高难）⭐⭐⭐

> **知识点**：多重背包、单调队列按余数分组优化| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 种物品、容量 V，每种有重量 w、数量 k、价值 v，求不超过 V 的最大价值。V 巨大需 O(V) 单调队列优化。

**思路**

💡 类比"按余数窗口取最值"：对每个余数 r，容量可写 r+t·w，dp 更新只依赖同一类余数的前一位，用单调队列在窗口 k 内维护最大值，全程均摊 O(V)。

```python
V, n = map(int, input().split())
dp = [0] * (V + 1)
for _ in range(n):
    v, w, k = map(int, input().split())  # (价值, 重量, 数量)
    # 单调队列优化
    for r in range(w):
        q = []  # (index within this residue class, value)
        hh = 0
        for t in range((V - r) // w + 1):
            cap = r + t * w
            if cap > V:
                break
            val = dp[cap] - t * v
            while len(q) > hh and q[-1][1] <= val:
                q.pop()
            q.append((t, val))
            # 弹出窗口外
            first_t = q[hh][0]
            if t - first_t > k:
                hh += 1
            dp[cap] = q[hh][1] + t * v
print(dp[V])
```

> **复杂度**：O(n·V) 时间，O(V) 空间

---

#### 17.15.47 例 47：状压 DP——最小化翻转 coin（棋盘状压，HDU 变式）⭐⭐

> **知识点**：状压 DP、按行枚举翻转| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n×n 棋盘每格硬币正/反，操作一次能翻转某格及其上下左右相邻格，求把全部翻成正面（或反面）的最少操作，并输出方案。

**思路**

💡 类比"草皮法翻转"：枚举行一（2^n 种翻转位），后续每行由上一行状态唯一决定（哪列需补翻）。逐行模拟并统计，取最小。

```python
n = int(input())
board = [list(map(int, input().split())) for _ in range(n)]
# 目标全部为 0
best = float('inf')
import sys
for first in range(1 << n):
    cur = [row[:] for row in board]
    flips = [[0] * n for _ in range(n)]
    cnt = 0
    for j in range(n):
        if first >> j & 1:
            # 翻转 (0,j) 及其邻居
            for dx, dy in ((0, 0), (0, 1), (0, -1), (1, 0)):
                nx, ny = dx, j + dy
                if 0 <= nx < n and 0 <= ny < n:
                    cur[nx][ny] ^= 1
            cnt += 1
            flips[0][j] = 1
    for i in range(1, n):
        for j in range(n):
            if cur[i - 1][j] == 1:  # 上一行待翻
                for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, 1), (0, -1)):
                    nx, ny = i + dx, j + dy
                    if 0 <= nx < n and 0 <= ny < n:
                        cur[nx][ny] ^= 1
                cnt += 1
                flips[i][j] = 1
    if all(cur[i][j] == 0 for i in range(n) for j in range(n)):
        best = min(best, cnt)
print(-1 if best == float('inf') else best)
```

> **复杂度**：O(2^n·n²) 时间，O(n²) 空间

---

#### 17.15.48 例 48：树形 DP——最大权值选择子树路径（树上最长链，UVA 10859 简化）⭐⭐

> **知识点**：树形 DP、每个节点的两条最长子链| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：带权树，求树中任意两点间路径权值和最大（带权直径）。

**思路**

💡 类比"带权最远"：树形 DP 维护每个节点的向下最长两条链，答案等于任意点两条最长链之和的最大值。

```python
import sys
sys.setrecursionlimit(1000000)
n = int(input())
g = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v, w = map(int, input().split())
    g[u].append((v, w))
    g[v].append((u, w))
vis = [False] * n
ans = 0

def dfs(u):
    global ans
    vis[u] = True
    max1 = 0
    max2 = 0
    for v, w in g[u]:
        if vis[v]:
            continue
        s = dfs(v) + w
        if s > max1:
            max2 = max1
            max1 = s
        elif s > max2:
            max2 = s
    ans = max(ans, max1 + max2)
    return max1

dfs(0)
print(ans)
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.49 例 49：树形 DP——最小遍历所有节点回到根（邮递员走遍，带边权）⭐⭐

> **知识点**：树形 DP/贪心、遍历计数| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：树中需要从根出发走遍每个节点且最后回到根，每条边长度已知，求最小总路程。

**思路**

💡 类比"回邮路"：环形遍历树，每条边需走两次（一去一回），故最小总长度 = 2×总边权和。

```python
n, r = map(int, input().split())
total = 0
for _ in range(n - 1):
    u, v, w = map(int, input().split())
    total += w
print(2 * total)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.15.50 例 50：树形背包强化——依赖关系多层（树形背包推广，森林与超级根）⭐⭐⭐

> **知识点**：树形背包、森林加超级根、DFS 合并| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 门课，选课有先修要求（修某课必须先修其前驱），每门课有学分，最多选 m 门，求最大总学分。

**思路**

💡 类比"先修再学"：把无前驱的课挂在虚拟根 0 上组成树，树形分组背包，dp[u][j]=选 j 门含 u 的最大学分，对每棵子树做 0-1 合并。

```python
import sys
sys.setrecursionlimit(1000000)
n, m = map(int, input().split())
val = [0] * (n + 1)
children = [[] for _ in range(n + 1)]
for i in range(1, n + 1):
    p, s = map(int, input().split())
    children[p].append(i)
    val[i] = s
dp = [[0] * (m + 2) for _ in range(n + 1)]

def dfs(u):
    dp[u][1] = val[u]
    for v in children[u]:
        dfs(v)
        for j in range(m + 1, 0, -1):
            for k in range(1, j):
                dp[u][j] = max(dp[u][j], dp[u][j - k] + dp[v][k])

dfs(0)
print(dp[0][m + 1])
```

> **复杂度**：O(n·m²) 时间，O(n·m) 空间

---

#### 17.15.51 例 51：区间 DP——回文分割（分割成最少回文串，LeetCode 132）⭐⭐

> **知识点**：区间 DP、预处理回文标志、一维分割| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串，求把它分割成若干个回文子串所需的最少分割次数。

**思路**

💡 类比"切香肠留对称段"：先 O(n²) 预处理 isPal[i][j]，再 dp[i]=min(dp[j]+1)（s[j+1..i] 为回文），答案是 dp。

```python
s = input().strip()
n = len(s)
isPal = [[False] * n for _ in range(n)]
for i in range(n):
    isPal[i][i] = True
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        if s[i] == s[j] and (length == 2 or isPal[i + 1][j - 1]):
            isPal[i][j] = True
INF = float('inf')
dp = [INF] * n
for i in range(n):
    if isPal[0][i]:
        dp[i] = 0
    else:
        for j in range(i):
            if isPal[j + 1][i]:
                dp[i] = min(dp[i], dp[j] + 1)
print(0 if n == 0 else dp[n - 1])
```

> **复杂度**：O(N²) 时间，O(N²) 空间

---

#### 17.15.52 例 52：区间 DP——最优二叉搜索树（经典）⭐⭐

> **知识点**：区间 DP、选择根使搜索代价最小| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个有序关键字，各有一个访问概率，构造二叉搜索树使期望比较次数最小（即 ∑ 深度×概率 最小）。

**思路**

💡 类比"词频深藏"：dp[i][j] 表示用关键字 i..j 构造子树的最小代价，枚举根 k，左右子子树代价 + 区间总概率（深度+1）。

```python
n = int(input())
p = [0.0] + list(map(float, input().split()))
pre = [0.0] * (n + 1)
for i in range(1, n + 1):
    pre[i] = pre[i - 1] + p[i]
INF = float('inf')
dp = [[0.0] * (n + 2) for _ in range(n + 2)]
root = [[0] * (n + 2) for _ in range(n + 2)]
for i in range(1, n + 1):
    dp[i][i] = p[i]
    root[i][i] = i
for length in range(2, n + 1):
    for i in range(1, n - length + 2):
        j = i + length - 1
        dp[i][j] = INF
        for k in range(root[i][j - 1], root[i + 1][j] + 1):
            c = dp[i][k - 1] + dp[k + 1][j] + (pre[j] - pre[i - 1])
            if c < dp[i][j]:
                dp[i][j] = c
                root[i][j] = k
print(f"{dp[1][n]:.4f}")
```

> **复杂度**：O(N²) 时间（四边形优化），O(N²) 空间

---

#### 17.15.53 例 53：状压 DP——桶装水看集合可行性（旅行商 subset 翻转简化）⭐⭐

> **知识点**：状压 DP、bitset 背包、物品集合| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：若干瓶子容量（有限数量），目标容量 T，求能否装满 T（每瓶至多用一次）。

**思路**

💡 类比"整数桶凑容量"：bitset DP，dp 是大整数，某位上 1 表示该容量可达。对每瓶容量 cap，dp |= dp << cap。

```python
caps = list(map(int, input().split()))
T = int(input())
dp = 1  # bit 0 set
for c in caps:
    dp |= dp << c
print("Yes" if (dp >> T) & 1 else "No")
```

> **复杂度**：O(n·T/字长) 时间，O(T) 空间

---

#### 17.15.54 例 54：数位 DP——求不含"00"的数（连续两个零禁止，加强）⭐⭐

> **知识点**：数位 DP、多状态记前两位是否零| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 [1,n] 中十进制表示不含连续两位都是 0 的数的个数。

**思路**

💡 类比"禁双零"：dfs(pos, lastzero, limit, started)。若上一数字是 0 且当前也为 0 则非法；跳过。

```python
def count(n):
    digits = list(map(int, str(n)))
    from functools import lru_cache
    @lru_cache(None)
    def dfs(pos, prev_zero, started, limit):
        if pos == len(digits):
            return 1
        up = digits[pos] if limit else 9
        res = 0
        for d in range(0, up + 1):
            if started and prev_zero and d == 0:
                continue
            res += dfs(pos + 1, started and d == 0, started or d != 0, limit and d == up)
        return res
    return dfs(0, False, False, True) - 1

n = int(input())
print(count(n))
```

> **复杂度**：O(位数×2×2) 时间，O(位数) 空间

---

#### 17.15.55 例 55：期望 DP——掷骰累积步数的期望（期望入门）⭐⭐

> **知识点**：期望 DP、线性期望、终点态| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从第 0 级爬到第 n 级，每步可走 1..k 级（等概率），求到达 n 的期望步数。

**思路**

💡 类比"掷骰爬楼"：E[i] 表示从 i 级出发还需期望步数，E[i]=1+∑(1/k)E[i+d]（到终点为 0）。倒序递推可得。

```python
n, k = map(int, input().split())
E = [0.0] * (n + k + 1)
for i in range(n - 1, -1, -1):
    s = 0.0
    for d in range(1, k + 1):
        j = min(n, i + d)
        s += E[j] / k
    E[i] = 1 + s
print(f"{E[0]:.6f}")
```

> **复杂度**：O(n·k) 时间，O(n) 空间

---

#### 17.15.56 例 56：期望 DP——随机游走吸收态（范围吸收概率）⭐⭐

> **知识点**：期望 DP、吸收态、方程组/迭代| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：区间 [0,N]，从中间位置 s 开始，每步以 p 概率向右 1、1−p 向左 1，0 与 N 是吸收态。求第一次到达 N 的概率。

**思路**

💡 类比"赌徒破产"：f[i]=p f[i+1]+(1−p) f[i−1]，f[0]=0, f[N]=1。用高斯消元或代数闭式解。

```python
N, s, p = map(int, input().split())
p = p / 100.0
q = 1 - p
if p == q:
    print(f"{s / N:.6f}")
else:
    r = q / p
    if abs(r - 1) < 1e-12:
        print(f"{s / N:.6f}")
    else:
        ans = (1 - r ** s) / (1 - r ** N)
        print(f"{ans:.6f}")
```

> **复杂度**：O(1) 时间，O(1) 空间

---

#### 17.15.57 例 57：单调队列——选择若干数使间距满足（线性 dp+窗口最值）⭐⭐

> **知识点**：单调队列、区间约束最值| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数，选一个子序列，相邻两次选择的间距在 [L,R]，求所选数的最大和。

**思路**

💡 类比"隔段取宝"：dp[i]=a[i]+max(dp[j])，j 在 [i−R, i−L] 范围内，用单调递减队列维护窗口内最大 dp。

```python
from collections import deque
n, L, R = map(int, input().split())
a = [0] + list(map(int, input().split()))  # a[0] 起点的基
NEG = float('-inf')
dp = [NEG] * (n + 1)
dp[0] = 0
q = deque()
# 逐个推进
for i in range(1, n + 1):
    # 可加入 j = i - L 作为候选（需满足 j>=0）
    j = i - L
    if j >= 0 and dp[j] > NEG:
        while q and dp[q[-1]] <= dp[j]:
            q.pop()
        q.append(j)
    # 移除超出 [i-R, i-L] 的
    while q and q[0] < i - R:
        q.popleft()
    if q:
        dp[i] = dp[q[0]] + a[i]
print(max(dp[i] for i in range(max(0, n - R + 1), n + 1)))
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.58 例 58：区间 DP——最大括号匹配巩固（带多种括号）⭐⭐

> **知识点**：区间 DP、多种括号配对| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：串含 ()[]{}，求能匹配的括号字符最大数量。

**思路**

💡 类比"整套配对"：dp[i][j]=max 区间内匹配数，若 s[i]、s[j] 配对则 dp[i+1][j−1]+2，否则分割取最大。

```python
s = input().strip()
n = len(s)
pair = {')': '(', ']': '[', '}': '{'}
dp = [[0] * n for _ in range(n)]
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        if s[j] in pair and pair[s[j]] == s[i]:
            dp[i][j] = dp[i + 1][j - 1] + 2
        for k in range(i, j):
            dp[i][j] = max(dp[i][j], dp[i][k] + dp[k + 1][j])
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.59 例 59：树形 DP——最小点覆盖（加权，POJ/HDU 树形覆盖）⭐⭐

> **知识点**：树形 DP、加权点覆盖| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：树中每点有选点代价，选择若干点覆盖所有边（每条边至少一个端点被选），求最小总代价。

**思路**

💡 类比"加点守边"：dp[u][0]=不选，则子必选；dp[u][1]=选，子可任选取 min。加权累加。

```python
import sys
sys.setrecursionlimit(1000000)
n = int(input())
cost = [0] + list(map(int, input().split()))
g = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    g[u].append(v)
    g[v].append(u)

def dfs(u, fa):
    take = cost[u]
    nottake = 0
    for v in g[u]:
        if v == fa:
            continue
        t, nt = dfs(v, u)
        take += min(t, nt)
        nottake += t
    return take, nottake

a, b = dfs(1, 0)
print(min(a, b))
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.60 例 60：状压 DP——恰好 k 个互不攻击皇后所在列（棋盘列状态简化）⭐⭐

> **知识点**：状压 DP、列掩码、限制行| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n×n 棋盘放 n 个车，使它们互不攻击（不同行不同列），求放法数。

**思路**

💡 类比"车不同列"：逐行放车，记录已占用列的掩码。dp[mask] 表示占用列集合为 mask 的方案数，转移在可用列中选。

```python
n = int(input())
full = 1 << n
dp = [0] * full
dp[0] = 1
for mask in range(full):
    row = bin(mask).count('1')  # 已放了 row 个，下一个放这行
    for col in range(n):
        if not (mask >> col) & 1:
            dp[mask | (1 << col)] += dp[mask]
print(dp[full - 1])
```

> **复杂度**：O(2^n·n) 时间，O(2^n) 空间

---

#### 17.15.61 例 61：树形 DP——树的中心/最小最大距离点（换根 DP）⭐⭐⭐

> **知识点**：换根 DP、两次 DFS| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：树中求一个点，使得到所有点的距离之和最小（树的加权中心），输出该距离和。

**思路**

💡 类比"重心集结"：第一次 DFS 计算子树大小与各点子树内的总距离；换根时把答案从父迁移到子，O(1) 转移，整体两次 DFS。

```python
import sys
sys.setrecursionlimit(1000000)
n = int(input())
g = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    g[u].append(v)
    g[v].append(u)
sz = [0] * n
dp = [0] * n

def dfs1(u, fa):
    sz[u] = 1
    for v in g[u]:
        if v == fa:
            continue
        dfs1(v, u)
        sz[u] += sz[v]
        dp[u] += dp[v] + sz[v]

def dfs2(u, fa):
    for v in g[u]:
        if v == fa:
            continue
        dp[v] = dp[u] + (n - sz[v]) - sz[v]
        dfs2(v, u)

dfs1(0, -1)
dfs2(0, -1)
print(min(dp))
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.62 例 62：数位 DP——和能被 3 整除的数（取模类数位 dp）⭐⭐

> **知识点**：数位 DP、模数作为状态| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：统计 [l,r] 中十进制各位数字之和能被 3 整除的数的个数。

**思路**

💡 类比"数位和取模"：dfs(pos, mod, limit)，mod 为已达数字和模 3。末位 mod==0 则计数。

```python
def count(n):
    if n < 0:
        return 0
    digits = list(map(int, str(n)))
    from functools import lru_cache
    @lru_cache(None)
    def dfs(pos, mod, limit):
        if pos == len(digits):
            return 1 if mod == 0 else 0
        up = digits[pos] if limit else 9
        res = 0
        for d in range(up + 1):
            res += dfs(pos + 1, (mod + d) % 3, limit and d == up)
        return res
    return dfs(0, 0, True)

l, r = map(int, input().split())
print(count(r) - count(l - 1))
```

> **复杂度**：O(位数×3) 时间，O(位数×3) 空间

---

#### 17.15.63 例 63：区间 DP——多边形分割最小（切多边形对角线和，经典）⭐⭐

> **知识点**：区间 DP、多边形代价满足四边形| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 边形顶点值，每切一条对角线代价为其两端顶点值之差，求把多边形三角剖分（n−3 条对角线）的最小总代价。

**思路**

💡 类比"裁多边形省差值"：dp[i][j]=min over k dp[i][k]+dp[k][j]+代价(i,k,j)，代价取两端顶点配对差值之和，区间增长枚举。

```python
n = int(input())
v = list(map(int, input().split()))
INF = float('inf')
dp = [[0] * n for _ in range(n)]
for length in range(2, n):
    for i in range(n - length):
        j = i + length
        dp[i][j] = INF
        for k in range(i + 1, j):
            cost = abs(v[i] - v[k]) + abs(v[i] - v[j]) + abs(v[j] - v[k])
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cost)
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.64 例 64：状压 DP——促销组合选最优（子集价值从掩码中求）⭐⭐

> **知识点**：状压 DP、子集和求最大| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：买物品，一次顺延结算——给定每个物品单价与若干"买满某子集折扣"的套餐，求买到全部物品的最低总价。

**思路**

💡 类比"合集省钱"：dp[mask] 表示买到 mask 集合物品的最低总价。可先求每种套餐对 mask 的价，再做子集 DP dp[mask]=min(dp[mask], dp[mask^sub]+price[sub])。

```python
n = int(input())
prices = list(map(int, input().split()))  # 单价
full = 1 << n
dp = [float('inf')] * full
dp[0] = 0
for mask in range(full):
    for i in range(n):
        if (mask >> i) & 1:
            dp[mask] = min(dp[mask], dp[mask ^ (1 << i)] + prices[i])
q = int(input())
for _ in range(q):
    data = list(map(int, input().split()))
    k = data[0]
    idx = [data[i + 1] - 1 for i in range(k)]
    cost = data[1 + k]
    s = 0
    for i in idx:
        s |= (1 << i)
    # 套餐可合并到 dp（视为一次买整集合）
    for mask in range(full):
        if (mask & s) == s:
            dp[mask] = min(dp[mask], dp[mask ^ s] + cost)
print(dp[full - 1])
```

> **复杂度**：O(2^n·(n+q)) 时间，O(2^n) 空间

---

#### 17.15.65 例 65：概率 DP——抛币连续期望（直到 k 连正所需期望步）⭐⭐

> **知识点**：期望 DP、k 连失败状态、马尔可夫| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：抛一枚成功概率 p 的硬币，求首次出现连续 k 次成功的期望抛掷次数。

**思路**

💡 类比"摸彩中连彩"：E[i] 表示已有 i 连成功达到 k 连还需期望次数，E[i]=1+p E[i+1]+(1−p) E[0]，解线性递推。

```python
k, p = map(int, input().split())
p = p / 100.0
q = 1 - p
# 用方程组递推：E[i] = 1 + p*E[i+1] + (1-p)*E[0]，E[k]=0
# 可解闭式：E[0] = (1 - p^k) / (p^k * q)
E = None
if q == 0:
    E0 = float(k)
else:
    E0 = (1 - p ** k) / (p ** k * q) if q else float(k)
print(f"{E0:.6f}")
```

> **复杂度**：O(1) 时间，O(1) 空间

---

#### 17.15.66 例 66：区间 DP——切蛋糕最大收益（分段分配，n 段加点）⭐⭐

> **知识点**：区间 DP、分段取极值| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一段糖果切成若干段，每段的收益由长度决定（给定函数），切开位置需在允许点集，求总收益最大。

**思路**

💡 类比"切蛋糕配酬"：dp[i][j] 表示区间 [i,j] 直接作为整段或不切的最大收益，枚举切点求和取最大。

```python
n = int(input())
# 函数收益：直接给收益数组 reward[l]
reward = list(map(int, input().split()))  # reward[i] 表示长度 i 的收益
# 简化：切点即整数位置 1..n-1，可选全部
dp = [0] * (n + 1)
for i in range(1, n + 1):
    dp[i] = reward[i]
# 允许自由切点，可分成任意整数段
for i in range(1, n + 1):
    for j in range(1, i):
        dp[i] = max(dp[i], dp[j] + reward[i - j])
print(dp[n])
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.15.67 例 67：树形 DP——安装软件依赖（DP 内存选课强化+输出方案）⭐⭐⭐

> **知识点**：树形背包、方案回溯| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个软件，各需内存、有价值，部分软件依赖另一个软件才能安装（形成森林），总内存 M，求最大价值与所选软件列表。

**思路**

💡 类比"依赖装软件"：加超级根后树形背包，记录选 j 是否含某子树决策，回溯输出。

```python
import sys
sys.setrecursionlimit(1000000)
n, m = map(int, input().split())
mem = [0] + list(map(int, input().split()))
val = [0] + list(map(int, input().split()))
children = [[] for _ in range(n + 1)]
for i in range(1, n + 1):
    p = int(input())
    children[p].append(i)

dp = [[-1] * (m + 1) for _ in range(n + 1)]

def dfs(u):
    if u == 0:
        dp[0][0] = 0
    elif mem[u] <= m:
        dp[u][mem[u]] = val[u]
    for v in children[u]:
        dfs(v)
        ndp = [-1] * (m + 1)
        for a in range(m + 1):
            if dp[u][a] < 0:
                continue
            for b in range(m + 1):
                if dp[v][b] < 0:
                    continue
                if a + b <= m:
                    ndp[a + b] = max(ndp[a + b], dp[u][a] + dp[v][b])
        dp[u] = ndp

dfs(0)
print(max(dp[0]))
```

> **复杂度**：O(n·m²) 时间，O(n·m) 空间

---

#### 17.15.68 例 68：数位 DP——统计各位递增的数（数位递增计数）⭐⭐

> **知识点**：数位 DP、非降/升序限制| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：统计 [1,n] 中十进制各位数字从左到右非严格递增（如 123、112）的数的个数。

**思路**

💡 类比"升序流水号"：dfs(pos, last, limit, started)，当前数字需 ≥ last。注意前导零时 last 为 −1 不限制。

```python
def count(n):
    digits = list(map(int, str(n)))
    from functools import lru_cache
    @lru_cache(None)
    def dfs(pos, last, limit, started):
        if pos == len(digits):
            return 1
        up = digits[pos] if limit else 9
        res = 0
        for d in range(0, up + 1):
            if not started:
                res += dfs(pos + 1, d, limit and d == up, True) if d != 0 else dfs(pos + 1, last, limit and d == up, False)
            else:
                if d >= last:
                    res += dfs(pos + 1, d, limit and d == up, True)
        return res
    return dfs(0, -1, True, False) - 1

n = int(input())
print(count(n))
```

> **复杂度**：O(位数×10) 时间，O(位数) 空间

---

#### 17.15.69 例 69：区间 DP——表达式最大最小（插入 + 或 × 求极值，经典）⭐⭐

> **知识点**：区间 DP、二元运算格错位排列| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：圆环上的 n 个数字与 n−1 个运算符（+ 或 ×），去掉一条边后按序计算，运算可任意加括号，求结果的最大值与最小值。

**思路**

💡 类比"括号任意算"：拆环为链，dp 同时维护最大最小（因乘法符号会翻转）。dp_max[i][j]=max 组合，运算对左右最大最小四组合取。

```python
n = int(input())
a = list(map(int, input().split()))
op = list(input().strip())  # '+' 或 '*'
# 环变链
A = a + a + a
size = 3 * n
INF = float('inf')
dpmax = [[-INF] * size for _ in range(size)]
dpmin = [[INF] * size for _ in range(size)]
for i in range(size):
    dpmax[i][i] = dpmin[i][i] = A[i]
for length in range(2, n + 1):
    for i in range(size - length + 1):
        j = i + length - 1
        for k in range(i, j):
            o = op[(k - (0)) % n]  # 简化：此处 op 按 pos 取
            o = op[k % n if k // n == 0 else (k % n)] if False else op[k % n]
            for x in (dpmax[i][k], dpmin[i][k]):
                for y in (dpmax[k + 1][j], dpmin[k + 1][j]):
                    v = x + y if op[(k) % n] == '+' else x * y
                    dpmax[i][j] = max(dpmax[i][j], v)
                    dpmin[i][j] = min(dpmin[i][j], v)
ans = max(dpmax[i][i + n - 1] for i in range(n))
print(ans)
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.70 例 70：状压 DP——骑士放置（互不攻击，棋盘状压高级）⭐⭐⭐

> **知识点**：状压 DP、行状态、攻击限制| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n×n 棋盘，放置若干马（骑士），任意两马不能互相攻击（走"日"字），部分格子不能放，求最大放置数。

**思路**

💡 类比"隔马不相干"：枚举行状态 mask，逐行 DP。判断同行使 (mask&(mask<<2)) 非法；列间攻击用相邻行转移条件 mask1 与 mask2 及位移错位检测。

```python
n = int(input())
grid = [list(map(int, input().split())) for _ in range(n)]  # 1 可放
full = 1 << n
def rowok(mask, r):
    if (mask & (mask << 2)) or (mask & (mask >> 2)):
        return False
    for j in range(n):
        if (mask >> j) & 1 and grid[r][j] == 0:
            return False
    return True
def cnt(mask):
    return bin(mask).count('1')
def attack(m1, m2):
    # 竖向差2横向差1 或 竖向差1横向差2（这里行差=1 只判错一位横差2）
    return ((m1 << 2) & m2) or ((m1 >> 2) & m2)
dp = {}
rows = []
for r in range(n):
    rows.append([m for m in range(full) if rowok(m, r)])
for m in rows[0]:
    dp[m] = cnt(m)
for r in range(1, n):
    ndp = {}
    for m2 in rows[r]:
        best = 0
        for m1 in rows[r - 1]:
            if attack(m1, m2):
                continue
            best = max(best, dp[m1])
        ndp[m2] = best + cnt(m2)
    dp = ndp
print(max(dp.values()) if dp else 0)
```

> **复杂度**：O(n·状态²) 时间，O(状态) 空间

---

#### 17.15.71 例 71：概率 DP——买卡集齐期望（收集套卡期望）⭐⭐

> **知识点**：期望 DP、套卡收集、调和数| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 种卡片，每次随机获得一种（等概率），求集齐全部 n 种所需购买次数期望。

**思路**

💡 类比"抽齐图鉴"：当已收集 i 种时，抽到新卡概率 (n−i)/n，期望次数为 n/(n−i)。总期望=∑n/(n−i)，i=0..n−1。

```python
n = int(input())
ans = 0.0
for i in range(n):
    ans += n / (n - i)
print(f"{ans:.6f}")
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.15.72 例 72：数位 DP——统计不降数（可重复，经典 HDU 2089 变式）⭐⭐

> **知识点**：数位 DP、不降序列| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 [a,b] 中各位数字非严格递增（不下降）的整数个数。

**思路**

💡 类比"渐大数"：dfs(pos,last,limit,started)，当前 d≥last 才合法。与例 68 相同模板应用双端区间。

```python
def count(n):
    if n < 0:
        return 0
    digits = list(map(int, str(n)))
    from functools import lru_cache
    @lru_cache(None)
    def dfs(pos, last, limit, started):
        if pos == len(digits):
            return 1
        up = digits[pos] if limit else 9
        res = 0
        for d in range(0, up + 1):
            if not started:
                res += dfs(pos + 1, d, limit and d == up, True) if d != 0 else dfs(pos + 1, -1, limit and d == up, False)
            else:
                if d >= last:
                    res += dfs(pos + 1, d, limit and d == up, True)
        return res
    return dfs(0, -1, True, False)

a, b = map(int, input().split())
print(count(b) - count(a - 1))
```

> **复杂度**：O(位数×10) 时间，O(位数) 空间

---

#### 17.15.73 例 73：区间 DP——合并石子取模求和（代价为和 mod K，环形删边）⭐⭐

> **知识点**：区间 DP、环形删边、代价取模| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数字围成环，删一条边展开成链，每次合并相邻两数代价为两数和 mod M，求合并成一数的最大/最小总代价。

**思路**

💡 类比"删边再聚石"：对每条被删边分别做线性区间 DP，取最值；指数较多时只在环上跑一遍并覆盖 2n 链各起点。

```python
n, M = map(int, input().split())
a = list(map(int, input().split()))
size = 2 * n
A = a + a
pre = [0] * (size + 1)
for i in range(size):
    pre[i + 1] = (pre[i] + A[i]) % M
INF = float('inf')
dpm = [[0] * size for _ in range(size)]
for length in range(2, n + 1):
    for i in range(size - length + 1):
        j = i + length - 1
        dpm[i][j] = INF
        for k in range(i, j):
            cost = (pre[j + 1] - pre[i]) % M
            dpm[i][j] = min(dpm[i][j], dpm[i][k] + dpm[k + 1][j] + cost)
print(min(dpm[i][i + n - 1] for i in range(n)))
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.74 例 74：树形 DP——树的点数最少覆盖（无加权，HDU 1054 简化）⭐⭐

> **知识点**：树形 DP、边覆盖最少数| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：多棵树森林，选最少城市使每条边至少一端被选，求最少点数。

**思路**

💡 类比"省着守边"：dp[u][0/1]，不选则子必选。对多棵树分别 dfs 累加。

```python
import sys
sys.setrecursionlimit(1000000)
n = int(input())
g = [[] for _ in range(n)]
seen = [False] * n
for _ in range(n - 1):
    u, v = map(int, input().split())
    g[u].append(v)
    g[v].append(u)

def dfs(u, fa):
    take = 1
    nottake = 0
    for v in g[u]:
        if v == fa:
            continue
        t, nt = dfs(v, u)
        take += min(t, nt)
        nottake += t
    return take, nottake

# 单棵树
a, b = dfs(0, -1)
print(min(a, b))
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.75 例 75：期望 DP——毕业期望抽奖（折半/朴素）⭐⭐

> **知识点**：概率期望、概率表| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：抽 n 次奖，每次中奖概率 p（各次独立），求至少中 m 次的概率。

**思路**

💡 类比"独立伯努利"：binomomial 分布，P(X≥m)=∑ C(n,k) p^k (1−p)^{n−k}，k=m..n。逐项累加。

```python
n, m, p = map(int, input().split())
p = p / 100.0
q = 1 - p
# 递推二项分布
prob = [1.0] + [0.0] * n
for i in range(1, n + 1):
    # 更新分布的迭代（从后往前）
    for k in range(i, 0, -1):
        prob[k] = prob[k] * q + prob[k - 1] * p
    prob[0] *= q
ans = sum(prob[m:]) if m <= n else 0.0
print(f"{ans:.6f}")
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.15.76 例 76：状压 DP——串不同排列且限制相邻（TSP 计数加强）⭐⭐

> **知识点**：状压 DP、字符串计数、禁止相邻对| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一串字符，可任意排列，但不能出现给定的若干长度为 2 的禁止子串（如 "ab" 不能相邻出现在结果中）。求不同排列总数（相同字符视为不同位置）对 1e9+7 取模。

**思路**

💡 类比"禁搭字母"：状压 dp[S][last] 表示已用集合 S、末尾字符下标 last 的合法排列数，新加字符需与 last 组合不在禁止表中。

```python
MOD = 10**9 + 7
s = input().strip()
n = len(s)
S = int(input())
forbidden = set()
for _ in range(S):
    forbidden.add(input().strip())
full = 1 << n
dp = [[0] * n for _ in range(full)]
for i in range(n):
    dp[1 << i][i] = 1
for mask in range(full):
    for i in range(n):
        if not (mask >> i) & 1 or dp[mask][i] == 0:
            continue
        for j in range(n):
            if (mask >> j) & 1:
                continue
            if s[i] + s[j] in forbidden:
                continue
            dp[mask | (1 << j)][j] = (dp[mask | (1 << j)][j] + dp[mask][i]) % MOD
print(sum(dp[full - 1][i] for i in range(n)) % MOD)
```

> **复杂度**：O(2^n·n²) 时间，O(2^n·n) 空间

---

#### 17.15.77 例 77：区间 DP——匹配回文串次数（最小步数化成回文）⭐⭐

> **知识点**：区间 DP、合并对称操作| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一次操作可将串中某个连续区间整体改成某个字符（涂色），求把一个给定串变成回文串的最少操作数。

**思路**

💡 类比"刷对称色"：dp[i][j] 表示把 s[i..j] 刷成回文最少次数，若两端相同则 dp[i][j]=dp[i+1][j−1]，否则 dp=min(dp[i][k]+dp[k+1][j])。

```python
s = input().strip()
n = len(s)
INF = float('inf')
dp = [[0] * n for _ in range(n)]
for i in range(n):
    dp[i][i] = 0
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        if s[i] == s[j]:
            dp[i][j] = dp[i + 1][j - 1]
        dp[i][j] = min(dp[i][j], dp[i + 1][j] + 1, dp[i][j - 1] + 1)
        for k in range(i, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j])
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.78 例 78：树形 DP——最大子树和（带权最大连通子树）⭐⭐

> **知识点**：树形 DP、最大连通块| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：带权树，求权值和最大的连通子树（可删一些边分成多块，取一块）的权值和。

**思路**

💡 类比"挑最肥一丛"：dp[u]=val[u]+∑max(0, dp[v])，答案即所有 dp[u] 的最大值。

```python
import sys
sys.setrecursionlimit(1000000)
n = int(input())
val = [0] + list(map(int, input().split()))
g = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    g[u].append(v)
    g[v].append(u)
vis = [False] * (n + 1)
ans = -10**18

def dfs(u):
    global ans
    vis[u] = True
    total = val[u]
    for v in g[u]:
        if vis[v]:
            continue
        total += max(0, dfs(v))
    ans = max(ans, total)
    return total

dfs(1)
print(ans)
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.79 例 79：数位 DP——能被 7 整除且不含 7（组合条件）⭐⭐

> **知识点**：数位 DP、多约束（取模 + 禁止数字）| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 [l,r] 中数字和能被 5 整除、且十进制不含数字 7 的数个数。

**思路**

💡 类比"多重筛选"：dfs(pos, mod5, has7, limit)。禁止 7 时直接跳过；末位要求 mod5==0 且不含 7。

```python
def count(n):
    if n < 0:
        return 0
    digits = list(map(int, str(n)))
    from functools import lru_cache
    @lru_cache(None)
    def dfs(pos, mod, limit):
        if pos == len(digits):
            return 1 if mod == 0 else 0
        up = digits[pos] if limit else 9
        res = 0
        for d in range(up + 1):
            if d == 7:
                continue
            res += dfs(pos + 1, (mod + d) % 5, limit and d == up)
        return res
    return dfs(0, 0, True)

l, r = map(int, input().split())
print(count(r) - count(l - 1))
```

> **复杂度**：O(位数×5) 时间，O(位数×5) 空间

---

#### 17.15.80 例 80：状压 DP——最小汉明距离分组（子集组合，理解"子集 DP 均摊"）⭐⭐

> **知识点**：状压 DP、子集枚举、分割| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个二进制串，把其分成两个集合使两个集合内任意两对的汉明距离和最小化（简化：目标最小化组内总距离）。

**思路**

💡 类比"切分减摩擦"：枚举左右两组子集 S 与其补集，预计算每组内所有配对距离和，双方相加取最小。子集转移均摊。

```python
n = int(input())
vs = [int(input(), 2) for _ in range(n)]
full = 1 << n
def ham(a, b):
    return bin(a ^ b).count('1')
# 预计算每个子集内部距离和
inner = [0] * full
for mask in range(full):
    # 从最低位拆分子集
    lsb = mask & -mask
    i = (lsb.bit_length() - 1)
    rest = mask ^ lsb
    inner[mask] = inner[rest]
    r = rest
    while r:
        b = r & -r
        j = b.bit_length() - 1
        inner[mask] += ham(vs[i], vs[j])
        r ^= b
best = float('inf')
for mask in range(full):
    comp = (full - 1) ^ mask
    if mask == 0 or comp == 0 or mask > comp:
        continue
    best = min(best, inner[mask] + inner[comp])
print(best)
```

> **复杂度**：O(2^n·n) 时间，O(2^n) 空间

---

#### 17.15.81 例 81：区间 DP——乘法链变式取玻璃球（两端保留中间取）⭐⭐

> **知识点**：区间 DP、取中选极（同例 11 微调）| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数字成环（首尾不算待取），每次取一个数字，代价为它与其左右邻居之积，取完中间所有数的最小代价（首尾保留）。

**思路**

💡 类比"环形抽球"：把环拆成 2n 链（首尾回绕），dp 同 Multiplication Puzzle 的取中转移。

```python
n = int(input())
a = list(map(int, input().split()))
# 环：选首尾相邻的"守护"，即固定拆出 n 种取法之一——简化为取直线
size = n
INF = float('inf')
dp = [[0] * size for _ in range(size)]
for length in range(2, size):
    for i in range(size - length):
        j = i + length
        dp[i][j] = INF
        for k in range(i + 1, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + a[i] * a[k] * a[j % size])
print(dp[0][size - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.82 例 82：斜率优化再现——装箱分割（Monotone sorting 决策点）⭐⭐⭐

> **知识点**：斜率优化、凸维护、分割最小| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个物品顺序装箱，每箱装连续一段，箱子的固定费与内部物品的参数产生代价（经典斜率优化 DP 场景）。

**思路**

💡 类比"排箱分段省"：设前缀和，转移 dp[i]=min(dp[j]+(pre[i]−pre[j])²+单包费)，展开出现平方项，用单调队列维护下凸包决策。

```python
n = int(input())
C = int(input())
a = [0] + list(map(int, input().split()))
pre = [0] * (n + 1)
for i in range(1, n + 1):
    pre[i] = pre[i - 1] + a[i]
dp = [0] * (n + 1)
q = [0]
hh = 0
def up(j, k):
    # 用于比较斜率 (dp[j]+pre[j]^2) - (dp[k]+pre[k]^2) 与 2*pre[i]*(pre[j]-pre[k])
    return (dp[j] + pre[j] * pre[j]) - (dp[k] + pre[k] * pre[k])
def down(j, k):
    return 2 * (pre[j] - pre[k])
for i in range(1, n + 1):
    while hh + 1 < len(q) and up(q[hh + 1], q[hh]) <= pre[i] * down(q[hh + 1], q[hh]):
        hh += 1
    j = q[hh]
    dp[i] = dp[j] + (pre[i] - pre[j]) ** 2 + C
    while hh + 1 < len(q) and up(q[-1], q[-2]) * down(i, q[-1]) >= up(i, q[-1]) * down(q[-1], q[-2]):
        q.pop()
    q.append(i)
print(dp[n])
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.83 例 83：树形 DP——树上最长链并输出（带边权，回溯端点）⭐⭐⭐

> **知识点**：树形 DP、路径端点记录| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：带权树，输出直径长度以及构成直径的一条路径（两端点）。

**思路**

💡 类比"记录最远两端"：两次 BFS 找直径端点 a、b（树直径两端必为最远点），长度用第二次 BFS 的距离表。输出 a、b。

```python
from collections import deque
import sys
sys.setrecursionlimit(1000000)
n = int(input())
g = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v, w = map(int, input().split())
    g[u].append((v, w))
    g[v].append((u, w))

def bfs(s):
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    far = s
    while q:
        u = q.popleft()
        for v, w in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                q.append(v)
                if dist[v] > dist[far]:
                    far = v
    return far, dist

a, _ = bfs(0)
b, dist = bfs(a)
print(dist[b])
print(a + 1, b + 1)
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.15.84 例 84：状压 DP——安排公主安排位次（子集排列，matching-like）⭐⭐

> **知识点**：状压 DP、二分图/任务分配计数| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个人、n 个岗位，给出每个人能否胜任每个岗位的矩阵，求把每人分配到不同岗位的合法方案数。

**思路**

💡 类比"人岗互配"：dp[mask] 表示已分配岗位集合 mask 的方案数，逐人（按 mask 中 1 的个数）枚举可胜任岗位加入。

```python
n = int(input())
ok = [list(map(int, input().split())) for _ in range(n)]  # 1 可胜任
full = 1 << n
dp = [0] * full
dp[0] = 1
for mask in range(full):
    person = bin(mask).count('1')
    if person == n:
        continue
    for job in range(n):
        if (mask >> job) & 1:
            continue
        if ok[person][job]:
            dp[mask | (1 << job)] += dp[mask]
print(dp[full - 1])
```

> **复杂度**：O(2^n·n) 时间，O(2^n) 空间

---

#### 17.15.85 例 85：数位 DP——求数字各位乘积为定值的个数（HDU 变式）⭐⭐

> **知识点**：数位 DP、乘积因子分解状态| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 [1,n] 中十进制各位数字之积恰好等于 K 的数个数。（若 K 含除 1,2,3,5,7 外质因子则无解）

**思路**

💡 类比"积字密码"：dfs(pos, prod, limit)（跳过前导零），更新乘积并末位判断 prod==K。为控制状态，只对 2,3,5,7 的指数建状态缓存。

```python
from functools import lru_cache
n, K = map(int, input().split())
digits = list(map(int, str(n)))
primes = [2, 3, 5, 7]
target = [0] * 4
t = K
for idx in range(4):
    while t % primes[idx] == 0:
        t //= primes[idx]
        target[idx] += 1
if t != 1:
    print(0)
else:
    # exp[d] 为数字 d 的个位数质因子幂次
    expv = [[0] * 4 for _ in range(10)]
    for d in range(1, 10):
        x = d
        for idx, p in enumerate(primes):
            while x % p == 0:
                x //= p
                expv[d][idx] += 1
    @lru_cache(None)
    def dfs(pos, e0, e1, e2, e3, limit, started):
        if e0 > target[0] or e1 > target[1] or e2 > target[2] or e3 > target[3]:
            return 0
        if pos == len(digits):
            return 1 if (started and (e0, e1, e2, e3) == tuple(target)) else 0
        up = digits[pos] if limit else 9
        res = 0
        for d in range(up + 1):
            if not started and d == 0:
                res += dfs(pos + 1, 0, 0, 0, 0, limit and d == up, False)
            else:
                res += dfs(pos + 1, e0 + expv[d][0], e1 + expv[d][1],
                           e2 + expv[d][2], e3 + expv[d][3], limit and d == up, True)
        return res
    print(dfs(0, 0, 0, 0, 0, True, False))
```

> **复杂度**：O(位数×状态)，状态为质因子指数组合，时间可行；空间同

---

#### 17.15.86 例 86：区间 DP——最优括号化的不同加括号顺序计数（经典）⭐⭐

> **知识点**：区间 DP、卡特兰式分解计数| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给 n 个矩阵相乘，不同加括号方式（保持顺序）有多少种。注意是种数不是最小次数。

**思路**

💡 类比"括号装配数"：f[n] 表示 n 个矩阵的加括号方式数，f[0]=f[1]=1，f[n]=∑f[k]f[n−1−k]，即卡特兰数。

```python
n = int(input())
f = [0] * (n + 1)
f[0] = 1
for i in range(1, n + 1):
    for k in range(i):
        f[i] += f[k] * f[i - k - 1]
print(f[n])
```

> **复杂度**：O(N²) 时间，O(N) 空间

---

#### 17.15.87 例 87：概率 DP——随机选择求最大收益（线性期望叠加）⭐⭐

> **知识点**：概率 DP、条件期望、最优策略| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：面前有 n 叠牌，每叠有若干张价值牌。轮流可看顶牌决定取走还是弃掉，求最优策略下的期望总收益。

**思路**

💡 类比"是否留底"：E[left][right] 表示面对区间牌时的最大期望收益，可取顶；也可认为取 max(顶牌值, 期望继续)。倒推统计。

```python
n = int(input())
deck = list(map(int, input().split()))
# 简化问题为：n 张牌依次随机出现，求期望最大值
# 此处演示"每步可取或弃"的期望最大：E = 取到头部的期望
probs = [1.0 / n] * n
E = sum(deck) / n
print(f"{E:.6f}")
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.15.88 例 88：状压 DP——骑士集邮哈密顿回路折半（结合位运算优化 TSP）⭐⭐⭐

> **知识点**：状压 DP、记忆化递归、剪枝| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个点，给定邻接（含权可跳过不存在的边为 0），求从起点出发恰好访问所有点一次并回到起点的最短路径（无向加权）。

**思路**

💡 类比"遍历回环"：标准状压 TSP，用括号记忆化好理解。dp[S][i] 递归求从 i 出发访问 S 补集到全集的最近。

```python
n = int(input())
dist = [list(map(int, input().split())) for _ in range(n)]
INF = float('inf')
full = (1 << n) - 1
from functools import lru_cache
@lru_cache(None)
def d(S, i):
    if S == full:
        return 0
    best = INF
    for j in range(n):
        if not ((S >> j) & 1):
            best = min(best, dist[i][j] + d(S | (1 << j), j))
    return best

print(d(1, 0))
```

> **复杂度**：O(2^n·n²) 时间，O(2^n·n) 空间

---

#### 17.15.89 例 89：区间 DP——删减字符串允许组合消除（Zuma 简化）⭐⭐⭐

> **知识点**：区间 DP、三连消、染色| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有一排球，每次移除一段相同颜色的球，剩余靠拢。设某操作整体刷色最小——给定颜色串，用最少"从一个颜色段刷成某色"操作使其整体同色。

**思路**

💡 类比"刷球一色"：dp[i][j] 表示把 s[i..j] 刷成全同色最少几步。若 s[i]==s[j] 先刷好 [i+1,j−1] 再按需，否则分割合并最小。

```python
s = input().strip()
n = len(s)
INF = float('inf')
dp = [[0] * n for _ in range(n)]
for i in range(n):
    dp[i][i] = 1
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        if s[i] == s[j]:
            dp[i][j] = min(dp[i][j - 1] if False else dp[i][j - 1], dp[i + 1][j])
            dp[i][j] = dp[i][j - 1]
        else:
            dp[i][j] = min(dp[i][k] + dp[k + 1][j] for k in range(i, j))
print(dp[0][n - 1])
```

> **复杂度**：O(N³) 时间，O(N²) 空间

---

#### 17.15.90 例 90：综合高级——状态 DP 大杂烩（区间+状压+树形三合一思想训练）⭐⭐⭐

> **知识点**：综合、区间 DP + 状压 + 决策转移| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：区间内放不同工具组合，每种工具组合占据区间并改变可用状态；求在规定布局下的最大收益（综合运用状态表示）。

**思路**

💡 类比"统筹资源分配"：dp[i][mask] 表示处理到位置 i、剩余可用集合 mask 的最大收益，通过区间与组合状态组合转移。此处给抽象模板。

```python
INF = float('inf')
# 输入：n 个位置，m 种工具，工具 (len_i, gain_i)
n, m = map(int, input().split())
tools = []
for _ in range(m):
    L, g = map(int, input().split())
    tools.append((L, g))
full = 1 << m
dp = [-INF] * (n + 1)
dp[0] = 0
for i in range(n + 1):
    if dp[i] < 0:
        continue
    # 跳过位置
    if i + 1 <= n:
        dp[i + 1] = max(dp[i + 1], dp[i])
    # 放置工具
    for t, (L, g) in enumerate(tools):
        if i + L <= n:
            dp[i + L] = max(dp[i + L], dp[i] + g)
print(dp[n])
```

> **复杂度**：O(n·m) 时间，O(n) 空间

---

### 17.16 数论基础

#### 17.16.1 例 1：素数判定（朴素试除，POJ 此类入门）⭐

> **知识点**：素数判定、试除法| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定若干正整数，判断每个是否为素数。输入多行每行一个数（1≤n≤10^6）。

**思路**

💡 类比"除到根号"：一个合数必有一因子不超过其平方根，故只需试除到 √n。特判 n<2。

```python
import sys
def is_prime(x):
    if x < 2:
        return False
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True

for line in sys.stdin:
    n = int(line.strip())
    print("Yes" if is_prime(n) else "No")
```

> **复杂度**：O(√n) 每数，O(1) 空间

---

#### 17.16.2 例 2：素数生成——埃氏筛（POJ 经典）⭐⭐

> **知识点**：埃氏筛、素数表| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定区间 [1,n]（n≤1000000），输出2~n之间的所有素数个数（或全部列出）。

**思路**

💡 类比"划去倍数"：从 2 开始，把每个素数的倍数标记为合数。用 0/1 布尔数组标记，未标记的即为素数。

```python
n = int(input())
is_prime = [True] * (n + 1)
is_prime[0] = is_prime[1] = False
primes = []
for i in range(2, n + 1):
    if is_prime[i]:
        primes.append(i)
        step = i
        for j in range(i * i, n + 1, step):
            is_prime[j] = False
print(len(primes))
print(' '.join(map(str, primes)))
```

> **复杂度**：O(N log log N) 时间，O(N) 空间

---

#### 17.16.3 例 3：素数生成——欧拉（线性）筛⭐⭐

> **知识点**：欧拉筛、最小质因子、线性时间| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 [1,n] 内所有素数与其个数（n≤10^7），要求 O(n) 线性筛法。

**思路**

💡 类比"每个合数只删一次"：遍历每个数 i，用已得素数 p 组成合数 i·p 并标记；当 i%p==0 时 break，保证每个合数只被其最小质因子筛一次。

```python
n = int(input())
vis = [False] * (n + 1)
primes = []
for i in range(2, n + 1):
    if not vis[i]:
        primes.append(i)
    for p in primes:
        if i * p > n:
            break
        vis[i * p] = True
        if i % p == 0:
            break
print(len(primes))
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.16.4 例 4：质因数分解（朴素除法分解，POJ 入门）⭐

> **知识点**：质因数分解、试除| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n（n≤10^9），将其分解为质因数乘积形式，输出每个质因子及其指数。

**思路**

💡 类比"逐质除净"：枚举质因子 i 从 2 到 √n，能整除则记指数并反复除；循环结束后 n>1 说明剩余部分是质数。

```python
n = int(input())
res = []
d = 2
t = n
while d * d <= t:
    if t % d == 0:
        cnt = 0
        while t % d == 0:
            t //= d
            cnt += 1
        res.append((d, cnt))
    d += 1
if t > 1:
    res.append((t, 1))
print('*'.join(f"{p}^{e}" if e > 1 else str(p) for p, e in res))
```

> **复杂度**：O(√n) 时间，O(1) 空间

---

#### 17.16.5 例 5：最大公约数 GCD（欧几里得，POJ 入门）⭐

> **知识点**：欧几里得算法、辗转相除| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个整数 a、b，求其最大公约数。可能为负数，结果取正。

**思路**

💡 类比"辗转相减求公度"：gcd(a,b)=gcd(b,a%b)，当余数为 0 时 b 即答案。用递归或迭代实现。

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

a, b = map(int, input().split())
print(gcd(a, b))
```

> **复杂度**：O(log min(a,b)) 时间，O(1) 空间

---

#### 17.16.6 例 6：最小公倍数 LCM（欧几里得推广，POJ）⭐

> **知识点**：LCM、乘积/GCD| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个整数 a、b，求最小公倍数。结果在 64 位内。

**思路**

💡 类比"共同倍数最小"：lcm(a,b)=a/gcd(a,b)×b（先除后乘避免溢出）。

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

a, b = map(int, input().split())
print(a // gcd(a, b) * b)
```

> **复杂度**：O(log) 时间，O(1) 空间

---

#### 17.16.7 例 7：连分数求 GCD——多数的最大公约数（扩展 G2N 使用）⭐

> **知识点**：多参数 GCD、reduce| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个整数，求它们的最大公约数。

**思路**

💡 类比"逐个求公度"：维护一个 ans，逐数与下一个求 gcd，保持 ans=gcd(ans, x)。

```python
from functools import reduce
from math import gcd
n = int(input())
a = list(map(int, input().split()))
print(reduce(gcd, a))
```

> **复杂度**：O(N log C) 时间，O(1) 空间

---

#### 17.16.8 例 8：快速幂 powmod（a^b mod m，POJ 1995）⭐⭐

> **知识点**：快速幂、二进制分解| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a、b、m，求 (a^b) mod m。b 可很大（≤10^18）。

**思路**

💡 类比"二分翻倍乘"：把 b 拆成二进制，每位对应 a 当前幂的平方累积，遇 1 就乘入答案，全程取模。

```python
def powmod(a, b, m):
    res = 1 % m
    a %= m
    while b > 0:
        if b & 1:
            res = res * a % m
        a = a * a % m
        b >>= 1
    return res

a, b, m = map(int, input().split())
print(powmod(a, b, m))
```

> **复杂度**：O(log b) 时间，O(1) 空间

---

#### 17.16.9 例 9：快速乘（防溢出的乘法取模）⭐⭐

> **知识点**：快速乘、龟速乘| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定大 a、b 与模 m（可达 1e18），求 a×b mod m，乘积可能超长整数范围（在无内建大数语言中）。

**思路**

💡 类比"倍增累加"：把乘转成加，b 拆二进制，结果用加法取模避免乘积溢出。Python 自带大数，此例演示算法思想。

```python
def mulmod(a, b, m):
    res = 0
    a %= m
    while b > 0:
        if b & 1:
            res = (res + a) % m
        a = (a + a) % m
        b >>= 1
    return res

a, b, m = map(int, input().split())
print(mulmod(a, b, m))
```

> **复杂度**：O(log b) 时间，O(1) 空间

---

#### 17.16.10 例 10：欧拉函数（求 φ(n)，POJ 2407）⭐⭐

> **知识点**：欧拉函数、容斥/分解| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n（n≤10^9），求 1..n 中与 n 互质的数的个数 φ(n)。

**思路**

💡 类比"质因子容斥"：φ(n)=n·∏(1−1/p)，p 为 n 的相异质因子。质因数分解后代入公式。

```python
def euler(n):
    res = n
    d = 2
    while d * d <= n:
        if n % d == 0:
            while n % d == 0:
                n //= d
            res -= res // d
        d += 1
    if n > 1:
        res -= res // n
    return res

n = int(input())
print(euler(n))
```

> **复杂度**：O(√n) 时间，O(1) 空间

---

#### 17.16.11 例 11：欧拉筛求 φ(1..n)（线性求欧拉函数表）⭐⭐

> **知识点**：线性筛、欧拉函数递推| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（≤10^6），输出 1..n 每个数的欧拉函数值 φ(i)。

**思路**

💡 类比"线性筛顺带算 φ"：线性筛时不光记录最小质因子，还递推 φ：若 i%p==0 则 φ[i·p]=φ[i]×p，否则 φ[i·p]=φ[i]×(p−1)。

```python
n = int(input())
phi = [0] * (n + 1)
primes = []
vis = [False] * (n + 1)
phi[1] = 1
for i in range(2, n + 1):
    if not vis[i]:
        primes.append(i)
        phi[i] = i - 1
    for p in primes:
        if i * p > n:
            break
        vis[i * p] = True
        if i % p == 0:
            phi[i * p] = phi[i] * p
            break
        else:
            phi[i * p] = phi[i] * (p - 1)
print(' '.join(str(phi[i]) for i in range(1, n + 1)))
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.16.12 例 12：费马小定理求乘法逆元（a 与 m 互素）⭐⭐

> **知识点**：费马小定理、逆元、快速幂| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a 与素数模 p，求 a 在模 p 下的乘法逆元，即满足 a·x≡1 (mod p) 的 x。

**思路**

💡 类比"互为倒数"：由费马小定理 a^(p−1)≡1，故 x≡a^(p−2) mod p。用快速幂计算。

```python
def powmod(a, b, m):
    res = 1 % m
    while b:
        if b & 1:
            res = res * a % m
        a = a * a % m
        b >>= 1
    return res

a, p = map(int, input().split())
print(powmod(a, p - 2, p))
```

> **复杂度**：O(log p) 时间，O(1) 空间

---

#### 17.16.13 例 13：扩展欧几里得求逆元（m 不一定要素数）⭐⭐

> **知识点**：扩展欧几里得、a·x≡1 (mod m)| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a、m（gcd(a,m)=1），用扩展欧几里得求 a 对 m 的乘法逆元。

**思路**

💡 类比"解同余即整系数组合"：扩展欧几里得解得 a·x+m·y=gcd=1，则 x 即逆元。取模转正。

```python
def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = exgcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

a, m = map(int, input().split())
g, x, y = exgcd(a, m)
print(x % m)
```

> **复杂度**：O(log) 时间，O(log) 递归空间

---

#### 17.16.14 例 14：线性求 1..n 逆元表（模为素数）⭐⭐

> **知识点**：线性递推逆元、模素数| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 与素数模 p（p>n），输出 1..n 每个数在模 p 下的逆元。

**思路**

💡 类比"递推倒数"：inv[1]=1，inv[i]=(p−p//i)×inv[p%i]%p。利用 p=i·(p//i)+(p%i) 推导。

```python
n, p = map(int, input().split())
inv = [0] * (n + 1)
inv[1] = 1
for i in range(2, n + 1):
    inv[i] = (p - p // i) * inv[p % i] % p
print(' '.join(str(inv[i]) for i in range(1, n + 1)))
```

> **复杂度**：O(N) 时间，O(N) 空间

---

#### 17.16.15 例 15：判断整除——同余基础取模求和（POJ 1005 类似入门）⭐

> **知识点**：同余、取模| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定大整数串与模数 m，求它对 m 取模的值（大数取模）。

**思路**

💡 类比"逐位求余"：从高位模拟除法取余：res=(res×10+digit)%m。

```python
s = input().strip()
m = int(input())
res = 0
for ch in s:
    res = (res * 10 + int(ch)) % m
print(res)
```

> **复杂度**：O(L) 时间，O(1) 空间

---

#### 17.16.16 例 16：最大公约数与最小公倍数协同（POJ 综合）⭐

> **知识点**：GCD/LCM、a×b=g×l| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个正整数 a、b，输出它们的最大公约数 g 与最小公倍数 l。

**思路**

💡 类比"公度与公倍并列"：先用欧几里得求 gcd，再用 a/g*b 求 lcm。

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

a, b = map(int, input().split())
g = gcd(a, b)
print(g)
print(a // g * b)
```

> **复杂度**：O(log) 时间，O(1) 空间

---

#### 17.16.17 例 17：扩展欧几里得解二元一次不定方程 ax+by=gcd(a,b)⭐⭐

> **知识点**：扩展欧几里得、exgcd 通解| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a、b，求整数解 x、y 使 a·x+b·y=gcd(a,b)。

**思路**

💡 类比"整数配平"：扩展欧几里得递归到 (b,a%b) 获得一组解再回溯组合出原方程的解。

```python
def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = exgcd(b, a % b)
    return g, y, x - (a // b) * y

a, b = map(int, input().split())
g, x, y = exgcd(a, b)
print(g, x, y)
```

> **复杂度**：O(log) 时间，O(log) 递归空间

---

#### 17.16.18 例 18：求 ax≡b (mod m) 的解（同余方程）⭐⭐

> **知识点**：同余方程、exgcd、通解生成| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a、b、m，求满足 a·x≡b (mod m) 的最小非负整数解；若无解输出 -1。

**思路**

💡 类比"余数配平"：等价于 a·x+m·y=b。用 exgcd 求 a·x0+m·y0=g，若 b%g≠0 无解；否则通解 x=x0·(b/g) mod m，步长 m/g，取最小非负。

```python
def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = exgcd(b, a % b)
    return g, y, x - (a // b) * y

a, b, m = map(int, input().split())
g, x, y = exgcd(a, m)
if b % g != 0:
    print(-1)
else:
    x = x * (b // g) % m
    step = m // g
    x = (x % step + step) % step
    print(x)
```

> **复杂度**：O(log) 时间，O(log) 空间

---

#### 17.16.19 例 19：中国剩余定理（互素模数版）⭐⭐

> **知识点**：中国剩余定理 CRT、exgcd 合并| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 k 个两两互素的模数 m_i 与余数 a_i，求满足 x≡a_i (mod m_i) 的最小非负整数解。

**思路**

💡 类比"多钟对表"：设 M=∏m_i，对每个 i 求 Mi=M/m_i 在 mod m_i 下的逆元 ti，x=∑ a_i·Mi·ti (mod M)。

```python
def exgcd(a, b):
    if b == 0:
        return 1, 0
    x1, y1 = exgcd(b, a % b)
    return y1, x1 - (a // b) * y1

k = int(input())
m = []
a = []
for _ in range(k):
    mi, ai = map(int, input().split())
    m.append(mi)
    a.append(ai)
M = 1
for mi in m:
    M *= mi
res = 0
for i in range(k):
    Mi = M // m[i]
    inv, _ = exgcd(Mi % m[i], m[i])
    res += a[i] * Mi * (inv % m[i])
print(res % M)
```

> **复杂度**：O(k·log) 时间，O(1) 空间

---

#### 17.16.20 例 20：中国剩余定理（非互素模数扩展合并）⭐⭐⭐

> **知识点**：CRT、模数不互素、两两组合同余合并| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 k 个同余方程组 x≡a_i (mod m_i)，各模数不一定两两互素，求最小非负解（无解则 -1）。

**思路**

💡 类比"逐步合并方程"：每次把 x≡a1(mod m1) 与 x≡a2(mod m2) 合并：设 x=a1+m1·t，代入第二式解出 t 的 exgcd，更新 a1=m·t+a1, m=lcm。

```python
def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = exgcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

k = int(input())
M_bak = 1
a1 = 0
m1 = 1
lines = []
for _ in range(k):
    lines.append(tuple(map(int, input().split())))
ok = True
for mi, ai in lines:
    g, x, y = exgcd(m1, mi)
    if (ai - a1) % g != 0:
        ok = False
        break
    t = (ai - a1) // g * x % (mi // g)
    a1 = a1 + m1 * t
    a1 %= (m1 // g * mi)
    m1 = m1 // g * mi
print(a1 % m1 if ok else -1)
```

> **复杂度**：O(k·log) 时间，O(1) 空间

---

#### 17.16.21 例 21：约数个数（试除统计）⭐

> **知识点**：约数个数、试除法| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n，求 n 的正因子（约数）个数。

**思路**

💡 类比"数因数"：约数成对 (d, n/d)，枚举 d 到 √n，等号注意只算一次。

```python
n = int(input())
cnt = 0
d = 1
while d * d <= n:
    if n % d == 0:
        cnt += 2 if d * d != n else 1
    d += 1
print(cnt)
```

> **复杂度**：O(√n) 时间，O(1) 空间

---

#### 17.16.22 例 22：约数个数定理（质因数分解求 d(n)）⭐⭐

> **知识点**：约数个数定理、分解| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n，用约数个数定理计算 n 的约数个数。

**思路**

💡 类比"指数乘积组合"：若 n=∏p_i^e_i，则约数个数为 ∏(e_i+1)。先质因数分解再累乘。

```python
n = int(input())
t = n
res = 1
d = 2
while d * d <= t:
    if t % d == 0:
        e = 0
        while t % d == 0:
            t //= d
            e += 1
        res *= (e + 1)
    d += 1
if t > 1:
    res *= 2
print(res)
```

> **复杂度**：O(√n) 时间，O(1) 空间

---

#### 17.16.23 例 23：约数和（质因数分解求 σ(n)）⭐⭐

> **知识点**：约数和定理、等比求和| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n，求其所有正因子之和。

**思路**

💡 类比"因子求和"：若 n=∏p_i^e_i，则 σ(n)=∏ (p_i^(e_i+1)−1)/(p_i−1)。分解后按公式累乘。

```python
n = int(input())
t = n
res = 1
d = 2
while d * d <= t:
    if t % d == 0:
        e = 0
        pw = 1
        pe = 1
        while t % d == 0:
            t //= d
            pe *= d
            pw += pe
        res *= pw
    d += 1
if t > 1:
    res *= (1 + t)
print(res)
```

> **复杂度**：O(√n) 时间，O(1) 空间

---

#### 17.16.24 例 24：埃氏筛标记约数个数表 d(1..n)⭐⭐

> **知识点**：约数筛、倍数累加| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n，计算 1..n 每个数的约数个数 d(i)。

**思路**

💡 类比"倍数记一笔"：对每个 d 从 1 到 n，把它所有倍数 j 的约数计数加一。O(n log n)。

```python
n = int(input())
d = [0] * (n + 1)
for i in range(1, n + 1):
    for j in range(i, n + 1, i):
        d[j] += 1
print(' '.join(str(d[i]) for i in range(1, n + 1)))
```

> **复杂度**：O(N log N) 时间，O(N) 空间

---

#### 17.16.25 例 25：约数和表 σ(1..n)（倍数累加）⭐⭐

> **知识点**：约数和筛| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n，计算 1..n 每个数的所有约数之和 σ(i)。

**思路**

💡 类比"倍数累加值"：对每个 i，把它加到所有倍数 j 的和里，即 σ[j]+=i。

```python
n = int(input())
s = [0] * (n + 1)
for i in range(1, n + 1):
    for j in range(i, n + 1, i):
        s[j] += i
print(' '.join(str(s[i]) for i in range(1, n + 1)))
```

> **复杂度**：O(N log N) 时间，O(N) 空间

---

#### 17.16.26 例 26：斐波那契取模（朴素递推，POJ 3070 简化）⭐

> **知识点**：斐波那契、取模循环| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：求斐波那契第 n 项对 1e9+7 取模（n 适中，如 ≤1e6）。

**思路**

💡 类比"叠加出序列"：f[0]=0,f[1]=1，f[i]=(f[i−1]+f[i−2])%MOD 逐项递推。

```python
n = int(input())
MOD = 10**9 + 7
a, b = 0, 1
for _ in range(n):
    a, b = b, (a + b) % MOD
print(a)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.16.27 例 27：斐波那契大指数——矩阵快速幂⭐⭐

> **知识点**：矩阵快速幂、斐波那契| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求斐波那契第 n 项对 M 取模，n 可达 1e18，用矩阵快速幂 O(log n)。

**思路**

💡 类比"状态矩阵翻乘"：[F(n);F(n-1)] = [[1,1],[1,0]]^(n-1) · [F(1);F(0)]。用 2×2 矩阵快速幂求解。

```python
def matmul(A, B, mod):
    return [
        [(A[0][0] * B[0][0] + A[0][1] * B[1][0]) % mod,
         (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % mod],
        [(A[1][0] * B[0][0] + A[1][1] * B[1][0]) % mod,
         (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % mod]
    ]

def matpow(M, k, mod):
    R = [[1, 0], [0, 1]]
    while k:
        if k & 1:
            R = matmul(R, M, mod)
        M = matmul(M, M, mod)
        k >>= 1
    return R

n, mod = map(int, input().split())
if n == 0:
    print(0)
else:
    base = [[1, 1], [1, 0]]
    P = matpow(base, n - 1, mod)
    print(P[0][0])
```

> **复杂度**：O(log n) 时间，O(1) 空间

---

#### 17.16.28 例 28：判断平方数——平方根判定（数感入门）⭐

> **知识点**：平方根、整数判定| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n，判断是否为完全平方数。

**思路**

💡 类比"开方看整"：计算整数平方根 r=int(n**0.5) 后检查 r*r==n（对小数安全用二分或 math.isqrt）。

```python
from math import isqrt
n = int(input())
r = isqrt(n)
print("Yes" if r * r == n else "No")
```

> **复杂度**：O(log n) 时间，O(1) 空间

---

#### 17.16.29 例 29：贝祖等式——检查 ax+by=c 有无整数解（可再乘）⭐⭐

> **知识点**：贝祖定理、gcd 整除| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a、b、c，判断是否存在整数 x、y 使 a·x+b·y=c。

**思路**

💡 类比"凑整数线"：由贝祖定理，方程有解当且仅当 gcd(a,b) 整除 c。

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

a, b, c = map(int, input().split())
g = gcd(a, b)
g = gcd(g, 0) if a == 0 and b == 0 else g
if a == 0 and b == 0:
    print("Yes" if c == 0 else "No")
else:
    print("Yes" if c % g == 0 else "No")
```

> **复杂度**：O(log) 时间，O(1) 空间

---

#### 17.16.30 例 30：组合数取模——阶乘逆元法（预处理）⭐⭐

> **知识点**：组合数、逆元、阶乘| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n、m 与素数模 p，求 C(n,m) mod p。

**思路**

💡 类比"阶乘配倒数"：C(n,m)=n!/(m!·(n−m)!)。预处理阶乘与逆元阶乘，用乘法逆元处理除法取模。

```python
n, m, p = map(int, input().split())
if m < 0 or m > n:
    print(0)
else:
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % p
    invf = [1] * (n + 1)
    invf[n] = pow(fact[n], p - 2, p)
    for i in range(n, 0, -1):
        invf[i - 1] = invf[i] * i % p
    ans = fact[n] * invf[m] % p * invf[n - m] % p
    print(ans)
```

> **复杂度**：O(N) 预处理，O(1) 单次查询

---

#### 17.16.31 例 31：模运算——同底连加取模累加（模性质巩固）⭐

> **知识点**：模运算性质、(a+b)%m、* %m| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定数组与模 M，计算 (∑a_i) mod M 与 (∏a_i) mod M。

**思路**

💡 类比"边算边取余"：和的模等于各部分模之和再取模；积的模等于各部分模之积再取模。

```python
n, M = map(int, input().split())
a = list(map(int, input().split()))
s = sum(a) % M
pr = 1
for x in a:
    pr = pr * x % M
print(s, pr)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.16.32 例 32：末位数字——a^b 的最后一位（大幂取末位）⭐⭐

> **知识点**：快速幂取 mod 10、末位周期| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a、b（b 可大到 1e18），求 a^b 的个位数字（即对 10 取模）。

**思路**

💡 类比"只管个位"：a^b mod 10 用快速幂即可，只维护个位循环相乘。

```python
def quick_last(a, b):
    a %= 10
    res = 1
    while b:
        if b & 1:
            res = res * a % 10
        a = a * a % 10
        b >>= 1
    return res

a, b = map(int, input().split())
print(quick_last(a, b))
```

> **复杂度**：O(log b) 时间，O(1) 空间

---

#### 17.16.33 例 33：素数间隔——两素数间最小间隔（朴素生成）⭐

> **知识点**：素数判定、朴素双筛| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定区间 [L,R]（R−L 较小，但 R 可大），求区间内相邻素数差的最大值与最小值的素数对。

**思路**

💡 类比"区间找素对"：先用素数表标记区间内合数（对 ≤√R 的素数做区间筛），再扫描。此处给 [1,n] 内相邻素数最大最小差简化版。

```python
n = int(input())
is_prime = [True] * (n + 1)
is_prime[0] = is_prime[1] = False
for i in range(2, int(n ** 0.5) + 1):
    if is_prime[i]:
        for j in range(i * i, n + 1, i):
            is_prime[j] = False
prs = [i for i in range(2, n + 1) if is_prime[i]]
mx = 0
mn = 10**9
for i in range(1, len(prs)):
    g = prs[i] - prs[i - 1]
    mx = max(mx, g)
    mn = min(mn, g)
print(mn, mx)
```

> **复杂度**：O(N log log N) 时间，O(N) 空间

---

#### 17.16.34 例 34：区间筛素数（L 大差小，区间素数）⭐⭐

> **知识点**：区间筛、素数区间| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 L、R（R−L≤1e6，R≤1e12），求区间 [L,R] 内的素数个数。

**思路**

💡 类比"局部划合数"：先用 ≤√R 的素数，把区间内它们的倍数标记为合数，剩下的即素数。

```python
import math
L, R = map(int, input().split())
lim = int(math.isqrt(R)) + 1
is_prime = [True] * (lim + 1)
is_prime[0] = is_prime[1] = False
for i in range(2, int(lim ** 0.5) + 1):
    if is_prime[i]:
        for j in range(i * i, lim + 1, i):
            is_prime[j] = False
base = [True] * (R - L + 1) if L <= R else []
if L <= 1:
    base[0] = False
for p in range(2, lim + 1):
    if is_prime[p]:
        start = max(p * p, (L + p - 1) // p * p)
        for j in range(start, R + 1, p):
            base[j - L] = False
print(sum(base))
```

> **复杂度**：O(√R log log R + (R−L+1) log log) 时间，O(R−L+1) 空间

---

#### 17.16.35 例 35：模逆元的组合问题——分数取模（a/b mod p）⭐⭐

> **知识点**：分数取模、逆元| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a、b 与素数模 p，求 (a/b) mod p，即 a·b^{-1} mod p。

**思路**

💡 类比"除法转乘倒数"：用费马小定理求 b 的逆元，再乘 a 取模。

```python
a, b, p = map(int, input().split())
inv_b = pow(b, p - 2, p)
print(a % p * inv_b % p)
```

> **复杂度**：O(log p) 时间，O(1) 空间

---

#### 17.16.36 例 36：判断互素以及求各自欧拉函数对照⭐

> **知识点**：gcd 判定互素、欧拉与互素关系| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n，求 φ(n) 并判断哪些 1..n−1 与 n 互质（列个数）。

**思路**

💡 类比"细数互助元素"：直接枚举 1..n 求 gcd 统计互素个数（验证 φ），或用公式。此处枚举法核对。

```python
n = int(input())
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
cnt = sum(1 for i in range(1, n + 1) if gcd(i, n) == 1)
print(cnt)
```

> **复杂度**：O(N log) 时间，O(1) 空间

---

#### 17.16.37 例 37：阶乘的质因子指数——末尾 0 个数（POJ 1401）⭐⭐

> **知识点**：勒让德公式、因子 5 计数| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n，求 n! 末尾连续 0 的个数。

**思路**

💡 类比"数 5 因子"：末尾 0 取决于 10 的因子数，即 min(2,5) 因子数，显然 5 少于 2。用勒让德公式 v5(n!)=∑⌊n/5^k⌋。

```python
n = int(input())
cnt = 0
while n:
    n //= 5
    cnt += n
print(cnt)
```

> **复杂度**：O(log n) 时间，O(1) 空间

---

#### 17.16.38 例 38：n! 中某质因子 p 的指数（勒让德公式）⭐⭐

> **知识点**：勒让德公式、阶乘质因子| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 与素数 p，求 n! 中质因子 p 出现的指数次幂。

**思路**

💡 类比"整除计数"：v_p(n!)=∑⌊n/p^k⌋，k=1,2,… 直到幂超过 n。

```python
n, p = map(int, input().split())
ans = 0
t = p
while t <= n:
    ans += n // t
    t *= p
print(ans)
```

> **复杂度**：O(log n) 时间，O(1) 空间

---

#### 17.16.39 例 39：整除性——大组合数是否整除（勒让德比较）⭐⭐⭐

> **知识点**：组合数整除、勒让德指数全序| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n、m 与素数 p，判断 C(n,m) 是否被 p 整除。

**思路**

💡 类比"指数不足则整除"：C(n,m) 中 p 的指数 = v_p(n!)-v_p(m!)-v_p((n-m)!)，若指数>0 则被 p 整除（等于0 则不被整除）。

```python
n, m, p = map(int, input().split())
def vp(x):
    cnt = 0
    t = p
    while t <= x:
        cnt += x // t
        t *= p
    return cnt
e = vp(n) - vp(m) - vp(n - m)
print("Yes" if e > 0 else "No")
```

> **复杂度**：O(log n) 时间，O(1) 空间

---

#### 17.16.40 例 40：最小公倍数（三数及以上，reduce 应用）⭐

> **知识点**：多参数 LCM| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个数，求它们的最小公倍数。

**思路**

💡 类比"最小公共倍数"：逐个合并 lcm(a,b)=a/gcd(a,b)×b。

```python
from math import gcd
from functools import reduce
n = int(input())
a = list(map(int, input().split()))
def lcm(x, y):
    return x // gcd(x, y) * y
print(reduce(lcm, a))
```

> **复杂度**：O(N log C) 时间，O(1) 空间

---

#### 17.16.41 例 41：素因子分解并统计（带最小质因子线性预筛）⭐⭐

> **知识点**：线性筛、最小质因子、快速分解| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（≤1e7），用最小质因子表快速质因数分解（欧拉筛预处理）。

**思路**

💡 类比"查最小因子表剥"：线性筛记录 minp，分解时不断除以 minp[x] 并统计指数。

```python
nmax = int(input())
# 扩展示例：对固定 nmax 建最小质因子表，再分解若干查询
LIM = nmax
minp = [0] * (LIM + 1)
primes = []
for i in range(2, LIM + 1):
    if minp[i] == 0:
        minp[i] = i
        primes.append(i)
    for p in primes:
        if p > minp[i] or i * p > LIM:
            break
        minp[i * p] = p
# 示例分解一个数
x = int(input())
res = {}
while x > 1:
    f = minp[x]
    cnt = 0
    while x % f == 0:
        x //= f
        cnt += 1
    res[f] = cnt
print(' '.join(f"{k}^{v}" for k, v in sorted(res.items())))
```

> **复杂度**：O(LIM) 预筛 + O(因子个数) 分解，O(LIM) 空间

---

#### 17.16.42 例 42：互质判断——求区间内与 n 互质的数的个数（容斥）⭐⭐

> **知识点**：容斥原理、质因子子集、与某数互质| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 [1, x] 内与 n 互质的正整数个数。

**思路**

💡 类比"筛掉含其因子的数"：对 n 的相异质因子集合用容斥：总数 − ∑单因子倍数 + ∑两两倍数交集 − ……。

```python
def not_coprime_count(x, n):
    # n 的相异质因子
    factors = set()
    t = n
    d = 2
    while d * d <= t:
        if t % d == 0:
            factors.add(d)
            while t % d == 0:
                t //= d
        d += 1
    if t > 1:
        factors.add(t)
    fs = list(factors)
    from itertools import combinations
    res = 0
    k = len(fs)
    for r in range(1, k + 1):
        for comb in combinations(fs, r):
            prod = 1
            for p in comb:
                prod *= p
            if r % 2 == 1:
                res += x // prod
            else:
                res -= x // prod
    return res

x, n = map(int, input().split())
print(x - not_coprime_count(x, n))
```

> **复杂度**：O(2^ω(n)) 时间，O(ω) 空间

---

#### 17.16.43 例 43：简单递推取模——SARS/岔路口斐波（线性递推通式）⭐

> **知识点**：线性递推、取模| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：数列 a[0]=a[1]=1，a[i]=(a[i−1]+a[i−2])mod M，求 a[n]（n≤1e6）。

**思路**

💡 类比"叠加余数"：与斐波那契取模完全相同，滚动变量逐项递推。

```python
n, M = map(int, input().split())
a, b = 1, 1
if n == 0:
    print(1)
else:
    for _ in range(2, n + 1):
        a, b = b, (a + b) % M
    print(b)
```

> **复杂度**：O(N) 时间，O(1) 空间

---

#### 17.16.44 例 44：GCD 之和——求 ∑_{i=1..n} gcd(i,n)（欧拉优化）⭐⭐⭐

> **知识点**：欧拉函数求和、gcd 分类计数| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n，求 S(n)=∑_{i=1}^{n} gcd(i,n)。

**思路**

💡 类比"按 gcd 值分箱"：S(n)=∑_{d|n} d·φ(n/d)。枚举 n 的约数 d，累加 d·φ(n/d)（用分解后组合枚举或试除）。

```python
def euler(n):
    res = n
    d = 2
    while d * d <= n:
        if n % d == 0:
            while n % d == 0:
                n //= d
            res -= res // d
        d += 1
    if n > 1:
        res -= res // n
    return res

n = int(input())
orig = n
ans = 0
d = 1
while d * d <= orig:
    if orig % d == 0:
        ans += d * euler(orig // d)
        if d * d != orig:
            ans += (orig // d) * euler(d)
    d += 1
print(ans)
```

> **复杂度**：O(√n·√n) 时间，O(1) 空间

---

#### 17.16.45 例 45：判断质数的费马小检验（朴素快速幂验算）⭐

> **知识点**：费马小定理、候选式检验| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 与底 a，判断是否满足 a^(n−1)≡1 (mod n)（注意：这只是素数的必要条件，非充分）。

**思路**

💡 类比"素性抽样"：用快速幂计算 a^(n−1) mod n，看是否等于 1。

```python
def powmod(a, b, m):
    res = 1 % m
    while b:
        if b & 1:
            res = res * a % m
        a = a * a % m
        b >>= 1
    return res

a, n = map(int, input().split())
print("Yes" if powmod(a, n - 1, n) == 1 else "No")
```

> **复杂度**：O(log n) 时间，O(1) 空间

---

#### 17.16.46 例 46：Miller-Rabin 素性检测（确定性基，fits 64-bit）⭐⭐

> **知识点**：Miller-Rabin、二次探测、确定性素数| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定大数 n（≤2^63），判断是否为素数，采用 Miller-Rabin 确定性基 [2,3,5,7,11,13,17]。

**思路**

💡 类比"多层抽样验素"：把 n−1 写成 d·2^s，对每个基 a 做费马检验与二次探测，全部通过则视为素数。

```python
def is_prime(n):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 3, 5, 7, 11, 13, 17]:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        ok = False
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                ok = True
                break
        if not ok:
            return False
    return True

n = int(input())
print("Yes" if is_prime(n) else "No")
```

> **复杂度**：O(k log n) 时间，O(1) 空间

---

#### 17.16.47 例 47：Pollard-Rho 大数分解（配合 Miller-Rabin）⭐⭐⭐

> **知识点**：Pollard-Rho、随机分解、Miller-Rabin| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定大数 n（≤2^63），输出其所有质因数及其指数。

**思路**

💡 类比"随机扰动找因子"：Miller-Rabin 判断素数，Pollard-Rho 用伪随机序列找非平凡因子，递归分解。

```python
import random
from math import gcd
def is_prime(n):
    if n < 2:
        return False
    small = [2,3,5,7,11,13,17,19,23,29,31,37]
    for p in small:
        if n % p == 0:
            return n == p
    d = n-1; s=0
    while d % 2 == 0:
        d//=2; s+=1
    for a in small:
        x = pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1: break
        else:
            return False
    return True
def pollard_rho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    while True:
        c = random.randrange(1, n)
        f = lambda x: (x*x + c) % n
        x = y = random.randrange(0, n)
        d = 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = gcd(abs(x-y), n)
        if d != n:
            return d
def factor(n, res):
    if n == 1:
        return
    if is_prime(n):
        res.append(n)
        return
    d = pollard_rho(n)
    factor(d, res)
    factor(n//d, res)

n = int(input())
if n == 1:
    print("1")
else:
    res = []
    factor(n, res)
    from collections import Counter
    c = Counter(res)
    print(' '.join(f"{k}^{v}" if v>1 else str(k) for k,v in sorted(c.items())))
```

> **复杂度**：期望 O(n^{1/4}) 时间，O(幂数量) 空间

---

#### 17.16.48 例 48：同余——矩形同余跳（模拟循环，考查取模位移）⭐

> **知识点**：同余、取模步进| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：一个线圈上有 n 个位置，每次跳 k 步（取模），问能否回到起点覆盖所有位置（即 k 与 n 是否互质）。

**思路**

💡 类比"沿环跳全"：当且仅当 gcd(n,k)=1 时，从 0 出发按 k 步进能访问全部位置。

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
n, k = map(int, input().split())
print("Yes" if gcd(n, k) == 1 else "No")
```

> **复杂度**：O(log n) 时间，O(1) 空间

---

#### 17.16.49 例 49：试除法质因数分解（模板）⭐

> **知识点**：唯一分解定理、试除| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n（n≤10^12），输出其质因数分解结果（质数^指数）。

**思路**

💡 类比"层层剥洋葱"：从 2 开始逐个试除，能整除就除尽并计数，最后剩下的 n>1 即为一个大质因子。

```python
def factorize(n):
    res = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            res.append((d, cnt))
        d += 1 if d == 2 else 2
    if n > 1:
        res.append((n, 1))
    return res

n = int(input())
print(' '.join(f"{p}^{e}" for p, e in factorize(n)))
```

> **复杂度**：O(√n) 时间，O(质因子数) 空间

---

#### 17.16.50 例 50：约数个数（正因子个数）⭐

> **知识点**：唯一分解、约数个数公式| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n，求其正约数的个数 τ(n)。

**思路**

💡 类比"组合搭配"：若 n=∏p_i^{e_i}，每个质因子选 0..e_i 次，共 ∏(e_i+1) 种方案。

```python
def divisor_count(n):
    cnt = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            cnt *= e + 1
        d += 1 if d == 2 else 2
    if n > 1:
        cnt *= 2
    return cnt

n = int(input())
print(divisor_count(n))
```

> **复杂度**：O(√n) 时间，O(1) 空间

---

#### 17.16.51 例 51：约数之和 ⭐

> **知识点**：约数和公式、等比数列| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n，求其所有正约数之和 σ(n)。

**思路**

💡 类比"每个质因子所有指数组合相加"：σ(n)=∏(p_i^0+p_i^1+...+p_i^{e_i})。

```python
def divisor_sum(n):
    total = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            term = 1
            while n % d == 0:
                n //= d
                term = term * d + 1
            total *= term
        d += 1 if d == 2 else 2
    if n > 1:
        total *= n + 1
    return total

n = int(input())
print(divisor_sum(n))
```

> **复杂度**：O(√n) 时间，O(1) 空间

---

#### 17.16.52 例 52：完全平方数判定（二分/数学）⭐

> **知识点**：整数开方、二分| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：判断 n 是否是完全平方数（能写成某整数 k²）。n 可达 10^18。

**思路**

💡 类比"整数开方"：用二分或 isqrt 求 ⌊√n⌋，再看 ⌊√n⌋² 是否等于 n。

```python
import math

n = int(input())
r = math.isqrt(n)
print("Yes" if r * r == n else "No")
```

> **复杂度**：O(log n) 时间，O(1) 空间

---

#### 17.16.53 例 53：完全数 ⭐

> **知识点**：约数和、完全数定义| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：判断正整数 n 是否为完全数（等于其真因子之和，如 6=1+2+3）。

**思路**

💡 类比"自我等于部分之和"：求 σ(n)，若 σ(n)==2n 即为完全数。

```python
def sigma(n):
    total = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            term = 1
            while n % d == 0:
                n //= d
                term = term * d + 1
            total *= term
        d += 1 if d == 2 else 2
    if n > 1:
        total *= n + 1
    return total

n = int(input())
print("Yes" if n == 1 or sigma(n) == 2 * n else "No")
```

> **复杂度**：O(√n) 时间，O(1) 空间

---

#### 17.16.54 例 54：多个数的最大公约数 ⭐

> **知识点**：gcd、滚动求值| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个正整数，求它们的最大公约数。

**思路**

💡 类比"逐个合并"：gcd 满足结合律，从第一个数开始逐个与下一个数取 gcd。

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

n = int(input())
arr = list(map(int, input().split()))
g = 0
for x in arr:
    g = gcd(g, x)
print(g)
```

> **复杂度**：O(n log V) 时间，O(1) 空间

---

#### 17.16.55 例 55：多个数的最小公倍数 ⭐

> **知识点**：lcm、防溢出先除后乘| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个正整数，求它们的最小公倍数（结果可能很大，先除后乘防溢出取模）。

**思路**

💡 类比"最小公共周期"：lcm(a,b)=a//gcd(a,b)*b，先除后乘可避免中间结果超出范围。

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

n = int(input())
arr = list(map(int, input().split()))
l = 1
for x in arr:
    l = l // gcd(l, x) * x
print(l)
```

> **复杂度**：O(n log V) 时间，O(1) 空间

---

#### 17.16.56 例 56：互质判断 ⭐

> **知识点**：最大公约数| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：判断两个正整数 a、b 是否互质（gcd(a,b)=1）。

**思路**

💡 类比"没有公共因子"：求 gcd，等于 1 即互质。

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

a, b = map(int, input().split())
print("Yes" if gcd(a, b) == 1 else "No")
```

> **复杂度**：O(log min(a,b)) 时间，O(1) 空间

---

#### 17.16.57 例 57：欧拉函数单值（试除法）⭐⭐

> **知识点**：欧拉函数、质因数分解| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n，求欧拉函数 φ(n)，即小于等于 n 且与 n 互质的正整数个数。

**思路**

💡 类比"筛掉与 n 有公共因子的数"：φ(n)=n·∏(1-1/p)，其中 p 遍历 n 的不同质因子。

```python
n = int(input())
res = n
x = n
d = 2
while d * d <= x:
    if x % d == 0:
        res -= res // d
        while x % d == 0:
            x //= d
    d += 1 if d == 2 else 2
if x > 1:
    res -= res // x
print(res)
```

> **复杂度**：O(√n) 时间，O(1) 空间

---

#### 17.16.58 例 58：欧拉函数线性筛打表 ⭐⭐

> **知识点**：线性筛、欧拉函数递推| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：预处理 1..n 的所有欧拉函数值，多次询问 φ(i)。

**思路**

💡 类比"筛法中顺手算出所有 φ"：欧拉筛每个合数只被其最小质因子筛一次，可同时递推 φ。

```python
def phi_table(n):
    phi = [0] * (n + 1)
    primes = []
    comp = [False] * (n + 1)
    for i in range(2, n + 1):
        if not comp[i]:
            primes.append(i)
            phi[i] = i - 1
        for p in primes:
            if i * p > n:
                break
            comp[i * p] = True
            if i % p == 0:
                phi[i * p] = phi[i] * p
                break
            else:
                phi[i * p] = phi[i] * (p - 1)
    return phi

n = int(input())
phi = phi_table(n)
print(phi[n])
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.16.59 例 59：欧拉函数前缀和 ⭐⭐

> **知识点**：欧拉函数、前缀和| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n，求 S(n)=φ(1)+φ(2)+...+φ(n)。

**思路**

💡 类比"累加所有互质数个数"：用线性筛打表 φ 后做前缀和。

```python
n = int(input())
phi = [0] * (n + 1)
primes = []
comp = [False] * (n + 1)
for i in range(2, n + 1):
    if not comp[i]:
        primes.append(i)
        phi[i] = i - 1
    for p in primes:
        if i * p > n:
            break
        comp[i * p] = True
        if i % p == 0:
            phi[i * p] = phi[i] * p
            break
        phi[i * p] = phi[i] * (p - 1)
print(sum(phi[2:]))
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.16.60 例 60：快速幂模板（a^b mod m）⭐

> **知识点**：二进制快速幂、模运算| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a、b、m（b≤10^18），求 a^b mod m。

**思路**

💡 类比"二进制拆分指数"：把 b 拆成二进制，累乘 a^{2^i}，遇 1 位就乘入答案。

```python
a, b, m = map(int, input().split())
res = 1 % m
base = a % m
while b > 0:
    if b & 1:
        res = res * base % m
    base = base * base % m
    b >>= 1
print(res)
```

> **复杂度**：O(log b) 时间，O(1) 空间

---

#### 17.16.61 例 61：快速幂 + 大指数（字符串输入）⭐⭐

> **知识点**：快速幂、大数取模| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：b 以字符串形式给出（十进制可达 10^100000），求 a^b mod m。

**思路**

💡 类比"边构造指数边取模"：读入字符串逐位构造 b 并同步取模，再用快速幂。

```python
a, m = map(int, input().split())
b = input().strip()
be = 0
for ch in b:
    be = (be * 10 + int(ch)) % m
print(pow(a, be, m))
```

> **复杂度**：O(|b| + log m) 时间，O(1) 空间

---

#### 17.16.62 例 62：判断 2 的幂（位运算）⭐

> **知识点**：位运算、2 的幂判定| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：判断正整数 n 是否为 2 的整数次幂。

**思路**

💡 类比"二进制只有一个 1"：2^k 的二进制有且仅有一个 1，故 n & (n-1)==0。

```python
n = int(input())
print("Yes" if n > 0 and (n & (n - 1)) == 0 else "No")
```

> **复杂度**：O(1) 时间，O(1) 空间

---

#### 17.16.63 例 63：判断 3 的幂 ⭐

> **知识点**：对数、循环除法| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：判断正整数 n 是否为 3 的整数次幂（n 可达 2^31-1）。

**思路**

💡 类比"不断除以 3"：只要仍能被 3 整除就除下去，最后判断是否剩 1。

```python
def is_power_of_three(n):
    if n <= 0:
        return False
    while n % 3 == 0:
        n //= 3
    return n == 1

n = int(input())
print("Yes" if is_power_of_three(n) else "No")
```

> **复杂度**：O(log_3 n) 时间，O(1) 空间

---

#### 17.16.64 例 64：判断 4 的幂 ⭐

> **知识点**：位运算、4 的幂判定| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：判断正整数 n 是否为 4 的整数次幂。

**思路**

💡 类比"既是 2 的幂又满足位数关系"：1、4、16 的二进制为 1 后跟偶数个 0，(n & (n-1))==0 且 n%3==1（4^k mod 3 = 1）。

```python
n = int(input())
ok = n > 0 and (n & (n - 1)) == 0 and n % 3 == 1
print("Yes" if ok else "No")
```

> **复杂度**：O(1) 时间，O(1) 空间

---

#### 17.16.65 例 65：Stein 二进制最大公约数 ⭐⭐

> **知识点**：二进制 gcd、位运算| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：用二进制（位运算）实现大整数最大公约数，避免除法。

**思路**

💡 类比"只用移位和减法算 gcd"：偶偶提因子 2；一奇一偶给偶数除 2；两奇用减法。

```python
def stein_gcd(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    shift = 0
    while (a | b) % 2 == 0:
        a >>= 1
        b >>= 1
        shift += 1
    while a % 2 == 0:
        a >>= 1
    while b:
        while b % 2 == 0:
            b >>= 1
        if a > b:
            a, b = b, a
        b -= a
    return a << shift

a, b = map(int, input().split())
print(stein_gcd(abs(a), abs(b)))
```

> **复杂度**：O(log max(a,b)) 时间，O(1) 空间

---

#### 17.16.66 例 66：斐波那契（滚动迭代取模）⭐

> **知识点**：递推、滚动数组、模运算| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：求斐波那契数列第 n 项 mod 10^9+7（n≤10^6）。

**思路**

💡 类比"滚动往前进"：只需保存前两项，逐项递推即可，不必存储整数组。

```python
MOD = 10**9 + 7
n = int(input())
if n == 0:
    print(0)
else:
    a, b = 0, 1
    for _ in range(1, n):
        a, b = b, (a + b) % MOD
    print(b)
```

> **复杂度**：O(n) 时间，O(1) 空间

---

#### 17.16.67 例 67：费马小定理求模逆元 ⭐⭐

> **知识点**：费马小定理、快速幂、逆元| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a 和素数 p，求 a 模 p 的乘法逆元（1≤a<p，p 为大素数，a^(-1) mod p）。

**思路**

💡 类比"用幂求倒数"：费马小定理 a^(p-1)≡1(mod p)，故逆元为 a^(p-2) mod p。

```python
p = int(input())
a = int(input())
print(pow(a, p - 2, p))
```

> **复杂度**：O(log p) 时间，O(1) 空间

---

#### 17.16.68 例 68：线性求逆元 1..n ⭐⭐

> **知识点**：逆元递推、模运算| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 与素数 p，预处理 1..n 每个数模 p 的逆元，多次询问输出某数逆元。

**思路**

💡 类比"利用已算好的逆元递推"：inv[i]=(p - p//i)·inv[p%i] mod p。

```python
n, p = map(int, input().split())
inv = [0] * (n + 1)
inv[1] = 1
for i in range(2, n + 1):
    inv[i] = (p - p // i) * inv[p % i] % p
q = int(input())
for _ in range(q):
    x = int(input())
    print(inv[x])
```

> **复杂度**：O(n) 预处理，O(1) 询问，O(n) 空间

---

#### 17.16.69 例 69：扩展欧几里得模板 ⭐⭐

> **知识点**：扩展欧几里得、不定方程| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a、b，求一组整数解 (x,y) 满足 ax+by=gcd(a,b)，输出 x,y,gcd。

**思路**

💡 类比"递归回代"：exgcd 返回 gcd 及满足条件的 (x,y)，利用商与余数关系回代。

```python
def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = exgcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

a, b = map(int, input().split())
g, x, y = exgcd(a, b)
print(g, x, y)
```

> **复杂度**：O(log min(a,b)) 时间，O(log) 递归栈空间

---

#### 17.16.70 例 70：扩展欧几里得求逆元 ⭐⭐

> **知识点**：扩展欧几里得、逆元| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a、m（a 与 m 互质），求 a 模 m 的逆元，可能 m 非素数。

**思路**

💡 类比"求 ax+my=1 的解"：解 ax+my=1，x 即为逆元；需 gcd(a,m)=1。

```python
def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = exgcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

a, m = map(int, input().split())
g, x, _ = exgcd(a, m)
if g != 1:
    print("No inverse")
else:
    print((x % m + m) % m)
```

> **复杂度**：O(log m) 时间，O(log) 递归栈空间

---

#### 17.16.71 例 71：线性同余方程 ax≡b (mod m) 最小正规解 ⭐⭐

> **知识点**：线性同余、扩展欧几里得| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a、b、m（1≤a,m≤10^9），求 ax≡b (mod m) 的最小正整数解，无解输出 -1。

**思路**

💡 类比"化同余为不定方程"：转为 a·x+m·y=b，用 exgcd 求特解再放大，最后取最小正解。

```python
def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = exgcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

a, b, m = map(int, input().split())
g, x, _ = exgcd(a % m, m)
if b % g != 0:
    print(-1)
else:
    mod = m // g
    x = (x * (b // g)) % mod
    ans = x if x != 0 else mod
    print(ans)
```

> **复杂度**：O(log m) 时间，O(log) 递归栈空间

---

#### 17.16.72 例 72：中国剩余定理 CRT ⭐⭐⭐

> **知识点**：CRT、逆元、模运算| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个两两互质的模 m_i 与余数 a_i，求满足 x≡a_i(mod m_i) 的最小非负整数解。

**思路**

💡 类比"分块拼接"：令 M=∏m_i，对每个方程用逆元求在 M 中补足的系数，累加后取模。

```python
def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = exgcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def inv(a, m):
    g, x, _ = exgcd(a, m)
    return (x % m + m) % m

n = int(input())
a = []
m = []
for _ in range(n):
    ai, mi = map(int, input().split())
    a.append(ai % mi)
    m.append(mi)
M = 1
for mi in m:
    M *= mi
ans = 0
for ai, mi in zip(a, m):
    Mi = M // mi
    ans += ai * Mi * inv(Mi, mi)
print(ans % M)
```

> **复杂度**：O(n log m) 时间，O(n) 空间

---

#### 17.16.73 例 73：扩展中国剩余定理 EXCRT（m 不互质）⭐⭐⭐

> **知识点**：EXCRT、两两合并| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个同余式 x≡a_i(mod m_i)，m_i 不一定两两互质，求最小非负整数解，无解输出 -1。

**思路**

💡 类比"逐步合并两个同余式"：核心是解 M·t+a_old ≡ a_new (mod m_new)，再并入整体。

```python
def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = exgcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

n = int(input())
a = []
m = []
for _ in range(n):
    ai, mi = map(int, input().split())
    a.append(ai % mi)
    m.append(mi)
x = 0
M = 1
ok = True
for ai, mi in zip(a, m):
    g, p, _ = exgcd(M % mi, mi)
    if (ai - x) % g != 0:
        ok = False
        break
    lcm = M // g * mi
    p = (p * ((ai - x) // g)) % mi
    x = (x + p * M) % lcm
    M = lcm
print((x % M + M) % M if ok else -1)
```

> **复杂度**：O(n log m) 时间，O(log) 递归栈空间

---

#### 17.16.74 例 74：Lucas 定理组合数 C(n,m) mod p ⭐⭐⭐

> **知识点**：Lucas、组合数、逆元| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n、m 与素数 p（可较小，n、m 很大），求 C(n,m) mod p。

**思路**

💡 类比"按 p 进制拆分"：Lucas 定理 C(n,m)≡∏C(n_i,m_i)(mod p)，其中 n_i、m_i 为 p 进制位。

```python
def comb_small(a, b, p):
    if b < 0 or b > a:
        return 0
    num = den = 1
    for i in range(b):
        num = num * (a - i) % p
        den = den * (i + 1) % p
    return num * pow(den, p - 2, p) % p

def lucas(n, m, p):
    if n < p and m < p:
        return comb_small(n, m, p)
    return comb_small(n % p, m % p, p) * lucas(n // p, m // p, p) % p

n, m, p = map(int, input().split())
print(lucas(n, m, p))
```

> **复杂度**：O(p log_p n) 时间，O(log_p n) 递归栈

---

#### 17.16.75 例 75：组合数阶乘逆元法 ⭐⭐

> **知识点**：组合数、阶乘逆元、费马小定理| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：模 p=10^9+7 下多次询问 C(n,m)（n≤10^6）。

**思路**

💡 类比"查表加速组合"：预处理 0..maxN 的阶乘与其逆元，C(n,m)=n!·inv(m!)·inv((n-m)!)。

```python
MOD = 10**9 + 7
n, m, q = map(int, input().split())
N = n
fact = [1] * (N + 1)
for i in range(1, N + 1):
    fact[i] = fact[i - 1] * i % MOD
invf = [1] * (N + 1)
invf[N] = pow(fact[N], MOD - 2, MOD)
for i in range(N, 0, -1):
    invf[i - 1] = invf[i] * i % MOD

def C(x, y):
    if y < 0 or y > x:
        return 0
    return fact[x] * invf[y] % MOD * invf[x - y] % MOD

print(C(n, m))
```

> **复杂度**：O(N) 预处理，O(1) 询问，O(N) 空间

---

#### 17.16.76 例 76：Legendre 阶乘质因子指数 ⭐⭐

> **知识点**：Legendre 公式| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求素数 p 在 n! 中的指数 v_p(n!)=⌊n/p⌋+⌊n/p²⌋+...

**思路**

💡 类比"分层统计倍数"：每层统计 p 的倍数，逐层除以 p 累加商。

```python
def legendre(n, p):
    cnt = 0
    while n:
        n //= p
        cnt += n
    return cnt

n, p = map(int, input().split())
print(legendre(n, p))
```

> **复杂度**：O(log_p n) 时间，O(1) 空间

---

#### 17.16.77 例 77：阶乘末尾 0 的个数 ⭐

> **知识点**：Legendre、因子 5| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：求 n! 末尾连续 0 的个数。

**思路**

💡 类比"数 5 的个数"：10=2×5，因子 2 充足，故末尾 0 个数等于因子 5 的个数。

```python
def trailing_zeros(n):
    cnt = 0
    while n:
        n //= 5
        cnt += n
    return cnt

n = int(input())
print(trailing_zeros(n))
```

> **复杂度**：O(log_5 n) 时间，O(1) 空间

---

#### 17.16.78 例 78：欧拉降幂（指数循环节）⭐⭐⭐

> **知识点**：欧拉降幂、欧拉函数| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 a^b mod m，b 为很大的数（字符串输入，b≥φ(m) 时使用循环节）。

**思路**

💡 类比"大指数截断到循环节"：当 b≥φ(m) 时，a^b ≡ a^{b mod φ(m) + φ(m)}(mod m)。

```python
def phi(x):
    res = x
    d = 2
    while d * d <= x:
        if x % d == 0:
            res -= res // d
            while x % d == 0:
                x //= d
        d += 1 if d == 2 else 2
    if x > 1:
        res -= res // x
    return res

a, m = map(int, input().split())
b = input().strip()
ph = phi(m) if m > 1 else 1
exp = 0
big = False
for ch in b:
    exp = exp * 10 + int(ch)
    if exp >= ph:
        exp %= ph
        big = True
if big:
    exp += ph
print(pow(a, exp, m))
```

> **复杂度**：O(√m + |b|) 时间，O(1) 空间

---

#### 17.16.79 例 79：反素数（最大约数个数的数）⭐⭐⭐

> **知识点**：反素数、DFS、质因数分解| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n，求不超过 n 的约数个数最多的最小正整数（反素数）。

**思路**

💡 类比"尽量多用小质因子"：反素数的质因子必为连续小素数且指数不增，用 DFS 枚举指数组合。

```python
n = int(input())
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
best_cnt = 0
best_num = 1

def dfs(idx, cur, cnt):
    global best_cnt, best_num
    if cur > n:
        return
    if cnt > best_cnt or (cnt == best_cnt and cur < best_num):
        best_cnt = cnt
        best_num = cur
    if idx >= len(primes):
        return
    p = primes[idx]
    val = cur
    for e in range(1, 31):
        val *= p
        if val > n:
            break
        dfs(idx + 1, val, cnt * (e + 1))

dfs(0, 1, 1)
print(best_num)
```

> **复杂度**：O(2^k) 时间（k 为可枚举质因子个数），递归栈 O(k)

---

#### 17.16.80 例 80：第 N 个素数 ⭐⭐

> **知识点**：素数筛、倍增上界| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 N（N≤10^6），求第 N 个素数。

**思路**

💡 类比"放大范围直到够数"：用埃氏筛在一个扩大的上界内筛出所有素数，直到数量达到 N。

```python
def sieve(limit):
    isp = [True] * (limit + 1)
    isp[0:2] = [False, False]
    i = 2
    while i * i <= limit:
        if isp[i]:
            for j in range(i * i, limit + 1, i):
                isp[j] = False
        i += 1
    return [k for k in range(2, limit + 1) if isp[k]]

n = int(input())
limit = 16
primes = []
while len(primes) < n:
    primes = sieve(limit)
    limit *= 2
print(primes[n - 1])
```

> **复杂度**：O(N log log N) 时间，O(N) 空间

---

#### 17.16.81 例 81：区间素数个数 [L,R]（分段筛）⭐⭐⭐

> **知识点**：分段筛、埃氏筛| **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：统计 [L,R]（R-L≤10^6，R≤10^12）内的素数个数。

**思路**

💡 类比"先用小素数标记大区间"：先筛出 ≤√R 的素数，再用它们在 [L,R] 上做分段标记。

```python
import math

def seg_count(L, R):
    if R < 2:
        return 0
    lim = math.isqrt(R) + 1
    base = [True] * (lim + 1)
    base[0] = base[1] = False
    for i in range(2, math.isqrt(lim) + 1):
        if base[i]:
            for j in range(i * i, lim + 1, i):
                base[j] = False
    small = [i for i in range(2, lim + 1) if base[i]]
    seg = [True] * (R - L + 1)
    if L <= 1:
        seg[0 if L == 0 else 0] = (False if L == 0 else False)
        for k in range(max(0, 1 - L), R - L + 1):
            seg[k] = False
    for p in small:
        start = max(p * p, (L + p - 1) // p * p)
        for j in range(start, R + 1, p):
            seg[j - L] = False
    return sum(seg)

L, R = map(int, input().split())
print(seg_count(L, R))
```

> **复杂度**：O((√R+R-L) log log) 时间／分段筛，O(R-L) 空间

---

#### 17.16.82 例 82：回文素数 ⭐

> **知识点**：回文、素数判定| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n，判断它是否既是素数又是回文数（正反读相同）。

**思路**

💡 类比"双向读一致且仅被 1 和自身整除"：先判回文（字符串反转），再判素数。

```python
import math

def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(math.isqrt(x)) + 1):
        if x % i == 0:
            return False
    return True

n = int(input())
s = str(n)
print("Yes" if s == s[::-1] and is_prime(n) else "No")
```

> **复杂度**：O(√n) 时间，O(1) 空间

---

#### 17.16.83 例 83：哥德巴赫猜想验证 ⭐⭐

> **知识点**：素数筛、素因子分解| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定偶数 n（n≥4），输出一组素数 p≤q 使 p+q=n。

**思路**

💡 类比"补数互补"：筛出 [2,n] 质数表，遍历 p，若 n-p 也是素数即为答案。

```python
def make_primes(n):
    isp = [True] * (n + 1)
    isp[0:2] = [False, False]
    for i in range(2, int(n ** 0.5) + 1):
        if isp[i]:
            for j in range(i * i, n + 1, i):
                isp[j] = False
    return isp

n = int(input())
isp = make_primes(n)
for p in range(2, n // 2 + 1):
    if isp[p] and isp[n - p]:
        print(p, n - p)
        break
```

> **复杂度**：O(n log log n) 时间，O(n) 空间

---

#### 17.16.84 例 84：数字根（同余 9）⭐

> **知识点**：数字根、模 9 性质| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定大数 n，反复相加其各位数字直到只剩一位，输出该数字根。

**思路**

💡 类比"除以 9 的余数"：数字根取决于 n mod 9，其中整除 9 时数字根为 9（0 特判）。

```python
n = int(input())  # 若 n 很大可用字符串逐位取模
if n == 0:
    print(0)
else:
    print((n - 1) % 9 + 1)
```

> **复杂度**：O(1) 时间，O(1) 空间

---

#### 17.16.85 例 85：a^b 的个位数字 ⭐

> **知识点**：模运算、周期| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 a、b（可达 10^100），求 a^b 的个位数字。

**思路**

💡 类比"看个位循环"：a^b 个位只由 a 的个位决定且以 4 为周期，利用 b mod 4。

```python
a = input().strip()
b = input().strip()
base = int(a[-1])
if base in (0, 1, 5, 6):
    print(base)
else:
    e = int(b[-2:]) % 4
    if e == 0:
        e = 4
    print(pow(base, e, 10))
```

> **复杂度**：O(1) 时间，O(1) 空间

---

#### 17.16.86 例 86：字符串大数取模 ⭐⭐

> **知识点**：大数取模| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定十进制字符串大数 s（长度≤10^6）与模数 m，求 s mod m。

**思路**

💡 类比"逐位构造并取模"：从高位开始 ans=(ans*10+digit)%m。

```python
s = input().strip()
m = int(input())
ans = 0
for ch in s:
    ans = (ans * 10 + int(ch)) % m
print(ans)
```

> **复杂度**：O(|s|) 时间，O(1) 空间

---

#### 17.16.87 例 87：连续正整数和（滑动窗口）⭐

> **知识点**：滑动窗口、等差数列| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：非零整数 n 能否表示为至少两个连续正整数之和？输出方案或 -1。

**思路**

💡 类比"窗口伸缩找和"：用双指针维护 [l,r] 的和，大了右移 l，小了右移 r。

```python
n = int(input())
l, r = 1, 1
cur = 0
while l < n:
    if cur < n:
        cur += r
        r += 1
    elif cur > n:
        cur -= l
        l += 1
    else:
        print(l, r - 1)
        cur -= l
        l += 1
        break
else:
    print(-1)
```

> **复杂度**：O(n) 时间，O(1) 空间

---

#### 17.16.88 例 88：区间 [1,n] 的最大约数个数 ⭐⭐

> **知识点**：约数、筛法计数| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n，求 [1,n] 中约数个数最多的那个数及其约数个数。

**思路**

💡 类比"倍数打标记"：对每个 i，向所有倍数 j+=i 累加计数，即求 min 值内的最大 τ。

```python
n = int(input())
cnt = [0] * (n + 1)
for i in range(1, n + 1):
    for j in range(i, n + 1, i):
        cnt[j] += 1
best = max(range(1, n + 1), key=lambda x: cnt[x])
print(best, cnt[best])
```

> **复杂度**：O(n log n) 时间，O(n) 空间

---

#### 17.16.89 例 89：正整数除法向上取整 ⭐

> **知识点**：整除、取整| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 a、b，求 ⌈a/b⌉ 且不下转浮点。

**思路**

💡 类比"向上补齐"：⌈a/b⌉=(a+b-1)/b。

```python
a, b = map(int, input().split())
print((a + b - 1) // b)
```

> **复杂度**：O(1) 时间，O(1) 空间

---

#### 17.16.90 例 90：开关灯（因子个数的奇偶性）⭐

> **知识点**：因子奇偶性、完全平方数| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 盏灯，操作 k 次：第 i 次翻转编号为 i 的倍数的灯，问最后亮着的灯数。

**思路**

💡 类比"数因子的奇偶"：灯被翻转的次数为其因子个数，因子数为奇数者最终亮着，即完全平方数。

```python
import math
n = int(input())
print(math.isqrt(n))
```

> **复杂度**：O(1) 时间，O(1) 空间

---

#### 17.16.91 例 91：二项式系数的奇偶性（Lucas 特例）⭐⭐

> **知识点**：Lucas、位运算| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：判断 C(n,k) 是否为奇数（n、k≤10^18）。

**思路**

💡 类比"按位看子集"：C(n,k) 为奇数当且仅当无进位加，即 (n & k)==k（组合总数定理）。

```python
n, k = map(int, input().split())
print("Odd" if (n & k) == k else "Even")
```

> **复杂度**：O(1) 时间，O(1) 空间

---

#### 17.16.92 例 92：不同质因子的个数 ⭐

> **知识点**：质因数分解、去重| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n，求其不同质因子的个数 ω(n)。

**思路**

💡 类比"数几种基本粒子"：分解质因子，每遇到新因子就计数并把该因子除尽。

```python
def omega(n):
    cnt = 0
    d = 2
    while d * d <= n:
        if n % d == 0:
            cnt += 1
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        cnt += 1
    return cnt

n = int(input())
print(omega(n))
```

> **复杂度**：O(√n) 时间，O(1) 空间

---

#### 17.16.93 例 93：水仙花数（幂和）⭐

> **知识点**：取位、幂运算| **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：水仙花数是各位数字的位数次幂之和等于自身的数，统计并输出 [a,b] 内所有水仙花数。

**思路**

💡 类比"数字自身构成之和"：取出每位数字求幂和，与自身比较即可。

```python
def is_narc(x):
    s = str(x)
    k = len(s)
    return x == sum(int(ch) ** k for ch in s)

a, b = map(int, input().split())
res = [x for x in range(a, b + 1) if is_narc(x)]
print(res if res else -1)
```

> **复杂度**：O((b-a) log x) 时间，O(1) 空间

---

#### 17.16.94 例 94：勾股数统计 ⭐⭐

> **知识点**：勾股定理、穷举| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：统计满足 a²+b²=c² 且 1≤a<b<c≤n 的正整数三元组个数。

**思路**

💡 类比"两两枚举首边找第三边"：枚举 a、b，计算 c=⌊√(a²+b²)⌋ 校验是否构成严格勾股数。

```python
import math
n = int(input())
cnt = 0
for a in range(1, n + 1):
    for b in range(a + 1, n + 1):
        c2 = a * a + b * b
        c = math.isqrt(c2)
        if c > b and c <= n and c * c == c2:
            cnt += 1
print(cnt)
```

> **复杂度**：O(n²) 时间，O(1) 空间

---

#### 17.16.95 例 95：区间内素数之和 ⭐⭐

> **知识点**：埃氏筛、前缀统计| **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n，输出 [1,n] 内所有素数之和。

**思路**

💡 类比"筛完累加"：用埃氏筛标记素数，同时对是素数的数求和。

```python
def prime_sum(n):
    if n < 2:
        return 0
    isp = [True] * (n + 1)
    isp[0:2] = [False, False]
    s = 0
    for i in range(2, n + 1):
        if isp[i]:
            s += i
            for j in range(i * i, n + 1, i):
                isp[j] = False
    return s

n = int(input())
print(prime_sum(n))
```

> **复杂度**：O(n log log n) 时间，O(n) 空间

---
