<#
.SYNOPSIS
    Stop the Langflow server started from this chapter.

.DESCRIPTION
    Finds the process listening on the given port and stops it.

.EXAMPLE
    .\scripts\stop_langflow.ps1
    .\scripts\stop_langflow.ps1 -Port 7861
#>
[CmdletBinding()]
param(
    [int]$Port = 7860
)

$listeners = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue

if (-not $listeners) {
    Write-Host "Nothing is listening on port $Port."
    return
}

foreach ($listener in $listeners) {
    try {
        Stop-Process -Id $listener.OwningProcess -Force -ErrorAction Stop
        Write-Host "Stopped PID $($listener.OwningProcess) (port $Port)."
    }
    catch {
        Write-Warning "Could not stop PID $($listener.OwningProcess): $($_.Exception.Message)"
    }
}
