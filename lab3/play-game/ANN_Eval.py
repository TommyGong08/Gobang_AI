import numpy as np
import h5py
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
from keras.models import load_model
import keras
from keras.models import model_from_json
from keras.layers import Dense,Dropout
from keras.models import Model
from keras.layers import Input, Dense


#load net work
model = model_from_json(open('model2_arch.json').read())
model.load_weights('model2_weight.h5')
ada = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(loss='mse',
              optimizer=ada,
              metrics=['mae'])

#
# def get_score_ANN(self):
#     x_input = np.zeros((1, 361), dtype=int)
#     for j in range(20):
#         for i in range(20):
#             x_input[:, j * 19 + i] = self.board[j][i]
#     print(x_input.shape)
#     score = model.predict(x_input) * 20000 - 10000
#     return score


