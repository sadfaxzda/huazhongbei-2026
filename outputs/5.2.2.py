import numpy as np
import cv2
from scipy.ndimage import zoom

def compute_frequency_compatibility(
    P_star_path: str,
    M_star_path: str,
    x0_mm: float, y0_mm: float,   # 圆柱中心在 A4 纸上的物理坐标 (mm)
    R_mm: float,                  # 圆柱半径 (mm)
    rho_max_mm: float,            # 可视外径 ρ_max (mm)，由公式(5.8)计算
    dpi: int = 300,               # 图像分辨率
    A4_w_mm: float = 210.0,
    A4_h_mm: float = 297.0
) -> dict:
    """
    计算纸面目标 P* 与镜面目标 M* 的频域兼容性相关系数。

    返回:
    {
      'corr_angular_horizontal': float,   # 角频谱(纸面) vs 横频谱(镜面)
      'corr_radial_vertical': float,      # 径向频谱(纸面) vs 纵频谱(镜面)
      'compatibility_score': float        # 综合得分 (最小值)
    }
    """
    # ---------- 读取并调整大小 ----------
    P = cv2.imread(P_star_path, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
    M = cv2.imread(M_star_path, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0

    # 计算像素尺度
    ppm = dpi / 25.4              # pixels per mm
    # A4 像素尺寸
    A4_w_px = int(A4_w_mm * ppm)
    A4_h_px = int(A4_h_mm * ppm)

    # 将 P* 缩放/裁剪至 A4 物理分辨率（假设输入图像就是 A4 幅面，否则先 resize）
    if P.shape[0] != A4_h_px or P.shape[1] != A4_w_px:
        P = cv2.resize(P, (A4_w_px, A4_h_px))

    # 圆柱中心像素坐标
    cx = int(round(x0_mm * ppm))
    cy = int(round(y0_mm * ppm))

    # 极坐标最大半径（像素）
    max_radius_px = int(round(rho_max_mm * ppm))
    # 角度采样数（可根据外围周长设定，保证无混叠）
    angle_samples = int(np.ceil(2 * np.pi * max_radius_px))

    # ---------- 纸面 P* 的极坐标映射 ----------
    # warpPolar 要求 dst_size = (width, height)，其中 width 对应角度方向，height 对应径向方向
    P_polar = cv2.warpPolar(
        P,
        dsize=(angle_samples, max_radius_px),
        center=(cx, cy),
        maxRadius=max_radius_px,
        flags=cv2.WARP_POLAR_LINEAR
    )
    # P_polar 尺寸：(max_radius_px, angle_samples)，行：径向，列：角度
    # 转换为 0‑1 浮动
    P_polar = np.clip(P_polar, 0, 1)

    # ---------- 提取一维频谱 ----------
    # 1. 对 P_polar 做 2D FFT，得到幅度谱
    F_P = np.fft.fftshift(np.fft.fft2(P_polar))
    Mag_P = np.abs(F_P)
    # 移除直流分量
    Mag_P[Mag_P.shape[0]//2, Mag_P.shape[1]//2] = 0

    # 角频谱：对径向求和（消除径向方向，保留角度方向的频率变化）
    angular_spectrum_P = np.sum(Mag_P, axis=0)  # 长度为 angle_samples
    # 径向频谱：对角方向求和（消除角度方向，保留径向方向的频率变化）
    radial_spectrum_P = np.sum(Mag_P, axis=1)    # 长度为 max_radius_px

    # 2. 对镜面目标 M* 做 2D FFT
    F_M = np.fft.fftshift(np.fft.fft2(M))
    Mag_M = np.abs(F_M)
    Mag_M[Mag_M.shape[0]//2, Mag_M.shape[1]//2] = 0

    # 横频谱（对应 θ 方向）：按列求和（消除高度方向，保留水平频率）
    horizontal_spectrum_M = np.sum(Mag_M, axis=0)  # 长度等于 M 的宽度
    # 纵频谱（对应 z 方向）：按行求和（消除水平方向，保留垂直频率）
    vertical_spectrum_M = np.sum(Mag_M, axis=1)    # 长度等于 M 的高度

    # ---------- 对齐长度并计算皮尔逊相关系数 ----------
    # 角频谱 vs 横频谱：都需要插值到公共长度（取两者的几何平均）
    common_len_ah = int(np.sqrt(len(angular_spectrum_P) * len(horizontal_spectrum_M)))
    ang_spec_resized = zoom(angular_spectrum_P, common_len_ah / len(angular_spectrum_P), order=1)
    hor_spec_resized = zoom(horizontal_spectrum_M, common_len_ah / len(horizontal_spectrum_M), order=1)
    corr_angular_horizontal = np.corrcoef(ang_spec_resized, hor_spec_resized)[0, 1]

    # 径向频谱 vs 纵频谱
    common_len_rv = int(np.sqrt(len(radial_spectrum_P) * len(vertical_spectrum_M)))
    rad_spec_resized = zoom(radial_spectrum_P, common_len_rv / len(radial_spectrum_P), order=1)
    ver_spec_resized = zoom(vertical_spectrum_M, common_len_rv / len(vertical_spectrum_M), order=1)
    corr_radial_vertical = np.corrcoef(rad_spec_resized, ver_spec_resized)[0, 1]

    # ---------- 综合得分 ----------
    # 取两个相关系数的较小值作为频域兼容性下限（更严格）
    compatibility_score = min(corr_angular_horizontal, corr_radial_vertical)

    return {
        'corr_angular_horizontal': corr_angular_horizontal,
        'corr_radial_vertical': corr_radial_vertical,
        'compatibility_score': compatibility_score
    }


# ========== 使用示例 ==========
if __name__ == '__main__':
    # 根据你的圆柱几何参数设置（与实际设计一致）
    x0_mm = 105.0        # 圆柱中心横坐标 (A4 210mm 的半宽)
    y0_mm = 148.5        # 圆柱中心纵坐标 (A4 297mm 的半高)
    R_mm = 30.0          # 圆柱半径
    # 由公式(5.8) 计算 ρ_max (举例：D=400, zE=200, H=100)
    D = 400.0
    zE = 200.0
    H = 100.0
    rho_max_mm = (zE - 2*H)/(zE - H) * R_mm + H/(zE - H) * D   # 约 130 mm

    result = compute_frequency_compatibility(
        P_star_path='cat.jpg',
        M_star_path='monalisa.jpg',
        x0_mm=x0_mm,
        y0_mm=y0_mm,
        R_mm=R_mm,
        rho_max_mm=rho_max_mm,
        dpi=300
    )
    print("Angular‑Horizontal Correlation:", result['corr_angular_horizontal'])
    print("Radial‑Vertical Correlation:", result['corr_radial_vertical'])
    print("Overall Compatibility Score:", result['compatibility_score'])

    # 判断阈值 ε_freq
    epsilon_freq = 0.6
    if result['compatibility_score'] >= epsilon_freq:
        print("✅ 频域预检通过，可进入双目标优化。")
    else:
        print("❌ 频域预检失败，两图在几何结构上互斥。")