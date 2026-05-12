import datetime
import os


def add_log(message, printable=True, showDate=False, init=False):
    if init:
        if "logs" not in os.listdir():
            os.makedirs("logs")

    if printable and showDate:
        print(f"[{datetime.datetime.now()}] {message}")
    elif printable:
        print(f"{message}")
    today = datetime.date.today()
    with open(f"logs/{today}.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {message} \n")
        f.close()


if __name__ == '__main__':
    add_log("Oppened app", printable=False)
