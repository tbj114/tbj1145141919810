# AxaltyX 补充设计文档 -- 图标体系、文件格式与导入导出

> 版权所有: TBJ114
> 本文档为 AxaltyX_Development_Plan.md 的补充，涵盖图标体系、.tbj 文件格式规范、多格式导入导出体系。

---

## 第九部分: 专属图标体系设计

### 9.1 图标设计原则

| 原则 | 说明 |
|------|------|
| 风格统一 | 所有图标遵循 Arco Design 线性图标风格，2px 描边，圆头端点 |
| 色彩一致 | 主色 `#165DFF`，辅助色使用 Arco 色板 |
| 尺寸规范 | 提供 16x16、24x24、32x32、48x48、64x64、128x128、256x256 多尺寸 |
| 格式标准 | 矢量图标使用 SVG，位图图标使用 ICO/PNG |
| 无文字依赖 | 图标不依赖文字传达含义（文件类型图标底部标签除外） |
| 无 Emoji | 所有图标均为纯几何图形，不使用任何 Emoji |

### 9.2 图标分类总览

```
axaltyx/resources/icons/
|
+-- brand/                           # 品牌图标
|   +-- app_icon.ico                 # 应用主图标 (多尺寸 ICO)
|   +-- app_icon_256.png             # 256x256 PNG
|   +-- app_icon_128.png             # 128x128 PNG
|   +-- app_icon_64.png              # 64x64 PNG
|   +-- app_icon_48.png              # 48x48 PNG
|   +-- app_icon_32.png              # 32x32 PNG
|   +-- app_icon_16.png              # 16x16 PNG
|   +-- logo.svg                     # SVG 矢量 Logo
|   +-- logo_dark.svg                # 深色模式 Logo
|   +-- logo_white.svg               # 白色版本 Logo（用于深色背景）
|
+-- file_types/                      # 文件类型图标
|   +-- tbj_file.ico                 # .tbj 数据文件图标
|   +-- tbj_file.svg                 # .tbj 数据文件 SVG
|   +-- axo_file.ico                 # .axo 输出文件图标
|   +-- axo_file.svg                 # .axo 输出文件 SVG
|   +-- axs_file.ico                 # .axs 语法文件图标
|   +-- axs_file.svg                 # .axs 语法文件 SVG
|   +-- tbj_file_large.png           # .tbj 大图标 (256x256)
|   +-- axo_file_large.png           # .axo 大图标 (256x256)
|   +-- axs_file_large.png           # .axs 大图标 (256x256)
|
+-- toolbar/                         # 工具栏图标 (24x24 SVG)
|   +-- new_file.svg                 # 新建文件
|   +-- open_file.svg                # 打开文件
|   +-- save_file.svg                # 保存文件
|   +-- save_as.svg                  # 另存为
|   +-- undo.svg                     # 撤销
|   +-- redo.svg                     # 重做
|   +-- cut.svg                      # 剪切
|   +-- copy.svg                     # 复制
|   +-- paste.svg                    # 粘贴
|   +-- clear.svg                    # 清除
|   +-- find.svg                     # 查找
|   +-- replace.svg                  # 替换
|   +-- run_analysis.svg             # 运行分析
|   +-- stop_analysis.svg            # 停止分析
|   +-- print.svg                    # 打印
|   +-- export.svg                   # 导出
|   +-- zoom_in.svg                  # 放大
|   +-- zoom_out.svg                 # 缩小
|   +-- zoom_fit.svg                 # 适应窗口
|
+-- analysis/                        # 分析菜单图标 (16x16 SVG)
|   +-- statistical_summary.svg      # 统计摘要 (sigma 符号)
|   +-- compare_means.svg            # 比较均值 (均值符号 x-bar)
|   +-- general_linear_model.svg     # 一般线性模型 (GLM 网格)
|   +-- nonparametric.svg            # 非参数检验 (分布曲线)
|   +-- correlation.svg              # 相关分析 (散点趋势)
|   +-- regression.svg               # 回归分析 (趋势线)
|   +-- classification.svg           # 分类 (聚类圆圈)
|   +-- scale.svg                    # 尺度分析 (刻度尺)
|   +-- survival.svg                 # 生存分析 (生存曲线)
|   +-- advanced.svg                 # 高级分析 (齿轮+图表)
|   +-- causal_inference.svg         # 因果推断 (因果箭头)
|   +-- machine_learning.svg         # 机器学习 (神经网络节点)
|   +-- text_analysis.svg            # 文本分析 (文档+字母)
|   +-- spatial.svg                  # 空间分析 (地图标记)
|   +-- multilevel.svg               # 多层模型 (层级方块)
|   +-- bayesian_advanced.svg        # 高级贝叶斯 (贝叶斯网络)
|
+-- variable_types/                  # 变量类型图标 (16x16 SVG)
|   +-- type_numeric.svg             # 数值型 (# 符号)
|   +-- type_string.svg              # 字符串型 (Aa 符号)
|   +-- type_date.svg                # 日期型 (日历符号)
|   +-- type_currency.svg            # 货币型 ($ 符号)
|
+-- measure_types/                   # 度量类型图标 (16x16 SVG)
|   +-- measure_scale.svg            # 度量 (刻度尺)
|   +-- measure_ordinal.svg          # 有序 (排序阶梯)
|   +-- measure_nominal.svg          # 名义 (标签)
|
+-- status/                          # 状态图标 (16x16 SVG)
|   +-- status_ready.svg             # 就绪 (绿色圆点)
|   +-- status_running.svg           # 运行中 (蓝色旋转)
|   +-- status_complete.svg          # 完成 (绿色对勾)
|   +-- status_error.svg             # 错误 (红色叉号)
|   +-- status_warning.svg           # 警告 (橙色感叹号)
|
+-- titlebar/                        # 标题栏图标 (16x16 SVG)
|   +-- btn_minimize.svg             # 最小化 (横线)
|   +-- btn_maximize.svg             # 最大化 (方块)
|   +-- btn_restore.svg              # 还原 (重叠方块)
|   +-- btn_close.svg                # 关闭 (X)
|
+-- sidebar/                         # 侧边栏图标 (16x16 SVG)
|   +-- sidebar_expand.svg           # 展开箭头
|   +-- sidebar_collapse.svg         # 折叠箭头
|   +-- sidebar_pin.svg              # 固定
|   +-- sidebar_unpin.svg            # 取消固定
|
+-- output/                          # 输出相关图标 (16x16 SVG)
|   +-- output_log.svg               # 日志
|   +-- output_table.svg             # 表格
|   +-- output_chart.svg             # 图表
|   +-- output_text.svg              # 文本
|   +-- output_warning.svg           # 警告
|   +-- output_note.svg              # 注释
|
+-- misc/                            # 杂项图标
    +-- empty_state.svg              # 空状态插图
    +-- loading.svg                  # 加载动画
    +-- about.svg                    # 关于
    +-- settings.svg                 # 设置 (齿轮)
    +-- help.svg                     # 帮助 (问号)
    +-- language.svg                 # 语言 (地球)
    +-- theme.svg                    # 主题 (调色板)
    +-- folder_open.svg              # 打开文件夹
    +-- recent_files.svg             # 最近文件
```

