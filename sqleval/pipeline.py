from __future__ import annotations
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from sqleval import config, metrics
from sqleval.grader import GraderInput, Verdict, build_grader


def render_schema(schema: dict) -> str:
    """The schema description and its PK/FK constraints as one block."""
    parts = []
    if schema.get("name"):
        parts.append(f"Database: {schema['name']}")
    parts.append(schema["schema_description"])
    if schema.get("constraints"):
        parts.append("Constraints:\n" + schema["constraints"])
    return "\n\n".join(parts)


def flatten(dataset: dict) -> list[dict]:
    """One record per submission, each carrying its own grader input."""
    records = []
    for schema in dataset["schemas"]:
        schema_text = render_schema(schema)
        for q in schema["questions"]:
            for sub in q["submissions"]:
                grader_input: GraderInput = {
                    "schema_ddl": schema_text,
                    "nl_question": q["nl_question"],
                    "gold_sql": q["gold_query"],
                    "submission_sql": sub["submission_query"],
                }
                records.append({
                    "schema_id": schema["schema_id"],
                    "question_id": q["question_id"],
                    "submission_id": sub["submission_id"],
                    "human_label": sub["human_label"],
                    "human_reason": sub["human_reason"],
                    "grader_input": grader_input,
                })
    return records


# A results file is one self-contained run: the stamp under "run_meta", the
# agreement analysis under "metrics", one entry per submission under "results".
def write_run(path: Path, stamp: dict, rows: list[dict], run_metrics: dict) -> Path:
    with open(path, "w") as f:
        json.dump({"run_meta": stamp, "metrics": run_metrics, "results": rows},
                  f, indent=2, ensure_ascii=False)
        f.write("\n")
    return Path(path)


def read_run(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def _unique_path(path: Path) -> Path:
    """Never overwrite a run that started in the same second.

    The suffix uses "_" rather than "-" so the disambiguated name still sorts
    after the plain one, keeping filename order equal to run order.
    """
    candidate, n = path, 2
    while candidate.exists():
        candidate = path.with_name(f"{path.stem}_{n}{path.suffix}")
        n += 1
    return candidate


def run(dataset_path: Path = config.DATASET_PATH,
        grader=None,
        max_concurrency: int = config.MAX_CONCURRENCY,
        temperature: float | None = config.GRADER_TEMPERATURE,
        output_dir: Path = config.OUTPUT_DIR) -> Path:
    with open(dataset_path) as f:
        dataset = json.load(f)
    model = dataset.get("grader_model", config.GRADER_MODEL)
    provider = dataset.get("grader_provider", config.GRADER_PROVIDER)

    # Claim the file and stamp the run before spending anything, so the id and
    # the file it lives in always agree.
    started_at = datetime.now(timezone.utc)
    path = _unique_path(config.results_path(started_at.strftime("%Y%m%dT%H%M%SZ"),
                                            output_dir))
    tag = path.stem.removeprefix("results_")
    run_id = f"{tag}-{re.sub(r'[^A-Za-z0-9.]+', '-', model).strip('-').lower()}"

    records = flatten(dataset)
    if grader is None:
        grader = build_grader(model=model, provider=provider, temperature=temperature)
    verdicts: list[Verdict] = grader.batch([r["grader_input"] for r in records],
                                           config={"max_concurrency": max_concurrency})

    rows = [{
        # Repeated on every row so a row stays attributable on its own, even
        # lifted out of the file or concatenated with another run.
        "run_id": run_id,
        "schema_id": r["schema_id"],
        "question_id": r["question_id"],
        "submission_id": r["submission_id"],
        "human_label": r["human_label"],
        "human_reason": r["human_reason"],
        "llm_model": model,
        "llm_label": v.label,
        "llm_reason": v.reason,
        "label_match": r["human_label"] == v.label,
    } for r, v in zip(records, verdicts)]

    stamp = {
        "run_id": run_id,
        "started_at": started_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "finished_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "model": model,
        "provider": provider,
        # None means the provider default was used, not that it was zero.
        "temperature": temperature,
        "dataset_version": dataset.get("dataset_version"),
    }
    return write_run(path, stamp, rows, metrics.summarize(rows, dataset["label_values"]))


def main() -> None:
    out = run()
    summary = read_run(out)["metrics"]
    print(f"wrote {out}\n")
    print(metrics.render_matrix(summary["confusion_matrix"], summary["labels"]))
    print(f"\naccuracy {summary['accuracy']:.0%} ({summary['n_agreed']}/{summary['n']})")


if __name__ == "__main__":
    main()
