from colors import Colors
from output_pipe import OutputPipe
from log import Log
import sys
from threading import Thread
import time

class ProgressPipe(OutputPipe):

  def put_line(self, line):
    Log.raw("{0}.{1}".format(Colors.GREEN_FG, Colors.NORMAL), new_line = False)

  def start(self):
    Log.print_msg(title = "Progress", msg = "", color = Colors.MAGENTA_FG, new_line = False)

  def stop(self):
    Log.raw(" Done!", new_line = True)


