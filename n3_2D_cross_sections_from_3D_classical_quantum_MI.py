"""
Figure — n=3 2D cross-sections with classical, quantum and MI boundaries
========================================================================

Two 2D cuts through the same 3D n=3 advantage-space geometry.

Panels
------
A: plane perpendicular to (1,0,0), i.e. c1 = 0
B: plane perpendicular to (1,-1,0), i.e. c1 = c2

Each panel overlays:

Classical:
    cross-section of the n=3 one-bit RAC polytope.

Quantum:
    cross-section of
        c1^2 + c2^2 + c3^2 = 1.

Mutual-information:
    cross-section of
        sum_i [1 - h2((1+c_i)/2)] = 1.

The mutual-information boundary is solved in the ORIGINAL 3D advantage
coordinates and then projected into each 2D slice basis.

Dependencies
------------
pip install numpy scipy matplotlib
"""

from __future__ import annotations

from pathlib import Path
from math import gcd

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull


# =============================================================================
# USER SETTINGS
# =============================================================================

# -----------------------------------------------------------------------------
# WHICH SHAPES TO SHOW
# -----------------------------------------------------------------------------

SHOW_CLASSICAL = True
SHOW_QUANTUM = True
SHOW_MUTUAL_INFORMATION = True

# -----------------------------------------------------------------------------
# OPACITY
# -----------------------------------------------------------------------------

CLASSICAL_ALPHA = 0.28
QUANTUM_ALPHA = 0.10
MUTUAL_INFORMATION_ALPHA = 0.32

# -----------------------------------------------------------------------------
# OPTIONAL DETAIL
# -----------------------------------------------------------------------------

SHOW_CLASSICAL_VERTICES = True
SHOW_ORIGIN = True

# Symmetric (1,1,1) direction.
SHOW_SYMMETRIC_DIRECTION = True
SYMMETRIC_DIRECTION = np.array([1.0, 1.0, 1.0])

SYMMETRIC_LINE_COLOR = "black"
SYMMETRIC_LINE_WIDTH = 1.2
SYMMETRIC_LINE_STYLE = (0, (4, 4))
SYMMETRIC_LINE_EXTENSION = 1.06

SYMMETRIC_DOT_SIZE = 72
SYMMETRIC_DOT_EDGE_COLOR = "white"
SYMMETRIC_DOT_EDGE_WIDTH = 0.8

# Number of angular samples for smooth quantum / MI boundaries.
CURVE_RESOLUTION = 1200

# Bisection iterations for the MI radial solve.
MI_BISECTION_STEPS = 55


# =============================================================================
# OUTPUT / LAYOUT
# =============================================================================

OUTPUT = Path(__file__).with_name(
    "Figure_3.png"
)

FIGURE_SIZE_INCH = (15.36, 8.7)
DPI = 200

SLICES = [
    ("A", np.array([1, 0, 0], dtype=int), 0.0),      # c1 = 0
    ("B", np.array([1, -1, 0], dtype=int), 0.0),     # c1 = c2
]

PANEL_BOXES = [
    [0.055, 0.18, 0.41, 0.68],
    [0.535, 0.18, 0.41, 0.68],
]

LEGEND_BOX = [0.08, 0.035, 0.84, 0.075]


# =============================================================================
# APPEARANCE
# =============================================================================

# Same visual family as the 3D MI figures.
CLASSICAL_COLOR = "#0072B2"
CLASSICAL_EDGE_COLOR = "#00263D"
CLASSICAL_EDGE_WIDTH = 1.6

QUANTUM_COLOR = "#E69F00"
QUANTUM_EDGE_COLOR = "#8F5E00"
QUANTUM_EDGE_WIDTH = 2.0

MUTUAL_INFORMATION_COLOR = "#CC79A7"
MUTUAL_INFORMATION_EDGE_COLOR = "#6B2A52"
MUTUAL_INFORMATION_EDGE_WIDTH = 2.0

AXIS_LINE_COLOR = "black"
AXIS_LINE_WIDTH = 1.25
AXIS_LENGTH_SCALE = 1.12

AXIS_LABEL_FONT_SIZE = 12.5
AXIS_LABEL_PAD = 0.06

# Classical vertex colors.
AXIS_TYPE_COLOR = "crimson"
MAJORITY_TYPE_COLOR = "darkorange"

AXIS_VERTEX_SIZE = 70
MAJORITY_VERTEX_SIZE = 60

ORIGIN_SIZE = 20


# =============================================================================
# n=3 CLASSICAL POLYTOPE
# =============================================================================

