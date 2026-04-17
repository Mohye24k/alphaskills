# AlphaSkills installer for Windows PowerShell
# Usage:
#   .\install.ps1                # installs to %USERPROFILE%\.claude\skills\
#   .\install.ps1 -Codex         # installs to %USERPROFILE%\.codex\skills\ (Codex CLI mode)
#   .\install.ps1 -Both          # installs to both
#   .\install.ps1 -Force         # overwrite existing skill symlinks

param(
    [switch]$Codex,
    [switch]$Both,
    [switch]$Force,
    [switch]$Help
)

if ($Help) {
    Write-Host @"
AlphaSkills installer

Usage:
  .\install.ps1          Install to ~/.claude/skills/ (Claude Code / Projects / Desktop)
  .\install.ps1 -Codex   Install to ~/.codex/skills/ (OpenAI Codex CLI)
  .\install.ps1 -Both    Install to both
  .\install.ps1 -Force   Overwrite existing symlinks
"@
    exit 0
}

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillsSrc = Join-Path $scriptDir "skills"

if (-not (Test-Path $skillsSrc)) {
    Write-Host "✗ Skills source not found: $skillsSrc" -ForegroundColor Red
    exit 1
}

# Mode flags
$installClaude = -not $Codex
$installCodex = $Codex -or $Both
if ($Both) { $installClaude = $true }

function Install-Skills {
    param([string]$TargetDir, [string]$Label)

    if (-not (Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
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
                Write-Host "  ↻ $name (already exists, use -Force to overwrite)"
                continue
            }
        }

        # Prefer symlink (requires admin on Win; falls back to copy)
        try {
            New-Item -ItemType SymbolicLink -Path $dest -Target $skill.FullName -ErrorAction Stop | Out-Null
            Write-Host "  ✓ $name (symlink)" -ForegroundColor Green
        } catch {
            Copy-Item -Path $skill.FullName -Destination $dest -Recurse
            Write-Host "  ✓ $name (copy — no admin for symlink)" -ForegroundColor Yellow
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
