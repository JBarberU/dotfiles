from os import path
from shutil import copyfile
from recipe_base import RecipeBase
from log import Log

class IrssiRecipe(RecipeBase):

  name = "irssi"

  def __init__(self, settings):
    RecipeBase.__init__(self, settings)
    self.links = [("{0}/irssi".format(self.settings.path), "{0}/.irssi".format(self.settings.home))]
    self.copy_list = [
          ("{0}/irssi/config.example".format(self.settings.path), "{0}/irssi/config".format(self.settings.path))
      ]


