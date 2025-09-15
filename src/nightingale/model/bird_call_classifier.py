import tensorflow_hub as hub
import tensorflow as tf
from nightingale.model.classifier_head import ClassifierHead

class BirdCallClassifier():
    def __init__(self):
        self.yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')
        self.classifier_head = tf.keras.models.load_model('bird_classifier_head.keras')
        self.bird_classes = ['Intermediate Egret', 'Common Hawk-Cuckoo', "Tickell's Leaf Warbler"]  # Example classes

    def predict(self, inputs):
        _, embeddings, _ = self.yamnet_model(inputs)
        result = self.classifier_head(embeddings).numpy()
        inferred_class = self.bird_classes[result.mean(axis=0).argmax()]

        return inferred_class