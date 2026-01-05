# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

---

## [3.1.1] - 2025-01-XX

### 🔧 Maintenance
- Version bump for release

---

## [3.1.0] - 2025-01-XX

### ✨ Features

#### Input Validation Improvements
- **ADDED**: Robust validation for field names and types in `add-domain` command
- **ADDED**: Validation for Dart reserved keywords in field names
- **ADDED**: Validation for valid Dart types (primitives, collections, domain models)
- **ADDED**: Better error messages with suggestions when validation fails
- **ADDED**: Support for composite model names (e.g., `NoteItem`) - maintains PascalCase for Dart classes while using snake_case for folder names

#### Complex Type Support
- **ADDED**: Support for complex types like `List<ModelName>` where `ModelName` is an existing domain model
- **ADDED**: Automatic validation that referenced models exist before allowing their use
- **ADDED**: Helpful error messages listing available models when a model name is incorrect
- **ADDED**: Support for both PascalCase (`List<TodoItem>`) and snake_case (`List<todo_item>`) input formats

#### Form Component Generation
- **ADDED**: Automatic form generation based on domain model fields
- **ADDED**: Form component automatically includes all fields from the domain model
- **ADDED**: Feature folder selection when creating components (default: `components`)

### 🐛 Fixes

#### Domain Entity Generation
- **FIXED**: Entity class names now correctly use PascalCase (e.g., `TodoItem`) while folder names use snake_case (e.g., `todo_item`)
- **FIXED**: Part statements in generated files now use correct snake_case format
- **FIXED**: DTO fields for `List<ModelType>` now correctly generate as `List<ModelTypeDto>`
- **FIXED**: Missing imports for referenced models in both entity and DTO classes
- **FIXED**: Mapper now correctly handles `List<Model>` conversions using referenced mappers
- **FIXED**: Mapper constructor now properly injects dependencies for referenced mappers

#### Template Fixes
- **FIXED**: Removed commented-out sections in generated form component code
- **FIXED**: Jinja placeholders now correctly processed (changed from `{{ }}` to `[[ ]]`)
- **FIXED**: Service template now uses correct kebab-case for API routes
- **FIXED**: Repository interface names now use correct PascalCase

### 🔧 Improvements

#### Code Generation
- **IMPROVED**: Better handling of primitive types vs domain models in entity generation
- **IMPROVED**: Automatic import generation for referenced domain models
- **IMPROVED**: Mapper generation now handles complex types with proper dependency injection
- **IMPROVED**: Better separation between ValueObjects (for primitives) and direct types (for domain models)

#### Developer Experience
- **IMPROVED**: Interactive mode now provides helpful tips for field type input
- **IMPROVED**: Better error messages when creating domain entities with invalid field types
- **IMPROVED**: Validation now checks for available models and suggests correct names

---

## [3.0.2] - 2025-01-XX

### 🗑️ Deprecated Commands Removed from CLI

#### Commands Removed from CLI
- **REMOVED**: Commands `add-drawer-item`, `add-bottom-nav-item`, and `init` have been removed from the CLI
- Code is maintained for backward compatibility but commands are no longer accessible via `flutterator --help`
- **Note**: These commands were already deprecated, they are now completely hidden from the CLI

### 📚 Documentation

#### README.md
- **FIXED**: Fixed generated structure to correctly reflect:
  - Pages in `lib/features/` (not directly in `lib/`)
  - Domain entities in `lib/domain/`
- **ADDED**: Added complete documentation for the missing `add-domain` command

#### TEST_COVERAGE.md
- **UPDATED**: Updated to reflect deprecated commands removed from CLI
- Updated coverage matrix and statistics

### 🔧 Code Quality

- Deprecated command code maintained for backward compatibility
- Improved documentation organization

---

## [3.0.1] - 2025-01-04

### 🔧 Fix

#### `list` Command
- **FIX**: Fixed `router.dart` parsing to correctly handle nested parentheses in `GoRoute` blocks
- Command now correctly finds all pages defined in the router
- Improved parsing to read `routeName` value from page files

### Refactoring

#### `list` Command
- **BREAKING**: The `list` command has been simplified
- Removed `resource_type` arguments (features, pages, components, routes)
- Now shows only:
  - **Pages**: Parsed from `router.dart` (extract imports and GoRoute routes)
  - **Domain models**: Found using `find_domain_models` in the `domain/` folder
