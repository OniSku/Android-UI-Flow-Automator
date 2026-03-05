import uiautomator2 as u2
import pandas as pd
import time
import os
import re
import traceback
from datetime import datetime
from settings import CONFIG


class MobileFlowEngine:
    """
    Advanced engine for automating user journeys and verifying UI metrics
    in Android applications via ADB.
    """

    def __init__(self, inventory_file, auth_file):
        self.inventory_path = inventory_file
        self.auth_path = auth_file
        self.d = None
        self._initialize_driver()

    def log(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def _initialize_driver(self):
        try:
            self.d = u2.connect(CONFIG["SERIAL"])
            self.log("Driver initialized successfully.")
        except Exception as e:
            self.log(f"Driver initialization failed: {e}")

    def _parse_metric(self, raw_str):
        raw_str = raw_str.replace(",", ".")
        match = re.search(r"([\d.]+)\s*([kк]?)", raw_str.lower())
        if match:
            val = float(match.group(1))
            multiplier = 1000 if match.group(2) else 1
            return int(val * multiplier)
        return None

    def fetch_ui_metric(self):
        try:
            elements = self.d.xpath("//*[@text]").all()
            for i, el in enumerate(elements):
                content = el.text.strip().lower()
                if CONFIG["METRIC_MARKER"] in content:
                    if i > 0:
                        metric_text = elements[i - 1].text.strip()
                        return self._parse_metric(metric_text)
            return None
        except:
            return None

    def handle_system_dialogs(self):
        """Handles Android system popups for application selection."""
        target_label = CONFIG["APP_LABEL"]
        if self.d(text=target_label).exists(timeout=2):
            self.d(text=target_label).click()
            time.sleep(1)
            if self.d(text="Always").exists():
                self.d(text="Always").click()
            elif self.d(text="Just once").exists():
                self.d(text="Just once").click()

    def perform_auth(self, username, password):
        d = self.d
        try:
            d.app_start(CONFIG["APP_PKG"])
            time.sleep(5)
            if not d(resourceId=CONFIG["ID_NAV"]).click_exists(timeout=10):
                d(textMatches="(?i)Profile|Профиль").click_exists(timeout=5)

            d(textMatches="(?i).*Login.*|.*Войти.*").click_exists(timeout=5)

            if d(className="android.widget.EditText").wait(timeout=15):
                fields = d(className="android.widget.EditText")
                fields[0].set_text(username)
                d(textMatches="(?i)Continue|Продолжить").click_exists(timeout=5)
                time.sleep(5)

                fields = d(className="android.widget.EditText")
                fields[0].set_text(password)
                d(textMatches="(?i)Submit|Login|Войти").click_exists(timeout=5)
                time.sleep(10)
                return True
        except Exception as e:
            self.log(f"Auth failed: {e}")
        return False

    def process_tasks(self):
        while True:
            try:
                df = pd.read_excel(self.inventory_path)
                active = df[~((df["initial_value"] > 0) &
                              (df["initial_value"] + df["progress"] >= df["target"]))]

                if active.empty:
                    self.log("Tasks completed. Idling...");
                    time.sleep(60);
                    continue

                with open(self.auth_path, "r") as f:
                    accs = [l.strip() for l in f if ":" in l]
                if not accs: break
                user, pwd = accs[0].split(":")

                if self.perform_auth(user, pwd):
                    for idx, task in active.iterrows():
                        url = task["url"]
                        self.d.app_start(CONFIG["BROWSER_PKG"], stop=True)
                        time.sleep(2)
                        self.d(resourceId="com.android.chrome:id/url_bar").set_text(url)
                        self.d.press("enter")
                        time.sleep(10)

                        if task["initial_value"] == 0:
                            current_m = self.fetch_ui_metric()
                            if current_m:
                                df.at[idx, "initial_value"] = current_m
                                df.to_excel(self.inventory_path, index=False)

                        self.d.swipe(0.5, 0.8, 0.5, 0.4)
                        if self.d(textMatches="(?i)Open|Открыть").click_exists(timeout=10):
                            self.handle_system_dialogs()
                            time.sleep(10)

                            btn = self.d(resourceId=CONFIG["ID_ACTION"])
                            if btn.exists():
                                btn.click()
                                time.sleep(5)
                                df.at[idx, "progress"] += 1
                                if (df.at[idx, "initial_value"] + df.at[idx, "progress"]) >= df.at[idx, "target"]:
                                    df = df.drop(idx)
                                df.to_excel(self.inventory_path, index=False)

                with open(self.auth_path, "w") as f:
                    f.writelines("\n".join(accs[1:] + [accs[0]]))
            except Exception as e:
                self.log(f"Runtime Exception: {e}");
                time.sleep(10)


if __name__ == "__main__":
    engine = MobileFlowEngine("inventory.xlsx", "credentials.txt")
    engine.process_tasks()