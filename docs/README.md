# 📚 Agenta 项目文档

欢迎来到 Agenta 项目文档中心！本目录包含了项目的所有架构设计和开发文档。

## 🗂️ 文档结构

### 核心架构文档

1. **[ARCHITECTURE.md](ARCHITECTURE.md)** - 最终架构设计文档 ⭐
   - 完整的系统架构设计
   - 四层架构详细说明
   - 技术栈选型和实现细节
   - 安全模型和扩展机制
   - **这是最重要的架构参考文档**

2. **[ARCHITECTURE_SUMMARY.md](ARCHITECTURE_SUMMARY.md)** - 架构文档快速导航
   - ARCHITECTURE.md 的目录和快速索引
   - 帮助快速定位具体章节
   - 适合需要查找特定内容的开发者

### 开发计划与路线图

3. **[PLAN.md](PLAN.md)** - 开发路线图
   - 四阶段开发计划（Phase 0-3）
   - 每个阶段的功能清单和验收标准
   - 技术选型建议
   - 参考 OpenCode 的设计经验

4. **[PHASE0_SUMMARY.md](PHASE0_SUMMARY.md)** - Phase 0 实施总结
   - Phase 0 的完成情况
   - 已实现的核心组件
   - 验收标准对照
   - 下一步计划

### 使用指南

5. **[QUICKSTART.md](QUICKSTART.md)** - 快速开始指南
   - 安装说明
   - 配置方法
   - 使用示例
   - 多 LLM 提供商支持
   - 故障排查

### 任务总结文档

6. **[TASK_COMPLETION.md](TASK_COMPLETION.md)** - 架构文档创建任务总结
   - 架构文档创建过程
   - 交付物清单
   - 质量保证说明
   - 与其他文档的关系

### 历史文档

7. **[ARCH.md](ARCH.md)** - 早期架构讨论（已废弃）
   - 早期的架构设计思路
   - 已被 ARCHITECTURE.md 取代
   - 仅供参考

## 🎯 阅读指南

### 如果你是新加入的开发者
推荐阅读顺序：
1. 从 [QUICKSTART.md](QUICKSTART.md) 开始，了解如何使用 Agenta
2. 阅读 [PLAN.md](PLAN.md) 了解项目的整体规划
3. 浏览 [ARCHITECTURE.md](ARCHITECTURE.md) 理解系统架构
4. 查看 [PHASE0_SUMMARY.md](PHASE0_SUMMARY.md) 了解当前进度

### 如果你需要实现新功能
推荐阅读顺序：
1. 查看 [PLAN.md](PLAN.md) 确认功能在哪个阶段
2. 参考 [ARCHITECTURE.md](ARCHITECTURE.md) 的相关章节
3. 使用 [ARCHITECTURE_SUMMARY.md](ARCHITECTURE_SUMMARY.md) 快速定位实现细节

### 如果你需要了解系统设计
推荐阅读：
1. [ARCHITECTURE.md](ARCHITECTURE.md) 第 79-151 行 - 四层架构图
2. [ARCHITECTURE.md](ARCHITECTURE.md) 第 580-678 行 - 数据流说明
3. [ARCHITECTURE.md](ARCHITECTURE.md) 第 708-783 行 - 安全模型

## 📖 文档维护

### 更新原则
- **ARCHITECTURE.md** 是架构的最终权威文档
- 所有架构变更必须同步更新 ARCHITECTURE.md
- PLAN.md 描述计划，PHASE*_SUMMARY.md 描述实际完成情况
- 保持文档之间链接的正确性

### 文档关系
```
README.md (项目根目录)
    ├── 链接到 docs/ARCHITECTURE.md
    ├── 链接到 docs/QUICKSTART.md
    ├── 链接到 docs/PLAN.md
    └── 链接到 docs/PHASE0_SUMMARY.md

docs/
    ├── ARCHITECTURE.md (核心设计文档)
    ├── ARCHITECTURE_SUMMARY.md (快速导航)
    ├── PLAN.md (开发计划)
    ├── PHASE0_SUMMARY.md (Phase 0 总结)
    ├── QUICKSTART.md (使用指南)
    ├── TASK_COMPLETION.md (任务总结)
    └── ARCH.md (历史文档，已废弃)
```

## 🔗 相关链接

- 返回[项目主页](../README.md)
- 查看[源代码](../src/)
- 运行[测试](../test_acceptance.py)

## 📝 贡献文档

如果你想为文档做出贡献：
1. 确保你的修改与现有文档保持一致
2. 更新相关的交叉引用链接
3. 保持文档的中英文风格一致
4. 提交 PR 前检查所有链接是否有效

---

**文档版本**: v1.0  
**最后更新**: 2026-02-10  
**维护者**: Agenta Team
