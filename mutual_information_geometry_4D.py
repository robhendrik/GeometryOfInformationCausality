"""
n=4 RAC advantage-space cross-sections:
classical + quantum + mutual-information boundaries
===================================================

Produces the same four 3D cross-sections used in the existing n=4 publication
figure, but overlays three nested regions in every panel:

    Classical:
        3D section of the n=4 classical RAC polytope.

    Quantum:
        section of the 4D unit hypersphere
            c1^2 + c2^2 + c3^2 + c4^2 = 1.

    mutual-information:
        section of
            sum_i [1 - h2((1 + c_i)/2)] = 1.

The mutual-information boundary is solved in ORIGINAL 4D advantage
coordinates, then projected into the oriented 3D slice basis. This is
important for tilted slices such as c1+c2+c3+c4=0.

Layout, camera, slice definitions, and sparse integer in-plane directions
follow the existing n=4 publication script.

Dependencies
------------
pip install numpy scipy pyvista matplotlib

Also place this script next to:

    n4_rac_cross_section_axis_inset_planar_edges.py
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction
from math import gcd, lcm
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
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
# OPTIONAL CLASSICAL DETAIL
# -----------------------------------------------------------------------------

SHOW_CLASSICAL_EDGES = True
SHOW_CLASSICAL_VERTICES = False

# -----------------------------------------------------------------------------
# ORIENTED SLICE AXES
# -----------------------------------------------------------------------------

SHOW_MAIN_AXES = True
SHOW_AXIS_DIRECTION_LABELS = True



# -----------------------------------------------------------------------------
# NUMERICAL RESOLUTION
# -----------------------------------------------------------------------------

QUANTUM_SPHERE_RESOLUTION = 180

# Starting unit sphere used as the direction mesh for the MI section.
MI_THETA_RESOLUTION = 180
MI_PHI_RESOLUTION = 120

# Bisection steps for the MI radial equality.
MI_BISECTION_STEPS = 55


# =============================================================================
# FILES / OUTPUT / LAYOUT
# =============================================================================

BASE_SCRIPT = Path(__file__).with_name(
    "n4_rac_cross_section_axis_inset_planar_edges.py"
)

OUTPUT = Path(__file__).with_name(
    "Figure_n4_classical_quantum_mutual_information_cross_sections.png"
)

# Same four cuts as the publication figure.
SLICES = [
    ("A", np.array([1., 0., 0., 0.]), 0.0),       # c1 = 0
    ("B", np.array([1., -1., 0., 0.]), 0.0),      # c1 = c2
    ("C", np.array([1., 1., 0., 0.]), 0.0),       # c1 = -c2
    ("D", np.array([1., 1., 1., 1.]), 0.0),       # c1+c2+c3+c4 = 0
]

FIGURE_SIZE_INCH = (15.36, 11.2)
DPI = 200
PANEL_RENDER_SIZE = (1300, 1120)

PANEL_BOXES = [
    [.035, .485, .455, .385],
    [.51,  .485, .455, .385],
    [.035, .085, .455, .385],
    [.51,  .085, .455, .385],
]


# =============================================================================
# APPEARANCE
# =============================================================================

# Same palette as the n=3 MI figure.

CLASSICAL_COLOR = "#0072B2"
CLASSICAL_EDGE_COLOR = "#00263D"
CLASSICAL_EDGE_WIDTH = 1.75
CLASSICAL_OPACITY = 0.55        # innermost, solid — should read as the most "opaque" shape

QUANTUM_COLOR = "#E69F00"
QUANTUM_EDGE_COLOR = "#8F5E00"
QUANTUM_OPACITY = 0.35          # middle shell — visible as a surface, not just gridlines

MUTUAL_INFORMATION_COLOR = "#CC79A7"
MUTUAL_INFORMATION_EDGE_COLOR = "#6B2A52"
MUTUAL_INFORMATION_OPACITY = 0.25   # outermost — must be the most transparent or it occludes everything inside it

BACKGROUND = "white"

# n=4 classical vertex types, if enabled.
VERTEX_SIZE = 19
VERTEX_COLORS = {
    "axis type (1,0,0,0)": "crimson",
    "3/4 + 1/4 type": "royalblue",
    "1/2 + 1/2 + 1/2 type": "darkorange",
}

# Slice-axis appearance.
MAIN_AXIS_LENGTH = 1.25
MAIN_AXIS_WIDTH = 1.35
MAIN_AXIS_LABEL_SCALE = 1.01
MAIN_AXIS_LABEL_FONT_SIZE = 15

# Per-axis screen-space text offsets.
LABEL_OFFSETS = [
    (-0.18,  0.00),
    ( 0.00, -0.02),
    (-0.08,  0.00),
]

# -----------------------------------------------------------------------------
# SURFACE GUIDES
# -----------------------------------------------------------------------------
#
# Geographic convention is defined in EACH rendered 3D slice:
#   slice-axis 3 = north/south
#   slice-axes 1-2 = equatorial plane
#
# For the quantum section these are ordinary circles on the slice sphere.
#
# For the mutual-information section the same 3D slice directions are first
# mapped back to ORIGINAL 4D advantage coordinates, then the exact MI radial
# equality is solved there. Hence the MI guide curves deform correctly.

SHOW_QUANTUM_EQUATOR = False
SHOW_QUANTUM_PARALLELS = False
SHOW_QUANTUM_NORTH_SOUTH = False
SHOW_QUANTUM_MERIDIANS_EAST_WEST = False

SHOW_MI_EQUATOR = True
SHOW_MI_PARALLELS = True
SHOW_MI_NORTH_SOUTH = True
SHOW_MI_MERIDIANS_EAST_WEST = True

PARALLEL_LATITUDE_DEG = 30.0
MERIDIAN_LONGITUDE_DEG = 45.0

QUANTUM_GUIDE_COLOR = QUANTUM_EDGE_COLOR
QUANTUM_GUIDE_WIDTH = 1.2
QUANTUM_GUIDE_OPACITY = 0.80

MI_GUIDE_COLOR = MUTUAL_INFORMATION_EDGE_COLOR
MI_GUIDE_WIDTH = 1.2
MI_GUIDE_OPACITY = 0.90

GUIDE_RESOLUTION = 360

# =============================================================================
# CAMERA / LIGHTING
# =============================================================================

CAMERA_POSITION = (3.0, 2.0, 1.0)
CAMERA_FOCAL_POINT = (0.0, 0.0, 0.0)
CAMERA_UP = (0.0, 0.0, 1.0)
CAMERA_ZOOM = 1.02
PARALLEL_PROJECTION = False

KEY_LIGHT_POSITION = (4.0, 3.0, 5.0)
FILL_LIGHT_POSITION = (-3.0, -2.0, 2.0)


# =============================================================================
# LOAD CLASSICAL GEOMETRY ENGINE
# =============================================================================

def load_geometry_module():
    if not BASE_SCRIPT.exists():
        raise FileNotFoundError(
            f"Geometry script not found:\n{BASE_SCRIPT}\n\n"
            "Place this file next to "
            "n4_rac_cross_section_axis_inset_planar_edges.py"
        )

    spec = importlib.util.spec_from_file_location("rac_geom", BASE_SCRIPT)

    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import {BASE_SCRIPT}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# =============================================================================
# CAMERA / IMAGE HELPERS
# =============================================================================

def normalize_slice(normal, offset):
    normal = np.asarray(normal, dtype=float)
    norm = np.linalg.norm(normal)

    if norm == 0:
        raise ValueError("Slice normal cannot be zero.")

    return normal / norm, float(offset) / norm


def apply_camera(plotter):
    plotter.camera.position = CAMERA_POSITION
    plotter.camera.focal_point = CAMERA_FOCAL_POINT
    plotter.camera.up = CAMERA_UP

    if PARALLEL_PROJECTION:
        plotter.enable_parallel_projection()
    else:
        plotter.disable_parallel_projection()

    plotter.camera.zoom(CAMERA_ZOOM)


def apply_lighting(plotter):
    plotter.remove_all_lights()

    plotter.add_light(
        pv.Light(
            position=KEY_LIGHT_POSITION,
            focal_point=CAMERA_FOCAL_POINT,
            intensity=1.0,
        )
    )

    plotter.add_light(
        pv.Light(
            position=FILL_LIGHT_POSITION,
            focal_point=CAMERA_FOCAL_POINT,
            intensity=0.38,
        )
    )


def rgba_crop(image, pad=30):
    image = np.asarray(image)

    if image.ndim != 3 or image.shape[2] != 4:
        return image

    ys, xs = np.where(image[:, :, 3] > 2)

    if not len(xs):
        return image

    return image[
        max(0, ys.min() - pad): min(image.shape[0], ys.max() + pad + 1),
        max(0, xs.min() - pad): min(image.shape[1], xs.max() + pad + 1),
    ]


# =============================================================================
# SLICE LABELS / ORIENTED INTEGER BASIS
# =============================================================================

def slice_label(normal, offset):
    n = np.asarray(normal, dtype=float)
    nz = np.flatnonzero(np.abs(n) > 1e-9)

    if len(nz) == 1:
        i = int(nz[0])
        return rf"$c_{i+1}={offset/n[i]:g}$"

    if abs(offset) < 1e-9 and len(nz) == 2:
        i, j = map(int, nz)

        if np.isclose(n[i], -n[j]):
            return rf"$c_{i+1}=c_{j+1}$"

        if np.isclose(n[i], n[j]):
            return rf"$c_{i+1}=-c_{j+1}$"

    terms = []

    for i, a in enumerate(n):
        if abs(a) < 1e-9:
            continue

        sign = "+" if a > 0 and terms else ""
        coeff = "" if np.isclose(abs(a), 1) else f"{abs(a):g}"

        if a < 0:
            sign = "-"

        terms.append(f"{sign}{coeff}c_{i+1}")

    return "$" + "".join(terms) + rf"={offset:g}$"


def _primitive_integer_vector(v):
    v = np.asarray(v, dtype=np.int64)
    nz = np.abs(v[v != 0])

    if len(nz) == 0:
        raise ValueError("Cannot reduce zero vector.")

    g = int(nz[0])

    for value in nz[1:]:
        g = int(np.gcd(g, int(value)))

    return v // g


def _orient_at_construction(v):
    v = np.asarray(v, dtype=np.int64)
    nz = np.flatnonzero(v)

    if len(nz) and v[nz[0]] < 0:
        v = -v

    return v


def integer_slice_normal(raw_normal, max_denominator=64):
    vals = [
        Fraction(float(x)).limit_denominator(max_denominator)
        for x in np.asarray(raw_normal, dtype=float)
    ]

    denom = 1

    for f in vals:
        denom = lcm(denom, f.denominator)

    ints = np.array(
        [
            int(f.numerator * (denom // f.denominator))
            for f in vals
        ],
        dtype=np.int64,
    )

    nz = np.abs(ints[ints != 0])

    if len(nz) == 0:
        raise ValueError("Slice normal cannot be zero.")

    g = int(nz[0])

    for value in nz[1:]:
        g = gcd(g, int(value))

    return ints // g


def sparse_oriented_basis_4d(raw_normal):
    """
    Construct three sparse, mutually orthogonal integer directions spanning
    raw_normal · c = 0.
    """
    n = integer_slice_normal(raw_normal)

    active = [int(i) for i in np.flatnonzero(n)]
    zero = [i for i in range(4) if n[i] == 0]

    vectors = []

    if len(active) >= 2:
        previous = [active[0]]

        for j in active[1:]:
            v = np.zeros(4, dtype=np.int64)
            s = 0

            for i in previous:
                v[i] = n[i] * n[j]
                s += int(n[i]) ** 2

            v[j] = -s
            v = _orient_at_construction(_primitive_integer_vector(v))
            vectors.append(v)
            previous.append(j)

    for j in zero:
        v = np.zeros(4, dtype=np.int64)
        v[j] = 1
        vectors.append(v)

    if len(vectors) != 3:
        raise RuntimeError(
            f"Expected 3 slice directions, got {len(vectors)}."
        )

    for v in vectors:
        if int(np.dot(n, v)) != 0:
            raise RuntimeError(f"{v} is not perpendicular to {n}.")

    for i in range(3):
        for j in range(i + 1, 3):
            if int(np.dot(vectors[i], vectors[j])) != 0:
                raise RuntimeError(
                    f"Basis vectors {vectors[i]} and {vectors[j]} "
                    "are not orthogonal."
                )

    return vectors


def normalized_basis_matrix(vectors4):
    return np.column_stack([
        np.asarray(v, dtype=float) / np.linalg.norm(v)
        for v in vectors4
    ])


def format_direction(v):
    return "(" + ",".join(str(int(x)) for x in v) + ")"


def add_oriented_axes(plotter, axis_vectors4):
    if not SHOW_MAIN_AXES:
        return

    for axis_index, (d3, v4) in enumerate(
        zip(np.eye(3), axis_vectors4)
    ):
        end = d3 * MAIN_AXIS_LENGTH

        plotter.add_mesh(
            pv.Line((0, 0, 0), end),
            color="black",
            line_width=MAIN_AXIS_WIDTH,
            lighting=False,
        )

        if not SHOW_AXIS_DIRECTION_LABELS:
            continue

        label_pos = d3 * (
            MAIN_AXIS_LENGTH * MAIN_AXIS_LABEL_SCALE
        )

        camera_pos = np.asarray(
            plotter.camera.position,
            dtype=float,
        )
        camera_focal = np.asarray(
            plotter.camera.focal_point,
            dtype=float,
        )
        camera_up = np.asarray(
            plotter.camera.up,
            dtype=float,
        )

        view = camera_focal - camera_pos
        view /= np.linalg.norm(view)

        screen_right = np.cross(view, camera_up)
        screen_right /= np.linalg.norm(screen_right)

        screen_up = np.cross(screen_right, view)
        screen_up /= np.linalg.norm(screen_up)

        dx, dy = LABEL_OFFSETS[axis_index]

        label_pos = (
            label_pos
            + dx * screen_right
            + dy * screen_up
        )

        plotter.add_point_labels(
            np.asarray([label_pos]),
            [format_direction(v4)],
            point_size=0,
            font_size=MAIN_AXIS_LABEL_FONT_SIZE,
            bold=False,
            show_points=False,
            always_visible=True,
            shape=None,
            text_color="black",
        )


# =============================================================================
# mutual-information IN ORIGINAL 4D COORDINATES
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
    p = 0.5 * (1.0 + np.asarray(c, dtype=float))
    return 1.0 - binary_entropy(p)


def mi_sum_4d(points4):
    points4 = np.asarray(points4, dtype=float)

    return np.sum(
        mutual_information_from_advantage(points4),
        axis=-1,
    )


def solve_mi_radius_in_slice(directions3, basis4x3):
    """
    Solve the MI boundary radially within a zero-offset 3D slice.

    directions3:
        N x 3 directions in rendered slice coordinates.

    basis4x3:
        orthonormal columns giving those directions in original R^4.

    For each 3D direction u3:
        u4 = basis @ u3

    then solve:
        sum_i I(r u4_i) = 1.
    """
    directions3 = np.asarray(directions3, dtype=float)

    norms = np.linalg.norm(directions3, axis=1)
    u3 = directions3 / norms[:, None]

    # 3D slice directions -> original 4D coordinates.
    u4 = u3 @ basis4x3.T

    # Numerical cleanup.
    u4 /= np.linalg.norm(u4, axis=1)[:, None]

    lo = np.zeros(len(u4), dtype=float)

    # Largest r before any original advantage coordinate leaves [-1,1].
    hi = 1.0 / np.max(np.abs(u4), axis=1)

    for _ in range(MI_BISECTION_STEPS):
        mid = 0.5 * (lo + hi)

        values = mi_sum_4d(
            mid[:, None] * u4
        )

        inside = values < 1.0

        lo[inside] = mid[inside]
        hi[~inside] = mid[~inside]

    return 0.5 * (lo + hi)


# =============================================================================
# SURFACE MESHES
# =============================================================================

def make_quantum_surface(radius=1.0):
    return pv.Sphere(
        radius=radius,
        center=(0.0, 0.0, 0.0),
        theta_resolution=QUANTUM_SPHERE_RESOLUTION,
        phi_resolution=QUANTUM_SPHERE_RESOLUTION,
    )


def make_mi_surface_in_slice(basis4x3):
    """
    Radially deform a unit sphere in the rendered 3D slice until the
    corresponding ORIGINAL 4D points satisfy sum_i I_i = 1.
    """
    seed = pv.Sphere(
        radius=1.0,
        center=(0.0, 0.0, 0.0),
        theta_resolution=MI_THETA_RESOLUTION,
        phi_resolution=MI_PHI_RESOLUTION,
    )

    directions3 = np.asarray(seed.points, dtype=float)
    radii = solve_mi_radius_in_slice(
        directions3,
        basis4x3,
    )

    unit3 = (
        directions3
        / np.linalg.norm(directions3, axis=1)[:, None]
    )

    surface = seed.copy(deep=True)
    surface.points = unit3 * radii[:, None]

    return surface


# =============================================================================
# GUIDE LINES
# =============================================================================

def closed_polyline(points):
    points = np.asarray(points, dtype=float)

    closed = np.vstack([points, points[0]])
    n = len(closed)

    poly = pv.PolyData(closed)

    poly.lines = np.hstack(
        ([n], np.arange(n, dtype=np.int64))
    )

    return poly


def guide_direction_sets():
    """
    Return named guide direction curves on a unit sphere in rendered
    3D slice coordinates.
    """
    theta = np.linspace(
        0.0,
        2.0 * np.pi,
        GUIDE_RESOLUTION,
        endpoint=False,
    )

    curves = {}

    # Equator.
    curves["equator"] = [
        np.column_stack([
            np.cos(theta),
            np.sin(theta),
            np.zeros_like(theta),
        ])
    ]

    # +/- latitude parallels.
    lat = np.deg2rad(PARALLEL_LATITUDE_DEG)
    r_xy = np.cos(lat)
    z_abs = np.sin(lat)

    curves["parallels"] = [
        np.column_stack([
            r_xy * np.cos(theta),
            r_xy * np.sin(theta),
            np.full_like(theta, z),
        ])
        for z in (+z_abs, -z_abs)
    ]

    def meridian(phi):
        return np.column_stack([
            np.cos(theta) * np.cos(phi),
            np.cos(theta) * np.sin(phi),
            np.sin(theta),
        ])

    curves["north_south"] = [
        meridian(0.0),
        meridian(0.5 * np.pi),
    ]

    lon = np.deg2rad(MERIDIAN_LONGITUDE_DEG)

    curves["east_west"] = [
        meridian(+lon),
        meridian(-lon),
    ]

    return curves


def add_quantum_guides(plotter, radius=1.0):
    curves = guide_direction_sets()

    selected = []

    if SHOW_QUANTUM_EQUATOR:
        selected.extend(curves["equator"])

    if SHOW_QUANTUM_PARALLELS:
        selected.extend(curves["parallels"])

    if SHOW_QUANTUM_NORTH_SOUTH:
        selected.extend(curves["north_south"])

    if SHOW_QUANTUM_MERIDIANS_EAST_WEST:
        selected.extend(curves["east_west"])

    for directions in selected:
        points = radius * directions

        plotter.add_mesh(
            closed_polyline(points),
            color=QUANTUM_GUIDE_COLOR,
            line_width=QUANTUM_GUIDE_WIDTH,
            opacity=QUANTUM_GUIDE_OPACITY,
            lighting=False,
        )


def mi_curve_from_slice_directions(
    directions3,
    basis4x3,
):
    directions3 = np.asarray(directions3, dtype=float)

    unit3 = (
        directions3
        / np.linalg.norm(directions3, axis=1)[:, None]
    )

    radii = solve_mi_radius_in_slice(
        unit3,
        basis4x3,
    )

    return unit3 * radii[:, None]


def add_mi_guides(plotter, basis4x3):
    curves = guide_direction_sets()

    selected = []

    if SHOW_MI_EQUATOR:
        selected.extend(curves["equator"])

    if SHOW_MI_PARALLELS:
        selected.extend(curves["parallels"])

    if SHOW_MI_NORTH_SOUTH:
        selected.extend(curves["north_south"])

    if SHOW_MI_MERIDIANS_EAST_WEST:
        selected.extend(curves["east_west"])

    for directions in selected:
        points = mi_curve_from_slice_directions(
            directions,
            basis4x3,
        )

        plotter.add_mesh(
            closed_polyline(points),
            color=MI_GUIDE_COLOR,
            line_width=MI_GUIDE_WIDTH,
            opacity=MI_GUIDE_OPACITY,
            lighting=False,
        )


# =============================================================================
# CLASSICAL SECTION
# =============================================================================

def add_classical_section(
    plotter,
    geom,
    vertices4,
    normal,
    offset,
    basis4x3,
):
    """
    Add the classical polytope section reprojected through the SAME oriented
    basis used for the quantum and MI surfaces.
    """
    _, points4, _, _ = geom.compute_section(
        vertices4,
        normal,
        offset,
    )

    x0 = offset * normal

    points3 = geom.to_slice_coordinates(
        points4,
        x0,
        basis4x3,
    )

    hull3 = ConvexHull(points3)
    mesh = geom.make_mesh(points3, hull3)

    plotter.add_mesh(
        mesh,
        color=CLASSICAL_COLOR,
        opacity=CLASSICAL_OPACITY,
        smooth_shading=False,
        show_edges=False,
    )

    if SHOW_CLASSICAL_EDGES:
        old = (
            geom.EDGE_COLOR,
            geom.EDGE_WIDTH,
            geom.SHOW_EDGES,
        )

        geom.EDGE_COLOR = CLASSICAL_EDGE_COLOR
        geom.EDGE_WIDTH = CLASSICAL_EDGE_WIDTH
        geom.SHOW_EDGES = True

        geom.add_feature_edges(
            plotter,
            points3,
            hull3,
        )

        (
            geom.EDGE_COLOR,
            geom.EDGE_WIDTH,
            geom.SHOW_EDGES,
        ) = old

    if SHOW_CLASSICAL_VERTICES:
        old_size = geom.ORIGINAL_VERTEX_SIZE
        old_colors = dict(geom.VERTEX_TYPE_COLORS)

        geom.ORIGINAL_VERTEX_SIZE = VERTEX_SIZE
        geom.VERTEX_TYPE_COLORS.update(
            VERTEX_COLORS
        )

        geom.add_original_vertices(
            plotter,
            vertices4,
            normal,
            offset,
            x0,
            basis4x3,
        )

        geom.ORIGINAL_VERTEX_SIZE = old_size
        geom.VERTEX_TYPE_COLORS.clear()
        geom.VERTEX_TYPE_COLORS.update(
            old_colors
        )


# =============================================================================
# PANEL RENDER
# =============================================================================

def render_panel(
    geom,
    vertices4,
    raw_normal,
    raw_offset,
):
    normal, offset = normalize_slice(
        raw_normal,
        raw_offset,
    )

    if abs(offset) > 1e-12:
        raise NotImplementedError(
            "This comparison renderer currently assumes zero-offset slices. "
            "All four publication slices satisfy this."
        )

    axis_vectors4 = sparse_oriented_basis_4d(
        raw_normal
    )

    basis4x3 = normalized_basis_matrix(
        axis_vectors4
    )

    p = pv.Plotter(
        off_screen=True,
        window_size=PANEL_RENDER_SIZE,
    )

    p.set_background(BACKGROUND)
    p.image_transparent_background = True

    apply_lighting(p)

    # Largest boundary first.
    if SHOW_MUTUAL_INFORMATION:
        print("      building MI section...")
        mi_surface = make_mi_surface_in_slice(
            basis4x3
        )

        p.add_mesh(
            mi_surface,
            color=MUTUAL_INFORMATION_COLOR,
            opacity=MUTUAL_INFORMATION_OPACITY,
            smooth_shading=True,
            show_edges=False,
            specular=0.10,
        )

        add_mi_guides(
            p,
            basis4x3,
        )

    if SHOW_QUANTUM:
        quantum_surface = make_quantum_surface(
            radius=1.0
        )

        p.add_mesh(
            quantum_surface,
            color=QUANTUM_COLOR,
            opacity=QUANTUM_OPACITY,
            smooth_shading=True,
            show_edges=False,
            specular=0.12,
        )

        add_quantum_guides(
            p,
            radius=1.0,
        )

    if SHOW_CLASSICAL:
        add_classical_section(
            p,
            geom,
            vertices4,
            normal,
            offset,
            basis4x3,
        )

    add_oriented_axes(
        p,
        axis_vectors4,
    )

    print(
        "      oriented slice axes:",
        ", ".join(
            format_direction(v)
            for v in axis_vectors4
        ),
    )

    apply_camera(p)
    p.render()

    image = p.screenshot(
        return_img=True,
        transparent_background=True,
    )

    p.close()

    return rgba_crop(
        image,
        pad=34,
    )


# =============================================================================
# FIGURE COMPOSITION
# =============================================================================

def add_shared_shape_legend(fig):
    """
    Compact shared legend in the same bottom-strip location as Figure 4.
    """
    ax = fig.add_axes(
        [0.075, 0.018, 0.85, 0.065]
    )
    ax.set_axis_off()

    entries = []

    if SHOW_CLASSICAL:
        entries.append((
            CLASSICAL_EDGE_COLOR,
            "Classical polytope",
        ))

    if SHOW_QUANTUM:
        entries.append((
            QUANTUM_EDGE_COLOR,
            r"Quantum  $\sum_i c_i^2=1$",
        ))

    if SHOW_MUTUAL_INFORMATION:
        entries.append((
            MUTUAL_INFORMATION_EDGE_COLOR,
            r"mutual-information  "
            r"$\sum_{i=1}^{4}[1-h_2((1+c_i)/2)]=1$",
        ))

    if not entries:
        return

    xs = np.linspace(
        0.08,
        0.72,
        len(entries),
    )

    for x, (color, label) in zip(
        xs,
        entries,
    ):
        ax.plot(
            [x, x + 0.055],
            [0.50, 0.50],
            color=color,
            linewidth=4.0,
            transform=ax.transAxes,
            solid_capstyle="round",
        )

        ax.text(
            x + 0.072,
            0.50,
            label,
            color=color,
            fontsize=11.0,
            va="center",
            transform=ax.transAxes,
        )


def compose(images):
    fig = plt.figure(
        figsize=FIGURE_SIZE_INCH,
        dpi=DPI,
        facecolor="white",
    )

    fig.text(
        .035,
        .965,
        "n=4 advantage-space cross-sections",
        fontsize=22,
        fontweight="bold",
        ha="left",
        va="top",
    )

    fig.text(
        .035,
        .928,
        "Classical, quantum and mutual-information boundaries "
        "in four 3D cuts through the same 4D advantage space",
        fontsize=14.5,
        ha="left",
        va="top",
    )

    for (
        letter,
        normal,
        offset,
    ), image, box in zip(
        SLICES,
        images,
        PANEL_BOXES,
    ):
        ax = fig.add_axes(box)

        ax.imshow(image)
        ax.set_axis_off()

        ax.text(
            .015,
            1.015,
            f"{letter}",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=14,
            fontweight="bold",
        )

        ax.text(
            .09,
            1.015,
            slice_label(normal, offset),
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=14,
        )

    add_shared_shape_legend(fig)

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
        "Rendering n=4 classical / quantum / "
        "mutual-information cross-sections..."
    )

    print(
        f"  classical={SHOW_CLASSICAL} "
        f"(opacity={CLASSICAL_OPACITY})\n"
        f"  quantum={SHOW_QUANTUM} "
        f"(opacity={QUANTUM_OPACITY})\n"
        f"  mutual-information={SHOW_MUTUAL_INFORMATION} "
        f"(opacity={MUTUAL_INFORMATION_OPACITY})"
    )

    geom = load_geometry_module()

    # Disable GUI/layout behavior in imported geometry module.
    geom.SHOW_LEGEND = False
    geom.SHOW_TITLE = False
    geom.SHOW_AXIS_INSET = False
    geom.SHOW_AXES = False

    vertices4 = geom.build_vertices()

    images = []

    for letter, normal, offset in SLICES:
        print(
            f"Rendering {letter}: "
            f"normal={tuple(normal)}, offset={offset:g}"
        )

        images.append(
            render_panel(
                geom,
                vertices4,
                normal,
                offset,
            )
        )

    compose(images)

    print(f"Saved: {OUTPUT}")
    print(
        f"Final size: "
        f"{int(FIGURE_SIZE_INCH[0] * DPI)} x "
        f"{int(FIGURE_SIZE_INCH[1] * DPI)} px"
    )


if __name__ == "__main__":
    main()