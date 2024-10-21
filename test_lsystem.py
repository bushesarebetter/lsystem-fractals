import random

import numpy as np
import pytest

from lsystem import PRESETS, rewrite, turtle


@pytest.mark.parametrize("n", range(6))
def test_koch_length(n):
    # axiom "F--F--F" has 3 F's and 4 turns; each F -> "F+F--F+F" adds 3 F's and 4 turns,
    # so F count is 3*4^n and length works out to 7*4^n
    p = PRESETS["Koch snowflake"]
    s = rewrite(p["axiom"], p["rules"], n)
    assert s.count("F") == 3 * 4**n
    assert len(s) == 7 * 4**n


@pytest.mark.parametrize("n", range(13))
def test_dragon_segments(n):
    p = PRESETS["Dragon curve"]
    segments = turtle(rewrite(p["axiom"], p["rules"], n), p["angle"])
    assert len(segments) == 2**n


def test_koch_closes():
    p = PRESETS["Koch snowflake"]
    segments = turtle(rewrite(p["axiom"], p["rules"], 3), p["angle"])
    assert np.allclose(segments[-1][1], segments[0][0])


def test_brackets_restore_state():
    segments = turtle("F[+F]F", 90)
    assert np.allclose(segments[2], [[1, 0], [2, 0]])


def test_stochastic_rules_vary_with_seed():
    p = PRESETS["Stochastic plant"]
    a = rewrite(p["axiom"], p["rules"], 4, random.Random(1))
    b = rewrite(p["axiom"], p["rules"], 4, random.Random(2))
    assert a != b
    assert a == rewrite(p["axiom"], p["rules"], 4, random.Random(1))
