# AxaltyX -- 个人学术科研专用统计软件 完整开发规划

> 版权所有: TBJ114
> 编译环境: Windows 11
> GUI框架: Qt6 (PyQt6/PySide6)
> 统计引擎: axaltyx-core (Python 包)
> 设计语言: Arco Design / ByteDesign

---

## 第一部分: 产品定位与设计语言

### 1.1 产品定位

| 维度 | 定义 |
|------|------|
| 面向用户 | 本科生、研究生、科研人员、问卷与数据分析用户 |
| 产品定位 | 专业统计工具，功能 >= SPSS 标准版，速度 >= SPSS 3 倍 |
| 运行模式 | 本地离线优先，可选字节账号登录同步配置 |
| 视觉风格 | 现代简洁、字节设计语言（Arco Design） |
| 分发方式 | Windows 安装包（NSIS/Inno Setup） |

### 1.2 设计语言规范 (基于 Arco Design)

#### 1.2.1 色彩系统

**主色 (Arco Blue)**

| 状态 | 色值 | 用途 |
|------|------|------|
| 常规态 | `#165DFF` | 主色、品牌色 |
| 悬浮态 | `#4080FF` | 按钮/链接 Hover |
| 点击态 | `#0E42D2` | 按钮/链接 Active |
| 浅色背景 | `#E8F3FF` | 选中行背景、高亮区域 |

**中性色 (灰阶)**

| Token | 色值 | 用途 |
|-------|------|------|
| gray-1 | `#F7F8FA` | 最浅背景 |
| gray-2 | `#F2F3F5` | 页面背景 |
| gray-3 | `#E5E6EB` | 边框/分割线 |
| gray-4 | `#C9CDD4` | 禁用态边框 |
| gray-5 | `#A9AEB8` | 占位文字 |
| gray-6 | `#86909C` | 次要文字 |
| gray-7 | `#6B7785` | 辅助文字 |
| gray-8 | `#4E5969` | 常规文字 |
| gray-9 | `#272E3B` | 标题文字 |
| gray-10 | `#1D2129` | 主要标题 |

**功能色**

| 功能 | 色值 | 用途 |
|------|------|------|
| 成功 | `#00B42A` | 操作成功、通过 |
| 警告 | `#FF7D00` | 警告提示 |
| 错误 | `#F53F3F` | 错误、危险操作 |
| 链接 | `#165DFF` | 可点击链接 |

**数据可视化色板 (前10色)**

| 序号 | 色值 | 序号 | 色值 |
|------|------|------|------|
| 1 | `#165DFF` | 6 | `#722ED1` |
| 2 | `#F53F3F` | 7 | `#F77234` |
| 3 | `#00B42A` | 8 | `#FADC19` |
| 4 | `#3491FA` | 9 | `#14C9C9` |
| 5 | `#F5319D` | 10 | `#9FDB1D` |

#### 1.2.2 字体系统

| 平台 | 中文字体 | 英文/数字字体 |
|------|----------|-------------|
| Windows | Microsoft YaHei | Nunito |
| macOS | PingFang SC | Nunito |

字体栈: `'Nunito', 'Microsoft YaHei', 'PingFang SC', 'Helvetica Neue', Arial, sans-serif`

**字号层级**

| Token | 值 | 用途 |
|-------|-----|------|
| font-size-caption | 12px | 辅助文案、水印 |
| font-size-body-1 | 14px | 正文（主字号） |
| font-size-title-1 | 16px | 小标题 |
| font-size-title-2 | 20px | 中标题 |
| font-size-title-3 | 24px | 大标题 |
| font-size-display-1 | 36px | 运营标题 |

**字重**

| 字重 | 使用场景 |
|------|---------|
| 400 (Regular) | 正文（最常用） |
| 500 (Medium) | 导航、标签、次要强调 |
| 600 (Semibold) | 标题、英文/数字加粗 |

#### 1.2.3 间距与圆角

**间距 (4px 基础网格)**

| Token | 值 | 用途 |
|-------|-----|------|
| spacing-mini | 4px | 最小间距 |
| spacing-small | 8px | 紧凑间距 |
| spacing-medium | 16px | 常规间距 |
| spacing-large | 24px | 宽松间距 |

**圆角**

| Token | 值 | 用途 |
|-------|-----|------|
| radius-none | 0px | 直角 |
| radius-small | 2px | 常规圆角 |
| radius-medium | 4px | 中等圆角 |
| radius-large | 8px | 较大圆角 |
| radius-circle | 50% | 全圆角 |

**阴影**

| 层级 | 值 | 用途 |
|------|-----|------|
| shadow-1 | `0 -2px 5px rgba(0,0,0,0.1)` | 卡片默认 |
| shadow-2 | `0 0 10px rgba(0,0,0,0.1)` | Hover 态 |
| shadow-3 | `0 0 20px rgba(0,0,0,0.1)` | 下拉菜单、模态框 |

#### 1.2.4 按钮规范

| 类型 | 视觉特征 |
|------|---------|
| Primary | 实心填充 `#165DFF`，白色文字 |
| Secondary | 浅灰背景，深色文字 |
| Outline | 透明背景，主色边框和文字 |
| Text | 纯文字，无边框 |

| 尺寸 | 高度 |
|------|------|
| mini | 24px |
| small | 28px |
| default | 32px |
| large | 36px |

---

## 第二部分: GUI 设计详细规范

### 2.1 整体布局架构

采用 Arco Design 的 **"T"型布局**（顶部导航 + 侧边栏 + 内容区），这是字节系产品最常用的布局模式。

```
+------------------------------------------------------------------+
|  [Logo] AxaltyX    [文件] [编辑] [视图] [分析] [图表] [工具] [帮助]  |  <- 顶部菜单栏 (高度: 40px)
+------------------------------------------------------------------+
|  [新建] [打开] [保存] | [撤销] [重做] | [复制] [粘贴] | [运行]     |  <- 工具栏 (高度: 36px)
+----------+-------------------------------------------------------+
|          |  数据编辑器标签页 |  输出查看器标签页                     |  <- 标签栏 (高度: 36px)
|  分析    +-------------------------------------------------------+
|  菜单    |                                                       |
|  树      |                                                       |
|          |                                                       |
|  (宽度   |              主内容区域                                 |
|  220px,  |          (数据表格 / 输出结果 / 图表)                    |
|  可折叠) |                                                       |
|          |                                                       |
|          |                                                       |
|          +-------------------------------------------------------+
|          |  状态栏: 就绪 | 行: 1, 列: 1 | 数据视图: 数据编辑器      |  <- 状态栏 (高度: 24px)
+----------+-------------------------------------------------------+
```

### 2.2 启动页面 (Splash Screen)

**设计规格**:
- 尺寸: 600 x 400 px，居中显示
- 背景: 纯白 `#FFFFFF`
- 内容: Logo + 产品名 "AxaltyX" + 版本号 + 加载进度条
- Logo: 使用 Arco Blue `#165DFF` 的几何图形（抽象统计符号，如正态分布曲线与柱状图的组合）
- 进度条: Arco Blue 渐变 (`#165DFF` -> `#4080FF`)，圆角 4px，高度 3px
- 版本号: 12px，灰色 `#86909C`
- 边框: 无边框，无边框阴影（无边框窗口 `FramelessWindow`）
- 显示时间: 1.5 - 3 秒（根据加载进度）
- 版权文字: "Copyright TBJ114. All rights reserved." 12px 灰色

**启动页面布局**:
```
+------------------------------------------+
|                                          |
|              [Logo 图标]                  |
|                                          |
|              AxaltyX                     |
|           v1.0.0 (Build 1)               |
|                                          |
|     [===========              ] 45%      |
|                                          |
|     Copyright TBJ114. All rights reserved|
+------------------------------------------+
```

### 2.3 主窗口框架 (定制边框)

**无边框窗口实现**:
- 使用 `Qt::FramelessWindowHint` 创建无边框窗口
- 自绘标题栏（高度: 32px）
- 支持拖拽移动、四边/四角调整大小
- 最小化、最大化/还原、关闭按钮位于标题栏右侧

**标题栏布局**:
```
+------------------------------------------------------------------+
| [App Icon] AxaltyX - [文件名.axl] - 数据编辑器    [_] [X] [X]   |
+------------------------------------------------------------------+
```

