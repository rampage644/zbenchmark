#!/usr/bin/env python

import os
import sys
import threading
import timeit
from zwiftclient.client import ZwiftConnection as Connection


# require AUTH/URL/KEY as zwift/swift/zpm utils do
# can't proceed without them
try:
    URL = os.environ['ST_AUTH']
    KEY = os.environ['ST_KEY']
    USER = os.environ['ST_USER']
except Exception, e:
    print >> sys.stderr, '%s is not set in env!' % e
    sys.exit(1)

# tls
thread_data = []

OVERALL_COUNT = int(sys.argv[1]) if len(sys.argv) >= 3 else 100
THREAD_COUNT = int(sys.argv[2]) if len(sys.argv) >= 3 else 50
COUNT_PER_THREAD = OVERALL_COUNT / THREAD_COUNT


def test_post_single_job(conn, number):
    """Zebra JSON job POST testing

    :param number interger pointing to object to read ('object12.txt')
    Create new connection and post json job: print some object content
    to stdout"""

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
    body, headers = conn.exec_account(
        None, None, data, content_type='application/json',
        content_length=len(data), headers={}, response_dict={})


def test_head_account(conn, number):
    """Zebra simple HEAD account testing

    :param number interger pointing to object to read ('object12.txt')
    Create new connection and post json job: print some object content
    to stdout"""
    conn.head_account()


def test_batch(start, count, func):
    """Running `test` function several times

    :param start integer to start with
    :param count times to execute
    :param func to execute, it should accept integer as first arg"""

    # putting results to kind of TLS
    results = []
    conn = Connection(authurl=URL,
                      key=KEY,
                      user=USER,
                      retries=1,
                      insecure=True)

    for i in range(start, start + count):
        try:
            l = timeit.repeat(stmt=lambda: func(conn, i),
                              setup='from __main__ import %s' % func.__name__,
                              number=1, repeat=1)
            results.append(l[0])
        except Exception as e:
            print >> sys.stderr, e

    thread_data.append(results)
    conn.close()

# !!! SET TESTING FUNCTION HERE !!!
TEST_FUNCTION = test_head_account
threads = []
for i in range(0, THREAD_COUNT):
    t = threading.Thread(target=test_batch,
                         args=(1 + COUNT_PER_THREAD*i,
                               COUNT_PER_THREAD,
                               TEST_FUNCTION))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

for results in thread_data:
    for line in results:
        print line
