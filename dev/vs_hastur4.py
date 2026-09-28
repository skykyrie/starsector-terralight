import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Hastur - Starsector style v1 (cruiser, battle-cruiser/carrier) in the current Terra Light language:
layer shadows v2, symmetric light + mirror, contoured silhouette (armour sponsons around the side mounts), sunk mounts with
outboard lips, deck in depth (plates over machinery, lit power trenches), buried armoured core, 3-tier command tower,
drives from under the hull + diagonal corner jets. Same canvas + slots as the locked EL Hastur (ball + 'baguette' on its forehead)."""
import json, sys, numpy as np
from scipy import ndimage as ndi
import vstyle, vparts as VP
from vstyle import Ship, spline

J = json.load(open(_ROOT + '/hastur_slots.json'))
W, H = J['W'], J['H']; CX = W//2
SLOTS = J['slots']; ENG = [tuple(e) for e in J['ENG']]
MEN = [(s_['px'], s_['py']) for s_ in SLOTS if s_['size'] == 'MEDIUM' and s_['type'] == 'ENERGY']
RAIL = [(s_['px'], s_['py']) for s_ in SLOTS if s_.get('hide')]
PIVX = 84                                                                # built-in gun pivot = outer face of the sponson
def garc(g, y):                                                          # Tiamat rule: front 0..135 outward, rear 45..180 outward
    lo, hi = (0, 135) if y < 150 else (45, 180)
    if g > 0: lo, hi = -hi, -lo
    return (lo + hi)/2, hi - lo
SMB = [(CX - 53, 289), (CX + 53, 289), (CX - 68, 364), (CX + 68, 364)]   # v4 (3D-approved): 2 in line with the hangar, 2 out on the ball's sides
new = []
for s_ in SLOTS:
    if s_['size'] == 'MEDIUM' and s_['type'] == 'ENERGY':
        g_ = -1 if s_['px'] < CX else 1; a_, r_ = garc(g_, s_['py'])
        new.append(dict(s_, px=CX + g_*PIVX, angle=a_, arc=r_, builtin='tl_hastur_beam'))
    elif s_.get('hide'): pass
for py_ in (70, 120, 170):                                              # 3 medium ballistic in a column along the belly, 90 deg forward arc
    new.append(dict(px=CX, py=py_, size='MEDIUM', type='BALLISTIC', mount='HIDDEN', angle=0, arc=90))
MOD_SLOTS = [dict(px=x_, py=y_, size='SMALL', type='BALLISTIC', mount='TURRET', angle=((20 if y_ < 300 else 100)*(1 if x_ < CX else -1)), arc=200) for (x_, y_) in SMB]
MOD_SLOTS.append(dict(px=CX, py=270, size='SMALL', type='LAUNCH_BAY', mount='HIDDEN', angle=0, arc=0))      # docking hangar below the visor
new.append(dict(px=CX, py=342, size='LARGE', type='STATION_MODULE', mount='HIDDEN', angle=0, arc=0, id='MODULE_COMMAND'))
SLOTS = new
BX, BY, BR = CX, 342, 75                                                   # the ball
BAG = (CX - 75, 18, CX + 75, 312)                                          # the 'baguette'

PL = np.array([130, 136, 140]); PL_D = np.array([94, 100, 106]); PL_L = np.array([158, 164, 168])
CYAN = np.array([86, 206, 226]); TEAL = np.array([40, 140, 160]); PINK = np.array([236, 96, 176]); BLUE = np.array([70, 110, 220])
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))

MODE = sys.argv[1] if len(sys.argv) > 1 else 'hull'      # hull = main ship (front hull) | module = back hull (ball = command module)
_L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = CX
s = Ship(W, H, seed=101)
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
def erode(m, px): return ndi.binary_erosion(m, iterations=max(1, int(px*s.SS)))
MET = (150, 150, 156)

# ================================================================ silhouette: ball + baguette (rounded prow) + 2 sponsons per side
ball = s.disk(BX, BY, BR)
R_ = [(0, 14), (26, 16), (50, 24), (64, 38), (70, 60), (70, 132), (62, 150), (62, 172), (70, 188), (70, 236), (64, 264), (60, 294), (54, 320), (40, 338), (20, 346), (0, 348)]
bag = s.poly(spline([(CX + a, y) for a, y in R_] + [(CX - a, y) for a, y in R_[::-1][1:-1]], 12, True))
SPON = {}
for g in (-1, 1):
    SPON[g] = []
    for (mx, my) in [p for p in MEN if (p[0] < CX) == (g < 0)]:
        sp = s.poly(spline([(X(g, 60), my - 30), (X(g, 78), my - 26), (X(g, 88), my - 14), (X(g, 90), my + 10), (X(g, 82), my + 24),
                            (X(g, 66), my + 30), (X(g, 58), my + 20), (X(g, 58), my - 20)], 10, True))
        SPON[g].append(sp)
spon = np.zeros_like(ball)
for g in (-1, 1):
    for m in SPON[g]: spon |= m
hull = (bag | spon) if MODE == 'hull' else ball
s.guts(hull, seed=103, tone=(50, 54, 58), minc=3, maxc=10); s.z[:] = 0

# ================================================================ stern: 2 drives from under the ball + 1 diagonal jet per rear quarter
SMALL = []
if MODE == 'module':
  def eng_z(z, *a, **k):
      m = VP.engine_housing(s, *a, **k); s.z[m] = z; return m
  for (ex, ey) in ENG: eng_z(1.3, ex, 392, 432, 24, metal=MET, bands=2)
  for g in (-1, 1):
      n = np.array([g*0.7071, 0.7071]); e = np.array([BX + g*BR*0.7071, BY + BR*0.7071])
      VP.diag_jet(s, g, *(e + n*3.0), 15, T=44, metal=(176, 174, 180), z=3.6); ex_ = e + n*17; SMALL.append((float(ex_[0]), float(ex_[1]), 135 if g < 0 else -135))
sysl('2 main drives + 1 diagonal jet per rear quarter', ENG[1][0], 428)

# ================================================================ COMMAND MODULE (ball) from the approved 3D (top-down):
# meridian ribs, crown seam ring, cyan band at the rim, VISOR + DOCKING HANGAR on the front face, 4 small ballistic, ELEVATOR TOWER on the crown
if MODE == 'module':
    rr_b = np.hypot(xx_ - BX, yy_ - BY); an_b = np.degrees(np.arctan2(yy_ - BY, xx_ - BX))      # 0 = right, -90 = forward
    s.plate(ball, PL, z=1.8, bevel=3.2, dome=1.6, inset=2.4, shadow_k=0.9)
    front_sec = np.abs(an_b + 90) < 50
    for a_ in range(0, 360, 30):                                                    # meridian ribs (none across the visor sector)
        if abs(((a_ + 90 + 180) % 360) - 180) < 50: continue
        rib = ball & (np.abs(((an_b - a_ + 180) % 360) - 180)*np.pi/180*rr_b < 1.2) & (rr_b > 30) & (rr_b < BR - 3)
        s.plate(rib, PL_L, z=2.3, bevel=0.8, inset=0.3, shadow_k=0.9)
    s.rgb[ball & (np.abs(rr_b - 41) < 0.7)] = (40, 44, 50)                            # crown seam ring
    rim = ball & (rr_b > BR - 5)
    s.plate(rim, PL_D, z=1.9, bevel=1.4, inset=0.6, shadow_k=0.9, paint=[(rim & (np.abs(rr_b - BR + 2.5) < 1.2), CYAN)])   # cyan band at the rim
    vis = ball & front_sec & (rr_b > 52) & (rr_b < 64)                               # VISOR on the front face
    vfr = ball & (np.abs(an_b + 90) < 54) & (rr_b > 49) & (rr_b < 67) & ~vis
    s.plate(vfr, PL_L*1.05, z=2.2, bevel=1.2, inset=0.5, shadow_k=0.9)
    gv = np.clip((rr_b - 52)/12, 0, 1); s.rgb[vis] = (BLUE*(1.35 - 0.6*gv[..., None]))[vis]; s.z[vis] = 2.0
    for a_ in range(-130, -49, 10): s.rgb[vis & (np.abs(an_b - a_) < 0.7)] = (30, 40, 80)
    s.rgb[vis & (np.abs(rr_b - 55) < 0.5)] = (170, 200, 255)
    hg = s.rrect(BX - 24, BY - BR - 1, BX + 24, BY - BR + 9, 2) & ball                # DOCKING HANGAR at the front rim (below the visor)
    s.rgb[hg] = (10, 12, 14); s.z[hg] = 1.6
    s.plate(s.rrect(BX - 27, BY - BR + 8, BX + 27, BY - BR + 11, 1) & ball, PL_L, z=2.1, bevel=0.8, inset=0.3, shadow_k=0.9)
    for xv in np.arange(BX - 20, BX + 21, 5.7): s.rgb[s.disk(xv, BY - BR + 7, 0.6)] = (255, 190, 110)
    for (sx, sy) in SMB:
        VP.sunk_mount(s, sx, sy, 6.0, (1 if sx > CX else -1, -0.8 if sy < 300 else 0.2), metal=PL_D, lip_metal=PL_L, z=2.3, lip_z=3.2, accent=CYAN)
    # ELEVATOR TOWER on the crown (goes up into the front hull's belly)
    eY = 326
    s.plate(s.disk(BX, eY, 33), PL_D, z=2.6, bevel=2.0, inset=1.4, shadow_k=0.9)
    re = np.hypot(xx_ - BX, yy_ - eY); s.rgb[s.disk(BX, eY, 33) & (np.abs(re - 30.5) < 0.9)] = (170, 176, 184)
    for a_ in range(0, 360, 30): s.rgb[s.disk(BX + 30.5*np.cos(np.radians(a_)), eY + 30.5*np.sin(np.radians(a_)), 0.8)] = (40, 42, 46)
    for g in (-1, 1):
        s.plate(s.rrect(X(g, 13) - 3, eY - 2, X(g, 13) + 3, eY + 2, 1), PL_D, z=3.4, bevel=0.8, inset=0.3, shadow_k=0.9)
        tube = s.disk(X(g, 22), eY, 6)
        s.plate(tube, np.array([110, 200, 214]), z=3.6, bevel=1.4, dome=0.8, inset=0.4, shadow_k=0.9)
        s.rgb[s.disk(X(g, 22), eY, 3.2)] = (230, 240, 244)                           # lit lift car seen through the glass
    s.plate(s.disk(BX, eY, 17), PL, z=4.0, bevel=2.0, dome=0.8, inset=1.2, shadow_k=0.95)
    s.rgb[s.disk(BX, eY, 17) & (np.abs(re - 15) < 0.7)] = (40, 44, 50)
    s.rgb[s.disk(BX, eY, 24.5) & ~s.disk(BX, eY, 23.5) & ~s.disk(BX, eY, 17)] = CYAN*0.9
    sysl('COMMAND MODULE: visor + docking hangar on the front face, 4 small ballistic, elevator tower on the crown', BX, BY)

# ================================================================ baguette: longitudinal armour bands (spine highest), lit power trench,
if MODE == 'hull':
    # 3 railgun EMBRASURES in the prow (the medium ballistic mounts live inside, sprite hidden)
    s.plate(bag, PL_D, z=5.0, bevel=3.2, dome=0.8, inset=2.4, shadow_k=0.95)
    BANDS = [(0, 20, 6.4, PL_L), (21, 46, 6.0, PL), (47, 76, 5.6, PL*0.97)]
    CUTS = [16, 70, 140, 210, 280, 348]
    for bi, (u0, u1, zz, col) in enumerate(BANDS):
        for k in range(len(CUTS) - 1):
            seg = bag & (ax_ >= u0 + 0.6) & (ax_ <= u1 - 0.6) & (yy_ > CUTS[k] + 1.2) & (yy_ < CUTS[k + 1] - 1.2)
            if bi == 0: seg = bag & (ax_ <= u1 - 0.6) & (yy_ > CUTS[k] + 1.2) & (yy_ < CUTS[k + 1] - 1.2)
            for g in ((-1, 1) if bi else (0,)):
                part = seg if g == 0 else seg & ((xx_ - CX)*g > 0)
                if not part.any(): continue
                m = s.plate(part, col, z=zz + 0.2*((k + bi) % 2), bevel=2.4, dome=0.5, inset=1.8, shadow_k=0.85,
                            paint=[(part & (np.abs(ax_ - 44) < 1.4), CYAN)] if bi == 1 else ())
    sysl('front hull: clean longitudinal armour bands (spine highest), cyan livery lines', X(1, 20), 200)
    for (rx, ry) in []:
        emb = s.rrect(rx - 9, ry - 4, rx + 9, ry + 8, 3) & bag
        s.rgb[emb] = (22, 24, 28); s.z[emb] = 5.0
        s.rgb[s.rrect(rx - 9, ry - 4, rx + 9, ry - 2.8, 0.6) & bag] = (170, 176, 182)          # lit upper lip
        for dx in (-4, 0, 4): s.rgb[s.rrect(rx + dx - 0.8, ry - 1, rx + dx + 0.8, ry + 6, 0.4) & bag] = (80, 84, 92)   # barrel tips inside
    sysl('3 medium ballistic in a column along the belly (hidden, 90 deg forward arc)', CX, 120)
    nose = bag & (yy_ < 60) & (ax_ < 30)
    s.plate(nose, PL_L, z=7.0, bevel=2.2, dome=0.5, inset=1.2, shadow_k=0.95)
    for g in (-1, 1):
        for (a_, b_) in ((62, 130), (190, 234)):                                     # side armour belts on the straight walls
            belt = bag & ((xx_ - CX)*g > 63) & (yy_ > a_) & (yy_ < b_)
            s.plate(belt, PL_L, z=5.9, bevel=1.4, tilt=(g*0.4, 0), inset=0.6, shadow_k=0.9,
                    lines=[s.rrect(0, y, W, y + 0.6, 0.2) for y in range(a_ + 12, b_, 18)])
        for k in range(4): s.rgb[s.rrect(min(X(g, 58), X(g, 61)), 151 + k*6.2, max(X(g, 58), X(g, 61)), 154 + k*6.2, 0.6)] = CYAN   # core heat vents
    prow = bag & (yy_ < 22)                                                                 # prow cap
    s.plate(prow, PL_L, z=6.8, bevel=2.2, dome=0.6, inset=1.2, shadow_k=0.9, paint=[(prow & (ax_ < 4), CYAN)])

    # ================================================================ sponsons: armour lobes that contour the flanks + SUNK mounts with lips
    for g in (-1, 1):
        for k, sp in enumerate(SPON[g]):
            s.plate(sp, PL_L, z=6.0, bevel=2.8, dome=0.8, tilt=(g*0.3, 0), inset=2.0, shadow_k=0.95,
                    paint=[(sp & (np.abs(xx_ - X(g, 86)) < 1.6), PINK)])
            s.bolt_row(sp, 1.4, 4.5)
    for (mx, my) in MEN:                                                                    # BUILT-IN side turrets (Tiamat mechanism)
        g = 1 if mx > CX else -1; px = X(g, PIVX)
        arm = s.rrect(min(X(g, 62), X(g, 82)), my - 5, max(X(g, 62), X(g, 82)), my + 5, 2)     # trunnion arm from the hull
        s.plate(arm, PL, z=6.6, bevel=1.6, ridge=('y', my, 1.4, 5), inset=1.2, outline=0.6, shadow_k=0.8, notch=0)
        for xx in (X(g, 67), X(g, 75)): s.rgb[s.disk(xx, my - 3, 0.6)] = (40, 42, 46); s.rgb[s.disk(xx, my + 3, 0.6)] = (40, 42, 46)
        col = s.disk(px, my, 8.5)
        s.plate(col, PL_L, z=7.0, bevel=2.6, dome=0.6, outline=0.7, shadow_k=0.85, notch=0)   # mount collar at the sponson face
        rr = np.hypot(xx_ - px, yy_ - my)
        s.rgb[col & (rr > 6.4) & (rr < 7.5) & (yy_ < my)] = (210, 216, 226); s.rgb[col & (rr > 6.4) & (rr < 7.5) & (yy_ >= my)] = (70, 74, 82)   # tracking ring
        s.rgb[col & (rr > 5.0) & (rr < 5.9)] = PINK; s.rgb[col & (rr > 5.25) & (rr < 5.65)] = (255, 170, 220)                  # EL pink ring
        s.rgb[col & (rr < 3.9)] = (26, 28, 32)                                                 # bearing the barrels turn in
        for a_ in range(0, 360, 45): s.rgb[s.disk(px + 7.9*np.cos(np.radians(a_)), my + 7.9*np.sin(np.radians(a_)), 0.5)] = (40, 42, 46)
    sysl('4 BUILT-IN medium energy side turrets (Tiamat mechanism: arm + collar, barrels turn 135 deg)', X(-1, 84), 100)

# ================================================================ symmetry + lights
_h = CX*s.SS
s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
if MODE == 'hull': s.lights([(X(-1, 70), 60), (X(1, 70), 60), (CX, 16)], [(255, 70, 60), (90, 255, 120), (255, 255, 240)])
else: s.lights([(X(-1, 74), 330), (X(1, 74), 330)], [(255, 70, 60), (90, 255, 120)])
if False: s.lights([],
         [(255, 70, 60), (90, 255, 120), (255, 70, 60), (90, 255, 120), (255, 255, 240)])
sprite = s.render()
if MODE == 'hull':      # bake the front hull's drop shadow into its sprite (semi-transparent), so it falls on the module below it
    from PIL import Image as _I
    A = np.asarray(sprite).astype(np.float32); al = A[..., 3]/255
    sh = np.maximum(np.roll(ndi.gaussian_filter(np.roll(al, (7, 5), (0, 1)), 3.0), 0, 0), ndi.gaussian_filter(np.roll(al, (7, -5), (0, 1)), 3.0))
    sh = np.clip(sh*0.7, 0, 1)*(1 - al)
    A[..., 3] = np.clip(al*255 + sh*255, 0, 255); A[..., :3] = A[..., :3]*al[..., None]/np.maximum(al + sh, 1e-6)[..., None]
    sprite = _I.fromarray(A.astype(np.uint8), 'RGBA')
sprite.save(_ROOT + f'/ss_style/hastur_ss_v4_{MODE}.png')
json.dump(dict(W=W, H=H, slots=SLOTS, module_slots=MOD_SLOTS, module_center=(BX, BY), ENG=ENG, small=SMALL, lat=[]), open(_ROOT + '/ss_style/hastur_ss_v4_slots.json', 'w'))
json.dump(SYSTEMS, open(_ROOT + f'/ss_style/hastur_v4_systems_{MODE}.json', 'w'))
print('ok')