- 左侧: 应用图标 (16x16) + 窗口标题（14px, gray-8）
- 右侧: 最小化、最大化、关闭按钮（各 32x32）
- 关闭按钮 Hover 态: 红色背景 `#F53F3F`，白色图标
- 其他按钮 Hover 态: gray-2 背景
- 标题栏背景: `#FFFFFF`
- 标题栏底部: 1px 分割线 `#E5E6EB`

### 2.4 数据编辑器 (类似 SPSS 数据视图)

**核心要求**: 即使是空文件，也显示 100 行 x 100 列的表格，表头可更改。

**表格规格**:
- 默认行数: 100 行（大文件可动态扩展，支持百万级行数）
- 默认列数: 100 列（可动态添加）
- 默认列名: VAR00001, VAR00002, ... VAR00100
- 行号列: 固定在左侧，宽度 48px，灰色背景 `#F7F8FA`
- 列头: 可双击编辑，支持中文/英文/自定义名称
- 单元格默认值: 空白（缺失值显示为 `.`，SPSS 风格）
- 选中单元格: 蓝色边框 `#165DFF`
- 选中行/列: 浅蓝背景 `#E8F3FF`
- 网格线: 1px `#E5E6EB`
- 单元格尺寸: 默认行高 28px，列宽 100px（可拖拽调整）
- 字体: 14px Regular，等宽字体用于数值列

**数据编辑器双视图模式** (标签页切换):

| 标签页 | 内容 |
|--------|------|
| 数据视图 | 显示实际数据值 |
| 变量视图 | 显示变量属性（名称、类型、宽度、小数位、标签、值标签、缺失值、度量尺度等） |

**变量视图表格列**:

| 列名 | 宽度 | 编辑方式 |
|------|------|---------|
| 名称 | 100px | 文本输入 |
| 类型 | 100px | 下拉选择（数值、字符串、日期） |
| 宽度 | 60px | 数字输入 |
| 小数位 | 60px | 数字输入 |
| 标签 | 200px | 文本输入 |
| 值标签 | 200px | 弹窗编辑器 |
| 缺失值 | 100px | 弹窗编辑器 |
| 列宽 | 60px | 数字输入 |
| 对齐 | 80px | 下拉选择（左/右/居中） |
| 度量 | 100px | 下拉选择（度量、有序、名义） |
| 角色 | 100px | 下拉选择（输入、目标、两者） |

### 2.5 侧边栏 - 分析菜单树

**宽度**: 220px（可折叠至 56px 仅显示图标）

**菜单结构** (树形，可展开/折叠):

```
分析
+-- 统计摘要
|   +-- 频数分析
|   +-- 描述性统计
|   +-- 探索分析
+-- 比较均值
|   +-- 均值
|   +-- 单样本 T 检验
|   +-- 独立样本 T 检验
|   +-- 配对样本 T 检验
+-- 一般线性模型
|   +-- 单因素方差分析
|   +-- 多因素方差分析
|   +-- 协方差分析
|   +-- 重复测量方差分析
+-- 非参数检验
|   +-- 卡方检验
|   +-- 二项检验
|   +-- 游程检验
|   +-- 单样本 K-S 检验
|   +-- 两个独立样本检验
|   +-- 多个独立样本检验
|   +-- 两个相关样本检验
|   +-- 多个相关样本检验
+-- 相关分析
|   +-- 双变量相关
|   +-- 偏相关
+-- 回归分析
|   +-- 线性回归
|   +-- 多元线性回归
|   +-- Logistic 回归
|   +-- 有序回归
|   +-- 非线性回归
|   +-- 曲线估计
|-- 分类
|   +-- 因子分析
|   +-- 主成分分析
|   +-- 聚类分析
|   +-- 判别分析
|   +-- 对应分析
+-- 尺度分析
|   +-- 信度分析
|   +-- 效度分析
|   +-- 多维尺度
+-- 生存分析
|   +-- Kaplan-Meier
|   +-- Cox 回归
+-- 高级分析
|   +-- 结构方程模型 SEM
|   +-- 贝叶斯统计
|   +-- Meta 分析
|   +-- 时间序列分析
|   +-- 对数线性模型
|   +-- Probit 分析
+-- 因果推断
|   +-- 倾向得分匹配 PSM
|   +-- 双重差分 DID
|   +-- 工具变量法
|   +-- 断点回归 RDD
|   +-- 分位数回归
+-- 机器学习
|   +-- Lasso / 岭回归 / 弹性网
|   +-- 随机森林
|   +-- 支持向量机
|   +-- 梯度提升树
|   +-- 神经网络
|   +-- 贝叶斯网络
+-- 文本分析
|   +-- 文本挖掘
|   +-- 情感分析
|   +-- 词云生成
+-- 空间分析
|   +-- 空间计量分析
|   +-- 网络分析
+-- 多层模型
|   +-- 多层线性模型 HLM
|   +-- 贝叶斯分层模型
+-- 高级贝叶斯
|   +-- 贝叶斯因子分析
|   +-- 贝叶斯聚类
|   +-- 贝叶斯生存分析
|   +-- 贝叶斯 Logistic 回归
```

**侧边栏样式**:
- 背景: `#FFFFFF`
- 菜单项高度: 32px
- 菜单项文字: 14px, gray-8
- 菜单项 Hover: 背景 `#F2F3F5`
- 菜单项选中: 背景 `#E8F3FF`，文字 `#165DFF`，左侧 2px 蓝色指示条
- 一级菜单图标: 16x16，Arco 线性图标风格（2px 描边）
- 展开/折叠箭头: 12x12，gray-6
- 分组标题: 12px, gray-6, Medium 字重, 大写字母间距
- 滚动条: 自定义细滚动条，宽度 4px

### 2.6 分析对话框 (以 "描述性统计" 为例)

点击侧边栏菜单项后弹出模态对话框，采用 SPSS 风格但使用 Arco Design 视觉语言。

**对话框布局**:
```
+----------------------------------------------------------+
|  描述性统计                                           [X] |
+----------------------------------------------------------+
|                                                          |
|  变量列表          [>]     分析变量列表                    |
|  +------------+    +---+  +------------------+            |
|  | VAR00001   |    | > |  | VAR00003         |            |
|  | VAR00002   |    |   |  | VAR00005         |            |
|  | VAR00003   |    | < |  |                  |            |
|  | VAR00004   |    +---+  |                  |            |
|  | VAR00005   |          |                  |            |
|  +------------+          +------------------+            |
|                                                          |
|  [统计量...]  [图表...]  [格式...]  [Bootstrap...]       |
|                                                          |
|                              [粘贴]  [重置]  [确定] [取消]|
+----------------------------------------------------------+
```

**对话框规范**:
- 标题栏: 高度 40px，16px Semibold，gray-10，左侧无图标
- 关闭按钮: 右上角，24x24
- 变量列表框: 高度自适应（最小 200px），带表头
- 变量移动按钮: 中间，垂直排列 `>` `>` `<` `<`，28x28 圆角按钮
- 选项按钮行: 对话框底部，Secondary 样式
- 底部按钮: 右对齐，[确定] Primary，[取消] Secondary，[粘贴] Text，[重置] Text
- 对话框尺寸: 最小 520x480，可调整大小
- 遮罩层: `rgba(29, 33, 41, 0.6)`

### 2.7 输出查看器

**输出内容结构** (树形导航 + 内容区):

```
+----------------------------------------------------------+
|  输出 - [文件名.axl]                                      |
+----------------------------------------------------------+
| 输出导航  |  日志                                          |
| 树        |  > GET DATA                                    |
|           |    FILE='data.csv'                             |
| +-- 日志  |    DATASET NAME 数据集1.                        |
| +-- 描述  |                                               |
| |   +-- 描述性统计  |  描述性统计                            |
| +-- 表格  |  +------------------------------------------+  |
| |   +-- 描述统计量  |  | 统计量    | VAR00001 | VAR00002 |  |
| +-- 图表  |  |----------|----------|----------|          |  |
|           |  | N        | 100      | 100      |          |  |
|           |  | 均值     | 45.23    | 32.10    |          |  |
|           |  | 标准差   | 12.45    | 8.76     |          |  |
|           |  +------------------------------------------+  |
|           |                                               |
+----------------------------------------------------------+
```

