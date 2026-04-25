import numpy as np
import matplotlib.pyplot as plt


def generate_conflict_mapping(size=800):
    """
    生成 5.5 部分所需的“不正确映射图” (极端扭曲演示)
    模拟将不具备角向对称性的规则网格，强行逆映射到纸面所产生的雅可比畸变
    """
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(x, y)

    # 1. 生成不兼容的初始纸面目标 P* (规则正交棋盘格，代表卡通猫等普通图像特征)
    # 增加频率以更清晰地展示畸变撕裂感
    checkerboard = np.sign(np.sin(15 * np.pi * X) * np.sin(15 * np.pi * Y))

    # 2. 模拟向极坐标的转换与柱面逆映射算子 T^{-1} 的空间拉伸
    R = np.sqrt(X ** 2 + Y ** 2) + 1e-4  # 加上微小偏移，防止中心点除以 0 的雅可比奇点崩溃
    Theta = np.arctan2(Y, X)

    # 假设强行进行逆向投影，径向 r 会受到 1/r 级别的非线性畸变撕裂
    # 这里我们构造一个模拟反射算子极限拉伸的畸变场
    distorted_R = 1 / (4 * R)
    distorted_X = distorted_R * np.cos(Theta)
    distorted_Y = distorted_R * np.sin(Theta)

    # 3. 将畸变场代入原特征图案，生成强行映射后的结果
    distorted_image = np.sign(np.sin(15 * np.pi * distorted_X) * np.sin(15 * np.pi * distorted_Y))

    # 裁剪可视区域（剔除无穷远处的发散像素）
    distorted_image[R > 1] = 0
    checkerboard[R > 1] = 0

    return checkerboard, distorted_image


# 运行并可视化保存
P_star_infeasible, T_inv_distortion = generate_conflict_mapping()

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(P_star_infeasible, cmap='gray')
plt.title("P*: Regular Orthogonal Grid\n(No Rotational Symmetry)")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(T_inv_distortion, cmap='gray')
plt.title("Conflict Map: Severe Jacobian Distortion\n(T^{-1} Mapping Collapse)")
plt.axis('off')

plt.tight_layout()
plt.show()