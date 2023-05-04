from Pyrus_client import Pyrus
from datetime import datetime
from pathlib import Path
from loguru import logger


def main():
    url = Path("creds.txt")
    pyrus_client = Pyrus(url)
    pyrus_client.save_files(1203495)


if __name__ == "__main__":
    main()