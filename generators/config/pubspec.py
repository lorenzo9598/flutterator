import subprocess
import sys
from pathlib import Path

def update_pubspec(flutter_name, has_login):
    """Aggiunge dipendenze al pubspec.yaml usando flutter pub add"""
    project_path = Path(flutter_name)
    
    # Dipendenze principali sempre necessarie
    main_dependencies = [
        "dartz",
        "freezed_annotation", 
        "flutter_bloc",
        "injectable",
        "get_it",
        "bloc",
        "another_flushbar",
        "flutter_lints",
        "caravaggio_ui",
        "font_awesome_flutter",
        "uuid",
        "collection", 
        "rxdart",
        "flutter_svg",
        "shared_preferences",
        "dio",
        "retrofit",
        "go_router",
    ]
    
    # Dipendenze di sviluppo
    dev_dependencies = [
        "build_runner",
        "freezed",
        "injectable_generator", 
        "json_serializable",
        "retrofit_generator",
        "flutter_launcher_icons",
        "analyzer"
    ]
    
    print("📦 Aggiungendo dipendenze principali...")
    for dep in main_dependencies:
        add_dependency(project_path, dep)
    
    print("🔧 Aggiungendo dipendenze di sviluppo...")
    for dep in dev_dependencies:
        add_dependency(project_path, dep, dev=True)
    
    # Aggiorna configurazione flutter in pubspec.yaml
    update_flutter_config(project_path)

def add_dependency(project_path: Path, package: str, dev: bool = False):
    """Aggiunge una singola dipendenza usando flutter pub add"""
    try:
        cmd = ["flutter", "pub", "add"]
        cmd.append(package)
        
        if dev:
            cmd.append("--dev")
        
        result = subprocess.run(
            cmd, 
            cwd=project_path, 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"  ✅ {package}")
        
    except subprocess.CalledProcessError as e:
        print(f"  ⚠️ Errore aggiungendo {package}: {e.stderr}")
    except FileNotFoundError:
        print("❌ Flutter non trovato nel PATH")
        sys.exit(1)

def update_flutter_config(project_path: Path):
    """Aggiorna la configurazione flutter nel pubspec.yaml"""
    pubspec_path = project_path / "pubspec.yaml"
    
    if not pubspec_path.exists():
        return
    
    try:
        # Leggi il contenuto esistente
        content = pubspec_path.read_text()
        
        # Sostituisci solo gli assets commentati
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # Sostituisci le righe di assets commentate
            if stripped.startswith("# assets:") or (stripped.startswith("#") and "assets:" in stripped):
                # Trova l'indentazione corretta dalla riga
                indent = line[:len(line) - len(line.lstrip())]
                new_lines.extend([
                    f"{indent}assets:",
                    f"{indent}  - assets/",
                    f"{indent}  - assets/svgs/"
                ])
            elif stripped.startswith("uses-material-design:"):
                new_lines.append(line)
                # Aggiungi generate: true subito dopo uses-material-design
                indent = line[:len(line) - len(line.lstrip())]
                new_lines.append(f"{indent}generate: true")
            else:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        # Scrivi il contenuto aggiornato
        pubspec_path.write_text(content)
        print("✅ Configurazione Flutter aggiornata")
        
    except Exception as e:
        print(f"⚠️ Errore nell'aggiornamento della configurazione Flutter: {e}")