### 9.3 应用主图标设计规格

**视觉描述**: 字母 "A" 与统计元素（正态分布曲线 + 柱状图）的融合设计。

| 属性 | 值 |
|------|-----|
| 主色 | `#165DFF` (Arco Blue) |
| 辅助色 | `#4080FF` (渐变终止色) |
| 背景色 | 白色 `#FFFFFF` |
| 外框 | 蓝色渐变圆角方形 |
| 圆角半径 | Windows 11 Fluent Design 标准圆角 |
| 风格 | 扁平化 + 微阴影 |
| 识别元素 | 字母 A + 钟形曲线 + 柱状图 |
| 生成文件 | app_icon_main.jpg (已生成于 /workspace/axaltyx_icons/) |

**ICO 文件制作流程**:
1. 从生成的 JPG 裁剪为正方形
2. 使用 Python PIL 库缩放为 16/32/48/64/128/256 六种尺寸
3. 使用 `ico` 库打包为多尺寸 ICO 文件
4. 同时导出各尺寸 PNG 用于 Qt 资源文件

### 9.4 文件类型图标设计规格

#### .tbj 数据文件图标

| 属性 | 值 |
|------|-----|
| 形状 | 文档 + 折角 |
| 主色 | `#165DFF` |
| 背景色 | `#FFFFFF` |
| 内容元素 | 数据网格 (3x3) + 柱状图 (3 柱) |
| 底部标签 | "TBJ" 深蓝 `#0E42D2` |
| 折角颜色 | `#E8F3FF` |
| 生成文件 | file_icon_tbj.jpg (已生成于 /workspace/axaltyx_icons/) |

#### .axo 输出文件图标

| 属性 | 值 |
|------|-----|
| 形状 | 文档 + 折角 |
| 主色 | `#165DFF` |
| 背景色 | `#FFFFFF` |
| 内容元素 | 柱状图 + 表格网格 |
| 底部标签 | "AXO" 深蓝 `#0E42D2` |
| 生成文件 | output_icon_axo.jpg (已生成于 /workspace/axaltyx_icons/) |

