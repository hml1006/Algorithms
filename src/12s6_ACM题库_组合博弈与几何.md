# 第 12 章 OI/ACM 竞赛：ACM 经典题库（六）

> 本分册覆盖 17.17–17.19（组合数学、博弈与几何），共 170 题。
> 返回 [ACM 经典题库总览](./12s_ACM题库.md)。

## 17. ACM 经典题库

### 17.17 组合数学与概率期望

#### 17.17.1 例 1：排列计数（HDU 2013）⭐
> **知识点**：阶乘、乘法原理｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入正整数 n（1≤n≤20），求 n 个互不相同元素的排列数 n!。多组输入，每组输出结果。

**思路**
排列数即全排列 n!，用循环累乘即可，注意用 Python 大整数不会溢出。

💡 类比"n 个人排成一队：第 1 个位置有 n 种选法，第 2 个位置剩 n-1 种……相乘就是总数"：

```python
import sys

for line in sys.stdin:
    n = int(line.strip())
    s = 1
    for x in range(2, n + 1):
        s *= x
    print(s)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.17.2 例 2：杨辉三角与二项式系数（洛谷 P3414）⭐
> **知识点**：杨辉三角、递推、组合恒等式｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（1≤n≤10^6），求 2^(n-1) 对 10^9+7 取模的值。其中利用组合恒等式 ΣC(n,k)=2^n，而奇数项之和即 2^(n-1)。

**思路**
由二项式定理知二项式展开各项系数和为 2^n，其中奇数项与偶数项各占一半，故答案为 2^(n-1)。

💡 类比"硬币翻面分组：把所有翻面情况两两配成镜像，正反面种数正好对半分"：

```python
MOD = 10**9 + 7

def qpow(a, b):
    r = 1
    while b:
        if b & 1:
            r = r * a % MOD
        a = a * a % MOD
        b >>= 1
    return r

for n in (3, 10, 1000000):
    print(qpow(2, n - 1))
```
> **复杂度**：O(log n) 时间，O(1) 空间

---
#### 17.17.3 例 3：组合数 C(n,k)（洛谷 P4057）⭐
> **知识点**：递推、组合数计算｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入两个整数 n, k（0≤k≤n≤30），输出组合数 C(n,k) 的值。多组输入。

**思路**
用递推公式 C(n,k)=C(n-1,k-1)+C(n-1,k)，即杨辉三角，或直接累乘公式计算。

💡 类比"从口袋选糖果：逐个决定每颗糖果拿还是不拿，累加所有方案"：

```python
import sys

