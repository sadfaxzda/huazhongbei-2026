<!-- 
修改记录：
- 统一符号系统为全局符号表版本
- 修复 D 符号冲突：原"入射方向向量 D"改为"反射方向向量 r"，D_z 改为 r_z
- 引言观察者符号统一为 E=(D,0,z_E)
- 2.2.2 开头新增对称放置假设声明
- 补充 φ 完整显式表达式，替换原占位符 atan2(y_P, x_P)
- 补充 α(z), β(z) 来源说明（Hunt et al. 2000，详见附录 A.1）
- 2.2.1 末尾新增可见性约束段落（V·n < 0 与 r_z < 0）
- 2.2.4 插值方法统一为 Delaunay 三角剖分线性插值
- 2.2.4 末尾新增 Wu et al. (2022) 引用
- 章节编号 2.2.x 全部改为 2.4.x
- 2.4.1 纸面交点 Q(u,v) → P_paper=(u,v,0)，与符号表 P_paper 统一
-->

# 2.4 圆柱镜面反射的几何映射模型

为系统描述纸面图案与镜面图案之间的关系，本文建立正向映射 $T$ 与逆向映射 $T^{-1}$，并在不同坐标系下给出其数学表达。全局坐标系约定如下：

- **3D 直角坐标系** $(x,y,z)$：用于光线追踪、反射定律推导和向量运算；
- **镜面柱面参数坐标系** $(\theta,z)$：用于镜面离散化与镜面图案 $G(\theta,z)$ 的定义；
- **纸面极坐标系** $(\rho,\phi)$：以圆柱轴心 $(x_0,y_0)$ 为极点，用于变形分析与对称性研究；
- **纸面直角坐标系** $(u,v)$：以 A4 纸左下角为原点，用于最终图像生成与打印输出。

主要符号遵循本文符号表：圆柱半径为 $R$，观察者位置为 $E=(D,0,z_E)$，水平距离为 $D$，镜面高度参数为 $z$，纸面直角坐标为 $(u,v)$，纸面极坐标为 $(\rho,\phi)$。纸面图案记为 $F(u,v)$ 或 $F(\rho,\phi)$，镜面图案记为 $G(\theta,z)$。映射算子定义为：

$$
T:(u,v)\mapsto(\theta,z),\qquad T^{-1}:(\theta,z)\mapsto(u,v).
$$

## 2.4.1 基于镜面参数坐标 $(\theta,z)$ 的映射模型（核心）

镜面上的点参数化为：

$$
P_{\text{mirror}}(\theta,z)=\bigl(x_0+R\cos\theta,\ y_0+R\sin\theta,\ z\bigr)
$$

单位外法向量为 $\mathbf{n}(\theta)=(\cos\theta,\sin\theta,0)$。

逆向映射（由镜面到纸面）是本文核心算子。从观察者 $E$ 出发，经镜面点 $P_{\text{mirror}}(\theta,z)$ 反射后与纸面 $z=0$ 相交于纸面点 $\mathbf{P}_{\mathrm{paper}}=(u(\theta,z),v(\theta,z),0)$。令单位视线向量

$$
\mathbf{V}=\frac{\mathbf{E}-P_{\text{mirror}}}{\lVert\mathbf{E}-P_{\text{mirror}}\rVert},
$$

根据反射定律，反射方向向量 $\mathbf{r}$ 满足：

$$
\mathbf{r}(\theta,z)=\mathbf{V}-2(\mathbf{V}\cdot\mathbf{n}(\theta))\,\mathbf{n}(\theta).
$$

参数方程 $P(t)=P_{\text{mirror}}+t\mathbf{r}$ 与平面 $z=0$ 求交，得：

$$
t(\theta,z)=-\frac{z}{r_z(\theta,z)},\quad (t>0,\ r_z<0).
$$

则逆向映射为：

$$
T^{-1}(\theta,z)=\bigl(u(\theta,z),\ v(\theta,z)\bigr)=P_{\text{mirror}}(\theta,z)+t(\theta,z)\cdot\mathbf{r}(\theta,z).
$$

纸面图案可由 $F(T^{-1}(\theta,z))=G(\theta,z)$ 确定。

