import os
import subprocess
import sys

def build():
    print("Building XMRiGUI v1.8.0 for Windows...")

    # Try to install PyInstaller if not present
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # PyInstaller Command using 'python -m PyInstaller' for better reliability on Windows
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--add-data", "xmrigui.png;.",
        "--collect-all", "gi",
        "--icon", os.path.join("windows", "xmrigui.ico"),
        "--name", "XMRiGUI",
        "xmrigui.py"
    ]

    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)

    print("\nBuild Complete! Check the 'dist' folder for XMRiGUI.exe")

if __name__ == "__main__":
    build()
