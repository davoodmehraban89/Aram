# Build only on a Windows machine with Python, Tkinter and PyInstaller installed.
# This is an UNSIGNED, UNRELEASED pilot; never claim financial readiness.
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$BackendDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $BackendDir
try {
    & python -m PyInstaller --noconfirm --clean --onefile --windowed `
        --name "AramPilot-UNRELEASED" --paths "src" `
        "desktop/aram_pilot_entry.py"
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller exited with error code $LASTEXITCODE"
    }
    $ExePath = Join-Path $BackendDir "dist/AramPilot-UNRELEASED.exe"
    if (-not (Test-Path -LiteralPath $ExePath -PathType Leaf)) {
        throw "PyInstaller did not produce the expected Windows EXE"
    }
    Write-Host "Unsigned, unreleased desktop pilot built: $ExePath"
}
finally {
    Pop-Location
}
