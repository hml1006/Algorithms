# 文档项目结构重组为 mdbook 格式 Spec

## Why

当前文档项目由多个 Markdown 文件平铺在根目录下，缺乏统一的导航结构和书籍式阅读体验。现有公式渲染依赖 Markdown 原生支持，部分复杂 LaTeX 公式无法正确渲染。将其改造为 mdbook 格式后，可提供：

- 左侧边栏目录导航
- 统一的页面样式和主题
- 通过 `mdbook-katex` 插件实现完整的 LaTeX 公式渲染
- 支持搜索、打印等内置功能
- 可构建为静态 HTML 网站

## 内容安全保障措施

> **核心原则**：绝不删除原文件，除非构建验证通过且有完整备份。

1. **备份先行**：执行任何操作前，先创建 `.md` 文件的完整备份
2. **复制而非移动**：文件迁移使用 `cp`（复制）而非 `mv`（移动），验证通过后再删除原文件
3. **增量修改**：链接更新逐文件分步进行，每修改一个文件后验证其内容完整性
4. **保留原 `README.md`**：根目录 `README.md` 仅做精简（保留头部项目介绍），其余内容通过复制到 `src/README.md` 再修改
5. **回滚方案**：若构建失败，可直接删除 `src/`、`book.toml`、`book/`，原文件完整保留在根目录，零损失

## What Changes

1. **创建 mdbook 项目骨架**：在项目根目录初始化 `book.toml` 配置文件
2. **启用 mdbook-katex 插件**：配置 `book.toml` 启用 KaTeX 公式渲染
3. **创建 `src/` 目录**：将所有 `.md` 文档**复制**到 `src/` 目录（原文件保留，验证构建通过后再删除）
4. **创建 `SUMMARY.md`**：定义书籍的章节导航结构，支持层级展开
5. **创建 `book.toml`**：配置书籍元数据、主题、插件
6. **调整图片路径**：更新 `src/` 内文档的图片引用路径（`images/` → `../images/`），原根目录文件不变
7. **更新文档内链接**：修复 `src/` 内文档间的相对链接，使其适应新的目录结构
8. **构建与验证**：运行 `mdbook build` 确认构建成功，检查渲染效果
9. **清理（可选）**：确认所有功能正常后，再删除根目录的 `.md` 原文件（保留 `README.md` 和 `LICENSE`）

## Impact

- Affected code: 所有 `.md` 文档文件、`images/` 目录
- 根目录新增：`book.toml`、`src/`、`book/`（构建输出）
- 文档间链接需要更新（`./11a_传统机器学习.md` → `./11a_传统机器学习.md` 等同级链接保持不变，但 `../README.md` 等需要调整）
- 不影响已存在的 `LICENSE` 文件
- 原 `README.md` 文件保留在根目录作为项目 README，但需精简
- 不影响 `.trae/` 目录

## ADDED Requirements

### Requirement: mdbook 项目初始化

系统 SHALL 在项目根目录创建 `book.toml` 配置文件。

#### Scenario: 配置 mdbook 基本设置
- **WHEN** 用户运行 `mdbook build`
- **THEN** 系统应根据 `book.toml` 构建出静态 HTML 网站

### Requirement: KaTeX 公式渲染

系统 SHALL 通过 `mdbook-katex` 插件支持 LaTeX 公式渲染。

#### Scenario: 公式渲染验证
- **WHEN** 构建包含 `$...$` 或 `$$...$$` 公式的页面
- **THEN** 输出 HTML 应正确渲染为 KaTeX 格式，而非纯文本

### Requirement: 章节导航结构

系统 SHALL 通过 `SUMMARY.md` 定义完整的书籍章节结构。

#### Scenario: 目录显示
- **WHEN** 用户打开构建后的书籍页面
- **THEN** 左侧边栏应显示所有章节的层级目录

### Requirement: 文档迁移（安全优先）

系统 SHALL 将所有 `.md` 文档**复制**到 `src/` 目录，原文件保留至构建验证通过。

#### Scenario: 安全复制流程
- **WHEN** 执行文档迁移
- **THEN** 应使用 `cp` 复制文件，原文件保持在根目录不变
- **AND** 构建验证通过后，再提示用户确认是否删除原文件

#### Scenario: 文档链接正确性
- **WHEN** 用户点击 `src/` 内文档中的内部链接
- **THEN** 应正确跳转到目标页面，无 404 错误

