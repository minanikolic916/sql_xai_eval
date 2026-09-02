from __future__ import annotations
import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env", override=False)

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


ANNOTATIONS_DIR = PROJECT_ROOT / "annotations"
ANNOTATIONS_DIR.mkdir(parents=True, exist_ok=True)

DATASET_PATH = DATA_DIR / "demo_dataset.json"


RESULTS_GLOB = "results_*.json"


def results_path(timestamp: str, output_dir: Path = OUTPUT_DIR) -> Path:
    return Path(output_dir) / f"results_{timestamp}.json"


def results_paths(output_dir: Path = OUTPUT_DIR) -> list[Path]:
    return sorted(Path(output_dir).glob(RESULTS_GLOB))


def latest_results_path(output_dir: Path = OUTPUT_DIR) -> Path:
    paths = results_paths(output_dir)
    if not paths:
        raise FileNotFoundError(f"no {RESULTS_GLOB} found in {output_dir} — "
                                "run `python -m sqleval.pipeline` first")
    return paths[-1]

GRADER_MODEL = os.getenv("GRADER_MODEL")
GRADER_PROVIDER = os.getenv("GRADER_PROVIDER")
DEFAULT_MODEL = "gpt-5.6"
DEFAULT_PROVIDER = "openai"
MAX_CONCURRENCY = int(os.getenv("GRADER_MAX_CONCURRENCY", "1"))

_temperature = os.getenv("GRADER_TEMPERATURE")
GRADER_TEMPERATURE = float(_temperature) if _temperature not in (None, "") else None
