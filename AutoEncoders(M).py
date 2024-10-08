from keras.layers import Layer, Dense, Dropout, Activation, Flatten, Reshape
import tensorflow as tf
from tensorflow import keras

import keras
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

from keras.datasets import mnist
from keras.models import Model
from keras.layers import Input, add
from keras import regularizers
from keras.regularizers import l2

#Loading the dataset
(X_train, _), (X_test, _) = mnist.load_data()

X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)  #For converting the data from Image-2D
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)

X_train = X_train.astype("float32")/255.   #FOR normalization
X_test = X_test.astype("float32")/255.

print('X_train shape:', X_train.shape)  #for checking no of samples in training and testing
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

X_train = X_train.reshape((len(X_train), np.prod(X_train.shape[1:])))  #For converting 2D to 1D
X_test = X_test.reshape((len(X_test), np.prod(X_test.shape[1:])))

input_size = 784
hidden_size = 64
output_size = 784

x = Input(shape=(input_size,))   #Backpropagation
h = Dense(hidden_size, activation='relu')(x)
r = Dense(output_size, activation='sigmoid')(h)

autoencoder = Model(inputs=x, outputs=r)
autoencoder.compile(optimizer='adam', loss='mse')

epochs = 5  #for training the data
batch_size = 100

history = autoencoder.fit(X_train, X_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(X_test, X_test))

conv_encoder = Model(x, h)
encoded_imgs = conv_encoder.predict(X_test)

n = 10             #encoding data at hidden layer
plt.figure(figsize=(20, 8))
for i in range(n):
    ax = plt.subplot(1, n, i+1)
    plt.imshow(encoded_imgs[i].reshape(4, 16).T)
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()

decoded_imgs = autoencoder.predict(X_test)

n = 10    #for plotting of 1st 10 numbers of the test set
plt.figure(figsize=(20, 6))
for i in range(n):
    # display original
    ax = plt.subplot(3, n, i+1)
    plt.imshow(X_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)


    # display reconstruction
    ax = plt.subplot(3, n, i+n+1)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

plt.show()

print(history.history.keys())

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()