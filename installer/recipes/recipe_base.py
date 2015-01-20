class RecipeBase:

  def __init__(self, platform):
    self.platform = platform

  def install(self):
    print "Install"

  def uninstall(self):
    print "Uninstall"

