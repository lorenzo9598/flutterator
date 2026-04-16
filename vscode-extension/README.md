# Flutterator (VS Code / Cursor)

Estensione che avvolge il **Flutterator CLI**: palette comandi, wizard con Quick Input e menu contestuale sull’Explorer per generare progetti Flutter in stile DDD.

## Link utili

| Risorsa | URL |
|--------|-----|
| **Sito Flutterator** (documentazione, getting started) | [flutterator.com](https://flutterator.com/) |
| **CLI su PyPI** (installazione consigliata) | [pypi.org/project/flutterator](https://pypi.org/project/flutterator/) |
| **Sorgente monorepo** (issue, PR, estensione in `vscode-extension/`) | [github.com/lorenzo9598/flutterator](https://github.com/lorenzo9598/flutterator) |

Il CLI si installa da PyPI, ad esempio:

```bash
pip install flutterator
```

## Versioni: estensione ↔ CLI

La **semver dell’estensione** (`package.json` → `version`) riusa la **major.minor** del Flutterator CLI con cui la release è **pensata e testata**. Il **patch** dell’estensione conta solo rilasci dell’UI (fix, compatibilità editor), **non** la patch del CLI su PyPI: il CLI può essere `3.1.4` mentre l’estensione è `3.1.0`, `3.1.1`, … purché resti la stessa linea **3.1.x**.

| Cosa | Dove leggerla |
|------|------------------|
| **Estensione** (questo pacchetto) | `version` in `package.json` |
| **CLI** nel monorepo | `project.version` in `pyproject.toml` (cartella radice del repo) |
| **CLI** sulla tua macchina | `flutterator --version` / `pip show flutterator` |

Le **release notes** per il Marketplace / GitHub sono in **`CHANGELOG.md`** (compatibilità CLI indicata lì a ogni bump).

## Requisito: il CLI Flutterator

Questa estensione **non** include l’eseguibile. Sul computer deve essere disponibile il comando `flutterator`. Il pacchetto ufficiale è su **[PyPI — flutterator](https://pypi.org/project/flutterator/)**.

1. **Installazione tipica (PATH)**  
   ```bash
   pip install flutterator
   ```  
   (vedi anche la pagina PyPI per versioni e metadati.)  
   Assicurati che lo script `flutterator` sia sul `PATH` del terminale **e** del processo con cui avvii VS Code / Cursor (su macOS/Linux spesso `~/.local/bin`).

2. **Percorso personalizzato**  
   Se non usi il PATH, imposta in **Impostazioni** la chiave **`flutterator.executablePath`** al percorso completo dell’eseguibile (es. `/opt/flutterator/bin/flutterator` o `C:\\Tools\\flutterator.exe`).

Senza CLI configurato correttamente, i comandi dell’estensione falliranno con errore nel pannello **Output** → canale **Flutterator**.

## Cosa offre l’estensione

| Area | Comportamento |
|------|-----------------|
| **Command Palette** | Comandi *Flutterator: …* (Create, Add Page, Add Domain, …). |
| **Explorer** | Tasto destro su una **cartella** → sottomenu **Flutterator** per lanciare gli stessi flussi con contesto sulla cartella. |
| **Output** | **Flutterator: Show Output** mostra i log del CLI. Scorciatoia predefinita: `Cmd+Shift+Alt+F` (macOS) / `Ctrl+Shift+Alt+F` (Windows/Linux), modificabile in Scorciatoie da tastiera. |

## Comandi

| Comando | Descrizione |
|---------|-------------|
| **Flutterator: Create** | Nuovo progetto (`create` con nome, login opzionale). |
| **Flutterator: Add Page** | `add-page`. |
| **Flutterator: Add Domain** | `add-domain` (campi opzionali, modalità non interattiva se vuoto). |
| **Flutterator: Add Component** | `add-component` con opzioni su domain model / campi. |
| **Flutterator: Add Enum** | `add-enum`. |
| **Flutterator: Show Output** | Apre il log Flutterator. |

## Explorer

Clic destro su una **cartella** → **Flutterator** → Add Page / Add Domain / Add Component / Add Enum. L’estensione risale fino a `pubspec.yaml` per individuare la root Flutter e suggerisce `--folder` per i componenti sotto `lib/`.

## Licenza

Il pacchetto VSIX e questa cartella includono **`LICENSE.md`** (MIT). Il campo `license` in `package.json` è `MIT`.

## Sviluppo e pacchetto VSIX

```bash
cd vscode-extension
npm install
npm run compile
```

- **F5** con questa cartella aperta: *Extension Development Host*.
- Pacchettizzazione: `npm run package` (usa `vsce` da devDependency) oppure `npx @vscode/vsce package`.

Repository Git e metadati npm: vedi `repository` e `bugs` in `package.json`. Il **sito ufficiale** del prodotto è [flutterator.com](https://flutterator.com/); in `package.json` il campo **homepage** punta al progetto PyPI del CLI (installazione).

Storico versioni estensione: `CHANGELOG.md`.
