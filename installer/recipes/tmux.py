from recipe_base import RecipeBase

class TmuxRecipe(RecipeBase):

  name = "tmux"

  def __init__(self, settings):
    RecipeBase.__init__(self, settings)

    self.links = [
          ("{0}/tmux/tmux.conf".format(self.settings.path), "{0}/.tmux.conf".format(self.settings.home))
      ]

