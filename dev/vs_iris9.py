import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Iris - Starsector style v9 (= v8 + 2 rear-corner Small Ballistic PD sunk on the stern taper, facing rear-outward), drawn top-down from the approved 3D block-out (ss/iris3d.html v4).
Cruiser carrier: white ceramic armour, slate-grey flight deck inset in an armoured rim (ogive bow), 4 hangar ramps sloping down
aft into lit hangar mouths, full deck detailing (two-tone lanes, seams, catapult tracks + shuttles, lane lights, recovery zones with
magenta hatching + arrestor wires, service hatches, tie-downs, edge heat grates, bow threshold bars); rounded tube sponsons with
8 small ballistic PD sunk on blisters; sloped glacis up to the raised stern block (convex taper), oval missile deck with 2 medium
missile pads, 2 domed extension pods on swept fairings with pads; 3-tier command tower (blue glass) + core heat vents;
2 round main drives + 2 diagonal jets on the stern taper."""
import json, numpy as np
import vstyle, vparts as VP
from vstyle import Ship, spline

W, H, CX = 220, 436, 110
BAYS = [(74, 120), (146, 120), (74, 220), (146, 220)]; RW, RL = 38, 58
LANES = (74, 146)
PDP = (80, 140, 200, 260)
PD = [(CX + g*80, py) for g in (-1, 1) for py in PDP]
RPD = [(61.0, 371.0), (2*CX - 61.0, 371.0)]              # v9: rear-corner PD on the stern taper (left, right)
MIS = [(110, 298, 0, 240), (110, 342, 0, 240), (26, 340, 20, 180), (194, 340, -20, 180)]
ENG = [(95, 424), (125, 424)]

AR = np.array([188, 192, 190]); AR_D = np.array([140, 147, 145]); AR_L = np.array([208, 212, 210])
DECK = np.array([74, 83, 92]); LANE = np.array([92, 102, 112]); DSEAM = np.array([53, 60, 67]); GRT = np.array([35, 40, 45])
MAG = np.array([224, 64, 154]); WHT = np.array([226, 230, 234]); LIT = np.array([255, 222, 140]); GLS = np.array([106, 184, 255])
SEAM = (70, 74, 78)
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))

_L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = CX
s = Ship(W, H, seed=151)
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

def HWD(py):                                    # deck hull half-width: ogive bow, slight waist bulge (3D HWD)
    py = np.asarray(py, np.float32)
    bow = 82*np.sqrt(np.clip(1 - ((80 - py)/58)**2, 0, 1))
    mid = 82 + 2*np.sin(np.pi*np.clip((py - 80)/192, 0, 1))
    return np.where(py < 80, bow, mid)
def HWS(py):                                    # stern block half-width: convex cosine taper (3D HWS)
    py = np.asarray(py, np.float32)
    return np.where(py < 318, 84.0, 40 + 44*np.cos(np.pi/2*np.clip((py - 318)/92, 0, 1)))
def seg(p0, p1, w):                             # thin straight stroke (paint mask)
    (x0, y0), (x1, y1) = p0, p1; L = np.hypot(x1 - x0, y1 - y0); nx, ny = -(y1 - y0)/L*w/2, (x1 - x0)/L*w/2
    return s.poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)])
def inbay(x, y, m=0.0):
    return any(abs(x - bx) < RW/2 + m and abs(y - by) < RL/2 + m for (bx, by) in BAYS)

# ================================================================ silhouette + machinery base
rimM = (ax_ <= HWD(yy_)) & (yy_ >= 22) & (yy_ <= 273)
deckM = (ax_ <= HWD(yy_) - 6) & (yy_ >= 27) & (yy_ <= 270)
tubes = s.rrect(X(-1, 90.5), 70, X(-1, 75.5), 275, 7.5) | s.rrect(X(1, 75.5), 70, X(1, 90.5), 275, 7.5)
blocks = (ax_ <= HWS(yy_)) & (yy_ >= 269) & (yy_ <= 410)
fair = s.disk(44, 342, 30) | s.disk(176, 342, 30)
pods = s.disk(26, 340, 22.5) | s.disk(194, 340, 22.5)
s.guts(rimM | tubes | blocks | fair | pods, seed=153, tone=(58, 62, 66), minc=3, maxc=10); s.z[:] = 0

# ================================================================ drives first (they emerge from under the stern armour)
SMALL = []
for ex in (95,):
    m = VP.engine_housing(s, ex, 398, 423, 22, metal=(196, 200, 204), bands=2); s.z[m] = 2.7
    lipr = s.ell(ex, 423, 12.4, 3.3) & ~s.ell(ex, 423, 10.6, 2.3)
    s.rgb[lipr & (yy_ > 422.2)] = MAG*0.95                                              # magenta tip ring on the bell
for g in (-1,):
    yj = 372.0; e = np.array([float(X(g, HWS(yj) + 0.5)), yj]); n = np.array([g*0.7071, 0.7071])
    VP.diag_jet(s, g, *(e + n*1.0), 11, T=36, metal=(196, 200, 204), z=3.0); ex_ = e + n*12
    SMALL.append((float(ex_[0]), float(ex_[1]), 135 if g < 0 else -135)); SMALL.append((float(2*CX - ex_[0]), float(ex_[1]), -135))
sysl('2 round main drives on the stern face (magenta tips) + 2 diagonal jets on the stern taper', CX, 418)

# ================================================================ extension pod fairings (swept, grown out of the stern flanks)
fairL = s.disk(44, 342, 30) & (xx_ < CX)
s.plate(fairL, AR_D*1.05, z=3.0, bevel=4.0, dome=0.8, inset=1.8, shadow_k=0.9)

# ================================================================ stern block: main tier, stepped top plate
blk = blocks
s.plate(blk, AR, z=3.4, bevel=3.5, dome=0.6, inset=2.4, shadow_k=0.95)
top = (ax_ <= HWS(yy_) - 7) & (yy_ >= 274) & (yy_ <= 405)
s.plate(top, AR_L, z=3.8, bevel=2.0, dome=0.4, inset=1.2, shadow_k=0.95,
        lines=[top & (np.abs(yy_ - v) < 0.3) & (ax_ > 30) for v in (300, 330, 360)])
s.bolt_row(top, 1.6, 5)
for g in (-1,):                                                                    # core heat vents either side of the tower
    for k in range(4):
        s.rgb[s.rrect(X(g, 36), 370.2 + k*5, X(g, 28), 371.8 + k*5, 0.4)] = GRT
        s.rgb[s.rrect(X(g, 35), 372.6 + k*5, X(g, 29), 373.5 + k*5, 0.3)] = MAG*0.9
sysl('raised stern block: stepped top plate, convex taper; drive core deep below the tower (heat vents)', X(-1, 60), 330)

# ================================================================ extension pods: domed round pods, magenta band, missile pad
for (px, py) in [(26, 340)]:
    pod = s.disk(px, py, 22.5)
    rr = np.hypot(xx_ - px, yy_ - py)
    s.plate(pod, AR, z=4.0, bevel=5.0, dome=1.2, inset=0.0, shadow_k=0.95, paint=[(pod & (rr > 20.6), MAG*0.92)])
    pad = s.disk(px, py, 17.5)
    s.plate(pad, AR_D, z=4.3, bevel=1.4, inset=0.8, shadow_k=0.9, paint=[(pad & (np.abs(rr - 15.3) < 1.3), MAG)])
    zmark(4.4, s.mount, px, py, 12.5, AR_D*0.9)
sysl('2 extension pods: domed, magenta band, medium missile pad (180 deg, +-20)', 26, 340)

# ================================================================ sloped glacis from the deck up to the stern block
gl = (ax_ <= HWD(yy_) - 10) & (yy_ >= 263) & (yy_ <= 292)
s.plate(gl, AR_L, z=3.3, bevel=1.6, tilt=(0, 0.05), inset=0.8, shadow_k=0.9)
s.z[gl] = (2.95 + 0.85*np.clip((yy_ - 263)/29, 0, 1))[gl]
s.rgb[gl & (yy_ < 264.2)] *= 0.55                                                   # foot of the slope meets the deck
for k in range(-5, 1):
    s.rgb[s.rrect(CX + k*14 - 0.7, 272, CX + k*14 + 0.7, 281, 0.4) & gl] = MAG      # glacis approach lights
sysl('sloped glacis deck -> stern block, magenta approach lights', X(-1, 40), 278)

# ================================================================ raised oval missile deck + 2 centreline medium missile pads
ov = (ax_ <= 26*np.sqrt(np.clip(1 - ((yy_ - 321)/46)**2, 0, 1))) & (yy_ > 275) & (yy_ < 367)
s.plate(ov, AR_L, z=4.2, bevel=2.2, dome=0.5, inset=1.2, shadow_k=0.95)
ridge = s.poly([(X(-1, 9), 364), (X(1, 9), 364), (X(1, 6), 376), (X(-1, 6), 376)])
s.plate(ridge, AR_L, z=4.3, bevel=1.4, dome=0.4, shadow_k=0.9)
for (px, py, a_, arc_) in MIS[:2]:
    rr = np.hypot(xx_ - px, yy_ - py)
    pad = s.disk(px, py, 18)
    s.plate(pad, AR_D, z=4.5, bevel=1.4, inset=0.8, shadow_k=0.9, paint=[(pad & (np.abs(rr - 15.5) < 1.4), MAG)])
    zmark(4.6, s.mount, px, py, 13, AR_D*0.9)
sysl('raised oval missile deck: 2 medium missile pads (240 deg)', CX, 320)

# ================================================================ deck edge sponsons: rounded tube fairings under the rim
tubeL = s.rrect(X(-1, 90.5), 70, X(-1, 75.5), 275, 7.5)
s.plate(tubeL, AR_L*1.06, z=3.0, bevel=5.5, dome=0.4, inset=0.0, shadow_k=0.95, gain=1.4)

# ================================================================ armoured deck rim (white) + slate flight deck inset in it
rimL = rimM
s.plate(rimL, AR_L, z=3.15, bevel=2.2, dome=0.2, inset=0.0, shadow_k=0.95)
dk = deckM
laneM = np.zeros_like(dk)
for lx in LANES: laneM |= (np.abs(xx_ - lx) <= 22) & (yy_ >= 40) & (yy_ <= 266)
s.plate(dk, DECK, z=2.9, bevel=1.0, outline=0.6, grad=0.08, inset=0.0, shadow_k=0.9, paint=[(laneM, LANE)])
dkin = dk & (ax_ <= HWD(yy_) - 8)
# plate seams (skip the ramp openings - the ramps are drawn over them later anyway)
for py in range(48, 266, 22): s.rgb[dkin & (np.abs(yy_ - py) < 0.4)] = (s.rgb*0.72)[dkin & (np.abs(yy_ - py) < 0.4)]
for px in (42, 56, 92, 110, 128, 164, 178):
    m = dkin & (np.abs(xx_ - px) < 0.4) & (yy_ > 34); s.rgb[m] = s.rgb[m]*0.72
# runway paint: lane edge lines, dashed centre line, chevrons
for lx in LANES:
    for e in (-1, 1): s.rgb[dkin & (np.abs(xx_ - (lx + e*24)) < 0.6) & (yy_ > 72) & (yy_ < 268)] = WHT*0.9
    for py in (74, 170):
        s.rgb[(seg((lx - 11.3, py - 2.9), (lx - 0.7, py + 2.9), 1.3) | seg((lx + 11.3, py - 2.9), (lx + 0.7, py + 2.9), 1.3)) & dkin] = WHT
for py in range(40, 266, 16): s.rgb[s.rrect(CX - 0.7, py - 4, CX + 0.7, py + 4, 0.3) & dkin] = WHT*0.9
# catapult tracks (dark slot, magenta edges) + shuttles ahead of each ramp; lane centre lights
for lx in LANES:
    for (a, b) in ((36, 89), (151, 189)):
        s.rgb[s.rrect(lx - 1.8, a, lx + 1.8, b, 0.5) & dkin] = MAG*0.85
        s.rgb[s.rrect(lx - 1.0, a, lx + 1.0, b, 0.3) & dkin] = GRT
    for py in (85, 185):
        s.plate(s.rrect(lx - 3.2, py - 2.2, lx + 3.2, py + 2.2, 1.0), AR_L, z=3.1, bevel=1.0, dome=0.3, shadow_k=0.9)
    for py in range(40, 250, 10):
        if not inbay(lx + 8, py, 3): s.rgb[s.disk(lx + 8, py, 0.6) & dkin] = LIT
# recovery zones (stern end of each lane): magenta hatched box + 3 arrestor wires with posts
for lx in LANES:
    rz = s.rrect(lx - 20.4, 250.6, lx + 20.4, 265.4, 0.3) & ~s.rrect(lx - 19.6, 251.4, lx + 19.6, 264.6, 0.3)
    s.rgb[rz & dkin] = MAG
    hat = s.rrect(lx - 19.6, 251.4, lx + 19.6, 264.6, 0.3) & ((((xx_ + yy_) % 6.0) < 1.2))
    s.rgb[hat & dkin] = MAG*0.8
    for py in (240, 244, 248):
        s.rgb[s.rrect(lx - 20, py - 0.35, lx + 20, py + 0.35, 0.2) & dkin] = AR_D*1.1
        for e in (-1, 1): s.plate(s.rrect(lx + e*21 - 1.1, py - 1.1, lx + e*21 + 1.1, py + 1.1, 0.4), AR_D, z=3.0, bevel=0.6, shadow_k=0.7)
# bow runway threshold bars
for lx in LANES:
    for k in range(4): s.rgb[s.rrect(lx - 10.3 + k*6, 43.5, lx - 7.7 + k*6, 52.5, 0.3) & dkin] = WHT
# service hatches on the walkways; tie-downs; edge heat grates; deck edge lights
for (hx, hy) in [(110, 60), (110, 170), (110, 250), (44, 170)]:
    s.rgb[s.rrect(hx - 5, hy - 5, hx + 5, hy + 5, 0.8)] = DSEAM
    s.plate(s.rrect(hx - 4, hy - 4, hx + 4, hy + 4, 0.8), LANE*1.05, z=2.95, bevel=0.8, inset=0.0, shadow_k=0.5, outline=0.4)
    s.rgb[s.rrect(hx + 1.5, hy + 2.7, hx + 3.5, hy + 3.3, 0.2)] = GRT
for py in range(50, 262, 14):
    x_ = float(X(-1, HWD(py) - 13))
    if not inbay(x_, py, 2): s.rgb[s.disk(x_, py, 0.55)] = GRT
for py in range(92, 256, 40):
    for k in range(6):
        x_ = float(X(-1, HWD(py) - 9)); s.rgb[s.rrect(x_ - 2, py + k*2.4 - 0.4, x_ + 2, py + k*2.4 + 0.4, 0.2)] = GRT
for py in range(46, 268, 18):
    x_ = float(X(-1, HWD(py) - 10)); s.rgb[s.rrect(x_ - 0.7, py - 1, x_ + 0.7, py + 1, 0.3)] = LIT
sysl('slate flight deck: lighter lanes, seams, catapults + shuttles, lane lights, recovery zones + arrestor wires, hatches, grates', X(-1, 36), 60)

# ================================================================ 4 hangar ramps: slope down aft into lit hangar mouths
for (bx, by) in BAYS[::2]:
    pit = VP.hangar_ramp(s, bx, by, RW/2, L=RL, light=(255, 226, 160), deck_z=2.9, wall_grow=4.0)
    yA, yM = by - RL/2, by + RL/2 - 9
    for k in range(6):                                                              # white ramp stripes, crowding + dimming as it recedes
        u = (k + 0.5)/6; yr = yA + 3 + (yM - yA - 8)*(1 - (1 - u)**1.5); hw_ = RW/2 - 4.0*u - 2.5
        s.rgb[pit & s.rrect(bx - hw_, yr - 0.45, bx + hw_, yr + 0.45, 0.2)] = WHT*(0.85 - 0.5*u)
    mouth = s.rrect(bx - RW/2 + 5, by + RL/2 - 9.5, bx + RW/2 - 5, by + RL/2 - 7.5, 0.6)
    s.rgb[mouth] = (255, 236, 180)                                                  # lit hangar mouth under the brow
    s.plate(s.rrect(bx - RW/2 - 2, by - RL/2 - 2.6, bx + RW/2 + 2, by - RL/2 - 0.2, 0.8), MAG, z=3.05, bevel=0.8, dome=0.2, shadow_k=0.8)
sysl('4 hangar ramps (1 more than vanilla cruiser carriers): slope down aft into lit hangar mouths, magenta approach lips', 74, 120)

# ================================================================ sponson blisters + 8 small ballistic PD sunk (magenta outboard lips)
for py in PDP:
    bl = s.ell(X(-1, 82), py, 11, 13.5)
    s.plate(bl, AR_L, z=3.35, bevel=5.0, dome=0.5, inset=1.2, shadow_k=0.95)
for (px, py) in PD[:4]:
    VP.sunk_mount(s, px, py, 5.2, (-1, 0), metal=AR*0.92, lip_metal=AR_L, z=3.4, lip_z=3.75, accent=MAG)
sysl('tube sponsons along both deck edges: 8 small ballistic PD sunk on blisters (200 deg to their side)', 30, 140)
for (px, py) in RPD[:1]:                                                            # v9: rear-corner PD, lip toward the rear-outward taper edge
    VP.sunk_mount(s, px, py, 5.2, (-0.7071, 0.7071), metal=AR*0.92, lip_metal=AR_L, z=4.0, lip_z=4.35, accent=MAG)
sysl('2 rear-corner small ballistic PD sunk in the stern taper (180 deg, rear-outward)', RPD[0][0], RPD[0][1])

# ================================================================ COMMAND TOWER (3 tiers), magenta band, blue visor glass
c0 = s.rrect(86, 363, 134, 409, 10)
s.plate(c0, MAG*0.92, z=5.0, bevel=1.4, shadow_k=0.95)
c1 = s.rrect(87.5, 364.5, 132.5, 407.5, 9)
s.plate(c1, AR, z=5.3, bevel=2.8, dome=0.9, inset=1.8, shadow_k=0.95)
s.bolt_row(c1, 1.6, 5)
c2 = s.rrect(93, 371, 127, 405, 7)
s.plate(c2, AR_L, z=6.3, bevel=2.4, dome=1.0, ridge=('x', CX, 1.2, 17), inset=1.4, shadow_k=0.95)
glass = s.rrect(95.5, 371.8, 124.5, 377.6, 2.2) & c2
gy = np.clip((yy_ - 371.8)/5.8, 0, 1); s.rgb[glass] = np.clip(GLS*(1.2 - 0.5*gy[..., None]), 0, 255)[glass]
for k_ in (-8, 0): s.rgb[glass & (np.abs(xx_ - (CX + k_)) < 0.4)] = (20, 44, 70)
c3 = s.rrect(100, 380, 120, 401, 5)
s.plate(c3, AR_L*1.03, z=7.2, bevel=1.8, dome=1.0, inset=1.1, shadow_k=0.95)
s.plate(s.disk(CX, 392, 4.5), AR_L, z=7.7, bevel=1.2, dome=1.0, inset=0.5, shadow_k=0.95)
s.rgb[s.disk(CX, 392, 1.5)] = (40, 90, 150)
sysl('command tower (3 tiers) at the stern, blue visor glass forward, magenta band', CX, 380)

# ================================================================ symmetry + lights
_h = CX*s.SS
s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
drv = s.a & (yy_ > 409.5) & (ax_ < 28)                                              # drives stand clear of the tower's shadow (they sit on the lit stern face)
s.z[drv] = 5.6
s.lights([(X(-1, float(HWD(40)) - 3), 40), (X(1, float(HWD(40)) - 3), 40), (CX, 24)], [(255, 70, 60), (90, 255, 120), (255, 255, 240)])
sprite = s.render()
sprite.save(_ROOT + '/ss_style/iris_ss_v9.png')
slots = [dict(px=x, py=y, size='MEDIUM', type='MISSILE', mount='TURRET', angle=a, arc=arc) for (x, y, a, arc) in MIS]
slots += [dict(px=x, py=y, size='SMALL', type='BALLISTIC', mount='TURRET', angle=(90 if x < CX else -90), arc=200) for (x, y) in PD]
slots += [dict(px=x, py=y, size='SMALL', type='BALLISTIC', mount='TURRET', angle=(135 if x < CX else -135), arc=180) for (x, y) in RPD]
slots += [dict(px=bx, py=by, size='SMALL', type='LAUNCH_BAY', mount='HIDDEN', angle=0, arc=0) for (bx, by) in BAYS]
json.dump(dict(W=W, H=H, slots=slots, ENG=[list(e) for e in ENG], small=[list(t) for t in SMALL], lat=[]),
          open(_ROOT + '/ss_style/iris_ss_v9_slots.json', 'w'))
json.dump(SYSTEMS, open(_ROOT + '/ss_style/iris_v9_systems.json', 'w'))
print('ok')
