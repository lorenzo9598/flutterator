# Flutter Project Generator CLI

Una CLI per generare progetti Flutter con una struttura personalizzata e configurazioni pre-impostate.

## Caratteristiche

- ✅ Crea progetti Flutter con struttura di cartelle personalizzata
- 🔐 Supporto opzionale per login (Email/Password, Google, Apple)
- 📦 Aggiunge automaticamente dipendenze comuni
- 🚀 File di esempio pronti all'uso
- 📁 Struttura organizzata per progetti scalabili

## Struttura delle Cartelle

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
│   └── auth/ (se login abilitato)
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

## Installazione

### Prerequisiti
- Python 3.7+
- Flutter SDK installato e nel PATH

### Installazione della CLI

1. Clona o scarica i file
2. Naviga nella cartella del progetto
3. Installa in modalità development:

```bash
pip install -e .
```

Oppure installa direttamente:

```bash
pip install .
```

### Installazione dipendenze

```bash
pip install click
```

## Utilizzo

### Modalità Interattiva (Consigliata)

```bash
flutter-gen
```

La CLI ti guiderà attraverso le opzioni:
- Nome del progetto
- Se includere login
- Tipi di login da supportare

### Modalità con Parametri

```bash
# Progetto base senza login
flutter-gen --name mio_progetto

# Progetto con login email/password
flutter-gen --name mio_progetto --login --email-password

# Progetto con tutti i tipi di login
flutter-gen --name mio_progetto --login --email-password --google --apple
```

### Opzioni Disponibili

- `--name TEXT`: Nome del progetto (richiesto)
- `--login`: Include funzionalità di login
- `--email-password`: Include login con email/password
- `--google`: Include login con Google
- `--apple`: Include login con Apple
- `--help`: Mostra l'aiuto

## Esempio di Utilizzo

```bash
$ flutter-gen
Nome del progetto: mia_app_fantastica
Il progetto ha login? [y/N]: y

🔐 Seleziona i tipi di login da includere:
  Email/Password? [y/N]: y
  Google? [y/N]: y  
  Apple? [y/N]: n

🚀 Creando progetto Flutter: mia_app_fantastica
🔐 Con login: Email/Password, Google

📦 Creando progetto Flutter base...
✅ Progetto Flutter creato

📁 Creando struttura delle cartelle...

✅ Progetto creato con successo!

📋 Riepilogo:
   Nome: mia_app_fantastica
   Percorso: /path/to/mia_app_fantastica
   Login: ✅ Email/Password, ✅ Google, ❌ Apple

🚀 Per iniziare:
   cd mia_app_fantastica
   flutter pub get
   flutter run
```

## File Generati

### File di Esempio Inclusi
- `main.dart` - Entry point dell'app
- `presentation/splash/splash_screen.dart` - Schermata di caricamento
- `presentation/home/home_screen.dart` - Schermata principale
- `presentation/auth/login_screen.dart` - Schermata di login (se abilitato)

### Dipendenze Aggiunte Automaticamente

**Sempre incluse:**
- `dio` - Client HTTP
- `get_it` - Dependency Injection
- `injectable` - Annotations per DI

**Con login:**
- `shared_preferences` - Storage locale
- `http` - Client HTTP aggiuntivo
- `google_sign_in` - Login Google (se selezionato)
- `sign_in_with_apple` - Login Apple (se selezionato)

## Sviluppo

### Struttura del Progetto
```
flutter-project-cli/
├── flutter_cli.py       # Script principale
├── setup.py             # Configurazione installazione
├── README.md            # Documentazione
└── requirements.txt     # Dipendenze Python
```

### Modifica della CLI

Per modificare la CLI:
1. Modifica `flutter_cli.py`
2. Reinstalla con `pip install -e .`
3. Testa i cambiamenti

### Aggiungere Nuove Funzionalità

Puoi facilmente estendere la CLI:
- Aggiungere nuovi tipi di login
- Modificare la struttura delle cartelle
- Includere template aggiuntivi
- Aggiungere configurazioni specifiche

## Troubleshooting

### Flutter non trovato
```
❌ Flutter non trovato. Assicurati che Flutter sia installato e nel PATH.
```
**Soluzione:** Installa Flutter e assicurati che sia nel PATH.

### Errore nella creazione del progetto
```
❌ Errore nella creazione del progetto Flutter
```
**Soluzione:** Verifica che il nome del progetto sia valido (solo lettere, numeri, _ e -).

### Click non installato
```
ModuleNotFoundError: No module named 'click'
```
**Soluzione:** Installa click con `pip install click`.

## Contributi

I contributi sono benvenuti! Sentiti libero di:
- Aprire issue per bug o richieste di funzionalità
- Inviare pull request
- Migliorare la documentazione

## Licenza

Questo progetto è rilasciato sotto licenza MIT.
