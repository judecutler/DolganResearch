"""Speaker-clustered tests for a time trend in a binary outcome, with or without controls.

The model is a linear probability model at the token level,
    y = a + b * time + (genre, source, ... dummies) + error,
with errors clustered by speaker, so the speaker, not the token, is the unit of
inference (CLAUDE.md rule 8). `time` is birth year (apparent time) or recording
year (real time), in decades. The statistic is the t-value of b with a
cluster-robust standard error. The p-value comes from a wild cluster bootstrap
with the null b = 0 imposed (Cameron, Gelbach and Miller 2008) and Webb's
six-point weights, which hold up with few clusters (Webb 2014). Stdlib only.

Because time is constant within a speaker and the controls are categorical, every
quantity depends only on cells: (speaker, time, control pattern, successes, n).
With no controls and one cell per speaker this is the object-weighted regression
of each speaker's share on time.

Why not permute birth years (the first version, D-028): in the real design the
speakers with few objects, whose shares are noisiest, are all born last. Permuting
birth years moves them to the middle of the range, so the permutation distribution
is too narrow. The false-positive rate was about 0.09 (handoff 003) and up to 0.15
in simulations of a similar design (D-034). Tried and rejected on the same
simulations: weighting every speaker equally (up to 0.11 with 6 speakers), and an
HC2 leverage correction (no change).
"""
import math
import random

WEBB = (-math.sqrt(1.5), -1.0, -math.sqrt(0.5), math.sqrt(0.5), 1.0, math.sqrt(1.5))


def _solve(a, b):
    """Solve a x = b for a small square matrix (Gauss-Jordan, partial pivoting). None if singular."""
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-10:
            return None
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c]:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def _wls(rows, k_of):
    """Least squares on cells. rows: (cluster, design row, n). k_of: cell index -> successes.

    Returns (coefficients, fitted share per cell), or None if the design is singular.
    """
    p = len(rows[0][1])
    xtx = [[sum(n * x[i] * x[j] for _, x, n in rows) for j in range(p)] for i in range(p)]
    xty = [sum(x[i] * k_of[c] for c, (_, x, _) in enumerate(rows)) for i in range(p)]
    beta = _solve(xtx, xty)
    if beta is None:
        return None
    return beta, [sum(bi * xi for bi, xi in zip(beta, x)) for _, x, _ in rows], xtx


def _t_first(rows, ks):
    """Coefficient on column 1 (time) and its t-value with a cluster-robust (CR0) SE.

    The CR1 small-sample factor is left out: it is the same for the observed data and
    every bootstrap draw, so it does not change the bootstrap p-value.
    """
    fit = _wls(rows, ks)
    if fit is None:
        return None
    beta, fitted, xtx = fit
    p = len(beta)
    # The time coefficient's row of (X'X)^-1, and the score X_g'e_g summed per cluster.
    e1 = [1.0 if i == 1 else 0.0 for i in range(p)]
    row1 = _solve(xtx, e1)
    score = {}
    for (g, x, n), k, f in zip(rows, ks, fitted):
        s = score.setdefault(g, [0.0] * p)
        resid = k - n * f
        for i in range(p):
            s[i] += x[i] * resid
    var = sum(sum(r * s_i for r, s_i in zip(row1, s)) ** 2 for s in score.values())
    return beta[1], (beta[1] / math.sqrt(var) if var > 0 else 0.0)


def _redundant(cols, ws, j, kept):
    """True if column j is (nearly) a weighted linear combination of the kept columns."""
    gram = [[sum(w * cols[a][r] * cols[b][r] for r, w in enumerate(ws)) for b in kept] for a in kept]
    rhs = [sum(w * cols[a][r] * cols[j][r] for r, w in enumerate(ws)) for a in kept]
    beta = _solve(gram, rhs)
    if beta is None:
        return True
    resid = sum(w * (cols[j][r] - sum(b * cols[a][r] for b, a in zip(beta, kept))) ** 2 for r, w in enumerate(ws))
    total = sum(w * cols[j][r] ** 2 for r, w in enumerate(ws))
    return resid <= 1e-9 * max(total, 1e-12)


def design_rows(cells, controls=True, scale=10):
    """cells: list of (cluster, time_in_years, control_labels, successes, n).

    Builds an intercept, time in decades, and one dummy per control level after the
    first level of each control. A dummy that adds nothing beyond the intercept and the
    dummies already kept (for example the source "published_folklore" when genre "flk"
    picks out the same objects) is dropped, so the fit stays solvable. Dummies are never
    pruned against time: a control that duplicates time must make time unidentifiable,
    not silently disappear (review, 2026-11-06).

    Returns (rows, time_identified).
    """
    width = len(cells[0][2]) if controls else 0
    levels = [sorted({c[2][j] for c in cells}) for j in range(width)]
    cols = [[1.0] * len(cells), [t / scale for _, t, *_ in cells]]
    for j in range(width):
        cols += [[1.0 if c[2][j] == lv else 0.0 for c in cells] for lv in levels[j][1:]]
    ws = [c[4] for c in cells]
    kept = [0]
    for j in range(2, len(cols)):
        if not _redundant(cols, ws, j, kept):
            kept.append(j)
    identified = not _redundant(cols, ws, 1, kept)
    order = [0, 1] + kept[1:]
    return [(c[0], [cols[j][r] for j in order], c[4]) for r, c in enumerate(cells)], identified


