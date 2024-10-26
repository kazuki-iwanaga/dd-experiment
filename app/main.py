import time
from ddtrace import tracer

@tracer.wrap()
def hello_goodbye():
    hello()
    goodbye()

@tracer.wrap()
def hello():
    time.sleep(1)
    goodbye()
    print("Hello World!")

@tracer.wrap()
def goodbye():
    time.sleep(1)
    print("Goodbye!")

if __name__ == "__main__":
    with tracer.trace("main"):
        hello_goodbye()