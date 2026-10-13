<#
.SYNOPSIS
    Install Langflow into the machine-level Python 3.13.

.DESCRIPTION
    One-time setup: installs (or upgrades) Langflow into the machine-level
    Python 3.13, so run_langflow.ps1 no longer needs a project-local virtualenv.
    The interpreter is resolved automatically: the Windows launcher (`py -3.13`)
    is used when available, otherwise `python` from PATH.

    If the global install fails (for example a permissions error on an all-users
    Python under Program Files), it retries into the user site-packages with
    --user.

.EXAMPLE
    .\scripts\install_langflow.ps1
    .\scripts\install_langflow.ps1 -Requirement "langflow==1.12.1"
#>
[CmdletBinding()]
param(
    [string]$Requirement = 'langflow'
)

$ErrorActionPreference = 'Stop'

# Machine-level Python 3.13: prefer the Windows launcher, fall back to python on PATH.
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonExe = 'py'
    $pythonPrefix = @('-3.13')
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonExe = (Get-Command python).Source
    $pythonPrefix = @()
}
else {
    throw "Python 3.13 was not found. Install Python 3.13 (or the py launcher) and ensure it is on PATH."
}

Write-Host "Using interpreter:"
& $pythonExe @pythonPrefix -c "import sys; print(sys.executable)"

& $pythonExe @pythonPrefix -m pip install --upgrade pip
& $pythonExe @pythonPrefix -m pip install $Requirement

if ($LASTEXITCODE -ne 0) {
    Write-Warning "Global install failed; retrying into the user site-packages (--user)."
    & $pythonExe @pythonPrefix -m pip install --user $Requirement
    if ($LASTEXITCODE -ne 0) {
        throw "pip install failed. Check the output above."
    }
}

Write-Host "Done. Verify with: python -m langflow --version"
