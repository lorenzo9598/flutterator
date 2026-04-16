#!/bin/bash

# =============================================================================
# Flutterator Build Script
# Crea una distribuzione standalone del progetto
# =============================================================================

set -e  # Esci in caso di errore

echo "🚀 Creando distribuzione Flutterator..."

# -----------------------------------------------------------------------------
# Configurazione
# -----------------------------------------------------------------------------
VERSION="v3.1.3"
DIST_NAME="flutterator-${VERSION}"
DIST_DIR="dist/${DIST_NAME}"

# -----------------------------------------------------------------------------
# Pulizia e creazione directory
# -----------------------------------------------------------------------------
echo "🧹 Pulizia directory precedenti..."
rm -rf dist/
mkdir -p "${DIST_DIR}/bin"

# -----------------------------------------------------------------------------
# Copia file sorgente
# -----------------------------------------------------------------------------
echo "📦 Copiando file sorgente..."

# Copia il file principale CLI
cp flutterator.py "${DIST_DIR}/"

# Copia l'intera cartella generators mantenendo la struttura
cp -r generators "${DIST_DIR}/"

# Rimuovi i file __pycache__ (non servono nella distribuzione)
find "${DIST_DIR}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "${DIST_DIR}" -type f -name "*.pyc" -delete 2>/dev/null || true

# -----------------------------------------------------------------------------
# Crea requirements.txt con tutte le dipendenze
# -----------------------------------------------------------------------------
echo "📋 Creando requirements.txt..."
cat > "${DIST_DIR}/requirements.txt" << 'EOF'
# Flutterator Dependencies
click>=8.0.0
jinja2>=3.0.0
rich>=13.0.0
pyyaml>=6.0.0
EOF

# -----------------------------------------------------------------------------
# Crea wrapper eseguibile per Unix/Mac
# -----------------------------------------------------------------------------
echo "🔧 Creando wrapper eseguibili..."
cat > "${DIST_DIR}/bin/flutterator" << 'WRAPPER'
#!/bin/bash
# Flutterator CLI Wrapper (Auto-install dependencies)

# Trova la directory di installazione
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLUTTERATOR_ROOT="$(dirname "$SCRIPT_DIR")"
MARKER_FILE="$FLUTTERATOR_ROOT/.deps_installed"

# Controlla se Python3 è disponibile
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "   Install it from https://www.python.org/downloads/"
    exit 1
fi

# Auto-install dipendenze al primo avvio
if [[ ! -f "$MARKER_FILE" ]]; then
    echo "🔧 First run - installing dependencies..."
    
    # Trova pip
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    else
        PIP_CMD="python3 -m pip"
    fi
    
    # Installa dipendenze (silenzioso, con fallback)
    if $PIP_CMD install --user -q click jinja2 rich pyyaml 2>/dev/null || \
       $PIP_CMD install --break-system-packages -q click jinja2 rich pyyaml 2>/dev/null || \
       $PIP_CMD install -q click jinja2 rich pyyaml 2>/dev/null; then
        echo "✅ Dependencies installed!"
        touch "$MARKER_FILE"
    else
        echo "⚠️  Could not auto-install dependencies."
        echo "   Please run: pip3 install click jinja2 rich pyyaml"
        exit 1
    fi
fi

# Esegui flutterator.py nella directory corrente dell'utente
# Aggiungi FLUTTERATOR_ROOT al PYTHONPATH per trovare i moduli 'generators'
export PYTHONPATH="$FLUTTERATOR_ROOT:$PYTHONPATH"
exec python3 "$FLUTTERATOR_ROOT/flutterator.py" "$@"
WRAPPER

chmod +x "${DIST_DIR}/bin/flutterator"

# -----------------------------------------------------------------------------
# Crea wrapper per Windows
# -----------------------------------------------------------------------------
cat > "${DIST_DIR}/bin/flutterator.bat" << 'WRAPPER'
@echo off
REM Flutterator CLI Wrapper per Windows

set SCRIPT_DIR=%~dp0
for %%I in ("%SCRIPT_DIR%\..") do set FLUTTERATOR_ROOT=%%~fI

