# Changelog

Tutti i cambiamenti notevoli a questo progetto saranno documentati in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

## [Unreleased]

---

## [3.0.0] - 2025-01-04

### 🔄 Refactoring Major

#### Rimozione comando `add-feature`
- **BREAKING**: Il comando `add-feature` è stato rimosso dalla CLI
- Il codice è mantenuto per retrocompatibilità ma il comando non è più accessibile
- **Migrazione**: Usa `add-domain` + `add-component --type list` invece di `add-feature`

#### Nuovo comando `add-domain`
- **Aggiunto**: Nuovo comando `add-domain` per creare entità domain (model + infrastructure)
- Crea solo i layer domain senza application/presentation
- Supporta modalità interattiva per i campi
- Supporta `--fields` in formato `"name:type,name:type"`
- Aggiunge automaticamente il campo `id` se non presente

#### Modifiche a `add-component`
- **BREAKING**: Rimosso flag `--form`, sostituito con `--type` che accetta: `form`, `list`, `single`
- **Aggiunto**: Supporto per tipo `list` che genera componente con CRUD completo
- **Aggiunto**: Modalità interattiva per selezionare il tipo se `--type` non è specificato
- Il tipo `list` genera:
  - BLoC con eventi: `loadRequested()`, `createRequested(item)`, `updateRequested(item)`, `deleteRequested(id)`
  - State con `List<Model> items`
  - Componente widget con ListView (senza Scaffold, solo BlocBuilder)

#### Modifiche a `add-page`
- **BREAKING**: Le pagine vengono ora create in `lib/features/{page_name}/` (senza cartella `presentation`) invece di `lib/{page_name}/presentation/`
- Il router viene aggiornato automaticamente con il percorso corretto
- Anche le pagine `home` e `splash` create con `create` seguono la stessa struttura: `lib/features/home/home_screen.dart` e `lib/features/splash/splash_screen.dart`

#### Template componenti lista
- **Modificato**: Template `component_list_widget_template.jinja` semplificato
- Rimosso `Scaffold`, `AppBar`, `FloatingActionButton` e `Builder`
- Il componente è ora un widget riutilizzabile che contiene solo `BlocBuilder`
- Il `BlocProvider` deve essere fornito dal widget parent

### 🐛 Fix

#### Esecuzione comandi
- **Fix**: I comandi flutterator vengono ora eseguiti nella directory di lavoro corrente invece che nella directory di installazione
- Risolve problemi quando si esegue flutterator da directory diverse

#### Entry point
- **Fix**: Aggiunto entry point mancante (`if __name__ == '__main__'`) in `flutterator.py`

### ✨ Miglioramenti

#### Documentazione
- Aggiornato README.md per riflettere i nuovi comandi
- Rimossa documentazione di `add-feature`
- Aggiunta documentazione per `add-domain`
- Aggiornata documentazione di `add-component` con i tre tipi
- Creato CHANGELOG.md per tracciare i cambiamenti

#### Test
- Aggiornati test per riflettere i nuovi comandi
- Aggiunto test per `add-component --type list`
- Rimossi test per `add-feature` (comando deprecato)

---

## [2.0.2] - 2025-12-09

### 🐛 Fix
- **Fix**: Esecuzione comandi flutterator nella directory di lavoro corrente invece che nella directory di installazione

---

## [2.0.1] - 2025-11-XX

### 🐛 Fix
- **Fix**: Aggiunto entry point mancante in `flutterator.py`

---

## [2.0.0] - 2025-11-XX

### ✨ Features
- **Feat**: Auto-installazione dipendenze al primo avvio
- **Feat**: Ripristinata distribuzione ZIP
- **Feat**: Build eseguibili standalone (PyInstaller) per Mac/Linux/Windows

### 🔧 Build
- Migliorato script di build
- Aggiornate GitHub Actions per il build automatizzato

---

## Note sulla Migrazione

### Da `add-feature` a `add-domain` + `add-component`

**Prima:**
```bash
flutterator add-feature --name todo --fields "title:string,done:bool"
```

**Dopo:**
```bash
# Crea domain entity
flutterator add-domain --name todo --fields "title:string,done:bool"

# Crea componente lista (opzionale)
flutterator add-component --name todo_list --type list
```

### Da `add-feature --domain` a `add-domain`

**Prima:**
```bash
flutterator add-feature --name todo --domain --fields "title:string"
```

**Dopo:**
```bash
flutterator add-domain --name todo --fields "title:string"
```

### Da `add-feature --presentation` a `add-component --type list`

**Prima:**
```bash
flutterator add-feature --name todo --presentation
```

**Dopo:**
```bash
flutterator add-component --name todo_list --type list
```

### Struttura pagine

**Prima:**
```
lib/settings/presentation/settings_page.dart
```

**Dopo:**
```
lib/features/settings/settings_page.dart
```

---

## Tipi di Componente

### `--type single` (default)
Componente che mostra un singolo item caricato per ID.

### `--type list`
Componente che mostra una lista di items con operazioni CRUD complete:
- Carica tutti gli items
- Crea nuovi items
- Modifica items esistenti
- Elimina items

### `--type form`
Componente form con validazione e gestione campi.
