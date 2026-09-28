# 🧪 测试与质量保证规范

SFusion 拥有覆盖全面的自动化测试体系，共包含 **66 项 Pytest 自动化测试**，确保核心模型、底层持久化和运算逻辑的高度稳定。

⬅️ [文档中心](README.md) | 🏛️ [系统架构](architecture.md) | ⚡ [API 参考](api_reference.md)

---

## 1. 运行测试命令

```bash
./.venv/bin/pytest tests/ -v
```

生成覆盖率报告：
```bash
./.venv/bin/pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
```

---

## 2. 测试模块划分 (66 项测试)

* `test_slm_engine.py`: SLM 智能体外观调度测试。
* `test_main_controller.py`: 控制器生命周期协调与暂存文件清理测试。
* `test_schemas.py`: Pydantic 强类型蓝图校验测试。
* `test_app_state.py` 与 `test_entities.py`: Qt 信号机制与领域实体模型测试。
* `test_sensor_processor.py` 与 `test_storage_repository.py`: 多线程 ETL 提取与 SQLite WAL 事务测试。
* `test_math_engine.py` 与 `test_parquet_service.py`: Polars 矢量运算图与 Parquet 导出验证。
* `test_slm_output_parser.py`: `<think>` 标签清洗及 JSON 提取鲁棒性测试。
* `test_cuda_loader.py`: CUDA 动态库预加载机制测试。

---

## 🔗 相关技术文档
* [文档中心首页](README.md)
* [系统架构](architecture.md)
* [API 参考](api_reference.md)
