import time
import os
from ddtrace import tracer
from datadog import initialize, statsd

options = {
    'statsd_host': 'localhost', #os.getenv('DOGSTATSD_HOST'),
    'statsd_port': 8125 #os.getenv('DOGSTATSD_PORT')
}

initialize(**options)

@tracer.wrap()
def hello_goodbye():
    hello()
    goodbye()

@tracer.wrap()
def hello():
    time.sleep(0.1)
    goodbye()
    print("Hello World!")

@tracer.wrap()
def goodbye():
    time.sleep(0.1)
    print("Goodbye!")

# with tracer.trace("main"):
hello_goodbye()

# while(1):
statsd.increment('main.invoked', tags=["environment:dev"])
statsd.increment('main.invoked', tags=["environment:dev"])
statsd.gauge('main.duration', 1.0, tags=["environment:dev"])

print("Invoked main")
# time.sleep(1)
