import os
import numpy as np
import subprocess as sp
import json
import time
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
    assistant = Assistant(cfg)
    wait_wake = True
    

    try:
        while True:
            if recorder.stream_stopped:
                recorder.stream_stopped = False
                transcript = transcriber.transcribe_audio(recorder.audio_frames)
                hallucination_filter = ["thank you.", "thank you", "you.", "you"]
                if transcript.lower() in hallucination_filter:
                    recorder.clear_audio_frames()
                    recorder.restart_stream()
                    continue
                #print(transcript)

                #waiting for wake word
                if wait_wake:
                    wake = transcriber.check_wake_word(transcript)
                    if wake:
                        speaker.speak("What can I help you with?")
                        recorder.clear_audio_frames()
                        recorder.restart_stream()
                        wait_wake = False
                    else:
                        recorder.clear_audio_frames()
                        recorder.restart_stream()

                else:
                    command, content = assistant.executor.parse_command(transcript)
                    if command:
                        if command == "stop robot":
                            wait_wake = True
                            speaker.speak("okay, let me know when you need more help")
                            recorder.clear_audio_frames()
                            recorder.restart_stream()
                            break
                        else:
                            speaker.speak(f"Executing command {command}")
                            assistant.executor.commands[command](content)
                    else:
                        response = assistant.get_response(transcript)
                        speaker.speak(response)
                        recorder.clear_audio_frames()
                        recorder.restart_stream()
            time.sleep(0.01)

           
    except Exception as e:
        speaker.speak("There was a problem, check the output below...")
        print(e)


if __name__ == "__main__":
    main()
