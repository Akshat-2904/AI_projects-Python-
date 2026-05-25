from core.model_router import RouteModel
from core.prompt_manager import Build_Promt




class LLMEngine:
    def generate(self,user_input,mode="fast",stream=False):
        
        prompt=Build_Promt(mode,user_input)
        model=RouteModel(mode)

        if stream:
              return model.stream(prompt)
        
        else:
             return model.generate(prompt)