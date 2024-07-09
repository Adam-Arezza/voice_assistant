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
    WAKE_FILE = cfg["wake_file"]
    CHUNK_FILE = cfg["chunk_file"]

    try:
        while True:
            if recorder.stream_stopped:
                recorder.stream_stopped = False
                transcript = transcriber.transcribe_audio(recorder.audio_frames)
                print(transcript)
                #waiting for wake word
                if wait_wake:
                   #wake = transcriber.check_wake_word(WAKE_FILE)
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
           #if not wait_wake:
           #    command, content = assistant.executor.parse_command(transcript)
           #    if command:
           #        if command == "stop robot":
           #            wait_wake = True
           #            speaker.speak("okay, let me know when you need more help")
           #            os.remove(CHUNK_FILE)
           #            break
           #        else:
           #            speaker.speak(f"Executing command {command}")
           #            assistant.executor.commands[command](content)
           #            os.remove(CHUNK_FILE)
               #recorder.record_chunk(CHUNK_FILE, 10)
               #TODO
               #detect if no query was given based on silent CHUNK_FILE
               #then continue, skipping to the next chunk file and transcription attempt
               #transcript = transcriber.transcribe_chunk(CHUNK_FILE)
               #try to strip command out of transcript and check if a command exists
               #process the transcription
               #if there are commands in the transcription, call the executor
               #speak relevant command information
              # else:
              #     response = assistant.get_response(transcript)
              #     speaker.speak(response)
              #     os.remove(CHUNK_FILE)
           #if recorder.stream_stopped:
           #    print("Restarting stream")
           #    recorder.stream_stopped = False
           #    transcript = transcriber.transcribe_audio(recorder.audio_frames)
           #    print(transcript)
           #    recorder.clear_audio_frames()
           #    recorder.restart_stream()

    except Exception as e:
        speaker.speak("There was a problem, check the output below...")
        print(e)


if __name__ == "__main__":
    main()
