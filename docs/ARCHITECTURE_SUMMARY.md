# ARCHITECTURE.md 快速导航

## 📄 文档概述
**ARCHITECTURE.md** 是 Agenta 项目的最终架构设计文档，详细描述了一个类似 Claude Code / OpenCode 体验的 CLI + Streamlit 智能体系统。

## 🎯 核心内容

### 1. 系统概述
- **位置**: 第 25-52 行
- **内容**: 愿景、核心特性、与 Claude Code/OpenCode 的对比

### 2. 设计原则 
- **位置**: 第 53-75 行
- **内容**: CLI First, No Surprises, Local by Default, Extensible, Fail Safe

### 3. 整体架构（重要）
- **位置**: 第 77-151 行
- **内容**: 四层架构图
  - Interface Layer (CLI + Streamlit Web)
  - Agent Core Layer (Orchestrator, Skills, Memory)
  - AI/ML Layer (LLM Client, RAG, Prompts)
  - Execution Layer (Sandbox, Playwright, File Ops)

### 4. 核心组件（最详细）
- **位置**: 第 153-579 行
- **内容**: 每一层的详细实现
  - CLI Interface 实现 (typer + rich)
  - Streamlit Web UI 实现
  - Orchestrator 调度器
  - Skill Registry 动态加载
  - LLM Client Manager
  - Sandbox Executor (Docker)
  - File Operator 安全写入

### 5. 数据流
- **位置**: 第 580-678 行
- **内容**: 三个关键场景
  - CLI 执行 /test 命令
  - Web UI 执行相同命令
  - 沙箱代码执行流程

### 6. 技术栈
- **位置**: 第 679-707 行
- **内容**: 所有依赖库及版本选型理由

### 7. 安全模型
- **位置**: 第 708-783 行
- **内容**: 四层安全防护
  - 权限确认
  - Docker 沙箱
  - 资源限制
  - 本地存储

### 8. 扩展机制
- **位置**: 第 784-874 行
- **内容**: Skill 插件系统设计
  - BaseSkill 基类
  - 自定义 Skill 示例
  - 动态加载机制

### 9. 部署架构
- **位置**: 第 875-945 行
- **内容**: 
  - 本地开发模式
  - Web 模式启动
  - Docker 部署
  - 云端部署（Streamlit Cloud / VPS）

### 10. 性能考量
- **位置**: 第 946-1013 行
- **内容**: 
  - 响应时间目标
  - 资源使用限制
  - 并发处理
  - 缓存策略

## 📊 关键数据

- **总行数**: 1,177 行
- **主要章节**: 18 个
- **子章节**: 42 个
- **代码示例**: 27 个代码块
- **架构图**: 4 个

## 🎯 适用场景

### 查看架构图
👉 跳转到第 79-151 行

### 了解技术选型
👉 跳转到第 679-707 行

### 学习 Skill 开发
👉 跳转到第 784-874 行

### 部署系统
👉 跳转到第 875-945 行

### 了解安全机制
👉 跳转到第 708-783 行

## 🔗 相关文档

- **[README.md](../README.md)** - 项目简介和快速开始
- **[PLAN.md](PLAN.md)** - 开发计划（4 个阶段）
- **[PHASE0_SUMMARY.md](PHASE0_SUMMARY.md)** - Phase 0 实现总结
- **[QUICKSTART.md](QUICKSTART.md)** - 安装和配置指南
- **[ARCH.md](ARCH.md)** - 早期架构讨论（已被 ARCHITECTURE.md 取代）

## 💡 快速理解架构

如果时间有限，重点阅读以下部分：

1. **系统概述** (第 25-52 行) - 了解是什么
2. **四层架构图** (第 79-151 行) - 理解整体结构
3. **核心组件 > Orchestrator** (第 228-266 行) - 理解核心调度逻辑
4. **数据流 > 场景 1** (第 583-619 行) - 理解典型执行流程
5. **总结** (第 1131-1177 行) - 把握核心价值

## ✅ 验收清单

文档已完成以下内容：
- [x] 系统概述和愿景
- [x] 设计原则
- [x] 四层架构设计
- [x] 所有核心组件详细设计
- [x] 数据流图
- [x] 完整技术栈
- [x] 安全模型
- [x] Skill 扩展机制
- [x] 部署方案
- [x] 性能优化建议
- [x] 与竞品对比
- [x] 演进路径
- [x] 参考资源

---

**创建日期**: 2026-02-09  
**文档版本**: v1.0  
**状态**: ✅ Final & Complete
