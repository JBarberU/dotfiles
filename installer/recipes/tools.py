from recipe_base import RecipeBase, Path
from command import run_cmd_ret_output, run_chained_commands
from output_pipe import OutputPipe
from getpass import getuser

common = ["vim", "irssi", "git", "tmux"]
brews = common + ["python"]
apt_gets = common + ["zsh", "xclip", "xmonad", "xmobar", "conky-all", "dmenu", "rxvt-unicode-256color", "feh", "build-essential"]

class ToolsRecipe(RecipeBase):

  name = "tools"

  def __check_for_root(self):
    if getuser() != "root":
      Log.fatal("In order to use ToolsRecipe, install.py needs to run as root")

  def install(self):
    return
    pipe = OutputPipe()
    if self.platform.mac:
      if run_chained_commands([(["curl", "-fsSL" ,"https://raw.githubusercontent.com/Homebrew/install/master/install"], []), (["ruby"], [1])], pipe):
        Log.fatal("Failed to install homebrew")

      if run_cmd_ret_output(["brew", "update"], pipe):
        Log.fatal("Faild to brew update")

      for b in brews:
        if run_cmd_ret_output(["brew", "install", b], pipe):
          Log.err("Failed to install: {0}".format(a))

    elif self.platform.linux:
      self.__check_for_root()
      if run_cmd_ret_output(["apt-get", "update"], pipe):
        Log.fatal("Failed to apt-get update")

      for a in apt_gets:
        if run_cmd_ret_output(["apt-get", "install", a], pipe):
          Log.err("Failed to install: {0}".format(a))

  def uninstall(self):
    if self.platform.mac:
      for b in brews:
        ret_code = run_cmd_ret_output(["brew", "uninstall", b], pipe)

      Log.warn("Not uninstalling homebrew, check https://github.com/Homebrew/homebrew/blob/master/share/doc/homebrew/FAQ.md#faq for that")

    elif self.platform.linux:
      self.__check_for_root()
      for a in apt_gets:
        if run_cmd_ret_output(["apt-get", "remove", a], pipe):
          Log.err("Failed to remove: {0}".format(a))


