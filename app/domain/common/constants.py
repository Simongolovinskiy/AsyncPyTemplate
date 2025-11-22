from pathlib import Path

MAX_RETRIES = 3
MIN_POOL_SIZE = 10
MAX_POOL_SIZE = 45



MIGRATIONS_DIR = str(Path(__file__).parent.parent.parent.parent / "migrations")
