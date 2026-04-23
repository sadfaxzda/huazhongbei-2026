# 华中杯 B 题：反射的艺术

## 项目结构

```
mathmodel/
├── src/                    # 源代码目录
│   ├── common/            # 共享模块
│   │   ├── __init__.py
│   │   ├── geometry.py     # 反射映射核心函数
│   │   ├── rendering.py    # 渲染管线
│   │   └── io_utils.py     # 图像读写、参数记录
│   ├── q1/                # Q1 反向光追渲染管线
│   ├── q2/                # Q2 双子问题实现
│   └── q3/                # Q3 兼容性判据算法
├── data/                  # 数据目录
│   ├── raw/              # 原始输入图像
│   ├── reference/        # 题目给的参考图（蒙娜丽莎、小猫）
│   └── processed/        # 处理后的中间数据
├── outputs/               # 输出目录
│   ├── renders/          # 渲染结果（全部 gitignore）
│   └── figures/          # 论文用图
│       ├── final/        # 最终论文用图（提交 Git）
│       └── draft/        # 草稿图（gitignore）
├── notebooks/             # Jupyter notebooks 用于实验
├── scripts/               # 一次性脚本
├── docs/                  # 文档
│   ├── symbols.md       # 符号表
│   ├── geometry.md      # 反射几何推导
│   └── references.md    # 文献列表
├── comp/                  # 比赛官方文件
│   ├── B题：反射的艺术.pdf
│   ├── “华中杯”大学生数学建模挑战赛承诺书.pdf
│   └── 作品提交说明.pdf
├── experiments.md         # 实验记录
├── SOP.md                 # 作战计划
├── environment.yml        # Conda 环境配置
└── README.md              # 本文件
```

## 快速开始

### 环境配置

```bash
# 创建 Conda 环境
conda env create -f environment.yml

# 激活环境
conda activate huazhongbei-b
```

## 分工

- **A**: 建模核心 + 数学主笔
- **B**: 代码主力 + 可视化
- **C**: 论文主笔 + 视觉设计

## 开发规范

### 代码命名

符号,含义,单位
R,圆柱体底面半径,cm
H,圆柱体高度,cm
"LA4​,WA4​",A4 纸张的长度与宽度,cm
"E(xe​,ye​,ze​)",观测点（人眼）在空间直角坐标系下的位置,cm
"Lp​,Wp​",镜面图像在圆柱侧面展开后的物理长度与宽度,cm
θ,镜面图像在圆柱体侧面所占的圆心角张角,rad
"[zmin​,zmax​]",镜面图像在圆柱体垂直方向上的高度区间,cm
a,单个像点（像素）的物理尺寸步长,cm
"m,n","像点矩阵的行数与列数，满足 m=Lp​/a,n=Wp​/a",-
Sm×n​,镜面图像像点矩阵（存储色彩或灰度信息）,-
"M(xmn​,ymn​,zmn​)","镜面上第 (m,n) 个像点的空间坐标",cm
"P(xmn′​,ymn′​,zmn′​)",纸面上对应像点的投影坐标（其中 zmn′​=0）,cm
- 渲染图：`{q}_{description}_R{R值}_H{H值}_E{Ey}_v{N}.{ext}`
- 示例：`q1_mona_lisa_R30_H80_E200_v1.png`
  - R: 镜面半径 (mm)
  - H: 镜面高度 (mm)
  - E: 观察者距离 (y坐标, mm)

### Git 提交
- 提交信息格式：`[Qx][类型] 简短描述`
- 类型：
  - feat: 新功能
  - fix: 修 bug
  - docs: 文档
  - render: 生成新渲染图
  - exp: 实验记录
- 示例：
  - `[Q1][feat] 实现反向光追核心函数`
  - `[Q1][render] 蒙娜丽莎 v3，参数 R40H100`
  - `[Q3][docs] 添加兼容性条件数学定义`
