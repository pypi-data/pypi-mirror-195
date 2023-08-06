import os

from dotenv import load_dotenv

from promptware.dataset import DatasetConfig
from promptware.load import install

load_dotenv()

os_api_key = os.getenv("OS_API_KEY")


__all__ = [
    "DatasetConfig",
    "install",
]
