from __future__ import annotations

def confusion_matrix(rows: list[dict], labels: list[str]) -> dict[str, dict[str, int]]:
    matrix = {human: {llm: 0 for llm in labels} for human in labels}
    for row in rows:
        human, llm = row.get("human_label"), row.get("llm_label")
        if human in matrix and llm in matrix[human]:
            matrix[human][llm] += 1
    return matrix

def summarize(rows: list[dict], labels: list[str]) -> dict:
    matrix = confusion_matrix(rows, labels)
    counted = sum(sum(row.values()) for row in matrix.values())
    agreed = sum(matrix[label][label] for label in labels)
    return {
        "n": counted,
        "n_off_label": len(rows) - counted,
        "n_agreed": agreed,
        "accuracy": round(agreed / counted, 4) if counted else None,
        "labels": labels,
        "confusion_matrix": matrix,
    }
def per_label(matrix: dict[str, dict[str, int]], labels: list[str]) -> dict[str, dict]:
    scores = {}
    for label in labels:
        hits = matrix[label][label]
        support = sum(matrix[label].values())
        predicted = sum(matrix[human][label] for human in labels)
        precision = hits / predicted if predicted else None
        recall = hits / support if support else None
        if precision is None or recall is None:
            f1 = None
        elif precision + recall:
            f1 = 2 * precision * recall / (precision + recall)
        else:
            f1 = 0.0
        scores[label] = {"precision": precision, "recall": recall, "f1": f1,
                         "support": support, "predicted": predicted}
    return scores


def cohen_kappa(matrix: dict[str, dict[str, int]], labels: list[str]) -> float | None:
    n = sum(sum(row.values()) for row in matrix.values())
    if not n:
        return None
    observed = sum(matrix[label][label] for label in labels) / n
    expected = sum(sum(matrix[label].values())
                   * sum(matrix[human][label] for human in labels)
                   for label in labels) / n ** 2
    return None if expected == 1 else round((observed - expected) / (1 - expected), 4)


def score(summary: dict) -> dict:
    matrix, labels = summary["confusion_matrix"], summary["labels"]
    scores = per_label(matrix, labels)
    rated = [s for s in scores.values() if s["f1"] is not None]
    return {"per_label": scores,
            "macro_f1": round(sum(s["f1"] for s in rated) / len(rated), 4) if rated else None,
            "cohen_kappa": cohen_kappa(matrix, labels)}


def render_scores(summary: dict) -> str:
    derived = score(summary)
    width = max(len(label) for label in summary["labels"]) + 2
    columns = ("precision", "recall", "f1", "support")
    header = "label".ljust(width) + "".join(c.rjust(11) for c in columns)

    counts = lambda key: ", ".join(f"{label} {derived['per_label'][label][key]}"
                                   for label in summary["labels"])
    lines = [f"labelled by human: {counts('support')}",
             f"labelled by llm:   {counts('predicted')}", "",
             header, "-" * len(header)]
    for label in summary["labels"]:
        row = derived["per_label"][label]
        lines.append(label.ljust(width)
                     + "".join(("—" if row[c] is None else
                                f"{row[c]:.0%}" if c != "support" else str(row[c])).rjust(11)
                               for c in columns))
    macro, kappa = derived["macro_f1"], derived["cohen_kappa"]
    lines += ["", f"macro F1 {'—' if macro is None else f'{macro:.0%}'}"
                  f"    Cohen's κ {'—' if kappa is None else f'{kappa:.3f}'}"]
    return "\n".join(lines)


def render_matrix(matrix: dict[str, dict[str, int]], labels: list[str]) -> str:
    width = max(len(label) for label in labels) + 2
    header = "human \\ llm".ljust(width) + "".join(l.rjust(width) for l in labels)
    lines = [header, "-" * len(header)]
    for human in labels:
        lines.append(human.ljust(width)
                     + "".join(str(matrix[human][llm]).rjust(width) for llm in labels))
    return "\n".join(lines)


def main() -> None:
    import argparse
    from pathlib import Path
    from sqleval import config
    from sqleval.pipeline import read_run

    parser = argparse.ArgumentParser(description="Score a stored run.")
    parser.add_argument("results_path", nargs="?", default=None,
                        help="run to score (default: the most recent)")
    args = parser.parse_args()
    path = Path(args.results_path) if args.results_path else config.latest_results_path()

    document = read_run(path)
    summary = document["metrics"]
    print(f"{document['run_meta']['run_id']} — {path.name}\n")
    print(render_matrix(summary["confusion_matrix"], summary["labels"]), "\n")
    print(render_scores(summary))
    print(f"\naccuracy {summary['accuracy']:.0%} "
          f"({summary['n_agreed']}/{summary['n']})")


if __name__ == "__main__":
    main()
