function render_3D_system_corrected()
    % 1. 物理参数（单位：mm）
    R = 35; D = 250; zE = 350; H = 150;
    
    figure('Color', 'white', 'Position', [100, 100, 1000, 800]);
    hold on; grid on; view(3);
    
    % 2. 绘制 A4 纸平面 (Y轴方向: -50 到 160)
    paper_x = [-148.5, 148.5, 148.5, -148.5];
    paper_y = [-50, -50, 160, 160];
    paper_z = [0, 0, 0, 0];
    fill3(paper_x, paper_y, paper_z, [0.9 0.9 0.9], 'FaceAlpha', 0.6, 'EdgeColor', 'k', 'LineWidth', 2);
    text(90, 140, 0, 'A4 Paper', 'FontSize', 14, 'FontWeight', 'bold');
    
    % 3. 绘制实体不透明圆柱体 (中心在 0,0)
    [THETA_CYL, Z_CYL] = meshgrid(linspace(0, 2*pi, 50), linspace(0, H, 50));
    X_CYL = R .* sin(THETA_CYL);
    Y_CYL = R .* cos(THETA_CYL);
    % FaceAlpha 设为 0.9，表现其几乎不透明的镜面实体感
    surf(X_CYL, Y_CYL, Z_CYL, 'FaceColor', [0.3 0.8 0.9], 'EdgeColor', 'none', 'FaceAlpha', 0.9);
    
    plot3(0, 0, 0, 'k+', 'MarkerSize', 12, 'LineWidth', 2);
    text(20, 0, 0, 'Origin O(0,0)', 'FontSize', 10, 'FontWeight', 'bold');
    
    % 4. 绘制观察者眼点 E (在 +Y 同侧)
    eye_x = 0; eye_y = D; eye_z = zE;
    plot3(eye_x, eye_y, eye_z, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
    
    text(eye_x, eye_y + 10, eye_z + 20, sprintf(' Eye E(0, %.0f, %.0f) mm', D, zE), ...
        'FontSize', 12, 'Color', 'r', 'FontWeight', 'bold');
    
    % 辅助垂直线
    plot3([eye_x, eye_x], [eye_y, eye_y], [0, eye_z], 'r:', 'LineWidth', 1.5);
    plot3(eye_x, eye_y, 0, 'rx', 'MarkerSize', 10);
    text(eye_x, eye_y + 10, 0, sprintf('Observer D=%.0fmm', D), 'Color', 'r');
    
    % 5. 追踪同侧反射光线
    theta_max = 13 * pi / 18;  % 130度张角
    thetas = linspace(-theta_max/2, theta_max/2, 9);
    mz = 80; 
    
    for i = 1:length(thetas)
        th = thetas(i);
        % 击中圆柱的前表面 (+Y)
        mx = R * sin(th);
        my = R * cos(th);
        
        alpha = (zE - 2*mz) / (zE - mz);
        beta = mz / (zE - mz);
        rho = sqrt((alpha*R)^2 + (beta*D)^2 + 2*alpha*beta*R*D*cos(th));
        y_term = alpha*R*sin(th) + beta*D*sin(2*th);
        x_term = alpha*R*cos(th) + beta*D*cos(2*th);
        phi = atan2(y_term, x_term);
        
        px = rho * sin(phi);
        py = rho * cos(phi); % 投影在 +Y
        pz = 0;
        
        h1 = plot3([eye_x, mx], [eye_y, my], [eye_z, mz], '--', 'Color', [1, 0.5, 0], 'LineWidth', 1.5);
        h2 = plot3([mx, px], [my, py], [mz, pz], '-', 'Color', 'b', 'LineWidth', 2);
        
        plot3(mx, my, mz, 'k.', 'MarkerSize', 15);
        plot3(px, py, pz, 'b.', 'MarkerSize', 20);
    end
    
    % 6. 设置与美化
    xlabel('X Width (mm)', 'FontWeight', 'bold');
    ylabel('Y Depth (mm)', 'FontWeight', 'bold');
    zlabel('Z Height (mm)', 'FontWeight', 'bold');
    title('Physically Accurate 3D Geometric Optics Rendering', 'FontSize', 16);
    
    legend([h1, h2], {'Incident Ray (from Eye)', 'Reflected Ray (to Paper)'}, 'Location', 'northeast');
    
    axis equal; 
    % 设定一个极具透视感的摄像机机位，从侧面清晰看到折线
    set(gca, 'CameraPosition', [600, 600, 400]); 
end
