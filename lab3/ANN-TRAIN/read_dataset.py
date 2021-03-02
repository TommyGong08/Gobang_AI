'''用来测试读取训练集'''
import re
import numpy as np
dataset_size = 28

# 读取x_train
i = 0
x_line = [[0 for col in range(361)] for row in range(dataset_size)]
for line in open("../../dataset/x_train.txt"):
    x_line[i] = [int(s) for s in re.findall(r'\d+', line)]
    i += 1
print(len(x_line))
X_TRAIN = np.zeros((dataset_size,361),dtype=int)
for i in range(dataset_size):
    x_train2 = np.array(x_line[i], dtype=int)
    x_train3 = x_train2.reshape(1,361)
    X_TRAIN[i] = x_train3
print(X_TRAIN)
print(X_TRAIN.shape)

i = 0
y_train = [[0 for col in range(1)] for row in range(dataset_size)]
for line in open("../../dataset/y_train.txt"):
    y_train[i] = line.splitlines()
    y_train[i] = list(map(int, y_train[i]))
    i += 1

y_train2 = np.array(y_train)
print(y_train2.shape)
print(y_train2)
