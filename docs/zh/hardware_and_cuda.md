# 🚀 硬件加速与 CUDA 环境配置

SFusion 利用本地 NVIDIA GPU 算力执行 **Phi-4-mini** 推理，在脱离云端网络的环境下达到亚秒级响应。

⬅️ [文档中心](README.md) | 🏛️ [系统架构](architecture.md) | 🧠 [神经管线](neural_pipeline.md)

---

## 1. CUDA 动态库自动搜索加载器 (`src/utils/cuda_loader.py`)

针对 pip 分发的 C/C++ 扩展无法自动寻获虚拟环境中独立 CUDA 动态库的问题，SFusion 实现了进程启动自发现机制：

```python
from src.utils.cuda_loader import ensure_cuda_libs
ensure_cuda_libs()
```

---

## 2. `config/slm_settings.json` 参数说明

* `n_gpu_layers: -1`: 将 100% 网络权重层卸载至 GPU 专用显存。
* `n_ctx: 16384`: 超宽上下文窗口，从容应对超大嵌套 JSON。
* `flash_attn: true`: 启用 FlashAttention 显著压低显存占用并提升运算吞吐。
* `temperature: 0.0`: 严格贪婪解码，彻底杜绝字段判断时的随机发散。

---

## 🔗 相关技术文档
* [文档中心首页](README.md)
* [神经管线](neural_pipeline.md)
* [测试指南](testing.md)
