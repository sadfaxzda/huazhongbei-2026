# 圆柱镜面反射的几何映射：正向与逆向模型

## 1. 符号定义与坐标系配置

将圆柱底面圆心置于纸面极坐标原点 $O$，纸面所在平面为 $z=0$。圆柱镜面为理想圆柱外侧面，半径 $R$，高度 $H$，竖直放置。观察者单眼位置固定为 $E=(L,0,H_e)$，其中 $L>R$，$H_e>0$，且视线无遮挡。

- 柱面点坐标：$Q(\theta,z)=\big(R\cos\theta,\;R\sin\theta,\;z\big)$，$\theta\in[0,2\pi)$ 为周向角，$z\in[0,H]$ 为高度。
- 镜面单位外法向：$\mathbf{n}=(\cos\theta,\;\sin\theta,\;0)$。
- 纸面点直角坐标：$(x,y,0)$，对应的极坐标表示为 $(\rho,\phi)$，满足 $x=\rho\cos\phi$，$y=\rho\sin\phi$，$\rho\ge0$，$\phi\in[0,2\pi)$。

---

## 2. 正向映射：镜面坐标到纸面极坐标

光线遵循反射定律，沿路径 $E\to Q\to P$ 传播，其中 $P$ 为纸面上的反射像点。下面推导镜面点 $(\theta,z)$ 到纸面点极坐标 $(\rho,\phi)$ 的闭合表达式。

### 2.1 反射向量计算

入射光线方向向量（由观察者指向镜面）：

$$
\mathbf{I}=Q-E = \big(R\cos\theta-L,\;R\sin\theta,\;z-H_e\big).
$$

镜面点法向量 $\mathbf{n}=(\cos\theta,\sin\theta,0)$，则入射向量与法向的点积为

$$
\mathbf{I}\cdot\mathbf{n} = (R\cos\theta-L)\cos\theta + R\sin^2\theta = R - L\cos\theta.
$$

根据反射定律，反射方向 $\mathbf{r}$ 满足 $\mathbf{r} = \mathbf{I} - 2(\mathbf{I}\cdot\mathbf{n})\mathbf{n}$，代入得

$$
\begin{aligned}
\mathbf{r} &= (R\cos\theta-L,\;R\sin\theta,\;z-H_e) - 2(R-L\cos\theta)(\cos\theta,\sin\theta,0) \\
&= \big(L\cos2\theta - R\cos\theta,\;\; L\sin2\theta - R\sin\theta,\;\; z-H_e \big).
\end{aligned}
$$

此处应用了恒等式 $\cos2\theta=2\cos^2\theta-1$ 及 $\sin2\theta=2\sin\theta\cos\theta$。

### 2.2 纸面交点坐标

反射光线的参数方程为 $P(t)=Q + t\mathbf{r}$，$t>0$。令其 $z$ 分量为 $0$，解得

$$
t = \frac{z}{H_e-z}, \quad 0\le z < H_e.
$$

将 $t$ 代入 $x,y$ 分量，得到纸面交点的直角坐标：

$$
\begin{aligned}
x_P &= R\cos\theta + \frac{z}{H_e-z}\big(L\cos2\theta - R\cos\theta\big),\\
y_P &= R\sin\theta + \frac{z}{H_e-z}\big(L\sin2\theta - R\sin\theta\big).
\end{aligned}
$$

### 2.3 极坐标形式

引入仅依赖于高度的中间系数

$$
\alpha(z) = \frac{H_e-2z}{H_e-z},\qquad
\beta(z) = \frac{z}{H_e-z},
$$

可将直角坐标整理为紧凑形式：

$$
\begin{aligned}
x_P &= \alpha(z)\,R\cos\theta + \beta(z)\,L\cos2\theta,\\
y_P &= \alpha(z)\,R\sin\theta + \beta(z)\,L\sin2\theta.
\end{aligned}\tag{1}
$$

