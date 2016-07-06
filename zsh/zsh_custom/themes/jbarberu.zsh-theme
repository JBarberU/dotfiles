PROMPT='%{$fg[cyan]%}%*%{$reset_color%} in %{$fg[magenta]%}%~%{$reset_color%} $(git_prompt_info)%{$reset_color%}
%{$fg_bold[white]%}%n%{$reset_color%}@%{$fg_bold[cyan]%}%m%{$reset_color%}$ '

ZSH_THEME_GIT_PROMPT_PREFIX="(%{$fg_bold[green]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX=")"
ZSH_THEME_GIT_PROMPT_DIRTY=" %{$fg[red]%}糞%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$reset_color%}"
