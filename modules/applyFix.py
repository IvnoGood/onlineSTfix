import os
import shutil
from modules.logs_manager import add_log
from difflib import SequenceMatcher
import sys
import time


def copy_fix(fixPath, gameName, steamPath=r"C:\Program Files (x86)\Steam"):
    steam_list = os.listdir(steamPath)

    values = []
    for game in steam_list:
        matcher = SequenceMatcher(None, gameName.lower(), game.lower()).ratio()
        if matcher > 0.3:
            values.append((game, matcher))

    if len(values) == 0:
        add_log(
            f"Didn't find any game folder compatible are you sure you are in the right steam folder ?: [{steamPath}]")
        time.sleep(4)
        return
    steam_game_name = sorted(values, key=lambda x: x[1], reverse=True)[0][0]
    add_log(
        rf"Applying fix at {steamPath}/{steam_game_name}", printable=False)

    response = input(
        f"Gonna apply fix at {steamPath}/{steam_game_name} de you wish to continue (Y/N)?").lower().strip()

    if response == "n":
        add_log("User said no to the install exiting program...")
        print("If not happy with the steam folder change it in the preference menu")
        time.sleep(4)
        sys.exit()

    shutil.copytree(
        fixPath,
        f"{steamPath}/{steam_game_name}",
        dirs_exist_ok=True,
        ignore_dangling_symlinks=True
    )


if __name__ == '__main__':
    copy_fix(r"downloads/fixes/Last Man Sitting Online",
             "ASTRONEER по сети", r"D:\SteamLibrary\steamapps\common")
