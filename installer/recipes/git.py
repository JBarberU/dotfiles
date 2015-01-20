from recipe_base import RecipeBase

class GitRecipe(RecipeBase):

  name = "git"

  def __init__(self, platform, path, home):
    RecipeBase.__init__(self, platform, path, home)
    self.links = [
            ("{0}/git/gitignore".format(self.path), "{0}/.gitignore".format(self.home)),
            ("{0}/git/gitconfig".format(self.path), "{0}/.gitconfig".format(self.home)),
        ]


