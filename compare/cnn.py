# -*- coding: utf-8 -*-
# @Time    : 2021/3/8 11:20
# @Author  : blue
# @FileName: cnn.py
# @Software: PyCharm

import numpy as np
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.utils import to_categorical


class CNNModel:
    def __init__(self, train_data, train_label, test_data, test_label, num_classes):
        self.train_data = train_data
        self.train_label = to_categorical(train_label, num_classes)  # One-hot encoding of labels
        self.test_data = test_data
        self.test_label = to_categorical(test_label, num_classes)  # One-hot encoding of labels
        self.num_classes = num_classes
        self.first_filters = 64
        self.second_filters = 128
        self.third_filters = 256
        self.kernel_size = (1, 3)
        self.pool_size = (1, 2)
        self.input_shape = (0, 0, 0)  # Adjusting input shape
        self.batch_size = 128
        self.epochs = 10

    def preprocess_data(self, train_data, max_tokens=800):
        # Initialize a zero array of the correct shape
        processed_data = np.zeros((len(train_data), max_tokens, 300))
        # Fill the data into the array
        for i, sample in enumerate(train_data):
            processed_data[i, :min(len(sample), max_tokens)] = sample[:max_tokens]
        processed_data = processed_data.reshape(processed_data.shape[0], processed_data.shape[1],
                                                processed_data.shape[2], 1)
        return processed_data

    def cnn_alg(self):
        self.train_data = self.preprocess_data(self.train_data)
        self.test_data = self.preprocess_data(self.test_data)
        self.input_shape = (self.train_data.shape[1], self.train_data.shape[2], 1)
        model = Sequential()
        model.add(Convolution2D(self.first_filters, self.kernel_size, padding='valid', strides=1,
                                input_shape=self.input_shape))
        model.add(Convolution2D(self.first_filters, self.kernel_size, padding='valid', strides=1))
        model.add(MaxPooling2D(pool_size=self.pool_size))

        model.add(Convolution2D(self.second_filters, self.kernel_size, padding='valid', strides=1))
        model.add(Convolution2D(self.second_filters, self.kernel_size, padding='same', strides=1))
        model.add(Convolution2D(self.second_filters, self.kernel_size, padding='same', strides=1))
        model.add(MaxPooling2D(pool_size=self.pool_size))

        model.add(Convolution2D(self.third_filters, self.kernel_size, padding='same', strides=1))
        model.add(Convolution2D(self.third_filters, self.kernel_size, padding='same', strides=1))
        model.add(Convolution2D(self.third_filters, self.kernel_size, padding='same', strides=1))
        model.add(MaxPooling2D(pool_size=self.pool_size))

        model.add(Flatten())
        model.add(Dense(100, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(20, activation='relu'))
        model.add(Dense(self.num_classes, activation='softmax'))  # Adjusting the output layer for multi-class classification

        model.summary()

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',  # Adjusting the loss for multi-class classification
            metrics=['accuracy'],
        )

        print("[INFO] Successfully initialize a CNN model!")
        print("[INFO] Training the model...")
        model.fit(self.train_data, self.train_label, batch_size=self.batch_size, epochs=self.epochs, verbose=1)

        # Evaluating the model
        score = model.evaluate(self.test_data, self.test_label, verbose=0)
        print('Test score:', score[0])
        print('Test accuracy:', score[1])