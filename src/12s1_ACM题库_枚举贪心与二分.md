# 第 12 章 OI/ACM 竞赛：ACM 经典题库（一）

> 本分册覆盖 17.1–17.3（枚举、贪心与二分），共 225 题。
> 返回 [ACM 经典题库总览](./12s_ACM题库.md)。

## 17. ACM 经典题库

### 17.1 枚举与模拟

#### 17.1.1 例 1：鸡兔同笼（POJ 3237）⭐
> **知识点**：暴力枚举、二元一次方程｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：笼中有鸡和兔共 n 只，共有 m 只脚（1≤n,m≤1000）。求鸡与兔各几只，若存在多个解输出任意一组，无解输出 "No answer"。多组测试直到输入结束。

**思路**
由于鸡 2 脚兔 4 脚，可直接枚举鸡的数量，检查脚数是否匹配。

💡 类比"乐高拼车：数了轮子和车子数，逐个假设每辆是三轮车还是自行车，把轮子核算一遍一样"：

<details>
先设鸡 x 只，则兔为 n-x 只，检查 2x+4(n-x)==m。
</details>

```python
import sys

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        n, m = map(int, line.split())
        ans = None
        for x in range(n + 1):          # x 只鸡
            if 2 * x + 4 * (n - x) == m:  # 兔 n-x 只
                ans = (x, n - x)
                break
        if ans is None:
            print("No answer")
        else:
            print(ans[0], ans[1])

if __name__ == "__main__":
    main()
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.1.2 例 2：水仙花数（HDU 2010）⭐
> **知识点**：逐位拆分、暴力枚举｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入区间 [m, n]（100≤m≤n≤999），输出其中所有"水仙花数"（各位数字的立方和等于该数本身），若区间内没有则输出 "no"。多组输入。

**思路**
对区间内每个整数拆出百十个位，检查立方和是否等于自身。

💡 类比"三位密码锁：把三种数字拨盘转遍，看哪个组合正好等于锁面数字"：

```python
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    m, n = map(int, line.split())
    res = []
    for x in range(m, n + 1):
        a = x // 100          # 百位
        b = x // 10 % 10      # 十位
        c = x % 10            # 个位
        if a**3 + b**3 + c**3 == x:
            res.append(str(x))
    print(' '.join(res) if res else "no")
```
> **复杂度**：O(n-m) 时间（每数 O(1)），O(k) 空间（k 为结果个数）

---
#### 17.1.3 例 3：特殊数字串（洛谷 P1098）⭐⭐
> **知识点**：字符串展开、范围枚举｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串展开规则 p1（填充字符大小写/星号）、p2（重复次数）、p3（正序逆序），对含 '-' 的字符串按规则展开。字符串长度≤100。输出展开结果。

**思路**
扫描字符串，遇到 '-' 时判断左右字符是否同为数字或同为字母，并决定是否按规则展开。

💡 类比"复印机设置：设定放大倍数和顺序，把-'两边的字符逐个复制填充进去"：

```python
s = input().strip()
# p1: 1小写 2大写 3星号; p2: 重复次数; p3: 1正序 2逆序（用于字母/数字展开）
p1, p2, p3 = map(int, input().split())
out = []
i = 0
n = len(s)
prev = 0  # 若要同时支持 p3 正逆序
while i < n:
    if s[i] == '-' and 0 < i < n - 1:
        l, r = s[i-1], s[i+1]
        # 只有当同为数字或同为字母且 l<r 时展开
        same = (l.isdigit() and r.isdigit()) or (l.isalpha() and r.isalpha())
        if same and l < r:
            lo = ord(l) + 1
            hi = ord(r)
            if p3 == 2:
                rng = range(hi - 1, lo - 1, -1)
            else:
                rng = range(lo, hi)
            if p1 == 3:                      # 用 * 填充
                out.append('*' * (p2 * (abs(l - r if False else (hi - lo)))))
            else:
                for ch in rng:
                    c = chr(ch)
                    if p1 == 2 and c.islower():
                        c = c.upper()
                    if p1 == 1 and c.isupper():
                        c = c.lower()
                    out.append(c * p2)
            i += 1
        elif l - r + 0 >= 0 and not same:    # 普通减号
            out.append('-')
            i += 1
        else:
            out.append('-')
            i += 1
    else:
        out.append(s[i])
        i += 1
print(''.join(out))
```
> **复杂度**：O(L·p2) 时间，O(L·p2) 空间

---
#### 17.1.4 例 4：数的计数（POJ 3666 同类 / 经典题型）⭐⭐
> **知识点**：递归计数、枚举基底｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n（1≤n≤1000），求满足"每个偶数位数字不超过其左边数字的 n 的数字计数问题"的简单位数枚举。实际处理：统计 1~n 中"数字中 2 出现的次数"。多组数据。

**思路**
逐位统计某数字 d 在 1..n 中出现的次数，按位枚举贡献。

💡 类比"数数投票箱：每到一位就问这一位作为个位/十位能作为某数出现几次，全加起来"：

```python
def count_digit(n, d):
    s = str(n)
    L = len(s)
    total = 0
    for i in range(L):
        hi = int(s[:i]) if i > 0 else 0
        cur = int(s[i])
        lo_len = L - i - 1
        mul = 10 ** lo_len
        # 高位贡献：数字 d 在第 i 位出现的完整块数
        if cur > d:
            total += (hi + 1) * mul
        elif cur == d:
            total += hi * mul + (int(s[i+1:]) + 1 if lo_len else 1)
        else:
            total += hi * mul
        if d == 0 and hi == 0:   # 前导零不计（简化，此处 n 较大可忽略）
            pass
    return total

n = int(input())
print(count_digit(n, 2))
```
> **复杂度**：O(k)=O(log n) 时间，O(1) 空间

---
#### 17.1.5 例 5：蛇形填数（HDU 传声筒 / P1411）⭐⭐
> **知识点**：方向模拟、二维数组｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n（1≤n≤100），输出 n×n 的方阵，从右上角开始按逆时针方向从 1 依次填入 n²。

**思路**
用方向数组模拟蛇形行走，撞到边界或已填就转向。

💡 类比"蜗牛爬饼干盘：从角上绕着圈从外往里一圈圈爬，碰到边就拐弯"：

```python
n = int(input())
a = [[0]*n for _ in range(n)]
# 方向：由于从右上角逆时针，先向左走
dirs = [(0,-1),(1,0),(0,1),(-1,0)]  # 左、下、右、上
x, y = 0, n-1
cur = 1
d = 0
while cur <= n*n:
    a[x][y] = cur
    cur += 1
    nx, ny = x+dirs[d][0], y+dirs[d][1]
    if not (0 <= nx < n and 0 <= ny < n and a[nx][ny] == 0):
        d = (d+1) % 4
        nx, ny = x+dirs[d][0], y+dirs[d][1]
    x, y = nx, ny
for row in a:
    print(' '.join(str(v) for v in row))
```
> **复杂度**：O(n²) 时间，O(n²) 空间

---
#### 17.1.6 例 6：字符串统计找频率（洛谷 P5015 / POJ 常考）⭐
> **知识点**：计数模拟、字典｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一行字符（含空格），输入一个目标字符 c 与一行文本 t，统计 t 中 c 出现的次数（忽略大小写）。

**思路**
遍历文本字符一一比对，不区分大小写。

💡 类比"点兵点将：一个字符一个字符从队伍里认出来是不是你要找的那个人"：

```python
c = input().strip().lower()
t = input().lower()
print(t.count(c))
```
> **复杂度**：O(L) 时间，O(1) 空间

---
#### 17.1.7 例 7：回文数判断与还原（洛谷 P1015）⭐⭐
> **知识点**：进制转换、模拟、高精度思想｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定整数 n 与 m 进制数 s，每次将 s 与其反序相加得到新数，求经过多少步能得到回文数。若超过 30 步输出 "Impossible!"。进制 ≤16。

**思路**
用加法模拟，每步判断当前数是否回文，注意用大数（Python 原生 int）支持任意长度。

💡 类比"照镜子求和：把数字倒过来跟自己加起来，反复直到左右对称，超过 30 次就算失败"：

```python
def to_str(num, base):
    digs = "0123456789ABCDEF"
    if num == 0:
        return "0"
    res = ""
    while num:
        res += digs[num % base]
        num //= base
    return res[::-1]

n = int(input())
s = input().strip()
base = n
num = int(s, base)
for step in range(1, 31):
    rev = int(str(num)[::-1] if str(num) == str(num)[::-1] else to_str(num, base)[::-1], base)
    # 更稳妥：直接从十进制反序
    # 把 num 生成对应进制字符串再反序转回
    st = to_str(num, base)
    rev_s = st[::-1]
    rev_num = int(rev_s, base)
    num = num + rev_num
    if to_str(num, base) == to_str(num, base)[::-1]:
        print("STEP=%d" % step)
        break
else:
    print("Impossible!")
```
> **复杂度**：最坏 30 步，每步 O(len)，总 O(30·len) 时间，O(len) 空间

---
#### 17.1.8 例 8：开关灯问题（洛谷 P1769 变式）⭐⭐
> **知识点**：模拟状态、位运算枚举｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 个开关（1≤n≤20），每个都对应一个状态。给定初始与目标状态，以及每个开关按下会影响哪些灯的矩阵，求最少按几次能达成目标。保证有解。

**思路**
对"第一个按或不按"做枚举，其余开关状态由前一个决定，逐位模拟。

💡 类比"翻转多米诺：开头的板子方向定了，后面的连锁反应就完全确定了，只需试两种开头"：

```python
def solve():
    n = int(input())
    start = list(map(int, input().split()))
    goal = list(map(int, input().split()))
    nxt = [[] for _ in range(n)]
    for i in range(n):
        # 读第 i 个开关影响的行
        nxt[i] = list(map(int, input().split()))
    cur = start[:]
    best = n + 1
    # 该变式为经典思路：枚举首开关状态，前后递推
    # 这里简化为对每个开关做 0/1 尝试的前向模拟（n≤20 用 2^n 枚举更通用）
    from itertools import product
    best = n + 1
    for mask in product(range(2), repeat=n):
        tmp = start[:]
        cnt = 0
        for i in range(n):
            if mask[i]:
                cnt += 1
                # 翻转灯 i
                tmp[i] ^= 1
                for j in nxt[i]:
                    tmp[j] ^= 1
        if tmp == goal:
            best = min(best, cnt)
    print(best)

solve()
```
> **复杂度**：O(2^n·n) 时间，O(n) 空间

---
#### 17.1.9 例 9：约瑟夫环（HDU 3089 变式 / 洛谷 P1996）⭐⭐⭐
> **知识点**：模拟删除、循环取模｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n（1≤n≤100）个人围成一圈，从 1 开始报数，报到 m（≥1）的人出列，求全部出列的顺序。

**思路**
用数组标记剩余的人，指针循环移动统计报数实现。

💡 类比"一圈人抢座位：数到第 m 个就被请出去，剩下的人继续转圈数"：

```python
n, m = map(int, input().split())
alive = [True] * (n + 1)
out = []
idx = 0
left = n
cnt = 0
i = 1
while left:
    if alive[i]:
        cnt += 1
        if cnt == m:
            alive[i] = False
            out.append(i)
            left -= 1
            cnt = 0
    i = i % n + 1
print(' '.join(map(str, out)))
```
> **复杂度**：O(n·m) 时间（最坏），O(n) 空间

---
#### 17.1.10 例 10：报数游戏去重（洛谷 P1387 类比自定义）⭐
> **知识点**：集合去重、枚举｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个整数，去掉其中重复的数字，只保留最先出现的一个，按原顺序输出。

**思路**
用一个 set 记录已出现数字，首次出现即输出。

💡 类比"盖章打卡机：盖过章的名字不再放进来，只记第一次"：

```python
n = int(input())
nums = list(map(int, input().split()))
seen = set()
res = []
for x in nums:
    if x not in seen:
        seen.add(x)
        res.append(x)
print(' '.join(map(str, res)))
```
> **复杂度**：O(n) 时间，O(n) 空间
#### 17.1.11 例 11：模拟计算器（HDU 1512 变式 / 洛谷 P1938）⭐⭐
> **知识点**：表达式模拟、栈｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：输入一个只含 + - * / 和括号的合法表达式，求值结果（保证能整除，结果整数）。表达式长度≤200。

**思路**
用双栈（数字栈、符号栈）处理运算符优先级，遇右括号出栈计算。

💡 类比"排队结账：数字排队，遇到高优先级符号先插队算掉，遇到括号就整段清账"：

```python
def calc(s):
    s = s.replace(' ', '')
    prio = {'+':1, '-':1, '*':2, '/':2}
    nums = []
    ops = []
    i = 0
    while i < len(s):
        if s[i].isdigit() or (s[i]=='-' and (i==0 or s[i-1] in '+-*/(')):
            j = i
            if s[i] in '+-':
                j += 1
            while j < len(s) and s[j].isdigit():
                j += 1
            nums.append(int(s[i:j]))
            i = j
            continue
        if s[i] == '(':
            ops.append(s[i])
        elif s[i] == ')':
            while ops[-1] != '(':
                b = nums.pop(); a = nums.pop(); o = ops.pop()
                nums.append(apply(a, b, o))
            ops.pop()
        else:
            while ops and ops[-1] != '(' and prio[ops[-1]] >= prio[s[i]]:
                b = nums.pop(); a = nums.pop(); o = ops.pop()
                nums.append(apply(a, b, o))
            ops.append(s[i])
        i += 1
    while ops:
        b = nums.pop(); a = nums.pop(); o = ops.pop()
        nums.append(apply(a, b, o))
    return nums[0]

def apply(a, b, o):
    if o == '+': return a+b
    if o == '-': return a-b
    if o == '*': return a*b
    return a//b

s = input().strip()
print(calc(s))
```
> **复杂度**：O(L) 时间，O(L) 空间

---
#### 17.1.12 例 12：日期推算（洛谷 P2613 变式 / 经典日期题）⭐⭐
> **知识点**：日期模拟、闰年判断｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个日期(y,m,d) 与一个整数 k（可为负），求该日期前/后 k 天对应的日期。年份 1≤y≤9999。

**思路**
把日期换算成"绝对天数"，加 k 后再转回日期，注意闰年与二月天数。

💡 类比"日历翻页：把日子搓成一条线，快进 k 天再一格格翻日历落回某页"：

```python
M = [0,31,28,31,30,31,30,31,31,30,31,30,31]
def leap(y):
    return y%400==0 or (y%4==0 and y%100!=0)
def days_in(y, m):
    if m==2 and leap(y):
        return 29
    return M[m]
def to_abs(y, m, d):
    total = 0
    for yy in range(1, y):
        total += 366 if leap(yy) else 365
    for mm in range(1, m):
        total += days_in(y, mm)
    return total + d
def from_abs(a):
    y = 1
    while True:
        dim = 366 if leap(y) else 365
        if a <= dim:
            break
        a -= dim
        y += 1
    m = 1
    while a > days_in(y, m):
        a -= days_in(y, m)
        m += 1
    return y, m, a

y, m, d = map(int, input().split())
k = int(input())
a = to_abs(y, m, d) + k
yy, mm, dd = from_abs(a)
print(yy, mm, dd)
```
> **复杂度**：O(y) 时间（最坏），O(1) 空间

---
#### 17.1.13 例 13：乘法口诀三角形（自定义经典）⭐
> **知识点**：双层循环、格式化输出｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n（1≤n≤9），输出 n 行的乘法口诀下三角，形如 `1*1=1` 每格等宽。

**思路**
外层 i 从 1 到 n，内层 j 从 1 到 i，输出 `j*i=j乘i`。

💡 类比"搭金字塔：第几层就摆几个积木，一层层往上叠"：

```python
n = int(input())
for i in range(1, n+1):
    row = []
    for j in range(1, i+1):
        row.append(f"{j}*{i}={i*j}")
    print(' '.join(row))
```
> **复杂度**：O(n²) 时间，O(1) 空间

---
#### 17.1.14 例 14：括号匹配（洛谷 P1739）⭐⭐
> **知识点**：栈模拟、括号配对｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个只含 ( ) 的字符串（长度≤100），判断括号是否完全匹配。

**思路**
用栈/计数器遇 ( 加一，遇 ) 减一，中途不能为负，最后为 0。

💡 类比"玩跷跷板：左括号把左边压下去，右括号把右边翘回来，结束后两边正好平衡"：

```python
s = input().strip()
cnt = 0
ok = True
for ch in s:
    if ch == '(':
        cnt += 1
    elif ch == ')':
        cnt -= 1
        if cnt < 0:
            ok = False
            break
if cnt != 0:
    ok = False
print("YES" if ok else "NO")
```
> **复杂度**：O(L) 时间，O(1) 空间

---
#### 17.1.15 例 15：统计字符出现次数模拟（洛谷 P1553）⭐
> **知识点**：计数、字符串处理｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给一行文本，统计其中每个小写字母出现次数，只输出出现过的字母及其次数。

**思路**
用计数数组统计，遍历 a~z 输出非零项。

💡 类比"发问卷：每见到一个字母就在对应的格子打一个勾"：

```python
s = input()
cnt = [0]*26
for ch in s:
    if 'a' <= ch <= 'z':
        cnt[ord(ch)-97] += 1
for i in range(26):
    if cnt[i]:
        print(chr(97+i), cnt[i])
```
> **复杂度**：O(L) 时间，O(1) 空间

---
#### 17.1.16 例 16：数字三角形最小和（经典枚举）⭐⭐
> **知识点**：三角形遍历、路径枚举（小规模）｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n 与一个数字三角形（1≤n≤10），从顶到底每次可走到下方或右下方，求路径上数字之和的最小值。

**思路**
小 n 可枚举所有路径，或用简单 dp 递推；这里用逐层累加最小。

💡 类比"下山选岔路：每一步都挑数字更小的一边，从下往上推最优"：

```python
n = int(input())
a = [list(map(int, input().split())) for _ in range(n)]
# 从倒数第二层向上累加
for i in range(n-2, -1, -1):
    for j in range(i+1):
        a[i][j] += min(a[i+1][j], a[i+1][j+1])
print(a[0][0])
```
> **复杂度**：O(n²) 时间，O(n²) 空间

---
#### 17.1.17 例 17：汉字笔画哈夫曼（自定义/洛谷 P3099）⭐
> **知识点**：排序、配对模拟｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n 个整数，将它们两两配对，每次配对代价为两数之和，累加所有代价，求可能的最小总代价（贪心近似演示，此处直接排序求法）。

**思路**
排序后相邻相加是简单演示；完整最优为哈夫曼，此处用每次取最小两个合并。

💡 类比"合并小沙堆：每次先并两个最小的堆，越小的越早并越省钱"：

```python
import heapq
n = int(input())
a = list(map(int, input().split()))
heapq.heapify(a)
total = 0
while len(a) > 1:
    x = heapq.heappop(a)
    y = heapq.heappop(a)
    s = x + y
    total += s
    heapq.heappush(a, s)
print(total)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.1.18 例 18：矩阵转置模拟（自定义经典）⭐
> **知识点**：二维数组访问、遍历模拟｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n,m 与 n×m 矩阵，输出其转置 m×n 矩阵。

**思路**
按列优先遍历，行变列列变行。

💡 类比"旋转书架：把横着放的格子竖起来，原来的一行变成一列"：

```python
n, m = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]
for j in range(m):
    print(' '.join(str(a[i][j]) for i in range(n)))
```
> **复杂度**：O(nm) 时间，O(nm) 空间

---
#### 17.1.19 例 19：汉诺塔模拟（常规经典）⭐⭐
> **知识点**：递归模拟、分治｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n（1≤n≤10），输出把 n 个盘子从 A 移到 C 的具体移动步骤（格式 `a->b`）。

**思路**
递归：先把上面 n-1 个移到辅助柱，再把最底层移到目标柱，再移回上面 n-1 个。

💡 类比"端盘子过河：要端最大那盘，得先把上面的都挪到旁边，端完再挪回来"：

```python
n = int(input())
def hanoi(k, a, b, c):  # 将 k 个从 a 经 b 移到 c
    if k == 1:
        print(f"{a}->{c}")
        return
    hanoi(k-1, a, c, b)
    print(f"{a}->{c}")
    hanoi(k-1, b, a, c)
hanoi(n, 'a', 'b', 'c')
```
> **复杂度**：O(2^n) 时间，O(n) 空间

---
#### 17.1.20 例 20：数列逆序统计（洛谷 P1908）⭐⭐
> **知识点**：归并思想枚举逆序对｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个整数（1≤n≤500），求逆序对个数（i<j 且 a[i]>a[j]）。

**思路**
小规模可暴力双层循环统计。

💡 类比"排队插队检查：从左往右每个人回头数一数身后有多少比自己小的先换位置"：

```python
n = int(input())
a = list(map(int, input().split()))
c = 0
for i in range(n):
    for j in range(i+1, n):
        if a[i] > a[j]:
            c += 1
print(c)
```
> **复杂度**：O(n²) 时间，O(1) 空间
#### 17.1.21 例 21：进制转换（HDU 2031）⭐⭐
> **知识点**：短除法、进制表示｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：输入两个整数 n 与 b（2≤b≤16），输出 n 的 b 进制表示（负数带负号，超过10用大写字母）。多组数据。

**思路**
用短除法反复取余，倒序输出，注意符号。

💡 类比"拆零钱：不断用新面额整除再取余，把零头一串串记下来倒着念"：

```python
import sys
dig = "0123456789ABCDEF"
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    n, b = map(int, line.split())
    neg = n < 0
    n = abs(n)
    if n == 0:
        print("0")
        continue
    res = ""
    while n:
        res += dig[n % b]
        n //= b
    print(("-" if neg else "") + res[::-1])
```
> **复杂度**：O(log_b n) 时间，O(1) 空间

