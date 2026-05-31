# 贪吃蛇游戏 - 详细设计文档

> 版本：v1.0  
> 日期：2026-05-30  
> 基于概要设计：./abstract-design.md

---

## 1. Core Game 模块 (src/game/)

### 1.1 snake.py - 蛇实体逻辑

`python
class Snake:
    """蛇实体，管理移动、生长、碰撞检测"""
    
    def __init__(self, start_pos: tuple[int, int], cell_size: int, initial_length: int = 3):
        """
        初始化蛇
        :param start_pos: 起始网格坐标 (row, col)
        :param cell_size: 每个格子的像素尺寸
        :param initial_length: 初始身体长度
        """
    
    def set_direction(self, new_dir: tuple[int, int]) -> bool:
        """
        设置移动方向（禁止180°反向）
        :param new_dir: 方向向量，如 (0, 1) 表示右
        :return: 方向是否设置成功
        """
    
    def move(self) -> bool:
        """
        按当前方向移动一格
        :return: 移动是否成功（未撞墙/未撞自身）
        """
    
    def grow(self) -> None:
        """蛇生长：尾部增加一节，不移除尾节点"""
    
    def check_collision(self, bounds: tuple[int, int, int, int]) -> str:
        """
        检测碰撞类型
        :param bounds: 游戏区域边界 (left, top, right, bottom) 像素坐标
        :return: 'none' | 'wall' | 'self'
        """
    
    def get_segments(self) -> list[tuple[int, int]]:
        """
        获取蛇身所有段的像素坐标列表
        :return: [(x1,y1), (x2,y2), ...] 从头到尾
        """
    
    def get_head_pos(self) -> tuple[int, int]:
        """获取蛇头像素坐标"""
`

### 1.2 food.py - 食物管理

`python
class Food:
    """食物生成与绘制"""
    
    def __init__(self, board: 'Board', assets: 'AssetManager'):
        """
        :param board: 游戏区域对象，用于坐标转换
        :param assets: 资源管理器，用于加载食物精灵
        """
    
    def respawn(self, snake_segments: list[tuple[int, int]]) -> None:
        """
        在空白位置重新生成食物
        :param snake_segments: 当前蛇身坐标列表，用于避让
        """
    
    def get_position(self) -> tuple[int, int]:
        """获取食物当前像素坐标"""
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        绘制食物到指定表面
        :param surface: pygame.Surface 渲染目标
        """
`

### 1.3 board.py - 游戏区域与坐标转换

`python
class Board:
    """游戏区域管理 + 网格/像素坐标转换"""
    
    def __init__(self, config: dict):
        """
        :param config: 配置字典，含 GRID_SIZE, BOARD_COLS, BOARD_ROWS 等
        """
    
    def to_pixel(self, grid_pos: tuple[int, int]) -> tuple[int, int]:
        """
        网格坐标转像素坐标
        :param grid_pos: (row, col)
        :return: (x, y) 左上角像素坐标
        """
    
    def to_grid(self, pixel_pos: tuple[int, int]) -> tuple[int, int]:
        """
        像素坐标转网格坐标
        :param pixel_pos: (x, y)
        :return: (row, col)
        """
    
    def is_out_of_bounds(self, pixel_pos: tuple[int, int]) -> bool:
        """
        检测像素坐标是否超出游戏区域
        :param pixel_pos: (x, y)
        :return: True 表示越界
        """
    
    def get_bounds_rect(self) -> tuple[int, int, int, int]:
        """获取游戏区域像素边界 (left, top, right, bottom)"""
`

### 1.4 controller.py - 游戏状态机与主循环调度

`python
from enum import Enum

class GameState(Enum):
    START = "start"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class GameController:
    """游戏核心控制器：状态机 + 输入分发 + 更新渲染调度"""
    
    def __init__(self, config: dict, board: Board, high_score: int):
        """
        :param config: 配置字典
        :param board: 游戏区域对象
        :param high_score: 历史最高分
        """
    
    def set_state(self, new_state: GameState) -> None:
        """切换游戏状态"""
    
    def handle_input(self, events: list[pygame.event.Event]) -> None:
        """
        处理输入事件，按当前状态分发
        :param events: pygame 事件列表
        """
    
    def update(self) -> None:
        """执行游戏逻辑更新（仅 PLAYING 状态有效）"""
    
    def render(self, surface: pygame.Surface) -> None:
        """
        分层渲染所有游戏元素
        :param surface: 主渲染表面
        """
    
    @property
    def running(self) -> bool:
        """主循环是否继续"""
    
    @property
    def score(self) -> int:
        """当前分数"""
`

---

## 2. UI 模块 (src/ui/)

### 2.1 menu.py - 菜单界面

`python
from enum import Enum

class MenuType(Enum):
    START = "start"
    PAUSE = "pause"
    GAME_OVER = "game_over"

class MenuAction(Enum):
    START_GAME = "start"
    RESUME = "resume"
    RESTART = "restart"
    QUIT = "quit"
    NONE = "none"

class Menu:
    """菜单界面渲染与交互"""
    
    def __init__(self, menu_type: MenuType, assets: 'AssetManager', score: int = 0, high_score: int = 0):
        """
        :param menu_type: 菜单类型
        :param assets: 资源管理器
        :param score: 当前分数（GAME_OVER 时显示）
        :param high_score: 历史最高分
        """
    
    def draw(self, surface: pygame.Surface, background: pygame.Surface = None) -> None:
        """
        绘制菜单界面
        :param surface: 渲染目标
        :param background: 可选背景快照，用于暂停时半透明遮罩
        """
    
    def handle_input(self, events: list[pygame.event.Event]) -> MenuAction:
        """
        处理菜单输入
        :param events: pygame 事件列表
        :return: 用户选择的动作
        """
`

