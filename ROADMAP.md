# 🗺️ Flutterator Roadmap

Proposte di miglioramento per rendere Flutterator più utile, intuitivo e pratico.

---

## 📊 Analisi Critica Attuale

### ✅ Punti di Forza

| Aspetto | Descrizione |
|---------|-------------|
| Architettura DDD | Struttura professionale con layer ben separati |
| CLI con Click | Framework robusto e ben documentato |
| Template Jinja | Separazione codice/template |
| Comandi specifici | Un comando per ogni caso d'uso |

### ⚠️ Aree di Miglioramento

| Problema | Impatto |
|----------|---------|
| Troppi prompt interattivi | Rallenta il workflow |
| Nessuna configurazione per progetto | Ogni progetto ha le stesse impostazioni |
| Template hardcoded (CaravaggioUI, bloc) | Difficile adattare ad altri stack |
| Manca dry-run mode | Non si può prevedere cosa farà |
| Manca comando per progetti esistenti | Solo `create` per nuovi progetti |
| Manca comando `list`/`remove` | Non si può ispezionare o rimuovere |
| Output poco informativo | Difficile capire cosa sta succedendo |

---

## 💡 Proposte di Implementazione

### 1. Configurazione per Progetto

Creare supporto per file `flutterator.yaml`:

```yaml
# flutterator.yaml - Configurazione per progetto

# Defaults per i comandi
defaults:
  feature_folder: "features"      # Cartella default per le feature
  component_folder: "components"  # Cartella default per i componenti
  use_bloc: true                  # Usa BLoC pattern
  use_freezed: true               # Usa Freezed per le classi
  auto_run_build_runner: true     # Esegui build_runner automaticamente

# Override template
templates:
  entity: "custom_templates/entity.jinja"
  bloc: "custom_templates/bloc.jinja"

# Configurazione UI
styling:
  primary_color: "#2196F3"
  secondary_color: "#FF9800"
  ui_library: "caravaggio_ui"  # Opzioni: caravaggio_ui, material, cupertino

# Dipendenze aggiuntive da includere
dependencies:
  - package: dartz
    version: ^0.10.1
  - package: freezed_annotation
    version: ^2.4.1
```

**Priorità config** (dalla più alta alla più bassa):
1. Flag CLI (`--folder features`)
2. `flutterator.yaml` nel progetto
3. `~/.flutteratorrc` globale
4. Defaults hardcoded

---

### 2. Nuovi Flag Globali

```bash
# Dry-run: mostra cosa farà senza eseguire
flutterator add-feature todo --dry-run

# Verbose: mostra dettagli durante esecuzione
flutterator add-feature todo --verbose

# Quiet: solo errori
flutterator add-feature todo --quiet

# No build_runner: salta l'esecuzione automatica
flutterator add-feature todo --no-build

# Force: sovrascrive file esistenti senza chiedere
flutterator add-feature todo --force
```

---

### 3. Nuovi Comandi

#### `flutterator init`
Inizializza Flutterator in un progetto Flutter esistente.

```bash
$ flutterator init

🔍 Detected Flutter project: my_app
📁 Creating flutterator.yaml...
📁 Creating folder structure...
   ├── lib/core/
   ├── lib/features/
   └── lib/shared/

✅ Flutterator initialized!

Next steps:
  1. Edit flutterator.yaml to customize settings
  2. Run: flutterator add-feature <name>
```

#### `flutterator list`
Lista risorse nel progetto.

```bash
$ flutterator list features
📋 Features in my_app:

  todo/
    ├── model: Todo, TodoFailure
    ├── infrastructure: TodoRepository, TodoDto
    ├── application: TodoBloc
    └── presentation: TodoPage

  auth/
    ├── model: User, AuthFailure
    └── ...

$ flutterator list routes
📋 Routes in my_app:

  /home          → HomeScreen
  /login         → LoginScreen
  /todo          → TodoPage
  /settings      → SettingsPage

$ flutterator list components
📋 Components in my_app:

  user_card/     (standard)
  login_form/    (form)
```

#### `flutterator remove`
Rimuove risorse con conferma.

