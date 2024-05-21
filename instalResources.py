import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def upgrade_pip():
    print("Upgrading pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

def install_dependencies():
    packages = [
        'pyinstaller',
        'argparse',
        'pyyaml',
        'xmltodict',
        'PyQt5'
    ]

    for package in packages:
        print(f"Installing {package}...")
        install(package)

    print("Installed packages:")
    subprocess.check_call([sys.executable, "-m", "pip", "list"])

if __name__ == "__main__":
    upgrade_pip()
    install_dependencies()
