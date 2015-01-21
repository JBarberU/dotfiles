from os import path
from shutil import copyfile
from recipe_base import RecipeBase, DPath, HPath
from log import Log

class IrssiRecipe(RecipeBase):

  name = "irssi"
  links = [(DPath("irssi"), HPath(".irssi"))]
  copy_list = [
        (DPath("irssi/config.example"), DPath("irssi/config"))
    ]