```bash
$ flutterator remove feature todo

⚠️  This will remove:
   - lib/features/todo/ (8 files)
   - Route: /todo in router.dart
   - Import in injection.dart

Continue? [y/N]: y

🗑️  Removing feature 'todo'...
   ├── ✅ Removed lib/features/todo/
   ├── ✅ Updated router.dart
   └── ✅ Updated injection.dart

✅ Feature 'todo' removed successfully!
```

#### `flutterator tree`
Mostra struttura del progetto.

```bash
$ flutterator tree

📁 my_app/
├── 📁 lib/
│   ├── 📁 core/
│   │   ├── 📁 infrastructure/
│   │   ├── 📁 model/
│   │   └── 📁 presentation/
│   ├── 📁 features/
│   │   ├── 📁 todo/
│   │   └── 📁 auth/
│   ├── 📁 home/
│   ├── 📁 splash/
│   ├── 📄 main.dart
│   ├── 📄 router.dart
│   └── 📄 injection.dart
└── 📄 flutterator.yaml
```

#### `flutterator doctor`
Verifica stato del progetto.

```bash
$ flutterator doctor

🔍 Checking my_app...

✅ Flutter SDK: 3.16.0
✅ Dart SDK: 3.2.0
✅ pubspec.yaml: valid
✅ flutterator.yaml: valid
⚠️  router.dart: 2 orphan routes found
⚠️  injection.dart: TodoBloc not registered
❌ build_runner: not in dev_dependencies

Issues found: 3

Run `flutterator fix` to auto-fix some issues.
```

---

### 4. Schema-Driven Generation

Invece di prompt interattivi, permettere generazione da file YAML:

```yaml
# schemas/todo.yaml
name: todo
folder: features
description: "Todo management feature"

fields:
  - name: id
    type: string
    required: true
    
  - name: title
    type: string
    required: true
    validators:
      - notEmpty
      - maxLength: 100
      
  - name: description
    type: string
    nullable: true
    
  - name: completed
    type: bool
    default: false
    
  - name: dueDate
    type: datetime
    nullable: true
    
  - name: priority
    type: enum
    values: [low, medium, high]
    default: medium

# Opzionale: relazioni
relations:
  - name: category
    type: belongsTo
    target: Category
    
  - name: tags
    type: hasMany
    target: Tag
```

```bash
$ flutterator add-feature --from schemas/todo.yaml

📦 Creating feature from schema: todo.yaml

   Fields detected:
   - id: String (required)
   - title: String (required, validated)
   - description: String? (nullable)
   - completed: bool (default: false)
   - dueDate: DateTime? (nullable)
   - priority: Priority (enum)

   Relations detected:
   - category → Category (belongsTo)
   - tags → List<Tag> (hasMany)

Continue? [Y/n]: y
```

---

### 5. Preset Architetturali

```bash
# Clean Architecture (default attuale)
flutterator create myapp --preset clean

# MVVM semplificato
flutterator create myapp --preset mvvm

# Minimal (senza DDD, per progetti piccoli)
flutterator create myapp --preset minimal

# Custom preset da file
flutterator create myapp --preset ./my_preset.yaml
```

**Esempio preset minimal:**
```yaml
# presets/minimal.yaml
name: minimal
description: "Minimal structure for small projects"

structure:
  - screens/
  - widgets/
  - services/
  - models/

dependencies:
  - provider
  - http

skip:
  - bloc
  - injectable
  - freezed
```

---

### 6. Output Migliorato

Usare la libreria `rich` per output colorato e formattato:

