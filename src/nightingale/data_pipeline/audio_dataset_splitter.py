import tensorflow as tf
from sklearn.model_selection import train_test_split

class AudioDatasetSplitter:
    """
    Utility class to split a dataframe of audio file paths and labels into
    TensorFlow datasets for training, validation and testing.

    Usage:
      splitter = AudioDatasetSplitter(filename_col='filename', label_col='target', seed=42)
      train_ds, val_ds, test_ds = splitter.build(df)

    Attributes:
      filename_col: Name of the dataframe column containing the audio file path.
      label_col: Name of the dataframe column containing the class label.
      seed: Random seed used for reproducible train/val/test splits.
      df: Internal copy of the dataframe provided to build().
      train_ds, val_ds, test_ds: tf.data.Dataset objects produced by build().
    """

    def __init__(self, filename_col='filename', label_col='target', seed=42):
        # Column names and RNG seed configuration
        self.filename_col = filename_col
        self.label_col = label_col
        self.seed = seed
        # Placeholder for the dataframe once build() is called
        self.df = None

    def build(self, df):
        """
        Create train/validation/test splits and return corresponding tf.data.Datasets.

        The function:
          - makes an internal copy of the provided dataframe,
          - performs a stratified split (60% train, 20% val, 20% test),
          - annotates the dataframe with a 'fold' column (1=train, 2=val, 3=test),
          - builds and returns datasets for each fold.

        Args:
          df: pandas.DataFrame containing at least filename_col and label_col.

        Returns:
          (train_ds, val_ds, test_ds): tuple of tf.data.Dataset objects where each
          yielded element is (wav_tensor, label).
        """
        # Work on a copy to avoid mutating caller's dataframe
        self.df = df.copy()

        # Split indices: first into train (60%) and temp (40%), then split temp into val/test evenly.
        train_idx, temp_idx = train_test_split(
            self.df.index, test_size=0.4, random_state=self.seed, stratify=self.df[self.label_col]
        )
        val_idx, test_idx = train_test_split(
            temp_idx, test_size=0.5, random_state=self.seed, stratify=self.df.loc[temp_idx, self.label_col]
        )

        # Annotate the dataframe with fold labels for later selection
        self.df['fold'] = ''
        self.df.loc[train_idx, 'fold'] = 1
        self.df.loc[val_idx, 'fold'] = 2
        self.df.loc[test_idx, 'fold'] = 3

        # Build tf.data.Datasets for each fold
        self.train_ds = self._build_dataset(1)
        self.val_ds   = self._build_dataset(2)
        self.test_ds  = self._build_dataset(3)

        return self.train_ds, self.val_ds, self.test_ds

    def _build_dataset(self, fold):
        """
        Construct a tf.data.Dataset for a given fold.

        The dataset is created from the filename and label columns and mapped through
        _load_wav to decode audio files into waveform tensors.

        Args:
          fold: integer 1/2/3 selecting train/val/test subset.

        Returns:
          A tf.data.Dataset yielding (wav_tensor, label).
        """
        subset = self.df[self.df['fold'] == fold]
        ds = tf.data.Dataset.from_tensor_slices(
            (subset[self.filename_col].to_numpy(), subset[self.label_col].to_numpy())
        )
        # Map the dataset to load and decode the wav files
        return ds.map(self._load_wav)

    @staticmethod
    def _load_wav(filename, label):
        """
        Read and decode a WAV file into a mono waveform tensor.

        Uses tf.io.read_file + tf.audio.decode_wav to load the file, squeezes the
        channel dimension so the returned tensor has shape [num_samples].

        Args:
          filename: path to the audio file (string tensor).
          label: associated label.

        Returns:
          (wav, label): tuple where wav is a 1-D float32 tensor and label is unchanged.
        """
        audio = tf.io.read_file(filename)
        wav, sr = tf.audio.decode_wav(audio, desired_channels=1)
        # Remove the trailing channel dimension -> shape [num_samples]
        wav = tf.squeeze(wav, axis=-1)
        return wav, label
