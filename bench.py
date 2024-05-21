#!/usr/bin/python3

import argparse
import os
import subprocess

if __name__ == '__main__':

  dir = os.path.dirname(os.path.realpath(__file__))
  outputDir = os.path.join(dir, "output")
  if not os.path.exists(outputDir):
    os.mkdir(outputDir)


  parser = argparse.ArgumentParser(prog='bench.py',
                                    description='util for benchmarking a rpc repository')
  parser.add_argument('directory', type=str, nargs=1, help='path to the repository')

  parser.add_argument('-o', '--output', dest='output', default='.', help="name of output dir")

  parser.add_argument('-b', '--bench', dest='bench', default='.', help="Regex for benchmarks to run")
  
  parser.add_argument('-s', '--secs', dest='time', type=int, default=1, help="How many seconds should each benchmark run")

  parser.add_argument('-i', '--iterations', dest='iterations', type=int, default=0, help="How many times should each benchmark run (Overrides -s)")

  parser.add_argument('-m', '--mem', dest='mem', action='store_true', help="Collect Memory Statistics")

  parser.add_argument('-f', '--fast', dest='fast', action='store_true', help="Skip over some benchmarks that may not be interesting")

  parser.add_argument('-p', '--profile', dest='profile', action='store_true', help="Collect cpu/mem profiles, and store in output directory.")

  parser.add_argument('-t', '--trace', dest='trace', action='store_true', help="Collect execution trace")

  args = parser.parse_args()
  
  
  
  
  outputDir = os.path.join(outputDir, args.output)
  if not os.path.exists(outputDir):
    os.mkdir(outputDir)



  benchtime=f"{args.time}"
  if args.iterations != 0:
    benchtime=f"{args.iterations}x"
  else:
    benchtime = benchtime + 's'


  cpu='-cpu 1,2,4,8'
  if args.fast:
    cpu=''

  benchMem=''
  if args.mem:
    benchMem='-benchmem'
  
  memOut = ''
  cpuOut = ''
  cpuProf = ''
  memProf = ''

  if args.profile:
    memOut = os.path.join(outputDir, "mem.prof")
    cpuOut = os.path.join(outputDir, "cpu.prof")

    cpuProf='-cpuprofile'
    memProf='-memprofile'

  trace = ''
  traceOut = ''
  if args.trace:
    trace = '-trace'
    traceOut = os.path.join(outputDir, "trace.out")
  
  os.chdir(args.directory[0])
  ls = ['go', 'test', 
          '-bench', args.bench, 
          '-run', '^#', 
          cpu,
          benchMem,
          '-benchtime', benchtime,
          cpuProf, cpuOut,
          memProf, memOut,
          trace, traceOut
      ]
  # print(ls)
  print("Running. This may take a while.")
  out = subprocess.run(ls, capture_output=True)
  
  with open(os.path.join(outputDir, "out.txt"), "w") as f:
    f.write(out.stdout.decode())


  