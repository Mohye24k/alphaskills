# AlphaSkills installer for Windows PowerShell (5.1 and 7+ compatible)
# Usage:
#   .\install.ps1                # installs to ~/.claude/skills/
#   .\install.ps1 -Codex         # installs to ~/.codex/skills/
#   .\install.ps1 -Both          # installs to both
#   .\install.ps1 -Force         # overwrite existing skill installs

param(
    [switch]$Codex,
    [switch]$Both,
    [switch]$Force,
    [switch]$Help
)

if ($Help) {
    Write-Host "AlphaSkills installer"
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  .\install.ps1          Install to ~/.claude/skills/ (Claude Code / Projects / Desktop)"
    Write-Host "  .\install.ps1 -Codex   Install to ~/.codex/skills/ (OpenAI Codex CLI)"
    Write-Host "  .\install.ps1 -Both    Install to both"
    Write-Host "  .\install.ps1 -Force   Overwrite existing symlinks"
    exit 0
}

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillsSrc = Join-Path $scriptDir "skills"

if (-not (Test-Path $skillsSrc)) {
    Write-Host "[ERROR] Skills source not found: $skillsSrc" -ForegroundColor Red
    exit 1
}

$installClaude = -not $Codex
$installCodex = $Codex -or $Both
if ($Both) { $installClaude = $true }

function Install-Skills {
    param([string]$TargetDir, [string]$Label)

    if (-not (Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
        Write-Host "  Created directory: $TargetDir" -ForegroundColor Gray
    }

    Write-Host "Installing to $TargetDir ($Label)..."
    $skills = Get-ChildItem -Path $skillsSrc -Directory

    foreach ($skill in $skills) {
        $name = $skill.Name
        $dest = Join-Path $TargetDir $name

        if (Test-Path $dest) {
            if ($Force) {
                Remove-Item $dest -Recurse -Force
            } else {
                Write-Host "  [SKIP] $name (already exists, use -Force to overwrite)"
                continue
            }
        }

        $symlinkOk = $false
        try {
            New-Item -ItemType SymbolicLink -Path $dest -Target $skill.FullName -ErrorAction Stop | Out-Null
            $symlinkOk = $true
            Write-Host "  [OK] $name (symlink)" -ForegroundColor Green
        } catch {
            $symlinkOk = $false
        }

        if (-not $symlinkOk) {
            Copy-Item -Path $skill.FullName -Destination $dest -Recurse
            Write-Host "  [OK] $name (copy - run PowerShell as admin to use symlinks instead)" -ForegroundColor Yellow
        }
    }
    Write-Host ""
}

Write-Host "AlphaSkills installer"
Write-Host "===================="
Write-Host ""

if ($installClaude) {
    Install-Skills -TargetDir "$HOME\.claude\skills" -Label "Claude Code / Projects / Desktop"
}

if ($installCodex) {
    Install-Skills -TargetDir "$HOME\.codex\skills" -Label "OpenAI Codex CLI"
}

Write-Host "Done. In any Claude chat, try:"
Write-Host "  /skill stock-signal-report NVDA"
Write-Host "  /skill company-deepdive MRNA"
Write-Host "  /skill hedge-fund-holdings berkshire"
Write-Host "  /skill patient-trial-navigator (for medical questions)"
Write-Host "  /skill alphastack-life-navigator (the master router)"
