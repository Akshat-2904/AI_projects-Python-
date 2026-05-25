# File: core/prompt_manager.py
MODES = {
    "fast": "You are a helpful AI assistant. Answer the user's question directly and concisely.",
    "dev": "You are a coding expert. Provide code snippets and technical explanations.",
    "research": "You are a deep reasoning AI. Analyze the topic thoroughly."
}

def Build_Promt(mode, User_Input):
    System_Promt = MODES.get(mode, MODES["fast"])
    
    # Crucial: No leading spaces and clear labels
    return f"System: {System_Promt}\nUser: {User_Input}\nAssistant:"