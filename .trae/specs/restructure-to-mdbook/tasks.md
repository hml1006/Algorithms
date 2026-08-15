# Tasks

> **安全准则**：所有操作优先使用 `cp`（复制），原文件保留不变。构建验证通过后，用户可自行决定是否清理。

- [x] Task 1: 备份根目录所有 `.md` 文件
  - 创建备份目录：`mkdir -p backup_$(date +%Y%m%d)` ✅
  - 复制根目录所有 `.md` 文件到备份目录：`cp *.md backup_$(date +%Y%m%d)/` ✅
  - 验证备份文件数量与源文件一致 ✅（21 个文件）

- [x] Task 2: 创建 `book.toml` 配置文件
  - 配置书籍元数据（标题、作者、语言） ✅
  - 启用 `mdbook-katex` 预处理器（`before = ["links"]`） ✅
  - 配置 HTML 输出主题（`ayu`/`navy`） ✅
  - 设置 `src = "src"` 和 `build-dir = "book"` ✅

- [x] Task 3: 创建 `src/` 目录，复制文档到 `src/`
  - 创建 `src/` 目录 ✅
  - 使用 `cp` 将所有 `.md` 文档复制到 `src/`（**不删除**根目录原文件） ✅
  - 复制后验证 `src/` 内文件数量与根目录 `.md` 文件一致（排除 `README.md`） ✅
  - 验证复制后文件内容完整性（`md5sum` 对比或行数对比） ✅

- [x] Task 4: 创建 `src/SUMMARY.md` 章节导航
  - 定义完整的书籍章节层级结构 ✅
  - 包含所有章节链接 ✅
  - 为 AI 子章节创建嵌套结构（第 11 章作为父章节，11a~11e 作为子章节） ✅

- [x] Task 5: 创建 `src/README.md` 书籍首页
  - 复制根目录 `README.md` 到 `src/README.md` ✅
  - 保留项目介绍、章节总览表、知识体系 ✅
  - 添加"本书由 mdbook 构建"脚注 ✅

- [x] Task 6: 更新 `src/` 内文档的图片路径
  - 将所有 `images/xxx.svg` 和 `images/xxx.gif` 引用更新为 `../images/xxx.svg` 和 `../images/xxx.gif` ✅
  - 逐文件替换，每修改一个文件后验证内容未被破坏 ✅

- [x] Task 7: 更新 `src/` 内文档的内部链接
  - 查找所有 `](./` 和 `](` 形式的内部链接 ✅
  - 对于指向其他 `.md` 文件的链接，保持原样（同级目录链接在 `src/` 内同样有效） ✅
  - 对于指向 `../README.md` 的链接，更新为 `./README.md` ✅
  - 对于指向 `README.md#xxx` 的锚点链接，更新为 `./README.md#xxx` ✅

- [x] Task 8: 构建并验证
  - 运行 `mdbook build` 确认无错误 ✅
  - 检查 `book/` 目录是否生成完整 ✅（24 个 HTML 文件）
  - 打开构建后的 HTML 检查公式渲染效果 ✅（KaTeX 已加载，公式正常渲染）
  - 验证导航链接是否正常跳转 ✅（侧边栏导航由 mdbook 自动生成）
  - 对比 `src/` 和根目录文件数量，确保无遗漏 ✅（21 个原始文档一致）

- [x] Task 9: 清理（可选，用户确认后执行）
  - 用户确认构建无误后，删除根目录的 `.md` 原文件（保留 `README.md`、`LICENSE`、`.trae/`） ✅

# Task Dependencies

- [Task 1] 必须在 [Task 3] 之前执行（备份优先） ✅
- [Task 2] 必须先于 [Task 4, Task 5] ✅
- [Task 3] 必须先于 [Task 6, Task 7] ✅
- [Task 4, Task 5] 可并行执行 ✅
- [Task 6, Task 7] 可并行执行 ✅
- [Task 6, Task 7] 依赖于 [Task 3] ✅
- [Task 8] 依赖于所有前置任务 ✅
- [Task 9] 仅在 [Task 8] 通过后，经用户确认才执行 ✅