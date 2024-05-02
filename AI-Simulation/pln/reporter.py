import google.generativeai as genai

class GeminiClient:
    def __init__(self):
        API_KEY = 'AIzaSyBW2qxN4Lqa9j7GPfCfNrGi-NsSBWrVxcM'
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_content(self, prompt: str):
        return self.model.generate_content(prompt)


class Reporter:
    def __init__(self,events,stadistics,stadistics_busses):
        self.client = GeminiClient()
        self.events = events
        self.stadistics = stadistics
        self.stadistics_busses = stadistics_busses

    def report(self):

        text="generame una noticia acerca de los los siguientes eventos tal que hagas un resumen de los lugares mas concurridos por las personas a lo largo del tiempo y los buses mas utilizados :"

        for event in self.events:
            text+=event+"\n"
        
        response = self.client.generate_content(text)
        print(response.text)

    def report_stadistics(self):
        text="generame una noticia acerca de los lugares mas concurridos por las personas a lo largo del tiempo y los buses mas utilizados dado a estas estadisticas:"

        for stadistic in self.stadistics:
            text+=f"Habian {self.stadistics[stadistic]} personas en promedio en la parada de buses de {stadistic}.\n"

        for stadistic in self.stadistics_busses:
            text+=f"Habian {self.stadistics_busses[stadistic]} personas en promedio en un bus {stadistic}.\n"

        response = self.client.generate_content(text)
        print(response.text)