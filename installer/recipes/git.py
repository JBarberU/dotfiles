from recipe_base import RecipeBase, DPath, HPath

class GitRecipe(RecipeBase):

  name = "git"
  links = [
          (DPath("git/gitignore"), HPath(".gitignore")),
          (DPath("git/gitconfig"), HPath(".gitconfig")),
      ]

