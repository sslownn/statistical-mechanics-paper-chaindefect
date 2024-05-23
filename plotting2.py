import paramiko
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# SFTP服务器信息
hostname = '10.158.198.180'
port = 22
username = 'undergrads'
password = 'undergrads'  # 替换为实际的密码

# 连接到SFTP服务器
transport = paramiko.Transport((hostname, port))
transport.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)

# 读取数据
base_path = '/home/undergrads/n=20/'
data = []

def read_average_file(file_path):
    with sftp.open(file_path) as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            if len(parts) >= 5:
                data.append((float(parts[0]), float(parts[2]), float(parts[4])))

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
df = pd.DataFrame(data, columns=['x', 'y1', 'y2'])

# 绘图
plt.figure(figsize=(10, 8))

# 划分区域并添加背景颜色
x = np.linspace(df['x'].min(), df['x'].max(), 500)
y_gas = np.full_like(x, 0.3)
y_liquid = np.full_like(x, 0.7)

plt.fill_between(x, 0, 0.3, color='blue', alpha=0.1, label='Gas')
plt.fill_between(x, 0.3, 0.7, color='green', alpha=0.1, label='Liquid')
plt.fill_between(x, 0.7, 1, color='red', alpha=0.1, label='Glass')

# 绘制散点图
plt.scatter(df['x'], df['y1'], color='blue', label='y1', alpha=0.6)
plt.scatter(df['x'], df['y2'], color='red', label='y2', alpha=0.6)

# 添加图例
plt.legend()

# 添加标签和标题
plt.xlabel('First Column (x)')
plt.ylabel('Phase Category')
plt.title('Phase Diagram')

# 保存为JPG文件
output_file = 'phase_diagram.jpg'
plt.savefig(output_file)

print(f"Plot saved as {output_file}")
