from recipe_base import RecipeBase

class ZshRecipe(RecipeBase):

  name = "zsh"

  def install(self):
    print "installing zsh"

  def uninstall(self):
    print "uninstalling zsh"


