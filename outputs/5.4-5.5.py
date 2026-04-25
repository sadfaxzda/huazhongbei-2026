import numpy as np
import matplotlib.pyplot as plt


def generate_mandala(size=500):
    """
    生成 5.4 部分所需的高兼容性曼陀罗图案 (纸面图案 P*)
    利用极坐标下的余弦和正弦波叠加，保证其具有完美的角向与径向频率对称性
    """
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(x, y)

    # 转换为极坐标
    R = np.sqrt(X ** 2 + Y ** 2)
    Theta = np.arctan2(Y, X)

    # 构建曼陀罗数学函数：12个花瓣(角向频率) + 径向波动(空间频率)
    mandala = np.cos(12 * Theta) * np.sin(15 * R) * np.exp(-1.5 * R ** 2)

    # 归一化到 0-1 范围用于显示
    mandala = (mandala - mandala.min()) / (mandala.max() - mandala.min())
    # 消除超出单位圆的背景
    mandala[R > 1] = 0
    return mandala


def generate_mirror_target(size=500):
    """
    生成 5.4 部分对应的镜面目标图案 (镜面图案 M*)
    这里生成规则的竖向条纹，与曼陀罗的角向频率完美契合
    """
    x = np.linspace(-1, 1, size)
    X, _ = np.meshgrid(x, x)
    # 竖向条纹波形
    mirror_target = np.abs(np.sin(12 * np.pi * X))
    return mirror_target


def simulate_incorrect_mapping(size=500):
    """
    生成 5.5 部分所需的“不正确映射图” (极端扭曲演示)
    模拟将一个常规网格（代表卡通猫等普通图像）强行塞入柱面逆映射算子后产生的剧烈畸变
    """
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(x, y)

    # 生成一个代表普通图像的规则棋盘格
    checkerboard = np.sign(np.sin(10 * np.pi * X) * np.sin(10 * np.pi * Y))

    # 模拟柱面逆映射算子 T^{-1} 带来的空间拉伸 (雅可比行列式畸变)
    # 越靠近中心 (盲区边缘)，径向拉伸越极度夸张
    R = np.sqrt(X ** 2 + Y ** 2) + 0.01  # 防止除以 0
    Theta = np.arctan2(Y, X)

    # 假设强行进行逆向投影，r 会被 1/r 级别的非线性畸变撕裂
    distorted_R = 1 / (3 * R)
    distorted_X = distorted_R * np.cos(Theta)
    distorted_Y = distorted_R * np.sin(Theta)

    # 生成畸变后的图像
    distorted_image = np.sign(np.sin(10 * np.pi * distorted_X) * np.sin(10 * np.pi * distorted_Y))
    distorted_image[R > 1] = 0
    return checkerboard, distorted_image


# ==================== 可视化输出与保存 ====================
plt.figure(figsize=(15, 10))

# 1. 5.4 纸面曼陀罗图案
mandala_img = generate_mandala()
plt.subplot(2, 2, 1)
plt.imshow(mandala_img, cmap='magma')
plt.title("5.4 Feasible P*: Mandala Pattern\n(High Polar Symmetry)")
plt.axis('off')

# 2. 5.4 镜面目标竖条纹
mirror_img = generate_mirror_target()
plt.subplot(2, 2, 2)
plt.imshow(mirror_img, cmap='magma')
plt.title("5.4 Feasible M*: Vertical Stripes\n(Matches Radial Freq)")
plt.axis('off')

# 3. 5.5 原始不兼容图像 (棋盘格/卡通风格特征)
normal_grid, distorted_grid = simulate_incorrect_mapping()
plt.subplot(2, 2, 3)
plt.imshow(normal_grid, cmap='gray')
plt.title("5.5 Infeasible P*: Regular Grid\n(No Rotational Symmetry)")
plt.axis('off')

# 4. 5.5 强行逆映射后的灾难性畸变图
plt.subplot(2, 2, 4)
plt.imshow(distorted_grid, cmap='gray')
plt.title("5.5 Conflict Map: Severe T^{-1} Distortion\n(Jacobian Singularity)")
plt.axis('off')

plt.tight_layout()
# 运行后会直接弹出这四张图，你可以截图或通过 plt.savefig() 保存高清原图放入论文
plt.show()