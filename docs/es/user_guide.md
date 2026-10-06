# 🖥️ Guía de Usuario y Manual Operativo

Procedimiento paso a paso para utilizar la interfaz gráfica de **SFusion Mapper**.

⬅️ [Centro de Documentación](README.md) | 🏛️ [Arquitetura](architecture.md) | 🔄 [Flujo de Trabajo](system_workflow.md)

---

## 1. Operación Paso a Paso

1. **Abrir Mapa**: Cargar la red SUMO con el botón **Abrir Mapa** (`Ctrl+M`).
2. **Agregar Fuente**: Seleccionar una carpeta con datos de sensores.
3. **Asociar**: Vincular la fuente haciendo clic en una calle de la red (ambos sentidos se seleccionan automáticamente) o configurar como Global.
4. **Validar Esquema**: Revisar las columnas detectadas por la IA en el panel derecho y asignar nombres reales de vías.
5. **Generar Dataset**: Hacer clic en **Generar Dataset** para crear el archivo `.parquet`.
6. **Guardar Proyecto**: Guardar la sesión en `.sfm.json` para reanudar más tarde.

---

## 🔗 Enlaces Relacionados
* [Centro de Documentación](README.md)
* [Flujo de Trabajo](system_workflow.md)
* [Modelos de Datos](data_models.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Ingeniería de Movilidad Inteligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado bajo AGPLv3.</small>
</div>
