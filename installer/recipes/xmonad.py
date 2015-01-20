from recipe_base import RecipeBase

class XmonadRecipe(RecipeBase):

  name = "xmonad"

  def __init__(self, platform, path, home):
    RecipeBase.__init__(self, platform, path, home)
    if platform.linux:
      self.links = [
            ("{0}/haskell/ghci".format(self.path), "{0}/.ghci".format(self.home)),
            ("{0}/xmonad/xmonad".format(self.path), "{0}/.xmonad".format(self.home)),
            ("{0}/xmonad/xmobarrc".format(self.path), "{0}/.xmobarrc".format(self.home)),
            ("{0}/conky/conkyrc".format(self.path), "{0}/.conkyrc".format(self.home)),
            ("{0}/xorg/xinitrc".format(self.path), "{0}/.xinitrc".format(self.home)),
            ("{0}/xmonad/xmonad.desktop".format(self.path), "/usr/share/xsessions/xmonad.desktop"),
          ]
      self.touch_list = ["{0}/.dmenu_favourites".format(self.home)]

