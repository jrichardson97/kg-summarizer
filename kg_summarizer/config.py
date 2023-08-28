from pathlib import Path
from dotenv import dotenv_values

PROJ_DIR = Path(__file__).parents[1]
CACHE_DIR = PROJ_DIR / 'cache'
CACHE_DIR.mkdir(parents=True, exist_ok=True)
ENV = dotenv_values(PROJ_DIR / '.env')