AXIS_VERTICES = np.array([
    [ 1.0,  0.0,  0.0],
    [-1.0,  0.0,  0.0],
    [ 0.0,  1.0,  0.0],
    [ 0.0, -1.0,  0.0],
    [ 0.0,  0.0,  1.0],
    [ 0.0,  0.0, -1.0],
])

MAJORITY_VERTICES = 0.5 * np.array([
    [sx, sy, sz]
    for sx in (-1.0, 1.0)
    for sy in (-1.0, 1.0)
    for sz in (-1.0, 1.0)
])

ALL_VERTICES = np.vstack([
    AXIS_VERTICES,
    MAJORITY_VERTICES,
])

TOL = 1e-9


# =============================================================================
# SLICE GEOMETRY
# =============================================================================

def primitive_integer_vector(v):
    """Reduce an integer vector by its positive gcd without flipping sign."""
    v = np.asarray(v, dtype=int)
    nz = np.abs(v[v != 0])

    if len(nz) == 0:
        raise ValueError("Zero vector has no direction.")

    g = int(nz[0])

    for value in nz[1:]:
        g = gcd(g, int(value))

    return v // g


def sparse_oriented_basis_3d(raw_normal):
    """
    Return two sparse, mutually orthogonal integer directions in the slice.

    The exact oriented directions are used for projection, plotting and labels.
    """
    n = primitive_integer_vector(raw_normal)

    active = [int(i) for i in np.flatnonzero(n)]
    zero = [i for i in range(3) if n[i] == 0]

    vectors = []

    if len(active) >= 2:
        i, j = active[0], active[1]

        v = np.zeros(3, dtype=int)
        v[i] = n[j]
        v[j] = -n[i]

        first = np.flatnonzero(v)

        if len(first) and v[first[0]] < 0:
            v = -v

        vectors.append(
            primitive_integer_vector(v)
        )

    for j in zero:
        v = np.zeros(3, dtype=int)
        v[j] = 1
        vectors.append(v)

    if len(vectors) == 1:
        v1 = vectors[0]
        v2 = np.cross(n, v1)

        first = np.flatnonzero(v2)

        if len(first) and v2[first[0]] < 0:
            v2 = -v2

        vectors.append(
            primitive_integer_vector(v2)
        )

    if len(vectors) != 2:
        raise RuntimeError(
            f"Expected two slice axes, got {len(vectors)} "
            f"for normal {tuple(n)}."
        )

    if np.dot(vectors[0], vectors[1]) != 0:
        raise RuntimeError("Constructed section axes are not orthogonal.")

    for v in vectors:
        if np.dot(n, v) != 0:
            raise RuntimeError("Constructed axis is not in the slice.")

    return vectors


def normalized_basis_matrix(vectors3):
    """3x2 orthonormal projection matrix."""
    return np.column_stack([
        np.asarray(v, dtype=float) / np.linalg.norm(v)
        for v in vectors3
    ])


def hull_candidate_edges(vertices):
    hull = ConvexHull(vertices)
    edges = set()

    for tri in hull.simplices:
        for a, b in (
            (int(tri[0]), int(tri[1])),
            (int(tri[1]), int(tri[2])),
            (int(tri[2]), int(tri[0])),
        ):
            edges.add(tuple(sorted((a, b))))

    return sorted(edges)


def unique_rows(points, decimals=10):
    points = np.asarray(points, dtype=float)
    rounded = np.round(points, decimals)

    _, idx = np.unique(
        rounded,
        axis=0,
        return_index=True,
    )

    return points[np.sort(idx)]


def section_points_3d(vertices, normal, offset):
    """Intersect the 3D classical polytope with a plane."""
    normal = np.asarray(normal, dtype=float)
    normal /= np.linalg.norm(normal)

    signed = vertices @ normal - float(offset)
    points = []

    for i, j in hull_candidate_edges(vertices):
        vi = vertices[i]
        vj = vertices[j]

        fi = signed[i]
        fj = signed[j]

        if abs(fi) <= TOL and abs(fj) <= TOL:
            points.extend((vi, vj))

        elif abs(fi) <= TOL:
            points.append(vi)

        elif abs(fj) <= TOL:
            points.append(vj)

        elif fi * fj < 0:
            t = fi / (fi - fj)
            points.append(
                vi + t * (vj - vi)
            )

    if not points:
        raise ValueError(
            "Selected plane does not intersect the polytope."
        )

    return unique_rows(
        np.asarray(points),
        decimals=9,
    )


