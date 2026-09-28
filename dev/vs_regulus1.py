import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Regulus - Starsector style v1, drawn top-down from the approved 3D block-out (ss/regulus3d.html v3).
Sand armour + teal livery (distinct from Hannibal). Bulb body (shingled tiles, ribs, teal rim band) + long snout over its front;
2 lime fore bubble-missile pods tucked under the snout tip (4 warheads each, fwd); 2 lime aft pods wrapped round the bulb's
rear flanks (8 warheads each on the front face, fwd); 10 small energy PD sunk (2+3 per side); 3-tier command tower with amber
visor glass; one central drive (teal ring stack) + 2 small diagonal jets tucked beside it."""
import json, numpy as np
import vstyle, vparts as VP
from vstyle import Ship, spline

W, H, CX = 330, 412, 165
BCY, BRX, BRZ = 272, 92, 100
SW, SNY0, SNY1 = 48, 30, 250
PA0, PA1, PI0, PI1 = np.pi/2, 2.36, 3, 39          # aft pod angle span + radial offsets (same as the 3D)
FP = [(109, 66, 0.35), (221, 66, -0.35)]           # fore pods: centre + yaw (rad)
PD_SN = [(CX + g*49.5, py) for g in (-1, 1) for py in (130, 185)]
PD_BD = [(CX + g*BRX*np.sin(a), BCY - BRZ*np.cos(a), a, g) for g in (-1, 1) for a in (0.78, 1.04, 1.30)]
ENG = [(CX, 392)]

AR = np.array([169, 162, 144]); AR_D = np.array([122, 116, 98]); AR_L = np.array([202, 195, 174])
TEAL = np.array([51, 201, 180]); TEAL_D = np.array([31, 143, 132]); LIME = np.array([180, 220, 60]); LIME_D = np.array([112, 146, 34])
WHC = np.array([255, 208, 64]); RED = np.array([255, 58, 80]); AMB = np.array([255, 194, 74]); SEAM = (62, 58, 50)
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))

_L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = CX
s = Ship(W, H, seed=121)
s.auto_z = True; s.depth = dict(unit=7.0, s_str=0.9, tint=0.38, ao=0.6, ao_r=5, sdir=((0.6, 0.8), (-0.6, 0.8)), s_soft=0.9)
_plate0, _bolt0 = s.plate, s.bolt_row
def _plate(mask, color, *a, **k):
    k.setdefault('tex', 0.018); k.setdefault('grime', 0.0); k.setdefault('notch', 0); return _plate0(mask, color, *a, **k)
def _bolt(m, inset=1.8, spacing=4.0, seed=0):
    if m is not None and m.sum()/s.SS**2 > 700: _bolt0(m, inset, spacing*2.4)
s.plate, s.bolt_row = _plate, _bolt
X = lambda g, dx: CX + g*dx
yy_ = s.yy/s.SS; xx_ = s.xx/s.SS

def crescent(g, o0, o1, a0, a1, n=40):
    pt = lambda o, a: (CX + g*(BRX + o)*np.sin(a), BCY - (BRZ + o)*np.cos(a))
    return s.poly([pt(o0, a0 + (a1 - a0)*i/n) for i in range(n + 1)] + [pt(o1, a0 + (a1 - a0)*i/n) for i in range(n, -1, -1)])
def obox(cx, cy, yaw, w, l, dy=0.0):
    """rotated rectangle (top view) of a pod with local width w (x) and length l (fore-aft); +yaw turns the front outward-left"""
    ux, uy = np.cos(yaw), -np.sin(yaw); fx, fy = -np.sin(yaw), -np.cos(yaw)      # local x, local forward
    c = [(cx + ux*a*w/2 + fx*b*l/2, cy + uy*a*w/2 + fy*b*l/2) for a, b in ((-1, 1), (1, 1), (1, -1), (-1, -1))]
    return s.poly(c)
def warhead(x, y, fx, fy):
    """one bubble warhead seen from above: yellow case behind, red dome tip in front, pointing (fx, fy)"""
    nx, ny = -fy, fx
    case = s.poly([(x + nx*4.2, y + ny*4.2), (x - nx*4.2, y - ny*4.2), (x - nx*4.2 - fx*6, y - ny*4.2 - fy*6), (x + nx*4.2 - fx*6, y + ny*4.2 - fy*6)])
    s.plate(case, WHC, z=3.0, bevel=1.0, dome=0.3, shadow_k=0.8, outline=0.6)
    dome_ = s.disk(x, y, 4.2) & (((xx_ - x)*fx + (yy_ - y)*fy) > -0.3)
    s.plate(dome_, RED, z=3.2, bevel=1.6, dome=0.8, shadow_k=0.8, outline=0.6)

# ================================================================ silhouette + machinery base
u_ = (xx_ - CX)/BRX; v_ = (yy_ - BCY)/BRZ; rb = np.hypot(u_, v_); ab = np.degrees(np.arctan2(v_, u_))   # -90 = forward
bulb = rb <= 1.0
snout = s.rrect(CX - SW, SNY0, CX + SW, SNY1, 12) | s.ell(CX, SNY0 + 2, SW, 26)
s.guts(bulb | snout, seed=123, tone=(56, 53, 46), minc=3, maxc=10); s.z[:] = 0

# ================================================================ drive + small diagonal jets tucked beside it
s.plate(s.ell(CX, 376, 34, 6) & (yy_ > 372), AR_D, z=1.0, bevel=1.6, inset=0.6, shadow_k=0.8)            # housing collar
for k in range(8):                                                                                     # cooling fins on the collar
    a = np.radians(k*45 + 22.5); fx_ = CX + 31*np.cos(a)
    if np.sin(a) > -0.2: s.plate(s.rrect(fx_ - 1.2, 375, fx_ + 1.2, 386, 0.4), AR_L, z=1.1, bevel=0.6, shadow_k=0.8)
for k, (r, y) in enumerate(((26, 381), (21, 388), (16, 394))):
    s.plate(s.ell(CX, y, r, 6.5), TEAL_D*(1 - 0.1*k), z=1.3 + 0.1*k, bevel=1.6, dome=0.6, inset=0.6, shadow_k=0.8)
s.rgb[s.ell(CX, 399, 9, 3)] = (200, 255, 244)
SMALL = []
for g in (-1, 1):
    a = 2.66; e = np.array([CX + g*(BRX + 3)*np.sin(a), BCY - (BRZ + 3)*np.cos(a)]); n = np.array([g*0.7071, 0.7071])
    VP.diag_jet(s, g, *(e + n*2.0), 10, T=34, metal=(186, 180, 164), z=1.6); ex_ = e + n*12; SMALL.append((float(ex_[0]), float(ex_[1]), 135 if g < 0 else -135))
sysl('one central drive (teal ring stack) + 2 small diagonal jets beside it (slower than Hannibal)', CX, 392)

# ================================================================ bulb: base shell, shingled tile rows, ribs, teal rim band, crown ring
s.plate(bulb, AR_D, z=1.6, bevel=3.0, dome=1.6, inset=2.0, shadow_k=0.9)
for row, (r0, r1) in enumerate(((0.80, 0.93), (0.64, 0.79), (0.46, 0.63))):
    n = (14, 12, 10)[row]
    for k in range(n):
        a0 = -180 + k*360/n + (row % 2)*180/n
        dang = ((ab - a0 - 180/n + 180) % 360) - 180
        tile = bulb & (rb > r0) & (rb < r1) & (np.abs(dang) < 180/n - 1.6)
        if (tile & snout).sum() > 0.4*tile.sum(): continue
        s.plate(tile, AR_L if (k + row) % 2 else AR*1.05, z=2.0 + 0.35*row, bevel=1.4, dome=0.4, inset=0.8, shadow_k=0.9)
crown = bulb & (rb < 0.45) & ~snout
s.plate(crown, AR_L, z=3.3, bevel=2.0, dome=0.8, inset=1.2, shadow_k=0.95, paint=[(crown & (np.abs(rb - 0.40) < 0.015), TEAL)])
rim = bulb & (rb > 0.94)
s.plate(rim, AR, z=1.9, bevel=1.4, inset=0.6, shadow_k=0.9, paint=[(rim & (np.abs(rb - 0.972) < 0.02), TEAL)])
for a_ in np.arange(0, 360, 360/14):                                                # meridian ribs, none under the snout
    if abs(((a_ + 90 + 180) % 360) - 180) < 36: continue
    s.rgb[bulb & (np.abs(((ab - a_ + 180) % 360) - 180) < 0.9) & (rb > 0.46) & (rb < 0.94)] = (70, 66, 56)
sysl('bulb: shingled tiles, ribs, teal rim band + crown ring (core deep inside)', X(-1, 40), 320)

# ================================================================ aft bubble-missile pods: crescents wrapped round the rear flanks
for g in (-1, 1):
    body = crescent(g, PI0, PI1, PA0, PA1)
    s.plate(body, LIME*0.82, z=2.2, bevel=1.4, inset=0.0, shadow_k=0.95)
    strip = crescent(g, PI0 + 1.2, PI1 + 1.8, PA0 + 0.004, PA1 + 0.01)
    s.plate(strip & ~crescent(g, PI0 + 2.2, PI1 + 0.6, PA0 + 0.02, PA1 - 0.004), AR_L, z=2.5, bevel=0.8, shadow_k=0.8)
    lid = crescent(g, PI0 + 1.8, PI1 + 0.8, PA0 + 0.01, PA1 - 0.004)
    s.plate(lid, LIME*0.92, z=2.9, bevel=1.8, dome=0.5, inset=1.0, shadow_k=0.95)
    pan = crescent(g, PI0 + 12, PI1 - 10, PA0 + 0.10, PA1 - 0.10)
    s.plate(pan, AR_D, z=3.3, bevel=1.4, dome=0.3, inset=0.7, shadow_k=0.9)
    for k in range(1, 4):                                                           # lid seams
        a = PA0 + (PA1 - PA0)*k/4
        p0 = (CX + g*(BRX + PI0 + 4)*np.sin(a), BCY - (BRZ + PI0 + 6)*np.cos(a)); p1 = (CX + g*(BRX + PI1 - 2)*np.sin(a), BCY - (BRZ + PI1 - 4)*np.cos(a))
        t = np.linspace(0, 1, 60)
        for tt in t: s.rgb[s.disk(p0[0] + (p1[0] - p0[0])*tt, p0[1] + (p1[1] - p0[1])*tt, 0.55)] = SEAM
    for c in range(4):                                                              # 8 warheads (2 x 4): top row seen from above
        warhead(CX + g*(BRX + PI0 + 4.5 + c*9), BCY - 1.5, 0.0, -1.0)
    s.plate(s.rrect(min(X(g, BRX + PI0 + 1), X(g, BRX + PI1 + 1)), BCY + 1.2, max(X(g, BRX + PI0 + 1), X(g, BRX + PI1 + 1)), BCY + 3.6, 0.8),
            AR_L, z=3.0, bevel=0.8, shadow_k=0.8)                                  # launcher face frame
sysl('aft bubble-missile pods: 8 warheads each on the front face, 120 deg fwd', X(-1, 115), 300)

# ================================================================ fore bubble-missile pods, tucked so their inner half sits under the snout tip
for (px, py, yaw) in FP:
    s.plate(obox(px, py, yaw, 37.4, 67.4), AR_L, z=3.4, bevel=1.0, shadow_k=0.95)
    s.plate(obox(px, py, yaw, 35, 65), LIME*0.92, z=3.8, bevel=1.8, dome=0.4, inset=1.0, shadow_k=0.95)
    s.plate(obox(px, py, yaw, 14, 40), AR_D, z=4.1, bevel=1.2, inset=0.6, shadow_k=0.9)
    fx, fy = -np.sin(yaw), -np.cos(yaw)
    warhead(px + fx*33, py + fy*33, fx, fy)
sysl('fore bubble-missile pods under the snout tip: 4 warheads each, 120 deg fwd', 109, 66)

# ================================================================ snout: shell, spine, panels, hoops, belts, nose
s.plate(snout, AR, z=4.6, bevel=3.4, dome=1.2, inset=2.2, shadow_k=0.95)
for g in (-1, 1):
    belt = snout & ((xx_ - CX)*g > 43) & (yy_ > 76) & (yy_ < 226)
    s.plate(belt, AR_L, z=4.8, bevel=1.2, tilt=(g*0.5, 0), inset=0.5, shadow_k=0.9)
    for yv in np.arange(90, 226, 24): s.rgb[belt & (np.abs(yy_ - yv) < 0.5)] = SEAM
    for yv in np.arange(92, 226, 24):
        if min(abs(yv - 130), abs(yv - 185)) < 14: continue
        s.rgb[s.rrect(X(g, 47) - 0.8, yv - 1, X(g, 47) + 0.8, yv + 1, 0.3)] = (216, 251, 255)          # side lights
    for pz in range(62, 240, 30):                                                   # raised armour panels either side of the spine
        pn = s.rrect(min(X(g, 21), X(g, 35)), pz + 2, max(X(g, 21), X(g, 35)), pz + 27, 2) & snout
        s.plate(pn, AR_L if (pz//30) % 2 else AR*1.04, z=5.4, bevel=1.4, dome=0.3, tilt=(g*0.25, 0), inset=0.8, shadow_k=0.9)
    s.rgb[snout & (np.abs(xx_ - X(g, 16)) < 0.8) & (yy_ > 56) & (yy_ < 246)] = TEAL                  # teal livery lines
spine = s.rrect(CX - 13, 50, CX + 13, 246, 3)
s.plate(spine, AR_L, z=6.0, bevel=1.6, dome=0.4, inset=1.0, shadow_k=0.95)
for yv in (70, 110, 150, 190, 230): s.rgb[snout & (np.abs(yy_ - yv) < 0.6) & ~spine] = SEAM          # hoop seams
nose = snout & (yy_ < SNY0 + 2)
s.plate(nose, AR_L, z=5.2, bevel=2.0, dome=0.8, inset=1.0, shadow_k=0.95)
for f in (0.35, 0.62, 0.9):
    s.rgb[nose & (np.abs(yy_ - (SNY0 + 2 - 26*np.cos(np.pi/2*f))) < 0.6)] = AR_L*1.08
s.plate(s.ell(CX, 13, 8, 5), np.array([120, 220, 245]), z=5.8, bevel=1.4, dome=1.0, inset=0.4, shadow_k=0.9)   # sensor
sysl('snout: spine, armour panels, hoops, side belts + lights, nose hoops + sensor', X(1, 28), 150)

# ================================================================ 10 small energy PD, sunk (teal lips): 2 per side on the snout walls, 3 per side on the bulb
for (px, py) in PD_SN:
    VP.sunk_mount(s, px, py, 5.4, (1 if px > CX else -1, 0), metal=AR_D, lip_metal=AR_L, z=5.0, lip_z=6.0, accent=TEAL)
for (px, py, a, g) in PD_BD:
    VP.sunk_mount(s, px, py, 5.4, (g*np.sin(a)/BRX, -np.cos(a)/BRZ*BRX/BRX), metal=AR_D, lip_metal=AR_L, z=2.2, lip_z=3.2, accent=TEAL)
sysl('10 small energy PD sunk: 2/side snout walls + 3/side on the bulb equator', X(-1, 80), 222)

# ================================================================ COMMAND TOWER (3 tiers), teal band, amber visor glass
def tier(hw, y0, y1, r):
    return s.poly(spline([(X(-1, hw - r), y0), (X(1, hw - r), y0), (X(1, hw), y0 + r), (X(1, hw), y1 - r), (X(1, hw - r), y1),
                          (X(-1, hw - r), y1), (X(-1, hw), y1 - r), (X(-1, hw), y0 + r)], 8, True))
c1 = tier(33, 282, 374, 12)
s.plate(c1, AR, z=5.0, bevel=3.0, dome=1.0, inset=2.2, shadow_k=0.95, paint=[(c1 & (np.abs(yy_ - 366) < 1.8), TEAL)])
s.bolt_row(c1, 1.6, 5)
c2 = tier(25, 286, 362, 10)
s.plate(c2, AR_L, z=6.2, bevel=2.6, dome=1.2, ridge=('x', CX, 1.6, 25), inset=1.8, shadow_k=0.95)
glass = tier(23, 288, 296, 3) & c2
gy = np.clip((yy_ - 288)/8, 0, 1); s.rgb[glass] = np.clip(AMB*(1.15 - 0.45*gy[..., None]), 0, 255)[glass]
for k_ in range(-20, 21, 5): s.rgb[glass & (np.abs(xx_ - (CX + k_)) < 0.35)] = (90, 60, 20)
for g in (-1, 1):
    for k in range(4): s.rgb[s.rrect(min(X(g, 12), X(g, 22)), 344 + k*4, max(X(g, 12), X(g, 22)), 345 + k*4, 0.3)] = SEAM
c3 = tier(15, 302, 348, 8)
s.plate(c3, AR_L*1.04, z=7.4, bevel=2.2, dome=1.2, inset=1.4, shadow_k=0.95)
s.plate(s.disk(CX, 330, 6.5), AR_L, z=7.9, bevel=1.4, dome=1.0, inset=0.6, shadow_k=0.95)
s.rgb[s.disk(CX, 330, 2.2)] = (40, 110, 104)
sysl('command tower (3 tiers), amber visor glass forward, teal band', CX, 292)

# ================================================================ symmetry + lights
_h = CX*s.SS
s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
s.lights([(X(-1, BRX + PI1 + 1.5), BCY + 6), (X(1, BRX + PI1 + 1.5), BCY + 6), (CX, 4)], [(255, 70, 60), (90, 255, 120), (255, 255, 240)])
sprite = s.render()
sprite.save(_ROOT + '/ss_style/regulus_ss_v1.png')
slots = [dict(px=x, py=y, size='MEDIUM', type='MISSILE', mount='HIDDEN', angle=round(np.degrees(yw)), arc=120) for (x, y, yw) in FP]
slots += [dict(px=X(g, BRX + (PI0 + PI1)/2), py=BCY - 2, size='MEDIUM', type='MISSILE', mount='HIDDEN', angle=(10 if g < 0 else -10), arc=120) for g in (-1, 1)]
slots += [dict(px=x, py=y, size='SMALL', type='ENERGY', mount='TURRET', angle=(90 if x < CX else -90), arc=180) for (x, y) in PD_SN]
slots += [dict(px=round(float(x), 1), py=round(float(y), 1), size='SMALL', type='ENERGY', mount='TURRET', angle=(90 if g < 0 else -90), arc=180) for (x, y, a, g) in PD_BD]
json.dump(dict(W=W, H=H, slots=slots, ENG=ENG, small=SMALL, lat=[]), open(_ROOT + '/ss_style/regulus_ss_v1_slots.json', 'w'))
json.dump(SYSTEMS, open(_ROOT + '/ss_style/regulus_v1_systems.json', 'w'))
print('ok')
