"""
n=3 RAC advantage-space comparison
===================================

Publication-style comparison of three nested regions in 3D advantage space:

    Classical:
        convex hull of the n=3 one-bit RAC vertices

    Quantum:
        c1^2 + c2^2 + c3^2 = 1

    Mutual information:
        sum_i [1 - h2((1 + c_i)/2)] = 1

The layout and camera are adapted from the existing n=3 publication figure.

Dependencies
------------
pip install numpy scipy pyvista matplotlib
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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
# OPACITY
# -----------------------------------------------------------------------------

CLASSICAL_OPACITY = 0.20
QUANTUM_OPACITY = 0.10
MUTUAL_INFORMATION_OPACITY = 0.65

# -----------------------------------------------------------------------------
# OPTIONAL DETAIL
# -----------------------------------------------------------------------------

SHOW_CLASSICAL_EDGES = True
SHOW_CLASSICAL_VERTICES = False
SHOW_MAIN_AXES = True

# -----------------------------------------------------------------------------
# SURFACE GUIDE LINES
# -----------------------------------------------------------------------------
# Geographic convention: c3 is north/south; c1-c2 is the equatorial plane.
# Available guides: equator, +/-45-degree parallels, principal N/S
# meridians, and +/-45-degree east/west meridians.
#
# Configure quantum and mutual-information surfaces independently.

SHOW_QUANTUM_EQUATOR = False
SHOW_QUANTUM_PARALLELS_45 = False
SHOW_QUANTUM_NORTH_SOUTH = False
SHOW_QUANTUM_MERIDIANS_45_EAST_WEST = False

SHOW_MI_EQUATOR = True
SHOW_MI_PARALLELS_45 = True
SHOW_MI_NORTH_SOUTH = True
SHOW_MI_MERIDIANS_45_EAST_WEST = True

# Latitude / longitude angles used by the extra guides.
PARALLEL_LATITUDE_DEG = 30.0
MERIDIAN_LONGITUDE_DEG = 45.0

QUANTUM_GUIDE_COLOR = "#8A8A8A"
QUANTUM_GUIDE_WIDTH = 1.2
QUANTUM_GUIDE_OPACITY = 0.80

MI_GUIDE_COLOR = "#B78B12"
MI_GUIDE_WIDTH = 1.2
MI_GUIDE_OPACITY = 0.90

GUIDE_RESOLUTION = 360

# Smooth-surface resolution. Increase for a denser export.
QUANTUM_THETA_RESOLUTION = 180
QUANTUM_PHI_RESOLUTION = 120

# Number of vectorized bisection steps used to solve the mutual-information
# radial boundary. 55 is already far beyond the visual precision required.
MI_BISECTION_STEPS = 55


# =============================================================================
# OUTPUT / LAYOUT
# =============================================================================

OUTPUT = Path(__file__).with_name("Figure_n3_classical_quantum_mutual_information_3D.png")

FIGURE_SIZE_INCH = (15.36, 10.24)
DPI = 200
PANEL_RENDER_SIZE = (1700, 1450)

LEFT_IMAGE_BOX = [0.025, 0.115, 0.60, 0.755]
RIGHT_LEGEND_BOX = [0.625, 0.47, 0.35, 0.30]
RIGHT_AXIS_BOX = [0.625, 0.08, 0.35, 0.34]


# =============================================================================
# APPEARANCE
# =============================================================================

# Palette chosen to fit the earlier RAC figures and the n=2 comparison:
# blue-grey classical body, warm gold quantum sphere, pale warm MI envelope.

CLASSICAL_COLOR = "#AFC8D3"
CLASSICAL_EDGE_COLOR = "#222222"
CLASSICAL_EDGE_WIDTH = 1.5

QUANTUM_COLOR = "#F1B733"
QUANTUM_EDGE_COLOR = "#C69212"

MUTUAL_INFORMATION_COLOR = "#F4D77D"
MUTUAL_INFORMATION_EDGE_COLOR = "#8C6B13"

AXIS_COLORS = ("crimson", "green", "royalblue")
AXIS_LENGTH = 1.28
AXIS_WIDTH = 1.5
AXIS_LABEL_FONT_SIZE = 15

AXIS_LABEL_OFFSETS = [
    (-0.12, -0.01),
    ( 0.08, -0.02),
    (-0.02,  0.06),
]

VERTEX_SIZE = 17
AXIS_VERTEX_COLOR = "crimson"
MAJORITY_VERTEX_COLOR = "darkorange"

BACKGROUND = "white"


# =============================================================================
# CAMERA / LIGHTING
# =============================================================================

CAMERA_POSITION = (3.0, 2.0, 1.0)
CAMERA_FOCAL_POINT = (0.0, 0.0, 0.0)
CAMERA_UP = (0.0, 0.0, 1.0)
CAMERA_ZOOM = 1.03

KEY_LIGHT_POSITION = (4.0, 3.0, 5.0)
FILL_LIGHT_POSITION = (-3.0, -2.0, 2.0)


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


# =============================================================================
# BASIC RENDER HELPERS
# =============================================================================

def apply_camera(plotter):
    plotter.camera.position = CAMERA_POSITION
    plotter.camera.focal_point = CAMERA_FOCAL_POINT
    plotter.camera.up = CAMERA_UP
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


def camera_frame(plotter):
    """Return screen-right and screen-up directions in world coordinates."""
    camera_pos = np.asarray(plotter.camera.position, dtype=float)
    focal = np.asarray(plotter.camera.focal_point, dtype=float)
    up_hint = np.asarray(plotter.camera.up, dtype=float)

    view = focal - camera_pos
    view /= np.linalg.norm(view)

    right = np.cross(view, up_hint)
    right /= np.linalg.norm(right)

    screen_up = np.cross(right, view)
    screen_up /= np.linalg.norm(screen_up)

    return right, screen_up


def rgba_crop(image, pad=30):
    """Crop transparent margins around a PyVista RGBA screenshot."""
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
# CLASSICAL GEOMETRY
# =============================================================================

def make_classical_polytope():
    hull = ConvexHull(ALL_VERTICES)

    triangles = hull.simplices.astype(np.int64)
    faces = np.column_stack(
        [np.full(len(triangles), 3, dtype=np.int64), triangles]
    ).ravel()

    mesh = pv.PolyData(ALL_VERTICES, faces)
    return mesh, hull


def true_edges_from_hull(hull):
    """
    Recover true polygon edges rather than Qhull triangulation diagonals.
    """
    equations = np.asarray(hull.equations, dtype=float)
    normals = equations[:, :3]
    offsets = equations[:, 3]

    lengths = np.linalg.norm(normals, axis=1)
    normals = normals / lengths[:, None]
    offsets = offsets / lengths

    groups = []
    tol = 1e-8

    for tri_id, (normal, offset) in enumerate(zip(normals, offsets)):
        placed = False

        for group in groups:
            if (
                np.linalg.norm(normal - group["normal"]) < tol
                and abs(offset - group["offset"]) < tol
            ):
                group["triangles"].append(tri_id)
                placed = True
                break

        if not placed:
            groups.append({
                "normal": normal.copy(),
                "offset": float(offset),
                "triangles": [tri_id],
            })

    true_edges = set()

    for group in groups:
        counts = {}

        for tri_id in group["triangles"]:
            tri = hull.simplices[tri_id]

            for a, b in (
                (int(tri[0]), int(tri[1])),
                (int(tri[1]), int(tri[2])),
                (int(tri[2]), int(tri[0])),
            ):
                edge = tuple(sorted((a, b)))
                counts[edge] = counts.get(edge, 0) + 1

        for edge, count in counts.items():
            if count == 1:
                true_edges.add(edge)

    return sorted(true_edges)


def add_classical_edges(plotter, hull):
    if not SHOW_CLASSICAL_EDGES:
        return

    edges = true_edges_from_hull(hull)

    lines = np.asarray(
        [[2, i, j] for i, j in edges],
        dtype=np.int64,
    ).ravel()

    edge_mesh = pv.PolyData(ALL_VERTICES.copy())
    edge_mesh.lines = lines

    plotter.add_mesh(
        edge_mesh,
        color=CLASSICAL_EDGE_COLOR,
        line_width=CLASSICAL_EDGE_WIDTH,
        lighting=False,
    )


def add_classical_vertices(plotter):
    if not SHOW_CLASSICAL_VERTICES:
        return

    plotter.add_mesh(
        pv.PolyData(AXIS_VERTICES),
        color=AXIS_VERTEX_COLOR,
        point_size=VERTEX_SIZE,
        render_points_as_spheres=True,
        lighting=True,
    )

    plotter.add_mesh(
        pv.PolyData(MAJORITY_VERTICES),
        color=MAJORITY_VERTEX_COLOR,
        point_size=VERTEX_SIZE,
        render_points_as_spheres=True,
        lighting=True,
    )


# =============================================================================
# QUANTUM SPHERE
# =============================================================================

def make_quantum_sphere():
    return pv.Sphere(
        radius=1.0,
        center=(0.0, 0.0, 0.0),
        theta_resolution=QUANTUM_THETA_RESOLUTION,
        phi_resolution=QUANTUM_PHI_RESOLUTION,
    )


# =============================================================================
# MUTUAL-INFORMATION BOUNDARY
# =============================================================================

def binary_entropy(p):
    """Vectorized binary entropy h2(p), including p=0 and p=1."""
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
    """
    Mutual information for a uniform binary bit through a symmetric channel,

        c = 2P - 1.
    """
    p = 0.5 * (1.0 + np.asarray(c, dtype=float))
    return 1.0 - binary_entropy(p)


def mi_sum(points):
    """
    Sum_i I_i for an array of (...,3) advantage vectors.
    """
    points = np.asarray(points, dtype=float)
    return np.sum(
        mutual_information_from_advantage(points),
        axis=-1,
    )


def solve_mi_radius(directions):
    """
    Solve the radial equation

        sum_i I(r * direction_i) = 1

    independently for every unit direction.

    The MI body is sign-symmetric and star-shaped around the origin.
    Along each direction the largest admissible radius before any coordinate
    leaves [-1,1] is

        r_max = 1 / max_i |direction_i|.

    At that point at least one coordinate is ±1 and already contributes one
    full bit, so the equality is always bracketed.
    """
    directions = np.asarray(directions, dtype=float)

    norms = np.linalg.norm(directions, axis=1)
    u = directions / norms[:, None]

    lo = np.zeros(len(u), dtype=float)
    hi = 1.0 / np.max(np.abs(u), axis=1)

    for _ in range(MI_BISECTION_STEPS):
        mid = 0.5 * (lo + hi)
        values = mi_sum(mid[:, None] * u)

        # f(r) = MI_sum - 1 is monotone increasing.
        inside = values < 1.0
        lo[inside] = mid[inside]
        hi[~inside] = mid[~inside]

    return 0.5 * (lo + hi)


def make_mutual_information_surface():
    """
    Start from a triangulated unit sphere and radially deform every vertex
    until sum_i I_i = 1.  Reusing the sphere topology gives a smooth, closed,
    full four-octant surface without seams.
    """
    sphere = pv.Sphere(
        radius=1.0,
        center=(0.0, 0.0, 0.0),
        theta_resolution=QUANTUM_THETA_RESOLUTION,
        phi_resolution=QUANTUM_PHI_RESOLUTION,
    )

    directions = np.asarray(sphere.points, dtype=float)
    radii = solve_mi_radius(directions)

    unit = directions / np.linalg.norm(directions, axis=1)[:, None]

    surface = sphere.copy(deep=True)
    surface.points = unit * radii[:, None]

    return surface



# =============================================================================
# SURFACE GUIDE LINES
# =============================================================================

def closed_polyline(points):
    """Create one closed PyVista polyline through the supplied 3D points."""
    points = np.asarray(points, dtype=float)

    closed = np.vstack([points, points[0]])
    n = len(closed)

    poly = pv.PolyData(closed)
    poly.lines = np.hstack(([n], np.arange(n, dtype=np.int64)))
    return poly


def add_quantum_guides(plotter):
    """
    Add configurable geographic-style guides to the unit quantum sphere.

    Available guides
    ----------------
    Equator:
        latitude 0 deg

    +/-45 deg parallels:
        latitude +PARALLEL_LATITUDE_DEG
        latitude -PARALLEL_LATITUDE_DEG

    North/South great circles:
        longitude 0 deg
        longitude 90 deg

    +/-45 deg east/west meridians:
        longitude +MERIDIAN_LONGITUDE_DEG
        longitude -MERIDIAN_LONGITUDE_DEG

    The c3 axis is treated as the north/south axis.
    """
    theta = np.linspace(
        0.0,
        2.0 * np.pi,
        GUIDE_RESOLUTION,
        endpoint=False,
    )

    def add_curve(points):
        plotter.add_mesh(
            closed_polyline(points),
            color=QUANTUM_GUIDE_COLOR,
            line_width=QUANTUM_GUIDE_WIDTH,
            opacity=QUANTUM_GUIDE_OPACITY,
            lighting=False,
        )

    # Equator: latitude = 0.
    if SHOW_QUANTUM_EQUATOR:
        equator = np.column_stack([
            np.cos(theta),
            np.sin(theta),
            np.zeros_like(theta),
        ])
        add_curve(equator)

    # Latitude parallels at +/- selected angle.
    if SHOW_QUANTUM_PARALLELS_45:
        lat = np.deg2rad(PARALLEL_LATITUDE_DEG)
        r_xy = np.cos(lat)
        z_abs = np.sin(lat)

        for z in (+z_abs, -z_abs):
            parallel = np.column_stack([
                r_xy * np.cos(theta),
                r_xy * np.sin(theta),
                np.full_like(theta, z),
            ])
            add_curve(parallel)

    # Helper for a full north/south great circle at longitude phi.
    def meridian(phi):
        t = theta
        return np.column_stack([
            np.cos(t) * np.cos(phi),
            np.cos(t) * np.sin(phi),
            np.sin(t),
        ])

    # The two principal north/south great circles.
    if SHOW_QUANTUM_NORTH_SOUTH:
        add_curve(meridian(0.0))
        add_curve(meridian(0.5 * np.pi))

    # Extra +/- longitude guides.
    if SHOW_QUANTUM_MERIDIANS_45_EAST_WEST:
        lon = np.deg2rad(MERIDIAN_LONGITUDE_DEG)
        add_curve(meridian(+lon))
        add_curve(meridian(-lon))


def mi_surface_curve(directions):
    """
    Map a set of directions radially onto the mutual-information boundary.
    """
    directions = np.asarray(directions, dtype=float)

    norms = np.linalg.norm(directions, axis=1)
    unit = directions / norms[:, None]

    radii = solve_mi_radius(unit)
    return unit * radii[:, None]


def add_mutual_information_guides(plotter):
    """
    Add configurable geographic-style guides to the actual MI boundary.

    The guide directions use the same latitude/longitude construction as the
    quantum sphere. Every direction is then projected radially onto

        sum_i [1 - h2((1+c_i)/2)] = 1.

    Thus the MI guides deform with the true mutual-information surface.

    Available guides
    ----------------
    Equator:
        latitude 0 deg

    +/-45 deg parallels:
        latitude +/- PARALLEL_LATITUDE_DEG

    North/South curves:
        longitude 0 deg and 90 deg

    +/-45 deg east/west:
        longitude +/- MERIDIAN_LONGITUDE_DEG
    """
    theta = np.linspace(
        0.0,
        2.0 * np.pi,
        GUIDE_RESOLUTION,
        endpoint=False,
    )

    def add_curve_from_directions(directions):
        points = mi_surface_curve(directions)
        plotter.add_mesh(
            closed_polyline(points),
            color=MI_GUIDE_COLOR,
            line_width=MI_GUIDE_WIDTH,
            opacity=MI_GUIDE_OPACITY,
            lighting=False,
        )

    # Equator.
    if SHOW_MI_EQUATOR:
        directions = np.column_stack([
            np.cos(theta),
            np.sin(theta),
            np.zeros_like(theta),
        ])
        add_curve_from_directions(directions)

    # Latitude parallels.
    if SHOW_MI_PARALLELS_45:
        lat = np.deg2rad(PARALLEL_LATITUDE_DEG)
        r_xy = np.cos(lat)
        z_abs = np.sin(lat)

        for z in (+z_abs, -z_abs):
            directions = np.column_stack([
                r_xy * np.cos(theta),
                r_xy * np.sin(theta),
                np.full_like(theta, z),
            ])
            add_curve_from_directions(directions)

    # Full north/south great-circle directions at longitude phi.
    def meridian_directions(phi):
        t = theta
        return np.column_stack([
            np.cos(t) * np.cos(phi),
            np.cos(t) * np.sin(phi),
            np.sin(t),
        ])

    # Principal N/S directions.
    if SHOW_MI_NORTH_SOUTH:
        add_curve_from_directions(meridian_directions(0.0))
        add_curve_from_directions(meridian_directions(0.5 * np.pi))

    # +/-45 east/west directions.
    if SHOW_MI_MERIDIANS_45_EAST_WEST:
        lon = np.deg2rad(MERIDIAN_LONGITUDE_DEG)
        add_curve_from_directions(meridian_directions(+lon))
        add_curve_from_directions(meridian_directions(-lon))


# =============================================================================
# AXES
# =============================================================================

def add_coordinate_axes(plotter):
    if not SHOW_MAIN_AXES:
        return

    # Camera first, because text offsets are defined in screen coordinates.
    apply_camera(plotter)
    screen_right, screen_up = camera_frame(plotter)

    for i, direction in enumerate(np.eye(3)):
        end = direction * AXIS_LENGTH

        plotter.add_mesh(
            pv.Line((0.0, 0.0, 0.0), end),
            color=AXIS_COLORS[i],
            line_width=AXIS_WIDTH,
            lighting=False,
        )

        label_pos = end.copy()

        dx, dy = AXIS_LABEL_OFFSETS[i]
        label_pos = (
            label_pos
            + dx * screen_right
            + dy * screen_up
        )

        # Explicitly 1-indexed: c1, c2, c3.
        plotter.add_point_labels(
            np.asarray([label_pos]),
            [f"c{i+1}"],
            point_size=0,
            font_size=AXIS_LABEL_FONT_SIZE,
            bold=True,
            show_points=False,
            always_visible=True,
            shape=None,
            text_color=AXIS_COLORS[i],
        )


# =============================================================================
# 3D RENDER
# =============================================================================

def render_scene():
    p = pv.Plotter(
        off_screen=True,
        window_size=PANEL_RENDER_SIZE,
    )

    p.set_background(BACKGROUND)
    p.image_transparent_background = True
    apply_lighting(p)

    # Draw largest region first so the nested bodies remain readable.
    if SHOW_MUTUAL_INFORMATION:
        print("Building mutual-information surface...")
        mi_surface = make_mutual_information_surface()

        p.add_mesh(
            mi_surface,
            color=MUTUAL_INFORMATION_COLOR,
            opacity=MUTUAL_INFORMATION_OPACITY,
            smooth_shading=True,
            show_edges=False,
            specular=0.10,
        )

        add_mutual_information_guides(p)

    if SHOW_QUANTUM:
        quantum = make_quantum_sphere()

        p.add_mesh(
            quantum,
            color=QUANTUM_COLOR,
            opacity=QUANTUM_OPACITY,
            smooth_shading=True,
            show_edges=False,
            specular=0.12,
        )

        add_quantum_guides(p)

    if SHOW_CLASSICAL:
        classical_mesh, classical_hull = make_classical_polytope()

        p.add_mesh(
            classical_mesh,
            color=CLASSICAL_COLOR,
            opacity=CLASSICAL_OPACITY,
            smooth_shading=False,
            show_edges=False,
        )

        add_classical_edges(p, classical_hull)
        add_classical_vertices(p)

    add_coordinate_axes(p)

    apply_camera(p)
    p.render()

    image = p.screenshot(
        return_img=True,
        transparent_background=True,
    )

    p.close()
    return rgba_crop(image, pad=35)


# =============================================================================
# MATPLOTLIB COMPOSITION
# =============================================================================

def rounded_box(ax, edgecolor, linewidth=1.4):
    patch = FancyBboxPatch(
        (0.01, 0.01),
        0.98,
        0.98,
        boxstyle="round,pad=0.012,rounding_size=0.035",
        transform=ax.transAxes,
        facecolor="white",
        edgecolor=edgecolor,
        linewidth=linewidth,
    )
    ax.add_patch(patch)


def add_shape_legend(fig):
    ax = fig.add_axes(RIGHT_LEGEND_BOX)
    ax.set_axis_off()

    ax.text(
        0.02, 0.95,
        "Boundaries in advantage coordinates",
        transform=ax.transAxes,
        fontsize=15,
        fontweight="bold",
        ha="left",
        va="top",
    )

    rows = []

    if SHOW_MUTUAL_INFORMATION:
        rows.append((
            MUTUAL_INFORMATION_EDGE_COLOR,
            "Mutual information",
            r"$\sum_{i=1}^{3}[1-h_2((1+c_i)/2)]=1$",
        ))

    if SHOW_QUANTUM:
        rows.append((
            QUANTUM_EDGE_COLOR,
            "Quantum",
            r"$c_1^2+c_2^2+c_3^2=1$",
        ))

    if SHOW_CLASSICAL:
        rows.append((
            "#4B788C",
            "Classical",
            "n=3 one-bit RAC polytope",
        ))

    if not rows:
        return

    # Spread active rows evenly through the legend area.
    ys = np.linspace(0.72, 0.18, len(rows))

    for y, (color, title, equation) in zip(ys, rows):
        ax.plot(
            [0.035, 0.17],
            [y, y],
            color=color,
            linewidth=4.0,
            transform=ax.transAxes,
            solid_capstyle="round",
        )

        ax.text(
            0.22,
            y + 0.045,
            title,
            transform=ax.transAxes,
            color=color,
            fontsize=12.8,
            fontweight="bold",
            ha="left",
            va="center",
        )

        ax.text(
            0.22,
            y - 0.055,
            equation,
            transform=ax.transAxes,
            color="black",
            fontsize=10.7,
            ha="left",
            va="center",
        )


def add_axis_box(fig):
    ax = fig.add_axes(RIGHT_AXIS_BOX)
    ax.set_axis_off()

    rounded_box(
        ax,
        edgecolor="steelblue",
    )

    ax.text(
        0.06,
        0.91,
        "Advantage axes",
        transform=ax.transAxes,
        fontsize=14.5,
        fontweight="bold",
        ha="left",
        va="top",
    )

    origin = np.array([0.43, 0.36])

    directions = [
        np.array([-0.23, -0.10]),
        np.array([ 0.28, -0.07]),
        np.array([ 0.00,  0.34]),
    ]

    # Explicitly 1-indexed.
    labels = [
        ("c1", "(1, 0, 0)", "crimson"),
        ("c2", "(0, 1, 0)", "green"),
        ("c3", "(0, 0, 1)", "royalblue"),
    ]

    ax.scatter(
        [origin[0]],
        [origin[1]],
        s=30,
        c=["black"],
        transform=ax.transAxes,
        zorder=3,
    )

    for d, (name, vec, color) in zip(directions, labels):
        tip = origin + d

        ax.annotate(
            "",
            xy=tip,
            xytext=origin,
            xycoords=ax.transAxes,
            textcoords=ax.transAxes,
            arrowprops=dict(
                arrowstyle="-|>",
                lw=2.0,
                color=color,
                mutation_scale=17,
            ),
        )

        ax.text(
            tip[0] + 0.02,
            tip[1] + 0.02,
            rf"${name}$" + "\n" + vec,
            transform=ax.transAxes,
            fontsize=10.5,
            color=color,
            ha="left",
            va="bottom",
        )


def compose(image):
    fig = plt.figure(
        figsize=FIGURE_SIZE_INCH,
        dpi=DPI,
        facecolor="white",
    )

    fig.text(
        0.025,
        0.955,
        "n=3 advantage-space boundaries",
        fontsize=22,
        fontweight="bold",
        ha="left",
        va="top",
    )

    fig.text(
        0.025,
        0.915,
        "Classical, quantum and mutual-information geometry in three advantage coordinates",
        fontsize=14.5,
        ha="left",
        va="top",
    )

    ax_image = fig.add_axes(LEFT_IMAGE_BOX)
    ax_image.imshow(image)
    ax_image.set_axis_off()

    add_shape_legend(fig)
    add_axis_box(fig)

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
    print("Rendering n=3 advantage-space comparison...")
    print(
        f"  classical={SHOW_CLASSICAL} (opacity={CLASSICAL_OPACITY})\n"
        f"  quantum={SHOW_QUANTUM} (opacity={QUANTUM_OPACITY})\n"
        f"  mutual information={SHOW_MUTUAL_INFORMATION} "
        f"(opacity={MUTUAL_INFORMATION_OPACITY})"
    )

    image = render_scene()
    compose(image)

    # Useful numerical checks on the positive symmetric direction.
    c_quantum = 1.0 / np.sqrt(3.0)

    direction = np.array([[1.0, 1.0, 1.0]]) / np.sqrt(3.0)
    r_mi = solve_mi_radius(direction)[0]
    c_mi = r_mi / np.sqrt(3.0)

    print(f"Saved: {OUTPUT}")
    print(f"Quantum symmetric coordinate: c = {c_quantum:.12f}")
    print(f"Mutual-information symmetric coordinate: c = {c_mi:.12f}")


if __name__ == "__main__":
    main()
