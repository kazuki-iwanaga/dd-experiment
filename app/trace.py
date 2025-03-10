import random
from time import sleep
import multiprocessing as mp
import requests

from ddtrace import tracer, patch
from ddtrace.context import Context
from datadog import initialize, statsd
initialize()

patch(requests=True)

@statsd.distributed('subproc.time')
def subproc(args):
    tracer.context_provider.activate(
        Context(
            trace_id=args['ctx']['trace_id'],
            span_id=args['ctx']['span_id'],
        )
    )

    # with tracer.trace('subproc %02d' % args['i'], service='myapp'):
    span = tracer.trace('subproc %02d' % args['i'], service='subproc')
    try:
        sleep(random.random()*0.1)
        subsubproc()
        subsubproc()
        _ = requests.get('http://lgtm:3000')

        span.set_tags({'hoge_tag_%02d' % args['i']: args['i']})
        # span.set_meta('hoge_meta_%02d' % args['i'], args['i'])
        raise Exception('hoge')
    except Exception as e:
        # https://github.com/DataDog/dd-trace-py/blob/65864cea98e8b3602fee619cb8f5b749b5e70bb3/ddtrace/span.py#L229-L239
        span.set_traceback()
    finally:
        span.finish()

    statsd.increment('subproc.count', 1)
    statsd.distribution('subproc.i', random.random())
    statsd.distribution('subproc.i2', random.random()**2)

    return args['i']

@tracer.wrap('subsubproc')
@statsd.distributed('subsubproc.time')
def subsubproc():
    sleep(random.random())

if __name__ == '__main__':
    with tracer.trace('main', service='pymain') as span:
        # https://github.com/DataDog/dd-trace-py/blob/65864cea98e8b3602fee619cb8f5b749b5e70bb3/ddtrace/span.py#L194-L203
        ctx = span.to_dict()
        # ctx = {
        #     'trace_id': span.context.trace_id,
        #     'span_id': span.context.span_id,
        # }

        statsd.increment('main.count', 1)

        pool = mp.Pool(8)
        args_list = [{'i': i, 'ctx': ctx} for i in range(10)]
        for res in pool.imap_unordered(subproc, args_list):
            print(res)
