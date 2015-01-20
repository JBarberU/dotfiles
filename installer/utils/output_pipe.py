import sys
import re
from colors import Colors
from meta_line import MetaLine
from line import Line

class UnacceptableOutputError(Exception):
  pass

class OutputPipe:
  meta_lines = []
  verbose = True
  pretty = True
  unacceptable_output = []

# unacceptable_output is usful for failing based on command output, rather than
# exitcode
  def __init__(self, verbose = True, pretty = True, unacceptable_output=[]):
    self.verbose = verbose
    self.pretty = pretty
    self.unacceptable_output = unacceptable_output
    self.meta_lines = []

  def put_line(self, line):
    m_line = MetaLine(line)
    self.meta_lines.append(m_line)

    if self.verbose:
      if self.pretty:
        output = m_line.str()
      else:
        output = line

      sys.stdout.write(output)

    for uo in self.unacceptable_output:
      if re.compile(uo).match(line):
        raise UnacceptableOutputError(line)

  def start(self):
    pass

  def stop(self):
    pass