def project_to_slice(
    points3,
    normal,
    offset,
    basis,
):
    normal = np.asarray(normal, dtype=float)
    normal /= np.linalg.norm(normal)

    x0 = float(offset) * normal

    return (
        np.asarray(points3, dtype=float) - x0
    ) @ basis


def compute_classical_section(
    raw_normal,
    raw_offset,
):
    normal = np.asarray(
        raw_normal,
        dtype=float,
    )
    normal /= np.linalg.norm(normal)

    offset = float(raw_offset)

    axis_vectors = sparse_oriented_basis_3d(
        raw_normal
    )
    basis = normalized_basis_matrix(
        axis_vectors
    )

    points3 = section_points_3d(
        ALL_VERTICES,
        normal,
        offset,
    )

    points2 = project_to_slice(
        points3,
        normal,
        offset,
        basis,
    )

    hull2 = ConvexHull(points2)
    boundary = points2[hull2.vertices]

    return (
        normal,
        offset,
        axis_vectors,
        basis,
        points3,
        points2,
        boundary,
    )


# =============================================================================
# Mutual-information
# =============================================================================

def binary_entropy(p):
    p = np.asarray(p, dtype=float)
    out = np.zeros_like(p)

    mask = (p > 0.0) & (p < 1.0)
    q = p[mask]

    out[mask] = (
        -q * np.log2(q)
        -(1.0 - q) * np.log2(1.0 - q)
    )

    return out


def mutual_information_from_advantage(c):
    p = 0.5 * (
        1.0 + np.asarray(c, dtype=float)
    )

    return 1.0 - binary_entropy(p)


def mi_sum_3d(points3):
    points3 = np.asarray(
        points3,
        dtype=float,
    )

    return np.sum(
        mutual_information_from_advantage(points3),
        axis=-1,
    )


def solve_mi_radius_in_slice(
    directions2,
    basis3x2,
):
    """
    Solve the MI equality radially inside a zero-offset 2D slice.

    A 2D unit direction u2 is mapped back to original advantage coordinates:

        u3 = basis @ u2

    and then r is solved from:

        sum_i I(r u3_i) = 1.
    """
    directions2 = np.asarray(
        directions2,
        dtype=float,
    )

    u2 = (
        directions2
        / np.linalg.norm(
            directions2,
            axis=1,
        )[:, None]
    )

    # slice coordinates -> original 3D coordinates
    u3 = u2 @ basis3x2.T

    u3 /= np.linalg.norm(
        u3,
        axis=1,
    )[:, None]

    lo = np.zeros(
        len(u3),
        dtype=float,
    )

    hi = 1.0 / np.max(
        np.abs(u3),
        axis=1,
    )

    for _ in range(MI_BISECTION_STEPS):
        mid = 0.5 * (lo + hi)

        values = mi_sum_3d(
            mid[:, None] * u3
        )

        inside = values < 1.0

        lo[inside] = mid[inside]
        hi[~inside] = mid[~inside]

    return 0.5 * (lo + hi)


def make_mi_boundary_2d(basis3x2):
    theta = np.linspace(
        0.0,
        2.0 * np.pi,
        CURVE_RESOLUTION,
        endpoint=False,
    )

    directions2 = np.column_stack([
        np.cos(theta),
        np.sin(theta),
    ])

    radii = solve_mi_radius_in_slice(
        directions2,
        basis3x2,
    )

    return (
        directions2
        * radii[:, None]
    )


def make_quantum_boundary_2d():
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


# =============================================================================
# LABELS / CLASSIFICATION
# =============================================================================

def format_direction(v):
    return "(" + ",".join(
        str(int(x))
        for x in v
    ) + ")"


def slice_label(
    raw_normal,
    raw_offset,
):
    n = np.asarray(
        raw_normal,
        dtype=float,
    )

    nz = np.flatnonzero(
        np.abs(n) > 1e-9
    )

    if len(nz) == 1 and abs(raw_offset) < TOL:
        return rf"$c_{nz[0] + 1}=0$"

    if len(nz) == 2 and abs(raw_offset) < TOL:
        i, j = map(int, nz)

        if np.isclose(n[i], -n[j]):
            return rf"$c_{i+1}=c_{j+1}$"

        if np.isclose(n[i], n[j]):
            return rf"$c_{i+1}=-c_{j+1}$"

    return rf"$n\cdot c={raw_offset:g}$"


def original_vertices_in_slice(
    normal,
    offset,
):
    mask = (
        np.abs(
            ALL_VERTICES @ normal - offset
        )
        <= 1e-8
    )

    return ALL_VERTICES[mask]


