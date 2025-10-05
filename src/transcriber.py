import whisper
import os
import numpy as np


class Transcriber:
    def __init__(self, model="tiny", device="cpu"):
        self.model = whisper.load_model(model, device=device)


    def transcribe_chunk(self, chunk_file):
        #print(f"attempting to transcribe from {chunk_file}")
        audio = whisper.load_audio(chunk_file)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        _, probs = self.model.detect_language(mel)
        options = whisper.DecodingOptions()
        result = whisper.decode(self.model, mel, options)
        transcript = "".join(result.text)
        return transcript


    def transcribe_audio(self, audio):
        print("transcribing...")
        audio = np.frombuffer(b''.join(audio), np.int16).flatten().astype(np.float32) / 32768.0
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        _, probs = self.model.detect_language(mel)
        options = whisper.DecodingOptions()
        result = whisper.decode(self.model, mel, options)
        transcript = "".join(result.text)
        hallucination_filter = ["Thank you.", "you.", "you"]
        return transcript


