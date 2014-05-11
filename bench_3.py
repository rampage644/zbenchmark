#!
import sys

# pass filename as first arg
# python script.py <file-name>
if len(sys.argv) < 2:
    sys.exit(1)
with open(sys.argv[1], 'r') as ifile:
    print(ifile.read()),
