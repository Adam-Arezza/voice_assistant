import pyaudio
import wave


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
                                    frames_per_buffer=frames_per_buffer)


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
 
