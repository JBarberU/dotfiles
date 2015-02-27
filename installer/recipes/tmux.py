from recipe_base import RecipeBase, DPath, HPath

class TmuxRecipe(RecipeBase):

  name = "tmux"
  links = [
        (DPath("tmux/tmux.conf"), HPath(".tmux.conf")),
        (DPath("tmux/tmux_powerline.snap"), HPath(".tmux_powerline.snap"))
    ]