---
#### 17.1.22 例 22：最大公约数模拟辗转相除（HDU 1019 前奏）⭐
> **知识点**：辗转相除、gcd｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入两个正整数 a,b（≤10^9），求它们的最大公约数与最小公倍数。

**思路**
辗转相除求 gcd，最小公倍数为 a*b//gcd。

💡 类比"拆长绳：把两根绳子互相折着减，最后拉直的公共段就是最大公约"：

```python
a, b = map(int, input().split())
x, y = a, b
while y:
    x, y = y, x % y
g = x
lcm = a // g * b
print(g, lcm)
```
> **复杂度**：O(log min(a,b)) 时间，O(1) 空间

---
#### 17.1.23 例 23：数字反转输出（洛谷 P1307）⭐
> **知识点**：取模逆序、去前导零｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入一个不超过|10^9|的整数 n，将其反转输出正数部分（去掉前导零），负数保留负号。

**思路**
转为字符去负号反转，去前导零后拼回。

💡 类比"倒着念号码：把数字当一长串倒着读一遍，开头的 0 省略"：

```python
s = input().strip()
neg = s[0] == '-'
if neg:
    s = s[1:]
rev = s[::-1].lstrip('0') or '0'
print("-" + rev if neg else rev)
```
> **复杂度**：O(len) 时间，O(1) 空间

---
#### 17.1.24 例 24：分数序列求和（HDU 2018）⭐
> **知识点**：递推模拟、分数累加｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：有一分数序列 2/1,3/2,5/3,...，分子分母分别为前一项的和，求前 n 项之和，保留两位小数。

**思路**
斐波那契式递推分子分母，累加并求和。

💡 类比"滚雪球加法：分子分母都是前两个数相加滚出来，一项项累加"：

```python
n = int(input())
a, b = 2, 1  # 分子、分母
s = 0.0
for _ in range(n):
    s += a / b
    a, b = a + b, a
print("%.2f" % s)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.1.25 例 25：杨辉三角输出（洛谷 P5732）⭐
> **知识点**：组合递推、二维模拟｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n（1≤n≤30），输出杨辉三角前 n 行，每行相邻数间以空格分隔。

**思路**
每行第一个与最后一个为 1，中间由上一行相邻和得到。

💡 类比"搭砖墙：每块砖压着下面两块砖，两头是 1"：

```python
n = int(input())
tri = []
for i in range(n):
    row = [1]*(i+1)
    for j in range(1, i):
        row[j] = tri[i-1][j-1] + tri[i-1][j]
    tri.append(row)
    print(' '.join(map(str, row)))
```
> **复杂度**：O(n²) 时间，O(n²) 空间

---
#### 17.1.26 例 26：字符图形旋转（自定义经典）⭐
> **知识点**：二维数组变换、遍历重排｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n,m 与 n×m 的 '#'/'.' 图案，输出逆时针旋转 90° 的 m×n 图案。

**思路**
旋转后新位置 (i,j) 对应原 (m-1-j, i)，逐格读取。

💡 类比"转魔方看侧脸：把整个图案转一下，行列就互换了"：

```python
n, m = map(int, input().split())
g = [list(input().strip()) for _ in range(n)]
for j in range(m-1, -1, -1):
    print(''.join(g[i][j] for i in range(n)))
```
> **复杂度**：O(nm) 时间，O(nm) 空间

---
#### 17.1.27 例 27：模拟电梯调度（POJ 常考变式）⭐⭐
> **知识点**：状态模拟、绝对值累加｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：电梯初始在 0 层，给定一串目标楼层序列，每上一/下一层耗 1 单位，求总耗时（含每经过一层 1 秒）。

**思路**
维护当前楼层，累加相邻目标楼层之差的绝对值。

💡 类比"查楼层牌：从这一层走到下一层要多少级台阶，把每一段加起来"：

```python
a = list(map(int, input().split()))
n = a[0]
cur = 0
total = 0
for i in range(1, n+1):
    total += abs(a[i] - cur)
    cur = a[i]
print(total)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.1.28 例 28：回文数范围统计（自定义）⭐
> **知识点**：回文判断、区间枚举｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入区间 [l,r]（1≤l≤r≤10^6），统计其中所有回文数的个数。

**思路**
遍历区间，将数字转为字符串判断是否回文。

💡 类比"照镜子数人：每个数都站到镜子前看看左右是否对称"：

```python
l, r = map(int, input().split())
cnt = 0
for x in range(l, r+1):
    s = str(x)
    if s == s[::-1]:
        cnt += 1
print(cnt)
```
> **复杂度**：O((r-l)·k) 时间，O(k) 空间

---
#### 17.1.29 例 29：单词出现次数（洛谷 P1308）⭐⭐
> **知识点**：字符串分割、计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定目标单词与一篇文章，统计该单词在文章中作为完整单词出现的次数，并输出第一次出现的下标（从0计），没有输出 -1。忽略大小写。

**思路**
把所有字母统一小写并加空格边界，按空格分割匹配。

💡 类比"在杂志里找词：把页面上所有词切成一个个念，看哪个和要找的一样"：

```python
word = input().strip().lower()
text = (' ' + input().lower() + ' ')
# 统一首尾加空格，保证按单词匹配
target = ' ' + word + ' '
idx = text.find(target)
if idx == -1:
    print(-1)
else:
    count = text.count(target)
    print(count, idx)
```
> **复杂度**：O(L) 时间，O(L) 空间

---
#### 17.1.30 例 30：序列最大连续和（POJ 2479 变式）⭐⭐
> **知识点**：前缀和、枚举区间｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个整数（可负），求最大连续子段和。

**思路**
线性扫描，维护以当前位置结尾的最大和 cur，更新全局 best。

💡 类比"算账户流水：一直记账，亏到负了就清零重来，记下历史最高结余"：

```python
n = int(input())
a = list(map(int, input().split()))
cur = 0
best = -10**18
for x in a:
    cur = max(x, cur + x)
    best = max(best, cur)
print(best)
```
> **复杂度**：O(n) 时间，O(1) 空间
#### 17.1.31 例 31：小学生算数进位次数（洛谷 P1036 变式）⭐⭐
> **知识点**：逐位相加、进位模拟｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个非负大整数（≤10^100），模拟小学竖式加法，求加法过程中产生进位的次数。

**思路**
从个位逐位相加，维护进位，统计进位的次数。

💡 类比"竖式加法课：一位位加起来，超过 9 就进一，数一数进过几次位"：

```python
a = input().strip()[::-1]
b = input().strip()[::-1]
if len(a) < len(b):
    a, b = b, a
b = b + '0'*(len(a)-len(b))
carry = 0
cnt = 0
for i in range(len(a)):
    s = int(a[i]) + int(b[i]) + carry
    if s >= 10:
        cnt += 1
        carry = 1
    else:
        carry = 0
print(cnt)
```
> **复杂度**：O(L) 时间，O(1) 空间

---
#### 17.1.32 例 32：导弹拦截模拟（洛谷 P1020 变式）⭐
> **知识点**：单调序列维护、贪心模拟｜**难度**：⭐｜**类型**：ACM/竞赛（简化版）
> **题目描述**：给定一串导弹高度序列（n≤1000），一套系统发射高度单调不升，求最多能拦截多少枚（简化：只求最长不升子序列长度）。

**思路**
用一个递减缓冲维护可用高度，逐个接入最接近的可用高度。

💡 类比"贴邮票：每枚导弹尽量放能接住而高度最接近的库里存着，保证以后能装更多"：

```python
a = list(map(int, input().split()))
n = len(a)
dp = [1]*n
for i in range(n):
    for j in range(i):
        if a[j] >= a[i]:
            dp[i] = max(dp[i], dp[j]+1)
print(max(dp))
```
> **复杂度**：O(n²) 时间，O(n) 空间

---
#### 17.1.33 例 33：含重复字符去重统计（自定义）⭐
> **知识点**：字典计数、集合｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个字符串（长度≤1000），输出它含多少种不同的小写字母，并按出现次数降序（相同按字母序）排列各字母。

**思路**
统计每种字母次数，然后排序输出。

💡 类比"投票统计：给每个候选字母记票，最后排名"：

```python
s = input()
c = {}
for ch in s:
    if 'a' <= ch <= 'z':
        c[ch] = c.get(ch, 0) + 1
items = sorted(c.items(), key=lambda x: (-x[1], x[0]))
print(len(items))
for k, v in items:
    print(k, v)
```
> **复杂度**：O(L + K log K) 时间，O(K) 空间

---
#### 17.1.34 例 34：螺旋矩阵（洛谷 P2239）⭐⭐
> **知识点**：方向模拟、边界控制｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n（1≤n≤100），从 1 开始顺时针螺旋填入 n×n 矩阵，输出矩阵。

**思路**
用方向数组，越界或已填即转向，依次填 n² 个数。

💡 类比"卷纸筒：沿着四边一圈圈往内卷，碰到新边界就拐弯"：

```python
n = int(input())
a = [[0]*n for _ in range(n)]
d = [(0,1),(1,0),(0,-1),(-1,0)]
x = y = 0
di = 0
for v in range(1, n*n+1):
    a[x][y] = v
    nx, ny = x+d[di][0], y+d[di][1]
    if not (0<=nx<n and 0<=ny<n and a[nx][ny]==0):
        di = (di+1) % 4
        nx, ny = x+d[di][0], y+d[di][1]
    x, y = nx, ny
for row in a:
    print(' '.join(map(str, row)))
```
> **复杂度**：O(n²) 时间，O(n²) 空间

---
#### 17.1.35 例 35：模拟收银找零（自定义）⭐
> **知识点**：整除取模、纸币张数模拟｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定应付款 p 与面额面值（100,50,20,10,5,2,1），求最少用几张纸币使顾客支付刚好 p。

**思路**
从大面额到小面额尽量多取。

💡 类比"凑钱找零：先用大票子，剩下的零头再用小票补"：

```python
p = int(input())
vals = [100,50,20,10,5,2,1]
cnt = 0
for v in vals:
    cnt += p // v
    p %= v
print(cnt)
```
> **复杂度**：O(7) 时间，O(1) 空间

---
#### 17.1.36 例 36：矩阵乘法（洛谷 P1990）⭐⭐
> **知识点**：三重循环、矩阵运算｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 a×b 矩阵 A 与 b×c 矩阵 B，输出 A*B（结果矩阵）。各维≤100，元素≤100。

**思路**
标准矩阵乘法三重循环累加。

💡 类比"成绩换算表：把每科的分数按权重表挨个乘起来再相加"：

```python
a, b, c = map(int, input().split())
A = [list(map(int, input().split())) for _ in range(a)]
B = [list(map(int, input().split())) for _ in range(b)]
C = [[0]*c for _ in range(a)]
for i in range(a):
    for k in range(b):
        if A[i][k]:
            for j in range(c):
                C[i][j] += A[i][k] * B[k][j]
for row in C:
    print(' '.join(map(str, row)))
```
> **复杂度**：O(abc) 时间，O(ac) 空间

---
#### 17.1.37 例 37：键盘键入差一行统计（自定义）⭐
> **知识点**：字符映射、模拟比对｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两串等长字符（仅含小写字母），计算对应位置上不同的字符个数（即汉明距离）。

**思路**
逐位比较，统计不同。

💡 类比"比对两页抄错的作业：一格格看是否完全一样"：

```python
a = input().strip()
b = input().strip()
print(sum(1 for x, y in zip(a, b) if x != y))
```
> **复杂度**：O(L) 时间，O(1) 空间

---
#### 17.1.38 例 38：模拟链表插入排序（自定义）⭐⭐
> **知识点**：链表模拟、插入排序｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个整数，用"依次插入到一个已排序序列中"的方式模拟插入排序，输出每轮插入后的序列。

**思路**
维护一个有序列表，每轮用二分或线性找到插入位置并插入。

💡 类比"扑克理牌：每摸一张牌，就插到手里已排好序的牌堆正确位置"：

```python
n = int(input())
a = list(map(int, input().split()))
s = []
for x in a:
    i = 0
    while i < len(s) and s[i] < x:
        i += 1
    s.insert(i, x)
    print(' '.join(map(str, s)))
```
> **复杂度**：O(n²) 时间，O(n) 空间

---
#### 17.1.39 例 39：超级楼梯组合数（HDU 2041）⭐⭐
> **知识点**：递推模拟、斐波那契｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：每次可上 1 级或 2 级台阶，问从第 0 级到第 n 级共有多少种走法（n≤40）。

**思路**
f(n)=f(n-1)+f(n-2)，递推计算即可。

💡 类比"跳石阶：到了这块石头，上一格或上两格来的情况都算一次"：

```python
n = int(input())
if n <= 1:
    print(1)
else:
    a, b = 1, 1
    for _ in range(2, n+1):
        a, b = b, a+b
    print(b)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.1.40 例 40：字符块查找（自定义）⭐
> **知识点**：字符串匹配、朴素查找｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定主串 s 与模式串 p（均在 ASCII 或小写），输出 p 在 s 中首次出现的下标，未出现输出 -1。

**思路**
朴素的逐位置滑动比较。

💡 类比"在抽屉里翻钥匙：从每格开始往后比对钥匙的形状是否吻合"：

```python
s = input().strip()
p = input().strip()
for i in range(len(s)-len(p)+1):
    if s[i:i+len(p)] == p:
        print(i)
        break
else:
    print(-1)
```
> **复杂度**：O(L·M) 时间，O(1) 空间
#### 17.1.41 例 41：百钱买百鸡（HDU 经典）⭐⭐
> **知识点**：暴力枚举、不等式优化｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：公鸡 5 元，母鸡 3 元，小鸡 1/3 元一只。用 100 元买恰好 100 只鸡，输出所有方案（x 公鸡 y 母鸡 z 小鸡）。

**思路**
枚举公鸡数与母鸡数，由钱数反推小鸡，检查数量与整除。

💡 类比"分装混合糖果：前面两类定了，第三类就锁定了，只需核对钱数"：

```python
res = []
for x in range(0, 20+1):
    for y in range(0, 34):
        z = 100 - x - y
        if z >= 0 and 5*x + 3*y + z/3 == 100 and z % 3 == 0:
            res.append((x, y, z))
for r in res:
    print(r[0], r[1], r[2])
```
> **复杂度**：O(21·34) 时间，O(1) 空间

---
#### 17.1.42 例 42：进制加法回文步数（自定义）⭐⭐⭐
> **知识点**：大数加法模拟、进制回文｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个大十进制整数 s（长度≤100），每一步把它与其十进制反序相加得到新数（可能超过 100 位），问最少步数能得到回文数。

**思路**
用字符串大数加法，每次判断是否回文，直到找到或步数超限。

💡 类比"镜像加法：把数字照镜子加上自己，一直加到左右对称为止"：

```python
def add_str(a, b):
    a, b = a[::-1], b[::-1]
    if len(a) < len(b):
        a, b = b, a
    b = b + '0'*(len(a)-len(b))
    carry = 0
    res = ''
    for i in range(len(a)):
        s = int(a[i]) + int(b[i]) + carry
        res += str(s % 10)
        carry = s // 10
    if carry:
        res += str(carry)
    return res[::-1]

s = input().strip()
for step in range(1, 100):
    if s == s[::-1]:
        print(step-1)
        break
    s = add_str(s, s[::-1])
else:
    print(-1)
```
> **复杂度**：最多 100 步，每步 O(L)，O(L) 空间

---
#### 17.1.43 例 43：方块消除连续段计数（自定义）⭐⭐
> **知识点**：扫描线、连续段模拟｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 0/1 数组，求相邻且值相同的连续段数量（例如 0 1 1 0 0 为 3 段）。

**思路**
依次比较当前元素与前一个，不同则段数加一。

💡 类比"数彩虹条纹：颜色一换就算一条新带子"：

```python
a = list(map(int, input().split()))
cnt = 1 if a else 0
for i in range(1, len(a)):
    if a[i] != a[i-1]:
        cnt += 1
print(cnt)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.1.44 例 44：有趣的数字三角形打印（自定义）⭐
> **知识点**：循环控制、格式化｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n（1≤n≤9），输出按 1..n 排列交叉的数字菱形（每行递增到 n 再递减）。

**思路**
对每行中心位置，从中心向两边对称填入数字。

💡 类比"搭数字塔：中间最高，两侧对称阶梯下降"：

```python
n = int(input())
for i in range(1, n+1):
    nums = list(range(1, n+1))
    line = [str(x) for x in (nums[:i] + nums[i-2::-1])]
    print(''.join(' ' + x for x in line))
```
> **复杂度**：O(n²) 时间，O(n) 空间

---
#### 17.1.45 例 45：模拟冒泡排序轮数（自定义）⭐⭐
> **知识点**：冒泡排序、交换计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个整数，用冒泡排序对 1..n 排列排序，问需要完整进行多少次外层轮次才能不再发生交换。

**思路**
每一轮扫描相邻元素，若无任何交换则提前结束，统计完成轮数。

💡 类比"水底气泡：每趟小心地往上冒一次泡，直到一趟下来水面毫无动静"：

```python
n = int(input())
a = list(map(int, input().split()))
res = 0
for i in range(n-1):
    swapped = False
    for j in range(n-1-i):
        if a[j] > a[j+1]:
            a[j], a[j+1] = a[j+1], a[j]
            swapped = True
    res += 1
    if not swapped:
        break
print(res)
```
> **复杂度**：O(n²) 时间，O(1) 空间

---
#### 17.1.46 例 46：字符串压缩（洛谷 P1925）⭐
> **知识点**：连续段压缩、遍历｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个字符串（长度≤1000），将连续相同的字符压缩为"字符+次数"，如 aabbb→a2b3，输出压缩结果。

**思路**
扫描统计连续相同字符的长度并输出。

💡 类比"打包快递：一样的货摞一起写个数，不必一件件写"：

```python
s = input().strip()
res = []
i = 0
while i < len(s):
    j = i
    while j < len(s) and s[j] == s[i]:
        j += 1
    res.append(s[i] + str(j-i))
    i = j
print(''.join(res))
```
> **复杂度**：O(L) 时间，O(L) 空间

---
#### 17.1.47 例 47：分数转小数循环节（洛谷 P1403 变式）⭐⭐⭐
> **知识点**：长除法、循环节检测｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定分子 a 与分母 b（正整数，≤10^5），输出 a/b 的小数形式，无限循环部分用括号标出。

**思路**
用长除法记录每次的余数位置，遇到重复余数即发现循环节。

💡 类比"报摊循环广播：记下每个余数出现过的位置，一旦重复就说明要开始无限循环"：

```python
a, b = map(int, input().split())
int_part = str(a // b)
a %= b
if a == 0:
    print(int_part)
else:
    seen = {}
    frac = ''
    i = 0
    while a != 0:
        if a in seen:
            idx = seen[a]
            frac = frac[:idx] + '(' + frac[idx:] + ')'
            break
        seen[a] = i
        a *= 10
        frac += str(a // b)
        a %= b
        i += 1
    print(int_part + '.' + frac)
```
> **复杂度**：最坏 O(b) 时间，O(b) 空间

---
#### 17.1.48 例 48：进制中某数字计数（自定义）⭐⭐
> **知识点**：短除法统计、数字位遍历｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：统计 1 到 n 的所有整数中，十进制数字 d 出现的总次数。

**思路**
对每个数用取模短除法统计各位数字。

💡 类比"抱数字宝宝：把 1 到 n 每个数拆成一位位，看每位是不是 d"：

```python
n, d = map(int, input().split())
cnt = 0
for x in range(1, n+1):
    while x:
        if x % 10 == d:
            cnt += 1
        x //= 10
print(cnt)
```
> **复杂度**：O(n·k) 时间，O(1) 空间

---
#### 17.1.49 例 49：模拟银行叫号队列（自定义）⭐⭐
> **知识点**：队列模拟、入队出队｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：初始队列编号 1..n 依次等待。给定操作序列：1 表示队首出队并输出其编号，2 x 表示把 x 排到队尾。输出所有出队编号。

**思路**
用 list 或 collections.deque 模拟队首出队与队尾加入。

💡 类比"排队点餐：前面办完就出队叫号，新来的排到末尾"：

```python
from collections import deque
n = int(input())
q = deque(range(1, n+1))
for _ in range(n):
    op = input().split()
    if op[0] == '1':
        print(q.popleft())
    else:
        q.append(int(op[1]))
```
> **复杂度**：O(n) 时间，O(n) 空间

---
#### 17.1.50 例 50：全排列之字典序下一个（洛谷 P1706）⭐⭐⭐
> **知识点**：排列枚举、字典序算法｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个 1..n 的排列（n≤9），求比它字典序大的下一个排列，若已是最大则输出 "No next"。

**思路**
从后往前找第一个下降位置，再在其后找最小大于它的数交换，并反转后缀。

💡 类比"调台换节目：找到可升的档位，把后面重新排成最小字典序"：

```python
a = list(map(int, input().split()))
n = len(a)
i = n - 2
while i >= 0 and a[i] >= a[i+1]:
    i -= 1
if i < 0:
    print("No next")
else:
    j = n - 1
    while a[j] <= a[i]:
        j -= 1
    a[i], a[j] = a[j], a[i]
    a[i+1:] = a[i+1:][::-1]
    print(' '.join(map(str, a)))
```
> **复杂度**：O(n) 时间，O(1) 空间
#### 17.1.51 例 51：算术表达式结果为零（自定义）⭐⭐
> **知识点**：递推生成、表达式枚举｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 1..n（n≤7），在相邻数字间插入 +、- 或拼出多位数，求所有计算结果为 0 的表达式。

**思路**
用递归枚举每个数字之间的符号（空格表示拼接），回溯求和。

💡 类比"拼算式闯关：试遍所有插入加减或拼接的方式，看哪种能等于零"：

