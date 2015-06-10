from platform_base import PlatformBase

import platform

class LinuxPlatform(PlatformBase):
  linux = True
  distro_name = "unknown"
  distro_version = "unknown"
  distro_id = "unknown"

  def __init__(self):
    self.distro_name, self.distro_version, self.distro_id = platform.linux_distribution()

  def __str__(self):
    return "Linux - {0} {1} ({2})".format(self.distro_name, self.distro_version, self.distro_id)
