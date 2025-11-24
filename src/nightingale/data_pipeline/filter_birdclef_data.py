import glob
import os
import pandas as pd

def load_birdclef_metadata(metadata_path="../data/birdclef-2024/train_metadata.csv",
                          audio_root="../data/birdclef-2024/train_audio_16"):
    """
    Load and filter BirdClef metadata to include only wav files present under audio_root.

    Args:
      metadata_path: Path to the CSV metadata file (e.g. ../data/birdclef-2024/train_metadata.csv).
      audio_root: Root folder containing audio files (e.g. ../data/birdclef-2024/train_audio_16).

    Returns:
      Tuple (filtered_bird_df, num_of_bird_classes_in_dataset)
        - filtered_bird_df: DataFrame with absolute paths in the 'filename' column and a 'target' column.
        - num_of_bird_classes_in_dataset: int count of unique bird classes present in the filtered set.
    """

    # Read metadata CSV
    bird_df = pd.read_csv(metadata_path)

    # Change the filename endings from .ogg to .wav in the filename column
    bird_df['filename'] = bird_df['filename'].str.replace('.ogg', '.wav', regex=False)

    # Find all wav files under audio_root and convert to relative paths for matching against metadata
    wav_paths = glob.glob(os.path.join(audio_root, "**", "*.wav"), recursive=True)
    wav_rel = [os.path.relpath(p, audio_root) for p in wav_paths]

    filtered_bird_df = bird_df[bird_df['filename'].isin(wav_rel)]

    bird_classes = list(set(filtered_bird_df['common_name']))
    num_of_bird_classes_in_dataset = len(bird_classes)

    map_class_to_id = {name: idx for idx, name in enumerate(bird_classes)}
    class_id = filtered_bird_df['common_name'].apply(lambda name: map_class_to_id[name])
    filtered_bird_df = filtered_bird_df.assign(target=class_id)

    # Convert filenames to absolute paths under audio_root
    full_path = filtered_bird_df['filename'].apply(lambda row: os.path.join(audio_root, row))
    filtered_bird_df = filtered_bird_df.assign(filename=full_path)

    return filtered_bird_df, num_of_bird_classes_in_dataset