#### .axs 语法文件图标

| 属性 | 值 |
|------|-----|
| 形状 | 文档 + 折角 |
| 主色 | `#165DFF` |
| 背景色 | `#FFFFFF` |
| 内容元素 | 语法高亮代码行 (蓝/绿/灰) + 运行三角按钮 |
| 底部标签 | "AXS" 深蓝 `#0E42D2` |
| 生成文件 | syntax_icon_axs.jpg (已生成于 /workspace/axaltyx_icons/) |

### 9.5 Windows 文件关联注册

安装时需在 Windows 注册表中注册以下文件关联:

```
HKEY_CLASSES_ROOT\.tbj
    (Default) = "AxaltyX.DataFile"
HKEY_CLASSES_ROOT\AxaltyX.DataFile
    (Default) = "AxaltyX Data File"
    DefaultIcon = "[INSTALL_PATH]\resources\icons\file_types\tbj_file.ico"
    shell\open\command = "[INSTALL_PATH]\AxaltyX.exe" "%1"

HKEY_CLASSES_ROOT\.axo
    (Default) = "AxaltyX.OutputFile"
HKEY_CLASSES_ROOT\AxaltyX.OutputFile
    (Default) = "AxaltyX Output File"
    DefaultIcon = "[INSTALL_PATH]\resources\icons\file_types\axo_file.ico"
    shell\open\command = "[INSTALL_PATH]\AxaltyX.exe" "%1"

HKEY_CLASSES_ROOT\.axs
    (Default) = "AxaltyX.SyntaxFile"
HKEY_CLASSES_ROOT\AxaltyX.SyntaxFile
    (Default) = "AxaltyX Syntax File"
    DefaultIcon = "[INSTALL_PATH]\resources\icons\file_types\axs_file.svg"
    shell\open\command = "[INSTALL_PATH]\AxaltyX.exe" "%1"
```

### 9.6 图标生成脚本步骤

**步骤**: 将 AI 生成的 JPG 转换为多尺寸 ICO/PNG/SVG 资源

**生成文件**: `build/generate_icons.py`

**功能**:
1. 读取生成的 JPG 图标
2. 裁剪为正方形
3. 缩放为 16/24/32/48/64/128/256 尺寸
4. 打包为 ICO 文件
5. 导出各尺寸 PNG
6. 生成 Qt 资源文件 (.qrc)

**验证**: 在 Windows 资源管理器中验证图标显示正确

---

## 第十部分: .tbj 文件格式规范

### 10.1 格式概述

| 属性 | 值 |
|------|-----|
| 扩展名 | `.tbj` |
| 全称 | TBJ114 Binary Data Format |
| 类型 | 二进制格式 |
| 压缩 | zlib 压缩 |
| 编码 | 内部使用 UTF-8 |
| 版本 | 1 |
| 最大文件大小 | 理论无限制（受磁盘空间约束） |
| 设计目标 | 快速读写、完整保留变量属性、支持大数据集 |

### 10.2 文件结构

```
.tbj 文件二进制布局:
+================================================================+
| 偏移量 | 长度   | 内容                                      |
|--------|--------|-------------------------------------------|
| 0x00   | 3 B    | Magic: "TBJ" (0x54 0x42 0x4A)             |
| 0x03   | 1 B    | 版本号: 1 (0x01)                          |
| 0x04   | 4 B    | 未压缩元数据长度 (uint32, little-endian)   |
| 0x08   | 4 B    | 压缩后元数据长度 (uint32, little-endian)   |
| 0x0C   | N B    | 压缩的元数据 (zlib)                       |
| 0x0C+N | 4 B    | 未压缩数据长度 (uint32, little-endian)     |
|        | 4 B    | 压缩后数据长度 (uint32, little-endian)     |
|        | M B    | 压缩的数据块 (zlib)                       |
+================================================================+
```

### 10.3 元数据结构 (JSON)

元数据部分为 JSON 格式，经 zlib 压缩后存储。

```json
{
  "format_version": 1,
  "created_by": "AxaltyX",
  "created_version": "1.0.0",
  "created_at": "2026-04-19T12:00:00+08:00",
  "modified_at": "2026-04-19T15:30:00+08:00",
  "author": "",
  "description": "",
  "dataset_name": "data1",
  "variables": [
    {
      "name": "VAR00001",
      "label": "age",
      "type": "numeric",
      "width": 8,
      "decimals": 2,
      "alignment": "right",
      "measure": "scale",
      "role": "input",
      "value_labels": [
        {"value": 1, "label": "male"},
        {"value": 2, "label": "female"}
      ],
      "missing_values": {
        "type": "discrete",
        "values": [-99, -999]
      },
      "column_width": 100,
      "format": "F8.2"
    }
  ],
  "variable_count": 100,
  "case_count": 100,
  "weight_variable": "",
  "filter_variable": "",
  "split_variable": "",
  "custom_attributes": {}
}
```

