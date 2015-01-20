from recipe_base import RecipeBase

class UrxvtRecipe(RecipeBase):

  name = "urxvt"

  def __init__(self, platform, path, home):
    RecipeBase.__init__(self, platform, path, home)
    if platform.linux:
      self.links = [
          ("{0}/xorg/Xresources".format(self.path), "{0}/.Xresources".format(self.home))
        ]