```python
n = int(input())
res = []
def dfs(x, path):
    if x > n:
        expr = ''.join(path)
        if eval(expr.replace(' ', '')) == 0:
            res.append(expr)
        return
    for op in ['+', '-', ' ']:
        dfs(x+1, path + [op, str(x)])

dfs(2, [str(1)])
for e in res:
    print(e.replace(' ', ''))
```
> **复杂度**：O(3^n·n) 时间，O(n) 空间

---
#### 17.1.52 例 52：乌龟爬行距离（自定义）⭐
> **知识点**：循环累加、模拟判断｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：乌龟每小时爬 a 米，爬满 v 小时后要休息 1 小时不前进。给定总路程 L 与 a、v，求到达终点所需的小时数（不足一小时按一小时计）。

**思路**
累加每小时前进量，不足整小时则补整。

💡 类比"长途司机歇车：开几小时歇一小时，一段段加起来看几天到"：

```python
L, a, v = map(int, input().split())
d = 0
h = 0
while d < L:
    for _ in range(v):
        h += 1
        d += a
        if d >= L:
            break
    if d < L:
        h += 1  # 休息 1 小时
print(h)
```
> **复杂度**：O(L/a) 时间，O(1) 空间

---
#### 17.1.53 例 53：回文日期统计（自定义）⭐⭐
> **知识点**：日期模拟、回文判断｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个日期（YYYYMMDD 格式），统计区间内有多少个"回文日期"（如 20200202 是回文）。

**思路**
日期格式固定 8 位数字，直接判断字符串是否为回文。

💡 类比"节日翻手册：把每天日期写成 8 位数看是否左右对称"：

```python
s1 = input().strip()
s2 = input().strip()
cnt = 0
y1, m1, d1 = int(s1[:4]), int(s1[4:6]), int(s1[6:])
y2, m2, d2 = int(s2[:4]), int(s2[4:6]), int(s2[6:])
M = [0,31,28,31,30,31,30,31,31,30,31,30,31]
def leap(y):
    return y%400==0 or (y%4==0 and y%100!=0)
def dom(y, m):
    if m==2 and leap(y):
        return 29
    return M[m]
y, m, d = y1, m1, d1
while (y, m, d) <= (y2, m2, d2):
    s = f"{y:04d}{m:02d}{d:02d}"
    if s == s[::-1]:
        cnt += 1
    d += 1
    if d > dom(y, m):
        d = 1
        m += 1
        if m > 12:
            m = 1
            y += 1
print(cnt)
```
> **复杂度**：O(区间天数) 时间，O(1) 空间

---
#### 17.1.54 例 54：数字各位之和递归计算（自定义）⭐
> **知识点**：递归或循环求和｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定正整数 n（≤10^9），不断求各位数字之和直到结果是一位数，输出该一位数。

**思路**
循环将各位相加，直到 n<10。

💡 类比"果汁浓缩：把每一位加一块，浓缩到只剩一位数字为止"：

```python
n = int(input())
while n >= 10:
    n = sum(map(int, str(n)))
print(n)
```
> **复杂度**：O(k·log n) 时间，O(1) 空间

---
#### 17.1.55 例 55：约瑟夫变式最后存活（HDU 2925）⭐⭐⭐
> **知识点**：逆推公式、数学模拟｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 人围成一圈，每数到 m 出列，求最后留下的那个人的编号（从 1 计）。

**思路**
用逆推公式从 1 人向上反推最后编号。

💡 类比"倒推幸存者：从只剩一人向上加回来，每一步都平移再加 1"：

```python
n, m = map(int, input().split())
pos = 0
for i in range(1, n+1):
    pos = (pos + m) % i
print(pos + 1)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.1.56 例 56：模拟归并排序逆序对（洛谷 P1908 进阶）⭐⭐⭐
> **知识点**：归并排序、逆序对计数｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个整数（n≤100000），统计逆序对个数（大数在前小数在后）。结果用 64 位整数输出。

**思路**
用归并排序，在合并时统计跨左右两半的逆序对。

💡 类比"分拣账单：把左右两半排好序合并，一有右边的更小就说明有逆序"：

```python
import sys
def merge_sort(a):
    cnt = 0
    if len(a) > 1:
        mid = len(a)//2
        l = a[:mid]; r = a[mid:]
        cnt += merge_sort(l)
        cnt += merge_sort(r)
        i = j = k = 0
        while i < len(l) and j < len(r):
            if l[i] <= r[j]:
                a[k] = l[i]; i += 1
            else:
                a[k] = r[j]; cnt += len(l) - i; j += 1
            k += 1
        while i < len(l):
            a[k] = l[i]; i += 1; k += 1
        while j < len(r):
            a[k] = r[j]; j += 1; k += 1
    return cnt

n = int(sys.stdin.readline())
a = list(map(int, sys.stdin.readline().split()))
print(merge_sort(a))
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.1.57 例 57：实现集合运算（自定义）⭐
> **知识点**：集合运算、去重排序｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个集合 A、B（元素为整数，无序），分别输出它们的并、交、差集（排序后输出）。

**思路**
用 Python 集合运算，再取排序。

💡 类比"整理两抽屉玩具：把两份清单并一起、交叉比对、算谁多谁少"：

```python
na, nb = map(int, input().split())
a = set(map(int, input().split()))
b = set(map(int, input().split()))
print(' '.join(map(str, sorted(a | b))))
print(' '.join(map(str, sorted(a & b))))
print(' '.join(map(str, sorted(a - b))))
```
> **复杂度**：O((na+nb) log) 时间，O(na+nb) 空间

---
#### 17.1.58 例 58：运动会入场方阵（自定义）⭐
> **知识点**：图形模拟、矩阵填充｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n，输出 n×n 的 '#' 边框（只画边缘一周），内部为空。

**思路**
逐行判断是否在边界，是则 '#',否则 '.'。

💡 类比"画相框：只涂最外一圈，中间留白"：

```python
n = int(input())
for i in range(n):
    print(''.join('#' if (i in (0, n-1) or j in (0, n-1)) else '.' for j in range(n)))
```
> **复杂度**：O(n²) 时间，O(1) 空间

---
#### 17.1.59 例 59：贪吃行走方向的迷宫字节（自定义）⭐⭐
> **知识点**：BFS/DFS 路径模拟、方向记录｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 m×n 网格（0 可走，1 障碍），从(1,1)到(m,n)，输出一条可行路径的方向序列（比如 DD... 表示向下），保证有解。

**思路**
用 BFS 找最短路径并回溯记录方向。

💡 类比"外卖导航：一层层圈地搜索邻居格子，找到终点再回放怎么走"：

```python
from collections import deque
m, n = map(int, input().split())
g = [list(map(int, input().split())) for _ in range(m)]
pre = [[None]*n for _ in range(m)]
q = deque()
q.append((0,0))
g[0][0] = 1
while q:
    x, y = q.popleft()
    if (x, y) == (m-1, n-1):
        break
    for dx, dy, ch in [(1,0,'D'),(0,1,'R')]:
        nx, ny = x+dx, y+dy
        if 0<=nx<m and 0<=ny<n and g[nx][ny]==0:
            g[nx][ny]=1
            pre[nx][ny]=(x,y,ch)
            q.append((nx,ny))
# 回溯
route = []
cx, cy = m-1, n-1
while (cx, cy) != (0, 0):
    px, py, ch = pre[cx][cy]
    route.append(ch)
    cx, cy = px, py
print(''.join(route[::-1]))
```
> **复杂度**：O(mn) 时间，O(mn) 空间

---
#### 17.1.60 例 60：进制回文自动机（自定义）⭐⭐
> **知识点**：进制转换、回文判断｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定进制 b 与整数 n，判断 n 在 b 进制下表示是否为回文，若是输出 "Yes" 与回文串，否则 "No"。

**思路**
短除法得到 b 进制串，判断回文。

💡 类比"换个语言报数字：把十进制翻成 b 进制写法再看看是否左右对称"：

```python
n, b = map(int, input().split())
dig = "0123456789ABCDEF"
s = ""
if n == 0:
    s = "0"
while n:
    s += dig[n % b]
    n //= b
s = s[::-1]
print("Yes" if s == s[::-1] else "No")
print(s)
```
> **复杂度**：O(log_b n) 时间，O(1) 空间
#### 17.1.61 例 61：牌的置换循环（自定义）⭐⭐
> **知识点**：置换模拟、循环标记｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 张牌编号 1..n，执行给定的置换 p 若干次，问要多后才能回到初始顺序（求置换的最小循环节 lcm）。

**思路**
求出每个元素所在置换循环的长度，取所有循环长度的最小公倍数。

💡 类比"钟表齿轮相位：每个齿轮转回原位需要不同圈数，所有一起回位要取它们的最小公倍数"：

```python
from math import gcd
n = int(input())
p = list(map(int, input().split()))
p = [x-1 for x in p]
vis = [False]*n
def lcm(a, b):
    return a // gcd(a, b) * b
ans = 1
for i in range(n):
    if not vis[i]:
        c = 0
        j = i
        while not vis[j]:
            vis[j] = True
            j = p[j]
            c += 1
        ans = lcm(ans, c)
print(ans)
```
> **复杂度**：O(n) 时间，O(n) 空间

---
#### 17.1.62 例 62：统计单词首字母出现（自定义）⭐
> **知识点**：单词拆分、计数｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一行英文句子（长度≤1000），统计各单词首字母出现的次数（大小写忽略）。

**思路**
用 split 拆词，取每个词首字母计数。

💡 类比"姓名首字户口本：把每个人名字开头的字登记一下看谁多"：

```python
import sys
s = sys.stdin.read().split()
cnt = {}
for w in s:
    ch = w[0].lower()
    cnt[ch] = cnt.get(ch, 0) + 1
for ch in sorted(cnt):
    print(ch, cnt[ch])
```
> **复杂度**：O(L) 时间，O(k) 空间

---
#### 17.1.63 例 63：顺时针打印矩阵（剑指offer 经典）⭐⭐⭐
> **知识点**：边界收缩、方向遍历｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 m×n 矩阵，请按顺时针螺旋顺序输出所有元素（从左上角开始）。

**思路**
维护上下左右四个边界，沿螺旋逐层收缩输出。

💡 类比"削洋葱皮：一圈圈从外向内把每层的数字揭下来"：

```python
m, n = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(m)]
top, bottom, left, right = 0, m-1, 0, n-1
res = []
while top <= bottom and left <= right:
    for j in range(left, right+1):
        res.append(a[top][j])
    top += 1
    for i in range(top, bottom+1):
        res.append(a[i][right])
    right -= 1
    if top <= bottom:
        for j in range(right, left-1, -1):
            res.append(a[bottom][j])
        bottom -= 1
    if left <= right:
        for i in range(bottom, top-1, -1):
            res.append(a[i][left])
        left += 1
print(' '.join(map(str, res)))
```
> **复杂度**：O(mn) 时间，O(1) 空间（除结果外）

---
#### 17.1.64 例 64：直角三角形边长枚举（自定义）⭐⭐
> **知识点**：勾股枚举、优化循环｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定周长 p，求三边为整数且构成直角三角形的个数（不同形状计 1 个）。

**思路**
枚举两直角边 a,b，由勾股数与周长关系推导第三边并验证。

💡 类比"拼三角尺：试遍两边组合看斜边是否正好是整数"：

```python
p = int(input())
cnt = 0
for a in range(1, p//3+1):
    for b in range(a, (p-a)//2+1):
        c = p - a - b
        if a*a + b*b == c*c:
            cnt += 1
print(cnt)
```
> **复杂度**：O(p²) 时间，O(1) 空间

---
#### 17.1.65 例 65：寻找第 k 个满足条件的数（自定义）⭐⭐
> **知识点**：枚举筛选、条件判断｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从 1 开始依次枚举正整数，找到第 k 个"各位数字之积大于各位数字之和"的数并输出。

**思路**
从 1 开始计数，逐个数判断条件，直到找到第 k 个。

💡 类比"彩票摇号排队：从一号往后一个个验条件，数到第 k 个中奖的"：

```python
k = int(input())
cnt = 0
x = 1
while True:
    s = sum(map(int, str(x)))
    pr = 1
    for d in str(x):
        pr *= int(d)
    if pr > s:
        cnt += 1
        if cnt == k:
            print(x)
            break
    x += 1
```
> **复杂度**：O(答案·k) 时间，O(1) 空间

---
#### 17.1.66 例 66：翻杯问题最少步（POJ 常考变式）⭐⭐
> **知识点**：状态模拟、暴力尝试｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 个杯口朝上的杯子，每次必须翻 m 个，问能否全部杯口朝下，若能输出最少次数（模拟小规模）。

**思路**
用 BFS 在 2^n 状态间搜索，每次翻转 m 个杯子找最短步数。

💡 类比"翻牌找全朝下：用广度优先圈层搜索所有可能翻法里最近的一次凑齐"：

```python
from collections import deque
n, m = map(int, input().split())
start = 0
st, ed = 0, (1 << n) - 1
dist = {start: 0}
q = deque([start])
while q:
    u = q.popleft()
    if u == ed:
        print(dist[u])
        break
    # 枚举要翻的 m 个杯子
    from itertools import combinations
    idxs = [i for i in range(n)]
    for comb in combinations(idxs, m):
        v = u
        for i in comb:
            v ^= (1 << i)
        if v not in dist:
            dist[v] = dist[u] + 1
            q.append(v)
else:
    print(-1)
```
> **复杂度**：O(2^n·C(n,m)) 时间，O(2^n) 空间

---
#### 17.1.67 例 67：大数阶乘输出（HDU 1042）⭐⭐⭐
> **知识点**：高精度乘法、Python 大整数｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（1≤n≤1000），输出 n! 的精确值（可能上百位）。

**思路**
用 Python 原生大整数循环连乘即可。

💡 类比"做大蛋糕层层加料：从 1 一直乘到 n，天然支持巨大数"：

```python
import math
n = int(input())
print(math.factorial(n))
```
> **复杂度**：O(n·M(n)) 时间，O(len) 空间

---
#### 17.1.68 例 68：模拟日期时钟走字（自定义）⭐
> **知识点**：时分秒模拟、进位｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定当前时间 h:m:s 与秒数 t，求 t 秒后的时间（24 小时制）。

**思路**
把总秒数换算后逐级取模进位。

💡 类比"秒表进位：秒满 60 进分，分满 60 进时，时满 24 归零"：

```python
h, m, s = map(int, input().split(':'))
t = int(input())
tot = h*3600 + m*60 + s + t
tot %= 86400
h = tot // 3600
m = tot % 3600 // 60
s = tot % 60
print("%02d:%02d:%02d" % (h, m, s))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.1.69 例 69：队列实现栈（自定义/数据结构题）⭐⭐
> **知识点**：队列模拟、LIFO 语义｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：使用两个队列模拟一个栈，支持 push(x)、pop() 返回栈顶并弹出、isEmpty()。输入若干命令，输出每个 pop 的结果。

**思路**
主队列存栈内容，pop 时把除队尾外全部移到辅助队列再弹出队尾。

💡 类比"排队进电梯：要拿最下面那个包，得把上面的先挪到旁边再拿底下的"：

```python
from collections import deque
q1 = deque()
q2 = deque()
n = int(input())
for _ in range(n):
    parts = input().split()
    if parts[0] == 'push':
        q1.append(int(parts[1]))
    else:
        while len(q1) > 1:
            q2.append(q1.popleft())
        print(q1.popleft())
        q1, q2 = q2, q1
```
> **复杂度**：push O(1)，pop O(n) 时间，O(n) 空间

---
#### 17.1.70 例 70：区间不相交最大数量（自定义/贪心预热）⭐⭐
> **知识点**：区间排序、模拟选择｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个闭区间，选择尽量多的区间使它们两两不重叠，求最大可选数量。

**思路**（枚举/模拟方向）按右端点排序，贪心取端点最早结束的区间。

💡 类比"隔间占位：先占最早结束的会议室，就能塞下最多的会"：

```python
n = int(input())
iv = [tuple(map(int, input().split())) for _ in range(n)]
iv.sort(key=lambda x: x[1])
cnt = 0
end = -1
for l, r in iv:
    if l >= end:
        cnt += 1
        end = r
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间
#### 17.1.71 例 71：双指针去重排序（自定义）⭐⭐
> **知识点**：排序、去重输出｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个整数（可重复），去重后按升序输出不重复元素。

**思路**
排序后用相邻比较跳过重复，或直接 set 排序。

💡 类比"整理书架按高矮：排好序后挨着看，跟上一个一样就跳过"：

```python
n = int(input())
a = list(map(int, input().split()))
a.sort()
res = []
for x in a:
    if not res or res[-1] != x:
        res.append(x)
print(' '.join(map(str, res)))
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.1.72 例 72：字符频率条形图（自定义）⭐
> **知识点**：计数、格式化图形输出｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入一串小写字母，按出现次数用 '*' 画出条形图，每行一个字母及对应星号（按字母序）。

**思路**
统计频率后逐字母输出星号数量。

💡 类比"画成绩柱状图：每个字母一根柱，柱高就是出现的次数"：

```python
s = input().strip()
c = [0]*26
for ch in s:
    if 'a' <= ch <= 'z':
        c[ord(ch)-97] += 1
for i in range(26):
    if c[i]:
        print(chr(97+i), '*' * c[i])
```
> **复杂度**：O(L) 时间，O(1) 空间

---
#### 17.1.73 例 73：跳石头模拟拼接（洛谷 P2084）⭐⭐
> **知识点**：循环模拟、条件累加｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定进制 b 与一个 b 进制整数，按"每项系数×b^位次"展开输出（如二进制 1101 → 1*2^3+1*2^2+1*2^0 形式）。

**思路**
从高位遍历，非零位输出"系数*b^k"用 + 连接。

💡 类比"拆数字低价超市：每位数字按它站在哪一位价位拆开发票"：

```python
b, s = input().split()
b = int(b)
res = []
n = len(s)
for i, ch in enumerate(s):
    if ch != '0':
        p = n - 1 - i
        res.append(f"{ch}*{b}^{p}")
