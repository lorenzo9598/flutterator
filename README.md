# Flutterator

A comprehensive CLI tool to generate Flutter projects with custom folder structure, pre-configured settings, and powerful code generation capabilities.

## Features

- ✅ Creates Flutter projects with custom folder structure
- 🔐 Optional login support (Email/Password)
- 📄 Add new pages to existing projects
- 🔧 Add complete features with full Clean Architecture layers
- 🧩 Add reusable components with BLoC pattern
- 📱 Add drawer navigation items
- 📲 Add bottom navigation items
- 📦 Automatically adds common dependencies
- 🚀 Ready-to-use example files
- 📁 Organized structure for scalable projects
- 🎯 DDD (Domain-Driven Design) architecture
- 🔄 Automatic dependency injection setup

## Installation

```bash
# Clone the repository
git clone https://github.com/lorenzo9598/flutterator.git
cd flutterator

# Install dependencies
pip install -r requirements.txt

# Make it available globally (optional)
pip install -e .
```

## Commands

### Create Project
```bash
flutterator create --name my_app --login
```
Creates a new Flutter project with custom folder structure and optional login functionality.

### Add Page
```bash
flutterator add-page --name profile --project-path ./my_app
```
Adds a new page with route to an existing Flutter project.

### Add Feature
```bash
# With fields specified
flutterator add-feature --name task --fields "title:string,description:string,isCompleted:bool" --project-path ./my_app

# Interactive mode
flutterator add-feature --name note --interactive --project-path ./my_app
```
Adds a complete feature with full Clean Architecture layers (Model, Infrastructure, Application, Presentation).

### Add Component
```bash
# Interactive mode (recommended)
flutterator add-component --project-path ./my_app

# With parameters
flutterator add-component --name user_form --fields "name:string,email:string" --form --folder forms --project-path ./my_app

# Regular component
flutterator add-component --name user_card --fields "name:string,avatar:string" --project-path ./my_app
```
Adds a reusable component with BLoC pattern. Supports both regular components and form components.

**Component Types:**
- **Regular Component**: Full CRUD operations with infrastructure layer
- **Form Component**: Specialized for form handling with validation states

### Add Navigation Items

#### Drawer Items
```bash
flutterator add-drawer-item --name settings --project-path ./my_app
```
Adds a drawer navigation item with automatic page creation and routing.

#### Bottom Navigation Items
```bash
flutterator add-bottom-nav-item --name profile --project-path ./my_app
```
Adds a bottom navigation item with automatic screen creation (no routing needed).

## Project Structure

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
├── splash/
│   └── presentation/
├── storage/
└── [features/components]/
    ├── application/
    ├── infrastructure/ (only for regular features)
    ├── model/
    └── presentation/
```

## Feature vs Component

| Aspect             | Feature                                     | Component                     |
| ------------------ | ------------------------------------------- | ----------------------------- |
| **Purpose**        | Full business feature with data persistence | Reusable UI component         |
| **Routing**        | Includes route in router.dart               | No routing (reusable widget)  |
| **Infrastructure** | Full repository pattern                     | Only for regular components   |
| **Use Case**       | Todo list, User management                  | Form widgets, Card components |
| **Navigation**     | Can be navigated to                         | Used within other screens     |

## Examples

### Creating a Complete App Structure

```bash
# 1. Create project with login
flutterator create --name my_social_app --login

# 2. Add main features
flutterator add-feature --name post --fields "title:string,content:string,authorId:string" --project-path ./my_social_app
flutterator add-feature --name comment --fields "postId:string,text:string,userId:string" --project-path ./my_social_app

# 3. Add navigation
flutterator add-drawer-item --name notifications --project-path ./my_social_app
flutterator add-bottom-nav-item --name feed --project-path ./my_social_app
flutterator add-bottom-nav-item --name profile --project-path ./my_social_app

# 4. Add reusable components
flutterator add-component --name post_card --fields "title:string,content:string" --project-path ./my_social_app
flutterator add-component --name comment_form --fields "text:string" --form --folder forms --project-path ./my_social_app
```

### Interactive Component Creation

```bash
flutterator add-component --project-path ./my_app

# Will prompt:
# Component name: user_profile
# Field name (or 'done'): name
# Field type: String
# Field name (or 'done'): email
# Field type: String
# Field name (or 'done'): avatar
# Field type: String
# Field name (or 'done'): done
# Is this a form component? (y/N): n
# Folder (leave empty for root): shared/components
```

## Dependencies Added

The tool automatically adds these dependencies to your `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  go_router: ^12.1.1
  flutter_bloc: ^8.1.3
  freezed_annotation: ^2.4.1
  dartz: ^0.10.1
  injectable: ^2.4.1
  get_it: ^7.6.4

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.4.7
  freezed: ^2.4.6
  injectable_generator: ^2.6.1
```

## Architecture

Flutterator follows Clean Architecture principles with DDD (Domain-Driven Design):

- **Domain Layer**: Business logic, entities, value objects, failures
- **Application Layer**: BLoC pattern for state management
- **Infrastructure Layer**: Data persistence, API calls, external services
- **Presentation Layer**: UI components, screens, widgets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

---

**Created by Lorenzo Busi @ GetAutomation**
