#!/usr/bin/python3

import argparse
import os
import subprocess
import time

if __name__ == '__main__':
  
  
  parser = argparse.ArgumentParser(prog='test.py',
                                    description='util for testing 2 rpc repositories')
  
  dir = os.path.dirname(os.path.realpath(__file__))
  outputDir = os.path.join(dir, "output")
  if not os.path.exists(outputDir):
    os.mkdir(outputDir)
  
  outputOne = os.path.join(outputDir, "one.csv")
  outputTwo = os.path.join(outputDir, "two.csv")

  cur_time = str(int(time.time()))

  parser.add_argument('directory1', type=str, nargs=1, help='path to the first repository')
  parser.add_argument('directory2', type=str, nargs=1, help='path to the second repository')
  
  parser.add_argument('-o', '--output1', dest='output1', default=outputOne)
  parser.add_argument('-t', '--output2', dest='output2', default=outputTwo)

  args = parser.parse_args()
  
  if os.path.exists(args.output1):
    os.remove(args.output1)
  if os.path.exists(args.output2):
    os.remove(args.output2)

  os.chdir(args.directory1[0])
  print(args.output1)

  subprocess.run(['go', 'test', 
                  '-output', args.output1,
                  '-seed', cur_time
                  ])
  
  os.chdir(dir)
  os.chdir(args.directory2[0])

  subprocess.run(['go', 'test', 
                  '-output', args.output2,
                  '-seed', cur_time
                  ])
  
  os.chdir(dir)
  out = subprocess.run([
    'diff', args.output1, args.output2
  ], capture_output=True)

  if out.returncode:
    print(out.stdout)
  else:
    print("All Tests Passed.")

  