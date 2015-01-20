from recipe_base import RecipeBase

class ZshRecipe(RecipeBase):

  name = "zsh"

  def __init__(self, platform, path, home):
    RecipeBase.__init__(self, platform, path, home)
    self.links = [
          ("{0}/zsh/zshrc".format(self.path), "{0}/.zshrc".format(self.home)),
          ("{0}/zsh/sh_functions".format(self.path), "{0}/.sh_functions".format(self.home)),
          ("{0}/zsh/oh-my-zsh".format(self.path), "{0}/.oh-my-zsh".format(self.home)),
      ]
    if self.platform.mac:
      self.links += [
            ("{0}/zsh/zshrc_osx".format(self.path), "{0}/.zshrc_osx".format(self.home)),
        ]
    self.touch_files = [
                  "{0}/.aliases".format(self.home),
                  "{0}/.paths".format(self.home),
              ]

  def install(self):
    RecipeBase.install(self)
    Log.warn("Run \"chsh -s /bin/zsh\" to set zsh as our default shell")

