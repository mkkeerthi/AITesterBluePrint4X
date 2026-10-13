<#
.SYNOPSIS
    Start the Langflow server for this chapter.

.DESCRIPTION
    Boots Langflow from the machine-level Python 3.13 and points it at the
    project-local data directory (flows, credentials, chat history), so this
    instance is self-contained and independent of any other install. No
    project-local virtualenv is required.

    The interpreter is resolved automatically: the Windows launcher (`py -3.13`)
    is used when available, otherwise `python` from PATH.

.EXAMPLE
    .\scripts\run_langflow.ps1
    .\scripts\run_langflow.ps1 -LangflowHost 0.0.0.0 -Port 7861
#>
[CmdletBinding()]
param(
    [string]$LangflowHost = '127.0.0.1',
    [int]$Port = 7860
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$dataDir = Join-Path $root 'langflow_data'
$dbPath = (Join-Path $dataDir 'langflow.db').Replace('\', '/')

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

$pythonLabel = (@($pythonExe) + $pythonPrefix) -join ' '

& $pythonExe @pythonPrefix -c "import langflow" 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "Langflow is not installed for $pythonLabel. Run: .\scripts\install_langflow.ps1"
}
if (-not (Test-Path (Join-Path $dataDir 'langflow.db'))) {
    throw "Langflow database not found at $dataDir\langflow.db. See README.md setup steps."
}

$env:LANGFLOW_CONFIG_DIR = $dataDir
$env:LANGFLOW_DATABASE_URL = "sqlite:///$dbPath"
$env:LANGFLOW_COMPONENTS_PATH = Join-Path $root 'Components'

Write-Host "Python            : $pythonLabel"
Write-Host "Langflow data dir : $dataDir"
Write-Host "Langflow database : $dbPath"
Write-Host "Custom components : $env:LANGFLOW_COMPONENTS_PATH"
Write-Host "Starting server on http://${LangflowHost}:$Port (first start is slow) ..."

& $pythonExe @pythonPrefix -m langflow run --host $LangflowHost --port $Port
