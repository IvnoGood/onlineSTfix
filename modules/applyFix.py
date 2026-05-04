import os
import shutil


def copy_fix(fixPath, gameName, steamPath=r"C:\Program Files (x86)\Steam\steamapps\common"):
    steam_game_name = gameName
    print(rf"Applying fix at {steamPath}/steamapps/common/{steam_game_name}")

    shutil.copytree(
        fixPath,
        f"{steamPath}/{steam_game_name}",
        dirs_exist_ok=True,
        ignore_dangling_symlinks=True
    )


if __name__ == '__main__':
    copy_fix("downloads/fixes/Last Man Sitting Online",
             "Last Man Sitting Online")
