# 🚀 Flutterator

**Una CLI per generare e gestire progetti Flutter con architettura DDD (Domain-Driven Design)**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flutter](https://img.shields.io/badge/Flutter-Compatible-02569B.svg)](https://flutter.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📑 Indice

- [Cos'è Flutterator?](#-cosè-flutterator)
- [Installazione](#-installazione)
- [Quick Start](#-quick-start)
- [Comandi Disponibili](#-comandi-disponibili)
  - [`create`](#flutterator-create) - Crea nuovo progetto
  - [`add-feature`](#flutterator-add-feature) - Aggiunge feature DDD completa
  - [`add-page`](#flutterator-add-page) - Aggiunge pagina semplice
  - [`add-component`](#flutterator-add-component) - Aggiunge componente riutilizzabile
  - [`add-drawer-item`](#flutterator-add-drawer-item) - Aggiunge item al drawer
  - [`add-bottom-nav-item`](#flutterator-add-bottom-nav-item) - Aggiunge tab alla bottom nav
  - [`init`](#flutterator-init) - Inizializza in progetto esistente
  - [`list`](#flutterator-list) - Elenca risorse del progetto
  - [`config`](#flutterator-config) - Gestisce configurazione
- [Flag Globali](#-flag-globali)
- [Configurazione](#-configurazione)
- [Architettura Generata](#-architettura-generata)
- [Test](#-test)
- [Troubleshooting](#-troubleshooting)

---

## 📖 Cos'è Flutterator?

Flutterator è uno strumento da riga di comando che **automatizza la creazione di progetti Flutter** seguendo le best practice dell'architettura **Domain-Driven Design (DDD)**. 

Invece di creare manualmente decine di file per ogni nuova feature (entity, repository, bloc, page, dto...), Flutterator li genera automaticamente con una struttura coerente e professionale.

### 🎯 Problema che Risolve

Creare una nuova feature in un progetto Flutter DDD richiede:
- 📁 Creare 4+ cartelle (model, infrastructure, application, presentation)
- 📄 Creare 10+ file Dart (entity, failure, repository interface, dto, bloc, event, state, page...)
- ✏️ Scrivere codice boilerplate per ogni file
- 🔗 Aggiornare il router con le nuove route
- ⏱️ **Tempo stimato: 30-60 minuti per feature**

Con Flutterator:

```bash
flutterator add-feature --name todo --fields "title:string,done:bool"
```

**Tempo: 5 secondi** ⚡

### 💡 A Chi è Rivolto

- **Sviluppatori Flutter** che usano architettura DDD/Clean Architecture
- **Team** che vogliono standardizzare la struttura del codice
- **Freelancer** che vogliono velocizzare lo sviluppo di nuovi progetti
- **Studenti** che vogliono imparare l'architettura DDD con esempi pratici

---

## 📦 Installazione

### Requisiti

- **Python 3.8+**
- **Flutter SDK** (per i progetti generati)

### Installazione da Sorgente (Consigliata)

```bash
# 1. Clona il repository
git clone https://github.com/lorenzobusi/flutterator.git
cd flutterator

# 2. Crea virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure: venv\Scripts\activate  # Windows

# 3. Installa dipendenze
pip install -e .

# 4. Verifica installazione
flutterator --help
```

### Installazione via pip (quando pubblicato)

```bash
pip install flutterator
```

### Verifica Installazione

```bash
flutterator --help
```

Output atteso:

```
Usage: flutterator [OPTIONS] COMMAND [ARGS]...

  🚀 Flutterator - Flutter DDD Project Generator
  ...
```

---

## 🚀 Quick Start

### Scenario 1: Nuovo Progetto

```bash
# 1. Crea un nuovo progetto Flutter con struttura DDD
flutterator create --name my_app

# 2. Entra nel progetto
cd my_app

# 3. Aggiungi una feature completa
flutterator add-feature --name todo --fields "title:string,done:bool,priority:int"

# 4. Esegui il progetto
flutter run
```

### Scenario 2: Progetto Esistente

```bash
# 1. Vai nel tuo progetto Flutter esistente
cd my_existing_flutter_app

# 2. Inizializza Flutterator
flutterator init

# 3. Aggiungi feature
flutterator add-feature --name user --fields "name:string,email:string"
```

### Scenario 3: Preview Prima di Creare

```bash
# Usa --dry-run per vedere cosa verrà creato senza modificare nulla
flutterator add-feature --name product --fields "name:string,price:double" --dry-run
```

---

## 📋 Comandi Disponibili

| Comando               | Descrizione                                         | Uso Tipico         |
| --------------------- | --------------------------------------------------- | ------------------ |
| `create`              | Crea nuovo progetto Flutter DDD                     | Inizio progetto    |
| `add-feature`         | Aggiunge feature completa (model, bloc, repo, page) | Nuova funzionalità |
| `add-page`            | Aggiunge pagina semplice                            | Pagine statiche    |
| `add-component`       | Aggiunge componente riutilizzabile                  | Widget condivisi   |
| `add-drawer-item`     | Aggiunge item al drawer                             | Menu laterale      |
| `add-bottom-nav-item` | Aggiunge tab alla bottom nav                        | Tab navigation     |
| `init`                | Inizializza Flutterator in progetto esistente       | Adozione graduale  |
| `list`                | Elenca risorse del progetto                         | Panoramica         |
| `config`              | Gestisce configurazione                             | Personalizzazione  |

---

## 🔧 Dettaglio Comandi

### `flutterator create`

**Crea un nuovo progetto Flutter con architettura DDD completa.**

#### Sintassi

```bash
flutterator create [OPTIONS]
```

#### Opzioni

| Opzione   | Tipo   | Obbligatorio | Default | Descrizione                    |
| --------- | ------ | ------------ | ------- | ------------------------------ |
| `--name`  | string | ❌            | -       | Nome del progetto (snake_case) |
| `--login` | flag   | ❌            | `false` | Include autenticazione         |

#### Modalità di Utilizzo

**1. Riga di comando completa:**

```bash
flutterator create --name my_app --login
```

**2. Modalità interattiva** (se non specifichi --name):

```bash
flutterator create
```

```
Project name: my_app
Does the project have login? [y/N]: y
```

#### Esempi

```bash
# Progetto base
flutterator create --name my_app

# Progetto con autenticazione
flutterator create --name my_app --login

# Modalità interattiva (chiede nome e opzioni)
flutterator create
```

#### Struttura Generata

```
my_app/
├── lib/
│   ├── core/
│   │   ├── model/              # Value objects, failures, errors
│   │   │   ├── value_objects.dart
│   │   │   ├── value_failures.dart
│   │   │   └── value_validators.dart
│   │   ├── infrastructure/     # Firebase modules, helpers
│   │   │   ├── firebase_injectable_module.dart
│   │   │   └── utils.dart
│   │   └── presentation/       # Widget comuni
│   │       └── app_widget.dart
│   ├── home/
│   │   └── presentation/
│   │       └── home_screen.dart
│   ├── splash/
│   │   └── presentation/
│   │       └── splash_screen.dart
│   ├── main.dart              # Entry point
│   ├── injection.dart         # Dependency injection setup
│   └── router.dart            # Routing con auto_route
├── pubspec.yaml               # Dipendenze Flutter
├── analysis_options.yaml
└── ...
```

---

### `flutterator add-feature`

**Aggiunge una feature DDD completa con tutti i layer (model, infrastructure, application, presentation) oppure una domain entity condivisa (solo model e infrastructure).**

Questo è il comando più potente: genera entity, repository, BLoC, page e tutto il boilerplate necessario.

**Tipi:**
- **Feature** (default): Use case completo con UI e BLoC
- **Domain Entity** (`--domain`): Entità condivisa tra più feature (solo model + infrastructure)

#### Sintassi

```bash
flutterator add-feature [OPTIONS]
```

#### Opzioni

| Opzione          | Tipo   | Obbligatorio | Default       | Descrizione                                                         |
| ---------------- | ------ | ------------ | ------------- | ------------------------------------------------------------------- |
| `--name`         | string | ✅            | -             | Nome della feature/entity (es: todo, user, product)                 |
| `--fields`       | string | ❌            | `"id:string"` | Campi del modello: `nome:tipo,nome:tipo`                            |
| `--domain`       | flag   | ❌            | `false`       | Crea come domain entity (condivisa, senza application/presentation) |
| `--folder`       | string | ❌            | da config     | Cartella di destinazione (es: features)                             |
| `--dry-run`      | flag   | ❌            | `false`       | Preview senza creare file                                           |
| `--no-build`     | flag   | ❌            | `false`       | Salta `flutter pub get` e `build_runner`                            |
| `--project-path` | string | ❌            | `.`           | Path al progetto Flutter                                            |

#### Tipi di Campo Supportati

| Tipo       | Dart Type              | Esempio               |
| ---------- | ---------------------- | --------------------- |
| `string`   | `String`               | `name:string`         |
| `int`      | `int`                  | `age:int`             |
| `double`   | `double`               | `price:double`        |
| `bool`     | `bool`                 | `active:bool`         |
| `datetime` | `DateTime`             | `created_at:datetime` |
| `list`     | `List<dynamic>`        | `tags:list`           |
| `map`      | `Map<String, dynamic>` | `metadata:map`        |

#### Modalità di Utilizzo

**1. Riga di comando completa:**

```bash
flutterator add-feature --name todo --fields "title:string,done:bool,priority:int"
```

**2. Modalità interattiva** (se non specifichi --fields):

```bash
flutterator add-feature --name todo
```

```
🔧 Adding fields interactively. Type 'done' when finished.
Field name (or 'done'): title
Field type [String]: string
Field name (or 'done'): completed
Field type [String]: bool
Field name (or 'done'): done
```

#### Esempi

```bash
# Feature con campi inline (use case completo)
flutterator add-feature --name todo --fields "title:string,done:bool,priority:int"

# Domain entity condivisa (senza application/presentation)
flutterator add-feature --name note --domain --fields "title:string,content:string"

# Feature in cartella specifica
flutterator add-feature --name user --folder features --fields "name:string,email:string"

# Preview senza creare (dry-run)
flutterator add-feature --name product --fields "name:string,price:double" --dry-run

# Modalità interattiva per i campi
flutterator add-feature --name order

# Salta build_runner (più veloce)
flutterator add-feature --name category --fields "name:string" --no-build
```

#### Struttura Generata

```
lib/todo/                          # o lib/features/todo/ se --folder features
├── model/                         # 📋 DOMAIN LAYER
│   ├── todo.dart                  # Entity con Freezed
│   ├── todo_failure.dart          # Failure class per errori
│   ├── i_todo_repository.dart     # Interface del repository
│   ├── value_objects.dart         # Value objects per ogni campo
│   └── value_validators.dart      # Validatori custom
│
├── infrastructure/                # 🔌 DATA LAYER
│   ├── todo_dto.dart              # Data Transfer Object
│   ├── todo_extensions.dart       # Extension methods
│   └── todo_repository.dart       # Implementazione repository
│
├── application/                   # ⚙️ BUSINESS LOGIC LAYER
│   ├── todo_bloc.dart             # BLoC state management
│   ├── todo_event.dart            # Eventi del BLoC
│   └── todo_state.dart            # Stati del BLoC
│
└── presentation/                  # 🎨 PRESENTATION LAYER
    └── todo_page.dart             # Page widget
```

**Inoltre aggiorna:**
- `lib/router.dart` - Aggiunge la nuova route

---

### `flutterator add-page`

**Aggiunge una pagina semplice senza business logic.**

Ideale per pagine statiche come About, Settings, Privacy Policy, etc.

#### Sintassi

```bash
flutterator add-page [OPTIONS]
```

#### Opzioni

| Opzione          | Tipo   | Obbligatorio | Default   | Descrizione              |
| ---------------- | ------ | ------------ | --------- | ------------------------ |
| `--name`         | string | ✅            | -         | Nome della pagina        |
| `--folder`       | string | ❌            | da config | Cartella di destinazione |
| `--dry-run`      | flag   | ❌            | `false`   | Preview senza creare     |
| `--no-build`     | flag   | ❌            | `false`   | Salta flutter pub get    |
| `--project-path` | string | ❌            | `.`       | Path al progetto         |

#### Modalità di Utilizzo

**Riga di comando:**

```bash
flutterator add-page --name settings
```

**Modalità interattiva:**

```bash
flutterator add-page
```

```
Page name: settings
```

#### Esempi

```bash
# Pagina settings
flutterator add-page --name settings

# Pagina about con preview
flutterator add-page --name about --dry-run

# Pagina in cartella specifica
flutterator add-page --name privacy --folder pages
```

#### Struttura Generata

```
lib/settings/
└── presentation/
    └── settings_page.dart
```

**Inoltre aggiorna:**
- `lib/router.dart` - Aggiunge la nuova route

---

### `flutterator add-component`

**Aggiunge un componente riutilizzabile con BLoC opzionale.**

Supporta due tipi: componenti standard (con stato BLoC) e form components (con validazione).

#### Sintassi

```bash
flutterator add-component [OPTIONS]
```

#### Opzioni

| Opzione      | Tipo   | Obbligatorio | Default   | Descrizione                        |
| ------------ | ------ | ------------ | --------- | ---------------------------------- |
| `--name`     | string | ✅            | -         | Nome del componente                |
| `--form`     | flag   | ❌            | `false`   | Crea come form component           |
| `--fields`   | string | ❌            | -         | Campi del form (richiede `--form`) |
| `--folder`   | string | ❌            | da config | Cartella di destinazione           |
| `--dry-run`  | flag   | ❌            | `false`   | Preview senza creare               |
| `--no-build` | flag   | ❌            | `false`   | Salta flutter pub get              |

#### Due Tipi di Componente

**1. Standard Component** - Widget riutilizzabile con stato BLoC:

```bash
flutterator add-component --name user_card
```

**2. Form Component** - Form con validazione e gestione campi:

```bash
flutterator add-component --name login --form --fields "email:string,password:string"
```

#### Modalità di Utilizzo

**Riga di comando:**

```bash
flutterator add-component --name user_card
```

**Modalità interattiva:**

```bash
flutterator add-component
```

```
Component name: user_card
Folder (leave empty for root) []: components
Is this a form component? [y/N]: n
```

#### Esempi

```bash
# Componente standard
flutterator add-component --name user_card

# Form component con campi
flutterator add-component --name login --form --fields "email:string,password:string"

# Componente in cartella specifica
flutterator add-component --name search_bar --folder shared/widgets

# Form registrazione
flutterator add-component --name registration --form --fields "name:string,email:string,password:string,confirm:string"
```

#### Struttura Generata

**Standard Component:**

```
lib/user_card/
├── application/
│   ├── user_card_bloc.dart
│   ├── user_card_event.dart
│   └── user_card_state.dart
└── presentation/
    └── user_card_component.dart
```

**Form Component:**

```
lib/login/
├── application/
│   ├── login_form_bloc.dart
│   ├── login_form_event.dart
│   └── login_form_state.dart
└── presentation/
    └── login_component.dart
```

---

### `flutterator add-drawer-item`

**Aggiunge un item al drawer (menu laterale) della navigazione.**

Crea la pagina, il drawer (se non esiste) e configura tutto automaticamente.

#### Sintassi

```bash
flutterator add-drawer-item [OPTIONS]
```

#### Opzioni

| Opzione          | Tipo   | Obbligatorio | Default | Descrizione           |
| ---------------- | ------ | ------------ | ------- | --------------------- |
| `--name`         | string | ✅            | -       | Nome dell'item        |
| `--dry-run`      | flag   | ❌            | `false` | Preview senza creare  |
| `--no-build`     | flag   | ❌            | `false` | Salta flutter pub get |
| `--project-path` | string | ❌            | `.`     | Path al progetto      |

#### Modalità di Utilizzo

**Riga di comando:**

```bash
flutterator add-drawer-item --name settings
```

**Modalità interattiva:**

```bash
flutterator add-drawer-item
```

```
Drawer item name: settings
```

#### Esempi

```bash
# Aggiungi settings al drawer
flutterator add-drawer-item --name settings

# Aggiungi profile
flutterator add-drawer-item --name profile

# Preview
flutterator add-drawer-item --name help --dry-run
```

#### Cosa Viene Generato/Modificato

1. ✅ Crea `lib/<nome>/presentation/<nome>_page.dart`
2. ✅ Crea/Aggiorna `lib/core/presentation/app_drawer.dart`
3. ✅ Aggiorna `lib/home/presentation/home_screen.dart` (aggiunge drawer)
4. ✅ Aggiorna `lib/router.dart`

---

### `flutterator add-bottom-nav-item`

**Aggiunge un tab alla bottom navigation bar.**

Crea la schermata e configura la bottom navigation automaticamente.

#### Sintassi

```bash
flutterator add-bottom-nav-item [OPTIONS]
```

#### Opzioni

| Opzione          | Tipo   | Obbligatorio | Default | Descrizione           |
| ---------------- | ------ | ------------ | ------- | --------------------- |
| `--name`         | string | ✅            | -       | Nome del tab          |
| `--dry-run`      | flag   | ❌            | `false` | Preview senza creare  |
| `--no-build`     | flag   | ❌            | `false` | Salta flutter pub get |
| `--project-path` | string | ❌            | `.`     | Path al progetto      |

#### Modalità di Utilizzo

**Riga di comando:**

```bash
flutterator add-bottom-nav-item --name search
```

**Modalità interattiva:**

```bash
flutterator add-bottom-nav-item
```

```
Tab name: search
```

#### Esempi

```bash
# Aggiungi tab search
flutterator add-bottom-nav-item --name search

# Aggiungi tab favorites
flutterator add-bottom-nav-item --name favorites

# Aggiungi tab profile
flutterator add-bottom-nav-item --name profile
```

#### Cosa Viene Generato/Modificato

1. ✅ Crea `lib/home/presentation/<nome>_screen.dart`
2. ✅ Crea/Aggiorna `lib/core/presentation/bottom_nav_bar.dart`
3. ✅ Aggiorna `lib/home/presentation/home_screen.dart` (aggiunge BottomNavigationBar)

---

### `flutterator init`

**Inizializza Flutterator in un progetto Flutter esistente.**

Ideale per adottare Flutterator gradualmente in progetti già avviati.

#### Sintassi

```bash
flutterator init [OPTIONS]
```

#### Opzioni

| Opzione          | Tipo   | Obbligatorio | Default | Descrizione                  |
| ---------------- | ------ | ------------ | ------- | ---------------------------- |
| `--project-path` | string | ❌            | `.`     | Path al progetto Flutter     |
| `--force`        | flag   | ❌            | `false` | Sovrascrive config esistente |

#### Esempi

```bash
# Inizializza nel progetto corrente
flutterator init

# Inizializza in altro progetto
flutterator init --project-path ../my_flutter_app

# Forza sovrascrittura config esistente
flutterator init --force
```

#### Cosa Viene Generato

1. ✅ `flutterator.yaml` - File di configurazione
2. ✅ `lib/core/` - Cartella core (se mancante)
3. ✅ `lib/features/` - Cartella features (se mancante)
4. ✅ `lib/shared/` - Cartella shared (se mancante)

#### Output

```
╭───────────────────────────────────────────╮
│ 🔧 Initializing Flutterator in: my_app    │
╰───────────────────────────────────────────╯
→ Creating flutterator.yaml...

→ Created directories:
   ✅ lib/core/
   ✅ lib/features/
   ✅ lib/shared/

✅ Flutterator initialized!

Next steps:
   1. Edit flutterator.yaml to customize settings
   2. Run: flutterator add-feature --name <feature_name>
   3. Run: flutterator list to see project structure
```

---

### `flutterator list`

**Elenca le risorse presenti nel progetto Flutter.**

Utile per avere una panoramica di features, pagine, componenti e routes.

#### Sintassi

```bash
flutterator list [TIPO] [OPTIONS]
```

#### Argomenti

| Argomento | Valori                                             | Default | Descrizione                |
| --------- | -------------------------------------------------- | ------- | -------------------------- |
| `TIPO`    | `all`, `features`, `pages`, `components`, `routes` | `all`   | Tipo di risorse da listare |

#### Opzioni

| Opzione          | Tipo   | Obbligatorio | Default | Descrizione      |
| ---------------- | ------ | ------------ | ------- | ---------------- |
| `--project-path` | string | ❌            | `.`     | Path al progetto |

#### Esempi

```bash
# Lista tutto
flutterator list

# Solo features DDD
flutterator list features

# Solo pagine semplici
flutterator list pages

# Solo componenti
flutterator list components

# Solo routes
flutterator list routes
```

#### Output Esempio

```
╭──────────────────────╮
│ 📋 Project: my_app   │
╰──────────────────────╯

📦 Features:
todo/
├── model/
│   ├── todo
│   └── todo_failure
├── application/
│   └── todo_bloc
└── presentation/
    └── todo_page

user/
├── model/
│   ├── user
│   └── user_failure
...

📄 Pages:
   settings/ (1 file)
   about/ (1 file)

🧩 Components:
   user_card/ (standard)
   login/ (form)

🛤️  Routes:
   /home           → HomePage
   /todo           → TodoPage
   /settings       → SettingsPage
   /user           → UserPage
```

---

### `flutterator config`

**Gestisce la configurazione di Flutterator.**

Permette di visualizzare o creare il file di configurazione.

#### Sintassi

```bash
flutterator config [OPTIONS]
```

#### Opzioni

| Opzione          | Tipo   | Descrizione                   |
| ---------------- | ------ | ----------------------------- |
| `--show`         | flag   | Mostra configurazione attuale |
| `--init`         | flag   | Crea file di configurazione   |
| `--project-path` | string | Path al progetto              |

#### Esempi

```bash
# Mostra configurazione attuale
flutterator config --show

# Crea file di configurazione
flutterator config --init
```

#### Output --show

```
╭─────────────────────── ⚙️  Configuration ────────────────────────╮
│ ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓                         │
│ ┃ Setting             ┃ Value         ┃                         │
│ ┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩                         │
│ │ Feature Folder      │ features      │                         │
│ │ Component Folder    │ components    │                         │
│ │ Page Folder         │               │                         │
│ │ Use BLoC            │ ✅            │                         │
│ │ Use Freezed         │ ✅            │                         │
│ │ Auto Build Runner   │ ✅            │                         │
│ └─────────────────────┴───────────────┘                         │
╰─────────────────────────────────────────────────────────────────╯

📄 Project config: /path/to/project/flutterator.yaml
```

---

## 🏃 Flag Globali

Questi flag sono disponibili per tutti i comandi `add-*`:

| Flag             | Descrizione                              | Esempio                 |
| ---------------- | ---------------------------------------- | ----------------------- |
| `--dry-run`      | Preview senza creare file                | `--dry-run`             |
| `--no-build`     | Salta `flutter pub get` e `build_runner` | `--no-build`            |
| `--project-path` | Specifica il path al progetto            | `--project-path ../app` |

### Esempio --dry-run

```bash
$ flutterator add-feature --name todo --dry-run
```

Output:

```
╭──────────────────────────╮
│ 🔍 DRY-RUN MODE          │
│ No files will be created │
╰──────────────────────────╯

🔧 Would add feature: todo
   Fields: id:string

📁 lib/todo/
├── 📁 model/
│   ├── 📄 todo.dart
│   ├── 📄 todo_failure.dart
│   ├── 📄 i_todo_repository.dart
│   └── ...
├── 📁 infrastructure/
│   └── ...
├── 📁 application/
│   └── ...
└── 📁 presentation/
    └── 📄 todo_page.dart

📝 Would update: lib/router.dart

──────────────────────────────────────────────────
ℹ️  Run without --dry-run to create these files
```

### Esempio --no-build

```bash
# Più veloce: salta pub get e build_runner
flutterator add-feature --name todo --fields "title:string" --no-build

# Poi esegui manualmente quando vuoi
flutter pub get
dart run build_runner build --delete-conflicting-outputs
```

---

## ⚙️ Configurazione

### Priorità Configurazione

Flutterator carica la configurazione da più fonti (in ordine di priorità):

1. **🔴 Flag CLI** (massima priorità) - `--folder features`
2. **🟠 `flutterator.yaml`** nel progetto
3. **🟡 `~/.flutteratorrc`** globale (home directory)
4. **🟢 Defaults** (minima priorità)

### Creare Configurazione

```bash
# Crea flutterator.yaml nel progetto
flutterator init

# Oppure
flutterator config --init
```

### Esempio flutterator.yaml

```yaml
# 📁 Cartelle default per il codice generato
defaults:
  feature_folder: "features"     # lib/features/todo/
  domain_folder: "domain"         # lib/domain/note/ (entità condivise)
  component_folder: "components" # lib/components/user_card/
  page_folder: ""                # lib/profile/ (root di lib/)
  use_bloc: true                 # Usa BLoC pattern
  use_freezed: true              # Usa Freezed per immutabilità
  auto_run_build_runner: true    # Esegue build_runner dopo generazione

# 🎨 Configurazione UI (per riferimento futuro)
styling:
  ui_library: "material"         # material, cupertino
  primary_color: "#2196F3"
  secondary_color: "#FF9800"
```

### Esempio ~/.flutteratorrc (Globale)

```yaml
# Configurazione globale per tutti i progetti
defaults:
  feature_folder: "features"
  use_bloc: true
  auto_run_build_runner: false  # Disabilita per tutti i progetti
```

---

## 🏗️ Architettura Generata

Flutterator genera progetti seguendo l'architettura **DDD (Domain-Driven Design)** con separazione in layer:

```
lib/
├── core/                        # 🔧 CORE - Codice condiviso
│   ├── model/                   # Value objects, failures comuni
│   │   ├── value_objects.dart
│   │   ├── value_failures.dart
│   │   └── value_validators.dart
│   ├── infrastructure/          # Moduli DI, helpers
│   │   └── firebase_injectable_module.dart
│   └── presentation/            # Widget comuni
│       └── app_widget.dart
│
├── domain/                      # 🏛️ DOMAIN ENTITIES - Entità condivise
│   ├── auth/                    # Entità Auth (condivisa)
│   │   ├── model/               # Entity, failures, repository interface
│   │   │   ├── user.dart
│   │   │   ├── user_profile.dart
│   │   │   └── i_auth_facade.dart
│   │   └── infrastructure/      # Repository implementation, DTOs
│   │       ├── firebase_auth_facade.dart
│   │       └── user_profile_repository.dart
│   │
│   └── note/                    # Esempio: entità Note (condivisa)
│       ├── model/
│       │   ├── note.dart
│       │   └── i_note_repository.dart
│       └── infrastructure/
│           └── note_repository.dart
│
├── features/                    # 📦 FEATURES - Use cases specifici
│   ├── auth/                    # Feature Auth (use case completo)
│   │   ├── application/         # ⚙️ APPLICATION LAYER
│   │   │   ├── auth_bloc.dart
│   │   │   ├── auth_event.dart
│   │   │   └── auth_state.dart
│   │   └── presentation/        # 🎨 PRESENTATION LAYER
│   │       └── login_screen.dart
│   │
│   └── notes/                    # Esempio feature "gestione note"
│       │                          # (usa domain/note)
│       ├── application/         # ⚙️ APPLICATION LAYER
│       │   ├── notes_bloc.dart      # BLoC (logica)
│       │   ├── notes_event.dart     # Events
│       │   └── notes_state.dart     # States
│       │
│       └── presentation/        # 🎨 PRESENTATION LAYER
│           └── notes_page.dart      # UI
│
├── shared/                      # 🧩 SHARED - Componenti condivisi
│   └── widgets/
│
├── main.dart                    # Entry point
├── injection.dart               # 💉 Dependency Injection
└── router.dart                  # 🛤️ Routing (auto_route)
```

### Perché DDD?

| Beneficio          | Descrizione                                    |
| ------------------ | ---------------------------------------------- |
| **Testabilità**    | Ogni layer è isolato e testabile               |
| **Manutenibilità** | Codice organizzato e prevedibile               |
| **Scalabilità**    | Facile aggiungere nuove feature                |
| **Team**           | Più sviluppatori possono lavorare in parallelo |

---

## 📚 Dipendenze Flutter Generate

I progetti generati usano queste dipendenze Flutter standard:

| Pacchetto         | Scopo                  | Link                                                |
| ----------------- | ---------------------- | --------------------------------------------------- |
| `flutter_bloc`    | State management       | [pub.dev](https://pub.dev/packages/flutter_bloc)    |
| `freezed`         | Immutable classes      | [pub.dev](https://pub.dev/packages/freezed)         |
| `injectable`      | Dependency injection   | [pub.dev](https://pub.dev/packages/injectable)      |
| `auto_route`      | Routing declarativo    | [pub.dev](https://pub.dev/packages/auto_route)      |
| `dartz`           | Functional programming | [pub.dev](https://pub.dev/packages/dartz)           |
| `json_annotation` | JSON serialization     | [pub.dev](https://pub.dev/packages/json_annotation) |

---

## 🧪 Test

```bash
# Attiva virtual environment
source venv/bin/activate

# Esegui tutti i test
pytest tests/ -v

# Solo test veloci (senza E2E)
pytest tests/test_basic.py tests/test_integration.py -v

# Solo test E2E (richiede Flutter SDK installato)
pytest tests/test_e2e_flutter.py -v

# Con coverage
pytest tests/ --cov=. --cov-report=html
```

---

## 🔧 Troubleshooting

### "Command not found: flutterator"

```bash
# Assicurati di aver installato correttamente
pip install -e .

# Oppure usa python direttamente
python flutterator.py --help
```

### "Not a valid Flutter project"

```bash
# Flutterator richiede pubspec.yaml e lib/
# Assicurati di essere in un progetto Flutter valido
ls pubspec.yaml lib/
```

### "rich import error" nell'IDE

L'IDE potrebbe non riconoscere il virtual environment. Soluzione:
1. `Cmd+Shift+P` → "Python: Select Interpreter"
2. Seleziona `./venv/bin/python`

### build_runner lento

```bash
# Usa --no-build per saltare build_runner
flutterator add-feature --name todo --no-build

# Esegui build_runner una volta alla fine
dart run build_runner build --delete-conflicting-outputs
```

### Errori di compilazione Dart

Dopo aver generato codice, esegui:

```bash
flutter pub get
dart run build_runner build --delete-conflicting-outputs
```

---

## 🤝 Contribuire

1. Fork del repository
2. Crea branch: `git checkout -b feature/nuova-feature`
3. Commit: `git commit -m 'Aggiunge nuova feature'`
4. Push: `git push origin feature/nuova-feature`
5. Apri Pull Request

### Struttura del Progetto

```
flutterator/
├── flutterator.py              # CLI principale
├── generators/
│   ├── helpers/                # Funzioni helper
│   │   ├── config.py           # Gestione configurazione
│   │   └── project.py          # Validazione progetto
│   └── static/templates/       # Template Jinja2
├── tests/                      # Test suite
└── docs/                       # Documentazione
```

---

## 📄 Licenza

MIT License - vedi [LICENSE](LICENSE)

---

## 👨‍💻 Autore

**Lorenzo Busi** - [GetAutomation](https://getautomation.it)

---

## 🙏 Ringraziamenti

- [Click](https://click.palletsprojects.com/) - CLI framework
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [Flutter](https://flutter.dev/) - UI framework
- [Reso Coder](https://resocoder.com/) - Ispirazione architettura DDD

---

<p align="center">
  <i>Generato con ❤️ da Flutterator</i>
</p>
