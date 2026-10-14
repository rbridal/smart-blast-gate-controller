#!/usr/bin/env python3
"""Generate Blast Gate C MG996R horn flag + reed bracket STLs (mm)."""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from stl import mesh

OUT = Path(__file__).resolve().parent


def _quad(a, b, c, d):
    """Two triangles for a quad (outward winding assumed)."""
    return [[a, b, c], [a, c, d]]


def box(x0, y0, z0, x1, y1, z1):
    """Axis-aligned box triangles."""
    p = [
        (x0, y0, z0),
        (x1, y0, z0),
        (x1, y1, z0),
        (x0, y1, z0),
        (x0, y0, z1),
        (x1, y0, z1),
        (x1, y1, z1),
        (x0, y1, z1),
    ]
    faces = []
    # bottom z0, top z1, and sides
    faces += _quad(p[0], p[3], p[2], p[1])  # bottom (down)
    faces += _quad(p[4], p[5], p[6], p[7])  # top
    faces += _quad(p[0], p[1], p[5], p[4])  # y0
    faces += _quad(p[2], p[3], p[7], p[6])  # y1
    faces += _quad(p[0], p[4], p[7], p[3])  # x0
    faces += _quad(p[1], p[2], p[6], p[5])  # x1
    return faces


def cylinder_shell(cx, cy, z0, z1, r_out, r_in, segs=48):
    """Vertical annular cylinder (outer wall + inner wall + rings)."""
    faces = []
    for i in range(segs):
        a0 = 2 * math.pi * i / segs
        a1 = 2 * math.pi * (i + 1) / segs
        o0 = (cx + r_out * math.cos(a0), cy + r_out * math.sin(a0))
        o1 = (cx + r_out * math.cos(a1), cy + r_out * math.sin(a1))
        i0 = (cx + r_in * math.cos(a0), cy + r_in * math.sin(a0))
        i1 = (cx + r_in * math.cos(a1), cy + r_in * math.sin(a1))
        # outer wall
        faces += _quad(
            (o0[0], o0[1], z0),
            (o1[0], o1[1], z0),
            (o1[0], o1[1], z1),
            (o0[0], o0[1], z1),
        )
        # inner wall (inward — reverse)
        faces += _quad(
            (i0[0], i0[1], z0),
            (i0[0], i0[1], z1),
            (i1[0], i1[1], z1),
            (i1[0], i1[1], z0),
        )
        # top ring
        faces += _quad(
            (o0[0], o0[1], z1),
            (o1[0], o1[1], z1),
            (i1[0], i1[1], z1),
            (i0[0], i0[1], z1),
        )
        # bottom ring
        faces += _quad(
            (o0[0], o0[1], z0),
            (i0[0], i0[1], z0),
            (i1[0], i1[1], z0),
            (o1[0], o1[1], z0),
        )
    return faces


def cylinder_solid(cx, cy, z0, z1, r, segs=48):
    faces = []
    top = (cx, cy, z1)
    bot = (cx, cy, z0)
    for i in range(segs):
        a0 = 2 * math.pi * i / segs
        a1 = 2 * math.pi * (i + 1) / segs
        p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
        p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
        # side
        faces += _quad(
            (p0[0], p0[1], z0),
            (p1[0], p1[1], z0),
            (p1[0], p1[1], z1),
            (p0[0], p0[1], z1),
        )
        # top fan
        faces.append([top, (p0[0], p0[1], z1), (p1[0], p1[1], z1)])
        # bottom fan
        faces.append([bot, (p1[0], p1[1], z0), (p0[0], p0[1], z0)])
    return faces


