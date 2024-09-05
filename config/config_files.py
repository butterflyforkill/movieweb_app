import os
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
@dataclass(frozen=True)
class APIkeys:
    APIkey: str = os.getenv('apiKey')
    