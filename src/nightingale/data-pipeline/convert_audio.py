import os
from pydub import AudioSegment

def convert_and_resample(input_file: str, output_file: str):
    """
    Converts an audio file to WAV format and resamples it to 16 kHz.
    Skips conversion if the output file already exists.

    Args:
        input_file (str): Path to the input audio file (e.g., .ogg, .mp3).
        output_file (str): Path to save the converted and resampled .wav file.
    """
    print("start conversion")
    if os.path.exists(output_file):
        print(f"Skipped (already exists): {output_file}")
        return

    try:
        # Load the input audio file
        audio = AudioSegment.from_file(input_file)
        #set quantisation
        audio_quant16 = audio.set_sample_width(2)  # 2 bytes = 16 bit
        # Resample to 16 kHz
        audio_16k = audio_quant16.set_frame_rate(16000)
        # Export as .wav
        audio_16k.export(output_file, format="wav")
        print(f"Conversion and resampling successful: {output_file}")
    except Exception as e:
        print(f"Error during conversion and resampling: {e}")


def batch_convert_and_resample(input_root, output_root, convert_and_resample, max_folders=None):
    """
    Walk through input_root, find all .ogg files, and convert them to .wav
    in output_root with the same folder structure.
    
    Parameters:
        input_root (str): Path to the root folder containing .ogg files.
        output_root (str): Path where converted .wav files will be saved.
        convert_and_resample (func): Function that takes (in_path, out_path).
        max_folders (int, optional): If set, only process the first N subfolders.
    """
    # List top-level subfolders in input_root
    subfolders = sorted(
        [os.path.join(input_root, d) for d in os.listdir(input_root) 
         if os.path.isdir(os.path.join(input_root, d))]
    )
    print("start conversion")
    # Limit to first N folders if requested
    if max_folders is not None:
        subfolders = subfolders[:max_folders]

    for folder in subfolders:
        for dirpath, _, filenames in os.walk(folder):
            for filename in filenames:
                if filename.lower().endswith(".ogg") or filename.lower().endswith(".wav"):
                    in_path = os.path.join(dirpath, filename)
                    
                    # Build matching output path
                    rel_path = os.path.relpath(in_path, input_root)
                    rel_path_no_ext = os.path.splitext(rel_path)[0] + ".wav"
                    out_path = os.path.join(output_root, rel_path_no_ext)

                    # Ensure output directory exists
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)

                    # Convert
                    convert_and_resample(in_path, out_path)
                    print(f"Converted: {in_path} -> {out_path}")