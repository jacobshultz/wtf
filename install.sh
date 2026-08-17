#!/usr/bin/env sh
set -eu

REPO="jacobshultz/wtf"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/wtf"
RUNNER="$CONFIG_DIR/wtf-run.sh"
SETTINGS="$CONFIG_DIR/wtf-settings.json"
PROMPT="$CONFIG_DIR/PROMPT.txt"

# ---------------------------------------------------------------------------
# Ensure dependencies are available
# ---------------------------------------------------------------------------
if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python is required but not installed." >&2
  exit 1
fi

if ! command -v pipx >/dev/null 2>&1; then
  echo "error: pipx is required but not installed." >&2
  exit 1
fi

if ! command -v ollama >/dev/null 2>&1; then
  echo "error: ollama is required but not installed." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Install the package (this puts 'wtf-bin' on PATH)
# ---------------------------------------------------------------------------
echo "Installing wtf from git+https://github.com/$REPO ..."
pipx install --force "git+https://github.com/jacobshultz/wtf"

# ---------------------------------------------------------------------------
# Write to the configuration folder
# ---------------------------------------------------------------------------
mkdir -p "$CONFIG_DIR"
cat > "$RUNNER" <<'EOF'
wtf() {
  local exit_code=$?
  local n=1
  local args=("$@")
  for i in "${!args[@]}"; do
    if [[ "${args[$i]}" == "--lines" || "${args[$i]}" == "-l" ]]; then
      n="${args[$((i+1))]}"
    fi
  done
  local history
  history=$(fc -ln -50 -1 \
    | sed 's/^[[:space:]]*//' \
    | grep -vE '^wtf($|[[:space:]])' \
    | tail -n "$n")
  WTF_EXIT="$exit_code" WTF_HISTORY="$history" command wtf-bin "$@"
}
EOF
echo "Wrote shell function to $RUNNER"

cat > "$SETTINGS" <<'EOF'
{
    "Version": "1.0.0",
    "Model": "qwen3:4b",
    "Think": true,
    "UseTools": false,
    "Debug": false
}
EOF
echo "Wrote settings to $SETTINGS"

cat > "$PROMPT" <<'EOF'
You examine command-line errors, determine their sources, and output cause and remedial steps to the user that produced the error.
If you are unsure of the source or solution(s) to the problem use web search tools if you have access to any.
THINK EXTREMELY HARD and DO NOT STOP until you have determined the cause of the error.
THINK EXTREMELY HARD and DO NOT STOP until you have determined remedial options.
ABSOLUTELY NEVER, UNDER ANY CIRCUMSTANCES output more than one or two paragraph worth of content.
ABSOLUTELY NEVER, UNDER ANY CIRCUMSTANCES tell the user about the exit code. The user does not care about exit codes.
EOF
echo "Wrote settings to $SETTINGS"

# ---------------------------------------------------------------------------
# Add the line to bash.rc
# ---------------------------------------------------------------------------
add_source_line() {
  rc="$1"
  [ -e "$rc" ] || return 0
  if ! grep -qF "$RUNNER" "$rc"; then
    printf '\n# wtf shell integration\n[ -f "%s" ] && . "%s"\n' "$RUNNER" "$RUNNER" >> "$rc"
    echo "Added source line to $rc"
  fi
}
add_source_line "$HOME/.bashrc"
add_source_line "$HOME/.zshrc"

echo ""
echo "Done. Logout, then open a new terminal, or run:  . \"$RUNNER\""
echo "Then trigger a failing command and type: wtf"