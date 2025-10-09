# Flutterator

A CLI tool to generate Flutter projects with custom folder structure and pre-configured settings.
## Features

- ✅ Creates Flutter projects with custom folder structure
- 🔐 Optional login support (Email/Password)
- 📦 Automatically adds common dependencies
- 🚀 Ready-to-use example files
- 📁 Organized structure for scalable projects

## Folder Structure

```
lib/
├── apis/
│   ├── clients/
│   ├── common/
│   ├── core/
│   └── interceptor/
├── application/
│   └── auth/ (se login abilitato)
├── infrastructure/
│   ├── core/
│   ├── auth/ (se login abilitato)
│   └── storage/
├── logging/
├── model/
│   ├── auth/ (se login abilitato)
│   └── core/
└── presentation/
    ├── auth/ (se login abilitato)
    ├── core/
    ├── home/
    └── splash/
```

## Install

### Prerequisites
- Python 3.7+
- Flutter SDK installed and in PATH

### CLI Installation

#### Download
1. Go to [www.flutterator.com](https://www.flutterator.com)
2. Download the ZIP file
3. Extract it to your desired folder

#### Add to PATH

**Windows:**
1. Extract the ZIP to a folder (e.g., `C:\flutterator`)
2. Add the folder to your PATH:
   - Open System Properties → Advanced → Environment Variables
   - Edit the `PATH` variable and add `C:\flutterator`
   - Restart your terminal

**macOS/Linux:**
1. Extract the ZIP to a folder (e.g., `/usr/local/flutterator`)
2. Add to PATH by adding this line to your `~/.bashrc` or `~/.zshrc`:
   ```bash
   export PATH="/usr/local/flutterator:$PATH"
   ```
3. Reload your shell: `source ~/.bashrc` or `source ~/.zshrc`

## Usage

### Interactive Mode (Recommended)

```bash
flutterator create
```

The CLI will guide you through the options:
- Project name
- Whether to include login functionality
- Login types to support

### Command with Parameters

```bash
# Basic project without login
flutterator create --name my_project

# Project with login
flutterator create --name my_project --login
```

### Available Options

- `--name TEXT`: Project name (required when not in interactive mode)
- `--login`: Include login functionality
- `--help`: Show help

## Example Usage

```bash
$ flutterator create
Project name: my_awesome_app 
Does the project have login? [y/N]: y
prova2

🚀 Creating Flutter project: my_awesome_app

📁 Creating folder structure...

📁 Generating files...

✅ Project created successfully!

📋 Summary:
   Name: prova2
   Path: /your/project/folder/my_awesome_app
   Login: ✅ Email/Password

🚀 To get started:
   cd my_awesome_app
   flutter pub get
   dart run build_runner build
   flutter run
```

## Generated Files

### Included Example Files
WIP

### Automatically Added Dependencies
**Always included:**

**Dependencies:**
- `dartz` - Functional programming constructs for Dart
- `freezed_annotation` - Annotations for code generation with freezed
- `injectable` - Compile-time dependency injection
- `flutter_bloc` - State management using the BLoC pattern
- `get_it` - Service locator for dependency injection
- `bloc` - Core BLoC state management library
- `another_flushbar` - Customizable snackbar notifications
- `caravaggio_ui` - UI component library
- `font_awesome_flutter` - Font Awesome icons for Flutter
- `uuid` - Generate RFC4122 UUIDs
- `collection` - Utility functions for collections
- `rxdart` - Reactive extensions for Dart streams
- `flutter_svg` - SVG rendering support
- `shared_preferences` - Local data persistence
- `dio` - HTTP client for API requests
- `retrofit` - Type-safe HTTP client generator
- `go_router` - Declarative routing solution

**Dev Dependencies:**
- `build_runner` - Code generation runner
- `freezed` - Code generation for data classes
- `injectable_generator` - Generator for injectable annotations
- `json_serializable` - JSON serialization code generation
- `retrofit_generator` - Generator for retrofit HTTP clients
- `flutter_launcher_icons` - Generate app launcher icons
- `analyzer` - Static analysis for Dart code

## Troubleshooting

### Flutter not found
```
❌ Flutter not found. Make sure Flutter is installed and in PATH.
```
**Solution:** Install Flutter and ensure it's in your PATH.

### Project creation error
```
❌ Error creating Flutter project
```
**Solution:** Verify the project name is valid (letters, numbers, _ and - only).

### Command not found
```
flutterator: command not found
```
**Solution:** Make sure flutterator is properly added to your PATH.

## Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests
- Improve documentation


## License

This project is released under the MIT License.