**输出查看器规范**:
- 左侧导航树: 宽度 200px，可折叠
- 右侧内容区: 富文本 + 表格 + 嵌入图表
- 表格样式: 交替行背景（白色 / `#F7F8FA`），1px `#E5E6EB` 边框
- 表头: gray-2 背景，14px Medium
- 表格内容: 14px Regular，右对齐数值
- 支持右键菜单: 复制、导出、删除
- 支持导出格式: HTML、PDF、CSV、PNG

### 2.8 图表展示与编辑

**图表窗口** (独立标签页或浮动窗口):
- 图表画布: 白色背景，自适应大小
- 图表标题: 16px Semibold，居中
- 坐标轴标签: 12px Regular，gray-8
- 图例: 右侧或底部，12px Regular
- 支持交互: 悬浮显示数值、缩放、平移
- 右键菜单: 导出 PNG/SVG/PDF、复制到剪贴板、编辑样式

**图表编辑面板** (右侧滑出面板):
- 标题编辑: 文本、字体、大小、颜色
- 坐标轴编辑: 范围、刻度、标签、网格线
- 图例编辑: 位置、字体、显示/隐藏
- 颜色编辑: 系列颜色、背景色
- 尺寸编辑: 宽度、高度、DPI

### 2.9 语法编辑器 (可选标签页)

- 语法高亮: 关键字蓝色、字符串绿色、注释灰色
- 行号: 左侧显示
- 自动补全: 分析命令、变量名
- 执行按钮: 工具栏或快捷键 Ctrl+R

### 2.10 设置对话框

**设置分类** (左侧导航):

| 分类 | 包含选项 |
|------|---------|
| 通用 | 语言（中文/英文）、启动行为、默认文件夹 |
| 数据 | 默认小数位数、自定义缺失值、数据缓存大小 |
| 输出 | 输出格式、表格样式、图表默认样式 |
| 图表 | 默认颜色方案、字体、分辨率 |
| 性能 | 多线程设置、内存限制、GPU 加速 |
| 高级 | 日志级别、插件管理、更新检查 |

---

## 第三部分: 项目目录结构

