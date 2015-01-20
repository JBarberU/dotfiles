#!/usr/bin/env python

import argparse
import sys
import os

f_path = os.path.dirname(__file__)
sys.path += [f_path] + [ s.format(f_path) for s in ["{0}/installer",
                                                    "{0}/installer/platforms",
                                                    "{0}/installer/recipes",
                                                    "{0}/installer/utils"]]

from log import Log

from xmonad import XmonadRecipe
from vim import VimRecipe
from zsh import ZshRecipe
from git import GitRecipe
from urxvt import UrxvtRecipe
from irssi import IrssiRecipe
from submodules import SubmodulesRecipe
from tools import ToolsRecipe
from linux import LinuxPlatform
from mac import MacPlatform
from windows import WindowsPlatform

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--xmonad", action = "store_true", help = "Installs xmonad stuff")
  parser.add_argument("--vim", action = "store_true", help = "Installs vim stuff")
  parser.add_argument("--zsh", action = "store_true", help = "Installs zsh stuff")
  parser.add_argument("--git", action = "store_true", help = "Installs git stuff")
  parser.add_argument("--urxvt", action = "store_true", help = "Installs urxvt stuff")
  parser.add_argument("--irssi", action = "store_true", help = "Installs irssi stuff")
  parser.add_argument("--tools", action = "store_true", help = "Runs apt-get and installs useful tools")
  parser.add_argument("--all", action = "store_true", help = "Installs everything")
  parser.add_argument("--uninstall", action = "store_true", help = "Uninstalls the given arguments")
  args = parser.parse_args()

  if sys.platform == "linux" or sys.platform == "linux2":
    platform = LinuxPlatform()
  elif sys.platform == "darwin":
    platform = MacPlatform()
  elif sys.platform == "win32":
    platform = WindowsPlatform()
  else:
    print("Unknown platform: {0}".format(sys.platform))
    exit(1)

  path = os.path.abspath(os.path.dirname(__file__))
  home = os.path.expanduser("~")

  recipes = []
  if args.all:
    recipes = [
        SubmodulesRecipe(platform, path, home),
        ToolsRecipe(platform, path, home),
        XmonadRecipe(platform, path, home),
        VimRecipe(platform, path, home),
        ZshRecipe(platform, path, home),
        GitRecipe(platform, path, home),
        UrxvtRecipe(platform, path, home),
        IrssiRecipe(platform, path, home),
        ]
  else:
    if args.xmonad:
      recipes.append(XmonadRecipe(platform, path, home))
    if args.vim:
      recipes += [SubmodulesRecipe(platform, path, home), VimRecipe(platform, path, home)]
    if args.zsh:
      recipes.append(ZshRecipe(platform, path, home))
    if args.git:
      recipes.append(GitRecipe(platform, path, home))
    if args.urxvt:
      recipes.append(UrxvtRecipe(platform, path, home))
    if args.irssi:
      recipes.append(IrssiRecipe(platform, path, home))
    if args.tools:
      recipes.append(ToolsRecipe(platform, path, home))

  for r in recipes:
    if args.uninstall:
      Log.info("Uninstalling {0}".format(r.name))
      r.uninstall()
    else:
      Log.info("Installing {0}".format(r.name))
      r.install()

  Log.msg("Done!")

if __name__ == "__main__": main()