**可见性约束**：上述逆向映射仅对可见镜面点有效，需同时满足以下两个条件：

$$
\mathbf{V}\cdot\mathbf{n}(\theta)<0 \quad\text{（法向背向观察者，镜面正面朝外可见）}
$$

$$
r_z < 0 \quad\text{（反射线向下与纸面相交，否则该点不产生有效纸面对应）}
$$

不满足上述条件的镜面点予以剔除，不参与图案生成。

正向映射 $T$ 为上述过程的逆，可通过求解射线与圆柱面的交点实现。

## 2.4.2 基于纸面极坐标 $(\rho,\phi)$ 的映射模型

**对称放置假设**：本节及后续推导中，约定观察者位于 $x$ 正半轴方向，即 $E=(D,0,z_E)$，圆柱轴心在坐标原点附近，$\phi=0$ 方向指向观察者投影方向。

以圆柱轴心 $(x_0,y_0)$ 为极点建立纸面极坐标 $(\rho,\phi)$。

正向映射可推导为显式形式。基于 Hunt et al.（2000）针对柱面镜提出的代数映射模型，定义中间系数（完整推导详见附录 A.1）：

$$
\alpha(z)=\frac{H_E-2z}{H_E-z},\qquad \beta(z)=\frac{z}{H_E-z},
$$

则纸面极坐标下的正向映射满足：

$$
\rho(\theta,z)=\sqrt{\alpha(z)^2 R^2+\beta(z)^2 L^2+2\alpha(z)\beta(z)RL\cos\theta},
$$

其中中间直角坐标为：

$$
\phi(\theta,z)=\operatorname{atan2}\!\bigl(\alpha(z)R\sin\theta+\beta(z)D\sin 2\theta,\;\alpha(z)R\cos\theta+\beta(z)D\cos 2\theta\bigr).
$$

该映射关于 $\theta=0$ 对称，在 $z<z_E$ 时光滑。

<!-- TODO: 附录 A.1 完整推导 -->

$$
\phi(\theta, z) = \text{atan2}(y_P, x_P).
$$

## 2.4.3 基于纸面直角坐标 $(u,v)$ 的映射模型

### 2.2.3 基于纸面直角坐标 $(u, v)$ 的映射模型

纸面直角坐标 $(u, v)$ 以 A4 纸左下角为原点，是最终输出所需的坐标系。

正向映射 $T: (u, v) \mapsto (\theta, z)$ 可通过求解以下非线性方程组获得：

$$
\begin{cases}
(x_0 + R \cos\theta - u)^2 + (y_0 + R \sin\theta - v)^2 = R^2, \\
z + (E_z - z) \dfrac{(E_x - x_0 - R \cos\theta)D_x + (E_y - y_0 - R \sin\theta)D_y}{(E_x - x_0 - R \cos\theta)^2 + (E_y - y_0 - R \sin\theta)^2} = 0
\end{cases}
$$

逆向映射 $T^{-1}:(\theta,z)\mapsto(u,v)$ 则通过 2.4.1 节中的向量形式直接计算，得到 $(u,v)$ 后可方便地转换为像素坐标进行图像生成。

## 2.4.4 映射模型的数值实现框架

由于逆向映射在解析形式上较为复杂，本文采用 **离散正向投影 + 散点插值** 的统一数值框架：

1. 在镜面参数域 $(\theta,z)$ 上进行高密度均匀采样；
2. 对每个采样点计算其在纸面坐标系 $(u,v)$ 或 $(\rho,\phi)$ 下的对应位置，形成带颜色的散点集；
3. 使用 **Delaunay 三角剖分线性插值**作为默认方法将散点转换为规则的纸面图像 $F(u,v)$；在散点稀疏或需要光滑性时可改用薄板样条（TPS）；
4. 通过像素物理尺寸 $a$（由 DPI 确定）完成从物理坐标到离散像素矩阵 $(i,j)$ 的转换。

该数值策略与 Wu et al.（2022）采用"反射形状 + 光栅化"替代反向光线追踪的思路一脉相承，均通过正向投影规避了反向映射解析求解的数值困难。该几何映射模型在四套坐标系下相互补充，共同构成了后续模型建立与计算的基础。