```
AxaltyX/
|
+-- axaltyx/                          # 主应用包
|   +-- __init__.py
|   +-- main.py                       # 应用入口
|   +-- app.py                        # QApplication 初始化
|   |
|   +-- core/                         # 核心引擎（纯 Python 统计库）
|   |   +-- __init__.py
|   |   +-- data/                     # 数据管理
|   |   |   +-- __init__.py
|   |   |   +-- dataset.py            # 数据集类（加载、保存、操作）
|   |   |   +-- variable.py           # 变量定义类
|   |   |   +-- missing.py            # 缺失值处理
|   |   |   +-- transform.py          # 数据变换
|   |   |   +-- aggregate.py          # 分类汇总
|   |   |   +-- restructure.py        # 数据重构
|   |   |   +-- weight.py             # 加权处理
|   |   |   +-- transpose.py          # 转置
|   |   +-- descriptive/              # 描述性统计
|   |   |   +-- __init__.py
|   |   |   +-- frequencies.py        # 频数分析
|   |   |   +-- descriptives.py       # 描述性统计
|   |   |   +-- crosstabs.py          # 交叉表与卡方检验
|   |   |   +-- explore.py            # 探索分析
|   |   +-- means/                    # 均值比较
|   |   |   +-- __init__.py
|   |   |   +-- means.py              # 均值
|   |   |   +-- ttest_one.py          # 单样本 T 检验
|   |   |   +-- ttest_independent.py  # 独立样本 T 检验
|   |   |   +-- ttest_paired.py       # 配对样本 T 检验
|   |   +-- anova/                    # 方差分析
|   |   |   +-- __init__.py
|   |   |   +-- oneway.py             # 单因素方差分析
|   |   |   +-- manova.py             # 多因素方差分析
|   |   |   +-- ancova.py             # 协方差分析
|   |   |   +-- rm_anova.py           # 重复测量方差分析
|   |   +-- nonparametric/            # 非参数检验
|   |   |   +-- __init__.py
|   |   |   +-- chisquare.py          # 卡方检验
|   |   |   +-- binomial.py           # 二项检验
|   |   |   +-- runs.py               # 游程检验
|   |   |   +-- ks.py                 # K-S 检验
|   |   |   +-- two_independent.py    # 两独立样本
|   |   |   +-- k_independent.py      # 多独立样本
|   |   |   +-- two_related.py        # 两相关样本
|   |   |   +-- k_related.py          # 多相关样本
|   |   +-- correlation/              # 相关分析
|   |   |   +-- __init__.py
|   |   |   +-- bivariate.py          # 双变量相关
|   |   |   +-- partial.py            # 偏相关
|   |   +-- regression/               # 回归分析
|   |   |   +-- __init__.py
|   |   |   +-- linear.py             # 线性回归
|   |   |   +-- multiple.py           # 多元线性回归
|   |   |   +-- logistic.py           # Logistic 回归
|   |   |   +-- ordinal.py            # 有序回归
|   |   |   +-- nonlinear.py          # 非线性回归
|   |   |   +-- curve_est.py          # 曲线估计
|   |   +-- classification/           # 分类分析
|   |   |   +-- __init__.py
|   |   |   +-- factor.py             # 因子分析
|   |   |   +-- pca.py                # 主成分分析
|   |   |   +-- cluster.py            # 聚类分析
|   |   |   +-- discriminant.py       # 判别分析
|   |   |   +-- correspondence.py     # 对应分析
|   |   +-- scale/                    # 尺度分析
|   |   |   +-- __init__.py
|   |   |   +-- reliability.py        # 信度分析
|   |   |   +-- validity.py           # 效度分析
|   |   |   +-- multidimensional.py   # 多维尺度
|   |   +-- survival/                 # 生存分析
|   |   |   +-- __init__.py
|   |   |   +-- kaplan_meier.py       # Kaplan-Meier
|   |   |   +-- cox.py                # Cox 回归
|   |   |   +-- advanced.py           # 高级生存模型
|   |   +-- advanced/                 # 高级分析
|   |   |   +-- __init__.py
|   |   |   +-- sem.py                # 结构方程模型
|   |   |   +-- bayesian.py           # 贝叶斯统计
|   |   |   +-- meta.py               # Meta 分析
|   |   |   +-- timeseries.py         # 时间序列分析
|   |   |   +-- loglinear.py          # 对数线性模型
|   |   |   +-- probit.py             # Probit 分析
|   |   +-- causal/                   # 因果推断
|   |   |   +-- __init__.py
|   |   |   +-- psm.py                # 倾向得分匹配
|   |   |   +-- did.py                # 双重差分
|   |   |   +-- iv.py                 # 工具变量法
|   |   |   +-- rdd.py                # 断点回归
|   |   |   +-- quantile_reg.py       # 分位数回归
|   |   +-- ml/                       # 机器学习
|   |   |   +-- __init__.py
|   |   |   +-- regularization.py     # Lasso/岭回归/弹性网
|   |   |   +-- random_forest.py      # 随机森林
|   |   |   +-- svm.py                # 支持向量机
|   |   |   +-- gbt.py                # 梯度提升树
|   |   |   +-- neural_network.py     # 神经网络
|   |   |   +-- bayesian_network.py   # 贝叶斯网络
|   |   +-- text/                     # 文本分析
|   |   |   +-- __init__.py
|   |   |   +-- mining.py             # 文本挖掘
|   |   |   +-- sentiment.py          # 情感分析
|   |   |   +-- wordcloud.py          # 词云生成
|   |   +-- spatial/                  # 空间分析
|   |   |   +-- __init__.py
|   |   |   +-- spatial_econ.py       # 空间计量
|   |   |   +-- network.py            # 网络分析
|   |   +-- multilevel/               # 多层模型
|   |   |   +-- __init__.py
|   |   |   +-- hlm.py                # 多层线性模型
|   |   |   +-- bayesian_hlm.py       # 贝叶斯分层模型
|   |   +-- bayesian_advanced/        # 高级贝叶斯
|   |   |   +-- __init__.py
|   |   |   +-- bayesian_factor.py    # 贝叶斯因子分析
|   |   |   +-- bayesian_cluster.py   # 贝叶斯聚类
|   |   |   +-- bayesian_survival.py  # 贝叶斯生存分析
|   |   |   +-- bayesian_logistic.py  # 贝叶斯 Logistic 回归
|   |   +-- tests/                    # 假设检验
|   |   |   +-- __init__.py
|   |   |   +-- normality.py          # 正态性检验
|   |   |   +-- hypothesis.py         # 通用假设检验框架
|   |
|   +-- gui/                          # GUI 层
|   |   +-- __init__.py
|   |   +-- main_window.py            # 主窗口
|   |   +-- frameless_window.py       # 无边框窗口基类
|   |   +-- title_bar.py              # 自定义标题栏
|   |   +-- splash_screen.py          # 启动页面
|   |   +-- menubar.py                # 顶部菜单栏
|   |   +-- toolbar.py                # 工具栏
|   |   +-- statusbar.py              # 状态栏
|   |   +-- sidebar.py                # 侧边栏分析菜单
|   |   +-- tabs/                     # 标签页系统
|   |   |   +-- __init__.py
|   |   |   +-- tab_widget.py         # 标签页管理器
|   |   |   +-- data_editor_tab.py    # 数据编辑器标签页
|   |   |   +-- variable_view_tab.py  # 变量视图标签页
|   |   |   +-- output_tab.py         # 输出查看器标签页
|   |   |   +-- syntax_tab.py         # 语法编辑器标签页
|   |   +-- widgets/                  # 自定义控件
|   |   |   +-- __init__.py
|   |   |   +-- data_table.py         # 数据表格控件
|   |   |   +-- variable_table.py     # 变量属性表格
|   |   |   +-- output_tree.py        # 输出导航树
|   |   |   +-- output_viewer.py      # 输出内容查看器
|   |   |   +-- arco_button.py        # Arco 风格按钮
|   |   |   +-- arco_input.py         # Arco 风格输入框
|   |   |   +-- arco_combo.py         # Arco 风格下拉框
|   |   |   +-- arco_dialog.py        # Arco 风格对话框
|   |   |   +-- arco_messagebox.py    # Arco 风格消息框
|   |   |   +-- arco_tabs.py          # Arco 风格标签页
|   |   |   +-- arco_tree.py          # Arco 风格树控件
|   |   |   +-- arco_splitter.py      # Arco 风格分割器
|   |   |   +-- arco_scrollbar.py     # Arco 风格滚动条
|   |   |   +-- arco_tooltip.py       # Arco 风格提示
|   |   |   +-- arco_progress.py      # Arco 风格进度条
|   |   |   +-- variable_selector.py  # 变量选择器（分析对话框核心组件）
|   |   |   +-- variable_list.py      # 变量列表框
|   |   |   +-- transfer_button.py    # 变量移动按钮组
|   |   +-- dialogs/                  # 分析对话框
|   |   |   +-- __init__.py
|   |   |   +-- dialog_base.py        # 对话框基类
|   |   |   +-- descriptives_dialog.py
|   |   |   +-- frequencies_dialog.py
|   |   |   +-- crosstabs_dialog.py
|   |   |   +-- ttest_one_dialog.py
|   |   |   +-- ttest_independent_dialog.py
|   |   |   +-- ttest_paired_dialog.py
|   |   |   +-- oneway_anova_dialog.py
|   |   |   +-- correlation_dialog.py
|   |   |   +-- regression_dialog.py
|   |   |   +-- factor_dialog.py
|   |   |   +-- cluster_dialog.py
|   |   |   +-- reliability_dialog.py
|   |   |   +-- survival_dialog.py
|   |   |   +-- ... (每个分析模块对应一个对话框)
|   |   +-- settings/                 # 设置
|   |   |   +-- __init__.py
|   |   |   +-- settings_dialog.py    # 设置主对话框
|   |   |   +-- general_page.py       # 通用设置页
|   |   |   +-- data_page.py          # 数据设置页
|   |   |   +-- output_page.py        # 输出设置页
|   |   |   +-- chart_page.py         # 图表设置页
|   |   |   +-- performance_page.py   # 性能设置页
|   |   +-- chart/                    # 图表展示与编辑
|   |   |   +-- __init__.py
|   |   |   +-- chart_window.py       # 图表窗口
|   |   |   +-- chart_editor.py       # 图表编辑面板
|   |   |   +-- chart_exporter.py     # 图表导出器
|   |   +-- styles/                   # QSS 样式表
|   |   |   +-- __init__.py
|   |   |   +-- theme_arco.py         # Arco Design 主题管理
|   |   |   +-- global.qss            # 全局样式表
|   |   |   +-- widgets.qss           # 控件样式表
|   |   |   +-- dialogs.qss           # 对话框样式表
|   |   |   +-- output.qss            # 输出查看器样式表
|   |
|   +-- i18n/                         # 国际化 (JSON)
|   |   +-- __init__.py
|   |   +-- i18n_manager.py           # 多语言管理器
|   |   +-- zh_CN/                    # 简体中文
|   |   |   +-- app.json              # 应用级文本
|   |   |   +-- menu.json             # 菜单文本
|   |   |   +-- sidebar.json          # 侧边栏文本
|   |   |   +-- dialogs.json          # 对话框文本
|   |   |   +-- output.json           # 输出文本
|   |   |   +-- settings.json         # 设置文本
|   |   |   +-- errors.json           # 错误提示文本
|   |   |   +-- tooltips.json         # 提示文本
|   |   +-- en_US/                    # 英文
|   |       +-- app.json
|   |       +-- menu.json
|   |       +-- sidebar.json
|   |       +-- dialogs.json
|   |       +-- output.json
|   |       +-- settings.json
|   |       +-- errors.json
|   |       +-- tooltips.json
|   |
|   +-- resources/                    # 资源文件
|   |   +-- icons/                    # 图标 (SVG)
|   |   |   +-- app_icon.svg          # 应用图标
|   |   |   +-- logo.svg              # Logo
|   |   |   +-- menu/                 # 菜单图标
|   |   |   +-- analysis/             # 分析菜单图标
|   |   |   +-- toolbar/              # 工具栏图标
|   |   |   +-- status/               # 状态图标
|   |   +-- fonts/                    # 字体文件
|   |   +-- images/                   # 图片资源
|   |
|   +-- utils/                        # 工具模块
|   |   +-- __init__.py
|   |   +-- file_io.py                # 文件读写 (.axl, .csv, .xlsx, .sav)
|   |   +-- config.py                 # 配置管理
|   |   +-- logger.py                 # 日志系统
|   |   +-- singleton.py              # 单例模式
|   |   +-- signal_bus.py             # 全局信号总线
|   |
|   +-- charting/                     # 图表引擎
|       +-- __init__.py
|       +-- chart_base.py             # 图表基类
|       +-- bar_chart.py              # 条形图/柱状图
|       +-- stacked_bar.py            # 堆叠条形图
|       +-- grouped_bar.py            # 分组条形图
|       +-- pie_chart.py              # 饼图/环图
|       +-- histogram.py              # 直方图
|       +-- density_chart.py          # 密度图
|       +-- scatter_chart.py          # 散点图
|       +-- matrix_scatter.py         # 矩阵散点图
|       +-- scatter_3d.py             # 三维散点图
|       +-- line_chart.py             # 折线图
|       +-- area_chart.py             # 面积图
|       +-- boxplot.py                # 箱线图
|       +-- error_bar.py              # 误差线图
|       +-- pp_plot.py                # P-P 图
|       +-- qq_plot.py                # Q-Q 图
|       +-- stem_leaf.py              # 茎叶图
|       +-- hi_lo.py                  # 高低图
|       +-- pyramid.py                # 人口金字塔
|       +-- roc_curve.py              # ROC 曲线
|       +-- interaction_plot.py       # 交互作用图
|       +-- profile_plot.py           # 轮廓图
|       +-- heatmap.py                # 热图
|       +-- dot_plot.py               # 点图
|       +-- acf_plot.py               # 自相关图
|       +-- pacf_plot.py              # 偏自相关图
|       +-- sequence_plot.py          # 序列图
|       +-- periodogram.py            # 周期图
|       +-- category_plot.py          # 分类图
|       +-- correspondence_plot.py    # 对应分析图
|       +-- dendrogram.py             # 树状图
|       +-- icicle_plot.py            # 冰挂图
|       +-- pareto_chart.py           # 帕累托图
|       +-- heatmap_map.py            # 热力地图
|       +-- geo_plot.py               # 空间地理分布图
|       +-- network_plot.py           # 网络图
|       +-- chord_diagram.py          # 和弦图
|       +-- sankey_diagram.py         # 桑基图
|       +-- sunburst.py               # 旭日图
|       +-- treemap.py                # 树图
|       +-- radar_chart.py            # 雷达图
|       +-- surface_3d.py             # 3D 曲面图
|       +-- violin_plot.py            # 小提琴图
|       +-- ridge_plot.py             # 山脊图
|       +-- grouped_density.py        # 分组密度图
|       +-- survival_curve.py         # 生存曲线
|       +-- wordcloud_chart.py        # 词云图
|       +-- multi_panel.py            # 多面板组合图
|
+-- tests/                            # 测试
|   +-- __init__.py
|   +-- test_core/                    # 核心引擎测试
|   |   +-- test_descriptive.py
|   |   +-- test_ttest.py
|   |   +-- test_anova.py
|   |   +-- test_regression.py
|   |   +-- ...
|   +-- test_gui/                     # GUI 测试
|   |   +-- test_main_window.py
|   |   +-- test_data_table.py
|   |   +-- ...
|
+-- docs/                             # 文档
|   +-- architecture.md
|   +-- api_reference.md
|   +-- user_guide.md
|
+-- build/                            # 构建脚本
|   +-- build_windows.py              # Windows 打包脚本
|   +-- setup.py                      # 安装配置
|   +-- AxaltyX.iss                   # Inno Setup 脚本
|   +-- requirements.txt              # Python 依赖
|
+-- README.md
+-- LICENSE
```

