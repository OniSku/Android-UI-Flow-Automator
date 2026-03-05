# Mobile UI Flow Interaction Engine

A professional, extensible automation framework built with **Python** and **uiautomator2**. This engine is designed for verifying complex user journeys, monitoring UI-based performance metrics, and stress-testing cross-application navigation (Deep Links) within the Android ecosystem.



## Core Capabilities

- **Smart Metric Extraction**: Advanced parsing of numerical data directly from the UI, supporting shorthand notations (e.g., converting "10.5K" or "19,5К" into raw integers).
- **Threshold-Based Termination**: Intelligent task management that automatically ceases interaction once a specific UI metric reaches a predefined goal.
- **Deep Link Verification**: Validates the seamless transition from external browsers (e.g., Chrome) to internal application states.
- **Automated Session Rotation**: Built-in support for multi-account authentication cycles, ideal for long-running QA test suites.
- **Adaptive UI Handling**: Robust interception of system dialogs ("Open with", "Just once") and dynamic pop-up suppression.

## Technical Architecture

The framework is built on a modular architecture to ensure scalability and ease of maintenance:

- **Logic Engine**: Decoupled interaction logic from UI selectors.
- **Environment Driven**: Uses `.env` files to keep sensitive application IDs and hardware serials out of the source code.
- **Data-Centric**: Leverages **Pandas** for real-time task inventory management and progress tracking.



## Technology Stack

- **Language**: Python 3.12+
- **Drivers**: ADB (Android Debug Bridge), uiautomator2
- **Data Processing**: Pandas, OpenPyXL
- **Configuration**: python-dotenv, XML/XPath parsing

## Installation

1. Clone the repository to your local machine:
```bash
git clone [https://github.com/OniSku/Android-UI-Flow-Automator.git](https://github.com/OniSku/Android-UI-Flow-Automator.git)
Install the required dependencies:

pip install -r requirements.txt
Configure your environment:

Rename .env.example to .env.

Update the file with your specific device ADB serial and target application package IDs.

Project Structure
├── automator.py        # Main execution engine
├── settings.py         # Configuration and environment loader
├── .env.example        # Template for environment variables
├── requirements.txt    # Project dependencies
├── .gitignore          # Rules to exclude local data from VCS
└── README.md           # Project documentation
Usage
Ensure your Android device (or emulator) has ADB debugging enabled and is connected:

python automator.py
The engine will automatically initialize the driver, load the task inventory from your local data source, and begin the interaction cycle.
Disclaimer
This framework is intended strictly for QA automation, UI/UX research, and internal application testing. The developer is not responsible for any misuse of this tool.