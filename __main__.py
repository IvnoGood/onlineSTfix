import csv
from pick import pick
from colorama import init, Fore, Back, Style
import os
import sys
import time
from supabase import create_client, Client, PostgrestAPIError
from dotenv import load_dotenv

from modules.fileDowload import download_file_selenium
from modules.extract_rar import extract_rar
from modules.applyFix import copy_fix
from modules.preferences import load_preferences, save_preferences
from modules.logs_manager import add_log

from modules.SteamPath import preferences_SteamPath


def load_games(option, index):
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    supabase: Client = create_client(url, key)

    if index == 0:
        try:
            response = (
                supabase.table("games")
                .select("*")
                .like("title", f"{option}%")
                .execute()
            )
            # print("\n".join([str(data) for data in sorted(response.data, key=lambda x: x["title"].lower())]))
            add_log(
                f"Found {len(response.data)+1} entries for {option}", printable=False)
            return sorted(
                response.data, key=lambda x: x["title"].lower())
        except PostgrestAPIError as e:
            add_log(f"Couldn't fetch data from database: {e.message}")
            add_log(
                f"Couldn't fetch data from database: {e}. Params: {option}/{index}", printable=False)
    elif index == 1:
        try:
            response = (
                supabase.table("games")
                .select("*")
                .text_search(
                    "tag",
                    f'"{option}"',
                    options={"config": "english"},
                )
                .execute()
            )
            # print("\n".join([str(data) for data in sorted(response.data, key=lambda x: x["title"].lower())]))
            add_log(
                f"Found {len(response.data)+1} entries for {option}", printable=False)
            return sorted(response.data, key=lambda x: x["title"].lower())

        except PostgrestAPIError as e:
            add_log(f"Couldn't fetch data from database: {e.message}")
            add_log(
                f"Couldn't fetch data from database: {e}. Params: {option}/{index}", printable=False)
    else:
        print("Not valid opt")
        return


def show_search_filters():
    title = "Choose a way to search your game"
    choices = ["By letter", "By type/tag", "Return"]
    option, index = pick(choices, title, indicator="→",  # quit_keys=('q', 'esc')
                         )

    if index == 0:
        letter_title = "Chose the starting letter of your game"
        letter_choices = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                          'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        option = pick(letter_choices, letter_title, indicator="→",  # quit_keys=('q', 'esc')
                      )
        data = load_games(option[0].upper(), index)
        show_list_games(data)

    if index == 1:
        tag_title = "Chose the filter of your game"
        tag_choices = ['adventures', 'arcade', 'fighting', 'horror', 'officialservers', 'puzzles',
                       'racing', 'rpg', 'sandbox', 'shooter', 'simulator', 'strategy', 'survival', 'vr']
        option = pick(tag_choices, tag_title, indicator="→",  # quit_keys=('q', 'esc')
                      )
        data = load_games(option[0], index)
        show_list_games(data)
    if index == 2:
        main()


def show_list_games(gamelist):
    gamePickTitle = "Choose a game to play"
    introChoices = [
        f"{game["title"]}" for game in gamelist]
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
    game = [game for game in gamelist if game["title"] == option][0]
    title = f"{game["title"]}\n{game["tag"]}\n{game["link"]}\n"
    choices = ["Exit"]
    if not game["fixLink"] == "None":
        choices.append("Download & Apply fix")
    else:
        title += "No fix available at momment"

    option, index = pick(choices, title, indicator="→",  # quit_keys=('q', 'esc')
                         )
    if option == "Download & Apply fix":
        print(Back.YELLOW + "WARNING! A browser window will apear. Don't touch it and let it work" + Style.RESET_ALL)
        add_log(f"Downlaoding game: {game["title"]} \n")
        path = download_file_selenium(
            game["link"], game["fixLink"], game["title"])
        if path:
            apply_fix(game["title"], path)
        else:
            add_log("Fix was not downloaded correctly")
            print("waiting 2sec for you to aknowledge this message")
            time.sleep(2)
            main()
    if option == "Exit":
        show_search_filters()


def apply_fix(gameTitle, path):
    add_log(f"Using {path} game as fix")
    extract_path = extract_rar(path, gameTitle)
    # TODO: change to regular path
    if extract_path:
        copy_fix(extract_path, gameTitle,
                 f"{user_preferences["steamPath"]}/steamapps/common/")


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
    add_log("--- Starting program ---", printable=False, init=True)

    load_dotenv()

    if "users_prefs.json" not in os.listdir():
        add_log("No configuration file found initializing with empty one")
        save_preferences()
        index = 2
        first = True
    else:
        introChoices = ["Game list",
                        "Apply downloaded fix", "Preferences", "Exit"]
        option, index = pick(introChoices, introTitle, indicator="→")

    global user_preferences
    user_preferences = load_preferences()

    if index == 0:
        show_search_filters()
    if index == 1:
        if not os.path.isdir(f"{"downloads"}"):
            if not os.path.isfile(f"{"downloads"}/latest.txt"):
                add_log(
                    "Did not found latest.txt so no previously downloaded files", printable=False)
                main()
            add_log(
                "Did not found latest.txt so no previously downloaded files", printable=False)
            main()

        with open(f"{"downloads"}/latest.txt", "r", encoding="utf-8") as log:
            # ['downloads/TogetherMoonEscape_Fix_Repair_Steam_Generic.rar', 'Together Moon Escape по сети ']
            try:
                lines = log.readlines()
                if len(lines) != 0:
                    add_log(
                        f"Using previusoly downloaded file: {lines[-1]}", printable=False)
                    lastDownload = lines[-1].strip("\n").split(" | ")
                    apply_fix(lastDownload[1], lastDownload[0])
                else:
                    main()
            except IndexError:
                add_log(
                    "failed to fetch from latest.txt delete the file in the downloads folder and try again")
                sys.exit()

    if index == 2:

        preferences_choices = [
            f"Steam Installation Path: {user_preferences["steamPath"]}",
            "Return"
        ]
        if not first:
            preferences_title = "Choose any item to change it's value"
        else:
            preferences_title = "Welcome to the program choose your preferences to start \nChoose any item to change it's value"

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
