'''
设计一个BP神经网络用于大作业第三问 训练棋局的评估函数
BP神经网络结构：
    输入层：input_dim = 361(棋盘19*19）
    输出层：一个神经元
'''

import keras
from keras.models import model_from_json
from keras.layers import Dense,Dropout
from keras.optimizers import SGD
import re
import numpy as np
import matplotlib.pyplot as plt



# 写一个LossHistory类，保存loss和acc
class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = {'batch': [], 'epoch': []}
        self.accuracy = {'batch': [], 'epoch': []}
        self.val_loss = {'batch': [], 'epoch': []}
        self.val_acc = {'batch': [], 'epoch': []}

    def on_batch_end(self, batch, logs={}):
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('acc'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_acc'))


    def on_epoch_end(self, batch, logs={}):
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('acc'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_acc'))

    def loss_plot(self, loss_type):
        iters = range(len(self.losses[loss_type]))
        plt.figure()
        # acc
        plt.plot(iters, self.accuracy[loss_type], 'r', label='train acc')
        # loss
        plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
        if loss_type == 'epoch':
            # val_acc
            plt.plot(iters, self.val_acc[loss_type], 'b', label='val acc')
            # val_loss
            plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')
        plt.grid(True)
        plt.xlabel(loss_type)
        plt.ylabel('acc-loss')
        plt.legend(loc="upper right")
        plt.show()

dataset_size = 7541
# X_TRAIN = np.zeros((dataset_size,361),dtype=int)
# Y_TRAIN = np.zeros((dataset_size,1),dtype=int)

def load_data():
    i = 0
    X_TRAIN = np.zeros((dataset_size, 361), dtype=int)
    x_line = [[0 for col in range(361)] for row in range(dataset_size)]
    for line in open("x_train.txt"):
        x_line[i] = [int(s) for s in re.findall(r'\d+', line)]
        i += 1
    print(len(x_line))
    for i in range(dataset_size):
        x_train2 = np.array(x_line[i], dtype=int)
        x_train3 = x_train2.reshape(1,361)
        X_TRAIN[i] = x_train3
    # print(X_TRAIN)
    print(X_TRAIN.shape)
    print(X_TRAIN)

    i = 0
    y_train = [[0 for col in range(1)] for row in range(dataset_size)]
    for line in open("y_train.txt"):
        y_train[i] = line.splitlines()
        y_train[i] = list(map(float, y_train[i]))
        i += 1

    Y_TRAIN = np.array(y_train)
    print(Y_TRAIN.shape)
    print(Y_TRAIN)
    return X_TRAIN, Y_TRAIN

x_train,y_train = load_data()
# 构建模型
model = keras.Sequential()
model.add(Dense(32,activation='relu',input_dim=361))
# 为了防止过拟合，训练时丢弃某些神经元
# model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dense(128,activation='relu'))
model.add(Dense(64,activation='relu'))
model.add(Dense(8,activation='relu'))
# model.add(Dropout(0.5))
# 激活函数：
# softmax一般用于多分类问题
# relu可以用于回归问题
model.add(Dense(1,activation='relu'))
#sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
ada = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(loss='mse',
              optimizer=ada,
              metrics=['mae'])
print("~~~~~~~~")
model.summary()
#创建一个实例history
history = LossHistory()

# 训练模型
# hist = model.fit(X_TRAIN,Y_TRAIN,epochs=500,batch_size=10)
hist = model.fit(x_train,y_train,epochs=200,batch_size=15,callbacks=[history])

# 保存模型
model.save('2021.1.10_200_10.h5')

# # evaluate返回损失值和你选定的指标值
score = model.evaluate(x_train,y_train,batch_size=10)
print(score)

#绘制acc-loss曲线
history.loss_plot('epoch')