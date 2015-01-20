from os import symlink, path, readlink, remove, rename
from shutil import copyfile
from output_pipe import OutputPipe
from command import run_cmd_ret_output
from log import Log


class RecipeBase:

  links = []
  name = ""

  def __init__(self, platform, path, home):
    self.platform = platform
    self.path = path
    self.home = home

  def install(self):
    self.create_links(self.links)

  def uninstall(self):
    self.remove_links(self.links)

  def create_links(self, links):
    for (s, d) in links:
      dest = "{0}/{1}".format(self.home, d)
      src = "{0}/{1}".format(self.path, s)
      if path.exists(dest):
        if not path.islink(dest):
          Log.info("Backing up {0} ({0}.bak)".format(dest))
          copyfile(dest, "{0}.bak".format(dest))
        elif path.islink(dest):
          if readlink(dest) != src:
            Log.warn("Removing existing symlink to {0}, which is currently pointing to {1}".format(dest, readlink(dest)))
        remove(dest)
      symlink(src, dest)

  def remove_links(self, links):
    for (s, d) in links:
      dest = "{0}/{1}".format(self.home, d)
      src = "{0}/{1}".format(self.path, s)
      remove(dest)
      if path.exists("{0}.bak".format(dest)):
        rename("{0}.bak".format(dest), dest)
        Log.info("Old {0} restored".format(dest))

