import ast
import sys
from pathlib import Path

APPLY = "--apply" in sys.argv
DIRS = [Path("backend/app"), Path("backend/rasa_taysir/actions")]


def is_print(n):
    return (
        isinstance(n, ast.Expr)
        and isinstance(n.value, ast.Call)
        and isinstance(n.value.func, ast.Name)
        and n.value.func.id == "print"
    )


def process(path):
    src = path.read_text(encoding="utf-8")
    lines = src.splitlines(keepends=True)
    tree = ast.parse(src)
    delete, to_pass = [], []

    for node in ast.walk(tree):
        for field in ("body", "orelse", "finalbody"):
            stmts = getattr(node, field, None)
            if not isinstance(stmts, list) or not stmts:
                continue
            if not all(isinstance(s, ast.stmt) for s in stmts):
                continue
            prints = [s for s in stmts if is_print(s)]
            if not prints:
                continue
            if len(prints) == len(stmts):
                to_pass.append(prints[0])
                delete += prints[1:]
            else:
                delete += prints

    if not delete and not to_pass:
        return 0

    edits = [(s.lineno - 1, s.end_lineno, None) for s in delete]
    edits += [(s.lineno - 1, s.end_lineno, " " * s.col_offset + "pass\n") for s in to_pass]
    for start, end, repl in sorted(edits, reverse=True):
        lines[start:end] = [repl] if repl else []

    print(f"{path}: {len(edits)} print() retiré(s)")
    if APPLY:
        path.write_text("".join(lines), encoding="utf-8")
    return len(edits)


total = 0
for d in DIRS:
    for f in d.rglob("*.py"):
        total += process(f)
print(f"\nTotal : {total} ({'appliqué' if APPLY else 'simulation, rien modifié'})")