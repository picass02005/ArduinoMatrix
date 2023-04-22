import json
import sys
import time

LOGFILE_PATH = "logs.txt"

with open(LOGFILE_PATH, "w"):
    pass

with open("config.json", "r") as f:
    LOG_MODE = json.loads(f.read())["logMode"]


class Logs:
    @staticmethod
    def info(log):
        if LOG_MODE != "err":
            print(f"[{time.strftime('%d/%m - %H:%M %S')} / INFO] {log}")

    @staticmethod
    def error(log):
        print(f"[{time.strftime('%d/%m - %H:%M %S')} / ERROR] {log}", file=sys.stderr)

        with open(LOGFILE_PATH, "a") as f:
            f.write(f"[{time.strftime('%d/%m - %H:%M %S')} / ERROR] {log}\n")