## 内容安全与回滚

### 备份策略
1. 执行前备份：`cp -r *.md src/*.md ../backup_$(date +%Y%m%d)/`
2. 构建验证通过后，根目录文件仍保留，不做自动删除
3. 用户可自行决定是否删除根目录原文件

### 零风险回滚方案
若任何步骤失败，完整回滚只需：
```bash
rm -rf src/ book/ book.toml
# 根目录所有 .md 文件原封不动，项目恢复原始状态
```

## 项目结构设计

### 最终目录结构

```
Algorithms/
├── book.toml              # mdbook 配置文件
├── README.md              # 精简后的项目 README
├── LICENSE
├── images/                 # 保留在根目录（通过 book.toml 映射）
├── src/
│   ├── SUMMARY.md          # 章节导航定义
│   ├── README.md           # 书籍首页（原 README.md 内容精简后移入）
│   ├── 00_数学基础.md
│   ├── 00_编程基础.md
│   ├── 01_算法基础与复杂度分析.md
│   ├── 02_基础数据结构.md
│   ├── 03_排序与搜索.md
│   ├── 04_进阶数据结构.md
│   ├── 05_图论算法.md
│   ├── 06_动态规划.md
│   ├── 07_字符串算法.md
│   ├── 08_数论与组合数学.md
│   ├── 09_计算几何.md
│   ├── 10_高级专题.md
│   ├── 11_人工智能.md
│   ├── 11_高级算法与复杂度理论.md      # 若已存在则保留
│   ├── 11a_传统机器学习.md
│   ├── 11b_深度学习.md
│   ├── 11c_强化学习.md
│   ├── 11d_生成式AI与大模型.md
│   ├── 11e_学习路径与资源.md
│   └── 12_OI竞赛高级专题.md            # 若已存在则保留
└── book/                   # 构建输出目录（.gitignore）
```

### SUMMARY.md 章节结构

```markdown
# 算法学习教程

[前言](./README.md)

- [数学基础](./00_数学基础.md)
- [编程基础](./00_编程基础.md)
- [算法基础与复杂度分析](./01_算法基础与复杂度分析.md)
- [基础数据结构](./02_基础数据结构.md)
- [排序与搜索](./03_排序与搜索.md)
- [进阶数据结构](./04_进阶数据结构.md)
- [图论算法](./05_图论算法.md)
- [动态规划](./06_动态规划.md)
- [字符串算法](./07_字符串算法.md)
- [数论与组合数学](./08_数论与组合数学.md)
- [计算几何](./09_计算几何.md)
- [高级专题](./10_高级专题.md)
  - [AI 算法体系](./11_人工智能.md)
    - [传统机器学习](./11a_传统机器学习.md)
    - [深度学习](./11b_深度学习.md)
    - [强化学习](./11c_强化学习.md)
    - [生成式 AI 与大模型](./11d_生成式AI与大模型.md)
    - [学习路径与资源](./11e_学习路径与资源.md)
  - [高级算法与复杂度理论](./11_高级算法与复杂度理论.md)
  - [OI 竞赛高级专题](./12_OI竞赛高级专题.md)
```

### book.toml 配置

```toml
[book]
title = "算法学习教程"
description = "计算机数据结构与算法学习教程"
authors = ["Algorithms"]
language = "zh-CN"
src = "src"

[build]
build-dir = "book"

[preprocessor.katex]
before = ["links"]
renders = ["html"]

[output.html]
default-theme = "ayu"
preferred-dark-theme = "navy"
mathjax-support = false
```

## 配置说明

- **mdbook-katex**: 作为预处理器，在 `links` 之前运行，确保链接处理前公式已转换
- **图片路径**: 图片使用相对路径 `../images/xxx.svg`（从 `src/` 目录引用父目录的 `images/`），或通过 `book.toml` 的 `output.html.additional-css` 配合 `copy-images` 等方式处理
- **公式格式**: 所有 `$...$`（行内）和 `$$...$$`（块级）LaTeX 公式将被 KaTeX 自动渲染

## REMOVED Requirements

### Requirement: 旧的平铺式文档结构

**Reason**: 平铺结构缺乏导航和统一渲染能力，无法满足阅读体验需求
**Migration**: 所有 `.md` 文件移至 `src/` 目录，通过 `SUMMARY.md` 定义导航结构