### 10.4 数据块结构

数据块采用 **列式存储** (Columnar Storage) 以优化分析性能:

```
数据块布局 (压缩前):
+----------------------------------------------------------+
| 数据编码头 (8 bytes)                                      |
|   encoding: 1 byte (0=double, 1=float, 2=int32, 3=int64)|
|   null_marker: 1 byte (NaN 值标记方式)                    |
|   reserved: 6 bytes                                       |
+----------------------------------------------------------+
| 列 0 数据: N * element_size bytes                         |
| 列 1 数据: N * element_size bytes                         |
| ...                                                       |
| 列 K 数据: N * element_size bytes                         |
+----------------------------------------------------------+
```

**编码规则**:
- 数值列: 根据数据范围自动选择 double/float/int32/int64
- 字符串列: UTF-8 编码，长度前缀 (4 bytes uint32) + 字节数据
- 日期列: int64 存储 Unix 时间戳 (毫秒)
- 缺失值: 数值列使用 NaN，字符串列使用空长度前缀 (0x00000000)

### 10.5 数据集类接口设计

```python
# core/data/dataset.py (伪代码)
class Dataset:
    """AxaltyX 数据集类"""

    def __init__(self, name: str = "Dataset1"):
        self.name: str = name
        self.variables: list[Variable] = []
        self.data: pd.DataFrame = pd.DataFrame()
        self.metadata: dict = {}
        self.weight_variable: str = ""
        self.filter_variable: str = ""
        self.split_variable: str = ""

    # --- 文件操作 ---
    def save_tbj(self, filepath: str) -> None: ...
    def load_tbj(self, filepath: str) -> None: ...
    def save_csv(self, filepath: str, **kwargs) -> None: ...
    def load_csv(self, filepath: str, **kwargs) -> None: ...
    def save_xlsx(self, filepath: str, **kwargs) -> None: ...
    def load_xlsx(self, filepath: str, **kwargs) -> None: ...
    def load_sav(self, filepath: str) -> None: ...
    def load_sas(self, filepath: str) -> None: ...
    def load_stata(self, filepath: str) -> None: ...
    def load_json(self, filepath: str) -> None: ...
    def load_html(self, filepath: str) -> None: ...
    def load_spss(self, filepath: str) -> None: ...  # .sav alias
    def load_parquet(self, filepath: str) -> None: ...
    def save_parquet(self, filepath: str) -> None: ...

    # --- 数据操作 ---
    def add_variable(self, var: Variable) -> None: ...
    def remove_variable(self, name: str) -> None: ...
    def rename_variable(self, old_name: str, new_name: str) -> None: ...
    def get_variable(self, name: str) -> Variable: ...
    def sort_cases(self, by: list[str], ascending: list[bool]) -> None: ...
    def select_cases(self, condition: str) -> None: ...
    def weight_cases(self, variable: str) -> None: ...
    def transpose(self) -> 'Dataset': ...
    def merge(self, other: 'Dataset', **kwargs) -> None: ...
    def aggregate(self, group_by: list[str], agg_dict: dict) -> 'Dataset': ...
    def restructure(self, **kwargs) -> 'Dataset': ...

    # --- 属性 ---
    @property
    def row_count(self) -> int: ...
    @property
    def column_count(self) -> int: ...
    @property
    def is_empty(self) -> bool: ...
```

### 10.6 .tbj 格式验证

**验证步骤**:
1. 读取 Magic "TBJ" (前 3 字节)
2. 读取版本号 (第 4 字节)，检查是否为支持的版本
3. 读取元数据长度，解压元数据 JSON
4. 验证 JSON 结构完整性（必须包含 variables、variable_count、case_count）
5. 读取数据块长度，解压数据
6. 验证数据行数与元数据 case_count 一致
7. 验证数据列数与元数据 variable_count 一致

**错误处理**:
- Magic 不匹配: 抛出 `InvalidFileFormatError`
- 版本不支持: 抛出 `UnsupportedVersionError`
- 元数据损坏: 抛出 `CorruptedMetadataError`
- 数据损坏: 抛出 `CorruptedDataError`

---

## 第十一部分: 多格式导入导出体系

### 11.1 支持格式总览

#### 导入格式 (读取)

