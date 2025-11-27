import os
from pathlib import Path

import numpy as np
import soundfile as sf
import pytest

from nightingale.data_pipeline.audio_preprocessor import AudioPreprocessor

def _write_test_wav(path: Path, sr: int = 16000, channels: int = 1, duration=0.5):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    tone = 0.1 * np.sin(2 * np.pi * 440 * t)
    if channels == 1:
        data = tone.astype(np.float32)
    else:
        data = np.stack([tone, tone], axis=-1).astype(np.float32)
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(path), data, sr)

def test_is_yamnet_ready_true_for_matching_wav(tmp_path):
    ap = AudioPreprocessor(target_sr=16000, mono=True)
    p = tmp_path / "mono_16k.wav"
    _write_test_wav(p, sr=16000, channels=1)
    assert ap.is_yamnet_ready(str(p)) is True

def test_load_audio_resamples_and_converts_to_mono(tmp_path):
    ap = AudioPreprocessor(target_sr=16000, mono=True)
    p = tmp_path / "stereo_22k.wav"
    _write_test_wav(p, sr=22050, channels=2)
    wav, sr = ap.load_audio(str(p))
    assert sr == ap.target_sr
    assert wav.dtype == np.float32
    assert wav.ndim == 1  # mono

def test_process_file_creates_output_and_is_ready(tmp_path):
    ap = AudioPreprocessor(target_sr=16000, mono=True)
    inp = tmp_path / "in" / "stereo_src.wav"
    out = tmp_path / "out" / "converted.wav"
    _write_test_wav(inp, sr=22050, channels=2)
    # ensure output does not exist initially
    assert not out.exists()
    ap.process_file(str(inp), str(out))
    assert out.exists()
    assert ap.is_yamnet_ready(str(out)) is True

def test_process_folder_creates_mirrored_structure(tmp_path):
    ap = AudioPreprocessor(target_sr=16000, mono=True)
    input_root = tmp_path / "input_root"
    subfolder = input_root / "sub1"
    file_in = subfolder / "sound.wav"
    _write_test_wav(file_in, sr=22050, channels=2)

    output_root = tmp_path / "output_root"
    ap.process_folder(str(input_root), str(output_root))
    expected_out = output_root / "sub1" / "sound.wav"
    assert expected_out.exists()
    assert ap.is_yamnet_ready(str(expected_out)) is True