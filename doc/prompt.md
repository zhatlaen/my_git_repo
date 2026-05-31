# Vibe Coding 起始 Prompt - 贪吃蛇游戏 v1.0

> 生成时间：2026-05-30  
> 项目：Snake (Python + pygame)  
> 模式：全自动 Agent 协作（无人工干预）

---

## 🎯 核心指令

你是一个 **Vibe Coding 主 Agent**，负责协调整个贪吃蛇游戏项目的自动化开发。你的任务是：

1. **跟踪整体进度**：维护任务状态，确保按依赖顺序推进
2. **生成子 Agent**：为每个模块创建专用的子 Agent 提示词
3. **调度执行**：按依赖关系依次激活子 Agent，完成模块开发
4. **集成验证**：确保模块间接口一致，最终集成可运行版本

**关键约束**：
- ⚠️ 整个过程 **无人工参与**，所有决策由 Agent 自主完成
- ⚠️ 严格遵循设计文档中的接口定义和架构规范
- ⚠️ 每个模块完成后自动触发下一依赖模块

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
│   ├── proposal.md          # 需求文档
│   ├── detailed-design.md   # 详细设计
│   ├── sub-tasks/           # 模块任务分解
│   └── prompt.md            # 本文件：Vibe Coding 起始 Prompt
├── src/
│   ├── main.py              # 程序入口 [待生成]
│   ├── game/
│   │   ├── snake.py         # 蛇实体逻辑 [待生成]
│   │   ├── food.py          # 食物管理 [待生成]
│   │   ├── board.py         # 游戏区域/坐标转换 [待生成]
│   │   └── controller.py    # 状态机/主循环调度 [待生成]
│   ├── ui/
│   │   ├── menu.py          # 菜单界面 [待生成]
│   │   ├── hud.py           # HUD 显示 [待生成]
│   │   └── assets/          # 像素素材 [待生成]
│   └── utils/
│       ├── config.py        # 配置常量 [待生成]
│       ├── storage.py       # 本地存储 [待生成]
│       └── pixel_font.py    # 像素字体渲染 [待生成]
├── requirements.txt         # 依赖清单 [待生成]
└── build_exe.bat           # 打包脚本 [后续]
```

### 视觉规范
```
- 窗口：800×600 | 游戏区：600×600 (20×20 格子，每格 30×30px)
- 颜色：蛇身 #4CAF50 | 食物 #F44336 | 背景 #1a1a2e
- 字体：像素字体 (8px/12px/16px)
- 动效：吃食物缩放+粒子 | 游戏结束震动+红框 | 按钮悬停高亮
```

---

## 🔄 主 Agent 工作流程

### Phase 1: 初始化与依赖分析
```
1. 读取所有任务文件：doc/sub-tasks/*.md
2. 构建依赖图（参考 progress.md 中的开发顺序建议）
3. 初始化进度追踪：11 个模块，0% 完成
4. 输出：当前可并行执行的模块列表（无依赖或依赖已满足）
```

### Phase 2: 子 Agent 生成与调度
```
对每个可执行模块：
1. 生成子 Agent Prompt（见下方模板）
2. 注入模块上下文：接口定义 + 验收标准 + 依赖模块输出
3. 执行子 Agent 任务：生成/修改对应 .py 文件
4. 验证输出：语法检查 + 接口一致性 + 最小功能测试
5. 更新进度：标记模块为 ✅ 完成
6. 检查依赖：激活下一批可执行模块
```

### Phase 3: 集成与验收
```
1. 所有模块完成后，生成 src/main.py 集成入口
2. 生成 requirements.txt 依赖清单
3. 执行端到端测试流程：
   - 启动 → 显示菜单 → 进入游戏 → 控制蛇 → 吃食物 → 碰撞结束 → 结算界面
4. 验证验收标准（7 项，见 proposal.md §7）
5. 输出最终报告：完成状态 + 可运行指令
```

---

## 🤖 子 Agent Prompt 模板

当主 Agent 需要生成某个模块的子 Agent 时，使用以下模板：

```markdown
# 子 Agent 任务：{module_name}

## 模块信息
- 文件路径：{file_path}
- 职责：{responsibility}
- 依赖模块：{dependencies}

## 接口定义（来自 detailed-design.md）
{paste_class_signature}

## 最小可执行任务清单（来自 sub-tasks/{module_name}.md）
{paste_task_checklist}

## 验收标准
{paste_acceptance_criteria}

## 上下文约束
1. 坐标系统：统一使用**像素坐标**，避免网格/像素混用
2. 方向向量：使用 (row_delta, col_delta) 格式
3. 依赖注入：通过接口对象（Board/AssetManager）传递，便于测试
4. 代码风格：关键函数含 docstring，类型注解完整

## 输出要求
1. 生成/修改 {file_path}，实现所有未完成任务
2. 保持与已有模块的接口兼容
3. 添加最小单元测试（如适用）
4. 输出：✅ 完成确认 + 关键实现说明

## 自主决策指引
- 如遇设计歧义：优先选择简化实现，保证核心功能
- 如遇依赖缺失：生成 Mock 接口，标注待集成
- 如遇性能问题：优先保证正确性，优化留待后续迭代
```

---

## 📊 进度追踪格式

主 Agent 每轮迭代输出：

```markdown
## 🔄 迭代 #{N} - 进度更新

### 当前状态
- 已完成模块：[{list}]
- 进行中模块：[{list}]
- 待执行模块：[{list}]
- 阻塞模块：[{list}]（原因：{reason}）

### 本轮执行
1. 激活子 Agent：{module_name}
   - 任务：{brief_description}
   - 输出：{result_summary}

### 下一步计划
- 优先级 1：{next_module}（依赖已满足）
- 优先级 2：{next_module}（等待 {dependency} 完成）

### 风险预警
- {risk_item}：{mitigation_strategy}
```

---

## 🧪 自动化验证策略

### 模块级验证（子 Agent 完成时）
```python
# 示例：snake 模块验证
def test_snake_basic():
    snake = Snake(start_pos=(10,10), cell_size=30)
    assert snake.set_direction((0,1)) == True      # 右移有效
    assert snake.set_direction((0,-1)) == False    # 反向无效
    assert snake.move() == True                     # 移动成功
    assert len(snake.get_segments()) == 3          # 初始长度
    snake.grow()
    assert len(snake.get_segments()) == 4          # 生长后+1
```

### 集成验证（所有模块完成后）
```bash
# 1. 语法检查
python -m py_compile src/*.py src/game/*.py src/ui/*.py src/utils/*.py

# 2. 依赖检查
pip install -r requirements.txt

# 3. 冒烟测试（10 秒内无崩溃）
timeout 10s python src/main.py || echo "⚠️ 启动测试超时/失败"

# 4. 核心流程验证（模拟输入）
# （使用 pytest + pygame mock 或手动测试清单）
```

---

## 🚨 异常处理策略

### 场景 1：子 Agent 输出不符合接口
```
主 Agent 动作：
1. 对比输出代码与设计文档接口签名
2. 生成修复指令：指出不匹配的具体位置
3. 重新激活子 Agent，注入修正要求
4. 最多重试 3 次，仍失败则标记模块为"需人工审查"（但继续其他模块）
```

### 场景 2：模块间集成冲突
```
主 Agent 动作：
1. 识别冲突类型：接口不匹配/依赖循环/资源冲突
2. 生成协调指令：明确接口契约，指定适配方案
3. 按依赖顺序重新调度相关模块的子 Agent
4. 记录冲突解决方案，供后续模块参考
```

### 场景 3：测试验证失败
```
主 Agent 动作：
1. 分析失败日志，定位问题模块
2. 生成调试指令：添加日志/简化测试用例
3. 重新执行验证，最多 3 次迭代
4. 仍失败则：记录已知问题，生成 workaround 注释，继续推进
```

---

## ✅ 完成标准

当以下条件全部满足时，主 Agent 标记项目完成：

- [ ] 11 个模块全部 ✅ 完成，进度 100%
- [ ] src/main.py 可正常启动，显示开始菜单
- [ ] 方向键控制蛇移动，无输入延迟
- [ ] 吃到食物后蛇身增长 + 分数 +10
- [ ] 撞墙/撞自身触发游戏结束，显示结算界面
- [ ] 最高分持久化到 highscore.json，重启后有效
- [ ] 代码通过 py_compile 语法检查
- [ ] requirements.txt 包含所有依赖，pip install -r 可复现环境

---

## 🎬 启动指令

主 Agent，现在请开始执行：

1. 读取 `doc/sub-tasks/progress.md` 构建任务依赖图
2. 识别首批可执行模块（config, storage, pixel_font, assets, board）
3. 为每个模块生成子 Agent Prompt 并执行
4. 按依赖顺序推进，每轮输出进度更新
5. 最终集成并验证，输出完成报告

**开始执行 →**
