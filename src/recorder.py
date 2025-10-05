import pyaudio
import wave
import numpy as np
import sys


class Recorder:
    def __init__(self,format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=1024):
        self.mic = pyaudio.PyAudio()
        self.format = format
        self.rate = rate
        self.channels = channels
        self.input = input
        self.frames_per_buffer = frames_per_buffer
        self.stream = self.mic.open(format=format,
                                    channels=channels,
                                    rate=rate,
                                    input=input,
                                    frames_per_buffer=frames_per_buffer,
                                    #stream_callback=self.stream_cb
                                    )
        self.silence_frames = 0
        self.stream_stopped = False
        self.audio_frames = []
        print(self.mic.get_default_input_device_info())

    def record_chunk(self, chunk_len):
        frames = []
        for _ in range(0, int(self.rate / self.frames_per_buffer * chunk_len)):
            data = self.stream.read(self.frames_per_buffer)
            frames.append(data)
        chunk_data = b''.join(frames)
        if len(self.audio_frames) > 0:
            self.audio_frames += chunk_data
        else:
            self.audio_frames = chunk_data

    def save_audio(self, file_path):
        w = wave.open(file_path, 'wb')
        w.setnchannels(self.channels)
        w.setsampwidth(self.mic.get_sample_size(self.format))
        w.setframerate(self.rate)
        w.writeframes(self.audio_frames)
        w.close()
        

    def close_stream(self):
        self.clear_audio_frames()
        self.stream.stop_stream()
        self.stream.close()
        self.mic.terminate()
        self.stream_stopped = True


    def restart_stream(self):
        self.stream = self.mic.open(format=self.format,
                                    channels=self.channels,
                                    rate=self.rate,
                                    input=self.input,
                                    frames_per_buffer=self.frames_per_buffer,
                                    #stream_callback=self.stream_cb
                                    )
        self.stream_stopped = False

    def clear_audio_frames(self):
        self.audio_frames = []
