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
                                    stream_callback=self.stream_cb
                                    )
        self.silence_frames = 0
        self.stream_stopped = False
        self.audio_frames = []
        print(self.mic.get_default_input_device_info())

    def record_chunk(self, file_path, chunk_len):
        frames = []
        for _ in range(0, int(self.rate / self.frames_per_buffer * chunk_len)):
            data = self.stream.read(self.frames_per_buffer)
            frames.append(data)
        chunk_data = b''.join(frames)
        w = wave.open(file_path, 'wb')
        w.setnchannels(self.channels)
        w.setsampwidth(self.mic.get_sample_size(self.format))
        w.setframerate(self.rate)
        w.writeframes(chunk_data)
        w.close()
        

    def detect_silence(self, audio_data):
        np.set_printoptions(threshold=sys.maxsize)
        silence_detected = False
        #read the data
        #compare the data to some threshold for silence
        #if the data is silence for x consecutive frames, stop the recording
        data = np.fromstring(audio_data, dtype=np.int16)
        avg_amp = np.average(abs(data))
        #print(len(data))
        #print(data.shape)
        #print(avg_amp)
        #print('checking this')
        if avg_amp < 300:
            silence_detected = True
        return silence_detected


    def stream_cb(self, in_data, frame_count, time_info, status_flags):
        flag = pyaudio.paContinue
        #print(frame_count)
        if self.detect_silence(in_data):
            #print("silence was detected")
            self.silence_frames += 1
            if self.silence_frames >= 20:
                self.stream_stopped = True
                flag = pyaudio.paComplete
                self.stream.close()
                self.silence_frames = 0
        else:
            self.silence_frames = 0
        self.audio_frames.append(in_data)
        return (in_data, flag)


    def restart_stream(self):
        self.stream = self.mic.open(format=self.format,
                                    channels=self.channels,
                                    rate=self.rate,
                                    input=self.input,
                                    frames_per_buffer=self.frames_per_buffer,
                                    stream_callback=self.stream_cb
                                    )

    def clear_audio_frames(self):
        self.audio_frames = []
