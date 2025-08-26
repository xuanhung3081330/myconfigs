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
while (( "$#" )); do
	case "$1" in
		-k) KEEP="${2:-}"; shift 2 ;;
		-p) CACHE_DIR="${2:-}"; shift 2 ;;
		-d) DELETE=true; shift ;;
		-v) VERBOSE=true; shift ;;
		--help) usage; exit 0 ;;
		*) echo "Unknown option: $1"; usage; exit 2 ;;
	esac
done

# ----- Sanity checks -----
# Ensure KEEP is a positive integer
if ! [[ "$KEEP" =~ ^[1-9][0-9]*$ ]]; then
	echo "ERROR: -k N must be a positive integer (got: $KEEP)"; exit 2
fi

# Ensure cache dir exists
if [[ ! -d "$CACHE_DIR" ]]; then
	echo "ERROR: Cache directory not found: $CACHE_DIR"; exit 2
fi

# If deleting, require root (so rm can actually remove files there)
if $DELETE && [[ $EUID -ne 0 ]]; then
	echo "ERROR: Deletion requires root. Re-run with: sudo $0 -d ${KEEP:+-k $KEEP} ${CACHE_DIR:+-p $CACHE_DIR}"; exit 1
fi
