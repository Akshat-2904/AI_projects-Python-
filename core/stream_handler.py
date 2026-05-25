import time

def stream_response(generator, delay=0.01):
    """
    Prints a stream of tokens from a generator
    """
    for chunk in generator:
        print(chunk, end="", flush=True)
        time.sleep(delay)  # optional delay for "typing effect"
    print()  # newline at the end