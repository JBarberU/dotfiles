import subprocess
import operator
import sys

from log import Log
from colors import Colors

def run_cmd_ret_output(args, formatter):
  cmd = ""
  for a in args:
    cmd += "%s " % a

  formatter.start()

  p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

  while True:
    line = p.stdout.readline()
    if line != '':
      try:
        formatter.put_line(line)
      except RuntimeError as e:
        p.terminate()
        raise e
    else:
      break
  p.wait()
  formatter.stop()
  return p.returncode

""" commands is an array of touples with command+args and array with acceptable
error codes. An example: [(["echo", "Hello World"], []), (["exit", "1"], [1])]"""
def run_chained_commands(commands, formatter):
  formatter.start()
  proc_list = []
  for (args, err_codes) in commands:
    if 0 not in err_codes:
      err_codes.append(0)

    if not proc_list:
      p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(args, stdin=proc_list[-1][0].stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      proc_list[-1][0].stdout.close()
    proc_list.append((p, err_codes))

  while True:
    line = proc_list[-1][0].stdout.readline()
    if line:
      Log.print_msg("Stdout", line, Colors.MAGENTA_FG)
    else:
      break

  for (p, err_codes) in proc_list:
    p.wait()
    if p.returncode not in err_codes:
      while True:
        line = p.stderr.readline()
        if line:
          Log.print_msg("Stderr", line, Colors.RED_FG)
        else:
          break
      return p.returncode

  return 0

