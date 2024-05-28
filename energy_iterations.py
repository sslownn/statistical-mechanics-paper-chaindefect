import matplotlib.pyplot as plt

# 读取第一个文件的第一列数据

data1 = []
with open(file1, 'r') as f:
    for line in f:
        values = line.split()
        if values:  # 确保行不为空
            data1.append(float(values[0]))

# 读取第二个文件的第一列数据

data2 = []
with open(file2, 'r') as f:
    for line in f:
        values = line.split()
        if values:  # 确保行不为空
            data2.append(float(values[0]))

# 绘制数据
plt.plot(range(len(data1)), data1, label='Data from first file', color='b')
plt.plot(range(len(data2)), data2, label='Data from second file', color='r')
plt.xlabel('Index')
plt.ylabel('Energy / eV')
plt.legend()
plt.title('Comparison of two model energy iterations')

output_file = 'energyiterations.jpg'

# 保存图片
plt.savefig(output_file)
print(f"Plot saved as {output_file}")
