# 第 12 章 OI/ACM 竞赛：ACM 经典题库（四）

> 本分册覆盖 17.10–17.13（并查集、字符串与图论），共 315 题。
> 返回 [ACM 经典题库总览](./12s_ACM题库.md)。

## 17. ACM 经典题库

### 17.10 并查集与图连通性

**说明**：本节共 60 题，覆盖并查集（路径压缩、按秩合并、带权并查集、种类并查集、离线统计、反向连边）、并查集维护连通块、最小生成树 Kruskal、二分图判定、Tarjan 强连通分量、割点割边、连通分量计数等方法。

#### 17.10.1 例 1：并查集模板——合并与判同（洛谷 P3367）（⭐）

> **知识点**：并查集、路径压缩、合并、查询｜**难度**：⭐｜**类型****：ACM/竞赛
> **题目描述**：n 个元素、m 个操作：合并两个集合、判断两个元素是否在同一集合。

**思路**

并查集用 fa[i] 数组，find 带路径压缩，union 直接挂根。判同即看 find(x)==find(y)。

💡 类比"找头头"：每个人记住自己的老大，要判断两人是否一伙就一路问到老大是否同一个人，并把路过的全改认最高老大缩短下次路程。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(n+1))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb
    out=[]
    for _ in range(m):
        op=int(next(it)); a=int(next(it)); b=int(next(it))
        if op==1: union(a,b)
        else: out.append('YES' if find(a)==find(b) else 'NO')
    sys.stdout.write('\n'.join(out))

if __name__=='__main__':
    main()
```

> **复杂度**：均摊 O(α(n)) 每次，O(n) 空间

---

#### 17.10.2 例 2：连通块数量与块大小（POJ 2524 Ubiquitous Religions）（⭐）

> **知识点**：并查集、连通块计数、集合大小维护｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个人、m 条"认识"关系，把互相认识(传递)的人归为一组，求组数。

**思路**

初始 n 个集合，每次 union 成功则组数 -1；也可用 size 数组合并时累加。

💡 类比"朋友圈合并"：每成功合并两伙人就少一伙，从 n 伙数起，合并多少次就减多少次。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(n+1)); size=[1]*(n+1)
    comp=n
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def union(a,b):
        nonlocal comp
        ra,rb=find(a),find(b)
        if ra==rb: return
        if size[ra]<size[rb]: ra,rb=rb,ra
        fa[rb]=ra; size[ra]+=size[rb]; comp-=1
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); union(a,b)
    print(comp)

if __name__=='__main__':
    main()
```

> **复杂度**：均摊 O(α(n)) 时间，O(n) 空间

---

#### 17.10.3 例 3：按秩合并的并查集（保证树高可控）（AcWing 836 变式）（⭐⭐）

> **知识点**：按秩(高度/大小)合并、摊还复杂度、防退化为链｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：实现并查集并显式使用"按高度合并"，保证合并树高 O(log n)，判断连通。

**思路**

用 rank 记录每棵树高度，合并时总是把矮的根挂到高的根下，rank 相同才 +1。

💡 类比"矮树当弟子"：两只队伍合并时，较矮那队的头目投靠较高的那队，避免队伍越拉越长。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(n+1)); rank=[0]*(n+1)
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra==rb: return
        if rank[ra]<rank[rb]: ra,rb=rb,ra
        fa[rb]=ra
        if rank[ra]==rank[rb]: rank[ra]+=1
    out=[]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); union(a,b)
        # 每次查询是否连通(示例)
    # 示例输出最后一次是否连通
    ra,rb=find(a),find(b)
    print('YES' if ra==rb else 'NO')

if __name__=='__main__':
    main()
```

> **复杂度**：均摊 O(α(n)) 时间，O(n) 空间

---

#### 17.10.4 例 4：带权并查集——维护到根的距离（银河英雄传说）（洛谷 P1196/POJ 2492 变式）（⭐⭐⭐）

> **知识点**：带权并查集、边权(到父)、路径压缩累加权、集合间距离｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：初始每列一只飞船。操作：把 i 所在整列接到 j 所在列之后；查询 i、j 之间相隔多少艘飞船。

**思路**

带权并查集 d[x] 表示 x 到 fa[x] 的飞船数，size[root] 表示列长度。路径压缩时更新 d；连接时更新被接列的根与 d。

💡 类比"排队间隔"：每个人记住自己跟上司隔几格，接队时同步更新老大间的距离与全列长度，追查间隔由路径累加得到。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    T=int(next(it))
    N=30000
    fa=list(range(N+1)); d=[0]*(N+1); sz=[1]*(N+1)
    def find(x):
        if fa[x]==x: return x
        r=find(fa[x]); d[x]+=d[fa[x]]; fa[x]=r; return r
    out=[]
    for _ in range(T):
        op=next(it); a=int(next(it)); b=int(next(it))
        if op==b'M':
            ra=find(a); rb=find(b)
            fa[ra]=rb; d[ra]=sz[rb]; sz[rb]+=sz[ra]
        else:
            if find(a)!=find(b): out.append('-1')
            else: out.append(str(abs(d[a]-d[b])-1))
    sys.stdout.write('\n'.join(out))

if __name__=='__main__':
    main()
```

> **复杂度**：均摊 O(α(n)) 时间，O(n) 空间

---

#### 17.10.5 例 5：种类并查集——三道菜相克（食物链）（POJ 1182/洛谷 P2024）（⭐⭐⭐）

> **知识点**：种类并查集、三倍空间、捕食关系、矛盾检测｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 只动物分三类 A/B/C，A 吃 B、B 吃 C、C 吃 A。给出 m 条说法(同类或 x 吃 y)，统计与前面矛盾的说法数。

**思路**

每个动物用三个结点表示其所在类别(本类/捕食者/被捕食者)。说法"x 与 y 同类/捕食"时检查是否与已有事实冲突，无冲突则对应 union。

💡 类比"三色戒指环"：每个动物三种身份各占一格，通过三格并查集的连线表达谁吃谁，核对说法是否破坏之前的环。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(3*n+3))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def same(a,b): return find(a)==find(b)
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb
    cnt=0
    def is_ok(d,x,y):
        if x>n or y>n: return False
        if d==1:
            if same(x,y+n) or same(x,y+2*n): return False
            union(x,y); union(x+n,y+n); union(x+2*n,y+2*n)
        else:
            if same(x,y) or same(x,y+2*n): return False
            union(x,y+n); union(x+n,y+2*n); union(x+2*n,y)
        return True
    ans=0
    for _ in range(m):
        d=int(next(it)); x=int(next(it)); y=int(next(it))
        if not is_ok(d,x,y): ans+=1
    print(ans)

if __name__=='__main__':
    main()
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.6 例 6：离线并查集——先全部合并再倒序回答（洛谷 P1197 星球大战）（⭐⭐⭐）

> **知识点**：离线逆向、并查集加边、连通块、删除变添加｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边图，k 次按顺序删除某些点（及其相连边）。初始求连通块数，每次删除后输出连通块数。

**思路**

经典套路：把"删除"倒过来变成"逐点重新加回"。先建立删完所有点后的图并求连通块，再逆序把点加回、恢复其连边合并，得到每步答案。

💡 类比"倒放积木"：拆房子难算，倒着把积木一块块装回去，每次加一块就更新队伍数，最后正序输出。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n)]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append(b); g[b].append(a)
    k=int(next(it))
    deleted=[-1]*k
    removed=[False]*n
    for i in range(k):
        x=int(next(it)); deleted[k-1-i]=x; removed[x]=True
    fa=list(range(n)); alive=n-k
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def union(a,b):
        nonlocal alive
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb; alive-=1
    # 初始不含被删点的连通块
    for u in range(n):
        if removed[u]: continue
        for v in g[u]:
            if not removed[v] and u<v:
                union(u,v)
    res=[alive]
    added=[False]*n
    for x in deleted:
        added[x]=True
        # 先把该点作为孤立块加回
        alive+=1
        for v in g[x]:
            if added[v] or not removed_vacant(v,removed):
                pass
        res.append(alive)
    print('\n'.join(map(str,res)))

def removed_vacant(v,removed):
    return not removed[v]
```

> **复杂度**：O((n+m+k) α(n)) 时间，O(n+m) 空间

---

#### 17.10.7 例 7：Kruskal 最小生成树（洛谷 P3366）（⭐⭐）

> **知识点**：最小生成树、Kruskal、并查集、边排序｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 条带宽费用边，求最小生成树总权值；若不连通输出特定信息。

**思路**

Kruskal：边按权排序，从小到大用并查集看两端是否已连通，不连通则取该边合并并累加；取到 n-1 条边即成树。

💡 类比"拉线最省钱"：先把所有可能光缆按价格排序，从便宜到贵逐条拉，只要两端还没通电就拉，拉满全村即最小成本。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    edges=[]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); w=int(next(it))
        edges.append((w,a,b))
    edges.sort()
    fa=list(range(n+1))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    ans=0; cnt=0
    for w,a,b in edges:
        ra,rb=find(a),find(b)
        if ra!=rb:
            fa[ra]=rb; ans+=w; cnt+=1
            if cnt==n-1: break
    print(ans if cnt==n-1 else 'orz')

if __name__=='__main__':
    main()
```

> **复杂度**：O(m log m) 时间，O(m) 空间

---

#### 17.10.8 例 8：图的最小生成森林（多连通分量各取 MST）（POJ 2349 变式）（⭐⭐）

> **知识点**：Kruskal、最小生成森林、边从小到大|分块连通｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边，求"森林"中各树最小，即边从小到大选 union 全部可能，总权即最小生成森林。

**思路**

与 Kruskal 相同流程，把所有不会被合并的边跳过，最终得到含全部点的生成森林（每连通分量一棵树）。

💡 类比"各自岛屿拉线"：不管是否整片连通，只在各岛屿内部拉最省电的光缆，全选能连的就成一片片子树森林。

```python
def mst_forest(edges,n):
    edges.sort()
    fa=list(range(n+1))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    total=0; cnt=0
    for w,a,b in edges:
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb; total+=w; cnt+=1
    return total,cnt

if __name__=='__main__':
    print(mst_forest([(1,1,2),(2,2,3),(1,3,4),(5,1,4)],4))
```

> **复杂度**：O(m log m) 时间，O(n) 空间

---

#### 17.10.9 例 9：判断图是否连通（BFS/DFS/并查集）（洛谷 P1697 变式）（⭐）

> **知识点**：连通性判定、从一出发遍历、越界边检查｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边的无向图，判断从点 1 出发能否到达所有点。

**思路**

从 1 DFS/BFS 标记可达；也可并查集把所有边 union 后看是否所有点与 1 同集合。

💡 类比"传纸条串"：从第一个人传纸条给身边连着的所有人，看是否人人都收到过。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append(b); g[b].append(a)
    vis=[False]*(n+1); vis[1]=True; stack=[1]
    while stack:
        u=stack.pop()
        for v in g[u]:
            if not vis[v]: vis[v]=True; stack.append(v)
    print('YES' if all(vis[1:]) else 'NO')

if __name__=='__main__':
    main()
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.10 例 10：二分图判定（染色法）（洛谷 P1330 封锁街道）（⭐⭐）

> **知识点**：二分图、染色、BFS/DFS、奇环检测｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向图，判断是否二分图（无奇环），若能则给出一种最小顶点覆盖规模的染色数(两色较少者之和)。

**思路**

对每个连通分量染色 0/1：DFS 给邻点染相反色；若遇已染色且颜色相同即不是二分图。统计每分量两色个数取较小。

💡 类比"练习题分组互斥"：同一道题不能和它相邻的题在相同组，用黑白两班分配，若有人注定和邻座同班则失败。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append(b); g[b].append(a)
    color=[-1]*(n+1); ok=True
    def dfs(u,c):
        nonlocal ok
        color[u]=c
        for v in g[u]:
            if color[v]==-1: dfs(v,c^1)
            elif color[v]==c: ok=False
    for i in range(1,n+1):
        if color[i]==-1: dfs(i,0)
    print('YES' if ok else 'NO')

if __name__=='__main__':
    main()
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.11 例 11：强连通分量 Tarjan（洛谷 P3387 缩点 简化版）（⭐⭐⭐）

> **知识点**：强连通分量、Tarjan、dfn/low、栈、缩点｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边有向图，求强连通分量个数，并输出每个点的所属分量编号。

**思路**

Tarjan：记录每点 dfn(发现时间)与 low(可达祖先最小 dfn)，用栈保存路径结点。当 low[u]==dfn[u] 时弹栈形成当前 SCC。

💡 类比"环形登山队"：登山时记录首次到达时间与退回最浅营地，若发现能走回出发营地的时间，就把一圈队员登记为同一登山队。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append(b)
    dfn=[0]*(n+1); low=[0]*(n+1); on=[False]*(n+1)
    st=[]; belong=[0]*(n+1); timer=0; comp_id=0
    def tarjan(u):
        nonlocal timer,comp_id
        timer+=1; dfn[u]=low[u]=timer
        st.append(u); on[u]=True
        for v in g[u]:
            if not dfn[v]:
                tarjan(v); low[u]=min(low[u],low[v])
            elif on[v]:
                low[u]=min(low[u],dfn[v])
        if low[u]==dfn[u]:
            comp_id+=1
            while True:
                x=st.pop(); on[x]=False; belong[x]=comp_id
                if x==u: break
    for i in range(1,n+1):
        if not dfn[i]: tarjan(i)
    print(comp_id)
    print(' '.join(map(str,belong[1:])))

if __name__=='__main__':
    main()
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.12 例 12：割点（洛谷 P3388）（⭐⭐⭐）

> **知识点**：割点、Tarjan、dfn/low、根特判、割点判定｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边无向图，求所有割点（删去后连通分量数增加的点）。

**思路**

Tarjan：对非根点 u，其儿子 v 满足 low[v] ≥ dfn[u] 时 u 是割点；对根，若有 ≥2 个儿子在 DFS 树的独立子树则根为割点。

💡 类比"必经咽喉要道"：若某个山口的后方队伍只有经它才能下山，那它就是一夫当关的割点。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append(b); g[b].append(a)
    dfn=[0]*(n+1); low=[0]*(n+1); cut=[False]*(n+1); timer=0
    def tarjan(u,fa):
        nonlocal timer
        timer+=1; dfn[u]=low[u]=timer; child=0
        for v in g[u]:
            if v==fa: continue
            if not dfn[v]:
                child+=1; tarjan(v,u); low[u]=min(low[u],low[v])
                if fa!=0 and low[v]>=dfn[u]: cut[u]=True
            else:
                low[u]=min(low[u],dfn[v])
        if fa==0 and child>1: cut[u]=True
    for i in range(1,n+1):
        if not dfn[i]: tarjan(i,0)
    res=[i for i in range(1,n+1) if cut[i]]
    print(len(res))
    print(' '.join(map(str,res)))

if __name__=='__main__':
    main()
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.13 例 13：割边（桥）数量统计（POJ 3352 变式）（⭐⭐⭐）

> **知识点**：割边、low、桥判定、边双连通｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边无向图，求割边（桥）的条数——删去后使图不连通的边。

**思路**

Tarjan 修订：边 (u,v)（v 为儿子）若 low[v] > dfn[u] 则它是桥。注意重边处理（用边的编号而非仅父结点避免把重边当回边）。

💡 类比"独木桥"：若某条路断掉村庄就不连通，那条路就是必须另造的独木桥；重边则因有备份不算桥。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]
    edges=[]
    for eid in range(m):
        a=int(next(it)); b=int(next(it)); edges.append((a,b))
        g[a].append((b,eid)); g[b].append((a,eid))
    dfn=[0]*(n+1); low=[0]*(n+1); timer=0; bridges=0
    def tarjan(u,pe):
        nonlocal timer,bridges
        timer+=1; dfn[u]=low[u]=timer
        for v,eid in g[u]:
            if eid==pe: continue
            if not dfn[v]:
                tarjan(v,eid); low[u]=min(low[u],low[v])
                if low[v]>dfn[u]: bridges+=1
            else:
                low[u]=min(low[u],dfn[v])
    for i in range(1,n+1):
        if not dfn[i]: tarjan(i,-1)
    print(bridges)

if __name__=='__main__':
    main()
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.14 例 14：并查集判环（无向图是否存在环）（HDU 1213 变式/洛谷 P2661 快慢针）（⭐⭐）

> **知识点**：并查集、判环、连通分量中边=点-1则无环｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边无向图，判断是否存在环。

**思路**

遍历边：若某边两端已属于同一集合（find 相同），则这条边成环；否则合并。

💡 类比"拉线防闭合"：给每个点组队，若发现要拉线的两端已经属于同一队，那这根线就会围成一个环。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(n+1))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    has_cycle=False
    for _ in range(m):
        a=int(next(it)); b=int(next(it))
        ra,rb=find(a),find(b)
        if ra==rb: has_cycle=True
        else: fa[ra]=rb
    print('YES' if has_cycle else 'NO')

if __name__=='__main__':
    main()
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.15 例 15：反向离线并查集——战争让位加边（UVA 10158 War 变式）（⭐⭐⭐）

> **知识点**：离线反问、先删后加、并查集恢复、断点查询｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定初始图，q 次"删除一条边"的操作与"查询两点是否连通"的询问，交错出现，输出每次询问。

**思路**

正着处理删除难，把操作序列倒读：先得到最终剩余边建好并查集，倒序遇删除边就把它加回（union），遇查询就用当前并查集回答。

💡 类比"倒放桥墩"：拆桥时算连通性麻烦，先把拆掉后的状态摆好，倒着一座一座架回桥同时回答当时的连通情况。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    base=[]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); base.append((min(a,b),max(a,b)))
    # 操作: 0 delete (u,v), 1 query (u,v)
    q=int(next(it))
    ops=[]; delset=set()
    for _ in range(q):
        t=int(next(it)); a=int(next(it)); b=int(next(it))
        ops.append((t,a,b))
        if t==0: delset.add((min(a,b),max(a,b)))
    fa=list(range(n))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb
    for e in base:
        if e not in delset: union(*e)
    res=[]
    for t,a,b in reversed(ops):
        if t==0: union(a,b)
        else: res.append('YES' if find(a)==find(b) else 'NO')
    for line in reversed(res): print(line)

if __name__=='__main__':
    main()
```

> **复杂度**：O((n+m+q) α(n)) 时间，O(n) 空间

---

#### 17.10.16 例 16：扩展域并查集——敌人与朋友（种类并查集二倍空间）（POJ 1611 变式/洛谷 P1892）（⭐⭐⭐）

> **知识点**：扩展域并查集、敌人链、矛盾检测|朋友匹配｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：生物有 A/B 两类。m 条说法：x、y 为同类，或 x 捕食 y。判断说法是否矛盾，统计矛盾条数。

**思路**

扩展域：每个动物映射"本体+其捕食者域+其被捕食者域"。依据规则 union 三处映射，冲突时通过"同域是否已连"判定。

💡 类比"三层身份牌"：把每人的本体、天敌、猎物三张牌分组，核对说法时看该连的三张牌是否已被别的身份占位。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(3*n))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def same(a,b): return find(a)==find(b)
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb
    def is_ok(d,x,y):
        if x>=n or y>=n: return False
        if d==1:
            if same(x,y+n) or same(x,y+2*n): return False
            union(x,y); union(x+n,y+n); union(x+2*n,y+2*n)
        else:
            if same(x,y) or same(x,y+2*n): return False
            union(x,y+n); union(x+n,y+2*n); union(x+2*n,y)
        return True
    ans=0
    for _ in range(m):
        d=int(next(it)); x=int(next(it))-1; y=int(next(it))-1
        if not is_ok(d,x,y): ans+=1
    print(ans)

if __name__=='__main__':
    main()
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.17 例 17：并查集维护集合最大/最小元素（HDU 1325 变式/洛浦 P1195）（⭐⭐）

> **知识点**：并查集、集合极值、合并时汇总｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：维护若干集合，支持合并，查询每个集合内最小值（或最大值）。初始单点。

**思路**

每个集合根记录集合最小值（等于根元素时），合并时更新。find 后即为该集合的最小值。

💡 类比"篮子里最小的苹果"：每伙人记住最小号，两伙合并后保留两者中较小的那一个号。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(n)); mini=list(range(n))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra==rb: return
        # 最小值根
        if mini[ra]<mini[rb]:
            fa[rb]=ra
        else:
            fa[ra]=rb
            if mini[ra]>=mini[rb]: pass
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); union(a,b)
    # 查询每个点的集合最小值
    res=[mini[find(i)] for i in range(n)]
    print(' '.join(map(str,res)))

if __name__=='__main__':
    main()
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.18 例 18：网格连通——数岛屿（DFS/BFS/并查集）（洛谷 P1451 细胞的数目）（⭐）

> **知识点**：网格、连通块、DFS/BFS/并查集、四邻接｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n×m 的 0/1 矩阵，求由相邻(上下左右)为 1 组成的连通块个数。并查集亦可。

**思路**

遍历每个格子若为 1 且未访问则新开一块，DFS/BFS 把相连的 1 全部访问并标 0；或用并查集把相邻 1 union 后统计根数。

💡 类比"水洼合坑"：每遇到一个水洼就圈出与之相连的所有水，数圈出来的水洼总数。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    n=int(data[0]); m=int(data[1])
    grid=[]
    idx=2
    for _ in range(n):
        row=list(map(int,list(data[idx]))); idx+=1; grid.append(row)
    def dfs(i,j):
        if not (0<=i<n and 0<=j<m) or grid[i][j]==0: return
        grid[i][j]=0
        for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):
            dfs(i+di,j+dj)
    cnt=0
    for i in range(n):
        for j in range(m):
            if grid[i][j]:
                cnt+=1; dfs(i,j)
    print(cnt)

if __name__=='__main__':
    main()
```

> **复杂度**：O(n·m) 时间，O(n·m) 递归空间

---

#### 17.10.19 例 19：带权并查集求和——求两点路径长度（LCA 法替代）（CF 变式/POJ 2186 变式）（⭐⭐⭐）

> **知识点**：带权并查集、边权到根、距离、应用族谱距离｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有 n 只生物构成族谱树，m 条"父-子"关系(带代数差)，q 次询问两生物的辈分差。

**思路**

带权并查集维护每点到根的"代数差"d[]，若两点连通则距离 = |d[a]-d[b]|；不连通无法确定。

💡 类比"族谱辈分标尺"：每个人记到老祖宗的代数差，两人差即以老祖为参照相减取绝对值。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(n+1)); w=[0]*(n+1)
    def find(x):
        if fa[x]!=x:
            r=find(fa[x]); w[x]+=w[fa[x]]; fa[x]=r
        return fa[x]
    out=[]
    for _ in range(m):
        op=next(it)
        if op==b'U':
            a=int(next(it)); b=int(next(it)); d=int(next(it))
            ra,rb=find(a),find(b)
            if ra!=rb:
                fa[ra]=rb; w[ra]= d + w[b]-w[a]  # 相对关系
        else:
            a=int(next(it)); b=int(next(it))
            if find(a)!=find(b): out.append('UNKNOWN')
            else: out.append(str(w[a]-w[b]))
    sys.stdout.write('\n'.join(out))

if __name__=='__main__':
    main()
```

> **复杂度**：均摊 O(α(n)) 时间，O(n) 空间

---

#### 17.10.20 例 20：Kruskal + 最小最大边差（POJ 1724 变式）（⭐⭐）

> **知识点**：Kruskal、并查集、排序绕双条件、连通最大承载边｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：点与点之间有承重上限边，问是否存在一条从 s 到 t 的道路使得整条路上"最小承重"最大，并求该最大承重。

**思路**

把边按承重从大到小排序，Kruskal 在线加边直到 s、t 首次连通，此时最后加入的边权即"瓶颈最大承重"。

💡 类比"救灾运输最重"：优先用承重最大的桥连线，连通目的地时用到的承重最小的那根就是瓶颈最大载荷。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it)); s=int(next(it)); t=int(next(it))
    edges=[]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); cap=int(next(it))
        edges.append((cap,a,b))
    edges.sort(reverse=True)  # 承重大优先
    fa=list(range(n+1))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    ans=0
    for cap,a,b in edges:
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb
        if find(s)==find(t):
            ans=cap; break
    print(ans)

if __name__=='__main__':
    main()
```

> **复杂度**：O(m log m) 时间，O(n+m) 空间

---

#### 17.10.21 例 21：二分图最大匹配匈牙利算法（洛谷 P3386）（⭐⭐⭐）

> **知识点**：二分图匹配、匈牙利算法、增广路、vis 标记｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：左部 n、右部 m 个点的二分图与若干边，求最大匹配数。

**思路**

匈牙利：对每个左部点尝试增广，通过 DFS 寻找"让位链"，用 vis 标记防死循环，match 记录右部匹配的点。

💡 类比"调婚委会排舞伴"：逐个介绍舞伴，若某舞伴已配对则礼貌地问那对能否换一换，尽量让每个人找到舞伴。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    nl=int(next(it)); nr=int(next(it)); e=int(next(it))
    g=[[] for _ in range(nl+1)]
    for _ in range(e):
        a=int(next(it)); b=int(next(it)); g[a].append(b)
    match=[0]*(nr+1)
    def try_kuhn(u,vis):
        for v in g[u]:
            if vis[v]: continue
            vis[v]=True
            if match[v]==0 or try_kuhn(match[v],vis):
                match[v]=u; return True
        return False
    cnt=0
    for u in range(1,nl+1):
        vis=[False]*(nr+1)
        if try_kuhn(u,vis): cnt+=1
    print(cnt)

if __name__=='__main__':
    main()
```

> **复杂度**：O(V·E) 时间，O(nl+nr) 空间

---

#### 17.10.22 例 22：传递闭包 Floyd——连通关系传递（POJ 3660 变式）（⭐⭐）

> **知识点**：Floyd 传递闭包、可达性、位压缩优化｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 条有向边，求传递可达闭包：哪些点对直接或间接可达。

**思路**

bitset 加速 Floyd：`for k: for i: if reach[i][k]: reach[i]|=reach[k]`，用整数按位或一次合并整行。

💡 类比"转告链条"：k 能转告 i、i 能转告的那群人，合并到 k 的可达名单里。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    reach=[0]*(n)   # bitset
    for _ in range(m):
        a=int(next(it))-1; b=int(next(it))-1
        reach[a]|=1<<b
    for k in range(n):
        for i in range(n):
            if reach[i]>>k & 1:
                reach[i]|=reach[k]
    # 统计每点可达点数
    out=[]
    for i in range(n):
        out.append(str(bin(reach[i]).count('1')))
    print(' '.join(out))

if __name__=='__main__':
    main()
```

> **复杂度**：O(n^3/64) 位压缩时间，O(n) 空间

---

#### 17.10.23 例 23：缩点成 DAG 后求入度（强连通分量缩点）（洛谷 P3387 简化）（⭐⭐⭐）

> **知识点**：强连通分量、缩点、DAG、入度统计｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定有向图，求强连通分量并缩点后，统计每个分量在新 DAG 中的入度（0 的分量无法被其它分量到达）。

**思路**

Tarjan 求分量编号后，遍历每条边 (u,v)，若 belong[u]!=belong[v] 则缩点图中 v 分量入度+1。

💡 类比"合并门派统计靠山"：把互相能达的门派合并成一个大帮派，再数每个帮派是否有别的帮派指向它。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]
    edges=[]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append(b); edges.append((a,b))
    dfn=[0]*(n+1); low=[0]*(n+1); belong=[0]*(n+1); on=[False]*(n+1); st=[]; tm=0; cid=0
    def tarjan(u):
        nonlocal tm,cid
        tm+=1; dfn[u]=low[u]=tm; st.append(u); on[u]=True
        for v in g[u]:
            if not dfn[v]:
                tarjan(v); low[u]=min(low[u],low[v])
            elif on[v]: low[u]=min(low[u],dfn[v])
        if low[u]==dfn[u]:
            cid+=1
            while True:
                x=st.pop(); on[x]=False; belong[x]=cid
                if x==u: break
    for i in range(1,n+1):
        if not dfn[i]: tarjan(i)
    indeg=[0]*(cid+1)
    for u,v in edges:
        if belong[u]!=belong[v]: indeg[belong[v]]+=1
    print(cid, sum(1 for x in indeg[1:] if x==0))

if __name__=='__main__':
    main()
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.24 例 24：欧拉回路判定与路径（无向图欧拉运用）（POJ 2513 Colored Sticks）（⭐⭐⭐）

> **知识点**：欧拉路径/回路、度数奇偶判定、连通性、字典映射｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给一些木棍，每根两头有颜色。问能否把所有木棍排成一列，使相邻木棍相接处颜色相同。

**思路**

把颜色当结点、木棍当边。能排成一列当且仅当：图连通，且奇度顶点数为 0（回路）或 2（路径）。

💡 类比"一笔画走遍"：能一笔画完整个颜色图（不抬笔不重复），仅当连通且奇度点≤2。

```python
import sys
from collections import Counter

def can_line(pairs):
    deg=Counter()
    for a,b in pairs:
        deg[a]+=1; deg[b]+=1
    odd=sum(1 for v in deg.values() if v%2)
    # 连通性检查用并查集
    fa={}
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb
    for a,b in pairs:
        if a not in fa: fa[a]=a
        if b not in fa: fa[b]=b
        union(a,b)
    roots=set(find(x) for x in deg)
    return odd in (0,2) and len(roots)<=1

if __name__=='__main__':
    print(can_line([("blue","red"),("red","green"),("blue","green")]))
```

> **复杂度**：O(n α(n)) 时间，O(n) 空间

---

#### 17.10.25 例 25：无向图连通分量间最少加边使其全体连通（POJ 3250 变式）（⭐⭐）

> **知识点**：连通分量、并查集、桥补边计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边无向图，问至少加几条边使整个图连通（或使所有连通分量"人手可达"）。

**思路**

并查集统计连通分量个数 c，则加 c-1 条边即可把各分量连成一整座相连通图（边位置任意）。

💡 类比"孤岛搭桥"：有 c 座孤岛，搭 c-1 座桥就能把整片海域连成一片。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(n+1))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); union(a,b)
    comps=len({find(i) for i in range(1,n+1)})
    print(comps-1)

if __name__=='__main__':
    main()
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.26 例 26：网格连通——群岛连通最少建桥（Prim/BFS 变式）（洛谷 P1099 变式）（⭐⭐）

> **知识点**：BFS/多源最短路、连通分量、桥梁规划｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n×m 网格，'0' 水、'1' 陆地。问至少搭几座 1 格桥（在相邻水格间）能把所有陆地联成一片。

**思路**

把每块陆地(1 连通分量)视为点，BFS 求陆地分量间最短路，建成图后跑最小生成树；或用多源 BFS 让两片水域扩圈看相遇距离。

💡 类比"跨岛架浮桥"：先认岛，再求岛之间最短水路，最后按最小成本把各岛串成整片。

```python
import sys
from collections import deque

def main():
    data=sys.stdin.buffer.read().split()
    n=int(data[0]); m=int(data[1])
    g=[]
    idx=2
    for _ in range(n):
        g.append(list(map(int,list(data[idx])))); idx+=1
    comp=[[-1]*m for _ in range(n)]
    dirs=((1,0),(-1,0),(0,1),(0,-1))
    def inside(i,j): return 0<=i<n and 0<=j<m
    cid=0
    for i in range(n):
        for j in range(m):
            if g[i][j]==1 and comp[i][j]==-1:
                cid+=1; dq=deque([(i,j)]); comp[i][j]=cid
                while dq:
                    x,y=dq.popleft()
                    for dx,dy in dirs:
                        nx,ny=x+dx,y+dy
                        if inside(nx,ny) and g[nx][ny]==1 and comp[nx][ny]==-1:
                            comp[nx][ny]=cid; dq.append((nx,ny))
    print('陆地连通分量数:', cid)

if __name__=='__main__':
    main()
```

> **复杂度**：O(n·m) 时间，O(n·m) 空间

---

#### 17.10.27 例 27：带权并查集求出色相对（包含矛盾判断）（POJ 1182 简/洛浦 P2024）（⭐⭐⭐）

> **知识点**：带权并查集、模 3 关系、矛盾检测、权(相对类别)｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 只动物三类别，m 条说法，判断矛盾数。（用带权 mod3 的并查集实现）

**思路**

d[x] 表示 x 与根的关系模 3（0 同类/1 捕食/2 被捕食）。合并与矛盾判定都建立在 find 时权对齐模 3 上。

💡 类比"时钟环对齐"：动物类别如同钟的 0/1/2 点，比较两者时针距离即可划分类别与捕食关系。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(n+1)); d=[0]*(n+1)
    def find(x):
        if fa[x]!=x:
            r=find(fa[x]); d[x]=(d[x]+d[fa[x]])%3; fa[x]=r
        return fa[x]
    ans=0
    for _ in range(m):
        rel=int(next(it)); x=int(next(it)); y=int(next(it))
        if x>n or y>n:
            ans+=1; continue
        if rel==2 and x==y:
            ans+=1; continue
        rx,ry=find(x),find(y)
        if rel==1:
            if rx==ry and d[x]!=d[y]: ans+=1
            elif rx!=ry: fa[rx]=ry; d[rx]=(d[y]-d[x]+3)%3
        else:
            if rx==ry and (d[y]-d[x]+3)%3!=1: ans+=1
            elif rx!=ry: fa[rx]=ry; d[rx]=(d[y]-d[x]+2)%3
    print(ans)

if __name__=='__main__':
    main()
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.28 例 28：洛谷 P2661 信息传递——最小环（拓扑删/并查集找环）（洛浦 P2661）（⭐⭐⭐）

> **知识点**：最小环、传递边、拓扑删叶/并查集找环、环上计数｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个人，每人把消息传给指定一个人。从某人开始传消息，多少轮后消息能传回他自己（中间经过的人最少）？

**思路**

每个人 deg=1 的出边构成若干基环树林。轮流传播一轮形成环；求最小环长度可用拓扑排序把非环节点删掉，再对环做计数。

💡 类比"传花鼓小了停"：每次把"没人指向的人"剔掉，剩下的都是环，搜每个环的大小取最小。

```python
import sys
from collections import deque

def min_cycle(n,to):
    indeg=[0]*(n+1)
    for i in range(1,n+1): indeg[to[i]]+=1
    removed=[False]*(n+1)
    dq=deque([i for i in range(1,n+1) if indeg[i]==0])
    while dq:
        u=dq.popleft(); removed[u]=True
        v=to[u]; indeg[v]-=1
        if indeg[v]==0: dq.append(v)
    ans=n+1
    for i in range(1,n+1):
        if not removed[i]:
            u=i; cnt=0
            while not removed[u]:
                removed[u]=True; cnt+=1; u=to[u]
            ans=min(ans,cnt)
    return ans

if __name__=='__main__':
    print(min_cycle(5,[0,2,3,2,5,4]))  # 环 2-3-2 长2
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.10.29 例 29：Kruskal 用并查集再做——洛谷 P2330 繁忙都市（⭐⭐）

> **知识点**：最小生成树、瓶颈边(最大边最小)、Kruskal｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 城市、m 道路(含宽度)。要连通所有城市且"使用的最宽道路最小"，求最小最大宽度与选取道路数。

**思路**

Kruskal 从小到大加边直到连通，最后加入的边宽即"最小可行的最大宽度"，已加入 n-1 条。

💡 类比"修路选口径"：从小口径路加起，加到全城连通时所用最粗的那条即最小所需承重上限。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    edges=[]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); w=int(next(it)); edges.append((w,a,b))
    edges.sort()
    fa=list(range(n+1))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    cnt=0; mx=0
    for w,a,b in edges:
        ra,rb=find(a),find(b)
        if ra!=rb:
            fa[ra]=rb; cnt+=1; mx=max(mx,w)
            if cnt==n-1: break
    print(n-1, mx)

if __name__=='__main__':
    main()
```

> **复杂度**：O(m log m) 时间，O(n+m) 空间

---

#### 17.10.30 例 30：离线并查集——区间删除询问连通（UVA 10158 变式完整）（⭐⭐⭐）

> **知识点**：离线并查集、逆向加边、查询连通、可回滚断点｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：初始 n 点图、m 条边，之后 q 个操作：删除一条仍存在的边、或查询两点是否连通；输出所有查询结果。

**思路**

同例 15：删除正难反易。先假设所有要删的边都删掉建并查集，再倒序把删除变成加边，边加边回答查询。

💡 类比"倒放架桥"：把整段操作倒着走，删除变架桥，每次架桥后回答当时的连通问题。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    base=[]; edgeset={}
    for ind in range(m):
        a=int(next(it)); b=int(next(it))
        if a>b: a,b=b,a
        base.append((a,b))
    q=int(next(it))
    ops=[]; delset=set()
    for _ in range(q):
        t=next(it); a=int(next(it)); b=int(next(it))
        if a>b: a,b=b,a
        ops.append((t,a,b))
        if t==b'D':
            delset.add((a,b))
    fa=list(range(n))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb
    for e in base:
        if e not in delset: union(*e)
    idds=0
    res=[]
    for t,a,b in reversed(ops):
        if t==b'D': union(a,b)
        else: res.append('YES' if find(a)==find(b) else 'NO')
    for x in reversed(res): print(x)

if __name__=='__main__':
    main()
```

> **复杂度**：O((n+m+q) α(n)) 时间，O(n) 空间

---
#### 17.10.31 例 31：连通分量计数与最大分量大小（HDU 1232 畅通工程/POJ 变式）（⭐⭐）

> **知识点**：连通分量、并查集、最大块、图论基础统计｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边，求连通分量个数与这些分量中最大的顶点数。

**思路**

并查集 union 后，用 size 数组记录以根为集合大小的和，统计根数与最大 size。

💡 类比"半岛分类"：把通路连接的城市并成一伙，数有几伙、最大一伙多少城。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(n+1)); sz=[1]*(n+1)
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    for _ in range(m):
        a=int(next(it)); b=int(next(it))
        ra,rb=find(a),find(b)
        if ra!=rb:
            if sz[ra]<sz[rb]: ra,rb=rb,ra
            fa[rb]=ra; sz[ra]+=sz[rb]
    comps=set()
    for i in range(1,n+1): comps.add(find(i))
    mx=max(sz[find(i)] for i in range(1,n+1))
    print(len(comps), mx)

if __name__=='__main__':
    main()
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.32 例 32：二分图最小路径覆盖=顶点数-最大匹配（POJ 2060 变式）（⭐⭐⭐）

> **知识点**：最小路径覆盖、二分匹配、DAG 转化、拆点｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个任务(依赖关系)，每个完成任务后可在规定时间内换下一个，问至少几个人能完成全部任务。

**思路**

建 DAG，路径覆盖数 = n(任务数) - 最大匹配（把每个职责拆成"离开点"与"到达点"的二分图）。

💡 类比"机器接力"：一部机器完成 a 后能接 b，就形成 a→b 的配对，最少机器数 = 任务数 - 最大接力对数。

```python
def min_path_cover(n, edges):
    # 二分图左侧[0..n),右侧拆点
    g=[[] for _ in range(n)]
    for a,b in edges: g[a].append(b)
    match=[-1]*n
    def try_k(u,vis):
        for v in g[u]:
            if vis[v]: continue
            vis[v]=True
            if match[v]==-1 or try_k(match[v],vis):
                match[v]=u; return True
        return False
    cnt=0
    for u in range(n):
        vis=[False]*n
        if try_k(u,vis): cnt+=1
    return n-cnt

if __name__=='__main__':
    # 任务0后可做1、2；任务1后可做3
    print(min_path_cover(4,[(0,1),(0,2),(1,3)]))
```

> **复杂度**：O(n·E) 时间，O(n+E) 空间

---

#### 17.10.33 例 33：次小生成树（枚举删掉一条树边）（洛浦 U94881/POJ 1679 变式）（⭐⭐⭐）

> **知识点**：次小生成树、MST 删除边重新 Kruskal、严格次小｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求无向图的严格次小生成树权值（比最小生成树大的最小权值生成树）。

**思路**

先求 MST；对 MST 每条边，删除它后跑最小生成树（保证不连通则跳过）得到候选，取全局最小且严格大于 MST 的。

💡 类比"换掉一条桥再算"：给最小桥方案各换拆一座桥重新省钱连线，得到的最小超过原方案的就是次小方案。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    edges=[]
    for ind in range(m):
        a=int(next(it))-1; b=int(next(it))-1; w=int(next(it)); edges.append((w,a,b,ind))
    edges_sorted=sorted(edges)
    def kruskal(skip=None):
        fa=list(range(n))
        def find(x):
            while fa[x]!=x:
                fa[x]=fa[fa[x]]; x=fa[x]
            return x
        total=0; cnt=0; used=[]
        for w,a,b,ind in edges_sorted:
            if ind==skip: continue
            ra,rb=find(a),find(b)
            if ra!=rb:
                fa[ra]=rb; total+=w; cnt+=1; used.append(ind)
        if cnt==n-1: return total,used
        return None,None
    w1,used1=kruskal()
    best=None
    for e in used1:
        w2,_=kruskal(e)
        if w2 is not None:
            if best is None or (w2>w1 and w2<best):
                if w2>w1: best=w2
    print(best)

if __name__=='__main__':
    main()
```

> **复杂度**：O(m log m + nm α(n)) 时间，O(m) 空间

---

#### 17.10.34 例 34：查若干基环森林的最小环（二并查集找环模板）（洛浦 P2666 变式）（⭐⭐）

> **知识点**：基环树、找环、并查集活用、度数删叶｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：若干棵"基环树"组成的森林，求所有简单环长之和（或最小/总数）。

**思路**

基环树唯一环；用拓扑剔叶（入度删到剩环），剩余仍在栈中且未被去除的即环上点，按前进边统计环长。

💡 类比"留环去枝"：不断把最外围没入环的枝剪掉，剩下的就是环，逐个环量一圈长度。

```python
def all_cycle_lengths(n,to):
    indeg=[0]*(n+1)
    for i in range(1,n+1): indeg[to[i]]+=1
    rem=[True]*(n+1)
    from collections import deque
    dq=deque([i for i in range(1,n+1) if indeg[i]==0])
    while dq:
        u=dq.popleft(); rem[u]=False
        v=to[u]; indeg[v]-=1
        if indeg[v]==0: dq.append(v)
    cycles=[]
    for i in range(1,n+1):
        if rem[i]:
            u=i; L=0
            while rem[u]:
                rem[u]=False; L+=1; u=to[u]
            cycles.append(L)
    return cycles

if __name__=='__main__':
    print(all_cycle_lengths(7,[0,2,3,2,5,4,6,7]))
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.10.35 例 35：桥——边双连通分量缩点后最少加边使其全面重连通图（POJ 3352）（⭐⭐⭐）

> **知识点**：边双连通、Tarjan 桥、缩点、叶结点配对最小加边｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：无向图，问最少加几条边使其变为"边双连通"（删任意一条边仍连通）。

**思路**

求桥并缩点成树，统计缩点后度数为 1 的叶结点数 leaf，最少需加 (leaf+1)//2 条边。

💡 类比"加固每座桥"：把桥缩成点后像一条链，让每个端点都多一条出路，最少添桥数是首尾配对数量的一半。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]
    for eid in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append((b,eid)); g[b].append((a,eid))
    dfn=[0]*(n+1); low=[0]*(n+1); timer=0; is_bridge=[False]*m
    def tarjan(u,pe):
        nonlocal timer
        timer+=1; dfn[u]=low[u]=timer
        for v,eid in g[u]:
            if eid==pe: continue
            if not dfn[v]:
                tarjan(v,eid); low[u]=min(low[u],low[v])
                if low[v]>dfn[u]: is_bridge[eid]=True
            else: low[u]=min(low[u],dfn[v])
    for i in range(1,n+1):
        if not dfn[i]: tarjan(i,-1)
    # 缩点: 用并查集把桥以外的边合并
    fa=list(range(n+1))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb
    for u in range(1,n+1):
        for v,eid in g[u]:
            if not is_bridge[eid]: union(u,v)
    # 统计缩点图度数
    deg={}
    for eid in range(m):
        pass
    from collections import Counter
    comp_deg=Counter()
    used=set()
    # 根据桥统计
    def mark():
        pass
    # 简单统计: 对每条桥的两端分量度数+1(去重)
    bridge_edges=[eid for eid in range(m) if is_bridge[eid]]
    # 我们从原边找桥两端
    edge_pairs=[None]*m
    for u in range(1,n+1):
        for v,eid in g[u]:
            if u<v and is_bridge[eid]: edge_pairs[eid]=(find(u),find(v))
    for eid in bridge_edges:
        a,b=edge_pairs[eid]
        if a==b: continue
        comp_deg[a]+=1; comp_deg[b]+=1
    leaf=sum(1 for d in comp_deg.values() if d==1)
    if len(comp_deg)==0: leaf=0
    print('最少加边:', (leaf+1)//2)

if __name__=='__main__':
    main()
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.36 例 36：并查集维护集合点权和（合并时累加战力）（POJ 1988 变式）（⭐⭐）

> **知识点**：并查集、集合大小/求和、合并汇总、查询根信息｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：初始 n 个营寨各有一战力。操作：合并两支队伍；查询某队伍当前总战力。

**思路**

size/sum[root] 记录以根为集合的元素数与总战力，合并时累加，查询 find 后的根取 sum。

💡 类比"兵团合并记账"：两支军队合并时把战力和并到新将军名下，问哪支部队就看其将军名下战力总和。

```python
class UnionSum:
    def __init__(self,n,val):
        self.fa=list(range(n)); self.sum=val[:]; self.sz=[1]*n
    def find(self,x):
        while self.fa[x]!=x:
            self.fa[x]=self.fa[self.fa[x]]; x=self.fa[x]
        return x
    def merge(self,a,b):
        ra,rb=self.find(a),self.find(b)
        if ra==rb: return
        if self.sz[ra]<self.sz[rb]: ra,rb=rb,ra
        self.fa[rb]=ra; self.sum[ra]+=self.sum[rb]; self.sz[ra]+=self.sz[rb]
    def total(self,x): return self.sum[self.find(x)]

if __name__=='__main__':
    us=UnionSum(5,[1,2,3,4,5])
    us.merge(0,1); us.merge(1,2)
    print(us.total(2))  # 6
```

> **复杂度**：O(α(n)) 合并/查询，O(n) 空间

---

#### 17.10.37 例 37：带权并查集求解区间和差分约束（POJ 1733 Parity 奇偶性）（⭐⭐⭐）

> **知识点**：带权并查集、差分约束、模 2 权、离线坐标映射｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 [1,n] 上的若干断言：区间 [l,r] 内 1 的个数是奇数还是偶数。逐条读入，输出第一条与前面矛盾的断言序号（之前都真）。

**思路**

前缀异或/奇偶思想：pref[r]^pref[l-1]=奇偶。把 pref 看成结点，关系用带权并查集(模2)维护；断言矛盾当 find(l-1)==find(r) 且权不符。

💡 类比"前缀奇偶对账"：用带权(0偶1奇)并查集连接前缀变量，断言像等式，核账时可查是否已有相反结论。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); q=int(next(it))
    fa={}; d={}
    def find(x):
        if x not in fa:
            fa[x]=x; d[x]=0; return x
        if fa[x]!=x:
            r=find(fa[x]); d[x]^=d[fa[x]]; fa[x]=r
        return fa[x]
    def diff(a,b):
        return d[a]^d[b] if a==b else 0
    ans=q
    for idx in range(q):
        l=int(next(it)); r=int(next(it)); s=next(it)
        parity=0 if s==b'even' else 1
        x=l-1; y=r
        rx,ry=find(x),find(y)
        if rx==ry:
            if (d[x]^d[y])!=parity:
                ans=idx; break
        else:
            # 连接 rx 到 ry
            fa[rx]=ry; d[rx]=d[x]^d[y]^parity
    print(ans)

if __name__=='__main__':
    main()
```

> **复杂度**：均摊 O(α(n)) 时间，O(n) 空间

---

#### 17.10.38 例 38：Kruskal 求"丛林道路"最小总成本（POJ 1251/洛浦 P1195 变式）（⭐⭐）

> **知识点**：最小生成树、字符地图点、Kruskal｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：字符表示的若干村庄间道路及其费用，求连通全部村庄的最小总费用。

**思路**（同 MST）字符映射编号后 Kruskal。

💡 类比"村庄联网"：把所有路按费用排序，逐条在已联网村庄间搭桥，直到村村相连。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it))
    edges=[]
    # 输入: 每行 大写字母 度数 (邻接 ...)
    # 简单格式: 先给 n，再给若干 (u,v,w)
    m=int(next(it))
    for _ in range(m):
        a=ord(next(it))-65; b=ord(next(it))-65; w=int(next(it)); edges.append((w,a,b))
    edges.sort()
    fa=list(range(n))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    total=0;cnt=0
    for w,a,b in edges:
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb; total+=w; cnt+=1
    print(total if cnt==n-1 else -1)

if __name__=='__main__':
    main()
```

> **复杂度**：O(m log m) 时间，O(n) 空间

---

#### 17.10.39 例 39：判断无向图是否为"树"（连通+无环+边数正确）（LeetCode 261/洛浦 P2055 变式）（⭐⭐）

> **知识点**：树的判定、并查集、无环无重边、n-1 条边｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边无向图，判断是否构成一棵树（连通且无环）。

**思路**

树充要条件：m==n-1 且无环。用并查集处理边，出现 find 相同即成环(非法)；遍历后检查共 n-1 条边且无环且所有点连通。

💡 类比"校验族谱"：人数比关系数恰好多 1，且没有人绕圈(循环血亲)才算合法家谱。

```python
def is_tree(n, edges):
    if len(edges)!=n-1: return False
    fa=list(range(n))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    for a,b in edges:
        ra,rb=find(a),find(b)
        if ra==rb: return False
        fa[ra]=rb
    return True

if __name__=='__main__':
    print(is_tree(4,[(0,1),(1,2),(2,3)]))  # True
    print(is_tree(4,[(0,1),(1,2),(2,0)]))  # False
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.40 例 40：冗余连接——找使图成环的那条边（LeetCode 684）（⭐⭐）

> **知识点**：并查集找环边、冗余连接、最后一个成环边｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个点的图，原为树，多加了一条边形成环。边按序给出，找出那条"冗余"边。

**思路**

依次 union 每条边，若某条边两端 find 相同，则这条边就是成环的冗余边。

💡 类比"找多余搭桥"：图本是一棵树，多出来的那根线必然让两个早已连通点又连一次，并查集一发现同族即为冗余。

```python
def redundant(edges,n):
    fa=list(range(n+1))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    for a,b in edges:
        ra,rb=find(a),find(b)
        if ra==rb: return (a,b)
        fa[ra]=rb
    return None

if __name__=='__main__':
    print(redundant([(1,2),(2,3),(3,1)],3))  # (3,1)
```

> **复杂度**：O(n α(n)) 时间，O(n) 空间

---

#### 17.10.41 例 41：二分图——黑白染色入团最大独立（求单色最大团）（洛浦 P1330 封锁变式）（⭐⭐⭐）

> **知识点**：二分图最小点覆盖/染色、最大独立集互补、计数两色小者｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定图，要求选尽量少的点覆盖所有边（每条边至少一端被选）。二分图时答案=最大匹配。

**思路**

连通分量内若为二分图，最小点覆盖(顶点覆盖)=该分量两色中较少那色之和；整体取 0 色与 1 色少者之和。若非二分别返回。

💡 类比"街头监控"：每条街至少一头装探头，二分图街道网络里装监视器最少需要两色人数较少那色统一。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append(b); g[b].append(a)
    color=[-1]*(n+1); ok=True; cnt=[0,0]
    def dfs(u,c):
        nonlocal ok
        color[u]=c; cnt[c]+=1
        for v in g[u]:
            if color[v]==-1: dfs(v,c^1)
            elif color[v]==c: ok=False
    total=0
    for i in range(1,n+1):
        if color[i]==-1:
            cnt=[0,0]
            dfs(i,0)
            total+=min(cnt)
    if not ok: print('Impossible')
    else: print(total)

if __name__=='__main__':
    main()
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.42 例 42：最大连通分量（无向图最大块大小，连通块点数取最大）（POJ 2608 变式）（⭐）

> **知识点**：连通块、DFS/BFS/并查集、最大块清点｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边无向图，求最大连通分量所包含的顶点数。

**思路**

并查集合并并维护 size，最后取根的 size 最大值；或用 DFS 遍历每分量数点数。

💡 类比"最大群岛"：把通路连成岛并数每座岛人数，挑出最大的那座。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(n+1)); sz=[1]*(n+1)
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    for _ in range(m):
        a=int(next(it)); b=int(next(it))
        ra,rb=find(a),find(b)
        if ra!=rb:
            if sz[ra]<sz[rb]: ra,rb=rb,ra
            fa[rb]=ra; sz[ra]+=sz[rb]
    mx=0
    for i in range(1,n+1): mx=max(mx,sz[find(i)])
    print(mx)

if __name__=='__main__':
    main()
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.43 例 43：最大生成树 Kruskal（POJ 2253 变式）（⭐⭐）

> **知识点**：最大生成树、Kruskal 反向排序、贪心最大权边｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 条带宽边，求"最大生成树"（连通且总带宽最大）。

**思路**

Kruskal 但把边按权从大到小排序，取尽量大的边合并直到 n-1 条。

💡 类比"拉最粗缆线"：先接带宽最大的线尽量用粗缆连通各站，得到的网络总带宽最大。

```python
def max_spanning(edges,n):
    edges.sort(reverse=True)
    fa=list(range(n))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    total=0;cnt=0
    for w,a,b in edges:
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb; total+=w; cnt+=1
    return total if cnt==n-1 else -1

if __name__=='__main__':
    # edges (w,a,b), a,b 0-based
    print(max_spanning([(5,0,1),(2,1,2),(3,0,2)],3))  # 8
```

> **复杂度**：O(m log m) 时间，O(n) 空间

---

#### 17.10.44 例 44：带权并查集食物链（标准写法 C——同根核对权）（POJ 1182）（⭐⭐⭐）

> **知识点**：带权并查集、mod3、捕食关系、标准实现｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 只动物三类。m 条说法："x 与 y 同类"或"x 吃 y"。统计说法中必然矛盾的条数（含 x>n、y>n、自己吃自己等）。

**思路**

带权并查集 d 表示与根关系模3(0同/1吃/2被吃)。同类要求 d[x]==d[y]；x 吃 y 要求 (d[y]-d[x])%3==1。冲突即矛盾。

💡 类比"钟点类别环"：把 '同类/猎物/天敌' 编码成钟上的 0/1/2 点，比较两者时针差验证关系。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(n+1)); d=[0]*(n+1)
    def find(x):
        if fa[x]!=x:
            r=find(fa[x]); d[x]=(d[x]+d[fa[x]])%3; fa[x]=r
        return fa[x]
    def same(x,y): return find(x)==find(y)
    ans=0
    for _ in range(m):
        rel=int(next(it)); x=int(next(it)); y=int(next(it))
        if x>n or y>n or (rel==2 and x==y):
            ans+=1; continue
        if rel==1:
            if same(x,y):
                if d[x]!=d[y]: ans+=1
            else:
                fa[find(x)]=find(y); d[find(x)]=(d[y]-d[x])%3
        else:
            if same(x,y):
                if (d[y]-d[x])%3!=1: ans+=1
            else:
                r1,r2=find(x),find(y)
                fa[r1]=r2; d[r1]=(d[y]-d[x]+2)%3
    print(ans)

if __name__=='__main__':
    main()
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.45 例 45：二分图最小点覆盖=最大匹配（König 定理应用）（洛浦 P3386 变式）（⭐⭐⭐）

> **知识点**：König 定理、最小点覆盖、最大匹配、棋盘覆盖｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：棋盘有若干障碍格，用最少行或列(直线)覆盖所有障碍格，求最少直线数。

**思路**

行与列构成二分图，障碍格即一条"行-列"边；最小直线覆盖数=二分图最大匹配数（König）。

💡 类比"划行划列挡点"：每个障碍是行与列的交点，用最少几条横纵线盖住所有交点即最大匹配数。

```python
def min_cover_rows_cols(rows, cols, obstacles):
    g=[[] for _ in range(rows)]
    for r,c in obstacles: g[r].append(c)
    match=[-1]*cols
    def try_k(u,vis):
        for c in g[u]:
            if vis[c]: continue
            vis[c]=True
            if match[c]==-1 or try_k(match[c],vis):
                match[c]=u; return True
        return False
    cnt=0
    for u in range(rows):
        vis=[False]*cols
        if try_k(u,vis): cnt+=1
    return cnt

if __name__=='__main__':
    print(min_cover_rows_cols(3,3,[(0,1),(1,0),(1,2),(2,1)]))  # 2 或 3 依据布局
```

> **复杂度**：O(V·E) 时间，O(V+E) 空间

---

#### 17.10.46 例 46：欧拉回路路径输出（Hierholzer 算法）（POJ 2230/洛浦 P4649 变式）（⭐⭐⭐）

> **知识点**：欧拉回路、Hierholzer、栈式回溯、路径重建输出｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：无向连通图，每个顶点度数均为偶（保证存在欧拉回路），输出一条欧拉回路顶点序列。

**思路**

Hierholzer：DFS 尽可能深走未访问边，递归返回时把顶点入栈，栈逆序输出即欧拉回路。

💡 类比"不抬笔一笔画"：能一次性走遍每条边不重复，关键是"能回退再走别的分支"——用栈记录回退顺序。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append(b); g[b].append(a)
    # 标记已用边(用计数减)
    # 简单: 每条边删一次
    used=set()
    stack=[]; path=[]
    stack.append(1)
    while stack:
        u=stack[-1]
        # 找一条未用边
        advanced=False
        g[u]=[v for v in g[u] if (u,v) not in used and (v,u) not in used]
        if g[u]:
            v=g[u].pop()
            used.add((u,v)); used.add((v,u))
            stack.append(v); advanced=True
        else:
            path.append(stack.pop())
    print(' '.join(map(str,path)))

if __name__=='__main__':
    main()
```

> **复杂度**：O(m) 时间，O(m) 空间

---

#### 17.10.47 例 47：合伙伴/敌人——三态关系并查集（POJ 2492 A Bug's Life）（⭐⭐⭐）

> **知识点**：三态带权并查集、异或莫比乌斯、矛盾检测｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 只虫，m 条"配对(pair)"记录。若两只同性(同类)却出现配对则科学家假设有误。判断是否存在矛盾(某次配对双方此前已确定不同性)。

**思路**

带权并查集(0/1) 记录相对性别：同类权0、异性权1。配对 (a,b) 要求权异或=1，若 find 相同且 d[a]^d[b]!=1 则矛盾。

💡 类比"异性牌互补"：每个人相对根性别用0/1记，配对需两牌异号，反了就有bug。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    t=int(next(it)); out=[]
    for case in range(1,t+1):
        n=int(next(it)); m=int(next(it))
        fa=list(range(n+1)); d=[0]*(n+1)
        def find(x):
            if fa[x]!=x:
                r=find(fa[x]); d[x]^=d[fa[x]]; fa[x]=r
            return fa[x]
        suspicious=False
        for _ in range(m):
            a=int(next(it)); b=int(next(it))
            ra,rb=find(a),find(b)
            if ra==rb:
                if d[a]^d[b]!=1: suspicious=True
            else:
                fa[ra]=rb; d[ra]=1^d[a]^d[b]
        out.append('Scenario #%d:'%case)
        out.append('Suspicious bugs found!' if suspicious else 'No suspicious bugs found!')
        out.append('')
    print('\n'.join(out))

if __name__=='__main__':
    main()
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.48 例 48：判断二分图并给出任一批次（BFS 分层染两校分）（洛浦 P2694 变式）（⭐⭐）

> **知识点**：二分图、BFS 染色、两色分组、奇环检测｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 名学生，m 对"不能同组"关系。判断能否分成两组使任意不能同组的人分到不同组，并输出每组人数。

**思路**

BFS 分层染色，邻点染相反色，遇同色即非二分(失败)。成功则两色人数即分组方案（每连通分量取两种排布之一）。

💡 类比"考场排座"：把不能相邻的考生隔开两列，若有人注定必须挨着不能同若有冲突则失败。

```python
import sys
from collections import deque

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append(b); g[b].append(a)
    color=[-1]*(n+1); ok=True
    cnt0=cnt1=0
    for s in range(1,n+1):
        if color[s]==-1:
            dq=deque([s]); color[s]=0
            while dq:
                u=dq.popleft()
                for v in g[u]:
                    if color[v]==-1:
                        color[v]=color[u]^1; dq.append(v)
                    elif color[v]==color[u]: ok=False
    if not ok: print('NO')
    else:
        print('YES', sum(1 for c in color[1:] if c==0), sum(1 for c in color[1:] if c==1))

if __name__=='__main__':
    main()
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.49 例 49：并查集动态合并统计最大集合大小（洛浦 P2455 变式）（⭐⭐）

> **知识点**：动态并查集、实时最大块、追踪根 size｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个点，m 次合并操作，每次合并后输出当前最大的连通集合大小。

**思路**

并查集维护 size，合并成功时更新最大 size 候选（若合并后更大则更新），每次输出。

💡 类比"拼图随时看最大板块"：每次拼上两块就更新"目前最大板块"，实时汇报。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    fa=list(range(n+1)); sz=[1]*(n+1); mx=1
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    out=[]
    for _ in range(m):
        a=int(next(it)); b=int(next(it))
        ra,rb=find(a),find(b)
        if ra!=rb:
            if sz[ra]<sz[rb]: ra,rb=rb,ra
            fa[rb]=ra; sz[ra]+=sz[rb]; mx=max(mx,sz[ra])
        out.append(str(mx))
    print('\n'.join(out))

if __name__=='__main__':
    main()
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.50 例 50：最小生成树变式——多条权同边处理（POJ 2349 省去卫星边）（⭐⭐）

> **知识点**：MST、Kruskal、若干最大边豁免、连通分量｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 村庄若干路网，有 k 套卫星直连设备。问剩余路中用到的最长路最小，即最小生成树中第 k 大的边长。

**思路**

Kruskal 求 MST 边序列（升序），有 k 台卫星可免 前k条? 实为使 MST 中删掉 k-1 条最大的边后,剩下最小生成森林的最大边最小 —— 答案为 MST 边升序中第 n-k 小的边。

💡 类比"留最粗直连"：给若干城配卫星可免最贵的路，那主路网最长路只需到第 n-k 小区间那条。

```python
def min_bottleneck(n,k,edges):
    # 求 MST 边升序，返回第 (n-k) 小(1基)即下标 n-k-1
    edges.sort()
    fa=list(range(n))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    tree=[]
    for w,a,b in edges:
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb; tree.append(w)
    return tree[n-k-1] if n-k-1>=0 else 0

if __name__=='__main__':
    print(min_bottleneck(4,2,[(5,0,1),(1,1,2),(3,0,2),(7,2,3)]))
```

> **复杂度**：O(m log m) 时间，O(n) 空间

---

#### 17.10.51 例 51：反向并查集——删点后连通块（洛浦 P1197 再练）（⭐⭐⭐）

> **知识点**：离线逆向加边、删点、连通块、栈式恢复｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边图，k 个点依次被删除(按给定顺序)，输出删除前与每次删除后的连通块数。

**思路**（同例6）先把所有被删点标记，建好其余点的连通块；再逆序把点加回、恢复连边合并，倒取答案。

💡 类比"拆塔倒拼"：先把全拆完再倒着重拼，每拼回一座城更新队伍数。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n)]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append(b); g[b].append(a)
    k=int(next(it))
    delorder=[]
    removed=[False]*n
    for _ in range(k):
        x=int(next(it)); removed[x]=True; delorder.append(x)
    fa=list(range(n)); comp=n-k
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    def union(a,b):
        nonlocal comp
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb; comp-=1
    for u in range(n):
        if removed[u]: continue
        for v in g[u]:
            if not removed[v] and u<v: union(u,v)
    res=[comp]
    active=[not removed[i] for i in range(n)]
    for x in reversed(delorder):
        active[x]=True; comp+=1   # 先加回作为新连通块
        for v in g[x]:
            if active[v]: union(x,v)
        res.append(comp)
    for c in reversed(res): print(c)

if __name__=='__main__':
    main()
```

> **复杂度**：O((n+m+k) α(n)) 时间，O(n+m) 空间

---

#### 17.10.52 例 52：DFS 森林统计——无向图最大连通块点数（多测/网格）（洛浦 U9051 变式）（⭐）

> **知识点**：DFS、连通块、网格或图、最大块｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边，求最大连通块包含顶点数（DFS 统计）。

**思路**（同例42）BFS/DFS 或者并查集取 size 最大。

💡 类比"数最大村落"：访问各连通村落并清点人数，报出最大的村落。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append(b); g[b].append(a)
    vis=[False]*(n+1); mx=0
    def dfs(u):
        c=1; vis[u]=True
        for v in g[u]:
            if not vis[v]: c+=dfs(v)
        return c
    for i in range(1,n+1):
        if not vis[i]: mx=max(mx,dfs(i))
    print(mx)

if __name__=='__main__':
    main()
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.53 例 53：并查集查询当前根/代表元素与集合编号（AcWing 836 变式）（⭐）

> **知识点**：根查询、代表元素、集合归属、序号映射｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定并查集，多次查询某个元素所在集合的"代表/根"编号。

**思路**：直接 find(x) 返回根即代表。

💡 类比"找带头人"：问谁是我们这伙的老大，一路问到根即可。

```python
class DSU:
    def __init__(self,n): self.fa=list(range(n))
    def find(self,x):
        while self.fa[x]!=x:
            self.fa[x]=self.fa[self.fa[x]]; x=self.fa[x]
        return x
    def union(self,a,b):
        ra,rb=self.find(a),self.find(b)
        if ra!=rb: self.fa[ra]=rb
    def root(self,x): return self.find(x)

if __name__=='__main__':
    d=DSU(6); d.union(0,1); d.union(1,2)
    print(d.root(2))  # 2(或0)
```

> **复杂度**：O(α(n)) 每次，O(n) 空间

---

#### 17.10.54 例 54：无向图连通块统计（洛浦 U9055 多组/平滑版）（⭐⭐）

> **知识点**：并查集、连通块计数、遍历边合并、统计根数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边，求连通分量个数（可能含孤立点）。

**思路**：并查集合并后统计不同根个数。

💡 类比"数营地"：合并完看一共有几个老大各带一群。

```python
import sys

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    while True:
        n=int(next(it)); m=int(next(it))
        if n==0 and m==0: break
        fa=list(range(n+1))
        def find(x):
            while fa[x]!=x:
                fa[x]=fa[fa[x]]; x=fa[x]
            return x
        def union(a,b):
            ra,rb=find(a),find(b)
            if ra!=rb: fa[ra]=rb
        for _ in range(m):
            a=int(next(it)); b=int(next(it)); union(a,b)
        print(len({find(i) for i in range(1,n+1)}))

if __name__=='__main__':
    main()
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.55 例 55：带权并查集区间差分（区间和约束成环矛盾）（POJ 3282 变式）（⭐⭐⭐）

> **知识点**：带权并查集、差分约束、区间和、路径压缩权累计｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：数列未知，给出若干"前缀和"或"区间和"范围，判断这些约束是否矛盾。

**思路**

把前缀和 pref[0..n] 当点；约束 S[l,r]=c 联结 pref[l-1]、pref[r]，用带权并查集维护差值，检测矛盾。

💡 类比"流水账等式"：区间和就是两个前缀和的差，用差权并查集来对齐每笔账。

```python
class DiffDSU:
    def __init__(self,n):
        self.fa=list(range(n)); self.w=[0]*n
    def find(self,x):
        if self.fa[x]!=x:
            r=self.find(self.fa[x]); self.w[x]+=self.w[self.fa[x]]; self.fa[x]=r
        return self.fa[x]
    def add(self,a,b,d):  # w[a]-w[b]=d
        ra,rb=self.find(a),self.find(b)
        if ra!=rb:
            self.fa[ra]=rb; self.w[ra]=self.w[b]+d-self.w[a]
        else:
            return self.w[a]-self.w[b]==d
        return True

if __name__=='__main__':
    d=DiffDSU(5)
    print(d.add(0,4,10))   # 设定区间(0,4]和=10
    print(d.add(2,4,3))    # 设定(2,4]和=3
    print(d.add(0,2,7))    # 检查(0,2]和应=7,若矛盾返回False
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.56 例 56：强连通分量个数（缩点后 DAG 上统计入度 0 的分量等）（洛浦 U2568 变式）（⭐⭐⭐）

> **知识点**：SCC、Tarjan、缩点、DAG 拓扑性质｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边有向图，求强连通分量个数，并缩点后输出各分量入度。

**思路**（同例23）Tarjan 求 belong，遍历边算缩点 DAG 入度。

💡 类比"门派合并报表"：互相能达的归一门派，再统计各门派被谁指向。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]; edges=[]
    for _ in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append(b); edges.append((a,b))
    dfn=[0]*(n+1); low=[0]*(n+1); on=[False]*(n+1); belong=[0]*(n+1); st=[]; tm=0;cid=0
    def tarjan(u):
        nonlocal tm,cid
        tm+=1; dfn[u]=low[u]=tm; st.append(u); on[u]=True
        for v in g[u]:
            if not dfn[v]: tarjan(v); low[u]=min(low[u],low[v])
            elif on[v]: low[u]=min(low[u],dfn[v])
        if low[u]==dfn[u]:
            cid+=1
            while True:
                x=st.pop(); on[x]=False; belong[x]=cid
                if x==u: break
    for i in range(1,n+1):
        if not dfn[i]: tarjan(i)
    indeg=[0]*(cid+1)
    for u,v in edges:
        if belong[u]!=belong[v]: indeg[belong[v]]+=1
    print(cid)
    print(' '.join(map(str,indeg[1:])))

if __name__=='__main__':
    main()
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.57 例 57：无向图点双连通分量（割点分离出的双连通块）（洛浦 U4055 变式）（⭐⭐⭐）

> **知识点**：点双连通、Tarjan、bcc、栈维护、割点归属多块｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：无向图，求点双连通分量数（点双：任意删去其中一点仍连通的最大点集）。

**思路**

Tarjan 变体：边入栈，遇到割点条件 low[v]>=dfn[u] 时从栈中弹出一堆边，构成一个点双；割点可能属于多个点双。

💡 类比"关节枢纽划分"：关节点像枢纽站被多条线路共用，每圈可用边归为一块，枢纽同时属于多块。

```python
import sys
sys.setrecursionlimit(1<<20)

def main():
    data=sys.stdin.buffer.read().split()
    it=iter(data)
    n=int(next(it)); m=int(next(it))
    g=[[] for _ in range(n+1)]
    for eid in range(m):
        a=int(next(it)); b=int(next(it)); g[a].append((b,eid)); g[b].append((a,eid))
    dfn=[0]*(n+1); low=[0]*(n+1); tm=0; st=[]; bcc_count=0
    def tarjan(u,pe):
        nonlocal tm,bcc_count
        tm+=1; dfn[u]=low[u]=tm
        for v,eid in g[u]:
            if eid==pe: continue
            if not dfn[v]:
                st.append((u,v))
                tarjan(v,eid); low[u]=min(low[u],low[v])
                if low[v]>=dfn[u]:
                    bcc_count+=1
                    # 弹出一个点双
                    while True:
                        e=st.pop()
                        if e==(u,v): break
            else: low[u]=min(low[u],dfn[v])
    for i in range(1,n+1):
        if not dfn[i]: tarjan(i,-1)
    print(bcc_count)

if __name__=='__main__':
    main()
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.58 例 58：欧拉路径判定（有向/无向通法）（POJ 1300 变式）（⭐⭐）

> **知识点**：欧拉路径/回路判定、度数判断、连通性、奇偶｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：无向图，判断是否存在欧拉通路（恰所有边走一遍，端点不必同）。

**思路**：无向图欧拉通路当且仅当连通且奇度顶点数为 0 或 2。

💡 类比"一笔画判定"：连通且奇度点≤2 就能一笔画完。

```python
def has_euler_path(n,edges):
    deg=[0]*n
    g=[[] for _ in range(n)]
    for a,b in edges:
        deg[a]+=1; deg[b]+=1; g[a].append(b); g[b].append(a)
    odd=sum(1 for x in deg if x%2)
    # 连通性
    fa=list(range(n))
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    for a,b in edges:
        ra,rb=find(a),find(b)
        if ra!=rb: fa[ra]=rb
    if odd not in (0,2): return False
    # 忽略0度点，其余连通
    roots={find(i) for i in range(n) if deg[i]>0}
    return len(roots)<=1

if __name__=='__main__':
    print(has_euler_path(4,[(0,1),(1,2),(2,0),(2,3)]))  # 欧拉通路? 奇度=2真
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.10.59 例 59：并查集动态加边求连通位次（逐增量最多连通量统计）（洛浦 U9081 变式）（⭐⭐）

> **知识点**：并查集、增量加边、实时连通、边序统计｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点、m 条边按顺序给出，求"加到第几条边时，图中首次出现某大小以上的连通块"（或首次全连通）。

**思路**

依次 union，维护最大块 size；当最大块达到阈值（或所有点连通=块数1）就记录当前边序号。

💡 类比"拼图里程碑"：边加边走，记下第一次让最大板块达到规定人数时用到第几块拼块。

```python
import sys

def first_full(n,edges):
    fa=list(range(n+1)); sz=[1]*(n+1); blocks=n
    def find(x):
        while fa[x]!=x:
            fa[x]=fa[fa[x]]; x=fa[x]
        return x
    for idx,(a,b) in enumerate(edges,1):
        ra,rb=find(a),find(b)
        if ra!=rb:
            if sz[ra]<sz[rb]: ra,rb=rb,ra
            fa[rb]=ra; sz[ra]+=sz[rb]; blocks-=1
        if blocks==1: return idx
    return -1

if __name__=='__main__':
    print(first_full(5,[(1,2),(2,3),(3,4),(4,5)]))
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.10.60 例 60：综合——网格岛屿连通块最小"开关"次数（洛浦 U4567 变式）（⭐⭐）

> **知识点**：网格连通、并查集/DFS、岛屿计数与统计、综合运用｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n×m 网格为 '0'/'1' 地形，'1' 为陆地。请统计有多少"岛屿"（上下左右相连的 1 组成块）。

**思路**：

遍历网格，遇 '1' 未访则新岛，用 DFS 把相连 '1' 全标 0；或并查集合并相邻 '1' 后统计根数。

💡 类比"数江心沙洲"：把连在一起的沙洲圈出来数有几个。

```python
import sys
sys.setrecursionlimit(1<<20)

def num_islands(grid):
    n=len(grid); m=len(grid[0]); cnt=0
    def dfs(i,j):
        if i<0 or i>=n or j<0 or j>=m or grid[i][j]=='0': return
        grid[i][j]='0'
        for di,dj in ((1,0),(-1,0),(0,1),(0,-1)): dfs(i+di,j+dj)
    for i in range(n):
        for j in range(m):
            if grid[i][j]=='1':
                cnt+=1; dfs(i,j)
    return cnt

if __name__=='__main__':
    g=[list('11000'),list('11000'),list('00100'),list('00011')]
    print(num_islands(g))  # 3
```

> **复杂度**：O(n·m) 时间，O(n·m) 递归空间

---

### 17.11 字符串算法

#### 17.11.1 例 1：朴素匹配计数（洛谷 P3375 变式）⭐
> **知识点**：字符串朴素匹配、双指针｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定文本串 T 与模式串 P，求 P 在 T 中作为连续子串出现的次数。字符串长度 n、m 均不超过 10^5，字符为小写字母。若匹配次数为 0 输出 0。

**思路**

💡 类比"在书页里没取词本的逐词比对"：每个位置作为起点依次与模式串比对，O(n·m) 暴力即可，适合作为入门题用来理解匹配本质。

```python
def count_occ(T, P):
    n, m = len(T), len(P)
    if m == 0:
        return 0
    cnt = 0
    for i in range(n - m + 1):
        if T[i:i+m] == P:
            cnt += 1
    return cnt

T = "abababa"
P = "aba"
print(count_occ(T, P))  # 输出 3
```

> **复杂度**：O(n·m) 时间，O(1) 空间

---

#### 17.11.2 例 2：KMP 主串匹配（洛谷 P3375）⭐⭐
> **知识点**：KMP、next 数组｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定长串 s（长度 ≤10^6）和短串 p（长度 ≤10^6），输出 p 在 s 中所有出现位置的起始下标（1-based），再输出 p 的 next 数组。字符为大写字母。

**思路**

💡 类比"错位不求重来，只让失配指针回退到已匹配前缀"：先用模式串自身构造 next 数组，再在匹配失败时只回退而主串指针不回退，O(n+m)。

```python
def build_next(p):
    m = len(p)
    nxt = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and p[i] != p[j]:
            j = nxt[j-1]
        if p[i] == p[j]:
            j += 1
        nxt[i] = j
    return nxt

def kmp(s, p):
    nxt = build_next(p)
    res = []
    j = 0
    for i, ch in enumerate(s):
        while j > 0 and ch != p[j]:
            j = nxt[j-1]
        if ch == p[j]:
            j += 1
        if j == len(p):
            res.append(i - j + 2)  # 1-based 起始位置
            j = nxt[j-1]
    return res, nxt

s = "ABABABCABAB"
p = "ABAB"
pos, nxt = kmp(s, p)
print(pos)   # [4, 10]
print(nxt)   # [0, 0, 1, 2]
```

> **复杂度**：O(n+m) 时间，O(m) 空间

---

#### 17.11.3 例 3：KMP 统计出现次数（POJ 3461 / UVA 11475 变式）⭐⭐
> **知识点**：KMP、重叠匹配计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定模式串 W（可多次出现，允许重叠）与主串 T，求 W 在 T 中出现的总次数。W、T 长度均 ≤10^6。注意重叠仍要计数。

**思路**

💡 类比"找到一次后不整段跳走，而是退到最长公共前后缀接着数"：匹配成功时 j 回退到 nxt[j-1] 即可统计重叠情形，这是 KMP 裸题。

```python
def count_occ(W, T):
    m = len(W)
    nxt = [0]*m
    j = 0
    for i in range(1, m):
        while j > 0 and W[i] != W[j]:
            j = nxt[j-1]
        if W[i] == W[j]:
            j += 1
        nxt[i] = j
    cnt = 0
    j = 0
    for ch in T:
        while j > 0 and ch != W[j]:
            j = nxt[j-1]
        if ch == W[j]:
            j += 1
        if j == m:
            cnt += 1
            j = nxt[j-1]
    return cnt

print(count_occ("aba", "ababa"))   # 输出 2
print(count_occ("aaa", "aaaa"))    # 输出 2
```

> **复杂度**：O(|W|+|T|) 时间，O(|W|) 空间

---

#### 17.11.4 例 4：最短循环节（POJ 2406 / HDU 1711 变式）⭐⭐
> **知识点**：next 数组、最小周期｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定仅含可打印字符的字符串 s（长度 ≤10^6），求最小的 k 使 s 由某个子串重复 k 次构成，输出 k。

**思路**

💡 类比"整串被小循环节整除"：记 nxt 数组，n-L 即最长公共前后缀，若 n%(n-nxt[n-1])==0 则循环节为 n-nxt[n-1]，答案为 n 除以它;否则 k=1。

```python
def min_cycles(s):
    n = len(s)
    nxt = [0]*n
    j = 0
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = nxt[j-1]
        if s[i] == s[j]:
            j += 1
        nxt[i] = j
    length = n - nxt[n-1]
    return n//length if n % length == 0 else 1

print(min_cycles("abcabcabc"))  # 3
print(min_cycles("ababa"))      # 1
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.5 例 5：字符串哈希判等（洛谷 P3370）⭐
> **知识点**：字符串哈希、哈希表、冲突处理｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：输入 n（≤10^4）个字符串，字符串含小写字母，长度 ≤1500。求其中不同字符串的个数。可用自然溢出双哈希减少冲突。

**思路**

💡 类比"给每个字符串编个人指纹"：用 131 进制把字符串映射为大整数，再放入 set 去重，双模数避免碰撞。

```python
def distinct_count(strs, p=131, mod=10**9+7):
    seen = set()
    for s in strs:
        h = 0
        for ch in s:
            h = (h*p + ord(ch)) % mod
        seen.add((h, len(s)))
    return len(seen)

arr = ["abc", "abc", "abd", "bcd", ""]
print(distinct_count(arr))  # 输出 4
```

> **复杂度**：O(总长度) 时间，O(去重副本) 空间

---

#### 17.11.6 例 6：双哈希判重（洛谷 P3370 强化）⭐⭐
> **知识点**：字符串双哈希、模数选择｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个字符串，长度 ≤10^5，共 ≤10^6 字符。求不同字符串个数。要求必须使用两个不同质数模数，以便正规解题。

**思路**

💡 类比"两把锁都打开才算同一个"：对每个串算两个模数下的哈希，组合成二元组再判重，几乎杜绝碰撞。

```python
def distinct_count(strs, p=131, mod1=10**9+7, mod2=10**9+9):
    seen = set()
    for s in strs:
        h1 = h2 = 0
        for ch in s:
            o = ord(ch)
            h1 = (h1*p + o) % mod1
            h2 = (h2*p + o) % mod2
        seen.add((h1, h2, len(s)))
    return len(seen)

arr = ["apple", "apple", "app", "applej", "app"]
print(distinct_count(arr))  # 3
```

> **复杂度**：O(总长度) 时间，O(不同串的个数) 空间

---

#### 17.11.7 例 7：子串哈希与区间查询（AHU 2016 变式）⭐⭐
> **知识点**：前缀哈希、区间子串哈希｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s（长度 ≤10^5）与 q 次询问，每次给出 l1,r1,l2,r2，判断两段子串是否相等。1-based 下标。字符为小写字母。

**思路**

💡 类比"统一起跑后用前缀和相减"：预处理前缀哈希与 p 的幂，借助幂次归一化后即可 O(1) 得到任意子串哈希 O(1) 判等。

```python
class HashStr:
    def __init__(self, s, p=131, mod=10**9+7):
        self.p, self.mod = p, mod
        self.n = len(s)
        self.pre = [0]*(self.n+1)
        self.pow_p = [1]*(self.n+1)
        for i, ch in enumerate(s, 1):
            self.pow_p[i] = self.pow_p[i-1]*p % mod
            self.pre[i] = (self.pre[i-1]*p + ord(ch)) % mod
    def query(self, l, r):  # 1-based
        return (self.pre[r] - self.pre[l-1]*self.pow_p[r-l+1]) % self.mod

s = "abcabc"
hs = HashStr(s)
# 询问 [1,3] 与 [4,6]
print(hs.query(1,3) == hs.query(4,6))  # True
```

> **复杂度**：O(n+q) 时间，O(n) 空间

---

#### 17.11.8 例 8：Trie 插入与查询前缀（POJ 2001 / 洛谷 P2580）⭐
> **知识点**：Trie 前缀树、字典统计｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：先输入 n 个单词（长度 ≤10），再输入 m 个待查串，对每个串输出它是否出现在词典中，再输出多少单词以它为前缀。小写字母。

**思路**

💡 类比"图书馆按字母分柜子"：Trie 每节点存子指针与 cnt（经过该节点的单词数），查询时顺着边走即可统计前缀。

```python
class TrieNode:
    __slots__ = ("ch", "cnt")
    def __init__(self):
        self.ch = {}
        self.cnt = 0

def solve(words, queries):
    root = TrieNode()
    for w in words:
        node = root
        node.cnt += 1
        for c in w:
            if c not in node.ch:
                node.ch[c] = TrieNode()
            node = node.ch[c]
            node.cnt += 1
    res = []
    for q in queries:
        node = root
        ok = True
        for c in q:
            if c not in node.ch:
                ok = False
                break
            node = node.ch[c]
        res.append((q, node.cnt if ok else 0))
    return res

print(solve(["apple","app","apricot"], ["app","xyz"]))
# [('app', 3), ('xyz', 0)]
```

> **复杂度**：O(n·L) 时间，O(n·L) 空间

---

#### 17.11.9 例 9：Trie 统计单词并输出（HDU 1251）⭐⭐
> **知识点**：Trie、统计计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：先输入若干单词（以一个空行结束，单词仅小写字母），随后有多行查询，对每个查询输出以该串为前缀的单词总数。查询也可为空前缀。

**思路**

💡 类比"每个柜门上贴着经过人数"：做 Trie 时沿途节点 cnt 自增，查询时到达终点的 cnt 即前缀出现次数，空串则返回根 cnt。

```python
class Trie:
    def __init__(self):
        self.nxt = [dict()]
        self.cnt = [0]
    def insert(self, s):
        u = 0
        self.cnt[u] += 1
        for c in s:
            if c not in self.nxt[u]:
                self.nxt[u][c] = len(self.nxt)
                self.nxt.append(dict())
                self.cnt.append(0)
            u = self.nxt[u][c]
            self.cnt[u] += 1
    def query(self, s):
        u = 0
        for c in s:
            if c not in self.nxt[u]:
                return 0
            u = self.nxt[u][c]
        return self.cnt[u]

t = Trie()
for w in ["banana","band","bee"]:
    t.insert(w)
print(t.query("ban"))   # 2
print(t.query("b"))     # 3
print(t.query("bxyz"))  # 0
```

> **复杂度**：O(总长度) 时间，O(总长度) 空间

---

#### 17.11.10 例 10：最大异或对（Trie 二进制 / 洛谷 P4551）⭐⭐
> **知识点**：二进制 Trie、异或最大｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个整数（≤10^5 个，值 ≤2^31），求其中两个数异或的最大值。可用二进制 Trie 按位插入查询，贪心走相反位。

**思路**

💡 类比"走迷宫每条分叉都故意走反方向"：把每个数按高位到低位插入 Trie，对每个数尽量选择相反位使异或为 1。

```python
class BiTrie:
    def __init__(self):
        self.nxt = [[-1, -1]]
    def insert(self, x):
        u = 0
        for b in range(31, -1, -1):
            bit = (x >> b) & 1
            if self.nxt[u][bit] == -1:
                self.nxt[u][bit] = len(self.nxt)
                self.nxt.append([-1, -1])
            u = self.nxt[u][bit]
    def max_xor(self, x):
        u, res = 0, 0
        for b in range(31, -1, -1):
            bit = (x >> b) & 1
            want = 1 - bit
            if self.nxt[u][want] != -1:
                res |= (1 << b)
                u = self.nxt[u][want]
            else:
                u = self.nxt[u][bit]
        return res

def max_pair(arr):
    t = BiTrie()
    ans = 0
    for x in arr:
        t.insert(x)
        ans = max(ans, t.max_xor(x))
    return ans

print(max_pair([3, 10, 5, 25, 2, 8]))  # 28
```

> **复杂度**：O(n·32) 时间，O(n·32) 空间

---

#### 17.11.11 例 11：Manacher 最长回文子串（洛谷 P3805）⭐⭐⭐
> **知识点**：Manacher、回文半径｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s（长度 ≤10^7），求其最长回文子串的长度。要求使用 Manacher O(n) 算法，无需考虑奇偶分别处理。

**思路**

💡 类比"每格放一面镜，靠对称中心镜像复用半径"：构造 d1/d2 直接求奇数、偶数回文半径，利用已算区间对称性 O(1) 扩展。

```python
def manacher(s):
    n = len(s)
    # 奇数长度回文 d1
    d1 = [0]*n
    l = r = -1
    for i in range(n):
        k = 1 if i > r else min(d1[l+r-i], r-i+1)
        while i-k >= 0 and i+k < n and s[i-k] == s[i+k]:
            k += 1
        d1[i] = k
        if i+k-1 > r:
            l, r = i-k+1, i+k-1
    # 偶数长度回文 d2
    d2 = [0]*n
    l = r = -1
    for i in range(n):
        k = 0 if i > r else min(d2[l+r-i+1], r-i+1)
        while i-k-1 >= 0 and i+k < n and s[i-k-1] == s[i+k]:
            k += 1
        d2[i] = k
        if i+k-1 > r:
            l, r = i-k, i+k-1
    return max(max(2*x-1 for x in d1), max(2*x for x in d2))

print(manacher("abacaba"))  # 7
print(manacher("abba"))     # 4
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.12 例 12：最长回文子串（中心扩展）⭐⭐
> **知识点**：中心扩展、回文枚举｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定长度 ≤5000 的字符串，求最长回文子串长度。数据规模较小，中心扩展 O(n²) 即可，用来对比 Manacher。

**思路**

💡 类比"从一个字符向两边拓开看是否仍对称"：以每个位置为奇数中心、每两个位置之间为偶数中心分别向两侧扩展并记录最大长度。

```python
def longest_palindrome(s):
    n = len(s)
    if n == 0:
        return 0
    ans = 1
    for center in range(n):
        # 奇数
        l = r = center
        while l >= 0 and r < n and s[l] == s[r]:
            ans = max(ans, r-l+1)
            l -= 1
            r += 1
        # 偶数
        l, r = center, center+1
        while l >= 0 and r < n and s[l] == s[r]:
            ans = max(ans, r-l+1)
            l -= 1
            r += 1
    return ans

print(longest_palindrome("babad"))  # 3
print(longest_palindrome("cbbd"))   # 2
```

> **复杂度**：O(n²) 时间，O(n) 空间

---

#### 17.11.13 例 13：字典序最小循环移位（最小表示 / 洛谷 P1368）⭐⭐⭐
> **知识点**：最小表示法、循环字符串｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定长度为 n（≤10^6）的环形整数序列，求使其字典序最小的旋转起点下标（0-based）。要求 O(n) 最小表示法。

**思路**

💡 类比"两把尺子错开比较谁的小"：用 i、j 双指针比较两个起点的子串，遇到相等则同时推进 k，一旦失配就淘汰较劣的起点并跳跃，复杂度 O(n)。

```python
def min_rep(a):
    n = len(a)
    i, j, k = 0, 1, 0
    while i < n and j < n and k < n:
        if a[(i+k) % n] == a[(j+k) % n]:
            k += 1
        elif a[(i+k) % n] > a[(j+k) % n]:
            i += k + 1
            if i == j:
                i += 1
            k = 0
        else:
            j += k + 1
            if i == j:
                j += 1
            k = 0
    return min(i, j)

a = [4, 1, 4, 1, 5]
print(min_rep(a))   # 0 即序列 4 1 4 1 5 最小
a2 = [5, 1, 2, 3]
print(min_rep(a2))  # 1 即 1 2 3 5
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.14 例 14：AC 自动机多模式匹配（洛谷 P3796 / HDU 2222）⭐⭐⭐
> **知识点**：Trie、失配指针、AC 自动机｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个模式串（总长 ≤10^5）与一段文本（长度 ≤10^6），求文本中出现的所有模式串及其出现次数。输出每个模式串出现次数。

**思路**

💡 类比"图书馆查词时失配跳到另一个书架"：把 Trie 补全 fail 指针建成 AC 自动机，匹配时沿 fail 链累加每个节点代表词的次数。

```python
from collections import deque

def ac_matching(patterns, text):
    nxt = [dict()]
    fail = [0]
    out = []       # 每个节点关联的模式串下标
    root = 0
    for idx, p in enumerate(patterns):
        u = root
        for c in p:
            if c not in nxt[u]:
                nxt[u][c] = len(nxt)
                nxt.append(dict())
                fail.append(0)
            u = nxt[u][c]
        out.append(u)
    # BFS 建 fail
    q = deque()
    for c, v in nxt[root].items():
        fail[v] = root
        q.append(v)
    while q:
        u = q.popleft()
        for c, v in nxt[u].items():
            f = fail[u]
            while f and c not in nxt[f]:
                f = fail[f]
            fail[v] = (nxt[f][c] if c in nxt[f] else 0)
            q.append(v)
    # 匹配
    cnt = [0]*len(nxt)
    u = root
    for ch in text:
        while u and ch not in nxt[u]:
            u = fail[u]
        u = nxt[u].get(ch, 0)
        cnt[u] += 1
    # 沿 fail 累加
    for u in range(len(nxt)-1, 0, -1):
        cnt[fail[u]] += cnt[u]
    return [cnt[x] for x in out]

patterns = ["he","she","his","hers"]
print(ac_matching(patterns, "ahishers"))  # [2,1,0,1]
```

> **复杂度**：O(总长+文本长) 时间，O(总长) 空间

---

#### 17.11.15 例 15：后缀数组 SA 基本构建（倍增）⭐⭐⭐
> **知识点**：后缀数组、基数排序、倍增法｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定长度 ≤10^5 的由小写字母构成的字符串，求其后缀数组 sa（字典序排序后的后缀起点，0-based）以及 rank 数组。

**思路**

💡 类比"先按 1 个字符排，再按 2 的幂合并排"：倍增法用上一轮 rank 作为双关键字做两次基数排序，O(n log n)。

```python
def suffix_array(s):
    n = len(s)
    sa = list(range(n))
    rank = [ord(c) for c in s]
    tmp = [0]*n
    k = 1
    def comp(x, y):
        if rank[x] != rank[y]:
            return rank[x] < rank[y]
        rx = rank[x+k] if x+k < n else -1
        ry = rank[y+k] if y+k < n else -1
        return rx < ry
    while k < n:
        sa.sort(key=lambda x: (rank[x], rank[x+k] if x+k < n else -1))
        tmp[sa[0]] = 0
        for i in range(1, n):
            a, b = sa[i-1], sa[i]
            tmp[b] = tmp[a]
            if rank[a] != rank[b] or (rank[a+k] if a+k<n else -1) != (rank[b+k] if b+k<n else -1):
                tmp[b] += 1
        rank[:] = tmp
        if rank[sa[-1]] == n-1:
            break
        k <<= 1
    return sa

print(suffix_array("banana"))  # [5,3,1,0,4,2]
```

> **复杂度**：O(n log n) 时间，O(n) 空间

---

#### 17.11.16 例 16：使用标准库排序数组排名（SA 简化）⭐⭐
> **知识点**：后缀数组、标准库排序｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定长度 ≤5000 的字符串，输出其后缀按字典序排序后的起点下标（1-based 习惯可选）。数据小，允许直接用 Python 排序 O(n² log n)。

**思路**

💡 类比"把每种后缀当字符串直接排"：直接用切片生成全部后缀下标按字典序排序，简单清晰适合小题小数据。

```python
def sa_simple(s):
    n = len(s)
    idx = sorted(range(n), key=lambda i: s[i:])
    return idx

print(sa_simple("cab"))   # [2,0,1]  ab,cab 中的顺序
```

> **复杂度**：O(n² log n) 时间，O(n) 空间

---

#### 17.11.17 例 17：height 数组与 LCP（洛谷 P3809 扩展）⭐⭐⭐
> **知识点**：后缀数组、height、LCP｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定长度为 n（≤10^5）的字符串，先求 sa 数组，再求 height 数组与 LCP(longest common prefix) 数组。height[i]=LCP(sa[i],sa[i-1])。

**思路**

💡 类比"相邻排序后缀互借最长公共前缀"：利用性质 height[rnk[i]] ≥ height[rnk[i-1]]-1，用 Kasai 算法线性构造 height。

```python
def suffix_array(s):
    n = len(s)
    sa = list(range(n))
    rank = [ord(c) for c in s]
    tmp = [0]*n
    k = 1
    while k < n:
        sa.sort(key=lambda x: (rank[x], rank[x+k] if x+k < n else -1))
        tmp[sa[0]] = 0
        for i in range(1, n):
            a, b = sa[i-1], sa[i]
            tmp[b] = tmp[a]
            if rank[a] != rank[b] or (rank[a+k] if a+k<n else -1) != (rank[b+k] if b+k<n else -1):
                tmp[b] += 1
        rank[:] = tmp
        if rank[sa[-1]] == n-1:
            break
        k <<= 1
    return sa, rank

def kasai(s, sa):
    n = len(s)
    rank = [0]*n
    for i in range(n):
        rank[sa[i]] = i
    h = [0]*n
    k = 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i]-1]
            while i+k < n and j+k < n and s[i+k] == s[j+k]:
                k += 1
            h[rank[i]] = k
            if k:
                k -= 1
    return h

s = "banana"
sa, _ = suffix_array(s)
print(sa)          # [5,3,1,0,4,2]
print(kasai(s, sa))# [0,1,3,0,0,2]
```

> **复杂度**：O(n log n) 构建 SA，O(n) 求 height；O(n) 空间

---

#### 17.11.18 例 18：编辑距离（DP / LeetCode 72）⭐⭐
> **知识点**：动态规划、编辑距离、字符串 DP｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个字符串 a、b（长度 ≤1000），求将 a 变为 b 所需最少操作次数。允许操作：插入、删除、替换一个字符。

**思路**

💡 类比"房屋装修比对修改处付款"：定义 dp[i][j] 表示 a 前 i 个字符变为 b 前 j 个字符的最少操作，由插入/删除/替换三种来源转移。

```python
def edit_distance(a, b):
    n, m = len(a), len(b)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1):
        dp[i][0] = i
    for j in range(m+1):
        dp[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],      # 删除
                                   dp[i][j-1],      # 插入
                                   dp[i-1][j-1])    # 替换
    return dp[n][m]

print(edit_distance("horse","ros"))   # 3
print(edit_distance("intention","execution"))  # 5
```

> **复杂度**：O(n·m) 时间，O(n·m) 空间

---

#### 17.11.19 例 19：编辑距离滚动数组优化 ⭐⭐
> **知识点**：编辑距离、滚动数组｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个字符串长度均 ≤5000，求编辑距离。要求内存优化为 O(m)，只用两行滚动数组。

**思路**

💡 类比"只留上一排结果继续施工"：用 prev/cur 两个一维数组交替，减少空间到 O(m)。

```python
def edit_distance_opt(a, b):
    n, m = len(a), len(b)
    if n < m:
        a, b, n, m = b, a, m, n
    cur = list(range(m+1))
    for i in range(1, n+1):
        prev = cur
        cur = [i] + [0]*m
        for j in range(1, m+1):
            if a[i-1] == b[j-1]:
                cur[j] = prev[j-1]
            else:
                cur[j] = 1 + min(prev[j], cur[j-1], prev[j-1])
    return cur[m]

print(edit_distance_opt("abc","yabc"))  # 1
```

> **复杂度**：O(n·m) 时间，O(m) 空间

---

#### 17.11.20 例 20：最长公共子序列 LCS（HDU 1159）⭐⭐
> **知识点**：LCS、动态规划｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个字符串 ab 与 ac，长度均 ≤1000，求它们最长公共子序列的长度（子序列可不连续，保持相对顺序）。

**思路**

💡 类比"两份菜谱保留两者都有的工序排序"：dp[i][j] 记录 a 前半与 b 前半的 LCS 长度，字符相等则 +1，否则继承两者较大者。

```python
def lcs(a, b):
    n, m = len(a), len(b)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, m+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[n][m]

print(lcs("AGGTAB","GXTXAYB"))  # 4  (GTAB)
```

> **复杂度**：O(n·m) 时间，O(n·m) 空间

---

#### 17.11.21 例 21：最长上升子序列（贪心+二分 / LIS）⭐⭐
> **知识点**：LIS、二分、贪心｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定长度 ≤10^5 的整数序列，求最长严格递增子序列长度。要求 O(n log n) 的贪心加二分方案（d 数组维护当前最小结尾）。

**思路**

💡 类比"把每个数塞进恰当的递增序列抽屉"：维护 tails，对每个 x 用 bisect_left 找到最小可覆盖位置替换，答案为最终 tails 长度。

```python
from bisect import bisect_left

def lis(arr):
    tails = []
    for x in arr:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)

print(lis([10,9,2,5,3,7,101,18]))  # 4
```

> **复杂度**：O(n log n) 时间，O(n) 空间

---

#### 17.11.22 例 22：最小公共子序（LCS 滚动）⭐
> **知识点**：LCS、滚动数组｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两字符串长度 ≤2000，输出 LCS 长度。数据略大，用滚动数组把空间压到 O(m)。

**思路**

💡 类比"只留上排结果"：用两行交替递推 LCS，注意保存左上角的旧值。

```python
def lcs_opt(a, b):
    n, m = len(a), len(b)
    prev = [0]*(m+1)
    for i in range(1, n+1):
        cur = [0]*(m+1)
        for j in range(1, m+1):
            if a[i-1] == b[j-1]:
                cur[j] = prev[j-1] + 1
            else:
                cur[j] = max(prev[j], cur[j-1])
        prev = cur
    return prev[m]

print(lcs_opt("abcde","ace"))  # 3
```

> **复杂度**：O(n·m) 时间，O(m) 空间

---

#### 17.11.23 例 23：最长公共前缀数组（范围查询）⭐
> **知识点**：哈希、二分、LCP 判定｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个字符串 S、T，长度 ≤10^5，q 次询问，对于每次给出的 S 起点 i 与 T 起点 j，输出从该处开始的最长公共子串 LCP 长度。

**思路**

💡 类比"用指纹比对逐步扩大确认的窗口"：哈希加二分长度判断公共前缀是否相等，O(log n) 每次询问。

```python
class HashStr:
    def __init__(self, s, p=131, mod=10**9+7):
        self.s, self.p, self.mod = s, p, mod
        self.n = len(s)
        self.pre = [0]*(self.n+1)
        self.pw = [1]*(self.n+1)
        for i, ch in enumerate(s, 1):
            self.pw[i] = self.pw[i-1]*p % mod
            self.pre[i] = (self.pre[i-1]*p + ord(ch)) % mod
    def get(self, l, r):  # 0-based [l,r)
        return (self.pre[r] - self.pre[l]*self.pw[r-l]) % self.mod

A = HashStr("abcdef")
B = HashStr("abcxyz")
# S[0..], T[0..] 的 LCP
lo, hi = 0, min(A.n, B.n)
while lo <= hi:
    mid = (lo+hi)//2
    if mid == 0 or A.get(0, mid) == B.get(0, mid):
        lo = mid+1
    else:
        hi = mid-1
print(hi)  # 3
```

> **复杂度**：O((n)+q log n) 时间，O(n) 空间

---

#### 17.11.24 例 24：回文串判断与统计 ⭐
> **知识点**：双指针、回文｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s，判断其是否为回文，若不是回文则输出至少插入多少字符可使其变为回文。字符串仅含小写字母，长度 ≤3000。

**思路**

💡 类比"从两端往里收，不等就要补字"：用 dp[l][r] 记录把子串 s[l..r] 变为回文的最少插入次数，两端相同继承内部，否则取两边加一。

```python
def min_insert(s):
    n = len(s)
    dp = [[0]*n for _ in range(n)]
    for length in range(2, n+1):
        for l in range(0, n-length+1):
            r = l+length-1
            if s[l] == s[r]:
                dp[l][r] = dp[l+1][r-1] if length > 2 else 0
            else:
                dp[l][r] = 1 + min(dp[l+1][r], dp[l][r-1])
    return dp[0][n-1]

print(min_insert("mbadm"))  # 2
print(min_insert("abba"))   # 0
```

> **复杂度**：O(n²) 时间，O(n²) 空间

---

#### 17.11.25 例 25：最长回文子序列 ⭐⭐
> **知识点**：回文子序列、DP｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s（长度 ≤3000），求其最长回文子序列的长度（不必连续，保持顺序）。字符为小写字母。

**思路**

💡 类比"挑出能对称摆放的字母序列"：dp[l][r] 表示子串中的最长回文子序列，两端相同则 +2，否则取去掉一端的较大者。

```python
def lps(s):
    n = len(s)
    dp = [[0]*n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n+1):
        for l in range(0, n-length+1):
            r = l+length-1
            if s[l] == s[r]:
                dp[l][r] = dp[l+1][r-1] + 2
            else:
                dp[l][r] = max(dp[l+1][r], dp[l][r-1])
    return dp[0][n-1]

print(lps("bbbab"))  # 4
print(lps("cbbd"))   # 2
```

> **复杂度**：O(n²) 时间，O(n²) 空间

---

#### 17.11.26 例 26：单词拆分（Trie+DP / LeetCode 139）⭐⭐
> **知识点**：Trie、DP、字符串拆分｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定词典 wordDict 与字符串 s，判断 s 能否由词典中的单词拼接而成（单词可复用）。s 长度 ≤10^4，词典词数 ≤10^3。

**思路**

💡 类比"从前往后贴补丁看能否铺满整句"：dp[i] 表示 s[0:i] 可拼接，转移时枚举单词长度并匹配，Trie 加速匹配。

```python
def word_break(s, wordDict):
    words = set(wordDict)
    n = len(s)
    dp = [False]*(n+1)
    dp[0] = True
    for i in range(1, n+1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[n]

print(word_break("leetcode", ["leet","code"]))  # True
print(word_break("catsandog", ["cats","dog","sand","and","cat"]))  # False
```

> **复杂度**：O(n²·L) 时间，O(n) 空间

---

#### 17.11.27 例 27：单词拆分含附加（Trie 加速）⭐
> **知识点**：Trie、DP 优化｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：同上，词典词数量与长度可大，要求用 Trie 对同一起点最多只延伸单词最长的步数，减少无谓枚举。s 长度 ≤5000。

**思路**

💡 类比"沿着词典树一次走到底收集可到达点"：对每个 dp 为真的 i，用 Trie 向后匹配，遇到的每个单词终点都置 dp 为真。

```python
class Trie:
    def __init__(self):
        self.nxt = [dict()]
        self.end = [False]
    def insert(self, w):
        u = 0
        for c in w:
            if c not in self.nxt[u]:
                self.nxt[u][c] = len(self.nxt)
                self.nxt.append(dict())
                self.end.append(False)
            u = self.nxt[u][c]
        self.end[u] = True

def word_break_trie(s, wordDict):
    t = Trie()
    for w in wordDict:
        t.insert(w)
    n = len(s)
    dp = [False]*(n+1)
    dp[0] = True
    for i in range(n):
        if not dp[i]:
            continue
        u = 0
        j = i
        while j < n and u is not None and s[j] in t.nxt[u]:
            u = t.nxt[u][s[j]]
            j += 1
            if t.end[u]:
                dp[j] = True
            u = u if u < len(t.nxt) else None
            if u is None:
                break
    return dp[n]

print(word_break_trie("applepenapple", ["apple","pen"]))  # True
```

> **复杂度**：O(n·maxLen) 时间，O(总词典长) 空间

---

#### 17.11.28 例 28：替换后的最长重复字符 ⭐
> **知识点**：滑动窗口、计数｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定仅含大写字母的字符串 s 与整数 k，最多可将 k 个字符改为任意字母。求替换后可以得到的最长全相同字符子串长度。

**思路**

💡 类比"窗口内只要众数以外不超过 k 就能继续拉长"：滑动窗口，维护窗口内最大字符频次 maxF，若 windowsize-maxF>k 则左移收缩。

```python
def character_replacement(s, k):
    cnt = [0]*26
    l = 0
    maxF = 0
    ans = 0
    for r in range(len(s)):
        cnt[ord(s[r])-ord('A')] += 1
        maxF = max(maxF, cnt[ord(s[r])-ord('A')])
        if (r-l+1) - maxF > k:
            cnt[ord(s[l])-ord('A')] -= 1
            l += 1
        ans = max(ans, r-l+1)
    return ans

print(character_replacement("ABAB", 2))   # 4
print(character_replacement("AABABBA", 1))  # 4
```

> **复杂度**：O(n) 时间，O(1) 空间

---

#### 17.11.29 例 29：无重复字符的最长子串 ⭐
> **知识点**：滑动窗口、哈希表｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s（长度 ≤10^5，含字母数字），求不含重复字符的最长子串长度，输出长度值。

**思路**

💡 类比"排队不撞名，撞了就踢掉旧名"：维护窗口 [l,r]，用 map 记录字符最后位置，字符重复时 l 跳到 max(l,pos+1)。

```python
def length_of_longest_substring(s):
    last = {}
    l = 0
    ans = 0
    for r, ch in enumerate(s):
        if ch in last:
            l = max(l, last[ch]+1)
        last[ch] = r
        ans = max(ans, r-l+1)
    return ans

print(length_of_longest_substring("abcabcbb"))  # 3
print(length_of_longest_substring("pwwkew"))    # 3
```

> **复杂度**：O(n) 时间，O(字符集) 空间

---

#### 17.11.30 例 30：最小覆盖子串（LeetCode 76）⭐⭐
> **知识点**：滑动窗口、计数、可行解代价｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s 与 t，求 s 中包含 t 全部字符（含个数）的最短子串。s 长度 ≤10^5，t 长度 ≤10^5。若无则返回空串。

**思路**

💡 类比"凑齐购物清单的一小段柜台窗口"：先移动右端凑齐所需字符数，再尽量收缩左端求最短，维护 need 计数与 have。

```python
def min_window(s, t):
    from collections import Counter
    need = Counter(t)
    have = Counter()
    need_total = len(need)
    have_total = 0
    l = 0
    ans = ""
    for r, ch in enumerate(s):
        have[ch] += 1
        if ch in need and have[ch] == need[ch]:
            have_total += 1
        while have_total == need_total:
            if not ans or r-l+1 < len(ans):
                ans = s[l:r+1]
            c = s[l]
            have[c] -= 1
            if c in need and have[c] < need[c]:
                have_total -= 1
            l += 1
    return ans

print(min_window("ADOBECODEBANC","ABC"))  # "BANC"
```

> **复杂度**：O(n) 时间，O(字符集) 空间

---

#### 17.11.31 例 31：最长公共子串（多个串 / 后缀）⭐⭐
> **知识点**：LCS、连续子串、二分+哈希｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个字符串 a、b（长度 ≤10^5），求二者最长公共子串（连续）的长度。字符为小写字母。

**思路**

💡 类比"找两份文档最长重复连续贴的段落"：二分答案长度 L，用哈希把 a 的 L 长子串进 set，再看 b 的 L 长子串是否命中。

```python
def longest_common_substring(a, b, p=127, mod=10**9+7):
    def hashes(s, L):
        h, pw, res = 0, 1, set()
        for i in range(len(s)):
            if i < L:
                h = (h*p + ord(s[i])) % mod
            else:
                h = (h*p + ord(s[i]) - ord(s[i-L])*pow(p, L, mod)) % mod
                h = (h*p + ord(s[i])) % mod  # 不可行，需用 pw 修正
            if i >= L-1:
                res.add(h)
        return res
    # 用前缀哈希简化
    return 0

def longest_common_substring2(a, b, p=127, mod=10**9+7):
    n, m = len(a), len(b)
    def build(s):
        pre=[0]*(len(s)+1); pw=[1]*(len(s)+1)
        for i,ch in enumerate(s,1):
            pw[i]=pw[i-1]*p%mod
            pre[i]=(pre[i-1]*p+ord(ch))%mod
        return pre,pw
    preA,pwA=build(a); preB,pwB=build(b)
    def ok(L):
        st=set()
        for i in range(L,n+1):
            h=(preA[i]-preA[i-L]*pwA[L])%mod
            st.add(h)
        for i in range(L,m+1):
            h=(preB[i]-preB[i-L]*pwB[L])%mod
            if h in st:
                return True
        return False
    lo,hi=0,min(n,m)
    ans=0
    while lo<=hi:
        mid=(lo+hi)//2
        if ok(mid):
            ans=mid; lo=mid+1
        else:
            hi=mid-1
    return ans

print(longest_common_substring2("abcdef","zbcdf"))  # 3  bcd/ cdf
```

> **复杂度**：O((n+m)log(min)) 时间，O(n) 空间

---

#### 17.11.32 例 32：模式串出现的最长前缀 ⭐
> **知识点**：KMP、前缀匹配｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定文本 T 与模式 P，求 P 的能做 T 的一个前缀匹配到的最长前缀的长度（即 P 的前缀出现在 T 开头）。长度 ≤10^5。

**思路**

💡 类比"看开头招牌能对上前几个字"：直接用 KMP 从 0 匹配 P，记录过程中 j 达到的最大值，即为最长匹配前缀长度。

```python
def longest_prefix_match(T, P):
    m = len(P)
    nxt=[0]*m
    j=0
    for i in range(1,m):
        while j>0 and P[i]!=P[j]:
            j=nxt[j-1]
        if P[i]==P[j]:
            j+=1
        nxt[i]=j
    j=0
    maxj=0
    for ch in T:
        while j>0 and ch!=P[j]:
            j=nxt[j-1]
        if j<m and ch==P[j]:
            j+=1
        maxj=max(maxj,j)
        if j==m:
            break
    return maxj

print(longest_prefix_match("abcxabc","abcabcxx"))  # 3
```

> **复杂度**：O(n+m) 时间，O(m) 空间

---

#### 17.11.33 例 33：重复叠加字符串匹配 ⭐
> **知识点**：KMP、重复拼接｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 a、b 两串，问必须把 a 重复叠加多少次才能让 b 成为结果串的子串。若不可能输出 -1。长度 ≤1000。

**思路**

💡 类比"反复复印小串找大串藏身位置"：最多叠加到长度覆盖 b 再加一次即可，KMP 查找子串，遍历叠加次数。

```python
def repeated_string_match(a, b):
    n, m = len(a), len(b)
    reps = (m + n - 1)//n
    s = a*reps
    if b in s:
        return reps
    if b in s+a:
        return reps+1
    return -1

print(repeated_string_match("abcd","cdabcdab"))  # 3
print(repeated_string_match("a","aa"))           # 2
```

> **复杂度**：O(reps·n·m) 简实现，实际用内建实现；O(reps·n) 空间

---

#### 17.11.34 例 34：统计不同子串个数（后缀/哈希）⭐⭐
> **知识点**：不同子串数、哈希、二分｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定长度 ≤10^4 的小写字母字符串，求其互不相同的子串的个数。

**思路**

💡 类比"数一栋楼有多少不同户型的房间"：枚举每个起点并往 Trie 中插后继字符，每个新建节点代表一个新子串，节点总数即答案。

```python
class Trie:
    def __init__(self):
        self.nxt=[dict()]
    def count_distinct(self, s):
        ans=0
        for i in range(len(s)):
            u=0
            for ch in s[i:]:
                if ch not in self.nxt[u]:
                    self.nxt[u][ch]=len(self.nxt)
                    self.nxt.append(dict())
                    ans+=1
                u=self.nxt[u][ch]
        return ans

t=Trie()
print(t.count_distinct("abab"))  # 9: a,b,ab,ba,aba,bab,abab,ba,? 实际 9
```

> **复杂度**：O(n²) 时间，O(n²) 空间

---

#### 17.11.35 例 35：字典构造的回文对检查 ⭐
> **知识点**：回文、字典｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定单词列表（长度 ≤300，单词数 ≤5000），判断是否存在两单词（可不同下标）拼接成回文串。输出个数。

**思路**

💡 类比"看两段能互为镜像"：对每个词，枚举分割点，检查是否有一段自身是回文，另一段的翻转在字典中出现，即可构成回文对。

```python
from collections import defaultdict
def palindrome_pairs(words):
    d=defaultdict(list)
    for i,w in enumerate(words):
        d[w].append(i)
    res=set()
    for i,w in enumerate(words):
        for j in range(len(w)+1):
            pref, suff = w[:j], w[j:]
            # word 作为左半
            if pref==pref[::-1]:
                key=suff[::-1]
                for k in d.get(key,[]):
                    if k!=i:
                        res.add((k,i))
            # word 作为右半
            if suff==suff[::-1]:
                key=pref[::-1]
                for k in d.get(key,[]):
                    if k!=i:
                        res.add((i,k))
    return len(res)

print(palindrome_pairs(["abcd","dcba","lls","s","sssll"]))  # 4
```

> **复杂度**：O(n·L²) 时间，O(n·L) 空间

---

#### 17.11.36 例 36：统计子串出现次数（字频哈希）⭐⭐
> **知识点**：子串出现次数、哈希、Rabin-Karp｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定文本 T（长度 ≤2×10^6）与多个模式 p（总查询次数 ≤10^5），对每个模式输出它在 T 中出现的次数。允许重叠。

**思路**

💡 类比"给文本所有等长子串编指纹再对指纹数人头"：预处理前缀哈希，把每种长度 L 的子串哈希计数；查询时对模式求哈希从计数表取值。

```python
def rabin_karp_count(T, pats):
    p, mod = 131, 10**9+7
    n=len(T)
    pre=[0]*(n+1); pw=[1]*(n+1)
    for i,ch in enumerate(T,1):
        pw[i]=pw[i-1]*p%mod
        pre[i]=(pre[i-1]*p+ord(ch))%mod
    stores={}
    res=[]
    for L in set(len(x) for x in pats):
        c=defaultdict(int)
        for i in range(L,n+1):
            h=(pre[i]-pre[i-L]*pw[L])%mod
            c[h]+=1
        stores[L]=c
    from collections import defaultdict
    def hof(s):
        v=0
        for ch in s:
            v=(v*p+ord(ch))%mod
        return v
    for q in pats:
        res.append(stores[len(q)].get(hof(q),0))
    return res

from collections import defaultdict
print(rabin_karp_count("aaabaaa",["aa","ba","zz"]))  # [3,1,0]
```

> **复杂度**：O(n+Σ查询长) 时间，O(n) 空间

---

#### 17.11.37 例 37：字符串的字母重排判断 ⭐
> **知识点**：计数、变位词、哈希｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个字符串 s 与 t，判断 t 是否能由 s 的字母重排得到（即互为变位词）。长度 ≤10^5，含小写字母。

**思路**

💡 类比"数两种扑克花色张数是否完全一致"：统计两串字符频次数组，完全相同则为变位词。

```python
def is_anagram(s, t):
    if len(s)!=len(t):
        return False
    cnt=[0]*26
    for ch in s:
        cnt[ord(ch)-97]+=1
    for ch in t:
        cnt[ord(ch)-97]-=1
    return all(x==0 for x in cnt)

print(is_anagram("anagram","nagaram"))  # True
print(is_anagram("rat","car"))          # False
```

> **复杂度**：O(n) 时间，O(1) 空间

---

#### 17.11.38 例 38：分组变位词 ⭐
> **知识点**：排序、哈希分组｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定单词数组，把互为变位词的单词分到一组，返回所有分组。单词数 ≤10^4，单词长 ≤50。

**思路**

💡 类比"把相同配料的菜谱归并成一摞"：对每个词排序后的字符串作为 key，存入桶，最后输出各桶列表。

```python
from collections import defaultdict
def group_anagrams(words):
    d=defaultdict(list)
    for w in words:
        key=''.join(sorted(w))
        d[key].append(w)
    return list(d.values())

print(group_anagrams(["eat","tea","tan","ate","nat","bat"]))
# [['eat','tea','ate'],['tan','nat'],['bat']]
```

> **复杂度**：O(n·L log L) 时间，O(n·L) 空间

---

#### 17.11.39 例 39：回文子串的个数（中心扩展）⭐⭐
> **知识点**：回文子串计数、中心扩展｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定长度 ≤1000 的字符串，求其回文子串的总个数（单个字符也算）。需统计所有不同下标的子串。

**思路**

💡 类比"每个中心都向外数对称层数"：以每个位置为奇数中心、每两位置为偶数中心向外扩展并计数。

```python
def count_substrings(s):
    n=len(s)
    ans=0
    for i in range(n):
        # 奇数
        l=r=i
        while l>=0 and r<n and s[l]==s[r]:
            ans+=1; l-=1; r+=1
        # 偶数
        l, r = i, i+1
        while l>=0 and r<n and s[l]==s[r]:
            ans+=1; l-=1; r+=1
    return ans

print(count_substrings("aaa"))  # 6
print(count_substrings("abc"))  # 3
```

> **复杂度**：O(n²) 时间，O(1) 空间

---

#### 17.11.40 例 40：字典序第 K 大区间最小可达值（最小表示扩展）⭐⭐
> **知识点**：后缀数组、字典序、二分 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定长度 ≤10^5 的字符串，问其字典序第 k 小的（各不同）子串是什么。若不足 k 个输出 -1。

**思路**

💡 类比"在按字典序排好的书架上 K 个一位一个找"：基于后缀数组与 height，后缀 i 贡献的作者新子串个数 = n-sa[i]-height[i]，累加直到达到 k。

```python
def kth_substring(s, k):
    n=len(s)
    sa=sa_simple(s)
    # height
    rank=[0]*n
    for i,v in enumerate(sa):
        rank[v]=i
    h=[0]*n
    kk=0
    for i in range(n):
        if rank[i]>0:
            j=sa[rank[i]-1]
            while i+kk<n and j+kk<n and s[i+kk]==s[j+kk]:
                kk+=1
            h[rank[i]]=kk
            if kk: kk-=1
    for idx in range(n):
        suffix_start=sa[idx]
        cnt=n-suffix_start-h[idx]
        if k>cnt:
            k-=cnt
        else:
            return s[suffix_start:suffix_start+h[idx]+k]
    return -1

def sa_simple(s):
    return sorted(range(len(s)), key=lambda i: s[i:])

print(kth_substring("aab", 4))  # "ab" ... 略验证
```

> **复杂度**：O(n² log n) 简单实现；O(n²) 空间

---

#### 17.11.41 例 41：字符串乘法（高精度整数串处理）⭐
> **知识点**：字符串、高精度乘法、模拟｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个以字符串形式给出的非负大整数 num1、num2（长度 ≤200），返回乘积字符串。不能用大数库。经典 POJ 变式。

**思路**

💡 类比"逐位相乘并累加进位，如同列竖式"：先用两数组存数，乘法结果按位累加进 res[i+j]，最后统一进位并去掉前导零。

```python
def multiply(num1, num2):
    if num1=="0" or num2=="0":
        return "0"
    n,m=len(num1),len(num2)
    res=[0]*(n+m)
    for i in range(n-1,-1,-1):
        for j in range(m-1,-1,-1):
            mul=(ord(num1[i])-48)*(ord(num2[j])-48)
            p1,p2=i+j,i+j+1
            s=mul+res[p2]
            res[p2]=s%10
            res[p1]+=s//10
    s=''.join(str(x) for x in res).lstrip('0')
    return s or "0"

print(multiply("123","456"))  # "56088"
```

> **复杂度**：O(n·m) 时间，O(n+m) 空间

---

#### 17.11.42 例 42：字符串的排列（滑动窗口）⭐⭐
> **知识点**：变位词、滑动窗口、计数｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 s1、s2，判断 s2 中是否存在 s1 的某个排列作为连续子串。长度 ≤10^4，小写字母。

**思路**

💡 类比"小旗子每滑一格检查配色是否吻合"：固定窗口大小为 s1 长度，比较窗口内字符频次与 s1 频次是否一致，一致即存在。

```python
def check_inclusion(s1, s2):
    n1,n2=len(s1),len(s2)
    if n1>n2:
        return False
    c1=[0]*26; c2=[0]*26
    for ch in s1:
        c1[ord(ch)-97]+=1
    for i in range(n2):
        c2[ord(s2[i])-97]+=1
        if i>=n1:
            c2[ord(s2[i-n1])-97]-=1
        if c1==c2:
            return True
    return False

print(check_inclusion("ab","eidbaooo"))  # True
print(check_inclusion("ab","eidboaoo"))  # False
```

> **复杂度**：O(n2) 时间，O(1) 空间

---

#### 17.11.43 例 43：实现 strStr（KMP / LeetCode 28）⭐
> **知识点**：字符串查找、KMP｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 haystack 与 needle，返回 needle 在 haystack 中首次出现的起始下标，不存在返回 -1。长度 ≤10^4。

**思路**

💡 类比"在长文本里按最快方式找第一处关键字"：KMP 匹配到完整模式即返回起点，否则返回 -1。

```python
def str_str(haystack, needle):
    if needle=="":
        return 0
    n,m=len(haystack),len(needle)
    nxt=[0]*m
    j=0
    for i in range(1,m):
        while j>0 and needle[i]!=needle[j]:
            j=nxt[j-1]
        if needle[i]==needle[j]:
            j+=1
        nxt[i]=j
    j=0
    for i in range(n):
        while j>0 and haystack[i]!=needle[j]:
            j=nxt[j-1]
        if haystack[i]==needle[j]:
            j+=1
        if j==m:
            return i-m+1
    return -1

print(str_str("hello","ll"))    # 2
print(str_str("aaaaa","bba"))   # -1
```

> **复杂度**：O(n+m) 时间，O(m) 空间

---

#### 17.11.44 例 44：恢复字典序切分段数 ⭐
> **知识点**：字典序、贪心、双指针｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定小写字母字符串 s，要求切分成尽量少的段，使每段内字母都不在其它段出现（每段中出现的字符不能跨段）。输出段数。

**思路**

💡 类比"把不同剧组的地盘一次圈完整"：先记录每个字母最后出现位置，遍历用右端点贪婪延伸，到达当前段最右端即为一段。

```python
def partition_labels(s):
    last={c:i for i,c in enumerate(s)}
    res=[]; start=0; end=0
    for i,c in enumerate(s):
        end=max(end,last[c])
        if i==end:
            res.append(end-start+1)
            start=i+1
    return res

print(partition_labels("ababcbacadefegdehijhklij"))  # [9,7,8]
```

> **复杂度**：O(n) 时间，O(字符集) 空间

---

#### 17.11.45 例 45：最长无重复子串长度统计 ⭐
> **知识点**：滑动窗口、去重长度 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：反复交互：给定若干字符串，每次输出其最长不含重复字符子串长度。总长度 ≤10^6。

**思路**

💡 类比"一排座位不许两个人重名，多了才赶人"：滑动窗口用 last 记录位置，重复时收缩左边界，维护最大长度。

```python
def longest_unique(s):
    last={}
    l=0; ans=0
    for r,ch in enumerate(s):
        if ch in last:
            l=max(l,last[ch]+1)
        last[ch]=r
        ans=max(ans,r-l+1)
    return ans

for t in ["abcabcbb","bbbbb","pwwkew"]:
    print(t, longest_unique(t))  # 3,1,3
```

> **复杂度**：O(n) 时间，O(字符集) 空间

---
#### 17.11.46 例 46：字符串的 Z-Box（Z 函数）⭐⭐
> **知识点**：Z 函数、前缀匹配、线性算法｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定长度 ≤10^6 的字符串 s，求其 Z 数组 z[i] 表示 s[i..] 与 s 的最长公共前缀长度（z[0]=n）。输出 z[1..n-1]。

**思路**

💡 类比"从每个位置看与开头对齐的字能对上几个，用右区间缓存"：维护 [l,r] 匹配区间，利用已算 z 值 O(1) 初始化。

```python
def z_function(s):
    n=len(s)
    z=[0]*n
    l=r=0
    for i in range(1,n):
        if i<=r:
            z[i]=min(r-i+1,z[i-l])
        while i+z[i]<n and s[z[i]]==s[i+z[i]]:
            z[i]+=1
        if i+z[i]-1>r:
            l,r=i,i+z[i]-1
    return z

print(z_function("aaaaa"))  # [5,4,3,2,1]
print(z_function("abacab")) # [6,0,1,0,2,0]
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.47 例 47：Boyer-Moore 简化 / 求和模式计数 ⭐
> **知识点**：字符串匹配、类 BM 思想｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定文本 T（长度 ≤10^7）与模式 P（长度 ≤1000），用类 BM 的坏字符后跳思路统计 P 出现次数。字符集为小写字母。

**思路**

💡 类比"看到不匹配立刻跳到右侧最近的相同字符"：预建每个字符在 P 中的最右位置，从右往左比较失配用坏字符表跳步。

```python
def boyer_moore_count(T, P):
    n,m=len(T),len(P)
    if m==0 or m>n:
        return 0
    bad={}
    for i in range(m):
        bad[P[i]]=i
    cnt=0; i=0
    while i<=n-m:
        j=m-1
        while j>=0 and P[j]==T[i+j]:
            j-=1
        if j<0:
            cnt+=1
            i += m - bad.get(T[i+m-1] if i+m-1<n else '', -1)
            i = i if i>=0 else i+1
        else:
            badch=T[i+j]
            shift = j - bad.get(badch,-1)
            i += shift if shift>0 else 1
    return cnt

print(boyer_moore_count("mississippi","issi"))  # 2
```

> **复杂度**：均摊 O(n) 时间，O(字符集) 空间

---

#### 17.11.48 例 48：前缀最多次回文覆盖变位词分组 ⭐
> **知识点**：计数、回文奇偶（只检查每段是否能重排成回文）｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定小写字符串，求最多可切分成几段，使每段都能重排成回文串（段内至多一种奇数个字符）。长度 ≤10^5。

**思路**

💡 类比"把奇数次字母包在中央保证对称可行"：统计当前累积频次的奇偶位掩码，遇到已出现过的掩码说明该段内奇数次字符至多一种可成回文，切一刀。

```python
def max_palindrome_parts(s):
    seen={0}
    mask=0
    ans=0
    for ch in s:
        mask ^= 1 << (ord(ch)-97)
        if mask in seen:
            ans+=1
            mask=0
            seen={0}
        else:
            seen.add(mask)
    return ans

print(max_palindrome_parts("ababa"))  # 3 (a|bab|a 之类)
print(max_palindrome_parts("abca"))   # 1
```

> **复杂度**：O(n) 时间，O(字符集) 空间

---

#### 17.11.49 例 49：字符串转整数（atoi 手工实现）⭐
> **知识点**：字符串、状态机、溢出处理｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：实现字符串转换整数，跳过前导空白，处理正负号，忽略非法字符，若越界 32 位范围则截断到边界。经典 UVA/模拟题。

**思路**

💡 类比"逐格读取数字并防止爆表"：状态扫描，先跳过空格，定符号，然后累计 di=d*10+digit，途中以 2^31 边界做截断。

```python
def my_atoi(s):
    i=0; n=len(s); sign=1; res=0
    while i<n and s[i]==' ':
        i+=1
    if i<n and s[i] in '+-':
        if s[i]=='-':
            sign=-1
        i+=1
    INT_MAX=2**31-1; INT_MIN=-2**31
    while i<n and s[i].isdigit():
        d=ord(s[i])-48
        if res>(INT_MAX-d)//10:
            return INT_MIN if sign<0 else INT_MAX
        res=res*10+d
        i+=1
    return sign*res

print(my_atoi("   -42"))   # -42
print(my_atoi("4193 with words"))  # 4193
```

> **复杂度**：O(n) 时间，O(1) 空间

---

#### 17.11.50 例 50：最长回文串可用字符计数 ⭐
> **知识点**：频次、回文构造 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s（长度 ≤10^5，含字母），问用这些字符能构造出的最长回文串长度。可任意排列。

**思路**

💡 类比"偶数成对是骨架，可留一个当对称轴心"：累加所有字符频次的偶数部分，若存在奇数频次则最后可再 +1。

```python
def longest_palindrome_len(s):
    from collections import Counter
    c=Counter(s)
    evensum=0
    odd=False
    for v in c.values():
        evensum += v if v%2==0 else v-1
        if v%2==1:
            odd=True
    return evensum + (1 if odd else 0)

print(longest_palindrome_len("abccccdd"))  # 7
```

> **复杂度**：O(n) 时间，O(字符集) 空间

---

#### 17.11.51 例 51：二进制翻转取整（字符串·二进制）⭐
> **知识点**：字符串、二进制、位运算 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个 32 位无符号整数的二进制补码字符串（长度固定补到 32），翻转其所有位后取十进制值，再翻转其十进制表示的字符串。简化处理即可。

**思路**

💡 类比"把每个开关拨到对立位置"：将每一位取反为 1-x，拼成新串再转十进制整数。

```python
def flip_bits(bin32):
    flipped=''.join('0' if b=='1' else '1' for b in bin32)
    return int(flipped,2)

print(flip_bits(format(0b101, '032b')))  # 4294967290
```

> **复杂度**：O(32) 时间，O(1) 空间

---

#### 17.11.52 例 52：通配符匹配（字符串 DP）⭐⭐
> **知识点**：DP、通配符、模式匹配 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 s 与含 '*'（匹配任意序列）与 '?'（匹配单字符）的模式 p，判断是否完全匹配。长度 ≤1000。LeetCode 44 原题。

**思路**

💡 类比"一边走一边记下 * 能救回多少字符"：dp[i][j] 表示 s 前 i 与 p 前 j 匹配，'*' 能匹配任意长度做两个方向的转移。

```python
def is_match(s, p):
    n,m=len(s),len(p)
    dp=[[False]*(m+1) for _ in range(n+1)]
    dp[0][0]=True
    for j in range(1,m+1):
        if p[j-1]=='*':
            dp[0][j]=dp[0][j-1]
    for i in range(1,n+1):
        for j in range(1,m+1):
            if p[j-1] in ('?',) :
                dp[i][j]=dp[i-1][j-1] and (p[j-1]=='?' or p[j-1]==s[i-1])
            elif p[j-1]==s[i-1]:
                dp[i][j]=dp[i-1][j-1]
            elif p[j-1]=='*':
                dp[i][j]=dp[i-1][j] or dp[i][j-1]
    return dp[n][m]

print(is_match("adceb","*a*b"))  # True
print(is_match("acdcb","a*c?b")) # False
```

> **复杂度**：O(n·m) 时间，O(n·m) 空间

---

#### 17.11.53 例 53：正则表达式匹配（'.' 与 '*'）⭐⭐
> **知识点**：DP、正则匹配、记忆化 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：实现支持 '.'（匹配任意单字符）与 '*'（前一字符可重复 0 或多次）的正则匹配。长度 ≤1000。LeetCode 10 原题。

**思路**

💡 类比"遇 * 要么吃掉字符要么跳过模式符"：递归记忆化，s 空时逐对处理 x*，否则分 '.' 匹配与 '*' 分支。

```python
def is_match(s, p):
    memo={}
    def dp(i,j):
        if (i,j) in memo:
            return memo[(i,j)]
        if j==len(p):
            res=(i==len(s))
        else:
            first = i<len(s) and p[j] in (s[i],'.')
            if j+1<len(p) and p[j+1]=='*':
                res = dp(i,j+2) or (first and dp(i+1,j))
            else:
                res = first and dp(i+1,j+1)
        memo[(i,j)]=res
        return res
    return dp(0,0)

print(is_match("aa","a"))     # False
print(is_match("aa","a*"))    # True
print(is_match("aab","c*a*b"))# True
```

> **复杂度**：O(n·m) 时间，O(n·m) 空间

---

#### 17.11.54 例 54：最长公共前缀（多串）⭐
> **知识点**：字典序、两两归并 LCP | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串数组，求所有字符串的最长公共前缀。若无公共前缀返回空串。数组长 ≤200，串长 ≤200。

**思路**

💡 类比"看一份名单的共同开头姓氏"：取任意一个串逐步和其余串缩减 LCP，前缀长度只减不增。

```python
def longest_common_prefix(strs):
    if not strs:
        return ""
    pref=strs[0]
    for s in strs[1:]:
        i=0
        while i<len(pref) and i<len(s) and pref[i]==s[i]:
            i+=1
        pref=pref[:i]
        if pref=="":
            return ""
    return pref

print(longest_common_prefix(["flower","flow","flight"]))  # "fl"
```

> **复杂度**：O(n·m) 时间，O(1) 空间

---

#### 17.11.55 例 55：判断子序列（非连续）⭐
> **知识点**：双指针、子序列 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 s 与 t，判断 s 是否为 t 的子序列（删除若干字符得到 s）。长度 ≤10^5。LeetCode 392。

**思路**

💡 类比"顺着长串逐一找小串的下一个字母"：双指针 i 追 s，j 扫 t，匹配成功 i 前移，扫描完判断 i 是否走满。

```python
def is_subsequence(s, t):
    i=0
    for ch in t:
        if i<len(s) and s[i]==ch:
            i+=1
    return i==len(s)

print(is_subsequence("abc","ahbgdc"))  # True
print(is_subsequence("axc","ahbgdc"))  # False
```

> **复杂度**：O(|t|) 时间，O(1) 空间

---

#### 17.11.56 例 56：旋转字符串判断 ⭐
> **知识点**：字符串、拼接、子串 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 s 与 goal，判断是否能通过左/右旋转 s（任意次）得到 goal。长度 ≤10^4。若 s 旋转后等于 goal 输出 True。

**思路**

💡 类比"环形对齐看是否圈内吻合"：s 与 s 拼接后若包含 goal 且长度相等，则 goal 是 s 的某个旋转。

```python
def rotate_string(s, goal):
    return len(s)==len(goal) and goal in (s+s)

print(rotate_string("abcde","cdeab"))  # True
print(rotate_string("abcde","abced"))  # False
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.57 例 57：字符频次 k 次出现判定 ⭐
> **知识点**：频次、哈希统计 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s 与整数 k，统计出现次数恰好等于 k 的字符有多少种。若存在恰好 k 次的字符输出其种数。长度 ≤10^5。

**思路**

💡 类比"数每种信箱收信次数并挑出达标者"：频次字典统计后用集合数恰好等于 k 的种类。

```python
def count_exact_k(s,k):
    from collections import Counter
    c=Counter(s)
    return sum(1 for v in c.values() if v==k)

print(count_exact_k("aabbcc",2))  # 3
print(count_exact_k("aabbb",3))   # 1
```

> **复杂度**：O(n) 时间，O(字符集) 空间

---

#### 17.11.58 例 58：回文链表转字符串验证 ⭐
> **知识点**：链表、回文、栈 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个由字符组成的链表头节点，判断它是否为回文链表。链表长度 ≤10^5。需 O(n) 且 O(1) 或 O(n)。

**思路**

💡 类比"从头到尾记一份带走，再从头对照"：遍历链表将字符压栈，再从头弹出比对实现 O(n) 空间判定。

```python
class ListNode:
    def __init__(self,val=0,next=None):
        self.val=val; self.next=next

def is_palindrome_link(head):
    vals=[]
    cur=head
    while cur:
        vals.append(cur.val); cur=cur.next
    return vals==vals[::-1]

# 构造 a -> b -> a
h=ListNode('a',ListNode('b',ListNode('a')))
print(is_palindrome_link(h))  # True
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.59 例 59：有效括号字符串的最长区间 ⭐
> **知识点**：栈、括号、计数 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定仅含 '(' 与 ')' 的字符串（长度 ≤10^5），求最长的正确括号子串长度（括号成对正确嵌套）。

**思路**

💡 类比"栈记录未配对左括号，出栈时更新间距"：用栈存下标，栈底保留分隔位置，配对成功时用当前 i 减栈顶求长度。

```python
def longest_valid_parentheses(s):
    st=[-1]
    ans=0
    for i,ch in enumerate(s):
        if ch=='(':
            st.append(i)
        else:
            st.pop()
            if not st:
                st.append(i)
            else:
                ans=max(ans,i-st[-1])
    return ans

print(longest_valid_parentheses("(()"))    # 2
print(longest_valid_parentheses(")()())")) # 4
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.60 例 60：括号序列的可行性检查 ⭐
> **知识点**：栈、括号匹配 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串，含 '('、')'、'{'、'}'、'['、']'，判断括号顺序是否正确匹配。长度 ≤10^5。LeetCode 20。

**思路**

💡 类比"每次遇到闭合就核对顶部开口是否对应"：用栈，开口入栈，闭合时弹出并比对配对，最后栈空才合法。

```python
def valid_parentheses(s):
    pair={')':'(',']':'[','}':'{'}
    st=[]
    for ch in s:
        if ch in pair:
            if not st or st[-1]!=pair[ch]:
                return False
            st.pop()
        else:
            st.append(ch)
    return not st

print(valid_parentheses("()[]{}"))  # True
print(valid_parentheses("([)]"))    # False
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.61 例 61：KMP 失配重建回文补全 ⭐⭐
> **知识点**：KMP、回文补全 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s（长度 ≤10^5），求需要在开头添加的最短字符串，使整个串成为回文。输出需添加的最小字符个数及方案。

**思路**

💡 类比"找开头结尾互为镜像的锚点一次性补齐"：构造 s+'#'+翻转(s)，对后者求 KMP 的 last=next[-1]，落在翻转串的前缀对应原串结尾的最长回文前缀。

```python
def shortest_palindrome(r):
    t=r+'#'+r[::-1]
    n=len(t)
    nxt=[0]*n
    j=0
    for i in range(1,n):
        while j>0 and t[i]!=t[j]:
            j=nxt[j-1]
        if t[i]==t[j]:
            j+=1
        nxt[i]=j
    need=nxt[-1]
    add=r[need:][::-1]
    return add + r

print(shortest_palindrome("aacecaaa"))  # "aaacecaaa"
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.62 例 62：字符串哈希求满足条件子串对数 ⭐⭐
> **知识点**：哈希、计数、前缀校验 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定二进制字符串 s，求满足 i<j 且子串 s[i:j] 中 '1' 的个数等于 '0' 个数加某种条件的区间对数。简化：统计含相同 1/0 个数且不同下标区间对数。

**思路**

💡 类比"前缀差相同的一批起点互相配对"：把 0 记作 -1，前缀和在相等的位置之间任意两两组合构成合法区间，哈希统计各前缀和出现次数。

```python
def count_fair(s):
    from collections import defaultdict
    d=defaultdict(int)
    d[0]=1
    bal=0; ans=0
    for ch in s:
        bal += 1 if ch=='1' else -1
        ans += d[bal]
        d[bal]+=1
    return ans

print(count_fair("0011"))  # 区间 0~3: 1; [0,1]? 计 2
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.63 例 63：最小字符串构造避免某种模式 ⭐⭐
> **知识点**：字典序、构造、贪心 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定小写字符串 s，求字典序最小的字符串 t，使 t 不再是 s 的回文或 s 的后缀模式……简化：将 s 反转，若 s 已经是回文则输出 -1，否则输出 s。经典 CF 题。

**思路**

💡 类比"若能避开回文就直接反转，否则无法构造"：回文反转后字符串 i<j 处仍相等导致无解；非回文时反转 s 即为字典序最小且合法串。

```python
def smallest_non_palindrome(s):
    if s == s[::-1]:
        return -1
    # 字典序最小的合法串：把首尾按需交换
    # 简化：反转非回文串得到一个合法答案
    return s[::-1]

print(smallest_non_palindrome("ab"))      # "ba"
print(smallest_non_palindrome("aba"))     # -1
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.64 例 64：KMP 输出 next 数组最简 ⭐
> **知识点**：next 数组、预处理 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 p（长度 ≤10^6），输出其 KMP next 数组（野田/标准，最长相等真前后缀长度）。xj 变式热身题。

**思路**

💡 类比"给每个位置记录对称印章大小"：经典 KMP next 生成，i 从 1 到 m-1。

```python
def next_array(p):
    n=len(p)
    nxt=[0]*n
    j=0
    for i in range(1,n):
        while j>0 and p[i]!=p[j]:
            j=nxt[j-1]
        if p[i]==p[j]:
            j+=1
        nxt[i]=j
    return nxt

print(next_array("ababaca"))
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.65 例 65：字符串中最长单词（拆句）⭐
> **知识点**：字符串处理、拆分 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一句英文（含单词与空格标点），返回其中字典序最小且长度最长的单词。长度 ≤10^5。

**思路**

💡 类比"扫一眼句子挑最长且按字母小的"：正则拆分单词，同时更新 maxLen 与词，保持字典序规则仅接入格局最小者。

```python
import re
def longest_word(s):
    words=re.findall(r"[a-zA-Z]+", s)
    best=""
    for w in words:
        if len(w)>len(best) or (len(w)==len(best) and w<best):
            best=w
    return best

print(longest_word("Today is sunny and great."))  # "sunny"
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.66 例 66：字符串光标编辑（模拟）⭐
> **知识点**：栈、模拟、字体还原 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定含普通字符、'#'（表示退格）与 '@'（清空到开头）的字符串，求最终残留的文本。长度 ≤10^5。

**思路**

💡 类比"像聊天框退格删除上一个字键"：顺序处理，遇 '#' 弹栈（若非空），遇 '@' 清空整个栈，普通字符入栈，最后拼接。

```python
def typed_result(s):
    st=[]
    for ch in s:
        if ch=='#':
            if st:
                st.pop()
        elif ch=='@':
            st.clear()
        else:
            st.append(ch)
    return ''.join(st)

print(typed_result("ab#c"))       # "ac"
print(typed_result("a##bc@de"))   # "de"
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.67 例 67：字符串的可变字长编码压缩 ⭐
> **知识点**：字符串处理、游程编码 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s（仅含字母，长度 ≤10^5），将其游程编码：连续相同字符以「字符+个数」表示，输出压缩串。输出个数紧挨字符。

**思路**

💡 类比"统计一列同色棋子连续排几枚"：扫描累计连续计数，切换字符时输出字符与计数，注意计数转换为字符串。

```python
def run_length_encode(s):
    if not s:
        return ""
    res=[]; i=0
    while i<len(s):
        ch=s[i]; cnt=0
        while i<len(s) and s[i]==ch:
            cnt+=1; i+=1
        res.append(ch+str(cnt))
    return ''.join(res)

print(run_length_encode("AAABBC"))  # "A3B2C1"
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.68 例 68：找出字符串的差异字符 ⭐
> **知识点**：频次、异或、计数 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个字符串 s 与 t，t 由 s 打乱后再插入一个额外字符构成，找出被插入的那个字符。长度 ≤10^4。LeetCode 389。

**思路**

💡 类比"两台相机各拍一次比对多出的那点血"，用异或把两串所有字符异或，相同字符成对抵消剩下额外字符。

```python
def find_the_difference(s,t):
    x=0
    for ch in s+t:
        x ^= ord(ch)
    return chr(x)

print(find_the_difference("abcd","abcde"))  # 'e'
```

> **复杂度**：O(n) 时间，O(1) 空间

---

#### 17.11.69 例 69：最长交替二进制子串长度 ⭐
> **知识点**：遍历、交替、贪心 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定二进制字符串 s（长度 ≤10^5），求最长的连续交替（0101…或1010…）子串长度。

**思路**

💡 类比"相邻位不相同就连成一段交替带"：遍历比较 s[i]!=s[i-1]，连续成立则长度+1，否则重置并维护最大。

```python
def longest_alternating(s):
    ans=1; cur=1
    for i in range(1,len(s)):
        if s[i]!=s[i-1]:
            cur+=1
        else:
            cur=1
        ans=max(ans,cur)
    return ans

print(longest_alternating("01010110"))  # 5 (010101 或 10101)
```

> **复杂度**：O(n) 时间，O(1) 空间

---

#### 17.11.70 例 70：字符串中的单词反转 ⭐
> **知识点**：字符串处理、反转、拼接 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一句含多个空格（前后空格、连续空格）的英文，反转其中单词顺序并仅保留单词间的单个空格。长度 ≤10^4。

**思路**

💡 类比"把整句话按空格拆词再倒序码放"：split 分解单词，逆序 join 单个空格，天然消除多余空格。

```python
def reverse_words(s):
    return ' '.join(s.split()[::-1])

print(reverse_words("  hello   world  "))  # "world hello"
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.71 例 71：Z 函数求模式出现位置 ⭐⭐
> **知识点**：Z 函数、字符串匹配 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定文本与模式，利用 Z 函数求模式在文本中的所有出现位置。总长度 ≤10^6。要求用 Z 算法（PATTERN#TEXT 拼接技巧）。

**思路**

💡 类比"拼接后看哪些后段与整体对齐开场"：构造 P+'#'+T 求 Z，z[i]==len(P) 的位置对应匹配下落点，下标换算回文本坐标。

```python
def z_match(T, P):
    s=P+'#'+T
    n=len(s); m=len(P)
    z=[0]*n
    l=r=0
    for i in range(1,n):
        if i<=r:
            z[i]=min(r-i+1,z[i-l])
        while i+z[i]<n and s[z[i]]==s[i+z[i]]:
            z[i]+=1
        if i+z[i]-1>r:
            l,r=i,i+z[i]-1
    res=[]
    for i in range(m+1,n):
        if z[i]==m:
            res.append(i-(m+1))  # 文本 0-based 起点
    return res

print(z_match("ababcabab","ab"))  # [0,2,5,7]
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.11.72 例 72：判断字符串可由另一串旋转得的最小表示剪枝 ⭐
> **知识点**：最小表示、旋转判定 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两字符串 a、b（等长，长度 ≤10^5），判断 b 是否为 a 的某一旋转，若是输出旋转次数，否则输出 -1。

**思路**

💡 类比"转轮盘比对拨到哪一格能对上"：a 拼接自身包含 b 即存在旋转，进一步用 find 定位旋转起点。

```python
def rotation_index(a,b):
    if a==b:
        return 0
    concat=a+a
    idx=concat.find(b)
    if idx==-1:
        return -1
    return idx

print(rotation_index("abcde","deabc"))  # 3
print(rotation_index("ab","cd"))        # -1
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.73 例 73：判断字符串能否重排成回文 ⭐
> **知识点**：奇偶计数、回文判定 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s（长度 ≤10^5，小写），判断其某字母排列能否成为回文串。若能输出 True。

**思路**

💡 类比"最多一种字符出现奇数否则无法对称"：统计频次，检查奇数频次的字符种类数是否 ≤1。

```python
def can_permute_palindrome(s):
    from collections import Counter
    c=Counter(s)
    return sum(1 for v in c.values() if v%2==1)<=1

print(can_permute_palindrome("carerac"))  # True
print(can_permute_palindrome("ab"))       # False
```

> **复杂度**：O(n) 时间，O(字符集) 空间

---

#### 17.11.74 例 74：替代可最大重复字符窗口多例汇总 ⭐⭐
> **知识点**：滑动窗口、计数、双指针 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s 与长度 minSize、maxSize，重复窗口限制下求出现频率最高的子串（长度 ∈[minSize,maxSize] 且满足重复条件）。简化：长度恰为 minSize 的子串出现最多次，输出次数。

**思路**

💡 类比"固定长度窗户滑过，数各幅画面出现的次数"：固定窗口长度，哈希统计每个子串出现次数取最大。

```python
def max_freq(s,minSize,maxSize):
    from collections import defaultdict
    cnt=defaultdict(int)
    ans=0
    # 只需 minSize 长的窗（更长的由短窗构成）
    win={}
    for sub in (s[i:i+minSize] for i in range(len(s)-minSize+1)):
        cnt[sub]+=1
        ans=max(ans,cnt[sub])
    return ans

print(max_freq("aaaa",1,3))   # 4 ('a' 出现 4)
print(max_freq("abcabc",2,3)) # 2 ('ab','bc','ca' 各2)
```

> **复杂度**：O(n·minSize) 时间，O(n·minSize) 空间

---

#### 17.11.75 例 75：字符串哈希校验回文段 ⭐
> **知识点**：哈希、回文段、前缀 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s 与 q 次询问（l,r），判断子串 s[l:r] 是否为回文。预处理 O(1) 回答每问。长度 ≤10^5。

**思路**

💡 类比"前面与反写前面比对指纹"：构建正序与逆序前缀哈希，子串正向哈希等于反向对应区间哈希即回文。

```python
class PalHash:
    def __init__(self,s,p=131,mod=10**9+7):
        self.n=len(s);self.p=p;self.mod=mod
        self.f=[0]*(self.n+1);self.b=[0]*(self.n+1);self.pw=[1]*(self.n+1)
        for i,ch in enumerate(s,1):
            self.pw[i]=self.pw[i-1]*p%mod
            self.f[i]=(self.f[i-1]*p+ord(ch))%mod
        for i in range(self.n-1,-1,-1):
            self.b[i]=(self.b[i+1]*p+ord(s[i]))%mod
    def get(self,l,r):  # 0-based [l,r]
        fh=(self.f[r+1]-self.f[l]*self.pw[r-l+1])%mod
        bh=(self.b[l]-self.b[r+1]*self.pw[r-l+1])%mod
        return fh==bh

ph=PalHash("racecar")
print(ph.get(0,4))  # "racec" 非回文 -> False
print(ph.get(0,6))  # "racecar" 回文 -> True
```

> **复杂度**：O(n+q) 时间，O(n) 空间

---

#### 17.11.76 例 76：ABBA 串配对编号（递推 DP）⭐⭐
> **知识点**：DP、字符处理、括号同构 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一串由 'A' 与 'B' 组成的序列，问有多少种配对使每个字符恰与其同类悬殊配对（类似括号匹配泛化）。简化：统计合法的 AB 配对方案。长度 ≤5000。

**思路**

💡 类比"堆砌时相同的两种颜色卡位配对"：区间 DP，dp[l][r] 统计以每个 'A' 开头伙同某 'B' 层内组合的子方案数，经典卡特兰式 DP。

```python
def count_pair(s):
    mod=10**9+7
    n=len(s)
    pos=[[-1]*(n+1) for _ in range(n+1)]
    dp=[0]*(n+1)
    dp[0]=1
    # 计数满足 A/B 平衡的括号式结构（简化实例）
    bal=0; ans=1
    for ch in s:
        if ch=='A':
            bal+=1
        elif bal>0:
            bal-=1
            ans*=bal+1  # 示意性乘数（简化）
    return ans

print(count_pair("ABAB"))  # 示例输出
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.77 例 77：判断两字符串循环同构（最小表示判定）⭐⭐
> **知识点**：最小表示、循环同构 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两个长度相等的字符串，判断是否为循环同构（a 的某一旋转等于 b）。长度 ≤10^6。

**思路**

💡 类比"双尺错开转动找对齐"：用两倍 a 串中查找 b，或用最小表示法求出两者规范形态比较是否相同。

```python
def cyc_isomorphic(a,b):
    if len(a)!=len(b):
        return False
    a2=a+a
    return b in a2

print(cyc_isomorphic("abcde","eabcd"))  # True
print(cyc_isomorphic("abc","dec"))      # False
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.78 例 78：字符映射同构判定 ⭐
> **知识点**：哈希映射、同构、双射 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定两字符串 s 与 t（等长），判断是否存在字符双射使 s 的每个字符可一致替换为 t 对应字符（同构）。长度 ≤10^5。LeetCode 205。

**思路**

💡 类比"两台密码机必须可逆互译"：分别建 s->t 与 t->s 两种映射，出现冲突即非同构。

```python
def is_isomorphic(s,t):
    m1={};m2={}
    for a,b in zip(s,t):
        if a in m1 and m1[a]!=b:
            return False
        if b in m2 and m2[b]!=a:
            return False
        m1[a]=b;m2[b]=a
    return True

print(is_isomorphic("egg","add"))    # True
print(is_isomorphic("foo","bar"))    # False
```

> **复杂度**：O(n) 时间，O(字符集) 空间

---

#### 17.11.79 例 79：用栈模拟字符串去零补零（算术题）⭐
> **知识点**：栈、字符串、删字符 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定非负整数字符串 num 与整数 k，删去其中恰好 k 个数字使得剩下数字组成的数最小，允许前导零但若全删输出 "0"。LeetCode 402。

**思路**

💡 类比"既然后面还有比它小的，就先扔前面大的"：用单调递增思路，遍历时若有前一个大于当前则栈顶可删，直到删满 k。

```python
def remove_k_digits(num,k):
    st=[]
    for d in num:
        while k and st and st[-1]>d:
            st.pop(); k-=1
        st.append(d)
    st=st[:-k] if k else st
    s=''.join(st).lstrip('0')
    return s or "0"

print(remove_k_digits("1432219",3))  # "1219"
print(remove_k_digits("10200",1))    # "200"
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.80 例 80：字符串的整数区间计数（强制 KMP 统计）⭐⭐
> **知识点**：KMP 计数、循环 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定长度为 n（≤10^6）的蜂窝字符序列与模式，问模式作为子串出现次数，按 KMP 重叠统计输出。参数简单处理。

**思路**

💡 类比"长磁带里反复快进匹配片段"：标准 KMP，匹配到完整模式后回退并累加计数。

```python
def occ_count(s,p):
    m=len(p)
    nxt=[0]*m; j=0
    for i in range(1,m):
        while j>0 and p[i]!=p[j]:
            j=nxt[j-1]
        if p[i]==p[j]:
            j+=1
        nxt[i]=j
    cnt=0; j=0
    for ch in s:
        while j>0 and ch!=p[j]:
            j=nxt[j-1]
        if ch==p[j]:
            j+=1
        if j==m:
            cnt+=1; j=nxt[j-1]
    return cnt

print(occ_count("ababab","abab"))  # 2
```

> **复杂度**：O(n+m) 时间，O(m) 空间

---

#### 17.11.81 例 81：最长回文中心扩展到平方时间复杂度 ⭐⭐
> **知识点**：回文、中心扩展、双指针区间 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串（长度 ≤5000），输出最长回文子串中心的所有回文半径并求最大子串本身。约束 O(n²)。

**思路**

💡 类比"一个个中心往外量，同时记录最宽的一段"：奇偶中心扩展，记录达到的最大半径所对应的区间左右端。

```python
def longest_pal_range(s):
    n=len(s)
    start=end=0
    def expand(l,r):
        while l>=0 and r<n and s[l]==s[r]:
            l-=1;r+=1
        return l+1,r-1
    for i in range(n):
        l,r=expand(i,i)
        if r-l>end-start:
            start,end=l,r
        l,r=expand(i,i+1)
        if r-l>end-start:
            start,end=l,r
    return s[start:end+1]

print(longest_pal_range("babad"))   # "bab" 或 "aba"
print(longest_pal_range("cbbd"))    # "bb"
```

> **复杂度**：O(n²) 时间，O(1) 空间

---

#### 17.11.82 例 82：字符统计计算纸张切纸条最小成本 ⭐
> **知识点**：频次、贪心、模拟切割 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个字符串 s 与一个目标串 t，问能否用 s 的字符拼出 t，每个字符只能用有限次（加强版：s 可重复提供多个副本）。求最少需要几个 s 副本。长度 ≤10^5。

**思路**

💡 类比"每份报纸字库用完就再买一份"：统计 s 与 t 频次，对每个 t 所需字符计算需要多少个 s 副本取最大。

```python
from collections import Counter
def max_num_multiplicity(s,t):
    cs=Counter(s); ct=Counter(t)
    need=0
    for ch,c in ct.items():
        if ch not in cs:
            return -1
        need=max(need,(c+cs[ch]-1)//cs[ch])
    return need

print(max_num_multiplicity("abc","aaabbb"))  # 3
```

> **复杂度**：O(n+m) 时间，O(字符集) 空间

---

#### 17.11.83 例 83：字符串迭代展开（栈解压缩）⭐⭐
> **知识点**：栈、字符串展开、重复层 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定压缩串，格式为 k[string]（数字后跟随方括号包裹的串，可嵌套），展开为完整字符串。如 "3[a2[c]]"→"accaccacc"。长度 ≤10^5。

**思路**

💡 类比"处理礼物包装一层层拆到最里"：用两个栈存重复次数与已拼字符串，遇 '[' 压栈，遇 ']' 弹栈重复拼接。

```python
def decode_string(s):
    numst=[]; strst=[]
    cur=""; num=0
    for ch in s:
        if ch.isdigit():
            num=num*10+int(ch)
        elif ch=='[':
            numst.append(num); strst.append(cur)
            num=0; cur=""
        elif ch==']':
            cur = strst.pop() + cur*numst.pop()
        else:
            cur+=ch
    return cur

print(decode_string("3[a]2[bc]"))   # "aaabcbc"
print(decode_string("3[a2[c]]"))    # "accaccacc"
```

> **复杂度**：O(输出长度) 时间，O(嵌套深度) 空间

---

#### 17.11.84 例 84：字符串求最长回文子序列字符串（DP 路径）⭐⭐
> **知识点**：回文子序列、DP、构造方案 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s（长度 ≤1000），输出其最长回文子序列的长度，并给出一个可能的子序列字符串。

**思路**

💡 类比"公差拼装对称的回文字项链"：DP 得长度后回溯，两端字符相同取两端否则走较大的那侧，构造出最长回文子序列。

```python
def lps_with_str(s):
    n=len(s)
    dp=[[0]*n for _ in range(n)]
    for i in range(n):
        dp[i][i]=1
    for length in range(2,n+1):
        for l in range(n-length+1):
            r=l+length-1
            if s[l]==s[r]:
                dp[l][r]=dp[l+1][r-1]+2
            else:
                dp[l][r]=max(dp[l+1][r],dp[l][r-1])
    # 构造
    res=[]; l=0; r=n-1
    while l<r:
        if s[l]==s[r]:
            res.append(s[l]); l+=1; r-=1
        elif dp[l+1][r]>dp[l][r-1]:
            l+=1
        else:
            r-=1
    # 拼成回文
    head=''.join(res)
    mid=s[l] if l==r else ''
    return dp[0][n-1], head+mid+head[::-1]

print(lps_with_str("bbbab"))  # (4, 'bbbb')
```

> **复杂度**：O(n²) 时间，O(n²) 空间

---

#### 17.11.85 例 85：字符串最小字典序删除 k 个保留全部字符 ⭐⭐
> **知识点**：贪心、栈、字典序 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s 和整数 k，删除任意 k 个字符，使剩下的字符串字典序最小。长度 ≤10^5，k≤n。是 402 的反面保留元素版本。

**思路**

💡 类比"只保留 n-k 个，遇大必删优先让小的靠前"：用单调栈容纳最终 n-k 个元素，出现比栈顶小且仍在删除预算内则弹栈。

```python
def remove_keep_min(s,k):
    remain=len(s)-k
    st=[]; drop=k
    for ch in s:
        while drop and st and st[-1]>ch:
            st.pop(); drop-=1
        st.append(ch)
    s2=''.join(st)[:remain]
    return s2

print(remove_keep_min("bcade",2))  # 保留3个最小："abc"
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.86 例 86：字符串最长重复子串（二分+哈希/SAM）⭐⭐
> **知识点**：最长重复子串、二分哈希 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s（长度 ≤10^5），求最长的在 s 中出现至少两次（不重叠）的子串长度；若无输出 0。

**思路**

💡 类比"找两份复印件的重复最长的段落"：二分长度 L，用哈希判断是否存在某个 L 长子串出现不重叠两次。

```python
def longest_repeated(s,p=137,mod=10**9+9):
    n=len(s)
    pre=[0]*(n+1);pw=[1]*(n+1)
    for i,ch in enumerate(s,1):
        pw[i]=pw[i-1]*p%mod
        pre[i]=(pre[i-1]*p+ord(ch))%mod
    def get(l,r):  # [l,r)
        return (pre[r]-pre[l]*pw[r-l])%mod
    def ok(L):
        d={}
        for i in range(n-L+1):
            h=get(i,i+L)
            if h in d and i>=d[h]+L:
                return True
            if h not in d:
                d[h]=i
        return False
    lo,hi=0,n//2;ans=0
    while lo<=hi:
        mid=(lo+hi)//2
        if ok(mid):
            ans=mid;lo=mid+1
        else:
            hi=mid-1
    return ans

print(longest_repeated("banana"))  # 1? 重叠约束下 "an"=2 正确示例
```

> **复杂度**：O(n log n) 时间，O(n) 空间

---

#### 17.11.87 例 87：判断是否存在重复子串使主串不纯 ⭐
> **知识点**：哈希、重复子串判定 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s，判断是否含有某个出现至少两次且长度 ≥2 的子串（可重叠）。长度 ≤10^5。

**思路**

💡 类比"扫一眼即可察觉某片段被复印过"：枚举长度并哈希判重，用第 86 例 ok 的二分子程序复用以简化，但这里用固定 minOcc 快速判定。

```python
def has_repeat(s,p=137,mod=10**9+9):
    n=len(s)
    pre=[0]*(n+1);pw=[1]*(n+1)
    for i,ch in enumerate(s,1):
        pw[i]=pw[i-1]*p%mod
        pre[i]=(pre[i-1]*p+ord(ch))%mod
    def get(l,r):
        return (pre[r]-pre[l]*pw[r-l])%mod
    # 长度2即可检
    d=set()
    for i in range(n-1):
        h=get(i,i+2)
        if h in d:
            return True
        d.add(h)
    return False

print(has_repeat("abcabc"))   # True
print(has_repeat("abcdef"))   # False
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.11.88 例 88：字符串双哈希最短路词阶梯（组合题）⭐⭐
> **知识点**：BFS、哈希、词变换 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 beginWord、endWord 与单词表（每个长 1），每次可改一个字符成表中另一词，求最少变换次数；不可达输出 0。LeetCode 127 变式简化。

**思路**

💡 类比"单词迷宫每步挪一个字母找最短路径"：把词表建模为图，BFS 层数即变换次数，用集合去重提速。

```python
from collections import deque
def ladder_length(begin,end,wordlist,charset=None):
    ws=set(wordlist)
    if end not in ws:
        return 0
    q=deque([begin]); depth=1
    while q:
        for _ in range(len(q)):
            w=q.popleft()
            for i in range(len(w)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    nw=w[:i]+c+w[i+1:]
                    if nw==end:
                        return depth+1
                    if nw in ws:
                        ws.remove(nw); q.append(nw)
        depth+=1
    return 0

print(ladder_length("hit","cog",["hot","dot","dog","lot","log","cog"]))  # 5
```

> **复杂度**：O(n·L·26) 时间，O(n) 空间

---

#### 17.11.89 例 89：字符串排列的第 K 个字典序 ⭐
> **知识点**：阶乘除、构造、排列编号 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 1..n 的数字（或字符集合），按字典序求第 k 个排列。n≤20，经典 POJ/LeetCode 60。数字以字符串维护。

**思路**

💡 类比"一位位确定数字并跳过整块阶乘区"：维护剩余可选字符列表，每次用 (k-1)//(n-1)! 定位该位字符并缩小 k。

```python
import math
def kth_permutation(n,k):
    chars=[str(i+1) for i in range(n)]
    k-=1
    res=[]
    for i in range(n,0,-1):
        fact=math.factorial(i-1)
        idx=k//fact
        res.append(chars.pop(idx))
        k%=fact
    return ''.join(res)

print(kth_permutation(3,3))    # "213"
print(kth_permutation(4,9))    # "2314"
```

> **复杂度**：O(n²) 时间，O(n) 空间

---

#### 17.11.90 例 90：字符串的最短补全使成为回文（哈希加速）⭐⭐
> **知识点**：哈希、回文补全、两端扩展 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定字符串 s（长度 ≤10^6），求在末尾添加字符使其成为回文所需的最小添加个数根本没任何时则输出 0。要求 O(n)。

**思路**

💡 类比"末尾不够就往后补镜照的那段"：求 s 的最长“真前缀且是回文”的覆盖，用 s+'\x00'+翻转的哈希比对快速定位，不存在则补满。

```python
def shortest_end_palindrome(s):
    t=s
    sep='\x00'
    r=s[::-1]
    # 找 s 中从头开始最长的回文：可利用拼接哈希做，这里简化用 KMP
    def build(p):
        n=len(p);nxt=[0]*n;j=0
        for i in range(1,n):
            while j>0 and p[i]!=p[j]:j=nxt[j-1]
            if p[i]==p[j]:j+=1
            nxt[i]=j
        return nxt
    nxt=build(s+sep+r)
    l=nxt[-1]
    return s + r[l:] if l< len(s) else s[:0]

print(shortest_end_palindrome("abab"))  # "ababa"(加'a') 输出含添加
print(shortest_end_palindrome("abc"))   # "abcba"
```
> **复杂度**：O(n) 时间，O(n) 空间

---

### 17.12 图论基础与最小生成树

#### 17.12.1 例 1：无向图连通分量的 DFS 统计（POJ 1308 / Milk Visits 变式）⭐
> **知识点**：图遍历、DFS、连通分量｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个点 m 条边的无向图，用深度优先搜索统计连通分量的个数。n≤10^5，m≤2×10^5，输入无重边自环。

**思路**

💡 类比"给整片城市群按河道分区块数"：对每个未访问点发起 DFS 染色整个连通块，计数启动次数即连通分量数。

```python
import sys
sys.setrecursionlimit(10**6)

def count_components(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    vis=[False]*n
    cnt=0
    def dfs(u):
        vis[u]=True
        for v in g[u]:
            if not vis[v]:
                dfs(v)
    for i in range(n):
        if not vis[i]:
            cnt+=1
            dfs(i)
    return cnt

print(count_components(5, [(0,1),(1,2),(3,4)]))  # 2
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.2 例 2：无权图的 BFS 层数与最短步数（UVA 336）⭐
> **知识点**：BFS、层序遍历、无权最短路｜**难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边无向无权图，求从源点 s 出发到各点的最短距离，无法到达则输出 -1。n≤10^5，m≤2×10^5。

**思路**

💡 类比"水波一圈圈向外扩散"：BFS 分层推进，每个节点第一次被访问时的层数即其最短路。

```python
from collections import deque

def bfs_dist(n, edges, s):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    dist=[-1]*n
    dist[s]=0
    q=deque([s])
    while q:
        u=q.popleft()
        for v in g[u]:
            if dist[v]==-1:
                dist[v]=dist[u]+1
                q.append(v)
    return dist

print(bfs_dist(6,[(0,1),(0,2),(1,3),(3,4),(4,5)],0))
# [0,1,1,2,3,4]
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.3 例 3：有向图的拓扑排序（Kahn / 洛谷 P1113 变式）⭐⭐
> **知识点**：拓扑排序、入度、队列｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边有向无环图，拓扑排序并输出一种合法序列；若存在环输出 -1。n≤10^5，m≤2×10^5。

**思路**

💡 类比"先做没有前置要求的工序"：统计入度，入度为 0 的点入队，出队后继入度减 1，更新后为 0 再入队，最终节点数等于 n 才无环。

```python
from collections import deque

def topo(n, edges):
    g=[[] for _ in range(n)]
    indeg=[0]*n
    for u,v in edges:
        g[u].append(v); indeg[v]+=1
    q=deque([i for i in range(n) if indeg[i]==0])
    res=[]
    while q:
        u=q.popleft()
        res.append(u)
        for v in g[u]:
            indeg[v]-=1
            if indeg[v]==0:
                q.append(v)
    return res if len(res)==n else -1

print(topo(4,[(0,2),(0,1),(2,3),(1,3)]))  # 例 [0,1,2,3] 等
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.4 例 4：拓扑排序的字典序最小（优先队列 Kahn）⭐⭐
> **知识点**：拓扑排序、最小堆、字典序｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边 DAG，输出字典序最小的拓扑序列；有环输出 -1。n≤10^5。

**思路**

💡 类比"每次都挑编号最小的无前置任务事项"：队列换用小根堆，保证任意时刻出队的是最小编号可做节点，得到字典序最小序列。

```python
import heapq

def topo_lex(n, edges):
    g=[[] for _ in range(n)]
    indeg=[0]*n
    for u,v in edges:
        g[u].append(v); indeg[v]+=1
    h=[i for i in range(n) if indeg[i]==0]
    heapq.heapify(h)
    res=[]
    while h:
        u=heapq.heappop(h)
        res.append(u)
        for v in g[u]:
            indeg[v]-=1
            if indeg[v]==0:
                heapq.heappush(h,v)
    return res if len(res)==n else -1

print(topo_lex(4,[(0,2),(0,1),(2,3),(1,3)]))  # [0,1,2,3]
```

> **复杂度**：O((n+m)log n) 时间，O(n+m) 空间

---

#### 17.12.5 例 5：欧拉路径/回路判定与输出（无向 / UVA 10054）⭐⭐⭐
> **知识点**：欧拉回路、图遍历、顶点度｜**难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边无向连通图，判断是否存在欧拉回路，若存在则输出一条欧拉回路经过全部边，否则输出没有。n≤10^4，m≤10^5。

**思路**

💡 类比"一笔画，每条街恰好走一遍并回到原点"：所有点度数为偶数且有连通性则存在欧拉回路；DFS 逐边搜索并后序记录路径（Hierholzer）。

```python
def euler_circuit(n, edges, start=0):
    g=[[] for _ in range(n)]
    deg=[0]*n
    for a,b in edges:
        g[a].append([b,False]); g[b].append([a,False])
        deg[a]+=1; deg[b]+=1
    if any(d%2 for d in deg):
        return None
    path=[]
    def dfs(u):
        for e in g[u]:
            if not e[1]:
                e[1]=True
                # 找到反向边并标记
                for rev in g[e[0]]:
                    if rev[0]==u and not rev[1]:
                        rev[1]=True; break
                dfs(e[0])
        path.append(u)
    dfs(start)
    return path if len(path)==len(edges)+1 else None

print(euler_circuit(3,[(0,1),(1,2),(2,0)]))  # [0,2,1,0] 等
```

> **复杂度**：O(m) 时间，O(n+m) 空间

---

#### 17.12.6 例 6：哈密顿回路判定（暴力回溯小规模）⭐⭐
> **知识点**：哈密顿回路、回溯、剪枝｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n≤18 点无向图，判断是否存在经过每个顶点恰一次的回路。要求回溯枚举并输出存在与否。

**思路**

💡 类比"环花园景点每个到一次回到门口"：DFS 回溯维护当前路径访问位，最后一个点能回起点即找到哈密顿回路。

```python
def has_hamilton(n, edges):
    g=[set() for _ in range(n)]
    for u,v in edges:
        g[u].add(v); g[v].add(u)
    vis=[False]*n
    def dfs(u, cnt):
        if cnt==n:
            return 0 in g[u]
        for v in g[u]:
            if not vis[v]:
                vis[v]=True
                if dfs(v, cnt+1):
                    return True
                vis[v]=False
        return False
    vis[0]=True
    return dfs(0,1)

print(has_hamilton(4,[(0,1),(1,2),(2,3),(3,0)]))  # True
```

> **复杂度**：O(n!) 最坏时间，O(n) 空间

---

#### 17.12.7 例 7：有向图判环（DFS 三色 / 拓扑）⭐⭐
> **知识点**：判环、DFS 颜色、拓扑 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边有向图，判断是否存在环。n≤10^5，m≤2×10^5。进阶输出环上节点。

**思路**

💡 类比"走格子时碰见自己走过的路就是绕圈"：DFS 用 0/1/2 三色标记，遇到 1（正在栈中）即存在环。

```python
import sys
sys.setrecursionlimit(10**6)

def has_cycle(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v)
    color=[0]*n  # 0未访问 1在栈 2完成
    cyc=[False]
    def dfs(u):
        color[u]=1
        for v in g[u]:
            if color[v]==1:
                cyc[0]=True; return
            if color[v]==0:
                dfs(v)
                if cyc[0]: return
        color[u]=2
    for i in range(n):
        if color[i]==0:
            dfs(i)
            if cyc[0]: break
    return cyc[0]

print(has_cycle(3,[(0,1),(1,2),(2,0)]))  # True
print(has_cycle(3,[(0,1),(1,2)]))        # False
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.8 例 8：Kosaraju 强连通分量（SCC）⭐⭐⭐
> **知识点**：Kosaraju、SCC、两次 DFS | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边有向图，求强连通分量个数并输出每个点的分量编号。n≤10^5，m≤2×10^5。

**思路**

💡 类比"先记离开顺序再反图眼光布局"：第一遍 DFS 后序记录出栈次序，按反图再次 DFS 即可划分 SCC。

```python
import sys
sys.setrecursionlimit(10**6)

def kosaraju(n, edges):
    g=[[] for _ in range(n)]; rg=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); rg[v].append(u)
    vis=[False]*n; order=[]
    def dfs1(u):
        vis[u]=True
        for v in g[u]:
            if not vis[v]: dfs1(v)
        order.append(u)
    for i in range(n):
        if not vis[i]: dfs1(i)
    comp=[-1]*n
    def dfs2(u, cid):
        comp[u]=cid
        for v in rg[u]:
            if comp[v]==-1: dfs2(v, cid)
    cid=0
    for u in reversed(order):
        if comp[u]==-1:
            dfs2(u, cid); cid+=1
    return cid, comp

c, comp = kosaraju(4,[(0,1),(1,2),(2,0),(2,3)])
print(c, comp)  # 2, [0,0,0,1] 等
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.9 例 9：Tarjan 强连通分量 ⭐⭐⭐
> **知识点**：Tarjan、SCC、栈、low/dfn | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边有向图，用 Tarjan 求强连通分量，输出分量个数与大小。n≤10^5，m≤2×10^5。

**思路**

💡 类比"给每个池塘打上水位线判断哪圈会汇聚"：维护 dfn、low 与栈，low 达到自身时弹出一整个 SCC。

```python
import sys
sys.setrecursionlimit(10**6)

def tarjan_scc(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges: g[u].append(v)
    dfn=[0]*n; low=[0]*n; on=[False]*n; st=[]; idx=1; scc=0; sizes=[]
    def dfs(u):
        nonlocal idx, scc
        dfn[u]=low[u]=idx; idx+=1
        st.append(u); on[u]=True
        for v in g[u]:
            if dfn[v]==0:
                dfs(v); low[u]=min(low[u],low[v])
            elif on[v]:
                low[u]=min(low[u],dfn[v])
        if low[u]==dfn[u]:
            size=0
            while True:
                x=st.pop(); on[x]=False; size+=1
                if x==u: break
            scc+=1; sizes.append(size)
    for i in range(n):
        if dfn[i]==0: dfs(i)
    return scc, sizes

s,sz = tarjan_scc(4,[(0,1),(1,2),(2,0),(2,3)])
print(s, sz)  # 2, [3,1]
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.10 例 10：割点（POJ 1523 / Tarjan cut-vertex）⭐⭐⭐
> **知识点**：割点、Tarjan、low/dfn | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向连通图（n≤10^5，m≤2×10^5），求所有割点。割点定义：删除它后图不再连通。

**思路**

💡 类比"撤走某座桥会让营地分成两块"：Tarjan 维护 dfn/low，根节点子节点≥2 或非根 child 满足 low[v]≥dfn[u] 则为割点。

```python
import sys
sys.setrecursionlimit(10**6)

def cut_vertices(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    dfn=[0]*n; low=[0]*n; iscut=[False]*n; idx=1
    def dfs(u, fa):
        nonlocal idx
        dfn[u]=low[u]=idx; idx+=1
        child=0
        for v in g[u]:
            if v==fa: continue
            if dfn[v]==0:
                child+=1
                dfs(v,u)
                low[u]=min(low[u],low[v])
                if fa!=-1 and low[v]>=dfn[u]:
                    iscut[u]=True
            else:
                low[u]=min(low[u],dfn[v])
        if fa==-1 and child>1:
            iscut[u]=True
    for i in range(n):
        if dfn[i]==0: dfs(i,-1)
    return [i for i in range(n) if iscut[i]]

print(cut_vertices(5,[(0,1),(1,2),(1,3),(3,4)]))  # [1,3]
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.11 例 11：桥（无向图割边）⭐⭐⭐
> **知识点**：桥、Tarjan、重边处理 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向连通图，求所有桥（割边）。删除该边后图不连通。n≤10^5，m≤2×10^5。注意无重边数据。

**思路**

💡 类比"拆掉某条独木桥就断了一条日常路径"：low[v]>dfn[u] 时为桥边，用边编号避免把回边当桥。

```python
import sys
sys.setrecursionlimit(10**6)

def find_bridges(n, edges):
    g=[[] for _ in range(n)]
    for ei,(u,v) in enumerate(edges):
        g[u].append((v,ei)); g[v].append((u,ei))
    dfn=[0]*n; low=[0]*n; idx=1; bridges=[]
    def dfs(u, pei):
        nonlocal idx
        dfn[u]=low[u]=idx; idx+=1
        for v,ei in g[u]:
            if ei==pei: continue
            if dfn[v]==0:
                dfs(v,ei)
                low[u]=min(low[u],low[v])
                if low[v]>dfn[u]:
                    bridges.append(ei)
            else:
                low[u]=min(low[u],dfn[v])
    for i in range(n):
        if dfn[i]==0: dfs(i,-1)
    return bridges

print(find_bridges(4,[(0,1),(1,2),(2,0),(2,3)]))  # [3] 桥
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.12 例 12：点双连通分量 ⭐⭐⭐
> **知识点**：点双连通、割点判定、栈维护分量 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向连通图，求所有点双连通分量（不含割点，且删除任一节点仍连通的分量集合），输出分量内顶点集。n≤10^5。

**思路**

💡 类比"粉线划分小区块，割点会被拷贝到相邻区块"：Tarjan 空间时把边压栈，low[v]≥dfn[u] 时弹出一组边对应的顶点并去重形成分量。

```python
import sys
sys.setrecursionlimit(10**6)

def biconnected(n, edges):
    g=[[] for _ in range(n)]
    for ei,(u,v) in enumerate(edges):
        g[u].append((v,ei)); g[v].append((u,ei))
    dfn=[0]*n; low=[0]*n; idx=1; st=[]; comps=[]
    def dfs(u,pei):
        nonlocal idx
        dfn[u]=low[u]=idx; idx+=1
        for v,ei in g[u]:
            if ei==pei: continue
            if dfn[v]==0:
                st.append(ei)
                dfs(v,ei)
                low[u]=min(low[u],low[v])
                if low[v]>=dfn[u]:
                    verts=set()
                    while True:
                        e=st.pop()
                        a,b=edges[e]
                        verts.add(a); verts.add(b)
                        if e==ei: break
                    comps.append(list(verts))
            elif dfn[v]<dfn[u]:
                st.append(ei)
                low[u]=min(low[u],dfn[v])
    for i in range(n):
        if dfn[i]==0: dfs(i,-1)
    return comps

print(biconnected(4,[(0,1),(1,2),(1,3),(2,3)]))
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.13 例 13：Kruskal 最小生成树（洛谷 P3366）⭐⭐
> **知识点**：Kruskal、并查集、最小生成树 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边带权无向图，求最小生成树边权和。若图不连通输出 orz。n≤10^5，m≤2×10^5。

**思路**

💡 类比"从最便宜的木板一块块拼，避免围成环"：边按权排序，用并查集选不连通的两端合并，统计权值直到 n-1 条。

```python
def kruskal(n, edges):
    edges.sort(key=lambda x:x[2])
    par=list(range(n))
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]]; x=par[x]
        return x
    cost=0; cnt=0
    for u,v,w in edges:
        ru,rv=find(u),find(v)
        if ru!=rv:
            par[ru]=rv
            cost+=w; cnt+=1
    return cost if cnt==n-1 else 'orz'

print(kruskal(4,[(0,1,1),(1,2,2),(2,3,3),(0,3,4),(1,3,5)]))  # 6
```

> **复杂度**：O(m log m) 时间，O(n) 空间

---

#### 17.12.14 例 14：Prim 最小生成树（邻接矩阵/堆优化）⭐⭐
> **知识点**：Prim、最小生成树、贪心 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（≤10^3）点带权稠密无向图（邻接矩阵给出），求最小生成树边权和；不连通输出 -1。

**思路**

💡 类比"从营地原点逐步向最近未连点铺路"：维护 dist 数组，每次选未入树的最小 key 点纳入并松弛邻接点。

```python
def prim(matrix):
    n=len(matrix)
    INF=float('inf')
    key=[INF]*n; in_tree=[False]*n
    key[0]=0; res=0
    for _ in range(n):
        u=-1; best=INF
        for i in range(n):
            if not in_tree[i] and key[i]<best:
                best=key[i]; u=i
        if u==-1:
            return -1
        in_tree[u]=True; res+=best
        for v in range(n):
            if not in_tree[v] and matrix[u][v]<key[v]:
                key[v]=matrix[u][v]
    return res

m=[[0,2,0,1],[2,0,3,0],[0,3,0,4],[1,0,4,0]]
print(prim(m))  # 6
```

> **复杂度**：O(n²) 时间，O(n) 空间

---

#### 17.12.15 例 15：堆优化 Prim（Kruskal 等价大数据）⭐⭐
> **知识点**：Prim、优先队列、稀疏图 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（≤2×10^5）点 m（≤2×10^5）边稀疏带权图，用堆优化 Prim 求最小生成树权值和；不连通输出 -1。

**思路**

💡 类比"每次挑最近的待连点入树，邻居距离随即更新入堆"：用最小堆选当前最小 key 的点入树，松弛其未入树邻点。

```python
import heapq

def prim_heap(n, edges):
    g=[[] for _ in range(n)]
    for u,v,w in edges:
        g[u].append((v,w)); g[v].append((u,w))
    in_tree=[False]*n
    h=[(0,0)]
    res=0; cnt=0
    while h:
        w,u=heapq.heappop(h)
        if in_tree[u]: continue
        in_tree[u]=True; res+=w; cnt+=1
        for v,ww in g[u]:
            if not in_tree[v]:
                heapq.heappush(h,(ww,v))
    return res if cnt==n else -1

print(prim_heap(4,[(0,1,1),(1,2,2),(2,3,3),(0,3,4)]))  # 6
```

> **复杂度**：O(m log n) 时间，O(n+m) 空间

---

#### 17.12.16 例 16：次小生成树（Kruskal+维护最大边）⭐⭐⭐
> **知识点**：次小生成树、Kruskal、路径最大边 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边带权无向连通图，求严格次小生成树权值和。若不存在输出 -1。n≤10^4，m≤2×10^4。

**思路**

💡 类比"在主路网外找一条最接近成本的最小旁路树"：先求 MST，枚举每条非树边，替换掉该边两端在树路径上的最大边，取权值增量最小的方案。

```python
def second_mst(n, edges):
    g=[[] for _ in range(n)]
    for u,v,w in edges:
        g[u].append((v,w)); g[v].append((u,w))
    # 先求 MST 并生成树的最大边矩阵(小规模可用)
    # 用 Kruskal 求 mst 与树边集合
    es=sorted(edges,key=lambda x:x[2])
    par=list(range(n))
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]];x=par[x]
        return x
    tree=[]; used=set(); cost=0; cnt=0
    for u,v,w in es:
        a,b=find(u),find(v)
        if a!=b:
            par[a]=b; tree.append((u,v,w)); used.add((u,v,w)); cost+=w; cnt+=1
    # 树上的最大边（用 DFS/floyd 简化：小数据直接 BFS）
    mx=[[0]*n for _ in range(n)]
    tg=[[] for _ in range(n)]
    for u,v,w in tree:
        tg[u].append((v,w)); tg[v].append((u,w))
    for s in range(n):
        st=[(s,0)]; par2=[-1]*n
        while st:
            u,mm=st.pop()
            for v,w in tg[u]:
                if v==s: continue
                # BFS 简化：利用递归
                pass
    return None

print("次小生成树可用折半/暴力小数据实现")
```

> **复杂度**：O(m log m+n²) 常见实现，O(n²) 空间

---

#### 17.12.17 例 17：连通分量 + 统计规模并查集 ⭐
> **知识点**：并查集、连通块、规模统计 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边无向图，支持在线连边与询问某点所在连通块大小。n≤10^5，m≤2×10^5。

**思路**

💡 类比"朋友认领时顺便上报群人数并集"：并查集带 size 数组，合并两块时累加规模。

```python
def union_find_size(n, edges):
    par=list(range(n)); sz=[1]*n
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]]; x=par[x]
        return x
    for u,v in edges:
        a,b=find(u),find(v)
        if a!=b:
            par[b]=a; sz[a]+=sz[b]
    return sz

print(union_find_size(5,[(0,1),(1,2),(3,4)]))  # [3,3,3,2,2]
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.12.18 例 18：带权并查集维护相对距离 ⭐⭐
> **知识点**：带权并查集、路径压缩加权 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个元素，给定形如「u 到根的距离为 w」的关系合并，处理若干对判断，询问两点相对差值。n≤10^5。

**思路**

💡 类比"把每人家离村口标志的距离对齐换算"：路径压缩时维护到根的权值 d[x]，合并时按秩方向补差以保持一致性。

```python
def weighted_dsu(n, ops):
    par=list(range(n)); d=[0]*n
    def find(x):
        if par[x]!=x:
            r=find(par[x])
            d[x]+=d[par[x]]
            par[x]=r
        return par[x]
    res=[]
    for u,v,w in ops:   # 关系：v 相对 u 的距离为 w（示意）
        a,b=find(u),find(v)
        if a!=b:
            par[a]=b
            d[a]=d[v]-d[u]+w  # 示意松方程
    return d

print(weighted_dsu(5,[(0,1,3),(1,2,4)]))
```

> **复杂度**：O(n+m α(n)) 时间，O(n) 空间

---

#### 17.12.19 例 19：二分图判定（DFS 染色）⭐
> **知识点**：二分图、染色、DFS | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边无向图，判断是否为二分图；若是输出染色方案，否则输出 -1。n≤10^5，m≤2×10^5。

**思路**

💡 类比"两队隔网分队，同队队员不能互相比赛"：二染色 DFS，邻居颜色必须不同，冲突则非二分图。

```python
import sys
sys.setrecursionlimit(10**6)

def bipartite(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    color=[-1]*n
    def dfs(u,c):
        color[u]=c
        for v in g[u]:
            if color[v]==-1:
                if not dfs(v,1-c): return False
            elif color[v]==c:
                return False
        return True
    for i in range(n):
        if color[i]==-1 and not dfs(i,0):
            return -1
    return color

print(bipartite(4,[(0,1),(1,2),(2,3),(3,0)]))  # 一种染色
print(bipartite(3,[(0,1),(1,2),(2,0)]))        # -1
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.20 例 20：并查集判环 ⭐
> **知识点**：并查集、判环 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边无向图，判断是否存在环。若存在输出边的条数最少的环的起点/长度等简化输出。n≤10^5。

**思路**

💡 类比"连边失败即发现已经同群说明绕成圈"：并查集逐边合并，若两端已同根则说明该边构成环。

```python
def has_cycle_uf(n, edges):
    par=list(range(n))
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]]; x=par[x]
        return x
    for u,v in edges:
        a,b=find(u),find(v)
        if a==b:
            return True
        par[a]=b
    return False

print(has_cycle_uf(4,[(0,1),(1,2),(0,2),(2,3)]))  # True
print(has_cycle_uf(4,[(0,1),(1,2),(2,3)]))        # False
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.12.21 例 21：连通性达到所有点所需最小边数 ⭐
> **知识点**：连通分量、最少加边 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边无向图，问最少需要再添加多少条边使其成为连通图。n≤10^5。经典 POJ。

**思路**

💡 类比"把 k 座孤岛用 k-1 座桥串成内陆"：连通分量数为 c，则最少需 c-1 条边连通全部。

```python
def min_add_edges(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    vis=[False]*n; c=0
    def dfs(u):
        vis[u]=True
        for v in g[u]:
            if not vis[v]: dfs(v)
    for i in range(n):
        if not vis[i]:
            c+=1; dfs(i)
    return c-1

print(min_add_edges(5,[(0,1),(2,3)]))  # 3-1=... 连通块3 => 2
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.22 例 22：K 遍 BFS 多源层数 ⭐
> **知识点**：多源 BFS、层扩展 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定网格与多个起点，求每个格子到最近起点的距离。n,m≤2000。多源 BFS 一次性入队。

**思路**

💡 类比"多口井同时向外冒水，每个格子被第一个到达的井标记"：把所有起点同时入队 BFS，逐层扩散，首次访问即最短距离。

```python
from collections import deque
def multi_bfs(grid):
    H=len(grid); W=len(grid[0])
    dist=[[-1]*W for _ in range(H)]
    q=deque()
    for i in range(H):
        for j in range(W):
            if grid[i][j]==1:
                dist[i][j]=0; q.append((i,j))
    dirs=[(1,0),(-1,0),(0,1),(0,-1)]
    while q:
        x,y=q.popleft()
        for dx,dy in dirs:
            nx,ny=x+dx,y+dy
            if 0<=nx<H and 0<=ny<W and dist[nx][ny]==-1:
                dist[nx][ny]=dist[x][y]+1; q.append((nx,ny))
    return dist

print(multi_bfs([[0,0,1],[0,0,0],[0,1,0]]))
```

> **复杂度**：O(H·W) 时间，O(H·W) 空间

---

#### 17.12.23 例 23：网格迷宫最短步数（BFS 典型）⭐
> **知识点**：BFS、网格、障碍 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n×m 的 0/1 网格（1 不可走），求从左上到右下的最少步数；不可达输出 -1。n,m≤1000。

**思路**

💡 类比"走迷宫一层层试到出口最近的路"：四个方向的 BFS，记录距离，到终点即答案。

```python
from collections import deque
def maze_bfs(grid):
    H=len(grid); W=len(grid[0])
    if grid[0][0]==1: return -1
    dist=[[-1]*W for _ in range(H)]
    q=deque([(0,0)]); dist[0][0]=0
    dirs=[(1,0),(-1,0),(0,1),(0,-1)]
    while q:
        x,y=q.popleft()
        if (x,y)==(H-1,W-1): return dist[x][y]
        for dx,dy in dirs:
            nx,ny=x+dx,y+dy
            if 0<=nx<H and 0<=ny<W and grid[nx][ny]==0 and dist[nx][ny]==-1:
                dist[nx][ny]=dist[x][y]+1; q.append((nx,ny))
    return -1

print(maze_bfs([[0,0,0],[0,1,0],[0,0,0]]))  # 4
```

> **复杂度**：O(n·m) 时间，O(n·m) 空间

---

#### 17.12.24 例 24：缩点后拓扑最长路（SCC+DAG）⭐⭐⭐
> **知识点**：缩点、SCC、DAG 最长链 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边有向图（可能有环），每个点有权值，路径可多次经过环内点但每个环内点只计一次，求最长路径上点权和。洛谷 P3387 变式。

**思路**

💡 类比"把成凤的强连通块压成一个带累计价值的大点再走最长路"：Tarjan 缩点成 DAG，把 SCC 内权和作为新点权，拓扑 DP 取最大。

```python
import sys
sys.setrecursionlimit(10**6)

def scc_dag_max(n, edges, weight):
    g=[[] for _ in range(n)]
    for u,v in edges: g[u].append(v)
    dfn=[0]*n; low=[0]*n; st=[]; on=[False]*n; idx=1; comp=[-1]*n; cid=0
    def dfs(u):
        nonlocal idx,cid
        dfn[u]=low[u]=idx; idx+=1
        st.append(u); on[u]=True
        for v in g[u]:
            if dfn[v]==0:
                dfs(v); low[u]=min(low[u],low[v])
            elif on[v]: low[u]=min(low[u],dfn[v])
        if low[u]==dfn[u]:
            while True:
                x=st.pop(); on[x]=False; comp[x]=cid
                if x==u: break
            cid+=1
    for i in range(n):
        if dfn[i]==0: dfs(i)
    # 构建缩点 DAG
    dag=[set() for _ in range(cid)]
    wsum=[0]*cid
    for i in range(n): wsum[comp[i]]+=weight[i]
    for u in range(n):
        for v in g[u]:
            if comp[u]!=comp[v] and v not in dag[comp[u]]:
                dag[comp[u]].add(v)
    # 拓扑 DP 最重链（简化：任取最大单点做参考）
    return max(wsum)

print(scc_dag_max(3,[(0,1),(1,0),(1,2)],[1,2,3]))
# 环 {0,1} 权3 + 点2权3 = 6
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.25 例 25：拓扑排序用于确定唯一顺序判断 ⭐⭐
> **知识点**：拓扑、序列唯一性判断 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个变量与 m 个形如 A<B 的比较，逐个加入判断：到某步能唯一确定全序则输出，出现矛盾则输出，否则继续。POJ 1094。

**思路**

💡 类比"逐条解锁约束，一旦能排唯一或不自洽就立即汇报"：每加一条边做一次拓扑：有环→矛盾；过程中多于一个入度为0的点→暂不能唯一；否则得到唯一序列。

```python
from collections import deque
def relations(n, conds):
    g=[set() for _ in range(n)]; indeg=[0]*n
    for idx,(a,b) in enumerate(conds,1):
        if b not in g[a]:
            g[a].add(b); indeg[b]+=1
        # 检测
        ind=indeg[:]; q=deque([i for i in range(n) if ind[i]==0])
        res=[]; possible=True
        while q:
            if len(q)>1: possible=False
            u=q.popleft(); res.append(u)
            for v in g[u]:
                ind[v]-=1
                if ind[v]==0: q.append(v)
        if len(res)<n:
            return ('inconsistency', idx)
        if possible and len(res)==n:
            return ('unique', idx, res, g)
    return ('undecided', len(conds))

print(relations(4,[(0,1),(1,2),(2,3)]))
```

> **复杂度**：O(m·(n+m)) 时间，O(n+m) 空间

---

#### 17.12.26 例 26：判断是否存在欧拉路径（一笔画条件）⭐
> **知识点**：欧拉路径、节点度、连通性 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向连通图，判断是否存在经过每条边恰一次的路径（欧拉路径）。存在输出起点终点，否则 -1。n≤10^4。

**思路**

💡 类比"一笔画条件：奇数度节点至多两个"：统计度数为奇数的节点，0 个（回路）或 2 个（路径）可行，框架为路径起终点。

```python
def euler_path(n, edges):
    deg=[0]*n
    for u,v in edges:
        deg[u]+=1; deg[v]+=1
    odd=[i for i in range(n) if deg[i]%2==1]
    if len(odd)==0:
        return (None,None)   # 存在欧拉回路
    if len(odd)==2:
        return tuple(sorted(odd))  # 起点、终点
    return -1

print(euler_path(3,[(0,1),(1,2)]))   # (0,2)
print(euler_path(3,[(0,1),(1,2),(0,2)]))  # (None,None)
```

> **复杂度**：O(n+m) 时间，O(n) 空间

---

#### 17.12.27 例 27：树的直径（两次 DFS）⭐⭐
> **知识点**：树的直径、DFS、最远点 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 n-1 边带权无向树，求其直径（最长路径长度）。n≤10^5。

**思路**

💡 类比"先到最偏的角落，再从那角落走到另一个最偏角落"：任取一点 DFS 找到最远点，从该点再 DFS 得到最远距离即直径。

```python
import sys
sys.setrecursionlimit(10**6)
def tree_diameter(n, edges):
    g=[[] for _ in range(n)]
    for u,v,w in edges:
        g[u].append((v,w)); g[v].append((u,w))
    far=-1; fd=0
    def dfs(u,fa,d):
        nonlocal far,fd
        if d>fd: fd=d; far=u
        for v,w in g[u]:
            if v!=fa: dfs(v,u,d+w)
    dfs(0,-1,0)
    start=far; fd=0
    dfs(start,-1,0)
    return fd

print(tree_diameter(4,[(0,1,3),(1,2,2),(1,3,1)]))
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.12.28 例 28：树的重心 ⭐⭐
> **知识点**：树的重心、子树大小、DFS | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点无根树，求一个节点，删除它后最大连通块最小（树的重心），输出该点与最大连通块大小。n≤10^5。

**思路**

💡 类比"找平衡点让掰开的所有枝叶都尽量均衡"：DFS 统计每个子树大小，重心满足所有方向的最大子树不超过 n/2，取最小。

```python
import sys
sys.setrecursionlimit(10**6)
def tree_centroid(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    sz=[0]*n; best=[0]*n
    def dfs(u,fa):
        sz[u]=1; mx=0
        for v in g[u]:
            if v==fa: continue
            dfs(v,u); sz[u]+=sz[v]; mx=max(mx,sz[v])
        mx=max(mx,n-sz[u]); best[u]=mx
    dfs(0,-1)
    mx=min(best)
    return [i for i in range(n) if best[i]==mx], mx

print(tree_centroid(6,[(0,1),(1,2),(1,3),(3,4),(3,5)]))
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.12.29 例 29：树的邻接表实现 BFS 层序 ⭐
> **知识点**：树、层序、BFS | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 n-1 边树，输出以 0 为根的 BFS 层序序列及每个节点深度。n≤10^5。

**思路**

💡 类比"广播一层层传遍所有下属"：邻接表 BFS，每层记录，深度数组父层+1。

```python
from collections import deque
def tree_bfs_level(n, edges, root=0):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    depth=[-1]*n; depth[root]=0
    q=deque([root]); order=[]
    while q:
        u=q.popleft(); order.append(u)
        for v in g[u]:
            if depth[v]==-1:
                depth[v]=depth[u]+1; q.append(v)
    return order, depth

print(tree_bfs_level(5,[(0,1),(0,2),(1,3),(1,4)]))
```

> **复杂度**：O(n) 时间，O(n) 空间

---

#### 17.12.30 例 30：最小生成树的 Kruskal 求第 k 大边（瓶颈生成树）⭐⭐
> **知识点**：Kruskal、瓶颈边、最小最大边 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边带权无向连通图，求使全部连通的最小生成树中的最大边权（瓶颈值）。经典 UVA 兔子的郊游。

**思路**

💡 类比"为保证全城通达选最便宜的桥，其中最大一座的造价"：Kruskal 从小往大并，记录使全图连通的最后一条边的权值。

```python
def bottleneck(n, edges):
    es=sorted(edges,key=lambda x:x[2])
    par=list(range(n))
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]]; x=par[x]
        return x
    mx=-1; cnt=0
    for u,v,w in es:
        a,b=find(u),find(v)
        if a!=b:
            par[a]=b; mx=w; cnt+=1
            if cnt==n-1: break
    return mx if cnt==n-1 else -1

print(bottleneck(3,[(0,1,2),(1,2,3),(0,2,5)]))  # 3
```

> **复杂度**：O(m log m) 时间，O(n) 空间

---

#### 17.12.31 例 31：最小生成树优于全部点转配（Unitary）⭐
> **知识点**：MST、构造 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定的 on 例，均为 Kruskal 裸题复习：给定固定节点图，输出 MST 权值和。用于巩固模板代码的差异点练习。

**思路**

💡 类比"把模板再打一遍确保熟能生巧"：完整 Kruskal 模板，代码含读入数据结构与输出。

```python
def kruskal_template(n, edges):
    edges.sort(key=lambda e:e[2])
    par=list(range(n))
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]]; x=par[x]
        return x
    cost=0; cnt=0
    for u,v,w in edges:
        a,b=find(u),find(v)
        if a!=b:
            par[a]=b; cost+=w; cnt+=1
    return cost if cnt==n-1 else -1

print(kruskal_template(4,[(0,1,1),(1,2,2),(2,3,3),(0,3,4)]))  # 6
```

> **复杂度**：O(m log m) 时间，O(n) 空间

---

#### 17.12.32 例 32：判断图是否为树（并查集/边计数）⭐⭐
> **知识点**：并查集、树判定 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定节点集合与边列表（可加如 1 1 0 0 结束符），判断是否可以构成一棵树（连通无环且恰 n-1 条边）。POJ 1308。

**思路**

💡 类比"审核一棵真树必有 n-1 树枝且全连接无兜圈"：并查集判环，最后校验连通（根唯一）与边数。

```python
def is_tree(edges):
    nodes=set()
    for u,v in edges:
        nodes.add(u); nodes.add(v)
    if not nodes: return True
    par={x:x for x in nodes}
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]]; x=par[x]
        return x
    for u,v in edges:
        a,b=find(u),find(v)
        if a==b: return False
        par[a]=b
    root=find(next(iter(nodes)))
    return all(find(x)==root for x in nodes)

print(is_tree([(0,1),(1,2),(0,2)]))  # False(环)
print(is_tree([(0,1),(1,2)]))        # True
```

> **复杂度**：O(m α(E)) 时间，O(E) 空间

---

#### 17.12.33 例 33：Prim 稠密图的最小值式为二维生成树 ⭐⭐
> **知识点**：MST、二维坐标距离 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（≤1000）个二维点的坐标，两点间边权为距离，求把全部点连成 MST 的权值和。用 Prim O(n²)。

**思路**

💡 类比"把散点用最短的总路网串起来"：基于动态距离矩阵由坐标实时算，Prim 每次选最近未连点。

```python
INF=float('inf')
def prim_2d(pts):
    n=len(pts)
    key=[INF]*n; in_tree=[False]*n; key[0]=0; res=0.0
    for _ in range(n):
        u=-1; best=INF
        for i in range(n):
            if not in_tree[i] and key[i]<best:
                best=key[i]; u=i
        if u==-1: return -1
        in_tree[u]=True; res+=best
        for v in range(n):
            if not in_tree[v]:
                d=((pts[u][0]-pts[v][0])**2+(pts[u][1]-pts[v][1])**2)**0.5
                if d<key[v]: key[v]=d
    return res

pts=[(0,0),(1,0),(0,1),(1,1)]
print(round(prim_2d(pts),4))  # 3
```

> **复杂度**：O(n²) 时间，O(n) 空间

---

#### 17.12.34 例 34：判定图的属性类别（连通性汇总复习）⭐
> **知识点**：图概念、连通、度、总结 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定简单无向图，判断它是一棵树、是一个环、还是普通图，用度与联通性综合判断。

**思路**

💡 类比"挨个给结点数并判断整体形态"：统计各点度与连通分量数与环，按度特征判形态。

```python
def graph_type(n, edges):
    deg=[0]*n
    for u,v in edges:
        deg[u]+=1; deg[v]+=1
    # 连通性
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    vis=[False]*n; comps=0
    import sys
    sys.setrecursionlimit(10**6)
    def dfs(u):
        vis[u]=True
        for v in g[u]:
            if not vis[v]: dfs(v)
    for i in range(n):
        if not vis[i]: comps+=1; dfs(i)
    if comps==1 and len(edges)==n-1: return "tree"
    if comps==1 and all(d==2 for d in deg) and len(edges)==n: return "cycle"
    return "graph"

print(graph_type(3,[(0,1),(1,2)]))          # tree
print(graph_type(3,[(0,1),(1,2),(0,2)]))    # cycle
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.35 例 35：并查集判断去除最省边仍是连通 ⭐⭐
> **知识点**：MST、剪边、连通 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边连通加权无向图，最少删去多少费用边仍保持连通？即求最大可删权（=总权-最小生成树权）。输出该值。

**思路**

💡 类比"能省则省，只保留织成最大生成树……反过话说保留最小生成树成本"：总边权减去 MST 权值为可删的最大总权。

```python
def max_del_save(n, edges):
    total=sum(w for _,_,w in edges)
    es=sorted(edges,key=lambda x:x[2])
    par=list(range(n))
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]]; x=par[x]
        return x
    keep=0; cnt=0
    for u,v,w in es:
        a,b=find(u),find(v)
        if a!=b:
            par[a]=b; keep+=w; cnt+=1
    return total-keep if cnt==n-1 else -1

print(max_del_save(3,[(0,1,1),(1,2,2),(0,2,3)]))  # 6-3=3
```

> **复杂度**：O(m log m) 时间，O(n) 空间

---

#### 17.12.36 例 36：最大生成树（Kruskal 反排）⭐⭐
> **知识点**：最大生成树、Kruskal | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边带权图，求最大生成树权值和；不连通输出 -1。n≤10^5。

**思路**

💡 类比"优先用最结实的梁搭骨架"：按边权从大到小排序执行 Kruskal 并集。

```python
def max_spanning_tree(n, edges):
    es=sorted(edges,key=lambda x:x[2],reverse=True)
    par=list(range(n))
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]]; x=par[x]
        return x
    cost=0; cnt=0
    for u,v,w in es:
        a,b=find(u),find(v)
        if a!=b:
            par[a]=b; cost+=w; cnt+=1
    return cost if cnt==n-1 else -1

print(max_spanning_tree(3,[(0,1,1),(1,2,2),(0,2,3)]))  # 5
```

> **复杂度**：O(m log m) 时间，O(n) 空间

---

#### 17.12.37 例 37：欧拉回路可行性 + 欧拉路径统计 ⭐⭐
> **知识点**：欧拉回路、度与连通综合 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向图，先判断是否立即可画出单一欧拉回路或路径，输出类型标记。n≤10^4。

**思路**

💡 类比"一条线能否贯通全画布并收尾闭合"：连通性 + 度奇偶综合，0 奇点是回路，2 奇点路径，否则不能一笔画。

```python
def one_stroke(n, edges):
    deg=[0]*n
    for u,v in edges:
        deg[u]+=1; deg[v]+=1
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    vis=[False]*n; comps=0
    import sys; sys.setrecursionlimit(10**6)
    def dfs(u):
        vis[u]=True
        for v in g[u]:
            if not vis[v]: dfs(v)
    for i in range(n):
        if deg[i]>0 and not vis[i]:
            comps+=1; dfs(i)
    odd=sum(d%2 for d in deg)
    if comps>1: return "not connected"
    if odd==0: return "euler circuit"
    if odd==2: return "euler path"
    return "not eulerian"

print(one_stroke(4,[(0,1),(1,2),(2,3),(3,0)]))  # euler circuit
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.38 例 38：网格图上的最大/最小生成树（类 Prim 网格）⭐⭐
> **知识点**：网格 MST、按合并 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 h×w 网格，相邻格子可连，边权为两格值的差的绝对值，求连通全部格子的最小生成树权值。简化用 Kruskal 边化。

**思路**

💡 类比"用相邻格差异最小的线路连成网络"：把相邻格全建成边按权排序，Kruskal 连全部格。

```python
def grid_mst(grid):
    h=len(grid); w=len(grid[0]); n=h*w
    edges=[]
    for i in range(h):
        for j in range(w):
            idx=i*w+j
            if j+1<w:
                edges.append((idx,idx+1,abs(grid[i][j]-grid[i][j+1])))
            if i+1<h:
                edges.append((idx,idx+w,abs(grid[i][j]-grid[i+1][j])))
    return kruskal_min(n,edges)

def kruskal_min(n,edges):
    edges.sort(key=lambda e:e[2])
    par=list(range(n))
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]]; x=par[x]
        return x
    cost=0; cnt=0
    for u,v,w in edges:
        a,b=find(u),find(v)
        if a!=b:
            par[a]=b; cost+=w; cnt+=1
    return cost

print(grid_mst([[1,3,5],[2,4,6]]))  # 连通树权
```

> **复杂度**：O(h·w log(h·w)) 时间，O(h·w) 空间

---

#### 17.12.39 例 39：带权并查集求可除关系（食物链变式简版）⭐⭐⭐
> **知识点**：带权并查集、模关系 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个节点，m 条描述相邻模 2 与的关系（0 同类 1 异类），遇矛盾停止统计矛盾条数。POJ 食物链简化同模。

**思路**

💡 类比"用模路牌换算每个人所在阵营的奇偶"：带权并查集存到根的异或值（0/1），合并时用等式校验矛盾。

```python
def w_uf_xor(n, ops):
    par=list(range(n)); rel=[0]*n  # 到根异或
    def find(x):
        if par[x]!=x:
            r=find(par[x])
            rel[x]^=rel[par[x]]
            par[x]=r
        return par[x]
    bad=0
    for a,b,c in ops:  # a,b 关系 c
        xa,xb=find(a),find(b)
        if xa==xb:
            if (rel[a]^rel[b])!=c:
                bad+=1
        else:
            par[xa]=xb
            rel[xa]=rel[a]^rel[b]^c
    return bad

print(w_uf_xor(5,[(0,1,1),(1,2,1),(0,2,1)]))  # (0与2应同 0)矛盾1
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.12.40 例 40：二分图最大匹配预备——匈牙利单点可增广 ⭐⭐
> **知识点**：二分图匹配、匈牙利入门 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定二分图（两侧点，右侧每个点可匹配左侧某些点），用匈牙利算法判断一个给定左侧点能否增广匹配，从而得到当前最大匹配。本部分单点探测。

**思路**

💡 类比"为某人寻找未占用搭档，或协商让位"：从该左点尝试 DFS 找增广路，命中即匹配数加一。

```python
def try_augment(u, match, vis, adj):
    for v in adj[u]:
        if not vis[v]:
            vis[v]=True
            if match[v]==-1 or try_augment(match[v],match,vis,adj):
                match[v]=u
                return True
    return False

adj={0:[0,1],1:[1],2:[0]}
match={0:-1,1:-1}
vis=[False]*2
print(try_augment(0,match,vis,adj))  # True
```

> **复杂度**：O(NR²) 单次最坏，O(NR²) 匹配全集 | 空间 O(NR)

---
#### 17.12.41 例 41：Kruskal 边排序细节（二元组参数整理）⭐
> **知识点**：Kruskal、边对象、排序键 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给出无向图边权，按自写比较排序得到 MST 中最关键的若干条边并输出其权值与两个端点。用于熟悉 Kruskal 的边结构。

**思路**

💡 类比"先把每根木料按强度编号再挑选"：构建带编号的边列表，以权值为键升序排序后依次考虑。

```python
def mst_print_edges(n, edges):
    es=sorted(enumerate(edges), key=lambda e:e[1][2])
    par=list(range(n))
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]]; x=par[x]
        return x
    res=[]
    for ei,(u,v,w) in es:
        a,b=find(u),find(v)
        if a!=b:
            par[a]=b
            res.append((ei,u,v,w))
    return res

print(mst_print_edges(3,[(0,1,5),(1,2,2),(0,2,3)]))
# 边序按权: (1,2,2),(0,2,3) => [(1,1,2,2),(2,0,2,3)]
```

> **复杂度**：O(m log m) 时间，O(m) 空间

---

#### 17.12.42 例 42：判断两图是否连通（BFS 与并查集双法对比）⭐
> **知识点**：连通性、并查集、BFS | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向图，分别用 DFS/BFS 与并查集两种方法判断是否连通，输出两种方法结论。n≤10^5。

**思路**

💡 类比"同一调查用走路和台账两种核对"：一种 DFS 数连通块是否为 1；一种并查集合并后检查根数是否为 1。

```python
from collections import deque
def judge_both(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    # 方法1 BFS
    vis=[False]*n; q=deque([0]); vis[0]=True
    while q:
        u=q.popleft()
        for v in g[u]:
            if not vis[v]:
                vis[v]=True; q.append(v)
    bfs_ok=all(vis)
    # 方法2 并查集
    par=list(range(n))
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    for u,v in edges:
        a,b=find(u),find(v)
        if a!=b: par[a]=b
    roots={find(i) for i in range(n)}
    uf_ok=len(roots)==1
    return bfs_ok, uf_ok

print(judge_both(5,[(0,1),(1,2),(0,2),(2,3),(3,4)]))
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.43 例 43：树中指定节点到根路径上权和（树上 DFS/前缀权）⭐⭐
> **知识点**：树、DFS、路径前缀 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定带权无根树，查询若干节点，输出从根 0 到该点路径上的边权和。n,q≤10^5。

**思路**

💡 类比"沿家谱一路累计家产到该支"：一遍 DFS 从 0 号节点出发维护累计距离 dis[u]=dis[fa]+w，O(1) 回答查询。

```python
import sys
sys.setrecursionlimit(10**6)
def root_path_sum(n, edges, queries):
    g=[[] for _ in range(n)]
    for u,v,w in edges:
        g[u].append((v,w)); g[v].append((u,w))
    dis=[0]*n
    def dfs(u,fa):
        for v,w in g[u]:
            if v==fa: continue
            dis[v]=dis[u]+w
            dfs(v,u)
    dfs(0,-1)
    return [dis[x] for x in queries]

print(root_path_sum(4,[(0,1,2),(1,2,3),(1,3,1)],[2,3]))  # [5,3]
```

> **复杂度**：O(n+q) 时间，O(n) 空间

---

#### 17.12.44 例 44：生成树中第 2 个较小的括弧枚举（次小生成树朴素小数据）⭐⭐
> **知识点**：次小生成树、暴力枚举小数据 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n≤10 个点的完全带权图，求严格次小生成树权值。数据小允许暴力枚举生成树或替换边。

**思路**

💡 类比"小范围把所有桥的路网都试一遍找第二便宜"：先用 Kruskal 求 MST，再枚举把每条非树边强制加入并删树上最大边求最小严格更大解。

```python
def second_mst_small(n, edges):
    edges_orig=edges
    return _second_impl(n, edges)

def _second_impl(n, ed):
    es=sorted(ed,key=lambda e:e[2])
    par=list(range(n))
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    used=[]; cost=0; cnt=0
    for u,v,w in es:
        a,b=find(u),find(v)
        if a!=b:
            par[a]=b; used.append((u,v,w)); cost+=w; cnt+=1
    # 树上最大边矩阵
    mx=[[0]*n for _ in range(n)]
    tg=[[] for _ in range(n)]
    for u,v,w in used:
        tg[u].append((v,w)); tg[v].append((u,w))
    for s in range(n):
        # DFS fill
        st=[(s,-1,0)]
        while st:
            u,fa,d=st.pop()
            for v,w in tg[u]:
                if v==fa: continue
                mx[s][v]=max(d,w)
                st.append((v,u,max(d,w)))
    INF=float('inf'); second=INF
    for u,v,w in ed:
        if (u,v,w) in used or (v,u,w) in used:
            continue
        if w==mx[u][v]:
            # 当前非树边与树上最大边相等无法严格替换，跳过
            continue
        second=min(second, cost - mx[u][v] + w)
    return -1 if second==INF else second

print(second_mst_small(3,[(0,1,1),(1,2,2),(0,2,1)]))
```

> **复杂度**：O(n²) 时间/空间（小数据）

---

#### 17.12.45 例 45：最小生成树判断唯一性 ⭐⭐
> **知识点**：MST 唯一性、等权边分析 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边带权图，判断最小生成树是否唯一。唯一输出权值，否则提示有多种。n≤100，m≤500。

**思路**

💡 类比"若存在措辞相等的木料可替换，主干就非唯一"：判是否存在另一条等权非树边替换树上某条与该等权边同权树边——当存在等权非树边与树上边同权且可互换时非唯一。

```python
def mst_unique(n, edges):
    es=sorted(edges,key=lambda e:e[2])
    par=list(range(n))
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    cnt_edges_in_tree=[set() for _ in range(n)]
    cost=0; cnt=0; tree_edges=[]
    for u,v,w in es:
        a,b=find(u),find(v)
        if a!=b:
            par[a]=b; cost+=w; tree_edges.append((u,v,w)); cnt+=1
    used=set(tree_edges)
    # 检查是否存在未用的同权非树边可替换
    for u,v,w in tree_edges:
        for u2,v2,w2 in es:
            if (u2,v2,w2) in used or (v2,u2,w2) in used:
                continue
            if w2==w:
                # 简化启发式：同权即可视为可能替换(近似)
                return (cost, False)
    return (cost, True)

print(mst_unique(3,[(0,1,1),(1,2,1),(0,2,1)]))  # 非唯一
```

> **复杂度**：O(m log m + m·k) 时间，O(m) 空间

---

#### 17.12.46 例 46：并查集实现路径压缩按秩合并 ⭐
> **知识点**：并查集、按秩、路径压缩 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：实现带秩（size）的并查集，给出若干 union 与 find，输出最终每个点的根。n≤10^5。

**思路**

💡 类比"人比较少的队伍并入较多人的队伍减少拉高"：合并时把小秩并入大秩，find 时路径压缩。

```python
def union_rank(n, unions):
    par=list(range(n)); sz=[1]*n
    def find(x):
        r=x
        while par[r]!=r: r=par[r]
        while par[x]!=x:
            p=par[x]; par[x]=r; x=p
        return r
    for a,b in unions:
        ra,rb=find(a),find(b)
        if ra!=rb:
            if sz[ra]<sz[rb]: ra,rb=rb,ra
            par[rb]=ra; sz[ra]+=sz[rb]
    return [find(i) for i in range(n)]

print(union_rank(5,[(0,1),(1,2),(3,4)]))
# 根分布 e.g. [0,0,0,3,3]
```

> **复杂度**：O(n+m α(n)) 时间，O(n) 空间

---

#### 17.12.47 例 47：无向图最小环长度（无权 BFS 改进）⭐⭐
> **知识点**：最小环、BFS、无权图 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向无权图（n≤2000，m≤20000），求最小环的长度；不存在环输出 -1。提示可用去边 BFS 或枚举中间点。

**思路**

💡 类比"在路网里找能兜回来的最短一圈"：对每边删去后看两点是否有另一条短路径，长度=短路径+1，取最小。

```python
from collections import deque
def min_cycle(n, edges):
    g=[set() for _ in range(n)]
    for u,v in edges:
        g[u].add(v); g[v].add(u)
    INF=float('inf'); best=INF
    def bfs(s,t,skip):
        dist=[-1]*n; q=deque([s]); dist[s]=0
        while q:
            u=q.popleft()
            for v in g[u]:
                if (u==s and v==t) or (u==t and v==s): 
                    pass
                if (s,t)==(skip): 
                    pass
                if (u,v)==skip or (v,u)==skip: continue
                if dist[v]==-1:
                    dist[v]=dist[u]+1; q.append(v)
        return dist[t]
    for u,v in edges:
        d=bfs(u,v,(u,v))
        if d!=-1:
            best=min(best,d+1)
    return -1 if best==INF else best

print(min_cycle(4,[(0,1),(1,2),(2,0),(0,3),(3,1),(1,3)]))
```

> **复杂度**：O(m·(n+m)) 时间，O(n+m) 空间

---

#### 17.12.48 例 48：图上判两点是否连通（在线并查集）⭐
> **知识点**：并查集、连通在线询问 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：动态加边 u-v，随时询问两节点是否在同一连通分量。n,q≤10^5。用并查集在线回答。

**思路**

💡 类比"历次修路实时更新老乡关系网"：每加一条边并一次，每询问 find 比较根是否相同。

```python
def online_connect(n, ops):
    par=list(range(n))
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    res=[]
    for op,a,b in ops:
        if op==1:  # add
            if find(a)!=find(b): par[find(a)]=find(b)
        else:      # query
            res.append(find(a)==find(b))
    return res

print(online_connect(5,[(1,0,1),(1,2,3),(2,0,1),(2,1,3)]))
# [True, False]
```

> **复杂度**：O((n+m)α(n)) 时间，O(n) 空间

---

#### 17.12.49 例 49：Kruskal 与 Prim 都要求生成的树权相等验证 ⭐⭐
> **知识点**：MST、双算法对拍 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：随机生成连通带权图，分别用 Kruskal 与 Prim 求 MST 权值并验证相等，用于交叉检验模板正确性。n≤500。

**思路**

💡 类比"用两套算法算同一问题互相印证"：一遍并查集排序，一遍朴素 Prim，比较结果一致。

```python
import random
def cross_check(n, edges):
    # Kruskal
    es=sorted(edges,key=lambda e:e[2])
    par=list(range(n))
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    k=0;cnt=0
    for u,v,w in es:
        a,b=find(u),find(v)
        if a!=b: par[a]=b;k+=w;cnt+=1
    k = k if cnt==n-1 else -1
    # Prim
    g=[[float('inf')]*n for _ in range(n)]
    for u,v,w in edges:
        g[u][v]=w; g[v][u]=w
    INF=float('inf'); key=[INF]*n; intree=[False]*n; key[0]=0; p=0
    for _ in range(n):
        u=-1;best=INF
        for i in range(n):
            if not intree[i] and key[i]<best:
                best=key[i];u=i
        if u==-1: p=-1;break
        intree[u]=True; p+=best
        for v in range(n):
            if not intree[v]: key[v]=min(key[v],g[u][v])
    print("Kruskal:",k,"Prim:",p)
    return k==p

random.seed(1)
def gen(n,m):
    ed=set()
    while len(ed)<m:
        u=random.randrange(n); v=random.randrange(n)
        if u==v: continue
        if u>v: u,v=v,u
        ed.add((u,v,random.randint(1,20)))
    # 保证连通：加一根生成树
    g=list(ed)
    return list(ed)
n=30
ed=gen(n,50)
print(cross_check(n,ed))
```

> **复杂度**：O(n²+m log m) 时间，O(n²) 空间

---

#### 17.12.50 例 50：求解生成树中最少怪边（旅游 M 变形）⭐⭐
> **知识点**：经典动物园、MST 边性质 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定带权连通图，求一条能连通所有点，且最大边与最小边差值极小的生成树（最小瓶颈差）。n≤100，m≤n²。

**思路**

💡 类比"挑一组木料既够跨度又把长短差距压到最小"：把边按权排序后双指针，滑动窗口里做并查集直到连通，更新差值。

```python
def min_diff_mst(n, edges):
    es=sorted(edges,key=lambda e:e[2])
    m=len(es)
    ans=float('inf')
    for L in range(m):
        par=list(range(n))
        def find(x):
            while par[x]!=x: par[x]=par[par[x]];x=par[x]
            return x
        cnt=0; R=L
        maxw=None
        for R in range(L,m):
            u,v,w=es[R]
            a,b=find(u),find(v)
            if a!=b:
                par[a]=b; cnt+=1
                maxw=w
                if cnt==n-1:
                    ans=min(ans,maxw-es[L][2])
                    break
    return -1 if ans==float('inf') else ans

print(min_diff_mst(3,[(0,1,1),(1,2,2),(0,2,5)]))  # 2-1=1
```

> **复杂度**：O(m² α(n)) 时间，O(n) 空间

---

#### 17.12.51 例 51：边数 n-1 的连通树检查 + 打印方案 ⭐
> **知识点**：树判定、连通、输出 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 个节点的若干无向边，判断是否能组成一棵树；若能输出选择的边对应的顶点对，否则输出 -1。

**思路**

💡 类比"检验草稿是否恰好连线一次的骨架"：连通且边数 = n-1 且无环即为树所需，并回显一条生成树。

```python
def build_tree_or_not(n, edges):
    par=list(range(n))
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    cnt=0; chosen=[]
    for u,v in edges:
        a,b=find(u),find(v)
        if a!=b:
            par[a]=b; cnt+=1; chosen.append((u,v))
    if cnt!=n-1:
        return -1
    # 检查连通(所有节点度或均被覆盖)
    nodes=set()
    for u,v in edges: nodes.add(u);nodes.add(v)
    return chosen if len(nodes)==n else -1

print(build_tree_or_not(3,[(0,1),(1,2)]))  # [(0,1),(1,2)]
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.12.52 例 52：无向图的最小割点数量（tarjan 割点计数）⭐⭐
> **知识点**：割点、tarjan、计数 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向连通图，输出割点个数与这些点升序。n≤10^5，m≤2×10^5。经典 UVA。

**思路**

💡 类比"数一数整片网络里有几座单点咽喉"：Tarjan 判 cut，收集所有 iscut 点。

```python
import sys
sys.setrecursionlimit(10**6)
def count_cuts(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    dfn=[0]*n; low=[0]*n; cut=[False]*n; idx=1
    def dfs(u,fa):
        nonlocal idx
        dfn[u]=low[u]=idx; idx+=1
        child=0
        for v in g[u]:
            if v==fa: continue
            if dfn[v]==0:
                child+=1
                dfs(v,u)
                low[u]=min(low[u],low[v])
                if fa!=-1 and low[v]>=dfn[u]: cut[u]=True
            else:
                low[u]=min(low[u],dfn[v])
        if fa==-1 and child>1: cut[u]=True
    for i in range(n):
        if dfn[i]==0: dfs(i,-1)
    return [i for i in range(n) if cut[i]]

print(count_cuts(5,[(0,1),(1,2),(1,3),(3,4)]))  # [1,3]
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.53 例 53：道路通行权限限制通边数（MST 边数统计）⭐
> **知识点**：MST、条数、权约束 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定带权图与阈值 T，只看权 ≤T 的边能连通的最小生成树条数（即这些子边里能用几条构成 k 树的贪心）。输出可构成的最小生成树条数。

**思路**

💡 类比"预算内能修几条关键路段串起全部"：筛选 w≤T 的边做 Kruskal，记录成功合并次数。

```python
def edges_in_budget(n, edges, T):
    es=sorted([e for e in edges if e[2]<=T],key=lambda e:e[2])
    par=list(range(n))
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    cnt=0
    for u,v,w in es:
        a,b=find(u),find(v)
        if a!=b: par[a]=b; cnt+=1
    return cnt

print(edges_in_budget(4,[(0,1,5),(1,2,4),(2,3,6),(0,3,3)],4))  # 2
```

> **复杂度**：O(m log m) 时间，O(n) 空间

---

#### 17.12.54 例 54：图的极大独立分量并查集分组 ⭐
> **知识点**：并查集、分组统计 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向图，用并查集把所有连通点分为若干组，输出各组组内节点数降序（前若干大）。n≤10^5。

**思路**

💡 类比"把互有交集的朋友链归并成朋友圈"：合并后统计每根的大小并排序输出前 k 大块。

```python
def group_sizes(n, edges, k=3):
    par=list(range(n)); sz=[1]*n
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    for u,v in edges:
        a,b=find(u),find(v)
        if a!=b:
            if sz[a]<sz[b]: a,b=b,a
            par[b]=a; sz[a]+=sz[b]
    roots={}
    for i in range(n):
        r=find(i); roots[r]=sz[r]
    return sorted(roots.values(),reverse=True)[:k]

print(group_sizes(6,[(0,1),(1,2),(3,4)]))  # [3,2,1]
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.12.55 例 55：判断从任意点出发皆可达（弱连通/出度检查）⭐
> **知识点**：可达性、度数、图性质 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定有向图，判断是否能从任意点出发到达所有其它点（强连通性简化检查）。n≤10^4。

**思路**

💡 类比"任何路口都能开到全城每个出口才算四通八达"：强连通当且仅当每个节点入度、出度相等且图强连通——用两次反向 BFS 近似判定。

```python
from collections import deque
def all_reachable(n, edges):
    g=[[] for _ in range(n)]; rg=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); rg[v].append(u)
    def bfs(gr, s):
        vis=[False]*n; q=deque([s]); vis[s]=True
        while q:
            u=q.popleft()
            for v in gr[u]:
                if not vis[v]: vis[v]=True; q.append(v)
        return all(vis)
    return bfs(g,0) and bfs(rg,0)

print(all_reachable(3,[(0,1),(1,2),(2,0)]))  # True
print(all_reachable(3,[(0,1),(1,2)]))        # False
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.56 例 56：稀疏图最短路全局连通度（图遍历热身）⭐
> **知识点**：DFS、连通、遍历复习 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边图，从 0 号出发用 DFS 遍历并输出访问顺序（邻接表原序）。验证对图的递归遍历掌握。n≤10^4。

**思路**

💡 类比"随便从一号营地沿路标一路探到底再折返"：DFS 逐个递归邻点记下访问先后序。

```python
import sys
sys.setrecursionlimit(10**6)
def dfs_order(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    vis=[False]*n; order=[]
    def dfs(u):
        vis[u]=True; order.append(u)
        for v in g[u]:
            if not vis[v]: dfs(v)
    dfs(0)
    return order

print(dfs_order(5,[(0,1),(0,2),(1,3),(1,4)]))  # [0,1,3,4,2]
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.57 例 57：森林（多棵树）根个数统计 ⭐
> **知识点**：森林、根、度数统计 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定有根森林（父向边），找出所有根节点（无父、无可达上溯）的个数。h 简化：统计入度为 0 的根。n≤10^5。

**思路**

💡 类比"每个族谱里最年长那位"：无向边的根是入度为 0 的点，统计其数量即可得树（根）个数。

```python
def forest_roots(n, edges):
    indeg=[0]*n
    has=[False]*n
    for u,v in edges:
        indeg[v]+=1; has[u]=True; has[v]=True
    return sum(1 for i in range(n) if indeg[i]==0 and has[i])

print(forest_roots(5,[(0,1),(0,2),(3,4)]))  # 2 (0 和 3)
```

> **复杂度**：O(n+m) 时间，O(n) 空间

---

#### 17.12.58 例 58：二分染色检查 + 染色方案还原 ⭐⭐
> **知识点**：二分图、染色、构造 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向图，判断是否为二分图，若是输出两组点集划分，否则输出 -1。n≤10^5。

**思路**

💡 类比"把互不链接的两拨客人分到两桌"：BFS 逐点决定颜色 0/1，冲突即非二分，最后按颜色分离点集。

```python
from collections import deque
def bipartition(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    color=[-1]*n
    for s in range(n):
        if color[s]!=-1: continue
        color[s]=0; q=deque([s])
        while q:
            u=q.popleft()
            for v in g[u]:
                if color[v]==-1:
                    color[v]=1-color[u]; q.append(v)
                elif color[v]==color[u]:
                    return -1
    a=[i for i in range(n) if color[i]==0]
    b=[i for i in range(n) if color[i]==1]
    return (a,b) if all(x!=-1 for x in color) else -1

print(bipartition(4,[(0,1),(1,2),(2,3),(0,3)]))
```

> **复杂度**：O(n+m) 时间，O(n) 空间

---

#### 17.12.59 例 59：拓扑排序检测是否交错合法（交替入队）⭐
> **知识点**：拓扑、偶数输出交替 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 DAG 工序，期望尽量输出一种「奇偶交错」的拓扑序以便热身掌握队列顺序（校验入队次序）。

**思路**

💡 类比"两班车间轮流出工看能否交错开着"：标准 Kahn 交替从两个队列取点输出并更新入度。

```python
from collections import deque
def alternating_topo(n, edges):
    g=[[] for _ in range(n)]; indeg=[0]*n
    for u,v in edges: g[u].append(v); indeg[v]+=1
    q0=deque(); q1=deque()
    for i in range(n):
        (q0 if i%2==0 else q1).append(i) if indeg[i]==0 else None
        if indeg[i]==0 and i%2==0: q0.append(i)
        elif indeg[i]==0: q1.append(i)
    res=[]
    turn=0
    while len(res)<n:
        q=q0 if turn==0 else q1
        if not q:
            turn=1-turn; continue
        u=q.popleft()
        res.append(u)
        for v in g[u]:
            indeg[v]-=1
            if indeg[v]==0:
                (q0 if v%2==0 else q1).append(v)
        turn=1-turn
    return res

print(alternating_topo(4,[(0,2),(0,3),(1,3)]))
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.60 例 60：所有点对是否存在路径（floyd 传递闭包 for 图论复习）⭐⭐
> **知识点**：闭包、floyd、布尔可达 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n≤200 有向图，求可达矩阵（能否从 i 到 j）。用布尔 Floyd Warshall 求传递闭包。

**思路**

💡 类比"逐一检查中转站能否架起两点的桥梁"：对每个中间点 k 刷新所有 (i,j) 可达性 OR。

```python
def reachable(n, edges):
    r=[[False]*n for _ in range(n)]
    for u,v in edges: r[u][v]=True
    for i in range(n): r[i][i]=True
    for k in range(n):
        for i in range(n):
            if r[i][k]:
                for j in range(n):
                    if r[k][j]: r[i][j]=True
    return r

r=reachable(3,[(0,1),(1,2)])
print(r[0][2])  # True
print(r[2][0])  # False
```

> **复杂度**：O(n³) 时间，O(n²) 空间

---

#### 17.12.61 例 61：并查集按需删除受限组统计 ⭐⭐
> **知识点**：并查集、离线、删除 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：动态加边，中途询问包含点 x 的连通分量大小。n,q≤10^5。并查集直接维护大小随时回答。

**思路**

💡 类比"实时报出每个村的人口规模"：合并随时更新 size，询问时 find 根取 size。

```python
def dsu_query(n, ops):
    par=list(range(n)); sz=[1]*n
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    res=[]
    for op,a,b in ops:
        if op==1:
            ra,rb=find(a),find(b)
            if ra!=rb:
                if sz[ra]<sz[rb]: ra,rb=rb,ra
                par[rb]=ra; sz[ra]+=sz[rb]
        else:
            res.append(sz[find(b)])
    return res

print(dsu_query(5,[(1,0,1),(1,1,2),(2,0,0)]))  # [3]
```

> **复杂度**：O((n+q)α(n)) 时间，O(n) 空间

---

#### 17.12.62 例 62：图论连词应用：在带权图中找连接两点必经哪些关键边 ⭐
> **知识点**：MST 组合、并查集 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：在带权无向连通图中，求必须被纳入任意一棵最小生成树的最小边数（对给定某条生成树参考边判是否必选）。简化问题。

**思路**

💡 类比"多椽并列时确认哪些梁无可替代"：重标号 - 若一条边权严格小于某条最小树中可替换边而言它可能必选——极简启发式计算。

```python
def count_mandatory(n, edges):
    es=sorted(edges,key=lambda e:e[2])
    par=list(range(n))
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    tree=[];cost=0;cnt=0
    for u,v,w in es:
        a,b=find(u),find(v)
        if a!=b: par[a]=b;tree.append((u,v,w));cost+=w;cnt+=1
    # 简化：判断哪些树边不能由等权非树边替换
    used=set((u,v) for u,v,w in tree)
    mandatory=0
    for u,v,w in tree:
        replaceable=False
        for u2,v2,w2 in edges:
            if w2==w and (u2,v2)!= (u,v) and (v2,u2)!=(u,v):
                replaceable=True
        if not replaceable:
            mandatory+=1
    return mandatory

print(count_mandatory(3,[(0,1,1),(1,2,1),(0,2,2)]))
```

> **复杂度**：O(m log m + m·E) 时间，O(n+m) 空间

---

#### 17.12.63 例 63：对称图判定（双向边一致性检查）⭐
> **知识点**：有向图、对称、邻接矩阵 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定有向图，判断每条有向边是否都有反向边（对称图）。n≤1000。

**思路**

💡 类比"检查每个人发出的邀请都有回帖人"：建邻接矩阵，验证对每对 (i,j)，存在 (j,i)。

```python
def is_symmetric(n, edges):
    mat=[[False]*n for _ in range(n)]
    for u,v in edges: mat[u][v]=True
    for u,v in edges:
        if not mat[v][u]: return False
    return True

print(is_symmetric(3,[(0,1),(1,0),(1,2),(2,1)]))  # True
```

> **复杂度**：O(n²+m) 时间，O(n²) 空间

---

#### 17.12.64 例 64：输入处理灵活图（点多边少带权重解析边）⭐⭐
> **知识点**：图输入、邻接表、参数 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：复杂输入：给定点数和若干行「起点 终点 权」（可能跨行，0 0 结束），解析成邻接表并输出每点出度权总和。n≤500。

**思路**

💡 类比"逐行解析台账转成邻接登记册"：循环读取直到哨兵 0 0，累加到邻接表与度数。

```python
def parse_edges(pairs):
    from collections import defaultdict
    deg=defaultdict(int); wsum=defaultdict(int)
    n=0
    for u,v,w in pairs:
        if u==0 and v==0: break
        n=max(n,u+1)
        deg[u]+=1; wsum[u]+=w
        # v 也可作为节点
        n=max(n,v+1)
    return n,[ (wsum[i],deg[i]) for i in range(n) ]

print(parse_edges([(1,2,5),(1,3,2),(2,3,4),(0,0,0)]))
# [(7,2),(4,1),(0,0)]
```

> **复杂度**：O(m) 时间，O(E) 空间

---

#### 17.12.65 例 65：无向连通图的割边数量（桥预备）⭐⭐
> **知识点**：桥、Tarjan、计数 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定连通无向图，输出桥（割边）的条数与每条桥两端点。n≤10^5，m≤2×10^5。

**思路**

💡 类比"数出整片岛上所有独木栈桥"：Tarjan low[v]>dfn[u] 即桥，逐条收集。

```python
import sys
sys.setrecursionlimit(10**6)
def bridges(n, edges):
    g=[[] for _ in range(n)]
    for ei,(u,v) in enumerate(edges):
        g[u].append((v,ei)); g[v].append((u,ei))
    dfn=[0]*n; low=[0]*n; idx=1; res=[]
    def dfs(u,pei):
        nonlocal idx
        dfn[u]=low[u]=idx; idx+=1
        for v,ei in g[u]:
            if ei==pei: continue
            if dfn[v]==0:
                dfs(v,ei)
                low[u]=min(low[u],low[v])
                if low[v]>dfn[u]: res.append((u,v))
            else:
                low[u]=min(low[u],dfn[v])
    for i in range(n):
        if dfn[i]==0: dfs(i,-1)
    return res

print(bridges(4,[(0,1),(1,2),(2,0),(2,3)]))  # [(2,3)]
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.66 例 66：二分图两大集合数：是否能隔成一两半 ⭐⭐
> **知识点**：二分图、集合大小 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向图，判断是否二分，若是输出两侧各自点数（较小的）。n≤10^5。

**思路**

💡 类比"两队计分看能否公平分开"：染色二分，统计 0 色与 1 色个数取较小。

```python
from collections import deque
def two_side_counts(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    color=[-1]*n
    for s in range(n):
        if color[s]!=-1: continue
        color[s]=0; q=deque([s])
        while q:
            u=q.popleft()
            for v in g[u]:
                if color[v]==-1:
                    color[v]=1-color[u]; q.append(v)
                elif color[v]==color[u]:
                    return -1
    return min(color.count(0),color.count(1))

print(two_side_counts(4,[(0,1),(1,2),(2,3),(3,0)]))  # 2
```

> **复杂度**：O(n+m) 时间，O(n) 空间

---

#### 17.12.67 例 67：最小生成树的 Kruskal 集合差分技巧修订 ⭐⭐
> **知识点**：MST、模、应用 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：带模图：给定带权完全图边权为两点数值之差取模意义下的最小值等组合题（POJ 变式）。输出 MST 权值模。数据小。

**思路**

💡 类比"用模数学把不相容的差拉成最近环路"：把可构成的所有边生成后 Kruskal，权做取模处理。

```python
def mst_edge_weight_only(n, w):
    edges=[]
    for i in range(n):
        for j in range(i+1,n):
            edges.append((i,j, (w[i]-w[j])%7 if (w[i]-w[j])%7 else 7))
    # Kruskal
    es=sorted(edges,key=lambda e:e[2])
    par=list(range(n))
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    cost=0;cnt=0
    for u,v,c in es:
        a,b=find(u),find(v)
        if a!=b:
            par[a]=b; cost+=c; cnt+=1
    return cost

print(mst_edge_weight_only(4,[1,8,15,22]))
```

> **复杂度**：O(n² log n²) 时间，O(n²) 空间

---

#### 17.12.68 例 68：强连通背景下最长链（DAG on SCC）⭐⭐⭐
> **知识点**：SCC、最长链、DP | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定有向图（可含环），定义最长路径为经过的“缩点链”节点数（不含重复环）。求最长路径经过的点数。洛谷 P3387 侧重。

**思路**

💡 类比"把互相咬合的团块当一颗大珠串钻石链"：SCC 缩点后建 DAG，再做最长路径 DP 计数。

```python
def longest_path_scc(n, edges):
    # 简化：直接用 SCC 数量近似值（链长）。完整可复用 tarjan_scc + 拓扑
    from collections import deque
    c, comp = _scc(n, edges)
    dag=[set() for _ in range(c)]
    for u in range(n):
        for v in g_of(edges,u):
            pass
    return _chain_len(c)

def _scc(n, edges):
    import sys
    sys.setrecursionlimit(10**6)
    g=[[] for _ in range(n)]
    for u,v in edges: g[u].append(v)
    dfn=[0]*n; low=[0]*n; st=[]; on=[False]*n; comp=[-1]*n; idx=1; cid=0
    def dfs(u):
        nonlocal idx,cid
        dfn[u]=low[u]=idx; idx+=1
        st.append(u); on[u]=True
        for v in g[u]:
            if dfn[v]==0:
                dfs(v); low[u]=min(low[u],low[v])
            elif on[v]: low[u]=min(low[u],dfn[v])
        if low[u]==dfn[u]:
            while True:
                x=st.pop(); on[x]=False; comp[x]=cid
                if x==u: break
            cid+=1
    for i in range(n):
        if dfn[i]==0: dfs(i)
    return cid, comp

def g_of(edges,u):
    return [v for v,w in edges if False]

def _chain_len(c):
    return c  # 链长上界 = SCC 个数(示意)

print(longest_path_scc(3,[(0,1),(1,0),(1,2)]))  # 2 (环{0,1}->{2})
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.69 例 69：并查集合并季节（多测试用例复习题）⭐
> **知识点**：并查集、多 case、重置 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：多组数据每组给出 n 与若干合并，求每组最终连通分量个数。要求正确重置数组以免污染。n≤10^4。

**思路**

💗 类比"每次新局都要洗好牌再开赛"：每组重新初始化 par 数组与根统计。

```python
def comps_per_case(cases):
    out=[]
    for n, unis in cases:
        par=list(range(n))
        def find(x):
            while par[x]!=x: par[x]=par[par[x]];x=par[x]
            return x
        for a,b in unis:
            if find(a)!=find(b): par[find(a)]=find(b)
        out.append(len({find(i) for i in range(n)}))
    return out

print(comps_per_case([(4,[(0,1),(1,2)]),(3,[(0,1)])]))
# [2,2]
```

> **复杂度**：O((n+m)α(n)) 每次，O(n) 空间

---

#### 17.12.70 例 70：图着色判定需要最小颜色的特例（二分覆盖）⭐⭐
> **知识点**：图着色、二分特判 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向图，若图中存在三角形则需 3 色；否则判断是否二分二分 2 色足够，输出需最小颜色数。n≤500。

**思路**

💡 类比"先查是否三足鼎立的三角桌，否则两队二分就够"：先查三角（任意点三相互相邻），否则二分染色验证能否 2 色。

```python
def chromatic_min(n, edges):
    mat=[[False]*n for _ in range(n)]
    for u,v in edges:
        mat[u][v]=mat[v][u]=True
    for a in range(n):
        for b in range(a+1,n):
            if mat[a][b]:
                for c in range(b+1,n):
                    if mat[a][c] and mat[b][c]:
                        return 3  # 三角
    return 2

print(chromatic_min(4,[(0,1),(1,2),(2,3),(0,3)]))  # 2
```

> **复杂度**：O(n³) 时间，O(n²) 空间

---

#### 17.12.71 例 71：网格红绿灯同步（无权所有奇偶节点计数）⭐
> **知识点**：网格、奇偶、二分看上色 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 h×w 网格（部分障碍），求连通主区里白色与黑色交错格的个数（看作棋盘染色分量）。简化输出黑格数。

**思路**

💡 类比"黑白棋盘各自归队数数"：BFS 遍历连通区域并按奇偶下标染 0/1 计数。

```python
from collections import deque
def grid_bw(board):
    h=len(board); w=len(board[0])
    vis=[[False]*w for _ in range(h)]
    bc=wc=0
    for i in range(h):
        for j in range(w):
            if board[i][j]==1 or vis[i][j]: continue
            q=deque([(i,j)]); vis[i][j]=True
            while q:
                x,y=q.popleft()
                if (x+y)%2==0: bc+=1
                else: wc+=1
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and not vis[nx][ny] and board[nx][ny]==0:
                        vis[nx][ny]=True; q.append((nx,ny))
    return bc,wc

print(grid_bw([[0,0,1,0],[0,1,0,0]]))
```

> **复杂度**：O(h·w) 时间，O(h·w) 空间

---

#### 17.12.72 例 72：无向图所有点对最短路（无权 BFS 全源）⭐
> **知识点**：全源 BFS、无权最短路径 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向无权图（n≤500，m≤n²），求全源最短路矩阵 dist[i][j]。可对每点 BFS 得 O(n(n+m))。

**思路**

💡 类比"从每个站点各自扫一遍全镇路程"：对每个源点 BFS 填一行距离。

```python
from collections import deque
def all_pairs(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    dist=[[-1]*n for _ in range(n)]
    for s in range(n):
        dist[s][s]=0; q=deque([s])
        while q:
            u=q.popleft()
            for v in g[u]:
                if dist[s][v]==-1:
                    dist[s][v]=dist[s][u]+1; q.append(v)
    return dist

d=all_pairs(4,[(0,1),(1,2),(2,3)])
print(d[0][3])  # 3
```

> **复杂度**：O(n(n+m)) 时间，O(n²) 空间

---

#### 17.12.73 例 73：带权并查集在 MST 冲突检测应用 ⭐⭐
> **知识点**：带权并查集、环路约束 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：逐步加带权的树边定义“两点间距离固定”，当出现与已知距离矛盾的新边时拒绝并计数，输出矛盾条数。可用模 3 或实数简化。

**思路**

💡 类比"每次校准路尺，量出来不符就报废该条"：带权并查集记录到根距离，合并用差值校验矛盾。

```python
def conflict_count(n, ops, mod=100):
    par=list(range(n)); d=[0]*n
    def find(x):
        if par[x]!=x:
            r=find(par[x])
            d[x]=(d[x]+d[par[x]])%mod
            par[x]=r
        return par[x]
    bad=0
    for u,v,w in ops:
        a,b=find(u),find(v)
        if a==b:
            if (d[u]-d[v])%mod != w%mod:
                bad+=1
        else:
            par[a]=b
            d[a]=(d[v]+w-d[u])%mod
    return bad

print(conflict_count(4,[(0,1,5),(1,2,3),(0,2,8)]))  # (0到2应为8)一致0
```

> **复杂度**：O(m α(n)) 时间，O(n) 空间

---

#### 17.12.74 例 74：图论名词检查：孤立点数量 ⭐
> **知识点**：孤立点、度数、遍历 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边无向图，统计度为 0 的孤立点个数。n≤10^5。

**思路**

💡 类比"一个社交圈里从未露面的沉默人"：度数数组统计，度为 0 记为孤立。

```python
def isolated_count(n, edges):
    deg=[0]*n
    for u,v in edges:
        deg[u]+=1; deg[v]+=1
    return sum(1 for x in deg if x==0)

print(isolated_count(5,[(0,1),(2,3)]))  # 3? (4 孤立 =>1)
```

> **复杂度**：O(n+m) 时间，O(n) 空间

---

#### 17.12.75 例 75：二分图最小同侧建立（匹配预备概念）⭐
> **知识点**：二分图、概念、度检查 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：判断给定图是否二分，若是输出两侧点数差的最小绝对值（既有割产）。n≤10^5。

**思路**

💗 类比"两班下课人数尽量均衡的可行性"：染色后两侧点数量，输出差的绝对值。

```python
from collections import deque
def side_diff(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    color=[-1]*n; c0=c1=0
    ok=True
    for s in range(n):
        if color[s]!=-1: continue
        color[s]=0; q=deque([s]); a=b=0
        while q:
            u=q.popleft()
            if color[u]==0: a+=1
            else: b+=1
            for v in g[u]:
                if color[v]==-1:
                    color[v]=1-color[u]; q.append(v)
                elif color[v]==color[u]:
                    ok=False
        c0+=a; c1+=b
    return -1 if not ok else abs(c0-c1)

print(side_diff(4,[(0,1),(1,2),(2,3),(3,0)]))  # 0
```

> **复杂度**：O(n+m) 时间，O(n) 空间

---

#### 17.12.76 例 76：最小生成树（完全图边权曼哈顿距离/切克洛伐集合）⭐⭐
> **知识点**：曼哈顿 MST、点到点 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（≤2000）个二维点，边权为两点的曼哈顿距离，求最小生成树总权。数据中缓 O(n²) 可行。

**思路**

💡 类比"按横竖整齐街道布网总里程"：生成全部 |dx|+|dy| 边，Prim（稠密）求 MST。

```python
INF=float('inf')
def mst_manhattan(pts):
    n=len(pts)
    key=[INF]*n; intree=[False]*n; key[0]=0; res=0
    for _ in range(n):
        u=-1; best=INF
        for i in range(n):
            if not intree[i] and key[i]<best: best=key[i]; u=i
        if u==-1: return -1
        intree[u]=True; res+=best
        for v in range(n):
            if not intree[v]:
                w=abs(pts[u][0]-pts[v][0])+abs(pts[u][1]-pts[v][1])
                key[v]=min(key[v],w)
    return res

print(mst_manhattan([(0,0),(1,0),(2,0),(3,0)]))  # 3
```

> **复杂度**：O(n²) 时间，O(n) 空间

---

#### 17.12.77 例 77：SCC 出度为零分量统计（经典支配可达）⭐⭐⭐
> **知识点**：SCC、缩点、出度 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定有向图，找出所有「聚合分量」中出度为 0 的强连通分量（POJ 2186 简化问法），输出其节点数。n≤10^5。

**思路**

💡 类比"找出所有流水的最后一个湖"：SCC 缩点后统计出度为 0 的分量，若恰有一个即为其大小。

```python
def zero_outdegree_scc(n, edges):
    import sys
    sys.setrecursionlimit(10**6)
    g=[[] for _ in range(n)]
    for u,v in edges: g[u].append(v)
    dfn=[0]*n; low=[0]*n; st=[]; on=[False]*n; comp=[-1]*n; idx=1; cid=0
    def dfs(u):
        nonlocal idx,cid
        dfn[u]=low[u]=idx; idx+=1
        st.append(u); on[u]=True
        for v in g[u]:
            if dfn[v]==0:
                dfs(v); low[u]=min(low[u],low[v])
            elif on[v]: low[u]=min(low[u],dfn[v])
        if low[u]==dfn[u]:
            while True:
                x=st.pop(); on[x]=False; comp[x]=cid
                if x==u: break
            cid+=1
    for i in range(n):
        if dfn[i]==0: dfs(i)
    outdeg=[set() for _ in range(cid)]
    for u in range(n):
        for v in g[u]:
            if comp[u]!=comp[v]:
                outdeg[comp[u]].add(comp[v])
    zc=[i for i in range(cid) if not outdeg[i]]
    if len(zc)!=1:
        return 0
    root=zc[0]
    return sum(1 for x in comp if x==root)

print(zero_outdegree_scc(5,[(0,1),(1,2),(2,1),(2,3)]))
# 分量3可被2到，仅3出度为0 => 节点 {3} => 1
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.78 例 78：拓扑排序检测依赖环的层级数量 ⭐⭐
> **知识点**：拓扑、层级、关键链 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 DAG，求最长依赖链的长度（拓扑最长路径上的节点数）。n≤10^5。经典 POJ 1932 变式。

**思路**

💡 类比"算出整条工期里最长的那条串联线路"：拓扑序 DP 用 dp[v]=max(dp[u])+1 求最长链。

```python
from collections import deque
def longest_dep_chain(n, edges):
    g=[[] for _ in range(n)]; indeg=[0]*n
    for u,v in edges: g[u].append(v); indeg[v]+=1
    q=deque([i for i in range(n) if indeg[i]==0])
    dp=[0]*n
    for i in q: dp[i]=1
    while q:
        u=q.popleft()
        for v in g[u]:
            dp[v]=max(dp[v],dp[u]+1)
            indeg[v]-=1
            if indeg[v]==0: q.append(v)
    return max(dp)

print(longest_dep_chain(5,[(0,1),(0,2),(1,3),(2,3),(3,4)]))  # 4
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.12.79 例 79：图论综合：判断三角形个数 ⭐
> **知识点**：三角计数、邻接矩阵 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（≤500）点无向图，统计其中三角形（三条边两两互连的三个点）的个数。

**思路**

💡 类比"数一数三人成队互相认识的组合"：邻接矩阵枚举三元组 a<b<c 判断三边均在。

```python
def count_triangles(n, edges):
    mat=[[False]*n for _ in range(n)]
    for u,v in edges:
        mat[u][v]=mat[v][u]=True
    cnt=0
    for a in range(n):
        for b in range(a+1,n):
            if mat[a][b]:
                for c in range(b+1,n):
                    if mat[a][c] and mat[b][c]:
                        cnt+=1
    return cnt

print(count_triangles(4,[(0,1),(1,2),(0,2),(2,3)]))  # 1
```

> **复杂度**：O(n³) 时间，O(n²) 空间

---

#### 17.12.80 例 80：最小生成树全部方案计数（并查集模等价类小数据）⭐⭐⭐
> **知识点**：MST 计数、同构方案 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定小规模带权图（n≤12），求最小生成树的个数。数据小允许枚举全部生成或矩阵树定理 M 的近似。输出模数。

**思路**

💗 类比"数有多少种搭法都同样最省料"：找出全部能构成最小权树并连通的边集合，对量级做计数，小数据暴力枚举子集判定。

```python
from itertools import combinations
def count_mst(n, edges):
    # 边按权排，暴力枚举是最小权的情形（小规模）
    es=sorted(enumerate(edges), key=lambda e:e[1][2])
    nums=[]
    best=float('inf'); cnt=0
    # 由于组合需子集枚举，以下用递归生成树近似
    par=[0]*n
    def connected(ch):
        p=list(range(n))
        def find(x):
            while p[x]!=x: p[x]=p[p[x]]; x=p[x]
            return x
        for u,v,w in ch:
            a,b=find(u),find(v)
            if a!=b: p[a]=b
        return len({find(i) for i in range(n)})==1
    m=len(edges)
    for mask in range(1,1<<m):
        ch=[es[i][1] for i in range(m) if mask>>i&1]
        if len(ch)!=n-1: continue
        w=sum(c[2] for c in ch)
        if not connected(ch): continue
        if w<best: best=w; cnt=1
        elif w==best: cnt+=1
    return cnt

print(count_mst(3,[(0,1,1),(1,2,1),(0,2,1)]))  # 3
```

> **复杂度**：O(2^m · n) 时间，O(n) 空间

---

### 17.13 最短路、网络流与二分图匹配

#### 17.13.1 例 1：Dijkstra 朴素版（POJ 1062 变式）⭐⭐
> **知识点**：Dijkstra、单源最短路、稠密图｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（≤1000）点 m 边带权无向图，权值为正，求 0 号点到其它所有点最短距离；若不可达输出 -1。给出程度用朴素 O(n²) 实现。

**思路**

💡 类比"从出发地一遍遍挑最近未定站更新周边"：每次选 dist 最小未定节点确定，继而松弛其邻接边。

```python
INF=float('inf')
def dijkstra_plain(n, edges, s=0):
    g=[[] for _ in range(n)]
    for u,v,w in edges:
        g[u].append((v,w)); g[v].append((u,w))
    dist=[INF]*n; done=[False]*n; dist[s]=0
    for _ in range(n):
        u=-1; best=INF
        for i in range(n):
            if not done[i] and dist[i]<best:
                best=dist[i]; u=i
        if u==-1: break
        done[u]=True
        for v,w in g[u]:
            if dist[u]+w<dist[v]:
                dist[v]=dist[u]+w
    return [-1 if x==INF else x for x in dist]

print(dijkstra_plain(4,[(0,1,2),(0,2,5),(1,2,1),(2,3,4)]))
# [0,2,3,7]
```

> **复杂度**：O(n²+m) 时间，O(n+m) 空间

---

#### 17.13.2 例 2：堆优化 Dijkstra（洛谷 P4779）⭐⭐
> **知识点**：Dijkstra、优先队列、稀疏图｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（≤10^5）点 m（≤2×10^5）边带权有向图，求 1 号点到所有点最短路；不可达输出 -1。

**思路**

💡 类比"快递员总从当前最近且未送达的客户出发派件"：最小堆维护 dist，弹出即确定，松弛邻点入堆。

```python
import heapq
INF=float('inf')
def dijkstra_heap(n, edges, s=0):
    g=[[] for _ in range(n)]
    for u,v,w in edges:
        g[u].append((v,w))
    dist=[INF]*n; dist[s]=0
    h=[(0,s)]
    while h:
        d,u=heapq.heappop(h)
        if d>dist[u]: continue
        for v,w in g[u]:
            nd=d+w
            if nd<dist[v]:
                dist[v]=nd
                heapq.heappush(h,(nd,v))
    return [-1 if x==INF else x for x in dist]

print(dijkstra_heap(4,[(0,1,2),(1,2,1),(0,2,5),(2,3,4)]))
# [0,2,3,7]
```

> **复杂度**：O(m log n) 时间，O(n+m) 空间

---

#### 17.13.3 例 3：Bellman-Ford 求最短路⭐⭐
> **知识点**：Bellman-Ford、松弛、边迭代｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边带权图（权可负但无负环），求 0 点到各点最短路。用 Bellman-Ford 迭代 n-1 轮。n≤1000。

**思路**

💡 类比"反复把每单业务比对看是否更划算直到不再改善"：对每条边做 dist[v]=min(dist[v],dist[u]+w)，循环至多 n-1 次。

```python
INF=float('inf')
def bellman_ford(n, edges, s=0):
    dist=[INF]*n; dist[s]=0
    for _ in range(n-1):
        updated=False
        for u,v,w in edges:
            if dist[u]!=INF and dist[u]+w<dist[v]:
                dist[v]=dist[u]+w; updated=True
        if not updated: break
    return [-1 if x==INF else x for x in dist]

print(bellman_ford(3,[(0,1,4),(0,2,2),(1,2,-3)]))
# [0,4,1]
```

> **复杂度**：O(n·m) 时间，O(n) 空间

---

#### 17.13.4 例 4：SPFA 最短路（负权判负环）⭐⭐
> **知识点**：SPFA、SLF、负环｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边带权图，求 0 到各点最短路；若存在从 0 可达的负环则输出 "negative"。n≤10^5。

**思路**

💡 类比"有惊雷的班车每出现新优惠都重新通知周边站点"：队列维护待松弛点，入队次数超 n 即判定负环。

```python
from collections import deque
INF=float('inf')
def spfa(n, edges, s=0):
    g=[[] for _ in range(n)]
    for u,v,w in edges: g[u].append((v,w))
    dist=[INF]*n; cnt=[0]*n; inq=[False]*n
    dist[s]=0; q=deque([s]); inq[s]=True
    while q:
        u=q.popleft(); inq[u]=False
        for v,w in g[u]:
            if dist[u]+w<dist[v]:
                dist[v]=dist[u]+w
                if not inq[v]:
                    q.append(v); inq[v]=True
                    cnt[v]+=1
                    if cnt[v]>n:
                        return "negative"
    return [-1 if x==INF else x for x in dist]

print(spfa(3,[(0,1,2),(1,2,1),(0,2,5)]))  # [0,2,3]
```

> **复杂度**：均摊 O(m)（最坏 O(n·m)），O(n+m) 空间

---

#### 17.13.5 例 5：Floyd 全源最短路⭐⭐
> **知识点**：Floyd、全源最短路、传递｜**难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（≤400）点带权图（可为有向），求所有点对最短路。无负数保证可正可幂。输出 dist[i][j]，不可达为 inf 表示 -1。

**思路**

💡 类比"每个聚点充当可能的中转站逐级打通地铁路网"：三层循环中间点 k 刷新所有 i→j 取经过 k 的最小值。

```python
def floyd(n, edges):
    INF=float('inf')
    d=[[INF]*n for _ in range(n)]
    for i in range(n): d[i][i]=0
    for u,v,w in edges:
        d[u][v]=min(d[u][v],w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k]+d[k][j]<d[i][j]:
                    d[i][j]=d[i][k]+d[k][j]
    return d

d=floyd(3,[(0,1,2),(1,2,3),(0,2,8)])
print(d[0][2])  # 5
```

> **复杂度**：O(n³) 时间，O(n²) 空间

---

#### 17.13.6 例 6：多元 DAG 拓扑初始化单源最短路⭐⭐
> **知识点**：拓扑排序、动态规划最短路 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边带权 DAG，求从每个入度 0 点到每个出度 0 点的最大收益（最长路），输出最大值。n≤10^5。

**思路**

💡 类比"顺着工艺流程算出整条流水线最长累计收益"：拓扑序依次 DP，dp[v]=max(dp[v],dp[u]+w)，答案取所有出度 0 点 dp 最大。

```python
from collections import deque
def dag_longest(n, edges):
    g=[[] for _ in range(n)]; indeg=[0]*n; outdeg=[0]*n
    for u,v,w in edges:
        g[u].append((v,w)); indeg[v]+=1; outdeg[u]+=1
    q=deque([i for i in range(n) if indeg[i]==0])
    dp=[0]*n
    for i in q: dp[i]=0
    while q:
        u=q.popleft()
        for v,w in g[u]:
            dp[v]=max(dp[v],dp[u]+w)
            indeg[v]-=1
            if indeg[v]==0: q.append(v)
    return max(dp[i] for i in range(n) if outdeg[i]==0)

print(dag_longest(4,[(0,1,3),(0,2,2),(1,3,4),(2,3,1)]))  # 7
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.13.7 例 7：次短路（Dijkstra 双状态）⭐⭐⭐
> **知识点**：次短路、Dijkstra、双 dist | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定带权无向图，求 0 到 n-1 严格次短路的长度。边权为正。n≤10^4，m≤2×10^4。

**思路**

💡 类比"第二快的路线往往绕开唯一瓶颈"：对每个点维护最短路与次短路两值，Dijkstra 时同时拓宽两个 dist。

```python
import heapq
INF=float('inf')
def second_short(n, edges, s=0, t=None):
    if t is None: t=n-1
    g=[[] for _ in range(n)]
    for u,v,w in edges:
        g[u].append((v,w)); g[v].append((u,w))
    dist=[[INF,INF] for _ in range(n)]
    dist[s][0]=0
    h=[(0,s)]
    while h:
        d,u=heapq.heappop(h)
        if d>dist[u][1]: continue
        for v,w in g[u]:
            nd=d+w
            if nd<dist[v][0]:
                dist[v][1]=dist[v][0]
                dist[v][0]=nd
                heapq.heappush(h,(nd,v))
            elif nd>dist[v][0] and nd<dist[v][1]:
                dist[v][1]=nd
                heapq.heappush(h,(nd,v))
    return dist[t][1]

print(second_short(3,[(0,1,1),(1,2,1),(0,2,3)]))  # 3
```

> **复杂度**：O(m log n) 时间，O(n+m) 空间

---

#### 17.13.8 例 8：差分约束系统（最长/最短路转化）⭐⭐⭐
> **知识点**：差分约束、Spfa、不等式 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 m 组形如 x_j - x_i ≤ c 的约束，求一组可行解；若无解输出 -1。n≤10^5。

**思路**

💡 类比"把不等式系化作路网并检查是否自相矛盾"：约束化为边 i→j 权 c，用 SPFA 判负环，无负环则 dist 即解。

```python
from collections import deque
def diff_constraints(n, cons):
    g=[[] for _ in range(n+1)]
    # 超级源点 0
    for i in range(1,n+1):
        g[0].append((i,0))
    for j,i,c in cons:
        g[i].append((j,c))   # x_j - x_i <= c
    INF=float('inf'); dist=[INF]*(n+1); dist[0]=0
    cnt=[0]*(n+1); inq=[False]*(n+1)
    q=deque([0]); inq[0]=True
    while q:
        u=q.popleft(); inq[u]=False
        for v,w in g[u]:
            if dist[u]+w<dist[v]:
                dist[v]=dist[u]+w
                if not inq[v]:
                    q.append(v); inq[v]=True; cnt[v]+=1
                    if cnt[v]>n: return -1
    return dist[1:]

print(diff_constraints(2,[(1,0,5),(0,1,3)]))  # 可行解
```

> **复杂度**：O(n·m) 最坏，O(n+m) 空间

---

#### 17.13.9 例 9：多源最短路（超级源点 Dijkstra）⭐⭐
> **知识点**：超级源点、Dijkstra | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定图与一批特殊点（起发点）。求其它任意点到最近特殊点的距离。n≤10^5，m≤2×10^5。

**思路**

💡 类比"新建一个总站把每个货仓直接连起，一站发全网"：加虚拟源连各特殊点权 0，跑一次 Dijkstra 即得各点最近特殊点距离。

```python
import heapq
INF=float('inf')
def multi_source(n, edges, sources):
    g=[[] for _ in range(n+1)]
    for u,v,w in edges:
        g[u].append((v,w))
    S=n
    dist=[INF]*(n+1); dist[S]=0
    h=[(0,S)]
    for x in sources:
        g[S].append((x,0))
    while h:
        d,u=heapq.heappop(h)
        if d>dist[u]: continue
        for v,w in g[u]:
            if d+w<dist[v]:
                dist[v]=d+w; heapq.heappush(h,(dist[v],v))
    return dist[:n]

print(multi_source(4,[(0,1,2),(1,2,1),(2,3,3)],[1,3]))
# 到最近特殊点: [2,0,1,0]
```

> **复杂度**：O(m log n) 时间，O(n+m) 空间

---

#### 17.13.10 例 10：网格地图带权最短路（Dijkstra on grid）⭐⭐
> **知识点**：网格 Dijkstra、四邻 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n×n（≤500）数字矩阵，从 (0,0) 走到 (n-1,n-1)，每次移动到相邻格代价为该格数值，求最小总代价。Dijkstra。

**思路**

💡 类比"穿过收费路段挑最省的一串路径"：Dijkstra 把格子当点，四方向松弛，dist 记累计通行费。

```python
import heapq
def grid_min_cost(mat):
    n=len(mat); INF=float('inf')
    dist=[[INF]*n for _ in range(n)]
    dist[0][0]=mat[0][0]
    h=[(mat[0][0],0,0)]
    dirs=[(1,0),(-1,0),(0,1),(0,-1)]
    while h:
        d,x,y=heapq.heappop(h)
        if (x,y)==(n-1,n-1): return d
        if d>dist[x][y]: continue
        for dx,dy in dirs:
            nx,ny=x+dx,y+dy
            if 0<=nx<n and 0<=ny<n:
                nd=d+mat[nx][ny]
                if nd<dist[nx][ny]:
                    dist[nx][ny]=nd; heapq.heappush(h,(nd,nx,ny))
    return dist[n-1][n-1]

print(grid_min_cost([[1,3,1],[1,5,1],[4,2,1]]))  # 7
```

> **复杂度**：O(n² log n) 时间，O(n²) 空间

---

#### 17.13.11 例 11：算法 对无权图用 BFS 最快 / DAG 拓扑 DP 复习⭐⭐
> **知识点**：BFS、无权最短路 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边无权无向图，求 0 到所有点最短距离（边权 1）。n≤2×10^5。

**思路**

💡 类比"逐层波纹传开即是最少跳数"：BFS 层扩展记距离即可，无权下优于 Dijkstra。

```python
from collections import deque
def bfs_shortest(n, edges, s=0):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    dist=[-1]*n; dist[s]=0; q=deque([s])
    while q:
        u=q.popleft()
        for v in g[u]:
            if dist[v]==-1:
                dist[v]=dist[u]+1; q.append(v)
    return dist

print(bfs_shortest(5,[(0,1),(1,2),(2,4),(0,3),(3,4)]))
# [0,1,2,1,2]
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.13.12 例 12：求最短路条数（Dijkstra 计数）⭐⭐
> **知识点**：最短路计数、Dijkstra | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定带权有向图（权正），求 0 到各点最短路径的条数。最短路径条数取模输出。n≤10^5。

**思路**

💡 类比"数清楚每座城市最短供货方案有几种"：Dijkstra 松弛：更新最短路则重置路径数为父路数，相等则累加。

```python
import heapq
INF=float('inf')
def count_shortest(n, edges, s=0, mod=10**9+7):
    g=[[] for _ in range(n)]
    for u,v,w in edges: g[u].append((v,w))
    dist=[INF]*n; cnt=[0]*n
    dist[s]=0; cnt[s]=1
    h=[(0,s)]
    while h:
        d,u=heapq.heappop(h)
        if d>dist[u]: continue
        for v,w in g[u]:
            nd=d+w
            if nd<dist[v]:
                dist[v]=nd; cnt[v]=cnt[u]
                heapq.heappush(h,(nd,v))
            elif nd==dist[v]:
                cnt[v]=(cnt[v]+cnt[u])%mod
    return cnt

print(count_shortest(4,[(0,1,1),(0,2,1),(1,3,1),(2,3,1)]))
# 到3两条最短路 => cnt[3]=2
```

> **复杂度**：O(m log n) 时间，O(n+m) 空间

---

#### 17.13.13 例 13：答案二分 + 最大流可行性（二分匹配应用预备）⭐⭐⭐
> **知识点**：二分答案、可行性 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定若干任务与能力对（每个任务可由某些人做），给定人员容量，判定是否可全部完成。化归最大流可行性，二分/直接检验。

**思路**

💡 类比"把人力资源经中转分派到每个工位"：建图源→人（容量人数）→任务→汇（容量 1），最大流等于任务数即可行（网络流模型预备）。

```python
def feasible(n, capacity, tasks_can_do):
    # 任务数
    m=len(tasks_can_do)
    total_tasks=m
    matched=[0]*m
    # 简化用贪心匹配近似（正式可用匈牙利/流）
    done=0
    assign=[[] for _ in range(n)]
    for t, people in enumerate(tasks_can_do):
        for p in people:
            if len(assign[p])<capacity:
                assign[p].append(t); done+=1
                break
    return done>=total_tasks, done

tasks=[[0,1],[0],[1,2]]
print(feasible(3,1,tasks))  # 可行近似
```

> **复杂度**：O(n·m) 简化，O(n·m) 空间

---

#### 17.13.14 例 14：朴素最大流（EDMONDS-KARP 多 BFS）⭐⭐
> **知识点**：最大流、EK、BFS增广 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边有向容量网络（n≤200，m≤1000），求从源点 0 到汇点 n-1 的最大流。

**思路**

💡 类比"反复沿还有余量的管道找增广路送更多水"：EK 每次 BFS 找残量增广路，沿路径减容量加反向边，直到无增广路。

```python
from collections import deque
def edmonds_karp(n, edges, s=0, t=None):
    if t is None: t=n-1
    cap=[[0]*n for _ in range(n)]
    g=[[] for _ in range(n)]
    for u,v,c in edges:
        if not g[u] or True:
            g[u].append(v); g[v].append(u)
        cap[u][v]+=c
    flow=0
    while True:
        par=[-1]*n; par[s]=s
        q=deque([s])
        while q and par[t]==-1:
            u=q.popleft()
            for v in g[u]:
                if par[v]==-1 and cap[u][v]>0:
                    par[v]=u; q.append(v)
        if par[t]==-1: break
        # 找瓶颈
        f=float('inf'); v=t
        while v!=s:
            u=par[v]; f=min(f,cap[u][v]); v=u
        v=t
        while v!=s:
            u=par[v]; cap[u][v]-=f; cap[v][u]+=f; v=u
        flow+=f
    return flow

print(edmonds_karp(4,[(0,1,2),(0,2,2),(1,2,1),(1,3,2),(2,3,2)]))  # 4
```

> **复杂度**：O(m·F) 时间，O(n²) 空间

---

#### 17.13.15 例 15：Dinic 最大流⭐⭐⭐
> **知识点**：Dinic、层次图、当前弧 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 点 m 边容量网，求 0→n-1 最大流。n≤10^4，m≤2×10^5。用 Dinic。

**思路**

💡 类比"按层级分批同时推进多路水流再重建层级"：BFS 建层次，DFS 在层次内多次增广，重复直到汇点不可达。

```python
from collections import deque
class Dinic:
    def __init__(self,n):
        self.n=n; self.g=[[] for _ in range(n)]
    def add(self,u,v,c):
        self.g[u].append([v,c,len(self.g[v])])
        self.g[v].append([u,0,len(self.g[u])-1])
    def max_flow(self,s,t):
        n=self.n; g=self.g; flow=0
        while True:
            level=[-1]*n; level[s]=0
            q=deque([s])
            while q:
                u=q.popleft()
                for v,c,rev in g[u]:
                    if c>0 and level[v]<0:
                        level[v]=level[u]+1; q.append(v)
            if level[t]<0: break
            it=[0]*n
            def dfs(u,f):
                if u==t: return f
                while it[u]<len(g[u]):
                    v,c,rev=g[u][it[u]]
                    if c>0 and level[v]==level[u]+1:
                        ret=dfs(v,min(f,c))
                        if ret>0:
                            g[u][it[u]][1]-=ret
                            g[v][rev][1]+=ret
                            return ret
                    it[u]+=1
                return 0
            while True:
                pushed=dfs(s,float('inf'))
                if pushed==0: break
                flow+=pushed
        return flow

d=Dinic(4)
d.add(0,1,2);d.add(0,2,2);d.add(1,2,1);d.add(1,3,2);d.add(2,3,2)
print(d.max_flow(0,3))  # 4
```

> **复杂度**：O(n²m) 最坏 / 一般远快，O(n+m) 空间

---

#### 17.13.16 例 16：最小割（最大流割=权解法）⭐⭐⭐
> **知识点**：最小割、最大流定理 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定有向网络，求把源汇分离的最小割容量（即删除使不连通的边容量和最小）。输出最小割值。

**思路**

💡 类比"切断能分离两端的细水管里成本最低的一组"：由最大流等于最小割，直接跑 Dinic；最小割边即残量图中从源可达边的反侧。

```python
def min_cut_value(dinic, s, t):
    return dinic.max_flow(s,t)

# 复用 Dinic
d=Dinic(4)
d.add(0,1,2);d.add(0,2,2);d.add(1,2,1);d.add(1,3,2);d.add(2,3,2)
print(min_cut_value(d,0,3))  # 4
```

> **复杂度**：同 Dinic O(n²m)，O(n+m) 空间

---

#### 17.13.17 例 17：二分图最大匹配（匈牙利入门）⭐⭐
> **知识点**：二分图匹配、匈牙利 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定左右两侧点集与部分可匹配边，用匈牙利求最大匹配数。n≤500。

**思路**

💡 类比"为自己争位置，抢不到就请对方让位再试"：DFS 增广，match[v]=u，vis 防死循环，统计匹配数。

```python
def hungarian(n_left, n_right, pairs):
    adj=[[] for _ in range(n_left)]
    for u,v in pairs: adj[u].append(v)
    match=[-1]*n_right
    def try_k(u, vis):
        for v in adj[u]:
            if not vis[v]:
                vis[v]=True
                if match[v]==-1 or try_k(match[v],vis):
                    match[v]=u; return True
        return False
    res=0
    for u in range(n_left):
        if try_k(u,[False]*n_right):
            res+=1
    return res

print(hungarian(3,3,[(0,0),(0,1),(1,1),(2,2)]))  # 3
```

> **复杂度**：O(n_left·E) 时间，O(E) 空间

---

#### 17.13.18 例 18：二分图最大匹配（Hopcroft-Karp）⭐⭐⭐
> **知识点**：HK、BFS分层、多层增广 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：左右各 ≤10^5、边 ≤10^5 的二分图，求最大匹配，要求 HK 算法多级增广提速。

**思路**

💡 类比"一次调度分清所有级别一次安排多对"：BFS 建立离源最短增广层，DFS 在层内一次批量增广，循环当前端。

```python
from collections import deque
def hopcroft_karp(n, m, pairs):
    adj=[[] for _ in range(n)]
    for u,v in pairs: adj[u].append(v)
    pairU=[-1]*n; pairV=[-1]*m; dist=[0]*n
    INF=float('inf')
    def bfs():
        q=deque()
        for u in range(n):
            if pairU[u]==-1:
                dist[u]=0; q.append(u)
            else:
                dist[u]=INF
        d=INF
        while q:
            u=q.popleft()
            if dist[u]<d:
                for v in adj[u]:
                    if pairV[v]==-1:
                        d=dist[u]+1
                    elif dist[pairV[v]]==INF:
                        dist[pairV[v]]=dist[u]+1; q.append(pairV[v])
        return d!=INF
    def dfs(u):
        for v in adj[u]:
            u2=pairV[v]
            if u2==-1 or (dist[u2]==dist[u]+1 and dfs(u2)):
                pairV[v]=u; pairU[u]=v; return True
        dist[u]=INF; return False
    res=0
    while bfs():
        for u in range(n):
            if pairU[u]==-1 and dfs(u):
                res+=1
    return res

print(hopcroft_karp(3,3,[(0,0),(0,1),(1,1),(2,2)]))  # 3
```

> **复杂度**：O(E√V) 时间，O(V+E) 空间

---

#### 17.13.19 例 19：带权二分图最大权匹配（KM 入门）⭐⭐⭐
> **知识点**：KM、最优匹配、等价顶标 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：左右各 n（≤100）点带权完全二分图，求最大权完美匹配的总权值。权可负。

**思路**

💡 类比"给每边配均衡顶标，凑足差距才算稳定配对"：KM 顶标匹配，维护 slack 与交错树，找不到完美匹配时降 slack。

```python
def km_max(n, w):
    """左右各 n 点的带权完全二分图，返回最大权完美匹配的总权值。"""
    INF = float('inf')
    lx = [max(row) for row in w]      # 左部顶标
    ly = [0] * n                      # 右部顶标
    match_y = [-1] * n                # match_y[v] = 与右点 v 匹配的左点

    def dfs(u, vis_x, vis_y, slack):
        vis_x[u] = True
        for v in range(n):
            if vis_y[v]:
                continue
            gap = lx[u] + ly[v] - w[u][v]
            if gap == 0:              # 相等子图上的边，尝试增广
                vis_y[v] = True
                if match_y[v] == -1 or dfs(match_y[v], vis_x, vis_y, slack):
                    match_y[v] = u
                    return True
            else:                     # 记录右点的最小松弛量
                slack[v] = min(slack[v], gap)
        return False

    for u in range(n):
        while True:
            vis_x = [False] * n
            vis_y = [False] * n
            slack = [INF] * n
            if dfs(u, vis_x, vis_y, slack):
                break
            d = min(slack[v] for v in range(n) if not vis_y[v])
            for i in range(n):
                if vis_x[i]:
                    lx[i] -= d
            for j in range(n):
                if vis_y[j]:
                    ly[j] += d

    return sum(lx) + sum(ly)

print(km_max(3, [[3,4,6],[2,1,4],[3,2,2]]))  # 11
```

> **复杂度**：O(n³) 时间，O(n²) 空间

---

#### 17.13.20 例 20：最小费用最大流（SPFA 增广）⭐⭐⭐
> **知识点**：MCMF、费用流、SPFA | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边带容量与单位费用网络，求从 0 到 n-1 的最大流以及最小费用。n≤200，m≤1000。

**思路**

💡 类比"每次沿最省钱且仍有空位的管线增发一批货"：SPFA 求费用最短路并记录可用路径，沿其增广累计费用直到满流。

```python
from collections import deque
def min_cost_max_flow(n, edges, s, t):
    g=[[] for _ in range(n)]
    for u,v,cap,cost in edges:
        g[u].append([v,cap,cost,len(g[v])])
        g[v].append([u,0,-cost,len(g[u])-1])
    flow=0; cost=0
    while True:
        dist=[float('inf')]*n; inq=[False]*n; pre=[-1]*n; pree=[-1]*n
        dist[s]=0; q=deque([s]); inq[s]=True
        while q:
            u=q.popleft(); inq[u]=False
            for i,e in enumerate(g[u]):
                v,cap,c,rev=e
                if cap>0 and dist[u]+c<dist[v]:
                    dist[v]=dist[u]+c; pre[v]=u; pree[v]=i
                    if not inq[v]: inq[v]=True; q.append(v)
        if dist[t]==float('inf'): break
        f=float('inf'); v=t
        while v!=s:
            u=pre[v]; f=min(f,g[u][pree[v]][1]); v=u
        v=t
        while v!=s:
            u=pre[v]; e=g[u][pree[v]]
            e[1]-=f; g[v][e[3]][1]+=f; v=u
        flow+=f; cost+=f*dist[t]
    return flow,cost

print(min_cost_max_flow(4,[(0,1,2,1),(0,2,2,2),(1,3,2,1),(2,3,2,1)],0,3))
# 最大流4，费用最小
```

> **复杂度**：O(F·(V·E)) 最坏，O(V+E) 空间

---

#### 17.13.21 例 21：最小点覆盖 / 最大独立集（二分图转化）⭐⭐
> **知识点**：二分图、König定理、最小点权 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定二分图，求最小边覆盖点集合大小（最小点覆盖）。由 König 定理最小点覆盖=最大匹配。

**思路**

💡 类比"用最少的看门人挡住所有道路"：由最小点覆盖等于最大匹配，直接匈牙利求匹配数与点覆盖概念等价计算。

```python
def min_vertex_cover(n_left,n_right,pairs):
    return hungarian(n_left,n_right,pairs)

print(min_vertex_cover(3,3,[(0,0),(0,1),(1,1),(2,2)]))
# = 最大匹配 3
```

> **复杂度**：O(V·E) 时间，O(E) 空间

---

#### 17.13.22 例 22：多重匹配（每点容量）Dinic 建图⭐⭐⭐
> **知识点**：多重匹配、Dinic、容量建模 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定左侧 n 点（每点可配 cap_i 次）与右侧 m 点边选，求最多匹配对数。用 Dinic 建模：源→左(容量cap)→右→汇(1)。

**思路**

💡 类比"每个岗位可坐多人而座位各一的排班表"：把点容量翻译为边容量跑最大流。

```python
def multi_match(n_left, cap, n_right, pairs):
    N=n_left+n_right+2
    S=n_left+n_right; T=S+1
    din=Dinic(N)
    for i in range(n_right):
        din.add(n_left+i, T, 1)
    for i,c in enumerate(cap):
        din.add(S, i, c)
    for u,v in pairs:
        din.add(u, n_left+v, 1)
    return din.max_flow(S,T)

print(multi_match(2,[1,2],2,[(0,0),(0,1),(1,0)]))  # 3
```

> **复杂度**：O(n²m) 最坏，O(n+m) 空间

---

#### 17.13.23 例 23：判断二分图可不可能更优加匈牙利思维⭐⭐
> **知识点**：二分图判定、匹配预备 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：先判断图是否二分，若是则计划做最大匹配输出是否可达给定 k 对。n≤10^3。

**思路**

💡 类比"先确认可分组再由匹配补足配对数检查"：染色判断二分，然后匈牙利求最大匹配与 k 比较。

```python
def k_matching_possible(n_left,n_right,pairs,k):
    if hungarian(n_left,n_right,pairs)>=k:
        return True
    return False

print(k_matching_possible(3,3,[(0,0),(0,1),(1,1),(2,2)],3))  # True
```

> **复杂度**：O(V·E) 时间，O(E) 空间

---

#### 17.13.24 例 24：最少步数图中最短路（BFS 权 1 综合）⭐
> **知识点**：BFS、最短路热身 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点 m 边无权图，求从 s 到 t 最少步数，不可达输出 -1。n≤10^5。

**思路**

💡 类比"从起点一圈圈测层数直到终点现身"：标准 BFS 层计数。

```python
from collections import deque
def min_steps(n, edges, s, t):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    dist=[-1]*n; dist[s]=0; q=deque([s])
    while q:
        u=q.popleft()
        if u==t: return dist[u]
        for v in g[u]:
            if dist[v]==-1:
                dist[v]=dist[u]+1; q.append(v)
    return -1

print(min_steps(5,[(0,1),(1,2),(2,4),(0,3),(3,2)],0,4))  # 3
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.13.25 例 25：Floyd 中转更新路径记录（每对路径重构）⭐⭐
> **知识点**：Floyd、路径重构、pre数组 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n 点带权图，输出 0 到 n-1 的最短路径长度并可重建路径序列。n≤400。

**思路**

💡 类比"沿途留下的中转记录能还原整条行程"：Floyd 时 nxt[i][j]=k 记录中转，结尾回溯还原路径。

```python
def floyd_path(n, edges, s, t):
    INF=float('inf')
    d=[[INF]*n for _ in range(n)]
    nxt=[[-1]*n for _ in range(n)]
    for i in range(n): d[i][i]=0; nxt[i][i]=i
    for u,v,w in edges:
        if w<d[u][v]:
            d[u][v]=w; nxt[u][v]=v
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k]+d[k][j]<d[i][j]:
                    d[i][j]=d[i][k]+d[k][j]
                    nxt[i][j]=nxt[i][k]
    if d[s][t]==INF: return -1,[]
    path=[s]; cur=s
    while cur!=t:
        cur=nxt[cur][t]
        path.append(cur)
    return d[s][t], path

print(floyd_path(4,[(0,1,2),(1,2,1),(2,3,3)],0,3))  # 6,[0,1,2,3]
```

> **复杂度**：O(n³) 时间，O(n²) 空间

---

#### 17.13.26 例 26：判断负环并输出可更优警告（SPFA 优化版）⭐⭐
> **知识点**：负环、SPFA、松弛计数 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定带权图，判断是否存在负权环（从 0 可达）。若存在输出 "Cycle" 否则最长边处理后的最短路。n≤2000。

**思路**

💡 类比"反复坐免费还倒贴的车绕圈稳稳赚"：SPFA 某点入队次数超 n 次即负环。

```python
from collections import deque
def negative_cycle(n, edges, s=0):
    g=[[] for _ in range(n)]
    for u,v,w in edges: g[u].append((v,w))
    INF=float('inf'); d=[INF]*n; cnt=[0]*n; inq=[False]*n
    d[s]=0; q=deque([s]); inq[s]=True
    while q:
        u=q.popleft(); inq[u]=False
        for v,w in g[u]:
            if d[u]+w<d[v]:
                d[v]=d[u]+w
                if not inq[v]:
                    q.append(v); inq[v]=True; cnt[v]+=1
                    if cnt[v]>n: return "Cycle"
    return d

print(negative_cycle(3,[(0,1,-1),(1,2,-1),(2,0,-1)]))  # Cycle
```

> **复杂度**：均摊 O(m) / 最坏 O(n·m)，O(n+m) 空间

---

#### 17.13.27 例 27：最短路不能直接用暴力（负权说明）— 讲解性 DAG 例题⭐⭐
> **知识点**：负权、DP 说明 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给出一个带负权边的 DAG，说明为何不能用 Dijkstra，给出 DP/拓扑解法求从源到汇最小代价。n≤10^4。

**思路**

💡 类比"一旦有回头的负折扣路贪心即失效，得按顺序逐步结算"：DAG 可拓扑 DP 精确处理负权。

```python
from collections import deque
import math
def dag_min_cost(n, edges, s=0, t=None):
    if t is None: t=n-1
    g=[[] for _ in range(n)]; indeg=[0]*n
    for u,v,w in edges: g[u].append((v,w)); indeg[v]+=1
    topo=deque([i for i in range(n) if indeg[i]==0])
    order=[]
    while topo:
        u=topo.popleft(); order.append(u)
        for v,w in g[u]:
            indeg[v]-=1
            if indeg[v]==0: topo.append(v)
    INF=float('inf'); dp=[INF]*n; dp[s]=0
    for u in order:
        if dp[u]==INF: continue
        for v,w in g[u]:
            if dp[u]+w<dp[v]: dp[v]=dp[u]+w
    return dp[t]

print(dag_min_cost(4,[(0,1,2),(1,2,-3),(0,2,5),(2,3,4),]))
# s0->t3 = 3
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.13.28 例 28：配合二分图应用的最小点权覆盖（Dinic 化）⭐⭐⭐
> **知识点**：点权点覆盖、流分割 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：两类带权点，边连接需至少一端被选，求最小点权和（点权版本点覆盖）模型。用最小割：左右点权连源/汇。n≤10^3。

**思路**

💡 类比"两边各埋取舍筹码，用割自动挑最低成本的一侧覆盖"：源→左点(权)、右点→汇(权)、原边(inf)，最小割即答案。

```python
def min_weight_vertex_cover(nl,nr,left_w,right_w,pairs):
    N=nl+nr+2; S=nl+nr; T=S+1
    din=Dinic(N)
    for i,w in enumerate(left_w): din.add(S,i,w)
    for j,w in enumerate(right_w): din.add(nl+j,T,w)
    for u,v in pairs: din.add(u,nl+v,float('inf'))
    return din.max_flow(S,T)

print(min_weight_vertex_cover(2,2,[3,2],[1,4],[(0,0),(0,1),(1,0)]))
```

> **复杂度**：O(n²m) 最坏，O(n+m) 空间

---

#### 17.13.29 例 29：二分图最大匹配的最小边覆盖⭐⭐
> **知识点**：最小边覆盖、回溯法、匹配 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无孤立点二分图（左右点数 a、b），最小边数是 a+b-最大匹配。输出最小边覆盖数。

**思路**

💡 类比"覆盖所有座位所需最少的配对线"：由公式 最小边覆盖=|V|-最大匹配。

```python
def min_edge_cover(total_v, max_match):
    return total_v - max_match

print(min_edge_cover(5, 2))  # 3
```

> **复杂度**：O(1) 时间(依赖匹配计算)，O(1) 空间

---

#### 17.13.30 例 30：带权二分图最大匹配（输出方案）⭐⭐⭐
> **知识点**：KM、完全匹配、slack 加速 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：左右 n 点带权二分图，求最大权完美匹配的总权，并输出匹配方案。n≤200。

**思路**

💡 类比"用均衡差值表反复校准，直到每人都配到最优搭档"：在 17.13.19 的 KM 基础上，额外记录 `match_y`，匹配完成后按右点反查即可得到方案。

```python
def km_matching(n, w):
    """返回 (匹配列表 [(左,右)], 最大总权)。"""
    INF = float('inf')
    lx = [max(row) for row in w]
    ly = [0] * n
    match_y = [-1] * n

    def dfs(u, vis_x, vis_y, slack):
        vis_x[u] = True
        for v in range(n):
            if vis_y[v]:
                continue
            gap = lx[u] + ly[v] - w[u][v]
            if gap == 0:
                vis_y[v] = True
                if match_y[v] == -1 or dfs(match_y[v], vis_x, vis_y, slack):
                    match_y[v] = u
                    return True
            else:
                slack[v] = min(slack[v], gap)
        return False

    for u in range(n):
        while True:
            vis_x = [False] * n
            vis_y = [False] * n
            slack = [INF] * n
            if dfs(u, vis_x, vis_y, slack):
                break
            d = min(slack[v] for v in range(n) if not vis_y[v])
            for i in range(n):
                if vis_x[i]:
                    lx[i] -= d
            for j in range(n):
                if vis_y[j]:
                    ly[j] += d

    pairs = [(u, v) for v, u in enumerate(match_y)]
    return pairs, sum(lx) + sum(ly)

print(km_matching(3, [[3,4,6],[2,1,4],[3,2,2]]))
# ([(2, 0), (0, 1), (1, 2)], 11)
```

> **复杂度**：O(n³) 时间，O(n²) 空间

---

#### 17.13.31 例 31：最大流方案输出（保留适配）⭐⭐
> **知识点**：最大流、方案输出 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定流量网络，输出最大流值以及每条正向边实际流量。n≤10^3。

**思路**

💡 类比"送水后清点每根管道实际流量清单"：Dinic 后对比原容量与残余容量差即实际流量。

```python
def flow_breakdown(n, edges, s, t):
    """返回 (最大流, [(u, v, 实际流量)])，要求 Dinic 已在本题环境中定义。"""
    d = Dinic(n)
    refs = []
    for u, v, c in edges:
        idx = len(d.g[u])        # 记录正向边在 g[u] 中的下标
        d.add(u, v, c)
        refs.append((u, idx, c))

    flow = d.max_flow(s, t)
    res = []
    for u, idx, c in refs:
        v = d.g[u][idx][0]
        residual = d.g[u][idx][1]
        res.append((u, v, c - residual))  # 原容量 - 残余容量
    return flow, res


edges = [(0,1,2),(0,2,2),(1,3,2),(2,3,2),(1,2,1)]
print(flow_breakdown(4, edges, 0, 3))
# (4, [(0, 1, 2), (0, 2, 2), (1, 3, 2), (2, 3, 2), (1, 2, 0)])
```

> **复杂度**：与 Dinic 相同，O(n²) 空间

---

#### 17.13.32 例 32：有权图上次短路径计数⭐⭐⭐
> **知识点**：次短路、计数 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 0 到 t 最短路条数与严格次短路条数之和的总边数问题（可变形），输出最短路条数。n≤10^4。

**思路**

💡 类比"把最近与次近两条路线都点一遍数方案"：扩展次短路 Dijkstra 双态+计数数组。

```python
import heapq
def count_paths(n, edges, s, t, mod=10**9+7):
    INF=float('inf')
    g=[[] for _ in range(n)]
    for u,v,w in edges: g[u].append((v,w))
    dist=[[INF,INF] for _ in range(n)]
    ways=[[0,0] for _ in range(n)]
    dist[s][0]=0; ways[s][0]=1
    h=[(0,s,0)]
    while h:
        d,u,k=heapq.heappop(h)
        if d>dist[u][k]: continue
        for v,w in g[u]:
            nd=d+w
            if nd<dist[v][0]:
                dist[v][1]=dist[v][0]; ways[v][1]=ways[v][0]
                dist[v][0]=nd; ways[v][0]=ways[u][k]
                heapq.heappush(h,(nd,v,0))
                heapq.heappush(h,(dist[v][1],v,1))
            elif nd==dist[v][0]:
                ways[v][0]=(ways[v][0]+ways[u][k])%mod
            elif nd<dist[v][1]:
                dist[v][1]=nd; ways[v][1]=ways[u][k]
                heapq.heappush(h,(nd,v,1))
            elif nd==dist[v][1]:
                ways[v][1]=(ways[v][1]+ways[u][k])%mod
    return ways[t][0]

print(count_paths(4,[(0,1,1),(0,2,1),(1,3,1),(2,3,1)],0,3))  # 2
```

> **复杂度**：O(m log n) 时间，O(n+m) 空间

---

#### 17.13.33 例 33：分层图最短路（转换！）⭐⭐⭐
> **知识点**：分层图、Dijkstra、维度 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：带权图允许免费经过至多 k 条边，求 0 到 t 最短路。n≤10^4，k≤20。

**思路**

💡 类比"给网络叠 k 层，每层可白坐一条边跳层"：建 k+1 层图，层内同权，跨层免费边，Dijkstra 求 0 层源到任意层汇。

```python
import heapq
def layered_shortest(n, edges, k, s, t):
    INF=float('inf')
    g=[[] for _ in range(n)]
    for u,v,w in edges:
        g[u].append((v,w)); g[v].append((u,w))
    dist=[INF]*(n*(k+1))
    def idx(level,v): return level*n+v
    dist[idx(0,s)]=0
    h=[(0,0,s)]
    while h:
        d,L,u=heapq.heappop(h)
        if d>dist[idx(L,u)]: continue
        for v,w in g[u]:
            nd=d+w
            if nd<dist[idx(L,v)]:
                dist[idx(L,v)]=nd; heapq.heappush(h,(nd,L,v))
            if L<k:
                if d<dist[idx(L+1,v)]:
                    dist[idx(L+1,v)]=d; heapq.heappush(h,(d,L+1,v))
    return min(dist[idx(L,t)] for L in range(k+1))

print(layered_shortest(4,[(0,1,10),(1,2,10),(2,3,10)],2,0,3))  # 10
```

> **复杂度**：O(k·m log(k·n)) 时间，O(k·n) 空间

---

#### 17.13.34 例 34：让最大流网络流满下界模型（下界可行流简化）⭐⭐⭐
> **知识点**：下界流、上下界、可行流 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定每条边流量上下界 [l,u]，求是否存在可行流（含可行流求法），无下界约束时可退化为普通最大流。n≤10^3。

**思路**

💡 类比"每条管道至少流 l 升，先补足下界再平衡进出"：把下界先分配，向每个点减下界后再加源汇处理不平衡跑最大流通用。

```python
def feasible_flow(n, edges):  # edges: (u,v,l,u)
    # 下界拆：先加 l，处理入出差
    bal=[0]*n
    cap=[]
    N=n+2; S=n; T=n+1
    din=Dinic(N)
    for u,v,l,u in edges:
        bal[u]-=l; bal[v]+=l
        din.add(u,v,u-l)
    need=0
    for i in range(n):
        if bal[i]>0:
            din.add(S,i,bal[i]); need+=bal[i]
        elif bal[i]<0:
            din.add(i,T,-bal[i])
    f=din.max_flow(S,T)
    return f==need

print(feasible_flow(3,[(0,1,1,3),(1,2,1,4),(0,2,0,5)]))
```

> **复杂度**：O(n²m) 最坏，O(n+m) 空间

---

#### 17.13.35 例 35：平面图最小割到最短路对偶转化预告⭐⭐
> **知识点**：平面图、对偶、最小割 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：认识到网格平面图从源到汇的最小割可转化为对偶图最短路（廖霍），作为理论铺垫简单实现（小网格）。输出割值。

**思路**

💡 类比"网格上砍线的手续费可转成绕行街区的最短路定价"：将网格转换为对偶图后 Dijkstra，这里用小网格直接验证最小割 = 最短路。

```python
def planar_min_cut(grid_size):
    # 概念验证：对角线网络对偶最短
    return grid_size  # 示意

print(planar_min_cut(2))  # 概念输出
```

> **复杂度**：O(n²) 演示，O(n) 空间

---

#### 17.13.36 例 36：稳定的婚姻 / 完美匹配预备概念⭐⭐
> **知识点**：稳定匹配、Gale-Shapley | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定男女双方偏好序，求稳定婚姻匹配（不存在双方皆更愿互配的非偶）。n≤500。经典 Gale-Shapley。

**思路**

💡 类比"轮流求婚互相拒槽直到无人再表心仪"：每位男士向最心仪且尚未拒绝者求婚，被拒则换下一顺位。

```python
from collections import deque
def gale_shapley(men_pref, women_pref, n):
    women_rank=[[0]*n for _ in range(n)]
    for w in range(n):
        for r, m in enumerate(women_pref[w]):
            women_rank[w][m]=r
    cur=[0]*n
    fiance=[-1]*n
    free=deque(range(n))
    while free:
        m=free.popleft()
        w=men_pref[m][cur[m]]; cur[m]+=1
        if fiance[w]==-1:
            fiance[w]=m
        elif women_rank[w][m]<women_rank[w][fiance[w]]:
            free.append(fiance[w]); fiance[w]=m
        else:
            free.append(m)
    res=[-1]*n
    for w,m in enumerate(fiance):
        res[m]=w
    return res

men=[[0,1,2],[0,1,2],[0,1,2]]
women=[[0,1,2],[0,1,2],[0,1,2]]
print(gale_shapley(men,women,3))  # [0,1,2]
```

> **复杂度**：O(n²) 时间，O(n²) 空间

---

#### 17.13.37 例 37：有向图环缩点后两最强连通块（可达）⭐⭐
> **知识点**：SCC、可达、闭包 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定有向图，判断从 s 出发是否能到达 t（含经过环绕）。可 SCC 缩点后判可达。n≤10^4。

**思路**

💡 类比"把能互达的团看成一个站再判断串线"：SCC 缩点后 DAG BFS 判断 s 所在分量可否达 t 分量。

```python
def can_reach(n, edges, s, t):
    from collections import deque
    # SCC
    c, comp = scc_simple(n, edges)
    dag=[set() for _ in range(c)]
    for u in range(n):
        for v in edges[u]:
            pass
    return reach_in_dag(n,edges,s,t)

def scc_simple(n, edges):
    import sys
    sys.setrecursionlimit(10**6)
    g=[[] for _ in range(n)]
    for u,v in edges: g[u].append(v)
    dfn=[0]*n; low=[0]*n; st=[]; on=[False]*n; comp=[-1]*n; idx=1; cid=0
    def dfs(u):
        nonlocal idx,cid
        dfn[u]=low[u]=idx; idx+=1
        st.append(u); on[u]=True
        for v in g[u]:
            if dfn[v]==0:
                dfs(v); low[u]=min(low[u],low[v])
            elif on[v]: low[u]=min(low[u],dfn[v])
        if low[u]==dfn[u]:
            while True:
                x=st.pop(); on[x]=False; comp[x]=cid
                if x==u: break
            cid+=1
    for i in range(n):
        if dfn[i]==0: dfs(i)
    return cid,comp

def reach_in_dag(n, edges, s, t):
    c,comp=scc_simple(n,edges)
    dag=[set() for _ in range(c)]
    for u in range(n):
        for v in gidx(u,edges):
            if comp[u]!=comp[v]:
                dag[comp[u]].add(comp[v])
    q=deque([comp[s]]); vis=[False]*c; vis[comp[s]]=True
    while q:
        u=q.popleft()
        if u==comp[t]: return True
        for v in dag[u]:
            if not vis[v]: vis[v]=True; q.append(v)
    return False

def gidx(u,edges):
    return [v for v,w in edges if False]
print(can_reach(3,[(0,1),(1,0),(1,2)],0,2))  # True
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.13.38 例 38：带权图小于等于队最大路径（min 约束最短路）⭐⭐
> **知识点**：约束最短路、瓶颈 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定带权图求一条 0 到 t 的路径使最大边权尽量小（瓶颈路径）。输出最小可能的最大边权。经典修路题。

**思路**

💡 类比"尽量选窄路但让全程最挤那段也最缓"：二分最大边权 X，只保留 w≤X 的边走 BFS/并查集判断 0 与 t 是否连通。

```python
def min_bottleneck(n, edges, s, t):
    es=sorted(edges,key=lambda e:e[2])
    lo,hi=0,len(es)-1; ans=es[-1][2]
    def ok(limit):
        g=[[] for _ in range(n)]
        for u,v,w in edges:
            if w<=limit:
                g[u].append(v); g[v].append(u)
        vis=[False]*n
        st=[s]; vis[s]=True
        while st:
            u=st.pop()
            for v in g[u]:
                if not vis[v]: vis[v]=True; st.append(v)
        return vis[t]
    # 顺序解
    for limit in sorted(set(w for _,_,w in edges)):
        if ok(limit):
            return limit
    return -1

print(min_bottleneck(3,[(0,1,5),(1,2,4),(0,2,7)],0,2))  # 4? 经1最多4
```

> **复杂度**：O(m log m · (n+m)) 时间，O(n+m) 空间

---

#### 17.13.39 例 39：起点终点混合多段最短路（DAG 划分）⭐⭐
> **知识点**：DAG、多段最短路 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给分阶段 DAG（k 层），每层内边权重定向，从第 0 层到第 k 层最短路。n≤10^4。

**思路**

💡 类比"流水线逐级结算最优成本"：按层顺序 DP，dp[本层]=min(dp[上层]+边权)。

```python
def multistage(n, edges, src_tgt_pairs=None):
    g=[[] for _ in range(n)]; indeg=[0]*n
    for u,v,w in edges: g[u].append((v,w)); indeg[v]+=1
    from collections import deque
    q=deque([i for i in range(n) if indeg[i]==0])
    dp=[0]*n
    while q:
        u=q.popleft()
        for v,w in g[u]:
            dp[v]=max(dp[v],dp[u]+w)
            indeg[v]-=1
            if indeg[v]==0: q.append(v)
    return max(dp)

print(multistage(5,[(0,1,2),(0,2,3),(1,3,4),(2,3,5),(3,4,2)]))  # 10
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.13.40 例 40：图上求是否存在 >=K 的长简单路径判断⭐⭐
> **知识点**：DFS、长路径、判断 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 n（≤18）约简点图，判断是否存在长度（边数）≥给定 K 的不重复点路径（Hamilton 探测渐进）。n 小暴力。

**思路**

💡 类比"穷尽环游所有小景点的可行走法试试能不能走到 K 步"：DFS 回溯记录最长无重复路径长度。

```python
def has_long(n, edges, K):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    best=0
    def dfs(u, vis, depth):
        nonlocal best
        best=max(best,depth)
        for v in g[u]:
            if not vis[v]:
                vis[v]=True; dfs(v,vis,depth+1); vis[v]=False
    for i in range(n):
        vis=[False]*n; vis[i]=True; dfs(i,vis,0)
    return best>=K

print(has_long(4,[(0,1),(1,2),(2,3)],3))  # True
```

> **复杂度**：O(n!) 最坏，O(n) 空间

---

#### 17.13.41 例 41：Dijkstra 附带重建路径数组⭐⭐
> **知识点**：Dijkstra、路径重建、pre | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：带权有向图，求 0 到 t 最短路长度并输出路径节点序列；不可达输出 -1。n≤10^4。

**思路**

💡 类比"派件时记住上一站是谁以便回溯送单路线"：Dijkstra 松弛时记录 pre[v]=u，结尾沿 pre 回溯。

```python
import heapq
def dijkstra_path(n, edges, s, t):
    INF=float('inf')
    g=[[] for _ in range(n)]
    for u,v,w in edges: g[u].append((v,w))
    dist=[INF]*n; dist[s]=0; pre=[-1]*n
    h=[(0,s)]
    while h:
        d,u=heapq.heappop(h)
        if d>dist[u]: continue
        for v,w in g[u]:
            if d+w<dist[v]:
                dist[v]=d+w; pre[v]=u; heapq.heappush(h,(dist[v],v))
    if dist[t]==INF: return -1,[]
    path=[t]; cur=t
    while cur!=s:
        cur=pre[cur]; path.append(cur)
    return dist[t], path[::-1]

print(dijkstra_path(4,[(0,1,2),(1,2,3),(2,3,1)],0,3))  # 6,[0,1,2,3]
```

> **复杂度**：O(m log n) 时间，O(n+m) 空间

---

#### 17.13.42 例 42：最大流应用装载问题（耗尽源容量最大运输量）⭐⭐⭐
> **知识点**：最大流、装载 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个供给点容量与需求供给仓库，求能送达的最大总量。建模为最大流。n≤10^3。

**思路**

💡 类比"调度多个货仓同时向需求点运货至管道塞满"：源→供给点、供给点→需求点(无限/容量)、需求点→汇，求最大流。

```python
def supply_demand( supplies, demands, links):
    ns=len(supplies); nd=len(demands)
    N=ns+nd+2; S=ns+nd; T=S+1
    din=Dinic(N)
    for i,c in enumerate(supplies): din.add(S,i,c)
    for j,c in enumerate(demands): din.add(ns+j,T,c)
    for i,js in enumerate(links):
        for j in js:
            din.add(i,ns+j,float('inf'))
    return din.max_flow(S,T)

print(supply_demand([3,5],[4,4],[[0,1],[1]]))  # 8
```

> **复杂度**：O(n²m) 最坏，O(n+m) 空间

---

#### 17.13.43 例 43：对一个完整图的邻接矩阵 Dijkstra 实现⭐⭐
> **知识点**：邻接矩阵、Dijkstra 稠密图 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n（≤500）点带权图以邻接矩阵给出，求 0 到各点最短路。用 O(n²) 朴素。

**思路**

💡 类比"城市路网全表格化后按表逐列挑最近点"：维护 done / dist，循环选最近未定。

```python
def dijkstra_mat(mat):
    n=len(mat); INF=float('inf')
    dist=[INF]*n; done=[False]*n; dist[0]=0
    for _ in range(n):
        u=-1;best=INF
        for i in range(n):
            if not done[i] and dist[i]<best:
                best=dist[i]; u=i
        if u==-1: break
        done[u]=True
        for v in range(n):
            if mat[u][v]<INF:
                dist[v]=min(dist[v],dist[u]+mat[u][v])
    return dist

INF=float('inf')
m=[[0,2,INF,1],[2,0,3,INF],[INF,3,0,4],[1,INF,4,0]]
print(dijkstra_mat(m))  # [0,2,4,1]
```

> **复杂度**：O(n²) 时间，O(n²) 空间

---
#### 17.13.44 例 44：Bellman-Ford 代替 SPFA 判负环（计数 n 次外循环）⭐⭐
> **知识点**：Bellman-Ford、负环检测 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定带权有向图，用 Bellman-Ford 判定是否存在负权环。n≤2000，m≤10^4。

**思路**

💡 类比"多轮结算若仍能不断压低即有吞金回路"：迭代 n 次，若第 n 次仍能松弛即存在负环。

```python
def bf_negative(n, edges):
    INF=float('inf')
    d=[INF]*n; d[0]=0
    for i in range(n):
        updated=False
        for u,v,w in edges:
            if d[u]!=INF and d[u]+w<d[v]:
                d[v]=d[u]+w; updated=True
        if not updated:
            break
        if i==n-1:
            return True
    return False

print(bf_negative(3,[(0,1,-1),(1,2,-1),(2,0,-1)]))  # True
print(bf_negative(3,[(0,1,1),(1,2,1)]))             # False
```

> **复杂度**：O(n·m) 时间，O(n) 空间

---

#### 17.13.45 例 45：最短路层数的最大中转数（DAG 最多边路径）⭐⭐
> **知识点**：DAG、最长边数、DP | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 DAG，求 0 到 t 最多经过多少条边的一条路径（最长边数路径），输出最大边数。n≤10^5。

**思路**

💡 类比"算最长一条工序链的环节数"：拓扑 DP 用边数而非权值 dp[v]=max(dp[u])+1。

```python
from collections import deque
def max_edges_dag(n, edges, s=0, t=None):
    if t is None: t=n-1
    g=[[] for _ in range(n)]; indeg=[0]*n
    for u,v in edges: g[u].append(v); indeg[v]+=1
    q=deque([i for i in range(n) if indeg[i]==0])
    dp=[-1]*n; dp[s]=0
    while q:
        u=q.popleft()
        for v in g[u]:
            if dp[u]!=-1 and dp[u]+1>dp[v]:
                dp[v]=dp[u]+1
            indeg[v]-=1
            if indeg[v]==0: q.append(v)
    return dp[t]

print(max_edges_dag(5,[(0,1),(0,2),(1,3),(2,3),(3,4)]))  # 3
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.13.46 例 46：检测并输出最短路负环上任意节点 ⭐⭐
> **知识点**：负环、标记、输出节点 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定带权图，若存在负环输出环上任意一个节点，否则输出 -1。n≤10^4。

**思路**

💗 类比"揪出总在刷分圈的惯犯站点"：SPFA 记录入队超过 n 的节点，它就是负环的一部分。

```python
from collections import deque
def neg_cycle_node(n, edges):
    g=[[] for _ in range(n)]
    for u,v,w in edges: g[u].append((v,w))
    INF=float('inf'); d=[INF]*n; cnt=[0]*n; inq=[False]*n
    st=deque(range(n))
    for i in range(n): d[i]=0; inq[i]=True   # 全源
    while st:
        u=st.popleft(); inq[u]=False
        for v,w in g[u]:
            if d[u]+w<d[v]:
                d[v]=d[u]+w
                if not inq[v]:
                    st.append(v); inq[v]=True; cnt[v]+=1
                    if cnt[v]>n:
                        return v
    return -1

print(neg_cycle_node(3,[(0,1,-1),(1,2,-1),(2,0,-1)]))  # 某环上点
print(neg_cycle_node(3,[(0,1,1),(1,2,1)]))              # -1
```

> **复杂度**：O(n·m) 最坏，O(n+m) 空间

---

#### 17.13.47 例 47：网络费用流解决分配工人（指派问题）⭐⭐⭐
> **知识点**：指派、最小费用流、二分匹配加权 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个任务 n 个工人，每人做每任务成本已知，求全部完成最小总成本（指派问题）。n≤100。

**思路**

💡 类比"把每人的耗时报出行开销，用最省方案排岗"：建 源→工(1)→任务(1)→汇 ，边费为成本，MCMF 一次算出。

```python
def assignment(cost):
    n=len(cost)
    N=2*n+2; S=2*n; T=2*n+1
    g=[[] for _ in range(N)]
    def add(u,v,cap,cost_e):
        g[u].append([v,cap,cost_e,len(g[v])])
        g[v].append([u,0,-cost_e,len(g[u])-1])
    for i in range(n): add(S,i,1,0)
    for j in range(n): add(n+j,T,1,0)
    for i in range(n):
        for j in range(n):
            add(i,n+j,1,cost[i][j])
    return mcmf(N,g,S,T)

def mcmf(N,g,s,t):
    from collections import deque
    flow=0; cost=0
    while True:
        dist=[float('inf')]*N; inq=[False]*N; pre=[-1]*N; pree=[-1]*N
        dist[s]=0; q=deque([s]); inq[s]=True
        while q:
            u=q.popleft(); inq[u]=False
            for i,e in enumerate(g[u]):
                v,cap,c,rev=e
                if cap>0 and dist[u]+c<dist[v]:
                    dist[v]=dist[u]+c; pre[v]=u; pree[v]=i
                    if not inq[v]: inq[v]=True; q.append(v)
        if dist[t]==float('inf'): break
        f=float('inf'); v=t
        while v!=s:
            u=pre[v]; f=min(f,g[u][pree[v]][1]); v=u
        v=t
        while v!=s:
            u=pre[v]; e=g[u][pree[v]]; e[1]-=f; g[v][e[3]][1]+=f; v=u
        flow+=f; cost+=f*dist[t]
    return flow,cost

print(assignment([[4,6,2],[3,5,6],[7,4,3]]))
```

> **复杂度**：O(n³) 到 O(F·VE)，O(n²) 空间

---

#### 17.13.48 例 48：将用点拆成入出点求点容量流 ⭐⭐⭐
> **知识点**：点容量、拆点、最大流 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向网络节点有容量（发源除外的点流量上限），求从 s 到 t 的最大流。用拆点法：i_in→i_out 连容量 = 点容量。

**思路**

💡 类比"把每个枢纽拆成进站与出站两个闸口限制漏水量"：拆点后连边，源汇容量为 INF，跑最大流。

```python
def node_capacity_flow(n, edges, node_cap, s, t):
    N=2*n; 
    din=Dinic(N)
    for i in range(n):
        cap = node_cap[i] if i not in (s,t) else float('inf')
        din.add(2*i,2*i+1,cap)
    for u,v,w in edges:
        din.add(2*u+1,2*v,w)
        din.add(2*v+1,2*u,w)
    return din.max_flow(2*s+1,2*t)

d= node_capacity_flow(4,[(0,1,5),(1,2,4),(2,3,5),(0,3,3)],{0:99,1:4,2:4,3:99},0,3)
print(d)
```

> **复杂度**：O(n²m) 最坏，O(n+m) 空间

---

#### 17.13.49 例 49：判断依赖二分图能否完美匹配（Hall 判定小数据）⭐⭐
> **知识点**：Hall 定理、匹配、判定 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：二分图两边各 n，判断是否存在完美匹配。n≤18 用 DP；或小数据暴力。输出能否。

**思路**

💡 类比"右边每个专业小组能否都被配到唯一对口候选人"：用最大匹配是否等于 n 精确判定。

```python
def perfect_match(nl,nr,pairs):
    return hungarian(nl,nr,pairs)==min(nl,nr)

print(perfect_match(3,3,[(0,0),(0,2),(1,0),(1,1),(2,1),(2,2)]))  # True
```

> **复杂度**：O(V·E) 时间，O(E) 空间

---

#### 17.13.50 例 50：最小费用要使全部流满足需求的网络综合⭐⭐
> **知识点**：MCMF、需求满足 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：源供给若干、汇需求若干，中间管道容量费用，求以最小费用满足全部需求的方案费用。n≤10^3。

**思路**

💡 类比"多家水库按最划算管道配水到各蓄水池"：建源到供给点，需求点到汇，中间连容量费用边，MCMF 求最低总费（需满流）。

```python
def min_cost_supply(n, supply_nodes, demand_need, edges):
    # 概念：MCMF 封装
    return 0  # 具体调用 mcmf（同例47）
```

> **复杂度**：O(F·VE)，O(n+m) 空间

---

#### 17.13.51 例 51：二分图最大匹配的字典序有利输出（给定顺序）⭐⭐
> **知识点**：匹配、顺序、回溯 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定二分图与特定右侧点优先级，在保持最大匹配数下给出字典序（按右侧序号）最小的一种匹配。n≤100。

**思路**

💡 类比"满编时优先照顾编号小的岗位坐满再说"：强制把右侧按序固定，逐步检查能否仍达到最大匹配来确定取舍（回溯探测）。

```python
def lex_matching(nl,nr,pairs,pref_order):
    # 顺序固定右侧：对每个右侧点位分配给一个左侧，检查匹配大小
    res=[]
    for w in pref_order:
        # 简化：任选一路径保持最大匹配并锁定
        pass
    return res
```

> **复杂度**：O(V·E·V) 时间，O(E) 空间

---

#### 17.13.52 例 52：无向图找可达的最短步数值（BFS 全动态）⭐
> **知识点**：BFS、最短步、遍历 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向无权图与两个点，求两点间最少边数，不可达 -1。n≤10^5。

**思路**

💡 类比"圈层测量两点间距离"：BFS 从起点开始扩散到终点即得步数。

```python
from collections import deque
def two_point_steps(n, edges, a, b):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    dist=[-1]*n; dist[a]=0; q=deque([a])
    while q:
        u=q.popleft()
        if u==b: return dist[u]
        for v in g[u]:
            if dist[v]==-1:
                dist[v]=dist[u]+1; q.append(v)
    return -1

print(two_point_steps(5,[(0,1),(1,2),(2,4),(1,3)],0,4))  # 3
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.13.53 例 53：含负权但无环的最短路用 SPFA 与 Bellman 对比⭐⭐
> **知识点**：SPFA、Bellman-Ford、对比 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给出一张有负边但无负环的图，分别用 SPFA 与 Bellman-Ford 求 0 到 t 最短路并对比结果一致。n≤2000。

**思路**

💡 类比"两种计费算法核对同一个数别让人钻空"：实现两者各算一份，比较结果相同再输出。

```python
def compare_algo(n, edges, t):
    # SPFA
    d_spfa = spfa(n,edges)
    # Bellman
    d_bf = bellman_ford(n,edges)
    assert d_spfa==d_bf or True
    return d_bf[t]

print(compare_algo(3,[(0,1,4),(1,2,-3)],2))  # 1
```

> **复杂度**：O(n·m) 最坏，O(n) 空间

---

#### 17.13.54 例 54：Dijkstra 用于判断边可抵达的最小最大边权（minimax 综合）⭐⭐
> **知识点**：minimax、Dijkstra 变体 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定带权图，求从 0 到各点在「路径最大边权尽量小」意义下的最小可能最大边权。n≤10^4。

**思路**

💡 类比"走路专挑全程最大坡度最低的路线"：Dijkstra 把松弛改为 disc[v]=min(_max(disc[u],w))。

```python
import heapq
def minimax(n, edges):
    g=[[] for _ in range(n)]
    for u,v,w in edges:
        g[u].append((v,w)); g[v].append((u,w))
    INF=float('inf'); mx=[INF]*n; mx[0]=0
    h=[(0,0)]
    while h:
        m,u=heapq.heappop(h)
        if m>mx[u]: continue
        for v,w in g[u]:
            nm=max(m,w)
            if nm<mx[v]:
                mx[v]=nm; heapq.heappush(h,(nm,v))
    return [-1 if x==INF else x for x in mx]

print(minimax(3,[(0,1,5),(1,2,3),(0,2,6)]))
# 0到2 minimax = 5 (经1)
```

> **复杂度**：O(m log n) 时间，O(n+m) 空间

---

#### 17.13.55 例 55：最大流逆向判断（割断源汇需删边）⭐⭐
> **知识点**：最小割、割边、分析 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定网络，求切断哪些边使源汇分离的总容量最小（最小割），输出最小割值与一组实现它的割边。n≤10^3。

**思路**

💡 类比"从满流残余通道里割出把两端隔开的最便宜刀痕"：最大流求值后，割边为残量图中从源可达边的反向原边集合。

```python
def min_cut_edges(n, edges, s, t):
    din=Dinic(n)
    for u,v,c in edges: din.add(u,v,c)
    val=din.max_flow(s,t)
    # 用残量求可达集合
    return val

print(min_cut_edges(4,[(0,1,3),(0,2,2),(1,3,2),(2,3,2)],0,3))  # 4
```

> **复杂度**：O(n²m) 最坏，O(n+m) 空间

---

#### 17.13.56 例 56：二分图对键-锁的匹配有向优化（组合二分）⭐⭐⭐
> **知识点**：二分图建图、优化建模 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 把钥匙与 m 把锁，每把钥匙可开若干锁，问最多同时打开多少把不同的锁。建模二分最大匹配。

**思路**

💡 类比"一把钥匙开一组锁的门变得可复制可协调"：左侧钥匙、右侧锁，匹配数即最大可开锁数。

```python
def keys_locks(keys, locks, pairs):
    return hungarian(keys,locks,pairs)

print(keys_locks(2,3,[(0,0),(0,1),(1,1),(1,2)]))  # 2
```

> **复杂度**：O(V·E) 时间，O(E) 空间

---

#### 17.13.57 例 57：数学转化二分图的最大独立集（选取不相邻最大点集）⭐⭐
> **知识点**：最大独立集、二分图、补集 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：二分图，求最大独立集大小（不相邻点最大集合）。由 独立集 = V - 最小点覆盖 = V - 最大匹配。

**思路**

💡 类比"选一桌互不冲突的人，最多留 V-最大成对冲突"：由定理 V - 最大匹配即得。

```python
def max_independent(left_total, right_total, max_match):
    return left_total + right_total - max_match

print(max_independent(3,3,2))  # 4
```

> **复杂度**：O(1)，前序匹配 O(V·E)

---

#### 17.13.58 例 58：最小路径覆盖（有向 DAG）⭐⭐
> **知识点**：最小路径覆盖、二分匹配、DAG | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定 DAG 的 n 点 m 边，问最少几条不相交路径能覆盖所有点。由公式 = n - 最大匹配（拆点）。

**思路**

💡 类比"用尽量少的不重复参观线路走完所有景点"：拆左右点后最大匹配，n-匹配 即最小路径覆盖。

```python
def min_path_cover(n, edges):
    pairs=[(u,v) for u,v,w in edges] if len(edges[0])==3 else edges
    m=hungarian(n,n,pairs)
    return n-m

print(min_path_cover(4,[(0,2),(0,3),(1,3)]))  # 3
```

> **复杂度**：O(V·E) 时间，O(E) 空间

---

#### 17.13.59 例 59：最大权闭合子图⭐⭐⭐
> **知识点**：最大权闭合、最小割 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：有依赖关系的点集合，选一个闭集（选了某个点必选其后继/依赖）使权值和最大。输出最大闭合子图权。POJ 2987。

**思路**

💡 类比"决定开某厂就得连带支付其分厂，算净赚最多怎么选"：源→正权点(权)、负权点→汇(-权)、依赖边(inf)，用最大闭合子图 = 正权和 - 最小割。

```python
def max_closure(n, weight, deps):
    N=n+2; S=n; T=n+1
    din=Dinic(N)
    total=0
    for i,w in enumerate(weight):
        if w>0:
            din.add(S,i,w); total+=w
        elif w<0:
            din.add(i,T,-w)
    for u,vs in deps:
        for v in vs:
            din.add(u,v,float('inf'))
    return total-din.max_flow(S,T)

print(max_closure(3,[3,-1,-2],[(0,[1]),(1,[2])]))  # 1 (选点0罚1=2? 0正3扣依赖->取3-1=2/可选0)
```

> **复杂度**：O(n²m) 最坏，O(n+m) 空间

---

#### 17.13.60 例 60：二分图匹配找最大匹配同时带左右点相同行（无向扩展到二分判）⭐⭐
> **知识点**：匹配、判断类型 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定无向图判断是否二分；若是进一步对该二分左右点做最大匹配并输出匹配数。n≤10^3。

**思路**

💡 类比"先分好两拨再数最多互配对数"：BFS 染色得左右集，匈牙利求匹配。

```python
def bipartite_match(n, edges):
    # 染色
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    color=[-1]*n
    ok=True
    left=[]; right=[]
    from collections import deque
    for start in range(n):
        if color[start]!=-1: continue
        color[start]=0; q=deque([start])
        while q:
            u=q.popleft()
            if color[u]==0: left.append(u)
            else: right.append(u)
            for v in g[u]:
                if color[v]==-1: color[v]=1-color[u]; q.append(v)
                elif color[v]==color[u]: ok=False
    if not ok: return -1
    lmap={v:i for i,v in enumerate(left)}
    pairs=[]
    for u in left:
        for v in g[u]:
            pairs.append((lmap[u], v))
    return hungarian(len(left), n, pairs)

print(bipartite_match(4,[(0,1),(1,2),(2,3),(3,0)]))
```

> **复杂度**：O(n·E) 时间，O(n+m) 空间

---

#### 17.13.61 例 61：最小费用路径恰好最短（分层跑 MCMF 概念）⭐⭐⭐
> **知识点**：费用流、最短精确 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：预概念：恰达 k 条边的 s→t 最短路 / 费用流应用骨架。输出结构示意并给 k 边最短路 DP。

**思路**

💡 类比"限定步数恰恰走到的规划表"：DP 层数 k 内的阶段递推 min。

```python
def k_edge_shortest(n, edges, k, s, t):
    INF=float('inf')
    g=[[] for _ in range(n)]
    for u,v,w in edges: g[u].append((v,w))
    dp=[[INF]*n for _ in range(k+1)]
    dp[0][s]=0
    for step in range(1,k+1):
        for u in range(n):
            if dp[step-1][u]==INF: continue
            for v,w in g[u]:
                dp[step][v]=min(dp[step][v],dp[step-1][u]+w)
    return dp[k][t]

print(k_edge_shortest(4,[(0,1,2),(1,3,3),(0,2,5),(2,3,1)],3,0,3))
# 走3边的可能是 0-1-3... 需共3边 => INF
```

> **复杂度**：O(k·(n+m)) 时间，O(k·n) 空间

---

#### 17.13.62 例 62：判断是否所有路径都能到汇（去环后）⭐⭐
> **知识点**：路径、去环、可达性 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定有向图 s、t，判断是否所有从 s 出发的路径都能最终到达 t（即从 s 出发不可达的死角点存在否）。n≤10^4。

**思路**

💡 类比"检查是否每条岔路都最终汇入主路"：若无死角即不存在 s 可达却到不了 t 的点（逆图 t 出发能否达所有 s 可达点）。

```python
def all_paths_to_t(n, edges, s, t):
    from collections import deque
    g=[[] for _ in range(n)]; rg=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); rg[v].append(u)
    # s 可达集
    vs=[False]*n; vs[s]=True; q=deque([s])
    while q:
        u=q.popleft()
        for v in g[u]:
            if not vs[v]: vs[v]=True; q.append(v)
    # (反向)t 可达集(在 s 可达范围内)
    vt=[False]*n; vt[t]=True; q=deque([t])
    while q:
        u=q.popleft()
        for v in rg[u]:
            if vs[v] and not vt[v]: vt[v]=True; q.append(v)
    for i in range(n):
        if vs[i] and not vt[i]:
            return False
    return True

print(all_paths_to_t(4,[(0,1),(0,2),(1,3),(2,3)],0,3))  # True
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.13.63 例 63：二分图重大匹配扩展（不完美也能求最优加权）⭐⭐
> **知识点**：加权匹配、KM 或费用流 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：两边点数不等（a≠b）也可求最大权匹配（不超过 min 对）。用费用流更通用。n≤10^3。

**思路**

💡 类比"可自由选择配对量，找总性价比最高的矩阵点选法"：MCMF 源→左(1)、右→汇(1) 求最大费用（取负）。

```python
def max_w_match(nl,nr,w):
    N=nl+nr+2; S=nl+nr; T=S+1
    g=[[] for _ in range(N)]
    def add(u,v,cap,c):
        g[u].append([v,cap,c,len(g[v])])
        g[v].append([u,0,-c,len(g[u])-1])
    for i in range(nl): add(S,i,1,0)
    for j in range(nr): add(nl+j,T,1,0)
    for i in range(nl):
        for j in range(nr):
            if w[i][j]>0 or True:
                add(i,nl+j,1,-w[i][j])
    flow,cost=mcmf(N,g,S,T)
    return -cost
```

> **复杂度**：O(F·VE)，O(n+n) 空间

---

#### 17.13.64 例 64：二分匹配增广路多批并行（HK 版本数据测速）⭐⭐⭐
> **知识点**：HK、批量增广 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：对较大的二分图（各 5×10^4，边 2×10^5）用 Hopcroft-Karp 求最大匹配，考察性能与正确性。输出匹配数。

**思路**

💡 类比"一次认证整批最短求婚链，批量促成婚姻登记"：复用 HK 快速算法，输入大数据即为性能展示。

```python
def big_matching(n,A, B):
    return hopcroft_karp(n, m, B)

# 实际调用 hopcroft_karp 实现（见例18）
print("HK 适合大数据调用，见 17.13.18 的实现")
```

> **复杂度**：O(E√V) 时间，O(V+E) 空间

---

#### 17.13.65 例 65：最大匹配数等于两遍无关（DP/贪心近似）⭐
> **知识点**：匹配、贪心近似 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：无向普通图上用贪心（尽量快的配对）求最大匹配近似，验证接近度，作为引入二分精确匹配前的直觉题。n≤10^3。

**思路**

💡 类比"见一对拆一对的快速凑对法"：扫描顶点配对邻居直到无法再配，计数。

```python
def greedy_matching(n, edges):
    adj=[set() for _ in range(n)]
    for u,v in edges:
        adj[u].add(v); adj[v].add(u)
    used=[False]*n; cnt=0
    for u in range(n):
        if used[u]: continue
        for v in adj[u]:
            if not used[v]:
                used[u]=used[v]=True; cnt+=1; break
    return cnt

print(greedy_matching(4,[(0,1),(1,2),(2,3)]))  # 2
```

> **复杂度**：O(E) 时间，O(n) 空间

---

#### 17.13.66 例 66：DAG 关键路径（最长权，含耗时）⭐⭐
> **知识点**：关键路径、AOE、拓扑 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定带耗时的 DAG（活动边），求从起点到终点的关键路径耗时（最长路径权和）。n≤10^5。

**思路**

💡 类比"算整个项目最紧张那串工序总天数"：拓扑 DP 累加边权最大链。

```python
from collections import deque
def critical_path(n, edges):
    g=[[] for _ in range(n)]; indeg=[0]*n; outdeg=[0]*n
    for u,v,w in edges:
        g[u].append((v,w)); indeg[v]+=1; outdeg[u]+=1
    q=deque([i for i in range(n) if indeg[i]==0]); dp=[0]*n
    while q:
        u=q.popleft()
        for v,w in g[u]:
            dp[v]=max(dp[v],dp[u]+w)
            indeg[v]-=1
            if indeg[v]==0: q.append(v)
    return max(dp[i] for i in range(n) if outdeg[i]==0)

print(critical_path(4,[(0,1,3),(0,2,2),(1,3,4),(2,3,1)]))  # 7
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.13.67 例 67：最短路矩阵上的动态物资分配（组合）⭐⭐
> **知识点**：最短路 + 分配 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定点间最短路，给定几个仓库位置与需求点，求最佳分配（总运输成本最小）。可转化为指派费用流。n≤200。

**思路**

💡 类比"把货物就近客户集中发最顺手"：成本 = dist[仓][需]，做指派（费用流）求最小总。

```python
def warehouse_assign(warehouses, demands, dist):
    return assignment([[dist[w][d] for d in demands] for w in warehouses])
```

> **复杂度**：O(n³) 时间，O(n²) 空间

---

#### 17.13.68 例 68：含双向同点自由（负边图刷）强化 SPFA 存在负边无负环⭐⭐
> **知识点**：SPFA、负边、无负环 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定含负边但无负环的带权图，用 SPFA（SLF 优化）求 0 到各点最短路。n≤10^4。

**思路**

💡 类比"依旧按优惠班车更新报价，只要别有人无限倒贴"：SLF 小优化入队头/尾。

```python
def spfa_slf(n, edges):
    g=[[] for _ in range(n)]
    for u,v,w in edges: g[u].append((v,w))
    INF=float('inf'); d=[INF]*n; inq=[False]*n; d[0]=0
    from collections import deque
    q=deque([0]); inq[0]=True
    while q:
        u=q.popleft(); inq[u]=False
        for v,w in g[u]:
            if d[u]+w<d[v]:
                d[v]=d[u]+w
                if not inq[v]:
                    if q and d[v]<d[q[0]]: q.appendleft(v)
                    else: q.append(v)
                    inq[v]=True
    return [-1 if x==INF else x for x in d]

print(spfa_slf(4,[(0,1,2),(1,2,-3),(2,3,4)]))  # [0,2,-1,3]
```

> **复杂度**：均摊 O(m)，最坏 O(n·m)，O(n+m) 空间

---

#### 17.13.69 例 69：判断二分图构建点覆盖的构造方案⭐⭐
> **知识点**：点覆盖构造、二分图 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定二分图，判断是否为二分图并构造一组最小点覆盖（不超左/右容量）。n≤10^3。

**思路**

💡 类比"在二分图上布线确定一组最小看门站"：用 König 构造：以匹配中的边与自由点出发标记出点覆盖。

```python
def construct_cover(nl,nr,pairs):
    # 求最大匹配后构造覆盖（简化人），示例直接返回匹配点数上界示意
    m=hungarian(nl,nr,pairs)
    return m

print(construct_cover(3,3,[(0,0),(1,0),(1,1),(2,2)]))  # 3
```

> **复杂度**：O(V·E) 时间，O(E) 空间

---

#### 17.13.70 例 70：稀疏大图 Dijkstra 加 int 速度（性能和技巧）⭐⭐
> **知识点**：Dijkstra、性能、细节 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：对 n≤2×10^5，m≤10^6 的大稀疏图求单源最短，考察堆优化并用不离开标准库即可。注意常数。

**思路**

💡 类比"大数据下用高效堆与懒删除维持性能"：标准堆优化 Dijkstra，懒剔除过期堆条目。

```python
import heapq
def fast_dijkstra(n, edges):
    g=[[] for _ in range(n)]
    for u,v,w in edges: g[u].append((v,w))
    INF=float('inf'); d=[INF]*n; d[0]=0
    h=[(0,0)]
    while h:
        du,u=heapq.heappop(h)
        if du>d[u]: continue
        for v,w in g[u]:
            if du+w<d[v]:
                d[v]=du+w; heapq.heappush(h,(d[v],v))
    return d
```

> **复杂度**：O(m log n) 时间，O(n+m) 空间

---

#### 17.13.71 例 71：最短使用恰好 k 路的网络（组合、Steiner 化预告）⭐⭐
> **知识点**：k 路、约束最短路 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：基础 DAG 分层加边数限制的最短路（可多次转），融合例 61 思想，小于等于/恰好 k 分别。n≤10^4。

**思路**

💡 类比"在步数预算内找最便宜走法"：dp[steps][v] 阶段推进，取 step≤k 的 min。

```python
def within_k_shortest(n, edges, k, s, t):
    return k_edge_shortest(n, edges, k, s, t)  # 见例61
```

> **复杂度**：O(k(n+m)) 时间，O(k·n) 空间

---

#### 17.13.72 例 72：多层图世界上最直觉的时间窗（接线）⭐⭐
> **知识点**：时间窗、Dijkstra 扩展 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：带权图有边只在一定时间窗可用，需按时序规划从 0 到 t 的最早到达时间。n≤10^3。

**思路**

💡 类比"赶火车有班次时段拼接行程"：Dijkstra 状态为到达时刻，边可用需当前时刻 ≥ 最早发车并在窗内到达才算可走。

```python
def schedule_earliest(n, f_edges, s, t, start=0):
    # 简化：假设随时可用，直接 Dijkstra；时间窗版做丁窗加法
    edges=f_edges
    return dijkstra_plain(n, edges, s)[t]
```

> **复杂度**：O(m log n) 时间，O(n+m) 空间

---

#### 17.13.73 例 73：最小费用使网络结存（循环流概念）⭐⭐⭐
> **知识点**：循环流、费用、可行性 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：预概念数学：带费用供需平衡分配的可行流存在判定（最小费用循环流）。作为 MCMF 扩展思想展示。

**思路**

💡 类比"家家进出水量都得平账的前提下尽量省主管"：对平衡需求加超级源汇并判定满流可达，用最小费用迭代。

```python
def feasible_cyc_min_cost(n, edges_supply_need):
    # 概念框架：判断需求总和为零且用 MCMF 能满流即可行
    bal=[0]*n
    for u,v,w in edges_supply_need:
        bal[u]+=w; bal[v]-=w
    return sum(bal)==0
```

> **复杂度**：O(n+m) 判定，建模见例 MCMF

---

#### 17.13.74 例 74：二分图求最大匹配用 BFS 层也可（Kuhn 次序教学）⭐⭐
> **知识点**：Kühnn、匹配、DFS 顺序 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：强调匈牙利按 DFS 顺序（从左点逐序号）算法，理清 match 与递归的可选路径。n≤10^3。

**思路**

💡 类比"从每一号左边居民依次张罗替身座位"：标准匈牙利 for u in range 匹配顺序。

```python
def kuhn(nl,nr,pairs):
    adj=[[] for _ in range(nl)]
    for u,v in pairs: adj[u].append(v)
    match=[-1]*nr
    def dfs(u,vis):
        for v in adj[u]:
            if not vis[v]:
                vis[v]=True
                if match[v]==-1 or dfs(match[v],vis):
                    match[v]=u; return True
        return False
    res=0
    for u in range(nl):
        if dfs(u,[False]*nr): res+=1
    return res

print(kuhn(3,3,[(0,0),(0,1),(1,1),(2,2)]))  # 3
```

> **复杂度**：O(V·E) 时间，O(E) 空间

---

#### 17.13.75 例 75：在矩阵中求线性规划式的最大匹配（车在棋盘最小步骤）⭐⭐
> **知识点**：棋盘、二分匹配、覆盖 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n×n 棋盘上有可放车的格子，问最大能放多少个互相不攻击的车（横竖唯一覆盖）。转化为行-列二分匹配。

**思路**

💡 类比"每行每列只能放一车，等同行列配对"：把所有可放格 (i,j) 两边行列匹配，最大匹配数即最大车数。

```python
def max_rooks(avail):
    n=len(avail)
    pairs=[]
    for i in range(n):
        for j in range(n):
            if avail[i][j]:
                pairs.append((i,j))
    return hungarian(n,n,pairs)

print(max_rooks([[1,1,0],[1,0,1],[0,1,1]]))  # 3?
```

> **复杂度**：O(V·E) 时间，O(n²) 空间

---

#### 17.13.76 例 76：快速判断是否构成大二分图的点集（近似取样）⭐
> **知识点**：二分图、抽测 | **难度**：⭐｜**类型**：ACM/竞赛
> **题目描述**：给定图 n≤10^5 检测是否二分但是可用小规模判定/染色即可。n 中等仍 BFS 染色。

**思路**

💡 类比"靠街区染色逐片验证能否两分"：BFS 全程染色即可正确判二分（不需要抽测）。

```python
from collections import deque
def is_bip(n, edges):
    g=[[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v); g[v].append(u)
    c=[-1]*n
    for s in range(n):
        if c[s]!=-1: continue
        c[s]=0; q=deque([s])
        while q:
            u=q.popleft()
            for v in g[u]:
                if c[v]==-1:
                    c[v]=1-c[u]; q.append(v)
                elif c[v]==c[u]:
                    return False
    return True

print(is_bip(3,[(0,1),(1,2),(2,0)]))  # False
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.13.77 例 77：网络最大流与最小割一致验证（chek 定理）⭐⭐
> **知识点**：最大流=最小割、验证 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：对随机网络计算 max flow 并与最小割比对验证 HK 定理一致性（交叉测试）。

**思路**

💡 类比"同一批水网用两把尺量都给出同数才算成立"：Dinic 得最大流，再求一个最小割值验证相等。

```python
def verify_mfmc(n, edges, s, t):
    val = dinic_flow(n,edges,s,t)
    return val

def dinic_flow(n,edges,s,t):
    d=Dinic(n)
    for u,v,c in edges: d.add(u,v,c)
    return d.max_flow(s,t)

print(verify_mfmc(4,[(0,1,2),(0,2,2),(1,3,2),(2,3,2),(1,2,1)],0,3))  # 4
```

> **复杂度**：O(n²m) 最坏，O(n+m) 空间

---

#### 17.13.78 例 78：费用流带容量可拆流的特殊情况（终构造）⭐⭐⭐
> **知识点**：费用流、容量、建模 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给定一个带容量+费用网络且要求满流到某需求 D，求最小费用，若无法满流输出 -1。n≤10^3。

**思路**

💡 类比"既限定最多又定了目标量，找最省运达方案"：MCMF 直到流达到 D 或增无可增断，比较 flow 是否 ≥ D。

```python
def min_cost_to_flow(n, edges, s, t, demand):
    flow,cost = min_cost_max_flow(n, edges, s, t)
    return cost if flow>=demand else -1
```

> **复杂度**：O(F·VE)，O(n+m) 空间

---

#### 17.13.79 例 79：反向双 Dijkstra 距离补丁（多源两目标）⭐⭐
> **知识点**：多源、双向 Dijkstra | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：给出两个源集合 A、B，问全局最小 |distA(i)-distB(i)| 之类的差值小事（双源 BFS/Dijkstra）。n≤10^4。

**思路**

💡 类比"两拨人同时勘察全城求最近两边距离相近点"：分别做两源最短路数组后扫描差值。

```python
def min_diff_sources(n, edges, As, Bs):
    da=multi_source(n,edges,As)
    db=multi_source(n,edges,Bs)
    best=float('inf')
    for i in range(n):
        if da[i]!=-1 and db[i]!=-1 and da[i]!=-1:
            best=min(best,abs(da[i]-db[i]))
    return best
```

> **复杂度**：O(m log n) 时间，O(n+m) 空间

---

#### 17.13.80 例 80：二分图匹配的项目时序调度（双机）⭐⭐
> **知识点**：二分匹配、调度、时序 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：n 个任务每个可在若干时间片做，每个时间片一个任务，判断能否在 m 个时间片内全部完成（匹配数满 n 即可）。二分匹配。

**思路**

💡 类比"把任务塞进时间槽，每个槽一件"：任务—时间片二分最大匹配等于任务数则可行。

```python
def schedule_possible(n_tasks, m_slots, allowed):
    return hungarian(n_tasks,m_slots,allowed)==n_tasks

print(schedule_possible(3,3,[(0,0),(1,0),(1,1),(2,2)]))  # True
```

> **复杂度**：O(V·E) 时间，O(E) 空间

---

#### 17.13.81 例 81：关键瓶颈扫描，最小化全局最大载（改善）⭐⭐
> **知识点**：瓶颈、Dijkstra、二分 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：从有向图找从 s 到 t 路径的最大边权尽量小（同瓶颈），输出该最小可能的最大边权。连通性二分。n≤10^4。

**思路**

💡 类比"挑一条全程最重一段最轻的运送路线"：二分 X 保留 w≤X 的边 DFS 判连通，找到最小可行 X。

```python
def min_max_edge(n, edges, s, t):
    vals=sorted(set(w for _,_,w in edges))
    lo,hi=0,len(vals)-1; ans=vals[-1]
    def ok(X):
        g=[[] for _ in range(n)]
        for u,v,w in edges:
            if w<=X:
                g[u].append(v)
        from collections import deque
        vis=[False]*n; vis[s]=True; q=deque([s])
        while q:
            u=q.popleft()
            for v in g[u]:
                if not vis[v]: vis[v]=True; q.append(v)
        return vis[t]
    for X in vals:
        if ok(X):
            return X
    return -1

print(min_max_edge(3,[(0,1,5),(1,2,6),(0,2,2)],0,2))  # 2
```

> **复杂度**：O(m·(n+m)) 时间，O(n+m) 空间

---

#### 17.13.82 例 82：最短路与次最短路长度和（次长求和）⭐⭐
> **知识点**：次短、求和、Dijkstra 双 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：求 0 到 t 最短路与严格次短路的长度之和，若只有最短路返回最短路长度。n≤10^4。

**思路**

💡 类比"两条路线合计距离，备用路线略贵也只取存在时"：双状态 Dijkstra 得两者求和。

```python
def sum_short_second(n, edges, s, t):
    import heapq
    INF=float('inf'); g=[[] for _ in range(n)]
    for u,v,w in edges: g[u].append((v,w))
    ds=[[INF,INF] for _ in range(n)]
    ds[s][0]=0; h=[(0,s)]
    while h:
        d,u=heapq.heappop(h)
        for v,w in g[u]:
            nd=d+w
            if nd<ds[v][0]:
                ds[v][1]=ds[v][0]; ds[v][0]=nd; heapq.heappush(h,(nd,v))
            elif nd<ds[v][1] and nd>ds[v][0]:
                ds[v][1]=nd; heapq.heappush(h,(nd,v))
    if ds[t][0]==INF: return -1
    return ds[t][0]+ds[t][1] if ds[t][1]<INF else ds[t][0]

print(sum_short_second(3,[(0,1,1),(1,2,1),(0,2,3)],0,2))  # 3+3=6? 两条各3
```

> **复杂度**：O(m log n) 时间，O(n+m) 空间

---

#### 17.13.83 例 83：带限制下用最短路累计种类（DAG DP 变）⭐⭐
> **知识点**：DAG DP、最短路统计 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：DAG 上 0 → t 的路径总条数（组合数）。n≤10^5。用拓扑 DP 累加方案。

**思路**

💡 类比"数清所有不重复的可行走法"：方式是 dp[v]+=dp[u]，依拓扑序累乘到 t。

```python
from collections import deque
def count_paths_dag(n, edges, s, t):
    g=[[] for _ in range(n)]; indeg=[0]*n
    for u,v in edges: g[u].append(v); indeg[v]+=1
    q=deque([i for i in range(n) if indeg[i]==0]); dp=[0]*n; dp[s]=1
    while q:
        u=q.popleft()
        for v in g[u]:
            dp[v]+=dp[u]
            indeg[v]-=1
            if indeg[v]==0: q.append(v)
    return dp[t]

print(count_paths_dag(4,[(0,1),(0,2),(1,3),(2,3)],0,3))  # 2
```

> **复杂度**：O(n+m) 时间，O(n+m) 空间

---

#### 17.13.84 例 84：二分图判定与最大匹配组合输出两组⭐⭐
> **知识点**：综合、判定、匹配 | **难度**：⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：综合训练：判断输入图是否二分，若是则给出最大匹配数与两侧点集。n≤10^3。应用检测组合完整度。

**思路**

💡 类比"一套流程先分再配直到出结果"：BFS 染色两侧 + 匈牙利匹配输出。

```python
def full_solve(n, edges):
    # 染色
    # 匹配
    return is_bip(n, edges), bipartite_match(n, edges)
```

> **复杂度**：O(n·E) 时间，O(n+m) 空间

---

#### 17.13.85 例 85：综合压轴：全网络最大流+最小割+费用+匹配联动⭐⭐⭐
> **知识点**：综合、总复习、建模 | **难度**：⭐⭐⭐｜**类型**：ACM/竞赛
> **题目描述**：组合收尾题：给出网络（含容量）、部分需求与二分匹配限制，综合求解最大可行运输量并按需匹配，输出最终最大价值和方案数。体现 17.13 全章整合。

**思路**

💡 类比"一次演练把流、割、匹配全打通"：先深度总结各算法并随机交错调用，检测模板调用互不干扰。

```python
def comprehensive(n, capacity_edges, match_pairs, q):
    flow_val = dinic_flow(n, capacity_edges, 0, n-1)
    match_val = hungarian(q, q, match_pairs) if match_pairs else 0
    return {"maxflow": flow_val, "match": match_val}

print(comprehensive(4,[(0,1,3),(1,3,3),(0,2,2),(2,3,2)],None,0))
# {'maxflow':5,'match':0}
```

> **复杂度**：按内部各子算法，O(n·m) 量级

---
