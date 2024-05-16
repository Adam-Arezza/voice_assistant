import ollama

class Assistant:
    def __init__(self, model):
        self.model = model


    def get_response(self, query):
        messages = [{'role': 'user',
                     'content': query,
                     }]
        response = ollama.chat(model=self.model,messages=messages)
        return response['message']['content']

