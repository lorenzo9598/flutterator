# Feature: ecosistema Cursor al `flutterator create`

## Stato

**Implementato.** Ogni `flutterator create` (salvo `--no-cursor`) genera rules, AGENTS.md, 10 subagents, skill `epic-delivery`, e documentazione architettura.

## Obiettivo

Guidare l'IA a **scrivere codice Dart direttamente** seguendo l'architettura DDD Flutterator — **senza** usare la CLI `flutterator`.

## Cosa viene generato

```
.cursor/rules/          # 8-9 file .mdc
.cursor/agents/         # 10 subagents
.cursor/skills/epic-delivery/
docs/architecture/      # DDD_LAYERS, FILE_TEMPLATES, WIDGETS_AND_CARAVAGGIO, ...
docs/epics/README.md
AGENTS.md               # root + lib/domain|features|widgets/
test/README.md
```

## Subagents (10)

| Subagent | Ruolo |
|----------|-------|
| `epic-orchestrator` | Entry point per epic; sceglie small vs large |
| `feature-implementer` | Fast path: 1 entità + 1 UI |
| `layer-model` | Domain model |
| `layer-infrastructure` | Domain infra |
| `layer-application` | BLoC |
| `layer-presentation` | UI CaravaggioUI |
| `integration-wiring` | router, DI, error_localizer, apis |
| `doc-writer` | Dartdoc + AGENTS.md per feature |
| `test-writer` | Test in `test/` |
| `layer-guardian` | Audit DDD readonly |

## Skill epic-delivery

Descrizione alto livello → epics in `docs/epics/` → orchestrazione con modalità **small** (~4-5 spawn) o **large** (~6-7 spawn).

## Implementazione

- Template: `generators/static/cursor/`
- Copia/render: `generators/cursor/setup.py` → `copy_cursor_ecosystem()`
- Hook: `generators/main.py` → `init(..., cursor_setup=True)`
- Opt-out: `flutterator create --no-cursor`

## Test

`tests/test_cursor_setup.py`
