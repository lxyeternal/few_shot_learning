# import re
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.signal import savgol_filter

# # 从文件中读取数据
# with open('new_induction_eval.txt', 'r') as file:
#     data = file.read()

# # 使用正则表达式提取数值
# steps = re.findall(r'step: (\d+)', data)
# losses = re.findall(r'loss: (\d+\.\d+)', data)
# accs = re.findall(r'acc: (\d+\.\d+)', data)
# recalls = re.findall(r'recall: (\d+\.\d+)', data)
# precisions = re.findall(r'precision: (\d+\.\d+)', data)
# f_betas = re.findall(r'f_beta: (\d+\.\d+)', data)

# # 将字符串转换为浮点数
# steps = np.array([int(step) for step in steps])
# losses = np.array([float(loss) for loss in losses])
# accs = np.array([float(acc) for acc in accs])
# recalls = np.array([float(recall) for recall in recalls])
# precisions = np.array([float(precision) for precision in precisions])
# f_betas = np.array([float(f_beta) for f_beta in f_betas])

# # 找到所有指标中的最短长度
# min_length = min(len(steps), len(losses), len(accs), len(recalls), len(precisions), len(f_betas))

# # 将所有数组截断到最短长度
# steps = steps[:min_length]
# losses = losses[:min_length]
# accs = accs[:min_length]
# recalls = recalls[:min_length]
# precisions = precisions[:min_length]
# f_betas = f_betas[:min_length]

# # 定义异常值处理函数
# def remove_outliers(data, threshold=4):
#     z_scores = (data - np.mean(data)) / np.std(data)
#     return data[np.abs(z_scores) < threshold]

# # 对数据进行异常值处理
# losses = remove_outliers(losses)
# accs = remove_outliers(accs)
# recalls = remove_outliers(recalls)
# precisions = remove_outliers(precisions)
# f_betas = remove_outliers(f_betas)

# # 确保所有数组的长度一致
# min_length = min(len(steps), len(losses), len(accs), len(recalls), len(precisions), len(f_betas))
# steps = steps[:min_length]
# losses = losses[:min_length]
# accs = accs[:min_length]
# recalls = recalls[:min_length]
# precisions = precisions[:min_length]
# f_betas = f_betas[:min_length]

# # 使用 Savitzky-Golay 滤波器平滑曲线
# window_length = 101  # 增大滤波器窗口长度
# polyorder = 3  # 多项式阶数,可以根据需要调整
# smoothed_losses = savgol_filter(losses, window_length, polyorder)
# smoothed_accs = savgol_filter(accs, window_length, polyorder)
# smoothed_recalls = savgol_filter(recalls, window_length, polyorder)
# smoothed_precisions = savgol_filter(precisions, window_length, polyorder)
# smoothed_f_betas = savgol_filter(f_betas, window_length, polyorder)

# # 绘制曲线图
# fig, ax1 = plt.subplots(figsize=(10, 6))
# ax1.plot(steps, smoothed_accs, label='Accuracy')
# ax1.plot(steps, smoothed_recalls, label='Recall')
# ax1.plot(steps, smoothed_precisions, label='Precision')
# ax1.plot(steps, smoothed_f_betas, label='F-beta')
# ax1.set_xlabel('Step')
# ax1.set_ylabel('Metric')
# ax1.set_title('Training Metrics (Smoothed)')
# ax1.legend(loc='lower right')
# ax1.grid(True)

# ax2 = ax1.twinx()  # 创建共享 x 轴的第二个 y 轴
# ax2.plot(steps, smoothed_losses, label='Loss', color='red')
# ax2.set_ylabel('Loss')
# ax2.legend(loc='upper right')

# plt.tight_layout()
# plt.savefig('eval_metrics_smoothed_optimized.png')  # 指定文件名
# plt.show()


import re
import matplotlib.pyplot as plt

# 从文件中读取数据
with open('new_induction_train.txt', 'r') as file:
    data = file.read()

# 使用正则表达式提取数值
steps = re.findall(r'step: (\d+)', data)
losses = re.findall(r'loss: (\d+\.\d+)', data)
accs = re.findall(r'acc: (\d+\.\d+)', data)
recalls = re.findall(r'recall: (\d+\.\d+)', data)
precisions = re.findall(r'precision: (\d+\.\d+)', data)
f_betas = re.findall(r'f_beta: (\d+\.\d+)', data)

# 将字符串转换为浮点数
steps = [int(step) for step in steps]
losses = [float(loss) for loss in losses]
accs = [float(acc) for acc in accs]
recalls = [float(recall) for recall in recalls]
precisions = [float(precision) for precision in precisions]
f_betas = [float(f_beta) for f_beta in f_betas]

# 创建图形和主次 y 轴
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

# 在主 y 轴上绘制 Accuracy、Recall、Precision 和 F-beta 曲线
ax1.plot(steps, accs, label='Accuracy')
ax1.plot(steps, recalls, label='Recall')
ax1.plot(steps, precisions, label='Precision')
ax1.plot(steps, f_betas, label='F-beta')
ax1.set_xlabel('Step')
ax1.set_ylabel('Metric')
ax1.legend(loc='upper left')
ax1.grid(True)

# 在次 y 轴上绘制 Loss 曲线
ax2.plot(steps, losses, label='Loss', color='blue')
ax2.set_ylabel('Loss')
ax2.legend(loc='upper right')

# 设置图的标题
plt.title('Training Metrics')

# 调整布局以避免重叠
plt.tight_layout()

# 保存图片
plt.savefig('training_metrics_with_loss.png')  # 指定文件名和格式
plt.show()