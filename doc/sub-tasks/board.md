# 模块任务：board（游戏区域与坐标转换）

> 文件：src/game/board.py  
> 职责：游戏区域管理 + 网格/像素坐标双向转换

## ? 最小可执行任务清单

- [ ] **初始化配置**：实现 __init__(config)，解析 GRID_SIZE/BOARD_COLS/BOARD_ROWS 等参数
- [ ] **网格转像素**：实现 	o_pixel(grid_pos)，(row,col) → (x,y) 左上角像素坐标
- [ ] **像素转网格**：实现 	o_grid(pixel_pos)，(x,y) → (row,col) 网格索引
- [ ] **越界检测**：实现 is_out_of_bounds(pixel_pos)，判断坐标是否超出游戏区域
- [ ] **获取边界**：实现 get_bounds_rect()，返回 (left, top, right, bottom) 像素边界
- [ ] **纯函数测试**：为坐标转换函数编写断言测试，验证双向转换一致性

## ?? 验收标准

- [ ] 	o_pixel(to_grid(pos)) == pos 对区域内任意像素坐标成立
- [ ] 越界检测边界值测试通过（刚好在边界内/外）
- [ ] 所有转换函数为纯函数，无副作用，可直接单元测试
- [ ] 配置参数变更后，转换逻辑自动适配
