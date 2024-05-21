#!/usr/bin/python3

import os
import argparse


if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog='prof.py', description='util for viewing rpc profiles')

  parser.add_argument("dir", nargs=1, help='subfolder that profiles were placed in. If -a flag is set, this is instead a full path to the file')

  parser.add_argument('-a', '--absolute', dest='absolute', action='store_true')

  parser.add_argument('-t', '--type', choices=["cpu", "mem"], dest='type', default='cpu')

  parser.add_argument('-i', '--ui', action="store_true", dest='ui', help="run with '-http :'")
  args = parser.parse_args()

  dir = os.path.dirname(os.path.realpath(__file__))
  outputDir = os.path.join(dir, "output")

  fileName = args.type + '.prof'

  realDir = ''
  if args.absolute:
    realDir = os.path.join(args.dir[0], fileName)
  else:
    realDir = os.path.join(outputDir, args.dir[0], fileName)

  http=''
  httpDest=''
  ls = ["go", "tool", "pprof", realDir]
  if args.ui:
    ls = ["go", "tool", "pprof", '-http', ':', realDir]


  print(realDir)
  os.execv("/usr/local/go/bin/go", ls)