import os
import librosa
import soundfile as sf
import numpy as np

class AudioPreprocessor:
    """
    Helper for loading, converting, resampling and saving audio files to a
    format suitable for YAMNet (16 kHz mono WAV by default).

    Responsibilities:
      - Check whether a file already matches the target format (is_yamnet_ready)
      - Load an audio file, resampling/mono-converting when necessary (load_audio)
      - Write a waveform to disk as WAV, creating parent folders if needed (save_wav)
      - Process a single file, skipping if already processed (process_file)
      - Walk an input folder tree and process all supported audio files while
        preserving folder structure under an output root (process_folder)

    The class intentionally does not alter the audio data beyond resampling
    and channel conversion. It returns/accepts numpy float32 waveforms and
    uses soundfile for saving to ensure stable WAV output.
    """

    def __init__(self, target_sr=16000, mono=True):
        # Target sample rate for YAMNet and whether to force mono output.
        self.target_sr = target_sr
        self.mono = mono

    def is_yamnet_ready(self, file_path):
        """
        Quick check whether the given file is already a WAV with the target
        sample rate and (optionally) a single channel.

        Returns:
          True when the file is a .wav with sample rate == target_sr and,
          if mono==True, has 1 channel. False for any error or mismatch.
        """
        try:
            # Use soundfile to inspect headers without decoding entire file.
            with sf.SoundFile(file_path) as f:
                sr = f.samplerate
                channels = f.channels
                ext = os.path.splitext(file_path)[1].lower()
            # Match extension, sample rate and channel count (if required).
            return ext == ".wav" and sr == self.target_sr and (channels == 1 if self.mono else True)
        except:
            # If file can't be opened or inspected, treat as not-ready.
            return False

    def load_audio(self, file_path):
        """
        Load audio into a numpy float32 waveform.

        If the file is already YAMNet-ready (checked by is_yamnet_ready) the
        function loads it without resampling to keep original samples when
        possible. Otherwise it forces resampling to target_sr and mono according
        to the object configuration.

        Returns:
          (wav, sr) where wav is a 1-D numpy.float32 array and sr == target_sr.
        """
        # If file already matches the desired format, load raw (no resample).
        if self.is_yamnet_ready(file_path):
            wav, sr = librosa.load(file_path, sr=None, mono=self.mono)
        else:
            # Force conversion/resampling to target sample rate and channel config.
            wav, sr = librosa.load(file_path, sr=self.target_sr, mono=self.mono)
        # Ensure dtype is float32 which downstream models expect.
        return wav.astype(np.float32), self.target_sr

    def save_wav(self, waveform, sr, output_path):
        """
        Save a numpy waveform to disk as a WAV file.

        Ensures parent directories exist before writing.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        sf.write(output_path, waveform, sr)

    def process_file(self, input_file, output_file):
        """
        Convert and save a single input file to the output path.

        Behavior:
          - If output_file already exists, skip processing.
          - Otherwise load (and convert/resample if needed) and save as WAV.
          - Prints simple status messages; exceptions are caught and printed.
        """
        if os.path.exists(output_file):
            print(f"Skipped (already exists): {output_file}")
            return

        try:
            wav, sr = self.load_audio(input_file)
            self.save_wav(wav, sr, output_file)
            print(f"Processed: {output_file}")
        except Exception as e:
            # Do not raise here; just report the problem and continue processing other files.
            print(f"Error processing {input_file}: {e}")

    def process_folder(self, input_root, output_root, max_folders=None):
        """
        Recursively process supported audio files under input_root and write
        converted files under output_root while preserving relative paths.

        Args:
          input_root: top-level folder to traverse.
          output_root: destination root where converted files will be placed.
          max_folders: optional int to limit number of top-level subfolders processed.

        Notes:
          - Only files with extensions (ogg, wav, mp3, flac) are processed.
          - The folder traversal preserves the input folder structure relative to input_root.
        """
        # Collect immediate subfolders under the input root (sorted for determinism).
        subfolders = sorted(
            [os.path.join(input_root, d) for d in os.listdir(input_root)
             if os.path.isdir(os.path.join(input_root, d))]
        )

        # Optionally limit the number of subfolders to process.
        if max_folders is not None:
            subfolders = subfolders[:max_folders]

        print(f"Processing {len(subfolders)} folders")

        # Walk each selected subfolder recursively and process supported files.
        for folder in subfolders:
            for dirpath, _, filenames in os.walk(folder):
                for filename in filenames:
                    if filename.lower().endswith((".ogg", ".wav", ".mp3", ".flac")):
                        in_path = os.path.join(dirpath, filename)

                        # Build output path that mirrors the input structure and ensures .wav extension.
                        rel_path = os.path.relpath(in_path, input_root)
                        rel_path = os.path.splitext(rel_path)[0] + ".wav"
                        out_path = os.path.join(output_root, rel_path)

                        self.process_file(in_path, out_path)
