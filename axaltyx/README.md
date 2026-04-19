# AxaltyX

专业统计分析软件，功能全面超越SPSS，速度更快，支持Windows 10/11桌面离线运行。

## 功能特性

### 统计分析
- 描述统计
- 频数分析
- 交叉表与卡方检验
- t检验
- 方差分析
- 非参数检验
- 相关分析
- 回归分析
- 因子分析
- 主成分分析
- 聚类分析
- 判别分析
- 生存分析
- 时间序列分析
- 贝叶斯统计
- 机器学习算法
- 空间计量分析
- 多层线性模型
- 因果推断

### 数据可视化
- 条形图、柱状图
- 饼图、环图
- 直方图、密度图
- 散点图
- 折线图、面积图
- 箱线图
- P-P图、Q-Q图
- 人口金字塔
- ROC曲线
- 交互作用图
- 热图
- 三维曲面图
- 动态交互图表
- 词云图
- 小提琴图
- 山脊图

### 数据处理
- 数据录入与管理
- 变量定义与编辑
- 缺失值处理
- 数据重构
- 数据导入导出

## 安装使用

### 环境要求
- Windows 10/11
- Python 3.8+

### 运行方式

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 运行程序
```bash
python main.py
```

### 打包安装

1. 安装PyInstaller
```bash
pip install pyinstaller
```

2. 运行构建脚本
```bash
python build.py
```

3. 打包文件位于 `dist` 目录

## 项目结构

```
axaltyx/
├── main.py                 # 程序入口
├── requirements.txt        # 依赖包
├── build.py               # 打包脚本
├── app/
│   ├── gui/              # GUI模块
│   │   ├── widgets/      # 自定义控件
│   │   ├── styles/       # 样式文件
│   │   └── modules/      # 功能模块
│   ├── core/             # 核心功能
│   │   ├── stats/        # 统计分析
│   │   ├── visualization/ # 可视化
│   │   └── io/           # 输入输出
│   ├── locale/           # 多语言配置
│   ├── utils/            # 工具函数
│   └── config/           # 配置文件
```

## 多语言支持

- 中文 (zh_CN)
- English (en_US)

## 设计风格

采用字节跳动（ByteDance）设计风格，使用Arco Design配色方案。

## 版权

Copyright 2025 TBJ114. All rights reserved.
