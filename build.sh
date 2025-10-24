#!/bin/bash

# Script per creare la distribuzione di Flutterator
set -e

echo "🚀 Creando distribuzione Flutterator..."

# Nome della versione
VERSION="v1.0.0"
DIST_NAME="flutterator-${VERSION}"

# Pulisci directory precedenti
rm -rf dist/
mkdir -p dist/${DIST_NAME}/bin
mkdir -p dist/${DIST_NAME}/lib

echo "📦 Copiando file necessari..."

# Copia il file principale esistente e adattalo per la distribuzione
cp flutterator.py dist/${DIST_NAME}/lib/
# Copia tutti i file dei generatori mantenendo la struttura
cp -r generators/* dist/${DIST_NAME}/lib/

# Correggi gli import nel file principale per la distribuzione
# Rimuovi l'import generators e aggiungi gli import corretti
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' 's/from generators import \*/# Import corretti per distribuzione/' dist/${DIST_NAME}/lib/flutterator.py
else
    # Linux
    sed -i 's/from generators import \*/# Import corretti per distribuzione/' dist/${DIST_NAME}/lib/flutterator.py
fi

# Aggiungi gli import necessari dopo la riga con sys e pathlib
cat > temp_imports.txt << 'EOF'

# Aggiungi il path dei moduli al sys.path per la distribuzione
lib_path = Path(__file__).parent
sys.path.insert(0, str(lib_path))

# Import dei moduli necessari
from main import init
EOF

# Inserisci gli import dopo le import standard
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' '/from pathlib import Path/r temp_imports.txt' dist/${DIST_NAME}/lib/flutterator.py
else
    # Linux  
    sed -i '/from pathlib import Path/r temp_imports.txt' dist/${DIST_NAME}/lib/flutterator.py
fi

# Rimuovi il file temporaneo
rm -f temp_imports.txt

# Correggi gli import relativi nel file main.py
sed -i '' 's/from \.assets/from assets.main/g' dist/${DIST_NAME}/lib/main.py
sed -i '' 's/from \.config/from config.main/g' dist/${DIST_NAME}/lib/main.py
sed -i '' 's/from \.templates/from templates.main/g' dist/${DIST_NAME}/lib/main.py
sed -i '' 's/from \.initializator/from initializator/g' dist/${DIST_NAME}/lib/main.py
cp requirements.txt dist/${DIST_NAME}/ 2>/dev/null || echo "requirements.txt not found, creating one..."

# Crea requirements.txt se non esiste
if [ ! -f requirements.txt ]; then
    echo "click>=8.0.0" > dist/${DIST_NAME}/requirements.txt
fi

# Crea l'eseguibile wrapper nella directory bin
cat > dist/${DIST_NAME}/bin/flutterator << 'EOF'
#!/bin/bash

# Flutterator CLI Wrapper
# Trova la directory di installazione
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLUTTERATOR_ROOT="$(dirname "$SCRIPT_DIR")"
FLUTTERATOR_LIB="$FLUTTERATOR_ROOT/lib"

# Controlla se Python3 è disponibile
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Esegui flutterator.py dalla directory lib
cd "$FLUTTERATOR_LIB"
exec python3 flutterator.py "$@"
EOF

# Crea wrapper per Windows
cat > dist/${DIST_NAME}/bin/flutterator.bat << 'EOF'
@echo off

REM Flutterator CLI Wrapper per Windows
set SCRIPT_DIR=%~dp0
for %%I in ("%SCRIPT_DIR%\..") do set FLUTTERATOR_ROOT=%%~fI
set FLUTTERATOR_LIB=%FLUTTERATOR_ROOT%\lib

REM Controlla se Python è disponibile
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    exit /b 1
)

REM Esegui flutterator.py dalla directory lib
cd /d "%FLUTTERATOR_LIB%"
python flutterator.py %*
EOF

# Crea script di installazione per Unix/Linux/Mac
cat > dist/${DIST_NAME}/install.sh << 'EOF'
#!/bin/bash
echo "🚀 Installing Flutterator..."

# Ottieni la directory corrente (dove è stato estratto flutterator)
FLUTTERATOR_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLUTTERATOR_BIN="$FLUTTERATOR_ROOT/bin"

# Controlla se Python3 è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Controlla se pip è installato
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

# Installa dipendenze
echo "📦 Installing dependencies..."
if pip3 install --user -r requirements.txt 2>/dev/null || pip3 install --break-system-packages -r requirements.txt 2>/dev/null; then
    echo "✅ Dependencies installed successfully!"
else
    echo "⚠️  Could not install dependencies automatically."
    echo "📋 Please install manually with one of these commands:"
    echo "   pip3 install --user -r requirements.txt"
    echo "   pip3 install --break-system-packages -r requirements.txt"
    echo "   python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt"
fi

# Rendi eseguibile il wrapper
chmod +x bin/flutterator

echo "✅ Flutterator installed successfully!"
echo ""
echo "📋 To use Flutterator from anywhere, add this to your PATH:"
echo "   export PATH=\"$FLUTTERATOR_BIN:\$PATH\""
echo ""
echo "🔧 Add the following line to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
echo "   export PATH=\"$FLUTTERATOR_BIN:\$PATH\""
echo ""
echo "🚀 Then restart your terminal or run:"
echo "   source ~/.bashrc  # or ~/.zshrc"
echo ""
echo "💡 After that, you can use 'flutterator' from anywhere!"

