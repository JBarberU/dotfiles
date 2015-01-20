from recipe_base import RecipeBase

class XmonadRecipe(RecipeBase):

  name = "xmonad"

  def install(self):
    if self.platform.linux:
      Log.msg("xmonad install goes here")

  def uninstall(self):
    if self.platform.linux:
      Log.msg("xmonad uninstall goes here")



