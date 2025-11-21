import tensorflow_hub as hub
import tensorflow as tf

class YamnetEmbedding(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.yamnet = hub.KerasLayer("https://tfhub.dev/google/yamnet/1")

    def call(self, audio_waveform, label):
        scores, embeddings, spectrogram = self.yamnet(audio_waveform)
        num_embeddings = tf.shape(embeddings)[0]
        return (embeddings, tf.repeat(label, num_embeddings))



