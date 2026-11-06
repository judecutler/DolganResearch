"""A speaker-level test for a birth-year trend in a binary outcome.

Each speaker contributes their share of "successes" (for B2: accusative objects),
weighted by their object count. The statistic is the t-value of the slope of that
share on birth year, with a cluster-robust standard error, so the speaker, not the
token, is the unit of inference (CLAUDE.md rule 8). The p-value comes from a wild
cluster bootstrap with the null imposed (Cameron, Gelbach and Miller 2008) and
Webb's six-point weights, which hold up with few clusters (Webb 2014). Stdlib only.

Why not permute birth years (the first version, D-028): in the real design the
speakers with few objects, whose shares are noisiest, are all born last. Permuting
birth years moves them to the middle of the range, so the permutation distribution
is too narrow. The false-positive rate was about 0.09 (handoff 003) and up to 0.15
in simulations of a similar design. The wild bootstrap keeps each speaker's birth
year and object count fixed and only rescales their residual (D-034).

Tried and rejected, on the same simulations: weighting every speaker equally
(false-positive rate up to 0.07 with 25 speakers and 0.11 with 6), and an HC2
leverage correction (no change).
"""
import math
import random

WEBB = (-math.sqrt(1.5), -1.0, -math.sqrt(0.5), math.sqrt(0.5), 1.0, math.sqrt(1.5))


def _fit(xs, ys, ws):
    """Weighted least-squares slope of ys on xs, and its t-value with a cluster-robust SE.

    The small-sample factor of CR1 is left out: it is the same for the observed data
    and every bootstrap draw, so it does not change the bootstrap p-value.
    """
    sw = sum(ws)
    mx = sum(w * x for w, x in zip(ws, xs)) / sw
    my = sum(w * y for w, y in zip(ws, ys)) / sw
    sxx = sum(w * (x - mx) ** 2 for w, x in zip(ws, xs))
    if sxx == 0:
        return 0.0, 0.0
    b = sum(w * (x - mx) * (y - my) for w, x, y in zip(ws, xs, ys)) / sxx
    meat = sum((w * (x - mx) * (y - my - b * (x - mx))) ** 2 for w, x, y in zip(ws, xs, ys))
    return b, (b / math.sqrt(meat / sxx ** 2) if meat > 0 else 0.0)


def trend_test(speakers, n_boot=999, rng=None):
    """speakers: list of (birth_year, successes, n).

    Returns (slope, p): the change in share per decade of birth year (0.05 = five
    percentage points), and the two-sided wild-cluster-bootstrap p-value.
    """
    rng = rng or random.Random(0)
    xs = [b / 10 for b, _, _ in speakers]
    ys = [k / n for _, k, n in speakers]
    ws = [n for _, _, n in speakers]
    slope, t = _fit(xs, ys, ws)
    mean = sum(w * y for w, y in zip(ws, ys)) / sum(ws)  # the fit under the null: no slope
    hits = 0
    for _ in range(n_boot):
        ystar = [mean + rng.choice(WEBB) * (y - mean) for y in ys]
        if abs(_fit(xs, ystar, ws)[1]) >= abs(t) - 1e-12:
            hits += 1
    return slope, (hits + 1) / (n_boot + 1)


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


def power(design, base_share, slope_per_decade, sd_speaker, n_sim=200, n_boot=199, alpha=0.05, seed=1):
    rng = random.Random(seed)
    sig = 0
    for _ in range(n_sim):
        data = simulate(design, base_share, slope_per_decade, sd_speaker, rng)
        if trend_test(data, n_boot, rng)[1] < alpha:
            sig += 1
    return sig / n_sim
