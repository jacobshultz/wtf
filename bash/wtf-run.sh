wtf() {
  local exit_code=$?
  local n=1
  local args=("$@")
  for i in "${!args[@]}"; do
    if [[ "${args[$i]}" == "--lines" || "${args[$i]}" == "-l" ]]; then
      n="${args[$((i+1))]}"
    fi
  done
  local history; history=$(fc -ln -"$n" -1)
  WTF_EXIT="$exit_code" WTF_HISTORY="$history" command wtf-bin "$@"
}
