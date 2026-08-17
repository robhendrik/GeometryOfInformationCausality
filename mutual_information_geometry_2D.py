"""
Figure — n=2 mutual-information boundary in RAC advantage space
================================================================

Plots the mutual-information form of the one-bit Information Causality bound

    sum_i I_i <= 1,

using RAC advantage coordinates

    c_i = 2 P_i - 1

and, for uniformly random input bits with a symmetric binary guessing channel,

    I_i = 1 - h2((1 + c_i)/2).

For n=2 the mutual-information boundary is

    [1 - h2((1+c1)/2)] + [1 - h2((1+c2)/2)] = 1.

The full sign-symmetric body is plotted. For comparison, the script also
overlays the quantum unit circle c1^2+c2^2=1 and the classical diamond
|c1|+|c2|=1.

The symmetric (1,1) direction is shown only in the positive quadrant.
The classical-majority, quantum, and mutual-information symmetric points
are labelled directly with arrows.

Dependencies
------------
pip install numpy scipy matplotlib
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq


# =============================================================================
# OUTPUT / LAYOUT
# =============================================================================

OUTPUT = Path(__file__).with_name("Figure_MI_n2.png")

FIGURE_SIZE_INCH = (15.36, 10.24)
DPI = 200

LEFT_IMAGE_BOX = [0.055, 0.13, 0.60, 0.72]
RIGHT_LEGEND_BOX = [0.69, 0.36, 0.27, 0.32]


# =============================================================================
# APPEARANCE
# =============================================================================

# Palette taken from the supplied reference image:
# warm yellow/gold outer region, muted blue-grey classical body,
# coral majority marker, ochre quantum marker, grey diagonal.

MI_FILL_COLOR = "#F7D77A"
MI_FILL_ALPHA = 0.34
MI_EDGE_COLOR = "#C89A14"
MI_EDGE_WIDTH = 2.2

QUANTUM_COLOR = "#F2B632"
QUANTUM_WIDTH = 2.4

CLASSICAL_FILL_COLOR = "#AFC3CF"
CLASSICAL_FILL_ALPHA = 0.30
CLASSICAL_COLOR = "#AAB8B5"
CLASSICAL_WIDTH = 2.0
CLASSICAL_LINESTYLE = "-"

MAJORITY_COLOR = "#E95A47"
QUANTUM_POINT_COLOR = "#C69310"
MI_POINT_COLOR = "#222222"

AXIS_COLOR = "#111111"
AXIS_WIDTH = 1.25

DIAGONAL_COLOR = "#8A8A8A"
DIAGONAL_WIDTH = 1.25
DIAGONAL_LINESTYLE = (0, (4, 4))

MARKER_SIZE = 95
MARKER_EDGE_COLOR = "white"
MARKER_EDGE_WIDTH = 0.8

FONT_SIZE = 13
TITLE_SIZE = 22
SUBTITLE_SIZE = 14.5

ARROW_WIDTH = 1.4
ARROW_HEAD_SCALE = 13


# =============================================================================
# INFORMATION THEORY
# =============================================================================

def binary_entropy(p):
    """Binary entropy h2(p), vectorized and numerically safe."""
    p = np.asarray(p, dtype=float)
    out = np.zeros_like(p)

    mask = (p > 0.0) & (p < 1.0)
    q = p[mask]
    out[mask] = -q * np.log2(q) - (1.0 - q) * np.log2(1.0 - q)

    return out


def mutual_information_from_advantage(c):
    """
    Mutual information for a uniform binary variable guessed through a
    symmetric binary channel with RAC advantage c = 2P-1.
    """
    c = np.asarray(c, dtype=float)
    p = 0.5 * (1.0 + c)
    return 1.0 - binary_entropy(p)


def mi_sum(c1, c2):
    """Sum of the two retrieval mutual informations."""
    return (
        mutual_information_from_advantage(c1)
        + mutual_information_from_advantage(c2)
    )


def symmetric_mi_coordinate():
    """Solve 2 * I(c) = 1 for the positive diagonal c1=c2=c."""
    f = lambda c: 2.0 * float(mutual_information_from_advantage(c)) - 1.0
    return brentq(f, 0.0, 1.0)


# =============================================================================
# BOUNDARY CONSTRUCTION
# =============================================================================

def positive_quadrant_mi_boundary(num=1000):
    """
    Construct the mutual-information equality boundary in the first quadrant.

    For each c1 in [0,1], solve

        I(c1) + I(c2) = 1

    for c2 in [0,1].
    """
    c1 = np.linspace(0.0, 1.0, num)
    c2 = np.empty_like(c1)

    for k, x in enumerate(c1):
        remaining = 1.0 - float(mutual_information_from_advantage(x))

        if remaining <= 0.0:
            c2[k] = 0.0
            continue

        f = lambda y: float(mutual_information_from_advantage(y)) - remaining
        c2[k] = brentq(f, 0.0, 1.0)

    return c1, c2


def full_mi_boundary(num=1000):
    """Mirror the first-quadrant boundary into the full sign-symmetric curve."""
    x, y = positive_quadrant_mi_boundary(num=num)

    quadrants = [
        np.column_stack([ x,  y]),
        np.column_stack([-x[::-1],  y[::-1]]),
        np.column_stack([-x, -y]),
        np.column_stack([ x[::-1], -y[::-1]]),
    ]

    return np.vstack(quadrants)


# =============================================================================
# COMPARISON SHAPES
# =============================================================================

def quantum_circle(num=1000):
    theta = np.linspace(0.0, 2.0 * np.pi, num)
    return np.cos(theta), np.sin(theta)


def classical_diamond():
    return np.array([
        [ 1.0,  0.0],
        [ 0.0,  1.0],
        [-1.0,  0.0],
        [ 0.0, -1.0],
        [ 1.0,  0.0],
    ])


# =============================================================================
# ANNOTATIONS
# =============================================================================

def add_point_with_arrow(
    ax,
    point,
    text,
    text_xy,
    color,
    ha="left",
    va="center",
):
    """Draw one symmetric-point marker and an arrow-labelled annotation."""
    x, y = point

    ax.scatter(
        [x], [y],
        s=MARKER_SIZE,
        c=[color],
        edgecolors=MARKER_EDGE_COLOR,
        linewidths=MARKER_EDGE_WIDTH,
        zorder=8,
    )

    ax.annotate(
        text,
        xy=(x, y),
        xytext=text_xy,
        fontsize=12.5,
        color=color,
        ha=ha,
        va=va,
        arrowprops=dict(
            arrowstyle="->",
            color=color,
            linewidth=ARROW_WIDTH,
            shrinkA=3,
            shrinkB=6,
            mutation_scale=ARROW_HEAD_SCALE,
        ),
        zorder=9,
    )


# =============================================================================
# FIGURE
# =============================================================================

def draw_main_panel(fig):
    ax = fig.add_axes(LEFT_IMAGE_BOX)

    # -------------------------------------------------------------------------
    # Full four-quadrant shapes
    # -------------------------------------------------------------------------

    mi_boundary = full_mi_boundary(num=1400)

    ax.fill(
        mi_boundary[:, 0],
        mi_boundary[:, 1],
        facecolor=MI_FILL_COLOR,
        alpha=MI_FILL_ALPHA,
        edgecolor=MI_EDGE_COLOR,
        linewidth=MI_EDGE_WIDTH,
        zorder=1,
    )

    diamond = classical_diamond()
    ax.fill(
        diamond[:, 0],
        diamond[:, 1],
        facecolor=CLASSICAL_FILL_COLOR,
        alpha=CLASSICAL_FILL_ALPHA,
        edgecolor="none",
        zorder=2,
    )
    ax.plot(
        diamond[:, 0],
        diamond[:, 1],
        color=CLASSICAL_COLOR,
        linewidth=CLASSICAL_WIDTH,
        linestyle=CLASSICAL_LINESTYLE,
        zorder=4,
    )

    qx, qy = quantum_circle()
    ax.plot(
        qx, qy,
        color=QUANTUM_COLOR,
        linewidth=QUANTUM_WIDTH,
        zorder=5,
    )

    # -------------------------------------------------------------------------
    # Coordinate axes
    # -------------------------------------------------------------------------

    ax.axhline(0.0, color=AXIS_COLOR, linewidth=AXIS_WIDTH, zorder=6)
    ax.axvline(0.0, color=AXIS_COLOR, linewidth=AXIS_WIDTH, zorder=6)

    # -------------------------------------------------------------------------
    # Symmetric direction: positive quadrant only
    # -------------------------------------------------------------------------

    ax.plot(
        [0.0, 1.035],
        [0.0, 1.035],
        color=DIAGONAL_COLOR,
        linewidth=DIAGONAL_WIDTH,
        linestyle=DIAGONAL_LINESTYLE,
        zorder=3,
    )

    ax.text(
        0.84, 1.00,
        "(1,1) diagonal",
        fontsize=12.2,
        color="#333333",
        ha="left",
        va="bottom",
    )

    # -------------------------------------------------------------------------
    # Three symmetric points
    # -------------------------------------------------------------------------

    c_mi = symmetric_mi_coordinate()
    c_q = 1.0 / np.sqrt(2.0)
    c_cl = 0.5

    add_point_with_arrow(
        ax,
        (c_cl, c_cl),
        "majority (classical)",
        (0.83, 0.42),
        MAJORITY_COLOR,
    )

    add_point_with_arrow(
        ax,
        (c_q, c_q),
        "quantum",
        (0.90, 0.69),
        QUANTUM_POINT_COLOR,
    )

    add_point_with_arrow(
        ax,
        (c_mi, c_mi),
        "Mutual information",
        (0.90, 0.89),
        MI_POINT_COLOR,
    )

    # -------------------------------------------------------------------------
    # Axis labels
    # -------------------------------------------------------------------------

    ax.text(
        1.045, -0.050,
        r"$c_1$",
        fontsize=FONT_SIZE + 1,
        color=AXIS_COLOR,
        ha="right",
        va="top",
    )
    ax.text(
        0.035, 1.045,
        r"$c_2$",
        fontsize=FONT_SIZE + 1,
        color=AXIS_COLOR,
        ha="left",
        va="top",
    )

    ax.set_xlim(-1.08, 1.16)
    ax.set_ylim(-1.08, 1.08)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    return c_mi


def add_legend(fig):
    """Boundary legend only; point labels are placed directly on the figure."""
    ax = fig.add_axes(RIGHT_LEGEND_BOX)
    ax.set_axis_off()

    ax.text(
        0.0, 0.98,
        "Boundaries in advantage space",
        fontsize=14.5,
        fontweight="bold",
        ha="left",
        va="top",
        transform=ax.transAxes,
    )

    rows = [
        (
            0.70,
            MI_EDGE_COLOR,
            "-",
            "Mutual information",
            r"$\sum_i [1-h_2((1+c_i)/2)] = 1$",
        ),
        (
            0.40,
            QUANTUM_COLOR,
            "-",
            "Quantum",
            r"$c_1^2+c_2^2=1$",
        ),
        (
            0.10,
            CLASSICAL_COLOR,
            CLASSICAL_LINESTYLE,
            "Classical",
            r"$|c_1|+|c_2|=1$",
        ),
    ]

    for y, color, ls, title, formula in rows:
        ax.plot(
            [0.02, 0.19],
            [y, y],
            color=color,
            linewidth=2.5,
            linestyle=ls,
            transform=ax.transAxes,
            clip_on=False,
        )
        ax.text(
            0.25,
            y + 0.055,
            title,
            fontsize=12.5,
            fontweight="bold",
            color=color,
            ha="left",
            va="center",
            transform=ax.transAxes,
        )
        ax.text(
            0.25,
            y - 0.055,
            formula,
            fontsize=10.7,
            color="black",
            ha="left",
            va="center",
            transform=ax.transAxes,
        )


def compose():
    fig = plt.figure(
        figsize=FIGURE_SIZE_INCH,
        dpi=DPI,
        facecolor="white",
    )

    fig.text(
        0.035,
        0.955,
        "n=2 mutual-information boundary",
        fontsize=TITLE_SIZE,
        fontweight="bold",
        ha="left",
        va="top",
    )

    fig.text(
        0.035,
        0.915,
        "The one-bit information-causality constraint in RAC advantage coordinates",
        fontsize=SUBTITLE_SIZE,
        ha="left",
        va="top",
    )

    c_mi = draw_main_panel(fig)
    add_legend(fig)

    fig.savefig(
        OUTPUT,
        dpi=DPI,
        facecolor="white",
        bbox_inches=None,
    )
    plt.close(fig)

    return c_mi


def main():
    c_mi = compose()

    print(f"Saved: {OUTPUT}")
    print(f"Symmetric mutual-information coordinate: c = {c_mi:.12f}")
    print(f"Quantum symmetric coordinate: c = {1/np.sqrt(2):.12f}")
    print("Classical majority coordinate: c = 0.500000000000")


if __name__ == "__main__":
    main()
