from recipe_base import RecipeBase

class GitRecipe(RecipeBase):

  name = "git"

  def __init__(self, settings):
    RecipeBase.__init__(self, settings)
    self.links = [
            ("{0}/git/gitignore".format(self.settings.path), "{0}/.gitignore".format(self.settings.home)),
            ("{0}/git/gitconfig".format(self.settings.path), "{0}/.gitconfig".format(self.settings.home)),
        ]


