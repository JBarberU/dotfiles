#!/bin/bash

DOTFILES_PATH=$(pwd)
TARGET_PATH=$HOME
#DRY_RUN=1

function verify_variable() {
    if [[ -z "${!1}" ]]
    then
        echo "Unable to set $1, aborting"
        exit 1
    fi
}

verify_variable DOTFILES_PATH
verify_variable TARGET_PATH


function create_link() {
    if [[ -z $1 ]]
    then
        echo "create_link called with no arguments, aborting"
        exit 1
    fi

    if [[ -z $2 ]]
    then
        echo "create_link called with only one argument. It needs a source and target, aborting"
        exit 1
    fi

    if [[ -v $DRY_RUN ]]
    then
        echo "$DOTFILES_PATH/$1" "$TARGET_PATH/$2"
    else
        DEST="$TARGET_PATH/$2"
        DEST_DIR=$(dirname "$DEST")
        if [[ ! -d "$DEST_DIR" ]]
        then
            mkdir -p "$DEST_DIR"
        fi
        if [[ -L "$DEST" ]]
        then
            LINK_DEST="$(readlink $DEST)"
            if [[ "$LINK_DEST" = "$DOTFILES_PATH/$1" ]]
            then
                echo "Skipped creating link to $DOTFILES_PATH/$1 (already exists)"
                return
            else
                echo "Encounterd link pointing at a different target , aborting"
                exit 1
            fi
        elif [[ -e "$DEST" ]]
        then
            echo "A regular file exists at path $DEST, aborting"
            exit 1
        fi
        ln -s "$DOTFILES_PATH/$1" "$DEST"
    fi
}

function create_copy() {
    if [[ -z $1 ]]
    then
        echo "create_copy called with no arguments, aborting"
        exit 1
    fi

    if [[ -z $2 ]]
    then
        echo "create_copy called with only one argument. It needs a source and target, aborting"
        exit 1
    fi

    if [[ -v $DRY_RUN ]]
    then
        echo "$DOTFILES_PATH/$1" "$TARGET_PATH/$2"
    else
        cp "$DOTFILES_PATH/$1" "$TARGET_PATH/$2"
    fi
}

function create_file() {
    if [[ -z $1 ]]
    then
        echo "create_file called with no arguments, aborting"
        exit 1
    fi

    if [[ -v $DRY_RUN ]]
    then
        echo "$TARGET_PATH/$1"
    else
        touch "$TARGET_PATH/$1"
    fi
}

function create_dir() {
    if [[ -z $1 ]]
    then
        echo "create_dir called with no arguments, aborting"
        exit 1
    fi

    if [[ -v $DRY_RUN ]]
    then
        echo "$HOME/$1"
    else
        mkdir -p "$HOME/$1"
    fi
}

function install_binaries() {
    if [[ -z $@ ]]
    then
        echo "install_binaries called with no arguments, aborting"
        exit 1
    fi

    if [[ -v $DRY_RUN ]]
    then
        echo "Installing $@"
    else
        sudo apt-get install -y $@
    fi
}

function install_git() {
    create_link git/gitignore .gitignore
    create_link git/gitconfig .gitconfig

    install_binaries git
}

function install_irssi() {
    create_link irssi .irssi

    create_copy irssi/config.example .irssi/config

    install_binaries irssi
}

function install_tmux() {
    create_link tmux/tmux.conf .tmux.conf
    create_link tmux/tmux_powerline.snap .tmux_powerline.snap

    install_binaries tmux

    # Build and install tmux-mem-cpy
    if [[ -v $DRY_RUN ]]
    then
        echo "Downloading, building and installing tmux-mem-cpu-load"
    else
        echo not dry run
        CURRENT_PATH="$(pwd)"

        cd /tmp
        git clone "https://github.com/thewtex/tmux-mem-cpu-load.git"
        cd /tmp/tmux-mem-cpu-load
        mkdir build
        cd build
        cmake ..
        make -j
        sudo make install

        cd "$CURRENT_PATH"
    fi
}

function install_urxvt() {
    create_link xorg/Xresources .Xresources

    install_binaries rxvt-unicode-256color
}

function install_vim() {
    create_link vimfiles .vim
    create_link vimfiles/vimrc .vimrc

    install_binaries vim exuberant-ctags ack-grep
}

function install_zsh() {
    create_file .aliases
    create_file .paths

    create_link zsh/zshrc .zshrc
    create_link zsh/zsh_custom .zsh_custom
    create_link zsh/zsh_env .zsh_env
    create_link zsh/cheat_sheet .cheat_sheet
    create_link zsh/sh_functions .sh_functions
    create_link zsh/oh-my-zsh .oh-my-zsh

    install_binaries zsh

    echo "Run \"chsh -s $(which zsh)\" to set zsh as our default shell"
}

function install_xmonad() {
    create_dir shots

    create_link haskell/ghci .ghci
    create_link xmonad/xmonad.hs .xmonad/xmonad.hs
    create_link xmonad/xmobarrc .xmobarrc
    create_link conky/conkyrc .conkyrc
    create_link xorg/xinitrc .xinitrc
    create_link rofi/config.rasi .config/rofi/config.rasi
    create_link xmonad/dunstrc .config/dunst/dunstrc

    install_binaries xmonad xmobar rofi conky-all xclip feh dunst xcompmgr numlockx xinput
}
