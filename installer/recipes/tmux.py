from recipe_base import RecipeBase, DPath, HPath

class TmuxRecipe(RecipeBase):

  name = "tmux"
  links = [
        (DPath("tmux/tmux.conf"), HPath(".tmux.conf"))
    ]


