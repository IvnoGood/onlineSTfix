from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

from modules.logs_manager import add_log


def download_file_selenium(gameUrl,
                           fixUrl,
                           gameTitle,
                           brave_path=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                           adBlockCRX=r"browser/uBlock-Origin-Lite-Chrome-Web-Store.crx",
                           save_path="downloads"):
    def download_wait(path_to_downloads):
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < 20:
            time.sleep(1)
            dl_wait = False
            for fname in os.listdir(path_to_downloads):
                if fname.endswith('.crdownload'):
                    dl_wait = True
            seconds += 1
        return fname

    starting_files = os.listdir(save_path)

    if (gameUrl == "" or gameUrl == "None") or (fixUrl == "" or fixUrl == "None"):
        add_log(f"Url: {gameUrl}|{fixUrl} not valid", printable=False)
        print("Couldn't download game")
        # return "URL-N-VAL"

    os.makedirs(save_path, exist_ok=True)

    if not os.path.exists(brave_path):
        add_log(f"Brave not found at {brave_path}")
        # return "BRAVE-N-FOUND"

    brave_options = Options()
    brave_options.binary_location = brave_path

    if not os.path.exists(adBlockCRX):
        add_log(f"Adblocker not found at {adBlockCRX}", printable=False)
        print("Couldn't download game try downlaoding the program again")
        # return "ADBLOCK-N-FOUND"
    brave_options.add_extension(adBlockCRX)

    prefs = {
        "download.default_directory": os.path.abspath(save_path),
        "download.prompt_for_download": False,
    }
    brave_options.add_experimental_option("prefs", prefs)
    brave_options.add_argument("--no-sandbox")
    brave_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=brave_options)
        driver.get(gameUrl)
        add_log(f"Brave oppened to link: {gameUrl}", printable=False)
        try:
            driver.find_element(
                By.XPATH, "//*[contains(text(), 'Скачать фикс с сервера')]").click()
        except:
            driver.find_element(
                By.XPATH, "//*[contains(text(), 'Download fix from server')]").click()
        time.sleep(2)
        driver.get(fixUrl)
        download_wait(save_path)
        new_folder = os.listdir(save_path)
        fname = [file for file in new_folder if file not in starting_files]
        if len(fname) == 0:
            add_log(
                f"Downloaded file not found all files: {new_folder}", printable=False)
            print("Download failed try downloading the file again")
            return False
        add_log(f"Found file: {fname}", printable=False)
        fname = fname[0]
        driver.quit()
        add_log(f"✓ Downloaded to {save_path}/{fname}")

        with open(f"{save_path}/latest.txt", "a", encoding="utf-8") as log:
            log.write(f"{save_path}/{fname} | {gameTitle}\n")

        return f"{save_path}/{fname}"

    except Exception as e:
        add_log(f"Error: {e}")
        if 'driver' in locals():
            driver.quit()
            pass
        return False


if __name__ == "__main__":
    fix = "https://uploads.online-fix.me:2053/uploads/Last%20Man%20Sitting/Fix%20Repair/LastManSitting_Fix_Repair_Steam_Generic.rar"
    url = "https://online-fix.me/games/adventures/18067-last-man-sitting-online.html"
    download_file_selenium(url, fix, "Last Man Sitting Online")
