# 贪吃蛇游戏 - 概要设计文档

> 版本：v1.0  
> 日期：2026-05-29  
> 基于需求文档：`./doc/proposal.md`

---

## 1. 系统架构总览

```
┌─────────────────────────────────────────┐
│              main.py (入口)              │
├─────────────────────────────────────────┤
│  • 初始化 pygame / 加载配置 / 启动主循环  │
│  • 依赖：config, storage, controller    │
└────────────────┬────────────────────────┘
                 │
    ┌────────────▼────────────┐
    │   controller.py (核心)   │
    │   游戏状态机 + 主循环调度  │
    ├─────────────────────────┤
    │  • handle_input()       │
    │  • update() / render()  │
    │  • set_state()          │
    └────┬────┬────┬────┬─────┘
         │    │    │    │
    ┌────▼─┐ ┌▼────┐ ┌▼────┐ ┌▼─────┐
    │snake │ │food │ │board│ │menu  │
    │.py   │ │.py  │ │.py  │ │.py   │
    └──────┘ └─────┘ └─────┘ └──────┘
         │         │         │
    ┌────▼─────────▼─────────▼────┐
    │        hud.py + assets/      │
    │   UI 渲染 / 精灵加载 / 字体    │
    └────────────┬────────────────┘
                 │
    ┌────────────▼────────────┐
    │   utils/storage.py      │
    │   本地存储 (highscore)   │
    └─────────────────────────┘
```

---

## 2. 模块划分与职责

### 2.1 Core Game 模块 (`src/game/`)

| 模块 | 职责 | 关键接口 | 依赖 |
|------|------|----------|------|
| `snake.py` | 蛇的移动/生长/碰撞逻辑 | `move(dir)`, `grow()`, `check_collision(head, body)`, `get_segments()` | `board.py` (坐标转换) |
| `food.py` | 食物生成与绘制 | `respawn(snake_body)`, `get_position()`, `draw(surface)` | `board.py`, `assets/` |
| `board.py` | 游戏区域管理 + 坐标转换 | `to_pixel(grid_pos)`, `to_grid(pixel_pos)`, `is_out_of_bounds(pos)` | `config.py` |
| `controller.py` | **游戏状态机 + 输入分发 + 主循环** | `handle_input(events)`, `update()`, `render(surface)`, `set_state(new_state)` | 全部 game/ui 模块 |

### 2.2 UI 模块 (`src/ui/`)

| 模块 | 职责 | 关键接口 | 依赖 |
|------|------|----------|------|
| `menu.py` | 开始/暂停/结算界面渲染与交互 | `draw(surface, bg_snapshot)`, `handle_input(events) -> MenuAction` | `assets/`, `pixel_font.py` |
| `hud.py` | 实时 HUD 显示（分数/进度条） | `update(score, high, length)`, `draw(surface)` | `pixel_font.py` |
| `assets/` | 像素精灵资源管理 | `load_sprite(name) -> Surface`, `get_animation(name) -> list` | pygame.image |

### 2.3 Utils 模块 (`src/utils/`)

| 模块 | 职责 | 关键接口 | 依赖 |
|------|------|----------|------|
| `config.py` | **启动时读取**的配置常量 | `get(key)`, `GRID_SIZE`, `INITIAL_FPS`, `COLORS` | json |
| `storage.py` | 本地数据持久化 | `load_highscore()`, `save_highscore(score)` | json, pathlib |
| `pixel_font.py` | 像素字体渲染辅助 | `render(text, size_px) -> Surface` | pygame.font |

### 2.4 入口模块 (`src/main.py`)

```python
def main():
    # 1. 初始化
    pygame.init()
    config = load_config()              # 仅启动时读取
    high_score = storage.load_highscore()
    
    # 2. 创建核心对象
    board = Board(config)
    controller = GameController(config, board, high_score)
    
    # 3. 主循环
    while controller.running:
        events = pygame.event.get()
        controller.handle_input(events)  # 状态机分发
        controller.update()              # 逻辑更新 (帧率动态调整)
        controller.render(screen)        # 分层渲染
        pygame.display.flip()
```

---

## 3. 模块间依赖关系

```
main.py
  │
  ├──► config.py (只读配置)
  ├──► storage.py (读/写 highscore.json)
  │
  └──► controller.py ──┬──► snake.py ──┬──► board.py
                       │               └──► config.py (GRID_SIZE)
                       ├──► food.py ───┬──► board.py
                       │               └──► assets/ (sprite)
                       ├──► board.py ──┴──► config.py
                       │
                       └──► menu.py ───┬──► assets/
                                       ├──► pixel_font.py
                                       └──► hud.py (结算时复用)
```

**依赖原则**：
- 单向依赖：上层模块依赖下层，禁止循环依赖
- `controller.py` 作为协调者，不直接操作 pygame.Surface，渲染委托给 UI 模块
- 所有模块通过 `board.py` 进行坐标系统一转换，避免像素/格子坐标混用

---

## 4. 关键设计决策

### 4.1 游戏循环与速度控制
- **策略**：直接调整 `pygame.time.Clock().tick(fps)` 的帧率参数
- **实现**：`controller.py` 维护 `current_fps`，蛇每增长 5 节 → `current_fps *= 1.1` (上限 150%)
- **优势**：逻辑简单，与需求"速度机制"直接映射

### 4.2 暂停/结算的状态冻结
- **暂停**：`controller.set_state(PAUSED)` → 停止 `update()` 调用，`menu.py` 渲染半透明遮罩 + 选项
- **结算**：保留当前 `screen` 作为背景快照 → `menu.py` 绘制结算面板叠加 → 用户选择后重置或返回

