import csv
from pick import pick
from colorama import init, Fore, Back, Style
import os
import sys

from modules.fileDowload import download_file_selenium
from modules.extract_rar import extract_rar
from modules.applyFix import copy_fix
from modules.preferences import load_preferences, save_preferences

from modules.SteamPath import preferences_SteamPath


def load_games(path):
    data = []
    with open(path, "r", encoding="utf-8") as csvData:
        i = 0
        for lines in csv.reader(csvData):
            if i != 0:
                data.append(lines)
            i += 1
        csvData.close()
    return data


def show_search_filters():

    if not os.path.isdir("database"):
        print("No database found. Read the README")
        return
    else:
        if not os.path.isdir("database/char") and not os.path.isdir("database/filters"):
            print("Not all filters found. Read the README")
            return
    title = "Choose a way to search your game"
    choices = ["By letter", "By type/tag", "Return"]
    option, index = pick(choices, title, indicator="→",  # quit_keys=('q', 'esc')
                         )

    if index == 0:
        letter_title = "Chose the starting letter of your game"
        letter_choices = []
        for file in os.listdir("database/char"):
            if file.endswith(".csv"):
                letter_choices.append(file[:-4])
        option, index = pick(letter_choices, letter_title, indicator="→",  # quit_keys=('q', 'esc')
                             )
        data = load_games(f"database/char/{option+".csv"}")
        show_list_games(data)

    if index == 1:
        tag_title = "Chose the filter of your game"
        tag_choices = []
        for file in os.listdir("database/filters"):
            if file.endswith(".csv"):
                tag_choices.append(file[:-4])
        option, index = pick(tag_choices, tag_title, indicator="→",  # quit_keys=('q', 'esc')
                             )
        data = load_games(f"database/filters/{option+".csv"}")
        show_list_games(data)
    if index == 2:
        main()


def show_list_games(gamelist):
    gamePickTitle = "Choose a game to play"
    introChoices = [
        f"{game[0]}" for game in gamelist]
    introChoices.insert(0, "--- Return to search page ---")
    introChoices.insert(len(introChoices), "--- Return to search page ---")
    option, index = pick(introChoices, gamePickTitle, indicator="→",  # quit_keys=('q', 'esc')
                         )
    if option == "--- Return to search page ---":
        show_search_filters()
    else:
        show_game_details(option, gamelist)
        return option, index


def show_game_details(option, gamelist):
    game = [game for game in gamelist if game[0] == option][0]
    title = f"{game[0]}\n{game[2]}\n{game[1]}\n"
    choices = ["Exit"]
    if not game[3] == "None":
        choices.append("Download & Apply fix")
    else:
        title += "No fix available at momment"

    option, index = pick(choices, title, indicator="→",  # quit_keys=('q', 'esc')
                         )
    if option == "Download & Apply fix":
        print(Back.YELLOW + "WARNING! A browser window will apear. Don't touch it and let it work" + Style.RESET_ALL)
        path = download_file_selenium(game[1], game[3], game[0])
        apply_fix(game[0], path)
    if option == "Exit":
        show_search_filters()


def apply_fix(gameTitle, path):
    print(f"Using {path} game as fix")
    extract_path = extract_rar(path, gameTitle)
    # TODO: change to regular path
    if extract_path:
        copy_fix(extract_path, gameTitle, user_preferences["steamPath"])


def main():
    introTitle = r"""                 _ _             _____ _______ __ _      
                | (_)           / ____|__   __/ _(_)     
    ___  _ __ | |_ _ __   ___| (___    | | | |_ ___  __
    / _ \| '_ \| | | '_ \ / _ \\___ \   | | |  _| \ \/ /
    | (_) | | | | | | | | |  __/____) |  | | | | | |>  < 
    \___/|_| |_|_|_|_| |_|\___|_____/   |_| |_| |_/_/\_\
                                                        
                                                        
        Welcome to OnlineSTfix choose option to continue
        Ctrl+C and then Enter to exit the program"""

    # Initialize program
    init()

    if "users_prefs.json" not in os.listdir():
        print("No configuration file found initializing with empty one")
        save_preferences()
    global user_preferences
    user_preferences = load_preferences()

    introChoices = ["Game list", "Apply downloaded fix", "Preferences", "Exit"]
    option, index = pick(introChoices, introTitle, indicator="→")

    if index == 0:
        show_search_filters()
    if index == 1:
        with open(f"{"downloads"}/latest.txt", "r", encoding="utf-8") as log:
            # ['downloads/TogetherMoonEscape_Fix_Repair_Steam_Generic.rar', 'Together Moon Escape по сети ']
            if len(log.readlines()) != 0:
                lastDownload = log.readlines()[0].strip("\n").split(" | ")
                apply_fix(lastDownload[1], lastDownload[0])
            else:
                main()

    if index == 2:
        preferences_choices = [
            f"Steam Installation Path: {user_preferences["steamPath"]}",
            "Return"
        ]
    preferences_title = "Choose any item to change it's value"

    preferences_option, preferences_index = pick(
        preferences_choices, preferences_title, indicator="→")

    if preferences_index == 0:
        preferences_SteamPath(main, save_preferences)
        user_preferences = load_preferences()
    if preferences_option == "Return":
        main()
    if index == 3:
        sys.exit()


if __name__ == '__main__':
    main()
