import subprocess
import os
import shutil


def extract_rar(rar_path, gameTitle, extract_path="downloads/fixes", password="online-fix.me"):
    path = f"{extract_path}/{gameTitle}"
    if not os.path.isdir(path):
        os.makedirs(path)
    else:
        print("Game already unzipped")
        shutil.rmtree(path)
        return

    unrar_path = r"modules/UnRAR.exe"

    try:
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
            print(f"✓ Successfully extracted to {path}")
            return path
        else:
            print(f"Error: {result.stderr}")
            print(f"Return code: {result.returncode}")
            return False

    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    extract_rar("TogetherMoonEscape_Fix_Repair_Steam_Generic",
                ["Together Moon Escape по сети"])
