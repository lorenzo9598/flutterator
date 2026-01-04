#!/bin/bash

# =============================================================================
# Build Standalone Executable
# =============================================================================
# Crea un eseguibile standalone che include Python + tutte le dipendenze
# L'utente scarica UN file e funziona subito, senza installare nulla
# =============================================================================

set -e

VERSION="v3.0.1"
echo "🚀 Building Flutterator ${VERSION} standalone executable..."
echo ""

# -----------------------------------------------------------------------------
# Verifica PyInstaller
# -----------------------------------------------------------------------------
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Installing PyInstaller..."
    pip3 install pyinstaller
fi

# -----------------------------------------------------------------------------
# Pulisci build precedenti
# -----------------------------------------------------------------------------
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/flutterator dist/flutterator.app 2>/dev/null || true

# -----------------------------------------------------------------------------
# Crea eseguibile con PyInstaller
# -----------------------------------------------------------------------------
echo "⚙️  Running PyInstaller..."

pyinstaller \
    --onefile \
    --name flutterator \
    --clean \
    --noconfirm \
    --add-data "generators:generators" \
    --hidden-import click \
    --hidden-import jinja2 \
    --hidden-import rich \
    --hidden-import rich.console \
    --hidden-import rich.panel \
    --hidden-import rich.tree \
    --hidden-import rich.text \
    --hidden-import yaml \
    --hidden-import pyyaml \
    flutterator.py

# -----------------------------------------------------------------------------
# Verifica
# -----------------------------------------------------------------------------
echo ""
if [[ -f "dist/flutterator" ]]; then
    echo "✅ Build successful!"
    echo ""
    echo "📦 Executable: dist/flutterator"
    echo "📏 Size: $(du -h dist/flutterator | cut -f1)"
    echo ""
    echo "🧪 Test:"
    ./dist/flutterator --version 2>/dev/null || ./dist/flutterator --help | head -5
    echo ""
    echo "🚀 Usage:"
    echo "   1. Copy 'dist/flutterator' anywhere"
    echo "   2. Run: ./flutterator --help"
    echo ""
    echo "💡 No Python or dependencies needed on target machine!"
else
    echo "❌ Build failed!"
    exit 1
fi
