# 华中杯 B 题：反射的艺术

## 项目结构

```
mathmodel/
├── src/                    # 源代码目录
│   ├── q1/                # Q1 反向光追渲染管线
│   ├── q2/                # Q2 双子问题实现
│   └── q3/                # Q3 兼容性判据算法
├── data/                  # 数据目录
│   ├── raw/              # 原始输入图像
│   └── processed/        # 处理后的中间数据
├── outputs/               # 输出目录
│   ├── figures/          # 论文用图
│   └── renders/          # 渲染结果
├── notebooks/             # Jupyter notebooks 用于实验
├── docs/                  # 文档
├── SOP.md                 # 作战计划
├── requirements.txt       # Python 依赖
└── README.md              # 本文件
```

## 快速开始

### 环境配置

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

## 分工

- **A**: 建模核心 + 数学主笔
- **B**: 代码主力 + 可视化
- **C**: 论文主笔 + 视觉设计

## 开发规范

### 代码命名
- 渲染图：`{q}_{description}_R{H}_W{H}_v{N}.{ext}`
- 示例：`q1_mona_lisa_R30_H80_v1.png`

### Git 提交
- 提交信息格式：`[Qx] 简短描述`
- 示例：`[Q1] 实现反向光追核心函数`
