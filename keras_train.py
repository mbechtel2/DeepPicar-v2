from keras_model import model
import tensorflow as tf
import numpy as np
import params
import data_shuffled as data
import local_common as cm

if params.shuffle_training:
    data.load_imgs()

x_train = np.asarray(data.imgs['train'])
x_val = np.asarray(data.imgs['val'])

y_train = np.asarray(data.wheels['train'])
y_val = np.asarray(data.wheels['val'])

#print(x_train[0])


model.compile(optimizer=tf.keras.optimizers.Adam(1e-4),
                loss='mse', metrics=['mae'])

history = model.fit(x_train, y_train, batch_size=100,
                    epochs=20, validation_data=(x_val, y_val))
                    
model.save('models/keras_model.h5')                    
