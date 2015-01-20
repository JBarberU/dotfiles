from recipe_base import RecipeBase

class VimRecipe(RecipeBase):

  name = "vim"

  links = [
        ("vim/vim", ".vim"),
        ("vim/vimrc", ".vimrc"),
      ]

