import os
import numpy as np
import subprocess as sp
import json
import time
import keyboard
from src.speaker import Speaker
from src.recorder import Recorder
from src.transcriber import Transcriber
from src.assistant import Assistant


def main():
    with open("config.json") as cfg_file:
        cfg = json.load(cfg_file)
        cfg_file.close()
    speaker = Speaker()
    recorder = Recorder()
    transcriber = Transcriber()
    assistant = Assistant(cfg, show_history=True)
    temp_audio_file = cfg["file"]

    try:
        while True:
            if keyboard.is_pressed("space") and not recorder.stream_stopped:
                print("Listening...")
                recorder.record_chunk(5)
            else:
                if len(recorder.audio_frames) > 0:
                    recorder.save_audio(temp_audio_file)
                    recorder.clear_audio_frames()
                    transcript = transcriber.transcribe_chunk(temp_audio_file)
                    print(transcript)
                    response = assistant.get_response(transcript)
                    try:
                        speaker.speak(response)
                    except Exception as e:
                        print("Error with speech to text")
                        print(e)
                    print(response)
                    os.remove(temp_audio_file)
                else:
                    continue
            time.sleep(0.1)

           
    except Exception as e:
        speaker.speak("There was a problem, check the output below...")
        print(e)


if __name__ == "__main__":
    main()