print('+'.join(res))
```
> **复杂度**：O(L) 时间，O(L) 空间

---
#### 17.1.74 例 74：最长公共子串（自定义）⭐⭐
> **知识点**：动态规划、字符比较｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个字符串，求它们的最长公共连续子串（连续子串）长度。

**思路**
用 dp[i][j] 表示以 s[i],t[j] 结尾的最长公共子串，相等则 +1 取最大。

💡 类比"比对两段绳子的重叠段：看看哪里颜色连续一样是最长的一段"：

```python
s = input().strip()
t = input().strip()
n, m = len(s), len(t)
dp = [[0]*(m+1) for _ in range(n+1)]
best = 0
for i in range(1, n+1):
    for j in range(1, m+1):
        if s[i-1] == t[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
            best = max(best, dp[i][j])
print(best)
```
> **复杂度**：O(nm) 时间，O(nm) 空间

---
#### 17.1.75 例 75：聪明的猴子摘桃（枚举综合题）⭐⭐⭐
> **知识点**：综合枚举、条件模拟｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一排 n 棵桃树，猴子从第 1 棵开始，每次可跳过恰好 k 棵（k≥0），收集经过树上的桃，问从 1 赶到 n 最少收集时能稳定摘到的最多桃数（枚举步长）。

**思路**
暴力枚举步长 k，模拟每步落点累加桃数，取最大。

💡 类比"挑着跳格子吃豆子：试遍各种跨步方式看哪种一路吃到的豆子最多"：

```python
n = int(input())
a = list(map(int, input().split()))
best = 0
for k in range(n):
    total = 0
    i = 0
    while i < n:
        total += a[i]
        i += 1 + k
    best = max(best, total)
print(best)
```
> **复杂度**：O(n²) 时间，O(1) 空间

---

### 17.2 贪心算法

#### 17.2.1 例 1：活动选择问题（HDU 2037）⭐
> **知识点**：区间贪心、活动安排｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 场活动各有开始与本结束时间，一个时间段只能安排一场，求最多能安排多少场。

**思路**：按结束时间升序，依次选结束最早的且不与前面冲突的活动。

💡 类比"排课表：先把下课最早的课抢座，剩下的时间窗口最大"：

```python
n = int(input())
acts = [tuple(map(int, input().split())) for _ in range(n)]
acts.sort(key=lambda x: x[1])
cnt = 0
end = -1
for s, e in acts:
    if s >= end:
        cnt += 1
        end = e
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.2 例 2：删数问题（洛谷 P1106）⭐⭐⭐
> **知识点**：单调栈、删 k 个数最小化｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个大整数（长度≤250）与整数 k，删去其中 k 个数字后使剩余数字组成的数最小，输出结果（去前导零）。

**思路**：用单调栈维护递增序列，出现下降就删；处理前导零。

💡 类比"做减法填位：从左往右，前面有个更大的就让它先被删掉，越小越靠前越好"：

```python
s = list(input().strip())
k = int(input())
stack = []
for ch in s:
    while k and stack and stack[-1] > ch:
        stack.pop()
        k -= 1
    stack.append(ch)
while k:
    stack.pop()
    k -= 1
res = ''.join(stack).lstrip('0')
print(res if res else '0')
```
> **复杂度**：O(L) 时间，O(L) 空间

---
#### 17.2.3 例 3：分糖果（洛谷 P3817）⭐⭐
> **知识点**：贪心调整、相邻约束｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 堆糖果，每堆 a_i，每次可从一个盒子拿走若干糖果，要求任意相邻两盒之和≤x，求最少拿走多少。

**思路**：从左往右扫，当前盒与前一个之和超 x，则减少当前盒的数量。

💡 类比"控制相邻水位"：左边高了左边先减，保持两两相邻和不过线：

```python
n, x = map(int, input().split())
a = list(map(int, input().split()))
ans = 0
for i in range(1, n):
    if a[i] + a[i-1] > x:
        over = a[i] + a[i-1] - x
        take = min(a[i], over)
        a[i] -= take
        ans += take
print(ans)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.2.4 例 4：小船过河（洛谷 P1809）⭐⭐⭐
> **知识点**：过河贪心、速度最小化｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个人过河，船每次最多载 2 人，速度取较慢者，要求 1 人把船开回。求所有人过河的最短总时间。

**思路**：排序后，每次比较"最快+次快先送再回"与"最快送两慢的"两种策略取最优。

💡 类比"接力送快递"：让最快的人来回当司机，对比两种带人方式谁更省时：

```python
n = int(input())
a = sorted(map(int, input().split()))
t = 0
while n > 3:
    s1 = a[0]*2 + a[n-2] + a[n-1]     # 最快送两慢
    s2 = a[1]*2 + a[0] + a[n-1]       # 次快送次慢后快回
    t += min(s1, s2)
    n -= 2
if n == 3:
    t += a[0] + a[1] + a[2]
elif n == 2:
    t += a[1]
else:
    t += a[0]
print(t)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.5 例 5：哈夫曼编码代码长度（洛谷 P2168）⭐⭐
> **知识点**：哈夫曼树、优先队列｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个字符出现频率已知，构建最优前缀编码，求加权路径长度（总编码长度）。

**思路**：用小顶堆反复合并最小两棵频率树，累加合并代价。

💡 类比"合并沙堆"：频繁出现的字符编码越短越好，用优先队列每次合并最少的：

```python
import heapq
n = int(input())
w = [int(input()) for _ in range(n)]
heapq.heapify(w)
cost = 0
while len(w) > 1:
    x = heapq.heappop(w); y = heapq.heappop(w)
    s = x + y
    cost += s
    heapq.heappush(w, s)
print(cost)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.6 例 6：跳跃游戏（LeetCode 55 / 洛谷 类题）⭐⭐
> **知识点**：最远可达、贪心扫描｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个格子，位置 i 可跳最多 a_i 步，求能否从下标 0 到达最后一个格子。

**思路**：维护当前能到的最远下标，逐格更新，若被卡住则失败。

💡 类比"踩着浮板过河"：记录最远能搭到的浮板，一路向前延伸：

```python
n = int(input())
a = list(map(int, input().split()))
far = 0
for i in range(n):
    if i > far:
        print("NO"); break
    far = max(far, i + a[i])
else:
    print("YES" if far >= n-1 else "NO")
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.2.7 例 7：跳跃游戏 II 最少步数（洛谷 类题）⭐⭐⭐
> **知识点**：区间扩展、最少跳跃｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个格子，位置 i 可跳最多 a_i 步，求从 0 到最后一格所需的最少跳跃次数。

**思路**：按"当前区间能跳到的最大距离"划分层数，每层跳跃次数 +1。

💡 类比"闯关推进"：每一跳把可达终点推远一波，数一共推了几波：

```python
n = int(input())
a = list(map(int, input().split()))
steps = 0
end, far = 0, 0
for i in range(n-1):
    far = max(far, i + a[i])
    if i == end:
        steps += 1
        end = far
print(steps)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.2.8 例 8：装水最多问题（洛谷 P1314 类）⭐⭐
> **知识点**：双指针、面积贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个隔板高度数组，选择两个隔板（下标 i<j）使其与 x 轴围成的容器能装最多水，求最大水量 min(a_i,a_j)*(j-i)。

**思路**：双指针从两端向中间，优先移动较矮的一侧。

💡 类比"端水桶找宽口"：两板固定时短板决定水量，麻木短板一边收就更可能变大：

```python
n = int(input())
a = list(map(int, input().split()))
i, j = 0, n-1
best = 0
while i < j:
    best = max(best, min(a[i], a[j]) * (j - i))
    if a[i] < a[j]:
        i += 1
    else:
        j -= 1
print(best)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.2.9 例 9：硬币找零最少张（洛谷 P1037 类）⭐⭐
> **知识点**：贪心板币、整除取模｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：硬币面值为 1,5,10,25,50，给定金额 m，求用最少硬币凑够 m。

**思路**：从大面额硬币往下贪心取整。

💡 类比"找零钱柜台"：能用大票就不用小票，张数必然最少（可换货币组）：

```python
m = int(input())
vals = [50, 25, 10, 5, 1]
cnt = 0
for v in vals:
    cnt += m // v
    m %= v
print(cnt)
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.2.10 例 10：区间覆盖最少（洛谷 P2082）⭐⭐⭐
> **知识点**：区间覆盖、贪心延伸｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：用若干长度为 len 的线段去覆盖数轴上 n 个点，求覆盖所有点需要的最少线段数（线段可重叠）。

**思路**：点排序后贪心，每根线段放在当前未覆盖最左点并尽可能向右延伸。

💡 类比"路灯照明"：每盏灯尽量照得远一点，数需要几盏灯：

```python
n, L = map(int, input().split())
p = sorted(map(int, input().split()))
cnt = 0
covered = -1
i = 0
while i < n:
    cnt += 1
    reach = p[i] + L - 1
    covered = reach
    while i < n and p[i] <= covered:
        i += 1
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.11 例 11：雷达站覆盖岛屿（POJ 1328）⭐⭐⭐
> **知识点**：区间转换、最少点覆盖｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：海岸线为 x 轴，雷达建在 x 轴上，半径固定 d。给定 n 个岛屿坐标，求覆盖所有岛屿需要的最少雷达数，无解输出 -1。

**思路**：每岛求出雷达可放的 x 区间，问题转为"区间上最少点交所有区间"，按右端点贪心。

💡 类比"串项链找打结处"：把每个岛屿能放雷达的横坐标范围看成一个区间，找最少的点穿线穿过所有区间：

```python
import math
n, d = map(int, input().split())
intervals = []
ok = True
for _ in range(n):
    x, y = map(int, input().split())
    if y > d:
        ok = False
    if ok:
        dis = math.sqrt(d*d - y*y)
        intervals.append((x-dis, x+dis))
if not ok:
    print(-1)
else:
    intervals.sort(key=lambda r: r[1])
    cnt = 0
    last = -float('inf')
    for l, r in intervals:
        if l > last + 1e-9:
            cnt += 1
            last = r
    print(cnt)
```
> **复杂度**：O(n log n) 时间，O(n) 空间
#### 17.2.12 例 12：木棒拼接最省（洛谷 P1120 变式）⭐
> **知识点**：分组贪心、平均分堆｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 段木棒长度已知，把它们分成两堆，使两堆总长度之差最小，求最小差值。

**思路**：简化题为尽量平均分配，用贪心排序后依次放到较小堆（近似）。

💡 类比"挑担匀平"：每次把最重的加给较轻的一边，让两边尽量接近：

```python
n = int(input())
a = sorted(map(int, input().split()), reverse=True)
s1 = s2 = 0
for x in a:
    if s1 <= s2:
        s1 += x
    else:
        s2 += x
print(abs(s1 - s2))
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.13 例 13：任务调度最小等待（POJ 1949 变式）⭐⭐
> **知识点**：短任务优先、排队贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个任务，单机每次做一个，求使"所有任务完成时间之和"最小的调度顺序的总等待时间。

**思路**：短作业优先——按执行时间升序执行，累加前缀完成时间。

💡 类比"ATM 排队取钱"：让取钱快的先办，大家平均等待最少：

```python
n = int(input())
t = sorted(map(int, input().split()))
total = 0
cur = 0
for x in t:
    cur += x
    total += cur
print(total)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.14 例 14：移动石头归位（自定义）⭐⭐
> **知识点**：中位数最优、位置贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：数轴上 n 堆石头位于坐标 x_i，要把它们移到连续 n 个位置（相邻间距 1），求最少移动总距离。

**思路**：做坐标变换后取中位数作为对齐基准，最小化绝对值距离和。

💡 类比"排纵队对齐"：都向中位数靠拢，人人挪的总步数最少：

```python
n = int(input())
x = sorted(map(int, input().split()))
b = sorted(x[i] - i for i in range(n))
m = b[n//2]
ans = sum(abs(v - m) for v in b)
print(ans)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.15 例 15：最大数拼接（洛谷 P1106 配套 / CF 变式）⭐⭐
> **知识点**：排序比较器、字符串拼接｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数字串，将它们按某个顺序拼接成一个大数，求能拼出的最大数。

**思路**：按"x+y > y+x"比较排序，越靠前的拼法整串更大。

💡 类比"排词牌"：两个数字谁先谁后看拼出来哪个更大，整体排序得到最大拼接：

```python
n = int(input())
a = input().split()
from functools import cmp_to_key
def cmp(x, y):
    if x + y > y + x:
        return -1
    if x + y < y + x:
        return 1
    return 0
a.sort(key=cmp_to_key(cmp))
res = ''.join(a).lstrip('0')
print(res if res else '0')
```
> **复杂度**：O(n log n·len) 时间，O(1) 空间

---
#### 17.2.16 例 16：加油站最小停靠（自定义/CF 变式）⭐⭐
> **知识点**：优先队列、沿途加油｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：汽车从 0 点出发到终点距离 D，初始油量 P，路上有 n 个加油站（坐标与该站可加量），每公里耗 1 油，求到达终点最少加油次数（不足则 -1）。

**思路**：优先选择经过加油站中油量最大的那个加油，用大顶堆维护。

💡 类比"没油找最大灌"：开到哪算到哪，路过加油站先进大顶堆备选，油尽时取加得最多的那个：

```python
import heapq
D, P = map(int, input().split())
n = int(input())
st = [tuple(map(int, input().split())) for _ in range(n)]
st.sort()
q = []
i = 0
fuel = P
cnt = 0
while fuel < D:
    while i < n and st[i][0] <= fuel:
        heapq.heappush(q, -st[i][1])
        i += 1
    if not q:
        cnt = -1
        break
    fuel += -heapq.heappop(q)
    cnt += 1
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.17 例 17：共同好友分组最小通信（自定义）⭐⭐
> **知识点**：配对贪心、排序挑选｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个人，每人有一通信代价 w_i。要求选若干人让总代价在"两两互相抵消"后最小（残缺题演示：选出代价和 ≤ W 的最大组）。

**思路**：排序后从最小代价开始累加，直到超过预算，统计人数。

💡 类比"买菜凑预算"：先把便宜的挑进篮子再到预算上限为止：

```python
n, W = map(int, input().split())
w = sorted(map(int, input().split()))
c = 0
s = 0
for x in w:
    if s + x <= W:
        s += x
        c += 1
print(c)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.18 例 18：木板锯成多段最小代价（POJ 3253）⭐⭐⭐
> **知识点**：哈夫曼合并、反向贪心｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：把一块长木板锯成 n 段，每锯一次代价为当前木板长度，求最小总锯木代价（等价于哈夫曼合并）。

**思路**：从最终小段反向合并，每次合并最短两段。

💡 类比"拼木条"：越是先拼起来的短条越便宜，用小顶堆每次取最短两条合并：

```python
import heapq
n = int(input())
a = list(map(int, input().split()))
heapq.heapify(a)
cost = 0
while len(a) > 1:
    x = heapq.heappop(a); y = heapq.heappop(a)
    s = x + y
    cost += s
    heapq.heappush(a, s)
print(cost)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.19 例 19：最少比较次数排序冒泡计数（自定义）⭐
> **知识点**：冒泡交换计数、逆序对｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 1..n 的一个排列，用相邻交换排序，求最少交换次数。

**思路**：最少交换次数等于逆序对数，统计即可。

💡 类比"相邻插队回位"：每次相邻交换修复一对逆序，数总逆序对：

```python
n = int(input())
a = list(map(int, input().split()))
cnt = 0
for i in range(n):
    for j in range(i+1, n):
        if a[i] > a[j]:
            cnt += 1
print(cnt)
```
> **复杂度**：O(n²) 时间，O(1) 空间

---
#### 17.2.20 例 20：分糖果围成圈（自定义）⭐⭐
> **知识点**：环形分配、中位数归位｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个小朋友围成一圈，各有若干糖果，总数为 n 的倍数，每次可把某人的糖果移给相邻一人 1 个，求最少移动次数使每人相同。

**思路**：等价于环状均分，用前缀和取中位数求最小绝对距离和。

💡 类比"传糖果传圈"：要让差额拉平，用中位数为落脚点最少移动：

```python
n = int(input())
a = list(map(int, input().split()))
avg = sum(a) // n
s = 0
pre = []
for x in a:
    s += x - avg
    pre.append(s)
pre.sort()
m = pre[n//2]
ans = sum(abs(v - m) for v in pre)
print(ans)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.21 例 21：最多不重叠区间变式（洛谷 P1803）⭐
> **知识点**：右端点排序、贪心选择｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个区间[l,r]，求最多能选出的两两不相交区间个数。

**思路**：按右端点升序，贪心选结束最早的。

💡 类比"开会排日程"：谁先开完谁先占时间窗，塞下最多场会议：

```python
n = int(input())
iv = [tuple(map(int, input().split())) for _ in range(n)]
iv.sort(key=lambda x: (x[1], x[0]))
cnt = 0
end = -1
for l, r in iv:
    if l >= end:
        cnt += 1
        end = r
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.22 例 22：装最多的长条（自定义）⭐⭐
> **知识点**：排序累加、可行性判断｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：箱子容量 V，n 个物品体积 v_i（均 ≤V），求最多能装多少个。

**思路**：体积升序，逐个塞入直到容量不足。

💡 类比"塞行李箱"：先塞体积小的东西能塞最多件：

```python
V, n = map(int, input().split())
v = sorted(map(int, input().split()))
cnt = 0
s = 0
for x in v:
    if s + x <= V:
        s += x
        cnt += 1
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间
#### 17.2.23 例 23：国王的金币最少金币数（自定义）⭐⭐
> **知识点**：贪心拆解、次方求和｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：需要凑出价值恰好为 m 的金币，可用面值为 1,2,4,...,2^k 的金币（每种不限），求最少用几枚。

**思路**：用最大面值尽量多取（等价于二进制表示中 1 的个数）。

💡 类比"翻硬币二进制"：答案是 m 的二进制 1 的个数：

```python
m = int(input())
print(bin(m).count('1'))
```
> **复杂度**：O(log m) 时间，O(1) 空间

---
#### 17.2.24 例 24：尽量打散的摆课（自定义）⭐⭐
> **知识点**：间隔贪心、计数分配｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 门课，第 i 门有 c_i 节需在一周排开。同一门课的课之间至少要隔 d 天，判断能否在不跨周（7 天）排下，并输出一种排法。

**思路**：按节数从多到少，尽量隔天放置（演示可行性判断：最多节数≤ceil(7/d)）。

💡 类比"隔天吃药"：最多的那门课的个数要放得下 7 天里满足间隔的槽位：

```python
n, d = map(int, input().split())
c = list(map(int, input().split()))
mx = max(c)
# 7 天里最多能放下间隔 d 的天数
slots = 0
day = 1
while day <= 7:
    slots += 1
    day += d + 1
print("YES" if mx <= slots else "NO")
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.2.25 例 25：最少票数贿选（自定义）⭐⭐
> **知识点**：贪心转移、累计调整｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 位候选人得票 a_i，要让你指定的候选人成为并列第一，需要从得票最多者那里"借"走多少票，求最少。

**思路**：让目标候选人的票数与当前最高者对齐，差多少补多少。

💡 类比"追赶第一名"：看第一的票数比目标多几票，最好借到他数即可平局：

```python
n = int(input())
a = list(map(int, input().split()))
target = a[0]
rest = max(a[1:])
if rest > target:
    print(rest - target)
else:
    print(0)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.2.26 例 26：最少接电话时间（自定义）⭐⭐
> **知识点**：短任务优先、前缀耗时｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：客服依次处理 n 通电话，每通耗时 t_i，求使所有顾客等待时间总和最小的顺序的总等待时间。

**思路**：按耗时升序处理，累加前半程等待。

💡 类比"排队柜台"：处理快的先办，别人等得就少：

```python
n = int(input())
t = sorted(map(int, input().split()))
tot = 0
cur = 0
for x in t:
    cur += x
    tot += cur - x   # 真正等待 = 完成时间 - 自身耗时
print(tot)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.27 例 27：合并颜色最小代价（自定义）⭐⭐⭐
> **知识点**：相邻合并、贪心局部判定｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一行 n 个数，每次只能合并相邻两项，代价为两者之和，合并后数为和，求把整行合并成一个数的最小总代价。

**思路**：经典石子合并，贪心不保证最优，标准做法是区间 DP；此处演示 O(n³) 区间 DP。

💡 类比"并石头"：用区间 DP 枚举先合并哪一段，取最小累计合并代价：

```python
n = int(input())
a = list(map(int, input().split()))
pre = [0]
for x in a:
    pre.append(pre[-1] + x)
dp = [[0]*(n+1) for _ in range(n+1)]
for length in range(2, n+1):
    for i in range(1, n-length+2):
        j = i + length - 1
        dp[i][j] = min(dp[i][k] + dp[k+1][j] for k in range(i, j)) + pre[j] - pre[i-1]
print(dp[1][n])
```
> **复杂度**：O(n³) 时间，O(n²) 空间

---
#### 17.2.28 例 28：最省邮票集合（自定义）⭐
> **知识点**：大票优先、组合贪心｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：邮票面值 1,2,5,10,20,50,100，凑出额度 m，求最少用张数。

**思路**：从大面值往下尽量取整。

💡 类比"代金券凑整"：能用大券就先用大券，张数最少：

```python
m = int(input())
vals = [100, 50, 20, 10, 5, 2, 1]
cnt = 0
for v in vals:
    cnt += m // v
    m %= v
print(cnt)
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.2.29 例 29：爬塔最少休息塔（自定义）⭐⭐
> **知识点**：越过障碍、能量守恒贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：爬 n 层塔，每层消耗体力 a_i，初始体力 E，途中可站某些补给点回复体力 b_i（每层回满成怪），求能否登顶的最小补给次数。

**思路**：用优先队列记录遇到的补给点，体力不足时取最大的补齐。

💡 类比"闯关急救包"：前面遇到的补给包先攒着，扛不住时用最强的（同加油站问题）：

```python
import heapq
n, E = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
q = []
hp = E
cnt = 0
for i in range(n):
    heapq.heappush(q, -b[i])
    if hp - a[i] < 0:
        if not q:
            cnt = -1
            break
        hp += -heapq.heappop(q)
        cnt += 1
    hp -= a[i]
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.30 例 30：最少加几次排序（自定义）⭐⭐
> **知识点**：贪心扫描、局部交换｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给一个 1..n 排列，允许每次交换相邻两项，求升序排序的最少交换次数。

**思路**：等于逆序对数，用归并统计大范围。

💡 类比"相邻插队"：每发生一次相邻交换就消灭一个逆序对：

```python
def ms(a):
    if len(a) <= 1:
        return 0, a
    m = len(a)//2
    c1, l = ms(a[:m])
    c2, r = ms(a[m:])
    i = j = 0
    c = c1 + c2
    res = []
    while i < len(l) and j < len(r):
        if l[i] <= r[j]:
            res.append(l[i]); i += 1
        else:
            res.append(r[j]); c += len(l)-i; j += 1
    res += l[i:] + r[j:]
    return c, res
n = int(input())
a = list(map(int, input().split()))
print(ms(a)[0])
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.31 例 31：分组求和最接近目标（自定义）⭐⭐
> **知识点**：双指针、两端逼近｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数，一分为两组使两组和尽量接近，等价求最小差。演示用排序后双指针思想处理 k 数分组近似。

**思路**：简化：排序后较大的放一号组、次大放二号组来回摆动，使两组接近。

💡 类比"分派两边抬杠"：轮流把最重的往轻的一边加，让两边平衡：

```python
n = int(input())
a = sorted(map(int, input().split()))
l, r = 0, n - 1
s1 = s2 = 0
turn = 0
while l <= r:
    if turn == 0:
        s1 += a[r]; r -= 1
    else:
        if l <= r:
            if a[r] >= a[l]:
                s2 += a[r]; r -= 1
            else:
                s2 += a[l]; l += 1
    turn = 1 - turn
print(abs(s1 - s2))
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.32 例 32：水龙头补水最少开关次数（自定义）⭐
> **知识点**：时刻覆盖、端点贪心｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个时刻需供水，每个水龙头持续 K 秒，求覆盖所有需求时刻的最少水龙头数。

**思路**：时刻排序后贪心，每个龙头覆盖到其末端最远，沿用未覆盖第一个时刻。

💡 类比"洒水定时器"：一次开启尽量覆盖更多的需求时段：

```python
n, K = map(int, input().split())
t = sorted(map(int, input().split()))
cnt = 0
i = 0
while i < n:
    cnt += 1
    end = t[i] + K - 1
    while i < n and t[i] <= end:
        i += 1
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.33 例 33：果篮称重配对最省（自定义）⭐⭐
> **知识点**：排序配对、双指针最小化｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个苹果重量已知，把它俩俩配对（n 为偶数），每对重量和为目标 w，若都能配成则 YES。

**思路**：排序后首尾双指针配对求和判断。

💡 类比"凑对拼桌"：最轻的和最重的搭配才能最容易凑成目标：

```python
n, w = map(int, input().split())
a = sorted(map(int, input().split()))
ok = True
l, r = 0, n-1
while l < r:
    if a[l] + a[r] != w:
        ok = False
        break
    l += 1; r -= 1
print("YES" if ok else "NO")
```
> **复杂度**：O(n log n) 时间，O(1) 空间
#### 17.2.34 例 34：分配教室最少间数（洛谷 P5019）⭐⭐
> **知识点**：前缀差分、贪心步数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 段地面需铺地砖，高度数组 a_i 表示第 i 段需要的砖数（每次可连续铺一行若干段 +1），求最少操作次数。

**思路**：每次把一段连续区间 +1，最小次数等于"恰好覆盖"的段与上一段的高度净增之和。

💡 类比"刷墙覆盖"：只对比前面高出来的部分补刷，最后累加增量：

```python
n = int(input())
a = list(map(int, input().split()))
ans = a[0]
for i in range(1, n):
    if a[i] > a[i-1]:
        ans += a[i] - a[i-1]
print(ans)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.2.35 例 35：分饼干给最多孩子（洛谷 P1077 变式）⭐⭐
> **知识点**：需求排序、饥饿度贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：每个孩子需要至少 s_i 块饼干才满足，总共有 k 块饼干，每个孩子至多拿一份，求最多能满足的孩子数。

**思路**：按需求升序，从需求最小的孩子逐个分配直到饼干用完。

💡 类比"先满足要得少的"：先把要求低的喂饱能照顾最多人：

```python
n, k = map(int, input().split())
s = sorted(map(int, input().split()))
cnt = 0
for x in s:
    if k >= x:
        k -= x
        cnt += 1
    else:
        break
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.36 例 36：连接所有点最短边（自定义/最小生成树思想）⭐⭐
> **知识点**：并查集、克鲁斯卡尔｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个点有坐标，可用任意两点的距离为代价相连，求让所有点连通的最小总代价（最小生成树）。

**思路**：生成所有边后按代价升序，用并查集依次加入不构成环的边。

💡 类比"修路连接城市"：先把最短的路修上，只要不绕成圈就收下：

```python
n = int(input())
xy = [tuple(map(int, input().split())) for _ in range(n)]
edges = []
for i in range(n):
    for j in range(i+1, n):
        w = abs(xy[i][0]-xy[j][0]) + abs(xy[i][1]-xy[j][1])
        edges.append((w, i, j))
edges.sort()
par = list(range(n))
def find(x):
    while par[x] != x:
        par[x] = par[par[x]]
        x = par[x]
    return x
tot = 0
cnt = 0
for w, u, v in edges:
    ru, rv = find(u), find(v)
    if ru != rv:
        par[ru] = rv
        tot += w
        cnt += 1
        if cnt == n-1:
            break
print(tot)
```
> **复杂度**：O(n² log n) 时间，O(n²) 空间

---
#### 17.2.37 例 37：最大子矩阵和（HDU 1081）⭐⭐
> **知识点**：前缀和、最大子段贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n×n 矩阵，元素可正可负，求子矩阵和的最大值。

**思路**：枚举上下边界，把该范围的每列和压缩成一维，跑最大子段和。

💡 类比"压扁取纵"：固定上下边把列求和变一维，再用最长子段贪心：

```python
n = int(input())
a = [list(map(int, input().split())) for _ in range(n)]
best = -10**18
for top in range(n):
    col = [0]*n
    for bot in range(top, n):
        cur = 0
        for j in range(n):
            col[j] += a[bot][j]
            cur = max(col[j], cur + col[j])
            best = max(best, cur)
print(best)
```
> **复杂度**：O(n³) 时间，O(n) 空间

---
#### 17.2.38 例 38：最少钞票+找零对称（自定义）⭐
> **知识点**：两次贪心、最小张数｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：顾客应付 P 元，他给售货员 Q 元（Q≥P），发售员找 R=Q-P 元。两个人都用 1 元面额，求两人总用张数。

**思路**：顾客给 Q 张 1 元，找零 R 张 1 元，总 Q+R。

💡 类比"交易计数"：双方都点清张数相加即可：

```python
P, Q = map(int, input().split())
print(Q + (Q - P))
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.2.39 例 39：字典 s 分割成子串最少数（自定义）⭐⭐
> **知识点**：字典匹配、贪心扫描｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给一个字符串 s 和一个单词字典，求最少切成几段使每段都在字典中（保证可切），若不可切输出 -1。

**思路**：用 BFS/DP 求最少段数，逐字符向后找成词前缀。

💡 类比"断句拆词"：从前往后用能匹配的词典词向后延伸，动态规划记最少切刀：

```python
s = input().strip()
m = int(input())
words = set(input().split())
n = len(s)
INF = 10**9
dp = [INF]*(n+1)
dp[0] = 0
for i in range(n):
    if dp[i] == INF:
        continue
    for j in range(i+1, n+1):
        if s[i:j] in words:
            dp[j] = min(dp[j], dp[i]+1)
print(dp[n] if dp[n] < INF else -1)
```
> **复杂度**：O(n²·len) 时间，O(n) 空间

---
#### 17.2.40 例 40：最短完全覆盖字符串（自定义）⭐⭐
> **知识点**：字符覆盖、去重长度｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给一个由小写字母组成的字符串，求包含 s 中全部不同字符的最短连续子串长度。

**思路**：滑动窗口维护当前窗口内不同字符种类，双指针收缩取最小。

💡 类比"装齐一套零件"：窗口装得下所有种类时尽量往短里收：

```python
s = input().strip()
need = len(set(s))
from collections import Counter
cnt = Counter()
have = 0
n = len(s)
l = 0
ans = n
for r, ch in enumerate(s):
    cnt[ch] += 1
    if cnt[ch] == 1:
        have += 1
    while have == need:
        ans = min(ans, r - l + 1)
        cnt[s[l]] -= 1
        if cnt[s[l]] == 0:
            have -= 1
        l += 1
print(ans)
```
> **复杂度**：O(n) 时间，O(k) 空间

---
#### 17.2.41 例 41：前 k 个最大数（自定义）⭐⭐
> **知识点**：堆、TopK 贪心保留｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数，求其中最大的 k 个数（按升序输出）。

**思路**：用小顶堆维护前 k 大，堆顶即当前最小门槛。

💡 类比"及格线筛选"：维护一个只装 k 个的手牌，比门槛大的才挤进来并把最小的挤走：

```python
import heapq
n, k = map(int, input().split())
a = list(map(int, input().split()))
h = a[:k]
heapq.heapify(h)
for x in a[k:]:
    if x > h[0]:
        heapq.heapreplace(h, x)
print(' '.join(map(str, sorted(h))))
```
> **复杂度**：O(n log k) 时间，O(k) 空间

---
#### 17.2.42 例 42：最少切分使子串回文（自定义）⭐⭐⭐
> **知识点**：回文切割、区间 DP｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给字符串 s，把它切分成若干回文子串，求最少切几刀。

**思路**：预处理任意区间是否回文，再用 DP 求最少段数，刀数=段数-1。

💡 类比"截镜面对称段"：先标出所有对称段，再取最省的切分方案：

```python
s = input().strip()
n = len(s)
pal = [[False]*n for _ in range(n)]
for i in range(n):
    pal[i][i] = True
for L in range(2, n+1):
    for i in range(n-L+1):
        j = i+L-1
        if s[i] == s[j] and (L == 2 or pal[i+1][j-1]):
            pal[i][j] = True
dp = [10**9]*n
for i in range(n):
    if pal[0][i]:
        dp[i] = 0
    else:
        for j in range(i):
            if pal[j+1][i]:
                dp[i] = min(dp[i], dp[j]+1)
print(dp[n-1])
```
> **复杂度**：O(n²) 时间，O(n²) 空间

---
#### 17.2.43 例 43：装袋最多重量（自定义）⭐
> **知识点**：排序累加、容量可用性｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：背包容量 W，n 个物品重量 w_i，求能装下的物品最大总重量（不限件数，只求尽量装满）。

**思路**：简化：因重量皆非负，尽量取能装的（先取轻的）即可装满近似；演示用取可装物品累加。

💡 类比"购物车塞满"：往购物车里一件件放，放不下就停：

```python
W, n = map(int, input().split())
w = sorted(map(int, input().split()))
s = 0
for x in w:
    if s + x <= W:
        s += x
print(s)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.44 例 44：最少操作使相等（自定义）⭐⭐
> **知识点**：中位数收敛、绝对值最小化｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数，每次操作可把任意一个数 +1 或 -1，求让所有数相等的最少总操作次。

**思路**：都变为中位数时操作最少，对中位数求各元素差的绝对值之和。

💡 类比"集合归位到中间值"：大家聚到中位数那点走路程总和最小：

```python
n = int(input())
a = sorted(map(int, input().split()))
m = a[n//2]
print(sum(abs(x - m) for x in a))
```
> **复杂度**：O(n log n) 时间，O(1) 空间
#### 17.2.45 例 45：最优装载集装箱（POJ 4269）⭐
> **知识点**：重量排序、装船贪心｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：货船载重 C，n 个集装箱重量 w_i，求最多能装多少个。

**思路**：按重量升序装到装不下为止。

💡 类比"装箱先装轻的"：轻的先上船能塞进最多件：

```python
C, n = map(int, input().split())
w = sorted(map(int, input().split()))
cnt = 0
sumw = 0
for x in w:
    if sumw + x <= C:
        sumw += x
        cnt += 1
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.46 例 46：糖果圈外跳最少次（自定义）⭐⭐
> **知识点**：环形贪心、差值累计｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个点围成环，要让人数归均，每次可把一点的员移给相邻点 1，求最少移动次数。

**思路**：同环均分，用前缀差取中位数最小化（与例题 17.2.20 同型重练）。

💡 类比"环上匀糖"：算出每人差额前缀，取中位数作落脚点累计绝对步数：

```python
n = int(input())
a = list(map(int, input().split()))
avg = sum(a)//n
cur = 0
pre = []
for x in a:
    cur += x - avg
    pre.append(cur)
pre.sort()
m = pre[n//2]
print(sum(abs(v-m) for v in pre))
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.47 例 47：整数分组背包（自定义）⭐⭐
> **知识点**：相邻分组、配对最小差｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个（偶数）整数，两两分组，使每组两数之差平方之和最小。

**思路**：排序后相邻两两配对得到最小差平方和（相邻配对最优）。

💡 类比"相近相配"：排序挨着结组差异最小，平方和自然最小：

```python
n = int(input())
a = sorted(map(int, input().split()))
ans = 0
for i in range(0, n, 2):
    ans += (a[i+1] - a[i])**2
print(ans)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.48 例 48：最少字符补成回文（自定义）⭐⭐
> **知识点**：LCS/贪心计数、两端贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：在字符串 s 的一端（只能加在末尾）插入字符使其成为回文，求最少插入次数（返回 0~len-1 基于 LCS）。

**思路**：等于 "len - s 与其逆序的最长公共子序列"，LCS 用 DP。

💡 类比"补录另一半"：找出最长已对称部分，剩下的都得补：

```python
s = input().strip()
t = s[::-1]
n = len(s)
dp = [[0]*(n+1) for _ in range(n+1)]
for i in range(1, n+1):
    for j in range(1, n+1):
        if s[i-1] == t[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
print(n - dp[n][n])
```
> **复杂度**：O(n²) 时间，O(n²) 空间

---
#### 17.2.49 例 49：接雨水最少挡板（LintCode 类）⭐⭐
> **知识点**：左右最高、水量累加｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个高度已知的柱子排一行，雨停后柱子间能积多少水。

**思路**：对每个位置蓄水量=min(左侧最高,右侧最高)-自身高度。

💡 类比"装雨水槽"：高度由左右最高柱子矮的那根决定，减自身高就是积水：

```python
n = int(input())
h = list(map(int, input().split()))
left = [0]*n
mx = 0
for i in range(n):
    mx = max(mx, h[i])
    left[i] = mx
right = [0]*n
mx = 0
for i in range(n-1, -1, -1):
    mx = max(mx, h[i])
    right[i] = mx
ans = 0
for i in range(n):
    ans += max(0, min(left[i], right[i]) - h[i])
print(ans)
```
> **复杂度**：O(n) 时间，O(n) 空间

---
#### 17.2.50 例 50：拆数最大乘积（数学贪心）⭐⭐⭐
> **知识点**：等分乘积、拆 3 贪心｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：把正整数 n 拆成至少两个正整数之和，并使这些数的乘积最大，输出最大乘积。

**思路**：尽可能拆成 3；余 1 时留一个 3 变 4（即 4 优于 3+1）。

💡 类比"切蛋糕让单块尽量大"：尽量切 3 份比切其他更划算，2 备用来调余数：

```python
n = int(input())
if n <= 3:
    print(n - 1)
else:
    if n % 3 == 0:
        print(3 ** (n//3))
    elif n % 3 == 1:
        print(4 * 3 ** (n//3 - 1))
    else:
        print(2 * 3 ** (n//3))
```
> **复杂度**：O(log n) 时间，O(1) 空间

---
#### 17.2.51 例 51：最少光纤连接电脑（自定义）⭐⭐
> **知识点**：差值排序、最少追加｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 台电脑分布于坐标 x_i，需要不间断网络。可在任意位置放置信号站覆盖区间长 L，求最少站数使都能入网。

**思路**：坐标排序，贪婪地从最左未覆盖点放站覆盖到最右。

💡 类比"补装路由器"：从最左没网的电脑开始装一个能往后覆盖最远的：

```python
n, L = map(int, input().split())
x = sorted(map(int, input().split()))
cnt = 0
i = 0
while i < n:
    cnt += 1
    reach = x[i] + L
    while i < n and x[i] <= reach:
        i += 1
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.52 例 52：相邻数字交换求极值（自定义）⭐⭐
> **知识点**：贪心探测、最值移动｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给一个 1..n 排列，每次可交换相邻两项，求把它变成升序需要的最少次数（==逆序对）。

**思路**：直接用归并统计逆序对。

💡 类比"交换修正"：每次邻位交换减少一逆序对，最少次数即逆序对数：

```python
def ms(a):
    if len(a) <= 1:
        return 0, a
    m = len(a)//2
    c1, l = ms(a[:m]); c2, r = ms(a[m:])
    i = j = 0; c = c1 + c2; res = []
    while i < len(l) and j < len(r):
        if l[i] <= r[j]:
            res.append(l[i]); i += 1
        else:
            res.append(r[j]); c += len(l)-i; j += 1
    res += l[i:] + r[j:]
    return c, res
n = int(input())
a = list(map(int, input().split()))
print(ms(a)[0])
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.53 例 53：食堂排队最少违纪（自定义）⭐
> **知识点**：统计、两侧贪心｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：一排座位 'L'(左撇) 'R'(右撇)，一个人坐下若左右有同向者即可优先坐。问最少有几人无邻座可坐。

**思路**：纯 L 或纯 R 段内除两端都可坐，统计相邻同向对。

💡 类比"找同伴挨坐"：统计相邻两个同一方向的对数即是能挨坐的人数：

```python
s = input().strip()
cnt = 0
for i in range(len(s)-1):
    if s[i] == s[i+1]:
        cnt += 1
print(cnt)
```
> **复杂度**：O(L) 时间，O(1) 空间

---
#### 17.2.54 例 54：最省搭配买套餐（自定义）⭐⭐
> **知识点**：排序取整、捆绑打包｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：小杯与大杯咖啡，小杯价 a、大杯价 b 且大杯容量是小杯 3 倍。要买恰好 X 份小杯容量，求最低总价（可用大杯超量）。

**思路**：比较买 3 个小杯 vs 1 个大杯的单价，先贪多用更省的，再用剩下的配。

💡 类比"大杯性价比"：若 3 小杯比 1 大杯贵就先买大杯，剩下零头再挑小的：

```python
X, a, b = map(int, input().split())
if b <= 3 * a:
    ans = (X // 3) * b
    rem = X % 3
    ans += min(rem * a, b)
else:
    ans = X * a
print(ans)
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.2.55 例 55：最大胜利回合（自定义）⭐⭐
> **知识点**：战力求和、先礼损失｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 场战斗各有敌方战力 a_i 与奖励战力 b_i，初始战力 x，每场先扣 a_i 若能赢（赢得下）再加 b_i，求最多能打赢几场。

**思路**：按"输掉战斗最少损失b-a越大越亏"思路，优先打"需要的少、奖励多"的，按 b-a 从大到小处理不可行则用排序法（此处演示按当前可打赢的贪心取 pre 小者）。

💡 类比"先易后难练级"：先把目前打得过的且加战力多的打赢变大：

```python
n, x = map(int, input().split())
a = []
for _ in range(n):
    ai, bi = map(int, input().split())
    a.append((ai, bi))
a.sort(key=lambda p: p[0])  # 需要的战力小的先打
cnt = 0
for ai, bi in a:
    if x >= ai:
        x += bi
        cnt += 1
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.56 例 56：最少分组让组内最大降幅≤k（自定义）⭐⭐
> **知识点**：排序、跨度分组｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数要分进若干组，组内任意两个数之差≤k，求最少组数。

**思路**：排序后贪心，每组的开头取最小未分组数，往后能放进的都放进一组。

💡 类比"按身高分段"：都从最矮的起一段，把差不超过 k 的划进同批：

```python
n, k = map(int, input().split())
a = sorted(map(int, input().split()))
cnt = 0
i = 0
while i < n:
    cnt += 1
    base = a[i]
    while i < n and a[i] - base <= k:
        i += 1
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间
#### 17.2.57 例 57：最小总代价合并果子（洛谷 P1090）⭐⭐
> **知识点**：优先队列、贪心最小合并代价｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 堆果子每堆重量 a_i，每次可合并任意两堆，代价为重量和求把全部合成一堆的最少总代价。

**思路**：每次合并最小的两堆，用小顶堆。

💡 类比"并小沙堆最省"：越早合并的小堆越省，每次取最轻两堆：

```python
import heapq
n = int(input())
a = list(map(int, input().split()))
heapq.heapify(a)
tot = 0
while len(a) > 1:
    x = heapq.heappop(a); y = heapq.heappop(a)
    s = x + y
    tot += s
    heapq.heappush(a, s)
print(tot)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.58 例 58：能到达目标的最少加油（自定义/CF 变式）⭐⭐
> **知识点**：贪心+优先队列、距离推进｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从家到公司距离 D，油箱可续航任意但初始有 P 油，路上加油站（距家位置、可加量），每单位油走 1，求最少加几次油能到公司。

**思路**：能走的就到，路过就进堆；油尽时取最大的加，直到能到或失败。

💡 类比"开到哪桩到哪"：把能开到的加油站先收起来，油尽时取加油最多的：

```python
import heapq
D, P = map(int, input().split())
n = int(input())
st = [tuple(map(int, input().split())) for _ in range(n)]
st.sort(key=lambda p: p[0])
q = []
i = 0
fuel = P
cnt = 0
while fuel < D:
    while i < n and st[i][0] <= fuel:
        heapq.heappush(q, -st[i][1])
        i += 1
    if not q:
        cnt = -1
        break
    fuel += -heapq.heappop(q)
    cnt += 1
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.59 例 59：伙伴结对最大配对（自定义）⭐⭐
> **知识点**：排序双指针、目标配对｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个选手水平值，两两配对训练，要求每对水平差在 [a,b] 区间，求最多配出几对。

**思路**：排序后双指针尽量配对相邻选手（贪心）。

💡 类比"相近搭档"：排好序尽量让能力接近的配对，成功对数最多：

```python
n, a, b = map(int, input().split())
v = sorted(map(int, input().split()))
used = [False]*n
cnt = 0
i = 0
while i < n:
    if used[i]:
        i += 1
        continue
    found = False
    for j in range(i+1, n):
        if not used[j] and a <= v[j] - v[i] <= b:
            used[i] = used[j] = True
            cnt += 1
            found = True
            break
    if not found:
        used[i] = True
    i += 1
print(cnt)
```
> **复杂度**：O(n²) 时间，O(n) 空间

---
#### 17.2.60 例 60：火箭燃料最省搭配（自定义）⭐⭐
> **知识点**：比例贪心、单价最小｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 种燃料各有单位含可量与单价，需要凑足至少 M 单位有效值，求最低总价（可超量，用量不限）。

**思路**：按"单位有效值单价"升序，优先买性价比最高的直到满足。

💡 类比"比价采购"：按每单位值价格从低到高买，凑够就停：

```python
n, M = map(int, input().split())
items = []
for _ in range(n):
    e, c = map(int, input().split())
    items.append((c/e, c, e))
items.sort()
tot = 0
need = M
for _, c, e in items:
    take = min(need, e)
    tot += take / e * c
    need -= take
    if need == 0:
        break
print(tot)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.61 例 61：老鼠搬粮最小损失（自定义）⭐⭐⭐
> **知识点**：比值贪心、双因子权衡｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个外卖盒子，第 i 个有美味 a_i、越放越差每小时掉 b_i。餐厅平均 b 分钟送出，求送餐顺序使总体损耗最小（按 a/b 排序）。

**思路**：按"越早做越能保值"规则，用 a_i/b_i 降序排序（比值贪心）。

💡 类比"先做易坏菜"：美味高又掉得快的菜先做，排序依据 a/b：

```python
n = int(input())
boxes = []
for _ in range(n):
    a, b = map(int, input().split())
    boxes.append((a / b, a, b))
# 比值 a/b 大的先送，能最大化保留美味总和（简化说明）
boxes.sort(reverse=True)
ans = 0
for _, a, b in boxes:
    ans += a            # 演示：按比值排序后的配送顺序累计美味
print(ans)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.62 例 62：最小差值拆分（自定义）⭐
> **知识点**：排序分组、奇偶分配｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数拆成两堆让和尽量接近（求最小绝对值差）。

**思路**：排序后交替把最大放轻的一堆（演示近似，可加 DP 增强）。

💡 类比"两边抬杠平衡"：每次把最重的放到较轻那边，让天平尽量平：

```python
n = int(input())
a = sorted(map(int, input().split()))
s1 = s2 = 0
l, r = 0, n-1
while l <= r:
    if s1 <= s2:
        s1 += a[r]
    else:
        s2 += a[r]
    r -= 1
print(abs(s1 - s2))
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.63 例 63：线段覆盖选点最少（自定义）⭐⭐
> **知识点**：右端点贪心、选点覆盖区间｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个闭区间，选尽量少的点使得每个区间都至少含有一个被选点。

**思路**：按右端点升序，逢当前点无法覆盖该区间则在该区间右端点放新点。

💡 类比"路灯覆盖街区"：在能看最远的右端点放灯，让一个灯覆盖最多区间：

```python
n = int(input())
iv = [tuple(map(int, input().split())) for _ in range(n)]
iv.sort(key=lambda x: x[1])
cnt = 0
last = -1
for l, r in iv:
    if last < l:
        cnt += 1
        last = r
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.64 例 64：最少去重撞击（自定义）⭐⭐
> **知识点**：涂色排序、去重计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一行 n 个球，颜色为 c_i，每次可把一整个连续同色段直接清掉（如消消乐），求最少清零步数。

**思路**：先把连续相同的段合并起来统计段数，用区间 DP 处理消消乐最优（此处演示段计数法简化）。

💡 类比"消除相同色块"：相同颜色挤一起的一段算一单位，段越少步数越省：

```python
n = int(input())
c = list(map(int, input().split()))
# 合并连续相同段
seg = []
for x in c:
    if not seg or seg[-1] != x:
        seg.append(x)
k = len(seg)
# 区间dp计算最少清空步数（相邻同色段合并仍有增益的分支从简）
dp = [[k]*(k) for _ in range(k)]
for i in range(k):
    dp[i][i] = 1
for length in range(2, k+1):
    for i in range(k-length+1):
        j = i+length-1
        dp[i][j] = dp[i+1][j] + 1
        if seg[i] == seg[j]:
            for m in range(i, j):
                if seg[m] == seg[j]:
                    dp[i][j] = min(dp[i][j], dp[i][m-1] + dp[m+1][j-1]) if m > i else min(dp[i][j], dp[m+1][j-1])
print(dp[0][k-1])
```
> **复杂度**：O(k³) 时间，O(k²) 空间

---
#### 17.2.65 例 65：区间合并最小次数去痕（自定义）⭐⭐
> **知识点**：区间覆盖长度、去重叠计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个线段（可重叠），把它们拼接，求拼接后覆盖的总长度。

**思路**：按左端点排序，维护当前合并段右端点，延伸或新开段。

💡 类比"接几条皮筋"：把重叠的接续成一段段，只算不重叠的净长度：

```python
n = int(input())
iv = [tuple(map(int, input().split())) for _ in range(n)]
iv.sort()
total = 0
l, r = iv[0]
for a, b in iv[1:]:
    if a <= r:
        r = max(r, b)
    else:
        total += r - l
        l, r = a, b
total += r - l
print(total)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.66 例 66：最少金币面值（数学）⭐⭐
> **知识点**：进制贪心、覆盖能力｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：要用最少的"面值种类"使得任意 1..m 都能被这些面值凑出（每种不限），求最少种类数（magic 面值翻倍贪心）。

**思路**：维护当前可覆盖上限，每加一种面值即 +1 再乘以覆盖能力翻倍。

💡 类比"发优惠券凑整"：每加一种券就能把可覆盖范围扩大一倍，是最省种类：

```python
m = int(input())
k = 0
reach = 0
while reach < m:
    reach = reach * 2 + 1
    k += 1
print(k)
```
> **复杂度**：O(log m) 时间，O(1) 空间

---
#### 17.2.67 例 67：最少能量清障（自定义）⭐
> **知识点**：障碍差分、覆盖统计｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：一排 n 个格点，有若干石头在位置处。用威力为 L 的爆炸可清掉一个区间，求最少炸几次清完。

**思路**：位置排序，贪心每炸覆盖最远。

💡 类比"定点爆破"：从最左的石头炸，把爆炸范围能波及的石头一把清掉：

```python
n, L = map(int, input().split())
p = sorted(map(int, input().split()))
cnt = 0
i = 0
while i < len(p):
    cnt += 1
    reach = p[i] + L
    while i < len(p) and p[i] <= reach:
        i += 1
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.68 例 68：最长递增子序列（LIS）长度（洛谷 P3902）⭐⭐
> **知识点**：贪心+二分维护尾部｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数，求最长严格递增子序列长度。

**思路**：维护一个单调尾数组 tail，逐个用二分替换，长度即答案。

💡 类比"接龙找最长链"：把各长度的最小结尾记下来，后续尽量接更长：

```python
import bisect
n = int(input())
a = list(map(int, input().split()))
tail = []
for x in a:
    i = bisect.bisect_left(tail, x)
    if i == len(tail):
        tail.append(x)
    else:
        tail[i] = x
print(len(tail))
```
> **复杂度**：O(n log n) 时间，O(n) 空间
#### 17.2.69 例 69：最小区间调度（自定义）⭐⭐
> **知识点**：工作优先级、两种维度贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个任务，每个需工作时间 t_i 与截止时间 d_i，单机执行。求能否全部在各自截止前完成（按截止排序判断）。

**思路**：按截止时间升序安排，累计当前时间检查是否超截止。

💡 类比"交作业倒排期"：先做截止早的，看会不会压线：

```python
n = int(input())
tasks = []
for _ in range(n):
    t, d = map(int, input().split())
    tasks.append((d, t))
tasks.sort()
cur = 0
ok = True
for d, t in tasks:
    cur += t
    if cur > d:
        ok = False
        break
print("YES" if ok else "NO")
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.70 例 70：尽可能多的不冲突表演（自定义）⭐
> **知识点**：右端点排序、区间选择｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 场演出有开始/结束时间，每场演出不重叠，求最多举行几场。

**思路**：按结束时间升序贪心选择。

💡 类比"抢舞台档期"：先办最先结束的，留给后面的时间段最大：

```python
n = int(input())
iv = [tuple(map(int, input().split())) for _ in range(n)]
iv.sort(key=lambda x: x[1])
cnt = 0
end = -1
for s, e in iv:
    if s >= end:
        cnt += 1
        end = e
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.71 例 71：分披萨最大块（自定义）⭐⭐
> **知识点**：等分最大最小、二分答案思想｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 块披萨半径 r_i，要切给 K 个小朋友每块大小相等，问每块能得到的最大披萨面积（切完可丢弃剩余）。

**思路**：二分每块目标面积，检查能否切出 K 块。

💡 类比"切披萨分人"：猜一块能做多大，看够不够切出所有人那份：

```python
import math
n, K = map(int, input().split())
r = list(map(int, input().split()))
area = [math.pi * x * x for x in r]
lo, hi = 0.0, max(area)
for _ in range(60):
    mid = (lo + hi) / 2
    if mid == 0:
        break
    cnt = sum(int(a / mid) for a in area)
    if cnt >= K:
        lo = mid
    else:
        hi = mid
print("%.6f" % lo)
```
> **复杂度**：O(n log precision) 时间，O(1) 空间

---
#### 17.2.72 例 72：等值子数组最长（自定义）⭐⭐
> **知识点**：前缀差平衡、贪心扫描｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：01 序列，求包含 '0' 与 '1' 个数相等的最长连续子段长度。

**思路**：把 0 当 -1、1 当 +1，找前缀和相等的最远间距。

💡 类比"平衡子串"：前缀和出现重复说明那一段 0/1 平衡：

```python
s = input().strip()
n = len(s)
mp = {0: -1}
cur = 0
ans = 0
for i, ch in enumerate(s):
    cur += 1 if ch == '1' else -1
    if cur in mp:
        ans = max(ans, i - mp[cur])
    else:
        mp[cur] = i
print(ans)
```
> **复杂度**：O(L) 时间，O(L) 空间

---
#### 17.2.73 例 73：最少转弯机器人路线（自定义）⭐⭐
> **知识点**：方位模拟、转弯计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：机器人从起点出发按指令(直线走动)绕障，给定一串方向指令序列，求实际转弯次数（相对初始朝向）。

**思路**：模拟朝向，相邻两次方向不同则转弯计数。

💡 类比"汽车方向灯"：只有真正改朝向才闪灯计数：

```python
op = list(input().strip().split())
dirs = {'N':0,'E':1,'S':2,'W':3}
facing = 0  # 初始朝北
turns = 0
for x in op:
    d = dirs[x]
    diff = (d - facing) % 4
    if diff == 1 or diff == 3:
        turns += 1
    elif diff == 2:
        turns += 2
    facing = d
print(turns)
```
> **复杂度**：O(L) 时间，O(1) 空间

---
#### 17.2.74 例 74：最优加油替代站（自定义）⭐⭐⭐
> **知识点**：贪心合并、中转最优｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个中转点坐标，卡车从 0 到 D，需经过恰 M 个中转点停靠加油（油桶容量可认为足），每段都有不同耗油，求最少停 3 次问题简化：求经过所有点到达 D 时选择 M 个站点加油使耗油最少。

**思路**：简化表述为：给定每段距离，停靠越少越省，求最少加油次数使续航足够，用优先队列贪心（同加油站）。

💡 类比"续航规划"：每到一个点争取满油，不够就先加油再走：

```python
import heapq
D, P = map(int, input().split())
n = int(input())
sts = [tuple(map(int, input().split())) for _ in range(n)]
sts.sort()
q = []
i = 0
fuel = P
cnt = 0
while fuel < D:
    while i < n and sts[i][0] <= fuel:
        heapq.heappush(q, -sts[i][1])
        i += 1
    if not q:
        cnt = -1
        break
    fuel += -heapq.heappop(q)
    cnt += 1
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.75 例 75：最少裁剪让旗子等宽（自定义）⭐⭐
> **知识点**：背包变体、容量贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 k 段布长度 l_i，要从这些布裁出 n 段等长小条，求小条最长能多长（每段最多裁一次改成可多次裁剪的重题说明，这里求并用二分长度判断）。

**思路**：二分等长小条长度，检查总段数是否≥n。

💡 类比"量布裁条"：先猜每根多长，看每段布能裁出几根满不够：

```python
n, k = map(int, input().split())
l = list(map(int, input().split()))
def ok(x):
    if x == 0:
        return True
    return sum(int(v // x) for v in l) >= n
lo, hi = 0, max(l)
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(k log max) 时间，O(1) 空间

---
#### 17.2.76 例 76：糖果卡车最大装载（自定义）⭐⭐
> **知识点**：条件排序、装载贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个包裹，每个有重量与价值，(简化：价值由优先送达顺序决定)，卡车上限 C 重量，求最大总价值（0/1 背包雏形，大 C 用贪心单位价值）。

**思路**：按单位价值降序装载，若能整放则整放否则按比例（分数背包）。

💡 类比"挑进购物车"：先拿单位价值最高的，装不下再考虑部分：

```python
C, n = map(int, input().split())
items = []
for _ in range(n):
    w, v = map(int, input().split())
    items.append((v / w, w, v))
items.sort(reverse=True)
val = 0.0
for ratio, w, v in items:
    if C >= w:
        val += v
        C -= w
    else:
        val += ratio * C
        break
print(val)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.2.77 例 77：最少补水站里程（自定义）⭐⭐
> **知识点**：端点贪心、断油检测｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：沙漠穿越距离 D，起点有 P 升水，每公里耗 1，沿途若干补水点，求到达终点最少补水次数（每次补满到 P）。

**思路**：维护当前可推进的最大距离，沿途可选补水点推进；断油即失败，选能补给最多的。

💡 类比"沙漠找井"：把能到达范围内的井都记下，渴了喝最足的那口：

```python
import heapq
D, P = map(int, input().split())
n = int(input())
wells = [tuple(map(int, input().split())) for _ in range(n)]
wells.sort()
q = []
i = 0
fuel = P
cnt = 0
while fuel < D:
    while i < n and wells[i][0] <= fuel:
        heapq.heappush(q, -wells[i][1])
        i += 1
    if not q:
        cnt = -1
        break
    fuel += -heapq.heappop(q)
    cnt += 1
print(cnt)
```
> **复杂度**：O(n log n) 时间，O(n) 空间

---
#### 17.2.78 例 78：买票最划算组合（自定义）⭐⭐
> **知识点**：次方取整、面额贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：单程票 S 元，三日票 T 元（3 天无限乘），需坐 n 天，求至少覆盖 n 天需要买多少（求买票最小花费组合封面演示）。单日游天可用单程或多日票覆盖，求最少花费。

**思路**：演示：设 3 日票比 3 张单程票划算时先尽量用 3 日票。

💡 类比"套票划算"：日票划算就优先套票，剩余天数单日买：

```python
n, S, T = map(int, input().split())
if T <= 3 * S:
    print((n // 3) * T + min(n % 3 * S, T))
else:
    print(n * S)
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.2.79 例 79：房间空调最少开关（自定义）⭐⭐
> **知识点**：温度贪心、预告累积｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：每天目标温度 a_i，空调每个单位时间只能 +1 或 -1，求一天几段连续变温最少要操作多少次开关（求相邻趋势变化次数）。

**思路**：统计累计到目标需要的总操作，等价"补齐斜坡"，相邻涨幅为正部分累加。

💡 类比"调温不陡"：只累加正的涨幅段（台阶上行的净增量）：

```python
n = int(input())
a = list(map(int, input().split()))
cur = 0
op = 0
for x in a:
    if x > cur:
        op += x - cur
    cur = x
print(op)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.2.80 例 80：围栏修最省木板（自定义·综合贪心）⭐⭐⭐
> **知识点**：差值累计、单峰贪心｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 段围栏高度 a_i，每次操作可把任意连续段整体 +1 或 -1，求还原为全 0 的最少操作次数（等价铺地砖）。

**思路**：对邻位高度差的正部分求和即为最少步数。

💡 类比"抹平土坡"：每次能同时调整一段，只需数净上涨的台阶数：

```python
n = int(input())
a = list(map(int, input().split()))
ans = abs(a[0])
for i in range(1, n):
    if a[i] > a[i-1]:
        ans += a[i] - a[i-1]
    elif a[i] < a[i-1]:
        ans += a[i-1] - a[i]
print(ans)
```
> **复杂度**：O(n) 时间，O(1) 空间

### 17.3 二分与三分

#### 17.3.1 例 1：二分查找经典（POJ 2002 变式）⭐
> **知识点**：二分查找、有序数组｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给一个升序数组与若干查询，对每个查询输出其下标（从 0 起）或 -1。

**思路**：标准二分查找第一个匹配位置。

💡 类比"猜页码翻半本"：每次对半翻书，比目标大往左、小往右：

```python
n, m = map(int, input().split())
a = list(map(int, input().split()))
q = list(map(int, input().split()))
for target in q:
    lo, hi = 0, n-1
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            ans = mid
            break
        elif a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    print(ans)
```
> **复杂度**：O(m log n) 时间，O(1) 空间

---
#### 17.3.2 例 2：二分求平方根（洛谷 P1426 变式）⭐
> **知识点**：浮点二分、精度控制｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定非负实数 x，求其平方根，精确到 6 位小数。

**思路**：对答案区间 [0,x] 二分，直到区间足够小。

💡 类比"逼近猜数"：在 0 和 x 之间反复对半，收敛到根附近：

```python
x = float(input())
lo, hi = 0.0, max(1.0, x)
for _ in range(60):
    mid = (lo + hi) / 2
    if mid * mid < x:
        lo = mid
    else:
        hi = mid
print("%.6f" % lo)
```
> **复杂度**：O(log precision) 时间，O(1) 空间

---
#### 17.3.3 例 3：最大值最小化任务切分（POJ 1064 变式）⭐
> **知识点**：二分答案、可行性判断｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 段木头长度，要截出 k 段等长木料，求每段最长的可能长度。

**思路**：二分每段长度，检查能截出的段数是否≥k。

💡 类比"扎竹签"：猜每根能多长，看总根数够不够：

```python
n, k = map(int, input().split())
L = [int(input()) for _ in range(n)]
def ok(x):
    return sum(v // x for v in L) >= k
lo, hi = 0, max(L)
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(n log max) 时间，O(1) 空间

---
#### 17.3.4 例 4：二分找旋转数组最小值（经典变式）⭐⭐
> **知识点**：旋转数组、二分夹逼｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一个升序数组在某点旋转（如 [3,4,5,1,2]），无重复元素，求最小值。

**思路**：比较 mid 与右端，判断最小值落在哪一半。

💡 类比"转圈找最低谷"：看中间和右端谁小，决定往一段走：

```python
a = list(map(int, input().split()))
lo, hi = 0, len(a)-1
while lo < hi:
    mid = (lo + hi) // 2
    if a[mid] > a[hi]:
        lo = mid + 1
    else:
        hi = mid
print(a[lo])
```
> **复杂度**：O(log n) 时间，O(1) 空间

---
#### 17.3.5 例 5：二分查找最近值（自定义）⭐
> **知识点**：二分定位、双端比较｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：升序数组，对每个查询输出与它绝对值差最小的元素。

**思路**：二分出插入位置，比较左右两个候选。

💡 类比"找最近的站牌"：二分到目标附近的站，再比较前后两个谁近：

```python
import bisect
n, m = map(int, input().split())
a = sorted(map(int, input().split()))
q = list(map(int, input().split()))
for x in q:
    i = bisect.bisect_left(a, x)
    cands = []
    if i < n:
        cands.append(a[i])
    if i > 0:
        cands.append(a[i-1])
    cands.sort(key=lambda v: (abs(v-x), v))
    print(cands[0])
```
> **复杂度**：O(m log n) 时间，O(1) 空间

---
#### 17.3.6 例 6：最小化最大值之平分数组（POJ 3273）⭐⭐⭐
> **知识点**：二分答案、连续分组｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数的数组，要划分成 m 个连续段，使所有段和的最大值最小，求该最小值。

**思路**：二分答案 s，检查能否分成不超过 m 段且每段和≤s。

💡 类比"均摊账单"：猜每段上限，看能否分出 m 段以内：

```python
n, m = map(int, input().split())
a = list(map(int, input().split()))
def ok(s):
    cap = 0
    seg = 1
    for x in a:
        if cap + x > s:
            seg += 1
            cap = x
        else:
            cap += x
    return seg <= m
lo, hi = max(a), sum(a)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log sum) 时间，O(1) 空间

---
#### 17.3.7 例 7：最大化最小值之气球距离（POJ 2456）⭐⭐⭐
> **知识点**：二分答案、贪心放置｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个牛棚坐标，放 m 头牛，使任意两头牛的最近距离尽可能大，求这个最大最近距离。

**思路**：二分距离 d，贪心验证能否按间距≥d 放下 m 头。

💡 类比"隔开吵架的牛"：猜最小间隔，让牛尽量靠远点排看看能否放得下：

```python
n, m = map(int, input().split())
x = sorted(map(int, input().split()))
def ok(d):
    cnt = 1
    last = x[0]
    for v in x[1:]:
        if v - last >= d:
            cnt += 1
            last = v
    return cnt >= m
lo, hi = 1, x[-1] - x[0]
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(n log range) 时间，O(1) 空间

---
#### 17.3.8 例 8：三分求凸函数极大值（自定义）⭐
> **知识点**：三分法、单峰函数｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：一元二次函数 f(x) 有唯一最大值，在定义域上求最大值的坐标与函数值。

**思路**：三分法不断缩小区间，比较两个三等分点取值。

💡 类比"登山找峰"：在左右三分点比高低，高的那边更靠近山顶：

```python
def f(x):
    return -x*x + 3*x + 5   # 凸函数（开口向下）
lo, hi = -10.0, 10.0
for _ in range(60):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    if f(m1) < f(m2):
        lo = m1
    else:
        hi = m2
print("%.6f %.6f" % ((lo+hi)/2, f((lo+hi)/2)))
```
> **复杂度**：O(log precision) 时间，O(1) 空间

---
#### 17.3.9 例 9：二分搜索插入位置（自定义）⭐
> **知识点**：二分边界、插入下标｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：升序数组与目标值 x，求 x 若插入并保持有序应放的下标。

**思路**：二分第一个 ≥x 的位置（lower_bound）。

💡 类比"插队排队"：找到第一个不小于自己的位置站进去：

```python
n = int(input())
a = list(map(int, input().split()))
x = int(input())
lo, hi = 0, n
while lo < hi:
    mid = (lo + hi) // 2
    if a[mid] < x:
        lo = mid + 1
    else:
        hi = mid
print(lo)
```
> **复杂度**：O(log n) 时间，O(1) 空间

---
#### 17.3.10 例 10：收谷物最少天数（洛谷 P1824）⭐⭐
> **知识点**：二分答案、需求检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：收割 k 公顷谷物需要机器，两种机各需时间，问最少几天收完（简化为给定每日可收量与总量，求天数）。

**思路**：二分天数 x，若每天可收量×天数≥总量则可行。

💡 类比"算工期"：猜几天收得完，日产量×天数够不够总量：

```python
k, per_day = map(int, input().split())
def ok(d):
    return per_day * d >= k
lo, hi = 1, k
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(log k) 时间，O(1) 空间
#### 17.3.11 例 11：二分找山峰（洛谷 P3865 变式）⭐
> **知识点**：峰值查找、二分下降｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：一个先增后减的数组（无相邻相等），找出峰值所在下标。

**思路**：二分，若 a[mid]>a[mid+1] 峰值在左半侧否则在右半侧。

💡 类比"沿坡找顶"：中间比右边高说明顶峰在左边段：

```python
a = list(map(int, input().split()))
lo, hi = 0, len(a)-1
while lo < hi:
    mid = (lo + hi) // 2
    if a[mid] > a[mid+1]:
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(log n) 时间，O(1) 空间

---
#### 17.3.12 例 12：浮点二分求方程根（自定义）⭐⭐
> **知识点**：单调方程、浮点二分｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求方程 x³ = a 的实数根，精确到 6 位（a≥0）。

**思路**：在[0, 上界]三分/二分求 x 使 x³ 逼近 a。

💡 类比"反函数逼近"：猜 x，看立方的结果与 a 相比往哪边调：

```python
a = float(input())
lo, hi = 0.0, max(1.0, a)
for _ in range(60):
    mid = (lo + hi) / 2
    if mid**3 < a:
        lo = mid
    else:
        hi = mid
print("%.6f" % lo)
```
> **复杂度**：O(log precision) 时间，O(1) 空间

---
#### 17.3.13 例 13：电量分组最少缺电（POJ 常考变式）⭐⭐
> **知识点**：二分最大容量、可行性判定｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 块电池电量各不相同，要平均分到 m 个容器且每个容器总电量不超过上限 cap，求最小 cap 使能放下（等价连续划分，但电池可乱序，用二分"能否装完 m 桶"）。

**思路**：二分 cap，贪心地装当前桶直到超限再开新桶。

💡 类比"装箱流水线"：一只桶塞到快满再换下一只，看能否装进 m 桶：

```python
n, m = map(int, input().split())
a = list(map(int, input().split()))
def ok(cap):
    buckets = 1
    cur = 0
    for x in a:
        if x > cap:
            return False
        if cur + x > cap:
            buckets += 1
            cur = x
        else:
            cur += x
    return buckets <= m
lo, hi = max(a), sum(a)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log sum) 时间，O(1) 空间

