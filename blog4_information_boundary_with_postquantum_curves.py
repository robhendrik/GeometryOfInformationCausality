"""
Figure 4 — Information-theoretic boundary as the game grows
============================================================

For each n, plot the 2D plane spanned by

    vertical:    (1,0,0,...,0)
    horizontal:  (0,1,1,...,1)/sqrt(n-1)

This plane contains the symmetric direction (1,1,...,1).

The figure compares

    Quantum:
        sum_i c_i^2 = 1

    Information boundary:
        sum_i [1 - h2((1+c_i)/2)] = 1

The information boundary is evaluated in the original n-dimensional
advantage coordinates.

Dependencies
------------
pip install numpy matplotlib
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch


# =============================================================================
# USER SETTINGS
# =============================================================================

N_VALUES = [2, 4, 8, 16]

OUTPUT = Path(__file__).with_name(
    "Figure_4_including_postquantum_curves.png"
)

FIGURE_SIZE_INCH = (15.36, 8.70)
DPI = 200

CURVE_RESOLUTION = 1400
MI_BISECTION_STEPS = 60

SHOW_QUANTUM = True
SHOW_INFORMATION = True
SHOW_SYMMETRIC_DIRECTION = True
SHOW_INTERSECTION_DOTS = True
SHOW_ORIGIN = True
SHOW_BOTTOM_NOTE = True
SHOW_POSTQUANTUM = True

# Exploratory strengths. E=1/sqrt(2) is the quantum member.
E_VALUES = [1 / np.sqrt(2), 0.75, 0.80, 0.90, 1.00]
POSTQUANTUM_LINE_WIDTH = 1.65
POSTQUANTUM_ALPHA = 0.92


# =============================================================================
# LAYOUT
# =============================================================================

TITLE = "Quantum, information, and exploratory post-quantum boundaries"

SUBTITLE = (
    "Cross-sections spanned by $(1,0,\\ldots,0)$ and "
    "$(0,1,\\ldots,1)$, containing the symmetric direction"
)

TITLE_SIZE = 22
SUBTITLE_SIZE = 14.5
PANEL_TITLE_SIZE = 17

PANEL_LEFT = 0.045
PANEL_RIGHT = 0.975
PANEL_BOTTOM = 0.33
PANEL_TOP = 0.82
PANEL_GAP = 0.024

LEGEND_BOX = [0.045, 0.13, 0.91, 0.12]
NOTE_BOX = [0.055, 0.018, 0.89, 0.085]


# =============================================================================
# APPEARANCE
# =============================================================================

# Same palette as the earlier Blog 4 figures.

QUANTUM_COLOR = "#E69F00"
QUANTUM_EDGE_COLOR = "#8F5E00"
QUANTUM_FILL_ALPHA = 0.10
QUANTUM_EDGE_WIDTH = 2.0

INFORMATION_COLOR = "#CC79A7"
INFORMATION_EDGE_COLOR = "#6B2A52"
INFORMATION_FILL_ALPHA = 0.28
INFORMATION_EDGE_WIDTH = 2.0

AXIS_COLOR = "black"
AXIS_WIDTH = 1.15

SYMMETRIC_COLOR = "black"
SYMMETRIC_WIDTH = 1.2
SYMMETRIC_STYLE = (0, (4, 4))
SYMMETRIC_EXTENSION = 1.08

ORIGIN_SIZE = 18

QUANTUM_DOT_COLOR = QUANTUM_EDGE_COLOR
INFORMATION_DOT_COLOR = INFORMATION_EDGE_COLOR

DOT_SIZE = 58
DOT_EDGE_COLOR = "white"
DOT_EDGE_WIDTH = 0.8

AXIS_LABEL_SIZE = 10.0
SYMMETRIC_LABEL_SIZE = 10.2

LEGEND_LINE_WIDTH = 4.0

POSTQUANTUM_COLORS = {
    0.75: "#0072B2",
    0.80: "#009E73",
    0.90: "#D55E00",
    1.00: "#000000",
}


# =============================================================================
# INFORMATION THEORY
# =============================================================================

def binary_entropy(p):
    """Binary entropy h2(p), vectorized and numerically safe."""

    p = np.asarray(p, dtype=float)
    out = np.zeros_like(p)

    mask = (p > 0.0) & (p < 1.0)
    q = p[mask]

    out[mask] = (
        -q * np.log2(q)
        - (1.0 - q) * np.log2(1.0 - q)
    )

    return out


def mutual_information_from_advantage(c):
    """
    Mutual information for a uniform binary variable with advantage

        c = 2P - 1.
    """

    c = np.asarray(c, dtype=float)
    p = 0.5 * (1.0 + c)

    return 1.0 - binary_entropy(p)


def mi_sum(points):
    """Sum of the individual mutual informations."""

    points = np.asarray(points, dtype=float)

    return np.sum(
        mutual_information_from_advantage(points),
        axis=-1,
    )


# =============================================================================
# SLICE GEOMETRY
# =============================================================================

def make_slice_basis(n):
    """
    Return an n x 2 orthonormal basis.

    Plotted x-axis:
        (0,1,1,...,1)/sqrt(n-1)

    Plotted y-axis:
        (1,0,0,...,0)

    Hence the single-coordinate axis is vertical.
    """

    if n < 2:
        raise ValueError("n must be at least 2.")

    horizontal = np.zeros(n)
    horizontal[1:] = 1.0
    horizontal /= np.linalg.norm(horizontal)

    vertical = np.zeros(n)
    vertical[0] = 1.0

    return np.column_stack([
        horizontal,
        vertical,
    ])


def symmetric_direction_2d(n):
    """
    Unit direction corresponding to (1,1,...,1).

    In this slice its unnormalised plotted coordinates are

        (sqrt(n-1), 1).
    """

    d = np.array([
        np.sqrt(n - 1.0),
        1.0,
    ])

    return d / np.linalg.norm(d)


# =============================================================================
# BOUNDARIES
# =============================================================================

def unit_directions_2d():
    theta = np.linspace(
        0.0,
        2.0 * np.pi,
        CURVE_RESOLUTION,
        endpoint=False,
    )

    return np.column_stack([
        np.cos(theta),
        np.sin(theta),
    ])


def quantum_boundary_2d():
    """Central cross-section of the quantum hypersphere."""

    return unit_directions_2d()


def solve_information_radius(directions2, basis):
    """
    Solve

        sum_i I(c_i) = 1

    radially inside the selected 2D plane.
    """

    directions2 = np.asarray(directions2, dtype=float)

    u2 = (
        directions2
        / np.linalg.norm(directions2, axis=1)[:, None]
    )

    # Back to original n-dimensional advantage coordinates.
    u_n = u2 @ basis.T

    u_n /= np.linalg.norm(
        u_n,
        axis=1,
    )[:, None]

    lo = np.zeros(len(u_n))

    # Physical coordinate limit |c_i| <= 1.
    hi = 1.0 / np.max(
        np.abs(u_n),
        axis=1,
    )

    for _ in range(MI_BISECTION_STEPS):

        mid = 0.5 * (lo + hi)

        values = mi_sum(
            mid[:, None] * u_n
        )

        inside = values < 1.0

        lo[inside] = mid[inside]
        hi[~inside] = mid[~inside]

    return 0.5 * (lo + hi)


def information_boundary_2d(n):
    basis = make_slice_basis(n)
    directions = unit_directions_2d()

    radii = solve_information_radius(
        directions,
        basis,
    )

    return directions * radii[:, None]


def symmetric_information_radius(n):
    basis = make_slice_basis(n)

    direction = symmetric_direction_2d(n)[None, :]

    return float(
        solve_information_radius(
            direction,
            basis,
        )[0]
    )


# =============================================================================
# EXPLORATORY POST-QUANTUM FAMILY
# =============================================================================

def p_from_E(E):
    """
    Choose p so that the symmetric point of the p-norm body scales as E^k
    for n=2^k.  Since n^(-1/p)=E^k, p=-1/log2(E).

    E=1/sqrt(2) -> p=2 (quantum sphere)
    E->1          -> p->infinity (hypercube)
    """
    if np.isclose(E, 1.0):
        return np.inf
    return -1.0 / np.log2(E)


def postquantum_boundary_2d(n, E):
    """
    Exploratory p-norm body sum_i |c_i|^p = 1, sliced in the same plane.

    Plotted coordinates are:
        x -> (0,1,...,1)/sqrt(n-1)
        y -> (1,0,...,0)

    Thus c1=y and c2=...=cn=x/sqrt(n-1).
    """
    if np.isclose(E, 1.0):
        xmax = np.sqrt(n - 1.0)
        return np.array([
            [-xmax, -1.0],
            [ xmax, -1.0],
            [ xmax,  1.0],
            [-xmax,  1.0],
            [-xmax, -1.0],
        ])

    p = p_from_E(E)
    theta = np.linspace(0.0, 2.0*np.pi, CURVE_RESOLUTION, endpoint=False)
    u = np.column_stack([np.cos(theta), np.sin(theta)])
    ux, uy = u[:, 0], u[:, 1]

    coeff = (n - 1.0) ** (1.0 - p/2.0)
    denom = np.abs(uy)**p + coeff*np.abs(ux)**p
    r = denom ** (-1.0/p)
    return u * r[:, None]


def postquantum_color(E):
    if np.isclose(E, 1.0 / np.sqrt(2.0)):
        return QUANTUM_EDGE_COLOR
    for key, color in POSTQUANTUM_COLORS.items():
        if np.isclose(E, key):
            return color
    return "0.35"


# =============================================================================
# PANEL
# =============================================================================

def draw_panel(ax, n):

    max_radius = 1.0

    # -------------------------------------------------------------------------
    # Information region
    # -------------------------------------------------------------------------

    if SHOW_INFORMATION:

        info = information_boundary_2d(n)

        ax.fill(
            info[:, 0],
            info[:, 1],
            facecolor=INFORMATION_COLOR,
            alpha=INFORMATION_FILL_ALPHA,
            edgecolor=INFORMATION_EDGE_COLOR,
            linewidth=INFORMATION_EDGE_WIDTH,
            zorder=1,
        )

        max_radius = max(
            max_radius,
            float(
                np.max(
                    np.linalg.norm(info, axis=1)
                )
            ),
        )

    # -------------------------------------------------------------------------
    # Quantum circle
    # -------------------------------------------------------------------------

    if SHOW_QUANTUM:

        quantum = quantum_boundary_2d()

        ax.fill(
            quantum[:, 0],
            quantum[:, 1],
            facecolor=QUANTUM_COLOR,
            alpha=QUANTUM_FILL_ALPHA,
            edgecolor=QUANTUM_EDGE_COLOR,
            linewidth=QUANTUM_EDGE_WIDTH,
            zorder=2,
        )

    # -------------------------------------------------------------------------
    # Exploratory post-quantum curves
    # -------------------------------------------------------------------------

    if SHOW_POSTQUANTUM:
        for E in E_VALUES:
            # E=1/sqrt(2) is exactly the quantum circle already shown.
            if np.isclose(E, 1.0 / np.sqrt(2.0)):
                continue

            pq = postquantum_boundary_2d(n, E)
            ax.plot(
                pq[:, 0],
                pq[:, 1],
                color=postquantum_color(E),
                linewidth=POSTQUANTUM_LINE_WIDTH,
                alpha=POSTQUANTUM_ALPHA,
                zorder=3,
            )
            max_radius = max(
                max_radius,
                float(np.max(np.linalg.norm(pq, axis=1))),
            )

    # -------------------------------------------------------------------------
    # Axes
    # -------------------------------------------------------------------------

    axis_extent = 1.14 * max_radius

    ax.plot(
        [-axis_extent, axis_extent],
        [0.0, 0.0],
        color=AXIS_COLOR,
        linewidth=AXIS_WIDTH,
        zorder=5,
    )

    ax.plot(
        [0.0, 0.0],
        [-axis_extent, axis_extent],
        color=AXIS_COLOR,
        linewidth=AXIS_WIDTH,
        zorder=5,
    )

    # -------------------------------------------------------------------------
    # Symmetric direction
    # -------------------------------------------------------------------------

    d_sym = symmetric_direction_2d(n)

    r_quantum = 1.0
    r_information = symmetric_information_radius(n)

    if SHOW_SYMMETRIC_DIRECTION:

        r_end = (
            SYMMETRIC_EXTENSION
            * max(r_quantum, r_information)
        )

        ax.plot(
            [0.0, d_sym[0] * r_end],
            [0.0, d_sym[1] * r_end],
            color=SYMMETRIC_COLOR,
            linewidth=SYMMETRIC_WIDTH,
            linestyle=SYMMETRIC_STYLE,
            zorder=7,
        )

    # -------------------------------------------------------------------------
    # Boundary intersections on symmetric direction
    # -------------------------------------------------------------------------

    if SHOW_INTERSECTION_DOTS:

        if SHOW_QUANTUM:

            p_q = d_sym * r_quantum

            ax.scatter(
                [p_q[0]],
                [p_q[1]],
                s=DOT_SIZE,
                c=[QUANTUM_DOT_COLOR],
                edgecolors=DOT_EDGE_COLOR,
                linewidths=DOT_EDGE_WIDTH,
                zorder=10,
            )

        if SHOW_INFORMATION:

            p_i = d_sym * r_information

            ax.scatter(
                [p_i[0]],
                [p_i[1]],
                s=DOT_SIZE,
                c=[INFORMATION_DOT_COLOR],
                edgecolors=DOT_EDGE_COLOR,
                linewidths=DOT_EDGE_WIDTH,
                zorder=11,
            )

    if SHOW_ORIGIN:

        ax.scatter(
            [0.0],
            [0.0],
            s=ORIGIN_SIZE,
            c=["black"],
            zorder=12,
        )

    # -------------------------------------------------------------------------
    # Axis labels
    # -------------------------------------------------------------------------

    # Vertical axis — horizontal label above it.
    if n == 2:
        ax.text(
                0.0,
                axis_extent * 1.025,
                r"$(1,0)$",
                fontsize=AXIS_LABEL_SIZE,
                color="black",
                ha="center",
                va="bottom",
                zorder=14,
            )
    else:
        ax.text(
            0.0,
            axis_extent * 1.025,
            r"$(1,0,\ldots,0)$",
            fontsize=AXIS_LABEL_SIZE,
            color="black",
            ha="center",
            va="bottom",
            zorder=14,
        )

    # Horizontal axis.
    if n == 2:
        ax.text(
                axis_extent * 1.025,
                0.0,
                r"$(0,1)$",
                fontsize=AXIS_LABEL_SIZE,
                color="black",
                ha="left",
                va="center",
                zorder=14,
            )
    else:
        ax.text(
            axis_extent * 1.025,
            0.0,
            r"$(0,1,\ldots,1)$",
            fontsize=AXIS_LABEL_SIZE,
            color="black",
            ha="left",
            va="center",
            zorder=14,
        )

    # Symmetric direction.
    label_r = 0.88 * max(
        r_quantum,
        r_information,
    )

    label_pos = d_sym * label_r

    ax.text(
        label_pos[0] + 0.035,
        label_pos[1] + 0.025,
        r"$(1,1,\ldots,1)$",
        fontsize=SYMMETRIC_LABEL_SIZE,
        color="black",
        ha="left",
        va="bottom",
        zorder=14,
    )

    # -------------------------------------------------------------------------
    # Panel formatting
    # -------------------------------------------------------------------------

    ax.set_aspect(
        "equal",
        adjustable="box",
    )

    ax.axis("off")

    visible = axis_extent * 1.05

    ax.set_xlim(
        -visible,
        visible,
    )

    ax.set_ylim(
        -visible,
        visible,
    )

    ax.set_title(
        rf"$n={n}$",
        fontsize=PANEL_TITLE_SIZE,
        fontweight="bold",
        pad=14,
    )

    return {
        "n": n,
        "quantum_radius": r_quantum,
        "information_radius": r_information,
    }


# =============================================================================
# LEGEND
# =============================================================================

def add_shared_legend(fig):

    ax = fig.add_axes(LEGEND_BOX)
    ax.set_axis_off()

    y1 = 0.70

    # Quantum
    ax.plot(
        [0.00, 0.055],
        [y1, y1],
        color=QUANTUM_EDGE_COLOR,
        linewidth=LEGEND_LINE_WIDTH,
        transform=ax.transAxes,
        solid_capstyle="round",
    )

    ax.text(
        0.065,
        y1,
        r"Quantum boundary  $\sum_i c_i^2=1$",
        color=QUANTUM_EDGE_COLOR,
        fontsize=11.2,
        va="center",
        transform=ax.transAxes,
    )

    # Information
    ax.plot(
        [0.33, 0.385],
        [y1, y1],
        color=INFORMATION_EDGE_COLOR,
        linewidth=LEGEND_LINE_WIDTH,
        transform=ax.transAxes,
        solid_capstyle="round",
    )

    ax.text(
        0.395,
        y1,
        r"Information boundary  "
        r"$\sum_i[1-h_2((1+c_i)/2)]=1$",
        color=INFORMATION_EDGE_COLOR,
        fontsize=11.2,
        va="center",
        transform=ax.transAxes,
    )

    # Symmetric direction
    ax.plot(
        [0.75, 0.805],
        [y1, y1],
        color=SYMMETRIC_COLOR,
        linewidth=SYMMETRIC_WIDTH,
        linestyle=SYMMETRIC_STYLE,
        transform=ax.transAxes,
    )

    ax.text(
        0.815,
        y1,
        r"Symmetric direction $(1,1,\ldots,1)$",
        fontsize=11.0,
        va="center",
        transform=ax.transAxes,
    )

    y2 = 0.22

    ax.scatter(
        [0.015],
        [y2],
        s=DOT_SIZE,
        c=[QUANTUM_DOT_COLOR],
        edgecolors=DOT_EDGE_COLOR,
        linewidths=DOT_EDGE_WIDTH,
        transform=ax.transAxes,
    )

    ax.text(
        0.04,
        y2,
        "Intersection with quantum boundary",
        fontsize=10.8,
        va="center",
        transform=ax.transAxes,
    )

    ax.scatter(
        [0.335],
        [y2],
        s=DOT_SIZE,
        c=[INFORMATION_DOT_COLOR],
        edgecolors=DOT_EDGE_COLOR,
        linewidths=DOT_EDGE_WIDTH,
        transform=ax.transAxes,
    )

    ax.text(
        0.36,
        y2,
        "Intersection with information boundary",
        fontsize=10.8,
        va="center",
        transform=ax.transAxes,
    )


def add_postquantum_legend(fig):
    if not SHOW_POSTQUANTUM:
        return

    ax = fig.add_axes([0.49, 0.105, 0.47, 0.055])
    ax.set_axis_off()

    entries = [
        (0.75, "E = 0.75"),
        (0.80, "E = 0.80"),
        (0.90, "E = 0.90"),
        (1.00, "E = 1"),
    ]

    for x, (E, label) in zip([0.00, 0.25, 0.50, 0.75], entries):
        ax.plot(
            [x, x + 0.065], [0.5, 0.5],
            color=postquantum_color(E),
            linewidth=POSTQUANTUM_LINE_WIDTH,
            transform=ax.transAxes,
        )
        ax.text(
            x + 0.078, 0.5, label,
            fontsize=10.2, va="center",
            transform=ax.transAxes,
        )


# =============================================================================
# BOTTOM NOTE
# =============================================================================

def add_bottom_note(fig):

    if not SHOW_BOTTOM_NOTE:
        return

    ax = fig.add_axes(NOTE_BOX)
    ax.set_axis_off()

    patch = FancyBboxPatch(
        (0.005, 0.05),
        0.99,
        0.90,
        boxstyle="round,pad=0.012,rounding_size=0.03",
        facecolor="white",
        edgecolor="#B8B8B8",
        linewidth=1.1,
        transform=ax.transAxes,
    )

    ax.add_patch(patch)

    ax.text(
        0.02,
        0.64,
        r"Along the symmetric direction, $c_i=c$ for all $i$. "
        r"The information bound gives $nI(c)=1$, so for large $n$ "
        r"(small $c$),",
        fontsize=10.7,
        ha="left",
        va="center",
        transform=ax.transAxes,
    )

    ax.text(
        0.02,
        0.30,
        r"$I(c)\approx c^2/(2\ln2)$ and "
        r"$c\approx\sqrt{2\ln2/n}\propto1/\sqrt{n}$. "
        r"The $1/\sqrt{n}$ scaling comes from distributing the "
        r"advantage over $n$ possible questions.",
        fontsize=10.7,
        ha="left",
        va="center",
        transform=ax.transAxes,
    )


# =============================================================================
# FIGURE
# =============================================================================

def panel_boxes(number):

    total_width = PANEL_RIGHT - PANEL_LEFT

    gap_total = PANEL_GAP * (number - 1)

    panel_width = (
        total_width - gap_total
    ) / number

    panel_height = (
        PANEL_TOP - PANEL_BOTTOM
    )

    boxes = []

    for i in range(number):

        left = (
            PANEL_LEFT
            + i * (panel_width + PANEL_GAP)
        )

        boxes.append([
            left,
            PANEL_BOTTOM,
            panel_width,
            panel_height,
        ])

    return boxes


def compose():

    fig = plt.figure(
        figsize=FIGURE_SIZE_INCH,
        dpi=DPI,
        facecolor="white",
    )

    fig.text(
        0.035,
        0.965,
        TITLE,
        fontsize=TITLE_SIZE,
        fontweight="bold",
        ha="left",
        va="top",
    )

    fig.text(
        0.035,
        0.922,
        SUBTITLE,
        fontsize=SUBTITLE_SIZE,
        ha="left",
        va="top",
    )

    results = []

    for n, box in zip(
        N_VALUES,
        panel_boxes(len(N_VALUES)),
    ):

        ax = fig.add_axes(box)

        results.append(
            draw_panel(ax, n)
        )

    add_shared_legend(fig)
    add_postquantum_legend(fig)

    add_bottom_note(fig)

    fig.savefig(
        OUTPUT,
        dpi=DPI,
        facecolor="white",
        bbox_inches=None,
    )

    plt.close(fig)

    return results


# =============================================================================
# MAIN
# =============================================================================

def main():

    print(
        "Rendering information-theoretic cross-sections "
        f"for n = {N_VALUES}..."
    )

    results = compose()

    print(f"Saved: {OUTPUT}")

    for result in results:

        print(
            f"n={result['n']:>3}: "
            f"quantum symmetric radius="
            f"{result['quantum_radius']:.8f}, "
            f"information symmetric radius="
            f"{result['information_radius']:.8f}"
        )


if __name__ == "__main__":
    main()