```bash
$ flutterator add-feature todo --fields "title:string,done:bool"

╭─────────────────────────────────────────────────────────────╮
│  📦 Creating feature: todo                                   │
╰─────────────────────────────────────────────────────────────╯

   📁 lib/features/todo/
   │
   ├── 📁 model/
   │   ├── ✅ todo.dart
   │   ├── ✅ todo_failure.dart
   │   ├── ✅ value_objects.dart
   │   ├── ✅ value_validators.dart
   │   └── ✅ i_todo_repository.dart
   │
   ├── 📁 infrastructure/
   │   ├── ✅ todo_dto.dart
   │   ├── ✅ todo_extensions.dart
   │   └── ✅ todo_repository.dart
   │
   ├── 📁 application/
   │   ├── ✅ todo_bloc.dart
   │   ├── ✅ todo_event.dart
   │   └── ✅ todo_state.dart
   │
   └── 📁 presentation/
       └── ✅ todo_page.dart

   📄 Updated: router.dart (+1 route)

╭─────────────────────────────────────────────────────────────╮
│  🔧 Post-generation tasks                                    │
╰─────────────────────────────────────────────────────────────╯

   ⏳ Running flutter pub get...     ✅ Done (2.3s)
   ⏳ Running build_runner build...  ✅ Done (5.1s)

╭─────────────────────────────────────────────────────────────╮
│  ✅ Feature 'todo' created successfully!                     │
╰─────────────────────────────────────────────────────────────╯

   Next steps:
   │
   ├── 1. Register TodoBloc in injection.dart
   │      BlocProvider<TodoBloc>(create: (_) => getIt<TodoBloc>())
   │
   ├── 2. Add navigation to TodoPage
   │      context.go(TodoPage.routeName)
   │
   └── 3. Run tests
          flutter test
```

---

### 7. Integrazione IDE

```bash
# Genera snippet per VS Code
flutterator generate-snippets --vscode
# → Creates .vscode/flutterator.code-snippets

# Genera live templates per Android Studio
flutterator generate-snippets --android-studio
# → Creates .idea/templates/Flutterator.xml

# Genera estensione VS Code (futuro)
flutterator generate-extension --vscode
```

**Esempio snippet generato:**
```json
{
  "Flutterator Feature": {
    "prefix": "ffeature",
    "body": [
      "// Feature: ${1:name}",
      "// Run: flutterator add-feature ${1:name} --fields \"${2:field}:${3:type}\""
    ]
  }
}
```

---

### 8. Watch Mode (Avanzato)

```bash
$ flutterator watch

👀 Watching for changes...

   Triggers:
   - New file in schemas/ → auto-generate feature
   - Change in *.jinja → rebuild affected files
   - Delete feature folder → update router

[12:34:56] 📝 schemas/user.yaml modified
[12:34:57] 🔄 Regenerating user feature...
[12:35:02] ✅ Done
```

---

## 🚀 Roadmap Versioni

### v0.2.0 - Usabilità Base ✅ COMPLETATA
**Focus**: Migliorare l'esperienza utente quotidiana

- [x] Configurazione `flutterator.yaml`
- [x] Flag `--dry-run` per preview
- [x] Flag `--no-build` per saltare build_runner
- [x] Output colorato con `rich`
- [x] Help migliorato con esempi
- [x] Comando `config --show/--init`
- [x] Comando `list` (features, pages, routes, components)
- [x] Comando `init` per progetti esistenti
- [x] Config globale `~/.flutteratorrc`

**Dipendenze aggiunte:**
```toml
dependencies = [
    "click>=8.0.0",
    "jinja2>=3.0.0",
    "rich>=13.0.0",      # Output colorato
    "pyyaml>=6.0.0",     # Config YAML
]
```

### v0.3.0 - Flessibilità 🔜 PROSSIMA
**Focus**: Adattarsi a diversi progetti e stili

- [ ] Schema YAML per definizione feature
- [ ] Preset architetturali (clean, mvvm, minimal)
- [ ] Override template custom
- [ ] Supporto per UI library diverse (material, cupertino)
- [ ] Generazione snippets IDE

### v0.4.0 - Produttività
**Focus**: Velocizzare il workflow

- [ ] Comando `remove` con cleanup automatico
- [ ] Comando `tree` per visualizzare struttura
- [ ] Comando `rename` per rinominare feature/component
- [ ] Watch mode per rigenerazione automatica

### v0.5.0 - Qualità
**Focus**: Robustezza e manutenibilità

