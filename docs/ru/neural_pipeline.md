# 🧠 Нейросетевой конвейер и движок SLM

**Нейросетевой конвейер SFusion** реализует локальную **нейро-символическую** систему сопоставления схем данных дорожных датчиков на базе модели **Phi-4-mini-reasoning**, среды `llama.cpp` и аппаратного ускорения CUDA.

⬅️ [Главный Хаб](README.md) | 🏛️ [Архитектура](architecture.md) | 🚀 [Аппаратное ускорение](hardware_and_cuda.md)

---

## 1. Нейро-символическая архитектура

1. **Нейросетевой уровень**: локальная SLM интерпретирует произвольные названия колонок (`spd_kmh`, `velocidade`, `current_speed`).
2. **Символический уровень**: модуль `NeuroSymbolicResolver` проверяет предложенные соответствия по правилам кинематики и формирует спецификацию `KinematicMap`.

---

## 2. Основные компоненты

* **`SLMEngine`**: высокоуровневый координатор инференса.
* **`LLMInferenceProvider`**: взаимодействие с `llama.cpp`, перенос слоев в VRAM (`n_gpu_layers = -1`) и детерминированная генерация (`temperature = 0.0`).
* **`SchemaPromptBuilder`**: обход вложенных полей JSON/CSV и генерация путей.
* **`SLMOutputParser`**: удаление тегов рассуждений `<think>...</think>` и очистка JSON.
* **`NeuroSymbolicResolver`**: верификация по эвристическим словарям (`SPEED_CANDIDATES`, `FLOW_CANDIDATES`).

---

## 🔗 Полезные ссылки
* [Главный Хаб](README.md)
* [Аппаратное ускорение](hardware_and_cuda.md)
* [Модели данных](data_models.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Инженерия интеллектуальной мобильности • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Лицензия AGPLv3.</small>
</div>
