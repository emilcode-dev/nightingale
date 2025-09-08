import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.saving import register_keras_serializable

@register_keras_serializable(package="nightingale.model")
class ClassifierHead(keras.Model):
    def __init__(self, num_classes: int = 3):
        super().__init__()
        self.dense1 = layers.Dense(512, activation='relu')
        self.dense2 = layers.Dense(num_classes, activation='softmax')

    def call(self, inputs, training=False):
        x = self.dense1(inputs)
        return self.dense2(x)
