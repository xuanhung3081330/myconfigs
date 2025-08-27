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

$VERBOSE && echo "KEEP=$KEEP CACHE_DIR=$CACHE_DIR MODE=$([[ "$DELETE" = true ]] && echo delete || echo dry-run)"

# ----- Delete and keep N -----
# 1) List package files (*.pkg.tar.zst|xz) with their mtimes (newest first)
# 2) Derive the package base name by stripping the last 3 dash-separated fields
# 3) For each package base, keep the first $KEEP files and mark the rest for deletion

# The array will hold full paths to files we intent to delete
mapfile -t TO_DELETE < <(
	# List files with epoch mtime and full path, newest first
	find "$CACHE_DIR" -maxdepth 1 -type f \
		-name '*.pkg.tar.zst' \
		! -name '*.sig' -printf '%T@ %p\n' \
	| sort -nr \
	| awk -v KEEP="$KEEP" -v dir="$CACHE_DIR/" '
		{
			# fields: $1 = mtime, $2 = full path
			file = $2
			base = file
			sub(dir, "", base) # strip directory, now base is just the filename

			# Remove "-<pkgver>-<pkgrel>-<arch>.pkg.tar.(zst|xz)"
			# (pkgname can have dashes; pkgver/pkgrel/arch are the last 3 dash-separated field)
			gsub(/-[^-]+-[^-]+-[^-]+\.pkg\.tar\.(zst|xz)$/, "", base)

			count[base]++
			if (count[base] > KEEP) print file
		}
		'	
	)

# Also delete matching .sig files when present
EXTRA_SIGS=()
for f in "${TO_DELETE[@]:-}"; 
do
	if [[ -f "$f.sig" ]]; then
		EXTRA_SIGS+=("$f.sig")
	fi
done

# Combine lists
TO_DELETE=( "${TO_DELETE[@]:-}" "${EXTRA_SIGS[@]:-}" )

# ----- DELETE -----
if (( ${#TO_DELETE[@]} == 0 )); then
	echo "Nothing to delete. Each package has <= $KEEP versions"
	exit 0
fi

if ! $DELETE; then
	echo "Dry run - the following files would be deleted:"
	printf ' %s\n ' "${TO_DELETE[@]}"
	echo "Run with -d (and sudo) to actually delete"
else
	echo "Deleting ${#TO_DELETE[@]} files..."
	rm -v -- "${TO_DELETE[@]}"
	echo "Done."
fi