def adjusted_test(cells, n_boot=999, rng=None, controls=True, scale=10):
    """Wild-cluster-bootstrap test of the time coefficient.

    cells: list of (cluster, time_in_years, control_labels, successes, n); control_labels is a
    tuple such as (genre, source), the same length in every cell.
    Returns (slope, p): the change in share per decade (0.05 = five percentage points) and the
    two-sided p-value, or (None, None) if time cannot be told apart from the controls.
    scale=1 tests any other numeric predictor, such as a 0/1 clause-type indicator.
    """
    rng = rng or random.Random(0)
    rows, identified = design_rows(cells, controls, scale)
    if not identified:
        return None, None
    ks = [c[3] for c in cells]
    obs = _t_first(rows, ks)
    if obs is None:
        return None, None
    slope, t = obs
    null_rows = [(g, x[:1] + x[2:], n) for g, x, n in rows]  # drop time: the null imposed
    null_fit = _wls(null_rows, ks)
    if null_fit is None:
        return None, None
    fitted0 = null_fit[1]
    clusters = sorted({g for g, _, _ in rows})
    hits = 0
    for _ in range(n_boot):
        v = {g: rng.choice(WEBB) for g in clusters}
        kstar = [n * f + v[g] * (k - n * f) for (g, _, n), k, f in zip(rows, ks, fitted0)]
        tb = _t_first(rows, kstar)
        if tb is not None and abs(tb[1]) >= abs(t) - 1e-12:
            hits += 1
    return slope, (hits + 1) / (n_boot + 1)


def trend_test(speakers, n_boot=999, rng=None):
    """speakers: list of (birth_year, successes, n), one cell per speaker. No controls."""
    cells = [(i, b, (), k, n) for i, (b, k, n) in enumerate(speakers)]
    return adjusted_test(cells, n_boot, rng, controls=False)


def collinearity(cells):
    """Share of the object-weighted variance of time explained by the controls (0 to 1).

    Design only: reads no outcome. Near 1 means time and the controls cannot be told apart.
    """
    rows, identified = design_rows(cells)
    if not identified:
        return 1.0
    xs = [(x[1], [x[0]] + x[2:], n) for _, x, n in rows]
    p = len(xs[0][1])
    xtx = [[sum(n * z[i] * z[j] for _, z, n in xs) for j in range(p)] for i in range(p)]
    beta = _solve(xtx, [sum(n * z[i] * t for t, z, n in xs) for i in range(p)])
    if beta is None:
        return None
    sw = sum(n for _, _, n in xs)
    mean = sum(n * t for t, _, n in xs) / sw
    total = sum(n * (t - mean) ** 2 for t, _, n in xs)
    resid = sum(n * (t - sum(b * zi for b, zi in zip(beta, z))) ** 2 for t, z, n in xs)
    return 1 - resid / total if total else None


def simulate(design, base_share, slope_per_decade, sd_speaker, rng):
    """One simulated data set with the real design: design is a list of (birth_year, n).

    The effect is generated on the log-odds scale: slope_per_decade is a log odds ratio.
    """
    mean_b = sum(b for b, _ in design) / len(design)
    base = math.log(base_share / (1 - base_share))
    out = []
    for b, n in design:
        eta = base + slope_per_decade * (b - mean_b) / 10 + rng.gauss(0, sd_speaker)
        p = 1 / (1 + math.exp(-eta))
        out.append((b, sum(rng.random() < p for _ in range(n)), n))
    return out


def simulate_cells(design, base_share, slope_per_decade, sd_speaker, rng, control_effects=None):
    """Like simulate, for cells: design is a list of (speaker, time_in_years, labels, n).

    control_effects maps a label to a log-odds shift (e.g. {"flk": -1.0}), to simulate a
    genre or source effect that is tangled with time.
    """
    mean_t = sum(t * n for _, t, _, n in design) / sum(n for *_, n in design)
    base = math.log(base_share / (1 - base_share))
    shift = {g: rng.gauss(0, sd_speaker) for g in sorted({d[0] for d in design})}  # sorted: same draws under any PYTHONHASHSEED
    out = []
    for g, t, labels, n in design:
        eta = base + slope_per_decade * (t - mean_t) / 10 + shift[g]
        eta += sum((control_effects or {}).get(lv, 0.0) for lv in labels)
        p = 1 / (1 + math.exp(-eta))
        out.append((g, t, labels, sum(rng.random() < p for _ in range(n)), n))
    return out


def power(design, base_share, slope_per_decade, sd_speaker, n_sim=200, n_boot=199, alpha=0.05, seed=1):
    """Power of trend_test for a design of (birth_year, n) per speaker."""
    rng = random.Random(seed)
    sig = 0
    for _ in range(n_sim):
        data = simulate(design, base_share, slope_per_decade, sd_speaker, rng)
        if trend_test(data, n_boot, rng)[1] < alpha:
            sig += 1
    return sig / n_sim


def power_cells(design, base_share, slope_per_decade, sd_speaker, n_sim=200, n_boot=199, alpha=0.05,
                seed=1, controls=True, control_effects=None):
    """Power (or, with slope 0, false-positive rate) of adjusted_test for a cell design."""
    rng = random.Random(seed)
    sig = 0
    for _ in range(n_sim):
        data = simulate_cells(design, base_share, slope_per_decade, sd_speaker, rng, control_effects)
        p = adjusted_test(data, n_boot, rng, controls)[1]
        if p is not None and p < alpha:
            sig += 1
    return sig / n_sim
