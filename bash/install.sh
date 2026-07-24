#!/usr/bin/env sh
# wtf installer (package route)
# Usage:  curl -fsSL https://yoursite/install.sh | sh
#         curl -fsSL https://yoursite/install.sh | sh -s -- v0.1.0   # pin a version
set -eu

REPO="jacobshultz/wtf"
VERSION="${latest}"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/wtf"
INIT_FILE="$CONFIG_DIR/wtf-run.sh"

# ---------------------------------------------------------------------------
# 1. Make sure pipx is available
# ---------------------------------------------------------------------------
if ! command -v pipx >/dev/null 2>&1; then
  echo "error: pipx is required but not installed." >&2
  echo "  Debian/Ubuntu:  sudo apt install pipx && pipx ensurepath" >&2
  echo "  Other:          python3 -m pip install --user pipx && python3 -m pipx ensurepath" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# 2. Install the package (this puts 'wtf-bin' on PATH)
# ---------------------------------------------------------------------------
if [ "$VERSION" = "latest" ]; then
  ref="git+https://github.com/$REPO"
else
  ref="git+https://github.com/$REPO@$VERSION"
fi

echo "Installing wtf from $ref ..."
pipx install --force "$ref"

# ---------------------------------------------------------------------------
# 3. Write the shell function that captures $? and recent history
# ---------------------------------------------------------------------------
mkdir -p "$CONFIG_DIR"
cat > "$INIT_FILE" <<'EOF'
# wtf shell integration — captures the failed command's context and hands it
# to the wtf-bin executable. Do not rename this to collide with wtf-bin.
wtf() {
  local exit_code=$?                    # MUST be the first line
  local hist; hist=$(fc -ln -10)        # last 10 history entries
  WTF_EXIT="$exit_code" WTF_HISTORY="$hist" wtf-bin "$@"
}
EOF
echo "Wrote shell function to $INIT_FILE"

# ---------------------------------------------------------------------------
# 4. Source it from the user's shell rc, idempotently
# ---------------------------------------------------------------------------
add_source_line() {
  rc="$1"
  [ -e "$rc" ] || return 0
  if ! grep -qF "$INIT_FILE" "$rc"; then
    printf '\n# wtf shell integration\n[ -f "%s" ] && . "%s"\n' "$INIT_FILE" "$INIT_FILE" >> "$rc"
    echo "Added source line to $rc"
  fi
}
add_source_line "$HOME/.bashrc"
add_source_line "$HOME/.zshrc"

echo ""
echo "Done. Open a new terminal, or run:  . \"$INIT_FILE\""
echo "Then trigger a failing command and type: wtf"