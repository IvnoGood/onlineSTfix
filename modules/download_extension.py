import os
import requests

from modules.logs_manager import add_log


def downlaod_extension(url, output):
    if not os.path.isdir(output):
        os.mkdir(output)
        add_log("Extension folder not found creating one", printable=False)

    if os.path.isfile(f"{output}/{url[1]}"):
        return True

    response = requests.get(url[0])

    add_log(f"Downloading: {url[1]}", printable=True)
    # Check if the request was successful
    if response.status_code == 200:
        with open(f"{output}/{url[1]}", "wb") as file:
            file.write(response.content)
        print("Download completed successfully.")
        return True
    else:
        add_log(
            f"Failed to download file. Status code: {response.status_code}")
        return False


if __name__ == "__main__":
    urls = [
        ["https://github.com/IvnoGood/onlineSTfix/raw/refs/heads/main/extensions/uBlock-Origin-Lite-Chrome-Web-Store.crx",
            "uBlock-Origin-Lite-Chrome-Web-Store.crx"],
        ["https://github.com/IvnoGood/onlineSTfix/raw/refs/heads/main/extensions/UnRAR.exe", "UnRAR.exe"]
    ]
    downlaod_extension(urls, "extensions")