def is_axis_vertex(v):
    return (
        np.isclose(
            np.sum(np.abs(v)),
            1.0,
        )
        and np.count_nonzero(
            np.abs(v) > 1e-8
        ) == 1
    )



# =============================================================================
# SYMMETRIC DIRECTION
# =============================================================================

def direction_in_slice(direction3, normal, tol=1e-9):
    """Return True when direction3 lies in the zero-offset slice."""
    direction3 = np.asarray(direction3, dtype=float)
    normal = np.asarray(normal, dtype=float)
    normal /= np.linalg.norm(normal)
    return abs(float(np.dot(direction3, normal))) <= tol


def project_direction_to_slice_2d(direction3, basis3x2):
    """Project an in-plane 3D direction into the plotted 2D slice basis."""
    direction3 = np.asarray(direction3, dtype=float)
    d2 = direction3 @ basis3x2
    norm = np.linalg.norm(d2)

    if norm < 1e-12:
        raise ValueError("Projected symmetric direction vanished.")

    return d2 / norm


def classical_radial_intersection(boundary2d, direction2):
    """
    Intersect a ray from the origin with a convex polygon boundary.

    Returns the positive radial distance r such that r*direction2 lies on
    the polygon boundary.
    """
    polygon = np.asarray(boundary2d, dtype=float)
    d = np.asarray(direction2, dtype=float)
    d /= np.linalg.norm(d)

    best_r = np.inf

    for i in range(len(polygon)):
        a = polygon[i]
        b = polygon[(i + 1) % len(polygon)]
        e = b - a

        # Solve r*d = a + t*e.
        mat = np.column_stack([d, -e])
        det = np.linalg.det(mat)

        if abs(det) < 1e-12:
            continue

        r, t = np.linalg.solve(mat, a)

        if r >= -1e-10 and -1e-10 <= t <= 1.0 + 1e-10:
            if r < best_r:
                best_r = r

    if not np.isfinite(best_r):
        raise RuntimeError("Could not intersect symmetric ray with classical polygon.")

    return float(best_r)


def add_symmetric_direction(
    ax,
    normal,
    basis,
    classical_boundary,
):
    """
    Add the positive (1,1,1) ray when it lies in the displayed slice.

    Dots mark its intersections with:
      - classical boundary,
      - quantum boundary,
      - mutual-information boundary.
    """
    if not SHOW_SYMMETRIC_DIRECTION:
        return

    if not direction_in_slice(SYMMETRIC_DIRECTION, normal):
        return

    d2 = project_direction_to_slice_2d(
        SYMMETRIC_DIRECTION,
        basis,
    )

    # Classical intersection.
    r_classical = classical_radial_intersection(
        classical_boundary,
        d2,
    )

    # Quantum unit circle.
    r_quantum = 1.0

    # Mutual-information boundary in the same slice.
    r_mi = solve_mi_radius_in_slice(
        np.asarray([d2]),
        basis,
    )[0]

    radial_values = []

    if SHOW_CLASSICAL:
        radial_values.append(r_classical)

    if SHOW_QUANTUM:
        radial_values.append(r_quantum)

    if SHOW_MUTUAL_INFORMATION:
        radial_values.append(r_mi)

    if not radial_values:
        return

    r_end = SYMMETRIC_LINE_EXTENSION * max(radial_values)

    ax.plot(
        [0.0, d2[0] * r_end],
        [0.0, d2[1] * r_end],
        color=SYMMETRIC_LINE_COLOR,
        linewidth=SYMMETRIC_LINE_WIDTH,
        linestyle=SYMMETRIC_LINE_STYLE,
        zorder=7,
    )

    points = []

    if SHOW_CLASSICAL:
        points.append((
            r_classical,
            CLASSICAL_EDGE_COLOR,
        ))

    if SHOW_QUANTUM:
        points.append((
            r_quantum,
            QUANTUM_EDGE_COLOR,
        ))

    if SHOW_MUTUAL_INFORMATION:
        points.append((
            r_mi,
            MUTUAL_INFORMATION_EDGE_COLOR,
        ))

    for radius, color in points:
        point = d2 * radius

        ax.scatter(
            [point[0]],
            [point[1]],
            s=SYMMETRIC_DOT_SIZE,
            c=[color],
            edgecolors=SYMMETRIC_DOT_EDGE_COLOR,
            linewidths=SYMMETRIC_DOT_EDGE_WIDTH,
            zorder=12,
        )


