#!/usr/bin/python3

import argparse
import os
import subprocess

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog='bench.py',
                                    description='util for benchmarking a rpc repository')
  parser.add_argument('directory', type=str, nargs=1, help='path to the repository')
  parser.add_argument('-b', '--bench', dest='bench', default='.')
  
  parser.add_argument('-s', '--secs', dest='time', type=int, default=1)

  parser.add_argument('-i', '--iterations', dest='iterations', type=int, default=0)

  parser.add_argument('-m', '--mem', dest='mem', action='store_true')

  parser.add_argument('-f', '--fast', dest='fast', action='store_true')

  args = parser.parse_args()
  
  os.chdir(args.directory)

  benchtime=f"{args.time}"
  if args.iterations != 0:
    benchtime=f"{args.iterations}x"
  
  cpu='-cpu 1,2,4,8'
  if args.fast:
    cpu=''
  
  
  subprocess.run(['go', 'test', 
                  '-bench', args.bench, 
                  '-run', '^#', 
                  cpu,
                  '-benchtime', benchtime
                  
                  ], capture_output=True)

  