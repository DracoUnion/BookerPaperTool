# CHANGELOG

## 2026.10.29.0 (2026-10-29)

- 初始化 `BookerPaperTool` 项目，从 [BookerGptTool](https://github.com/DracoUnion/BookerGptTool) 拆分出论文与素材处理相关子命令。
- 迁移子命令：
  - `paper2textbook` → `textbook`（多篇论文到可溯源教科书）
  - `any2textbook` → `textbook-any`（多篇素材到可溯源教科书）
  - `paper2code` → `code`（从论文生成代码方案）
  - `auto-research` 保持不变（合规科研自动化流水线）
- 一并迁移共享模块：`openai.py`、`util.py`。
- 完整复制命令行通用参数（`-m/-k/-H/-r/-tm/-tp/-fp/-pp/-mt/--emb/-vm/-im/-ua/-st/-eb/-ct/-rt/-rr/-nt` 等）。
- 精简依赖到四个子命令实际所需的第三方库。