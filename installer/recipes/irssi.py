from os import path
from shutil import copyfile
from recipe_base import RecipeBase
from log import Log

class IrssiRecipe(RecipeBase):

  links = [("irssi", ".irssi")]

  def install(self):
    config = "{0}/irssi/config".format(self.path)
    if not path.exists(config):
      copyfile("{0}.example".format(config), config)
      Log.info("{0} created, tweak it to suit your needs")

    RecipeBase.install(self)

