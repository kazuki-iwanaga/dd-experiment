import random
from time import sleep
from ddtrace import tracer
from datadog import initialize, statsd

initialize()

cnt = 0
while True:
    # Count
    statsd.increment('hoge.count', random.randint(0, 10))

    # Gauge
    statsd.gauge('hoge.gauge', random.randint(0, 100))

    # Set
    statsd.set('hoge.set', random.randint(0, 100))

    # Histogram
    statsd.histogram('hoge.histogram', random.randint(0, 100))

    # Timing
    statsd.timing('hoge.timing', random.randint(0, 1000))

    # Distribution
    statsd.distribution('hoge.distribution', random.randint(0, 1000))

    print('cnt: {}'.format(cnt))
    cnt += 1
    sleep(1)    
