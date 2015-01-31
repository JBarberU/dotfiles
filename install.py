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
from settings import Settings

from xmonad import XmonadRecipe
from vim import VimRecipe
from zsh import ZshRecipe
from git import GitRecipe
from urxvt import UrxvtRecipe
from tmux import TmuxRecipe
from irssi import IrssiRecipe
from submodules import SubmodulesRecipe
from tools import ToolsRecipe
from linux import LinuxPlatform
from mac import MacPlatform
from windows import WindowsPlatform

def main():
  if sys.platform == "linux" or sys.platform == "linux2":
    platform = LinuxPlatform()
  elif sys.platform == "darwin":
    platform = MacPlatform()
  elif sys.platform == "win32":
    platform = WindowsPlatform()
  else:
    print("Unknown platform: {0}".format(sys.platform))
    exit(1)

  parser = argparse.ArgumentParser()
  parser.add_argument("--xmonad", action = "store_true", help = "Installs xmonad stuff")
  parser.add_argument("--vim", action = "store_true", help = "Installs vim stuff")
  parser.add_argument("--zsh", action = "store_true", help = "Installs zsh stuff")
  parser.add_argument("--git", action = "store_true", help = "Installs git stuff")
  parser.add_argument("--urxvt", action = "store_true", help = "Installs urxvt stuff")
  parser.add_argument("--tmux", action = "store_true", help = "Installs tmux stuff")
  parser.add_argument("--irssi", action = "store_true", help = "Installs irssi stuff")
  parser.add_argument("--tools", action = "store_true", \
      help = "Runs {0} to install useful tools".format("apt-get" if platform.linux else "homebrew"))
  parser.add_argument("-a", "--all", action = "store_true", help = "Installs everything")
  parser.add_argument("-b", "--but", nargs="+", help = "Not installing the given arguments (can only be used together with --all)")
  parser.add_argument("-o", "--overwrite", action = "store_true", help = "Overwrites any existing files (= creates no backups)")
  parser.add_argument("-u", "--uninstall", action = "store_true", help = "Uninstalls the given arguments")
  args = parser.parse_args()

  path = os.path.abspath(os.path.dirname(__file__))
  home = os.path.expanduser("~")
  settings = Settings(platform, path, home, args.overwrite)

  recipes = []
  if args.all:
    recipes = [
        SubmodulesRecipe(settings),
        ToolsRecipe(settings),
        XmonadRecipe(settings),
        VimRecipe(settings),
        ZshRecipe(settings),
        GitRecipe(settings),
        UrxvtRecipe(settings),
        TmuxRecipe(settings),
        IrssiRecipe(settings),
        ]
    if args.but:
      recipes = filter(lambda r: r.name not in args.but, recipes)
  else:
    if args.xmonad:
      recipes.append(XmonadRecipe(settings))
    if args.vim:
      recipes += [SubmodulesRecipe(settings), VimRecipe(settings)]
    if args.zsh:
      recipes.append(ZshRecipe(settings))
    if args.git:
      recipes.append(GitRecipe(settings))
    if args.urxvt:
      recipes.append(UrxvtRecipe(settings))
    if args.tmux:
      recipes.append(TmuxRecipe(settings))
    if args.irssi:
      recipes.append(IrssiRecipe(settings))
    if args.tools:
      recipes.append(ToolsRecipe(settings))

  for r in recipes:
    if args.uninstall:
      Log.info("Uninstalling {0}".format(r.name))
      r.uninstall()
    else:
      Log.info("Installing {0}".format(r.name))
      r.install()

  if not recipes:
    Log.warn("Nothing to install (see -h or --help)")
  else:
    Log.msg("Done!")

if __name__ == "__main__": main()
