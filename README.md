# Prerequisites
## Xmonad
- Xmonad
- Xmobar
- acpi (if installing for laptop)

## Vim 
- Vim (duh)

## ZSH
- ZSH (duh)

## Git
- Git (duh)

# Installation
To install you can either copy the files you'd like to use to their destinations (or symlink). Or you may use the install.sh script.

The install.sh script symlinks all files from the dotfiles directory to the correct destinations which means that they'll be under version control should you wish to make any changes.

Please note that the install script will remove all conflicting files. If you feel uncertain, check what files are affected by the script before using it!

There are a couple of possible parameters to use:
-a All the following will be installed (-l or -d must also be provided as it's a requisite for xmonad)
-l Laptop configuration of xmonad (or rather xmobar)
-d Desktop configuration of xmonad (or rather xmobar)
-g Git gitconfig is installed
-v Vim configuration and plugins are installed
-z oh-my-zsh is installed, and zshrc is installed

# Uninstallation
You don't want to uninstall my dotfiles :) If you do, you're on your own...