---
#### 17.3.14 例 14：跳格子最少移除（洛谷 P2678）⭐⭐
> **知识点**：二分答案、跳距贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：起点 0 终点 L，途中有 n 块石头坐标递增，可移走至多 m 块，求最短跳跃距离的最大值。

**思路**：二分最短跳距 d，检查保留下来相邻有效石头间距至少为 d 需要的移走数是否≤m。

💡 类比"抽掉碍事石头"：规定每跳至少 d，数至少要抽走几块：

```python
L, n, m = map(int, input().split())
st = [int(input()) for _ in range(n)]
st.append(L)
def ok(d):
    cnt = 0
    prev = 0
    for x in st:
        if x - prev < d:
            cnt += 1
        else:
            prev = x
    return cnt <= m
lo, hi = 1, L
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(n log L) 时间，O(1) 空间

---
#### 17.3.15 例 15：二分求最接近目标的三元素和（自定义）⭐⭐
> **知识点**：排序+双指针、最接近和｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数，选三个使和最接近给定目标 T，输出最接近的和。

**思路**：排序后固定一个，用双指针找最接近的另两个。

💡 类比"三拼拼骰子"：固定一个再移动左右指针逼近目标：

```python
n = int(input())
a = sorted(map(int, input().split()))
T = int(input())
best = None
for i in range(n-2):
    l, r = i+1, n-1
    while l < r:
        s = a[i] + a[l] + a[r]
        if best is None or abs(s - T) < abs(best - T):
            best = s
        if s < T:
            l += 1
        else:
            r -= 1
