#!/usr/bin/env python3
"""
2->1 entanglement-assisted RAC posterior visualizer.

Alice holds two uniformly random classical bits x0,x1.
She and Bob share |Phi+>. Alice uses the standard CHSH/RAC encoding:

    s = x0 XOR x1
    Alice measures A_s and gets outcome alpha in {0,1}
    m = x0 XOR alpha

Bob chooses y in {0,1}:
    y=0 -> measure B
    y=1 -> measure B'
    outcome beta in {0,1}
    guess g = m XOR beta

The four planar Bloch-sphere angles A, A', B, B' are configurable below.

For |Phi+> and measurements in one Bloch great circle,

    E(theta_A, theta_B) = cos(theta_A - theta_B)

and

    P(alpha,beta | theta_A,theta_B)
      = 1/4 * [1 + (-1)^(alpha XOR beta) E].

The script computes the exact Bayesian posterior over Alice's four possible
strings after Bob knows:
    * his selected setting y,
    * Alice's communication bit m,
    * his own measurement outcome beta.

No Monte-Carlo sampling is used.

Standard Tsirelson-optimal Bloch angles:
    A  =   0 deg
    A' =  90 deg
    B  =  45 deg
    B' = -45 deg
"""

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# USER SETTINGS
# ============================================================

ALICE_A_DEG = 0.0
ALICE_APRIME_DEG = 90.0
BOB_B_DEG = -0.0
BOB_BPRIME_DEG = 90.0

# Condition the posterior on this observed transcript.
OBSERVED_MESSAGE = 0
OBSERVED_BOB_OUTCOME = 0

SAVE_FIGURE = True
SHOW_FIGURE = True
OUTPUT_FILE = "rac_n2_posteriors.png"

FIGSIZE = (11.0, 4.8)
BAR_ALPHA = 0.9
SHOW_BAR_LABELS = True


# ============================================================
# PHYSICS / RAC MODEL
# ============================================================

STRINGS = [(0, 0), (0, 1), (1, 0), (1, 1)]
STRING_LABELS = ["00", "01", "10", "11"]


def deg2rad(angle_deg):
    return math.radians(angle_deg)


def phi_plus_correlation(theta_a, theta_b):
    """Correlation E=<(-1)^alpha (-1)^beta> for |Phi+> in one Bloch plane."""
    return math.cos(theta_a - theta_b)


def joint_outcome_probability(alpha, beta, theta_a, theta_b):
    """P(alpha,beta | theta_a,theta_b) for |Phi+> with unbiased marginals."""
    e = phi_plus_correlation(theta_a, theta_b)
    parity_sign = 1.0 if (alpha ^ beta) == 0 else -1.0
    p = 0.25 * (1.0 + parity_sign * e)
    return float(np.clip(p, 0.0, 1.0))


def alice_angle_for_string(x0, x1):
    """Alice uses A if x0 XOR x1=0, and A' if x0 XOR x1=1."""
    s = x0 ^ x1
    return deg2rad(ALICE_A_DEG if s == 0 else ALICE_APRIME_DEG)


def bob_angle(y):
    """Bob uses B for y=0 and B' for y=1."""
    return deg2rad(BOB_B_DEG if y == 0 else BOB_BPRIME_DEG)


def transcript_likelihood(x0, x1, y, message, beta):
    """
    Likelihood P(m=message, beta | x0,x1,y).

    Since m = x0 XOR alpha, alpha = x0 XOR m.
    """
    alpha = x0 ^ message
    theta_a = alice_angle_for_string(x0, x1)
    theta_b = bob_angle(y)
    return joint_outcome_probability(alpha, beta, theta_a, theta_b)


def posterior_over_strings(y, message, beta):
    """Exact posterior P(x0,x1 | y,m,beta), for a uniform prior."""
    prior = 0.25
    weights = np.array(
        [
            prior * transcript_likelihood(x0, x1, y, message, beta)
            for x0, x1 in STRINGS
        ],
        dtype=float,
    )
    evidence = weights.sum()
    if evidence <= 1e-15:
        raise ValueError(
            "The selected transcript has zero probability for the chosen angles."
        )
    return weights / evidence


def shannon_entropy(probabilities):
    h = 0.0
    for p in probabilities:
        if p > 0.0:
            h -= float(p) * math.log2(float(p))
    return h


def bit_posterior_stats(posterior):
    """
    For each bit return:
      P(bit=0), P(bit=1), best-guess probability, advantage c=2P-1.
    """
    stats = []
    for bit_index in (0, 1):
        p0 = sum(
            posterior[k]
            for k, bits in enumerate(STRINGS)
            if bits[bit_index] == 0
        )
        p1 = 1.0 - p0
        p_correct = max(p0, p1)
        advantage = 2.0 * p_correct - 1.0
        stats.append((p0, p1, p_correct, advantage))
    return stats