利用 $\cos\theta\cos2\theta + \sin\theta\sin2\theta = \cos\theta$，纸面点的极径平方为

$$
\rho^2 = x_P^2 + y_P^2 = \alpha^2 R^2 + \beta^2 L^2 + 2\alpha\beta R L\cos\theta.
$$

由此得到正向映射的显式表达式：

$$
\boxed{
\begin{aligned}
\rho(\theta,z) &= \sqrt{\alpha^2 R^2 + \beta^2 L^2 + 2\alpha\beta R L\cos\theta},\\[4pt]
\phi(\theta,z) &= \operatorname{atan2}\big(y_P,\;x_P\big).
\end{aligned}}
\tag{2}
$$

式 $(2)$ 将柱面上任意可见点 $(\theta,z)$ 直接映射为纸面极坐标 $(\rho,\phi)$，且映射关于 $\theta=0$ 对称、在 $z<H_e$ 时处处光滑。

---

## 3. 逆映射：由纸面坐标反求镜面坐标

在实际设计中，更常见的需求是逆向映射：给定一幅期望在镜面中呈现的图案 $I_{\text{target}}(\theta,z)$，需要确定纸面上每一点 $(\rho,\phi)$ 所对应的颜色。这相当于求正向映射 $\mathcal{F}:(\theta,z)\mapsto(\rho,\phi)$ 的逆 $\mathcal{F}^{-1}$。

### 3.1 逆映射的存在性与求解策略

正向映射 $\mathcal{F}$ 在可见区域内是光滑单射，故其在数学上存在逆映射。但由于表达式 $(2)$ 包含三角函数的复杂耦合，难以导出显式解析解。因此，采用基于离散前向投影的数值方法。

### 3.2 数值逆映射算法

**输入**：目标镜面图案 $I_{\text{target}}(\theta,z)$，定义域 $\Omega\subset[-\theta_{\max},\theta_{\max}]\times[z_{\min},z_{\max}]$，以及几何参数 $R,L,H_e$。  
**输出**：纸面图像 $I_{\text{paper}}(\rho,\phi)$。

**步骤**：

1. **构建前向映射表**  
   在 $\Omega$ 内构造规则采样网格 $\{(\theta_i,z_j)\}$，利用式 $(2)$ 计算每一样本对应的纸面极坐标 $(\rho_{ij},\phi_{ij})$，存储三元组 $(\rho_{ij},\phi_{ij},\theta_i,z_j)$。

2. **纸面区域离散化**  
   根据 $(\rho_{ij},\phi_{ij})$ 的范围确定纸面输出图像的有效区域，并划分像素网格，各像素中心记为 $(\rho_p,\phi_q)$。

3. **散乱数据插值反求**  
   对于每一像素中心 $(\rho_p,\phi_q)$：
   - 在以 $(\rho_{ij},\phi_{ij})$ 为顶点的点集中进行二维 Delaunay 三角剖分或使用 KD‑树加速搜索；
   - 定位包含 $(\rho_p,\phi_q)$ 的三角形，利用重心坐标插值得到对应的 $(\theta,z)$；
   - 若点位于映射表凸包之外，则标记为背景或裁剪。

4. **颜色赋值**  
   由插值获得的 $(\theta,z)$ 读取目标镜面图案颜色：
   $$
   I_{\text{paper}}(\rho_p,\phi_q) = I_{\text{target}}(\theta,z).
   $$
   当 $(\theta,z)$ 超出定义域时，该像素置为透明或预先定义的底色。

5. **像素坐标转换（输出）**  
   将极坐标 $(\rho,\phi)$ 转换为纸面直角坐标 $(x,y)$，并输出标准光栅图像。

该算法的精度取决于前向映射网格的分辨率。由于映射光滑、无奇点，双线性或重心插值即可获得视觉上令人满意的结果，能够满足反射艺术品制作的要求。