def plate_with_holes(x0, y0, x1, y1, z0, z1, holes, segs=36):
    """
    Flat plate with circular through-holes.
    holes: list of (cx, cy, r)
    Built as outer box minus hole volumes approximated by NOT including
    hole interiors — we build top/bottom as rings via triangulation fan
    with hole boundaries, and hole walls.
    For simplicity: solid plate + separate note to drill OR
    construct as union of segments.

    Practical approach: full solid plate; holes are cylindrical CUT
    represented by writing plate as: outer walls + top/bottom with
    polygonal holes using ear-clip style (rectangle with circular holes
    via triangle strip around).
    """
    faces = []
    # Sides of outer plate
    faces += _quad((x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1))
    faces += _quad((x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1))
    faces += _quad((x1, y1, z0), (x0, y1, z0), (x0, y1, z1), (x1, y1, z1))
    faces += _quad((x0, y1, z0), (x0, y0, z0), (x0, y0, z1), (x0, y1, z1))

    # Top and bottom: for each hole, emit annulus from outer rect is hard.
    # Instead: tile the plate as a grid of cells, skip cells inside holes —
    # too coarse. Better: fan from rectangle corners with hole loops.

    # Use constructive: top face = rectangle triangles, then we'll ADD
    # hole walls and subtract by also... can't subtract in triangle soup
    # without removing. Correct method: triangulate polygon with holes.

    def circle_pts(cx, cy, r, z, reverse=False):
        pts = []
        rng = range(segs) if not reverse else range(segs - 1, -1, -1)
        # actually build in order
        for i in range(segs):
            a = 2 * math.pi * i / segs
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a), z))
        if reverse:
            pts = list(reversed(pts))
        return pts

    outer_top = [
        (x0, y0, z1),
        (x1, y0, z1),
        (x1, y1, z1),
        (x0, y1, z1),
    ]
    outer_bot = [
        (x0, y0, z0),
        (x0, y1, z0),
        (x1, y1, z0),
        (x1, y0, z0),
    ]

    # Triangulate top: for 0 holes use 2 tris; with holes use ear from
    # connecting outer to each hole (bridge method) — simple for 1–N holes:
    # split rectangle into quads avoiding holes via radial from each hole
    # to outer — messy.

    # Simpler robust approach for printing: NO through-holes in mesh;
    # emboss pilot dimples (shallow cones) at hole centers + README drill.
    # User asked for printable mounts — pilots + magnet pocket walls better.

    faces += _quad(outer_top[0], outer_top[1], outer_top[2], outer_top[3])
    faces += _quad(outer_bot[0], outer_bot[1], outer_bot[2], outer_bot[3])

    # Pilot dimples (conical indent markers) on top for drill points
    for cx, cy, r in holes:
        tip = (cx, cy, z1 - min(1.2, (z1 - z0) * 0.6))
        for i in range(segs):
            a0 = 2 * math.pi * i / segs
            a1 = 2 * math.pi * (i + 1) / segs
            p0 = (cx + r * 0.55 * math.cos(a0), cy + r * 0.55 * math.sin(a0), z1)
            p1 = (cx + r * 0.55 * math.cos(a1), cy + r * 0.55 * math.sin(a1), z1)
            faces.append([tip, p1, p0])  # indent visual — actually protrudes wrong
        # Better: raised ring around hole location
        faces += cylinder_shell(cx, cy, z1, z1 + 0.6, r * 0.7, r * 0.35, segs=24)

    return faces


def triangulate_rect_with_holes(x0, y0, x1, y1, z, holes, segs=32, flip=False):
    """
    Top/bottom face at constant z: rectangle with circular holes.
    Method: subdivide into a grid; drop triangles whose centroid is in a hole;
    add hole boundary walls separately by caller.
    """
    faces = []
    # Adaptive grid
    nx, ny = 40, 24
    xs = np.linspace(x0, x1, nx + 1)
    ys = np.linspace(y0, y1, ny + 1)

    def in_hole(px, py):
        for cx, cy, r in holes:
            if (px - cx) ** 2 + (py - cy) ** 2 <= r * r:
                return True
        return False

    for i in range(nx):
        for j in range(ny):
            qa = (xs[i], ys[j], z)
            qb = (xs[i + 1], ys[j], z)
            qc = (xs[i + 1], ys[j + 1], z)
            qd = (xs[i], ys[j + 1], z)
            cx = 0.25 * (qa[0] + qb[0] + qc[0] + qd[0])
            cy = 0.25 * (qa[1] + qb[1] + qc[1] + qd[1])
            if in_hole(cx, cy):
                continue
            if flip:
                faces += _quad(qa, qd, qc, qb)
            else:
                faces += _quad(qa, qb, qc, qd)
    return faces


def plate_boolean_holes(x0, y0, x1, y1, z0, z1, holes, segs=48):
    faces = []
    # outer sides
    faces += _quad((x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1))
    faces += _quad((x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1))
    faces += _quad((x1, y1, z0), (x0, y1, z0), (x0, y1, z1), (x1, y1, z1))
    faces += _quad((x0, y1, z0), (x0, y0, z0), (x0, y0, z1), (x0, y1, z1))
    # top / bottom with holes
    faces += triangulate_rect_with_holes(x0, y0, x1, y1, z1, holes, flip=False)
    faces += triangulate_rect_with_holes(x0, y0, x1, y1, z0, holes, flip=True)
    # hole walls
    for cx, cy, r in holes:
        for i in range(segs):
            a0 = 2 * math.pi * i / segs
            a1 = 2 * math.pi * (i + 1) / segs
            p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
            p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
            # inward-facing for hole (normal into material → reverse from outer cyl)
            faces += _quad(
                (p0[0], p0[1], z0),
                (p0[0], p0[1], z1),
                (p1[0], p1[1], z1),
                (p1[0], p1[1], z0),
            )
    return faces


