"""Read the tables written by build_tables.py."""
import csv
import io
import os


def table(derived, name):
    with open(os.path.join(derived, name + ".csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path, columns, rows):
    """Write the whole CSV in one call: many small writes were too slow on a mounted
    Windows folder (handoff 006)."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=columns, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())


def num(x):
    return float(x) if x not in ("", None) else None
