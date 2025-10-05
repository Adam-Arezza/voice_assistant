import ollama
from ollama import Client  
from src.command_map import CommandExecutor

class Assistant:
    def __init__(self, cfg, show_history=False):
        self.model = cfg["model"]
        self.executor = CommandExecutor(cfg)
        self.initial_prompt = "You are an assistant, I want your responses to be concise and relatively breif unless I say otherwise."
        self.client = Client(
                host="https://ollama.com",
                headers={'Authorization': cfg["key"]}
                )
        self.initial_response = self.client.chat(model=self.model, messages=[{'role': 'user', 'content': self.initial_prompt}])
        self.initialize = {"role":self.initial_response['message']['role'], "content":self.initial_response['message']['content']}
        self.history = [self.initialize]
        self.show_history = show_history

    def get_response(self, query):
        message = {'role': 'user',
                     'content': query,
                     }
        self.history.append(message)
        response = self.client.chat(model=self.model,messages=self.history)
        ai_message = {
                "role": response['message']['role'],
                "content": response['message']['content']
                }
        self.history.append(ai_message)
        if self.show_history:
            print(self.history)
        return ai_message['content']
