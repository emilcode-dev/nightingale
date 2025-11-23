import os
import librosa
import soundfile as sf
import numpy as np

class AudioPreprocessor:
    def __init__(self, target_sr=16000, mono=True):
        self.target_sr = target_sr
        self.mono = mono

    def is_yamnet_ready(self, file_path):
        """Check if audio file is already in correct format."""
        try:
            # Read audio info
            with sf.SoundFile(file_path) as f:
                sr = f.samplerate
                channels = f.channels
                ext = os.path.splitext(file_path)[1].lower()
                
            return ext == ".wav" and sr == self.target_sr and (channels == 1 if self.mono else True)
        except RuntimeError:
            # Can't read file
            return False

    def load_audio(self, file_path):
        """Load audio and convert if necessary"""
        if self.is_yamnet_ready(file_path):
            # Already ready, load directly
            waveform, sr = librosa.load(file_path, sr=None, mono=self.mono)
        else:
            # Load and resample/convert
            waveform, sr = librosa.load(file_path, sr=self.target_sr, mono=self.mono)
        
        waveform = waveform.astype(np.float32)
        return waveform, sr

    def save_wav(self, waveform, sr, output_path):
        sf.write(output_path, waveform, sr)


