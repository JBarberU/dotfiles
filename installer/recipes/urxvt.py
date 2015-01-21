from recipe_base import RecipeBase, DPath, HPath

class UrxvtRecipe(RecipeBase):

  name = "urxvt"

  def __init__(self, settings):
    RecipeBase.__init__(self, settings)
    if self.settings.platform.linux:
      self.links = [
          (DPath("xorg/Xresources"), HPath(".Xresources"))
        ]


