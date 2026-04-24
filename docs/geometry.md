# 2.2 圆柱镜面反射的几何映射模型

为系统描述纸面图案与镜面图案之间的关系，本文建立正向映射 $T$ 与逆向映射 $T^{-1}$，并在不同坐标系下给出其数学表达。全局坐标系约定如下：

- **3D 直角坐标系** $(x,y,z)$：用于光线追踪、反射定律推导和向量运算；
- **镜面柱面参数坐标系** $(\theta,z)$：用于镜面离散化与镜面图案 $G(\theta,z)$ 的定义；
- **纸面极坐标系** $(\rho,\phi)$：以圆柱轴心 $(x_0,y_0)$ 为极点，用于变形分析与对称性研究；
- **纸面直角坐标系** $(u,v)$：以 A4 纸左下角为原点，用于最终图像生成与打印输出。

主要符号遵循本文符号表：圆柱半径为 $R$，观察者位置为 $\mathbf{E}=(x_E,y_E,H_E)$，水平距离为 $L$，镜面高度参数为 $z$，纸面直角坐标为 $(u,v)$，纸面极坐标为 $(\rho,\phi)$。纸面图案记为 $F(u,v)$ 或 $F(\rho,\phi)$，镜面图案记为 $G(\theta,z)$。映射算子定义为：

$$
T:(u,v)\mapsto(\theta,z),\qquad T^{-1}:(\theta,z)\mapsto(u,v).
$$

## 2.2.1 基于镜面参数坐标 $(\theta,z)$ 的映射模型（核心）

镜面上的点参数化为：

$$
P_{\text{mirror}}(\theta,z)=\bigl(x_0+R\cos\theta,\ y_0+R\sin\theta,\ z\bigr)
$$

单位外法向量为 $\mathbf{n}(\theta)=(\cos\theta,\sin\theta,0)$。

逆向映射（由镜面到纸面）是本文核心算子。从观察者 $\mathbf{E}$ 出发，经镜面点 $P_{\text{mirror}}(\theta,z)$ 反射后与纸面 $z=0$ 相交于点 $Q(u(\theta,z),v(\theta,z))$。令单位视线向量

$$
\mathbf{V}=\frac{\mathbf{E}-P_{\text{mirror}}}{\lVert\mathbf{E}-P_{\text{mirror}}\rVert},
$$

根据反射定律，反射方向向量 $\mathbf{D}$ 满足：

$$
\mathbf{D}(\theta,z)=\mathbf{V}-2(\mathbf{V}\cdot\mathbf{n}(\theta))\,\mathbf{n}(\theta).
$$

参数方程 $P(t)=P_{\text{mirror}}+t\mathbf{D}$ 与平面 $z=0$ 求交，设 $\mathbf{D}=(D_x,D_y,D_z)$，由 $z+tD_z=0$ 得：

$$
t(\theta,z)=-\frac{z}{D_z(\theta,z)},\quad (t>0,\ D_z<0).
$$

则逆向映射为：

$$
T^{-1}(\theta,z)=\bigl(u(\theta,z),\ v(\theta,z)\bigr)=P_{\text{mirror}}(\theta,z)+t(\theta,z)\cdot\mathbf{D}(\theta,z).
$$

纸面图案可由 $F(T^{-1}(\theta,z))=G(\theta,z)$ 确定。

正向映射 $T$ 为上述过程的逆，可通过求解射线与圆柱面的交点实现。

## 2.2.2 基于纸面极坐标 $(\rho,\phi)$ 的映射模型

以圆柱轴心 $(x_0,y_0)$ 为极点建立纸面极坐标 $(\rho,\phi)$，其中 $\phi=0$ 方向指向观察者投影方向。

正向映射可推导为显式形式（对称放置假设下）。定义中间系数：

$$
\alpha(z)=\frac{H_E-2z}{H_E-z},\qquad \beta(z)=\frac{z}{H_E-z},
$$

则纸面极坐标下的正向映射满足：

$$
\rho(\theta,z)=\sqrt{\alpha(z)^2 R^2+\beta(z)^2 L^2+2\alpha(z)\beta(z)RL\cos\theta},
$$

其中中间直角坐标为：

$$
\begin{aligned}
x_P &= \alpha R\cos\theta+\beta L\cos2\theta,\\
y_P &= \alpha R\sin\theta+\beta L\sin2\theta,
\end{aligned}
$$

于是

$$
\phi(\theta,z)=\operatorname{atan2}\!\bigl(y_P,\;x_P\bigr).
$$

该映射关于 $\theta=0$ 对称，在 $z<H_E$ 时光滑。逆向映射 $T^{-1}$ 在极坐标下无简洁解析式，通常通过数值方法由 $(\rho,\phi)$ 反求 $(\theta,z)$。

## 2.2.3 基于纸面直角坐标 $(u,v)$ 的映射模型

纸面直角坐标 $(u,v)$ 以 A4 纸左下角为原点，是最终输出所必需的坐标系。

正向映射 $T:(u,v)\mapsto(\theta,z)$ 可通过求解以下非线性方程组获得：

$$
\begin{cases}
(x_0+R\cos\theta-u)^2+(y_0+R\sin\theta-v)^2=R^2,\\[4pt]
z+(\mathbf{E}_z-z)\dfrac{(\mathbf{E}_x-x_0-R\cos\theta)D_x+(\mathbf{E}_y-y_0-R\sin\theta)D_y}{(\mathbf{E}_x-x_0-R\cos\theta)^2+(\mathbf{E}_y-y_0-R\sin\theta)^2}=0,
\end{cases}
$$

其中 $\mathbf{E}=(L,0,H_E)$ 为观察者位置，$D_x,D_y$ 为反射方向向量 $\mathbf{D}$ 的 $x,y$ 分量（隐含 $\theta$ 依赖）。

逆向映射 $T^{-1}:(\theta,z)\mapsto(u,v)$ 则通过 2.2.1 节中的向量形式直接计算，得到 $(u,v)$ 后可方便地转换为像素坐标进行图像生成。

## 2.2.4 映射模型的数值实现框架

由于逆向映射在解析形式上较为复杂，本文采用 **离散正向投影 + 散点插值** 的统一数值框架：

1. 在镜面参数域 $(\theta,z)$ 上进行高密度均匀采样；
2. 对每个采样点计算其在纸面坐标系 $(u,v)$ 或 $(\rho,\phi)$ 下的对应位置，形成带颜色的散点集；
3. 使用径向基函数（RBF）或网格数据插值方法，将散点转换为规则的纸面图像 $F(u,v)$；
4. 通过像素物理尺寸 $a_{\text{pix}}$（由 DPI 确定）完成从物理坐标到离散像素矩阵 $(i,j)$ 的转换。

该几何映射模型在四套坐标系下相互补充，共同构成了后续模型建立与计算的基础。
