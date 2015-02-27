from recipe_base import RecipeBase, Path
from command import run_cmd_ret_output, run_chained_commands
from output_pipe import OutputPipe
from getpass import getuser
from log import Log

common = ["vim", "irssi", "git", "tmux", "exuberant-ctags"]
brews = common + ["python, ack", "ctags"]
apt_gets = common + ["zsh", "xclip", "xmonad", "xmobar", "conky-all", "dmenu", "rxvt-unicode-256color", "feh", "build-essential", "ack-grep"]

class ToolsRecipe(RecipeBase):

  name = "tools"

  def install(self):
    pipe = OutputPipe()
    if self.settings.platform.mac:
      if run_chained_commands([(["curl", "-fsSL" ,"https://raw.githubusercontent.com/Homebrew/install/master/install"], []), (["ruby"], [1])], pipe):
        Log.fatal("Failed to install homebrew")

      if run_cmd_ret_output(["brew", "update"], pipe):
        Log.fatal("Faild to brew update")

      for b in brews:
        if run_cmd_ret_output(["brew", "install", b], pipe):
          Log.err("Failed to install: {0}".format(b))

    elif self.settings.platform.linux:
      if run_cmd_ret_output(["pkexec", "apt-get", "update"], pipe):
        Log.fatal("Failed to apt-get update")

      if run_cmd_ret_output(["pkexec", "apt-get", "install", "-y"] + apt_gets, pipe):
        Log.err("Failed to install: {0}".format(a))

    if run_cmd_ret_output(["pip", "install", "jedi"], pipe):
      Log.err("Failed to install: jedi")


  def uninstall(self):
    if self.settings.platform.mac:
      for b in brews:
        ret_code = run_cmd_ret_output(["brew", "uninstall", b], pipe)

      Log.warn("Not uninstalling homebrew, check https://github.com/Homebrew/homebrew/blob/master/share/doc/homebrew/FAQ.md#faq for that")

    elif self.settings.platform.linux:
      if run_cmd_ret_output(["pkexec", "apt-get", "remove"] + apt_gets, pipe):
        Log.err("Failed to remove: {0}".format(a))


