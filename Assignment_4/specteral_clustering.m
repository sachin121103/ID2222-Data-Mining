% Clear memory and close old plots
clear; clc; close all;

% --- 1. SETTINGS ---
filename = 'example1.dat';  % CHANGE THIS to your actual file name
k = 3;                     % Number of clusters to find
sigma = 1.0;               % Scaling parameter (adjust if results look bad)

% --- 2. LOAD DATA ---
% Check if the file exists first
if isfile(filename)
    % Load data into a matrix
    % 'load' works for space-separated .dat files
    raw_data = load(filename);
else
    % If you don't have a file yet, let's create dummy data 
    % so you can see the code running immediately.
    fprintf('File not found. Generating dummy concentric circles...\n');
    theta = linspace(0,2*pi, 200)';
    % Circle 1 (inner)
    c1 = [3*cos(theta), 3*sin(theta)] + 0.1*randn(200,2);
    % Circle 2 (outer)
    c2 = [6*cos(theta), 6*sin(theta)] + 0.1*randn(200,2);
    raw_data = [c1; c2];
    k = 2; % Force k=2 for this dummy example
end

% --- 3. RUN ALGORITHM ---
fprintf('Running Spectral Clustering...\n');
[labels, Y_matrix, L_matrix] = spectral_clustering(raw_data, k, sigma);

% --- 4. VISUALIZATION ---
figure('Name', 'Spectral Clustering Results', 'Color', 'w');

% Subplot 1: The Result
subplot(1, 2, 1);
% gscatter automatically colors points by group 'labels'
gscatter(raw_data(:,1), raw_data(:,2), labels);
title('Final Clustering Result');
xlabel('Feature 1'); ylabel('Feature 2');
grid on; legend off;

% Subplot 2: The Spectral Embedding (The Y Matrix)
% This shows what the algorithm "sees" (points on a circle/sphere)
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
