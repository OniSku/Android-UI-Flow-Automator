import os
from dotenv import load_dotenv

load_dotenv()

# Centralized configuration loader for the automation engine
CONFIG = {
    "SERIAL": os.getenv("ADB_SERIAL", "127.0.0.1:5555"),
    "APP_PKG": os.getenv("TARGET_PACKAGE", "com.example.app"),
    "BROWSER_PKG": os.getenv("BROWSER_PACKAGE", "com.android.chrome"),

    # UI Elements
    "ID_NAV": os.getenv("UI_NAV_PROFILE_ID", ""),
    "ID_ACTION": os.getenv("UI_ACTION_BUTTON_ID", ""),
    "ID_EXIT": os.getenv("UI_LOGOUT_BUTTON_ID", ""),

    # Metadata
    "METRIC_MARKER": os.getenv("METRIC_KEYWORD", "followers"),
    "APP_LABEL": os.getenv("APP_LABEL", "TargetApp")
}