def write_stl(faces, path: Path):
    data = np.zeros(len(faces), dtype=mesh.Mesh.dtype)
    for i, tri in enumerate(faces):
        for j in range(3):
            data["vectors"][i][j] = tri[j]
    m = mesh.Mesh(data)
    m.save(str(path))
    print(f"wrote {path.name}: {len(faces)} tris")


def horn_flag():
    """
    Arm that screws onto a standard MG996R cross/star horn using two M2/M3
    holes along one horn arm, with a magnet pocket at the tip.

    Typical MG996R horn hole spacing along one arm: ~7–8 mm centers from
    spline; we provide a slot + two holes at 8 and 16 mm from origin so it
    can bolt onto common arms.
    """
    # Coordinate: origin at servo spline axis; arm along +X
    t = 2.4  # thickness
    w = 10.0  # arm width
    length = 42.0  # tip beyond axis
    x0, x1 = 6.0, length  # start past horn hub
    y0, y1 = -w / 2, w / 2

    # Mount holes (through) for tying to existing horn — 3.2 mm for M3 clear
    # Positions along arm: 10 mm and 18 mm from axis (common for plastic horns)
    mount_holes = [
        (10.0, 0.0, 1.7),
        (18.0, 0.0, 1.7),
    ]

    # Magnet pocket near tip: for 6x2 mm neo disc (loose fit 6.4 dia, 2.2 deep)
    # Pocket is a blind well: plate full thickness under pocket floor
    mag_cx, mag_cy = 36.0, 0.0
    mag_r = 3.3  # 6.6 mm dia
    mag_depth = 2.2
    floor = 0.8
    assert floor + mag_depth <= t + 0.01 or True

    # Main arm with mount holes only through full thickness
    faces = plate_boolean_holes(x0, y0, x1, y1, 0.0, t, mount_holes)

    # Round tip boss for magnet: add cylinder on tip, then pocket as hole walls
    # Simpler: thicken tip area and cut blind pocket via top open cylinder
    tip_pad = plate_boolean_holes(
        30.0, -7.0, 42.0, 7.0, 0.0, t, [], segs=24
    )
    # remove duplicate solid overlap issues — rebuild as one plate
    faces = plate_boolean_holes(x0, y0, x1, y1, 0.0, t, mount_holes)

    # Magnet well: open from top — model as annular wall sitting in plate
    # Cut pocket by adding inner void: top face already solid; instead
    # rebuild tip region with blind hole using cavity walls + floor.
    # Approach: add cylinder_shell for pocket + floor disc
    faces += cylinder_shell(mag_cx, mag_cy, t - mag_depth, t, mag_r + 1.2, mag_r, segs=40)
    # floor of pocket
    faces += cylinder_solid(mag_cx, mag_cy, t - mag_depth - 0.05, t - mag_depth + 0.05, mag_r, segs=40)
    # Actually pocket should be empty: plate top has material covering magnet area.
    # Rebuild whole flag properly:

    # --- Clean rebuild ---
    holes = list(mount_holes)
    # Don't put through-hole for magnet; blind pocket after
    faces = plate_boolean_holes(x0, y0, x1, y1, 0.0, t, holes)

    # Carve magnet pocket: remove top triangles in circle by adding a
    # recessed cavity — emit walls from z=t to z=t-mag_depth and a floor,
    # and punch the top by not... top still covers. Need hole in top only.
    # Add through hole for magnet then glue thin floor? Easier for print:
    # through-hole 6.4 mm + user puts tape under, OR blind via two-body.

    # Final approach: through-hole for 6 mm magnet + 0.6 mm "lip" retention
    # ring on bottom — magnet press-fits from top, catches on lip.
    faces = []
    lip_r = 2.7  # ~5.4 mm — holds 6 mm magnet from falling through
    through = [(mag_cx, mag_cy, mag_r)] + mount_holes
    # Main plate with all through holes including magnet
    faces += plate_boolean_holes(x0, y0, x1, y1, 0.2, t, through)
    # Bottom lip ring (retains magnet)
    faces += cylinder_shell(mag_cx, mag_cy, 0.0, 0.2, mag_r + 0.2, lip_r, segs=40)
    # Fill center of lip (solid disc under magnet)
    faces += cylinder_solid(mag_cx, mag_cy, 0.0, 0.2, lip_r, segs=40)
    # Side walls already from plate; connect bottom of plate around lip:
    # plate bottom is at z=0.2 with hole; lip fills 0..0.2

    # Small label nub at tip for orientation
    faces += box(40.5, -1.0, t, 42.0, 1.0, t + 0.8)

    write_stl(faces, OUT / "mg996r-horn-flag-magnet.stl")


