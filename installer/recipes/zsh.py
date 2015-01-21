from recipe_base import RecipeBase, DPath, HPath
from log import Log

class ZshRecipe(RecipeBase):

  name = "zsh"
  links = [
        (DPath("zsh/zshrc"), HPath(".zshrc")),
        (DPath("zsh/sh_functions"), HPath(".sh_functions")),
        (DPath("zsh/oh-my-zsh"), HPath(".oh-my-zsh")),
    ]
  touch_list = [
                HPath(".aliases"),
                HPath(".paths"),
            ]

  def __init__(self, settings):
    RecipeBase.__init__(self, settings)
    if self.settings.platform.mac:
      self.links += [
            (DPath("zsh/zshrc_osx"), HPath(".zshrc_osx")),
        ]

  def install(self):
    RecipeBase.install(self)
    Log.note("Run \"chsh -s $(which zsh)\" to set zsh as our default shell")

