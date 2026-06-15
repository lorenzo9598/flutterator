# Changelog

## [3.1.6] - 2026-06-15

### Release

- Version aligned with CLI **3.1.6**; published automatically via GitHub Actions to VS Code Marketplace and Open VSX alongside PyPI.

### Compatibilità CLI

- **Ultima verifica** con il CLI del repo: **3.1.6** (`pyproject.toml` / `flutterator --version`).

## [3.1.5] - 2026-04-16

### Documentazione / versioning

- Root `CHANGELOG.md`: sezione **3.1.5** e cronologia **3.1.2–3.1.5** del CLI.
- Compatibilità documentata con il CLI **3.1.5** (`pyproject.toml` / `flutterator --version`).

## [3.1.4] - 2026-04-16

### Allineamento CLI (PyPI / repo)

- Documentate in root `CHANGELOG.md` le release **3.1.2–3.1.4** del CLI: form vuoto, parsing nullable nei generici, help `--fields` e note zsh.

## [3.1.3] - 2026-04-16

### CLI

- Validazione tipi: generici con `?` interno (`List<String?>`, `Map<String, String?>`) e parametri nullable nei type arguments.

## [3.1.2] - 2026-04-16

### CLI

- `add-component --type form` senza modello e senza campi: scaffold vuoto (dominio “0 – Vuoto” o `--domain-model none`).

## [3.1.1] - 2026-04-16

### Documentazione

- README con link espliciti a **[PyPI — flutterator](https://pypi.org/project/flutterator/)** e al **[repository GitHub](https://github.com/lorenzo9598/flutterator)**.
- `package.json`: `homepage` → PyPI del CLI, `bugs` → issue tracker del repo.

## [3.1.0] - 2026-04-16

### Versioning

- La versione dell’estensione segue la **major.minor** del **Flutterator CLI** con cui è pensata / testata (qui linea **3.1**). Il **patch** dell’estensione (`3.1.0`, `3.1.1`, …) è indipendente dalla patch del CLI su PyPI (`3.1.4`, `3.1.5`, …).

### Compatibilità CLI

- **Ultima verifica manuale** con il CLI del repo: **3.1.5** (vedi `CHANGELOG.md` in radice e `version` in `pyproject.toml`).
- In uso: controlla con `flutterator --version` o `pip show flutterator`.

### Contenuto

- Estensione VS Code / Cursor: palette comandi, Quick Input, menu Explorer, output dedicato (vedi `README.md`).
