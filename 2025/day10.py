from collections import deque
from functools import lru_cache

import numpy as np
from itertools import combinations, product

filepath = "day10.txt"


def read_file():
    return [line.strip().split(" ") for line in open(filepath)]

def min_presses(target: int, masks, n_lights: int) -> int:
    """
    BFS on light configurations (bitmasks) to find the minimum number
    of button presses to reach `target` from all-off (0).
    """
    start = 0
    if target == 0:
        return 0

    max_state = 1 << n_lights
    dist = [-1] * max_state
    dist[start] = 0

    q = deque([start])

    while q:
        state = q.popleft()
        d = dist[state]

        for mask in masks:
            next_state = state ^ mask
            if dist[next_state] == -1:
                dist[next_state] = d + 1
                if next_state == target:
                    #print(f"Found solution: {dist[next_state]}")
                    return dist[next_state]
                q.append(next_state)

    # If there is somehow no solution
    raise RuntimeError("No solution for this machine")

def solve_part_I():
    lines = read_file()
    print(lines)

    total_presses = 0

    for line in lines:
        buttons = [list(map(int, button[1:-1].split(","))) for button in line[1:-1]]

        lights_bits = ''
        lights_string = line[0][1:-1]
        for sign in lights_string:
            if sign == '#':
                lights_bits += '1'
            else:
                lights_bits += '0'

        lights_int = int(lights_bits[::-1], 2)


        masks = []
        for button in buttons:
            mask = 0
            for num in button:
                mask |= 1 << num
            masks.append(mask)

        print(f"Lights: {lights_string}, reversed bits: {lights_bits[::-1]} as int: {lights_int} and buttons: {buttons} translated to bits: {masks}")

        presses = min_presses(lights_int, masks, len(lights_string))
        total_presses += presses

        print(f"{lights_string} -> target={lights_int}, buttons={masks}, presses={presses}")

    return total_presses

# result_1 = solve_part_I()
# print(result_1)

def build_button_matrix(buttons, m):
    n = len(buttons)
    A = np.zeros((m, n), dtype=int)
    for j, btn in enumerate(buttons):
        for i in btn:
            A[i, j] = 1
    return A


def ranks_consistent(A, b):
    Af = A.astype(float)
    bf = b.astype(float).reshape(-1, 1)
    rA = np.linalg.matrix_rank(Af)
    rAug = np.linalg.matrix_rank(np.hstack([Af, bf]))
    return rA, rAug, (rA == rAug)

def solve_unique_if_possible(A, b, tol=1e-9):
    """
    If A has full column rank (rank == n), then either:
      - no solution, or
      - exactly one solution. If it's integral & nonneg, it's the minimum presses.
    """
    m, n = A.shape
    rA, rAug, ok = ranks_consistent(A, b)
    if not ok:
        return None

    if rA == n:  # full column rank => unique solution (if consistent)
        x, residuals, _, _ = np.linalg.lstsq(A.astype(float), b.astype(float), rcond=None)
        xr = np.rint(x).astype(int)
        if np.max(np.abs(x - xr)) > tol: # solution not ints
            return None
        if np.any(xr < 0): # solution with negatives
            return None
        if not np.array_equal(A @ xr, b):
            return None
        return int(xr.sum()), xr

    return None

def independent_rows(A, tol=1e-9):
    """Greedy: keep rows that increase rank (uses NumPy rank)."""
    rows, r = [], 0
    Af = A.astype(float)
    for i in range(A.shape[0]):
        cand = rows + [i]
        r2 = np.linalg.matrix_rank(Af[cand, :], tol=tol)
        if r2 > r:
            rows, r = cand, r2
    return np.array(rows, dtype=int)

