import sys
sys.path.append('../../')

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import json
import matplotlib.pyplot as plt
import numpy as np
import h5py
from utils.metrics import precision

epochs =  50
batch_size=64

data = None
with open('../../data/data_20170722_02/data.json', 'r') as f:
    data = json.load(f)

if data is None:
    print('data is None')
    exit(1)

x_data = np.array(data[0])
y_data = np.array(data[1])

train_len = int(len(x_data)*0.9)
x_train = x_data[0:train_len]
y_train = y_data[0:train_len]
x_test = x_data[train_len:]
y_test = y_data[train_len:]
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)
data_dim = len(x_train[0][0])
print(data_dim)
timesteps = len(x_train[0])
print(timesteps)

# expected input data shape: (batch_size, timesteps, data_dim)
model = Sequential()
model.add(LSTM(32, return_sequences=True,
               input_shape=(timesteps, data_dim)))  # returns a sequence of vectors of dimension 32
model.add(LSTM(32, return_sequences=True))  # returns a sequence of vectors of dimension 32
model.add(LSTM(32))  # return a single vector of dimension 32
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy', precision])

# model.load_weights('./model_weights.h5')

history = model.fit(x_train, y_train,
          epochs=epochs,
          batch_size=batch_size,
          verbose=1,
          validation_split=0.1)

model.save_weights('./model_weights.h5')

score = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=1)
print(score)

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.plot(history.history['precision'])
plt.plot(history.history['val_precision'])
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model accuracy, precision and loss')
plt.ylabel('accuracy, precision or loss')
plt.xlabel('epoch')
plt.legend(['train_acc', 'val_acc', 'train_precision', 'val_precision', 'train_loss', 'val_loss'], loc='upper left')
plt.show()