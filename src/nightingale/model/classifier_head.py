import tensorflow as tf
from tensorflow.keras.utils import register_keras_serializable

@register_keras_serializable()
class ClassifierHead(tf.keras.Model):
    def __init__(self, num_classes = 3, **kwargs):
        super().__init__(**kwargs)
        self.num_classes = num_classes
        self.dense1 = tf.keras.layers.Dense(512, activation='relu')
        self.dense2 = tf.keras.layers.Dense(num_classes, activation='softmax')

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        return x
    
    def get_config(self):
        base_config = super().get_config()
        config = {
            "num_classes": self.num_classes,
        }
        return {**base_config, **config}
