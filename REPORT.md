# 📋 Flutterator - Report Stato Progetto

**Ultimo aggiornamento**: Dicembre 2025  
**Versione**: 0.2.0 (in sviluppo)  
**Autore**: Lorenzo Busi @ GetAutomation

---

## 🎯 Cos'è Flutterator

Flutterator è una **CLI Python** per generare e gestire progetti Flutter con architettura **DDD (Domain-Driven Design)**. Automatizza la creazione di:

- Struttura progetto completa
- Feature con tutti i layer (model, infrastructure, application, presentation)
- Domain entities condivise (solo model + infrastructure)
- Componenti riutilizzabili con BLoC
- Navigazione (drawer, bottom nav)
- Pagine semplici

---

## 📁 Struttura Progetto

```
flutterator/
├── flutterator.py          # 🔥 Entry point CLI principale (1165 righe)
├── pyproject.toml          # Configurazione pacchetto Python
├── requirements.txt        # Dipendenze
│
├── generators/             # 🏭 Generatori di codice
│   ├── __init__.py         # Export della funzione init()
│   ├── initializator.py    # Inizializzazione progetto Flutter
│   ├── main.py             # Orchestratore generatori
│   │
│   ├── helpers/            # 🛠️ Funzioni helper (NUOVO)
│   │   ├── __init__.py     # Export di tutte le funzioni
│   │   ├── config.py       # Gestione configurazione YAML
│   │   ├── project.py      # Validazione progetto Flutter
│   │   ├── utils.py        # Utility (to_pascal_case, map_field_type)
│   │   ├── feature.py      # Generazione feature DDD
│   │   ├── domain.py       # Generazione domain entities
│   │   ├── component.py    # Generazione componenti
│   │   ├── page.py         # Generazione pagine
│   │   └── navigation.py   # Drawer e bottom nav
│   │
│   ├── static/
│   │   ├── assets/         # Logo e icone
│   │   └── templates/      # 📝 Template Jinja2
│   │       ├── feature/    # Template per feature DDD
│   │       ├── component/  # Template per componenti
│   │       ├── core/       # Template core (app_widget, etc.)
│   │       ├── home/       # Template home screen
│   │       ├── auth/       # Template autenticazione (generati in domain/auth/)
│   │       └── ...
│   │
│   ├── templates/          # Generatori Python per template
│   │   ├── _core/          # core_generator.py
│   │   ├── lib/            # lib_generator.py
│   │   ├── home/           # home_generator.py
│   │   └── ...
│   │
│   ├── config/             # Generatori config Flutter
│   │   ├── pubspec.py
│   │   └── analisy_options.py
│   │
│   └── assets/             # Generatori assets
│
├── tests/                  # 🧪 Test suite
│   ├── conftest.py         # Fixture pytest
│   ├── test_basic.py       # Test unitari (7 test)
│   └── test_integration.py # Test integrazione (23 test)
│
├── ROADMAP.md              # Roadmap con priorità e versioni
├── REPORT.md               # Questo file
└── TEST_COVERAGE.md        # Analisi copertura test
```

---

## 🚀 Comandi CLI Disponibili

### Comandi Principali

| Comando                            | Descrizione                                                    |
| ---------------------------------- | -------------------------------------------------------------- |
| `flutterator create`               | Crea nuovo progetto Flutter con struttura DDD                  |
| `flutterator add-feature`          | Aggiunge feature completa (model, bloc, repo, page)            |
| `flutterator add-feature --domain` | Aggiunge domain entity condivisa (solo model + infrastructure) |
| `flutterator add-page`             | Aggiunge pagina semplice                                       |
| `flutterator add-component`        | Aggiunge componente riutilizzabile                             |
| `flutterator add-drawer-item`      | Aggiunge item al drawer navigation                             |
| `flutterator add-bottom-nav-item`  | Aggiunge tab alla bottom navigation                            |

### Comandi Utility

