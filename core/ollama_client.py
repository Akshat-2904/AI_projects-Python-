#this file is a communication layer with ollama
#we need our system to talk to the model
import requests# library that enabels python to make http request
import json

class OllamaClient: #connects with the llm
  def __init__(self):
    self.url= "http://localhost:11434/api/generate"#ollama request for text genration
    self.model="llama3"#selecting the model
  
 
  def generate(self,prompt):#promnt is the full text send to ai
    
    response=requests.post ( #use post to send data to the server and returns
      self.url,#where to send
      json={
            "model":self.model,
            "prompt":prompt,
            "stream":False #stream is false indicating give me full response at once

          }
    )
    return response.json()["response"] 
     
  def stream(self, prompt):
    response = requests.post(
        self.url,
        json={
            "model": self.model,
            "prompt": prompt,
            "stream": True 
        },
        stream=True
    )
    for line in response.iter_lines():
        if line:
            # Each line is a JSON object like {"response": "word", "done": false}
            chunk = json.loads(line.decode())
            text = chunk.get("response", "")
            yield text
            if chunk.get("done"):
                break