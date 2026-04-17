#!/usr/bin/env bash
# AlphaSkills installer for macOS / Linux
# Usage: ./install.sh          # installs to ~/.claude/skills/
#        ./install.sh --codex  # installs to ~/.codex/skills/ (Codex CLI mode)
#        ./install.sh --both   # installs to both

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILLS_SRC="$SCRIPT_DIR/skills"

if [ ! -d "$SKILLS_SRC" ]; then
    echo "✗ Skills source not found: $SKILLS_SRC"
    exit 1
fi

# Mode flags
INSTALL_CLAUDE=true
INSTALL_CODEX=false

for arg in "$@"; do
    case "$arg" in
        --codex) INSTALL_CLAUDE=false; INSTALL_CODEX=true ;;
        --both)  INSTALL_CLAUDE=true;  INSTALL_CODEX=true ;;
        --help|-h)
            echo "AlphaSkills installer"
            echo ""
            echo "Usage:"
            echo "  ./install.sh          Install to ~/.claude/skills/ (Claude Code / Projects / Desktop)"
            echo "  ./install.sh --codex  Install to ~/.codex/skills/ (OpenAI Codex CLI)"
            echo "  ./install.sh --both   Install to both"
            exit 0
            ;;
    esac
done

link_skill() {
    local target_dir=$1
    mkdir -p "$target_dir"
    for skill_src in "$SKILLS_SRC"/*/; do
        local skill_name
        skill_name="$(basename "$skill_src")"
        local dest="$target_dir/$skill_name"
        if [ -e "$dest" ]; then
            echo "  ↻ $skill_name (already exists, skipping — use --force to overwrite)"
        else
            ln -s "$skill_src" "$dest"
            echo "  ✓ $skill_name"
        fi
    done
}

echo "AlphaSkills installer"
echo "===================="
echo ""

if [ "$INSTALL_CLAUDE" = true ]; then
    CLAUDE_TARGET="$HOME/.claude/skills"
    echo "Installing to $CLAUDE_TARGET (Claude Code / Projects / Desktop)..."
    link_skill "$CLAUDE_TARGET"
    echo ""
fi

if [ "$INSTALL_CODEX" = true ]; then
    CODEX_TARGET="$HOME/.codex/skills"
    echo "Installing to $CODEX_TARGET (OpenAI Codex CLI)..."
    link_skill "$CODEX_TARGET"
    echo ""
fi

echo "Done. In any Claude chat, try:"
echo "  /skill stock-signal-report NVDA"
echo "  /skill company-deepdive MRNA"
echo "  /skill hedge-fund-holdings berkshire"
