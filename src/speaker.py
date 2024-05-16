import pyttsx3

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)


    def speak(self, message):
        print(message)
        self.engine.say(message)
        self.engine.runAndWait()