# =============================================================================
# PLOTTING
# =============================================================================

def draw_panel(
    ax,
    letter,
    raw_normal,
    raw_offset,
):
    (
        normal,
        offset,
        axis_vectors,
        basis,
        points3,
        points2,
        classical_boundary,
    ) = compute_classical_section(
        raw_normal,
        raw_offset,
    )

    if abs(offset) > 1e-12:
        raise NotImplementedError(
            "This comparison currently assumes zero-offset slices."
        )

    # -------------------------------------------------------------------------
    # Mutual-information — largest region
    # -------------------------------------------------------------------------

    if SHOW_MUTUAL_INFORMATION:
        mi_boundary = make_mi_boundary_2d(
            basis
        )

        ax.fill(
            mi_boundary[:, 0],
            mi_boundary[:, 1],
            facecolor=MUTUAL_INFORMATION_COLOR,
            alpha=MUTUAL_INFORMATION_ALPHA,
            edgecolor=MUTUAL_INFORMATION_EDGE_COLOR,
            linewidth=MUTUAL_INFORMATION_EDGE_WIDTH,
            zorder=1,
        )

    # -------------------------------------------------------------------------
    # Quantum circle
    # -------------------------------------------------------------------------

    if SHOW_QUANTUM:
        quantum_boundary = make_quantum_boundary_2d()

        ax.fill(
            quantum_boundary[:, 0],
            quantum_boundary[:, 1],
            facecolor=QUANTUM_COLOR,
            alpha=QUANTUM_ALPHA,
            edgecolor=QUANTUM_EDGE_COLOR,
            linewidth=QUANTUM_EDGE_WIDTH,
            zorder=2,
        )

    # -------------------------------------------------------------------------
    # Classical polygon
    # -------------------------------------------------------------------------

    if SHOW_CLASSICAL:
        ax.fill(
            classical_boundary[:, 0],
            classical_boundary[:, 1],
            facecolor=CLASSICAL_COLOR,
            alpha=CLASSICAL_ALPHA,
            edgecolor=CLASSICAL_EDGE_COLOR,
            linewidth=CLASSICAL_EDGE_WIDTH,
            zorder=3,
        )

    # -------------------------------------------------------------------------
    # Symmetric (1,1,1) direction, when contained in this slice
    # -------------------------------------------------------------------------

    add_symmetric_direction(
        ax,
        normal,
        basis,
        classical_boundary,
    )

    # -------------------------------------------------------------------------
    # True in-plane axes
    # -------------------------------------------------------------------------

    all_extents = [
        np.max(
            np.linalg.norm(
                classical_boundary,
                axis=1,
            )
        )
    ]

    if SHOW_QUANTUM:
        all_extents.append(1.0)

    if SHOW_MUTUAL_INFORMATION:
        all_extents.append(
            np.max(
                np.linalg.norm(
                    mi_boundary,
                    axis=1,
                )
            )
        )

    extent = max(all_extents)
    axis_length = AXIS_LENGTH_SCALE * extent

    for axis_index, v in enumerate(axis_vectors):
        d2 = np.eye(2)[axis_index]

        ax.plot(
            [
                -axis_length * d2[0],
                axis_length * d2[0],
            ],
            [
                -axis_length * d2[1],
                axis_length * d2[1],
            ],
            color=AXIS_LINE_COLOR,
            linewidth=AXIS_LINE_WIDTH,
            zorder=8,
        )

        tip = d2 * axis_length

        if axis_index == 0:
            ha, va = "left", "bottom"
            xytext = (
                AXIS_LABEL_PAD,
                AXIS_LABEL_PAD,
            )
        else:
            ha, va = "center", "bottom"
            xytext = (
                0.0,
                AXIS_LABEL_PAD,
            )

        ax.text(
            tip[0] + xytext[0],
            tip[1] + xytext[1],
            format_direction(v),
            fontsize=AXIS_LABEL_FONT_SIZE,
            color="black",
            ha=ha,
            va=va,
            zorder=10,
        )

    # -------------------------------------------------------------------------
    # Classical vertices lying genuinely in the plane
    # -------------------------------------------------------------------------

    if SHOW_CLASSICAL and SHOW_CLASSICAL_VERTICES:
        original = original_vertices_in_slice(
            normal,
            offset,
        )

        for v in original:
            p2 = project_to_slice(
                np.asarray([v]),
                normal,
                offset,
                basis,
            )[0]

            if is_axis_vertex(v):
                color = AXIS_TYPE_COLOR
                size = AXIS_VERTEX_SIZE
            else:
                color = MAJORITY_TYPE_COLOR
                size = MAJORITY_VERTEX_SIZE

            ax.scatter(
                [p2[0]],
                [p2[1]],
                s=size,
                c=[color],
                edgecolors="black",
                linewidths=0.7,
                zorder=9,
            )

    if SHOW_ORIGIN:
        ax.scatter(
            [0],
            [0],
            s=ORIGIN_SIZE,
            c=["black"],
            zorder=11,
        )

    ax.set_aspect(
        "equal",
        adjustable="box",
    )
    ax.axis("off")

    lim = axis_length * 1.18

    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)

    # Panel letter.
    ax.text(
        0.015,
        1.02,
        letter,
        transform=ax.transAxes,
        fontsize=15,
        fontweight="bold",
        ha="left",
        va="top",
    )

    # Slice equation.
    ax.text(
        0.095,
        1.02,
        slice_label(
            raw_normal,
            raw_offset,
        ),
        transform=ax.transAxes,
        fontsize=15,
        ha="left",
        va="top",
    )

    # Same in-plane direction line as the source figure.
    basis_text = (
        "In-plane directions: "
        + "   ·   ".join(
            format_direction(v)
            for v in axis_vectors
        )
    )

    ax.text(
        0.5,
        -0.02,
        basis_text,
        transform=ax.transAxes,
        fontsize=10.8,
        ha="center",
        va="top",
        color="black",
    )


