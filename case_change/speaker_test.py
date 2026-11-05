"""A speaker-level test for a birth-year trend in a binary outcome.

Each speaker contributes one point: the empirical logit of their share of
"successes" (for B2: accusative objects), weighted by their token count. The
statistic is the weighted slope of that logit on birth year. Its p-value comes
from permuting birth years across speakers, so the speaker, not the token, is the
unit of inference (CLAUDE.md rule 8). Stdlib only.
"""
import math
import random


def empirical_logit(k, n):
    return math.log((k + 0.5) / (n - k + 0.5))


def weighted_slope(xs, ys, ws):
    sw = sum(ws)
    mx = sum(w * x for w, x in zip(ws, xs)) / sw
    my = sum(w * y for w, y in zip(ws, ys)) / sw
    sxx = sum(w * (x - mx) ** 2 for w, x in zip(ws, xs))
    if sxx == 0:
        return 0.0
    return sum(w * (x - mx) * (y - my) for w, x, y in zip(ws, xs, ys)) / sxx


def trend_test(speakers, n_perm=999, rng=None):
    """speakers: list of (birth_year, successes, n). Returns (slope per decade, two-sided p)."""
    rng = rng or random.Random(0)
    xs = [b / 10 for b, _, _ in speakers]
    ys = [empirical_logit(k, n) for _, k, n in speakers]
    ws = [n for _, _, n in speakers]
    obs = weighted_slope(xs, ys, ws)
    perm = xs[:]
    hits = 0
    for _ in range(n_perm):
        rng.shuffle(perm)
        if abs(weighted_slope(perm, ys, ws)) >= abs(obs) - 1e-12:
            hits += 1
    return obs, (hits + 1) / (n_perm + 1)


def simulate(design, base_share, slope_per_decade, sd_speaker, rng):
    """One simulated data set with the real design: design is a list of (birth_year, n)."""
    mean_b = sum(b for b, _ in design) / len(design)
    base = math.log(base_share / (1 - base_share))
    out = []
    for b, n in design:
        eta = base + slope_per_decade * (b - mean_b) / 10 + rng.gauss(0, sd_speaker)
        p = 1 / (1 + math.exp(-eta))
        out.append((b, sum(rng.random() < p for _ in range(n)), n))
    return out


def power(design, base_share, slope_per_decade, sd_speaker, n_sim=200, n_perm=199, alpha=0.05, seed=1):
    rng = random.Random(seed)
    sig = 0
    for _ in range(n_sim):
        data = simulate(design, base_share, slope_per_decade, sd_speaker, rng)
        if trend_test(data, n_perm, rng)[1] < alpha:
            sig += 1
    return sig / n_sim
