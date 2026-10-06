# 🧪 测试与质量保证规范

SFusion 拥有覆盖全面的自动化测试体系，共包含 **160 项 Pytest 自动化测试**，整体代码覆盖率超过 **91%**（前端界面 **~97%**，后端服务 **~89%**），确保领域实体模型、UI 交互、控制器流转、多线程 ETL 和本地 SLM 推理的高度稳定性。

⬅️ [文档中心](README.md) | 🏛️ [系统架构](architecture.md) | ⚡ [API 参考](api_reference.md)

---

## 1. 运行测试命令

### 1.1 无头离屏全量测试执行
使用项目本地虚拟环境，在无 X11/Wayland 窗口系统的离屏模式下运行：
```bash
QT_QPA_PLATFORM=offscreen ./.venv/bin/pytest tests/ -v
```

### 1.2 生成完整代码覆盖率报告
同时统计后端 (`src/`) 与前端视图 (`ui/`) 的分支与语句覆盖率：
```bash
QT_QPA_PLATFORM=offscreen ./.venv/bin/pytest tests/ -v --cov=src --cov=ui --cov-report=term-missing --cov-report=html
```
交互式 HTML 覆盖率报告将输出至 `htmlcov/index.html`。

---

## 2. 测试模块划分 (160 项测试 / 10 大模块)

| 测试模块 | 测试文件 | 目标测试组件 | 核心验证行为 |
| :--- | :--- | :--- | :--- |
| **前端视图 (UI)** | `test_editor_panel.py`<br/>`test_sources_panel.py`<br/>`test_map_view.py`<br/>`test_settings_dialog.py`<br/>`test_main_window.py` | Qt 界面组件 (`ui/`) | 无头离屏渲染、组件布局、信号与槽绑定、列表多选、右键上下文菜单、鼠标平移缩放及模态配置 (~97% 覆盖率)。 |
| **控制器层** | `test_main_controller.py`<br/>`test_info_controller.py`<br/>`test_map_controller.py`<br/>`test_sources_controller.py`<br/>`test_settings_controller.py` | 流程控制器 (`src/controllers/`) | 五阶段流水线协调 (持久化 -> ETL -> Parquet -> 清理)、地图画布高亮、双向路段配对与 AppState 状态同步。 |
| **核心与依赖注入** | `test_app_builder.py`<br/>`test_map_renderer.py`<br/>`test_schemas.py` | App Builder 与渲染器 | 完整依赖注入装配、QGraphicsScene 矢量绘制 (Ribbon Stroker、交叉路口、方向箭头) 与 Pydantic 蓝图约束校验。 |
| **SLM 智能体与推理** | `test_slm_engine.py`<br/>`test_neuro_symbolic_resolver.py`<br/>`test_prompt_builder.py`<br/>`test_slm_output_parser.py` | SLM 神经管线 (`src/slm/`) | 确定性单位推导、启发式候选模式判定、点分层级键名提取、`<think>` 标签清洗与动态 Prompt 生成。 |
| **领域实体模型** | `test_app_state.py`<br/>`test_entities.py` | `AppState`<br/>`DataSource`, `MapEdge`, `MapNode` | 响应式 Qt 信号分发 (`map_data_loaded`, `data_sources_changed`)、反向边自动绑定与 `_is_savable()` 不变量验证。 |
| **ETL 提取子系统** | `test_sensor_processor.py`<br/>`test_storage_repository.py`<br/>`test_etl_service.py`<br/>`test_neural_transformer.py` | ETL 与数据转换服务 | 多线程并行提取、MD5 去重哈希、zlib 快速压缩、SQLite WAL PRAGMA 调优及 Polars 物理编译。 |
| **服务与计算层** | `test_math_engine.py`<br/>`test_parquet_service.py`<br/>`test_data_importer.py`<br/>`test_map_importer.py`<br/>`test_persistence.py`<br/>`test_project_service.py`<br/>`test_extractors.py` | 后台 Worker 与引擎 | Polars 运算图编译、SI 国际单位换算 ($km/h$, $m/s$, $mph$)、调和空间平均速度、Parquet 列式导出、SUMO XML/GZ 解析及 `.sfm.json` 序列化。 |
| **底层工具链** | `test_cuda_loader.py`<br/>`test_config.py`<br/>`test_i18n.py`<br/>`test_slm_telemetry.py` | 基础设施与硬件 | 配置持久化读写、双层 i18n 嵌套国际化、CPU/显存动态遥测、CUDA 共享对象动态探测及安全降级。 |

---

## 3. Mock 与隔离机制设计

1. **Qt Headless 离屏架构**：所有 PySide6 视图在测试中均运行在 `QT_QPA_PLATFORM=offscreen` 模式下。`tests/conftest.py` 统一定义了 `qapp` 全局共享固件，并注入国际化与配置 Mock，确保 CI/CD 纯命令行环境中无阻塞流畅运行。
2. **确定性 SLM 固件测试**：`SLMEngine` 与 `NeuroSymbolicResolver` 均采用确定性 JSON 样本及 `unittest.mock`，在无 GPU 和无需 3.5GB 模型文件的环境下即可毫秒级完成逻辑验证。
3. **SQLite WAL 暂存隔离**：ETL 与数据仓库测试使用临时目录中的 SQLite 数据库并开启 WAL 模式，确保多线程并发读写的安全性与无污染清理。
4. **临时文件沙盒化**：所有测试生成的工程文件、暂存库与 Parquet 文件均由 pytest 的 `tmp_path` 临时目录管理，测试结束后自动卸载回收。
5. **进程退出守卫**：生产环境中 `MainWindow.closeEvent` 会调用 `os._exit(0)`，测试中通过 `monkeypatch` 拦截该方法，防止其直接杀掉 pytest 测试进程。

---

## 🔗 相关技术文档
* [文档中心首页](README.md)
* [系统架构](architecture.md)
* [API 参考](api_reference.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>卓越科技 • A State Of Art Company</i><br/>
  <i>智慧交通出行工程 • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. 基于 AGPLv3 协议授权.</small>
</div>