| Comando                     | Descrizione                                         |
| --------------------------- | --------------------------------------------------- |
| `flutterator init`          | Inizializza Flutterator in progetto esistente       |
| `flutterator list [type]`   | Lista risorse (features, pages, components, routes) |
| `flutterator config --show` | Mostra configurazione attuale                       |
| `flutterator config --init` | Crea flutterator.yaml                               |

### Flag Globali

| Flag             | Descrizione                          |
| ---------------- | ------------------------------------ |
| `--dry-run`      | Preview senza creare file            |
| `--no-build`     | Salta flutter pub get e build_runner |
| `--project-path` | Path al progetto Flutter             |
| `--help`         | Mostra aiuto con esempi              |

---

## ⚙️ Sistema di Configurazione

### Priorità (dalla più alta alla più bassa)

1. **Flag CLI** (`--folder features`)
2. **flutterator.yaml** (nel progetto)
3. **~/.flutteratorrc** (globale)
4. **Defaults hardcoded**

### Esempio flutterator.yaml

```yaml
defaults:
  feature_folder: "features"     # lib/features/todo/
  component_folder: "components" # lib/components/user_card/
  page_folder: ""                # lib/profile/ (root)
  use_bloc: true
  use_freezed: true
  auto_run_build_runner: true    # false = salta flutter pub get

styling:
  ui_library: caravaggio_ui      # material, cupertino
  primary_color: "#2196F3"
  secondary_color: "#FF9800"
```

### File di Config

- **Progetto**: `flutterator.yaml` nella root del progetto Flutter
- **Globale**: `~/.flutteratorrc` nella home directory

---

## 📦 Dipendenze Python

```toml
# pyproject.toml
dependencies = [
    "click>=8.0.0",      # CLI framework
    "jinja2>=3.0.0",     # Template engine
    "rich>=13.0.0",      # Output colorato
    "pyyaml>=6.0.0",     # Config YAML
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]
```

---

## 🧪 Test

### Eseguire i Test

```bash
# Attiva venv
source venv/bin/activate

# Tutti i test
pytest tests/ -v

# Con copertura
pytest tests/ --cov=. --cov-report=html
```

### Stato Test Attuale

- **Test totali**: 30
- **Passati**: 30 (100%)
- **Categorie**: Import, Utility, Page, Feature, Drawer, BottomNav, Component, CLI, DryRun, ErrorHandling

---

## ✅ Feature Implementate (v0.2.0)

| Feature                         | Stato | File Principale                    |
| ------------------------------- | ----- | ---------------------------------- |
| Creazione progetto              | ✅     | `generators/initializator.py`      |
| Add feature DDD                 | ✅     | `generators/helpers/feature.py`    |
| Add page semplice               | ✅     | `generators/helpers/page.py`       |
| Add component                   | ✅     | `generators/helpers/component.py`  |
| Add drawer item                 | ✅     | `generators/helpers/navigation.py` |
| Add bottom nav item             | ✅     | `generators/helpers/navigation.py` |
| Flag --dry-run                  | ✅     | `flutterator.py`                   |
| Flag --no-build                 | ✅     | `flutterator.py`                   |
| Output colorato (rich)          | ✅     | `flutterator.py`                   |
| Help con esempi                 | ✅     | `flutterator.py`                   |
| Config flutterator.yaml         | ✅     | `generators/helpers/config.py`     |
| Config globale ~/.flutteratorrc | ✅     | `generators/helpers/config.py`     |
| Comando init                    | ✅     | `flutterator.py`                   |
| Comando list                    | ✅     | `flutterator.py`                   |
| Comando config                  | ✅     | `flutterator.py`                   |

---

## ❌ Feature da Implementare

| Feature             | Priorità | Descrizione                    |
| ------------------- | -------- | ------------------------------ |
| Schema YAML         | 🟢 Bassa  | Definire feature via file YAML |
| Preset architetture | 🟢 Bassa  | --preset clean/mvvm/minimal    |
| Snippets IDE        | 🟢 Bassa  | VS Code / Android Studio       |
| Comando remove      | 🔵 Futura | Rimuovere feature/component    |
| Comando rename      | 🔵 Futura | Rinominare risorse             |

