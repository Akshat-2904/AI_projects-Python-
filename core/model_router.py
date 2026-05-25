from core.ollama_client import OllamaClient
#from core.custom_model import CustomModel


ollama=OllamaClient()
#Custom=CustomModel()


def RouteModel(Mode):# selects the mode of the model
    if Mode=="fast":
     return ollama
    #else:
       # return Custom