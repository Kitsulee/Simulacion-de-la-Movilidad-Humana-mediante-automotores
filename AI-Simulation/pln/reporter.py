import google.generativeai as genai

class GeminiClient:
    def __init__(self):
        API_KEY = 'AIzaSyBW2qxN4Lqa9j7GPfCfNrGi-NsSBWrVxcM'
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_content(self, prompt: str):
        return self.model.generate_content(prompt)


class Reporter:
    def __init__(self,events):
        self.client = GeminiClient()
        self.events = events

    def report(self):

        text="generame una noticia acerca de los los siguientes eventos tal que hagas un resumen de los lugares mas concurridos por las personas a lo largo del tiempo y los buses mas utilizados :"

        for event in self.events:
            text+=event+"\n"
        
        response = self.client.generate_content(text)
        print(response.text)