---

## 🗂️ File Chiave da Conoscere

### Entry Point
- **`flutterator.py`** - CLI principale, tutti i comandi Click

### Helpers (funzioni estratte)
- **`generators/helpers/config.py`** - FlutteratorConfig, load_config(), create_default_config()
- **`generators/helpers/project.py`** - validate_flutter_project(), get_project_name()
- **`generators/helpers/feature.py`** - create_feature_layers()
- **`generators/helpers/component.py`** - create_component_layers(), create_component_form_layers()
- **`generators/helpers/navigation.py`** - create_drawer_widget(), create_bottom_nav_widget()
- **`generators/helpers/page.py`** - generate_page_file(), update_router()
- **`generators/helpers/utils.py`** - to_pascal_case(), map_field_type()

### Template Jinja2
- **`generators/static/templates/feature/`** - Template per feature DDD
- **`generators/static/templates/component/`** - Template per componenti
- **`generators/static/templates/core/`** - Template core Flutter

### Test
- **`tests/test_basic.py`** - Test unitari helper functions
- **`tests/test_integration.py`** - Test integrazione comandi CLI

---

## 🔧 Come Riprendere lo Sviluppo

### 1. Setup Ambiente

```bash
cd /Users/lorenzobusi/development/flutterator
source venv/bin/activate
pip install -e ".[dev]"
```

### 2. Verifica Test

```bash
pytest tests/ -v
```

### 3. Prossimi Passi (da ROADMAP.md)

Le **priorità alte e medie sono completate**. Prossime feature da implementare:

1. **Schema YAML** - Permettere di definire feature tramite file YAML
2. **Preset architetture** - Supportare strutture diverse (clean, mvvm, minimal)
3. **Snippets IDE** - Generare snippet per VS Code

### 4. Come Aggiungere un Nuovo Comando

```python
# In flutterator.py

@cli.command()
@click.option('--name', help='...')
@click.option('--project-path', default='.', help='Path to Flutter project')
@click.option('--dry-run', is_flag=True, help='Preview without creating')
def nuovo_comando(name, project_path, dry_run):
    """
    Descrizione del comando.
    
    \b
    Examples:
      flutterator nuovo-comando --name test
    """
    project_dir = Path(project_path)
    lib_path, project_name = validate_flutter_project(project_dir)
    cfg = load_config(project_dir)
    
    if dry_run:
        print_dry_run_header()
        # ... preview
        print_dry_run_footer()
        return
    
    # ... implementazione
    print_success("Done!")
```

### 5. Come Aggiungere un Nuovo Template

1. Crea file `.jinja` in `generators/static/templates/`
2. Usa variabili Jinja: `{{ variable_name }}`
3. Carica con:
   ```python
   from jinja2 import Environment, FileSystemLoader
   env = Environment(loader=FileSystemLoader(templates_path))
   template = env.get_template("my_template.jinja")
   content = template.render(var1=value1, var2=value2)
   ```

---

## 📊 Metriche Progetto

| Metrica                          | Valore |
| -------------------------------- | ------ |
| Righe di codice (flutterator.py) | ~1165  |
| Numero comandi CLI               | 9      |
| Template Jinja2                  | 50+    |
| Test totali                      | 30     |
| Test passati                     | 100%   |
| Dipendenze Python                | 4      |

---

## 🔗 Link Utili

- **ROADMAP.md** - Priorità e versioni future
- **TEST_COVERAGE.md** - Analisi copertura test
- **README.md** - Documentazione utente

---

## 📝 Note per lo Sviluppatore

1. **Naming convention**: Funzioni Python snake_case, classi Dart PascalCase
2. **Output**: Usa sempre funzioni `print_success()`, `print_error()`, `print_info()` da rich
3. **Config**: Carica sempre con `cfg = load_config(project_dir)` per rispettare priorità
4. **Dry-run**: Ogni comando che crea file deve supportare `--dry-run`
5. **Test**: Aggiungi test per ogni nuova funzionalità in `tests/test_integration.py`

---

*Report generato: Dicembre 2025*
