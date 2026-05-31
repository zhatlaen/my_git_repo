import sys, os
sys.path.insert(0, "src")

from utils.config import load_config, STORAGE_PATH, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, BOARD_ROWS, BOARD_COLS
print("Config: GRID=%d, ROWS=%d, COLS=%d" % (GRID_SIZE, BOARD_ROWS, BOARD_COLS))
print("Window: %dx%d, Sidebar: %dpx" % (WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH - BOARD_COLS*GRID_SIZE))

from utils.storage import load_highscore, save_highscore
hs = load_highscore(STORAGE_PATH)
print("High score loaded: %d" % hs)

from utils.pixel_font import PixelFont
pf = PixelFont(default_size=12)
surf = pf.render("Test", size=16, color=(255,255,255))
print("PixelFont surface: %dx%d" % (surf.get_width(), surf.get_height()))

from game.board import Board
b = Board(load_config())
px = b.to_pixel((0, 0))
print("Board to_pixel(0,0): %s" % str(px))
print("Board bounds: %s" % str(b.get_bounds_rect()))

from game.snake import Snake
s = Snake((10, 10), 30, initial_length=3)
s.set_direction(Snake.DIR_RIGHT)
s.move()
segs = s.get_segments()
head = s.get_head_pos()
print("Snake len=%d, head=%s, segs[0]=%s" % (s.length, str(head), str(segs[0])))
collision = s.check_collision((-1,-1, 1000, 1000))
print("Collision check (safe area): %s" % collision)

# Test reverse direction blocked
result = s.set_direction(Snake.DIR_LEFT)
print("Reverse direction blocked: %s" % str(not result))

# Test food respawn with snake segments
from ui.assets import AssetManager
am = AssetManager(30)
from game.food import Food
f = Food(b, am)
f.respawn(segs)
food_pos = f.get_position()
print("Food spawned at: %s" % str(food_pos))

# Test menu imports
from ui.menu import Menu, MenuType, MenuAction
m = Menu(pf)
print("Menu type %s, action %s" % (MenuType.START.name, MenuAction.NONE.name))

# Test HUD
from ui.hud import HUD
hud = HUD(pf)
hud.update(100, 50, 10, speed_ratio=1.2)
print("HUD updated: score=%d, high=%d, length=%d" % (hud._score, hud._high_score, hud._snake_length))

print("\nAll core module tests PASSED!")
