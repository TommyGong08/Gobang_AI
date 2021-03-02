# 用于编程测试一些函数
import numpy as np
from keras.models import load_model
model = load_model('model_200_10.h5')
x_input = np.zeros((1,361),dtype=int)
x_input[0,180] = 1
x_input[0,181] = 2
print(x_input)
print(x_input.shape)
score = model.predict(x_input) * 20000 - 10000
print(score)
score = score[0,0]
print(score)
print("------------")

