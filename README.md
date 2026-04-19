# AxaltyX 统计分析软件

专业统计分析软件，功能全面超越SPSS，速度更快，支持Windows 10/11桌面离线运行。

## 项目简介

AxaltyX是一款面向科研人员和数据分析工作者的专业统计软件，采用Qt6开发，支持中文和英文多语言界面，具有完整的统计分析和可视化功能。

## 功能特点

### 统计分析
- 描述统计
- 频数分析
- 交叉表与卡方检验
- t检验（单样本、独立样本、配对样本）
- 方差分析（单因素、多因素、协方差、重复测量）
- 非参数检验
- 相关分析、偏相关分析
- 回归分析（线性、Logistic、有序、非线性）
- 因子分析、主成分分析
- 聚类分析、判别分析、对应分析
- 信度效度分析
- 生存分析、Cox回归
- 时间序列分析
- 贝叶斯统计
- 机器学习算法（随机森林、SVM、梯度提升树、神经网络）
- 深度学习模型
- 因果推断（PSM、DID、IV、RDD）
- 空间计量分析
- 多层线性模型（HLM）
- 贝叶斯网络

### 数据可视化
- 条形图、柱状图、堆叠条形图、分组条形图
- 饼图、环图
- 直方图、密度图
- 散点图、矩阵散点图、三维散点图
- 折线图、面积图
- 箱线图、误差线图
- P-P图、Q-Q图
- 茎叶图
- 高低图、人口金字塔
- ROC曲线图
- 交互作用图、轮廓图
- 热图、点图
- 自相关图、偏自相关图
- 序列图、周期图
- 分类图、对应分析图
- 树状图、冰挂图、帕累托图
- 动态交互图表
- 热力地图、空间地理分布图
- 网络图、和弦图、桑基图
- 旭日图、树图
- 雷达图高级定制
- 三维曲面图
- 动态折线图
- 交互式散点图
- 词云图
- 小提琴图、山脊图、分组密度图
- 动态生存曲线、动态ROC曲线
- 热图聚类图
- 复杂布局可视化
- 多面板组合图
- 动态时间序列图
- 交互式箱线图
- 动态相关性网络图

### 数据处理
- 数据录入与管理
- 变量定义与编辑
- 缺失值处理
- 数据重构
- 加权与转置
- 数据导入导出

## 项目结构

```
/workspace/
├── axaltyx/                    # 主项目目录
│   ├── main.py                 # 程序入口
│   ├── requirements.txt        # 依赖包
│   ├── build.py               # 打包脚本
│   ├── README.md              # 项目说明
│   └── app/                   # 应用程序包
│       ├── gui/               # GUI模块
│       │   ├── widgets/       # 自定义控件
│       │   │   ├── custom_title_bar.py    # 自定义标题栏
│       │   │   └── data_editor.py          # 数据编辑器
│       │   ├── styles/        # 样式文件
│       │   │   └── byte_style.qss         # 字节风格样式
│       │   ├── modules/       # 功能模块
│       │   ├── resources/     # 资源文件
│       │   └── main_window.py # 主窗口
│       ├── core/              # 核心功能
│       │   ├── stats/         # 统计分析
│       │   ├── visualization/ # 可视化
│       │   └── io/            # 输入输出
│       ├── locale/            # 多语言配置
│       │   ├── zh_CN.json     # 中文配置
│       │   └── en_US.json     # 英文配置
│       ├── utils/             # 工具函数
│       │   └── locale_manager.py # 语言管理器
│       └── config/            # 配置文件
└── run_axaltyx.py             # 快捷启动脚本
```

## 快速开始

### 环境要求
- Windows 10/11
- Python 3.8 或更高版本

### 安装依赖

在项目根目录运行：

```bash
pip install -r axaltyx/requirements.txt
```

### 运行程序

方式1：使用快捷启动脚本

```bash
python run_axaltyx.py
```

方式2：直接运行主程序

```bash
cd axaltyx
python main.py
```

### 打包安装

1. 安装PyInstaller

```bash
pip install pyinstaller
```

2. 运行构建脚本

```bash
cd axaltyx
python build.py
```

3. 打包后的可执行文件位于 `axaltyx/dist` 目录

## 多语言支持

AxaltyX支持以下语言：
- 简体中文 (zh_CN)
- English (en_US)

所有界面文本都通过JSON配置文件管理，便于后续添加更多语言支持。

## 设计风格

采用字节跳动（ByteDance）Arco Design设计风格，具有：
- 简洁现代的界面
- 友好的用户交互
- 清晰的视觉层次

## 版权信息

Copyright 2025 TBJ114. All rights reserved.