print(best)
```
> **复杂度**：O(n²) 时间，O(1) 空间

---
#### 17.3.16 例 16：分牛连续和最小差（自定义）⭐⭐
> **知识点**：前缀和、二分答案｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数要分为 k 组（连续），使各组和尽量均匀即最大一组和最小，求最小可能的最大组和（即最小化最大值）。

**思路**：二分答案 x，贪心分段验证。

💡 类比"分批次加工"：限制每批和不超过 x，看能否 1..k 批装完：

```python
n, k = map(int, input().split())
a = list(map(int, input().split()))
def ok(x):
    seg = 1
    cur = 0
    for v in a:
        if cur + v > x:
            seg += 1
            cur = v
        else:
            cur += v
    return seg <= k
lo, hi = max(a), sum(a)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log sum) 时间，O(1) 空间

---
#### 17.3.17 例 17：全部装车最少车数（自定义）⭐⭐
> **知识点**：二分运载上限、贪心分车｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 件货物重量，每辆车限载上限可自定义，用恰好 m 辆车装完（顺序不可乱），求单辆车最小载重。

**思路**：二分单车载重，验证可分车数≤m。

💡 类比"安排车队"：限每车装多少，算算要几辆车，太多就加载重：

```python
n, m = map(int, input().split())
w = list(map(int, input().split()))
def ok(cap):
    cnt = 1
    cur = 0
    for x in w:
        if cur + x > cap:
            cnt += 1
            cur = x
        else:
            cur += x
    return cnt <= m
lo, hi = max(w), sum(w)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log sum) 时间，O(1) 空间

---
#### 17.3.18 例 18：三分求凹函数极小（自定义）⭐
> **知识点**：三分法、单谷函数｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：一元函数有唯一最小值（单谷），在定义域上求最小值及对应 x。

**思路**：三分比较两三分点，向较小的一侧逼近谷底。

💡 类比"下坡找谷"：两三分点谁低就往谁那边缩小范围：

```python
def f(x):
    return (x - 3) ** 2 + 2   # 单谷
