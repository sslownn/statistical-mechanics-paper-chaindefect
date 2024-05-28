import paramiko
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


# 连接到SFTP服务器
transport = paramiko.Transport((hostname, port))
transport.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)


data = []

def read_average_file(file_path):
    with sftp.open(file_path) as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            if len(parts) >= 5:
                data.append((float(parts[0]), float(parts[1]), float(parts[4])))

for dirname in sftp.listdir(base_path):
    dir_path = os.path.join(base_path, dirname)
    if sftp.stat(dir_path).st_mode & 0o040000:  # 检查是否为目录
        avg_file_path = os.path.join(dir_path, 'Average.txt')
        try:
            read_average_file(avg_file_path)
        except Exception as e:
            print(f"Failed to read {avg_file_path}: {e}")

sftp.close()
transport.close()

# 将数据转换为DataFrame
df = pd.DataFrame(data, columns=['x', 'y', 'phase'])

# 设置颜色映射
cmap = 'viridis'

# 插值
xi = np.linspace(df['x'].min(), df['x'].max(), 500)
yi = np.linspace(df['y'].min(), df['y'].max(), 500)
zi = griddata((df['x'], df['y']), df['phase'], (xi[None, :], yi[:, None]), method='linear')

# 绘图
plt.figure(figsize=(10, 8))
contour = plt.contourf(xi, yi, zi, levels=np.linspace(0, 1, 100), cmap=cmap)
plt.colorbar(contour, label='Phase Category')

# 标出临界点的虚线
plt.axvline(x=1.0, color='gray', linestyle='--')  # 替换为你的实际临界点
plt.axhline(y=1.0, color='gray', linestyle='--')  # 替换为你的实际临界点
plt.axvline(x=5.0, color='white', linestyle='--')  # 替换为你的实际临界点
plt.axhline(y=5.0, color='white', linestyle='--')  # 替换为你的实际临界点

plt.xlabel('First Column (x)')
plt.ylabel('Second Column (y)')
plt.title('Phase Diagram')

# 保存为JPG文件
output_file = 'phase_diagram4.jpg'
plt.savefig(output_file)

print(f"Plot saved as {output_file}")





