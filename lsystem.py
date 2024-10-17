import argparse
import math
import random

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# A rule maps a symbol to a replacement string, or to a list of (weight, replacement)
# pairs for stochastic rules. Symbols without a rule are copied unchanged.
PRESETS = {
    "Koch snowflake": dict(axiom="F--F--F", rules={"F": "F+F--F+F"}, angle=60, n=4, cmap="winter"),
    "Sierpinski triangle": dict(axiom="F-G-G", rules={"F": "F-G+F+G-F", "G": "GG"}, angle=120, n=6, heading=180, cmap="cool"),
    "Dragon curve": dict(axiom="FX", rules={"X": "X+YF+", "Y": "-FX-Y"}, angle=90, n=12, cmap="plasma"),
    "Hilbert curve": dict(axiom="A", rules={"A": "+BF-AFA-FB+", "B": "-AF+BFB+FA-"}, angle=90, n=5, cmap="viridis"),
    "Fractal plant": dict(axiom="X", rules={"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}, angle=25, n=6, heading=65, cmap="summer"),
    "Stochastic plant": dict(
        axiom="X",
        rules={
            "X": [(1, "F+[[X]-X]-F[-FX]+X"), (1, "F-[[X]+X]+F[+FX]-X"), (1, "F[+X]F[-X]+X")],
            "F": "FF",
        },
        angle=22.5, n=6, heading=90, cmap="summer",
    ),
}


def rewrite(axiom, rules, n, rng=None):
    rng = rng or random.Random(0)
    s = axiom
    for _ in range(n):
        out = []
        for ch in s:
            rule = rules.get(ch, ch)
            if isinstance(rule, list):
                weights, options = zip(*rule)
                rule = rng.choices(options, weights)[0]
            out.append(rule)
        s = "".join(out)
    return s


def turtle(s, angle, heading=0.0, draw="FG"):
    # F and G both move forward drawing a line; Sierpinski needs two kinds of edge
    x, y, a = 0.0, 0.0, heading
    stack, segments = [], []
    for ch in s:
        if ch in draw:
            nx, ny = x + math.cos(math.radians(a)), y + math.sin(math.radians(a))
            segments.append(((x, y), (nx, ny)))
            x, y = nx, ny
        elif ch == "+":
            a += angle
        elif ch == "-":
            a -= angle
        elif ch == "[":
            stack.append((x, y, a))
        elif ch == "]":
            x, y, a = stack.pop()
    return np.array(segments)


def draw(ax, segments, cmap):
    lc = LineCollection(segments, array=np.arange(len(segments)), cmap=cmap, linewidths=0.8)
    ax.add_collection(lc)
    ax.autoscale()
    ax.set_aspect("equal")
    ax.axis("off")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="gallery.png")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    fig, axes = plt.subplots(2, 3, figsize=(13, 9))
    for ax, (name, p) in zip(axes.flat, PRESETS.items()):
        s = rewrite(p["axiom"], p["rules"], p["n"], rng)
        segments = turtle(s, p["angle"], p.get("heading", 0.0))
        draw(ax, segments, p["cmap"])
        ax.set_title(f"{name} (n={p['n']}, {len(segments)} segments)", fontsize=10)
        print(f"{name:<20} n={p['n']:<3} {len(s):>7} chars {len(segments):>6} segments")
    fig.tight_layout()
    fig.savefig(args.out, dpi=130)
    print(f"saved {args.out}")


if __name__ == "__main__":
    main()
