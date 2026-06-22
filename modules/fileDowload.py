from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import platform
import zipfile

try:
    from modules.logs_manager import add_log
    from modules.download_extension import downlaod_extension
except ModuleNotFoundError:
    from logs_manager import add_log
    from download_extension import downlaod_extension


def download_file_selenium(gameUrl,
                           fixUrl,
                           gameTitle,
                           brave_path=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                           adBlockCRX=r"extensions/uBlock-Origin-Lite-Chrome-Web-Store.crx",
                           save_path="downloads"):
    def download_wait(path_to_downloads):
        seconds = 0
        dl_wait = True
        while dl_wait:
            time.sleep(1)
            dl_wait = False
            for fname in os.listdir(path_to_downloads):
                if fname.endswith('.crdownload'):
                    dl_wait = True
            seconds += 1
        return fname

    def get_chrome_driver_manual():
        """Manually detect OS and load correct driver"""

        system = platform.system()

        if system == "Windows":
            driver_path = "./extensions/drivers/chromedriver_win32.zip"
        elif system == "Darwin":  # macOS
            arch = platform.machine()
            if arch == "arm64":  # M1/M2 Mac
                driver_path = "./extensions/drivers/chromedriver_mac_arm64.zip"
            else:  # Intel Mac
                driver_path = "./extensions/drivers/chromedriver_mac64.zip"
        elif system == "Linux":
            driver_path = "./extensions/drivers/chromedriver_linux64.zip"
        else:
            raise Exception(f"Unsupported OS: {system}")

        if not os.path.exists(driver_path):
            raise FileNotFoundError(f"ChromeDriver not found at {driver_path}")

        driver_folder = "./extensions/drivers/"
        with zipfile.ZipFile(driver_path, 'r') as zip_ref:
            zip_ref.extractall(driver_folder)

        for file in os.listdir(driver_folder):
            if file.startswith("chromedriver"):
                return f"./extensions/drivers/{os.path.relpath(file)}"

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    starting_files = os.listdir(save_path)

    if (gameUrl == "" or gameUrl == "None") or (fixUrl == "" or fixUrl == "None"):
        add_log(f"Url: {gameUrl}|{fixUrl} not valid", printable=False)
        print("Couldn't download game")
        return False

    os.makedirs(save_path, exist_ok=True)

    if not os.path.exists(brave_path):
        add_log(f"Brave not found at {brave_path}")
        return False

    if not downlaod_extension(["https://github.com/IvnoGood/onlineSTfix/raw/refs/heads/main/extensions/uBlock-Origin-Lite-Chrome-Web-Store.crx",
                               "uBlock-Origin-Lite-Chrome-Web-Store.crx"], "extensions"):
        return False

    if not os.path.exists(adBlockCRX):
        add_log(f"Adblocker not found at {adBlockCRX}", printable=False)
        print("Couldn't download game try downlaoding the program again")
        return False

    # driver_loc = get_chrome_driver_manual()
    print("Starting browser session.... (1/4)")

    brave_options = Options()
    # brave_options.binary_location = brave_path
    brave_options.add_extension(adBlockCRX)

    prefs = {
        "download.default_directory": os.path.abspath(save_path),
        "download.prompt_for_download": False,
    }
    brave_options.add_experimental_option("prefs", prefs)
    brave_options.add_argument("--no-sandbox")
    brave_options.add_argument("--disable-dev-shm-usage")

    """ brave_options.add_argument("--headless")
    brave_options.add_argument("--headless=new") """

    driver = webdriver.Chrome(options=brave_options)

    """ firefox_options = Options()
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference(
        "browser.download.manager.showWhenStarting", False)
    firefox_options.set_preference("browser.download.dir",
                                   os.path.abspath(save_path))

    firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                   "application/x-rar-compressed,application/octet-stream")
    firefox_options.set_preference(
        "browser.download.manager.alertOnExit", False)

    driver = webdriver.Firefox(options=firefox_options)
    driver.install_addon(
        r"./extensions/ublock_origin-1.71.0.xpi", temporary=True) """

    try:
        driver.get(gameUrl)
        print("Opening the website.... (2/4)")
        add_log(f"Brave oppened to link: {gameUrl}", printable=False)
        driver.execute_script("window.scrollBy(0, 1500);")
        try:
            driver.find_element(
                By.XPATH, "//*[contains(text(), 'Скачать фикс с сервера')]").click()
        except:
            driver.find_element(
                By.XPATH, "//*[contains(text(), 'Download fix from server')]").click()
        print("Grabing the fix.... (3/4)")
        time.sleep(2)
        driver.get(fixUrl)
        print("Downloading the fix.... (4/4)")

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
        add_log(f"Saved {gameTitle} ! \n")

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
