from recipe_base import RecipeBase

class ZshRecipe(RecipeBase):

  name = "zsh"

  def __init__(self, platform, path, home):
    RecipeBase.__init__(self, platform, path, home)



