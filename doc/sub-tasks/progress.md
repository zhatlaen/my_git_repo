# ?? 贪吃蛇游戏 - 任务总体进度

> 最后更新：2026-05-30  
> 使用说明：每完成一个模块的所有子任务后，勾选下方对应模块；所有模块完成后项目v1.0即达成

---

## ?? 模块完成状态

### ?? Core Game 模块
- [ ] **snake** - 蛇实体逻辑（移动/生长/碰撞）→ [./snake.md](./snake.md)
- [ ] **food** - 食物管理（生成/绘制/避让）→ [./food.md](./food.md)
- [ ] **board** - 游戏区域与坐标转换 → [./board.md](./board.md)
- [ ] **controller** - 游戏状态机与主循环调度 → [./controller.md](./controller.md)

### ?? UI 模块
- [ ] **menu** - 开始/暂停/结算菜单界面 → [./menu.md](./menu.md)
- [ ] **hud** - 分数/进度条/HUD显示 → [./hud.md](./hud.md)
- [ ] **assets** - 像素精灵资源缓存管理 → [./assets.md](./assets.md)

### ?? Utils 模块
- [ ] **config** - 配置常量与加载 → [./config.md](./config.md)
- [ ] **storage** - 本地数据持久化（最高分） → [./storage.md](./storage.md)
- [ ] **pixel_font** - 像素字体渲染辅助 → [./pixel_font.md](./pixel_font.md)

### ?? 入口模块
- [ ] **main** - 程序入口与主循环调度 → [./main.md](./main.md)

---

## ?? 进度统计

| 模块分类 | 模块数 | 已完成 | 进度 |
|---------|--------|--------|------|
| Core Game | 4 | 0 | 0% |
| UI | 3 | 0 | 0% |
| Utils | 3 | 0 | 0% |
| Entry | 1 | 0 | 0% |
| **总计** | **11** | **0** | **0%** |

---

## ?? 开发顺序建议（依赖关系）

`
1?? 基础层（无依赖，优先完成）
   ├─ config → storage → pixel_font → assets
   └─ board（纯坐标转换，可独立测试）

2?? 核心层（依赖基础层）
   ├─ snake（依赖board坐标转换）
   ├─ food（依赖board+assets）
   └─ controller（依赖snake+food+board+hud）

3?? 表现层（依赖核心层+基础层）
   ├─ hud（依赖config+pixel_font）
   └─ menu（依赖pixel_font+assets）

4?? 集成层（依赖以上所有）
   └─ main（组装所有模块，执行主循环）
`

---

## ? 验收检查清单（项目级）

- [ ] 方向键控制流畅，无输入延迟
- [ ] 碰撞检测准确，无穿模/漏判
- [ ] 所有UI界面可正常切换，无卡死
- [ ] 最高分本地持久化，重启后仍有效
- [ ] 代码结构清晰，关键函数含docstring
- [ ] 提供 requirements.txt，pip install -r 可直接运行
- [ ] 像素风格视觉统一，无模糊/错位元素
- [ ] 游戏流程完整：开始→游戏→暂停→结算→重开

---

> ?? **VibeCoding 提示**  
> - 每个模块任务文件中的子任务均为**最小可执行单元**，建议逐个勾选完成  
> - 完成一个模块后，可运行简单测试验证功能，再进入下一模块  
> - 遇到阻塞问题时，先完成其他无依赖模块，保持开发节奏  
> - 所有任务文件支持直接复制到AI助手作为上下文，实现"对话即编码"
