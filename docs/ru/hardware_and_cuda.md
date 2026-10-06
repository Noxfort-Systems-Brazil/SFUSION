# 🚀 Аппаратное ускорение и настройка CUDA

SFusion использует графические процессоры для локального инференса модели **Phi-4-mini** с задержками менее одной секунды.

⬅️ [Главный Хаб](README.md) | 🏛️ [Архитектура](architecture.md) | 🧠 [Нейросетевой конвейер](neural_pipeline.md)

---

## 1. Динамический загрузчик библиотек CUDA (`src/utils/cuda_loader.py`)

Находит библиотеки CUDA, поставляемые с pip-пакетами (`nvidia-cuda-runtime-cu12`, `nvidia-cublas-cu12`), и загружает их в память до инициализации `llama.cpp`.

```python
from src.utils.cuda_loader import ensure_cuda_libs
ensure_cuda_libs()
```

---

## 2. Конфигурация в `config/slm_settings.json`

* `n_gpu_layers: -1`: перенос 100% слоев модели в память видеокарты.
* `n_ctx: 16384`: расширенное окно контекста под крупные схемы JSON.
* `flash_attn: true`: оптимизация памяти и ускорение вычислений.
* `temperature: 0.0`: полностью детерминированный ответ модели.

---

## 🔗 Полезные ссылки
* [Главный Хаб](README.md)
* [Нейросетевой конвейер](neural_pipeline.md)
* [Тестирование](testing.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Инженерия интеллектуальной мобильности • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Лицензия AGPLv3.</small>
</div>