### 2.2 hud.py - 实时信息显示

`python
class HUD:
    """HUD：分数/最高分/蛇长度实时显示"""
    
    def __init__(self, config: dict, font: 'PixelFont'):
        """
        :param config: 配置字典
        :param font: 像素字体渲染器
        """
    
    def update(self, score: int, high_score: int, snake_length: int) -> None:
        """
        更新显示数据
        :param score: 当前分数
        :param high_score: 历史最高分
        :param snake_length: 当前蛇长度
        """
    
    def draw(self, surface: pygame.Surface) -> None:
        """绘制 HUD 到指定表面"""
`

### 2.3 assets/ - 资源管理

`python
class AssetManager:
    """像素精灵资源缓存与管理"""
    
    def __init__(self, asset_dir: str):
        """
        :param asset_dir: 资源文件目录路径
        """
    
    def load_sprite(self, name: str) -> pygame.Surface:
        """
        加载并缓存精灵
        :param name: 资源键名，如 'snake_head', 'food_apple'
        :return: pygame.Surface 对象
        """
    
    def get_animation(self, name: str) -> list[pygame.Surface]:
        """
        获取动画帧序列
        :param name: 动画资源键名
        :return: 帧列表
        """
`

---

## 3. Utils 模块 (src/utils/)

### 3.1 config.py - 配置常量

`python
# 配置加载（启动时一次性读取）
def load_config(config_path: str = "config.json") -> dict:
    """
    加载配置文件
    :param config_path: 配置文件路径
    :return: 配置字典
    """

# 常用常量（示例）
GRID_SIZE: int = 20          # 网格单元像素尺寸
BOARD_COLS: int = 30         # 游戏区域列数
BOARD_ROWS: int = 30         # 游戏区域行数
INITIAL_FPS: int = 8         # 初始帧率
SPEED_INCREMENT: float = 1.1 # 每增长5节的速度倍率
COLORS: dict = { ... }       # 颜色定义
`

### 3.2 storage.py - 本地数据持久化

`python
def load_highscore(storage_path: str = "data/highscore.json") -> int:
    """
    读取历史最高分
    :param storage_path: 存储文件路径
    :return: 最高分值，文件不存在时返回 0
    """

def save_highscore(score: int, storage_path: str = "data/highscore.json") -> bool:
    """
    保存最高分
    :param score: 要保存的分数
    :param storage_path: 存储文件路径
    :return: 是否保存成功
    """
`

### 3.3 pixel_font.py - 像素字体渲染

`python
class PixelFont:
    """像素风格字体渲染辅助"""
    
    def __init__(self, font_path: str, default_size: int):
        """
        :param font_path: 字体文件路径
        :param default_size: 默认字号（像素）
        """
    
    def render(self, text: str, size: int = None, color: tuple = (255, 255, 255)) -> pygame.Surface:
        """
        渲染文本为表面
        :param text: 待渲染文本
        :param size: 字号（可选，默认使用初始化值）
        :param color: RGB 颜色三元组
        :return: 渲染后的 pygame.Surface
        """
`

---

## 4. 入口模块 (src/main.py)

`python
def main() -> None:
    """
    程序入口：初始化 + 主循环
    职责：
    1. 初始化 pygame 与显示窗口
    2. 加载配置与持久化数据
    3. 创建核心对象（Board, GameController, AssetManager 等）
    4. 执行主循环：事件→更新→渲染
    5. 资源清理与退出
    """

if __name__ == "__main__":
    main()
`

---

## 5. 关键数据流说明

### 5.1 输入事件分发
`
pygame.event.get() 
    ↓
controller.handle_input(events)
    ├── GameState.START/GAME_OVER: Menu.handle_input() → MenuAction
    ├── GameState.PLAYING: 方向键 → snake.set_direction()
    └── GameState.PAUSED: P键/菜单选择 → set_state()
`

### 5.2 游戏更新流程（仅 PLAYING）
`
controller.update()
    ├── snake.move() → 更新蛇身坐标
    ├── 碰撞检测:
    │   ├── board.is_out_of_bounds(snake.head) → GAME_OVER
    │   └── snake.check_collision() → GAME_OVER
    ├── 食物检测:
    │   └── snake.head == food.pos → snake.grow() + score+=10 + food.respawn()
    ├── 速度调整: len(snake) % 5 == 0 → fps *= SPEED_INCREMENT
    └── hud.update(score, high_score, len(snake))
`

### 5.3 渲染分层顺序
`
1. board.draw_background()     # 底层网格/背景
2. snake.draw(surface)         # 蛇身（按顺序绘制保证头部在上）
3. food.draw(surface)          # 食物
4. hud.draw(surface)           # UI 分数栏
5. if 非 PLAYING: menu.draw()  # 菜单遮罩层（最上层）
`

---

## 6. 模块独立测试建议（可选）

> 虽不强制，但以下设计便于后续单元测试：

- **snake.py**: move() / check_collision() 可独立调用，无需 pygame 初始化
- **board.py**: 坐标转换函数为纯函数，可直接断言测试
- **food.py**: 
espawn() 接收蛇身列表，可传入模拟数据验证避让逻辑
- **storage.py**: 文件路径参数化，测试时可传入临时路径避免污染真实数据

---

> ?? **开发提示**  
> - 所有坐标计算统一使用**像素坐标**，避免网格/像素混用导致偏差  
> - 方向向量使用 (row_delta, col_delta) 格式，与网格坐标一致  
> - 模块间通过接口对象（如 Board, AssetManager）依赖，便于 Mock 测试