---

## 第四部分: i18n JSON 文本规范

### 4.1 设计原则

- **所有用户可见文本必须存储在 JSON 文件中**，禁止在 Python 代码中硬编码任何文字
- JSON 文件按功能模块拆分，便于维护
- 使用嵌套 key 结构，支持命名空间
- 占位符使用 `{variable}` 格式

### 4.2 JSON 文件示例

**zh_CN/app.json**:
```json
{
  "app_name": "AxaltyX",
  "version": "1.0.0",
  "copyright": "Copyright TBJ114. All rights reserved.",
  "splash_loading": "正在加载...",
  "splash_init": "正在初始化...",
  "splash_ready": "准备就绪",
  "untitled": "未命名",
  "file_filter": "AxaltyX 文件 (*.axl);;CSV 文件 (*.csv);;Excel 文件 (*.xlsx);;SPSS 文件 (*.sav);;所有文件 (*.*)",
  "confirm_save": "文件已修改，是否保存?",
  "confirm_close": "确定要关闭当前文件吗?",
  "save_success": "保存成功",
  "save_failed": "保存失败: {error}",
  "open_success": "已加载 {rows} 行 {cols} 列数据",
  "open_failed": "打开失败: {error}",
  "no_data": "当前没有打开的数据文件",
  "analysis_running": "正在执行分析...",
  "analysis_complete": "分析完成",
  "analysis_failed": "分析失败: {error}"
}
```

**zh_CN/menu.json**:
```json
{
  "file": "文件",
  "edit": "编辑",
  "view": "视图",
  "data": "数据",
  "transform": "转换",
  "analyze": "分析",
  "graphs": "图表",
  "utilities": "实用程序",
  "window": "窗口",
  "help": "帮助",
  "file_new": "新建",
  "file_open": "打开...",
  "file_save": "保存",
  "file_save_as": "另存为...",
  "file_close": "关闭",
  "file_exit": "退出",
  "edit_undo": "撤销",
  "edit_redo": "重做",
  "edit_cut": "剪切",
  "edit_copy": "复制",
  "edit_paste": "粘贴",
  "edit_clear": "清除",
  "edit_find": "查找...",
  "edit_replace": "替换...",
  "view_data_editor": "数据编辑器",
  "view_variable_view": "变量视图",
  "view_output": "输出查看器",
  "view_syntax": "语法编辑器",
  "data_define_variables": "定义变量",
  "data_sort_cases": "排序个案",
  "data_select_cases": "选择个案",
  "data_weight_cases": "加权个案",
  "data_transpose": "转置",
  "data_restructure": "重构",
  "data_merge_files": "合并文件",
  "data_split_file": "拆分文件",
  "analyze_descriptives": "描述性统计",
  "analyze_frequencies": "频数分析",
  "analyze_crosstabs": "交叉表",
  "help_about": "关于 AxaltyX",
  "help_documentation": "文档"
}
```

**zh_CN/sidebar.json**:
```json
{
  "analysis": "分析",
  "statistical_summary": "统计摘要",
  "frequencies": "频数分析",
  "descriptives": "描述性统计",
  "explore": "探索分析",
  "compare_means": "比较均值",
  "means": "均值",
  "one_sample_t": "单样本 T 检验",
  "independent_t": "独立样本 T 检验",
  "paired_t": "配对样本 T 检验",
  "general_linear_model": "一般线性模型",
  "one_way_anova": "单因素方差分析",
  "manova": "多因素方差分析",
  "ancova": "协方差分析",
  "repeated_measures": "重复测量方差分析",
  "nonparametric": "非参数检验",
  "chi_square": "卡方检验",
  "binomial": "二项检验",
  "runs_test": "游程检验",
  "kolmogorov_smirnov": "单样本 K-S 检验",
  "two_independent_samples": "两个独立样本检验",
  "k_independent_samples": "多个独立样本检验",
  "two_related_samples": "两个相关样本检验",
  "k_related_samples": "多个相关样本检验",
  "correlation": "相关分析",
  "bivariate": "双变量相关",
  "partial": "偏相关",
  "regression": "回归分析",
  "linear": "线性回归",
  "multiple_linear": "多元线性回归",
  "logistic": "Logistic 回归",
  "ordinal": "有序回归",
  "nonlinear": "非线性回归",
  "curve_estimation": "曲线估计",
  "classification": "分类",
  "factor_analysis": "因子分析",
  "principal_components": "主成分分析",
  "cluster": "聚类分析",
  "discriminant": "判别分析",
  "correspondence": "对应分析",
  "scale": "尺度分析",
  "reliability": "信度分析",
  "validity": "效度分析",
  "multidimensional_scaling": "多维尺度",
  "survival": "生存分析",
  "kaplan_meier": "Kaplan-Meier",
  "cox_regression": "Cox 回归",
  "advanced": "高级分析",
  "sem": "结构方程模型",
  "bayesian": "贝叶斯统计",
  "meta_analysis": "Meta 分析",
  "time_series": "时间序列分析",
  "log_linear": "对数线性模型",
  "probit": "Probit 分析",
  "causal_inference": "因果推断",
  "psm": "倾向得分匹配",
  "did": "双重差分",
  "instrumental_variables": "工具变量法",
  "rdd": "断点回归",
  "quantile_regression": "分位数回归",
  "machine_learning": "机器学习",
  "regularization": "正则化回归",
  "random_forest": "随机森林",
  "svm": "支持向量机",
  "gradient_boosting": "梯度提升树",
  "neural_network": "神经网络",
  "bayesian_network": "贝叶斯网络",
  "text_analysis": "文本分析",
  "text_mining": "文本挖掘",
  "sentiment": "情感分析",
  "word_cloud": "词云生成",
  "spatial": "空间分析",
  "spatial_econometrics": "空间计量分析",
  "network_analysis": "网络分析",
  "multilevel": "多层模型",
  "hlm": "多层线性模型",
  "bayesian_hierarchical": "贝叶斯分层模型",
  "advanced_bayesian": "高级贝叶斯",
  "bayesian_factor": "贝叶斯因子分析",
  "bayesian_cluster": "贝叶斯聚类",
  "bayesian_survival": "贝叶斯生存分析",
  "bayesian_logistic": "贝叶斯 Logistic 回归"
}
```

