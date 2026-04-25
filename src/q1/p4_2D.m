function generate_cat_perfect_layout()
    % 注：角跨度从 120° 调整为 90°，使其落入角度放大效应（φ≈2θ）的线性适用范围
    % 详见论文 3.6 节

    % 1. 以圆心为原点的小猫专属参数
    R = 3.5; D = 25.0; zE = 35.0;
    z_min = 0.2; z_max = 9.0;
    theta_max = pi / 2;        % 90度张角（角度放大效应适用范围内）

    img = imread('/Users/zhangchunhe/Desktop/mathmodel/data/reference/图4.png');
    img = im2double(img);

    % 2. 映射计算
    m = 400; n = 300;
    z_l = linspace(z_max, z_min, m);
    theta_k = linspace(-theta_max/2, theta_max/2, n);
    [THETA, Z] = meshgrid(theta_k, z_l);
    
    img_resized = imresize(img, [m, n]);
    R_chan = reshape(img_resized(:,:,1), [], 1);
    G_chan = reshape(img_resized(:,:,2), [], 1);
    B_chan = reshape(img_resized(:,:,3), [], 1);
    
    theta_flat = THETA(:); z_flat = Z(:);
    alpha = (zE - 2*z_flat) ./ (zE - z_flat);
    beta = z_flat ./ (zE - z_flat);
    
    rho = sqrt((alpha.*R).^2 + (beta.*D).^2 + 2.*alpha.*beta.*R.*D.*cos(theta_flat));
    y_term = alpha.*R.*sin(theta_flat) + beta.*D.*sin(2.*theta_flat);
    x_term = alpha.*R.*cos(theta_flat) + beta.*D.*cos(2.*theta_flat);
    phi = atan2(y_term, x_term);
    
    x_paper = rho .* sin(phi);
    y_paper = rho .* cos(phi);
    
    % 3. 生成 A4 横向画布 (X:[-14.85, 14.85], Y:[16.0, -5.0])
    disp('正在执行 90° 平滑插值（角度放大效应适用范围内）...');
    [grid_x, grid_y] = meshgrid(linspace(-14.85, 14.85, 2970), linspace(16.0, -5.0, 2100));
    
    grid_colors = ones(2100, 2970, 3);
    F_R = scatteredInterpolant(x_paper, y_paper, R_chan, 'natural', 'none');
    grid_colors(:,:,1) = F_R(grid_x, grid_y);
    F_G = scatteredInterpolant(x_paper, y_paper, G_chan, 'natural', 'none');
    grid_colors(:,:,2) = F_G(grid_x, grid_y);
    F_B = scatteredInterpolant(x_paper, y_paper, B_chan, 'natural', 'none');
    grid_colors(:,:,3) = F_B(grid_x, grid_y);
    grid_colors(isnan(grid_colors)) = 1;
    
    % 4. 绝对遮罩：挖空圆柱体
    dist_sq = grid_x.^2 + grid_y.^2;
    cylinder_mask = dist_sq <= R^2;
    grid_colors(repmat(cylinder_mask, [1, 1, 3])) = 1; 
    
    final_img = uint8(grid_colors * 255);
    
    % 5. 绘图与强制锁定横版比例
    f = figure('Visible', 'off');
    set(f, 'PaperUnits', 'centimeters', 'PaperPosition', [0 0 29.7 21.0]);
    ax = axes('Parent', f, 'Position', [0 0 1 1]);
    imshow(final_img, 'Parent', ax);
    hold on;
    
    % 标尺坐标 (1cm = 100像素)
    px_x = 1485; 
    px_y = 1600; 
    r_px = R * 100;
    axis_color = [0.4 0.4 0.4];
    
    % 画轴与刻度
    plot([1, 2970], [px_y, px_y], 'Color', axis_color, 'LineWidth', 2);
    plot([px_x, px_x], [1, 2100], 'Color', axis_color, 'LineWidth', 2);
    
    % X 轴与 Y 轴刻度线辅助
    for cm = -10:5:10
        plot([px_x + cm*100, px_x + cm*100], [px_y - 20, px_y + 20], 'Color', axis_color, 'LineWidth', 2);
    end
    for cm = -5:5:15
        plot([px_x - 20, px_x + 20], [px_y - cm*100, px_y - cm*100], 'Color', axis_color, 'LineWidth', 2);
    end
    
    % 画圆与中心标记
    theta_c = linspace(0, 2*pi, 100);
    plot(px_x + r_px*cos(theta_c), px_y + r_px*sin(theta_c), 'k', 'LineWidth', 4);
    plot(px_x, px_y, 'r+', 'MarkerSize', 15, 'LineWidth', 3);
    
    text(px_x + 50, px_y - 60, sprintf('Origin O(0,0)\nR=%.1fcm', R), 'FontSize', 20, 'Color', 'k', 'FontWeight', 'bold');
    text(2900, px_y - 30, 'X', 'FontSize', 22, 'Color', axis_color, 'FontWeight', 'bold');
    text(px_x + 30, 40, 'Y', 'FontSize', 22, 'Color', axis_color, 'FontWeight', 'bold');
    
    print(f, '/Users/zhangchunhe/Desktop/mathmodel/outputs/figures/draft/p4_2D_matlab.jpg', '-djpeg', '-r300');
    close(f);
    disp('成功！已生成 90° 张角小猫图纸（应呈漂亮半环）！');
end