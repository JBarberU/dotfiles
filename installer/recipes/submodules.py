from recipe_base import RecipeBase
from output_pipe import OutputPipe
from command import run_cmd_ret_output
from log import Log

class SubmodulesRecipe(RecipeBase):

  name = "git submodules"

  def install(self):
    pipe = OutputPipe()
    if run_cmd_ret_output(["git", "submodule", "update", "--init"], pipe):
      Log.err("Unable to update git submodules")
      return

    RecipeBase.install(self)


