import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Duilius - Starsector style v1, drawn top-down from the approved 3D block-out (ss/duilius3d.html v1).
Gunmetal armoured capsule, yellow livery, cobalt claw bays down both flanks (4 hatches each = 8 claws, ship system);
2 LARGE ballistic under the bow (under-hull slots: nothing painted, the weapon sprites' barrels poke past the nose);
6 small ballistic PD sunk into the upper hull; drive core under an armoured petal cover; 3-tier command tower with pink glass;
ribbed drive collar + one big bell; 2 small diagonal jets."""
import json, numpy as np
import vstyle, vparts as VP
from vstyle import Ship, spline

W, H, CX = 190, 436, 95
HW, C0, C1, NOSE, TAIL = 52, 100, 310, 52, 34
BAY0, BAY1 = 112, 322
HATCH = (136, 191, 246, 301)
PD = [(CX + g*30, py) for g in (-1, 1) for py in (96, 176, 256)]
LB = [(CX - 30, 66), (CX + 30, 66)]
ENG = [(CX, 416)]

AR = np.array([143, 151, 159]); AR_D = np.array([96, 103, 111]); AR_L = np.array([182, 190, 198])
YEL = np.array([255, 198, 46]); COB = np.array([47, 126, 240]); COB_L = np.array([122, 184, 255]); PNK = np.array([255, 90, 168])
SEAM = (40, 44, 50)
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))

_L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = CX
s = Ship(W, H, seed=131)
s.auto_z = True; s.depth = dict(unit=7.0, s_str=0.9, tint=0.38, ao=0.6, ao_r=5, sdir=((0.6, 0.8), (-0.6, 0.8)), s_soft=0.9)
_plate0, _bolt0 = s.plate, s.bolt_row
def _plate(mask, color, *a, **k):
    k.setdefault('tex', 0.018); k.setdefault('grime', 0.0); k.setdefault('notch', 0); return _plate0(mask, color, *a, **k)
def _bolt(m, inset=1.8, spacing=4.0, seed=0):
    if m is not None and m.sum()/s.SS**2 > 700: _bolt0(m, inset, spacing*2.4)
s.plate, s.bolt_row = _plate, _bolt
X = lambda g, dx: CX + g*dx
yy_ = s.yy/s.SS; xx_ = s.xx/s.SS; ax_ = np.abs(xx_ - CX)
def sec(py): return np.sqrt(np.clip(1 - ((C0 - py)/NOSE)**2, 0, 1)) if py < C0 else (np.sqrt(np.clip(1 - ((py - C1)/TAIL)**2, 0, 1)) if py > C1 else 1.0)
halfw = np.where(yy_ < C0, HW*np.sqrt(np.clip(1 - ((C0 - yy_)/NOSE)**2, 0, 1)), np.where(yy_ > C1, HW*np.sqrt(np.clip(1 - ((yy_ - C1)/TAIL)**2, 0, 1)), HW))

# ================================================================ silhouette + machinery base
hull = (ax_ <= halfw) & (yy_ > C0 - NOSE) & (yy_ < C1 + TAIL)
bays = s.rrect(X(-1, HW + 10), BAY0 - 6, X(-1, HW - 6), BAY1 + 6, 1.5) | s.rrect(X(1, HW - 6), BAY0 - 6, X(1, HW + 10), BAY1 + 6, 1.5)
drive = s.rrect(CX - 44, 340, CX + 44, 398, 3)
s.guts(hull | bays | drive, seed=133, tone=(46, 50, 56), minc=3, maxc=10); s.z[:] = 0

# ================================================================ main drive: ribbed collar (EL ribs) + one big bell, 2 small diagonal jets
bell = s.poly([(CX - 30, 396), (CX + 30, 396), (CX + 36, 423), (CX - 36, 423)])
s.plate(bell, AR_D, z=0.8, bevel=2.2, dome=0.8, inset=1.0, shadow_k=0.9)
s.rgb[bell & (yy_ > 420.5)] = (255, 236, 170)                                       # hot lip of the bell
s.plate(s.rrect(CX - 33, 340, CX + 33, 400, 4), AR_D*0.9, z=1.0, bevel=2.0, dome=1.0, shadow_k=0.9)     # neck
for i, (r, y) in enumerate(((44, 352), (43, 364), (41, 376), (39, 388))):
    rib = s.rrect(CX - r, y - 3.5, CX + r, y + 3.5, 2.5)
    s.plate(rib, YEL*0.95 if i == 0 else AR_L, z=1.4, bevel=1.4, dome=0.5, inset=0.0, shadow_k=0.9)
    for k in range(-5, 6):                                                          # notches round each rib
        nx = CX + r*np.sin(k*np.pi/12)
        s.rgb[rib & (np.abs(xx_ - nx) < 0.7)] = SEAM
SMALL = []
for g in (-1, 1):
    e = np.array([X(g, 44), 334.0]); n = np.array([g*0.7071, 0.7071])
    VP.diag_jet(s, g, *(e + n*2.0), 10, T=34, metal=(176, 184, 192), z=1.8); ex_ = e + n*12; SMALL.append((float(ex_[0]), float(ex_[1]), 135 if g < 0 else -135))
sysl('ribbed drive collar + one big bell, 2 small diagonal jets', CX, 400)

# ================================================================ main hull: capsule shell, seams, yellow hoops, spine + stripes, tiles, windows
s.plate(hull, AR, z=3.4, bevel=7.0, dome=2.2, inset=2.2, shadow_k=0.95)
for py in (128, 158, 188, 236, 266, 296): s.rgb[hull & (np.abs(yy_ - py) < 0.55) & (ax_ < halfw - 2)] = SEAM
for py in (106, 318): s.rgb[hull & (np.abs(yy_ - py) < 1.1) & (ax_ < halfw - 1.5)] = YEL*0.95
for (a, b) in ((102, 196), (236, 262)):
    sp = s.rrect(CX - 6, a, CX + 6, b, 1.5)
    s.plate(sp, AR_L, z=4.2, bevel=1.2, dome=0.3, inset=0.6, shadow_k=0.9)
    for g in (-1, 1): s.rgb[s.rrect(X(g, 9) - 1, a, X(g, 9) + 1, b, 0.5)] = YEL
for g in (-1, 1):
    for py in range(112, 300, 26):
        if abs(py - 176) < 14 or abs(py - 256) < 14 or py > 262: continue
        t = s.rrect(min(X(g, 12.5), X(g, 21.5)), py, max(X(g, 12.5), X(g, 21.5)), py + 20, 1.2)
        s.plate(t, AR_L, z=4.0, bevel=1.0, dome=0.2, tilt=(g*0.2, 0), inset=0.5, shadow_k=0.9)
    for py in range(116, 301, 12):                                                  # lit crew windows
        if min(abs(py - p) for p in (96, 176, 256)) < 10: continue
        s.rgb[s.rrect(X(g, 41.6) - 0.8, py - 2.4, X(g, 41.6) + 0.8, py + 2.4, 0.3)] = (255, 236, 170)
nose = hull & (yy_ < C0)
s.plate(nose, AR_L, z=3.6, bevel=5.0, dome=1.8, inset=1.6, shadow_k=0.95)
for f in (0.3, 0.55, 0.8):
    k = np.sin(np.pi/2*f); yv = C0 - NOSE*np.cos(np.pi/2*f)
    s.rgb[nose & (np.abs(yy_ - yv) < 0.6) & (ax_ < HW*k)] = AR*0.9
s.plate(s.ell(CX, 53, 7, 4.5), np.array([140, 225, 250]), z=4.2, bevel=1.4, dome=1.0, inset=0.4, shadow_k=0.9)     # sensor eye
sysl('armoured capsule: yellow hoops + spine stripes, armour tiles, crew windows, nose hoops + sensor eye', X(1, 20), 140)

# ================================================================ claw bays (cobalt galleries): top face, thin yellow outer rail, end caps, hatch frames
for g in (-1, 1):
    top = s.rrect(min(X(g, HW - 3), X(g, HW + 10)), BAY0, max(X(g, HW - 3), X(g, HW + 10)), BAY1, 1.2)
    s.plate(top, COB*1.1, z=3.6, bevel=1.6, dome=0.3, tilt=(g*0.35, 0), inset=0.8, shadow_k=0.95)
    rail = s.rrect(min(X(g, HW + 6.5), X(g, HW + 10.5)), BAY0 - 2, max(X(g, HW + 6.5), X(g, HW + 10.5)), BAY1 + 2, 1.0)
    s.plate(rail, YEL, z=3.9, bevel=1.0, dome=0.3, shadow_k=0.9)
    for yb in (BAY0 - 6, BAY1 - 2):                                                 # armoured end caps
        s.plate(s.rrect(min(X(g, HW - 4), X(g, HW + 11)), yb, max(X(g, HW - 4), X(g, HW + 11)), yb + 8, 1.5), AR_D, z=4.0, bevel=1.4, inset=0.6, shadow_k=0.9)
    for hy in HATCH:                                                                # hatch frames: door seam + lit tab on the outer lip
        s.rgb[top & (np.abs(yy_ - (hy - 11)) < 0.5)] = SEAM; s.rgb[top & (np.abs(yy_ - (hy + 11)) < 0.5)] = SEAM
        tab = s.rrect(min(X(g, HW + 1.5), X(g, HW + 5.5)), hy - 8, max(X(g, HW + 1.5), X(g, HW + 5.5)), hy + 8, 1.2)
        s.plate(tab, COB_L, z=3.8, bevel=0.8, dome=0.3, shadow_k=0.8)
        s.rgb[tab & (np.abs(yy_ - hy) < 0.45)] = SEAM
sysl('claw bays: 4 hatches per side = 8 grapple claws (ship system)', X(-1, 54), 216)

# ================================================================ drive core under an armoured petal cover
VP.core_armour(s, CX, 216, 13, glow=(255, 200, 80), metal=AR_L*0.82, z=4.4)
sysl('drive core deep below an armoured petal cover', CX, 216)

# ================================================================ 6 small ballistic PD sunk into the upper hull (yellow outboard lips)
for (px, py) in PD:
    VP.sunk_mount(s, px, py, 5.4, (1 if px > CX else -1, 0), metal=AR_D, lip_metal=AR_L, z=3.9, lip_z=4.9, accent=YEL)
sysl('6 small ballistic PD sunk, 3 per side, 240 deg to their side', X(-1, 30), 176)

# ================================================================ COMMAND TOWER (3 tiers), yellow band, pink visor glass
def tier(hw, y0, y1, r):
    return s.poly(spline([(X(-1, hw - r), y0), (X(1, hw - r), y0), (X(1, hw), y0 + r), (X(1, hw), y1 - r), (X(1, hw - r), y1),
                          (X(-1, hw - r), y1), (X(-1, hw), y1 - r), (X(-1, hw), y0 + r)], 8, True))
c0 = tier(25, 264, 336, 11)
s.plate(c0, YEL*0.92, z=5.0, bevel=1.4, shadow_k=0.95)
c1 = tier(23.5, 266, 334, 10)
s.plate(c1, AR, z=5.4, bevel=2.6, dome=0.9, inset=1.8, shadow_k=0.95)
s.bolt_row(c1, 1.6, 5)
c2 = tier(17.5, 273, 323, 8)
s.plate(c2, AR_L, z=6.4, bevel=2.2, dome=1.0, ridge=('x', CX, 1.2, 17), inset=1.4, shadow_k=0.95)
glass = tier(16, 274.5, 281, 3) & c2
gy = np.clip((yy_ - 274.5)/6.5, 0, 1); s.rgb[glass] = np.clip(PNK*(1.15 - 0.45*gy[..., None]), 0, 255)[glass]
for k_ in (-9, 0, 9): s.rgb[glass & (np.abs(xx_ - (CX + k_)) < 0.35)] = (70, 20, 45)
for g in (-1, 1):
    for k in range(3): s.rgb[s.rrect(min(X(g, 8), X(g, 15)), 312 + k*4, max(X(g, 8), X(g, 15)), 313 + k*4, 0.3)] = SEAM
c3 = tier(10.5, 285, 315, 6)
s.plate(c3, AR_L*1.04, z=7.4, bevel=1.8, dome=1.0, inset=1.1, shadow_k=0.95)
s.plate(s.disk(CX, 302, 5), AR_L, z=7.9, bevel=1.2, dome=1.0, inset=0.5, shadow_k=0.95)
s.rgb[s.disk(CX, 302, 1.8)] = (110, 40, 80)
sysl('command tower (3 tiers), pink visor glass forward, yellow band', CX, 278)

# ================================================================ symmetry + lights
_h = CX*s.SS
s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
s.lights([(X(-1, HW + 8), BAY0 - 8), (X(1, HW + 8), BAY0 - 8), (CX, 314)], [(255, 70, 60), (90, 255, 120), (255, 255, 240)])
sprite = s.render()
sprite.save(_ROOT + '/ss_style/duilius_ss_v1.png')
slots = [dict(px=x, py=y, size='SMALL', type='BALLISTIC', mount='TURRET', angle=(90 if x < CX else -90), arc=240) for (x, y) in PD]
slots += [dict(px=x, py=y, size='LARGE', type='BALLISTIC', mount='TURRET', angle=0, arc=20, hide=True) for (x, y) in LB]
slots += [dict(px=X(g, HW + 10), py=hy, size='SMALL', type='SYSTEM', mount='HIDDEN', angle=(90 if g < 0 else -90), arc=90) for g in (-1, 1) for hy in HATCH]
json.dump(dict(W=W, H=H, slots=slots, ENG=ENG, small=SMALL, lat=[]), open(_ROOT + '/ss_style/duilius_ss_v1_slots.json', 'w'))
json.dump(SYSTEMS, open(_ROOT + '/ss_style/duilius_v1_systems.json', 'w'))
print('ok')
