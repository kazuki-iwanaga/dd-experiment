import logging
import time
from ddtrace import tracer

ddtrace_logger = logging.getLogger("ddtrace")
ddtrace_logger.setLevel(logging.CRITICAL)

dogstatsd_logger = logging.getLogger("datadog.dogstatsd")
dogstatsd_logger.setLevel(logging.CRITICAL)

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