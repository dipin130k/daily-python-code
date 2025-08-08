#!/usr/bin/env python3
"""
Generates a new Python file each day with a small algorithm or utility.
No external dependencies. Updates daily_code/README.md index.
"""

from __future__ import annotations
import os
import random
from datetime import datetime
from pathlib import Path
import textwrap
import re

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "daily_code"

def today_seed() -> int:
    return int(datetime.utcnow().strftime("%Y%m%d"))

def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", name.lower())

def pick_template(rng: random.Random):
    templates = [
        {
            "name": "fibonacci_iterative",
            "desc": "Compute the first N Fibonacci numbers iteratively.",
            "code": """
                def fibonacci(n: int) -> list[int]:
                    \"\"\"Return the first n Fibonacci numbers (n>=1).\"\"\"
                    if n <= 0:
                        return []
                    if n == 1:
                        return [0]
                    seq = [0, 1]
                    for _ in range(2, n):
                        seq.append(seq[-1] + seq[-2])
                    return seq
                if __name__ == "__main__":
                    N = {N}
                    print(f"Fibonacci first {N}: ", fibonacci(N))
            """,
            "params": lambda r: {"N": r.randint(8, 20)},
        },
        {
            "name": "sieve_of_eratosthenes",
            "desc": "Generate primes up to a limit using the Sieve of Eratosthenes.",
            "code": """
                def primes_up_to(limit: int) -> list[int]:
                    \"\"\"Return all primes <= limit using the sieve.\"\"\"
                    if limit < 2:
                        return []
                    sieve = [True] * (limit + 1)
                    sieve[0] = sieve[1] = False
                    p = 2
                    while p * p <= limit:
                        if sieve[p]:
                            for m in range(p * p, limit + 1, p):
                                sieve[m] = False
                        p += 1
                    return [i for i, is_prime in enumerate(sieve) if is_prime]
                if __name__ == "__main__":
                    LIMIT = {LIMIT}
                    print(f"Primes up to {LIMIT}: ", primes_up_to(LIMIT))
            """,
            "params": lambda r: {"LIMIT": r.randint(50, 200)},
        },
        {
            "name": "merge_sort",
            "desc": "Stable merge sort implementation with type hints.",
            "code": """
                from typing import List, TypeVar
                T = TypeVar('T')

                def merge_sort(arr: List[T]) -> List[T]:
                    if len(arr) <= 1:
                        return arr[:]
                    mid = len(arr) // 2
                    left = merge_sort(arr[:mid])
                    right = merge_sort(arr[mid:])
                    return merge(left, right)

                def merge(left: List[T], right: List[T]) -> List[T]:
                    i = j = 0
                    out: List[T] = []
                    while i < len(left) and j < len(right):
                        if left[i] <= right[j]:
                            out.append(left[i]); i += 1
                        else:
                            out.append(right[j]); j += 1
                    out.extend(left[i:]); out.extend(right[j:])
                    return out

                if __name__ == "__main__":
                    data = {DATA}
                    print("Input:", data)
                    print("Sorted:", merge_sort(data))
            """,
            "params": lambda r: {"DATA": sorted({r.randint(-50, 50) for _ in range(r.randint(8, 14))}) or [0]},
        },
        {
            "name": "levenshtein_distance",
            "desc": "Compute Levenshtein (edit) distance between two strings.",
            "code": """
                def levenshtein(a: str, b: str) -> int:
                    \"\"\"Return edit distance between a and b.\"\"\"
                    if a == b:
                        return 0
                    if not a:
                        return len(b)
                    if not b:
                        return len(a)
                    prev = list(range(len(b) + 1))
                    for i, ca in enumerate(a, 1):
                        curr = [i]
                        for j, cb in enumerate(b, 1):
                            ins = curr[j-1] + 1
                            delete = prev[j] + 1
                            subst = prev[j-1] + (ca != cb)
                            curr.append(min(ins, delete, subst))
                        prev = curr
                    return prev[-1]

                if __name__ == "__main__":
                    A = "{A}"
                    B = "{B}"
                    print(f"levenshtein('{A}','{B}') =", levenshtein(A, B))
            """,
            "params": lambda r: {"A": "".join(r.choice("codecraft") for _ in range(r.randint(4, 7))),
                                "B": "".join(r.choice("workflows") for _ in range(r.randint(4, 7)))},
        },
        {
            "name": "dijkstra_on_grid",
            "desc": "Dijkstra shortest path on a small weighted grid (no deps).",
            "code": """
                import heapq
                from typing import Tuple, List

                def neighbors(r: int, c: int, R: int, C: int):
                    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < R and 0 <= nc < C:
                            yield nr, nc

                def dijkstra(grid: List[List[int]], start=(0,0), goal=None) -> int:
                    R, C = len(grid), len(grid[0])
                    if goal is None: goal = (R-1, C-1)
                    dist = [[float('inf')]*C for _ in range(R)]
                    sr, sc = start
                    dist[sr][sc] = grid[sr][sc]
                    pq: List[Tuple[int,int,int]] = [(grid[sr][sc], sr, sc)]
                    while pq:
                        d, r, c = heapq.heappop(pq)
                        if (r,c) == goal:
                            return d
                        if d != dist[r][c]:
                            continue
                        for nr, nc in neighbors(r,c,R,C):
                            nd = d + grid[nr][nc]
                            if nd < dist[nr][nc]:
                                dist[nr][nc] = nd
                                heapq.heappush(pq, (nd, nr, nc))
                    return -1

                if __name__ == "__main__":
                    grid = {GRID}
                    print("Grid:")
                    for row in grid: print(row)
                    print("Min path cost:", dijkstra(grid))
            """,
            "params": lambda r: {"GRID": [[r.randint(1, 9) for _ in range(r.randint(4, 6))] for __ in range(r.randint(4, 6))]},
        },
    ]
    return rng.choice(templates)

def ensure_index():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / ".gitkeep").touch(exist_ok=True)
    index = OUT_DIR / "README.md"
    if not index.exists():
        index.write_text("# Daily Python Code\n\nAuto-generated snippets, one per day.\n\n", encoding="utf-8")

def update_index(rel_path: Path, title: str, desc: str):
    index = OUT_DIR / "README.md"
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    line = f"- {now}: [{title}]({rel_path.as_posix()}) — {desc}\n"
    with index.open("a", encoding="utf-8") as f:
        f.write(line)

def main():
    rng = random.Random(today_seed())
    ensure_index()

    t = pick_template(rng)
    params = t["params"](rng)

    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    year_dir = OUT_DIR / datetime.utcnow().strftime("%Y")
    year_dir.mkdir(parents=True, exist_ok=True)

    base_name = f"{date_str}_{slugify(t['name'])}.py"
    out_path = year_dir / base_name

    counter = 2
    while out_path.exists():
        out_path = year_dir / f"{date_str}_{slugify(t['name'])}_v{counter}.py"
        counter += 1

    header = f'''"""
Title: {t["name"].replace("_"," ").title()}
Date: {date_str}
Description: {t["desc"]}
This file was auto-generated by scripts/generate_daily_code.py
"""
'''
    body = textwrap.dedent(t["code"]).format(**params).lstrip("\n")
    out_path.write_text(header + body, encoding="utf-8")

    rel = out_path.relative_to(ROOT)
    update_index(rel, t["name"], t["desc"])
    print(f"Wrote {rel}")

if __name__ == "__main__":
    main()
