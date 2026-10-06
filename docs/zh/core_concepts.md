# 📖 核心理念与交通工程理论基础

**SFusion Mapper** 作为 **SFusion ETL** 生态中的“零日”（Day Zero）视觉化数据工程平台，核心目标在于弥合异构城市多源传感器数据与微观交通仿真（如 SUMO）之间的严苛标准差距。

⬅️ [文档中心](README.md) | 🏛️ [系统架构](architecture.md) | 🔄 [系统工作流](system_workflow.md)

---

## 1. “零日”（Day Zero）工程范式

在传统交通数据工程中，面对不同厂商的设备数据，技术人员往往需要编写大量一次性转换脚本与正则表达式。一旦设备固件升级修改了字段名称，整个数据管道随即崩溃。

**SFusion Mapper 终结了手工脆弱的 ETL 模式**：
* 构建仿真前数据治理与快速标定的“零日”可视化控制台。
* 工程师可交互式加载城市路网拓扑，并批量绑定异构传感器目录。
* 本地大模型（*Phi-4-mini*）与确定性符号规则联合推断字段语义，并在几分钟内编译出符合工业标准的高性能 **Apache Parquet** 仿真级数据集。

---

## 2. 空间拓扑与路网图论模型

任何脱离几何空间锚点的交通感知数据均不具备微观仿真价值：
* **路网节点 (`MapNode`)**：包含空间直角坐标 $(x, y)$ 的交叉路口与环岛节点。
* **路网边线 (`MapEdge`)**：带有折线几何坐标串（`shape`）的有向路段，连接起始节点与目标节点。
* **对向车道智能配对**：现实城市道路通常包含对向双向通行路段。系统能自动识别并绑定相反方向路段对（如 `edge_123` 与 `-edge_123`），实现统一命名与感知数据双向关联。
* **局部关联 vs 全局关联**：
  * **全局关联 (Global)**：环境宏观数据，均匀作用于全城路网（如气象温湿度、全城限速指令）。
  * **局部关联 (Local)**：微观观测数据，精确绑定到某一路段或信号控制节点（如雷达卡口、微波探头）。

---

## 3. 神经符号模式自动发现

面对不同厂商五花八门的命名习惯（`spd_kmh`、`velocidade`、`current_speed`）：
* **神经网络层**：本地小型大语言模型通过上下文理解字段的人类语义内涵。
* **符号系统层**：确定性校验器（`NeuroSymbolicResolver`）将输出严格约束在物理法则与强类型契约 `KinematicMap` 内，防范模型幻觉并推断物理量纲单位。

---

## 4. 矢量化运动学物理标准化

微观仿真环境强制要求国际标准单位（SI / SUMO）：
$$\text{速度 } (v) \in \text{km/h}, \quad \text{流量 } (q) \in \text{veh/h}, \quad \text{密度 } (k) \in \text{veh/km}$$

系统利用 `MathEngine` 将推断蓝图直接编译为 **Polars 抽象语法树（AST）** 表达式（`pl.Expr`），借助多核 CPU 与 SIMD 指令集实现内存级飞速向量化运算。

---

## 5. 奖章式数据流架构 (Medallion Architecture)

```mermaid
flowchart LR
    Bronze["🥉 铜级 (原始备份、MD5、zlib)"] --> Silver["🥈 银级 (orjson 结构化、SQLite WAL)"]
    Silver --> Gold["🥇 金级 (统一 Parquet 列式数据集)"]
```

---

## 🔗 相关技术文档
* [文档中心首页](README.md)
* [数据模型规范](data_models.md)
* [矢量物理引擎](math_engine.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>卓越科技 • A State Of Art Company</i><br/>
  <i>智慧交通出行工程 • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. 基于 AGPLv3 协议授权.</small>
</div>
