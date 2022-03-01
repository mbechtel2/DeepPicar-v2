#from keras_model import model
import tensorflow as tf
from tensorflow import keras
import numpy as np

model = keras.models.load_model('models/keras_model.h5')

frame = np.zeros((1,66,200,3), np.uint8)

output = model.predict(frame)[0][0]
print("Output: {}".format(output))