- [ ] Comando `doctor` per diagnostica
- [ ] Comando `fix` per auto-fix problemi comuni
- [ ] Validazione schema feature
- [ ] Test coverage > 80%
- [ ] Documentazione completa

### v1.0.0 - Release Stabile
**Focus**: Pronto per produzione

- [ ] Pubblicazione su PyPI
- [ ] GitHub Actions per CI/CD
- [ ] Changelog automatico
- [ ] Estensione VS Code (opzionale)
- [ ] Website documentazione

---

## 🎯 Quick Wins (Implementabili Subito)

### 1. Flag `--dry-run` (1-2 ore)

```python
@cli.command()
@click.option('--dry-run', is_flag=True, help='Show what would be created without creating')
def add_feature(name, dry_run, ...):
    if dry_run:
        click.echo("Would create:")
        click.echo(f"  - lib/{folder}/{name}/model/")
        click.echo(f"  - lib/{folder}/{name}/infrastructure/")
        # ... etc
        return
    # Esecuzione normale
```

### 2. Output colorato con `rich` (2-3 ore)

```python
from rich.console import Console
from rich.tree import Tree

console = Console()

def show_created_structure(feature_name, folder):
    tree = Tree(f"📁 lib/{folder}/{feature_name}/")
    model = tree.add("📁 model/")
    model.add("✅ [green]entity.dart[/green]")
    # ...
    console.print(tree)
```

### 3. Help migliorato (1 ora)

```python
@cli.command()
@click.option('--name', help='Feature name (e.g., todo, user_profile)')
@click.option('--fields', help='Fields in format: name:type,name:type\n\nExample: --fields "title:string,done:bool,count:int"')
def add_feature(...):
    """
    Add a complete DDD feature to your Flutter project.
    
    Examples:
    
        flutterator add-feature --name todo --fields "title:string,done:bool"
        
        flutterator add-feature --name user --folder features --fields "name:string,email:string,age:int"
    """
```

---

## 📋 Priorità Implementazione

### ✅ Completate

| Priorità | Feature | Stato | Note |
|----------|---------|-------|------|
| 🔴 Alta | `--dry-run` flag | ✅ Fatto | Preview modifiche senza creare file |
| 🔴 Alta | Output con `rich` | ✅ Fatto | Panel, Tree, colori, tabelle |
| 🔴 Alta | Help con esempi | ✅ Fatto | Docstring migliorate con esempi pratici |
| 🟡 Media | `flutterator.yaml` | ✅ Fatto | Config per progetto + ~/.flutteratorrc globale |
| 🟡 Media | Comando `list` | ✅ Fatto | Lista features, pages, components, routes |
| 🟡 Media | Comando `init` | ✅ Fatto | Inizializza Flutterator in progetto esistente |

### ❌ Da Fare

| Priorità | Feature | Effort | Impatto | Descrizione |
|----------|---------|--------|---------|-------------|
| 🟢 Bassa | Schema YAML | Alto | Medio | Definire feature via file YAML con campi, relazioni, validazioni |
| 🟢 Bassa | Preset architetture | Alto | Medio | `--preset clean/mvvm/minimal` per strutture diverse |
| 🟢 Bassa | Snippets IDE | Basso | Basso | Generazione snippet per VS Code/Android Studio |

---

## 📈 Changelog Implementazioni

### Dicembre 2025

**v0.2.0 - Usabilità Base** ✅
- [x] Flag `--dry-run` su tutti i comandi add-*
- [x] Flag `--no-build` per saltare flutter pub get
- [x] Output colorato con libreria `rich`
- [x] Help migliorato con esempi pratici
- [x] Configurazione `flutterator.yaml` per progetto
- [x] Configurazione globale `~/.flutteratorrc`
- [x] Comando `config --show` e `config --init`
- [x] Comando `list` (features, pages, components, routes)
- [x] Comando `init` per progetti esistenti

**Prossimo: v0.3.0 - Flessibilità**
- [ ] Schema YAML per feature definition
- [ ] Preset architetturali
- [ ] Snippets IDE

---

*Roadmap creata: Dicembre 2025*
*Ultimo aggiornamento: Dicembre 2025*

