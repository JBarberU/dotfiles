from recipe_base import RecipeBase

class XmonadRecipe(RecipeBase):

  name = "xmonad"

  def __init__(self, settings):
    RecipeBase.__init__(self, settings)
    if self.settings.platform.linux:
      self.links = [
            ("{0}/haskell/ghci".format(self.settings.path), "{0}/.ghci".format(self.settings.home)),
            ("{0}/xmonad/xmonad.hs".format(self.settings.path), "{0}/.xmonad/xmonad.hs".format(self.settings.home)),
            ("{0}/xmonad/xmobarrc".format(self.settings.path), "{0}/.xmobarrc".format(self.settings.home)),
            ("{0}/conky/conkyrc".format(self.settings.path), "{0}/.conkyrc".format(self.settings.home)),
            ("{0}/xorg/xinitrc".format(self.settings.path), "{0}/.xinitrc".format(self.settings.home)),
          ]
      self.touch_list = ["{0}/.dmenu_favourites".format(self.settings.home)]
      self.mkdir_list = ["{0}/.xmonad".format(self.settings.home)]

