# Flutterator

A CLI tool to generate Flutter projects with custom folder structure and pre-configured settings.

## Features

- ✅ Creates Flutter projects with custom folder structure
- 🔐 Optional login support (Email/Password)
- 📄 Add new pages to existing projects
- 🔧 Add complete features with full Clean Architecture layers
- 📦 Automatically adds common dependencies
- 🚀 Ready-to-use example files
- 📁 Organized structure for scalable projects

## Commands

### Create Project
```bash
flutterator create --name my_app --login
```

### Add Page
```bash
flutterator add-page --name profile --project-path ./my_app
```

### Add Feature
```bash
# With fields specified
flutterator add-feature --name task --fields "title:string,description:string,isCompleted:bool" --project-path ./my_app

# Interactive mode
flutterator add-feature --name note --interactive --project-path ./my_app
```

### Add Navigation Items (Coming Soon)
```bash
flutterator add-drawer-item --name settings --project-path ./my_app
flutterator add-bottom-nav-item --name home --project-path ./my_app
```

## Folder Structure

```
lib/
├── apis/
│   ├── clients/
│   ├── common/
│   └── interceptors/
├── auth/ (if login enabled)
│   ├── application/
│   ├── infrastructure/
│   ├── model/
│   └── presentation/
├── core/
│   ├── infrastructure/
│   ├── model/
│   └── presentation/
├── home/
│   └── presentation/
├── logging/
├── splash/
│   └── presentation/
└── storage/
```

## Feature Structure

When adding a feature, the following structure is created:

```
lib/
└── feature_name/
    ├── application/
    │   ├── feature_name_bloc.dart
    │   ├── get_feature_name_use_case.dart
    │   └── create_feature_name_use_case.dart
    ├── infrastructure/
    │   └── feature_name_repository_impl.dart
    ├── model/
    │   └── feature_name.dart
    └── presentation/
        └── feature_name_page.dart
```
