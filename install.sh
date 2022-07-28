#!/bin/bash

#################### Helpers ##################################################

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
                echo "Encountered link pointing at a different target ($DEST -> current: $LINK_DEST vs proposed: $DOTFILES_PATH/$1)"
                read -p "Replace, skip or abort? [R/S/A]: " _ANS
                case "$_ANS" in
                    r|R) echo "Replacing link $DEST -> $DOTFILES_PATH/$1"; rm "$DEST";;
                    s|S) echo "Skipping";;
                    *) echo "Aborting"; exit 1;;
                esac
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
        echo "Installing the following: $@"
        sudo apt-get install -y $@
    fi
}

#################### Installers ###############################################

function install_cmus() {
    create_dir .config/cmus
    create_link cmus/rc .config/cmus/rc

    install_binaries cmus
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
    create_dir .bin
    create_dir .config/boop
    create_file .aliases
    create_file .paths

    create_link zsh/zshrc .zshrc
    create_link zsh/zsh_custom .zsh_custom
    create_link zsh/zsh_env .zsh_env
    create_link zsh/cheat_sheet .cheat_sheet
    create_link zsh/sh_functions .sh_functions
    create_link zsh/oh-my-zsh .oh-my-zsh
    create_link zsh/zsh_paths .zsh_paths
    create_link bin .bin/dotbin

    install_binaries zsh

    echo "Add files/symlinks {good,bad}.wav to .config/boop in order for the boop command to work properly!"
    echo "Run \"chsh -s $(which zsh)\" to set zsh as our default shell"
}

function patch_kbd_layout() {
    echo "Patching dvorak-intl"
    sudo patch /usr/share/X11/xkb/symbols/us "$DOTFILES_PATH/kbdlayout/dvorak-intl.patch"
}

function install_xmonad() {
    create_dir shots

    create_link haskell/ghci .ghci
    create_link xmonad/xmonad.hs .xmonad/xmonad.hs
    create_link xmonad/xmobarrc .xmobarrc
    create_link conky/conkyrc .conkyrc
    create_link xorg/xinitrc .xinitrc
    create_link xorg/start-xmonad .xmonad/start-xmonad
    create_link rofi/config.rasi .config/rofi/config.rasi
    create_link rofi/gruvbox-purple.rasi .config/rofi/gruvbox-purple.rasi
    create_link xmonad/dunstrc .config/dunst/dunstrc

    sudo mkdir /usr/share/dotfiles/backgrounds
    sudo cp "$DOTFILES_PATH/xorg/start-xmonad" "/usr/bin/stxmonad"

    install_binaries xmonad xmobar rofi conky-all xclip feh dunst xcompmgr numlockx xinput scrot
}

function install_rando_tools() {
    install_binaries simple-scan oathtool
}

install_fonts() {
    FONT_VIEWER="gnome-font-viewer"

    # Font Awesome
    ZIP_FILE="/tmp/fontawesome5.zip"
    FOLDER="/tmp/fontawesome5"
    wget -O "$ZIP_FILE" "https://use.fontawesome.com/releases/v5.15.4/fontawesome-free-5.15.4-desktop.zip"
    unzip -d "$FOLDER" "$ZIP_FILE"
    ls "$FOLDER"/fontawesome-free-5.*-desktop/otfs/*.otf | while read line;
    do
        $FONT_VIEWER "$line";
    done

    rm "$ZIP_FILE"
    rm -r "$FOLDER"

    # DejaVu Sans for Powerline
    FOLDER="/tmp/dejavu_sans"
    mkdir $FOLDER
    wget -O "$FOLDER/1.ttf" "https://github.com/powerline/fonts/blob/master/DejaVuSansMono/DejaVu%20Sans%20Mono%20Bold%20Oblique%20for%20Powerline.ttf?raw=true"
    wget -O "$FOLDER/2.ttf" "https://github.com/powerline/fonts/blob/master/DejaVuSansMono/DejaVu%20Sans%20Mono%20Bold%20for%20Powerline.ttf?raw=true"
    wget -O "$FOLDER/3.ttf" "https://github.com/powerline/fonts/blob/master/DejaVuSansMono/DejaVu%20Sans%20Mono%20Oblique%20for%20Powerline.ttf?raw=true"
    wget -O "$FOLDER/4.ttf" "https://github.com/powerline/fonts/blob/master/DejaVuSansMono/DejaVu%20Sans%20Mono%20for%20Powerline.ttf?raw=true"

    ls "$FOLDER"/* | while read line;
    do
        $FONT_VIEWER "$line"
    done

    rm -r "$FOLDER"
}

#################### Call desired installers ##################################

install_cmus
install_git
install_irssi
install_tmux
install_urxvt
install_vim
install_zsh
install_xmonad
patch_kbd_layout
install_rando_tools
install_fonts

exit 0
