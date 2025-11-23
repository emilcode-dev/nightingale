import glob
import os
import pandas as pd

def load_birdclef_metadata(base_data_path="../data/birdclef-2024"):

    # Read train meta data
    base_data_path = "../data/birdclef-2024"
    bird_metadata_path = os.path.join(base_data_path, "train_metadata.csv")
    bird_df = pd.read_csv(bird_metadata_path)

    # Change the filename endings from .ogg to .wav in the filename column of bird_df
    bird_df['filename'] = bird_df['filename'].str.replace('.ogg', '.wav', regex=False)

    # Show rows where the filename matches the pattern "cohcuc1/*.wav"
    wav_files = glob.glob(base_data_path + "/train_audio_16/**/*.wav", recursive=True)
    wav_files = [f.replace(base_data_path + "/train_audio_16/", "") for f in wav_files]

    filtered_bird_df = bird_df[bird_df['filename'].isin(wav_files)]

    bird_classes = list(set(filtered_bird_df['common_name']))

    map_class_to_id = {name: idx for idx, name in enumerate(bird_classes)}

    class_id = filtered_bird_df['common_name'].apply(lambda name: map_class_to_id[name])
    filtered_bird_df = filtered_bird_df.assign(target=class_id)

    full_path = filtered_bird_df['filename'].apply(lambda row: os.path.join(base_data_path + "/train_audio_16/", row))
    filtered_bird_df = filtered_bird_df.assign(filename=full_path)

    return filtered_bird_df
