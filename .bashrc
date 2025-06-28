#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export PATH="$HOME/go/bin:$PATH"

# This allows the terminal and tools (ssh, git, etc) to find the agent.
# If this isn't specified, the terminal uses the agent from other places
export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh-agent.socket"

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ 
