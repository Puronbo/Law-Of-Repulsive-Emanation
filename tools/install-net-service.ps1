# Puno Net - install as a Windows supervised service (Task Scheduler).
#
# Creates a scheduled task "PunoNet" that:
#   * starts at log-on (and at startup for the current user account)
#   * restarts on failure up to 5 times, waiting 60s between attempts
#   * runs with no execution-time limit (indefinite service)
#   * writes stdout/stderr to a rotating log via the service itself
#
# The app is already self-healing (checkpoints + resume), so a restart
# after a crash simply continues the same tick counter and RNG stream.
#
# Usage:
#   .\tools\install-net-service.ps1 [-PythonPath <python.exe>]
#                                   [-Port 8766] [-Checkpoint <path>]
#   .\tools\uninstall-net-service.ps1
#
# The default PythonPath is the venv python next to this repo (.\venv),
# falling back to the system python on PATH.

param(
    [string]$PythonPath = "",
    [int]$Port = 8766,
    [string]$Checkpoint = ""
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot

if (-not $PythonPath) {
    $venvPy = Join-Path $RepoRoot "venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $venvPy) {
        $PythonPath = $venvPy
    } else {
        $PythonPath = (Get-Command python).Source
    }
}
if (-not (Test-Path -LiteralPath $PythonPath)) {
    Write-Error "python not found: $PythonPath"
}
if (-not $Checkpoint) {
    $Checkpoint = Join-Path $RepoRoot "live.pkl"
}

$argument = "-m puno_app.live_net --port $Port --save `"$Checkpoint`""
$cwd = $RepoRoot

$action = New-ScheduledTaskAction `
    -Execute $PythonPath `
    -Argument $argument `
    -WorkingDirectory $cwd

$triggers = @(
    (New-ScheduledTaskTrigger -AtLogOn),
    (New-ScheduledTaskTrigger -AtStartup)
)

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -RestartCount 5 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -MultipleInstances IgnoreNew

$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME `
    -LogonType Interactive

Register-ScheduledTask -TaskName "PunoNet" `
    -Action $action -Trigger $triggers `
    -Settings $settings -Principal $principal -Force | Out-Null

Write-Output "PunoNet task installed."
Write-Output "  python   : $PythonPath"
Write-Output "  command  : $PythonPath $argument"
Write-Output "  cwd      : $cwd"
Write-Output "  restarts : up to 5, 60s apart (on failure)"
Write-Output ""
Write-Output "Start it now with:"
Write-Output "  Start-ScheduledTask -TaskName PunoNet"
Write-Output "Watch it with:"
Write-Output "  python -m puno_app.live_net --status --port $Port"
