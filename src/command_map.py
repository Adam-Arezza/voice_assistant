import subprocess as sp
import string
import os


class CommandExecutor:
    def __init__(self, cfg):
        self.commands = {
            "describe image": self.get_image,
            "take note": self.take_note,
            "open browser": self.open_browser,
            "stop robot": ""
            }

        self.NOTE_PATH = cfg["notes_dir"]

    def parse_command(self, transcript):
        text = transcript.lower()
        punctuation_remover = str.maketrans('','',string.punctuation)
        text = text.translate(punctuation_remover)
        split_text = text.split(" ")[0:2]
        split_text = " ".join(split_text)
        if split_text in self.commands:
            content = transcript.split(" ")
            content.pop(0)
            content.pop(0)
            content = " ".join(content)
            return split_text, content
        else:
            return None, None 


    def take_note(self, note_content):
        note_num = len(os.listdir(self.NOTE_PATH))
        with open(self.NOTE_PATH + f"assistant_note{note_num + 1}.txt", 'a') as note_file:
            note_file.writelines(note_content)
            note_file.close()


    def get_image(self, image_path):
        pass

    def open_browser(self):
        pass