def rac_guess(message, beta):
    return message ^ beta


def selected_bit_success_probability(y):
    """Average RAC success probability for Bob setting y."""
    success = 0.0
    for x0, x1 in STRINGS:
        prior = 0.25
        theta_a = alice_angle_for_string(x0, x1)
        theta_b = bob_angle(y)
        target = x0 if y == 0 else x1

        for alpha in (0, 1):
            message = x0 ^ alpha
            for beta in (0, 1):
                p_ab = joint_outcome_probability(alpha, beta, theta_a, theta_b)
                guess = rac_guess(message, beta)
                if guess == target:
                    success += prior * p_ab
    return success


# ============================================================
# PLOT
# ============================================================

def make_plot():
    post_b = posterior_over_strings(
        y=0,
        message=OBSERVED_MESSAGE,
        beta=OBSERVED_BOB_OUTCOME,
    )
    post_bp = posterior_over_strings(
        y=1,
        message=OBSERVED_MESSAGE,
        beta=OBSERVED_BOB_OUTCOME,
    )

    posts = [post_b, post_bp]
    titles = ["Bob selects B  (index 1)", "Bob selects B'  (index 2)"]

    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE, sharey=True)
    x = np.arange(len(STRINGS))

    for y, (ax, posterior, title) in enumerate(zip(axes, posts, titles)):
        bars = ax.bar(x, posterior, alpha=BAR_ALPHA)

        ax.set_xticks(x, STRING_LABELS)
        ax.set_ylim(0.0, 1.0)
        ax.set_xlabel("Alice's bit string")
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.25)

        if y == 0:
            ax.set_ylabel("Posterior probability")

        if SHOW_BAR_LABELS:
            for bar, p in zip(bars, posterior):
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    bar.get_height() + 0.018,
                    f"{100*p:.1f}%",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

        h = shannon_entropy(posterior)
        stats = bit_posterior_stats(posterior)
        selected = stats[y]
        other = stats[1 - y]
        avg_success = selected_bit_success_probability(y)

        info = (
            f"Observed: m={OBSERVED_MESSAGE}, beta={OBSERVED_BOB_OUTCOME}\n"
            f"Posterior entropy: {h:.3f} bits\n"
            f"Selected bit: {100*selected[2]:.1f}%  (c={selected[3]:.3f})\n"
            f"Other bit: {100*other[2]:.1f}%  (c={other[3]:.3f})\n"
            f"Protocol avg. selected-bit success: {100*avg_success:.1f}%"
        )
        ax.text(
            0.03,
            0.96,
            info,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=9.5,
            bbox=dict(boxstyle="round,pad=0.45", facecolor="white", alpha=0.88),
        )

    angle_text = (
        f"A={ALICE_A_DEG:g}°,  A'={ALICE_APRIME_DEG:g}°,  "
        f"B={BOB_B_DEG:g}°,  B'={BOB_BPRIME_DEG:g}°"
    )
    fig.suptitle(
        "2→1 entanglement-assisted RAC: Bob's posterior over Alice's strings\n"
        + angle_text,
        fontsize=14,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.90))

    if SAVE_FIGURE:
        out = Path(OUTPUT_FILE)
        fig.savefig(out, dpi=200, bbox_inches="tight")
        print(f"Saved figure to: {out.resolve()}")

    print("\nConfigured Bloch angles:")
    print(f"  A  = {ALICE_A_DEG:8.3f} deg")
    print(f"  A' = {ALICE_APRIME_DEG:8.3f} deg")
    print(f"  B  = {BOB_B_DEG:8.3f} deg")
    print(f"  B' = {BOB_BPRIME_DEG:8.3f} deg")
    print(
        f"\nConditioning on transcript: "
        f"m={OBSERVED_MESSAGE}, beta={OBSERVED_BOB_OUTCOME}"
    )

    for y, posterior in enumerate(posts):
        setting_name = "B" if y == 0 else "B'"
        stats = bit_posterior_stats(posterior)
        print(f"\nBob setting {setting_name}:")
        print(
            "  posterior = "
            + ", ".join(
                f"P({label})={p:.6f}"
                for label, p in zip(STRING_LABELS, posterior)
            )
        )
        print(f"  H(string | transcript) = {shannon_entropy(posterior):.6f} bits")
        for i, (_, _, p_corr, adv) in enumerate(stats):
            print(
                f"  bit {i+1}: best guess={p_corr:.6f}, "
                f"advantage={adv:.6f}"
            )
        print(
            f"  average RAC success for selected bit = "
            f"{selected_bit_success_probability(y):.6f}"
        )

    if SHOW_FIGURE:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    make_plot()
