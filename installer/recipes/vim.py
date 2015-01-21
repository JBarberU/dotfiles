from recipe_base import RecipeBase, DPath, HPath

class VimRecipe(RecipeBase):

  name = "vim"
  links = [
        (DPath("vim/vim"), HPath(".vim")),
        (DPath("vim/vimrc"), HPath(".vimrc")),
      ]

