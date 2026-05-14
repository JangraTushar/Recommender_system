from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

CHAPTERS_PATH = DATA_DIR / "chapters.csv"
INTERACTIONS_PATH = DATA_DIR / "interactions.csv"

TOP_K = 5
RANDOM_SEED = 42