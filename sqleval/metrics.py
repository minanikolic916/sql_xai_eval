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
def render_matrix(matrix: dict[str, dict[str, int]], labels: list[str]) -> str:
    width = max(len(label) for label in labels) + 2
    header = "human \\ llm".ljust(width) + "".join(l.rjust(width) for l in labels)
    lines = [header, "-" * len(header)]
    for human in labels:
        lines.append(human.ljust(width)
                     + "".join(str(matrix[human][llm]).rjust(width) for llm in labels))
    return "\n".join(lines)
