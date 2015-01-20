from recipe_base import RecipeBase
from output_pipe import OutputPipe
from command import run_cmd_ret_output
from log import Log


class VimRecipe(RecipeBase):

  links = [
        ("vim/vim", ".vim"),
        ("vim/vimrc", ".vimrc"),
      ]

  def install(self):
    pipe = OutputPipe()
    if run_cmd_ret_output(["git", "submodule", "update", "--init"], pipe):
      Log.err("Unable to update git submodules")
      return

    RecipeBase.install(self)


  def uninstall(self):
    RecipeBase.uninstall(self)

