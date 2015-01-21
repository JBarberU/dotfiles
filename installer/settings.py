
class Settings:

  platform = None
  path = ""
  home = ""
  overwrite = False

  def __init__(self, platform, path, home, overwrite):
    self.platform = platform
    self.path = path
    self.home = home
    self.overwrite = overwrite

