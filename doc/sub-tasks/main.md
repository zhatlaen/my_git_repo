# 模块任务：main（程序入口）

> 文件：src/main.py  
> 职责：程序初始化 + 主循环调度 + 资源清理

## ? 最小可执行任务清单

- [ ] **Pygame初始化**：pygame.init() + 设置窗口标题/图标 + 创建800×600显示表面
- [ ] **配置加载**：调用 load_config() 加载游戏参数，处理加载异常
- [ ] **持久化加载**：调用 load_highscore() 读取历史最高分
- [ ] **资源初始化**：创建 AssetManager/Board/GameController 等核心对象
- [ ] **主循环结构**：实现 while controller.running: 循环，按帧率控制更新节奏
- [ ] **事件处理**：每帧获取 pygame.event.get()，传给 controller.handle_input()
- [ ] **逻辑更新**：PLAYING 状态调用 controller.update() 执行游戏逻辑
- [ ] **分层渲染**：清屏 → controller.render() → pygame.display.flip()
- [ ] **帧率控制**：使用 pygame.time.Clock() 维持目标FPS，支持动态加速
- [ ] **资源清理**：循环退出后调用 pygame.quit()，确保资源正确释放
- [ ] **入口保护**：if __name__ == '__main__': main() 标准入口写法
- [ ] **启动测试**：验证程序能正常启动→显示菜单→进入游戏→退出，无崩溃

## ?? 验收标准

- [ ] 程序启动后显示开始菜单，无黑屏/闪退
- [ ] 主循环帧率稳定，无内存泄漏迹象
- [ ] 退出游戏后进程完全结束，无僵尸进程
- [ ] 各模块依赖注入正确，无循环导入问题
- [ ] 代码含关键步骤注释，便于后续维护
