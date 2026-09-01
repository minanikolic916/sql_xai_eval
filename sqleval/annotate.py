
from __future__ import annotations
import argparse
import json
from pathlib import Path

from sqleval import config
from sqleval.pipeline import read_run

CAUSE_VALUES = ["same", "partial", "different"]

def seed(results_path: Path | None = None,
         dataset_path: Path = config.DATASET_PATH) -> Path:
    if results_path is None:
        results_path = config.latest_results_path()
    doc = read_run(results_path)
    run_id = doc["run_meta"]["run_id"]

    out_path = config.ANNOTATIONS_DIR / f"reasons_{run_id}.json"
    if out_path.exists():
        raise SystemExit(f"{out_path} already exists — refusing to overwrite annotations")

    with open(dataset_path) as f:
        dataset = json.load(f)
    context = {sub["submission_id"]: (q, sub)
               for schema in dataset["schemas"]
               for q in schema["questions"]
               for sub in q["submissions"]}

    entries = []
    for row in doc["results"]:
        question, submission = context[row["submission_id"]]
        entries.append({
            "submission_id": row["submission_id"],
            "question_id": question["question_id"],
            "nl_question": question["nl_question"],
            "gold_query": question["gold_query"],
            "submission_query": submission["submission_query"],
            "human_reason": row["human_reason"],
            "llm_reason": row["llm_reason"],
            "cause": None,
        })

    with open(out_path, "w") as f:
        json.dump({"run_id": run_id,
                   "dataset_version": doc["run_meta"]["dataset_version"],
                   "cause_values": CAUSE_VALUES,
                   "annotations": entries}, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return out_path


def _find_run(run_id: str, output_dir: Path) -> Path:
    for path in config.results_paths(output_dir):
        if read_run(path)["run_meta"]["run_id"] == run_id:
            return path
    raise SystemExit(f"no run in {output_dir} with run_id {run_id}")


def compare(annotation_path: Path | None = None,
            output_dir: Path = config.OUTPUT_DIR) -> dict:
    if annotation_path is None:
        paths = sorted(config.ANNOTATIONS_DIR.glob("reasons_*.json"))
        if not paths:
            raise SystemExit(f"no reasons_*.json in {config.ANNOTATIONS_DIR} — "
                             "run `python -m sqleval.annotate seed` first")
        annotation_path = paths[-1]
    with open(annotation_path) as f:
        document = json.load(f)

    rows = {row["submission_id"]: row
            for row in read_run(_find_run(document["run_id"], output_dir))["results"]}
    table = {"agreed": dict.fromkeys(CAUSE_VALUES, 0),
             "differed": dict.fromkeys(CAUSE_VALUES, 0)}
    blank, invalid = [], []
    for entry in document["annotations"]:
        cause, submission_id = entry["cause"], entry["submission_id"]
        if cause is None:
            blank.append(submission_id)
        elif cause not in CAUSE_VALUES:
            invalid.append(f"{submission_id}={cause!r}")
        else:
            side = "agreed" if rows[submission_id]["label_match"] else "differed"
            table[side][cause] += 1

    return {"run_id": document["run_id"], "n_total": len(document["annotations"]),
            "table": table, "blank": blank, "invalid": invalid}

def render_comparison(summary: dict) -> str:
    table = summary["table"]
    agreed = sum(table["agreed"].values())
    annotated = agreed + sum(table["differed"].values())
    width = max(len(value) for value in CAUSE_VALUES) + 3
    header = "label".ljust(16) + "".join(v.rjust(width) for v in CAUSE_VALUES)

    lines = [f"reason cause vs label agreement — run {summary['run_id']}",
             f"annotated {annotated}/{summary['n_total']}", "", header, "-" * len(header)]
    for side in ("agreed", "differed"):
        lines.append(side.ljust(16)
                     + "".join(str(table[side][v]).rjust(width) for v in CAUSE_VALUES))

    wrong = table["agreed"]["partial"] + table["agreed"]["different"]
    lines += ["", f"right label, wrong reason: {wrong} of {agreed} correctly labelled"]
    if summary["blank"]:
        lines.append(f"still blank: {', '.join(summary['blank'])}")
    if summary["invalid"]:
        lines.append(f"unrecognised cause values (ignored): {', '.join(summary['invalid'])}")
    return "\n".join(lines)

def main() -> None:
    parser = argparse.ArgumentParser(description="Hand-judge the grader's reasons.")
    sub = parser.add_subparsers(dest="command", required=True)
    seed_parser = sub.add_parser("seed", help="create a blank annotation file")
    seed_parser.add_argument("results_path", nargs="?", default=None,
                             help="run to annotate (default: the most recent)")
    report_parser = sub.add_parser("report", help="cross annotations with label agreement")
    report_parser.add_argument("annotation_path", nargs="?", default=None,
                               help="annotation file (default: the most recent)")
    args = parser.parse_args()

    if args.command == "seed":
        path = seed(Path(args.results_path) if args.results_path else None)
        entries = json.loads(path.read_text())["annotations"]
        print(f"wrote {path}\n{len(entries)} entries to fill in "
              f"(cause: {' | '.join(CAUSE_VALUES)})")
    else:
        print(render_comparison(compare(
            Path(args.annotation_path) if args.annotation_path else None)))

if __name__ == "__main__":
    main()
