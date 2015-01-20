from recipe_base import RecipeBase

class UrxvtRecipe(RecipeBase):

  def __init__(self, platform, path, home):
    if platform.linux:
      self.links = [("xorg/Xresources", ".Xresources")]

    RecipeBase.__init__(self, platform, path, home)