| 格式 | 扩展名 | 依赖库 | 变量属性 | 编码支持 | 大数据 |
|------|--------|--------|---------|---------|--------|
| AxaltyX 数据 | `.tbj` | 内置 | 完整 | UTF-8 | 优秀 |
| CSV | `.csv` | pandas | 基础 | 自动检测 | 良好 |
| Excel | `.xlsx` `.xls` | openpyxl/xlrd | 基础 | UTF-8 | 一般 |
| SPSS | `.sav` | pyreadstat | 完整 | UTF-8 | 良好 |
| SPSS 便携 | `.por` | pyreadstat | 完整 | UTF-8 | 良好 |
| Stata | `.dta` | pandas | 完整 | UTF-8 | 良好 |
| SAS | `.sas7bdat` `.xpt` | pyreadstat | 完整 | UTF-8 | 良好 |
| JSON | `.json` | pandas | 无 | UTF-8 | 一般 |
| HTML 表格 | `.html` `.htm` | pandas | 无 | 自动检测 | 一般 |
| Parquet | `.parquet` | pyarrow | 基础 | UTF-8 | 优秀 |
| Feather | `.feather` | pyarrow | 基础 | UTF-8 | 优秀 |
| Clipboard | (剪贴板) | pandas | 无 | 系统编码 | N/A |
| ODS | `.ods` | pandas | 基础 | UTF-8 | 一般 |

#### 导出格式 (写入)

| 格式 | 扩展名 | 依赖库 | 变量属性 | 编码 | 大数据 |
|------|--------|--------|---------|------|--------|
| AxaltyX 数据 | `.tbj` | 内置 | 完整 | UTF-8 | 优秀 |
| CSV | `.csv` | pandas | 仅列名 | 可选 | 良好 |
| Excel | `.xlsx` | openpyxl | 仅列名 | UTF-8 | 一般 |
| SPSS | `.sav` | pyreadstat | 完整 | UTF-8 | 良好 |
| Stata | `.dta` | pandas | 完整 | UTF-8 | 良好 |
| SAS XPORT | `.xpt` | pyreadstat | 完整 | UTF-8 | 良好 |
| JSON | `.json` | pandas | 无 | UTF-8 | 一般 |
| Parquet | `.parquet` | pyarrow | 基础 | UTF-8 | 优秀 |
| Feather | `.feather` | pyarrow | 基础 | UTF-8 | 优秀 |
| HTML | `.html` | 内置 | 无 | UTF-8 | 一般 |
| PDF | `.pdf` | reportlab | 无 | UTF-8 | 一般 |
| LaTeX | `.tex` | 内置 | 无 | UTF-8 | 一般 |
| ODS | `.ods` | pandas | 仅列名 | UTF-8 | 一般 |

#### 输出导出格式

| 格式 | 扩展名 | 内容 | 依赖 |
|------|--------|------|------|
| AxaltyX 输出 | `.axo` | 完整输出 (表格+图表+日志) | 内置 |
| HTML | `.html` | 输出查看器内容 | 内置 |
| PDF | `.pdf` | 输出查看器内容 (含图表) | reportlab |
| Word | `.docx` | 输出表格 | python-docx |
| 纯文本 | `.txt` | 输出文本 | 内置 |
| CSV | `.csv` | 输出表格数据 | pandas |
| PNG | `.png` | 单个图表 | matplotlib |
| SVG | `.svg` | 单个图表 | matplotlib |
| Clipboard | (剪贴板) | 表格/图表 | 系统剪贴板 |

### 11.2 文件对话框过滤器

**打开文件对话框**:
```
AxaltyX Data (*.tbj);;SPSS Files (*.sav);;Stata Files (*.dta);;SAS Files (*.sas7bdat);;CSV Files (*.csv);;Excel Files (*.xlsx *.xls);;JSON Files (*.json);;Parquet Files (*.parquet);;HTML Tables (*.html *.htm);;All Files (*.*)
```

**保存文件对话框**:
```
AxaltyX Data (*.tbj);;CSV Files (*.csv);;Excel Files (*.xlsx);;SPSS Files (*.sav);;Stata Files (*.dta);;SAS XPORT (*.xpt);;JSON Files (*.json);;Parquet Files (*.parquet);;HTML (*.html);;PDF (*.pdf);;LaTeX (*.tex);;All Files (*.*)
```

**导出输出对话框**:
```
AxaltyX Output (*.axo);;HTML (*.html);;PDF (*.pdf);;Word (*.docx);;Text (*.txt);;CSV (*.csv);;All Files (*.*)
```

### 11.3 导入选项对话框