# Chiedi se aggiungere automaticamente al PATH
read -p "Do you want to automatically add Flutterator to your PATH? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Rileva il tipo di shell
    if [[ "$SHELL" == */zsh ]]; then
        PROFILE="$HOME/.zshrc"
    elif [[ "$SHELL" == */bash ]]; then
        PROFILE="$HOME/.bashrc"
    else
        PROFILE="$HOME/.profile"
    fi
    
    # Controlla se il PATH è già configurato
    if ! grep -q "flutterator" "$PROFILE" 2>/dev/null; then
        echo "" >> "$PROFILE"
        echo "# Flutterator CLI" >> "$PROFILE"
        echo "export PATH=\"$FLUTTERATOR_BIN:\$PATH\"" >> "$PROFILE"
        echo "✅ Added to $PROFILE"
        echo "🔄 Please restart your terminal or run: source $PROFILE"
    else
        echo "ℹ️  Flutterator PATH already configured in $PROFILE"
    fi
fi
EOF

# Crea script di installazione per Windows
cat > dist/${DIST_NAME}/install.bat << 'EOF'
@echo off
echo 🚀 Installing Flutterator...

REM Ottieni la directory corrente
set FLUTTERATOR_ROOT=%~dp0
set FLUTTERATOR_BIN=%FLUTTERATOR_ROOT%bin

REM Controlla se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    pause
    exit /b 1
)

REM Installa dipendenze
echo 📦 Installing dependencies...
pip install -r requirements.txt

echo ✅ Flutterator installed successfully!
echo.
echo � To use Flutterator from anywhere, add this to your PATH:
echo    %FLUTTERATOR_BIN%
echo.
echo 🔧 Steps to add to PATH:
echo    1. Press Win + R, type "sysdm.cpl" and press Enter
echo    2. Click "Environment Variables..."
echo    3. Under "User variables", select "Path" and click "Edit..."
echo    4. Click "New" and add: %FLUTTERATOR_BIN%
echo    5. Click "OK" on all dialogs
echo    6. Restart Command Prompt
echo.
echo 💡 After that, you can use 'flutterator' from anywhere!
pause
EOF

# Crea README per la distribuzione
cat > dist/${DIST_NAME}/README.md << 'EOF'
# Flutterator

🚀 CLI per creare e gestire progetti Flutter con struttura personalizzata

## Installation

### Quick Start
1. Extract the zip file to your desired location (e.g., `~/flutterator/`)
2. Run the installer for your platform:

#### Unix/Linux/Mac
```bash
chmod +x install.sh
./install.sh
```

#### Windows
```cmd
install.bat
```

### Manual PATH Setup

#### Unix/Linux/Mac
Add this line to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
export PATH="/path/to/flutterator/bin:$PATH"
```

#### Windows
1. Press `Win + R`, type `sysdm.cpl` and press Enter
2. Click "Environment Variables..."
3. Under "User variables", select "Path" and click "Edit..."
4. Click "New" and add the path to `flutterator/bin` folder
5. Click "OK" on all dialogs and restart Command Prompt

## Usage

After installation, you can use `flutterator` from anywhere:

```bash
# Crea un nuovo progetto
flutterator create --name myapp --login

# Aggiunge una feature
flutterator add --feature notes

# Help
flutterator --help
```

## Directory Structure

```
flutterator/
├── bin/
│   ├── flutterator       # Unix/Linux/Mac executable
│   └── flutterator.bat   # Windows executable
├── lib/
│   ├── flutterator.py    # Main CLI script
│   └── generators/       # Code generation modules
├── install.sh            # Unix installer
├── install.bat           # Windows installer
└── requirements.txt      # Python dependencies
```

## Requirements

- Python 3.7+
- Flutter SDK
- pip

---

Creato da Lorenzo Busi @ GetAutomation
EOF

# Rendi eseguibili gli script
chmod +x dist/${DIST_NAME}/install.sh
chmod +x dist/${DIST_NAME}/bin/flutterator
chmod +x dist/${DIST_NAME}/lib/flutterator.py

echo "📁 Creando archivio..."
cd dist/
zip -r ${DIST_NAME}.zip ${DIST_NAME}/
cd ..

echo "✅ Distribuzione creata: dist/${DIST_NAME}.zip"
echo ""
echo "📋 Struttura (simile a Flutter SDK):"
echo "   flutterator/"
echo "   ├── bin/"
echo "   │   ├── flutterator       # Eseguibile Unix/Mac"
echo "   │   └── flutterator.bat   # Eseguibile Windows"
echo "   ├── lib/"
echo "   │   ├── flutterator.py    # CLI principale"
echo "   │   └── generators/       # Moduli generazione"
echo "   ├── install.sh            # Installer Unix/Mac"
echo "   ├── install.bat           # Installer Windows"
echo "   └── README.md             # Istruzioni complete"
echo ""
echo "🚀 Installazione per gli utenti:"
echo "   1. unzip ${DIST_NAME}.zip"
echo "   2. cd ${DIST_NAME}"
echo "   3. ./install.sh  (Unix/Mac) o install.bat (Windows)"
echo "   4. Aggiungere bin/ al PATH di sistema"
echo "   5. Usare 'flutterator' da qualsiasi directory!"
