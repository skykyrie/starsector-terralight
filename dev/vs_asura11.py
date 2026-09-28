import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Asura-II v11 - Terra Light unique detailing (closed armour: no exposed drive core, power trench, cables or machinery gaps).
Based on v10 (identical canvas/silhouette/slots).  Old notes: Starsector style v4: less blocky. Curved spline hull (ogive prow, flared shoulders, slight waist, rounded
engine nacelles), armour plates that follow the hull contour, streamlined missile blisters, flush side-thruster
fairings, wider main-drive gap (ENG CX+-56, shared with EL), Quad Railgun v3."""
import json, numpy as np
from scipy import ndimage as ndi
import vstyle, vparts as VP
from vstyle import Ship, spline

SL = json.load(open(_ROOT + '/asura_slots.json'))
W, H = SL['W'], SL['H']; CX = W//2
SLOTS = SL['slots']; ENG = SL['ENG']
GUN = (CX, 100)
MIS_WALL = [(s_['px'], s_['py']) for s_ in SLOTS if s_['type'] == 'MISSILE' and s_['py'] < 330]
MIS_DECK = [(s_['px'], s_['py']) for s_ in SLOTS if s_['type'] == 'MISSILE' and s_['py'] >= 330]

PL = np.array([132, 134, 140]); PL_D = np.array([100, 102, 110]); PL_L = np.array([158, 160, 166])
ORNG = np.array([200, 120, 56]); ORNG_D = np.array([140, 80, 36]); GREEN = np.array([86, 160, 112])
PWR = (190, 110, 50); COOL = (150, 152, 158)
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))

_L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = CX     # symmetric light from the bow
s = Ship(W, H, seed=41)
s.auto_z = True; s.depth = dict(unit=7.0, s_str=0.9, tint=0.38, ao=0.6, ao_r=5, sdir=((0.6, 0.8), (-0.6, 0.8)), s_soft=0.9)
def zmark(z, fn, *a, **k):
    before = s.rgb.copy(); a0 = s.a.copy(); r = fn(*a, **k)
    ch = (np.abs(s.rgb - before).sum(2) > 0.5) | (s.a & ~a0); s.z[ch] = z; return r
_plate0, _bolt0, _haz0, _cab0, _win0 = s.plate, s.bolt_row, s.hazard, s.cable, s.windows
def _plate(mask, color, *a, **k):
    k.setdefault('tex', 0.018); k.setdefault('grime', 0.0); k.setdefault('notch', 0); return _plate0(mask, color, *a, **k)
def _bolt(m, inset=1.8, spacing=4.0, seed=0):
    if m is not None and m.sum()/s.SS**2 > 900: _bolt0(m, inset, spacing*2.4)
def _haz(x0, y0, x1, y1, mask=None, period=4):
    if abs(x1 - x0)*abs(y1 - y0) >= 90: _haz0(x0, y0, x1, y1, mask, period)
def _cab(pts, width, color, clamps=10.0, clamp_col=None, cast=True, smooth=True):
    return _cab0(pts, width, color, clamps=(clamps*1.8 if width >= 3 else 0), clamp_col=clamp_col, cast=cast, smooth=smooth)
def _win(x0, x1, y, mask, step=2.4, lit=(255, 222, 160), frac=0.8, seed=3):
    return _win0(x0, x1, y, mask, step=step*1.6, lit=lit, frac=frac, seed=seed)
s.plate, s.bolt_row, s.hazard, s.cable, s.windows = _plate, _bolt, _haz, _cab, _win
X = lambda g, dx: CX + g*dx
def mir(pts): return pts + [(2*CX - x, y) for x, y in pts[::-1]]
SP = lambda pts: s.poly(spline(mir(pts), 20, True))
def both(fn): fn(-1); fn(1)
yy_ = s.yy/s.SS; xx_ = s.xx/s.SS; ax_ = np.abs(xx_ - CX)
def erode(m, px): return ndi.binary_erosion(m, iterations=max(1, int(px*s.SS)))

# ================================================================ silhouette: ogive prow, flared shoulders, waist, nacelles
LEFT = [(CX - 4, 18), (CX - 26, 50), (CX - 58, 96), (CX - 86, 142), (CX - 99, 182), (CX - 96, 240), (CX - 99, 300),
        (CX - 100, 350), (CX - 94, 392), (CX - 80, 414), (CX - 40, 420), (CX - 20, 412)]
hull = SP(LEFT)
nac = np.zeros_like(hull)
s.guts(hull | nac, seed=43, tone=(50, 52, 58), minc=3, maxc=10); s.z[:] = 0
# lower DECK armour under everything (machinery only shows in the service trenches) - calmer, less noisy
deck = erode(hull, 12)                                                  # v32 TL: one closed armour deck, seams engraved (no trenches)
s.plate(deck, PL_D*1.02, z=1.4, bevel=2.0, dome=0.3, inset=2.0, shadow_k=0.5, notch=0,
        lines=[s.rrect(0, y, W, y + 0.7, 0.2) for y in (120, 150, 180, 240, 270, 304, 340, 370)] +
              [s.rrect(X(g, d) - 0.35, 0, X(g, d) + 0.35, H, 0.2) for g in (-1, 1) for d in (4, 28, 64)])

# ================================================================ main drives in rounded nacelles (wider gap)
MET = (146, 144, 150); SIDE_W = 14
def eng_z(z, *a, **k):
    m = VP.engine_housing(s, *a, **k); s.z[m] = z; return m
# v6: THREE big mains + TWO small drives on each side, all emerging from under one stern armour block
ENG = [(CX - 44, 434), (CX, 424), (CX + 44, 434)]
SMALL = [(CX + g*dx, ye) for g in (-1, 1) for dx, ye in ((67, 430), (78, 426))]
for (ex, ey) in ENG: eng_z(1.3, ex, 394, ey, 34 if ex == CX else 30, metal=MET, bands=2)
DIAG = []
def diag_jet(g, cx_, cy_, w_):
    """small drive drawn upright in a tile, rotated 45 deg so it fires back-outward"""
    T = 36; j = Ship(T, T, SS=s.SS, seed=5)
    mm = VP.engine_housing(j, T/2, 3, 26, w_, metal=MET, bands=1); j.z[mm] = 1.1
    ang = -45 if g < 0 else 45
    rgb = np.stack([ndi.rotate(j.rgb[..., c], ang, reshape=False, order=1) for c in range(3)], -1)
    al = ndi.rotate(j.a.astype(np.float32), ang, reshape=False, order=1) > 0.5
    zr = ndi.rotate(j.z, ang, reshape=False, order=0)
    ox, oy = int(round((cx_ - T/2)*s.SS)), int(round((cy_ - T/2)*s.SS))
    sub = (slice(oy, oy + j.h), slice(ox, ox + j.w))
    s.rgb[sub][al] = rgb[al]; s.a[sub] |= al; s.z[sub][al] = zr[al]
def hull_bottom(x):                                                   # lowest hull row at column x
    col = hull[:, int(x*s.SS)]; ys = np.where(col)[0]; return ys.max()/s.SS
SMALL = []
for g in (-1, 1):                                                     # 4 small drives, 2 per side, firing diagonally back-outward
    n = np.array([g*0.7071, 0.7071])
    for dx, w_ in ((75, 10), (87, 9)):
        e = np.array([X(g, dx), hull_bottom(X(g, dx))])
        c = e + n*(-1.0)
        diag_jet(g, c[0], c[1], w_)
        ex_ = c + n*9.5; SMALL.append((float(ex_[0]), float(ex_[1]), 135 if g < 0 else -135))
stern_blk = hull & (yy_ > 384)
m = s.plate(stern_blk, PL_D, z=2.4, bevel=2.8, dome=0.6, tilt=(0, 0.1), inset=2.2, shadow_k=0.8,
            lines=[s.rrect(X(g, dx) - 0.35, 386, X(g, dx) + 0.35, 420, 0.2) for g in (-1, 1) for dx in (22, 62)])
for g in (-1, 1): s.grille(s.rrect(min(X(g, 34), X(g, 54)), 390, max(X(g, 34), X(g, 54)), 398, 0.4), period=2.0)
sysl('3 main drives under the stern armour', CX, 430); sysl('2 small drives per side', X(1, 72), 422)

# ================================================================ contour armour: an outer skin band that follows the hull line
outer = hull & ~erode(hull, 15)
skin_aft = outer & (yy_ > 150) & (yy_ < 400)
m = s.plate(skin_aft & (yy_ < 386), PL, z=3.0, bevel=3.0, dome=0.6, inset=2.4, shadow_k=0.7,
            paint=[(hull & ~erode(hull, 2.8) & erode(hull, 1.2) & (yy_ > 150), ORNG)],
            lines=[s.rrect(0, y, W, y + 0.7, 0.2) for y in (212, 268, 326, 372)])
s.bolt_row(m, 2.0, 5)
sysl('contour armour skin (follows the hull line)', X(-1, 96), 360)
# prow: ogive skin in two layers + keel ridge
prow = hull & (yy_ <= 156)
pskin = prow & ~erode(prow, 16)
for g in (-1, 1):
    side = pskin & ((xx_ - CX)*g > 5)
    m = s.plate(side, PL_D*1.05, z=3.2, bevel=3.2, dome=0.8, inset=2.6, shadow_k=0.7,
                paint=[(side & (np.abs(yy_ - (60 + (ax_ - 20)*1.15)) < 2.2), ORNG)])
    s.bolt_row(m, 1.8, 5)
pin = prow & erode(prow, 14) & ~s.disk(*GUN, 35)                          # v11: prow interior closed by armour (no open deck)
for g in (-1, 1):
    side = pin & ((xx_ - CX)*g > 1)
    m_ = s.plate(side, PL*0.98, z=2.6, bevel=2.4, dome=0.5, inset=1.8, shadow_k=0.75, notch=0,
                 paint=[(side & (np.abs(yy_ - (104 + (ax_ - 20)*0.9)) < 1.2), PL_L*1.05)])
    s.bolt_row(m_, 1.6, 5)
keel = SP([(CX - 3, 22), (CX - 10, 40), (CX - 22, 90), (CX - 34, 132), (CX - 38, 156)]) & prow
s.plate(keel & ~s.disk(*GUN, 34), PL, z=3.9, bevel=3, ridge=('x', CX, 5.0, 38), inset=2.6, shadow_k=0.8, paint=[(np.abs(xx_ - CX) < 3.5, ORNG)])
tip = SP([(CX - 3, 20), (CX - 9, 34), (CX - 6, 44), (CX, 46)])
s.plate(tip, ORNG, z=4.4, bevel=2, ridge=('x', CX, 2.4, 10), inset=1.2, shadow_k=0.7)
s.mount(CX, 56, 4.5, PL_L, well_col=(80, 110, 140))
for g in (-1, 1):                                                                              # flush prow vents
    s.grille(s.poly([(X(g, 44), 118), (X(g, 70), 136), (X(g, 70), 144), (X(g, 44), 128)]) & prow, period=2.0)
s.emblem(CX, 146, 4.4)
sysl('ogive prow: layered armour + orange keel', X(-1, 40), 110); sysl('bow sensor', CX, 56)

# ================================================================ Quad Railgun barbette + magazines + capacitors
bar = s.disk(*GUN, 32)
s.plate(bar, PL_D, z=3.4, bevel=3.5, dome=0.8, inset=2.6, shadow_k=0.85)
rr = np.hypot(xx_ - GUN[0], yy_ - GUN[1])
s.rgb[bar & (rr > 27.2) & (rr < 29.0) & (yy_ < GUN[1])] = (210, 214, 222)
s.rgb[bar & (rr > 27.2) & (rr < 29.0) & (yy_ >= GUN[1])] = (70, 72, 80)
s.rgb[bar & (rr > 25.0) & (rr < 26.4)] = ORNG
s.rgb[bar & (rr < 24.5)] = (32, 34, 38)
sysl('Quad Railgun barbette; twin gun hidden below', GUN[0], GUN[1] - 30)
def mag(g):
    m = SP([(X(g, 30), 150), (X(g, 58), 152), (X(g, 60), 178), (X(g, 30), 178)]) if False else s.rrect(min(X(g, 32), X(g, 62)), 152, max(X(g, 32), X(g, 62)), 178, 6)
    m = s.plate(m, PL, z=2.3, bevel=2.2, dome=0.6, inset=1.8, shadow_k=0.7)
    for k in range(4): s.rgb[s.rrect(min(X(g, 37), X(g, 57)), 156 + k*5.2, max(X(g, 37), X(g, 57)), 158 + k*5.2, 0.8)] = (70, 72, 78)
both(mag); sysl('railgun magazine armour', X(1, 47), 164)
spn = SP([(CX - 8, 134), (CX - 14, 144), (CX - 14, 184), (CX - 22, 192)]) | SP([(CX - 22, 190), (CX - 26, 200), (CX - 26, 226), (CX - 18, 236)])   # v11: core buried under a closed armour block + spine
m = s.plate(spn, PL, z=2.6, bevel=3.0, dome=0.8, ridge=('x', CX, 2.4, 26), inset=2.4, shadow_k=0.8,
            paint=[(np.abs(xx_ - CX) < 3.0, ORNG), ((np.abs(xx_ - CX) >= 3.0) & (np.abs(xx_ - CX) < 4.4), PL_L)])
s.bolt_row(m & ~(np.abs(xx_ - CX) < 7), 1.8, 5)
for yv in (200, 216): s.grille(s.rrect(CX - 20, yv, CX - 9, yv + 6, 0.8), period=2.0); s.grille(s.rrect(CX + 9, yv, CX + 20, yv + 6, 0.8), period=2.0)
s.hazard(CX - 16, 229, CX + 16, 232, m, period=3)
sysl('core bay: closed armour block + spine (core buried)', CX, 212)
def caps(g):
    cp = s.rrect(min(X(g, 32), X(g, 60)), 186, max(X(g, 32), X(g, 60)), 226, 5)
    m = s.plate(cp, PL, z=2.2, bevel=2.6, dome=0.7, inset=2.0, shadow_k=0.75, notch=2.5, paint=[(cp & (np.abs(xx_ - X(g, 58)) < 2.0), ORNG)])
    s.bolt_row(m, 1.6, 5)
    s.hatch(min(X(g, 38), X(g, 52)), 194, max(X(g, 38), X(g, 52)), 206)
    s.grille(s.rrect(min(X(g, 38), X(g, 52)), 212, max(X(g, 38), X(g, 52)), 220, 0.8), period=2.0)
both(caps); sysl('capacitor bay armour: sunk hatch + flush vent', X(-1, 46), 200)

# ================================================================ streamlined missile blisters (teardrop) + reload racks
def blisters(g):
    for (mx, my) in [p for p in MIS_WALL if (p[0] < CX) == (g < 0)]:
        bl = s.poly(spline([(mx, my - 22), (X(g, 94), my - 8), (X(g, 94), my + 12), (mx, my + 26), (X(g, 70), my + 12), (X(g, 70), my - 8)], 16, True))
        m = s.plate(bl, PL_L*0.97, z=3.4, bevel=3, dome=0.8, inset=2.0, shadow_k=0.8, paint=[(bl & (yy_ > my + 17), ORNG)])
        VP.sunk_mount(s, mx, my, 10.0, (g, 0.35), metal=PL_D, lip_metal=PL_L, z=3.0, lip_z=4.3, accent=ORNG)   # sunk into the blister
        r = s.rrect(min(X(g, 58), X(g, 68)), my - 13, max(X(g, 58), X(g, 68)), my + 13, 2.5)       # closed reload-hatch cover
        m_ = s.plate(r, PL, z=2.4, bevel=1.8, dome=0.4, inset=1.2, outline=0.7, shadow_k=0.7)
        s.engrave(s.rrect(min(X(g, 58), X(g, 68)), my - 0.3, max(X(g, 58), X(g, 68)), my + 0.3, 0.1))
        s.hazard(min(X(g, 58.6), X(g, 67.4)), my - 12.4, max(X(g, 58.6), X(g, 67.4)), my - 10.6, m_, period=2.4)
both(blisters); sysl('missile mounts SUNK into the blisters, raised outboard lip x6 + closed reload hatches', X(-1, 83), 225)

# ================================================================ crew decks + aft engineering (rounded modules)
def decks(g):
    m = s.rrect(min(X(g, 30), X(g, 58)), 238, max(X(g, 30), X(g, 58)), 300, 8)
    m = s.plate(m, PL, z=2.3, bevel=2.8, dome=0.8, inset=2.2, shadow_k=0.7)
    for yy in range(248, 292, 12): s.windows(min(X(g, 34), X(g, 54)), max(X(g, 34), X(g, 54)), yy, m, step=2.4, seed=yy + g)
    e = s.rrect(min(X(g, 30), X(g, 72)), 308, max(X(g, 30), X(g, 72)), 384, 10)
    e = s.plate(e, PL, z=2.4, bevel=2.8, dome=0.8, inset=2.2, shadow_k=0.75); s.bolt_row(e, 2.0, 5)
    s.plate(s.rrect(min(X(g, 34), X(g, 68)), 314, max(X(g, 34), X(g, 68)), 356, 5), PL_L*0.96, z=2.8, bevel=2.2, dome=0.5, inset=1.8, shadow_k=0.75, notch=2.5,
            paint=[(s.rrect(min(X(g, 34), X(g, 68)), 350, max(X(g, 34), X(g, 68)), 353), ORNG)])
    s.hatch(min(X(g, 42), X(g, 60)), 322, max(X(g, 42), X(g, 60)), 336)
    s.grille(s.rrect(min(X(g, 36), X(g, 66)), 362, max(X(g, 36), X(g, 66)), 378, 2), period=2.0)
both(decks); sysl('crew decks', X(-1, 44), 262); sysl('engineering deck: filler hatch + vents', X(-1, 50), 334)

# ================================================================ command superstructure (rounded, tall toward centre, green command room)
cmd1 = SP([(CX - 20, 244), (CX - 32, 262), (CX - 34, 330), (CX - 26, 352), (CX - 24, 396), (CX - 14, 404)])
m1 = s.plate(cmd1, PL, z=3.4, bevel=4, dome=1.4, inset=3.0, shadow_k=0.85, paint=[(np.abs(yy_ - 338) < 2.5, ORNG)])
s.bolt_row(m1, 2.0, 5)
cmd2 = SP([(CX - 8, 250), (CX - 22, 266), (CX - 23, 322), (CX - 16, 334)])
m2 = s.plate(cmd2, PL_L, z=4.8, bevel=3.4, dome=1.6, ridge=('x', CX, 2.0, 23), inset=2.6, shadow_k=0.85)
glass = SP([(CX - 8, 253), (CX - 19.5, 266), (CX - 20, 272), (CX - 8, 262)]) & m2
gy = np.clip((yy_ - 252)/20, 0, 1)
s.rgb[glass] = (GREEN*(1.15 - 0.55*gy[..., None]))[glass]
for k_ in range(-20, 21, 4): s.rgb[glass & (np.abs(xx_ - (CX + k_)) < 0.35)] = (36, 44, 40)
cmd3 = SP([(CX - 7, 282), (CX - 13, 292), (CX - 13, 322), (CX - 8, 330)])
m3 = s.plate(cmd3, PL_L*1.03, z=6.0, bevel=2.6, dome=1.4, ridge=('x', CX, 1.6, 13), inset=2.0, shadow_k=0.85)
for yy in (294, 308):
    band = s.rrect(CX - 10, yy, CX + 10, yy + 3, 1.2) & m3
    s.rgb[band] = (70, 130, 96); s.rgb[band & (yy_ < yy + 1)] = (130, 190, 150)
s.mount(CX, 318, 5.5, PL, well_col=(80, 120, 100))
s.grille(s.rrect(CX - 16, 356, CX + 16, 366, 2), period=2.0); s.hatch(CX - 9, 374, CX + 9, 388)
sysl('command block (green command room)', CX, 262); sysl('CIC + fire-control dome', CX, 318)
for (dx_, dy_) in MIS_DECK:
    VP.sunk_mount(s, dx_, dy_, 10.0, (1 if dx_ > CX else -1, 0.6), metal=PL_D, lip_metal=PL_L, z=2.8, lip_z=4.0, accent=ORNG)
sysl('deck missile pods x2', MIS_DECK[1][0], MIS_DECK[1][1])

# ================================================================ side thrusters v3: FLUSH fairings in the hull wall (no pods)
LAT = [(g, y) for g in (-1, 1) for y in (196, 256, 330)]
def hw_at(y):                                                                                 # outer hull x-offset at row y
    row = hull[int(y*s.SS)]; xs = np.where(row)[0]
    return (CX - xs.min()/s.SS) if len(xs) else 90
def lateral(g, y):
    hw = hw_at(y)
    fair = s.poly(spline([(X(g, hw - 10), y - 13), (X(g, hw + 3), y - 9), (X(g, hw + 4), y + 9), (X(g, hw - 10), y + 13), (X(g, hw - 14), y)], 14, True))
    m = s.plate(fair, PL_D*1.05, bevel=2.4, dome=0.8, inset=1.6, shadow_k=0.75, paint=[(fair & (np.abs(yy_ - y) > 10), ORNG)])
    for dy in (-5, 0, 5):                                                                       # 3 recessed nozzle slots facing out
        sl = s.rrect(min(X(g, hw - 3), X(g, hw + 3.6)), y + dy - 1.6, max(X(g, hw - 3), X(g, hw + 3.6)), y + dy + 1.6, 1.2)
        s.rgb[sl] = (24, 24, 28)
        s.rgb[sl & (np.abs(xx_ - X(g, hw + 3.0)) < 0.5)] = (255, 150, 90)                         # ember at the mouth
        s.rgb[sl & (yy_ < y + dy - 0.9)] = (120, 122, 128)                                        # lit upper lip
    s.rgb[s.disk(X(g, hw - 9), y, 1.3)] = (40, 42, 46)
LAT = []   # v5: side thrusters removed (vanilla crewed hulls have none)

# ================================================================ livery + lights
armour = s.a.copy()
s.livery(armour, (yy_ > 226) & (yy_ < 233) & (ax_ > 30) & (ax_ < 60), ORNG, keep=0.3)
_h = CX*s.SS                                                        # exact left/right symmetry
s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
s.stencil(X(-1, 56), 240, 3, h=4, seed=3); s.stencil(X(1, 44), 240, 3, h=4, seed=4); s.stencil(CX - 8, 60 + 10, 4, h=4, seed=9) if False else None
s.lights([(X(-1, 94), 176), (X(1, 94), 176), (X(-1, 74), 382), (X(1, 74), 382), (CX, 21)],
         [(255, 70, 60), (90, 255, 120), (255, 70, 60), (90, 255, 120), (255, 255, 240)])

sprite = s.render()
sprite.save(_ROOT + '/ss_style/asura_ss_v11.png')
json.dump(dict(W=W, H=H, slots=SLOTS, ENG=ENG, small=SMALL, lat=[], diag=[]),
          open(_ROOT + '/ss_style/asura_ss_v11_slots.json', 'w'))
json.dump(SYSTEMS, open(_ROOT + '/ss_style/asura_v11_systems.json', 'w'))
print('ok')