**zh_CN/dialogs.json**:
```json
{
  "common": {
    "ok": "确定",
    "cancel": "取消",
    "apply": "应用",
    "paste": "粘贴",
    "reset": "重置",
    "help": "帮助",
    "close": "关闭",
    "variables": "变量",
    "analysis_variables": "分析变量",
    "available_variables": "可用变量",
    "options": "选项",
    "statistics": "统计量",
    "charts": "图表",
    "format": "格式",
    "save": "保存",
    "export": "导出",
    "select_all": "全选",
    "deselect_all": "取消全选"
  },
  "descriptives": {
    "title": "描述性统计",
    "variables_label": "变量",
    "statistics_dialog_title": "描述性统计: 统计量",
    "mean": "均值",
    "std_dev": "标准差",
    "variance": "方差",
    "range": "全距",
    "minimum": "最小值",
    "maximum": "最大值",
    "kurtosis": "峰度",
    "skewness": "偏度",
    "sum": "总和",
    "stderr": "标准误"
  },
  "ttest_one": {
    "title": "单样本 T 检验",
    "test_variable": "检验变量",
    "test_value": "检验值",
    "confidence_interval": "置信区间百分比",
    "missing_values": "缺失值",
    "exclude_analysis": "按分析排除个案",
    "exclude_listwise": "按列表排除个案"
  }
}
```

**zh_CN/output.json**:
```json
{
  "output_viewer": "输出查看器",
  "log": "日志",
  "warnings": "警告",
  "notes": "注释",
  "title": "标题",
  "tables": "表格",
  "charts": "图表",
  "text_output": "文本输出",
  "descriptive_statistics": "描述性统计量",
  "n": "N",
  "mean": "均值",
  "std_deviation": "标准差",
  "variance": "方差",
  "skewness": "偏度",
  "kurtosis": "峰度",
  "minimum": "最小值",
  "maximum": "最大值",
  "percentiles": "百分位数",
  "valid": "有效",
  "missing": "缺失",
  "total": "总计",
  "df": "自由度",
  "sig": "显著性",
  "t_value": "t 值",
  "f_value": "F 值",
  "chi_square": "卡方值",
  "p_value": "p 值",
  "confidence_interval": "置信区间",
  "lower_bound": "下限",
  "upper_bound": "上限",
  "std_error": "标准误",
  "correlation": "相关系数",
  "r_squared": "R 方",
  "adjusted_r_squared": "调整后 R 方",
  "regression_coefficient": "回归系数",
  "standardized_coefficient": "标准化系数"
}
```

### 4.3 i18n 管理器接口设计

```python
# i18n/i18n_manager.py (伪代码，仅描述接口)
class I18nManager:
    """多语言管理器 - 单例模式"""

    def __init__(self):
        self._lang = "zh_CN"
        self._cache = {}

    def set_language(self, lang: str) -> None: ...

    def t(self, key: str, **kwargs) -> str:
        """翻译函数，例如: t('app.save_success') -> '保存成功'"""
        ...

    def get_language(self) -> str: ...
```

---

## 第五部分: 分步实施计划

### 阶段 0: 项目初始化

#### 步骤 0.1: 创建项目骨架

**目标**: 建立完整的目录结构和基础文件

**生成文件**:
- `AxaltyX/` 根目录及所有子目录（按第三部分结构）
- `axaltyx/__init__.py`
- `axaltyx/main.py` (最小入口，仅打印版本号)
- `axaltyx/app.py` (QApplication 最小初始化)
- `build/requirements.txt`
- `build/setup.py`
- `README.md`
- `LICENSE`

**验证**: `python -m axaltyx.main` 能正常运行并打印版本信息

#### 步骤 0.2: 配置开发环境与依赖

**目标**: 安装所有依赖并验证

**requirements.txt 内容**:
```
PyQt6>=6.5.0
numpy>=1.24.0
pandas>=2.0.0
scipy>=1.10.0
statsmodels>=0.14.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.15.0
networkx>=3.1.0
lifelines>=0.27.0
pymc>=5.0.0
openpyxl>=3.1.0
pyreadstat>=1.2.0
nltk>=3.8.0
jieba>=0.42.1
wordcloud>=1.9.0
pyqtgraph>=0.13.0
pyinstaller>=6.0.0
```

**验证**: `pip install -r requirements.txt` 无报错

#### 步骤 0.3: 创建 i18n 基础设施

**目标**: 实现多语言管理器和所有 JSON 文件

**生成文件**:
- `axaltyx/i18n/__init__.py`
- `axaltyx/i18n/i18n_manager.py`
- `axaltyx/i18n/zh_CN/` 下所有 JSON 文件
- `axaltyx/i18n/en_US/` 下所有 JSON 文件

**验证**:
```python
from axaltyx.i18n import I18nManager
mgr = I18nManager()
mgr.set_language("zh_CN")
assert mgr.t("app.app_name") == "AxaltyX"
assert mgr.t("menu.file") == "文件"
mgr.set_language("en_US")
assert mgr.t("menu.file") == "File"
```

---

### 阶段 1: GUI 基础框架

#### 步骤 1.1: 无边框窗口基类

**目标**: 实现可拖拽、可调整大小的无边框窗口

**生成文件**:
- `axaltyx/gui/frameless_window.py`
- `axaltyx/gui/title_bar.py`

**功能**:
- 无边框窗口 `FramelessWindow(QWidget)`
- 自定义标题栏 `TitleBar(QWidget)`: Logo + 标题 + 最小化/最大化/关闭按钮
- 拖拽移动: 鼠标按下标题栏时移动窗口
- 调整大小: 鼠标在窗口边缘时显示调整光标并允许调整
- 最小化/最大化/关闭按钮功能
- 关闭按钮 Hover 红色背景

**验证**:
- 创建一个 `FramelessWindow` 子类，显示一个空白窗口
- 窗口可拖拽移动
- 窗口可调整大小
- 最小化/最大化/关闭按钮正常工作
- 关闭按钮 Hover 显示红色

#### 步骤 1.2: 启动页面

**目标**: 实现品牌化的启动页面

**生成文件**:
- `axaltyx/gui/splash_screen.py`
- `axaltyx/resources/icons/logo.svg`
- `axaltyx/resources/icons/app_icon.svg`

**功能**:
- 居中显示 600x400 启动窗口
- Logo (SVG) + "AxaltyX" 产品名 + 版本号
- 加载进度条（Arco Blue 渐变）
- 版权文字
- 无边框，无阴影
- 支持通过信号更新进度

**验证**:
- 启动时显示 Splash Screen
- 进度条从 0% 到 100% 动画
- 1.5 秒后自动关闭并显示主窗口

#### 步骤 1.3: Arco Design QSS 主题系统

**目标**: 建立完整的 QSS 样式表系统

**生成文件**:
- `axaltyx/gui/styles/theme_arco.py`
- `axaltyx/gui/styles/global.qss`
- `axaltyx/gui/styles/widgets.qss`

**功能**:
- 定义所有 Arco Design 色彩变量（通过 QSS 变量或 Python 常量）
- 全局样式: 背景、字体、间距
- 按钮样式: Primary/Secondary/Outline/Text，4 种尺寸
- 输入框样式: 聚焦边框、禁用态
- 下拉框样式
- 滚动条样式: 细滚动条 4px
- 分割线样式

**验证**:
- 创建测试窗口，包含各种控件
- 控件样式符合 Arco Design 规范
- 按钮 Hover/Active 状态正确

#### 步骤 1.4: 主窗口骨架

**目标**: 实现主窗口的 "T" 型布局

**生成文件**:
- `axaltyx/gui/main_window.py`
- `axaltyx/gui/menubar.py`
- `axaltyx/gui/toolbar.py`
- `axaltyx/gui/statusbar.py`
- `axaltyx/gui/sidebar.py`

**功能**:
- 继承 `FramelessWindow`
- 顶部菜单栏: 文件、编辑、视图、数据、转换、分析、图表、实用程序、窗口、帮助
- 工具栏: 新建、打开、保存、撤销、重做、复制、粘贴、运行
- 左侧侧边栏: 分析菜单树（占位，后续填充）
- 中央区域: 标签页容器（占位）
- 底部状态栏: 就绪、行列信息
- 所有文本通过 i18n 获取

**验证**:
- 主窗口正常显示，布局正确
- 菜单栏显示所有菜单项（文本来自 JSON）
- 工具栏按钮可点击
- 侧边栏占位显示
- 状态栏显示 "就绪"
- 窗口可拖拽、可调整大小

---

### 阶段 2: 数据编辑器

#### 步骤 2.1: 数据表格控件

**目标**: 实现 SPSS 风格的数据表格

**生成文件**:
- `axaltyx/gui/widgets/data_table.py`
- `axaltyx/core/data/dataset.py`
- `axaltyx/core/data/variable.py`

