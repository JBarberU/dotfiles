# Path to your oh-my-fish.
set fish_path $HOME/.oh-my-fish

# Theme
set fish_theme gianu

# Aliases
switch (uname)
  case "Darwin"
    function pubkey
      cat ~/.ssh/id_rsa.pub | pbcopy | echo "Copied public key to clipboard...";
    end
  case "Linux"
    function pubkey
      cat ~/.ssh/id_rsa.pub | xclip -selection clipboard | echo "Copied public key to clipboard...";
    end
    function dvorak
      setxkbmap "se(svdvorak)" and echo "clear Lock\nkeycode 0x42 = Escape\n" | xmodmap -;
    end
    function se
      setxkbmap se and echo "clear Lock\nkeycode 0x42 = Escape\n" | xmodmap -;
    end
    function ag; sudo apt-get; end
    function sx; startx; end
end

function gs; git status; end
function natti; echo "Shutting down $HOST" and sudo -k and sudo shutdown -h now; end
function j; jump; end
function fishreload; source ~/.config/fish/config.fish; end
function tmux; tmux -u; end

# Sourcing other files
function src_if_exists
	if test -e $argv[1]
		source $argv[1]
  end
end

function src_if_os
	if [uname] == $argv[1]
		src_if_exists $argv[2]
  end
end

src_if_exists $HOME/.paths
#src_if_exists "$HOME/.aliases"
#src_if_exists "$HOME/.paths"
#src_if_exists "$HOME/.env"
#src_if_exists "$HOME/.osx_only"
#src_if_exists "$HOME/.linux_only"
#src_if_exists "$HOME/.sh_functions"
#src_if_os "Darwin" "$HOME/.zshrc_osx"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-fish/plugins/*)
# Custom plugins may be added to ~/.oh-my-fish/custom/plugins/
# Example format: set fish_plugins autojump bundler
set fish_plugins gem git jump rails

# Path to your custom folder (default path is $FISH/custom)
#set fish_custom $HOME/dotfiles/oh-my-fish

# Load oh-my-fish configuration.
. $fish_path/oh-my-fish.fish
