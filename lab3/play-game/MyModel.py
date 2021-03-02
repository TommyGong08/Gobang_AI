# 用于加载模型和拟合评估值
import numpy as np
from keras.models import load_model

class Model:
    def __init__(self):
        # 选择想要加载的模型
        self.model = load_model('2021.1.10_200_10.h5')

    # 输入当前局面，输出评估函数
    def get_score_ANN(self, board):
        x_input = np.zeros((1, 361), dtype=int)
        # print(x_input.shape)
        for j in range(19):
            for i in range(19):
                x_input[0, j * 19 + i] = board[j][i]
        score = self.model.predict(x_input) * 20000 - 10000
        score = -score[0, 0]
        if score > 10000:
            score = 10000
        elif score < -10000:
            score = -10000
        return int(score)