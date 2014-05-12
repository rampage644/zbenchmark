# Benchmark for Zebra

## Proposed methodology

Given only one host we could only measure response time for arbitrary Zebra request.

We will fire Zebra installation with `M` identical requests in `N` threads. So, every thread will fire `M/N` measuring response time for every request. Every request implies establishing SSL connection and performing actual request.

### POSTing JSON job

I used following JSON as request:

```JSON
[{
"exec": {
    "path":"swift://~/bench/bench_2",
    "args": "/dev/input"
},
"file_list": [
    {
        "device": "input",
        "path": "swift://~/input/input/objectN.txt"
    },
    {
        "device": "stdout"
    }
],
"name": "bench_2"
}]
```

where `N` is an integer from 1 to 10000. Every accesses different object as `N` goes from 1 to some number depending on total request count.

### HEADing an account

Request in this case is just making HEAD request to an account url.

## Results

Raw results could be found in `results/` directory. Every file has name like `Mreq_Nthread.txt` where M is total requests and N is thread count.

Analyse is done using IPython Notebook, please see:

1. [First stage](http://nbviewer.ipython.org/github/rampage644/zbenchmark/blob/master/results/First.ipynb)
2. [Second stage](http://nbviewer.ipython.org/github/rampage644/zbenchmark/blob/master/results/Second.ipynb)

## TODO
