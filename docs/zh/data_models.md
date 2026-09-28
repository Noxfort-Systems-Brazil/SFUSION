# 🗃️ 数据模型定义与模式规范

本文档详尽收录 **SFusion Mapper** 的数据字典规范，涵盖内存领域实体模型、响应式应用状态机、Pydantic `KinematicMap` 蓝图、SQLite 暂存表以及最终交付的 **Apache Parquet** 列式数据格式。

⬅️ [文档中心](README.md) | 🏛️ [系统架构](architecture.md) | ⚡ [ETL 流水线](etl_pipeline.md)

---

## 1. 领域模型实体 (`src/domain/entities.py`)

### `AssociationType` (枚举)
* `UNASSOCIATED`: 数据源已载入，但尚未分配关联目标。
* `GLOBAL`: 全局广播属性，宏观应用于全路网。
* `LOCAL`: 局部微观关联，精确绑定到特定路段（`MapEdge`）或交叉口（`MapNode`）。

### `DataSource` (数据类)
```python
@dataclass
class DataSource:
    path: str                                # 文件夹绝对物理路径
    name: str                                # 界面展示友好名称
    file_types: list[str] = field(...)       # 识别到的数据格式 (如 ["CSV", "JSON"])
    id: str = field(...)                     # 唯一哈希标识 (例如 "src_a1b2c3d4")
    parser_id: str | None = None             # 匹配的抽取器标识
    association_type: AssociationType = ...  # UNASSOCIATED, GLOBAL 或 LOCAL
    associated_element_id: str | None = None # 绑定的 SUMO 路网图元 ID
```

---

## 2. 响应式系统状态机 (`src/domain/app_state.py`)

* 继承自 `PySide6.QtCore.QObject`，提供强类型事件通知：`map_data_loaded`、`data_sources_changed`、`data_association_changed`、`savable_state_changed`。
* **可保存性不变式 (`_is_savable`)**：只有当路网已加载且所有标记为 `LOCAL` 的传感器源均完成实体绑定时，数据集生成动作才被允许激活。

---

## 3. 强类型运动学蓝图 (`src/core/schemas.py`)

```python
class KinematicMap(BaseModel):
    speed_col: Optional[str] = None          # 速度字段
    flow_col: Optional[str] = None           # 流量字段
    intensity_col: Optional[str] = None      # 拥堵指数/密度字段
    distance_col: Optional[str] = None       # 距离差字段 (用于 v = d / t)
    time_col: Optional[str] = None           # 时间差字段 (用于 v = d / t)
    occupancy_col: Optional[str] = None      # 线圈占有率/驻留时间
    speed_unit: Optional[str] = "km/h"       # "km/h", "m/s" 或 "mph"
    confidence_score: Optional[float] = None # 模型置信度得分 [0.0 - 1.0]
```

---

## 4. 最终统一交付 Parquet 模式 (`.parquet`)

| 字段名称 | Arrow 数据类型 | 允许空值 | 业务含义描述 |
| :--- | :--- | :---: | :--- |
| `event_timestamp` | `timestamp[ns, UTC]` | 否 | 统一转换为 UTC 标准时区的毫秒时间戳。 |
| `sensor_id` | `string` | 否 | 传感器探头或采集源设备的唯一识别码。 |
| `sumo_id` | `string` | 是 | 映射绑定的 SUMO 路网路段/节点编号（全局源为 null）。 |
| `location_text` | `string` | 是 | 工程师在界面上标注的实际主干道路名文本。 |
| `lat` | `float64` | 是 | 提取的 WGS84 纬度坐标。 |
| `lon` | `float64` | 是 | 提取的 WGS84 经度坐标。 |
| `origin_type` | `string` | 否 | 作用域范围：`"LOCAL"` 或 `"GLOBAL"`。 |
| `speed_val` | `Int64` | 是 | **统一转换为 km/h 的车流速度值**（四舍五入整型）。 |
| `flow_val` | `float64` | 是 | **标定为 veh/h 的标准通行流量**（保留 2 位小数）。 |
| `intensity_val` | `float64` | 是 | **拥堵/密度综合指数**（保留 2 位小数）。 |
| `source_table` | `string` | 否 | 对应 SQLite 暂存表名称（`section_<name>`）。 |

---

## 🔗 相关技术文档
* [文档中心首页](README.md)
* [矢量物理引擎](math_engine.md)
* [ETL 流水线详解](etl_pipeline.md)