**功能**:
- 使用 `QTableView` + 自定义 `QAbstractTableModel`
- 默认 100 行 x 100 列
- 行号列固定在左侧
- 列头可双击编辑（默认 VAR00001...）
- 单元格选中: 蓝色边框
- 行/列选中: 浅蓝背景
- 网格线: 1px 灰色
- 缺失值显示为 `.`
- 支持滚动、选择、编辑
- 支持键盘导航（Tab、Enter、方向键）

**验证**:
- 空文件显示 100x100 表格
- 列头显示 VAR00001 ~ VAR00100
- 行号显示 1 ~ 100
- 双击列头可编辑列名
- 单元格可编辑
- 选中状态视觉正确

#### 步骤 2.2: 变量视图表格

**目标**: 实现变量属性编辑表格

**生成文件**:
- `axaltyx/gui/widgets/variable_table.py`
- `axaltyx/gui/tabs/variable_view_tab.py`

**功能**:
- 表格列: 名称、类型、宽度、小数位、标签、值标签、缺失值、列宽、对齐、度量、角色
- 类型列: 下拉选择（数值、字符串、日期）
- 对齐列: 下拉选择（左、右、居中）
- 度量列: 下拉选择（度量、有序、名义）
- 值标签/缺失值: 点击弹出编辑对话框
- 与数据视图同步

**验证**:
- 切换到变量视图标签页，显示变量属性表
- 修改变量名后，数据视图列头同步更新
- 修改类型后，数据视图单元格编辑行为变化

#### 步骤 2.3: 标签页系统

**目标**: 实现数据编辑器/变量视图/输出查看器的标签页切换

**生成文件**:
- `axaltyx/gui/tabs/tab_widget.py`
- `axaltyx/gui/tabs/data_editor_tab.py`
- `axaltyx/gui/tabs/output_tab.py`
- `axaltyx/gui/tabs/syntax_tab.py`

**功能**:
- Arco 风格标签页（圆角、选中态蓝色下划线）
- 数据编辑器标签页: 包含数据表格
- 变量视图标签页: 包含变量属性表格
- 输出查看器标签页: 占位（后续实现）
- 语法编辑器标签页: 占位（后续实现）

**验证**:
- 标签页可切换
- 数据编辑器显示 100x100 表格
- 变量视图显示变量属性表

---

### 阶段 3: 文件 I/O

#### 步骤 3.1: 数据集序列化

**目标**: 实现自定义 .axl 文件格式

**生成文件**:
- `axaltyx/utils/file_io.py`
- `axaltyx/core/data/dataset.py` (扩展)

**功能**:
- 保存: 数据 + 变量属性 -> JSON 压缩 (.axl)
- 加载: .axl -> 数据集对象
- 新建: 创建空数据集（100x100）
- 最近文件列表

**验证**:
- 新建文件 -> 输入数据 -> 保存 -> 关闭 -> 打开 -> 数据完整
- .axl 文件可被正确解析

#### 步骤 3.2: 外部格式支持

**目标**: 支持 CSV、Excel、SPSS(.sav) 导入导出

**生成文件**:
- `axaltyx/utils/file_io.py` (扩展)

**功能**:
- CSV 导入/导出（编码自动检测）
- Excel 导入/导出（openpyxl）
- SPSS .sav 导入（pyreadstat）
- 文件对话框过滤器

**验证**:
- 导入 CSV 文件，数据正确显示
- 导入 Excel 文件，数据正确显示
- 导入 SPSS .sav 文件，变量属性正确加载
- 导出为 CSV/Excel，外部软件可正确打开

---

### 阶段 4: 侧边栏与分析对话框框架

#### 步骤 4.1: 侧边栏分析菜单树

**目标**: 实现完整的分析菜单树

**生成文件**:
- `axaltyx/gui/sidebar.py` (完善)
- `axaltyx/gui/widgets/arco_tree.py`

**功能**:
- 树形菜单，按第二部分 2.5 节结构
- 一级菜单带图标
- 展开/折叠动画
- 选中态: 蓝色背景 + 左侧指示条
- 可折叠至仅图标模式
- 所有文本来自 i18n JSON

**验证**:
- 所有菜单项正确显示
- 展开/折叠正常
- 点击菜单项触发信号（后续连接对话框）

#### 步骤 4.2: 对话框基类与变量选择器

**目标**: 实现分析对话框的通用组件

**生成文件**:
- `axaltyx/gui/dialogs/dialog_base.py`
- `axaltyx/gui/widgets/variable_selector.py`
- `axaltyx/gui/widgets/variable_list.py`
- `axaltyx/gui/widgets/transfer_button.py`
- `axaltyx/gui/widgets/arco_dialog.py`

**功能**:
- `DialogBase(QDialog)`: 标准分析对话框模板
  - 标题栏 + 关闭按钮
  - 底部按钮栏: 粘贴、重置、确定、取消
  - 标准尺寸: 520x480
- `VariableSelector(QWidget)`: 变量选择器组合
  - 左侧: 可用变量列表
  - 中间: 移动按钮组 (>> << > <)
  - 右侧: 已选变量列表
- `VariableList(QListWidget)`: 变量列表框
  - 显示变量名 + 类型图标
  - 支持多选
  - 支持拖拽排序

**验证**:
- 创建测试对话框，包含变量选择器
- 变量可在两个列表间移动
- 确定按钮返回选中变量列表
- 取消按钮关闭对话框

#### 步骤 4.3: 描述性统计对话框 (第一个完整对话框)

**目标**: 实现第一个完整的分析对话框

**生成文件**:
- `axaltyx/gui/dialogs/descriptives_dialog.py`
- `axaltyx/core/descriptive/descriptives.py`

**功能**:
- 变量选择器
- 统计量选项: 均值、标准差、方差、全距、最小值、最大值、峰度、偏度、标准误
- 图表选项: 直方图、茎叶图
- 确定后执行分析并输出结果

**验证**:
- 打开描述性统计对话框
- 选择变量，勾选统计量
- 点击确定，输出查看器显示结果表格

---

### 阶段 5: 输出查看器

#### 步骤 5.1: 输出导航树

**目标**: 实现输出结果的树形导航

**生成文件**:
- `axaltyx/gui/widgets/output_tree.py`

**功能**:
- 树形结构: 日志、标题、表格、图表等分类
- 点击节点跳转到对应输出内容
- 支持删除、导出单个输出项

**验证**:
- 执行分析后，输出树新增节点
- 点击节点，右侧内容区跳转

#### 步骤 5.2: 输出内容查看器

**目标**: 实现富文本输出内容展示

**生成文件**:
- `axaltyx/gui/widgets/output_viewer.py`
- `axaltyx/gui/tabs/output_tab.py` (完善)

**功能**:
- 使用 QTextBrowser 渲染 HTML
- 表格渲染: 交替行背景、边框
- 文本日志渲染
- 嵌入图表（matplotlib 渲染为图片）
- 右键菜单: 复制、导出 HTML/PDF/PNG
- 与输出树联动

**验证**:
- 描述性统计结果以表格形式显示
- 表格样式正确（交替行、边框）
- 可复制表格内容
- 可导出为 HTML

---

### 阶段 6: 核心统计引擎（按优先级）

#### 步骤 6.1: 描述性统计与频数分析

**生成文件**:
- `axaltyx/core/descriptive/descriptives.py` (完善)
- `axaltyx/core/descriptive/frequencies.py`
- `axaltyx/core/descriptive/crosstabs.py`

**验证**: 与 SPSS 输出对比，数值精度一致（小数点后 4 位）

#### 步骤 6.2: T 检验系列

**生成文件**:
- `axaltyx/core/means/ttest_one.py`
- `axaltyx/core/means/ttest_independent.py`
- `axaltyx/core/means/ttest_paired.py`

**验证**: 与 scipy 结果交叉验证

#### 步骤 6.3: 方差分析系列

**生成文件**:
- `axaltyx/core/anova/oneway.py`
- `axaltyx/core/anova/manova.py`
- `axaltyx/core/anova/ancova.py`
- `axaltyx/core/anova/rm_anova.py`

**验证**: 标准数据集测试

#### 步骤 6.4: 相关与回归

**生成文件**:
- `axaltyx/core/correlation/bivariate.py`
- `axaltyx/core/correlation/partial.py`
- `axaltyx/core/regression/linear.py`
- `axaltyx/core/regression/multiple.py`
- `axaltyx/core/regression/logistic.py`