lo, hi = -10.0, 10.0
for _ in range(60):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    if f(m1) < f(m2):
        hi = m2
    else:
        lo = m1
mid = (lo + hi) / 2
print("%.6f %.6f" % (mid, f(mid)))
```
> **复杂度**：O(log precision) 时间，O(1) 空间

---
#### 17.3.19 例 19：二分求最小覆盖半径（自定义）⭐⭐
> **知识点**：二分求半径、贪心覆盖点｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：数轴上 n 个点，用 r 个半径为 L 的圆盘覆盖所有点，求最小半径 L。

**思路**：二分半径 L，贪心验证能否覆盖。

💡 类比"路灯半径优化"：猜灯照多远，看几盏灯能否波及全部点：

```python
n, r = map(int, input().split())
p = sorted(map(int, input().split()))
def ok(L):
    cnt = 1
    cover = p[0] + L
    for x in p:
        if x > cover:
            cnt += 1
            cover = x + L
    return cnt <= r
lo, hi = 0.0, float(p[-1] - p[0])
for _ in range(60):
    mid = (lo + hi) / 2
    if ok(mid):
        hi = mid
    else:
        lo = mid
print("%.6f" % hi)
```
> **复杂度**：O(n log precision) 时间，O(1) 空间

---
#### 17.3.20 例 20：母牛产奶最少天（自定义）⭐⭐
> **知识点**：二分答案、持续性检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：每天产奶 m 桶（点滴式），仓库容量 C 吨，产满就停，问过程需至少多少天才攒够 target 桶（简化二分天）。

**思路**：二分天数 d，天×m 是否≥target。

💡 类比"攒积分兑换"：猜要攒多少天，天数×每天量够不够兑换值：

```python
target, m = map(int, input().split())
lo, hi = 1, target
while lo < hi:
    mid = (lo + hi) // 2
    if mid * m >= target:
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(log target) 时间，O(1) 空间
#### 17.3.21 例 21：管道运水最大流速（洛谷 P3374 变式）⭐⭐
> **知识点**：二分答案、最大流判定（简化）｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 段水管各有限流 c_i 与长度 l_i，水同向往一个方向流到终点，总流速为各段流经的最小值，问在 t 时间内能否输送 V 体积（简化）。

**思路**：二分总流速 v，验证 v×t 是否≥V。

💡 类比"瓶颈漏斗"：总流速受最细管的限制，算流量够不够：

```python
n = int(input())
c = []
l = []
for _ in range(n):
    ci, li = map(int, input().split())
    c.append(ci); l.append(li)
V, t = map(int, input().split())
max_flow = min(c)
def ok(v):
    return v * t >= V
lo, hi = 0, max_flow
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo if lo * t >= V else -1)
```
> **复杂度**：O(n + log max) 时间，O(1) 空间

---
#### 17.3.22 例 22：寻找重复数的区间二分（自定义）⭐⭐
> **知识点**：抽屉原理、计数二分｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n+1 个数取自 1..n，保证恰有一个重复，找出该重复数（空间限制小，要求不用额外大数组）。

**思路**：二分"值域"，统计≤mid 的个数判断重复落在哪半。

💡 类比"按号段数人"：看 1..mid 里人数是不是大于格子数，来决定重复在哪段：

```python
n = int(input())
a = list(map(int, input().split()))
lo, hi = 1, n
while lo < hi:
    mid = (lo + hi) // 2
    cnt = sum(1 for x in a if x <= mid)
    if cnt > mid:
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.3.23 例 23：最大化最小给薪（自定义）⭐⭐
> **知识点**：二分答案、组合验证｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 名员工技能 a_i，需组成 k 组，每组人数≥2 且技能差≤x 才行，求最小的可行 x 使能组出 k 组。

**思路**：二分 x，贪心地邻近配对检验。

💡 类比"撮合搭档"：猜容忍差距，排好序尽量把差距小的人凑对：

```python
n, k = map(int, input().split())
a = sorted(map(int, input().split()))
def ok(x):
    cnt = 0
    i = 0
    used = [False]*n
    while i < n-1:
        if not used[i] and a[i+1] - a[i] <= x:
            cnt += 1
            used[i] = used[i+1] = True
            i += 2
        else:
            i += 1
    return cnt >= k
lo, hi = 0, 10**9
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log range) 时间，O(n) 空间

---
#### 17.3.24 例 24：河流通过最少桥数（自定义）⭐⭐
> **知识点**：二分跨度、贪心架桥｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个河洲坐标，用长度为 L 的桥从起点到终点连通相邻洲，求最短桥长使能到达终点（每座桥两岸固定，求最大间隔）。

**思路**：答案即相邻坐标差的最大值。

💡 类比"搭桥最长一跨"：相邻两洲间距的最大值就是必须的最短桥长：

```python
n = int(input())
p = sorted(map(int, input().split()))
print(max(p[i+1] - p[i] for i in range(n-1)))
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.3.25 例 25：二分查找最后一个等于（自定义）⭐
> **知识点**：上界二分、后向搜索｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：升序数组含重复，给出目标 x，输出最后一次出现 x 的下标，没有则 -1。

**思路**：二分第一个>x 位置，其前一位即为最后等于。

💡 类比"找最后一个相同品"：先找到越过 x 的分界，前一个就是它：

```python
import bisect
n = int(input())
a = list(map(int, input().split()))
x = int(input())
r = bisect.bisect_right(a, x)
print(r - 1 if r > 0 and a[r-1] == x else -1)
```
> **复杂度**：O(log n) 时间，O(1) 空间

---
#### 17.3.26 例 26：最大化最小间距放棋子（洛谷 P2678 类）⭐⭐
> **知识点**：二分答案、间距验证｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：线段上 n 个可放点坐标，挑 m 个点使相邻挑中点的最小间距最大。

**思路**：二分间距 d，验证能否挑出≥m 个。

💡 类比"隔桩插旗"：每面旗间隔至少 d，数能插几面：

```python
n, m = map(int, input().split())
p = sorted(map(int, input().split()))
def ok(d):
    cnt = 1
    last = p[0]
    for x in p[1:]:
        if x - last >= d:
            cnt += 1
            last = x
    return cnt >= m
lo, hi = 1, p[-1] - p[0]
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(n log range) 时间，O(1) 空间

---
#### 17.3.27 例 27：三分求最大圆覆盖角度（自定义）⭐⭐
> **知识点**：三分、三角函数结合｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两点坐标，移动一点使被某半径圆覆盖的最长弧（演示为求某距离函数的最大值单峰）。

**思路**：对角度参数三分求单峰函数最大值。

💡 类比"调角度取最大覆盖"：角度两端低中间高，三分夹出峰：

```python
import math
def f(a):
    return math.sin(a) + math.sin(2*a)  # 单峰演示函数
lo, hi = 0.0, math.pi/2
for _ in range(60):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    if f(m1) < f(m2):
        lo = m1
    else:
        hi = m2
print("%.6f % .6f" % ((lo + hi)/2, f((lo+hi)/2)))
```
> **复杂度**：O(log precision) 时间，O(1) 空间

---
#### 17.3.28 例 28：最少加油站的二分（自定义）⭐⭐
> **知识点**：二分答案、加油站判定｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：数轴上 n 个加油站位置即可补油，但求两点间最大缺油段，为了全程不断油需要在空隙补建站，求补站后任意段长度不超过 K 面临最少补建数（简化为：把跨越最大空隙 K 分解）。

**思路**：二分每站覆盖半径 r，检查能否在 n 站覆盖全程；等价相邻间距里加 ceil(di/r)-1 个站。

💡 类比"补信号基站"：相邻站间距除以覆盖半径向上取整就是要补的站：

```python
n, K = map(int, input().split())
p = sorted(map(int, input().split()))
gaps = [p[i+1] - p[i] for i in range(n-1)]
def ok(r):
    need = 0
    for d in gaps:
        need += (d - 1) // r
    return need <= K
lo, hi = 1, max(gaps) if gaps else 1
if not gaps:
    print(0)
else:
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    print(lo)
```
> **复杂度**：O(n log range) 时间，O(1) 空间

---
#### 17.3.29 例 29：购书最便宜分册（自定义）⭐⭐
> **知识点**：二分每册容量、装册检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一份长文档要分成 k 册装订（每册顺序连续），希望每册页数尽量平均即最大册页数最小，求该值。

**思路**：二分每册页数上限 x，验证可分≤k 册。

💡 类比"分卷装书"：每册限 X 页，看能否分进 k 册内：

```python
n, k = map(int, input().split())
w = list(map(int, input().split()))
def ok(x):
    cnt = 1
    cur = 0
    for v in w:
        if cur + v > x:
            cnt += 1
            cur = v
        else:
            cur += v
    return cnt <= k
lo, hi = max(w), sum(w)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log sum) 时间，O(1) 空间

---
#### 17.3.30 例 30：全部赚够最少天（自定义）⭐⭐
> **知识点**：二分天、增长模型｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：银行每天利息使存款增长 r 倍（初始本金 P 元累计），问多少天后总额≥target（简化二分天）。

**思路**：二分天数 d，判断 P×(1+r)^d ≥ target。

💡 类比"利滚利算日子"：猜几天翻够，用乘幂检验够不够：

```python
P, r, target = map(int, input().split())
lo, hi = 1, target
while lo < hi:
    mid = (lo + hi) // 2
    if P * (1 + r) ** mid >= target:
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(log target) 时间，O(1) 空间
#### 17.3.31 例 31：最大化最小停靠距离（自定义）⭐⭐⭐
> **知识点**：二分答案、停车位贪心｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个停车坐标，要选 m 个位置停车使相邻停车最小间距最大。

**思路**：二分间距 d，验证能否挑≥m 个。

💡 类比"隔位停车"：要求间距至少 d，数数能停几台：

```python
n, m = map(int, input().split())
p = sorted(map(int, input().split()))
def ok(d):
    cnt, last = 1, p[0]
    for x in p[1:]:
        if x - last >= d:
            cnt += 1
            last = x
    return cnt >= m
lo, hi = 1, p[-1] - p[0]
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(n log range) 时间，O(1) 空间

---
#### 17.3.32 例 32：二进制中分数上限（自定义）⭐⭐
> **知识点**：二分答案、整除判定｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给 n 个数，问取其中 ≥x 个数的某种容量约束，求最大 x 使"第 k 大≥某值"（演示：求最大的 k 使存在 k 个数都≥mid）。

**思路**：二分 mid，统计 ≥mid 的个数是否≥k（此处输出最大 mid 使 count≥k）。

💡 类比"划线看多少人过线"：猜分数，数够不够 k 人达标：

```python
n, k = map(int, input().split())
a = list(map(int, input().split()))
def ok(x):
    return sum(1 for v in a if v >= x) >= k
lo, hi = 0, max(a)
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(n log range) 时间，O(1) 空间

---
#### 17.3.33 例 33：管道工程最少工期（自定义）⭐⭐
> **知识点**：二分工期、工时检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：每天最多能铺 L 米管道，总需铺 D 米（当天足量），问最少多少天完成。

**思路**：二分天数，天×L≥D。

💡 类比"铺管道排期"：每天进 L 米，算几天够总量：

```python
D, L = map(int, input().split())
lo, hi = 1, D
while lo < hi:
    mid = (lo + hi) // 2
    if mid * L >= D:
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(log D) 时间，O(1) 空间

---
#### 17.3.34 例 34：最小建筑费用（自定义）⭐⭐
> **知识点**：二分单参数、凸费用最小化｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：某成本函数为开口向上的凸函数（与某高度 h 相关），求使成本最小的 h（浮点）。

**思路**：三分法求凸（单谷）函数最小值。

💡 类比"调高度省材料"：成本先降后升，三分夹出谷底：

```python
def cost(h):
    # 演示凸函数，返回人工成本
    return (h - 5) ** 2 + 3
lo, hi = 0.0, 10.0
for _ in range(60):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    if cost(m1) < cost(m2):
        hi = m2
    else:
        lo = m1
print("%.6f" % cost((lo + hi) / 2))
```
> **复杂度**：O(log precision) 时间，O(1) 空间

---
#### 17.3.35 例 35：二分求离群点去除半径（自定义）⭐⭐
> **知识点**：二分半径、聚类计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个点坐标，希望用 k 个半径为 r 的圆覆盖全部点，求最小 r。

**思路**：二分 r，贪心用最左点作为圆左端覆盖能盖住的点。

💡 类比"圈地占地"：猜圈半径，让每个圆尽量往远盖：

```python
n, k = map(int, input().split())
x = sorted(map(float, input().split()))
def ok(r):
    cnt = 1
    cover = x[0] + 2 * r
    for v in x[1:]:
        if v > cover:
            cnt += 1
            cover = v + 2 * r
    return cnt <= k
lo, hi = 0.0, x[-1] - x[0]
for _ in range(60):
    mid = (lo + hi) / 2
    if ok(mid):
        hi = mid
    else:
        lo = mid
print("%.6f" % hi)
```
> **复杂度**：O(n log precision) 时间，O(1) 空间

---
#### 17.3.36 例 36：最少洒水装置（自定义）⭐⭐
> **知识点**：二分半径、覆盖检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个喷嘴位置，每个半径可调，要用 r 个装置让整条路的每点都被喷到（相邻重叠无缝），求最小半径。

**思路**：二分半径 r，验证相邻间隔 2r 内能否连接无缝。

💡 类比"接龙喷水"：两装置间距 ≤2r 才能无缝，检查能否连成一条线：

```python
n, r = map(int, input().split())
p = sorted(map(float, input().split()))
def ok(R):
    reach = p[0] + R
    for v in p[1:]:
        if v - R > reach + 1e-9:
            return False
        reach = max(reach, v + R)
    return True
lo, hi = 0.0, p[-1]
for _ in range(60):
    mid = (lo + hi) / 2
    if ok(mid):
        hi = mid
    else:
        lo = mid
print("%.6f" % hi)
```
> **复杂度**：O(n log precision) 时间，O(1) 空间

---
#### 17.3.37 例 37：全局求中位数二分（自定义）⭐⭐
> **知识点**：二分阈值、计数判断第 k 小｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数（未排序也演示），求第 k 小元素。

**思路**：二分值域，统计 ≤mid 的个数判断第 k 小在哪半。

💡 类比"猜及格线"：数滑到线以下的个数，判断第 k 个在线上还是线下：

```python
n, k = map(int, input().split())
a = list(map(int, input().split()))
k -= 1
lo, hi = min(a), max(a)
while lo < hi:
    mid = (lo + hi) // 2
    cnt = sum(1 for v in a if v <= mid)
    if cnt > k:
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log range) 时间，O(1) 空间

---
#### 17.3.38 例 38：全校分班最少人数（自定义）⭐⭐
> **知识点**：二分答案、容量检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数分成 m 组且每组和不能超过上限 cap，求最小 cap（顺序打乱版，用能装则装）。

**思路**：二分 cap，贪心 check。

💡 类比"打包限量"：每袋到上限就换下一袋，看能否 m 袋装完：

```python
n, m = map(int, input().split())
a = list(map(int, input().split()))
def ok(cap):
    bag = 1
    cur = 0
    for x in a:
        if cur + x > cap:
            bag += 1
            cur = x
        else:
            cur += x
    return bag <= m
lo, hi = max(a), sum(a)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log sum) 时间，O(1) 空间

---
#### 17.3.39 例 39：自动驾驶跟车最小间距（自定义）⭐⭐
> **知识点**：二分刹车距离、单调判定｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：车以初速 v 行驶刹车加速度 a，需在 D 距离内停稳，求满足的最短刹车距离（给定 D 求 a 的可行性，简化为二分 a 求最小可行加速度）。

**思路**：二分加速度 a，验证 v²/(2a)≤D。

💡 类比"调刹车力度"：刹车越猛距离越短，二分找出够用最小力度：

```python
v, D = map(int, input().split())
def ok(a):
    return v * v / (2 * a) <= D + 1e-9
lo, hi = 0.000001, 1e6
for _ in range(60):
    mid = (lo + hi) / 2
    if ok(mid):
        hi = mid
    else:
        lo = mid
print("%.6f" % hi)
```
> **复杂度**：O(log precision) 时间，O(1) 空间

---
#### 17.3.40 例 40：装货最少趟次（自定义）⭐⭐
> **知识点**：二分车载、趟次检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：卸货站需搬运 n 件物品，一辆车每趟能装 w 重，每天能运 k 趟，问每天最少车载多大能当天运完（简化二分每月趟次）。

**思路**：二分车载，验证总趟次≤k。

💡 类比"卡车备货量"：载重越大趟次越少，找刚好够的最小车载：

```python
n, k = map(int, input().split())
w = list(map(int, input().split()))
def ok(cap):
    trips = 1
    cur = 0
    for x in w:
        if cur + x > cap:
            trips += 1
            cur = x
        else:
            cur += x
    return trips <= k
lo, hi = max(w), sum(w)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log sum) 时间，O(1) 空间
#### 17.3.41 例 41：最大化最小每人面积（自定义）⭐⭐
> **知识点**：二分面积、分配检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 块地面积 a_i，需分给 m 户人家每户一整块（可剩），求每户能分到的最小最大面积（最大化最小值）。

