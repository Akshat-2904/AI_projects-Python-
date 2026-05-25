from core.llm_engine import LLMEngine



def main():
    print("Welcome to your AI Terminal")

    engine=LLMEngine()

    while True:
        user_input=input("\n>>>>")\
        
        if user_input.lower() ==["exit","quit"]:
            break


        
        mode="fast"
        stream=True

        response=engine.generate(user_input,mode)

            
        if stream:
            # streaming generator
            for chunk in response:
                print(chunk, end="", flush=True)
            print()  # newline at end
        else:
            print(response)


if __name__ == "__main__":
    main()