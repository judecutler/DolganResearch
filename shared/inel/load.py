"""Read the tables written by build_tables.py."""
import csv
import os


def table(derived, name):
    with open(os.path.join(derived, name + ".csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path, columns, rows):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def num(x):
    return float(x) if x not in ("", None) else None
