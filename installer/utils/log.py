import sys
from colors import Colors

class Log:

  @classmethod
  def print_msg(cls, title, msg, color, new_line = True):
    Log.raw("{0}{1}{2}: {3}".format(color, title, Colors.NORMAL, msg), new_line)

  @classmethod
  def msg(cls, msg, new_line = True):
    Log.print_msg("Message", msg, Colors.MAGENTA_FG, new_line)

  @classmethod
  def info(cls, msg, new_line = True):
    Log.print_msg("Info", msg, Colors.CYAN_FG, new_line)

  @classmethod
  def warn(cls, msg, new_line = True):
    Log.print_msg("Warning", msg, Colors.YELLOW_FG, new_line)

  @classmethod
  def note(cls, msg, new_line = True):
    Log.print_msg("Note", msg, Colors.YELLOW_FG, new_line)

  @classmethod
  def err(cls, msg, new_line = True):
    Log.print_msg("Error", msg, Colors.RED_FG, new_line)

  @classmethod
  def fatal(cls, msg, new_line = True):
    Log.print_msg("Fatal", msg, Colors.RED_FG, new_line)
    exit(1)

  @classmethod
  def raw(cls, msg, new_line = True):
    if new_line and msg[-1:] != "\n":
      msg += "\n"
    sys.stdout.write("{0}".format(msg))
