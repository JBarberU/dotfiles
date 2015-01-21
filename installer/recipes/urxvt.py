from recipe_base import RecipeBase

class UrxvtRecipe(RecipeBase):

  name = "urxvt"

  def __init__(self, settings):
    RecipeBase.__init__(self, settings)
    if self.settings.platform.linux:
      self.links = [
          ("{0}/xorg/Xresources".format(self.settings.path), "{0}/.Xresources".format(self.settings.home))
        ]


