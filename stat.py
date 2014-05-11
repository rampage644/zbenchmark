#!/usr/bin/env python

import sys
import numpy as np

if len(sys.argv) < 2:
    print >> sys.stderr, "Usage is python stat.py <filename>"
    sys.exit(1)

with open(sys.argv[1], 'r') as ifile:
    l = [float(line) for line in ifile.readlines()]

array = np.array(l)
print 'min=%f, max=%f, mead=%f, median=%f, stddev=%f' % (
    np.min(array),
    np.max(array),
    np.mean(array),
    np.median(array),
    np.std(array, dtype=np.float64))
