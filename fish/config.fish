# Path to your oh-my-fish.
set fish_path $HOME/.oh-my-fish

# Theme
set fish_theme gianu 

set fish_plugins git

function natti
    sudo shutdown -h now
end

function gs
    git status
end

function pubkey
    cat ~/.ssh/id_rsa.pub | xclip -selection clipboard | echo \"Copied public key to clipboard...\"
end

function dvorak
    setxkbmap "se(svdvorak)"
end
function se
    setxkbmap se
end
# Which plugins would you like to load? (plugins can be found in ~/.oh-my-fish/plugins/*)
# Custom plugins may be added to ~/.oh-my-fish/custom/plugins/
# Example format: set fish_plugins autojump bundler

# Path to your custom folder (default path is $FISH/custom)
#set fish_custom $HOME/dotfiles/oh-my-fish

# Load oh-my-fish configuration.
. $fish_path/oh-my-fish.fish
