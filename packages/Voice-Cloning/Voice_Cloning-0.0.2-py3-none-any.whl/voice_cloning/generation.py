# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 07:51:17 2023

@author: dreji18

this script is created from https://github.com/CorentinJ/Real-Time-Voice-Cloning
"""

import argparse
import os
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
import torch
import sounddevice as sd

from encoder import inference as encoder
from encoder.params_model import model_embedding_size as speaker_embedding_size
from synthesizer.inference import Synthesizer
from utils.argutils import print_args
from utils.default_models import ensure_default_models
from vocoder import inference as vocoder

from scipy.io import wavfile
import noisereduce as nr

path = os.path.dirname(os.path.abspath(__file__))

#%%
# allocating cuda infra if available
if torch.cuda.is_available():
    device_id = torch.cuda.current_device()
    gpu_properties = torch.cuda.get_device_properties(device_id)
    ## Print some environment information (for debugging purposes)
    print("Found %d GPUs available. Using GPU %d (%s) of compute capability %d.%d with "
        "%.1fGb total memory.\n" %
        (torch.cuda.device_count(),
        device_id,
        gpu_properties.name,
        gpu_properties.major,
        gpu_properties.minor,
        gpu_properties.total_memory / 1e9))
else:
    print("Using CPU for inference.\n")

#%%
# loading all the model artefacts
def load_model(model_type):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-e", "--enc_model_fpath", type=Path,
                        default="saved_models/"+model_type+"/encoder.pt",
                        help="Path to a saved encoder")
    parser.add_argument("-s", "--syn_model_fpath", type=Path,
                        default="saved_models/"+model_type+"/synthesizer.pt",
                        help="Path to a saved synthesizer")
    parser.add_argument("-v", "--voc_model_fpath", type=Path,
                        default="saved_models/"+model_type+"/vocoder.pt",
                        help="Path to a saved vocoder")
    args = parser.parse_args()

    enc_model_fpath = os.path.join(path, "saved_models/"+model_type+"/encoder.pt")
    syn_model_fpath = os.path.join(path, "saved_models/"+model_type+"/synthesizer.pt")
    voc_model_fpath = os.path.join(path, "saved_models/"+model_type+"/vocoder.pt")
    
    encoder.load_model(enc_model_fpath)
    synthesizer = Synthesizer(syn_model_fpath)
    vocoder.load_model(voc_model_fpath)
    
    return encoder, synthesizer, vocoder,  args

def voice_generator(sound_path, speech_text, voice_type = None):
    
    if voice_type == "western" or voice_type == None:
        encoder, synthesizer, vocoder,  args = load_model(model_type="default")
    
    if voice_type == "indian":
        encoder, synthesizer, vocoder,  args = load_model(model_type="indian")

    in_fpath = Path(sound_path.replace("\"", "").replace("\'", ""))

    preprocessed_wav = encoder.preprocess_wav(in_fpath)

    original_wav, sampling_rate = librosa.load(str(in_fpath))
    preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)

    embed = encoder.embed_utterance(preprocessed_wav)
    synthesizer = Synthesizer(args.syn_model_fpath)

    texts = [speech_text]
    embeds = [embed]

    specs = synthesizer.synthesize_spectrograms(texts, embeds)
    spec = specs[0]
    print("Created the mel spectrogram")

    vocoder.load_model(args.voc_model_fpath)
    generated_wav = vocoder.infer_waveform(spec)
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
    generated_wav = encoder.preprocess_wav(generated_wav)
    
    return generated_wav

def play_sound(generated_wav):
    try:
        sd.stop()
        sd.play(generated_wav, 16000)
    except sd.PortAudioError as e:
        print("\nCaught exception: %s" % repr(e))
        print("Continuing without audio playback. Suppress this message with the \"--no_sound\" flag.\n")
        
def save_sound(generated_wav, filename=False, noise_reduction=False):
    
    # noise reduction function
    def noise_reduction(generated_wav, file_out):
        rate = 16000
        data = generated_wav
        snr = 2 # signal to noise ratio
        noise_clip = data/snr
        reduced_noise = nr.reduce_noise(y=data, sr=rate, y_noise = noise_clip, n_std_thresh_stationary=1.5,stationary=True)
        
        wavfile.write(rate, reduced_noise, file_out)
        
    # Save it on the disk    
    if filename:
        file_out = filename + ".wav"
    else:
        file_out = "voice_output" + ".wav"
    
    if noise_reduction==True:
        noise_reduction(generated_wav, file_out)
    else:
        sf.write(file_out, generated_wav.astype(np.float32), 16000)

#%%


