- Obsolete functions `_list_features`, `_list_pages`, `_list_components`, `_list_routes` have been commented out

---

## [3.0.0] - 2025-01-04

### 🔄 Major Refactoring

#### Removal of `add-feature` Command
- **BREAKING**: The `add-feature` command has been removed from the CLI
- Code is maintained for backward compatibility but the command is no longer accessible
- **Migration**: Use `add-domain` + `add-component --type list` instead of `add-feature`

#### New `add-domain` Command
- **Added**: New `add-domain` command to create domain entities (model + infrastructure)
- Creates only domain layers without application/presentation
- Supports interactive mode for fields
- Supports `--fields` in format `"name:type,name:type"`
- Automatically adds `id` field if not present

#### Changes to `add-component`
- **BREAKING**: Removed `--form` flag, replaced with `--type` that accepts: `form`, `list`, `single`
- **Added**: Support for `list` type that generates component with complete CRUD
- **Added**: Interactive mode to select type if `--type` is not specified
- The `list` type generates:
  - BLoC with events: `loadRequested()`, `createRequested(item)`, `updateRequested(item)`, `deleteRequested(id)`
  - State with `List<Model> items`
  - Component widget with ListView (without Scaffold, only BlocBuilder)

#### Changes to `add-page`
- **BREAKING**: Pages are now created in `lib/features/{page_name}/` (without `presentation` folder) instead of `lib/{page_name}/presentation/`
- Router is automatically updated with the correct path
- Pages `home` and `splash` created with `create` also follow the same structure: `lib/features/home/home_page.dart` and `lib/features/splash/splash_page.dart`

#### List Component Templates
- **Modified**: `component_list_widget_template.jinja` template simplified
- Removed `Scaffold`, `AppBar`, `FloatingActionButton`, and `Builder`
- Component is now a reusable widget that contains only `BlocBuilder`
- `BlocProvider` must be provided by the parent widget

### 🐛 Fix

#### Command Execution
- **Fix**: Flutterator commands are now executed in the current working directory instead of the installation directory
- Fixes issues when running flutterator from different directories

#### Entry Point
- **Fix**: Added missing entry point (`if __name__ == '__main__'`) in `flutterator.py`

### ✨ Improvements

#### Documentation
- Updated README.md to reflect new commands
- Removed documentation for `add-feature`
- Added documentation for `add-domain`
- Updated documentation for `add-component` with the three types
- Created CHANGELOG.md to track changes

#### Testing
- Updated tests to reflect new commands
- Added test for `add-component --type list`
- Removed tests for `add-feature` (deprecated command)

---

## [2.0.2] - 2025-12-09

### 🐛 Fix
- **Fix**: Flutterator commands execution in current working directory instead of installation directory

---

## [2.0.1] - 2025-11-XX

### 🐛 Fix
- **Fix**: Added missing entry point in `flutterator.py`

---

## [2.0.0] - 2025-11-XX

### ✨ Features
- **Feat**: Auto-installation of dependencies on first run
- **Feat**: ZIP distribution restored
- **Feat**: Build standalone executables (PyInstaller) for Mac/Linux/Windows

### 🔧 Build
- Improved build script
- Updated GitHub Actions for automated build

---

## Migration Notes

### From `add-feature` to `add-domain` + `add-component`

**Before:**
```bash
flutterator add-feature --name todo --fields "title:string,done:bool"
```

**After:**
```bash
# Create domain entity
flutterator add-domain --name todo --fields "title:string,done:bool"

# Create list component (optional)
flutterator add-component --name todo_list --type list
```

### From `add-feature --domain` to `add-domain`

**Before:**
```bash
flutterator add-feature --name todo --domain --fields "title:string"
```

**After:**
```bash
flutterator add-domain --name todo --fields "title:string"
```

### From `add-feature --presentation` to `add-component --type list`

**Before:**
```bash
flutterator add-feature --name todo --presentation
```

**After:**
```bash
flutterator add-component --name todo_list --type list
```

### Page Structure

**Before:**
```
lib/settings/presentation/settings_page.dart
```

**After:**
```
lib/features/settings/settings_page.dart
```

---

## Component Types

### `--type single` (default)
Component that displays a single item loaded by ID.

### `--type list`
Component that displays a list of items with complete CRUD operations:
- Load all items
- Create new items
- Update existing items
- Delete items

### `--type form`
Form component with validation and field management.
