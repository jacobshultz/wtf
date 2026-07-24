function wtf {
    $exit = $LASTEXITCODE
    $last = (Get-History -Count 10).CommandLine
    $env:WTF_EXIT = $exit
    $env:WTF_HISTORY = $last
    wtf-bin @args
}