对于每种导入格式，提供专门的导入选项对话框:

#### CSV 导入选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| 编码 | 下拉选择 | 自动检测 | UTF-8, GBK, GB2312, GB18030, BIG5, Shift-JIS, ISO-8859-1 |
| 分隔符 | 下拉选择 | 逗号 | 逗号、制表符、分号、空格、自定义 |
| 小数符号 | 下拉选择 | 点 | 点 (.)、逗号 (,) |
| 文本限定符 | 下拉选择 | 双引号 | 双引号、单引号、无 |
| 首行作为变量名 | 复选框 | 勾选 | - |
| 最大导入行数 | 数字输入 | 0 (全部) | 0 表示全部导入 |
| 缺失值标记 | 文本输入 | 空 | 指定哪些值视为缺失值 |
| 字符串引号处理 | 下拉选择 | 遵循限定符 | 遵循限定符、全部去除、保留 |
| 日期格式 | 下拉选择 | 自动检测 | YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY 等 |

#### Excel 导入选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| 工作表 | 下拉选择 | 第一个 | 选择要导入的工作表 |
| 数据范围 | 文本输入 | 全部 | 如 A1:Z1000 |
| 首行作为变量名 | 复选框 | 勾选 | - |
| 最大导入行数 | 数字输入 | 0 (全部) | - |

#### SPSS .sav 导入选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| 导入变量标签 | 复选框 | 勾选 | 将 SPSS 变量标签导入为 AxaltyX 标签 |
| 导入值标签 | 复选框 | 勾选 | 将 SPSS 值标签导入 |
| 导入缺失值定义 | 复选框 | 勾选 | 将 SPSS 缺失值定义导入 |
| 导入变量度量 | 复选框 | 勾选 | 将 SPSS 度量类型导入 |
| 导入多重响应集 | 复选框 | 勾选 | 将 SPSS 多重响应集定义导入 |
| 编码 | 下拉选择 | 自动检测 | UTF-8, GBK, 等 |

### 11.4 导出选项对话框

#### CSV 导出选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| 编码 | 下拉选择 | UTF-8 (BOM) | UTF-8, UTF-8 BOM, GBK, GB2312 |
| 分隔符 | 下拉选择 | 逗号 | 逗号、制表符、分号 |
| 小数符号 | 下拉选择 | 点 | 点 (.)、逗号 (,) |
| 变量名写入首行 | 复选框 | 勾选 | - |
| 缺失值输出 | 下拉选择 | 空字符串 | 空字符串、"."、"NA"、自定义 |
| 引号包裹 | 下拉选择 | 仅字符串 | 仅字符串、全部、无 |

#### Excel 导出选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| 工作表名称 | 文本输入 | 数据 | - |
| 变量名写入首行 | 复选框 | 勾选 | - |
| 包含变量标签行 | 复选框 | 不勾选 | 在变量名下方添加标签行 |
| 数值格式 | 下拉选择 | 自动 | 自动、固定小数位、科学计数法 |
| 小数位数 | 数字输入 | 自动 | 0-15 |
| 冻结首行 | 复选框 | 勾选 | - |

### 11.5 文件 I/O 管理器接口设计

```python
# utils/file_io.py (伪代码)
class FileManager:
    """文件输入输出管理器 - 单例模式"""

    # --- 导入 ---
    def import_file(self, filepath: str, options: dict = None) -> Dataset: ...
    def import_csv(self, filepath: str, options: dict = None) -> Dataset: ...
    def import_xlsx(self, filepath: str, options: dict = None) -> Dataset: ...
    def import_sav(self, filepath: str, options: dict = None) -> Dataset: ...
    def import_dta(self, filepath: str, options: dict = None) -> Dataset: ...
    def import_sas(self, filepath: str, options: dict = None) -> Dataset: ...
    def import_json(self, filepath: str, options: dict = None) -> Dataset: ...
    def import_html(self, filepath: str, options: dict = None) -> Dataset: ...
    def import_parquet(self, filepath: str, options: dict = None) -> Dataset: ...
    def import_feather(self, filepath: str, options: dict = None) -> Dataset: ...
    def import_clipboard(self) -> Dataset: ...

    # --- 导出 ---
    def export_file(self, dataset: Dataset, filepath: str, options: dict = None) -> None: ...
    def export_csv(self, dataset: Dataset, filepath: str, options: dict = None) -> None: ...
    def export_xlsx(self, dataset: Dataset, filepath: str, options: dict = None) -> None: ...
    def export_sav(self, dataset: Dataset, filepath: str, options: dict = None) -> None: ...
    def export_dta(self, dataset: Dataset, filepath: str, options: dict = None) -> None: ...
    def export_xpt(self, dataset: Dataset, filepath: str, options: dict = None) -> None: ...
    def export_json(self, dataset: Dataset, filepath: str, options: dict = None) -> None: ...
    def export_parquet(self, dataset: Dataset, filepath: str, options: dict = None) -> None: ...
    def export_feather(self, dataset: Dataset, filepath: str, options: dict = None) -> None: ...
    def export_html(self, dataset: Dataset, filepath: str, options: dict = None) -> None: ...
    def export_pdf(self, dataset: Dataset, filepath: str, options: dict = None) -> None: ...
    def export_latex(self, dataset: Dataset, filepath: str, options: dict = None) -> None: ...

    # --- 输出导出 ---
    def export_output(self, output, filepath: str, options: dict = None) -> None: ...
    def export_output_html(self, output, filepath: str) -> None: ...
    def export_output_pdf(self, output, filepath: str) -> None: ...
    def export_output_docx(self, output, filepath: str) -> None: ...
    def export_output_txt(self, output, filepath: str) -> None: ...

    # --- 工具 ---
    def detect_encoding(self, filepath: str) -> str: ...
    def detect_delimiter(self, filepath: str, encoding: str) -> str: ...
    def get_supported_import_formats(self) -> list[FormatInfo]: ...
    def get_supported_export_formats(self) -> list[FormatInfo]: ...
```

