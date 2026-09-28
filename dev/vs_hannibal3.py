import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Hannibal - Starsector style v1, drawn top-down from the approved 3D block-out (ss/hannibal3d.html v3).
Bulb body (shingled dome tiles, meridian ribs, violet rim band, orange window rows) + long snout riding over its front
(spine plate, armour panels, hoops, side belts + lights, nose hoops + sensor); 3 medium energy IN LINE at the snout front
(2 on top on orange rings, 1 under the tip = hidden), 90 deg forward arcs; 6 small ballistic PD sunk in the bulb walls;
raised pink command head with cyan visor; one central drive (pink ring stack) + 2 diagonal jets."""
import json, numpy as np
from scipy import ndimage as ndi
import vstyle, vparts as VP
from vstyle import Ship, spline

W, H, CX = 220, 420, 110
BCX, BCY, BRX, BRZ = CX, 272, 96, 104
SNX0, SNX1, SNY0, SNY1 = CX - 50, CX + 50, 34, 250
MEN = [(CX - 30, 52), (CX + 30, 52)]; TIP = (CX, 52)
PD = [(CX + s*dx, y) for s in (-1, 1) for dx, y in ((89, 232), (96, 272), (89, 312))]
HEAD = (CX, 332); ENG = [(CX, 390)]

PL = np.array([136, 134, 144]); PL_D = np.array([100, 98, 110]); PL_L = np.array([164, 162, 172])
VIO = np.array([196, 118, 232]); ORG = np.array([255, 166, 64]); PINK = np.array([240, 96, 160]); CYN = np.array([120, 230, 250])
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))

_L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = CX
s = Ship(W, H, seed=111)
s.auto_z = True; s.depth = dict(unit=7.0, s_str=0.9, tint=0.38, ao=0.6, ao_r=5, sdir=((0.6, 0.8), (-0.6, 0.8)), s_soft=0.9)
_plate0, _bolt0 = s.plate, s.bolt_row
def _plate(mask, color, *a, **k):
    k.setdefault('tex', 0.018); k.setdefault('grime', 0.0); k.setdefault('notch', 0); return _plate0(mask, color, *a, **k)
def _bolt(m, inset=1.8, spacing=4.0, seed=0):
    if m is not None and m.sum()/s.SS**2 > 700: _bolt0(m, inset, spacing*2.4)
s.plate, s.bolt_row = _plate, _bolt
def zmark(z, fn, *a, **k):
    before = s.rgb.copy(); a0 = s.a.copy(); r = fn(*a, **k)
    ch = (np.abs(s.rgb - before).sum(2) > 0.5) | (s.a & ~a0); s.z[ch] = z; return r
X = lambda g, dx: CX + g*dx
yy_ = s.yy/s.SS; xx_ = s.xx/s.SS; ax_ = np.abs(xx_ - CX)
MET = (150, 148, 156)

# ================================================================ silhouette
u_ = (xx_ - BCX)/BRX; v_ = (yy_ - BCY)/BRZ; rb = np.hypot(u_, v_); ab = np.degrees(np.arctan2(v_, u_))   # -90 = forward
bulb = rb <= 1.0
snout = s.rrect(SNX0, SNY0, SNX1, SNY1, 12) | s.ell(CX, SNY0 + 2, 50, 24)
s.guts(bulb | snout, seed=113, tone=(52, 50, 58), minc=3, maxc=10); s.z[:] = 0

# ================================================================ drive + jets (under the bulb's stern)
hous = s.disk(CX, 376, 30) & (yy_ > 368)
for (ex, ey) in ENG:
    for k, (r, y) in enumerate(((26, 380), (21, 387), (16, 393))):
        rg = s.ell(ex, y, r, 6.5)
        s.plate(rg, PINK*(1 - 0.1*k), z=1.0 + 0.1*k, bevel=1.6, dome=0.6, inset=0.6, shadow_k=0.8)
    s.rgb[s.ell(ex, 398, 9, 3)] = (255, 210, 235)
SMALL = []
for g in (-1, 1):
    n = np.array([g*0.7071, 0.7071]); e = np.array([BCX + g*BRX*0.70, BCY + BRZ*0.70])
    VP.diag_jet(s, g, *(e + n*3.0), 14, T=44, metal=(176, 174, 180), z=2.4); ex_ = e + n*16; SMALL.append((float(ex_[0]), float(ex_[1]), 135 if g < 0 else -135))
sysl('one central drive (pink ring stack) + 2 diagonal jets', CX, 392)

# ================================================================ bulb: base shell, 3 rows of shingled dome tiles, meridian ribs, violet rim band
s.plate(bulb, PL_D, z=1.6, bevel=3.0, dome=1.6, inset=2.0, shadow_k=0.9)
for row, (r0, r1) in enumerate(((0.80, 0.93), (0.64, 0.79), (0.46, 0.63))):
    n = (18, 16, 12)[row]
    for k in range(n):
        a0 = -180 + k*360/n + (row % 2)*180/n
        dang = ((ab - a0 - 180/n + 180) % 360) - 180
        tile = bulb & (rb > r0) & (rb < r1) & (np.abs(dang) < 180/n - 1.4)
        if (tile & snout).sum() > 0.5*tile.sum(): continue
        s.plate(tile, PL_L if (k + row) % 2 else PL*1.06, z=2.0 + 0.35*row, bevel=1.4, dome=0.4, inset=0.8, shadow_k=0.9)
crown = bulb & (rb < 0.45) & ~snout
s.plate(crown, PL_L, z=3.3, bevel=2.0, dome=0.8, inset=1.2, shadow_k=0.95, paint=[(crown & (np.abs(rb - 0.40) < 0.015), VIO)])
rim = bulb & (rb > 0.94)
s.plate(rim, PL, z=1.9, bevel=1.4, inset=0.6, shadow_k=0.9, paint=[(rim & (np.abs(rb - 0.972) < 0.02), VIO)])
for a_ in range(0, 360, 26):                                                       # meridian ribs
    if abs(((a_ + 90 + 180) % 360) - 180) < 40: continue
    rib = bulb & (np.abs(((ab - a_ + 180) % 360) - 180) < 0.9) & (rb > 0.46) & (rb < 0.94)
    s.rgb[rib] = (60, 58, 68)
for g in (-1, 1):                                                                  # orange window rows (crew decks) at the rim
    for a_ in np.arange(20, 150, 7.5):
        ang = np.radians(-90 + g*a_); px, py = BCX + BRX*0.965*np.cos(ang), BCY + BRZ*0.965*np.sin(ang)
        if abs(px - CX) < 54 and py < SNY1 + 4: continue
        s.rgb[s.rrect(px - 1.0, py - 1.4, px + 1.0, py + 1.4, 0.4)] = ORG
    for k in range(5):                                                              # radiator fins, rear quarters
        ang = np.radians(-90 + g*(118 + k*5)); px, py = BCX + BRX*0.9*np.cos(ang), BCY + BRZ*0.9*np.sin(ang)
        fin = s.rrect(px - 1.0, py - 5, px + 1.0, py + 5, 0.4)
        s.plate(fin, PL_L, z=2.4, bevel=0.6, inset=0.2, shadow_k=0.9)
    for k in range(4):                                                              # core heat vents (the core is inside the bulb)
        s.rgb[s.rrect(X(g, 83) - 1.2, 236 + k*6, X(g, 83) + 1.2, 239 + k*6, 0.4)] = VIO
sysl('bulb: shingled dome tiles, ribs, violet rim band, orange window rows, radiator fins', X(-1, 70), 300)

# ================================================================ snout (rides over the bulb's front): shell, spine, panels, hoops, belts, nose
s.plate(snout, PL, z=4.4, bevel=3.4, dome=1.2, inset=2.2, shadow_k=0.95)
for g in (-1, 1):
    belt = snout & ((xx_ - CX)*g > 44) & (yy_ > 76) & (yy_ < 236)
    s.plate(belt, PL_L, z=4.6, bevel=1.2, tilt=(g*0.5, 0), inset=0.5, shadow_k=0.9)
    for yv in np.arange(92, 236, 24): s.rgb[s.rrect(X(g, 49) - 0.8, yv - 1, X(g, 49) + 0.8, yv + 1, 0.3)] = ORG      # side lights
    for pz in range(64, 240, 30):                                                   # raised armour panels either side of the spine
        pn = s.rrect(min(X(g, 21), X(g, 35)), pz + 2, max(X(g, 21), X(g, 35)), pz + 27, 2) & snout
        s.plate(pn, PL_L if (pz//30) % 2 else PL*1.04, z=5.2, bevel=1.4, dome=0.3, tilt=(g*0.25, 0), inset=0.8, shadow_k=0.9)
    s.rgb[snout & (np.abs(xx_ - X(g, 16)) < 0.8) & (yy_ > 60) & (yy_ < 245)] = VIO    # violet livery lines
spine = s.rrect(CX - 13, 52, CX + 13, 246, 3)
s.plate(spine, PL_L, z=5.8, bevel=1.6, dome=0.4, inset=1.0, shadow_k=0.95)
for yv in (70, 110, 150, 190, 230): s.rgb[snout & (np.abs(yy_ - yv) < 0.6) & ~spine] = (60, 58, 68)   # hoop seams
nose = snout & (yy_ < 40)
s.plate(nose, PL_L, z=5.0, bevel=2.0, dome=0.8, inset=1.0, shadow_k=0.95)
for f in (0.35, 0.62, 0.9):                                                        # nose armour hoops (arcs)
    s.rgb[nose & (np.abs(yy_ - (34 - 24*np.cos(np.pi/2*f))) < 0.6)] = (178, 176, 186)
s.plate(s.ell(CX, 13, 8, 5), CYN*0.85, z=5.6, bevel=1.4, dome=1.0, inset=0.4, shadow_k=0.9)                     # sensor dome
sysl('snout: spine plate, armour panels, hoops, side belts + lights, nose hoops + sensor', X(1, 28), 150)

# ================================================================ 3 medium energy IN LINE at the snout front (orange rings; middle one is under the tip)
for (mx, my) in MEN:
    base = s.disk(mx, my, 13)
    s.plate(base, PL_D, z=5.9, bevel=1.6, inset=0.8, shadow_k=0.95)
    rr = np.hypot(xx_ - mx, yy_ - my)
    s.plate(base & (rr > 9.8), ORG, z=6.2, bevel=1.2, dome=0.5, inset=0.3, shadow_k=0.9)
    s.rgb[rr < 8.6] = (30, 30, 36); s.z[rr < 8.6] = 5.8
sysl('3 medium energy in line at the snout front (2 on orange rings, 1 under the tip), 90 deg forward', CX, 52)

# ================================================================ 6 small ballistic PD sunk in the bulb walls (violet lips)
for (px, py) in PD:
    VP.sunk_mount(s, px, py, 6.0, (1 if px > CX else -1, (py - BCY)/BRZ), metal=PL_D, lip_metal=PL_L, z=2.2, lip_z=3.2, accent=VIO)
sysl('6 small ballistic PD in the bulb walls', X(-1, 92), 272)

# ================================================================ COMMAND TOWER (Terra Light concept, 3 tiers) with the EL cues: pink top tier, cyan visor glass
from vstyle import spline as _sp
def tier(hw, y0, y1, r):
    return s.poly(_sp([(X(-1, hw - r), y0), (X(1, hw - r), y0), (X(1, hw), y0 + r), (X(1, hw), y1 - r), (X(1, hw - r), y1),
                       (X(-1, hw - r), y1), (X(-1, hw), y1 - r), (X(-1, hw), y0 + r)], 8, True))
c1 = tier(33, 282, 374, 12)
s.plate(c1, PL, z=5.0, bevel=3.0, dome=1.0, inset=2.2, shadow_k=0.95, paint=[(c1 & (np.abs(yy_ - 366) < 1.8), VIO)])
s.bolt_row(c1, 1.6, 5)
c2 = tier(25, 286, 362, 10)
m2 = s.plate(c2, PL_L, z=6.2, bevel=2.6, dome=1.2, ridge=('x', CX, 1.6, 25), inset=1.8, shadow_k=0.95)
glass = tier(23, 288, 296, 3) & c2
gy = np.clip((yy_ - 288)/8, 0, 1); s.rgb[glass] = (CYN*(1.2 - 0.5*gy[..., None]))[glass]
for k_ in range(-20, 21, 5): s.rgb[glass & (np.abs(xx_ - (CX + k_)) < 0.35)] = (40, 70, 90)
for g in (-1, 1):
    for k in range(4): s.rgb[s.rrect(min(X(g, 12), X(g, 22)), 344 + k*4, max(X(g, 12), X(g, 22)), 345 + k*4, 0.3)] = (60, 58, 68)   # vents
c3 = tier(15, 302, 348, 8)
s.plate(c3, PL_L*1.04, z=7.4, bevel=2.2, dome=1.2, inset=1.4, shadow_k=0.95)
s.plate(s.disk(CX, 330, 6.5), PL_L, z=7.9, bevel=1.4, dome=1.0, inset=0.6, shadow_k=0.95)                   # fire-control dome
s.rgb[s.disk(CX, 330, 2.2)] = (60, 90, 120)
sysl('command tower (3 tiers, long), cyan visor glass forward', CX, 292)

# ================================================================ symmetry + lights
_h = CX*s.SS
s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
s.lights([(X(-1, 95), 262), (X(1, 95), 262), (CX, 8)], [(255, 70, 60), (90, 255, 120), (255, 255, 240)])
sprite = s.render()
sprite.save(_ROOT + '/ss_style/hannibal_ss_v3.png')
slots = [dict(px=x, py=y, size='MEDIUM', type='ENERGY', mount='TURRET', angle=0, arc=90) for (x, y) in MEN]
slots.append(dict(px=TIP[0], py=TIP[1], size='MEDIUM', type='ENERGY', mount='TURRET', angle=0, arc=90, hide=True))
slots += [dict(px=x, py=y, size='SMALL', type='BALLISTIC', mount='TURRET', angle=(90 if x < CX else -90), arc=200) for (x, y) in PD]
json.dump(dict(W=W, H=H, slots=slots, ENG=ENG, small=SMALL, lat=[]), open(_ROOT + '/ss_style/hannibal_ss_v3_slots.json', 'w'))
json.dump(SYSTEMS, open(_ROOT + '/ss_style/hannibal_v3_systems.json', 'w'))
print('ok')
