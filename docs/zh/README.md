<div align="center">

<img src="../assets/sfusion-logo.png" alt="SFusion Mapper Logo" width="120" />

# SFusion Mapper — 官方技术文档库
### 系统架构规范、神经模式自动发现与矢量物理引擎
*Noxfort Systems — 卓越科技*

[![Status](https://img.shields.io/badge/Status-活跃-brightgreen?style=flat&logo=github)](https://github.com/Noxfort-Systems-Brazil/SFUSION)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![PySide6](https://img.shields.io/badge/Framework-PySide6%20(Qt6)-41CD52?style=flat&logo=qt&logoColor=white)](https://www.qt.io/)
[![Engine: Polars](https://img.shields.io/badge/Engine-Polars-CD792C?style=flat)](https://pola.rs/)
[![Format: Parquet](https://img.shields.io/badge/Output-Apache%20Parquet-teal?style=flat)](https://parquet.apache.org/)

---

🌐 **语言导航：** **[🇺🇸 English](../en/README.md)** • **[🇧🇷 Português (Brasil)](../pt-br/README.md)** • **[🇪🇸 Español](../es/README.md)** • **[🇫🇷 Français](../fr/README.md)** • **[🇷🇺 Русский](../ru/README.md)** • **[🇨🇳 简体中文](README.md)** • **[📖 文档总中心](../README.md)**

---

</div>

## 欢迎查阅官方技术文档

本目录汇集了面向智能交通系统（ITS）工程师和数据科学家的 **SFusion Mapper** (SYNAPSE Fusion) 完整**简体中文**技术文档体系。SFusion Mapper 是由 Noxfort Systems 研发的高性能“零日”（Day Zero）视觉化数据工程与运动学标准化工具，旨在打通城市异构多源感知数据（Waze、TomTom、地磁地感线圈、雷达测速探头）与严格微观交通仿真系统（如 SUMO）之间的技术鸿沟。

## 专业技术指南索引

| 指南名称 | 核心范畴与目标 | 重点技术主题 |
| :--- | :--- | :--- |
| 🏛️ **[系统架构与工程规范](architecture.md)** | 系统架构与分层设计 | Clean MVC 模式、Builder 模式依赖注入、PySide6 视图解耦、后台异步服务以及响应式 AppState 单一事实真理。 |
| 📖 **[核心概念与理论基础](core_concepts.md)** | ITS 理论与范式 | “零日”配置范式、SUMO 拓扑有向图（MapNode/MapEdge）、神经符号推理以及奖章式数据架构（Bronze/Silver/Gold）。 |
| 🗃️ **[数据模型与模式规范](data_models.md)** | 数据字典与蓝图 | 不可变领域实体、Pydantic v2 `KinematicMap` 数学契约、临时 SQLite WAL 暂存表以及最终统一 Apache Parquet 列式规范。 |
| ⚡ **[高性能 ETL 流水线](etl_pipeline.md)** | 摄取与持久化引擎 | `QThreadPool` 多线程编排、`SensorBatchProcessor`、MD5 完整性哈希、zlib 压缩以及 SQLite WAL 模式 PRAGMA 调优。 |
| 📐 **[矢量物理引擎](math_engine.md)** | Polars AST 编译 | 无 Python GIL 瓶颈的 SIMD 矢量计算、SI 标准国际单位转换（$km/h$、$m/s$、$mph$）、调和空间平均速度与流体力学基本密度 $k = q / v$。 |
| 🧠 **[神经管线与 SLM 引擎](neural_pipeline.md)** | 本地大模型推理 | 本地量化小语言模型 *Phi-4-mini* GGUF、`llama.cpp` 高速运行时、点分层级 Prompt 抽取、`<think>` 标签清洗与 `NeuroSymbolicResolver`。 |
| 🚀 **[硬件加速与 CUDA 配置](hardware_and_cuda.md)** | GPU 显存与运行时 | 动态 CUDA 共享库加载钩子（`ensure_cuda_libs`）、`slm_settings.json`、TensorCore 调用、CPU 多线程回退机制与硬件遥测。 |
| 🔄 **[系统工作流与生命周期](system_workflow.md)** | 5 阶段端到端流转 | 确定性执行流水线：路网拓扑导入、数据源扫描登记、空间关联与自动发现、ETL 暂存写入及 Parquet 列式导出与清理。 |
| 🖥️ **[用户手册与操作指南](user_guide.md)** | 图形界面交互指南 | 画布平移缩放、双向车道对自动配对、局部/全局属性绑定、手动覆盖重设与 `.sfm.json` 项目工程管理。 |
| 🧪 **[测试与质量保证规范](testing.md)** | QA 测试与验证标准 | 160 项 Pytest 自动化测试、覆盖率超 91%（前端 ~97%、后端 ~89%）、无头 Qt 离屏执行、确定性 AI Mock 固件及 10 大测试套件。 |
| ⚡ **[内部核心 API 参考](api_reference.md)** | 类接口与 Qt 信号 | 领域状态机核心类、底层数据仓库 DAO、Qt 信号与槽机制、业务处理服务及控制器调用契约。 |

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>卓越科技 • A State Of Art Company</i><br/>
  <i>智慧交通出行工程 • SFusion Mapper v0.1.0</i>
</div>