### 11.6 编码自动检测策略

```
优先级顺序:
1. 用户在导入对话框中手动指定
2. 文件 BOM 头检测 (UTF-8 BOM: EF BB BF, UTF-16 LE: FF FE, UTF-16 BE: FE FF)
3. chardet 库自动检测 (置信度 > 0.9 时采用)
4. cchardet 库快速检测 (C 加速版)
5. 回退到系统默认编码 (Windows: GBK, macOS: UTF-8)
```

### 11.7 大数据优化策略

| 策略 | 说明 |
|------|------|
| 分块读取 | CSV/Excel 超过 10 万行时启用分块读取 |
| 延迟加载 | 仅加载元数据，数据按需加载到内存 |
| 内存映射 | Parquet/Feather 使用零拷贝内存映射 |
| 类型推断优化 | 首次扫描前 1000 行推断列类型 |
| 进度反馈 | 大文件导入时显示进度条 |
| 取消支持 | 大文件导入过程中可取消 |
| 列式存储 | .tbj 原生格式采用列式存储优化分析性能 |

### 11.8 实施步骤补充

#### 步骤 3.1 (修订): 数据集序列化 (.tbj 格式)

**目标**: 实现 .tbj 二进制文件格式读写

**生成文件**:
- `axaltyx/core/data/dataset.py`
- `axaltyx/core/data/tbj_format.py` (新增: .tbj 格式编解码器)
- `axaltyx/core/data/tbj_validator.py` (新增: .tbj 格式验证器)

**功能**:
- `TBJEncoder`: Dataset -> .tbj 二进制
  - 编写 Magic + 版本号
  - 序列化元数据 JSON -> zlib 压缩
  - 列式序列化数据 -> zlib 压缩
  - 写入文件
- `TBJDecoder`: .tbj 二进制 -> Dataset
  - 读取并验证 Magic + 版本号
  - 解压并解析元数据 JSON
  - 解压并反序列化数据
  - 重建 Dataset 对象
- `TBJValidator`: 验证 .tbj 文件完整性
  - Magic 验证
  - 版本兼容性检查
  - CRC32 校验 (可选)
  - 元数据完整性检查
  - 数据维度一致性检查

**验证**:
- 创建数据集 -> 保存为 .tbj -> 加载 -> 数据完全一致
- 变量属性（标签、值标签、缺失值、度量）完整保留
- 大数据集 (100万行 x 100列) 保存/加载 < 3 秒
- 损坏的 .tbj 文件抛出正确的异常类型

#### 步骤 3.2 (修订): 多格式导入导出

**目标**: 实现所有格式的导入导出

**生成文件**:
- `axaltyx/utils/file_io.py` (完善)
- `axaltyx/utils/encoding_detector.py` (新增)
- `axaltyx/gui/dialogs/import_dialog.py` (新增: 导入选项对话框)
- `axaltyx/gui/dialogs/export_dialog.py` (新增: 导出选项对话框)
- `axaltyx/gui/dialogs/import_csv_dialog.py` (新增)
- `axaltyx/gui/dialogs/import_xlsx_dialog.py` (新增)
- `axaltyx/gui/dialogs/import_sav_dialog.py` (新增)
- `axaltyx/gui/dialogs/export_csv_dialog.py` (新增)
- `axaltyx/gui/dialogs/export_xlsx_dialog.py` (新增)

