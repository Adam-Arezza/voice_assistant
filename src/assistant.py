import ollama
from src.command_map import CommandExecutor

class Assistant:
    def __init__(self, cfg):
        self.model = cfg["model"]
        self.executor = CommandExecutor(cfg)
        self.initial_prompt = "You are an assistant, I want your responses to be concise and relatively breif unless I say otherwise."
        ollama.chat(model=self.model, messages=[{'role': 'user', 'content': self.initial_prompt}])

    def get_response(self, query):
        messages = [{'role': 'user',
                     'content': query,
                     }]
        response = ollama.chat(model=self.model,messages=messages)
        return response['message']['content']
