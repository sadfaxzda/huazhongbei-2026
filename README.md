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
├── docs/                      # 文档
│   ├── symbols.md             # 全局符号表（v3）
│   ├── geometry.md            # 2.4 节：反射几何映射模型推导
│   ├── coordinate_choice.md   # 2.3 节：坐标系选择与对比
│   ├── pixel grid.md          # 3.2–3.3 节：镜面参数化与像素网格
│   ├── define R,H,Position.md # 3.5–3.6 节：圆柱参数确定算法
│   ├── references.md          # 文献列表
│   └── temp/                  # 论文工作目录
│       ├── paper.tex          # LaTeX 主文件（整合所有数学内容）
│       ├── paper.pdf          # 编译输出（预览用）
│       └── paper-outline.md   # 论文大纲
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

