import subprocess
import os
import shutil
from modules.logs_manager import add_log


def extract_rar(rar_path, gameTitle, extract_path="downloads/fixes", password="online-fix.me"):
    path = f"{extract_path}/{gameTitle}"
    if not os.path.isdir(path):
        os.makedirs(path)
    else:
        add_log(f"Game {gameTitle} was already unzipped")
        shutil.rmtree(path)
        return path

    unrar_path = r"modules/UnRAR.exe"

    try:
        with open(f"{path}/Patched using OnlineSTfix Website in the file.txt", "w") as f:
            f.write("https://github.com/IvnoGood/onlineSTfix.txt")
            f.close()

        cmd = [
            unrar_path,
            "x",
            "-p" + password,
            "-y",
            rar_path,
            path
        ]

        result = subprocess.run(
            cmd, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            add_log(f"✓ Successfully extracted to {path}")
            return path
        else:
            error = result.stderr.split("\n")
            add_log(
                f"Error: {" ".join([line for line in error if line != ""])}", printable=False)
            add_log(
                f"Return code: {result.returncode}", printable=False)
            return False

    except Exception as e:
        add_log("Error while unzipping: "+e)
        return False


if __name__ == "__main__":
    extract_rar("./TogetherMoonEscape_Fix_Repair_Steam_Generic.rar",
                "Together Moon Escape по сети")