**验证**:
- 导入 CSV (UTF-8/GBK/含BOM) 数据正确
- 导入 Excel 多工作表选择正确
- 导入 SPSS .sav 变量属性完整保留
- 导入 Stata .dta 数据正确
- 导入 SAS .sas7bdat 数据正确
- 导入 JSON/HTML/Parquet 数据正确
- 导出 CSV (UTF-8 BOM) Excel 可正确打开
- 导出 Excel 变量名/标签正确
- 导出 SPSS .sav 变量属性完整保留
- 导出 PDF 表格格式正确
- 大文件导入显示进度条，可取消

---

## 第十二部分: 原规划文档修订对照

### 12.1 需要修订的原有内容

| 原文位置 | 原内容 | 修订为 |
|---------|--------|--------|
| 第六部分 6.4 | .axl 文件格式 | 替换为 .tbj 文件格式（第十部分） |
| 第三部分 resources/icons/ | 简单的图标目录 | 替换为完整的图标体系（第九部分 9.2） |
| 第五部分 步骤 3.1 | .axl 序列化 | 替换为 .tbj 序列化（第十一部分 11.8） |
| 第五部分 步骤 3.2 | 仅 CSV/Excel/SPSS | 扩展为全格式支持（第十一部分） |
| 第八部分 依赖版本 | 缺少新依赖 | 补充 pyarrow, chardet, cchardet, python-docx, reportlab |

### 12.2 新增依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| pyarrow | >= 12.0.0 | Parquet/Feather 读写 |
| chardet | >= 5.0.0 | 编码自动检测 |
| cchardet | >= 2.1.0 | 快速编码检测 (C 加速) |
| python-docx | >= 0.8.11 | Word 文档导出 |
| reportlab | >= 4.0.0 | PDF 导出 |
| Pillow | >= 10.0.0 | 图标处理 (JPG -> ICO/PNG) |

### 12.3 新增 i18n JSON 条目

**zh_CN/app.json 新增**:
```json
{
  "file_filter_import": "AxaltyX 数据 (*.tbj);;SPSS 文件 (*.sav);;Stata 文件 (*.dta);;SAS 文件 (*.sas7bdat);;CSV 文件 (*.csv);;Excel 文件 (*.xlsx *.xls);;JSON 文件 (*.json);;Parquet 文件 (*.parquet);;HTML 表格 (*.html *.htm);;所有文件 (*.*)",
  "file_filter_export": "AxaltyX 数据 (*.tbj);;CSV 文件 (*.csv);;Excel 文件 (*.xlsx);;SPSS 文件 (*.sav);;Stata 文件 (*.dta);;SAS XPORT (*.xpt);;JSON 文件 (*.json);;Parquet 文件 (*.parquet);;HTML (*.html);;PDF (*.pdf);;LaTeX (*.tex);;所有文件 (*.*)",
  "file_filter_output": "AxaltyX 输出 (*.axo);;HTML (*.html);;PDF (*.pdf);;Word (*.docx);;文本 (*.txt);;CSV (*.csv);;所有文件 (*.*)",
  "import_title": "导入数据",
  "export_title": "导出数据",
  "import_progress": "正在导入: {filename} ({percent}%)",
  "export_progress": "正在导出: {filename} ({percent}%)",
  "import_complete": "导入完成: {rows} 行 {cols} 列",
  "export_complete": "导出完成",
  "import_cancelled": "导入已取消",
  "encoding_detect": "自动检测",
  "encoding_utf8": "UTF-8",
  "encoding_utf8_bom": "UTF-8 (BOM)",
  "encoding_gbk": "GBK",
  "encoding_gb2312": "GB2312",
  "encoding_gb18030": "GB18030",
  "delimiter_comma": "逗号",
  "delimiter_tab": "制表符",
  "delimiter_semicolon": "分号",
  "delimiter_space": "空格",
  "decimal_dot": "点 (.)",
  "decimal_comma": "逗号 (,)",
  "first_row_variables": "首行作为变量名",
  "max_rows": "最大导入行数 (0 = 全部)",
  "missing_values_custom": "自定义缺失值标记",
  "tbj_invalid_format": "无效的 .tbj 文件格式",
  "tbj_unsupported_version": "不支持的 .tbj 文件版本: {version}",
  "tbj_corrupted": ".tbj 文件已损坏: {detail}"
}
```

---

*本文档为 AxaltyX 项目补充设计文档，版权所有 TBJ114。*
*配套主文档: AxaltyX_Development_Plan.md*
