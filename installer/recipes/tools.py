from recipe_base import RecipeBase
from command import run_cmd_ret_output, run_chained_commands
from output_pipe import OutputPipe

class ToolsRecipe(RecipeBase):
  def install(self):
    if self.platform.mac:
      pipe = OutputPipe()
      ret_code = run_chained_commands([(["curl", "-fsSL" ,"https://raw.githubusercontent.com/Homebrew/install/master/install"], []), (["ruby"], [1])], pipe)
    elif self.platform.linux:
      Log.msg("Install linux stuff")

  def uninstall(self):
    print "uninstalling tools"

