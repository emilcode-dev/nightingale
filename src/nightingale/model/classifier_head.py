import tensorflow as tf
from tensorflow.keras.utils import register_keras_serializable

@register_keras_serializable()
class ClassifierHead(tf.keras.Model):
    """
    A simple classifier head implemented as a Keras model.

    This model consists of two dense layers:
    
    - A fully connected layer with 512 units and ReLU activation.
    - An output layer with `num_classes` units and softmax activation.

    It can be used as the final classification head on top of
    a feature extractor in transfer learning or custom models.

    Parameters
    ----------
    num_classes : int, optional, default=3
        The number of output classes for classification.
    **kwargs : dict
        Additional keyword arguments passed to ``tf.keras.Model``.
    """
    def __init__(self, num_classes = 3, **kwargs):
        super().__init__(**kwargs)
        self.num_classes = num_classes
        self.dense1 = tf.keras.layers.Dense(512, activation='relu')
        self.dense2 = tf.keras.layers.Dense(num_classes, activation='softmax')

    def call(self, inputs):
        """
        Forward pass of the classifier head.

        Parameters
        ----------
        inputs : Input tensor to the model, typically output from a feature extractor.

        Returns
        -------
        The softmax probabilities for each class with shape
        ``(batch_size, num_classes)``.
        """
        x = self.dense1(inputs)
        x = self.dense2(x)
        return x
    
    def get_config(self):
        """
        Returns the configuration of the model for serialization.

        This method is used by Keras to save and load models.

        Returns
        -------
        dict
            A dictionary containing the model configuration, including
            ``num_classes`` and base Keras model configuration.
        """
        base_config = super().get_config()
        config = {
            "num_classes": self.num_classes,
        }
        return {**base_config, **config}
