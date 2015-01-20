from recipe_base import RecipeBase

class TmuxRecipe(RecipeBase):

  name = "tmux"
  
  def __init__(self, platform, path, home):
    RecipeBase.__init__(self, platform, path, home)

    self.links = [
          ("{0}/tmux/tmux.conf".format(self.path), "{0}/.tmux.conf".format(self.home))
      ]