REM Controlla se Python è disponibile
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    echo    Install it from https://www.python.org/downloads/
    exit /b 1
)

REM Esegui flutterator.py dalla directory root
cd /d "%FLUTTERATOR_ROOT%"
python flutterator.py %*
WRAPPER

# -----------------------------------------------------------------------------
# Crea script di installazione per Unix/Mac
# -----------------------------------------------------------------------------
echo "📦 Creando installer..."
cat > "${DIST_DIR}/install.sh" << 'INSTALLER'
#!/bin/bash
echo "🚀 Installing Flutterator..."
echo ""

# Ottieni la directory corrente
FLUTTERATOR_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLUTTERATOR_BIN="$FLUTTERATOR_ROOT/bin"

# Controlla Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "   Install it from https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Controlla pip
if ! command -v pip3 &> /dev/null; then
    echo "⚠️  pip3 not found, trying python3 -m pip..."
    PIP_CMD="python3 -m pip"
else
    PIP_CMD="pip3"
fi

# Installa dipendenze
echo ""
echo "📦 Installing dependencies..."
if $PIP_CMD install --user -r requirements.txt 2>/dev/null; then
    echo "✅ Dependencies installed successfully!"
elif $PIP_CMD install --break-system-packages -r requirements.txt 2>/dev/null; then
    echo "✅ Dependencies installed successfully!"
else
    echo "⚠️  Automatic installation failed."
    echo ""
    echo "📋 Please install manually:"
    echo "   pip3 install -r requirements.txt"
    echo "   # or"
    echo "   python3 -m pip install -r requirements.txt"
fi

# Rendi eseguibile il wrapper
chmod +x "$FLUTTERATOR_BIN/flutterator"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Flutterator installed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Add Flutterator to your PATH:"
echo ""
echo "   export PATH=\"$FLUTTERATOR_BIN:\$PATH\""
echo ""

# Chiedi se aggiungere automaticamente al PATH
read -p "Add to PATH automatically? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Rileva shell profile
    if [[ "$SHELL" == */zsh ]]; then
        PROFILE="$HOME/.zshrc"
    elif [[ "$SHELL" == */bash ]]; then
        PROFILE="$HOME/.bashrc"
    else
        PROFILE="$HOME/.profile"
    fi
    
    # Aggiungi al PATH se non presente
    if ! grep -q "flutterator" "$PROFILE" 2>/dev/null; then
        echo "" >> "$PROFILE"
        echo "# Flutterator CLI" >> "$PROFILE"
        echo "export PATH=\"$FLUTTERATOR_BIN:\$PATH\"" >> "$PROFILE"
        echo ""
        echo "✅ Added to $PROFILE"
        echo "🔄 Run: source $PROFILE"
    else
        echo "ℹ️  Already configured in $PROFILE"
    fi
fi

echo ""
echo "🚀 Usage:"
echo "   flutterator --help"
echo "   flutterator create --name myapp"
echo "   flutterator add-domain --name todo --fields \"title:string,done:bool\""
echo "   flutterator add-component --name todo_list --type list"
echo ""
INSTALLER

chmod +x "${DIST_DIR}/install.sh"

# -----------------------------------------------------------------------------
# Crea script di installazione per Windows
# -----------------------------------------------------------------------------
cat > "${DIST_DIR}/install.bat" << 'INSTALLER'
@echo off
echo 🚀 Installing Flutterator...
echo.

set FLUTTERATOR_ROOT=%~dp0
set FLUTTERATOR_BIN=%FLUTTERATOR_ROOT%bin

REM Controlla Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    echo    Install it from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Installa dipendenze
echo 📦 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ⚠️  Failed to install dependencies
    echo    Try: pip install click jinja2 rich pyyaml
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ✅ Flutterator installed!
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📋 Add this folder to your PATH:
echo    %FLUTTERATOR_BIN%
echo.
echo 🔧 Steps:
echo    1. Press Win + R, type "sysdm.cpl", press Enter
echo    2. Click "Environment Variables..."
echo    3. Under "User variables", select "Path", click "Edit..."
echo    4. Click "New" and paste: %FLUTTERATOR_BIN%
echo    5. Click "OK" on all dialogs
echo    6. Restart Command Prompt
echo.
echo 🚀 Then use: flutterator --help
echo.
pause
INSTALLER

