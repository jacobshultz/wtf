function wtf {
    $exit = $LASTEXITCODE
    $last = (Get-History -Count 1).CommandLine
    $env:WTF_EXIT = $exit
    $env:WTF_HISTORY = $last
    wtf-bin @args
}