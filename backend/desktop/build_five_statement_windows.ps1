# Build on Windows only. Output is UNSIGNED, NONOFFICIAL and UNRELEASED.
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$BackendDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $BackendDir
try {
    & python -m PyInstaller --noconfirm --clean --onefile --windowed `
        --name "AramFivePilot-UNRELEASED" --paths "src" `
        "desktop/aram_five_statement_entry.py"
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller failed: exit $LASTEXITCODE"
    }
    $ExePath = Join-Path $BackendDir "dist/AramFivePilot-UNRELEASED.exe"
    if (-not (Test-Path -LiteralPath $ExePath -PathType Leaf)) {
        throw "No executable produced"
    }
    Write-Host "Unsigned local inspection build: $ExePath"
}
finally {
    Pop-Location
}
