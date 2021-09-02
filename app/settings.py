from pathlib import Path
import os

from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
IMG_FORMAT = "jpeg"
COMICS_TIME = "11:00"
SCHEDULE_TIME = "08:00"
SQLALCHEMY_URL = os.getenv("SQLALCHEMY_URL")
