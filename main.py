import os
import numpy as np
import subprocess as sp
from src.speaker import Speaker
from src.recorder import Recorder
from src.transcriber import Transcriber
from src.assistant import Assistant


def main():
    speaker = Speaker()
    recorder = Recorder()
    transcriber = Transcriber()
    assistant = Assistant("llava")
    wait_wake = True
    WAKE_FILE = "temp/wake.wav"
    CHUNK_FILE = "temp/chunk.wav"

    try:
        while True:
            if wait_wake:
                recorder.record_chunk(WAKE_FILE, 5)
                wake = transcriber.check_wake_word(WAKE_FILE)
                if wake:
                    speaker.speak("What can I help you with?")
                    wait_wake = False

            if not wait_wake:
                recorder.record_chunk(CHUNK_FILE, 10)
                #TODO
                #detect if no query was given based on silent CHUNK_FILE
                #then continue, skipping to the next chunk file and transcription attempt
                transcript = transcriber.transcribe_chunk(CHUNK_FILE)
                if transcript.lower() == "stop robot.":
                    wait_wake = True
                    speaker.speak("okay, let me know when you need more help")
                    os.remove(CHUNK_FILE)
                    break
                else:
                    response = assistant.get_response(transcript)
                    speaker.speak(response)
                    os.remove(CHUNK_FILE)

    except Exception as e:
        speaker.speak("There was a problem, check the output below...")
        print(e)


if __name__ == "__main__":
    main()
