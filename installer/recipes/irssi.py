from os import path
from shutil import copyfile
from recipe_base import RecipeBase
from log import Log

class IrssiRecipe(RecipeBase):

  name = "irssi"

  def __init__(self, platform, path, home):
    RecipeBase.__init__(self, platform, path, home)
    self.links = [("{0}/irssi".format(self.path), "{0}/.irssi".format(self.home))]
    self.copy_list = [
          ("{0}/irssi/config.example".format(self.path), "{0}/irssi/config".format(self.path))
      ]


