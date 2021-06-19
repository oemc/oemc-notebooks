import numpy as np
import tensorflow as tf

filModel = tf.keras.models.load_model('./weights.h5')

def Predict(board):
    oneDimArray = []
    for column in board:
        for row in column:
            oneDimArray.append(1 if row == 0 else -1 if row == 1 else 0)
        for i in range(6 - len(column)):
            oneDimArray.append(0)
    x = np.reshape(oneDimArray, (1,6,7,1))
    return filModel.predict(x)