def min_presses_branch_and_bound(A, b, chunk=200_000, tol=1e-8):
    A = np.asarray(A, dtype=int)
    b = np.asarray(b, dtype=int)
    m, n = A.shape

    # Consistency check via ranks (works even if A is singular)
    Af = A.astype(float)
    rA = np.linalg.matrix_rank(Af)
    rAug = np.linalg.matrix_rank(np.hstack([Af, b.reshape(-1, 1).astype(float)]))
    if rA != rAug:
        return None  # no solutions

    # Per-button upper bounds
    ub = np.zeros(n, dtype=int)
    for j in range(n):
        idx = np.where(A[:, j] == 1)[0]
        ub[j] = 0 if idx.size == 0 else int(b[idx].min())

    # Unique-solution fast path (full column rank)
    if rA == n:
        x = np.linalg.solve(Af, b.astype(float))
        xr = np.rint(x).astype(int)
        if np.max(np.abs(x - xr)) <= tol and np.all(xr >= 0) and np.array_equal(A @ xr, b):
            return int(xr.sum()), xr
        return None

    # Reduce to independent rows so we can form square bases
    R = independent_rows(A)
    Ar = A[R, :].astype(float)
    br = b[R].astype(float)
    r = Ar.shape[0]
    d = n - r

    best = None
    best_x = None
    cols = np.arange(n)

    for basic in combinations(cols, r):
        basic = np.array(basic, dtype=int)
        B = Ar[:, basic]
        if np.linalg.matrix_rank(B) < r:
            continue

        free = np.array([j for j in cols if j not in set(basic)], dtype=int)
        Afree = Ar[:, free]

        # ---- super fast case: 1 free variable (your problematic machine) ----
        if d == 1:
            j = free[0]
            t = np.arange(ub[j] + 1, dtype=float)  # all candidates at once
            rhs = br[:, None] - Afree[:, [0]] * t[None, :]  # (r, T)
            Xb = np.linalg.solve(B, rhs)  # (r, T)
            Xbr = np.rint(Xb)
            ok = np.max(np.abs(Xb - Xbr), axis=0) <= tol
            if not np.any(ok):
                continue

            Xbr = Xbr[:, ok].astype(int)
            t_ok = t[ok].astype(int)

            # nonnegativity
            ok2 = np.all(Xbr >= 0, axis=0)
            if not np.any(ok2):
                continue
            Xbr = Xbr[:, ok2]
            t_ok = t_ok[ok2]

            # Build candidate full X and check exactness
            Q = Xbr.shape[1]
            X = np.zeros((n, Q), dtype=int)
            X[basic, :] = Xbr
            X[j, :] = t_ok

            mask = np.all(X >= 0, axis=0) & np.all(X <= ub[:, None], axis=0) & np.all((A @ X) == b[:, None], axis=0)
            if not np.any(mask):
                continue
            X = X[:, mask]
            totals = X.sum(axis=0)
            k = int(np.argmin(totals))
            tot = int(totals[k])
            if best is None or tot < best:
                best, best_x = tot, X[:, k].copy()
            continue

        # ---- general d>1: chunked vectorized enumeration (still non-recursive) ----
        dims = (ub[free] + 1).astype(int)
        P = int(np.prod(dims))
        for start in range(0, P, chunk):
            end = min(P, start + chunk)
            idx = np.arange(start, end, dtype=np.int64)
            grid = np.array(np.unravel_index(idx, dims), dtype=int).T  # (Q, d)

            rhs = br[:, None] - Afree @ grid.T  # (r, Q)
            Xb = np.linalg.solve(B, rhs)
            Xbr = np.rint(Xb)

            ok = np.max(np.abs(Xb - Xbr), axis=0) <= tol
            if not np.any(ok):
                continue

            Xbr = Xbr[:, ok].astype(int)
            grid = grid[ok, :]

            ok2 = np.all(Xbr >= 0, axis=0)
            if not np.any(ok2):
                continue
            Xbr = Xbr[:, ok2]
            grid = grid[ok2, :]

            Q = Xbr.shape[1]
            X = np.zeros((n, Q), dtype=int)
            X[basic, :] = Xbr
            X[free, :] = grid.T

            mask = np.all(X >= 0, axis=0) & np.all(X <= ub[:, None], axis=0) & np.all((A @ X) == b[:, None], axis=0)
            if not np.any(mask):
                continue
            X = X[:, mask]
            totals = X.sum(axis=0)
            k = int(np.argmin(totals))
            tot = int(totals[k])
            if best is None or tot < best:
                best, best_x = tot, X[:, k].copy()

    return best


def min_presses_joltage(target, buttons):
    button_matrix = build_button_matrix(buttons, len(target))

    presses = solve_unique_if_possible(button_matrix, np.array(target))
    if presses is not None:
        print("Solved as unique solution")
        return presses

    return min_presses_branch_and_bound(button_matrix, np.array(target))


def solve_part_II():
    lines = read_file()
    total_presses = 0

    for line in lines:
        print(f"Line: {line}")
        buttons = [list(map(int, button[1:-1].split(","))) for button in line[1:-1]]
        target = list(map(int, line[-1][1:-1].split(",")))

        presses = min_presses_joltage(target, buttons)
        total_presses += presses if isinstance(presses, int) else presses[0]

        print(f"Buttons: {buttons} and target: {target}; presses: {presses}")

    return total_presses





result_2 = solve_part_II()
print(result_2)
