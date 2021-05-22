import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import librosa
import tensorflow as tf
import os
from tensorflow.keras.models import load_model
import numpy as np

model = load_model('Speech_to_Text/model.h5')
r = sr.Recognizer()
classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'activate', 'add', 'and', 'backslash', 'bits slash std c plus plus dot h', 'bitwise', 'bool', 'break', 'char', 'character', 'column', 'compile', 'continue', 'deactivate', 'define', 'delete', 'divide', 'do', 'double', 'down', 'else', 'equal to', 'escape', 'false', 'first', 'float', 'for', 'goto', 'greater', 'hey', 'if', 'include', 'int', 'iostream', 'iterator', 'left', 'less', 'line', 'long', 'main', 'make', 'map', 'misty', 'modulo', 'move', 'namespace', 'new', 'newline', 'not', 'npos', 'null', 'open', 'or', 'pair', 'plus', 'position', 'quotes', 'read', 'remove', 'right', 'run', 'save', 'second', 'set', 'shift', 'short', 'sizeof', 'slash', 'std', 'string', 'switch', 'tab', 'true', 'typedef', 'underscore', 'unknown', 'unordered', 'unordered_map', 'unordered_set', 'unsigned', 'up', 'using', 'vector', 'void', 'while', 'xor']

def predict(audio):
    prob=model.predict(audio.reshape(1,8000,1))
    index=np.argmax(prob[0])
    return classes[index]

def load_audio_file(file_path):
    input_length = 8000
    data = librosa.core.load(file_path)[0]
    if len(data)>input_length:
        data = data[:input_length]
    else:
        data = np.pad(data, (0, max(0, input_length - len(data))), "constant")
    return data


def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 100,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )

    text = ""
    for chunk in chunks:
        samples = chunk.get_array_of_samples()
        data = np.array(samples)
        if len(data)>8000:
            data = data[:8000]
        else:
            data = np.pad(data, (0, max(0, 8000 - len(data))), "constant")
        text+=predict(data)
    # return the text for all chunks detected
    return text