### 4.3 像素素材加载策略
- **方案**：预先切好的单格精灵 (30×30px PNG)
- **加载时机**：游戏启动时一次性加载到 `assets/` 缓存字典
- **内存管理**：精灵尺寸固定，无需动态缩放，避免运行时性能开销

### 4.4 碰撞检测实现
- **坐标系统**：统一使用**像素坐标**进行检测（与渲染坐标系一致）
- **蛇头碰撞**：`snake.py` 中 `check_collision(head_pixel_pos, body_segments_pixel_list)` 遍历检测矩形重叠
- **边界检测**：`board.is_out_of_bounds(pixel_pos)` 基于游戏区域像素边界 (0~600)

### 4.5 配置加载策略
- **时机**：仅在 `main.py` 启动时读取 `config.py`
- **热更新**：不支持运行时修改，确保游戏逻辑稳定性
- **扩展点**：配置项采用字典 + 默认值模式，便于后续新增参数

---

## 5. 数据流设计

### 5.1 游戏主循环数据流
```
[输入事件] 
    │
    ▼
controller.handle_input() 
    ├── 方向键 → snake.set_direction()
    ├── P 键 → set_state(PAUSED)
    └── 菜单选择 → set_state(PLAYING/START/GAME_OVER)
    │
    ▼
controller.update() [仅 PLAYING 状态执行]
    ├── snake.move() → 更新蛇身像素坐标列表
    ├── 检测蛇头 & 食物重叠 → snake.grow() + score+=10 + food.respawn()
    ├── 检测蛇头 & 墙/身体重叠 → set_state(GAME_OVER)
    ├── 速度更新：每 5 节增长 → current_fps *= 1.1
    └── hud.update(score, high_score, len(snake.body))
    │
    ▼
controller.render(surface)
    ├── board.draw_background()
    ├── snake.draw(surface, assets)      # 按身体顺序绘制精灵
    ├── food.draw(surface, assets)
    ├── hud.draw(surface)                # 分数/进度条
    └── if paused/game_over: menu.draw(surface, bg_snapshot)
```

### 5.2 分数持久化流程
```
游戏结束结算时:
    │
    ▼
if current_score > high_score:
    ├── storage.save_highscore(current_score)  # 写入 highscore.json
    ├── config.HIGH_SCORE = current_score      # 更新内存值
    └── hud 标记"新纪录"动效
```

---

## 6. 接口规范摘要

### 6.1 Snake 类
```python
class Snake:
    def __init__(self, start_pos: PixelPos, cell_size: int): ...
    def set_direction(self, new_dir: Vector2) -> bool:  # 禁止 180° 反向
    def move(self) -> None:  # 按当前方向移动一格
    def grow(self) -> None:  # 尾部增加一节
    def check_collision(self, bounds: Rect, body: list[PixelPos]) -> CollisionType
    def get_segments(self) -> list[PixelPos]:  # 返回当前身体像素坐标列表
```

### 6.2 Controller 类（状态机核心）
```python
class GameController:
    def __init__(self, config: dict, board: Board, high_score: int): ...
    
    # 状态机
    def set_state(self, new_state: GameState) -> None
    def handle_input(self, events: list[Event]) -> None  # 按当前状态分发
    def update(self) -> None  # 仅 PLAYING 状态执行逻辑更新
    def render(self, surface: Surface) -> None  # 分层渲染所有元素
    
    # 属性
    @property def running(self) -> bool: ...
    @property def score(self) -> int: ...
```

### 6.3 Menu 类
```python
class Menu:
    def __init__(self, menu_type: MenuType, assets: AssetManager): ...
    def draw(self, surface: Surface, background: Optional[Surface] = None) -> None
    def handle_input(self, events: list[Event]) -> Optional[MenuAction]  # 返回用户选择
```

---

## 7. 扩展性设计

- **模块隔离**：游戏逻辑 (`game/`) 与渲染 (`ui/`) 分离，便于后续替换渲染后端
- **配置驱动**：格子大小、颜色、速度参数均通过 `config.py` 管理，支持快速调整
- **资源抽象**：`assets/` 通过名称加载精灵，新增素材只需添加文件 + 注册键名
- **状态机模式**：`controller.py` 采用显式状态枚举，新增游戏模式（如双人）只需扩展状态分支

---

## 8. 验收标准映射

| 验收项 | 设计保障 |
|--------|----------|
| 方向键控制流畅 | `controller.handle_input()` 直接映射方向，无中间队列延迟 |
| 碰撞检测准确 | 像素坐标统一 + 矩形重叠检测，`board.py` 提供边界校验 |
| UI 界面正常切换 | `Menu` 类独立渲染 + 背景快照机制，状态切换无闪烁 |
| 最高分持久化 | `storage.py` 封装 json 读写，游戏结束自动校验保存 |
| 代码结构清晰 | 模块职责单一 + 接口文档 + 关键函数 docstring |
| 依赖可安装 | `requirements.txt` 锁定 pygame==2.5.2，入口 `main.py` 标准化 |

---

> 📌 **后续开发建议**  
> 1. 优先实现 `board.py` + `snake.py` 核心逻辑，验证碰撞与移动  
> 2. 使用占位色块代替精灵素材，加速 Phase 2 核心玩法验证  
> 3. `controller.py` 状态机先实现 `PLAYING` → `GAME_OVER` 最小闭环，再扩展菜单状态  
> 4. 每完成一个模块，编写最小单元测试（如 `snake.test_move()`）