# -----------------------------------------------------------------------------
# Crea README per la distribuzione
# -----------------------------------------------------------------------------
cat > "${DIST_DIR}/README.md" << 'README'
# 🚀 Flutterator

CLI per creare e gestire progetti Flutter con architettura DDD (Domain-Driven Design)

## 📦 Installation

### Unix/Linux/Mac

```bash
# 1. Estrai l'archivio
unzip flutterator-v2.0.0.zip
cd flutterator-v2.0.0

# 2. Esegui l'installer
chmod +x install.sh
./install.sh

# 3. Ricarica il terminale
source ~/.zshrc  # o ~/.bashrc
```

### Windows

```cmd
# 1. Estrai l'archivio
# 2. Esegui install.bat
# 3. Aggiungi bin\ al PATH di sistema
```

## 🚀 Quick Start

```bash
# Crea nuovo progetto
flutterator create --name my_app

# Aggiungi domain entity e componente
cd my_app
flutterator add-domain --name todo --fields "title:string,done:bool"
flutterator add-component --name todo_list --type list

# Vedi tutti i comandi
flutterator --help
```

## 📋 Comandi Disponibili

| Comando | Descrizione |
|---------|-------------|
| `create` | Crea nuovo progetto Flutter DDD |
| `add-domain` | Aggiunge domain entity (model + infrastructure) |
| `add-component` | Aggiunge componente riutilizzabile (form, list, single) |
| `add-page` | Aggiunge pagina semplice |
| `add-component` | Aggiunge componente riutilizzabile |
| `add-drawer-item` | Aggiunge item al drawer |
| `add-bottom-nav-item` | Aggiunge tab alla bottom nav |
| `init` | Inizializza in progetto esistente |
| `list` | Elenca risorse del progetto |
| `config` | Gestisce configurazione |

## 📁 Struttura

```
flutterator-v2.0.0/
├── bin/
│   ├── flutterator        # Eseguibile Unix/Mac
│   └── flutterator.bat    # Eseguibile Windows
├── generators/            # Moduli di generazione
├── flutterator.py         # CLI principale
├── requirements.txt       # Dipendenze Python
├── install.sh             # Installer Unix/Mac
└── install.bat            # Installer Windows
```

## ⚙️ Requirements

- Python 3.8+
- Flutter SDK

---

Creato da **Lorenzo Busi** @ [GetAutomation](https://getautomation.it)
README

# -----------------------------------------------------------------------------
# Crea archivio ZIP
# -----------------------------------------------------------------------------
echo "📁 Creando archivi ZIP..."
cd dist/

# Crea ZIP con versione (es: flutterator-v2.0.0.zip)
zip -r "${DIST_NAME}.zip" "${DIST_NAME}/"

# Crea copia con nome fisso per link statici (flutterator.zip)
cp "${DIST_NAME}.zip" "flutterator.zip"

cd ..

# -----------------------------------------------------------------------------
# Output finale
# -----------------------------------------------------------------------------
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Distribuzione creata!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 File generati:"
echo "   dist/${DIST_NAME}.zip       # Con versione"
echo "   dist/flutterator.zip  # Per link statici"
echo ""
echo "📁 Struttura interna:"
echo "   ${DIST_NAME}/"
echo "   ├── bin/"
echo "   │   ├── flutterator        # Eseguibile Unix/Mac"
echo "   │   └── flutterator.bat    # Eseguibile Windows"
echo "   ├── generators/            # Moduli generazione"
echo "   ├── flutterator.py         # CLI principale"
echo "   ├── requirements.txt       # Dipendenze"
echo "   ├── install.sh             # Installer Unix/Mac"
echo "   ├── install.bat            # Installer Windows"
echo "   └── README.md"
echo ""
echo "🔗 Link statico:"
echo "   https://github.com/lorenzobusi9595/flutterator/releases/download/latest/flutterator.zip"
echo ""
