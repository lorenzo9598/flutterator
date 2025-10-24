#!/bin/bash

echo "🚀 Creando eseguibile standalone con PyInstaller..."

# Installa PyInstaller se non presente
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Installando PyInstaller..."
    pip3 install pyinstaller
fi

# Crea l'eseguibile
pyinstaller --onefile --name flutterator flutterator.py

echo "✅ Eseguibile creato in dist/flutterator"
echo "💡 Ora puoi distribuire solo il file dist/flutterator senza dipendenze Python"
