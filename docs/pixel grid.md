# 3. 镜面图案的参数化与像素网格生成

## 3.1 问题分析

题目给定的"镜面图案参考图" $I_{\mathrm{ref}}$ 是一幅矩形数字图像，代表观察者透过圆柱镜**期望看到的虚像**，而非直接印在圆柱侧面上的纹理。因此从参考图到可打印纸面图案，需要两步转换：

1. **视觉反扭曲** $\;I_{\mathrm{ref}}(u,v)\;\longrightarrow\;I_{\mathrm{mirror}}(\theta,z)$：将虚像反求为圆柱侧面上的实际纹理；
2. **光学逆映射** $\;I_{\mathrm{mirror}}(\theta,z)\;\longrightarrow\;I_{\mathrm{paper}}(u,v)$：将镜面纹理沿反射光路投影到纸面。

本节聚焦第一步，即镜面参数化与规则像素网格的建立。

## 3.2 几何模型

### 3.2.1 视平面与视线

观察者眼点 $E=(L,0,H_e)$。设主视线 $\hat{\mathbf{v}}_0=(-1,0,0)$ 指向圆柱轴心，虚拟视平面 $\Pi$ 垂直于主视线、距眼点 $d_0$，即

$$
\Pi:\; x = L-d_0.
$$

视平面上以主视线交点为原点建立局部坐标 $(u,v)$（$u$ 水平、$v$ 垂直），则像素对应的空间点为

$$
P_{\mathrm{view}}(u,v)=(L-d_0,\; u,\; H_e+v).
$$

### 3.2.2 视线与圆柱求交

从眼点出发的视线 $\mathbf{r}(t)=E+t\,(P_{\mathrm{view}}-E)$ 与圆柱侧面

$$
x^2+y^2=R^2,\qquad 0\le z\le H
$$

联立，得关于 $t$ 的二次方程。取面向观察者一侧的较小正根 $t^{*}$，代回得交点 $Q=(x_Q,y_Q,z_Q)$，其柱面参数为

$$
\theta=\mathrm{atan2}(y_Q,x_Q),\qquad z=z_Q.
$$

若方程无正实根或 $z_Q\notin[0,H]$，则该像素落在镜面外，予以舍弃。由此得到映射

$$
\mathcal{T}:(u,v)\longmapsto(\theta,z).
$$

当 $R\ll L$ 时 $\theta\approx u/L$，退化为近似线性关系。

## 3.3 镜面像素网格的建立

### 3.3.1 规则 $(\theta,z)$ 网格

由所有有效像素经 $\mathcal{T}$ 映射得到的散点，取包络矩形

$$
[\Theta_{\min},\Theta_{\max}]\times[Z_{\min},Z_{\max}],
$$

并以分辨率 $N_\theta\times N_z$ 均匀划分：

$$
\theta_k=\Theta_{\min}+k\,\Delta\theta,\qquad 
z_l=Z_{\min}+l\,\Delta z,
$$

其中 $k=0,\dots,N_\theta-1,\;l=0,\dots,N_z-1$。$N_\theta,N_z$ 一般不低于参考图分辨率，以避免下采样造成细节丢失。

### 3.3.2 网格点着色

对每个网格节点 $(\theta_k,z_l)$，采用"正向散点 + 插值"策略确定其颜色：

1. 对 $I_{\mathrm{ref}}$ 的每个像素 $(u_m,v_m)$ 计算 $(\theta_m,z_m)=\mathcal{T}(u_m,v_m)$，得到散点集 $\{(\theta_m,z_m,u_m,v_m)\}$；
2. 在该散点集上对 $(\theta_k,z_l)$ 做二维插值（建议三角剖分线性插值），求得视平面坐标 $(u_{kl},v_{kl})$；
3. 在 $I_{\mathrm{ref}}$ 中用双线性插值采样 $(u_{kl},v_{kl})$，赋给 $I_{\mathrm{mirror}}(\theta_k,z_l)$；落在映射覆盖区域外的节点置为透明。

所得 $I_{\mathrm{mirror}}$ 即为理想情况下直接包裹在圆柱侧面、能重建参考图像的纹理。

## 3.4 生成纸面图案的完整流程

| 步骤 | 操作 | 关键公式 / 说明 |
|------|------|------------------|
| 1. 参数预设 | 读入 $I_{\mathrm{ref}}$；设定 $R,H,E=(L,0,H_e),d_0$，以及圆柱在 A4 上的放置点 $(X_0,Y_0)$ | A4 竖置：$X\in[0,210]$ mm，$Y\in[0,297]$ mm |
| 2. 视觉反扭曲 | 按 3.2–3.3 节生成 $I_{\mathrm{mirror}}(\theta,z)$ | 映射 $\mathcal{T}$ + 散点插值 |
| 3. 正向映射到纸面 | 对每个 $(\theta_k,z_l)$ 计算纸面极坐标 $(\rho_{kl},\phi_{kl})$ | 见下式 |
| 4. 纸面图像重采样 | 在纸面规则网格上，由散点 $(\rho_{kl},\phi_{kl})$ 插值反查 $(\theta,z)$，再取 $I_{\mathrm{mirror}}$ 颜色 | 得到 $I_{\mathrm{paper}}$ |
| 5. A4 适配与输出 | 平移 $(X,Y)=(X_0+\rho\cos\phi,\;Y_0+\rho\sin\phi)$；调整 $(X_0,Y_0)$ 使图案落在纸内并留边距；以 $\ge 300$ DPI 输出 | 必要时优化 $R,H$ 或裁剪 |

**纸面正向映射公式**（对称放置，$\alpha_l=\dfrac{H_e-2z_l}{H_e-z_l},\;\beta_l=\dfrac{z_l}{H_e-z_l}$）：

$$
\rho_{kl}=\sqrt{\alpha_l^{2}R^{2}+\beta_l^{2}L^{2}+2\alpha_l\beta_l RL\cos\theta_k},
$$

$$
\phi_{kl}=\mathrm{atan2}\!\bigl(\alpha_l R\sin\theta_k+\beta_l L\sin 2\theta_k,\;\alpha_l R\cos\theta_k+\beta_l L\cos 2\theta_k\bigr).
$$

**验证**：可通过正向光线追踪渲染出虚拟观察图，与 $I_{\mathrm{ref}}$ 用 SSIM/PSNR 定量对比。

## 3.5 实现注意事项

- **分辨率匹配**：纸面图像因径向拉伸通常需显著高于 $I_{\mathrm{ref}}$ 的分辨率，建议以最大局部雅可比行列式作为上采样因子的参考。
- **插值方法**：散点→网格阶段推荐 Delaunay 三角剖分线性插值或薄板样条（TPS），避免最近邻造成的马赛克。
- **可见性剔除**：仅保留 $\hat{\mathbf{v}}\cdot\mathbf{n}(\theta)<0$ 的镜面点（法向背向观察者的面不可见），并剔除被圆柱自身遮挡的区域。
- **极端畸变**：当 $R$ 较大或图案靠近镜面边缘时纸面上对应区域会剧烈拉伸，可能超出 A4 或导致打印失真。应限制 $\theta$ 取值范围或缩小图案在视平面上的角尺寸。
- **数值稳定**：$z_l\to H_e$ 时 $\alpha_l,\beta_l$ 发散，需将镜面有效高度严格限制在 $z<H_e$ 以内。

该参数化与网格化方案将任意矩形参考图系统地转换为可打印的变形纸面图案，满足问题一的设计要求。
