# 贪吃蛇游戏 - 单 Agent 自动化开发 Prompt v1.0

> 生成时间：2026-05-30  
> 项目：Snake (Python + pygame)  
> 模式：**单 Agent 全流程自动化**（无人工干预、无子 Agent）

---

## 🎯 核心指令

你是一个 **独立的 Vibe Coding Agent**，负责从文档阅读到完整代码生成的整个贪吃蛇游戏项目开发流程。你将自主完成以下工作：

1. **阅读并理解所有设计文档**（proposal.md、abstract-design.md、detailed-design.md、sub-tasks/*.md）
2. **按依赖顺序构建项目骨架**，逐个模块实现所有源代码文件
3. **确保模块间接口一致**，最终集成出可运行的版本
4. **执行自检与验证**，输出项目完成报告

**关键约束**：
- ⚠️ 整个过程 **无人工参与、无子 Agent 调度**，所有任务由单个 Agent 自主完成
- ⚠️ 严格遵循设计文档中的接口定义和架构规范
- ⚠️ 按依赖顺序推进，先实现的模块作为后实现模块的上下文

---

## 📋 项目上下文

### 项目目标
开发一款基于 Python + pygame 的经典贪吃蛇游戏：
- 简约像素风视觉设计（800×600 窗口，600×600 游戏区）
- 完整游戏流程：开始 → 游戏 → 暂停 → 结算
- 核心玩法：方向键控制、食物生成、碰撞检测、速度递增
- 数据持久化：本地存储最高分 (highscore.json)
- 支持后续打包为 Windows .exe

### 技术栈
```
- Python 3.10+
- pygame 2.5.2
- PyInstaller (后续打包)
- Git 版本管理
```

### 项目结构
```
Snake/
├── doc/
│   ├── proposal.md              # 需求文档
│   ├── abstract-design.md       # 概要设计
│   ├── detailed-design.md       # 详细设计
│   ├── sub-tasks/               # 模块任务分解
│   │   ├── config.md            # 配置常量模块
│   │   ├── storage.md           # 本地存储模块
│   │   ├── pixel_font.md        # 像素字体模块
│   │   ├── board.md             # 游戏区域/坐标转换模块
│   │   ├── snake.md             # 蛇实体逻辑模块
│   │   ├── food.md              # 食物管理模块
│   │   ├── assets.md            # 资源管理模块
│   │   ├── menu.md              # 菜单界面模块
│   │   ├── hud.md               # HUD 显示模块
│   │   ├── controller.md        # 游戏状态机与主循环调度
│   │   ├── main.md              # 程序入口集成模块
│   │   └── progress.md          # 开发顺序建议
│   └── prompt-single-agent.md   # 本文件：单 Agent 开发 Prompt
├── src/
│   ├── __init__.py              # [待生成]
│   ├── main.py                  # 程序入口 [待生成]
│   ├── game/
│   │   ├── __init__.py          # [待生成]
│   │   ├── snake.py             # 蛇实体逻辑 [待生成]
│   │   ├── food.py              # 食物管理 [待生成]
│   │   ├── board.py             # 游戏区域/坐标转换 [待生成]
│   │   └── controller.py        # 状态机/主循环调度 [待生成]
│   ├── ui/
│   │   ├── __init__.py          # [待生成]
│   │   ├── menu.py              # 菜单界面 [待生成]
│   │   ├── hud.py               # HUD 显示 [待生成]
│   │   └── assets.py            # 像素素材管理 [待生成]
│   └── utils/
│       ├── __init__.py          # [待生成]
│       ├── config.py            # 配置常量 [待生成]
│       ├── storage.py           # 本地存储 [待生成]
│       └── pixel_font.py        # 像素字体渲染 [待生成]
├── requirements.txt             # 依赖清单 [待生成]
├── build_exe.bat                # 打包脚本 [后续]
├── data/                        # 运行时数据目录 [自动生成]
└── README.md                    # [待更新]
```

### 视觉规范
```
- 窗口：800×600 | 游戏区：600×600 (20×20 格子，每格 30×30px)
- 颜色：蛇身 #4CAF50 | 食物 #F44336 | 背景 #1a1a2e
- 字体：像素字体 (8px/12px/16px)
- 动效：吃食物缩放+粒子 | 游戏结束震动+红框 | 按钮悬停高亮
```

---

## 🔄 工作流程（单 Agent 顺序执行）

### Phase 1: 文档阅读与分析
```
1. 读取 doc/proposal.md — 理解项目目标、功能需求、验收标准
2. 读取 doc/abstract-design.md — 理解系统架构、模块划分、依赖关系
3. 读取 doc/detailed-design.md — 获取每个模块的详细接口定义
4. 读取 doc/sub-tasks/progress.md — 确定开发顺序
5. 按需读取各 sub-tasks/*.md — 获取模块级任务清单和验收标准
6. 输出：确认所有模块的职责、接口签名、依赖图、开发顺序
```

### Phase 2: 基础层实现（无外部依赖的模块）
```
依次创建以下文件，每个文件完成后进行语法检查：
1. src/utils/config.py     — 配置常量与加载
2. src/utils/storage.py    — 最高分持久化
3. src/utils/pixel_font.py — 像素字体渲染
4. src/game/board.py       — 游戏区域与坐标转换

每步完成后用 py_compile 验证语法正确性。
```

### Phase 3: 核心游戏层实现（依赖基础层模块）
```
依次创建以下文件，每个文件完成后进行语法检查：
1. src/game/snake.py       — 蛇实体逻辑（依赖 Board）
2. src/ui/assets.py        — 资源管理器
3. src/game/food.py        — 食物管理（依赖 Board, Assets）

每个模块需引用 Phase 2 中已定义的类与函数。
```

### Phase 4: UI 层实现（依赖基础层与游戏层）
```
依次创建以下文件，每个文件完成后进行语法检查：
1. src/ui/menu.py          — 菜单界面（依赖 PixelFont, Assets）
2. src/ui/hud.py           — HUD 显示（依赖 PixelFont）
```

### Phase 5: 集成与入口
```
1. 创建 src/controller.py — 游戏状态机与主循环调度（聚合所有其他模块）
2. 创建 src/main.py      — 程序入口（初始化 Pygame、组装对象、启动主循环）
3. 创建 requirements.txt  — 依赖清单
4. 添加所有 __init__.py  — 确保包结构完整

最后执行一次完整的 py_compile 批量检查。
```

### Phase 6: 自检与验证
```
1. 语法检查：python -m py_compile src/**/*.py
2. 依赖安装：pip install -r requirements.txt
3. 冒烟测试：尝试导入所有模块确认无 ImportError
4. 手动测试清单（供用户后续运行验证）：
   - 启动游戏，显示开始菜单
   - 按回车进入游戏，方向键控制蛇移动
   - 吃到食物后蛇身增长、分数增加
   - 按 P 键暂停/继续
   - 撞墙或撞自身触发游戏结束，显示结算界面
   - 再次按回车重启游戏
   - 关闭游戏窗口正常退出

