function render_3D_cat_system()
    % 1. 小猫专属物理参数
    R = 3.5; D = 25.0; zE = 35.0; H = 15.0;
    z_min = 0.2; z_max = 9.0; % 图像高度范围
    theta_max = 2 * pi / 3;   % 120度大张角
    
    figure('Color', 'white', 'Position', [100, 100, 1000, 800]);
    hold on; grid on; view(3);
    
    % 2. 绘制 A4 纸平面 (Y轴范围: -5.0 到 16.0)
    paper_x = [-14.85, 14.85, 14.85, -14.85];
    paper_y = [-5.0, -5.0, 16.0, 16.0];
    paper_z = [0, 0, 0, 0];
    fill3(paper_x, paper_y, paper_z, [0.9 0.9 0.9], 'FaceAlpha', 0.6, 'EdgeColor', 'k', 'LineWidth', 2);
    text(9, 14, 0, 'A4 Paper', 'FontSize', 14, 'FontWeight', 'bold');
    
    % 3. 绘制实体不透明圆柱体 (灰色/青色表现实体)
    [THETA_CYL, Z_CYL] = meshgrid(linspace(0, 2*pi, 60), linspace(0, H, 50));
    X_CYL = R .* sin(THETA_CYL);
    Y_CYL = R .* cos(THETA_CYL);
    % 设为不透明
    surf(X_CYL, Y_CYL, Z_CYL, 'FaceColor', [0.3 0.8 0.9], 'EdgeColor', 'none', 'FaceAlpha', 0.95);
    
    plot3(0, 0, 0, 'k+', 'MarkerSize', 12, 'LineWidth', 2);
    text(2, 0, 0, 'Origin O(0,0)', 'FontSize', 10, 'FontWeight', 'bold');
    
    % 4. 绘制观察者眼点 E (在 +Y 区域，满足实心反射)
    eye_x = 0; eye_y = D; eye_z = zE;
    plot3(eye_x, eye_y, eye_z, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
    
    text(eye_x, eye_y + 1, eye_z + 2, sprintf(' Eye E(0, %.1f, %.1f)', D, zE), ...
        'FontSize', 12, 'Color', 'r', 'FontWeight', 'bold');
    
    % 辅助线与地面位置
    plot3([eye_x, eye_x], [eye_y, eye_y], [0, eye_z], 'r:', 'LineWidth', 1.5);
    plot3(eye_x, eye_y, 0, 'rx', 'MarkerSize', 10);
    text(eye_x, eye_y + 1, 0, sprintf('Observer D=%.1fcm', D), 'Color', 'r');
    
    % 5. 追踪同侧反射光线 (小猫 120°)
    thetas = linspace(-theta_max/2, theta_max/2, 9); % 采样 9 条线以表现 120° 的宽度
    mz = 6.0; % 采样高度
    
    for i = 1:length(thetas)
        th = thetas(i);
        % 击中圆柱的前表面 M
        mx = R * sin(th);
        my = R * cos(th);
        
        alpha = (zE - 2*mz) / (zE - mz);
        beta = mz / (zE - mz);
        rho = sqrt((alpha.*R).^2 + (beta.*D).^2 + 2.*alpha.*beta.*R.*D.*cos(th));
        y_term = alpha.*R.*sin(th) + beta.*D.*sin(2.*th);
        x_term = alpha.*R.*cos(th) + beta.*D.*cos(2.*th);
        phi = atan2(y_term, x_term);
        
        px = rho * sin(phi);
        py = rho * cos(phi); % 投影在 +Y
        pz = 0;
        
        % 画视线 (虚线)
        h1 = plot3([eye_x, mx], [eye_y, my], [eye_z, mz], '--', 'Color', [1, 0.5, 0], 'LineWidth', 1);
        % 画投影反射线 (实线)
        h2 = plot3([mx, px], [my, py], [mz, pz], '-', 'Color', 'b', 'LineWidth', 2);
        
        plot3(mx, my, mz, 'k.', 'MarkerSize', 12);
        plot3(px, py, pz, 'b.', 'MarkerSize', 18);
    end
    
    % 6. 设置与美化
    xlabel('X Width (cm)', 'FontWeight', 'bold');
    ylabel('Y Depth (cm)', 'FontWeight', 'bold');
    zlabel('Z Height (cm)', 'FontWeight', 'bold');
    title('Physically Accurate 3D Trace for Cat (120° Angle)', 'FontSize', 16);
    
    legend([h1, h2], {'Incident Ray (from Eye)', 'Reflected Ray (to Paper)'}, 'Location', 'northeast');
    
    axis equal; 
    % 摄像机机位：侧上方，清晰展示折线关系和极宽的扇面覆盖
    set(gca, 'CameraPosition', [60, 60, 40]); 
end