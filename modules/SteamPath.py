import os
import pick


def preferences_SteamPath(main, save_preferences):

    while True:
        print("type exit whenever you want to save without changes")
        steamPath = input(
            "Please enter your full SteamLibrary folder path: ")

        if steamPath == "exit":
            main()

        if not os.path.isdir(steamPath):
            print("Path specified is not a folder")
            continue

        if "steam.dll" in os.listdir(steamPath):
            save_preferences({
                "steamPath": steamPath
            })
            print("Your preference was successfully saved")
            main()
        else:
            print(
                r"No valid steam folder found try again. Clue: normal SteamLibrary path is: C:\Program Files (x86)\Steam\steamapps\common")