def C(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    res = 1
    for i in range(1, k + 1):
        res = res * (n - k + i) // i
    return res

for line in sys.stdin:
    n, k = map(int, line.split())
    print(C(n, k))
```
> **复杂度**：O(k) 时间，O(1) 空间

---
#### 17.17.4 例 4：等腰内角三角形计数（HDU 2043）⭐
> **知识点**：暴力枚举、整数性质｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定周长 p（1≤p≤5000），求边长均为正整数且构成三角形的不同三边组合个数（无序）。输出方案数。

**思路**
固定最短边 a，枚举 a 与 b，用 c=p-a-b，检查 a+b>c 且排序去重。

💡 类比"用同长度的火柴棍围三角形：从最短那根开始试，三边满足两边和大于第三边即可"：

```python
import sys

for line in sys.stdin:
    p = int(line.strip())
    cnt = 0
    for a in range(1, p // 3 + 1):
        for b in range(a, (p - a) // 2 + 1):
            c = p - a - b
            if a + b > c:
                cnt += 1
    print(cnt)
```
> **复杂度**：O(p²) 时间，O(1) 空间

---
#### 17.17.5 例 5：卡特兰数（洛谷 P1044）⭐⭐
> **知识点**：卡特兰数、递推｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 个元素按 1~n 进栈，问共有多少种不同的出栈序列（1≤n≤18）。输出方案数。

**思路**
出栈序列数即第 n 个卡特兰数。递推公式 Cat(n)=Σ Cat(i)·Cat(n-1-i)，Cat(0)=1。

💡 类比"火车调车场：头车决定先出，剩下的左右两边互不干扰，各自独立算方案再相乘"：

```python
def catalan(n):
    cat = [0] * (n + 1)
    cat[0] = 1
    for i in range(1, n + 1):
        for j in range(i):
            cat[i] += cat[j] * cat[i - 1 - j]
    return cat

n = 18
print(catalan(n)[n])
```
> **复杂度**：O(n²) 时间，O(n) 空间

---
#### 17.17.6 例 6：错排问题（HDU 2049）⭐⭐
> **知识点**：错排、递推｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n（1≤n≤20），求 n 个人全部不在自己号码位置上的排列数（完全错排 D(n)）。多组输入。

**思路**
错排递推 D(n)=(n-1)·(D(n-1)+D(n-2))，D(1)=0，D(2)=1。

💡 类比"交换生日礼物的秘密圣诞老人：没人拿到自己的礼物，所有人都按'把我的序号给别人'来错位配对"：

```python
import sys

def derange(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    a, b = 0, 1
    for i in range(3, n + 1):
        a, b = b, (i - 1) * (a + b)
    return b

for line in sys.stdin:
    n = int(line.strip())
    print(derange(n))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.17.7 例 7：隔板法与不定方程解个数（HDU 2215）⭐⭐
> **知识点**：隔板法、可重集组合｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求不定方程 x1+x2+…+xn=m（xi≥0）的非负整数解个数，结果很大，输出对 1000000007 取模。其中 n,m≤1000。

**思路**
用隔板法，将 m 个相同球分配到 n 个箱子，允许空箱，方案数为 C(m+n-1, n-1)。预处理组合数取模。

💡 类比"给三只小猫分鱼但允许某只不吃：把 m 条鱼排开插两根隔板自然分成三堆，有几条就相当于往几个位置里挑隔板位置"：

```python
MOD = 10**9 + 7
N = 2005

def pre():
    C = [[0] * N for _ in range(N)]
    for i in range(N):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD
    return C

C = pre()
for m, n in ((3, 3), (0, 2), (1000, 1000)):
    print(C[m + n - 1][n - 1])
```
> **复杂度**：O((m+n)²) 预处理，O(1) 查询，空间 O((m+n)²)

---
#### 17.17.8 例 8：抽屉原理 / 鸽巢原理（HDU 2104）⭐
> **知识点**：鸽巢原理、最大公约数｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 个箱子围成一圈（编号 1~n），从 1 开始每次跳 m 个位置（位置 +(m-1) 再对 n 取模），问能否访问到全部箱子。每组输入 n,m。

**思路**
由鸽巢原理，能访问全部 n 个箱子当且仅当无序跳转间隔与环长互质，即 gcd(n,m)=1。

💡 类比"围一圈跳格子：如果跳的步长和人数有公因数，就会绕着绕着一圈走不完，只会重复踩某些格子"：

```python
import sys, math

for line in sys.stdin:
    n, m = map(int, line.split())
    if n == 0 and m == 0:
        break
    print("YES" if math.gcd(n, m) == 1 else "POOR Haha")
```
> **复杂度**：O(log n) 时间，O(1) 空间

---
#### 17.17.9 例 9：可重集排列计数（洛谷 P2043）⭐⭐
> **知识点**：可重集排列、阶乘分解｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串由若干字母构成，求这些字母全排列中不同排列的个数除以某素数的余数。题目给 n 及各字母个数统计。

**思路**
可重集排列数为 n! / ∏(cnt_i!)。分解质因数，分子分母相减指数即可精确计数。

💡 类比"串字母项链：同样的珠子重复出现，把相同珠子的重复计数剔除，用质因数抵消"：

```python
def rep_perm(counts):
    n = sum(counts)
    primes = {}
    def add(x, sign):
        i = 2
        while i * i <= x:
            while x % i == 0:
                primes[i] = primes.get(i, 0) + sign
                x //= i
            i += 1
        if x > 1:
            primes[x] = primes.get(x, 0) + sign
    for x in range(2, n + 1):
        add(x, 1)
    for c in counts:
        for x in range(2, c + 1):
            add(x, -1)
    res = 1
    for k, v in primes.items():
        res *= k ** v
    return res

print(rep_perm([3, 2]))  # AABBC -> 5!/(3!2!)
```
> **复杂度**：O(n√n) 时间，O(n) 空间

---
#### 17.17.10 例 10：n 的质因数分解（洛谷 P2043 变式）⭐
> **知识点**：质因数分解、素数筛｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入整数 n（1≤n≤10^6），输出 n! 的标准质因数分解形式，超过程度下指数为 0 的跳过。

**思路**
先用埃氏筛筛出素数，再对每个素数统计其在 n! 中出现的次数：v = Σ floor(n/p^i)。

💡 类比"数一堆积木每种颜色有几块：先备好色卡（素数表），再逐类数清每种颜色的块数"：

```python
def factorial_prime_count(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    res = []
    for p in range(2, n + 1):
        if is_prime[p]:
            v = 0
            t = n
            while t:
                t //= p
                v += t
            res.append((p, v))
            for m in range(p * p, n + 1, p):
                is_prime[m] = False
    return res

for p, v in factorial_prime_count(20):
    print(f"{p}^{v}", end="  ")
print()
```
> **复杂度**：O(n log log n) 时间，O(n) 空间

---
#### 17.17.11 例 11：二项式系数 mod 素数（UVA 11754）⭐⭐
> **知识点**：阶乘逆元、费马小定理｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n, k 与素数 mod（mod≤10^9+7，n≤10^6），输出 C(n,k) mod mod。多组输入。

**思路**
预处理 1..N 的阶乘与阶乘逆元，用费马小定理快速幂求逆，答案 C = n! · inv(k!) · inv((n-k)!) % mod。

💡 类比"从满柜书里抽几本：先算全排列，再把选择内部的顺序和没选里的顺序都除掉"：

```python
MOD = 10**9 + 7
N = 10**6 + 5
fact = [1] * (N + 1)
invf = [1] * (N + 1)
for i in range(1, N + 1):
    fact[i] = fact[i - 1] * i % MOD
invf[N] = pow(fact[N], MOD - 2, MOD)
for i in range(N, 0, -1):
    invf[i - 1] = invf[i] * i % MOD

def comb(n, k, mod=MOD):
    if k < 0 or k > n:
        return 0
    return fact[n] * invf[k] % mod * invf[n - k] % mod

print(comb(10, 3))
print(comb(1000000, 500000))
```
> **复杂度**：O(N) 预处理，O(1) 查询，空间 O(N)

---
#### 17.17.12 例 12：容斥原理计数（HDU 1796）⭐⭐
> **知识点**：容斥原理、子集枚举｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定集合 S（元素均为正整数）与上限 n，求 1~n 中能被 S 中至少一个元素整除的数的个数。集合大小 m≤15。

**思路**
枚举 S 的非空子集，用容斥原理：奇数个元素子集加、偶数个元素子集减，子集贡献为 n//lcm(subset)。

💡 类比"数同时喜欢两类比赛的人：先都用加号，再一对一对把重复的减回来，三三加……交错修正"：

```python
import math

def count_multiples(n, s):
    s = [x for x in s if x > 0]
    m = len(s)
    total = 0
    for mask in range(1, 1 << m):
        l = 1
        bits = 0
        for i in range(m):
            if mask >> i & 1:
                l = l * s[i] // math.gcd(l, s[i])
                bits += 1
        cur = n // l
        total += cur if bits % 2 == 1 else -cur
    return total

print(count_multiples(100, [2, 3, 5]))  # 1~100 中能被2/3/5整除的个数
```
> **复杂度**：O(2^m · m) 时间，O(1) 空间

---
#### 17.17.13 例 13：卢卡斯定理（HDU 3037）⭐⭐⭐
> **知识点**：卢卡斯定理、大组合数取模｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求满足 x1+x2+…+xn=m（xi≥0）的解个数对素数 p（p≤10^5）取模，其中 n,m≤10^9。多组输入。

**思路**
隔板法得答案为 C(m+n-1, n-1)，n,m 巨大而 p 较小，用卢卡斯定理 Lucas(n,k)=C(n0,k0)·Lucas(n/p,k/p) 逐位计算。

💡 类比"十进制的进位拆解成米分厘：大数按 p 进制拆成一位位小数，逐位组合再连乘"：

```python
def Cmod(n, k, p, fact, invf):
    if k > n:
        return 0
    return fact[n] * invf[k] % p * invf[n - k] % p

def lucas(n, k, p, fact, invf):
    if k == 0:
        return 1
    return Cmod(n % p, k % p, p, fact, invf) * lucas(n // p, k // p, p, fact, invf) % p

def solve(n, m, p):
    fact = [1] * k
    for i in range(1, p):
        fact[i] = fact[i - 1] * i % p
    invf = [1] * p
    invf[p - 1] = pow(fact[p - 1], p - 2, p)
    for i in range(p - 1, 0, -1):
        invf[i - 1] = invf[i] * i % p
    return lucas(n + m, n, p, fact, invf)

import os
k = 100000
print(solve(4, 2, 10007))
```
> **复杂度**：O(p) 预处理，O(log_p n) 查询，空间 O(p)

---
#### 17.17.14 例 14：第一类斯特林数符号计数（HDU 2111 变式）⭐
> **知识点**：斯特林数、动态规划、圆排列｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n, k（1≤k≤n≤20），求把 n 个不同元素恰好分成 k 个非空圆排列（循环）的方案数（无符号第一类斯特林数）。

**思路**
递推 S(n,k)=S(n-1,k-1)+(n-1)·S(n-1,k)，前者新元素单成圆，后者插入已有圆排列的 (n-1) 个空隙。

💡 类比"围炉座谈排圆桌：新来的人要么自己开一桌，要么插进某桌某人旁边，插法就是已有的人数种"：

```python
def stirling1(n, k):
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            dp[i][j] = dp[i - 1][j - 1] + (i - 1) * dp[i - 1][j]
    return dp[n][k]

print(stirling1(5, 2))
```
> **复杂度**：O(nk) 时间，O(nk) 空间

---
#### 17.17.15 例 15：第二类斯特林数划分（HDU 2216 变式）⭐⭐
> **知识点**：第二类斯特林数、动态规划｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n, k（1≤k≤n≤1000），求把 n 个不同元素划分成 k 个非空集合（组内无序）的方案数 S(n,k)。

**思路**
递推 S(n,k)=S(n-1,k-1)+k·S(n-1,k)，新元素要么自成一组，要么放入已有 k 组中任意一组。

💡 类比"把学生分进 k 个不署名的小组：新同学要么单独开新组，要么随便钻哪一组去"：

```python
def stirling2(n, k):
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            dp[i][j] = dp[i - 1][j - 1] + j * dp[i - 1][j]
    return dp[n][k]

print(stirling2(5, 3))
```
> **复杂度**：O(nk) 时间，O(nk) 空间

---
#### 17.17.16 例 16：指数型生成函数 / Bell 数（HDU 2068）⭐⭐
> **知识点**：Bell 数、指数型计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n（1≤n≤20），求将 n 个不同元素划分成任意个非空集合的方案总数（第 n 个 Bell 数 B(n)）。

**思路**
Bell 数满足 B(n)=Σ_{k=1..n} S(n,k)，即各分块数第二类斯特林数之和，也可用递推 B(n+1)=Σ C(n,k)·B(k)。

💡 类比"给一群演员随意分组：不管分成几组都可以，把所有分组数都加起来"：

```python
def bell(n):
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            dp[i][j] = dp[i - 1][j - 1] + j * dp[i - 1][j]
    return sum(dp[n])

for n in range(1, 7):
    print(n, bell(n))
```
> **复杂度**：O(n²) 时间，O(n²) 空间

---
#### 17.17.17 例 17：生成函数求方案数（洛谷 P2069）⭐⭐⭐
> **知识点**：生成函数、多项式卷积、背包DP｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：`(1+x+x^2+…+x^{a1})` 等多组括号相乘，求展开式中 x^m 项的系数。即从若干组物品中各取 0≤取≤limit 个，总数为 m 的方案数。

**思路**
每组物品对应因子，求其幂指数分布；做多项式卷积（DP 递推系数）得到最终 x^m 系数。

💡 类比"自助餐搭配：每种菜品能夹多少份是个限位，求恰好装满的搭配方法数，用背包一层一层累计"：

```python
def gen_count(m, limits):
    dp = [0] * (m + 1)
    dp[0] = 1
    for cap in limits:
        ndp = [0] * (m + 1)
        for cur in range(m + 1):
            if dp[cur] == 0:
                continue
            for take in range(cap + 1):
                if cur + take <= m:
                    ndp[cur + take] += dp[cur]
        dp = ndp
    return dp[m]

print(gen_count(5, [2, 3, 5]))  # 三组,每组取 0..cap,凑5
```
> **复杂度**：O(g·m·limit) 时间，O(m) 空间

---
#### 17.17.18 例 18：鸽巢原理求重复点对（洛谷 P2239 变式）⭐
> **知识点**：鸽巢原理、哈希｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n（1≤n≤10^6）个整数（值域 [1,m]，m<n），由鸽巢原理必存在重复值，输出任意一个出现至少两次的数及其位置。

**思路**
因为数域小于数量，用哈希表记录每个数首次出现位置，遇到重复即输出。

💡 类比"羽毛球的球筒必须装 12 只但有 13 只：抽屉只有 12 个格子，多出的那只必塞进已有球的格子"：

```python
def duplicate(a, m):
    first = {}
    for idx, x in enumerate(a):
        if x in first:
            return first[x], idx, x
        first[x] = idx
    return None

a = [3, 1, 4, 2, 5, 3, 1]
print(duplicate(a, 5))
```
> **复杂度**：O(n) 时间，O(m) 空间

---
#### 17.17.19 例 19：可重集组合正整数解（HDU 2014 变式）⭐
> **知识点**：隔板法、可重集组合｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：求正整数解 x1+x2+…+xn = m 的个数（xi≥1）。结果可能很大，输出对 1000 mod。

**思路**
先每项减去 1 得非负解，转化为隔板法：等价于 C(m-1, n-1)。

💡 类比"给 n 个孩子最少分一块再分剩下的：每份都先保证 1，剩下 m-n 块任意插板"：

```python
def comb(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r

def pos_int_solutions(n, m):
    return comb(m - 1, n - 1)

print(pos_int_solutions(3, 10))  # x+y+z=10, xi>=1
```
> **复杂度**：O(k) 时间，O(1) 空间

---
#### 17.17.20 例 20：错排+组合混合（HDU 2068 变式）⭐⭐
> **知识点**：错排、组合数组合应用｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 人猜对至少一半才算通过，求全部猜对的获奖安排总数：选 k 个位置正确（k=n/2 向上取整到 n），其余错排。n≤25。

**思路**
枚举正确位置数 k（从 ceil(n/2) 到 n），方案数 C(n,k)·D(n-k)，D 为错排，累加。

💡 类比"猜名次榜：先挑出 k 个保证猜对的，剩下一帮人必须全部猜错，两部分方案相乘"：

```python
def derange(n):
    if n == 0:
        return 1
    if n == 1:
        return 0
    if n == 2:
        return 1
    a, b = 0, 1
    for i in range(3, n + 1):
        a, b = b, (i - 1) * (a + b)
    return b

def C(n, k):
    from math import comb
    return comb(n, k)

def ans(n):
    total = 0
    for k in range((n + 1) // 2, n + 1):
        total += C(n, k) * derange(n - k)
    return total

for n in (4, 5, 20):
    print(n, ans(n))
```
> **复杂度**：O(n²) 时间，O(1) 空间

---
#### 17.17.21 例 21：双色球组合期望（洛谷 P2116）⭐⭐
> **知识点**：概率、条件概率、组合计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：袋中有 R 个红球、B 个蓝球，每次不放回取 1 个球，求抽完所有球前"红球一直多于蓝球"的概率。R,B≤100。

**思路**
经典计数：先取任意排列数为 C(R+B,R)，红球始终领先的排列数与"从 (0,0) 到 (R,B) 不越线"的卡特兰型路径一致，概率 = (R-B)*C(R+B,R)/(R+B 相关公式) 用球计数等式：有利数 = C(R+B-1, R-B)。

💡 类比"红蓝两条线赛跑：把红蓝各看成上下台阶组成的折线，全程不让蓝反超等价于路径始终在线下方，可用反射法计数"：

```python
from math import comb

def leading_prob(R, B):
    if R <= B:
        return 0.0
    fav = comb(R + B - 1, R - B)   # 反射原理/领先路径计数
    return fav / comb(R + B, B)

for R, B in ((3, 2), (5, 2), (4, 4)):
    print(R, B, round(leading_prob(R, B), 5))
```
> **复杂度**：O(1)（组合函数 O(min)）时间，O(1) 空间

---
#### 17.17.22 例 22：摸球数学期望（HDU 2018 变式）⭐
> **知识点**：期望、线性期望运算法则｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：袋中 n 个球标号 1..n，不放回逐个取。定义随机变量 X_i=1 若第 i 次取到标号 i，求 ΣX_i 的期望（固定点为配对期望）。

**思路**
由期望线性性，E[ΣX_i]=ΣE[X_i]，单点被对中的概率均为 1/n，故期望为 n·(1/n)=1。

💡 类比"每人把自己的帽子挂架随机抽回来：每个人抽到自己帽子的平均个数，就等于所有人抽中自己概率再相加"：

```python
def fixed_point_expect(n):
    # E[Σ Xi], Xi=1 if i-th draw equals i
    return 1.0  # n * (1/n)

for n in (1, 10, 100):
    print(f"n={n}, E={fixed_point_expect(n)}")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.17.23 例 23：掷骰子到达终点的期望步数（洛谷 P1365）⭐⭐
> **知识点**：期望递推、动态规划｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从下标 0 出发，每次掷一个面数 m 的骰子等概率前进 1~m 步（超出终点则停止），求到达终点 N 的期望掷骰子次数。N≤10^5。

**思路**
倒推 dp[i]=1 + (1/m)·Σ dp[i+j]，i+j 越界时用 dp[N]（终点 0）；从 N-1 倒推到 0，dp[i] 表示从 i 到 N 的期望步数。

💡 类比"爬阶梯扔骰子：站在哪一级，往后的平均还需要多少步，只跟下一步可能落到哪有关，所以倒着算"：

```python
def expect_steps(N, m):
    dp = [0.0] * (N + 1)
    for i in range(N - 1, -1, -1):
        s = 0.0
        cnt = 0
        for j in range(1, m + 1):
            s += dp[N] if i + j >= N else dp[i + j]
            cnt += 1
        dp[i] = 1.0 + s / cnt
    return dp[0]

print(expect_steps(10, 6))
print(expect_steps(100, 3))
```
> **复杂度**：O(N·m) 时间，O(N) 空间

---
#### 17.17.24 例 24：马尔可夫链吸收态期望（HDU 2019 变式）⭐⭐
> **知识点**：马尔可夫链、状态转移、期望方程｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：虫子在环 0..n-1 上游走，从 0 出发，在 i 处分别以随机概率左/右移或停留，求首次回到并停留在吸收态的期望时间。n≤20。

**思路**
设 E[i] 为从 i 出发首次到达吸收态 s 的期望步数，列线性方程组 E[i]=1+Σ P(i→j)·E[j]，E[s]=0 或对吸收态直接定义目标，高斯消元求解。

💡 类比"公园随机散步找出口：每个路口平均再走几步，取决于各条岔路各自的平均步数，写成一元一次方程组联立解"：

```python
def gauss(A):
    n = len(A)
    for col in range(n):
        r = next(i for i in range(col, n) if A[i][col] != 0)
        A[col], A[r] = A[r], A[col]
        for i in range(n):
            if i != col and A[i][col]:
                f = A[i][col] / A[col][col]
                for j in range(col, n + 1):
                    A[i][j] -= f * A[col][j]
    return [A[i][n] / A[i][i] for i in range(n)]

def expected_steps(n, sink):
    A = []
    for i in range(n):
        if i == sink:
            row = [0.0] * (n + 1)
            row[i] = 1.0
            row[n] = 0.0
        else:
            row = [0.0] * (n + 1)
            l = (i - 1) % n
            r = (i + 1) % n
            row[i] += 1
            row[l] -= 0.5
            row[r] -= 0.5
            row[n] = 1.0
        A.append(row)
    E = gauss(A)
    return E[0]

print(round(expected_steps(4, 0), 4))
```
> **复杂度**：O(n³) 时间，O(n²) 空间

---
#### 17.17.25 例 25：金鸡蛋 / 双蛋摔落问题（HDU 2082 变式）⭐⭐⭐
> **知识点**：最优策略期望、动态规划、数学建模｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 K 个鸡蛋与 N 层楼，鸡蛋从某临界楼层及以上摔碎。求在最坏情况下确定临界楼层所需的最少尝试次数 f(N,K)。N≤10^3,K≤100。

**思路**
dp[i][j]=用 i 次尝试、j 个鸡蛋最多能确定的楼层数：dp[i][j]=dp[i-1][j-1] + dp[i-1][j] + 1，逐次累加得到覆盖全部楼层的最少次数。

💡 类比"测摔不碎的玻璃：分成两段猜，一段测碎了剩一颗换个范围，没碎就在上面继续分，信息量最优二分"：

```python
def min_tests(N, K):
    if K == 1:
        return N
    dp = [[0] * (K + 1) for _ in range(N + 1)]
    best = 0
    for i in range(1, N + 1):
        for j in range(1, K + 1):
            dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j] + 1
        if dp[i][K] >= N:
            best = i
            break
    return best

print(min_tests(100, 2))
print(min_tests(1000, 3))
```
> **复杂度**：O(N·K) 时间，O(N·K) 空间

---
#### 17.17.26 例 26：二项式系数整除奇偶性（洛谷 P1866 变式）⭐
> **知识点**：卢卡斯特例、二进制位、组合奇偶（Lucas 定理 Kummer）｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n, k，判断 C(n,k) 是否为奇数（即是否不整除 2）。n,k≤10^9。

**思路**
由 Lucas 定理（模 2），C(n,k) 奇当且仅当 n 的每个二进制位 >= k 的对应位，即 (k & ~n)==0（k 是 n 的子集位）。

💡 类比"二进制里位与位：k 的每一位都必须长在 n 的位里，差一位结果就变偶"：

```python
def comb_is_odd(n, k):
    return (k & ~n) == 0

for n, k in ((5, 2), (7, 3), (8, 2), (10, 5)):
    print(n, k, comb_is_odd(n, k))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.17.27 例 27：全错排概率（洛谷 P1608 变式）⭐
> **知识点**：错排、概率比值｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个信封随机装入 n 封信，求没有一封信装进自己信封的概率。n≤20，输出浮点数。

**思路**
概率 = D(n)/n!，其中 D(n) 为完全错排数。递推 D(n)=(n-1)(D(n-1)+D(n-2))。

💡 类比"圣诞错位投递：让所有信都投错信箱，比对总数就是错排数与全排列之比"：

```python
from math import factorial

def miss_prob(n):
    if n == 1:
        return 0.0
    a, b = 0, 1
    for i in range(3, n + 1):
        a, b = b, (i - 1) * (a + b)
    if n == 2:
        b = 1
    return b / factorial(n) if n >= 2 else 0

for n in (3, 5, 10, 20):
    print(n, round(miss_prob(n), 8))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.17.28 例 28：矩形的组合拼砌块数（HDU 2050）⭐
> **知识点**：平面分割、递推公式｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 条折线两两相交时最多把平面分成几部分？输入 n（≤10^4），输出平面区域数。折线由两条射线共点构成。

**思路**
每条折线相当于两条"半直线"，递推区域数 f(n)=f(n-1)+4(n-1)+1，化简 f(n)=2n²-n+1。

💡 类比"切披萨：每加一刀，新增的块数等于这条线被旧线切成的段数加一，逐刀累加"：

```python
import sys

for line in sys.stdin:
    n = int(line.strip())
    print(2 * n * n - n + 1)
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.17.29 例 29：排列的环分解（洛谷 P2070 变式）⭐⭐
> **知识点**：循环置换、排列结构｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 1..n 的一个排列，求其循环分解中所含循环的个数以及每个循环的长度。n≤10^5。

**思路**
按位置做并查集或直接标记遍历，模拟把 p[i] 放到 i，每个未访问起点走一圈记为一个循环。

💡 类比"连连交换座位的同学：从一个人开始顺着'他坐的又是谁的位'一路找，直到回到自己，形成一圈"：

```python
def cycle_partition(p):
    n = len(p)
    vis = [False] * n
    res = []
    for i in range(n):
        if not vis[i]:
            cyc = []
            j = i
            while not vis[j]:
                vis[j] = True
                cyc.append(j + 1)
                j = p[j] - 1
            res.append(cyc)
    return res

p = [2, 3, 1, 5, 4]
for c in cycle_partition(p):
    print("cycle:", c)
```
> **复杂度**：O(n) 时间，O(n) 空间

---
#### 17.17.30 例 30：可重集组合通解（HDU 2017 变式）⭐⭐
> **知识点**：可重集组合、容斥原理｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从 n 种物品中取 r 个，第 i 种至少取 a_i、至多取 b_i 个，求方案数。n≤10，r,b≤10^3。

**思路**
先统一减去下界 a_i，变成每项 ≤ (b_i-a_i) 的取法，用容斥枚举超过上界的子集再 C(r'-sum... , n-1) 校正。

💡 类比"自助取餐有上限：先把保底夹满，再用容斥把哪些菜夹超量的情况减掉"：

```python
from math import comb as C

def bounded_combs(lo, hi, r):
    n = len(lo)
    r -= sum(lo)
    if r < 0:
        return 0
    cap = [hi[i] - lo[i] for i in range(n)]
    total = 0
    for mask in range(1 << n):
        extra = 0
        bits = 0
        for i in range(n):
            if mask >> i & 1:
                extra += cap[i] + 1
                bits += 1
        if r - extra < 0:
            cur = 0
        else:
            cur = C(r - extra + n - 1, n - 1)
        total += cur if bits % 2 == 0 else -cur
    return total

print(bounded_combs([1, 1, 1], [2, 2, 2], 6))
```
> **复杂度**：O(2^n·n) 时间，O(1) 空间

---
#### 17.17.31 例 31：连续正整数划分数（洛谷 P2404）⭐⭐
> **知识点**：组合、整数划分、搜索｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：把正整数 n（2≤n≤200）表示成若干个递增正整数之和，输出所有划分（非递降序列且无重复，按字典序）。

**思路**
DFS 搜索，每步从 last 到 n 递增取数，累计和等于 n 时输出序列，剪枝保证和不超过 n。

💡 类比"把一条长度 n 的绳子剪成递增小段：从上一段的长度开始，只能越剪越长，到整段用完为止输出"：

```python
def partitions(n):
    res = []
    def dfs(last, s, cur):
        if s == n:
            res.append(cur[:])
            return
        # 需要至少还能取一段
        for x in range(last, n - s + 1):
            cur.append(x)
            dfs(x, s + x, cur)
            cur.pop()
    dfs(1, 0, [])
    return res

for p in partitions(6):
    print("+".join(map(str, p)))
```
> **复杂度**：指数级（划分函数 p(n)）时间，O(n) 空间

---
#### 17.17.32 例 32：多项系数的通项（HDU 2084 变式）⭐⭐
> **知识点**：多项展开、分子系数、可重集排列｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 (x1+x2+…+xk)^n 展开中 x1^a1 x2^a2 … xk^ak 项的系数 mod 1000000007，其中 Σa_i=n。

**思路**
系数为多项式系数 n!/(a1!a2!…ak!)，预处理阶乘与逆元，乘起来取模。

💡 类比"分糖果给 k 个标签盒：总排列里把相同目标糖的重复计数除掉"：

```python
MOD = 10**9 + 7
N = 2005
fact = [1] * N
for i in range(1, N):
    fact[i] = fact[i - 1] * i % MOD
invf = [1] * N
invf[N - 1] = pow(fact[N - 1], MOD - 2, MOD)
for i in range(N - 1, 0, -1):
    invf[i - 1] = invf[i] * i % MOD

def multinomial(n, a):
    r = fact[n]
    for x in a:
        if x < 0:
            return 0
        r = r * invf[x] % MOD
    return r

print(multinomial(5, [2, 2, 1]))
print(multinomial(5, [3, 1, 1]))
```
> **复杂度**：O(N) 预处理，O(k) 查询，空间 O(N)

---
#### 17.17.33 例 33：独立事件并的概率（洛谷 P1433 变式）⭐
> **知识点**：概率、独立事件、容斥原理｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个独立事件，第 i 个发生概率为 p_i，求"至少发生一件"的概率。输出保留若干位小数。n≤20。

**思路**
至少一件 = 1 - 全部不发生的概率 = 1 - ∏(1-p_i)，独立事件可相乘。

💡 类比"多个并联报警器：只要有一个响就算响，全都不响的概率是各自失灵概率的乘积"：

```python
def at_least_one(p):
    none = 1.0
    for q in p:
        none *= (1 - q)
    return 1 - none

print(round(at_least_one([0.5, 0.3, 0.2]), 6))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.17.34 例 34：随机过程吸收期望（HDU 2011 变式）⭐⭐
> **知识点**：随机过程、期望递推｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：赌徒以 1/2 概率赢 1 元、以 1/2 概率输 1 元，破产为 0 元、封顶为 N 元。若初金 i 元，求破产概率。i≤N≤100。

**思路**
设 P[i] 破产概率：0 处 1，N 处 0，中间 P[i]=0.5·P[i-1]+0.5·P[i+1]，等差解 P[i]=1-i/N。

💡 类比"左右各一步的醉汉走路：对称随机游走破产概率从两端线性插值，边界一危一早封顶"：

```python
def ruin_prob(N, i):
    # 对称随机游走，有吸收墙0和N
    return 1.0 - i / N

for case in ((10, 5), (10, 2), (20, 10)):
    N, i = case
    print(case, round(ruin_prob(N, i), 4))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.17.35 例 35：期望线性性求逆序对期望（洛谷 P2894 变式）⭐⭐
> **知识点**：期望线性性、逆序对、均匀随机｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：随机均匀生成 1..n 的一个排列，求逆序对个数的期望。n≤10^6，输出浮点数。

**思路**
逆序对期望 = C(n,2)·(1/2)，因为每对数恰好各有 1/2 概率构成逆序（对选择的均匀排列前半偏序独立）。

💡 类比"排队随机乱序：任意两人谁在前一样可能，平均一半对数是逆序"：

```python
def expected_inversions(n):
    return n * (n - 1) / 4.0

for n in (2, 3, 10, 1000000):
    print(n, expected_inversions(n))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.17.36 例 36：几何分布期望（HDU 2015 变式）⭐
> **知识点**：几何分布、期望均值｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：中奖概率 p，独立重复抽奖直到首次中奖，求期望抽奖次数。p∈(0,1]，输出保留 2 位小数。

**思路**
首次成功所需次数服从几何分布，期望 E=1/p，直接计算。

💡 类比"刮刮乐抽到大奖：平均要刮的次数就是成功率倒数，成功率越高刮得越少"：

```python
def geo_expect(p):
    return 1.0 / p

for p in (0.5, 0.1, 1.0):
    print(f"p={p}, E={geo_expect(p):.2f}")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.17.37 例 37：含重复字符的排列数（洛谷 P2080 变式）⭐
> **知识点**：可重集排列、阶乘比｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一串字符（含重复），求其不同排列个数。长度 ≤20，结果可大整数。

**思路**
不同排列 = len! / ∏(每种字符个数!)，用 Counter 统计频次后乘除。

💡 类比"洗一副重复花色扑克：把所有排列数出来除以相同花色内部的重复交换"：

```python
from collections import Counter

def distinct_permutations(s):
    n = len(s)
    fact = [1] * (n + 1)
    for i in range(2, n + 1):
        fact[i] = fact[i - 1] * i
    res = fact[n]
    for c in Counter(s).values():
        res //= fact[c]
    return res

print(distinct_permutations("AABB"))
print(distinct_permutations("banana"))
```
> **复杂度**：O(n) 时间，O(n) 空间

---
#### 17.17.38 例 38：全排列中的第 k 个排列（洛谷 P2012 变式）⭐⭐⭐
> **知识点**：阶乘进制、康托展开逆运算｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 与 k（1≤n≤15，1≤k≤n!），输出 1..n 全排列中字典序第 k 个排列。k 为 1-index 大整数。

**思路**
逆康托展开：对每一位，用 (k-1)//(n-1-i)! 决定选剩余数字中第几小的，更新 k，逐位构造。

💡 类比"按字典序找书：第一个数字决定它落在所有排列里的第几个'区块'，余数再去定第二位"：

```python
def kth_permutation(n, k):
    fact = [1] * (n + 1)
    for i in range(2, n + 1):
        fact[i] = fact[i - 1] * i
    pool = list(range(1, n + 1))
    k -= 1
    res = []
    for i in range(n):
        block = fact[n - 1 - i]
        idx = k // block
        res.append(pool.pop(idx))
        k %= block
    return res

print(kth_permutation(4, 5))
print(''.join(map(str, kth_permutation(9, 362880))))
```
> **复杂度**：O(n²) 时间，O(n) 空间

---
#### 17.17.39 例 39：不同对象的成圈方案（洛谷 P2020 变式）⭐⭐
> **知识点**：圆排列、循环计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个不同的人围成一圈（旋转视为相同）有多少种坐法？n≤20，输出方案数。

**思路**
圆排列数 = (n-1)!，因为环的起点 1 的 n 个旋转等价，故 n!/n=(n-1)!。

💡 类比"圆桌固定一把椅子：先随便排再除以转圈重复的次数"：

```python
from math import factorial

def circular_perm(n):
    return factorial(n - 1) if n >= 1 else 1

for n in range(1, 6):
    print(n, circular_perm(n))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.17.40 例 40：正整数的无序拆分数（洛谷 P2388 变式）⭐⭐
> **知识点**：整数划分、动态规划｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求正整数 n（≤200）拆分成若干正整数之和（顺序无关）的方案数 p(n)。结果较大，输出对 10^9+7 取模。

**思路**
DP：dp[s][max] 表示最大加数不超过 max 且和为 s 的拆分数，转移选与不选 max 这个加数。

💡 类比"零钱换硬币：每增加一种面额，就用它多凑若干遍，类似完全背包"：

```python
MOD = 10**9 + 7

def partition_count(n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for coin in range(1, n + 1):
        for s in range(coin, n + 1):
            dp[s] = (dp[s] + dp[s - coin]) % MOD
    return dp[n]

for n in (5, 10, 200):
    print(n, partition_count(n))
```
> **复杂度**：O(n²) 时间，O(n) 空间

---
#### 17.17.41 例 41：n 个元素的二元组配对（洛谷 P2013 变式）⭐
> **知识点**：配对计数、乘法原理、阶乘｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：把 2n 个不同元素两两配成 n 对（内部无序、对之间无序），求方案数。2n≤30。

**思路**
方案数 = (2n)!/(2^n·n!)，即 C(2n,2)·C(2n-2,2)…/n!。

💡 类比"班级两两握手配对：先给 2n 人排长队第一个跟第二个握，第二个跟第三个握……成对后再把顺序打乱重复除"：

```python
def pairings(n):
    res = 1
    for i in range(n):
        res *= (2 * n - 2 * i) * (2 * n - 2 * i - 1) // 2
        res //= (i + 1)
    return res

for n in range(1, 7):
    print(n, pairings(n))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.17.42 例 42：快速幂组合原理（HDU 2099 变式）⭐
> **知识点**：快速幂、组合、费马小定理｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 a 与素数 mod，求 2^(a mod 关系) 系列问题的基底训练：输出 a^b mod p。a,b≤10^9。

**思路**
快速幂：反复平方法，将指数按二进制累乘。

💡 类比"翻倍叠方块纸：每次平方成倍，按幂的二进制位挑要乘的层"：

```python
def qpow(a, b, mod):
    r = 1
    a %= mod
    while b:
        if b & 1:
            r = r * a % mod
        a = a * a % mod
        b >>= 1
    return r

print(qpow(2, 10, 1000000007))
print(qpow(3, 0, 5))
```
> **复杂度**：O(log b) 时间，O(1) 空间

---
#### 17.17.43 例 43：二项分布某一项的贡献（洛谷 P2051 变式）⭐⭐
> **知识点**：二项分布、组合数、概率权值｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：独立重复伯努利试验成功概率 p，做 n 次，求恰好成功 k 次的概率，乘以总权值重标度。n≤1000。

**思路**
恰好 k 次成功概率 = C(n,k)·p^k·(1-p)^(n-k)，累乘避免大数溢出。

💡 类比"投篮命中率：选哪 k 次中，再把每次概率乘起来"：

```python
from math import comb

def binomial_pmf(n, k, p):
    return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

print(round(binomial_pmf(10, 5, 0.5), 6))
print(round(binomial_pmf(20, 10, 0.4), 6))
```
> **复杂度**：O(k) 时间，O(1) 空间

---
#### 17.17.44 例 44：递推数列的矩阵快速幂（HDU 2045 变式）⭐⭐⭐
> **知识点**：矩阵快速幂、递推、斐波那契｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求斐波那契式递推 F(n)=F(n-1)+F(n-2) 的第 n 项 mod 1e9+7，n 可达 10^18。

**思路**
用 2×2 转移矩阵 [[1,1],[1,0]] 的 n 次幂快速算，把递推转成矩阵乘法的对数复杂度。

💡 类比"兔子数列加速器：把两个递推写进矩阵，用快速幂一次跳到很大 n"：

```python
MOD = 10**9 + 7

def matmul(A, B):
    return [[(A[0][0]*B[0][0]+A[0][1]*B[1][0])%MOD,
             (A[0][0]*B[0][1]+A[0][1]*B[1][1])%MOD],
            [(A[1][0]*B[0][0]+A[1][1]*B[1][0])%MOD,
             (A[1][0]*B[0][1]+A[1][1]*B[1][1])%MOD]]

def fib(n):
    if n == 0:
        return 0
    M = [[1, 1], [1, 0]]
    R = [[1, 0], [0, 1]]
    while n:
        if n & 1:
            R = matmul(R, M)
        M = matmul(M, M)
        n >>= 1
    return R[0][1]

print(fib(10))
print(fib(10**18))
```
> **复杂度**：O(log n) 时间，O(1) 空间

---
#### 17.17.45 例 45：期望最优决策（洛谷 P1289 变式）⭐⭐⭐
> **知识点**：期望DP、最优策略、动态规划博弈混合｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：盗贼面对两扇门，门 A 可获 x 元后被困 t_A 轮，门 B 可获 y 元后被困 t_B 轮，均可重复进入。求在 r 轮内能获得金币的最大期望。r≤10^3。

**思路**
设 E[t] 为剩余 t 轮的最大期望收益：E[t]=max( x+E[max(0,t-tA)], 与停留门比较)，倒推 dp 并做决策取最大。

💡 类比"反复抽奖机的两个按钮：每个按钮的期望收益都可能把剩余抽数带回来，选更划算的那个"：

```python
def best_expect(T, x, tA, y, tB):
    dp = [0.0] * (T + 1)
    for t in range(1, T + 1):
        chooseA = x + dp[max(0, t - tA + 1)]
        chooseB = y + dp[max(0, t - tB + 1)]
        dp[t] = max(chooseA, chooseB)
    return dp[T]

print(best_expect(10, 5, 2, 8, 3))
print(best_expect(100, 3, 1, 10, 5))
```
> **复杂度**：O(T) 时间，O(T) 空间

---
#### 17.17.46 例 46：环形分发组合（洛谷 P1390 变式）⭐⭐
> **知识点**：组合数、环形染色思想、循环同构｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个位置围成一圈，用 k 种颜色给各位置涂色，相邻不同色，且旋转相同视为同一方案，求方案数 mod p。n,k≤10^6。

**思路**
不旋转去重时为 (k-1)^n + (-1)^n·(k-1)（经典环形染色公式），再结合 Burnside 需除去循环同构组数——本题近似使用染色公式，配合逆元取模。

💡 类比"串彩色珠子手链：首尾回环让第一个和最后一个也不能同色，形成闭环约束"：

```python
MOD = 10**9 + 7

def ring_colors(n, k, mod=MOD):
    return (pow(k - 1, n, mod) + (k - 1) * ((-1) ** n)) % mod

print(ring_colors(3, 3))
print(ring_colors(4, 3))
```
> **复杂度**：O(log n) 时间，O(1) 空间

---
#### 17.17.47 例 47：子集生成与子集和计数（洛谷 P1412 变式）⭐
> **知识点**：子集枚举、二进制表示｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个元素，求所有子集的个数以及"和为给定值 S"的子集个数。n≤20，S 绝对值可控。

**思路**
用位掩码从 0 枚举到 2^n-1，每位代表选不选，统计和等于 S 的个数。

💡 类比"开关串灯：每个灯一个二进制开关位，遍历所有 0/1 组合看亮灯情况"：

```python
def subset_count(a, S):
    n = len(a)
    cnt = 0
    for mask in range(1 << n):
        s = 0
        for i in range(n):
            if mask >> i & 1:
                s += a[i]
        if s == S:
            cnt += 1
    return cnt

print(subset_count([1, 2, 3, 4], 5))  # {1,4},{2,3}
```
> **复杂度**：O(2^n·n) 时间，O(1) 空间

---
#### 17.17.48 例 48：可分拆数的递推（洛谷 P2038 变式）⭐⭐
> **知识点**：整数划分、五边形数、生成函数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 p(n)（正整数拆分数）对 1e9+7 取模，n≤10^4。用欧拉五边形数定理递推加速。

**思路**
五边形数定理：p(n)=p(n-g1)-p(n-g2)+…，广义五边形数 g_k=k(3k-1)/2 交错加减。

💡 类比"快速数零钱组合：利用生成函数因子把它变成每个 n 只跟少数几个更小的 p 相加减"：

```python
MOD = 10**9 + 7

def partition_fast(n):
    p = [0] * (n + 1)
    p[0] = 1
    for i in range(1, n + 1):
        k = 1
        while True:
            g1 = k * (3 * k - 1) // 2
            g2 = k * (3 * k + 1) // 2
            sign = 1 if k % 2 == 1 else -1
            if g1 > i and g2 > i:
                break
            if g1 <= i:
                p[i] += sign * p[i - g1]
            if g2 <= i:
                p[i] += sign * p[i - g2]
            k += 1
        p[i] %= MOD
    return p[n]

for n in (5, 10, 10000):
    print(n, partition_fast(n))
```
> **复杂度**：O(n√n) 时间，O(n) 空间

---
#### 17.17.49 例 49：容斥求与集合互质个数（洛谷 P1442 变式）⭐⭐
> **知识点**：容斥、质因数分解、欧拉思想｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 m，求 1..n 中与 m 互质的数的个数。n,m≤10^9。

**思路**
对 m 质因数分解，容斥：用 p1,p2,… 的子集排除不互质的，答案 = n - 单质数集合并各阶找补。

💡 类比"筛掉含特定质因子的数：把每个质因数当一桶颜料，用容斥层层扣除重复涂色的数"：

```python
def coprime_count(n, m):
    # 质因数分解 m
    fs = set()
    d = 2
    x = m
    while d * d <= x:
        while x % d == 0:
            fs.add(d)
            x //= d
        d += 1
    if x > 1:
        fs.add(x)
    fs = list(fs)
    total = 0
    for mask in range(1, 1 << len(fs)):
        prod = 1
        bits = 0
        for i in range(len(fs)):
            if mask >> i & 1:
                prod *= fs[i]
                bits += 1
        total += (n // prod) if bits % 2 == 1 else -(n // prod)
    return n - total

print(coprime_count(30, 12))  # 与12互质的数
```
> **复杂度**：O(√m + 2^ω(log)) 时间，O(1) 空间

---
#### 17.17.50 例 50：对称函数期望（HDU 2105 变式）⭐⭐
> **知识点**：期望线性性、对称分布｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：随机均匀地从 n 个不同数中选一个，求所选数为最大与最小平均值的期望（均匀分布最大值期望）。

**思路**
均匀选一个时每个值被选中概率 1/n，因此期望就是平均值 (min+…+max)/n，若求两端均值特殊则取三均值中位数思想补充。

💡 类比"抽签发奖金：每人纸条重量一样，平均值就是每个人平均能抽到的数额"：

```python
def uniform_expect(arr):
    return sum(arr) / len(arr)

def endpoint_expect(arr):
    s = sorted(arr)
    return (s[0] + s[-1]) / 2.0

arr = [1, 5, 3, 9, 2]
print(round(uniform_expect(arr), 4))
print(round(endpoint_expect(arr), 4))
```
> **复杂度**：O(n) 时间，O(n log n) 空间（排序）可选 O(n)

---
#### 17.17.51 例 51：错位乘法阶梯计（POJ 2249）⭐⭐
> **知识点**：组合数、大整数无溢出技巧｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：计算组合数 b!/(a!(b-a)!)，其中 5≤b≤2^31-1, 1≤a≤b 且保证结果 ≤2^63。多组输入，测试样例以 0 0 结束。

**思路**
用累乘公式逐项相乘再相除控制中间值，确保 long long 范围内不溢出，Python 大整数可自由。

💡 类比"分步取整分摊：乘一点除一点别让中间结果爆表，像做减法前先借位"：

```python
import sys

for line in sys.stdin:
    b, a = map(int, line.split())
    if b == 0 and a == 0:
        break
    a = min(a, b - a)
    res = 1
    for i in range(1, a + 1):
        res = res * (b - a + i) // i
    print(f"{b} things taken {a} at a time is {res} exactly.")
```
> **复杂度**：O(a) 时间，O(1) 空间

---
#### 17.17.52 例 52：伯努利独立重复成功前期望（洛谷 P1503 变式）⭐
> **知识点**：几何分布、期望、负二项｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：一次射击命中率 p，求命中一次前的失败次数期望（即首次成功前失败数几何分布）。

**思路**
首次成功前失败数服从 0-index 几何分布，期望 E=(1-p)/p，先失败次数期望。

💡 类比"打靶练手，打到第一发上靶前空靶的平均枪数"：

```python
def failures_before_success(p):
    return (1 - p) / p

for p in (0.5, 0.2, 0.9):
    print(f"p={p}, E[fail before success]={failures_before_success(p):.3f}")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.17.53 例 53：可重集暴力+容斥上界（洛谷 P1226 变式）⭐⭐
> **知识点**：容斥原理、面向对象枚举、质数集合｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 k 个质数 p_i 与上限 N，求 1..N 中既不被任何 p_i 整除又不是完全平方的数的个数，剔除平方数部分二次容斥。

**思路**
先用容斥统计能被任一 p_i 整除的个数，再对平方数集合（1²..floor(√N)²）做第二层容斥求交，相减。

💡 类比"两层筛网先后筛豆子：先筛质因子覆盖的，再专门回头挑出平方粒，两遍都排除"：

```python
import math

def inc_excl(N, primes):
    from math import gcd
    total = 0
    m = len(primes)
    from functools import reduce
    for mask in range(1, 1 << m):
        l = 1
        bits = 0
        for i in range(m):
            if mask >> i & 1:
                l = l * primes[i] // gcd(l, primes[i])
                bits += 1
            if l > N:
                break
        add = N // l
        total += add if bits % 2 == 1 else -add
    return total

def nonsquare_nonmult(N, primes):
    div = inc_excl(N, primes)
    # 完全平方同时被某 p 整除的交集
    sqmax = int(math.isqrt(N))
    sqs = [x * x for x in range(1, sqmax + 1)]
    squared_div = inc_excl(N, [p for p in primes])
    # 通过统计: 完全平方数中能被任一 p 整除 —— 直接枚平方数
    cntsq = sum(1 for s in sqs if any(s % p == 0 for p in primes))
    return N - div - (len(sqs) - cntsq)

# 例: N=100, primes=[2,5] => 不能含2/5因子且非平方
print(nonsquare_nonmult(100, [2, 5]))
```
> **复杂度**：O(k·2^k + √N·k) 时间，O(1) 空间

---
#### 17.17.54 例 54：全错排队列情侣（洛谷 P1288 变式）⭐⭐
> **知识点**：错排问题形变、DP 组合｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 对夫妻围桌就座，要求夫妻不相邻，求坐法数 mod p。n≤10^5。

**思路**
先用容斥：总数(2n)! 减去至少一对相邻：枚举 k 对并在一起，用容斥与可重排列整理成递推，最后乘 2^n 方式整理对性别。

💡 类比"圆桌夫妻互不见面：先按不相邻的总约束做容斥扣除相邻情形，再处理旋转同构"：

```python
MOD = 10**9 + 7

def couple_round(n, mod=MOD):
    # 利用容斥: 不相邻圆排列
    F = 1
    jc = [1] * (n + 1)
    for i in range(1, n + 1):
        jc[i] = jc[i - 1] * i % mod
    total = 0
    for k in range(n + 1):
        sgn = 1 if k % 2 == 0 else -1
        term = jc[n - k] * pow(2, k, mod) % mod * pow(jc[k], mod - 2, mod) % mod
        # 简化数学: 用组合计 C(n,k)*(n-k)!*2^k ... 见下近似注释
        comb = jc[n] * pow(jc[k], mod - 2, mod) % mod * pow(jc[n - k], mod - 2, mod) % mod
        term = comb * jc[n - k] % mod * pow(2, k, mod) % mod
        total = (total + sgn * term) % mod
    return pow(2, n, mod) * total % mod

print(couple_round(3))
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.17.55 例 55：位数与数字和的组合（洛谷 P1641 变式）⭐⭐
> **知识点**：数字DP、组合计数、卡特兰穿越｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求长度为 odd 的合法数字序列中满足"任意前缀 1 不少于 0"的括号型序列个数 mod p。即 n 对括号合法序列 = 卡特兰数。n≤10^6。

**思路**
卡特兰数 C_n=C(2n,n)/(n+1)，用阶乘逆元计算 mod p。

💡 类比"压栈出栈计数：左括号当入栈，右括号当出栈，任意时刻栈不能为负"：

```python
MOD = 10**9 + 7
N = 2000005
fact = [1] * N
for i in range(1, N):
    fact[i] = fact[i - 1] * i % MOD
invf = [1] * N
invf[N - 1] = pow(fact[N - 1], MOD - 2, MOD)
for i in range(N - 1, 0, -1):
    invf[i - 1] = invf[i] * i % MOD

def catalan(n):
    c = fact[2 * n] * invf[n] % MOD * invf[n] % MOD
    return c * pow(n + 1, MOD - 2, MOD) % MOD

print(catalan(5))
print(catalan(1000000))
```
> **复杂度**：O(N) 预处理，O(1) 查询，空间 O(N)

---
#### 17.17.56 例 56：错排近似渐进（洛谷 P2014 变式）⭐⭐
> **知识点**：错排、渐近尾数量级｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 很大（≤10^6），求错排数 D(n) mod p。利用递推 D(n)=(n-1)(D(n-1)+D(n-2)) mod p 的线性时间。

**思路**
两次环形扫描递推即可，注意阶梯取模。

💡 类比"打乱后无人坐原位：递推每个位置少了许多，前两个已知逐项推进"：

```python
MOD = 10**9 + 7

def derange_mod(n, mod=MOD):
    if n == 0:
        return 1
    if n == 1:
        return 0
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b % mod, ((i - 1) * (a + b)) % mod
    return b % mod

print(derange_mod(10))
print(derange_mod(1000000))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.17.57 例 57：等价关系与贝尔细分（洛谷 P1287 变式）⭐⭐⭐
> **知识点**：斯特林分布、Bell 多项式、组合DP 高级｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：把 n 个不同元素放入 m 个不同盒子，盒子空不空分别讨论：求使用不超过 m 个非空盒子或恰好填满 m 个盒子的放法（Surjection 计数）。n,m≤10^3。

**思路**
恰好填满 m 盒 = m!·S(n,m)；不超过 m 盒 = Σ_{j=1..m} C(m,j)·j!·S(n,j) 或直接 m^n（允许空盒）。

💡 类比"给邮箱群发：是看每封都得塞进且互相区分，把重复的划分抹平再分配"：

```python
def surjections(n, m):
    # 恰好填满 m 个不同盒子 = m! S(n,m)
    S = [[0] * (m + 1) for _ in range(n + 1)]
    S[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(i, m) + 1):
            S[i][j] = S[i - 1][j - 1] + j * S[i - 1][j]
    from math import factorial
    return factorial(m) * S[n][m]

def allow_empty(n, m):
    return m ** n

print(surjections(5, 3))
print(allow_empty(5, 3))
```
> **复杂度**：O(n·m) 时间，O(n·m) 空间

---
#### 17.17.58 例 58：错排DP+前缀优化（HDU 2116 变式）⭐⭐
> **知识点**：错排、前缀和优化动态规划｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 D(n)=Σ_{k=0..n}(-1)^k n!/k! 的标准求和取值（mod p），验证两种递推结果一致。n≤10^6。

**思路**
用数学式 D(n)=n!·Σ_{k=0..n}(-1)^k/k! mod p，预先算逆元阶乘，一次循环。

💡 类比"交错加减的级数求和：把各项逆元准备好，一正一负累加"：

```python
MOD = 10**9 + 7

def derange_by_sum(n, mod=MOD):
    fact = 1
    for i in range(2, n + 1):
        fact = fact * i % mod
    inv = [1] * (n + 1)
    for i in range(2, n + 1):
        inv[i] = pow(fact, mod - 2, mod)  # 简化实际用阶乘逆元递推
    # 直接用 pow 因式
    s = 0
    for k in range(n + 1):
        fk = 1
        for i in range(1, k + 1):
            fk = fk * i % mod
        term = fact * pow(fk, mod - 2, mod) % mod
        s = (s + (-term if k % 2 else term)) % mod
    return s

print(derange_by_sum(10))
```
> **复杂度**：O(n²)（演示）实际 O(n) 时间，O(1) 空间

---
#### 17.17.59 例 59：超几何计数（不放回抽样）（HDU 2114 变式）⭐⭐
> **知识点**：超几何分布、不放回组合概率｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：袋中共 N 个球，其中 K 个红。不放回抽 n 个，求正好抽到 k 个红的概率。N≤30。

**思路**
超几何概率 = C(K,k)·C(N-K, n-k)/C(N,n)，用组合公式逐一相乘。

💡 类比"从混合车厢数红车：先挑中红车的组合，再挑非蓝的组合，除以总组合"：

```python
from math import comb

def hypergeo(N, K, n, k):
    if k > K or n - k > N - K:
        return 0.0
    return comb(K, k) * comb(N - K, n - k) / comb(N, n)

print(round(hypergeo(20, 6, 5, 2), 6))
print(round(hypergeo(10, 4, 3, 1), 6))
```
> **复杂度**：O(min(k, n-k)) 时间，O(1) 空间

---
#### 17.17.60 例 60：全排列相邻约束计数（洛谷 P1992 变式）⭐⭐
> **知识点**：排列DP、子集DP、位运算｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：把 n 个不同数排成一列，要求相邻元素差的绝对值都 ≥ d，问合法排列数 mod p。n≤18。

**思路**
排序后做状压 DP：dp[mask][last] 表示已选集合 mask 且最后一个是 last 的合法方案数，转移枚举下一个元素。

💡 类比"排座位不能挨着太近：按位集记录谁已入座，逐个往后接人且检查间距"：

```python
def count_perms(nums, d, mod=10**9 + 7):
    n = len(nums)
    dp = [[0] * n for _ in range(1 << n)]
    for i in range(n):
        dp[1 << i][i] = 1
    for mask in range(1 << n):
        for last in range(n):
            if dp[mask][last] == 0:
                continue
            for nxt in range(n):
                if mask >> nxt & 1:
                    continue
                if abs(nums[nxt] - nums[last]) >= d:
                    dp[mask | (1 << nxt)][nxt] = (dp[mask | (1 << nxt)][nxt] + dp[mask][last]) % mod
    return sum(dp[(1 << n) - 1][i] for i in range(n)) % mod

print(count_perms([1, 3, 5, 2], 2))
```
> **复杂度**：O(2^n·n²) 时间，O(2^n·n) 空间

---
#### 17.17.61 例 61：等比数列求和的二项引理（洛谷 P2050 变式）⭐⭐
> **知识点**：等比求和、二项式、整除同余｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 S = 1 + q + q² + … + q^n mod p，其中 p 为素数，n 可达 10^9。d 分组法用分治（民间经典 UVA 11401 相近）。

**思路**
分治折半：偶数项利用 S(2n)=S(n)(1+q^n)-q^(2n)，奇数用公式递归，O(log n)。

💡 类比"对半切账单一按比例缩放：奇偶分别化成更小区的平方组合手算"：

```python
MOD = 10**9 + 7

def geom_sum(q, n, mod=MOD):
    if n == 0:
        return 1 % mod
    # S(n) = 1+q+..+q^n (共 n+1 项, 0-index 到 n)
    if n % 2 == 1:
        return (1 + q * geom_sum(q, n - 1, mod)) % mod
    half = geom_sum(q, (n // 2) - 1, mod)
    return (half + pow(q, n // 2, mod) * (half + pow(q, (n//2), mod)) ) % mod

# 修正版：直接用公式 S(n)= (q^(n+1)-1)/(q-1)
def geom_fast(q, n, mod=MOD):
    if q == 1:
        return (n + 1) % mod
    num = (pow(q, n + 1, mod) - 1) % mod
    return num * pow(q - 1, mod - 2, mod) % mod

print(geom_fast(2, 5))      # 1+2+4+8+16+32=63
```
> **复杂度**：O(log n) 时间，O(1) 空间

---
#### 17.17.62 例 62：复合选择期望大数（洛谷 P1530 变式）⭐⭐⭐
> **知识点**：期望、斯特林近似、大数组合｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：随机排列 n 个元素，求"第 k 个位置取值恰在其正确区间"的期望个数的近似（或固定点高阶矩），用大组合精确到浮点。

**思路**
固定点指示量期望为 1/n，期望总和恒等于 1。欲求更高时刻端用包含-排除展开成各阶固定点期望。

💡 类比"猜卡片对位：每个位置本就有 1/n 概率对，相加即平均对位张数"：

```python
def fixed_point_moments(n):
    # 随机置换固定点个数的期望 = 1
    one = None
    # 第二矩 E[X^2]=E[X] + n(n-1)*1/(n(n-1)) = 2
    e1 = 1
    e2 = 2
    return e1, e2

print(fixed_point_moments(10))

# 用递推验证
def simulate_expect(n, trials=100000):
    import random
    tot = 0
    for _ in range(trials):
        p = list(range(n))
        random.shuffle(p)
        tot += sum(1 for i in range(n) if p[i] == i)
    return tot / trials

print(round(simulate_expect(12), 4))
```
> **复杂度**：O(n) 时间，O(1) 空间（模拟为 O(n·trials)）

---
#### 17.17.63 例 63：多重集合中位数期望（洛谷 P2044 变式）⭐⭐
> **知识点**：均匀随机、次序统计量、概率密度｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从连续均匀分布 U(0,1) 独立取 n 个样本，求第 k 个次序统计量的期望（=k/(n+1)），输出近似。

**思路**
Beta 分布期望：第 k 个次序统计量期望为 k/(n+1)，直接代数公式。

💡 类比"抽 n 支箭排顺序，中间偏左第 k 支的平均位置约在整体轴上的 k/(n+1) 处"：

```python
def order_stat_expect(n, k):
    return k / (n + 1)

for case in ((10, 1), (10, 5), (20, 15)):
    n, k = case
    print(f"n={n}, k={k}, E={order_stat_expect(n, k):.4f}")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.17.64 例 64：组合恒等式的数论验证（洛谷 P2062 变式）⭐
> **知识点**：组合恒等式、模运算自检｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：验证 Vandermonde 恒等式 Σ_{k}C(a,k)C(b,n-k)=C(a+b,n) mod p，输出结果验证相等。a,b,n≤10^5。

**思路**
左边预处理阶乘逆元求组合，循环求和，右边直接算，比较是否相等（相等则 mp 均同）。

💡 类比"两组菜乱拼的计数自检：从两组子里挑恰好 n 件，等价于从合并的大组挑 n 件"：

```python
MOD = 10**9 + 7
N = 200005
fact = [1] * N
for i in range(1, N):
    fact[i] = fact[i - 1] * i % MOD
invf = [1] * N
invf[N - 1] = pow(fact[N - 1], MOD - 2, MOD)
for i in range(N - 1, 0, -1):
    invf[i - 1] = invf[i] * i % MOD

def comb(n, k):
    if k < 0 or k > n:
        return 0
    return fact[n] * invf[k] % MOD * invf[n - k] % MOD

a, b, n = 5, 6, 4
left = sum(comb(a, k) * comb(b, n - k) for k in range(n + 1)) % MOD
right = comb(a + b, n) % MOD
print("Vandermonde 成立:", left == right, left)
```
> **复杂度**：O(n) 时间，O(N) 空间

---
#### 17.17.65 例 65：随机置换循环期望（HDU 2051 变式）⭐⭐⭐
> **知识点**：线性期望、循环置换、马尔可夫平均结构｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：随机均匀置换 n 个元素，求循环分解中循环个数（固定点即长度为 1 的循环）的期望。n 可达 10^6。

**思路**
用期望线性性：E[循环数]=Σ_{j=1..n} 1/j，因为每个点依概率 1 落进长度 j 的循环；等价于调和数 H_n。

💡 类比"拆礼物环环相扣：每个元素随机连下一个形成环，平均环数正好是调和级数的和"：

```python
def expected_cycles(n):
    # H_n = sum 1/k
    h = 0.0
    for k in range(1, n + 1):
        h += 1.0 / k
    return h

for n in (5, 10, 100, 1000000):
    print(f"n={n}, E[cycles]={expected_cycles(n):.5f}")
```
> **复杂度**：O(n) 时间，O(1) 空间

---

### 17.18 博弈论与 SG 函数

#### 17.18.1 例 1：巴什博弈（HDU 2188）⭐
> **知识点**：巴什博弈、取石子、先手必胜判定｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：一堆 n 个石子，两人轮流取，每次至多取 m 个，取走最后石子者胜。判断先手必胜输出。多组输入。

**思路**
n%(m+1)!=0 则先手必胜，n%(m+1)==0 则后手必胜，因为可维持"和为 m+1"的配对策略。

💡 类比"补齐配对的二进制回暖：后手总能补够 m+1 的量，谁落后于填满回合谁输"：

```python
import sys

def bash_win(n, m):
    return n % (m + 1) != 0

for line in sys.stdin:
    n, m = map(int, line.split())
    print("Win" if bash_win(n, m) else "Lose")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.2 例 2：单堆取法限制（HDU 2147 变式）⭐
> **知识点**：递推博弈、必败态分析｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：只有一堆 n 个石子，每次可取 1、2 或 3 个，取到最后一个获胜，判断先手胜负。多组输入。

**思路**
SG 式从 n 倒推：n%4==0 必败，否则必胜（可维持对 4 的补足）。

💡 类比"四步一循环的节拍：后手总能补成整四，先手只要不撞上整四就稳"：

```python
import sys

for line in sys.stdin:
    n = int(line.strip())
    print("Lose" if n % 4 == 0 else "Win")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.3 例 3：Nim 游戏判定（洛谷 P2197）⭐⭐
> **知识点**：Nim 博弈、异或操作｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 堆石子，每堆 a_i 个，两人轮流取走任意正整数个石子，无子可取者败。判断先手是否必胜。多组输入，n 总和 ≤2·10^5，a_i≤10^9。

**思路**
Nim-Sum：所有堆石子数的异或 XOR。XOR≠0 先手必胜，XOR==0 后手必胜。

💡 类比"三堆军棋对子：把三堆石子的二进制异或归零，谁把异或减到 0 谁掌握节奏"：

```python
import sys

for line in sys.stdin:
    n = int(line.strip())
    a = list(map(int, input().split()))
    x = 0
    for v in a:
        x ^= v
    print("Win" if x else "Lose")
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.18.4 例 4：取石子可选步长米非 Nim（洛谷 P1247）⭐⭐
> **知识点**：Nim + 掌握性、对异或调整取堆｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 堆石子，每次取一堆中任意数量，判断先手是否必胜，若必胜还需输出第一步该取哪堆取几个。a_i≤10^9,n≤10^5。

**思路**
先算总 XOR。若为 0 必败；否则找 max 堆满足 (a_i XOR XOR) < a_i，从该堆减去使之变为 a_i^XOR，输出取出量。

💡 类比"把天平调回平衡点：挑一根能降到位的堆，把它变成全局异或后的目标值"：

```python
import sys

def nim_first_move(a):
    x = 0
    for v in a:
        x ^= v
    if x == 0:
        return None
    for i, v in enumerate(a):
        target = v ^ x
        if target < v:
            return i + 1, v - target
    return None

n = int(input())
a = list(map(int, input().split()))
mv = nim_first_move(a)
if mv is None:
    print("lose")
else:
    i, take = mv
    print(i, take)
    a[i - 1] -= take
    print(' '.join(map(str, a)))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.18.5 例 5：威佐夫博弈（POJ 1067）⭐⭐
> **知识点**：威佐夫博弈、黄金分割、必败态｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：两堆石子 a,b（a,b≤10^9），每次可从任一堆取任意多个，或从两堆取相同多个，取完者胜。判断先手胜负。

**思路**
威佐夫必败态是 (⌊kφ⌋, ⌊kφ²⌋)，其中 φ=(1+√5)/2。先标准化 (a,b) 大小序，检查 b-a 是否满足 a==⌊(b-a)φ⌋。

💡 类比"黄金分割的固定点：必败点都排在两条斜线，用黄金比判定是否踩到"：

```python
import math, sys

PHI = (1 + math.sqrt(5)) / 2

for line in sys.stdin:
    a, b = map(int, line.split())
    if a > b:
        a, b = b, a
    k = b - a
    t = int(k * PHI)
    print("%d" % (1 if t != a else 0))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.6 例 6：SG 函数模板（UVA 12293）⭐⭐
> **知识点**：SG 函数、mex、记忆化搜索｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给一堆 n 个石子与一个可取的步数集合 S（如每次取 1、3、4），不能再取者败，判断先手胜负。n≤10^3，多次询问。

**思路**
SG[x] = mex{ SG[x−s] | s∈S }，SG[0]=0，先手必胜当且仅当 SG[n]!=0。mex 是取集合中最小未出现的非负整数。

💡 类比"蜗牛爬阶梯每步固定跳跃：把每个状态编号成它能到达的最小新编号，谁站着不动谁输"：

```python
def sg_build(maxn, steps):
    sg = [0] * (maxn + 1)
    for x in range(1, maxn + 1):
        seen = set()
        for s in steps:
            if x - s >= 0:
                seen.add(sg[x - s])
        g = 0
        while g in seen:
            g += 1
        sg[x] = g
    return sg

steps = [1, 3, 4]
sg = sg_build(20, steps)
for n in ([10, 15, 7]):
    print(n, "Win" if sg[n] != 0 else "Lose")
```
> **复杂度**：O(maxn·|S|) 时间，O(maxn) 空间

---
#### 17.18.7 例 7：取石子可拆堆（HDU 1846）⭐⭐
> **知识点**：拆分博弈、SG 合并、模型转换｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有一堆 n 个石子，每次操作可把一堆分成两堆不同大小的非空堆（或不分），无法操作者败，判断先手胜负。此为"分裂"型 SG 递推。

**思路**
SG[n] 由所有合法拆分 (i, n-i)（i≠n-i）的 SG[i]^SG[n-i] 取 mex。递推构建即可。

💡 类比"分披萨换小玩家：把一块变成两块，双方一起博弈的值是两个小块的异或"：

```python
def split_sg(maxn):
    sg = [0] * (maxn + 1)
    for n in range(1, maxn + 1):
        seen = set()
        for i in range(1, n // 2 + 1):
            j = n - i
            if i != j:
                seen.add(sg[i] ^ sg[j])
            # 也可以保留不拆即到 0
        g = 0
        while g in seen:
            g += 1
        sg[n] = g
    return sg

sg = split_sg(50)
for n in (6, 10, 15):
    print(n, "Win" if sg[n] != 0 else "Lose")
```
> **复杂度**：O(n²) 时间，O(n) 空间

---
#### 17.18.8 例 8：阶梯博弈（HDU 3389）⭐⭐
> **知识点**：阶梯博弈、奇偶层归约｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 级阶梯，每级放若干石子，每次可把某一级的多块石头向下移动若干级（≥1 级），移下楼梯的可落在地面（0 级）即失去。判断先手胜负。

**思路**
阶梯博弈等价于对所有奇数层（含最下为层 1）的石子做 Nim 异或，偶数层的操作总可被后手对称地搬走；只对奇数编号堆异或。

💡 类比"远古信鸽逐级位：真正决定胜负的是奇数号台阶的石子异或，偶数台阶可被对手原样退回来"：

```python
def staircase_win(a):
    x = 0
    # 阶梯从地面向上编号 1..n，异或奇数下标层
    for i in range(len(a)):
        if i % 2 == 0:  # 层级 = i+1，若 i+1 为奇则异或
            pass
    # 层级从1开始，奇层 index 为偶数(0-based)
    for idx, v in enumerate(a):
        if (idx + 1) % 2 == 1:
            x ^= v
    return x != 0

# 例：floor1..floor4 石子数
print("Win" if staircase_win([1, 0, 3, 0]) else "Lose")
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.18.9 例 9：反 Nim 游戏（洛谷 P2596 变式）⭐⭐
> **知识点**：反 Nim、misère 规则、边界判断｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 堆石子，每次取一堆中任意正数个，取最后一个石子者判负（missere）。判断先手胜负。

**思路**
全 1 时奇偶判；否则与标准 Nim 判断一致：存在 >1 的堆时，XOR≠0 必胜；全为 1 时奇数堆必败。

💡 类比"改判规则的大乱斗：当还有大堆好控制数局时仍看异或；只剩单粒堆才考验奇偶"：

```python
def anti_nim_win(a):
    all_one = all(v == 1 for v in a)
    x = 0
    for v in a:
        x ^= v
    if all_one:
        return len(a) % 2 == 0
    return x != 0

for a in ([1, 1, 1], [1, 2, 3], [2, 2], [1, 1, 1, 1]):
    print(a, "Win" if anti_nim_win(a) else "Lose")
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.18.10 例 10：Nim-and（洛谷 P2676 变式）⭐⭐⭐
> **知识点**：Nim 变种、位权博弈、多个游戏合成｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：两堆石子，每次可从一堆取若干或同时从两堆取相同数，取完者胜（近似威佐夫的扩展判定）。实际为"非标准取法"的经典 Nim 变体，判先手胜负。

**思路**
同时取相同数相当于威佐夫博弈；也可归到将两堆差归一维并验收附加维度。用威佐夫必败态判定。

💡 类比"双线取子的特技：一条单取线沿座杯，一条同时扣的双取构成斜线的黄金必败带"：

```python
import math

def win(a, b):
    if a > b:
        a, b = b, a
    k = b - a
    phi = (1 + math.sqrt(5)) / 2
    return int(k * phi) != a

for case in ((2, 1), (3, 5), (4, 7), (8, 4)):
    print(case, "Win" if win(*case) else "Lose")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.11 例 11：树上删边游戏（洛谷 P1099 变式）⭐⭐⭐
> **知识点**：树上删边、仙女数 Sprague-Grundy、递归归约｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一棵带根树，每次操作删去一条边并移除其下方子树，无法删边者败，判断先手胜负。n≤10^5。

**思路**
每棵子树的 SG 等于其所有子节点子树的 SG 加 1 的异或（Green Hackenbush 单根树），即 SG(u)=⊕(SG(v)+1)，根 SG≠0 则先手胜。

💡 类比"剪贪吃虫的每段身体：每剪掉一段就把剩下部分视为独立的局，安全性用异或合并"：

```python
import sys
sys.setrecursionlimit(200000)

def tree_grundy(n, adj):
    sg = [0] * (n + 1)
    def dfs(u, fa):
        x = 0
        for v, _ in adj[u]:
            if v == fa:
                continue
            dfs(v, u)
            x ^= (sg[v] + 1)
        sg[u] = x
    dfs(1, 0)
    return sg[1]

# 树以边权表示，构造示例: 1-2, 1-3
n = 3
adj = {i: [] for i in range(1, n + 1)}
adj[1].extend([(2, 1), (3, 1)])
adj[2].append((1, 1))
adj[3].append((1, 1))
print("Win" if tree_grundy(n, adj) != 0 else "Lose")
```
> **复杂度**：O(n) 时间，O(n) 空间

---
#### 17.18.12 例 12：微型 Green Hackenbush（洛谷 P2199 变式）⭐⭐
> **知识点**：Green Hackenbush、SG 分解、异或组合｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：若干条"绿色"木桩（可无限延伸），每次砍掉一根木桩的某段，若其上方悬空也随之掉落。问多根木桩合成的游戏先手胜负。实际为多棵树 SG 异或。

**思路**
每条独立"串"木桩的 SG 就是它的长度；整个游戏等于各独立系列的 SG 异或，非 0 必胜。

💡 类比"叠叠乐的多根塔：每条塔可以独立砍到任意矮，等价于 Nim 的堆"：

```python
def green_hackenbush_win(lengths):
    x = 0
    for L in lengths:
        x ^= L % 2
    # 更正：每根木桩对应的 SG 即长度（连续整数可走），对长度本身异或更贴近 Nim
    x = 0
    for L in lengths:
        x ^= L
    return x != 0

for lens in ([1, 2, 3], [2, 2, 2], [4, 5, 9]):
    print(lens, "Win" if green_hackenbush_win(lens) else "Lose")
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.18.13 例 13：每次取约数个石子（HDU 2218 变式）⭐⭐
> **知识点**：SG、meg 逐态、约数枚举｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一堆 n 个石子，每次可拿走石子数的某个真因子个数（即拿 k 个，要求 k<n 且 k | n 或 k|剩余变化规则简化），取到 1 个后无合法步则败。判断 n≤10^5 先手胜负。

**思路**
构造可取集合 S=所有真因子（不含自身），SG 递推 mex 每次可达减去的约数。

💡 类比"按约数批量清账：每步只能清一档固定倍额的账，用 mex 标状态"：

```python
def divisor_sg(maxn):
    sg = [0] * (maxn + 1)
    for n in range(1, maxn + 1):
        seen = set()
        for k in range(1, n):
            if n % k == 0:
                seen.add(sg[n - k])
        g = 0
        while g in seen:
            g += 1
        sg[n] = g
    return sg

sg = divisor_sg(100)
for n in (4, 6, 12, 30):
    print(n, "Win" if sg[n] != 0 else "Lose")
```
> **复杂度**：O(maxn·d(maxn)) 时间，O(maxn) 空间

---
#### 17.18.14 例 14：对称拿取必败策略（HDU 1850）⭐⭐
> **知识点**：Nim 变式、构造镜像策略｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一堆 n 枚硬币排成一行，每次取任意连续的一段硬币，两端被取的部分空出，无法再取者败。问先手是否必胜（近似对称博弈思路）。

**思路**
转化为两个区间（左右端）的子游戏做 SG 异或组合，属"分割取子"模型，对称态势位归零判定。

💡 类比"吃饼干条的两端：取中间会让左右成两段独立战斗，各自 SG 异或"：

```python
def strip_game_win(n):
    # 取连续段后剩余为 (0..i) 与 (j..n) 两段，简化为标准 Nim 值
    # 用 SG 递推
    sg = [0] * (n + 1)
    for L in range(1, n + 1):
        seen = set()
        for i in range(L):
            for j in range(i + 1, L + 1):
                left = i
                right = L - (j + 0)
                seen.add(sg[left] ^ sg[L - j])
        g = 0
        while g in seen:
            g += 1
        sg[L] = g
    return sg[n] != 0

for n in (1, 2, 3, 4):
    print(n, "Win" if strip_game_win(n) else "Lose")
```
> **复杂度**：O(n³) 时间，O(n) 空间

---
#### 17.18.15 例 15：取石子必须取奇数个（洛谷 P2046 变式）⭐⭐
> **知识点**：SG、步数集合、必败态模式寻找｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一堆 n 个石子，每次必须取某素数个石子（取值于给定素数集 S），无法取者败。判断先手胜负，n≤10^5。

**思路**
SG 递推：当前 n 的可达态是减去各素数后状态的 SG 集，取 mex。可达位大量为正态现必败模。构造完直接查表。

💡 类比"跳石灰印：能跳的格子由固定素数步决定，逐格数 mex 序列"：

```python
def prime_step_sg(maxn, primes):
    sg = [0] * (maxn + 1)
    for n in range(1, maxn + 1):
        seen = set()
        for p in primes:
            if p <= n:
                seen.add(sg[n - p])
        g = 0
        while g in seen:
            g += 1
        sg[n] = g
    return sg

sg = prime_step_sg(100, [2, 3, 5, 7])
for n in (10, 20, 31, 50):
    print(n, "Win" if sg[n] != 0 else "Lose")
```
> **复杂度**：O(maxn·|P|) 时间，O(maxn) 空间

---
#### 17.18.16 例 16：翻牌 Nim（取不同堆不同数量）（洛谷 P2016 变式）⭐⭐
> **知识点**：混合取法、SG 多项、均衡策略｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：两堆石子，一次操作可从第 1 堆取 a 个或第 2 堆取 b 个或各取 c 个，取完者胜。判断先手胜负（值域较小时枚举成 SG 二维）。

**思路**
构造二维 SG 表 sg[i][j]：mex(斯三种可达(sg[i-a][j], sg[i][j-b], sg[i-c][j-c]))；起点非 0 必先手胜。

💡 类比"双夹棋盘走子：把 can-take 三个方向标出可达位，逐格 mex 填表"：

```python
def two_stack_sg(N, a, b, c):
    sg = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        for j in range(N + 1):
            if i == 0 and j == 0:
                continue
            seen = set()
            if i >= a:
                seen.add(sg[i - a][j])
            if j >= b:
                seen.add(sg[i][j - b])
            if i >= c and j >= c:
                seen.add(sg[i - c][j - c])
            g = 0
            while g in seen:
                g += 1
            sg[i][j] = g
    return sg

sg = two_stack_sg(20, 1, 2, 3)
print("sg[5][5]=", sg[5][5], "Win" if sg[5][5] != 0 else "Lose")
```
> **复杂度**：O(N²) 时间，O(N²) 空间

---
#### 17.18.17 例 17：取火柴指定组（HDU 2176）⭐⭐
> **知识点**：Nim、取法输出构造、异或调整｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 堆火柴，每次取一堆中任意根，最后取者胜。若先手必胜，输出"有若干可行第一步选择清单"格式。a_i≤10^9。

**思路**
总 XOR 非 0 时，枚举每堆，若 (a_i^XOR) < a_i 则该堆可取 a_i - (a_i^XOR) 根，即为合法第一步。

💡 类比"找那根能掰动总异的平衡杆：对所有堆挑出能收敛到全局 XOR 的那一根"：

```python
def nim_first_moves(a):
    x = 0
    for v in a:
        x ^= v
    if x == 0:
        return []
    moves = []
    for i, v in enumerate(a):
        t = v ^ x
        if t < v:
            moves.append((i, v - t))
    return moves

a = [7, 5, 6]
for idx, take in nim_first_moves(a):
    print(f"取第{idx+1}堆 {take} 个")
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.18.18 例 18：两人分果按取尽必败（洛谷 P1246 变式）⭐⭐
> **知识点**：非 Nim 取法、孙博弈步、find 规律｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一堆 n 个，每次取数量必须是两人共取的上一步取数的 1 到 2 倍之间（首步可取 1..n-1），取到最后一个负（也可按规则重述）。判断先手胜负 n≤10^6。

**思路**
按"取法比例递增"的经典博弈（1~2 倍），必败态出现于斐波那契数位；用斐波那契数列判定当前 n 是否为斐波那契数。

💡 类比"斐波那契链的缺口：取数受上一轮倍率锁定，能封死到斐波那契位就控局"：

```python
def fib_position_win(n):
    a, b = 1, 1
    while b < n:
        a, b = b, a + b
    return b != n   # 若 n 是斐波那契数则必败

for n in (2, 3, 5, 8, 6, 10):
    print(n, "Win" if fib_position_win(n) else "Lose")
```
> **复杂度**：O(log n) 时间，O(1) 空间

---
#### 17.18.19 例 19：转盘偶数步走（洛谷 P1603 变式）⭐⭐
> **知识点**：环形走子、模周期、SG 对环退化简述｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：在长度 n 的环形转盘上有一颗棋子，每步必须顺时针走 1 到 3 格，走过起点后无法继续时步…实际为退化成线性到达终点的步长博弈，判先手胜负。

**思路**
线性化：终点前第 i 格所需步长集合 {1,2,3}，退化为取 1..3 的简单博弈，n%4==0 时先手必败。

💡 类比"四拍进行曲：只要能补满四拍就永远别让对方走到最后一步"：

```python
def circle_step_win(n):
    return n % 4 != 0

for n in (1, 4, 7, 8, 11):
    print(n, "Win" if circle_step_win(n) else "Lose")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.20 例 20：分区 Nim 异或（洛谷 P2235 变式）⭐⭐
> **知识点**：Nim、异或性质、分组策略｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 堆石子分两组进行 Nim，先手可任意操作一组，组内两堆同时受影响的特殊取法，需判断多个独立 Nim 组合并（异或）后是否必胜。n≤10^5。

**思路**
将每组视为独立 Nim，整个游戏 = 各独立游戏的 SG 异或；每独立戏若为 Nim 其 SG 即组内异或，再全局异或判定。

💡 类比"两个副战场共定全局胜负：每战场的异或代表其状态值，再整体异或看归零与否"：

```python
def group_nim_win(groups):
    x = 0
    for g in groups:
        sg = 0
        for v in g:
            sg ^= v
        x ^= sg
    return x != 0

groups = [[1, 2, 3], [4, 5], [6]]
print("Win" if group_nim_win(groups) else "Lose")
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.18.21 例 21：多 Nim 异或计数（HDU 2187 变式）⭐⭐
> **知识点**：Nim、异或策略计数、规律统计｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：若干堆石子，断言先手必胜的初始异或条件本质，题目要求统计有多少个"先手必胜"的不同初始之一判定。简化为给定堆验证异或非零。

**思路**
逐堆异或判定非零即先手胜，与单 Nim 相同，注意数据规模与 long。

💡 类比"逐个扫进异或寄存器：任何一堆改变都能翻转整体胜负天平"：

```python
def any_multi_win(moves_sets):
    # 演示：判断若干组独立子局的组合
    x = 0
    for s in moves_sets:
        sx = 0
        for v in s:
            sx ^= v
        x ^= sx
    return x != 0

print([ (s, "Win" if any_multi_win(s) else "Lose")
        for s in [ [ [1,1],[1,2] ], [ [2,3],[3,4] ] ] ])
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.18.22 例 22：翻硬币最后反面（洛谷 P2609 变式）⭐⭐
> **知识点**：SG、取序列、镜像 NIM 变体｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一排 n 枚硬币全正面，每次可取任意一枚并翻转它右边的所有硬币，最后全部反面者胜。判断先手胜负（退化为经典取子：实际等价于每次取 1.. 任意个）。

**思路**
这类"翻转右侧"游戏的 SG 常与堆取 Nim 等价，n%3 依据可推——本场用标准 Nim+S 计算：SG 即 n 的模式为大小。

💡 类比"多米诺连锁推倒：取最右有效反转一片，剩下问题规模递减成新战斗"：

```python
def coin_flip_win(n):
    # 等价于每次取走任意个, 模型 = Nim 单堆
    return n != 0

for n in (0, 1, 5, 8):
    print(n, "Win" if coin_flip_win(n) else "Lose")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.23 例 23：两人同条件必败总数（UVA 10540）⭐⭐
> **知识点**：博弈、状态对称、Str大策略｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：两堆数量 (a,b) 的石头，仿威佐夫但只允许取走一堆的若干或同时某规则，判定先手，但本题为"拿任意堆或两堆同量"完全威佐夫，直接套黄金比。

**思路**
威佐夫判定：b-a 与 a 满足整部公式即可。

💡 类比"黄金斜线的陷阱位：必败态聚在两条间隔黄金比的直线上"：

```python
import math

def wythoff(a, b):
    if a > b:
        a, b = b, a
    k = b - a
    phi = (1 + math.sqrt(5)) / 2
    return int(k * phi) == a

for case in ((3, 5), (4, 7), (1, 2), (6, 10)):
    print(case, "Lose" if wythoff(*case) else "Win")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.24 例 24：取石子只能取平方数（洛谷 P2625 变式）⭐⭐
> **知识点**：SG、平方数步、必败态规律搜索｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一堆 n 个石子，每次取 1、4、9、16……（某个可行平方数）个，取完者胜。判断 n≤10^5 先手胜负。

**思路**
SG 递推计算而后查 SG[k]!=0 即先手胜。递推步骤简单。

💡 类比"方块跳远棋盘：能跳的格子是平方步长，逐格标 mex"：

```python
def square_step_sg(maxn):
    sq = [i * i for i in range(1, int(maxn ** 0.5) + 1)]
    sg = [0] * (maxn + 1)
    for n in range(1, maxn + 1):
        seen = set()
        for s in sq:
            if s <= n:
                seen.add(sg[n - s])
        g = 0
        while g in seen:
            g += 1
        sg[n] = g
    return sg

sg = square_step_sg(1000)
for n in (10, 25, 64, 100):
    print(n, "Win" if sg[n] != 0 else "Lose")
```
> **复杂度**：O(maxn·√maxn) 时间，O(maxn) 空间

---
#### 17.18.25 例 25：两堆威佐夫变形（HDU 2633 变式）⭐⭐
> **知识点**：威佐夫、黄金比例、判定初态｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：两堆 (a,b)，一次可任意取第一堆、第二堆或两堆同时取相等的正整数个。判定先手胜负 (a,b≤10^9)。

**思路**
威佐夫必败态判定，图解黄金斜线。已在 18.18.23 展示，此处换输入读数输出，多测试。

💡 类比"双杆天平必败带定位：差值 φ 倍对应的一端恰好对上整数即踩必败"：

```python
import math, sys

phi = (1 + math.sqrt(5)) / 2
for line in sys.stdin:
    a, b = map(int, line.split())
    if a == 0 and b == 0:
        break
    if a > b:
        a, b = b, a
    k = b - a
    print("0" if int(k * phi) == a else "1")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.26 例 26：点一招涂满棋盘（洛谷 P2026 变式）⭐⭐
> **知识点**：格点游戏、对称策略、配色必胜｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：棋盘上有 (x,y) 个格子，每次可涂整行或整列未涂的格子，最后无格可涂者败。判断先手（行列数对称时可中间对称应付）必胜条件。

**思路**
等价为取行/列两个堆的取一操作，即 Nim 两堆（行 n、列 m），先手胜当且仅当 n != m（XOR!=0），相等则后手镜像必胜。

💡 类比"对称镜像复印术：对手涂一行我就涂对称一行，保证全局对仗到没格为止"：

```python
def board_paint_win(n, m):
    return (n ^ m) != 0

for case in ((2, 2), (2, 3), (3, 5), (5, 5)):
    print(case, "Win" if board_paint_win(*case) else "Lose")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.27 例 27：拆分两堆必须不同（洛谷 P2091 变式）⭐⭐
> **知识点**：拆分游戏、SG、size 递归归纳｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一堆 n 个石子可拆成 a,b（a≠b，均非空）两堆，也可以直接取任意个到消失来转换玩法，标准"拆成一黑一白"分裂游戏，判先手胜负。

**思路**
n 的值关键：能拆的都能等价变化，SG[n] 由所有 (a,b) a≠b 的 sg[a]^sg[b] 定 mex。

💡 类比"项链两头开链拆环：拆成两个锁环的异或决定当前编号"：

```python
def split_diff_sg(maxn):
    sg = [0] * (maxn + 1)
    for n in range(1, maxn + 1):
        seen = set()
        for a in range(1, n):
            b = n - a
            if a == b:
                continue
            seen.add(sg[a] ^ sg[b])
        g = 0
        while g in seen:
            g += 1
        sg[n] = g
    return sg

sg = split_diff_sg(60)
for n in (5, 8, 12, 30):
    print(n, "Win" if sg[n] != 0 else "Lose")
```
> **复杂度**：O(n²) 时间，O(n) 空间

---
#### 17.18.28 例 28：三分支条件取（洛谷 P2240 变式）⭐⭐
> **知识点**：博弈决策、状态机、SG 综合｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定三堆石子，规定每步只能对指定某堆按限定数量操作（对应 SG 表的组合全局）。当前局面 (a,b,c) 问先手胜记 XOR 全局判。

**思路**
每堆规则给出的值若限定取整堆，则为 Nim 三堆，判定 XOR 非 0 必胜；若限定步集合则各自 SG 异或。

💡 类比"三乐器合奏独立旋律：三个子局的 SG 异或成整体音符"：

```python
def tri_nim_win(a, b, c):
    return (a ^ b ^ c) != 0

for case in ((1, 2, 3), (2, 3, 4), (1, 1, 1), (3, 5, 6)):
    print(case, "Win" if tri_nim_win(*case) else "Lose")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.29 例 29：井字棋对称策略（洛谷 P2211 变式）⭐⭐
> **知识点**：策略博弈、平局防守、镜像归约｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：3×3 棋盘两人轮流落子，先连三子胜，否则平局；判断给定棋面下当前玩家是否存在必胜策略（极小化递归或直接九格搜索）。棋盘最多 9 格。

**思路**
用极小极大（minimax）递归对未落子格搜索，评估胜负平并取最优，后手用极大保持对称可防守。

💡 类比"守卫占位的双人围棋剪枝：每个空格都试一手，给对手最坏结果选最佳"：

```python
def winner(b):
    for line in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
        a0,a1,a2 = line
        if b[a0] and b[a0]==b[a1]==b[a2]:
            return b[a0]
    if all(b):
        return "?"
    return None

def minimax(b, turn):
    w = winner(b)
    if w in ('X','O'):
        return 1 if w=='X' else -1
    if w == '?':
        return 0
    best = -10 if turn=='X' else 10
    for i in range(9):
        if not b[i]:
            b[i]=turn
            v = minimax(b, 'O' if turn=='X' else 'X')
            b[i]=''
            if turn=='X':
                best=max(best,v)
            else:
                best=min(best,v)
    return best

b = ['X','','O','','X','','','','O']
print("X可胜?" if minimax(b,'X')>0 else "不可胜")
```
> **复杂度**：O(9!) 最坏时间，O(9) 空间

---
#### 17.18.30 例 30：多石不可均分（洛谷 P2331 变式）⭐⭐
> **知识点**：拆分限制、SG 推导、成对固定招式｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一堆 n 个，规则为要么取走全部并令对方败（取完者败——misère 化），或是把一堆拆成相差不小于 2 的两堆继续，判先手胜负。

**思路**
拆分限制使 SG 序列呈现规律：属于"Bob 必胜"的 n 恰为 2 的幂类约束处收集，直接打表发现必败 n 为满足某整除条件值，递推构建全套。

💡 类比"基因分裂必须拉开差距：能拆开的数才有退路，恰好的平衡位成为死局"：

```python
def diff_split_sg(maxn):
    sg=[0]*(maxn+1)
    for n in range(1,maxn+1):
        seen=set()
        for a in range(1,n):
            b=n-a
            if a!=b and abs(a-b)>=2:
                seen.add(sg[a]^sg[b])
        g=0
        while g in seen:
            g+=1
        sg[n]=g
    return sg

sg=diff_split_sg(60)
for n in (5,9,16,31,50):
    print(n,"Win" if sg[n]!=0 else "Lose")
```
> **复杂度**：O(n²) 时间，O(n) 空间

---
#### 17.18.31 例 31：金字塔堆 Nim（洛谷 P2092 变式）⭐⭐
> **知识点**：阶梯 Nim 变种、单堆分层、奇数层异或｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：石子堆成金字塔状，每层一堆，操作把某一层若干粒移到下一层，最底层移出即消失，判先手胜负。

**思路**
阶梯博弈：只异或奇数层堆的石子（从下往上计数），偶数层可镜像抵消。

💡 类比"搬货楼梯：只把关心的奇数层码数异或即可知天平方向"：

```python
def pyramid_win(levels):
    # levels[0] 是最底层
    x = 0
    for i in range(0, len(levels)):
        if (i + 1) % 2 == 1:
            x ^= levels[i]
    return x != 0

print("Win" if pyramid_win([2, 1, 3, 0, 4]) else "Lose")
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.18.32 例 32：DAG 有向图游戏结局（洛谷 P2387 变式）⭐⭐
> **知识点**：SG 泛化、DAG 博弈、拓扑与记忆化｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一个 DAG（节点数 n≤10^5，边数 m≤2·10^5），棋子初始在起点，双方轮流沿有向边走，无法移动者败。判断先手胜负。

**思路**
在 DAG 上自底向上（逆拓扑）计算各节点 SG 值：某点 SG = mex{ 后继点 SG }，先手胜当且仅当起点 SG≠0。

💡 类比"无人机的航线节点：每个停机坪能不能赢取决于它能到达哪些更出口的点，反着标号"：

```python
import sys
sys.setrecursionlimit(300000)

def dag_game(n, g, start=1):
    sg = [-1] * (n + 1)
    def dfs(u):
        if sg[u] != -1:
            return sg[u]
        seen = set()
        for v in g[u]:
            seen.add(dfs(v))
        gv = 0
        while gv in seen:
            gv += 1
        sg[u] = gv
        return gv
    return dfs(start) != 0

n = 5
g = {1: [2, 3], 2: [4], 3: [4], 4: [5], 5: []}
print("Win" if dag_game(n, g, 1) else "Lose")
```
> **复杂度**：O(n+m) 时间，O(n+m) 空间

---
#### 17.18.33 例 33：多堆取任意（洛谷 P2196 变式）⭐
> **知识点**：Nim 基础、异或判断｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 堆石子，每次从任意一个非空堆中取任意正整数个，最后取完者胜。判断先手胜负。n≤10^5，a_i≤10^9。

**思路**
对全部堆做按位异或，结果为 0 后手胜，否则先手胜。

💡 类比"账本凑零：每堆石子二进制异或为零就是陷阱，谁把异或翻成零谁领跑"：

```python
def nim_win(a):
    x = 0
    for v in a:
        x ^= v
    return x != 0

for a in ([1,1,2,2], [1,2,3], [3,4,5]):
    print(a, "Win" if nim_win(a) else "Lose")
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.18.34 例 34：阶梯石子的奇层归约（洛谷 P2238 变式）⭐⭐
> **知识点**：阶梯博弈、奇偶层、镜像策略｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 级台阶，第 i 级有 a_i 个石子，每次可将某一级上的若干石子向下移（可一次下多级），移到地面即不计，无法再移者败。判断先手胜负。

**思路**
只对奇数编号台阶（1-base）的石子数异或：XOR≠0 先手胜；偶数层总可被后手对称搬回。

💡 类比"遥控搬运机器人：真正决定胜负的是奇数层的棋子异或，偶数层是对手能原样退回的垫脚石"：

```python
def staircase_win(a):
    x = 0
    for idx, v in enumerate(a):
        if (idx + 1) % 2 == 1:
            x ^= v
    return x != 0

for a in ([3,2,1], [1,0,1,0], [1,3,0,0]):
    print(a, "Win" if staircase_win(a) else "Lose")
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.18.35 例 35：只能取指定奇数/偶数规则（洛谷 P2340 变式）⭐⭐
> **知识点**：SG、取法限制、mex 模式｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一堆 n 个石子，每次要么取 1 个，要么取当前堆一半向上取整个（说白取 n//2+1 若为奇才允许……简化）——本题给定可取集合，mex 判定先手。n≤10^5。

**思路**
按给定可取集合递推 SG，直到 n。

💡 类比"限定规矩的跳房子：能跳的距离被框死，从 0 开始逐格标注 mex"：

```python
def sg_with_steps(maxn, steps):
    sg = [0] * (maxn + 1)
    for n in range(1, maxn + 1):
        seen = set()
        for s in steps:
            if s <= n:
                seen.add(sg[n - s])
        g = 0
        while g in seen:
            g += 1
        sg[n] = g
    return sg

sg = sg_with_steps(200, [1, 3, 3, 5])  # 去重由 set 保证
for n in (5, 9, 30, 100):
    print(n, "Win" if sg[n] != 0 else "Lose")
```
> **复杂度**：O(n·|S|) 时间，O(n) 空间

---
#### 17.18.36 例 36：克莱因瓶翻牌（洛谷 P2412 变式）⭐⭐⭐
> **知识点**：周期必败态、规律归纳、SG 观察｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一行 n 颗棋，每次可拿走任意相邻的 1 或 2 颗（两端视为相邻的化简处理），无法拿者败，判断先手胜负。n≤10^9。

**思路**
由于可"拿相邻两颗"，当 n≡1(mod 3) 时存在镜像对策，必败态出现在 n%3==1 类，直接在周期上判定。

💡 类比"整排糖果按三节奏拿：以三个为一组制造镜像，剩下的一格放飞对手"：

```python
def adjacent_pair_win(n):
    return n % 3 != 1

for n in range(1, 13):
    print(n, "Win" if adjacent_pair_win(n) else "Lose")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.37 例 37：翻硬币全反标记（UVA 10209 变式）⭐⭐
> **知识点**：对称博弈、中心对称策略、必胜铺陈｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：m×n 格棋盘，两人轮流把一块完整的未覆盖子矩形线覆盖（覆盖任意矩形），最后无空位者败，判断先手。m,n≤50。

**思路**
横纵可独立取，等价 Nim 两堆：先手胜当且仅当 m!=n（异或不 0），m==n 时后手取中心对称矩形必胜。

💡 类比"对称折叠地图涂色：对手涂哪块，我就在中心对称处涂一样形状，保证棋局镜像到底"：

```python
def rect_cover_win(m, n):
    return (m ^ n) != 0

for case in ((3, 3), (3, 4), (5, 7), (6, 6)):
    print(case, "Win" if rect_cover_win(*case) else "Lose")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.38 例 38：两堆等量与威佐夫（HDU 2177）⭐⭐
> **知识点**：威佐夫、获取必败判定、黄金比推导｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：两堆石子 (a,b)，一次可从任一取任意个或从两堆取相同个数。判定先手胜负，a,b≤10^9。多组测试至 0 0。

**思路**
威佐夫必败态判定：小序整理后用黄金分割比值，若 (b-a)·φ 整数部分等于 a 则后手胜。

💡 类比"双轴黄金天平：把两堆差乘上黄金比对回小堆，能对上必然输"：

```python
import math, sys

phi = (1 + math.sqrt(5)) / 2
out = []
for line in sys.stdin:
    a, b = map(int, line.split())
    if a == 0 and b == 0:
        break
    if a > b:
        a, b = b, a
    k = b - a
    out.append("先手胜" if int(k * phi) != a else "先手负")
print("\n".join(out))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.18.39 例 39：多堆限制步集合组合（洛谷 P2453 变式）⭐⭐
> **知识点**：多独立 SG、异或叠合、组合博弈总和｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：k 堆石子，各自有不同可取集合，每步在一堆上按其规则取，最后取到无合法步者败。判断全体先手胜负。各堆规模≤100。

**思路**
每堆独立算 SG，再全体异或，不为 0 则先手胜。用 mex 逐堆递推。

💡 类比"多条赛道各自限速：先把每条赛道的 SG 值算出来，再全部异或定全局胜负"：

```python
def sg_with(steps, maxn):
    sg = [0] * (maxn + 1)
    for n in range(1, maxn + 1):
        seen = set()
        for s in steps:
            if s <= n:
                seen.add(sg[n - s])
        g = 0
        while g in seen:
            g += 1
        sg[n] = g
    return sg

def total_win(piles):
    x = 0
    for n, steps in piles:
        sg = sg_with(steps, n)
        x ^= sg[n]
    return x != 0

piles = [(7, [1,2,3]), (6, [1,4,5])]
print("Win" if total_win(piles) else "Lose")
```
> **复杂度**：O(k·n·|S|) 时间，O(maxn) 空间

---
#### 17.18.40 例 40：综合归约的混合博弈（洛谷 P2463 变式）⭐⭐⭐
> **知识点**：博弈模型归约、SG 综合、异或汇总｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一个混合局面由几种标准子游戏拼成：一堆巴什（可取≤m）、一堆纯 Nim、两堆威佐夫。分别计算各子状态值后整体异或，判先手胜。数值较大。

**思路**
巴什子局 SG 为 n%(m+1)；Nim 堆 SG 为 a；威佐夫子局（两堆）SG 用黄金比必败判定贡献 0/1（简化为其判定结果）。各子局值异或，非 0 胜。

💡 类比"混合联盟棋赛：三种玩法各自结算成一个数值，最后统一异或判定总冠军归属"：

```python
import math

phi = (1 + math.sqrt(5)) / 2

def bash_sg(n, m):
    return n % (m + 1)

def wythoff_sg(a, b):
    if a > b:
        a, b = b, a
    k = b - a
    return 0 if int(k * phi) == a else 1

def mixed_win(bash, nim_piles, wythoff):
    x = 0
    x ^= bash_sg(*bash)
    for v in nim_piles:
        x ^= v
    x ^= wythoff_sg(*wythoff)
    return x != 0

print("Win" if mixed_win((10, 3), [2, 5], (3, 5)) else "Lose")
```
> **复杂度**：O(n) 时间，O(1) 空间

---

### 17.19 计算几何

#### 17.19.1 例 1：欧氏距离计算（洛谷 P3958 变式）⭐
> **知识点**：距离公式、浮点精度｜**难度**：⭐｜**类型****：ACM/竞赛
> **题目描述**：给平面两点 (x1,y1)、(x2,y2)，输出两点欧氏距离。坐标及结果均可能是实数，输出保留 2 位小数。多组输入。

**思路**
用 sqrt((x1-x2)²+(y1-y2)²) 计算，注意格式化输出与浮点精度。

💡 类比"最短直线的尺量：横纵坐标的差平方再开跟，就是两点直线距离"：

```python
import sys, math

for line in sys.stdin:
    x1, y1, x2, y2 = map(float, line.split())
    d = math.hypot(x1 - x2, y1 - y2)
    print(f"{d:.2f}")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.2 例 2：曼哈顿距离与切比雪夫距离（HDU 2421 变式）⭐
> **知识点**：曼哈顿距离、切比雪夫距离、坐标变换｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给平面两点，分别输出曼哈顿距离 |dx|+|dy| 与切比雪夫距离 max(|dx|,|dy|)。多组输入。

**思路**
直接按公式算，曼哈顿为横纵差绝对值之和，切比雪夫为二者最大值。

💡 类比"城市街区直角走 vs 棋盘王走斜线一步到位"：

```python
import sys

for line in sys.stdin:
    x1, y1, x2, y2 = map(int, line.split())
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    print(dx + dy, max(dx, dy))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.3 例 3：二维向量叉积（洛谷 P1193 变式）⭐
> **知识点**：叉积、叉积符号意义｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给两个从原点出发的向量 (xa,ya)、(xb,yb)，输出叉积 xa·yb - ya·xb 及其符号（正/零/负，表示 b 在 a 的逆时针/共线/顺时针方向）。

**思路**
叉积 cross = xa*yb - ya*xb，符号判断两向量相对转向。

💡 类比"皮带轮转向判断：叉积为正就是逆时针拨动，为零等于一条直线"：

```python
def cross(xa, ya, xb, yb):
    return xa * yb - ya * xb

for v in [(1,0,0,1), (1,0,2,0), (2,1,-1,2)]:
    xa, ya, xb, yb = v
    c = cross(xa, ya, xb, yb)
    print(c, "CCW" if c > 0 else ("CW" if c < 0 else "COLINE"))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.4 例 4：三点共线性判定（HDU 2274 变式）⭐
> **知识点**：叉积、共线判定｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给三点 A、B、C，判断是否共线。坐标整数，输出 YES/NO。多组输入。

**思路**
三点共线当且仅当向量 AB 与 AC 的叉积为 0（面积为零）。

💡 类比"三种子地标是否在一条直线上：用前进方向和旁向能否画成一个零面积三角形判断"：

```python
import sys

for line in sys.stdin:
    ax, ay, bx, by, cx, cy = map(int, line.split())
    c = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    print("YES" if c == 0 else "NO")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.5 例 5：中点与对称点（洛谷 P7071 变式）⭐
> **知识点**：中点公式、对称点、向量｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给两点 A(x1,y1)、B(x2,y2)，输出中点 M，以及 A 关于 B 对称的点 A'。实数输出 2 位小数。

**思路**
中点即 (A+B)/2；关于 B 对称点为 2B - A。

💡 类比"钟摆中心与镜像翻转：中线取平均，对称则把 B 当镜面翻到另一侧"：

```python
def mid(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

def reflect_about(a, b):
    return (2 * b[0] - a[0], 2 * b[1] - a[1])

A = (1.0, 3.0)
B = (4.0, -1.0)
M = mid(A, B)
R = reflect_about(A, B)
print(f"M={M[0]:.2f},{M[1]:.2f} R={R[0]:.2f},{R[1]:.2f}")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.6 例 6：判断点在圆内（HDU 2096 变式）⭐
> **知识点**：距离与半径比较、浮点容差｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给圆心 (cx,cy)、半径 r 与点 P，判断点在圆内（含边界）还是圆外。输出 IN/OUT。多组输入。

**思路**
比较点到圆心距离平方与 r²（用平方避免开方），小于等于为圆内。

💡 类比"画的圈内站人：点到圆心的绳长没超过半径就算你画进去了"：

```python
import sys

for line in sys.stdin:
    cx, cy, r, x, y = map(float, line.split())
    if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + 1e-9:
        print("IN")
    else:
        print("OUT")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.7 例 7：向量点积与夹角（UVA 152）⭐
> **知识点**：点积、夹角、向量投影｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给两向量 (x1,y1)、(x2,y2)，输出点积，以及两向量夹角余弦（模长可能的归一）。输出点积整数与余弦保留 2 位。

**思路**
点积 = x1x2+y1y2；余弦 = 点积/(|a||b|)，注意两向量皆非零且浮点。

💡 类比"投影打灯两束线：点积反应同向程度，除以模长归一成夹角余弦"：

```python
import math

def dot(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2

def cos_angle(x1, y1, x2, y2):
    la = math.hypot(x1, y1)
    lb = math.hypot(x2, y2)
    if la == 0 or lb == 0:
        return 1.0
    return dot(x1, y1, x2, y2) / (la * lb)

for v in [(1,0,0,1), (3,4,4,3), (2,0, -3,0)]:
    x1,y1,x2,y2 = v
    print("dot=", dot(x1,y1,x2,y2), "cos=", round(cos_angle(x1,y1,x2,y2),2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.8 例 8：多边形周长（HDU 2158 变式）⭐
> **知识点**：周长、相邻距离累加、封闭性｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给一个多边形 n 个顶点（按顺序），求其周长。n≤100，坐标整数。

**思路**
依次把相邻顶点距离累加，最后补上末点到首点的闭合边。

💡 类比"沿着篱笆走一圈量长度：每段篱笆长度相加，别忘首尾相连的一段"：

```python
import math

def perimeter(P):
    n = len(P)
    s = 0.0
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        s += math.hypot(a[0] - b[0], a[1] - b[1])
    return s

P = [(0,0), (3,0), (3,4), (0,4)]
print(round(perimeter(P), 2))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.19.9 例 9：线段中点外的点定比分点（HDU 2039 变式）⭐
> **知识点**：定比分点、向量伸缩｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：线段 AB 上有一点 P 满足 AP:PB = m:n（m,n 正整数），求 P 坐标。输出 2 位小数。

**思路**
P = (n·A + m·B)/(m+n)，即按比例插值。

💡 类比"糕点上 m:n 切分：权重反着加权平均两端的坐标"：

```python
def ratio_point(A, B, m, n):
    x = (n * A[0] + m * B[0]) / (m + n)
    y = (n * A[1] + m * B[1]) / (m + n)
    return x, y

A = (1.0, 1.0)
B = (4.0, 5.0)
x, y = ratio_point(A, B, 1, 2)
print(f"{x:.2f} {y:.2f}")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.10 例 10：点到直线的距离（POJ 2398 变式）⭐⭐
> **知识点**：点到直线距离、叉积几何意义｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给直线过两点 P1(x1,y1)、P2(x2,y2) 与点 P，求点 P 到直线（或线段）的垂直距离。输出 2 位小数。

**思路**
叉积面积除以底边长：d = |cross(P2-P1, P-P1)| / |P2-P1|，若要求线段距离再夹最近垂足投影范围。

💡 类比"线杆垂下的影子长度：平行四边形的面积除以底边，就是到直线的高度"：

```python
import math

def pt_line_dist(P1, P2, P):
    dx = P2[0] - P1[0]
    dy = P2[1] - P1[1]
    base = math.hypot(dx, dy)
    if base == 0:
        return math.hypot(P[0]-P1[0], P[1]-P1[1])
    c = dx * (P[1] - P1[1]) - dy * (P[0] - P1[0])
    return abs(c) / base

print(round(pt_line_dist((0,0),(3,0),(1,4)), 2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.11 例 11：点到线段的最短距离（洛谷 P1995 变式）⭐⭐
> **知识点**：点线距离、投影、长度比较｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给线段 AB 与点 P，求点 P 到线段（不是无穷直线）的最短距离。坐标整数，输出 2 位小数。

**思路**
先用点积判断垂足是否落在线段内部；在内则用垂距，在外则取到 A、B 的较近端点距离。

💡 类比"找离路灯最近的护栏点：垂足在栏内就算栏上距离，出了栏就取两端点到灯较近的那个"：

```python
import math

def pt_seg_dist(A, B, P):
    ax, ay = A
    bx, by = B
    px, py = P
    vx, vy = bx - ax, by - ay
    wx, wy = px - ax, py - ay
    c1 = vx * wx + vy * wy
    if c1 <= 0:
        return math.hypot(px - ax, py - ay)
    c2 = vx * vx + vy * vy
    if c1 >= c2:
        return math.hypot(px - bx, py - by)
    b = c1 / c2
    proj = (ax + b * vx, ay + b * vy)
    return math.hypot(px - proj[0], py - proj[1])

print(round(pt_seg_dist((0,0),(4,0),(2,3)), 2))
print(round(pt_seg_dist((0,0),(4,0),(6,0)), 2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.12 例 12：两矩形交叠面积（洛谷 P1537 变式）⭐
> **知识点**：矩形交、区间交、并集面积｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给两个轴对齐矩形（各以左下、右上角表示），求交叠矩形面积；无交叠输出 0。坐标整数。

**思路**
交叠矩形的左右界=两个左界取大、右界取小，上下同理，交宽高为正才有交叠，面积=宽×高，另求并集面积=两面积-交叠。

💡 类比"两块床单重叠铺床：看横和竖各自有没有 正 的重叠区间，把它们相乘"：

```python
def rect_intersect(r1, r2):
    # r = (xmin,ymin,xmax,ymax)
    xmin = max(r1[0], r2[0])
    xmax = min(r1[2], r2[2])
    ymin = max(r1[1], r2[1])
    ymax = min(r1[3], r2[3])
    if xmin >= xmax or ymin >= ymax:
        return 0
    return (xmax - xmin) * (ymax - ymin)

r1 = (0,0,4,3)
r2 = (2,1,6,5)
print(rect_intersect(r1, r2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.13 例 13：判断点在轴对齐矩形内（HDU 2133 变式）⭐
> **知识点**：区间包含、边界容差｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给轴对齐矩形左下、右上角与点 P，判断点是否落在矩形内（含边界）。输出 IN/OUT。多组输入。

**思路**
检查 xmin≤x≤xmax 且 ymin≤y≤ymax，含等号边界。

💡 类比"套框子量照片：横纵都在框的刻度之间就算装得下"：

```python
def in_rect(P, xmin, ymin, xmax, ymax):
    x, y = P
    return xmin <= x <= xmax and ymin <= y <= ymax

tests = [((2,2),0,0,4,4), ((5,1),0,0,4,4), ((4,4),0,0,4,4)]
for P,x1,y1,x2,y2 in tests:
    print(P, "IN" if in_rect(P,x1,y1,x2,y2) else "OUT")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.14 例 14：向量旋转（洛谷 P2306 变式）⭐⭐
> **知识点**：旋转矩阵、三角恒等、复数坐标｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：把向量 (x,y) 绕原点逆时针旋转 θ 度，输出旋转后的向量，保留 2 位小数。

**思路**
旋转变换：(x',y') = (x·cosθ − y·sinθ, x·sinθ + y·cosθ)，注意角度转弧度。

💡 类比"方向盘转一轮：横纵坐标按旋转矩阵重新分配，余弦带正转、正弦跨象限"：

```python
import math

def rotate(x, y, deg):
    rad = math.radians(deg)
    c, s = math.cos(rad), math.sin(rad)
    return (x * c - y * s, x * s + y * c)

x, y = 1.0, 0.0
nx, ny = rotate(x, y, 90)
print(f"{nx:.2f} {ny:.2f}")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.15 例 15：三点外接圆圆心（外心）（HDU 2078 变式）⭐⭐
> **知识点**：外心、三角形外接圆、垂径定理方程组｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给不共线三点 A、B、C，求它们外接圆的圆心坐标与半径，输出 2 位小数。

**思路**
外心是两边中垂线的交点。由 (x-ax)²+(y-ay)² 相等拆出两个线性方程，解出 (ox,oy)，半径即到任一顶点距离。

💡 类比"圆形转盘的三根支柱定心：取两条边中垂线相交即圆心，半径量任一支柱长度"：

```python
def circumcenter(A, B, C):
    (ax, ay), (bx, by), (cx, cy) = A, B, C
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if d == 0:
        return None, 0
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    import math
    r = math.hypot(ux - ax, uy - ay)
    return (ux, uy), r

O, r = circumcenter((0,0),(2,0),(0,2))
print("O=", O, "r=", round(r, 2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.16 例 16：三角形面积（POJ 1571）⭐
> **知识点**：海伦公式、叉积面积、浮点｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给三角形三点，求其面积，输出 2 位小数。坐标可为整数或实数。

**思路**
用体积叉积面积 = |cross(B-A, C-A)|/2 最稳，避免海伦开方误差。

💡 类比"斜放的三角旗面积：平行四边形面积折半就是三角形那块布料"：

```python
def tri_area(A, B, C):
    c = (B[0]-A[0])*(C[1]-A[1]) - (B[1]-A[1])*(C[0]-A[0])
    return abs(c) / 2

print(round(tri_area((0,0),(4,0),(0,3)), 2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.17 例 17：多边形面积（鞋带公式）（HDU 2035 变式）⭐⭐
> **知识点**：鞋带公式、有向面积、环绕数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给按顺序排列的多边形 n 个顶点，求其面积（绝对值的两倍也可以按通常面积），输出整数或 2 位小数。顶点顺序任意（凸凹皆可）。n≤10^4。

**思路**
鞋带公式 S = ½·|Σ (x_i·y_{i+1} − x_{i+1}·y_i)|，闭合成环计算，对任意简单多边形成立。

💡 类比"鞋带绕多边形一圈：把相邻顶点的叉积交叉累加再除以 2，正负相抵整流出净面积"：

```python
def polygon_area(P):
    n = len(P)
    s = 0.0
    for i in range(n):
        x1, y1 = P[i]
        x2, y2 = P[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0

P = [(0,0),(4,0),(4,3),(0,3)]
print(round(polygon_area(P), 2))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.19.18 例 18：两线段相交判定（HDU 1086）⭐⭐
> **知识点**：线段相交、快速排斥、跨立实验｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给两条线段 (P1,P2)、(P3,P4)，判断（含端点重合）是否相交，输出 YES/NO。多组测试。

**思路**
标准做法：快速排斥（包围盒相交）+ 跨立实验（两线段互跨对方所在直线方向相反，用叉积判断）。含共线端点情形用跨立中的"点在另一线段上"判定。

💡 类比"两根筷子是否打架：先看外包框有没有机会碰上，再用两侧跨立判断实际穿插"：

```python
def on_seg(p, a, b):
    return (min(a[0],b[0]) - 1e-9 <= p[0] <= max(a[0],b[0]) + 1e-9 and
            min(a[1],b[1]) - 1e-9 <= p[1] <= max(a[1],b[1]) + 1e-9)

def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def intersect(p1, p2, p3, p4):
    d1 = cross(p3, p4, p1)
    d2 = cross(p3, p4, p2)
    d3 = cross(p1, p2, p3)
    d4 = cross(p1, p2, p4)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    elif d1 == 0 and on_seg(p1, p3, p4):
        return True
    elif d2 == 0 and on_seg(p2, p3, p4):
        return True
    elif d3 == 0 and on_seg(p3, p1, p2):
        return True
    elif d4 == 0 and on_seg(p4, p1, p2):
        return True
    return False

print(intersect((0,0),(2,2),(0,2),(2,0)))
print(intersect((0,0),(1,0),(2,0),(3,0)))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.19 例 19：点在多边形内的判定（射线法）（POJ 2398 变式）⭐⭐
> **知识点**：射线法、奇偶规则、边界处理｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给一个简单多边形 n 个顶点与若干查询点，判断每个查询点位于多边形内、外（或边界）。n≤10^3，查询 ≤100。

**思路**
射线法：从 P 向右水平射线，统计与多边形边的交点数，偶数在外、奇数在内；交点恰在顶点/射线上时需特殊处理（用叉积与上下开区间判断）。

💡 类比"迷宫外墙数穿墙次数：向一个方向越出墙一次就换进/出，奇数次就是被困在里头"：

```python
def point_in_poly(P, poly):
    n = len(poly)
    x, y = P
    inside = False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if min(y1, y2) < y <= max(y1, y2) and x <= max(x1, x2):
            if y1 != y2:
                xint = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if y1 == y2:
                xint = min(x1, x2)
            if xint >= x:
                inside = not inside
    return inside

poly = [(0,0),(4,0),(4,4),(0,4)]
for p in [(2,2),(5,2),(0,2),(0,0)]:
    print(p, point_in_poly(p, poly))
```
> **复杂度**：O(n) 每查询，O(1) 空间

---
#### 17.19.20 例 20：旋转卡壳求凸多边形直径（洛谷 P2516 变式）⭐⭐⭐
> **知识点**：旋转卡壳、凸包直径、最远点对｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给 n 个点（n≤10^5），求凸多边形（或点集的凸包）直径，即所有点对中的最大距离。输出距离平方或浮点。

**思路**
先求凸包，再用旋转卡壳：在对踵点对上移动，用叉积比较面积单调推进两条平行线，得到最大距离。复杂度 O(n log n)（主要凸包排序）。

💡 类比"量一对最远的糖葫芦夹子最开的两颗：凸包的顶点围成多边形，旋转两把平行尺夹住最远对点"：

```python
def convex_hull(points):
    pts = sorted(points)
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
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

def rotating_calipers(hull):
    n = len(hull)
    if n == 1:
        return 0
    j = 1
    maxd = 0
    res = hull[0]
    for i in range(n):
        while abs(cross_area(hull[i], hull[(i+1)%n], hull[j])) < abs(cross_area(hull[i], hull[(i+1)%n], hull[(j+1)%n])):
            j = (j + 1) % n
        ni = hull[(i+1)%n]
        for cand in (hull[i], hull[j], hull[(j+1)%n]):
            d = (cand[0]-hull[0][0])**2 + (cand[1]-hull[0][1])**2
        d = (hull[i][0]-hull[j][0])**2 + (hull[i][1]-hull[j][1])**2
        maxd = max(maxd, d)
    return maxd

def cross_area(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

pts = [(0,0),(1,0),(0,1),(1,1),(2,3),(3,1)]
hull = convex_hull(pts)
print("hull=", hull)
print("diam^2=", rotating_calipers(hull))
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.19.21 例 21：圆与直线的交点（HDU 2180 变式）⭐⭐
> **知识点**：圆线交点、判别式、几何解方程｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给圆心 (cx,cy)、半径 r 与直线（过两点），求直线与圆的交点个数及坐标（若存在）。输出交点坐标到 2 位小数，无交点输出 None。

**思路**
把圆心平移到原点，直线化为标准式，用判别式判断相切/相交/相离，解出交点坐标再平移回去。

💡 类比"激光穿过泳圈：看圆心到直线的垂距比半径判断切两个/一个/没有，垂足两侧对称取交点"：

```python
import math

def circle_line(c, r, P1, P2):
    cx, cy = c
    # 直线 Ax+By+C=0（用 P1->P2）
    ax = P2[0] - P1[0]
    ay = P2[1] - P1[1]
    A, B = ay, -ax
    C = -(A * P1[0] + B * P1[1])
    # 平移圆心到原点后求与单位圆交点
    # 用标准：投影法
    dx = P2[0] - P1[0]
    dy = P2[1] - P1[1]
    seg = math.hypot(dx, dy)
    ux, uy = dx / seg, dy / seg
    fx, fy = P1[0] - cx, P1[1] - cy
    t = -(fx * ux + fy * uy)
    footx = cx + t * ux + fx   # 垂足
    # 垂距
    d = abs(A * cx + B * cy + C) / math.hypot(A, B)
    if d > r + 1e-9:
        return []
    # 沿方向 half
    half = math.sqrt(max(0.0, r * r - d * d))
    # 垂足坐标
    nrx = ux * 0
    # 用T表达
    px = cx - A * d_scale(A, B, C, cx, cy)  # simplified
    return tangent_points(A,B,C,cx,cy,r)

def d_scale(A,B,C,cx,cy):
    val = (A*cx + B*cy + C) / (A*A + B*B)
    return A*val, B*val

def tangent_points(A,B,C,cx,cy,r):
    cross_check = abs(A*cx+B*cy+C)/math.hypot(A,B)
    if cross_check > r + 1e-9:
        return []
    # 单位法向量
    nrm = math.hypot(A, B)
    nx, ny = A/nrm, B/nrm
    # 圆心到直线有向距离（带符号）
    sgn = (A*cx+B*cy+C)
    dw = sgn/nrm
    # 垂足 P0 = 圆心 - 有向偏移 n*(C+...)
    p0x = cx - nx * dw
    p0y = cy - ny * dw
    half = math.sqrt(max(0.0, r*r - dw*dw))
    # 方向向量 (与 n 垂直)
    tx, ty = -ny, nx
    p1 = (p0x + tx * half, p0y + ty * half)
    p2 = (p0x - tx * half, p0y - ty * half)
    return sorted([p1, p2])

for pt in circle_line((0,0),5,(10,0),(10,10)):
    print(round(pt[0],2), round(pt[1],2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.22 例 22：点按极角排序（POJ 2007）⭐⭐
> **知识点**：极角排序、atan2、叉积比较｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给平面上若干点（含原点），把点按绕原点的极角从小到大排序并输出。点不共极角化简。

**思路**
用 atan2 求极角或自定义比较：先按象限，再同象限用叉积判角度。直接按 (atan2(y,x)) 排序即可。

💡 类比"钟表盘号码盘小时刻度排序：按指针角度从小到大排，逆时针转一圈"：

```python
import math

def polar_sort(points):
    return sorted(points, key=lambda p: math.atan2(p[1], p[0]))

ps = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (-1,1)]
for p in polar_sort(ps):
    print(p)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.19.23 例 23：向量加减与数乘（洛谷 P1994 变式）⭐
> **知识点**：向量运算、线性组合｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给两向量 a=(x1,y1)、b=(x2,y2) 与标量 k，依次输出 a+b、a−b、k·a 三个向量。坐标整数，输出整数分量。

**思路**
逐分量做加减与数乘，即可。

💡 类比"坐标纸上的箭头合成：同向加码、反向折回，放大就各分量乘倍数"：

```python
def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1])
def vsub(a, b):
    return (a[0] - b[0], a[1] - b[1])
def vscale(a, k):
    return (a[0] * k, a[1] * k)

a, b, k = (1, 2), (3, -1), 2
print(vadd(a, b), vsub(a, b), vscale(a, k))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.24 例 24：两向量夹角（HDU 2041 变式）⭐
> **知识点**：夹角、点积、acos｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给两向量，输出它们夹角（度，0~180），保留 2 位小数。两向量均非零。

**思路**
cosθ = 点积/(|a||b|)，再用 acos 反解弧度转角度，注意 clamp 到 [-1,1] 防精度越界。

💡 类比"量两把尺的张开角：看同向重合度经余弦反算成度数"：

```python
import math

def angle_deg(a, b):
    la = math.hypot(*a)
    lb = math.hypot(*b)
    if la == 0 or lb == 0:
        return 0.0
    cosv = (a[0]*b[0] + a[1]*b[1]) / (la * lb)
    cosv = max(-1.0, min(1.0, cosv))
    return math.degrees(math.acos(cosv))

print(round(angle_deg((1,0),(0,1)), 2))
print(round(angle_deg((1,0),(-1,0)), 2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.25 例 25：判断点是否在圆上/内部（洛谷 P1313 变式）⭐
> **知识点**：距离比较、圆的区域划分｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给圆心、半径与点，判断点位于圆内、圆上还是圆外，输出 IN/ON/OUT。坐标整数。

**思路**
比较点到圆心距平方与 r²：小于 IN，等于 ON，大于 OUT。

💡 类比"飞镖上靶心判定：半径没到是内围，正好压线是尘缘，超出为外围"：

```python
def circle_region(c, r, p):
    d2 = (p[0]-c[0])**2 + (p[1]-c[1])**2
    r2 = r * r
    if d2 < r2:
        return "IN"
    if abs(d2 - r2) < 1e-9:
        return "ON"
    return "OUT"

c, r = (0,0), 5
for p in [(1,1),(3,4),(6,0),(5,0)]:
    print(p, circle_region(c, r, p))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.26 例 26：两直线求交点（HDU 2109 变式）⭐⭐
> **知识点**：直线交点、叉积、行列式｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给两条直线（各由两点确定），求交点坐标，若平行无交点输出 None。坐标可为实数，输出 2 位小数。

**思路**
写成参数/方程 Ax+By+C 形式，解两元一次方程组，或向量叉积交比法。平行时判行列式为零。

💡 类比"两条射线的十字路口：用叉积算比例把交点插出来，方向平行则永不交汇"：

```python
def line_intersect(P1, P2, P3, P4):
    A1, B1 = P2[1]-P1[1], P1[0]-P2[0]
    C1 = A1*P1[0] + B1*P1[1]
    A2, B2 = P4[1]-P3[1], P3[0]-P4[0]
    C2 = A2*P3[0] + B2*P3[1]
    det = A1*B2 - A2*B1
    if abs(det) < 1e-9:
        return None
    x = (C1*B2 - C2*B1) / det
    y = (A1*C2 - A2*C1) / det
    return (x, y)

print(line_intersect((0,0),(2,2),(0,2),(2,0)))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.27 例 27：三角形内心坐标（洛谷 P1665 变式）⭐⭐
> **知识点**：内心、角平分线、加权平均｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给三角形三顶点 A、B、C，求内心（角平分线交点）坐标，输出 2 位小数。三边不共线。

**思路**
内心是三条边长度加权平均顶点：I = (a·A + b·B + c·C)/(a+b+c)，其中 a 是 A 对边 BC 长。

💡 类比"三角桌布的内圆针脚：内切圆圆心按各边长度加权均衡三顶点"：

```python
import math

def incenter(A, B, C):
    def dist(p, q):
        return math.hypot(p[0]-q[0], p[1]-q[1])
    a = dist(B, C)
    b = dist(A, C)
    c = dist(A, B)
    s = a + b + c
    x = (a*A[0] + b*B[0] + c*C[0]) / s
    y = (a*A[1] + b*B[1] + c*C[1]) / s
    return (x, y)

print(tuple(round(v, 2) for v in incenter((0,0),(6,0),(0,8))))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.28 例 28：凸多边形判定（POJ 1584）⭐⭐
> **知识点**：凸性检测、转向一致、叉积｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给 n 个顶点按顺序，判断多边形是否为凸多边形（允许共线边按处理规则）。n≤10^3。

**思路**
依次计算相邻三点转向，若叉积符号始终同号（非严格可允许 0）则为凸，出现正负交替（且非零）则非凸。

💡 类比"捏多边形的骨架看是否所有转角朝同一方向：只要有一处折反拐就不凹下去"：

```python
def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def is_convex(P):
    n = len(P)
    if n < 3:
        return False
    sign = 0
    for i in range(n):
        o = P[i]
        a = P[(i + 1) % n]
        b = P[(i + 2) % n]
        c = cross(o, a, b)
        if c != 0:
            if sign == 0:
                sign = 1 if c > 0 else -1
            elif sign * c < 0:
                return False
    return True

print(is_convex([(0,0),(3,0),(3,2),(2,2),(1,3)]))
print(is_convex([(0,0),(3,0),(1,1),(0,2)]))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.19.29 例 29：Andrew 单调链凸包（洛谷 P1456 变式）⭐⭐
> **知识点**：凸包、Andrew 算法、单调链｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给 n 个点，求最小凸包（逆时针，去掉共线点）顶点集。n≤10^5，坐标 ≤10^9。

**思路**
Andrew 算法：按 (x,y) 排序，先建下凸链再建上凸链，用叉积判断出栈，合并成完整凸包。

💡 类比"用橡皮筋绷住钉子：把点按横坐标排好，先包底下再包顶上，两段链围成外壳"：

```python
def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
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

pts = [(0,0),(1,0),(0,1),(1,1),(2,2),(3,1),(2,0)]
print(convex_hull(pts))
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.19.30 例 30：最近点对（分治）（洛谷 P1981 变式）⭐⭐⭐
> **知识点**：扫描线求最近点对、分治、最近对经典法｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给 n 个平面点，求所有点对中最近的一对的距离平方。n≤10^5，坐标整数（可能有重合点）。

**思路**
按 x 排序后分治：中线左右分别求最近，再检查跨越中线的窄条（距中线 < d）内按 y 排序的至多常数个点更新。递归 O(n log n)。

💡 类比"分教室找最近的同桌：先分两片各自找，再只检查挨着分界线那撮人是否反而更近"：

```python
import math

def closest_pair(points):
    pts = sorted(points)
    def dd(p, q):
        return (p[0]-q[0])**2 + (p[1]-q[1])**2
    def solve(l, r):
        if r - l <= 1:
            return float('inf')
        m = (l + r) // 2
        best = min(solve(l, m), solve(m, r))
        strip = []
        for i in range(l, r):
            if (pts[i][0] - pts[m][0]) ** 2 < best:
                strip.append(pts[i])
        strip.sort(key=lambda p: p[1])
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j][1] - strip[i][1])**2 < best:
                best = min(best, dd(strip[i], strip[j]))
                j += 1
        return best
    d = solve(0, len(pts))
    if d == float('inf'):
        return 0
    return math.isqrt(d)

pts = [(0,0),(3,4),(1,1),(7,9),(2,2),(5,1)]
print(closest_pair(pts))
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.19.31 例 31：半平面交（客厅染色基础）（洛谷 P1982 变式）⭐⭐⭐
> **知识点**：半平面交、凸核、直线裁剪｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给 n 条半平面（直线左侧），求它们的交是否为空；非空输出交多边形的顶点数或边界顶点的最小最大包围。n≤10^3。

**思路**
半平面交用平面裁剪（cut）：从一个大矩形/大凸多边形出发，逐条用直线把其留在左侧（右侧部分剪掉），最终剩余凸多边形；裁剪判空即可（简化入门），再用格雷厄姆裁剪实现。

💡 类比"开灯切蛋糕：每次用一条直线切一刀只留左边，剩下的区域不断被收窄成最终凸核"：

```python
# 入门半平面交（多边形裁剪，返回剩余顶点；为空返回 None）
def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def half_plane_cut(poly, A, B, C):
    # 直线 Ax+By+C>0 保留
    n = len(poly)
    if n == 0:
        return []
    newpoly = []
    for i in range(n):
        a = poly[i]
        b = poly[(i + 1) % n]
        fa = A*a[0] + B*a[1] + C
        fb = A*b[0] + B*b[1] + C
        if fa >= 0:
            newpoly.append(a)
        if (fa > 0 and fb < 0) or (fa < 0 and fb > 0):
            # 交点
            t = fa / (fa - fb)
            newpoly.append((a[0] + t*(b[0]-a[0]), a[1] + t*(b[1]-a[1])))
    return newpoly

# 例：一个大正方形交 x>=1
poly = [(-10,-10),(10,-10),(10,10),(-10,10)]
poly = half_plane_cut(poly, 1, 0, -1)
print(poly)
```
> **复杂度**：O(n²) 时间（逐线裁剪多边），O(n) 空间

---
#### 17.19.32 例 32：最小覆盖圆（洛谷 P1091 变式）⭐⭐⭐
> **知识点**：最小圆覆盖、Welzl 算法、随机化｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给 n 个点，求能覆盖全部点的最小半径圆（圆或圆周可含所有点），输出圆心与半径。n≤10^5。

**思路**
Welzl 随机增量算法：打乱点，递推确定过至多三点的最小圆，O(n) 期望。直接实现两点/三点定圆的增量式。

💡 类比"一把伞尽可能小罩住所有钉子：从外圈钉子里挑出真正顶伞的 2~3 颗来确定伞心伞径"：

```python
import math, random

def circle_from2(a, b):
    return ((a[0]+b[0])/2, (a[1]+b[1])/2, math.hypot(a[0]-b[0], a[1]-b[1])/2)

def circle_from3(a, b, c):
    d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
    if abs(d) < 1e-12:
        return None
    ux = ((a[0]**2+a[1]**2)*(b[1]-c[1]) + (b[0]**2+b[1]**2)*(c[1]-a[1]) + (c[0]**2+c[1]**2)*(a[1]-b[1])) / d
    uy = ((a[0]**2+a[1]**2)*(c[0]-b[0]) + (b[0]**2+b[1]**2)*(a[0]-c[0]) + (c[0]**2+c[1]**2)*(b[0]-a[0])) / d
    r = math.hypot(ux-a[0], uy-a[1])
    return (ux, uy, r)

def min_circle(points):
    p = points[:]
    random.shuffle(p)
    c = (0.0, 0.0, 0.0)
    def valid(cc, q):
        return math.hypot(q[0]-cc[0], q[1]-cc[1]) <= cc[2] + 1e-9
    n = len(p)
    for i in range(n):
        if valid(c, p[i]):
            continue
        c = (p[i][0], p[i][1], 0.0)
        for j in range(i):
            if valid(c, p[j]):
                continue
            c = circle_from2(p[i], p[j])
            for k in range(j):
                if valid(c, p[k]):
                    continue
                c3 = circle_from3(p[i], p[j], p[k])
                if c3:
                    c = c3
    return c

pts = [(0,0),(1,0),(0,1),(1,1),(0.5,0.5)]
cx, cy, r = min_circle(pts)
print(round(cx,2), round(cy,2), round(r,2))
```
> **复杂度**：O(n) 期望时间，O(n) 空间

---
#### 17.19.33 例 33：三点是否构成锐角/直角/钝角三角形（HDU 2106 变式）⭐
> **知识点**：三角形分类、余弦定理、勾股｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给三点，判断三角形是锐角、直角还是钝角三角形（或无法构成）。输出相应字样。坐标整数。

**思路**
取三边平方 a²≤b²≤c²，若 a²+b²==c² 直角；> 为锐角；< 为钝角。先判是否可成三角。

💡 类比"看最长的边对应对角：最长边平方等于另两方和为直角，大了钝、小了锐"：

```python
def tri_type(A, B, C):
    def sq(p, q):
        return (p[0]-q[0])**2 + (p[1]-q[1])**2
    s = sorted([sq(A,B), sq(B,C), sq(C,A)])
    # 任两边 > 第三边
    if s[0] + s[1] != s[2]:
        # 不构成三角形(退化) 用严格不等式检查也可以，此处以平方关系分类
        pass
    if s[0] + s[1] == s[2]:
        return "直角"
    if s[0] + s[1] > s[2]:
        return "锐角"
    return "钝角"

print(tri_type((0,0),(3,0),(0,4)))
print(tri_type((0,0),(1,0),(0,1)))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.34 例 34：多边形是否顺时针排列（洛谷 P1315 变式）⭐
> **知识点**：有向面积、环绕方向、鞋带和符号｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给多边形顶点（顺序既定，简单多边形），判断顶点是按顺时针还是逆时针排列。输出 CW/CCW。n≤10^4。

**思路**
鞋带公式的有向面积符号：负为顺时针，正为逆时针（x 轴右、y 轴上的常规左手系）。

💡 类比"绕圈跑的方向感应：鞋带和的正负卦在坐标系里给出是顺时针还是逆时针跑"：

```python
def orientation(P):
    n = len(P)
    s = 0
    for i in range(n):
        x1, y1 = P[i]
        x2, y2 = P[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    if s > 0:
        return "CCW"
    if s < 0:
        return "CW"
    return "LINE/退化"

print(orientation([(0,0),(3,0),(3,3),(0,3)]))
print(orientation([(0,0),(0,3),(3,3),(3,0)]))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.19.35 例 35：判断四边形是否为矩形（HDU 2113 变式）⭐⭐
> **知识点**：向量、垂直、矩形判定｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给四边形的四点坐标（顶点顺序给定），判断是否为矩形（对边平行且相等、邻边垂直）。输出 YES/NO。多组输入。

**思路**
按顺序计算四边向量，检查对边向量相等（平行等长）且相邻边点积为零。

💡 类比"量四边的桌板角：对边一样长又都互相平行，转角相邻两线垂直才方正"：

```python
def is_rect(P):
    def v(a, b):
        return (b[0]-a[0], b[1]-a[1])
    p = P
    va = v(p[0], p[1])
    vb = v(p[1], p[2])
    vc = v(p[2], p[3])
    vd = v(p[3], p[0])
    # 对边: va==-vc 且 vb==-vd, 邻边垂直 va·vb=0
    para1 = va[0]==-vc[0] and va[1]==-vc[1]
    para2 = vb[0]==-vd[0] and vb[1]==-vd[1]
    perp = va[0]*vb[0] + va[1]*vb[1] == 0
    return para1 and para2 and perp

print(is_rect([(0,0),(4,0),(4,3),(0,3)]))
print(is_rect([(0,0),(4,0),(3,3),(0,3)]))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.36 例 36：点在三角形内部（叉积法）（洛谷 P1374 变式）⭐⭐
> **知识点**：点在三角内、叉积同向、凸组合｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给三角形顶点 A、B、C 与点 P，判断 P 是否在三角形内部（含边），输出 IN/OUT。坐标整数。

**思路**
对三条有向边用叉积判定同向：若 P 始终在每条边同一侧（同号）则在内部；等于 0 表示在边上。

💡 类比"三角格子里站人是否在器具里：绕着三边看人都朝同一侧，就站进去了"：

```python
def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def point_in_tri(A, B, C, P):
    d1 = cross(A, B, P)
    d2 = cross(B, C, P)
    d3 = cross(C, A, P)
    has_neg = d1 < 0 or d2 < 0 or d3 < 0
    has_pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (has_neg and has_pos)

print(point_in_tri((0,0),(4,0),(0,3),(1,1)))
print(point_in_tri((0,0),(4,0),(0,3),(5,5)))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.37 例 37：凸多边形重心（洛谷 P1022 变式）⭐⭐
> **知识点**：多边形重心、鞋带加权、面积划分三角形｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：凸多边形 n 个顶点，求其均匀多边形重心坐标，输出 2 位小数。n≤10^4。

**思路**
把多边形按首点为基准三角剖分，重心 = Σ(三角形重心·三角形面积)/总面积，用鞋带公式算各三角形面积。

💡 类比"薄铁板的悬吊平衡点：分红多边形做若干三角板，各自重心按质量加权平均"：

```python
def poly_centroid(P):
    n = len(P)
    A = 0.0
    cx = cy = 0.0
    for i in range(n):
        x1, y1 = P[i]
        x2, y2 = P[(i + 1) % n]
        cross = x1 * y2 - x2 * y1
        A += cross
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
    A *= 0.5
    cx = cx / (6 * A)
    cy = cy / (6 * A)
    return (cx, cy)

print(tuple(round(v, 2) for v in poly_centroid([(0,0),(4,0),(4,3),(0,3)])))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.19.38 例 38：圆内整点计数（洛谷 P1633 变式）⭐⭐
> **知识点**：圆、整点枚举、计数优化｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：以原点为圆心、半径 r 的圆（含边界内）有多少个整点？r≤10^5。

**思路**
枚举 x 从 -r 到 r，每列算出 y 范围 ±√(r²−x²) 内的整点个数累加，取整向下向上即可计数（对称计数）。

💡 类比"网格纸上画圆数格点：一列一列数这列圆里压了多少个坐标格点"：

```python
import math

def lattice_in_circle(r):
    cnt = 0
    for x in range(-r, r + 1):
        d = r * r - x * x
        if d < 0:
            continue
        m = int(math.isqrt(d))
        cnt += 2 * m + 1
    return cnt

for r in (1, 2, 5):
    print(r, lattice_in_circle(r))
```
> **复杂度**：O(r) 时间，O(1) 空间

---
#### 17.19.39 例 39：判断线段是否穿过/触碰圆（HDU 2136 变式）⭐⭐
> **知识点**：线段与圆、点到线段距离、相离/相交/相切｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给圆（圆心、半径）与线段 AB，判断线段与圆是否相交或相切（触碰即算），输出 YES/NO。坐标整数。

**思路**
计算线段 AB 到圆心的最短距离，若 ≤ r 则线段与圆有公共点（含端点相切）。用 17.19.11 的线段最短距离。

💡 类比"举杆探钱币：杆子离钱心最近处不超过半径就算碰到钱"：

```python
import math

def pt_seg_dist(A, B, P):
    vx, vy = B[0]-A[0], B[1]-A[1]
    wx, wy = P[0]-A[0], P[1]-A[1]
    c1 = vx*wx + vy*wy
    if c1 <= 0:
        return math.hypot(P[0]-A[0], P[1]-A[1])
    c2 = vx*vx + vy*vy
    if c1 >= c2:
        return math.hypot(P[0]-B[0], P[1]-B[1])
    b = c1 / c2
    px = A[0] + b*vx
    py = A[1] + b*vy
    return math.hypot(P[0]-px, P[1]-py)

def seg_circle(c, r, A, B):
    return pt_seg_dist(A, B, c) <= r + 1e-9

print(seg_circle((0,0), 5, (10,0),(10,10)))
print(seg_circle((0,0), 5, (0,-2),(2,0)))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.40 例 40：求三角形重心坐标（洛谷 P1288 变式）⭐
> **知识点**：重心、质心、三点平均｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给三角形三点 A、B、C，求其重心（三条中线的交点）坐标，输出 2 位小数。

**思路**
重心 = (A+B+C)/3 的算术平均坐标。

💡 类比"三根吊索的平衡点：三条线各取中点的中点绳子交汇处，就是三点平均"：

```python
def centroid(A, B, C):
    return ((A[0]+B[0]+C[0])/3, (A[1]+B[1]+C[1])/3)

print(tuple(round(v,2) for v in centroid((0,0),(6,0),(0,9))))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.41 例 41：圆两点相切的切点（给定圆外一点作切线）（洛谷 P2006 变式）⭐⭐
> **知识点**：切线、余弦/正弦、外点切点坐标｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给圆（原点）圆心、半径 r 与圆外点 P，求过 P 的两条切线的切点坐标。输出两切点。坐标可实数，保留 2 位小数。

**思路**
用几何：切点与圆心、外点构成直角三角。夹角法或向量法：设 OP 与切点连线夹角 φ，切点在以 OP 为半径的圆与给定圆交点上，用两点圆求交点或角度推两切点。

💡 类比"用定长绳绕大球找贴合点：外点与球心线段上沿两个对称角度拨出的贴合位置"：

```python
import math

def tangent_points(c, r, P):
    cx, cy = c
    # 平移 P 相对圆心
    dx = P[0] - cx
    dy = P[1] - cy
    d = math.hypot(dx, dy)
    if r >= d:
        return []
    # 角度法
    base = math.atan2(dy, dx)
    delta = math.acos(r / d)
    res = []
    for s in (1, -1):
        ang = base + delta * s
        tx = cx + r * math.cos(ang)
        ty = cy + r * math.sin(ang)
        res.append((tx, ty))
    return res

for p in tangent_points((0,0), 5, (13,0)):
    print(round(p[0],2), round(p[1],2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.42 例 42：判断两点是否对称于直线（洛谷 P2006 变式）⭐⭐
> **知识点**：对称点、垂直平分、距离相等｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给直线 L（过两点）与 A、B 两点，判断 A、B 是否关于 L 对称。输出 YES/NO。坐标整数。

**思路**
A、B 关于 L 对称当且仅当：L 是 AB 的垂直平分线。即 AB 中点落在 L 上，且 AB 方向垂直于 L。

💡 类比"镜面照两点重合：两点连线被镜面垂直且中分，就是镜像对称"：

```python
import math

def is_symmetric(L1, L2, A, B):
    # 中点
    mx = (A[0]+B[0])/2
    my = (A[1]+B[1])/2
    # 中点是否在 L 上
    dxl = L2[0]-L1[0]
    dyl = L2[1]-L1[1]
    on_line = abs(dxl*(my-L1[1]) - dyl*(mx-L1[0])) < 1e-9
    # AB 方向
    dab = (B[0]-A[0], B[1]-A[1])
    dot = dxl*dab[0] + dyl*dab[1]
    return on_line and abs(dot) < 1e-9

print(is_symmetric((0,0),(0,1),(2,1),(-2,1)))
print(is_symmetric((0,0),(1,0),(2,1),(-2,1)))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.43 例 43：求凸包周长（洛谷 P1393 变式）⭐⭐
> **知识点**：凸包+周长、链长求和｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给 n 个点，求其凸包的周长，输出 2 位小数。n≤10^5。

**思路**
先 Andrew 求凸包顶点，再按顺序累加相邻顶点距离（收尾闭合）。

💡 类比"给钉子群套最短橡皮筋，量这根橡皮筋拉直后的总长"：

```python
import math

def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
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

def hull_perimeter(points):
    h = convex_hull(points)
    if len(h) <= 1:
        return 0.0
    s = 0.0
    for i in range(len(h)):
        a, b = h[i], h[(i+1) % len(h)]
        s += math.hypot(a[0]-b[0], a[1]-b[1])
    return s

pts = [(0,0),(1,0),(0,1),(1,1),(2,2),(3,1)]
print(round(hull_perimeter(pts), 2))
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.19.44 例 44：圆和矩形的交（包含/相离/相交判断）（洛谷 P1648 变式）⭐⭐
> **知识点**：圆与矩形、点到矩形最短距离、包含判断｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给圆（圆心、半径）与轴对齐矩形，判断圆与矩形是否相交（含矩内/部分/相切触碰）。输出 YES/NO。

**思路**
先看圆心是否在矩形内矩扩近；否则求圆心到矩形边界的最短距离，≤ r 则相交。

💡 类比"圆盘滚向方槽：圆心进到槽里算交，没进就看离槽壁最近的垂直距离是否够贴近"：

```python
import math

def pt_rect_dist(c, xmin, ymin, xmax, ymax):
    cx, cy = c
    dx = max(xmin - cx, 0, cx - xmax)
    dy = max(ymin - cy, 0, cy - ymax)
    return math.hypot(dx, dy)

def circle_rect_hit(c, r, rect):
    if x_in(c[0], rect) and y_in(c[1], rect):
        return True
    return pt_rect_dist(c, *rect) <= r + 1e-9

def x_in(x, r):
    return r[0] <= x <= r[2]
def y_in(y, r):
    return r[1] <= y <= r[3]

rect = (0, 0, 4, 4)
print(circle_rect_hit((2, 2), 1, rect))
print(circle_rect_hit((6, 2), 1, rect))
print(circle_rect_hit((5, 2), 2, rect))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.45 例 45：三点张的最大角 / 视线最大夹角（洛谷 P1332 变式）⭐⭐
> **知识点**：极角、角度比较、最大夹角扫描｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给 n 个向量（原点向各点），求其中最接近共线（即夹角最大不超过某阈值）的一对向量，输出最大两两夹角。n≤10^4。

**思路**
按极角排序后，在环上相邻比较角度差（或用补角技巧），考察排序后相邻向量夹角，最大值在相邻或首尾邻接处取得。

💡 类比"圆形货架相邻品项最挤：把箭头按方向排一圈，相邻两箭夹角最小/必需看，最近的一对即最大间隙补出"：

```python
import math

def max_pair_angle(vecs):
    ang = sorted(math.atan2(y, x) for x, y in vecs)
    n = len(ang)
    # 环上相邻夹角最大值
    best = 0.0
    for i in range(n):
        d = ang[(i+1) % n] - ang[i]
        if i == n - 1:
            d += 2 * math.pi
        best = max(best, d)
    # 最大夹角应是 2π - 最小相邻间隙
    pass

def min_angle_pair(vecs):
    ang = sorted(math.atan2(y, x) for x, y in vecs)
    n = len(ang)
    best = 10
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(ang[j] - ang[i])
            if d > math.pi:
                d = 2 * math.pi - d
            best = min(best, d)
    return best

v = [(1,0),(0,1),(-1,1)]
print(round(math.degrees(min_angle_pair(v)), 2))
```
> **复杂度**：O(n²) 朴素 时间，O(n) 空间（可优化 O(n log n)）

---
#### 17.19.46 例 46：判断点在多边形边界上（洛谷 P1451 变式）⭐⭐
> **知识点**：点在线段上、边界判定、点到线段｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给简单多边形 n 顶点与点 P，判断 P 是否落在多边形某条边上（边界），输出 ON/OFF。n≤10^3。

**思路**
遍历每条边，用"点积/叉积判点在线段上"：点 P 与边两端点叉积为 0 且在两端点包围盒内即为在边上。

💡 类比"看人是否恰好踩在自己院墙的围栏线上：既在墙直线上又在两界桩之间"：

```python
def on_seg(P, A, B):
    c = (B[0]-A[0])*(P[1]-A[1]) - (B[1]-A[1])*(P[0]-A[0])
    if abs(c) > 1e-9:
        return False
    return (min(A[0],B[0])-1e-9 <= P[0] <= max(A[0],B[0])+1e-9 and
            min(A[1],B[1])-1e-9 <= P[1] <= max(A[1],B[1])+1e-9)

def point_on_polygon(P, poly):
    n = len(poly)
    for i in range(n):
        if on_seg(P, poly[i], poly[(i+1) % n]):
            return True
    return False

poly = [(0,0),(4,0),(4,3),(0,3)]
print(point_on_polygon((2,0), poly))
print(point_on_polygon((2,1), poly))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.19.47 例 47：两圆位置关系（HDU 2172 变式）⭐⭐
> **知识点**：圆与圆、圆心距、相交/相切/内含判定｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给两圆 (c1,r1)、(c2,r2)，判断它们的位置关系：外离/外切/相交/内切/内含。输出对应字样。坐标实数。

**思路**
算圆心距 d，比较 d 与 |r1-r2|、r1+r2 的大小关系分类。

💡 类比"两个光圈的远离贴近：看两圆心距离对比半径和与半径差，判定离、切、交、含"：

```python
import math

def circle_relation(c1, r1, c2, r2):
    d = math.hypot(c1[0]-c2[0], c1[1]-c2[1])
    eps = 1e-9
    if d > r1 + r2 + eps:
        return "外离"
    if abs(d - (r1 + r2)) <= eps:
        return "外切"
    if d > abs(r1 - r2) + eps:
        return "相交"
    if d == 0:
        return "同心"
    if abs(d - abs(r1 - r2)) <= eps:
        return "内切"
    return "内含"

print(circle_relation((0,0),3,(8,0),2))
print(circle_relation((0,0),3,(5,0),2))
print(circle_relation((0,0),3,(4,0),2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.48 例 48：圆面积与周长（HDU 2027 变式）⭐
> **知识点**：圆、π、浮点输出｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给半径 r，输出圆面积 πr² 与周长 2πr，保留 2 位小数。多组输入。

**思路**
直接用数学常量和公式计算，π 取 math.pi。

💡 类比"量圆饼的用料：面积看铺开布料，周长看外圈包条长度"：

```python
import sys, math

for line in sys.stdin:
    r = float(line.strip())
    area = math.pi * r * r
    cir = 2 * math.pi * r
    print(f"{area:.2f} {cir:.2f}")
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.49 例 49：三角形内切圆半径（洛谷 P1205 变式）⭐⭐
> **知识点**：内切圆、海伦/面积、半周长｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给三角形三点，求内切圆半径，输出 2 位小数。三点不共线。

**思路**
面积 S（叉积法）与半周长 s=(a+b+c)/2，内切圆半径 r = S/s。

💡 类比"三角烤盘里的最大蒸笼环：面积除上半周长就是能放下内圆的最大半径"：

```python
import math

def incircle_radius(A, B, C):
    def dist(p, q):
        return math.hypot(p[0]-q[0], p[1]-q[1])
    a = dist(B, C)
    b = dist(A, C)
    c = dist(A, B)
    sem = (a + b + c) / 2
    area2 = abs((B[0]-A[0])*(C[1]-A[1]) - (B[1]-A[1])*(C[0]-A[0]))
    area = area2 / 2
    return area / sem

print(round(incircle_radius((0,0),(3,0),(0,4)), 2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.50 例 50：点到直线垂足坐标（洛谷 P2016 变式）⭐⭐
> **知识点**：垂足、投影、参数投影公式｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给直线过两点 P1、P2 与点 P，求 P 到直线上的垂足坐标（投影点），输出 2 位小数。

**思路**
把 P1P2 看成方向向量，垂足 F = P1 + t·(P2-P1)，其中 t = (P-P1)·(P2-P1)/|P2-P1|²。

💡 类比"太阳垂直打下的影点：沿墙壁方向把点投影到那个方向的坐标刻度上"：

```python
def foot_on_line(P1, P2, P):
    vx = P2[0] - P1[0]
    vy = P2[1] - P1[1]
    denom = vx*vx + vy*vy
    if denom == 0:
        return P1
    t = ((P[0]-P1[0])*vx + (P[1]-P1[1])*vy) / denom
    return (P1[0] + t*vx, P1[1] + t*vy)

print(tuple(round(v,2) for v in foot_on_line((0,0),(4,0),(2,3))))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.51 例 51：线段 n 等分点（洛谷 P1324 变式）⭐
> **知识点**：插值、向量缩放、等分点｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给线段 A(x1,y1)、B(x2,y2) 与整数 n，输出把 AB 分成 n 等份时的中间分点坐标（n-1 个）。输出 2 位小数。

**思路**：第 k 个分点 = A + k/n·(B-A)，k=1..n-1。

💡 类比"蛋糕切成 n 等份标记刻度：每切一刀的位置按 k/n 比例落在两端的连线上"：

```python
def division_points(A, B, n):
    res = []
    for k in range(1, n):
        t = k / n
        res.append((A[0] + t*(B[0]-A[0]), A[1] + t*(B[1]-A[1])))
    return res

for p in division_points((0,0),(4,0),4):
    print(round(p[0],2), round(p[1],2))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.19.52 例 52：四边形是否正方形（洛谷 P1420 变式）⭐⭐
> **知识点**：正方形判定、边长相等、对角线垂直相等｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给四点，判断它们是否构成正方形（顶点顺序任意），输出 YES/NO。多组输入。

**思路**：计算所有 6 对两点距离平方（12 个组合实为 6 条边/对角线），正方形恰有 4 条相等的短边和 2 条相等的长边，且长边=√2 短边。统计即可。

💡 类比"量四根木条和两条对角线：四根同长、两对角线同长且互为 √2 倍，就是方正"：

```python
def is_square(p):
    def d2(a, b):
        return (a[0]-b[0])**2 + (a[1]-b[1])**2
    ds = []
    for i in range(4):
        for j in range(i+1, 4):
            ds.append(d2(p[i], p[j]))
    ds.sort()
    # 前4是最短边长(中有3对=边长? 实际上正方形: 4边+2对角线)
    a, b = ds[0], ds[4]
    return ds[0]==ds[1]==ds[2]==ds[3] and ds[4]==ds[5] and a > 0 and ds[4] == 2*ds[0]

print(is_square([(0,0),(2,0),(2,2),(0,2)]))
print(is_square([(0,0),(2,1),(1,3),(-1,2)]))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.53 例 53：皮克定理求内部格点数（洛谷 P1490 变式）⭐⭐
> **知识点**：皮克定理、格点计数、多边形整点｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给顶点均为整点的简单多边形，求内部整点（不含边界）的个数 I。n≤10^3，坐标 ≤10^9。

**思路**：皮克定理 I = S − B/2 + 1，S 是面积（鞋带），B 是边界格点数 = Σ gcd(|dx|,|dy|) 对每条边。

💡 类比"数多边形格点棋盘上的内格：从总面积里扣掉边界一半再加 1（皮克魔术）"：

```python
import math

def inside_lattice(P):
    n = len(P)
    S2 = 0
    B = 0
    for i in range(n):
        x1, y1 = P[i]
        x2, y2 = P[(i+1) % n]
        S2 += x1*y2 - x2*y1
        B += math.gcd(abs(x2-x1), abs(y2-y1))
    S = abs(S2) / 2
    return int(S - B/2 + 1)

print(inside_lattice([(0,0),(4,0),(4,3),(0,3)]))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.19.54 例 54：三点顺逆方向判定（HDU 2012 变式）⭐
> **知识点**：转向、叉积符号、点序列方向｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给三点 A、B、C，判断从 A 经 B 到 C 的转向是左转（逆时针）、右转（顺时针）还是直行（共线）。输出 LEFT/RIGHT/NONE。

**思路**：叉积 cross(B-A, C-A) 的正负，正=左转，负=右转，0=直行。

💡 类比"驾驶转向灯：看清楚前一段方向，叉积正就是向左打、负向右打、零是直走"：

```python
def turn(A, B, C):
    c = (B[0]-A[0])*(C[1]-A[1]) - (B[1]-A[1])*(C[0]-A[0])
    if c > 0:
        return "LEFT"
    if c < 0:
        return "RIGHT"
    return "NONE"

print(turn((0,0),(1,0),(0,1)))
print(turn((0,0),(1,0),(2,0)))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.55 例 55：两矩形重叠判定（洛谷 P1416 变式）⭐
> **知识点**：矩形重叠、区间交叉、边界判交｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给两个轴对齐矩形（左下、右上），判断是否重叠（边界触碰也算重叠或需判定 BY 规则），输出 YES/NO。

**思路**：重叠当且仅当两个 x 区间、y 区间都相交（max 下界 < min 上界，含 ≤ 视题目）。用区间交非空判断。

💡 类比"两块铺地砖是否有共同的缝：横竖两个方向区间都碰得上就有交集"：

```python
def rect_overlap(r1, r2):
    xmin = max(r1[0], r2[0])
    xmax = min(r1[2], r2[2])
    ymin = max(r1[1], r2[1])
    ymax = min(r1[3], r2[3])
    # 含边界触碰算重叠则用 <=
    return xmin <= xmax and ymin <= ymax

print(rect_overlap((0,0,2,2), (1,1,3,3)))
print(rect_overlap((0,0,2,2), (3,0,5,2)))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.56 例 56：判断四点是凸四边形（洛谷 P1425 变式）⭐⭐
> **知识点**：凸四边、凸性、叉积逐一转向｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给四点，判断四个点（按此序或多边形）是否构成凸四边形，输出 YES/NO。多组输入。

**思路**：按顺序遍历四条边，检查所有顶点转向一致（都是左转或右转），即每次叉积同号。

💡 类比"拐弯方向全同的赛道：走一圈相邻三点的转向从不同号，才拦得住成凸形"：

```python
def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def is_convex_quad(p):
    sign = 0
    for i in range(4):
        c = cross(p[i], p[(i+1) % 4], p[(i+2) % 4])
        if c != 0:
            if sign == 0:
                sign = 1 if c > 0 else -1
            elif sign * c < 0:
                return False
    return True

print(is_convex_quad([(0,0),(2,0),(2,2),(0,2)]))
print(is_convex_quad([(0,0),(1,1),(2,0),(2,2)]))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.57 例 57：圆外一点到圆的切线长（洛谷 P2005 变式）⭐⭐
> **知识点**：切线长、勾股、外点切线｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给圆（圆心、半径）与圆外一点 P，求过 P 的两条切线长度（两条等长），输出 2 位小数。若 P 在圆内输出 0。

**思路**：切线长 = √(d² − r²)，其中 d 为 P 到圆心的距离；d<r 则无切线输出 0。

💡 类比"圆外柱子拉两根绷直绳子贴着圆：绳长等于眉心距平方减去半径平方开根"：

```python
import math

def tangent_length(c, r, P):
    d = math.hypot(P[0]-c[0], P[1]-c[1])
    if d <= r:
        return 0.0
    return math.sqrt(d*d - r*r)

print(round(tangent_length((0,0), 5, (13,0)), 2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.58 例 58：点绕任意圆心旋转（洛谷 P2072 变式）⭐⭐
> **知识点**：旋转、平移、旋转矩阵复合｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给一点 P、旋转中心 O 与角度 θ（度，逆时针），求旋转后的点坐标，输出 2 位小数。

**思路**：先把 P 平移到以 O 为原点，应用旋转矩阵，再平移回原处。

💡 类比"以钉子为中心转动的摇臂：先把钉子当原点转，再把坐标搬回原来的位置"：

```python
import math

def rotate_about(P, O, deg):
    rad = math.radians(deg)
    c, s = math.cos(rad), math.sin(rad)
    x = P[0] - O[0]
    y = P[1] - O[1]
    nx = x*c - y*s + O[0]
    ny = x*s + y*c + O[1]
    return (nx, ny)

print(tuple(round(v,2) for v in rotate_about((3,0),(0,0),90)))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.59 例 59：边界格点数（非皮克补贴）（洛谷 P1446 变式）⭐⭐
> **知识点**：gcd 边界格点、整点、最大公约数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给一条线段的两个整点端点 A、B，求这条线段（含两端）经过的整点个数。坐标 ≤10^9。

**思路**：线段上整点个数 = gcd(|dx|,|dy|) + 1。两端点均为整点时适用。

💡 类比"数直线桥墩点：横向步长与纵向步长的公约数决定能把线段切成多少个整格"：

```python
import math

def lattice_on_segment(A, B):
    g = math.gcd(abs(A[0]-B[0]), abs(A[1]-B[1]))
    return g + 1

print(lattice_on_segment((0,0),(4,2)))
print(lattice_on_segment((0,0),(6,6)))
```
> **复杂度**：O(log max) 时间，O(1) 空间

---
#### 17.19.60 例 60：凸多边形的外接正方形（包围盒）（洛谷 P1393 变式）⭐
> **知识点**：最小轴对齐包围盒、极值｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给 n 个点，求能框住全部点的最小轴对齐矩形的左下角与右上角坐标（即 x/y 的最小最大值）。坐标整数。

**思路**：分别统计所有点的 x_min、y_min、x_max、y_max。

💡 类比"量最紧的照片相框：把最左最右最下最上的点当框的边界即可"：

```python
def bounding_box(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))

pts = [(3,5),(1,2),(7,0),(4,9),(-1,3)]
print(bounding_box(pts))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.19.61 例 61：多边形的伪面积与内外点判定综合（洛谷 P2286 变式）⭐⭐⭐
> **知识点**：鞋带积累、凸包剪裁与面积差、并集思想入门｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给两个简单多边形 P 与 Q（顶点均为整点），求二者重叠（交集）部分顶点构成多边形的面积。n,m≤500。

**思路**：用 Sutherland–Hodgman 多边形裁剪，任选一多边形作为窗口，用另一多边形的每条边裁剪剩余区域，得到交集多边形，再用鞋带求面积。

💡 类比"两张透明胶片叠印：用其中一板的每条边像刀一样把另一板以外部分切掉，剩的就是重叠区"：

```python
def clip_poly(subject, x1, y1, x2, y2):
    # 保留在直线左侧 (由 P1->P2 定义, cross >= 0 为内侧)
    n = len(subject)
    if n == 0:
        return []
    out = []
    def f(a):
        return (x2-x1)*(a[1]-y1) - (y2-y1)*(a[0]-x1)
    for i in range(n):
        a = subject[i]
        b = subject[(i+1) % n]
        fa = f(a)
        fb = f(b)
        if fa >= 0:
            out.append(a)
        if (fa > 0 and fb < 0) or (fa < 0 and fb > 0):
            t = fa / (fa - fb)
            out.append((a[0] + t*(b[0]-a[0]), a[1] + t*(b[1]-a[1])))
    return out

def poly_area(P):
    n = len(P)
    s = 0
    for i in range(n):
        x1, y1 = P[i]
        x2, y2 = P[(i+1) % n]
        s += x1*y2 - x2*y1
    return abs(s) / 2

qa = (0,0),(0,3),(3,3),(3,0)          # 正方形窗
res = list(qa)
# 用四边形 (1,1),(1,5),(5,5),(5,1) 的每条边裁剪
window = [(1,1),(1,5),(5,5),(5,1)]
for i in range(4):
    x1,y1 = window[i]
    x2,y2 = window[(i+1) % 4]
    res = clip_poly(res, x1, y1, x2, y2)
print("交面积=", round(poly_area(res), 2))
```
> **复杂度**：O((m+n)·k) 时间，O(n) 空间

---
#### 17.19.62 例 62：三角形三边围出多边形质心的快速计算（洛谷 P2145 变式）⭐⭐⭐
> **知识点**：多边形质心一般式、鞋带加权、统一公式｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给任意简单多边形，直接按鞋带加权的统一公式求其形心（质心）坐标，输出 2 位小数。即使非凸也成立。

**思路**：Cx = Σ(x_i+x_{i+1})(x_i·y_{i+1}−x_{i+1}·y_i) / (3·2 倍面积)! 用统一 centroid 公式带符号面积即可。

💡 类比"弯折铁丝围圈的平衡点：每段腿线按带符号的杆面积加权，整圈取加权平均"：

```python
def poly_centroid_gen(P):
    n = len(P)
    A = 0.0
    cx = cy = 0.0
    for i in range(n):
        x1, y1 = P[i]
        x2, y2 = P[(i+1) % n]
        cross = x1*y2 - x2*y1
        A += cross
        cx += (x1 + x2)*cross
        cy += (y1 + y2)*cross
    A2 = A / 2
    if abs(A) < 1e-9:
        return (0.0, 0.0)
    return (cx/(6*A2*2/A2*2), cy/(6*A2*2/A2*2)) if False else (cx/(3*A), cy/(3*A))

P = [(0,0),(4,0),(4,3),(0,3)]
print(tuple(round(v,2) for v in poly_centroid_gen(P)))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.19.63 例 63：判断线段部分在凸多边形内（洛谷 P2187 变式）⭐⭐
> **知识点**：线段与凸多边、交点、剪刀法｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给凸多边形与线段 AB，判断线段上是否存在位于多边形内部的点（相交于内部），输出 YES/NO。n≤10^3。

**思路**：线段与多边形任一边相交，或线段某端点在多边内部（射线法）即 YES；用交点检测与点在内判定综合。

💡 类比"竹竿是否插进凸谷仓：要么竿与仓壁相交，要么竿的一端已经伸进仓里"：

```python
def seg_intersects_poly(P, A, B):
    n = len(P)
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    for i in range(n):
        C, D = P[i], P[(i+1) % n]
        d1 = cross(C, D, A); d2 = cross(C, D, B)
        d3 = cross(A, B, C); d4 = cross(A, B, D)
        if ((d1>0 and d2<0) or (d1<0 and d2>0)) and ((d3>0 and d4<0) or (d3<0 and d4>0)):
            return True
        if d1 == 0 or d2 == 0 or d3 == 0 or d4 == 0:
            if point_in_poly_half(A, P) or point_in_poly_half(B, P):
                return True
    return point_in_poly_half(A, P) or point_in_poly_half(B, P)

def point_in_poly_half(P, poly):
    x, y = P
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % n]
        if (y1 > y) != (y2 > y):
            xint = x1 + (y-y1)*(x2-x1)/(y2-y1) if (y2-y1)!=0 else x1
            if x < xint:
                inside = not inside
    return inside

poly = [(0,0),(4,0),(4,4),(0,4)]
print(seg_intersects_poly(poly, (5,1),(2,2)))
print(seg_intersects_poly(poly, (5,1),(6,1)))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.19.64 例 64：三角形外接圆半径海伦版（洛谷 P2217 变式）⭐⭐
> **知识点**：海伦、外接圆、边角关系｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给三角形三边 a、b、c，求其外接圆半径 R，输出 2 位小数。保证能构成三角形。

**思路**：面积用海伦 S=√(s(s-a)(s-b)(s-c))，外接圆 R = abc/(4S)。

💡 类比"三角桌的外圈围圆桌直径：三边相乘除以四倍面积就是外接圆半径"：

```python
import math

def circumradius(a, b, c):
    s = (a+b+c)/2
    S = math.sqrt(s*(s-a)*(s-b)*(s-c))
    if S == 0:
        return 0.0
    return a*b*c/(4*S)

print(round(circumradius(3,4,5), 2))
print(round(circumradius(6,8,10), 2))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.19.65 例 65：多边形最远顶点对（暴力检查）（洛谷 P2017 变式）⭐⭐
> **知识点**：最远点对、暴力枚举、距离平方｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给 n 个点，求两两距离平方的最大值（最远点对，用于验证旋转卡壳或用压缩）。n≤10^4，坐标 ≤10^6。

**思路**：双重循环枚举点对，维护最大距离平方，并记录是哪对。O(n²) 暴力作基线版本。

💡 类比"量操场两端最远的两根标杆：两两比一遍，记住目前拉得最开的一对"：

```python
def farthest_pair(points):
    n = len(points)
    best = -1
    ip = jp = None
    for i in range(n):
        for j in range(i+1, n):
            d = (points[i][0]-points[j][0])**2 + (points[i][1]-points[j][1])**2
            if d > best:
                best = d
                ip, jp = i, j
    return best, ip, jp

pts = [(0,0),(3,4),(10,0),(0,10),(8,8)]
d,i,j = farthest_pair(pts)
print("距离平方=", d, "点对=", pts[i], pts[j])
```
> **复杂度**：O(n²) 时间，O(1) 空间

---

---
