clear; clc; close all;

filename = 'example1.dat';  
k = 3;                     
sigma = 1.0;              


if isfile(filename)
    raw_data = load(filename);
else
    fprintf('File not found\n');
     
end

fprintf('Running Spectral Clustering...\n');
[labels, Y_matrix, L_matrix] = spectral_clustering(raw_data, k, sigma);

figure('Name', 'Spectral Clustering Results', 'Color', 'w');

subplot(1, 2, 1);
gscatter(raw_data(:,1), raw_data(:,2), labels);
title('Final Clustering Result');
xlabel('Feature 1'); ylabel('Feature 2');
grid on; legend off;


subplot(1, 2, 2);
if k == 2
    gscatter(Y_matrix(:,1), Y_matrix(:,2), labels);
    title('Projected Space (Matrix Y)');
    axis equal; % Make sure circles look like circles
elseif k >= 3
    scatter3(Y_matrix(:,1), Y_matrix(:,2), Y_matrix(:,3), 15, labels, 'filled');
    title('Projected Space (Matrix Y)');
end
grid on;

fprintf('Done! Check the plot window.\n');
