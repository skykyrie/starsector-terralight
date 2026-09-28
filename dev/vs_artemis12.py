import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Artemis - Starsector style v1 (Terra Light language: layers/depth, symmetric light + mirror, buried armoured cores,
drives emerging from under armour + diagonal corner jets).  Same canvas + slots as the locked EL Artemis (artemis_slots.json).
Catamaran carrier: two streamlined flight-deck hulls, magnetic catapult rail + pink shuttle in the gap, command 'stick'
lying back over the stern joint with its screen/bridge at the forward tip."""
import json, numpy as np
from scipy import ndimage as ndi
import vstyle, vparts as VP
from vstyle import Ship, spline

J = json.load(open(_ROOT + '/artemis_slots.json'))
W, H = J['W'], J['H']; CX = W//2
SLOTS = J['slots']
PD = [(s_['px'], s_['py']) for s_ in SLOTS if s_['type'] == 'ENERGY']
HY = [356, 290, 224, 158]                                            # hatch rows from the BACK of the deck forward, with landing gaps
for s_ in SLOTS:
    if s_['type'] == 'LAUNCH_BAY': s_['py'] = HY[[120, 190, 260, 330].index(s_['py'])]
BAYS = [(s_['px'], s_['py']) for s_ in SLOTS if s_['type'] == 'LAUNCH_BAY']
DECKS = [(20, 116), (154, 250)]; Y0, Y1 = 26, 424

PL = np.array([128, 134, 132]); PL_D = np.array([94, 100, 98]); PL_L = np.array([156, 162, 158])
GRN = np.array([92, 170, 104]); GRN_D = np.array([56, 112, 70]); PINK = np.array([236, 112, 186]); PINK_D = np.array([160, 70, 120])
SCREEN = np.array([60, 96, 190])
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))

_L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = CX
s = Ship(W, H, seed=71)
s.auto_z = True; s.depth = dict(unit=7.0, s_str=0.9, tint=0.38, ao=0.6, ao_r=5, sdir=((0.6, 0.8), (-0.6, 0.8)), s_soft=0.9)
_plate0, _bolt0 = s.plate, s.bolt_row
def _plate(mask, color, *a, **k):
    k.setdefault('tex', 0.018); k.setdefault('grime', 0.0); k.setdefault('notch', 0); return _plate0(mask, color, *a, **k)
def _bolt(m, inset=1.8, spacing=4.0, seed=0):
    if m is not None and m.sum()/s.SS**2 > 900: _bolt0(m, inset, spacing*2.4)
s.plate, s.bolt_row = _plate, _bolt
def zmark(z, fn, *a, **k):
    before = s.rgb.copy(); a0 = s.a.copy(); r = fn(*a, **k)
    ch = (np.abs(s.rgb - before).sum(2) > 0.5) | (s.a & ~a0); s.z[ch] = z; return r
X = lambda g, dx: CX + g*dx
yy_ = s.yy/s.SS; xx_ = s.xx/s.SS
def erode(m, px): return ndi.binary_erosion(m, iterations=max(1, int(px*s.SS)))
MET = (146, 144, 150)

# ================================================================ silhouette: two streamlined deck hulls + stern joint
def deck_hull(x0, x1):
    cx = (x0 + x1)/2; hw = (x1 - x0)/2
    R_ = [(0.0, Y0 - 3), (0.35, Y0 - 2), (0.62, Y0 + 2), (0.84, Y0 + 11), (0.96, Y0 + 26), (1.0, Y0 + 44), (1.0, 150), (1.0, 250),
          (1.0, 350), (1.0, Y1 - 30), (0.97, Y1 - 14), (0.86, Y1 - 4), (0.6, Y1), (0.3, Y1)]
    pts = [(cx + hw*a, y) for a, y in R_] + [(cx - hw*a, y) for a, y in R_[::-1][:-1]]
    return s.poly(spline(pts, 14, True))
HULLS = [deck_hull(*d) for d in DECKS]
joint = s.poly(spline([(X(-1, 38), 330), (X(1, 38), 330), (X(1, 40), 420), (X(1, 22), 428), (X(-1, 22), 428), (X(-1, 40), 420)], 10, True))
body = HULLS[0] | HULLS[1] | joint | s.rrect(CX - 16, 40, CX + 16, 346, 6)
s.guts(body, seed=73, tone=(50, 54, 52), minc=3, maxc=10); s.z[:] = 0

# ================================================================ stern: 2 drives per hull under the hull armour + 1 diagonal jet per outer corner
ENG = [tuple(e) for e in J['ENG']]
def eng_z(z, *a, **k):
    m = VP.engine_housing(s, *a, **k); s.z[m] = z; return m
for (ex, ey) in ENG: eng_z(1.3, ex, 404, 440, 26, metal=MET, bands=2)
def diag_jet(g, cx_, cy_, w_):
    T = 40; j = Ship(T, T, SS=s.SS, seed=5)
    mm = VP.engine_housing(j, T/2, 3, 29, w_, metal=MET, bands=2); j.z[mm] = 1.1
    ang = -45 if g < 0 else 45
    rgb = np.stack([ndi.rotate(j.rgb[..., c], ang, reshape=False, order=1) for c in range(3)], -1)
    al = ndi.rotate(j.a.astype(np.float32), ang, reshape=False, order=1) > 0.5
    zr = ndi.rotate(j.z, ang, reshape=False, order=0)
    ox, oy = int(round((cx_ - T/2)*s.SS)), int(round((cy_ - T/2)*s.SS))
    x0, y0 = max(0, ox), max(0, oy); x1, y1 = min(s.w, ox + j.w), min(s.h, oy + j.h)
    sub = (slice(y0, y1), slice(x0, x1)); tl = (slice(y0 - oy, y1 - oy), slice(x0 - ox, x1 - ox))
    al, rgb, zr = al[tl], rgb[tl], zr[tl]
    s.rgb[sub][al] = rgb[al]; s.a[sub] |= al; s.z[sub][al] = zr[al]
SMALL = []
HALL = HULLS[0] | HULLS[1]
def edge_x(y, g):                                                    # outer hull edge at row y
    xs = np.where(HALL[int(y*s.SS)])[0]; return (xs.max() if g > 0 else xs.min())/s.SS
for g in (-1, 1):
    n = np.array([g*0.7071, 0.7071])
    for y_ in (396, 412):                                            # two corner jets per side, stepped round the corner
        e = np.array([edge_x(y_, g) - g*2.5, y_ + 2.5])
        diag_jet(g, *(e + n*4.5), 12); ex_ = e + n*15; SMALL.append((float(ex_[0]), float(ex_[1]), 135 if g < 0 else -135))
sysl('4 main drives (2 per hull) + 2 diagonal corner jets per side', ENG[3][0], 438)

# ================================================================ stern joint (cross-structure) + catapult trench
s.plate(joint, PL_D, z=2.2, bevel=2.8, dome=0.5, inset=2.2, shadow_k=0.8)
trench = s.rrect(CX - 13, 44, CX + 13, 344, 5)
s.plate(trench, PL_D*0.62, z=1.2, bevel=1.8, inset=1.2, shadow_k=0.8)
for y in np.arange(56, 336, 14):                                                   # catapult coil segments
    s.rgb[s.rrect(CX - 10, y, CX + 10, y + 3.4, 1) & trench] = (118, 128, 124); s.rgb[s.rrect(CX - 10, y, CX + 10, y + 1, 0.5) & trench] = (168, 176, 172)
s.channel([(CX, 60), (CX, 338)], 4.0, light=tuple(PINK), step=14, nodes=False)     # lit magnetic rail
sysl('magnetic catapult: coil segments + lit rail', CX, 200)

# ================================================================ the two flight-deck hulls
for hi, (x0, x1) in enumerate(DECKS):
    hull = HULLS[hi]; cx = (x0 + x1)/2; g = -1 if cx < CX else 1
    rim = hull & ~erode(hull, 11)
    s.plate(hull, PL, z=3.0, bevel=3.2, dome=0.8, inset=2.6, shadow_k=0.85)
    fd = s.rrect(cx - 36, Y0 + 24, cx + 36, Y1 - 30, 16)
    s.plate(fd, GRN_D*0.9, z=2.2, bevel=1.6, inset=1.4, shadow_k=0.85,                  # recessed flight deck (EL green)
            lines=[s.rrect(cx - 36, y, cx + 36, y + 0.6, 0.2) for y in (96, 156, 224, 294, 360)])
    s.rgb[s.rrect(cx - 1.2, Y0 + 70, cx + 1.2, HY[-1] - 26, 0.6) & fd & ((yy_ // 12) % 2 == 0)] = (214, 222, 206)   # runway centre dashes (front half)
    for k in range(3): s.rgb[s.rrect(cx - 16 + k*1.5, Y0 + 40 + k*7, cx + 16 - k*1.5, Y0 + 42.5 + k*7, 1) & fd] = (214, 222, 206)   # bow chevrons
    for yl in np.arange(Y0 + 60, Y1 - 50, 18):                                         # deck edge lights
        for sd in (-1, 1): s.rgb[s.disk(cx + sd*31, yl, 0.8)] = (170, 255, 190)
    for (bx, by) in [b for b in BAYS if abs(b[0] - cx) < 5]:
        # HANGAR RAMP cut into the deck, drawn with its DEPTH: the cut walls get taller (so wider in view) going aft,
        # the floor narrows and its grip ribs crowd together (receding), guide lights shrink and dim, and at the aft end
        # the deck overhangs a black tunnel mouth with a thick lit lip and a soft shadow thrown onto the ramp.
        yA, yM, yB, HW0 = by - 22, by + 12, by + 20, 33.5          # full deck width (inside the rails)
        f = lambda y: np.clip((y - yA)/(yM - yA), 0, 1)
        pit = s.poly([(bx - HW0, yA), (bx + HW0, yA), (bx + HW0, yB), (bx - HW0, yB)])
        deck0 = s.rgb.copy()
        s.rgb[pit] = (60, 66, 68); s.a |= pit
        ff = f(yy_)
        for sd in (-1, 1):                                                             # visible cut walls (depth grows aft)
            wall = pit & ((xx_ - bx)*sd > HW0 - 6.0*ff) & (yy_ < yM + 0.5)
            s.rgb[wall] = (np.array([150, 158, 154])*(1.0 - 0.5*ff[..., None]))[wall]
            s.rgb[wall & ((xx_ - bx)*sd > HW0 - 0.7)] = (150, 160, 158)               # deck lip highlight on the cut edge
        floor = pit & (np.abs(xx_ - bx) <= HW0 - 6.0*ff) & (yy_ < yM)
        s.rgb[floor] = (np.array([96, 106, 104])*(1.0 - 0.72*ff[..., None]))[floor]
        for k in range(9):                                                             # grip ribs crowd together as the ramp recedes
            yr = yA + 2 + (yM - yA - 3)*(1 - (1 - k/9)**1.7)
            s.rgb[floor & (np.abs(yy_ - yr) < 0.35)] *= 0.55
        for sd in (-1, 1):                                                             # guide lights at the wall foot: shrink + dim aft
            for k in range(9):
                u = k/9; yl = yA + 3 + (yM - yA - 6)*(1 - (1 - u)**1.5)
                xl = bx + sd*(HW0 - 3.2 - 6.0*f(yl)); r_ = 1.25 - 0.55*u
                s.rgb[s.ell(xl, yl, 0.9*r_, 0.8*r_)] = np.array([130, 255, 180])*(1.0 - 0.5*u)
        mouth = pit & (yy_ >= yM - 3.5)                                                # tunnel mouth: fades to black
        md = np.clip((yy_ - (yM - 3.5))/4.5, 0, 1)
        s.rgb[mouth] = (np.array([40, 46, 48])*(1 - md[..., None]))[mouth]
        over = s.poly(spline([(bx - HW0 - 1, yB + 1), (bx - HW0 - 1, yM + 3), (bx - HW0*0.6, yM - 0.5), (bx, yM - 2.5), (bx + HW0*0.6, yM - 0.5), (bx + HW0 + 1, yM + 3), (bx + HW0 + 1, yB + 1)], 12, False))
        over &= pit
        s.rgb[over] = deck0[over]                                                      # the deck itself overhangs the tunnel
        front = over & ~np.roll(over, int(1.3*s.SS), axis=0)                            # its forward (arched) edge = the lip
        s.rgb[front] = np.clip(deck0[front]*1.5 + 20, 0, 255)
        s.rgb[over & ~front & ~np.roll(over, int(2.4*s.SS), axis=0)] = deck0[over & ~front & ~np.roll(over, int(2.4*s.SS), axis=0)]*0.8
        sh = pit & ~over & np.roll(over, -int(3.0*s.SS), axis=0)                        # overhang shadow falling on the ramp
        s.rgb[sh] *= 0.5
        s.z[pit] = 2.2 - 0.45*ff[pit]; s.z[over] = 2.3                                 # heights for the depth pass (AO in the cut)
    # outer armour rail with the PD blisters; inner wall facing the catapult
    orail = hull & (((xx_ - cx)*g) > 34) & (yy_ > Y0 + 44) & (yy_ < Y1 - 30)
    s.plate(orail, PL_L, z=3.6, bevel=2.2, tilt=(g*0.35, 0), inset=1.6, shadow_k=0.85,
            paint=[(orail & (np.abs(xx_ - X(g, 133)) < 1.6), GRN)], lines=[s.rrect(0, y, W, y + 0.6, 0.2) for y in (142, 228, 312)])
    irail = hull & (((xx_ - cx)*g) < -34) & (yy_ > Y0 + 50) & (yy_ < Y1 - 40)
    s.plate(irail, PL, z=3.4, bevel=1.8, tilt=(-g*0.35, 0), inset=1.4, shadow_k=0.8)
    # engineering block at the stern of each hull + its buried drive core
    eb = hull & (yy_ > Y1 - 30)
    s.plate(eb, PL_D*1.05, z=3.2, bevel=2.4, inset=1.8, shadow_k=0.85)
    zmark(0.4, s.drive_core, cx, Y1 - 12, 11, glow=tuple(PINK))
    VP.core_armour(s, cx, Y1 - 12, 9, glow=tuple(PINK), z=3.6)
sysl('4 hangar entrances per deck (landing gaps): ramps with guide lights sink under an arched brow into the ship', X(-1, 68), 290)
sysl('outer armour rails carry the PD blisters', X(-1, 128), 270); sysl('buried drive core in each hull (armoured cover)', X(1, 67), 412)

for (px, py) in PD:                                                                 # small energy PD SUNK into the outer rails (vanilla protection): collar, socket, outboard lip
    VP.sunk_mount(s, px, py, 5.6, (1 if px > CX else -1, 0), metal=PL_D, lip_metal=PL_L, z=3.3, lip_z=4.3, accent=GRN)

# ================================================================ catapult shuttle (bow) + command stick (stern joint)
sh = s.rrect(CX - 15, 30, CX + 15, 76, 10)
s.plate(sh, PINK, z=3.3, bevel=2.4, dome=0.9, inset=1.6, shadow_k=0.85)
s.rgb[s.rrect(CX - 8, 40, CX + 8, 50, 3)] = PINK_D
s.grille(s.rrect(CX - 9, 58, CX + 9, 68, 1), period=1.8)
sysl('catapult shuttle', CX, 50)
# COMMAND TOWER (Tiamat / Asura concept): 3 stepped tiers over the stern joint, tallest toward the centre,
# wide bridge glass on the front of tier 2, fire-control dome on tier 3; EL pink kept as the tower's livery
cmd1 = s.poly(spline([(X(-1, 14), 290), (X(1, 14), 290), (X(1, 22), 306), (X(1, 25), 414), (X(1, 18), 436), (X(-1, 18), 436), (X(-1, 25), 414), (X(-1, 22), 306)], 10, True))
m1 = s.plate(cmd1, PL, z=4.0, bevel=3.2, dome=1.0, inset=2.4, shadow_k=0.9, paint=[(cmd1 & ((np.abs(yy_ - 424) < 2.2) | (np.abs(yy_ - 316) < 1.6)), PINK)])
s.bolt_row(m1, 1.6, 5)
cmd2 = s.poly(spline([(X(-1, 9), 300), (X(1, 9), 300), (X(1, 17), 312), (X(1, 18), 400), (X(1, 12), 410), (X(-1, 12), 410), (X(-1, 18), 400), (X(-1, 17), 312)], 10, True))
m2 = s.plate(cmd2, PL_L, z=5.2, bevel=2.8, dome=1.3, ridge=('x', CX, 1.8, 18), inset=2.0, shadow_k=0.9)
glass = s.poly(spline([(X(-1, 9), 303), (X(1, 9), 303), (X(1, 14.5), 311), (X(1, 14.5), 317), (X(1, 8), 310), (X(-1, 8), 310), (X(-1, 14.5), 317), (X(-1, 14.5), 311)], 8, True)) & m2
gy = np.clip((yy_ - 302)/14, 0, 1); s.rgb[glass] = (SCREEN*(1.4 - 0.6*gy[..., None]))[glass]
for k_ in range(-15, 16, 4): s.rgb[glass & (np.abs(xx_ - (CX + k_)) < 0.35)] = (26, 34, 60)
cmd3 = s.poly(spline([(X(-1, 6), 330), (X(1, 6), 330), (X(1, 11), 340), (X(1, 11), 392), (X(1, 7), 400), (X(-1, 7), 400), (X(-1, 11), 392), (X(-1, 11), 340)], 8, True))
s.plate(cmd3, PL_L*1.03, z=6.3, bevel=2.2, dome=1.3, ridge=('x', CX, 1.4, 11), inset=1.6, shadow_k=0.9, paint=[(cmd3 & (np.abs(yy_ - 334) < 1.6), PINK)])
s.mount(CX, 380, 4.4, PL, well_col=(110, 60, 96))
for yv in (350, 362): s.grille(s.rrect(CX - 7, yv, CX + 7, yv + 6, 1), period=1.6)
tail = s.rrect(CX - 4, 434, CX + 4, 454, 3)                                            # EL stick remnant: comms spine aft
s.plate(tail, PINK*0.95, z=3.4, bevel=1.4, dome=0.8, inset=0.8, shadow_k=0.8)
sysl('command tower (3 tiers), bridge glass forward, fire-control dome; pink comms spine aft', CX, 350)

# ================================================================ livery + symmetry + lights
armour = s.a.copy()
s.livery(armour, (np.abs(yy_ - 52) < 3) & ((np.abs(xx_ - 68) < 40) | (np.abs(xx_ - 202) < 40)), tuple(GRN), keep=0.3)
s.emblem(X(-1, 67), Y1 - 44, 4.0) if False else None
_h = CX*s.SS
s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
s.lights([(X(-1, 112), 90), (X(1, 112), 90), (X(-1, 100), 410), (X(1, 100), 410), (CX, 29)],
         [(255, 70, 60), (90, 255, 120), (255, 70, 60), (90, 255, 120), (255, 255, 240)])

import pickle; pickle.dump((s.rgb, s.a, s.z), open(_ROOT + '/_scratch/sa11.pkl','wb'))
sprite = s.render()
sprite.save(_ROOT + '/ss_style/artemis_ss_v12.png')
json.dump(dict(W=W, H=H, slots=SLOTS, ENG=ENG, small=SMALL, lat=[]), open(_ROOT + '/ss_style/artemis_ss_v12_slots.json', 'w'))
json.dump(SYSTEMS, open(_ROOT + '/ss_style/artemis_v12_systems.json', 'w'))
print('ok')
