import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Tiamat v32 - Terra Light unique detailing (closed armour: no exposed drive core, conduits or machinery gaps).
Based on v31 (identical canvas/silhouette/slots).  Old notes: Starsector style v15: v7 model (casemate "tyre" sponsons on the side walls) + v12 Terra Light detailing.
The Triple Beam gun sprite (barrel pack only, no cockpit) is attached on the OUTER SIDE of each sponson.
Static base (hull): trunnion arm + mount collar + tracking ring at the sponson face.  Moving part (weapon): barrels.
Arcs 135 deg: front 0..135 (outward), rear 45..180.  Small energy PD: 4 per side on the centre-hull gun rails;
the wall PD between the beams is removed."""
import json, sys, numpy as np
from scipy import ndimage as ndi
import vstyle
from vstyle import Ship
_L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = 130      # v28: symmetric light (from the bow)

W, H, CX = 260, 400, 130
S_ = json.load(open(_ROOT + '/tiamat_slots.json'))
sh = lambda p: (p[0] - 130 + CX, p[1])
FLANK = [sh(p) for p in S_['FLANK']]; DECK = [(CX + g*66, y) for g in (-1, 1) for y in (88, 152, 230, 292)]; ENG = [sh(p) for p in S_['ENG']]
PODS = [(-1, 120), (-1, 262), (1, 120), (1, 262)]
PIV = 108                                                         # pivot = outer face of the sponson
PD_Y = sorted({y for _, y in FLANK})

PL = np.array([132, 137, 146]); PL_D = np.array([100, 104, 114]); PL_L = np.array([156, 160, 168])
BLUE = np.array([62, 100, 172]); PWR = (60, 96, 170); COOL = (150, 152, 158); DATA = (190, 160, 70)
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))

s = Ship(W, H, seed=10)
s.auto_z = True; s.depth = dict(unit=7.0, s_str=0.9, tint=0.38, ao=0.6, ao_r=5, sdir=((0.6, 0.8), (-0.6, 0.8)), s_soft=0.9)
ZC = [None]                                                        # current layer height for the section being drawn
def Z(z): ZC[0] = z
def zmark(z, fn, *a, **k):                                        # give a non-plate part (cylinder, mount...) its own layer
    before = s.rgb.copy(); a0 = s.a.copy(); r = fn(*a, **k)
    ch = (np.abs(s.rgb - before).sum(2) > 0.5) | (s.a & ~a0); s.z[ch] = z; return r
# ---------------- v21 CLEAN-UP pass: calmer surfaces, fewer repeated micro-details
_plate0, _bolt0, _haz0, _cab0, _win0 = s.plate, s.bolt_row, s.hazard, s.cable, s.windows
def _plate(mask, color, *a, **k):
    if ZC[0] is not None and 'z' not in k and 'dz' not in k: k['z'] = ZC[0]
    k.setdefault('tex', 0.018); k.setdefault('grime', 0.0); return _plate0(mask, color, *a, **k)
def _bolt(m, inset=1.8, spacing=4.0, seed=0):
    if m is not None and m.sum()/s.SS**2 > 900: _bolt0(m, inset, spacing*2.4)        # bolts only on big armour, widely spaced
def _haz(x0, y0, x1, y1, mask=None, period=4):
    if abs(x1 - x0)*abs(y1 - y0) >= 90: _haz0(x0, y0, x1, y1, mask, period)          # drop the tiny hazard chips
def _cab(pts, width, color, clamps=10.0, clamp_col=None, cast=True, smooth=True):
    return _cab0(pts, width, color, clamps=(clamps*1.8 if width >= 3 else 0), clamp_col=clamp_col, cast=cast, smooth=smooth)
def _win(x0, x1, y, mask, step=2.4, lit=(255, 222, 160), frac=0.8, seed=3):
    return _win0(x0, x1, y, mask, step=step*1.6, lit=lit, frac=frac, seed=seed)
s.plate, s.bolt_row, s.hazard, s.cable, s.windows = _plate, _bolt, _haz, _cab, _win
X = lambda g, dx: CX + g*dx
def both(fn): fn(-1); fn(1)
M = lambda pts: s.poly(Ship.mirror_pts(pts, CX))

# ================================================================ silhouette: main box + centre block + pods
main = M([(CX - 58, 24), (CX - 90, 56), (CX - 90, 340), (CX - 66, 364)])          # v7 outline
notch = np.zeros_like(main); podm = {}; POCKET = {}
for g, y in PODS:                                                  # v7 casemate sponsons ("tyres")
    xo, xi = X(g, 108), X(g, 76)
    podm[(g, y)] = s.poly([(xo, y - 32), (xo - g*9, y - 44), (xi + g*4, y - 44), (xi, y - 40), (xi, y + 40), (xi + g*4, y + 44), (xo - g*9, y + 44), (xo, y + 32)])
    POCKET[(g, y)] = s.poly([(xo, y - 22), (X(g, 86), y - 22), (X(g, 81), y - 16), (X(g, 81), y + 16), (X(g, 86), y + 22), (xo, y + 22)])
body = main | s.rrect(CX - 60, 338, CX + 60, 368, 4)
s.guts(body, seed=14, tone=(50, 52, 58), minc=3, maxc=10)                 # base only - fully covered by the deck armour below
_yy, _xx = s.yy/s.SS, s.xx/s.SS
DECKLINES = [s.rrect(0, y, W, y + 0.7, 0.2) for y in (70, 146, 204, 268, 338)] + \
            [s.rrect(CX + g*d - 0.35, 60, CX + g*d + 0.35, 366, 0.2) for g in (-1, 1) for d in (22, 48)]
s.plate(body, PL_D*1.04, z=1.4, bevel=2.0, dome=0.3, inset=1.8, shadow_k=0.5, notch=0, lines=DECKLINES)   # v32: closed armour deck
PLATES = []
def P(mask, color, **k):
    k.setdefault('notch', 3.0)
    m = s.plate(mask, color, **k); PLATES.append(m); return m

# ================================================================ engines + stern block
import vparts as VP
ACC_T = (225, 120, 255)                                            # Tiamat drive accent (matches its pink/violet flame)
# v26: drives pushed further into the hull (shorter), satellite thrusters added, corner jets exit a solid corner wedge
# that is part of the stern block (the hull corner itself), not a strap along the chamfer.
SIDE_W = 14; SX = 45; MW_ = 40; MET = (146, 144, 150)
ENG = [(CX - SX, 372), (CX, 374), (CX + SX, 372)]; MAN = []
SAT = []
def eng_z(z, *a, **k):
    m = VP.engine_housing(s, *a, **k); s.z[m] = z; return m
eng_z(1.3, CX, 352, 388, MW_, metal=MET, bands=2)                  # one wide centre main
for g in (-1, 1): eng_z(1.1, CX + g*SX, 352, 381, SIDE_W, metal=MET, bands=2)   # one drive each side, clear gap
DIAG = []
def diag_jet(g, cx_, cy_):
    """corner drive (same can as the side drives) + one satellite, drawn upright in a tile, rotated 45 deg back-outward"""
    T = 44; j = Ship(T, T, SS=s.SS, seed=5)
    mm = VP.engine_housing(j, T/2, 4, 31, SIDE_W, metal=MET, bands=2); j.z[mm] = 1.1
    ang = -45 if g < 0 else 45
    rgb = np.stack([ndi.rotate(j.rgb[..., c], ang, reshape=False, order=1) for c in range(3)], -1)
    al = ndi.rotate(j.a.astype(np.float32), ang, reshape=False, order=1) > 0.5
    zr = ndi.rotate(j.z, ang, reshape=False, order=0)
    ox, oy = int(round((cx_ - T/2)*s.SS)), int(round((cy_ - T/2)*s.SS))
    sub = (slice(oy, oy + j.h), slice(ox, ox + j.w))
    s.shadow(np.pad(al, ((oy, s.h - oy - j.h), (ox, s.w - ox - j.w))), 1.4, 1.8, 0.7, 1.0)
    s.rgb[sub][al] = rgb[al]; s.a[sub] |= al; s.z[sub][al] = zr[al]
from vstyle import spline
WEDGE = {}
for g in (-1, 1):
    A, B = np.array([X(g, 91), 336.0]), np.array([X(g, 61), 367.0])                   # outer edge = the hull chamfer, nudged out
    n = np.array([g*0.7071, 0.7071]); u = (B - A)/np.linalg.norm(B - A); mid = A + (B - A)*0.5
    diag_jet(g, *(mid + n*4.5))
    DIAG.append((mid[0] + n[0]*15, mid[1] + n[1]*15, g))
    pts = [(X(g, 56), 336), tuple(A + n*1.0), tuple(mid - u*8 + n*1.6), tuple(mid - u*4 + n*3.2), tuple(mid + u*4 + n*3.2),
           tuple(mid + u*8 + n*1.6), tuple(B + n*1.0), (X(g, 56), 367)]
    WEDGE[g] = s.poly(spline(pts, 10, True)) | s.poly([(X(g, 56), 336), tuple(A + n*1.0), tuple(B + n*1.0), (X(g, 56), 367)])
Z(2.2)
stern = M([(CX - 60, 338), (CX - 60, 360), (CX - 52, 366), (CX, 366)])
m = P(stern | WEDGE[-1] | WEDGE[1], PL_D, bevel=2.5, dome=0.5, tilt=(0, 0.1), inset=2.4); s.bolt_row(m, 1.6, 5)
for g in (-1, 1):
    s.grille(s.rrect(min(X(g, 24), X(g, 34)), 344, max(X(g, 24), X(g, 34)), 356, 0.4), period=2.0)
    A, B = np.array([X(g, 91), 336.0]), np.array([X(g, 61), 367.0]); n = np.array([g*0.7071, 0.7071])
    for k in (0.28, 0.72):                                                               # panel seams echo the chamfer
        p = A + (B - A)*k - n*1.5; q = p - n*8; w_ = np.array([n[1], -n[0]])*0.35
        s.engrave(s.poly([tuple(p + w_), tuple(q + w_), tuple(q - w_), tuple(p - w_)]))
yy_, xx_ = s.yy/s.SS, s.xx/s.SS
sysl('engine block + radiators', X(1, 46), 350); sysl('3 main + 2 manoeuvring engines', CX, 384)

# ================================================================ wall armour belts (v7) - full length, bolted
def belt(g):
    """side-wall armour belt as overlapping SLABS: raised slabs (z 3.7) sit over recessed joints (z 3.0), each slab
    overlaps the next so the belt reads as layered armour, not one flat strip"""
    pts = [(X(g, 90), 60), (X(g, 86), 56), (X(g, 76), 56), (X(g, 76), 340), (X(g, 84), 340), (X(g, 90), 334)]
    base = s.poly(pts)
    m = P(base, PL_D, bevel=1.6, tilt=(-g*0.45, 0), inset=1.2, z=3.0)
    cuts = (56, 90, 150, 190, 232, 292, 340)
    for i in range(len(cuts) - 1):
        y0, y1 = cuts[i] + 1.5, cuts[i + 1] - 1.5
        slab = base & s.poly([(X(g, 91), y0), (X(g, 77.5), y0 + 2), (X(g, 77.5), y1), (X(g, 91), y1 - 2)])
        P(slab, PL, bevel=2.2, tilt=(-g*0.45, 0.05), inset=1.8, z=3.7 + 0.25*(i % 2),
          paint=[(s.rrect(min(X(g, 89), X(g, 86)), y0, max(X(g, 89), X(g, 86)), y1), BLUE)])
    s.bolt_row(m, 1.5, 5)
both(belt); sysl('side-wall armour belt', X(-1, 83), 330)

# ================================================================ bow: centre block armour (ram) + hood over the main box
Z(3.2)
ram = M([(CX - 48, 24), (CX - 60, 34), (CX - 60, 60), (CX - 40, 66), (CX - 20, 68)])
m = P(ram, PL, bevel=3, ridge=('x', CX, 5.0, 60), tilt=(0, 0.15), inset=3.0,
      paint=[(s.rrect(CX - 5, 18, CX + 5, 70), BLUE), (s.rrect(CX - 8, 18, CX - 5, 70) | s.rrect(CX + 5, 18, CX + 8, 70), PL_L)])
s.bolt_row(m & ~s.rrect(CX - 9, 0, CX + 9, 80), 1.7, 5)
cap = M([(CX - 24, 26), (CX - 36, 34), (CX - 30, 48), (CX - 14, 52)])
P(cap, PL_L, z=4.2, bevel=2.2, ridge=('x', CX, 2.4, 36), tilt=(0, 0.12), inset=2.0, shadow_k=0.7, paint=[(s.rrect(CX - 5, 18, CX + 5, 70), BLUE)])
def shoulder(g):
    m = s.poly([(X(g, 57), 26), (X(g, 88), 57), (X(g, 88), 68), (X(g, 72), 68), (X(g, 60), 60), (X(g, 60), 26)])
    m = P(m, PL_D*1.05, z=2.6, bevel=2.2, tilt=(g*0.3, 0.2), inset=2.0); s.bolt_row(m, 1.5, 4.5)
both(shoulder)
# v28 RAM ARMOUR: glacis slabs shingled down the bow chamfers (front slab on top, deflects impacts),
# then a heavy crescent prow plate across the whole front, overlapping the cap and the ram block
def glacis(g):
    A, B = np.array([X(g, 56), 24.0]), np.array([X(g, 90), 58.0])
    n = np.array([g*0.7071, -0.7071]); u = (B - A)/np.linalg.norm(B - A); L = np.linalg.norm(B - A)
    for i, (t0, t1, zz) in enumerate(((0.62, 1.0, 3.3), (0.30, 0.70, 3.6), (0.0, 0.38, 3.9))):     # aft -> fore, fore on top
        p0, p1 = A + u*L*t0, A + u*L*t1
        sl = s.poly([tuple(p0 + n*1.2), tuple(p1 + n*1.2), tuple(p1 - n*9 - u*1.5), tuple(p0 - n*9 + u*1.5)])
        m_ = P(sl, PL_L if i == 2 else PL, z=zz, bevel=2.0, tilt=(g*0.25, -0.25), inset=1.6, notch=0)
        s.bolt_row(m_, 1.3, 4.0)
both(glacis)
prow = M([(CX, 11), (CX - 26, 13), (CX - 46, 19), (CX - 56, 25), (CX - 50, 31), (CX - 30, 30), (CX - 12, 33), (CX, 35)])
m = P(prow, PL_L, z=4.8, bevel=3.2, ridge=('x', CX, 3.0, 40), tilt=(0, -0.25), inset=2.4, dome=0.8, notch=0,
      paint=[(s.rrect(CX - 4, 8, CX + 4, 36), BLUE)],
      lines=[s.rrect(X(g, 18) - 0.35, 12, X(g, 18) + 0.35, 34, 0.2) for g in (-1, 1)] + [s.rrect(X(g, 38) - 0.35, 16, X(g, 38) + 0.35, 31, 0.2) for g in (-1, 1)])
edge = prow & ~ndi.binary_dilation(M([(CX, 14), (CX - 26, 16), (CX - 46, 22), (CX - 56, 28), (CX - 56, 40), (CX, 40)]), iterations=0) if False else None
s.bolt_row(m & ~s.rrect(CX - 6, 0, CX + 6, 40), 1.6, 5)
s.mount(CX, 44, 6.0, PL_L, well_col=(70, 96, 140))                   # sensor dome sits behind the prow armour
sysl('ram armour: crescent prow plate over 3 shingled glacis slabs per side', CX - 44, 30); sysl('main sensor dome', CX, 44)
sysl('RCS thrusters', X(1, 80), 58)

# ================================================================ inner deck (v7 layout): spine, rails, flank modules, aft deck
Z(1.8)
for i, (y0, y1) in enumerate(((84, 142),)):
    m = M([(CX - 10, y0), (CX - 17, y0 + 8), (CX - 17, y1 - 4), (CX - 10, y1 - 10), (CX - 4, y1 - 6)]) | s.poly([(CX - 4, y1 - 6), (CX, y1 - 4), (CX + 4, y1 - 6)])
    P(m, PL if i != 1 else PL_L, bevel=2.2, ridge=('x', CX, 4.0, 17), dome=0.6, inset=2.6,
      paint=[(s.rrect(CX - 3, y0 + 4, CX + 3, y1 - 8, 0.5), BLUE)])
sysl('spine armour ridge', CX, 110)
Z(2.5)
for sx in (CX - 34, CX + 34):
    r = s.poly([(sx - 10, 92), (sx - 6, 84), (sx + 6, 84), (sx + 10, 92), (sx + 10, 192), (sx + 6, 198), (sx - 6, 198), (sx - 10, 192)])
    m = P(r, PL_L, bevel=3, dome=0.8, ridge=('x', sx, 3.2, 10), inset=2.6, shadow_k=0.7, notch=0,
          paint=[(s.rrect(sx - 10, 84, sx + 10, 89), BLUE), (s.rrect(sx - 10, 193, sx + 10, 198), BLUE)])
    s.bolt_row(m, 1.6, 5)
    for yv in (104, 164): s.grille(s.rrect(sx - 5, yv, sx + 5, yv + 12, 1.0), period=2.0)     # flush heat vents
sysl('armoured gun rails (flush vents)', X(1, 34), 120)
Z(None)
def flank(g):
    for y in (120, 262):                                             # beam capacitor bank + radiator facing each pod
        cp = s.rrect(min(X(g, 72), X(g, 48)), y - 26, max(X(g, 72), X(g, 48)), y + 3, 1.5)
        m = P(cp, PL, z=2.0, bevel=2.4, dome=0.5, tilt=(-g*0.12, 0), inset=2.0, notch=2.5,
              paint=[(s.rrect(min(X(g, 72), X(g, 69)), y - 26, max(X(g, 72), X(g, 69)), y + 3), BLUE)])
        s.bolt_row(m, 1.5, 5)
        s.hatch(min(X(g, 64), X(g, 54)), y - 19, max(X(g, 64), X(g, 54)), y - 7)
        rad = s.rrect(min(X(g, 70), X(g, 50)), y + 6, max(X(g, 70), X(g, 50)), y + 22, 1)
        m = P(rad, PL_D, z=1.6, bevel=1.5, inset=1.4, shadow_k=0.55); s.grille(s.rrect(min(X(g, 67), X(g, 53)), y + 9, max(X(g, 67), X(g, 53)), y + 19, 0.6), period=2.0)
    hab = s.rrect(min(X(g, 74), X(g, 50)), 162, max(X(g, 74), X(g, 50)), 220, 2)                    # crew habitat between the pods
    m = P(hab, PL, z=2.3, bevel=2.4, dome=0.6, tilt=(-g*0.15, 0), inset=2.2); s.bolt_row(m, 1.6, 5)
    for yy in range(166, 186, 5): s.windows(min(X(g, 67), X(g, 53)), max(X(g, 67), X(g, 53)), yy, m, step=2.6, seed=int(yy) + g)
    s.hatch(min(X(g, 66), X(g, 56)), 206, max(X(g, 66), X(g, 56)), 215)
    fs = s.poly([(X(g, 70), 58), (X(g, 56), 58), (X(g, 50), 62), (X(g, 50), 66), (X(g, 70), 66)])     # supply hatch strip
    P(fs, PL, z=1.4, bevel=1.6, inset=1.4)
both(flank)
for (dx_, dy_) in DECK:                                                   # PD mounts on armoured bulges near the side edges
    VP.sunk_mount(s, dx_, dy_, 7.0, (1 if dx_ > CX else -1, 0), metal=PL_D, lip_metal=PL_L, z=2.4, lip_z=3.6, accent=BLUE)
sysl('small energy PD (4 per side): SUNK in octagonal collars, raised armour lip on the outboard side', X(-1, 66), 152)
sysl('beam bay armour panel + sunk hatch', X(1, 63), 105); sysl('flush heat vent', X(1, 63), 135)
sysl('crew habitat + airlock', X(-1, 62), 165)
cb = M([(CX - 12, 146), (CX - 21, 154), (CX - 21, 196), (CX - 14, 202)])          # v32: core fully buried - closed armour block
m = P(cb, PL, z=2.4, bevel=3.0, dome=0.8, ridge=('x', CX, 2.0, 21), inset=2.4, notch=2.5,
      paint=[(s.rrect(CX - 3, 146, CX + 3, 202), BLUE), (s.rrect(CX - 5, 146, CX - 3.6, 202) | s.rrect(CX + 3.6, 146, CX + 5, 202), PL_L)])
s.bolt_row(m & ~s.rrect(CX - 7, 0, CX + 7, 400), 1.6, 5)
for yv in (158, 186): s.grille(s.rrect(CX - 16, yv, CX - 8, yv + 6, 0.8), period=2.0); s.grille(s.rrect(CX + 8, yv, CX + 16, yv + 6, 0.8), period=2.0)
s.hazard(CX - 18, 197, CX + 18, 200, cb, period=3)
sysl('core bay: closed armour block (core buried)', CX, 170)
def aft(g):
    m = s.poly([(CX, 268), (X(g, 60), 268), (X(g, 74), 276), (X(g, 74), 334), (CX, 334)])
    m = P(m, PL, z=2.3, bevel=3, dome=0.8, tilt=(0, 0.06), inset=3.0, paint=[(s.rrect(min(CX, X(g, 74)), 324, max(CX, X(g, 74)), 328, 0.3), BLUE)])
    s.bolt_row(m, 1.7, 5)
    s.hatch(min(X(g, 70), X(g, 56)), 284, max(X(g, 70), X(g, 56)), 298)
    s.grille(s.rrect(min(X(g, 70), X(g, 50)), 304, max(X(g, 70), X(g, 50)), 316, 1.0), period=2.0)
both(aft); sysl('aft deck: propellant filler hatch + vents', X(-1, 59), 300)
# ================================================================ COMMAND SUPERSTRUCTURE (capital-size, 3 tiers)
Z(None)
# tier 1: crew / operations block
cmd1 = M([(CX - 30, 204), (CX - 44, 216), (CX - 44, 330), (CX - 38, 338)])
m = P(cmd1, PL, z=3.3, bevel=3.5, dome=1.0, inset=3.0, shadow_k=0.85, paint=[(s.rrect(CX - 44, 326, CX + 44, 331), BLUE)])
s.bolt_row(m, 1.8, 5)
for g_ in (-1, 1):                                                     # crew-deck windows down both flanks
    for yy in range(226, 322, 12):
        s.windows(min(X(g_, 41), X(g_, 35)), max(X(g_, 41), X(g_, 35)), yy, cmd1, step=2.3, seed=int(yy)*3 + g_)
    s.hatch(min(X(g_, 43), X(g_, 35)), 330.5, max(X(g_, 43), X(g_, 35)), 336.5)            # side access airlocks
# tier 2: the bridge - a forward-pointing prow with a wraparound window band
cmd2 = M([(CX - 12, 208), (CX - 32, 224), (CX - 32, 320), (CX - 26, 326)])
m2 = P(cmd2, PL_L, z=4.7, bevel=3.2, dome=1.2, ridge=('x', CX, 2.0, 32), inset=2.6, shadow_k=0.85, notch=2.0)
s.bolt_row(m2, 1.6, 4.5)
glass = M([(CX - 12, 211.5), (CX - 29.5, 225.5), (CX - 29.5, 231.5), (CX - 12, 218)]) & m2         # wraparound bridge glazing
gy = np.clip((s.yy/s.SS - 210)/20, 0, 1)
s.rgb[glass] = (np.array([60, 110, 150])*(1.1 - 0.5*gy[..., None]))[glass]
for k_ in range(-28, 29, 3):                                                                       # window mullions
    s.rgb[glass & (np.abs(s.xx/s.SS - (CX + k_)) < 0.35)] = (36, 40, 46)
s.rgb[glass & (np.abs(s.yy/s.SS - (212.6 + np.maximum(np.abs(s.xx/s.SS - CX) - 12, 0)*0.8)) < 0.5)] = (200, 236, 250)   # glint along the top
rng_ = np.random.default_rng(77)
for k_ in range(-26, 27, 3):                                                                       # consoles glowing behind the glass
    yb = 216.2 + max(abs(k_) - 12, 0)*0.8
    if rng_.random() < 0.8: s.rgb[s.disk(CX + k_ + 0.8, yb, 0.55) & glass] = (255, 205, 120) if rng_.random() < 0.7 else (120, 200, 255)
# tier 3: combat information centre + flag bridge, crowned by the main fire-control dome
cmd3 = M([(CX - 10, 236), (CX - 18, 242), (CX - 18, 318), (CX - 12, 322)])
m3 = P(cmd3, PL_L*1.03, z=6.0, bevel=2.6, dome=1.2, ridge=('x', CX, 1.6, 18), inset=2.0, shadow_k=0.85, notch=0)
s.rgb[M([(CX - 10, 238.5), (CX - 15.5, 243), (CX - 15.5, 244.5), (CX - 10, 240.5)]) & m3] = (70, 120, 160)
for yy in (256, 276):                                                                              # flag-deck window bands (clean strips)
    band = s.rrect(CX - 13, yy, CX + 13, yy + 3, 0.8) & m3
    s.rgb[band] = (60, 104, 140); s.rgb[band & (s.yy/s.SS < yy + 1)] = (120, 170, 205)
    for k_ in range(-12, 13, 4): s.rgb[band & (np.abs(s.xx/s.SS - (CX + k_)) < 0.35)] = (36, 40, 46)
s.mount(CX, 306, 7.5, PL, well_col=(70, 96, 140))
for g_ in (-1, 1):                                                                                  # comm masts behind the CIC
    x_ = X(g_, 22); mast = s.poly([(x_ - 1.2, 324), (x_ - 0.7, 312), (x_ + 0.7, 312), (x_ + 1.2, 324)])
    s.plate(mast, PL_D, bevel=0.7, outline=0.5, shadow_k=0.6, notch=0); s.lights([(x_, 312.5)], [(255, 90, 80)])
    s.rcs(X(g_, 26), 250, 'l' if g_ < 0 else 'r', PL_D)                                            # station-keeping thrusters
s.emblem(CX, 330.5, 3.6)
sysl('command block: crew decks (windows) + side airlocks', X(-1, 38), 260)
sysl('bridge: wraparound window band + consoles', X(-1, 20), 220)
sysl('CIC / flag bridge + main fire-control dome', CX, 306); sysl('comm masts', X(1, 22), 314)

# ================================================================ the 4 casemate sponsons + static gun bases (v7 model)
Z(None)
def casemate(g, y):
    sm, pk = podm[(g, y)], POCKET[(g, y)]; px = X(g, PIV); xo, xi = X(g, 108), X(g, 76)
    m = s.plate(sm & ~pk, PL_D, z=3.9, bevel=2.6, dome=0.8, tilt=(-g*0.3, 0), inset=2.2, shadow_k=0.8, notch=3.0,
                paint=[(s.rrect(min(xo, xo - g*4), y - 44, max(xo, xo - g*4), y + 44), BLUE)],
                lines=[s.rrect(min(xo, xi), y - 30, max(xo, xi), y - 29.3, 0.2), s.rrect(min(xo, xi), y + 29.3, max(xo, xi), y + 30, 0.2)])
    PLATES.append(m); s.bolt_row(m, 1.5, 4.5)
    for yj in (y - 42, y + 39):
        s.hazard(min(xo - g*12, xo - g*2), yj, max(xo - g*12, xo - g*2), yj + 3, m)
    # the well (v7): dark floor, hydraulic lines, AO edge, frame shadow
    s.rgb[pk] = (30, 33, 36); s.a |= pk
    for yy in np.arange(y - 21, y + 21, 2.5):
        s.rgb[pk & s.rrect(0, yy, W, yy + 0.8, 0.1)] = (48, 52, 58) if int(yy*2) % 3 else (22, 24, 26)
    s.rgb[pk & (s.yy/s.SS < y - 12)] *= 0.72
    ao = pk & ~ndi.binary_erosion(pk, iterations=s.SS); s.rgb[ao] = 0
    # v32: well kept as a clean armoured recess (no exposed servo / cells / cables)
    for yj in (y - 21.5, y + 19.5):
        s.rgb[pk & s.rrect(0, yj, W, yj + 2, 0.2)] = (70, 74, 82)
    # status lights on the bay wall (ready / charging / fault)
    for k_, lc in enumerate(((90, 255, 120), (90, 150, 240), (255, 90, 80))):
        s.rgb[s.disk(X(g, 96 + k_*2.4), y - 23.5, 0.6)] = lc
    # STATIC BASE: trunnion arm from the well's back wall out to the sponson face, mount collar + tracking ring
    arm = s.rrect(min(X(g, 82), X(g, 104)), y - 6, max(X(g, 82), X(g, 104)), y + 6, 2)
    s.plate(arm, PL, z=4.4, bevel=1.8, ridge=('y', y, 1.6, 6), inset=1.4, outline=0.6, shadow_k=0.7, notch=0)
    for xx in (X(g, 88), X(g, 96)): s.rgb[s.disk(xx, y - 3.6, 0.7)] = (40, 42, 46); s.rgb[s.disk(xx, y + 3.6, 0.7)] = (40, 42, 46)
    col = s.disk(px, y, 9.5)
    s.plate(col, PL_L, z=4.9, bevel=3, dome=0.6, outline=0.7, shadow_k=0.75, notch=0)
    rr = np.hypot(s.xx/s.SS - px, s.yy/s.SS - y)
    s.rgb[col & (rr > 7.2) & (rr < 8.4) & (s.yy/s.SS < y)] = (210, 216, 226)      # tracking ring (lit half)
    s.rgb[col & (rr > 7.2) & (rr < 8.4) & (s.yy/s.SS >= y)] = (70, 74, 82)
    s.rgb[col & (rr > 5.6) & (rr < 6.6)] = (90, 150, 240); s.rgb[col & (rr > 5.9) & (rr < 6.3)] = (170, 210, 255)   # blue ring
    s.rgb[col & (rr < 4.4)] = (26, 28, 32)                                          # bearing the barrels turn in
    for a_ in range(0, 360, 45):
        bx, by = px + 8.8*np.cos(np.radians(a_)), y + 8.8*np.sin(np.radians(a_))
        s.rgb[s.disk(bx, by, 0.55)] = (40, 42, 46)
    # arc stops: small blocks marking the 135 deg traverse limits on the collar rim
    # power + coolant into the sponson from the hull
for g, y in PODS: casemate(g, y)
# ---- LATERAL THRUSTERS (strafe left / right): wall housings with 2 outward-facing nozzle bells each
LAT = [(g, y) for g in (-1, 1) for y in (62, 191, 322)]
def lateral(g, y):
    """vanilla-style outboard thruster pod (cf. Eagle / Conquest): bolted pylon, pod body with ring bands, two flared
    nozzle bells pointing outward with ring seams + ember glow, cooling vanes, flanged fuel line, exhaust hazard mark"""
    lo_, hi_ = lambda a_, b_: min(X(g, a_), X(g, b_)), lambda a_, b_: max(X(g, a_), X(g, b_))
    s.hazard(lo_(84, 90), y - 14, hi_(84, 90), y + 14, None, period=3)                            # exhaust warning on the wall
    py_ = s.rrect(lo_(83, 96), y - 4.5, hi_(83, 96), y + 4.5, 1.2)
    m_ = s.plate(py_, PL_D, bevel=1.4, ridge=('y', y, 1.0, 4.5), outline=0.6, shadow_k=0.75, notch=0)
    for xx in (88, 92): s.rgb[s.disk(X(g, xx), y - 2.6, 0.6)] = (40, 42, 46); s.rgb[s.disk(X(g, xx), y + 2.6, 0.6)] = (40, 42, 46)
    s.cylinder(lo_(93, 103), y - 13, hi_(93, 103), y + 13, (150, 152, 158), axis='v', bands=(y - 8, y, y + 8), caps=(100, 102, 110))
    for dy in (-6.5, 6.5):
        x0, x1 = X(g, 101), X(g, 109.5)
        bell = s.poly([(x0, y + dy - 3.2), (x1, y + dy - 4.8), (x1, y + dy + 4.8), (x0, y + dy + 3.2)])
        s.shadow(bell, 1.0, 1.2, 0.5, 0.8)
        v = np.clip((s.yy/s.SS - (y + dy))/4.8, -1, 1); cyl = np.sqrt(np.clip(1 - v**2, 0, 1))
        lum = 0.3 + 0.75*cyl*(1 - 0.35*v) + 0.6*np.exp(-((v + 0.45)/0.16)**2)
        col_ = np.array([150, 146, 150], np.float32)[None, None, :]*lum[..., None]
        s.rgb[bell] = np.clip(col_[bell], 0, 255); s.a |= bell
        for xx in (104, 106.5):
            s.rgb[bell & (np.abs(s.xx/s.SS - X(g, xx)) < 0.35)] *= 0.55                               # ring seams
        lip = bell & (np.abs(s.xx/s.SS - x1) < 1.1); s.rgb[lip] = (36, 34, 38)
        s.rgb[bell & (np.abs(s.xx/s.SS - (x1 - g*0.4)) < 0.4) & (np.abs(s.yy/s.SS - (y + dy)) < 2.2)] = (255, 150, 90)   # ember
        e_ = bell & ~ndi.binary_erosion(bell, iterations=max(1, int(0.6*s.SS))); s.rgb[e_] *= 0.35
    for dy in (-1.5, 1.5):                                                                            # cooling vanes between bells
        s.rgb[s.poly([(X(g, 102), y + dy - 0.5), (X(g, 107), y + dy), (X(g, 102), y + dy + 0.5)])] = (120, 124, 132)
    s.cable([(X(g, 78), y - 11), (X(g, 86), y - 11), (X(g, 94), y - 10)], 1.8, (160, 116, 80), clamps=4, clamp_col=(200, 150, 60))
    s.connector(X(g, 94.5), y - 10, 1.8, ring=(200, 150, 60))
LAT = []   # v24: side thrusters removed (no crewed vanilla hull has them; only drones/stations)
sysl('lateral thrusters: strafe left / right (3 per side)', X(-1, 92), 191)
sysl('casemate sponson ("tyre", v7)', X(-1, 92), 150); sysl('well + trunnion arm (static base)', X(-1, 92), 120); 
sysl('mount collar + tracking ring: barrels turn here', X(1, 108), 262)

# ================================================================ Terra Light livery: one paint job across the hull
Z(None)
armour = np.zeros((s.h, s.w), bool)
for m_ in PLATES: armour |= m_
yy_ = s.yy/s.SS
s.livery(armour, (yy_ > 186) & (yy_ < 196), BLUE, keep=0.3)                                   # horizon band
s.livery(armour, ((yy_ > 182.6) & (yy_ < 184.2)) | ((yy_ > 197.8) & (yy_ < 199.4)), (225, 228, 234), keep=0.25)   # pinstripes
for g_, y_ in PODS:                                                                              # pod slashes
    sl = s.poly([(X(g_, 76), y_ - 30), (X(g_, 110), y_ - 44), (X(g_, 110), y_ - 36), (X(g_, 76), y_ - 22)]) & ~POCKET[(g_, y_)]
    s.livery(armour, sl, BLUE, keep=0.3)
    sl2 = s.poly([(X(g_, 76), y_ + 24), (X(g_, 110), y_ + 38), (X(g_, 110), y_ + 41), (X(g_, 76), y_ + 27)])
    s.livery(armour, sl2, (225, 228, 234), keep=0.25)
for g_ in (-1, 1): s.emblem(X(g_, 26), 50, 4.6)
sysl('TL livery: horizon band + pinstripes', X(1, 40), 191); sysl('Terra Light emblem', X(-1, 26), 50)

# ================================================================ connections on the deck
# v28: enforce exact left/right colour symmetry - mirror the finished left half onto the right
# (only the deliberately one-sided items below - data line, nav lights, stencil - are drawn after this)
_h = CX*s.SS
s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1]; s.a[:, _h:] = s.a[:, :_h][:, ::-1]; s.z[:, _h:] = s.z[:, :_h][:, ::-1]
sysl('structural pylons: engines hang from them, lines inside', CX + 15, 370)
s.stencil(CX - 10, 70, 5, h=4, mask=ram | body, seed=2)
s.stencil(X(-1, 70), 272, 3, h=4, seed=5); s.stencil(X(1, 57), 272, 3, h=4, seed=6)
s.stencil(X(-1, 38), 128, 2, h=4, seed=7)
s.lights([(X(-1, 88), 60), (X(1, 88), 60), (X(-1, 57), 352), (X(1, 57), 352), (CX, 25)],
         [(255, 70, 60), (90, 255, 120), (255, 70, 60), (90, 255, 120), (255, 255, 240)])

sprite = s.render()

sprite.save(_ROOT + '/ss_style/tiamat_ss_v32.png')
def arc(g, y):          # 135 deg: front 0..135 outward, rear 45..180 outward (angles +left)
    lo, hi = (0, 135) if y < 200 else (45, 180)
    if g > 0: lo, hi = -hi, -lo
    return (lo + hi)/2, hi - lo
slots = [dict(px=X(g, PIV), py=y, size='LARGE', type='ENERGY', mount='TURRET', builtin='tl_triplebeam', angle=arc(g, y)[0], arc=arc(g, y)[1]) for g, y in PODS]
slots += [dict(px=x, py=y, size='SMALL', type='ENERGY', mount='TURRET', angle=(90 if x < CX else -90), arc=210) for x, y in DECK]
json.dump(dict(lat=[(X(g, 109.5), y, 90 if g < 0 else -90) for g, y in LAT], W=W, H=H, beam=[(X(g, PIV), y) for g, y in PODS], deck=DECK, eng=ENG, man=MAN, diag=[(px, py, (135 if g < 0 else -135)) for px, py, g in DIAG], sat=SAT, slots=slots),
          open(_ROOT + '/ss_style/tiamat_ss_v32_slots.json', 'w'))
json.dump(SYSTEMS, open(_ROOT + '/ss_style/tiamat_v32_systems.json', 'w'))
print('ok')
