#!/bin/bash
# Checks if $SSH_AUTH_SOCK exists and is a Unix domain socket
[-S "$SSH_AUTH_SOCK" ] && ssh-add -l > /dev/null 2>&1 || ssh-add ~/.ssh/id_ed25519_github
