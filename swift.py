#!/usr/bin/env python

import os
import sys
import threading
import timeit


# require AUTH/URL/KEY as zwift/swift/zpm utils do
# can't proceed without them
try:
    URL = os.environ['ST_AUTH']
    KEY = os.environ['ST_KEY']
    USER = os.environ['ST_USER']
except KeyError as e:
    print e
    sys.exit(1)

# tls
thread_data = []

def test(number):
    """Zebra testing

    :param number interger pointing to object to read ('object12.txt')
    Create new connection and post json job: print some object content
    to stdout"""

    from zwiftclient.client import ZwiftConnection as Connection
    data = """[{
"exec": {
    "path":"swift://~/bench/bench_2",
    "args": "/dev/input"
},
"file_list": [
    {
        "device": "input",
        "path": "swift://~/input/input/object%d.txt"
    },
    {
        "device": "stdout"
    }
],
"name": "bench_2"
}]
""" % number
    conn = Connection(authurl=URL,
                      key=KEY,
                      user=USER,
                      retries=1,
                      insecure=True)
    conn.head_account()
    body, headers = conn.exec_account(
        None, None, data, content_type='application/json',
        content_length=len(data), headers={}, response_dict={})


def test_batch(start, count):
    """Running `test` function several times

    :param start integer to start with
    :param count times to execute"""

    # putting results to kind of TLS
    results = []

    for i in range(start, start + count + 1):
        try:
            l = timeit.repeat(stmt='test(%d)' % i,
                              setup='from __main__ import test',
                              number=1, repeat=1)
            results.append(l[0])
        except Exception as e:
            print >> sys.stderr, e

    thread_data.append(results)


OVERALL_COUNT = 100
THREAD_COUNT = 50
COUNT_PER_THREAD = OVERALL_COUNT / THREAD_COUNT

threads = []
for i in range(0, THREAD_COUNT):
    t = threading.Thread(target=test_batch,
                         args=(1 + COUNT_PER_THREAD*i, COUNT_PER_THREAD))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

for results in thread_data:
    for line in results:
        print line
