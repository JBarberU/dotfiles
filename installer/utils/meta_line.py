from colors import Colors
from line import Line
import re

prefixes = [
            ("Start", "", Colors.MAGENTA_FG),
            ("Pass", "", Colors.GREEN_FG),
            ("Fail", "", Colors.RED_FG),
            ("Debug", "", Colors.BLUE_FG),
            ("Error", "", Colors.RED_FG),
            ("Default", "", Colors.MAGENTA_FG),
            ("Warning", "", Colors.YELLOW_FG),
            ("Duration", "s;", Colors.BLUE_FG),
            ("logElementTree", "", Colors.BLUE_FG),
           ]

class MetaLine(Line):
  color = Colors.NORMAL
  prefix = ""
  body = ""

  def __init__(self, line):
    self.body = line
    if line.find("Waiting for device to boot") != -1:
      self.color = Colors.CYAN_FG
      self.prefix = "Instruments"
      self.body = "Booting device\n"
      return

    for (p, end, c) in prefixes:
      match = re.compile(".*%s ?: ?" % p).match(line)
      if match:
        self.color = c
        self.prefix = p
        (_, index) = match.span()
        body = line[index:]

        if end != "":
          index = body.find(end)
          if index != -1:
            body = body[:index]
            body += "\n"

        self.body = body
        break

  def str(self):
    return "%s%s%s: %s" % (self.color, self.prefix, Colors.NORMAL, self.body)

