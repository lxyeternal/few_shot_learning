# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 14:35
# @Author  : blue
# @FileName: gru.py
# @Software: PyCharm


import numpy as np
from keras.models import Sequential
from keras.layers import GRU, Flatten, Dense, Dropout
from keras.utils import to_categorical


class GRUModel:
    def __init__(self, train_data, train_label, test_data, test_label, num_classes):
        self.train_data = train_data
        self.train_label = to_categorical(train_label, num_classes)  # One-hot encoding of labels
        self.test_data = test_data
        self.test_label = to_categorical(test_label, num_classes)  # One-hot encoding of labels
        self.units = 128
        self.batch_size = 128
        self.epochs = 10
        self.num_classes = num_classes

    def preprocess_data(self, train_data, max_tokens=800):
        # Initialize a zero array of the correct shape
        processed_data = np.zeros((len(train_data), max_tokens, 300))
        # Fill the data into the array
        for i, sample in enumerate(train_data):
            processed_data[i, :min(len(sample), max_tokens)] = sample[:max_tokens]
        return processed_data

    def gru_alg(self):
        self.train_data = self.preprocess_data(self.train_data)
        self.test_data = self.preprocess_data(self.test_data)

        model = Sequential()
        model.add(GRU(self.units, return_sequences=True, input_shape=(self.train_data.shape[1], self.train_data.shape[2])))
        model.add(GRU(self.units, return_sequences=True))
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

        print("[INFO] Successfully initialize a GRU model!")
        print("[INFO] Training the model...")
        model.fit(self.train_data, self.train_label, batch_size=self.batch_size, epochs=self.epochs, verbose=1)

        # Evaluating the model
        score = model.evaluate(self.test_data, self.test_label, verbose=0)
        print('Test score:', score[0])
        print('Test accuracy:', score[1])