# =============================================================================
# SHARED LEGEND
# =============================================================================

def add_shared_legend(fig):
    ax = fig.add_axes(LEGEND_BOX)
    ax.set_axis_off()

    entries = []

    if SHOW_CLASSICAL:
        entries.append((
            CLASSICAL_EDGE_COLOR,
            "Classical",
        ))

    if SHOW_QUANTUM:
        entries.append((
            QUANTUM_EDGE_COLOR,
            r"Quantum  $c_1^2+c_2^2+c_3^2=1$",
        ))

    if SHOW_MUTUAL_INFORMATION:
        entries.append((
            MUTUAL_INFORMATION_EDGE_COLOR,
            r"Mutual-information  "
            r"$\sum_{i=1}^{3}[1-h_2((1+c_i)/2)]=1$",
        ))

    if not entries:
        return

    xs = np.linspace(
        0.08,
        0.68,
        len(entries),
    )

    for x, (color, label) in zip(
        xs,
        entries,
    ):
        ax.plot(
            [x, x + 0.05],
            [0.55, 0.55],
            color=color,
            linewidth=4.0,
            transform=ax.transAxes,
            solid_capstyle="round",
        )

        ax.text(
            x + 0.065,
            0.55,
            label,
            color=color,
            fontsize=10.8,
            va="center",
            transform=ax.transAxes,
        )


# =============================================================================
# FIGURE
# =============================================================================

def compose():
    fig = plt.figure(
        figsize=FIGURE_SIZE_INCH,
        dpi=DPI,
        facecolor="white",
    )

    fig.text(
        0.035,
        0.965,
        "n=3 cross-sections",
        fontsize=22,
        fontweight="bold",
        ha="left",
        va="top",
    )

    fig.text(
        0.035,
        0.922,
        "Two 2D cuts through the same classical, quantum and "
        "mutual-information advantage-space geometry",
        fontsize=14.5,
        ha="left",
        va="top",
    )

    for (
        letter,
        normal,
        offset,
    ), box in zip(
        SLICES,
        PANEL_BOXES,
    ):
        ax = fig.add_axes(box)

        draw_panel(
            ax,
            letter,
            normal,
            offset,
        )

    add_shared_legend(fig)

    fig.savefig(
        OUTPUT,
        dpi=DPI,
        facecolor="white",
        bbox_inches=None,
    )

    plt.close(fig)


# =============================================================================
# MAIN
# =============================================================================

def main():
    print(
        "Rendering n=3 2D classical / quantum / "
        "mutual-information cross-sections..."
    )

    for letter, normal, offset in SLICES:
        (
            _,
            _,
            axis_vectors,
            _,
            _,
            _,
            classical_boundary,
        ) = compute_classical_section(
            normal,
            offset,
        )

        print(
            f"{letter}: normal={tuple(normal)}, "
            f"offset={offset:g}, "
            f"classical section vertices={len(classical_boundary)}, "
            f"axes="
            + ", ".join(
                format_direction(v)
                for v in axis_vectors
            )
        )

    compose()

    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()