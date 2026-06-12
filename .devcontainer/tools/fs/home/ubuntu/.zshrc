eval "$(~/.local/bin/mise activate zsh)"
eval "$(starship init zsh)"


export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"
plugins=(git)

source $ZSH/oh-my-zsh.sh

# Set up the prompt

autoload -Uz promptinit
promptinit
prompt adam1

setopt histignorealldups sharehistory

# Use emacs keybindings even if our EDITOR is set to vi
bindkey -e

# Keep 1000 lines of history within the shell and save it to ~/.zsh_history:
HISTSIZE=1000
SAVEHIST=1000
HISTFILE=~/.zsh_history

# Use modern completion system
autoload -Uz compinit
compinit

zstyle ':completion:*' auto-description 'specify: %d'
zstyle ':completion:*' completer _expand _complete _correct _approximate
zstyle ':completion:*' format 'Completing %d'
zstyle ':completion:*' group-name ''
zstyle ':completion:*' menu select=2
eval "$(dircolors -b)"
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' list-prompt %SAt %p: Hit TAB for more, or the character to insert%s
zstyle ':completion:*' matcher-list '' 'm:{a-z}={A-Z}' 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=* l:|=*'
zstyle ':completion:*' menu select=long
zstyle ':completion:*' select-prompt %SScrolling active: current selection at %p%s
zstyle ':completion:*' use-compctl false
zstyle ':completion:*' verbose true

zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#)*=0=01;31'
zstyle ':completion:*:kill:*' command 'ps -u $USER -o pid,%cpu,tty,cputime,cmd'

eval "$(zoxide init zsh)"

alias vi=nvim
alias kubectl="kubecolor"
alias tree="eza --tree"

# ---- SSH Agent initialization ----

SSH_ENV="$HOME/.ssh/agent.env"

start_ssh_agent() {
  echo "Starting new ssh-agent..."
  ssh-agent -s | sed 's/^echo/#echo/' > "$SSH_ENV"
  chmod 600 "$SSH_ENV"
  source "$SSH_ENV"
}

# Load existing agent info if present
if [[ -f "$SSH_ENV" ]]; then
  source "$SSH_ENV" >/dev/null
fi

# Start agent if not running or socket is invalid
if [[ -z "$SSH_AUTH_SOCK" || ! -S "$SSH_AUTH_SOCK" ]]; then
  start_ssh_agent
fi

# Optionally auto-add default keys (silent if none exist)
ssh-add -q ~/.ssh/id_ed25519 ~/.ssh/id_rsa 2>/dev/null
#-----------------------------------------------------------

# Fallback if TERM is something the server doesn't know
case "$TERM" in
  xterm-ghostty)
    export TERM=xterm-256color
    bindkey "^[[H" beginning-of-line
    bindkey "^[[F" end-of-line ;;
esac

[[ -d /data ]] && cd /data
