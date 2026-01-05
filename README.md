# 🚀 Flutterator

**A CLI to generate and manage Flutter projects with DDD (Domain-Driven Design) architecture**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flutter](https://img.shields.io/badge/Flutter-Compatible-02569B.svg)](https://flutter.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📑 Table of Contents

- [What is Flutterator?](#-what-is-flutterator)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Available Commands](#-available-commands)
  - [`create`](#flutterator-create) - Create new project
  - [`add-domain`](#flutterator-add-domain) - Add domain entity (model + infrastructure)
  - [`add-page`](#flutterator-add-page) - Add simple page
  - [`add-component`](#flutterator-add-component) - Add reusable component (form, list, single)
  - [`list`](#flutterator-list) - List project resources
  - [`config`](#flutterator-config) - Manage configuration
- [Global Flags](#-global-flags)
- [Configuration](#-configuration)
- [Generated Architecture](#-generated-architecture)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)

---

## 📖 What is Flutterator?

Flutterator is a command-line tool that **automates Flutter project creation** following **Domain-Driven Design (DDD)** architecture best practices.

Instead of manually creating dozens of files for each new feature (entity, repository, bloc, page, dto...), Flutterator generates them automatically with a consistent and professional structure.

### 🎯 Problem It Solves

Creating a new feature in a Flutter DDD project requires:
- 📁 Creating 4+ folders (model, infrastructure, application, presentation)
- 📄 Creating 10+ Dart files (entity, failure, repository interface, dto, bloc, event, state, page...)
- ✏️ Writing boilerplate code for each file
- 🔗 Updating the router with new routes
- ⏱️ **Estimated time: 30-60 minutes per feature**

With Flutterator:

```bash
flutterator add-domain --name todo --fields "title:string,done:bool"
flutterator add-component --name todo_list --type list
```

**Time: 5 seconds** ⚡

### 💡 Who It's For

- **Flutter developers** using DDD/Clean Architecture
- **Teams** wanting to standardize code structure
- **Freelancers** wanting to speed up new project development
- **Students** wanting to learn DDD architecture with practical examples

---

## 📦 Installation

### Requirements

- **Python 3.8+**
- **Flutter SDK** (for generated projects)

### Installation from Source (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/lorenzobusi/flutterator.git
cd flutterator

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -e .

# 4. Verify installation
flutterator --help
```

### Installation via pip (when published)

```bash
pip install flutterator
```

### Verify Installation

```bash
flutterator --help
```

Expected output:

```
Usage: flutterator [OPTIONS] COMMAND [ARGS]...

  🚀 Flutterator - Flutter DDD Project Generator
  ...
```

---

## 🚀 Quick Start

### Scenario 1: New Project

```bash
# 1. Create a new Flutter project with DDD structure
flutterator create --name my_app

# 2. Enter the project
cd my_app

# 3. Add a complete feature
flutterator add-domain --name todo --fields "title:string,done:bool,priority:int"
flutterator add-component --name todo_list --type list

# 5. Run the project
flutter run
```

### Scenario 2: Existing Project

```bash
# 1. Go to your existing Flutter project
cd my_existing_flutter_app

# 2. Add features
flutterator add-domain --name user --fields "name:string,email:string"
flutterator add-component --name user_list --type list
```

### Scenario 3: Preview Before Creating

```bash
# Use --dry-run to see what will be created without modifying anything
flutterator add-domain --name product --fields "name:string,price:double" --dry-run
```

---

## 📋 Available Commands

| Command         | Description                               | Typical Use       |
| --------------- | ----------------------------------------- | ----------------- |
| `create`        | Create new Flutter DDD project            | Project start     |
| `add-domain`    | Add domain entity (model, infrastructure) | New functionality |
| `add-component` | Add component (form, list, single)        | New functionality |
| `add-page`      | Add simple page                           | Static pages      |
| `list`          | List project resources                    | Overview          |
| `config`        | Manage configuration                      | Customization     |

---

## 🔧 Command Details

### `flutterator create`

**Creates a new Flutter project with complete DDD architecture.**

#### Syntax

```bash
flutterator create [OPTIONS]
```

#### Options

| Option    | Type   | Required | Default | Description               |
| --------- | ------ | -------- | ------- | ------------------------- |
| `--name`  | string | ❌        | -       | Project name (snake_case) |
| `--login` | flag   | ❌        | `false` | Include authentication    |

#### Usage Modes

**1. Complete command line:**

```bash
flutterator create --name my_app --login
```

**2. Interactive mode** (if you don't specify --name):

```bash
flutterator create
```

```
Project name: my_app
Does the project have login? [y/N]: y
```

#### Examples

```bash
# Basic project
flutterator create --name my_app

# Project with authentication
flutterator create --name my_app --login

# Interactive mode (asks for name and options)
flutterator create
```

#### Generated Structure

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
│   │   └── presentation/       # Common widgets
│   │       └── app_widget.dart
│   ├── domain/                 # Domain entities (shared business entities)
│   ├── features/               # Features (use cases)
│   │   ├── home/
│   │   │   └── presentation/
│   │   │       └── home_page.dart
│   │   └── splash/
│   │       └── presentation/
│   │           └── splash_page.dart
│   ├── main.dart              # Entry point
│   ├── injection.dart         # Dependency injection setup
│   └── router.dart            # Routing with auto_route
├── pubspec.yaml               # Flutter dependencies
├── analysis_options.yaml
└── ...
```

---

### `flutterator add-domain`

**Adds a domain entity (model + infrastructure only).**

Domain entities are shared business entities that can be used by multiple features. They do NOT include application or presentation layers.

#### Syntax

```bash
flutterator add-domain [OPTIONS]
```

#### Options

| Option           | Type   | Required | Default     | Description                       |
| ---------------- | ------ | -------- | ----------- | --------------------------------- |
| `--name`         | string | ✅        | -           | Domain entity name                |
| `--fields`       | string | ❌        | -           | Fields as name:type,name:type     |
| `--folder`       | string | ❌        | from config | Domain folder (default: "domain") |
| `--dry-run`      | flag   | ❌        | `false`     | Preview without creating          |
| `--no-build`     | flag   | ❌        | `false`     | Skip flutter pub get              |
| `--project-path` | string | ❌        | `.`         | Project path                      |

#### Usage Modes

**Command line:**

```bash
flutterator add-domain --name todo --fields "title:string,done:bool,priority:int"
```

**Interactive mode:**

```bash
flutterator add-domain --name todo
```

```
Domain entity name: todo
Fields (name:type,name:type): title:string,done:bool,priority:int
```

#### Examples

```bash
# Domain entity with fields
flutterator add-domain --name todo --fields "title:string,done:bool,priority:int"

# Interactive mode (will prompt for fields)
flutterator add-domain --name user

# Preview what will be created
flutterator add-domain --name product --fields "name:string,price:double" --dry-run

# Custom domain folder
flutterator add-domain --name note --fields "title:string" --folder shared/domain
```

#### Generated Structure

```
lib/domain/todo/
├── model/
│   ├── todo.dart
│   ├── todo_failure.dart
│   ├── i_todo_repository.dart
│   ├── value_objects.dart
│   └── value_validators.dart
└── infrastructure/
    ├── todo_dto.dart
    ├── todo_service.dart
    ├── todo_mapper.dart
    └── todo_repository.dart
```

---

### `flutterator add-page`

**Adds a simple page without business logic.**

Ideal for static pages like About, Settings, Privacy Policy, etc.

#### Syntax

```bash
flutterator add-page [OPTIONS]
```

#### Options

| Option           | Type   | Required | Default     | Description              |
| ---------------- | ------ | -------- | ----------- | ------------------------ |
| `--name`         | string | ✅        | -           | Page name                |
| `--folder`       | string | ❌        | from config | Destination folder       |
| `--dry-run`      | flag   | ❌        | `false`     | Preview without creating |
| `--no-build`     | flag   | ❌        | `false`     | Skip flutter pub get     |
| `--project-path` | string | ❌        | `.`         | Project path             |

#### Usage Modes

**Command line:**

```bash
flutterator add-page --name settings
```

**Interactive mode:**

```bash
flutterator add-page
```

```
Page name: settings
```

#### Examples

```bash
# Settings page
flutterator add-page --name settings

# About page with preview
flutterator add-page --name about --dry-run

# Page in specific folder
flutterator add-page --name privacy --folder pages
```

#### Generated Structure

```
lib/features/settings/
└── settings_page.dart
```

**Also updates:**
- `lib/router.dart` - Adds the new route

---

### `flutterator add-component`

**Adds a reusable component with optional BLoC.**

Supports three types: single (single item), list (list with CRUD), and form (form with validation).

#### Syntax

```bash
flutterator add-component [OPTIONS]
```

#### Options

| Option       | Type   | Required | Default               | Description                          |
| ------------ | ------ | -------- | --------------------- | ------------------------------------ |
| `--name`     | string | ✅        | -                     | Component name                       |
| `--type`     | choice | ❌        | -                     | Type: `form`, `list`, or `single`    |
| `--fields`   | string | ❌        | -                     | Form fields (requires `--type form`) |
| `--folder`   | string | ❌        | `features/components` | Destination folder                   |
| `--dry-run`  | flag   | ❌        | `false`               | Preview without creating             |
| `--no-build` | flag   | ❌        | `false`               | Skip flutter pub get                 |

#### Three Component Types

**1. Single Component** (`--type single` or default) - Widget that displays a single item loaded by ID:

```bash
flutterator add-component --name user_card
# or
flutterator add-component --name user_card --type single
```

**2. List Component** (`--type list`) - Widget that displays a list of items with complete CRUD operations:

```bash
flutterator add-component --name todo_list --type list
```

**3. Form Component** (`--type form`) - Form with validation and field management:

```bash
flutterator add-component --name login --type form --fields "email:string,password:string"
```

#### Usage Modes

**Command line:**

```bash
# Single component (default)
flutterator add-component --name user_card

# List component
flutterator add-component --name todo_list --type list

# Form component
flutterator add-component --name login --type form --fields "email:string,password:string"
```

**Interactive mode:**

```bash
flutterator add-component
```

```
Component name: todo_list
Select component type:
  1. Single item (loads one item by ID)
  2. List (shows all items with CRUD operations)
  3. Form (form with validation)
Type (1-3): 2
```

#### Examples

```bash
# Single component (default)
flutterator add-component --name user_card

# List component with complete CRUD
flutterator add-component --name todo_list --type list

# Form component with fields
flutterator add-component --name login --type form --fields "email:string,password:string"

# Component in specific folder
flutterator add-component --name search_bar --folder shared/widgets

# Registration form
flutterator add-component --name registration --type form --fields "name:string,email:string,password:string"
```

#### Generated Structure

**Single Component:**

```
lib/user_card/
├── application/
│   ├── user_card_bloc.dart
│   ├── user_card_event.dart
│   └── user_card_state.dart
└── presentation/
    └── user_card_component.dart
```

**List Component:**

```
lib/todo_list/
├── application/
│   ├── todo_list_bloc.dart      # BLoC with getAll, create, update, delete
│   ├── todo_list_event.dart      # loadRequested, createRequested, updateRequested, deleteRequested
│   └── todo_list_state.dart      # initial, loading, loaded(List<Model>), error
└── presentation/
    └── todo_list_component.dart   # Widget with ListView and CRUD operations
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

<!-- DEPRECATED: This command has been removed from the CLI but code is maintained for backward compatibility -->
<!-- ### `flutterator add-drawer-item` (DEPRECATED)

**Adds an item to the drawer (side menu) navigation.**

Creates the page, drawer (if it doesn't exist) and configures everything automatically.

**⚠️ DEPRECATED**: This command has been removed. Use `add-page` for simple pages or `add-component` for more complex navigation.

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
3. ✅ Aggiorna `lib/features/home/home_page.dart` (aggiunge drawer)
4. ✅ Aggiorna `lib/router.dart`

-->

---

<!-- DEPRECATED: This command has been removed from the CLI but code is maintained for backward compatibility -->
<!-- ### `flutterator add-bottom-nav-item` (DEPRECATED)

**Adds a tab to the bottom navigation bar.**

Creates the screen and configures the bottom navigation automatically.

**⚠️ DEPRECATED**: This command has been removed. Use `add-page` for simple pages or `add-component` for more complex navigation.

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

1. ✅ Crea `lib/features/home/<nome>_screen.dart`
2. ✅ Crea/Aggiorna `lib/core/presentation/bottom_nav_bar.dart`
3. ✅ Aggiorna `lib/features/home/home_page.dart` (aggiunge BottomNavigationBar)

-->
---

### `flutterator list`

**Lists pages and domain models in the project.**

Shows all pages parsed from `router.dart` and all domain models from the `domain/` folder.

#### Syntax

```bash
flutterator list [OPTIONS]
```

#### Options

| Option           | Type   | Required | Default | Description  |
| ---------------- | ------ | -------- | ------- | ------------ |
| `--project-path` | string | ❌        | `.`     | Project path |

#### Examples

```bash
# List pages and models
flutterator list
```

#### Example Output

```
╭──────────────────────╮
│ 📋 Project: my_app   │
╰──────────────────────╯

📄 Pages:
   /home          → HomePage        (lib/features/home/home_page.dart)
   /              → SplashPage      (lib/features/splash/splash_page.dart)
   /settings      → SettingsPage     (lib/features/settings/settings_page.dart)

📦 Domain Models:
   todo           (lib/domain/todo/model/todo.dart)
   user           (lib/domain/user/model/user.dart)
```

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

**Manages Flutterator configuration.**

Allows viewing or creating the configuration file.

#### Syntax

```bash
flutterator config [OPTIONS]
```

#### Options

| Option           | Type   | Description                |
| ---------------- | ------ | -------------------------- |
| `--show`         | flag   | Show current configuration |
| `--init`         | flag   | Create configuration file  |
| `--project-path` | string | Project path               |

#### Examples

```bash
# Show current configuration
flutterator config --show

# Create configuration file
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

## 🏃 Global Flags

These flags are available for all `add-*` commands:

| Flag             | Description                               | Example                 |
| ---------------- | ----------------------------------------- | ----------------------- |
| `--dry-run`      | Preview without creating files            | `--dry-run`             |
| `--no-build`     | Skip `flutter pub get` and `build_runner` | `--no-build`            |
| `--project-path` | Specify project path                      | `--project-path ../app` |

### --dry-run Example

```bash
$ flutterator add-domain --name todo --fields "title:string" --dry-run
$ flutterator add-component --name todo_list --type list --dry-run
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

### --no-build Example

```bash
# Faster: skip pub get and build_runner
flutterator add-domain --name todo --fields "title:string" --no-build
flutterator add-component --name todo_list --type list --no-build

# Then run manually when you want
flutter pub get
dart run build_runner build --delete-conflicting-outputs
```

---

## ⚙️ Configuration

### Configuration Priority

Flutterator loads configuration from multiple sources (in priority order):

1. **🔴 CLI Flags** (highest priority) - `--folder features`
2. **🟠 `flutterator.yaml`** in project
3. **🟡 `~/.flutteratorrc`** global (home directory)
4. **🟢 Defaults** (lowest priority)

### Create Configuration

```bash
# Create flutterator.yaml in project
flutterator config --init
```

### flutterator.yaml Example

```yaml
# 📁 Default folders for generated code
defaults:
  feature_folder: "features"     # lib/features/todo/
  domain_folder: "domain"         # lib/domain/note/ (shared entities)
  component_folder: "features/components" # lib/features/components/user_card/
  auto_run_build_runner: true    # Runs build_runner after generation

# 🎨 UI Configuration (for future reference)
styling:
  primary_color: "#2196F3"
  secondary_color: "#FF9800"
```

### ~/.flutteratorrc Example (Global)

```yaml
# Global configuration for all projects
defaults:
  feature_folder: "features"
  auto_run_build_runner: false  # Disable for all projects
```

---

## 🏗️ Generated Architecture

Flutterator generates projects following **DDD (Domain-Driven Design)** architecture with layer separation:

```
lib/
├── core/                        # 🔧 CORE - Shared code
│   ├── model/                   # Value objects, common failures
│   │   ├── value_objects.dart
│   │   ├── value_failures.dart
│   │   └── value_validators.dart
│   ├── infrastructure/          # DI modules, helpers
│   │   └── firebase_injectable_module.dart
│   └── presentation/            # Common widgets
│       └── app_widget.dart
│
├── domain/                      # 🏛️ DOMAIN ENTITIES - Shared entities
│   ├── auth/                    # Auth entity (shared)
│   │   ├── model/               # Entity, failures, repository interface
│   │   │   ├── user.dart
│   │   │   ├── user_profile.dart
│   │   │   └── i_auth_facade.dart
│   │   └── infrastructure/      # Repository implementation, DTOs
│   │       ├── firebase_auth_facade.dart
│   │       └── user_profile_repository.dart
│   │
│   └── note/                    # Example: Note entity (shared)
│       ├── model/
│       │   ├── note.dart
│       │   └── i_note_repository.dart
│       └── infrastructure/
│           └── note_repository.dart
│
├── features/                    # 📦 FEATURES - Specific use cases
│   ├── auth/                    # Auth feature (complete use case)
│   │   ├── application/         # ⚙️ APPLICATION LAYER
│   │   │   ├── auth_bloc.dart
│   │   │   ├── auth_event.dart
│   │   │   └── auth_state.dart
│   │   └── presentation/        # 🎨 PRESENTATION LAYER
│   │       └── login_page.dart
│   │
│   └── notes/                    # Example feature "note management"
│       │                          # (uses domain/note)
│       ├── application/         # ⚙️ APPLICATION LAYER
│       │   ├── notes_bloc.dart      # BLoC (logic)
│       │   ├── notes_event.dart     # Events
│       │   └── notes_state.dart     # States
│       │
│       └── presentation/        # 🎨 PRESENTATION LAYER
│           └── notes_page.dart      # UI
│
├── shared/                      # 🧩 SHARED - Shared components
│   └── widgets/
│
├── main.dart                    # Entry point
├── injection.dart               # 💉 Dependency Injection
└── router.dart                  # 🛤️ Routing (auto_route)
```

### Why DDD?

| Benefit             | Description                              |
| ------------------- | ---------------------------------------- |
| **Testability**     | Each layer is isolated and testable      |
| **Maintainability** | Organized and predictable code           |
| **Scalability**     | Easy to add new features                 |
| **Team**            | Multiple developers can work in parallel |

---

## 📚 Flutter Generated Dependencies

Generated projects use these standard Flutter dependencies:

| Package           | Purpose                | Link                                                |
| ----------------- | ---------------------- | --------------------------------------------------- |
| `flutter_bloc`    | State management       | [pub.dev](https://pub.dev/packages/flutter_bloc)    |
| `freezed`         | Immutable classes      | [pub.dev](https://pub.dev/packages/freezed)         |
| `injectable`      | Dependency injection   | [pub.dev](https://pub.dev/packages/injectable)      |
| `auto_route`      | Declarative routing    | [pub.dev](https://pub.dev/packages/auto_route)      |
| `dartz`           | Functional programming | [pub.dev](https://pub.dev/packages/dartz)           |
| `json_annotation` | JSON serialization     | [pub.dev](https://pub.dev/packages/json_annotation) |

---

## 🧪 Testing

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Only fast tests (without E2E)
pytest tests/test_basic.py tests/test_integration.py -v

# Only E2E tests (requires Flutter SDK installed)
pytest tests/test_e2e_flutter.py -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

---

## 🔧 Troubleshooting

### "Command not found: flutterator"

```bash
# Make sure you installed correctly
pip install -e .

# Or use python directly
python flutterator.py --help
```

### "Not a valid Flutter project"

```bash
# Flutterator requires pubspec.yaml and lib/
# Make sure you're in a valid Flutter project
ls pubspec.yaml lib/
```

### "rich import error" in IDE

The IDE might not recognize the virtual environment. Solution:
1. `Cmd+Shift+P` → "Python: Select Interpreter"
2. Select `./venv/bin/python`

### build_runner slow

```bash
# Use --no-build to skip build_runner
flutterator add-domain --name todo --fields "title:string" --no-build
flutterator add-component --name todo_list --type list --no-build

# Run build_runner once at the end
dart run build_runner build --delete-conflicting-outputs
```

### Dart compilation errors

After generating code, run:

```bash
flutter pub get
dart run build_runner build --delete-conflicting-outputs
```

---

## 🤝 Contributing

1. Fork the repository
2. Create branch: `git checkout -b feature/new-feature`
3. Commit: `git commit -m 'Add new feature'`
4. Push: `git push origin feature/new-feature`
5. Open Pull Request

### Project Structure

```
flutterator/
├── flutterator.py              # Main CLI
├── generators/
│   ├── helpers/                # Helper functions
│   │   ├── config.py           # Configuration management
│   │   └── project.py          # Project validation
│   └── static/templates/       # Jinja2 templates
├── tests/                      # Test suite
└── docs/                       # Documentation
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 👨‍💻 Author

**Lorenzo Busi** - [GetAutomation](https://getautomation.it)

---

## 🙏 Acknowledgments

- [Click](https://click.palletsprojects.com/) - CLI framework
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [Flutter](https://flutter.dev/) - UI framework
- [Reso Coder](https://resocoder.com/) - DDD architecture inspiration

---

<p align="center">
  <i>Generated with ❤️ by Flutterator</i>
</p>
