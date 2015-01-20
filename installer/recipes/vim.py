from recipe_base import RecipeBase

class VimRecipe(RecipeBase):

  name = "vim"

  def __init__(self, platform, path, home):
    RecipeBase.__init__(self, platform, path, home)
    self.links = [
          ("{0}/vim/vim".format(self.path), "{0}/.vim".format(self.home)),
          ("{0}/vim/vimrc".format(self.path), "{0}/.vimrc".format(self.home)),
        ]

