#!/usr/bin/python
# some lame fibonacci benchmarking
# 0, 1, 1, 2, 3, 5, 8, ...

import sys
import time

class InputError(Exception):
  pass

def fibLoop(n):
  a, b = 1, 1
  while n > 1:
    a, b = b, a + b
    n -= 1
  return b

def fibRec(n):
  if n == 1 or n == 0:
    return 1
  else:
    a = fibRec(n - 1)
    b = fibRec(n - 2)
    return a + b

def fibGen():
  a, b = 1, 1
  yield a
  yield b
  while True:
    a, b = b, a + b
    yield b

def fibGenWrapper(n):
  for i, res in enumerate(fibGen()):
    if i == n:
      return res

def avgBenchmarkTest(loops, func, func_arg):
  benchmark = []
  for i in range(loops):
    start = time.time()
    res = func(func_arg)
    benchmark.append(time.time() - start)
  return sum(benchmark)/len(benchmark)

def main():
  n = int(sys.argv[1])
  if n < 1:
    raise InputError('n smaller than 1: %s' % n)
  print('fibLoop avg time: %s' % avgBenchmarkTest(100, fibLoop, n))
  print('fibGen avg time: %s' % avgBenchmarkTest(100, fibGenWrapper, n))
  print('fibRec avg time: %s' % avgBenchmarkTest(100, fibRec, n))

if __name__ == '__main__':
  main()
