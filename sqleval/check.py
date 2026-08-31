
from __future__ import annotations
import argparse
import json

from sqleval import config
from sqleval.grader import PROMPT, build_grader
from sqleval.pipeline import flatten


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission_id", nargs="?", default=None,
                        help="which submission to grade (default: the first one)")
    parser.add_argument("--prompt", action="store_true",
                        help="print the prompt for this submission and exit, without calling the model")
    args = parser.parse_args()

    with open(config.DATASET_PATH) as f:
        dataset = json.load(f)
    records = flatten(dataset)
    if args.submission_id:
        records = [r for r in records if r["submission_id"] == args.submission_id]
        if not records:
            raise SystemExit(f"submission_id '{args.submission_id}' not found in dataset")
    record = records[0]

    if args.prompt:
        for message in PROMPT.format_messages(**record["grader_input"]):
            print(f"=============== {message.type.upper()} ===============")
            print(message.content, "\n")
        return

    model = dataset.get("grader_model", config.GRADER_MODEL)
    provider = dataset.get("grader_provider", config.GRADER_PROVIDER)
    verdict = build_grader(model=model, provider=provider).invoke(record["grader_input"])

    print(f"{record['submission_id']} graded by {model} ({provider})\n")
    print(f"llm   : {verdict.label}\n        {verdict.reason}\n")
    print(f"human : {record['human_label']}\n        {record['human_reason']}\n")
    print(f"match : {verdict.label == record['human_label']}")


if __name__ == "__main__":
    main()
