#!/usr/bin/env bash

# This is Bash-only pacman cache cleaner (keep N latest versions per package)

set -Eeuo pipefail

# ------ Defaults -----
KEEP=3 # How many recent versions to keep per package
CACHE_DIR=/var/cache/pacman/pkg # Where pacman stores package files
DELETE=false # Default to dry-run (show what would be deleted)
VERBOSE=false # Print a bit more information

# ----- Help/usage ------
usage() {
	cat << 'EOF'
Usage: clean_pacman_cache.sh [-k N] [-p DIR] [-d] [-v] [--help]

Options:
	-k N		Keep N latest versions per package (default: 3)
	-p DIR		Pacman cache directory (default: /var/cache/pacman/pkg)
	-d		Delete for real (default: dry-run)
	-v		Verbose output
	--help		Show this help

Examples:
	Dry run, keep 3 versions:	clean_pacman_cache.sh
	Delete, keep 2 versions:	sudo clean_pacman_cache.sh -d -k 2
	Difference cache dir:		clean_pacman_cache.sh -p /some/other/dir
EOF
}

# ----- Parse options -----
#while (( "$#" )); do
#	case "$1" in
#		-k) KEEP="${2:-}"; shift 2 ;;
#		-p) 
#done
