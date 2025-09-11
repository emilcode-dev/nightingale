from pydub import AudioSegment
import tensorflow as tf

def load_wav_16k_mono(filename):
    """ Load a WAV file, convert it to a float tensor, resample to 16 kHz single-channel audio. """
    file_contents = tf.io.read_file(filename)
    wav, sample_rate = tf.audio.decode_wav(
          file_contents,
          desired_channels=1)
    wav = tf.squeeze(wav, axis=-1)
    
    #sample_rate = tf.cast(sample_rate, dtype=tf.int64)
    #wav = tfio.audio.resample(wav, rate_in=sample_rate, rate_out=16000)
    return wav