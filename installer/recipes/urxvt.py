from recipe_base import RecipeBase

class UrxvtRecipe(RecipeBase):
  def install(self):
    if self.platform.linux:
      Log.msg("urxvt install goes here")

  def uninstall(self):
    if self.platform.linux:
      Log.msg("urxvt uninstall goes here")

