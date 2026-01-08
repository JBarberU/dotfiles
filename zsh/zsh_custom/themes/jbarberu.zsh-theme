PROMPT='%{$fg[cyan]%}%*%{$reset_color%} in %{$fg[magenta]%}%~%{$reset_color%} $(git_prompt_info)%{$reset_color%}
%{$fg_bold[white]%}%n%{$reset_color%}@%{$fg_bold[cyan]%}%m%{$reset_color%}'
PROMPT="$PROMPT\$(vi_mode_prompt_info)\\\$%{$reset_color%} "
RPROMPT=""

# git
ZSH_THEME_GIT_PROMPT_PREFIX="(%{$fg_bold[green]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX=")"
ZSH_THEME_GIT_PROMPT_DIRTY=" %{$fg[red]%}✘%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$reset_color%}"

# vi-mode
VI_MODE_RESET_PROMPT_ON_MODE_CHANGE=true
VI_MODE_SET_CURSOR=true
MODE_INDICATOR="%F{magenta}"
