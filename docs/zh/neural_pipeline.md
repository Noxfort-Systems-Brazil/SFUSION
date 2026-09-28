# 🧠 神经管线与 SLM 推理引擎

**SFusion 神经管线** 依托本地部署的小型语言模型（SLM）—— **Phi-4-mini-reasoning** 与 `llama.cpp` CUDA 加速运行时，构建了一套用于城市多源交通数据模式自动解析的**神经符号系统**。

⬅️ [文档中心](README.md) | 🏛️ [系统架构](architecture.md) | 🚀 [硬件加速](hardware_and_cuda.md)

---

## 1. 神经符号架构设计

1. **神经网络层**：本地模型解析样本内容，理解人类对列名的自由命名意图（如理解 `spd_kmh`、`velocidade`、`current_speed` 均为车流速度）。
2. **符号规则层**：`NeuroSymbolicResolver` 运用物理启发式词表对候选字段进行严格过滤，自动识别物理单位，产出合规的 `KinematicMap`。

---

## 2. 核心组件分工

* **`SLMEngine`**: 顶层 AI 外观调度类。
* **`LLMInferenceProvider`**: 管理 `llama.cpp` 底层，负责显存层卸载 (`n_gpu_layers = -1`) 与贪婪解码 (`temperature = 0.0`)。
* **`SchemaPromptBuilder`**: 深度递归 JSON 与 CSV 结构，构建点分路径层次结构。
* **`SLMOutputParser`**: 剔除推理大模型内部思考过程标签 `<think>...</think>`，净化出纯净 JSON。
* **`NeuroSymbolicResolver`**: 启发式物理词表交叉匹配与量纲推断。

---

## 🔗 相关技术文档
* [文档中心首页](README.md)
* [硬件加速指南](hardware_and_cuda.md)
* [数据模型规范](data_models.md)
