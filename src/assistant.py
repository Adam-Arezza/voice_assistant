import ollama
from src.command_map import CommandExecutor

class Assistant:
    def __init__(self, cfg):
        self.model = cfg["model"]
        self.executor = CommandExecutor(cfg)

    def get_response(self, query):
        messages = [{'role': 'user',
                     'content': query,
                     }]
        response = ollama.chat(model=self.model,messages=messages)
        return response['message']['content']