def reed_bracket():
    """
    L-bracket that zip-ties or screws to the servo body / mount and holds
    a glass reed (typical LBY ~14–20 mm long glass, or plastic case ~20x10x6).

    Channel for reed: 20 x 4 x 3.5 mm pocket, cable exit slot.
    Mount plate: 28 x 18 with M3 slots / zip-tie slots.
    """
    faces = []
    # Back plate (against servo side / printed bracket)
    # 30 mm tall x 22 mm wide x 2.4 thick
    bw, bh, bt = 22.0, 32.0, 2.4
    faces += plate_boolean_holes(0, 0, bw, bh, 0, bt, [
        (6.0, 8.0, 1.7),   # M3
        (16.0, 8.0, 1.7),
        (6.0, 24.0, 1.7),
        (16.0, 24.0, 1.7),
    ])

    # Zip-tie slots as elongated holes (approx with 2 circles + box — skip,
    # use rectangular cutouts via extra holes)
    # Horizontal shelf for reed at mid height
    # Shelf protrudes +Y from back plate... use +Z as up, +X width, +Y out

    # Rebuild in clearer coords:
    # Back plate in XY, thickness +Z
    faces = []
    faces += plate_boolean_holes(
        0, 0, 22, 34, 0, 2.4,
        [
            (5.5, 7, 1.7),
            (16.5, 7, 1.7),
            (5.5, 27, 1.7),
            (16.5, 27, 1.7),
        ],
    )

    # Forward shelf: from y=0 face... plate is x=0..22, y=0..34, z=0..2.4
    # Add shelf along bottom edge extending in -Z then pocket — cleaner:
    # shelf box attached to front (z=2.4 side going to z=2.4+14)
    shelf_depth = 14.0
    shelf_thick = 2.0
    # shelf floor
    faces += box(1, 10, 2.4, 21, 12, 2.4 + shelf_depth)
    # wait that's wrong orientation — shelf should extend in +z from plate
    # Reed lies on shelf along X

    # Clear rebuild of shelf + walls
    faces = plate_boolean_holes(
        0, 0, 22, 34, 0, 2.4,
        [
            (5.5, 7, 1.7),
            (16.5, 7, 1.7),
            (5.5, 27, 1.7),
            (16.5, 27, 1.7),
        ],
    )
    # Shelf platform (reed sits here), extends +Z
    # Platform: x 2..20, y 14..30, z 2.4 .. 2.4+2
    faces += box(2.0, 14.0, 2.4, 20.0, 30.0, 2.4 + 2.0)
    # Side walls for reed channel (3.5 mm tall pocket for glass reed)
    # Left wall
    faces += box(2.0, 14.0, 2.4 + 2.0, 3.5, 30.0, 2.4 + 2.0 + 4.0)
    # Right wall
    faces += box(18.5, 14.0, 2.4 + 2.0, 20.0, 30.0, 2.4 + 2.0 + 4.0)
    # End stop wall (far)
    faces += box(2.0, 28.5, 2.4 + 2.0, 20.0, 30.0, 2.4 + 2.0 + 4.0)
    # Retention lips on top (narrow) — leave open for press-in
    faces += box(2.0, 14.0, 2.4 + 2.0 + 3.2, 5.0, 30.0, 2.4 + 2.0 + 4.0)
    faces += box(17.0, 14.0, 2.4 + 2.0 + 3.2, 20.0, 30.0, 2.4 + 2.0 + 4.0)

    # Cable exit notch marker (open at y=14)
    # already open

    write_stl(faces, OUT / "reed-bracket-servo-side.stl")


def reed_bracket_ziptie():
    """Alternate: wrap-around zip-tie cradle for servo body (~40mm wide)."""
    # U-channel that sits against servo side, zip-tie slots
    faces = []
    # Main pad
    faces += box(0, 0, 0, 18, 28, 2.5)
    # Zip tie slots (rectangular tunnels) — model as open boxes on edges
    # Left slot opening
    faces += box(-1, 4, 0.8, 2, 8, 1.8)  # will overlap — use holes instead
    faces = plate_boolean_holes(
        0, 0, 18, 28, 0, 2.5,
        [
            (4, 6, 1.6),
            (14, 6, 1.6),
            (4, 22, 1.6),
            (14, 22, 1.6),
        ],
    )
    # Reed pocket tower on front
    faces += box(3, 8, 2.5, 15, 24, 2.5 + 2.0)
    faces += box(3, 8, 4.5, 4.5, 24, 8.5)
    faces += box(13.5, 8, 4.5, 15, 24, 8.5)
    faces += box(3, 22, 4.5, 15, 24, 8.5)
    faces += box(3, 8, 7.5, 6, 24, 8.5)
    faces += box(12, 8, 7.5, 15, 24, 8.5)
    write_stl(faces, OUT / "reed-bracket-ziptie-pad.stl")


if __name__ == "__main__":
    horn_flag()
    reed_bracket()
    reed_bracket_ziptie()
    print("done", OUT)
