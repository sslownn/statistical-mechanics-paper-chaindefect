import math
import numpy as np

def sin_wave(x, y):
    return math.sin(x) * math.sin(y)

num_particles = 400
max_displacement = 0.9
num_frames = 300

# 初始化粒子位置
particles = np.random.rand(num_particles, 2) * 2 * math.pi  # 生成0-2π之间的随机位置

# 初始化粒子速度
velocities = np.random.uniform(-1, 1, (num_particles, 2)) * max_displacement

for frame in range(num_frames):
    # 计算粒子新的位置
    particles += velocities
    
    # 限制粒子位置在0-2π之间
    particles %= 2 * math.pi

    # 计算粒子 z 坐标
    z_coords = np.array([sin_wave(p[0], p[1]) for p in particles])

    # 输出 x, y, z 坐标到 CSV 文件
    with open('output.csv', 'a') as f:
        for i in range(num_particles):
            f.write(f"{particles[i, 0]},{particles[i, 1]},{z_coords[i]}\n")