# Android UI Flow Automator

An extensible automation framework built with **Python** and **uiautomator2** for verifying complex user journeys, monitoring UI-based performance metrics, and stress-testing cross-application navigation (Deep Links) on Android.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12+ |
| Device Control | ADB (Android Debug Bridge), uiautomator2 |
| Data Processing | Pandas, OpenPyXL |
| XPath / XML | lxml |
| Configuration | python-dotenv |

---

## Key Features

- **Smart Metric Extraction** — advanced parsing of numerical data from the UI, supporting shorthand notations (e.g., "10.5K", "19,5К" → raw integers)
- **Threshold-Based Termination** — automatically stops interaction once a UI metric reaches a predefined target
- **Deep Link Verification** — validates correct transition from an external browser to internal application states
- **Automated Session Rotation** — multi-account authentication cycles for long-running test suites
- **Adaptive UI Handling** — intercepts system dialogs ("Open with", "Always", "Just once") and suppresses pop-ups
- **Excel-Based Task Inventory** — manages tasks and progress tracking via a local `.xlsx` file

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│               MobileFlowEngine                  │
├─────────────────────────────────────────────────┤
│  _initialize_driver()   → ADB connection        │
│  perform_auth()         → Login flow            │
│  process_tasks()        → Main loop             │
│  fetch_ui_metric()      → XPath metric read     │
│  handle_system_dialogs()→ Pop-up suppression    │
└─────────────────────────────────────────────────┘
         │                        │
    settings.py              inventory.xlsx
  (env-driven config)       (task dataframe)
```

- **Logic Engine** — interaction logic is decoupled from UI selectors
- **Environment Driven** — sensitive IDs and device serials live in `.env`, never in source
- **Data-Centric** — Pandas manages real-time task inventory and progress tracking

---

## Project Structure

```
Android-UI-Flow-Automator/
├── app_automator.py     # Main execution engine (MobileFlowEngine class)
├── settings.py          # Centralized configuration loader (.env → CONFIG dict)
├── .env.example         # Template for environment variables
├── requirements.txt     # Python dependencies
├── .gitignore           # VCS exclusion rules
└── README.md            # Project documentation
```

Runtime data files (not tracked in VCS):
- `inventory.xlsx` — task list with columns: `url`, `initial_value`, `progress`, `target`
- `credentials.txt` — account credentials in `user:password` format (one per line)

---

## Installation & Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/OniSku/Android-UI-Flow-Automator.git
cd Android-UI-Flow-Automator
pip install -r requirements.txt
```

### 2. Configure environment

Rename `.env.example` to `.env` and update the values:

| Variable | Description | Default |
|----------|-------------|---------|
| `ADB_SERIAL` | ADB device serial or emulator address | `127.0.0.1:5555` |
| `TARGET_PACKAGE` | Package name of the target application | `com.example.app` |
| `BROWSER_PACKAGE` | Package name of the browser | `com.android.chrome` |
| `APP_LABEL` | Display label for system dialog matching | `TargetApp` |
| `UI_NAV_PROFILE_ID` | Resource ID of the profile navigation element | — |
| `UI_ACTION_BUTTON_ID` | Resource ID of the primary action button | — |
| `UI_LOGOUT_BUTTON_ID` | Resource ID of the logout button | — |
| `METRIC_KEYWORD` | Keyword to locate the metric element in UI | `followers` |

### 3. Prepare data files

- **inventory.xlsx** — Excel file with columns: `url`, `initial_value`, `progress`, `target`
- **credentials.txt** — one `username:password` pair per line

### 4. Connect device

Ensure your Android device or emulator has USB/ADB debugging enabled:

```bash
adb devices   # verify connection
```

### 5. Run

```bash
python app_automator.py
```

The engine initializes the driver, loads the task inventory, and begins the interaction cycle.

---

## How It Works

1. Reads active tasks from `inventory.xlsx` (filters out completed ones)
2. Rotates through accounts in `credentials.txt`
3. Authenticates into the target app
4. Opens each task URL in Chrome, triggering a Deep Link into the target app
5. Reads the current UI metric and records the initial value
6. Performs the target action and increments progress
7. Removes tasks that have reached their target threshold
8. Rotates to the next account and repeats

---

## Disclaimer

This framework is intended strictly for QA automation, UI/UX research, and internal application testing. The developer is not responsible for any misuse of this tool.
