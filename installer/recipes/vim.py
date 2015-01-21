from recipe_base import RecipeBase

class VimRecipe(RecipeBase):

  name = "vim"

  def __init__(self, settings):
    RecipeBase.__init__(self, settings)
    self.links = [
          ("{0}/vim/vim".format(self.settings.path), "{0}/.vim".format(self.settings.home)),
          ("{0}/vim/vimrc".format(self.settings.path), "{0}/.vimrc".format(self.settings.home)),
        ]