**思路**：二分每户面积 x，统计面积 ≥x 的块数是否≥m。

💡 类比"分地按整块"：规定每户至少多大，数够不够 m 块大田：

```python
n, m = map(int, input().split())
a = list(map(int, input().split()))
def ok(x):
    return sum(1 for v in a if v >= x) >= m
lo, hi = 1, max(a)
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(n log range) 时间，O(1) 空间

---
#### 17.3.42 例 42：最少带宽分配（自定义）⭐⭐
> **知识点**：二分带宽、上限判定｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个视频各自带宽需求 b_i，租用总带宽 B 需覆盖全部且每月成本与 B 正比，求最小可行月租带宽=峰值需求最大值。

**思路**：答案即 max(b_i)。

💡 类比"按峰值买带宽"：总带宽必须不小于任何单路需求，取最大：

```python
n = int(input())
b = list(map(int, input().split()))
print(max(b))
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.3.43 例 43：三分求最短路径点高度（自定义）⭐⭐
> **知识点**：三分、几何最短｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从地面上一点到另一点，途中可先走斜上坡（角度任意）再下坡，求某转折高度使总距离最短（演示单谷）。

**思路**：对转折高度三分求距离函数最小值。

💡 类比"翻山选隘口"：高度太低绕路远，太高爬坡远，取中间谷底：

```python
import math
def dist_of(h):
    # 演示：高度 h 下的总距离（凸函数）
    return math.sqrt(h*h + 4) + math.sqrt((10-h)**2 + 4)
lo, hi = 0.0, 10.0
for _ in range(60):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    if dist_of(m1) < dist_of(m2):
        hi = m2
    else:
        lo = m1
print("%.6f" % dist_of((lo + hi) / 2))
```
> **复杂度**：O(log precision) 时间，O(1) 空间

---
#### 17.3.44 例 44：最少删除使差值≤k（自定义）⭐⭐
> **知识点**：排序+二分、两端裁剪｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个数，允许删去任意个（保留顺序无关），使剩下的数两两差≤k，求最少删几个。

**思路**：排序后找满足差值≤k 的最长滑窗，最小删除=n-最长。

💡 类比"一排减到跨度合适"：排序后看最长的差值≤k 的连续子段：

```python
n, k = map(int, input().split())
a = sorted(map(int, input().split()))
r = 0
best = 0
for l in range(n):
    while r < n and a[r] - a[l] <= k:
        r += 1
    best = max(best, r - l)
print(n - best)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.3.45 例 45：二分求最小值得分组（自定义）⭐⭐
> **知识点**：二分答案、分组可行性｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个连续任务耗时 a_i，派 k 个工人并行（每人连续段）完成，求完成全工程的最短时间（=最小化单人工人最大耗时）。

**思路**：二分单人工时上限 x，验证可分≤k 段。

💡 类比"人手分段同时干"：每人限时 x，数要几人才能同时干完：

```python
n, k = map(int, input().split())
a = list(map(int, input().split()))
def ok(x):
    seg = 1
    cur = 0
    for v in a:
        if cur + v > x:
            seg += 1
            cur = v
        else:
            cur += v
    return seg <= k
lo, hi = max(a), sum(a)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log sum) 时间，O(1) 空间

---
#### 17.3.46 例 46：三分类点对小（自定义）⭐⭐
> **知识点**：排序、双指针最接近对和｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给两组数 A、B，分别在 A、B 中各取一个，使两数和最接近目标 target，求最接近的和。

**思路**：A 排序后对 B 每个元素二分或双指针找最接近 target-a。

💡 类比"配鞋码"：固定一只鞋找最适合的另一只：

```python
na = int(input())
A = sorted(map(int, input().split()))
nb = int(input())
B = list(map(int, input().split()))
target = int(input())
import bisect
ans = None
for b in B:
    need = target - b
    i = bisect.bisect_left(A, need)
    for idx in (i-1, i):
        if 0 <= idx < na:
            s = A[idx] + b
            if ans is None or abs(s-target) < abs(ans-target):
                ans = s
print(ans)
```
> **复杂度**：O((na+nb) log na) 时间，O(1) 空间

---
#### 17.3.47 例 47：最长连续上升最长可用段（自定义）⭐⭐
> **知识点**：二分边界、滑动窗口|最长子数组|要求差值∈[l,r]｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求数组中最长连续子数组，满足子数组内 max-min 在某范围内（此处演示单参数版本：元素互异判定枚举过长用双指针 max-min≤k）。

**思路**：滑动窗口维护当前窗口 max 与 min，超标则左移。

💡 类比"窗口平滑检查"：窗口宽度可调，超差就收左边：

```python
n, k = map(int, input().split())
a = list(map(int, input().split()))
from collections import deque
mx = deque(); mn = deque()
l = 0
best = 0
for r in range(n):
    while mx and a[mx[-1]] <= a[r]:
        mx.pop()
    mx.append(r)
    while mn and a[mn[-1]] >= a[r]:
        mn.pop()
    mn.append(r)
    while a[mx[0]] - a[mn[0]] > k:
        l += 1
        while mx and mx[0] < l:
            mx.popleft()
        while mn and mn[0] < l:
            mn.popleft()
    best = max(best, r - l + 1)
print(best)
```
> **复杂度**：O(n) 时间，O(n) 空间

---
#### 17.3.48 例 48：最少中间站（自定义）⭐⭐
> **知识点**：二分续航、站数检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：电动车续航 R 公里，相邻充电站间距已知，求若中途只能充 k 次，最大续航 R 至少多大（最小化最大段）。

**思路**：答案为相邻站点间最大间距。

💡 类比"按最长一段定续航"：最远两个站之间的里程决定了最小续航：

```python
n, k = map(int, input().split())
p = sorted(map(int, input().split()))
print(max(p[i+1] - p[i] for i in range(n-1)))
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.3.49 例 49：二分求可装块数判断（自定义）⭐⭐
> **知识点**：二分块长、装块验证｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：一截长绳要剪成 m 段每段长度相同（可为任意浮点），求最大长度（经典 POJ 1064 浮点版）。

**思路**：浮点二分长度 x，验证 sum(len//x)≥m。

💡 类比"浮点剪绳"：浮点二分控制精度：

```python
n, m = map(int, input().split())
L = [float(input()) for _ in range(n)]
def ok(x):
    return sum(int(v // x) for v in L) >= m
lo, hi = 0.0, max(L)
for _ in range(60):
    mid = (lo + hi) / 2
    if ok(mid):
        lo = mid
    else:
        hi = mid
print("%.6f" % lo)
```
> **复杂度**：O(n log precision) 时间，O(1) 空间

---
#### 17.3.50 例 50：最少清空货物趟次（自定义）⭐⭐
> **知识点**：二分车载、趟次判定｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：仓库有 n 堆货堆量 a_i（可拆），一辆车一趟最大载 capacity，需要清空仓库，问最少趟数（总重/车载向上取整）。

**思路**：既然可拆，答案=ceil(总重/车载)；如需整堆则不可拆，演示整数除。

💡 类比"一趟运多少"：全部重量除以每趟容量向上取整即为趟数：

```python
n, cap = map(int, input().split())
a = list(map(int, input().split()))
total = sum(a)
print((total + cap - 1) // cap)
```
> **复杂度**：O(n) 时间，O(1) 空间
#### 17.3.51 例 51：二分最小考场数（自定义）⭐⭐
> **知识点**：二分容量、分场检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 名学生代号 s_i（升序可排），要求任意相邻两个考场内的学生代号差≤k，问最少分成几个考场（组内两两差≤k）。

**思路**：排序，二分单场容纳跨度 k 下求最少组等价，贪心统计最少组数。

💡 类比"按分数分考场"：排好序后贪心把差量在 k 内同场：

```python
n, k = map(int, input().split())
a = sorted(map(int, input().split()))
res = 1
start = a[0]
for x in a[1:]:
    if x - start > k:
        res += 1
        start = x
print(res)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.3.52 例 52：运费随载重段优惠（自定义）⭐⭐
> **知识点**：分段函数、二分单价拐点｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：托运费用分两档：≤w kg 单价 a，>w kg 部分单价 b（b<a 优惠），求某重量 x 的运费，多次查询。

**思路**：直接按分段计费模拟输出。

💡 类比"阶梯水价"：先按平价算前 w，超部分按优惠价算：

```python
w, a, b = map(int, input().split())
q = list(map(int, input().split()))
for x in q:
    if x <= w:
        print(a * x)
    else:
        print(a * w + b * (x - w))
```
> **复杂度**：O(q) 时间，O(1) 空间

---
#### 17.3.53 例 53：最大化最小空调冷度（自定义）⭐⭐
> **知识点**：二分答案、覆盖检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个房间温度，用 k 台制冷能力可调空调覆盖，希望所有被覆盖房间温度降到低于 T，求覆盖所有房间需要的最小制冷能力（最大化最小降温）。

**思路**：模拟简化——二分能力 x，检查每台空调可覆盖到目标低温的房间数之和≥总房间。

💡 类比"调冷功率够不够"：猜每台功率，看能否把所有房间吹到指定低温：

```python
n, k, T = map(int, input().split())
temp = list(map(int, input().split()))
def ok(x):
    cover = 0
    for t in temp:
        if t - x <= T:
            cover += 1
    return cover >= n
lo, hi = 0, max(temp) - T
if hi <= 0:
    print(0)
else:
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    print(lo)
```
> **复杂度**：O(n log range) 时间，O(1) 空间

---
#### 17.3.54 例 54：最小书架层高（自定义）⭐⭐
> **知识点**：二分每层容量、层数检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 本书宽 w_i，每层能放长度 chunks 将书按序放入，共可以 k 层，求每层最短长度（最小化最长层）。

**思路**：二分每层长度 x，验证可分≤k 层。

💡 类比"压缩书架层数"：每层限长 x，数要几层摆完：

```python
n, k = map(int, input().split())
w = list(map(int, input().split()))
def ok(x):
    layers = 1
    cur = 0
    for v in w:
        if cur + v > x:
            layers += 1
            cur = v
        else:
            cur += v
    return layers <= k
lo, hi = max(w), sum(w)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log sum) 时间，O(1) 空间

---
#### 17.3.55 例 55：存储最低电压（自定义）⭐⭐
> **知识点**：二分电量、放电检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：手机电量从满开始每分钟耗 a%，且后台任务瞬扣b。需支撑 t 分钟，求购买的最小初始电量（缓充演示为需要初始电量即 t×a + b）。

**思路**：答案= t×a + b。

💡 类比"算最少进场电量"：每分钟耗+一次性后台耗即所需初始电量：

```python
t, a, b = map(int, input().split())
print(t * a + b)
```
> **复杂度**：O(1) 时间，O(1) 空间

---
#### 17.3.56 例 56：最大化最小游泳间距（自定义）⭐⭐
> **知识点**：坐标离散、二分答案｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：河岸 n 个救生圈坐标，运动员要踩 m 个圈前进，希望相邻踩中圈间距最大（最大化最小间距）。

**思路**：二分间距 d，贪心验证。

💡 类比"跳荷叶最远间距"：规定两圈至少 d 远，数能跳几步：

```python
n, m = map(int, input().split())
p = sorted(map(int, input().split()))
def ok(d):
    cnt, last = 1, p[0]
    for x in p[1:]:
        if x - last >= d:
            cnt += 1
            last = x
    return cnt >= m
lo, hi = 1, p[-1] - p[0]
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(n log range) 时间，O(1) 空间

---
#### 17.3.57 例 57：最短施工连续日数（自定义）⭐⭐
> **知识点**：二分工期、进度检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：工程总工作量 W，每天能做 p 工作量，且每个工作日还能加班补 g（一次性），求最少天数。

**思路**：二分天数，天数×p + g 是否≥W。

💡 类比"算工期含加班"：每天常规+一次性加班补足总量：

```python
W, p, g = map(int, input().split())
lo, hi = 1, W
while lo < hi:
    mid = (lo + hi) // 2
    if mid * p + g >= W:
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(log W) 时间，O(1) 空间

---
#### 17.3.58 例 58：均匀分库存最小峰（自定义）⭐⭐
> **知识点**：二分答案、转运检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个仓库库存 a_i，可通过货车把任意库存匀给相邻，希望每仓库存差异尽量小即最大-最小最小，求最小可能的最大库存（所有人≥某值演示：能否让每仓≥x）。

**思路**：二分每仓目标 x，检查总库存≥n×x。

💡 类比"定保底库存"：只要总量够 n 个仓库都到 x 就行：

```python
n = int(input())
a = list(map(int, input().split()))
total = sum(a)
def ok(x):
    return total >= n * x
lo, hi = 0, total
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(n + log total) 时间，O(1) 空间

---
#### 17.3.59 例 59：最少树枝搭桥（自定义）⭐⭐
> **知识点**：二分桥宽、拼接检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 根树枝长 l_i，要凑出至少总长 L 的桥（可拼接），求最少用几根。

**思路**：长度降序取直至总长≥L。

💡 类比"取最长棍搭桥"：先拿最长的几根最快凑够长度：

```python
n, L = map(int, input().split())
l = sorted(map(int, input().split()), reverse=True)
s = 0
cnt = 0
for x in l:
    s += x
    cnt += 1
    if s >= L:
        print(cnt)
        break
else:
    print(-1)
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.3.60 例 60：最小总溢水量调度（自定义）⭐⭐
> **知识点**：二分均值、溢出判断｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个蓄水池容量 c_i 与当前水位 a_i，现补水总量 X，目标是水位尽量平均且不溢出，求补水后可能达到的最大统一水位（受容量限制）。

**思路**：二分水位 h，检查 sum(max(0, h-a_i)) ≤ X 且 h 不超过容量。

💡 类比"统一灌到 h 水位"：算每个池差多少才到 h，够不够灌：

```python
n, X = map(int, input().split())
a = list(map(int, input().split()))
c = list(map(int, input().split()))
def ok(h):
    need = 0
    for ai, ci in zip(a, c):
        if h > ci:
            return False
        need += max(0, h - ai)
    return need <= X
lo, hi = 0.0, max(c)
for _ in range(60):
    mid = (lo + hi) / 2
    if ok(mid):
        lo = mid
    else:
        hi = mid
print("%.6f" % lo)
```
> **复杂度**：O(n log precision) 时间，O(1) 空间
#### 17.3.61 例 61：最少潜水艇深潜设备（自定义）⭐⭐
> **知识点**：二分容量、装备检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 根备用氧气瓶装量 b_i，需分配给 m 个潜水计划（每个需要氧量 req），一个瓶只能给一个人用，问每人能否分到最大等量（最大化最小单人供氧）。

**思路**：二分单人供氧 x，统计 b_i≥x 的瓶数是否≥m。

💡 类比"按罐供氧"：每罐至少给 x，数够不够 m 个计划：

```python
n, m = map(int, input().split())
b = list(map(int, input().split()))
def ok(x):
    return sum(1 for v in b if v >= x) >= m
lo, hi = 1, max(b)
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(n log range) 时间，O(1) 空间

---
#### 17.3.62 例 62：最大化最小每字段分数（自定义）⭐⭐
> **知识点**：二分答案、段和检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个分数 a_i，分成 m 个连续段，希望任意段和都≥x（使最小段和最大），求最大可行 x。

**思路**：二分 x，贪心尽量多分到≥x 段可分出段数≥m。

💡 类比"保底线分段"：每段总和要够 x，看能否切出 m 段：

```python
n, m = map(int, input().split())
a = list(map(int, input().split()))
def ok(x):
    cnt = 0
    s = 0
    for v in a:
        s += v
        if s >= x:
            cnt += 1
            s = 0
    return cnt >= m
lo, hi = 1, sum(a)
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(n log sum) 时间，O(1) 空间

---
#### 17.3.63 例 63：三分求最短总爬升（自定义）⭐⭐
> **知识点**：三分、行程函数单谷｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从A到B可以选择不同中转高度 h，行程总油耗是先降后升的单谷函数，求最小油耗。

**思路**：对 h 三分求最小值。

💡 类比"滑翔找最省高度"：油耗随高度先降后升，三分夹谷：

```python
def fuel(h):
    # 演示单谷总油耗函数
    return (h - 5) ** 2 + abs(h - 3) + 10
lo, hi = 0.0, 10.0
for _ in range(60):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    if fuel(m1) < fuel(m2):
        hi = m2
    else:
        lo = m1
print("%.6f" % fuel((lo + hi) / 2))
```
> **复杂度**：O(log precision) 时间，O(1) 空间

---
#### 17.3.64 例 64：二分找缺失数（自定义）⭐⭐
> **知识点**：索引二分、缺失检测｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：0..n 中缺一个数，给定已排序的 0..n-1 排列（缺一个），找出缺失的那个。

**思路**：二分，若 a[mid]==mid 则缺失在右边否则在左边。

💡 类比"点名缺号"：哪个位置和值对不上，缺的数就在左半边：

```python
n = int(input())
a = list(map(int, input().split()))
lo, hi = 0, n
while lo < hi:
    mid = (lo + hi) // 2
    if a[mid] == mid:
        lo = mid + 1
    else:
        hi = mid
print(lo)
```
> **复杂度**：O(log n) 时间，O(1) 空间

---
#### 17.3.65 例 65：最少收费拦杆（自定义）⭐⭐
> **知识点**：二分间距、放置检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：公路相邻收费站间距已定，想新增 k 个收费站使任意相邻站间距都不超过 D，求满足时允许的最大间距 min 的可行化的最小新增数（简化为二分间距求最少新增）。

**思路**：二分间距 d，路口由原站+新增互补，求新增数。

💡 类比"加站密网"：每段间距除以 d 减 1 就是在该段补的站：

```python
n, D, k = map(int, input().split())
p = sorted(map(int, input().split()))
def extra_for(d):
    add = 0
    for i in range(n-1):
        gap = p[i+1] - p[i]
        add += (gap - 1) // d
    return add
lo, hi = 1, max(p[i+1]-p[i] for i in range(n-1))
if n < 2:
    print(0)
else:
    while lo < hi:
        mid = (lo + hi) // 2
        if extra_for(mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    print(lo)
```
> **复杂度**：O(n log range) 时间，O(1) 空间

---
#### 17.3.66 例 66：端口感应距离最小（自定义）⭐⭐
> **知识点**：二分感应半径、判覆盖｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个传感器位置，需使所有相邻传感器间都能通信（感应半径需≥相邻间距），求可能的最小感应半径=最大相邻间距。

**思路**：答案即相邻坐标差最大值。

💡 类比"按紧挨间距定信号"：最远相邻两传感器间距决定了最小信号半径：

```python
n = int(input())
p = sorted(map(int, input().split()))
print(max(p[i+1]-p[i] for i in range(n-1)))
```
> **复杂度**：O(n log n) 时间，O(1) 空间

---
#### 17.3.67 例 67：最少装箱趟次（自定义）⭐⭐
> **知识点**：二分车载、趟数判定｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 件行李重 w_i 不可拆分，一趟运最多 cap，但要全部运完（按任意顺序），求最少趟数（用贪心装入则转为箱装问题；此演示用趟=总重/cap 上限近似并给可拆整数答案）。

**思路**：能拆时答案为 ceil(总重/cap)。

💡 类比"整车发运"：总量除每车承载向上取整：

```python
n, cap = map(int, input().split())
w = list(map(int, input().split()))
print((sum(w) + cap - 1) // cap)
```
> **复杂度**：O(n) 时间，O(1) 空间

---
#### 17.3.68 例 68：浇花最少水车浇次（自定义）⭐⭐
> **知识点**：二分水车容量、浇次检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 棵树的需水量 a_i 依次浇，一辆水车最多装 x 升，装满一次算一趟，求最小水车容量使总趟数≤k。

**思路**：二分容量 x，贪心分段验证趟数≤k。

💡 类比"加水车趟数"：限制每趟水量，看几趟能浇完：

```python
n, k = map(int, input().split())
a = list(map(int, input().split()))
def ok(x):
    tri = 1
    cur = 0
    for v in a:
        if cur + v > x:
            tri += 1
            cur = v
        else:
            cur += v
    return tri <= k
lo, hi = max(a), sum(a)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log sum) 时间，O(1) 空间

---
#### 17.3.69 例 69：最大化最小等待接受率（自定义）⭐⭐
> **知识点**：二分 rate、统计检查｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个工单 SLA 时长 a_i，希望经过处理后每个工单等待时长都≤t，且只能接受其中 k 个尽快处理，问能保证的最长可满足 t（最大化最小余量）。

**思路**：简化为二分可接受等待 w，统计 a_i≤w 的个数≥k。

💡 类比"划红线验收"：限时 w，够不够 k 个工单达线：

```python
n, k = map(int, input().split())
a = list(map(int, input().split()))
def ok(w):
    return sum(1 for v in a if v <= w) >= k
lo, hi = 1, max(a)
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```
> **复杂度**：O(n log range) 时间，O(1) 空间

---
#### 17.3.70 例 70：运输串行总长最小段（综合二分）⭐⭐⭐
> **知识点**：二分答案、串行容量验证｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 段材料长度 l_i 要分成 k 条流水线（顺序段）运输，使最长流水线总长最小。

**思路**：二分单线长度 x，贪心分段验证≤k。

💡 类比"均衡分线"：限制单线长度，看够不够分 k 条：

```python
n, k = map(int, input().split())
l = list(map(int, input().split()))
def ok(x):
    line = 1
    cur = 0
    for v in l:
        if cur + v > x:
            line += 1
            cur = v
        else:
            cur += v
    return line <= k
lo, hi = max(l), sum(l)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
```
> **复杂度**：O(n log sum) 时间，O(1) 空间
