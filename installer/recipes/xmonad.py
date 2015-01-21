from recipe_base import RecipeBase, DPath, HPath

class XmonadRecipe(RecipeBase):

  name = "xmonad"

  def __init__(self, settings):
    RecipeBase.__init__(self, settings)
    if self.settings.platform.linux:
      self.links = [
            (DPath("haskell/ghci"), HPath(".ghci")),
            (DPath("xmonad/xmonad.hs"), HPath(".xmonad/xmonad.hs")),
            (DPath("xmonad/xmobarrc"), HPath(".xmobarrc")),
            (DPath("conky/conkyrc"), HPath(".conkyrc")),
            (DPath("xorg/xinitrc"), HPath(".xinitrc")),
          ]
      self.touch_list = [HPath(".dmenu_favourites")]
      self.mkdir_list = [HPath(".xmonad")]

