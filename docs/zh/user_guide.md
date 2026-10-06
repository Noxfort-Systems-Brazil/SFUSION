# 🖥️ 用户操作手册与图形界面指南

本手册提供使用 **SFusion Mapper** 图形交互界面的完整标准操作规程。

⬅️ [文档中心](README.md) | 🏛️ [系统架构](architecture.md) | 🔄 [系统工作流](system_workflow.md)

---

## 1. 标准操作流程

1. **载入路网**：点击工具栏 **打开地图**（快捷键 `Ctrl+M`），选择 SUMO 网络文件。
2. **添加传感器数据源**：点击 **添加源**，选取包含原始监控数据的文件夹。
3. **执行实体关联**：选中源项点击 **关联**，在地图上点击目标道路（系统自动连带选中对向车道），或右键设为全局源。
4. **校对属性**：在右侧 **编辑面板** 查看 AI 推导结果，按需手动重选下拉列，并填写实际路名（如“中关村大街”）。
5. **生成数据集**：所有源关联就绪后，点击 **生成数据集**，指定保存路径完成 Parquet 导出。
6. **工程持久化**：使用 **保存工程** 将本次映射成果存为 `.sfm.json` 工程文件。

---

## 🔗 相关技术文档
* [文档中心首页](README.md)
* [系统工作流](system_workflow.md)
* [数据模型规范](data_models.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>卓越科技 • A State Of Art Company</i><br/>
  <i>智慧交通出行工程 • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. 基于 AGPLv3 协议授权.</small>
</div>
