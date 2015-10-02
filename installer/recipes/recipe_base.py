from os import symlink, path, readlink, remove, rename, mkdir
from shutil import copyfile, rmtree
from output_pipe import OutputPipe
from command import run_cmd_ret_output
from log import Log

class Path:

  home = 1
  dot_dir = 2

  def __init__(self, base, path = "", absolute = False):
    self.base = base
    self.path = path
    self.absolute = absolute

  def get_full_path(self, settings):
    if self.absolute:
      return self.path
    else:
      if self.base == Path.home:
        base = settings.home
      elif self.base == Path.dot_dir:
        base = settings.path
      else:
        raise Exception("Invalid base {0}: {1}".format(self.path, self.base))
      return "{0}/{1}".format(base, self.path)

class HPath(Path):
  def __init__(self, path = ""):
    Path.__init__(self, Path.home, path, False)

class DPath(Path):
  def __init__(self, path = ""):
    Path.__init__(self, Path.dot_dir, path, False)

class RecipeBase:

  links = []
  links_abs = []
  copy_list = []
  touch_list = []
  mkdir_list = []
  name = ""

  def __init__(self, settings):
    self.settings = settings

  def install(self):
    self.mkdirs(self.mkdir_list)
    self.create_links(self.links)
    self.copy_files(self.copy_list)
    self.touch_files(self.touch_list)

  def uninstall(self):
    self.remove_links(self.links)
    self.remove_files(self.copy_list + self.touch_list)

  def create_links(self, links):
    for (s, d) in links:
      if path.lexists(d.get_full_path(self.settings)):
        if not path.islink(d.get_full_path(self.settings)) and not self.settings.overwrite:
          d_full_path = d.get_full_path(self.settings)
          Log.info("Backing up {0} ({0}.bak)".format(d_full_path))
          rename(d_full_path, "{0}.bak".format(d_full_path))
        elif not self.settings.overwrite:
          if readlink(d.get_full_path(self.settings)) != s.get_full_path(self.settings):
            Log.warn("Removing existing symlink to {0}, which is currently pointing to {1}".format(d.get_full_path(self.settings), readlink(d.get_full_path(self.settings))))
          remove(d.get_full_path(self.settings))
        else:
          try:
            remove(d.get_full_path(self.settings))
          except OSError:
            rmtree(d.get_full_path(self.settings))

      symlink(s.get_full_path(self.settings), d.get_full_path(self.settings))

  def remove_links(self, links):
    for (s, d) in links:
      remove(d.get_full_path(self.settings))
      if path.exists("{0}.bak".format(d.get_full_path(self.settings))):
        rename("{0}.bak".format(d.get_full_path(self.settings)), d.get_full_path(self.settings))
        Log.info("Old {0} restored".format(d.get_full_path(self.settings)))

  def touch_files(self, touch_list):
    for f in touch_list:
      open(f.get_full_path(self.settings), 'a').close()

  def mkdirs(self, dirs):
    for d in dirs:
      try:
        mkdir(d.get_full_path(self.settings))
      except OSError:
        Log.info("{0} already exists".format(d.get_full_path(self.settings)))

  def copy_files(self, copy_list):
    for (s, d) in copy_list:
      if path.exists(d.get_full_path(self.settings)):
        if path.islink(d.get_full_path(self.settings)):
          Log.warn("Removing symlink {0}, pointing at {1}".format(d.get_full_path(self.settings), readlink(d.get_full_path(self.settings))))
        elif not self.settings.overwrite:
          rename(d.get_full_path(self.settings), "{0}.bak".format(d.get_full_path(self.settings)))
          Log.info("Backed up file {0} ({0}.bak)".format(d.get_full_path(self.settings)))
        else:
          remove(d.get_full_path(self.settings))

      copyfile(s.get_full_path(self.settings), d.get_full_path(self.settings))

  def remove_files(self, remove_list):
    for f in remove_list:
      remove(f.get_full_path(self.settings))