**验证**: 与 statsmodels 结果交叉验证

#### 步骤 6.5: 非参数检验

**生成文件**:
- `axaltyx/core/nonparametric/` 下所有文件

**验证**: 标准非参数检验数据集

#### 步骤 6.6: 高级分析模块

按以下顺序逐步实现:
1. 因子分析 / 主成分分析
2. 聚类分析 / 判别分析
3. 信度效度分析
4. 生存分析
5. 时间序列分析
6. 结构方程模型
7. Meta 分析
8. 因果推断系列
9. 机器学习系列
10. 贝叶斯系列
11. 文本分析
12. 空间分析
13. 多层模型

---

### 阶段 7: 图表引擎

#### 步骤 7.1: 图表基类与基础图表

**生成文件**:
- `axaltyx/charting/chart_base.py`
- `axaltyx/charting/bar_chart.py`
- `axaltyx/charting/line_chart.py`
- `axaltyx/charting/scatter_chart.py`
- `axaltyx/charting/histogram.py`
- `axaltyx/charting/boxplot.py`
- `axaltyx/charting/pie_chart.py`

**功能**:
- 基于 matplotlib 的图表渲染
- Arco Design 配色方案
- 图表嵌入输出查看器
- 图表独立窗口展示
- 导出 PNG/SVG/PDF

**验证**: 生成各种基础图表，样式符合 Arco Design

#### 步骤 7.2: 统计专用图表

**生成文件**:
- `axaltyx/charting/` 下所有统计图表文件

**验证**: 每种图表生成正确

#### 步骤 7.3: 高级图表与交互

**生成文件**:
- `axaltyx/charting/heatmap.py`
- `axaltyx/charting/network_plot.py`
- `axaltyx/charting/sankey_diagram.py`
- `axaltyx/charting/wordcloud_chart.py`
- `axaltyx/charting/multi_panel.py`
- `axaltyx/gui/chart/chart_window.py`
- `axaltyx/gui/chart/chart_editor.py`

**功能**:
- 图表编辑面板
- 交互式图表（缩放、平移、悬浮提示）
- 多面板组合图

**验证**: 图表可编辑、可交互

---

### 阶段 8: 完善对话框与菜单功能

#### 步骤 8.1: 完成所有分析对话框

**生成文件**: `axaltyx/gui/dialogs/` 下所有对话框文件

**验证**: 每个对话框可打开、选择变量、执行分析、输出结果

#### 步骤 8.2: 菜单功能实现

**功能**:
- 文件菜单: 新建、打开、保存、另存为、关闭、退出
- 编辑菜单: 撤销、重做、剪切、复制、粘贴、查找、替换
- 数据菜单: 定义变量、排序、选择个案、加权、转置、重构、合并、拆分
- 视图菜单: 切换面板显示/隐藏
- 帮助菜单: 关于对话框

**验证**: 所有菜单项功能正常

#### 步骤 8.3: 设置对话框

**生成文件**:
- `axaltyx/gui/settings/settings_dialog.py`
- `axaltyx/gui/settings/general_page.py`
- `axaltyx/gui/settings/data_page.py`
- `axaltyx/gui/settings/output_page.py`
- `axaltyx/gui/settings/chart_page.py`
- `axaltyx/gui/settings/performance_page.py`

**验证**: 修改设置后重启应用，设置生效

---

### 阶段 9: 打包与分发

#### 步骤 9.1: PyInstaller 打包

**生成文件**:
- `build/build_windows.py`
- `build/AxaltyX.spec` (PyInstaller spec 文件)

**功能**:
- 打包为单个 .exe 或目录模式
- 包含所有依赖
- 包含图标、资源文件
- 包含 i18n JSON 文件

**验证**: 在干净的 Windows 11 机器上运行打包后的程序

#### 步骤 9.2: Inno Setup 安装包

**生成文件**:
- `build/AxaltyX.iss`

**功能**:
- 安装向导（Arco Design 风格）
- 选择安装路径
- 创建桌面快捷方式
- 创建开始菜单项
- 文件关联 (.axl)
- 卸载功能

**验证**: 安装、运行、卸载流程完整

---

## 第六部分: 技术要点与约束

### 6.1 编码规范

1. **禁止在 Python 代码中硬编码任何用户可见文本**，所有文本必须通过 `i18n_manager.t("key")` 获取
2. **模块化**: 每个分析模块独立文件，独立可测试
3. **信号槽通信**: GUI 组件之间通过 Qt 信号槽通信，禁止直接调用
4. **单例模式**: I18nManager、Config、SignalBus 使用单例
5. **类型注解**: 所有函数必须有类型注解
6. **文档字符串**: 所有公共类和方法必须有 docstring

### 6.2 性能要求

- 数据加载: 100 万行 x 100 列 < 3 秒
- 描述性统计: 100 万行 < 1 秒
- 表格滚动: 60fps 流畅
- 内存占用: 空载 < 200MB

### 6.3 Qt6 特定注意事项 (Windows 11)

- 使用 `PyQt6` 或 `PySide6`
- 无边框窗口需处理 `WM_NCHITTEST` 消息实现拖拽和调整大小
- DPI 缩放: 启用高 DPI 支持 `QApplication.setHighDpiScaleFactorRoundingPolicy()`
- Windows 11 圆角窗口: 可选使用 `DWM` API 实现系统级圆角
- 任务栏集成: 正确设置窗口图标和 AppUserModelID

### 6.4 数据文件格式 (.axl)

```
.axl 文件结构:
+-------------------+
| Magic: "AXL" (3B) |
| Version: 1 (1B)   |
| Compressed JSON   |
| (zlib)            |
| - metadata        |
| - variables       |
| - data            |
+-------------------+
```

---

## 第七部分: 验证检查清单

### 7.1 GUI 验证

- [ ] 启动页面正常显示，进度条动画流畅
- [ ] 主窗口无边框，可拖拽，可调整大小
- [ ] 标题栏按钮（最小化/最大化/关闭）功能正常
- [ ] 关闭按钮 Hover 显示红色
- [ ] 菜单栏所有项文本来自 JSON，无硬编码
- [ ] 工具栏按钮可点击
- [ ] 侧边栏菜单树展开/折叠正常
- [ ] 侧边栏可折叠至图标模式
- [ ] 标签页切换正常
- [ ] 数据编辑器显示 100x100 空表格
- [ ] 列头可双击编辑
- [ ] 变量视图表格显示正确
- [ ] 状态栏信息正确更新

### 7.2 功能验证

- [ ] 新建/打开/保存/另存为文件
- [ ] CSV/Excel/SPSS 文件导入
- [ ] 导出 CSV/Excel/HTML/PDF
- [ ] 描述性统计计算正确
- [ ] T 检验计算正确
- [ ] 方差分析计算正确
- [ ] 回归分析计算正确
- [ ] 图表生成正确
- [ ] 输出查看器显示正确
- [ ] 设置保存和加载正常
- [ ] 中英文切换正常

### 7.3 性能验证

- [ ] 空载内存 < 200MB
- [ ] 100 万行数据加载 < 3 秒
- [ ] 表格滚动流畅 (60fps)
- [ ] 分析执行速度 >= SPSS 3 倍

### 7.4 打包验证

- [ ] PyInstaller 打包成功
- [ ] 安装包安装/卸载正常
- [ ] 干净 Windows 11 环境可运行
- [ ] 文件关联正常

---

## 第八部分: 关键依赖版本

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | >= 3.10 | 运行时 |
| PyQt6 | >= 6.5.0 | GUI 框架 |
| NumPy | >= 1.24.0 | 数值计算 |
| Pandas | >= 2.0.0 | 数据处理 |
| SciPy | >= 1.10.0 | 科学计算 |
| statsmodels | >= 0.14.0 | 统计模型 |
| scikit-learn | >= 1.3.0 | 机器学习 |
| Matplotlib | >= 3.7.0 | 静态图表 |
| Plotly | >= 5.15.0 | 交互式图表 |
| PyMC | >= 5.0.0 | 贝叶斯统计 |
| lifelines | >= 0.27.0 | 生存分析 |
| PyInstaller | >= 6.0.0 | 打包 |
| Inno Setup | >= 6.2 | 安装包制作 |

---

*本文档为 AxaltyX 项目的完整开发规划，版权所有 TBJ114。*
