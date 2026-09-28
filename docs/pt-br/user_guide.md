# 🖥️ Manual de Operações e Guia do Usuário

Este guia fornece o procedimento operacional passo a passo para utilização do **SFusion Mapper** através de sua interface gráfica (GUI).

⬅️ [Central de Documentação](README.md) | 🏛️ [Arquitetura](architecture.md) | 🔄 [Fluxo de Trabalho](system_workflow.md)

---

## 1. Zonas Funcionais da Interface

```text
+-------------------------------------------------------------------------+
| Barra: [Abrir Projeto] [Salvar Projeto] | [Abrir Mapa] [Nova Fonte] | [Gerar Dataset] | [Config]
+-------------------+--------------------------------+--------------------+
|                   |                                |                    |
| Painel de Fontes  |        Visualizador de         |   Painel Editor    |
| (Barra Esquerda)  |      Malha Viária (Centro)     |  (Barra Direita)   |
|                   |                                |                    |
| - Lista de Fontes | - Rede SUMO Interativa         | - Esquema Deduzido |
| - Local / Global  | - Cruzamentos (Nós)            | - Unidades Físicas |
| - Associação      | - Vias Direcionais (Arestas)   | - Ajuste Manual    |
|                   | - Pareamento de Sentidos       | - Nomes Reais      |
|                   |                                |                    |
+-------------------+--------------------------------+--------------------+
| Barra de Status: Pronto / Progresso / Telemetria do Sistema             |
+-------------------------------------------------------------------------+
```

---

## 2. Passo a Passo Operacional

### Passo 1: Importar a Malha Viária
1. Clique em **Abrir Mapa** na barra de ferramentas (ou tecle `Ctrl+M`).
2. Selecione o arquivo de rede do SUMO (`.net.xml` ou `.net.xml.gz`).
3. Navegue na tela gráfica: use a roda do mouse para zoom e arraste sobre o fundo para pan.

### Passo 2: Adicionar Pastas de Sensores
1. Clique em **Adicionar Fonte** na barra de ferramentas.
2. Selecione o diretório contendo os arquivos de telemetria.
3. A pasta aparecerá no **Painel de Fontes** à esquerda com as extensões identificadas.

### Passo 3: Configurar Associações
* **Associação Local**: Selecione a fonte, clique em **Associar** e clique na via desejada no mapa. O SFusion detecta e seleciona automaticamente os dois sentidos da avenida.
* **Associação Global**: Clique com o botão direito sobre a fonte na lista e escolha **Definir como Global**.

### Passo 4: Validar e Ajustar Esquemas de IA
1. Inspecione os campos deduzidos pelo SLM no **Painel Editor** à direita.
2. Caso necessário, utilize as caixas suspensas para redefinir as colunas de velocidade, vazão ou intensidade.
3. Digite o nome real da avenida (ex: *"Avenida Paulista"*) para enriquecer os dados finais.
4. Clique em **Salvar** no painel editor.

### Passo 5: Gerar o Dataset Final
1. Com todas as fontes locais associadas, clique em **Gerar Dataset**.
2. Defina a pasta e o nome do arquivo de saída (ex: `dataset_simulacao.parquet`).
3. Acompanhe a barra de progresso durante o processamento ETL e a compilação Parquet.

### Passo 6: Gerenciamento de Sessão
* Clique em **Salvar Projeto** para salvar a sessão atual em um arquivo `.sfm.json`.
* Clique em **Abrir Projeto** para retomar trabalhos anteriores instantaneamente.

---

## 🔗 Documentos Relacionados
* [Central de Documentação](README.md)
* [Fluxo de Trabalho](system_workflow.md)
* [Modelos de Dados](data_models.md)
