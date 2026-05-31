# 模块任务：controller（游戏状态机与主循环调度）

> 文件：src/game/controller.py  
> 职责：状态机管理 + 输入分发 + 更新/渲染调度

## ? 最小可执行任务清单

- [ ] **状态枚举**：定义 GameState Enum：START/PLAYING/PAUSED/GAME_OVER
- [ ] **初始化**：实现 __init__，接收 config/board/high_score，初始化游戏对象和状态
- [ ] **状态切换**：实现 set_state(new_state)，安全切换游戏状态
- [ ] **输入分发-菜单态**：handle_input 在 START/GAME_OVER 状态分发到菜单选择
- [ ] **输入分发-游戏态**：handle_input 在 PLAYING 状态将方向键传给 snake.set_direction
- [ ] **输入分发-暂停态**：handle_input 在 PAUSED 状态处理继续/重开/返回选项
- [ ] **逻辑更新**：实现 update()，仅 PLAYING 状态执行：蛇移动→碰撞检测→食物检测→分数更新→速度调整
- [ ] **分层渲染**：实现 ender(surface)，按顺序绘制：背景→蛇→食物→HUD→菜单遮罩
- [ ] **属性访问**：实现 unning 和 score 属性，供主循环查询
- [ ] **状态流转测试**：验证各状态间切换逻辑和输入响应正确性

## ?? 验收标准

- [ ] 四种状态可正常切换，无状态丢失
- [ ] 输入事件按当前状态正确分发，无误触发
- [ ] update() 仅在 PLAYING 状态执行游戏逻辑
- [ ] 渲染顺序正确，菜单遮罩始终在最上层
- [ ] 主循环可通过 unning 属性正常退出