5. 输出最终完成报告
```

---

## 📦 每个模块的开发指引

对每个模块，你应执行以下步骤：

1. **确定文件路径**：根据项目结构确定目标 .py 文件路径
2. **阅读该模块的任务描述**：打开 doc/sub-tasks/{module_name}.md，理解任务清单
3. **查阅详细设计**：参考 doc/detailed-design.md 中的接口定义
4. **确认依赖**：列出上游模块，确保能正确 import
5. **编写代码**：实现所有未完成任务项，包含必要的 docstring 和类型注解
6. **语法验证**：通过 `apply_patch` 写入文件后，自动使用 py_compile 检查
7. **标记完成**：在进度报告中确认该模块 ✅ 完成

---

## ✅ 完成标准

当以下条件全部满足时，标记项目完成：

- [ ] 所有 11 个模块的代码文件均已创建（__init__.py 除外不计入）
- [ ] src/main.py 可正常启动，显示开始菜单
- [ ] 方向键控制蛇移动，无输入延迟
- [ ] 吃到食物后蛇身增长 + 分数 +10
- [ ] 撞墙/撞自身触发游戏结束，显示结算界面
- [ ] 最高分持久化到 highscore.json，重启后有效
- [ ] 所有 .py 文件通过 py_compile 语法检查
- [ ] requirements.txt 存在且内容正确，pip install -r 可复现环境
- [ ] doc/sub-tasks/progress.md 中标记所有任务为完成

---

## 🚨 异常处理策略

### 情况 1：设计文档存在歧义或不一致
```
处理方式：
1. 优先遵循 detailed-design.md（最详细）
2. 若仍有冲突，采用简化实现保证核心功能
3. 在代码中添加注释说明取舍理由
```

### 情况 2：某个模块无法独立完成（缺少必要上下文）
```
处理方式：
1. 使用合理的默认实现
2. 标注 TODO 或 HACK 注释
3. 继续实现下游模块（避免阻塞整体进度）
4. 在最终报告中列出需人工审查的项目
```

### 情况 3：代码生成后出现语法错误或逻辑问题
```
处理方式：
1. 立即查看错误信息
2. 分析问题根源（缩进 / 拼写 / 类型不匹配 / 未定义变量等）
3. 直接修正并重写文件
4. 重试不超过 3 次
```

---

## 🎬 启动指令

Agent，现在请开始执行：

1. **第一步**：依次读取 doc/proposal.md、doc/abstract-design.md、doc/detailed-design.md、doc/sub-tasks/progress.md
2. **第二步**：确认开发顺序与依赖图
3. **第三步**：按 Phase 1→6 的顺序，逐模块创建代码文件
4. **第四步**：完成所有文件后进行批量语法检查
5. **第五步**：生成 requirements.txt，输出最终完成报告

**开始执行 →**