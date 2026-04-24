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
### 反射的艺术数学模型主要参数与变量（蒙娜丽莎方案）

#### 1. 参数汇总表

| 类别           | 符号                          | 物理意义                           | 推荐值 / 说明                                      |
|----------------|-------------------------------|------------------------------------|----------------------------------------------------|
| **纸张参数**   | $(x,y,0)$                     | 纸面直角坐标系                     | 原点取纸张左下角（$210\times297\,\text{mm}$）     |
| **圆柱镜参数** | $r$                           | 圆柱镜半径                         | $32\,\text{mm}$                                    |
|                | $(x_0, y_0)$                  | 圆柱轴心坐标                       | $(105, 92)\,\text{mm}$                             |
|                | $H$                           | 圆柱有效高度                       | $165\,\text{mm}$                                   |
|                | $\theta$                      | 方位角范围                         | $[-110^\circ, 110^\circ]$                          |
|                | $h$                           | 高度坐标                           | $[8, 158]\,\text{mm}$                              |
| **观察者参数** | $E=(e_x,e_y,e_z)$             | 观察者眼睛位置                     | $(105, -185, 355)\,\text{mm}$                      |
|                | 关键假设                      | 视线默认经过镜面轴心               | $e_x = x_0$（对称面内）                            |
| **映射变量**   | $\mathbf{N}(\theta)$          | 镜面单位外法向量                   | $(\cos\theta, \sin\theta, 0)^\top$                 |
|                | $\mathbf{V}(\theta,h)$        | 从 $M$ 指向 $E$ 的单位视线向量     | $\dfrac{E-M}{\|E-M\|}$                             |
|                | $\mathbf{D}(\theta,h)$        | 反射定律得到的入射方向向量         | $\mathbf{V}-2(\mathbf{V}\cdot\mathbf{N})\mathbf{N}$ |
|                | $Q(x(\theta,h), y(\theta,h))$ | 纸面对应绘图点                     | $M + t \cdot \mathbf{D}$                           |
| **离散化参数** | $N_\theta, N_h$               | $\theta$和高度方向采样点数         | $2400 \times 500$（建议 $2000\sim4000 \times 400\sim800$） |
|                | 分辨率                        | 输出纸面图像分辨率                 | $200\,\text{dpi}$（约 $1654\times2339$ 像素）      |
|                | 插值方法                      | 散点到规则像素网格的插值方式       | RBF / `griddata`（linear 或 cubic）                |

#### 2. 镜面坐标到纸面坐标的映射关系

$$
\begin{align*}
M(\theta,h) &= 
\begin{pmatrix}
x_0 + r \cos\theta \\
y_0 + r \sin\theta \\
h
\end{pmatrix}, 
&
\mathbf{N}(\theta) &= 
\begin{pmatrix}
\cos\theta \\
\sin\theta \\
0
\end{pmatrix}, \\[10pt]
E &= 
\begin{pmatrix}
105 \\[4pt] -185 \\[4pt] 355
\end{pmatrix}
\quad (\text{mm}), 
&
\mathbf{V}(\theta,h) &= \frac{E - M(\theta,h)}{\|E-M(\theta,h)\|}, \\[10pt]
\mathbf{D}(\theta,h) &= \mathbf{V}(\theta,h) - 2 \big( \mathbf{V}(\theta,h) \cdot \mathbf{N}(\theta) \big) \mathbf{N}(\theta), \\[8pt]
t(\theta,h) &= -\frac{h}{D_z(\theta,h)}, \qquad (t>0 \text{ 且 } D_z < 0), \\[6pt]
Q(\theta,h) &= M(\theta,h) + t(\theta,h) \cdot \mathbf{D}(\theta,h).
\end{align*}
$$

**说明**：
- $M(\theta,h)$ 为圆柱镜面上的采样点；
- $Q(x(\theta,h), y(\theta,h))$ 为通过反射定律反向映射到纸面 $z=0$ 的对应绘图点；
- 实际生成纸面图案时，对 $(\theta, h)$ 进行高密度离散采样后，通过插值得到规则像素图像。

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

