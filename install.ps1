#!/usr/bin/env pwsh
#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Repo = 'jacobshultz/wtf'
$ConfigDir = Join-Path $HOME '.config/wtf'

$Runner   = Join-Path $ConfigDir 'wtf-run.ps1'
$Settings = Join-Path $ConfigDir 'wtf-settings.json'
$PromptFile = Join-Path $ConfigDir 'PROMPT.txt'

function Write-Err {
    param([string]$Message)
    [Console]::Error.WriteLine($Message)
}

# Set-Content -Encoding UTF8 writes a BOM on Windows PowerShell 5.1 and no BOM
# on PowerShell 7+. Write the bytes directly so both editions behave the same.
function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][AllowEmptyString()][string]$Text
    )
    if (-not $Text.EndsWith("`n")) { $Text += "`r`n" }
    [IO.File]::WriteAllText($Path, $Text, [Text.UTF8Encoding]::new($false))
}

function Add-Utf8NoBom {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][AllowEmptyString()][string]$Text
    )
    [IO.File]::AppendAllText($Path, $Text, [Text.UTF8Encoding]::new($false))
}

# ---------------------------------------------------------------------------
# Ensure dependencies are available
# ---------------------------------------------------------------------------
foreach ($dep in 'python', 'pipx', 'ollama') {
    if (-not (Get-Command $dep -ErrorAction SilentlyContinue)) {
        Write-Err "error: $dep is required but not installed."
        exit 1
    }
}

# ---------------------------------------------------------------------------
# Install the package (this puts 'wtf-bin' on PATH)
# ---------------------------------------------------------------------------
Write-Host "Installing wtf from git+https://github.com/$Repo ..."
& pipx install --force "git+https://github.com/$Repo"
if ($LASTEXITCODE -ne 0) {
    Write-Err 'error: pipx install failed.'
    exit 1
}

if (-not (Get-Command 'wtf-bin' -ErrorAction SilentlyContinue)) {
    Write-Host "warning: wtf-bin is not on PATH. Run 'pipx ensurepath' and restart your shell."
}

# ---------------------------------------------------------------------------
# Write to the configuration folder
# ---------------------------------------------------------------------------
New-Item -ItemType Directory -Path $ConfigDir -Force | Out-Null

$RunnerBody = @'
function wtf {
    $ok = $?
    $exitCode = Get-Variable -Name LASTEXITCODE -Scope Global -ValueOnly -ErrorAction SilentlyContinue
    if ($null -eq $exitCode) { if ($ok) { $exitCode = 0 } else { $exitCode = 1 } }

    $n = 1
    for ($i = 0; $i -lt $args.Count; $i++) {
        if ($args[$i] -eq '--lines' -or $args[$i] -eq '-l') {
            if (($i + 1) -lt $args.Count) { $n = [int]$args[$i + 1] }
        }
    }

    # Skip the 'wtf' call itself; PowerShell may commit it to history early.
    $entries = @(Get-History | Where-Object { $_.CommandLine -notmatch '^\s*wtf(\s|$)' })
    if ($entries.Count -gt $n) { $entries = $entries[-$n..-1] }
    $history = ($entries | ForEach-Object { $_.CommandLine }) -join "`n"

    $env:WTF_EXIT = $exitCode
    $env:WTF_HISTORY = $history
    try {
        & wtf-bin @args
    } finally {
        Remove-Item Env:WTF_EXIT, Env:WTF_HISTORY -ErrorAction SilentlyContinue
    }
}
'@

Write-Utf8NoBom -Path $Runner -Text $RunnerBody
Write-Host "Wrote shell function to $Runner"

$SettingsBody = @'
{
    "Version": "1.0.0",
    "Model": "qwen3:4b",
    "Think": true,
    "UseTools": false,
    "Debug": false
}
'@

Write-Utf8NoBom -Path $Settings -Text $SettingsBody
Write-Host "Wrote settings to $Settings"

$PromptBody = @'
You examine command-line errors, determine their sources, and output cause and remedial steps to the user that produced the error.
If you are unsure of the source or solution(s) to the problem use web search tools if you have access to any.
THINK EXTREMELY HARD and DO NOT STOP until you have determined the cause of the error.
THINK EXTREMELY HARD and DO NOT STOP until you have determined remedial options.
ABSOLUTELY NEVER, UNDER ANY CIRCUMSTANCES output more than one or two paragraph worth of content.
ABSOLUTELY NEVER, UNDER ANY CIRCUMSTANCES tell the user about the exit code. The user does not care about exit codes.
'@

Write-Utf8NoBom -Path $PromptFile -Text $PromptBody
Write-Host "Wrote prompt to $PromptFile"

# ---------------------------------------------------------------------------
# Add the dot-source line to the PowerShell profile(s)
# ---------------------------------------------------------------------------
function Add-SourceLine {
    param([string]$ProfilePath)

    $dir = Split-Path -Parent $ProfilePath
    if (-not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    if (-not (Test-Path -LiteralPath $ProfilePath)) {
        New-Item -ItemType File -Path $ProfilePath -Force | Out-Null
    }

    $content = Get-Content -LiteralPath $ProfilePath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if ($null -eq $content) { $content = '' }

    if ($content.IndexOf($Runner, [StringComparison]::OrdinalIgnoreCase) -lt 0) {
        $line = "`r`n# wtf shell integration`r`nif (Test-Path -LiteralPath `"$Runner`") { . `"$Runner`" }`r`n"
        Add-Utf8NoBom -Path $ProfilePath -Text $line
        Write-Host "Added source line to $ProfilePath"
    }
}

$profiles = @($PROFILE.CurrentUserAllHosts)

# Also cover the other PowerShell edition's profile when it exists.
$docs = [Environment]::GetFolderPath('MyDocuments')
if ($docs) {
    foreach ($leaf in 'PowerShell', 'WindowsPowerShell') {
        $other = Join-Path (Join-Path $docs $leaf) 'profile.ps1'
        if ((Test-Path -LiteralPath (Split-Path -Parent $other)) -and ($profiles -notcontains $other)) {
            $profiles += $other
        }
    }
}

foreach ($p in $profiles) { Add-SourceLine $p }

Write-Host ''
Write-Host "Done. Open a new terminal, or run:  . `"$Runner`""
Write-Host 'Then trigger a failing command and type: wtf'
Write-Host 'If the profile does not load, check: Get-ExecutionPolicy -List'