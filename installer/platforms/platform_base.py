class PlatformBase:
  mac = False
  linux = False
  windows = False

  distro_name = "N/A"
  distro_version = "N/A"
  distro_id = "N/A"

  def __str__(self):
    if self.mac:
      return "OS X"
    elif self.windows:
      return "Windows"
    elif self.linux:
      return "Linux"
