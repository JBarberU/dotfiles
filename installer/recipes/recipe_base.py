from os import symlink, path, readlink, remove, rename
from shutil import copyfile
from output_pipe import OutputPipe
from command import run_cmd_ret_output
from log import Log


class RecipeBase:

  links = []
  links_abs = []
  copy_list = []
  touch_list = []
  name = ""

  def __init__(self, platform, path, home):
    self.platform = platform
    self.path = path
    self.home = home

  def install(self):
    self.create_links(self.links)
    self.copy_files(self.copy_list)
    self.touch_files(self.touch_list)

  def uninstall(self):
    self.remove_links(self.links)
    self.remove_files(self.copy_list + self.touch_list)

  def create_links(self, links):
    for (s, d) in links:
      if path.exists(d):
        if not path.islink(d):
          Log.info("Backing up {0} ({0}.bak)".format(d))
          copyfile(d, "{0}.bak".format(d))
        elif path.islink(d):
          if readlink(d) != s:
            Log.warn("Removing existing symlink to {0}, which is currently pointing to {1}".format(d, readlink(d)))
        remove(d)
      symlink(s, d)

  def remove_links(self, links):
    for (s, d) in links:
      remove(d)
      if path.exists("{0}.bak".format(d)):
        rename("{0}.bak".format(d), d)
        Log.info("Old {0} restored".format(d))

  def touch_files(self, touch_list):
    for f in touch_list:
      open(f, 'a').close()

  def copy_files(self, copy_list):
    for (s, d) in copy_list:
      if path.exists(d):
        if path.islink(d):
          Log.warn("Removing symlink {0}, pointing at {1}".format(d, readlink(d)))
        else:
          rename(d, "{0}.bak".format(d))
          Log.info("Backed up file {0} ({0}.bak)".format(d))

      copyfile(s, d)

  def remove_files(self, remove_list):
    for f in remove_list:
      remove(d)

