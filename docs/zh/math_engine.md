# 📐 矢量物理引擎与 AST 表达式编译器

**MathEngine** (`src/services/math_engine.py`) 是 SFusion 的核心计算模块，完全在 CPU 与内存中执行，依托 **Polars** 矢量化计算图突破 Python 全局解释器锁（GIL）瓶颈。

⬅️ [文档中心](README.md) | 🏛️ [系统架构](architecture.md) | ⚡ [ETL 流水线](etl_pipeline.md)

---

## 1. 国际标准单位 (SI) 规范化

微观交通仿真需要统一量纲：
* **速度 ($v$)**: $\text{km/h}$
* **流量 ($q$)**: $\text{veh/h}$
* **密度 ($k$)**: $\text{veh/km}$

---

## 2. 逐行 AST 计算图生成 (`compile_ast`)

将推断生成的 `KinematicMap` 编译为 Polars 原生表达式：
* **速度**:
  * `'m/s'`: $\text{速度} \times 3.6$
  * `'mph'`: $\text{速度} \times 1.60934$
  * `'knots'`: $\text{速度} \times 1.852$
  * 缺失时通过物理公式推导：$\text{速度} = \frac{\text{距离\_km}}{\text{时间\_小时}}$
* **距离**: 将 `'m'`、`'miles'` 转换为千米。
* **时间**: 将 `'s'`、`'ms'`、`'min'` 统一转换为小时。

---

## 3. 多事件宏观车流聚合 (`compile_aggregations`)

### 1. 空间平均速度（调和平均数）
交通工程理论表明，算术平均会高估车流平均速度。系统采用空间调和平均：
$$v_s = \frac{N}{\sum_{i=1}^{N} \frac{1}{v_i}}$$

### 2. 宏观交通流量 ($q$)
将时段内的检测车辆数换算为每小时通行能力：
$$q = \frac{N}{\Delta t_{\text{小时}}} \quad [\text{veh/h}]$$

### 3. 车流密度与物理占有率 ($k$)
根据车流连续流体力学基本原理方程推导：
$$k = \frac{q}{v_s} \quad [\text{veh/km}]$$

---

## 4. 容错防护与安全运算
* **安全除法 (`safe_div`)**: 遇到零分母自动填入 `None`，杜绝除零崩溃。
* **宽容转换**: 所有类型转换均采用 `strict=False`，异常脏数据安全转化为 `None`/`NaN`。
* **无穷大值过滤**: 对计算产生的 $\pm\infty$ 预先替换为 `np.nan` 后再执行整型取整。

---

## 🔗 相关技术文档
* [文档中心首页](README.md)
* [神经管线](neural_pipeline.md)
* [数据模型规范](data_models.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>卓越科技 • A State Of Art Company</i><br/>
  <i>智慧交通出行工程 • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. 基于 AGPLv3 协议授权.</small>
</div>
