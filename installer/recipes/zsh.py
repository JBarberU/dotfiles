from recipe_base import RecipeBase
from log import Log

class ZshRecipe(RecipeBase):

  name = "zsh"

  def __init__(self, settings):
    RecipeBase.__init__(self, settings)
    self.links = [
          ("{0}/zsh/zshrc".format(self.settings.path), "{0}/.zshrc".format(self.settings.home)),
          ("{0}/zsh/sh_functions".format(self.settings.path), "{0}/.sh_functions".format(self.settings.home)),
          ("{0}/zsh/oh-my-zsh".format(self.settings.path), "{0}/.oh-my-zsh".format(self.settings.home)),
      ]
    if self.settings.platform.mac:
      self.links += [
            ("{0}/zsh/zshrc_osx".format(self.settings.path), "{0}/.zshrc_osx".format(self.settings.home)),
        ]
    self.touch_list = [
                  "{0}/.aliases".format(self.settings.home),
                  "{0}/.paths".format(self.settings.home),
              ]

  def install(self):
    RecipeBase.install(self)
    Log.note("Run \"chsh -s $(which zsh)\" to set zsh as our default shell")

