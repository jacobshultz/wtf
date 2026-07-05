wtf() {
  local exit_code=$?
  local history; history=$(fc -ln -1)
  WTF_EXIT="$exit_code" WTF_HISTORY="$history" command wtf-bin "$@"
}