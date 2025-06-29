#!/bin/bash
#(
#	sleep 3600
#) &
#exit 0

# Start sleep as a new session and detach
# setsid: starts a new session (like a daemon would)
setsid sleep 60 </dev/null &>/dev/null &
