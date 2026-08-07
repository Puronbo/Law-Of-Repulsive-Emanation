# Puno Net - remove the Windows supervised task.
#
# Usage:  .\tools\uninstall-net-service.ps1

$ErrorActionPreference = "Stop"

$task = Get-ScheduledTask -TaskName "PunoNet" -ErrorAction SilentlyContinue
if (-not $task) {
    Write-Output "No PunoNet task installed."
    exit 0
}

Stop-ScheduledTask -TaskName "PunoNet" -ErrorAction SilentlyContinue
Unregister-ScheduledTask -TaskName "PunoNet" -Confirm:$false
Write-Output "PunoNet task removed."
