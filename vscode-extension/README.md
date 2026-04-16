# Flutterator VS Code / Cursor extension

Run the Flutterator CLI from the editor: **Command Palette** (`Cmd+Shift+P` / `Ctrl+Shift+P`), Quick Input wizards, and **Explorer** right‑click on folders (submenu **Flutterator**).

## Requirements

- `flutterator` on your `PATH`, **or** set **Flutterator: Executable Path** in Settings (`flutterator.executablePath`).

## Commands

| Command | Description |
|--------|-------------|
| **Flutterator: Create** | New project (`create --name … --login` / `--no-login`) |
| **Flutterator: Add Page** | `add-page` |
| **Flutterator: Add Domain** | `add-domain` (optional `--fields`, `--non-interactive` when empty) |
| **Flutterator: Add Component** | `add-component` with `--domain-model` / `--use-all-model-fields` as needed |
| **Flutterator: Add Enum** | `add-enum` (optional `--force`) |
| **Flutterator: Show Output** | Opens the Flutterator output log |

Default keybinding for **Show Output**: `Cmd+Shift+Alt+F` (macOS) / `Ctrl+Shift+Alt+F` (Windows/Linux). Change or remove it under Keyboard Shortcuts.

## Explorer context menu

Right‑click a **folder** → **Flutterator** → Add Page / Add Domain / Add Component / Add Enum. The same wizards run; the Flutter project root is found by walking up to `pubspec.yaml`, and a folder under `lib/` becomes the suggested `--folder` for components.

## Development

```bash
cd vscode-extension
npm install
npm run compile
```

Press `F5` in VS Code with this folder opened to launch an **Extension Development Host**.

Package a VSIX (install [`@vscode/vsce`](https://github.com/microsoft/vscode-vsce) globally): `vsce package`.
