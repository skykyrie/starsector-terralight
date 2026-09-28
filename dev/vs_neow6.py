import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Neow - Starsector style v2 (current Terra Light language, approved on Tiamat v28/29 + Asura v7).
Zeppelin envelope built from longitudinal armour GORES (the EL meridian lines become real armour strips),
3 Armageddon launch tubes in a column near the prow (pipes pointing forward), heavy prow cap (tankiest ship),
buried + armoured drive core, stepped command tower aft, stern block with 2 big mains + 2 diagonal small drives.
Layer/depth pass, symmetric light + left->right mirror."""
import json, numpy as np
from scipy import ndimage as ndi
import vstyle, vparts as VP
from vstyle import Ship, spline

SL = json.load(open(_ROOT + '/nodens_slots.json'))
W, H = SL['W'], SL['H']; CX = W//2
SLOT = SL['slots'][0]
MUZ = [SLOT['py'] - o[0] for o in SLOT['offsets']]                  # muzzle rows: front, middle, back (EL-shared)
TR, TL = 30, 64                                                     # tube half-width, length

PL = np.array([128, 132, 140]); PL_D = np.array([96, 100, 110]); PL_L = np.array([156, 160, 168])
SKY = np.array([96, 150, 222])                                      # Neow envelope blue (from the EL zeppelin)
ORG = np.array([214, 116, 48]); PINK = (255, 150, 210)
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))

_L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = CX
s = Ship(W, H, seed=61)
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
def mir(pts): return pts + [(2*CX - x, y) for x, y in pts[::-1]]
SP = lambda pts, n=20: s.poly(spline(mir(pts), n, True))
yy_ = s.yy/s.SS; xx_ = s.xx/s.SS; ax_ = np.abs(xx_ - CX)
def erode(m, px): return ndi.binary_erosion(m, iterations=max(1, int(px*s.SS)))

# ================================================================ silhouette: zeppelin envelope + stern gondola
LEFT = [(CX - 8, 22), (CX - 56, 36), (CX - 96, 72), (CX - 120, 138), (CX - 128, 230), (CX - 126, 330),
        (CX - 114, 412), (CX - 88, 468), (CX - 52, 504), (CX - 20, 514)]
hull = SP(LEFT)
gond = s.rrect(CX - 46, 480, CX + 46, 526, 10)
body = hull | gond
s.guts(body, seed=63, tone=(50, 52, 58), minc=3, maxc=10); s.z[:] = 0
rows = np.where(hull.any(1))[0]
HW = np.zeros(s.h, np.float32)                                        # envelope half-width per supersampled row
for r in rows:
    xs = np.where(hull[r])[0]; HW[r] = (CX*s.SS - xs.min())/s.SS
U = ax_/np.maximum(HW[:, None], 1)                                    # 0 on the spine .. 1 at the envelope edge

# ================================================================ stern: 2 big mains + 2 diagonal small drives, all under the gondola block
MET = (146, 144, 150)
def eng_z(z, *a, **k):
    m = VP.engine_housing(s, *a, **k); s.z[m] = z; return m
ENG = [(X(-1, 19), 546), (X(1, 19), 546)]
for (ex, ey) in ENG: eng_z(1.3, ex, 508, ey, 30, metal=MET, bands=2)
def diag_jet(g, cx_, cy_, w_):
    T = 40; j = Ship(T, T, SS=s.SS, seed=5)
    mm = VP.engine_housing(j, T/2, 3, 29, w_, metal=MET, bands=2); j.z[mm] = 1.1
    ang = -45 if g < 0 else 45
    rgb = np.stack([ndi.rotate(j.rgb[..., c], ang, reshape=False, order=1) for c in range(3)], -1)
    al = ndi.rotate(j.a.astype(np.float32), ang, reshape=False, order=1) > 0.5
    zr = ndi.rotate(j.z, ang, reshape=False, order=0)
    ox, oy = int(round((cx_ - T/2)*s.SS)), int(round((cy_ - T/2)*s.SS))
    x0, y0 = max(0, ox), max(0, oy); x1, y1 = min(s.w, ox + j.w), min(s.h, oy + j.h)     # clip to the canvas
    sub = (slice(y0, y1), slice(x0, x1)); tl = (slice(y0 - oy, y1 - oy), slice(x0 - ox, x1 - ox))
    al, rgb, zr = al[tl], rgb[tl], zr[tl]
    s.rgb[sub][al] = rgb[al]; s.a[sub] |= al; s.z[sub][al] = zr[al]
SMALL = []
m = s.plate(gond, PL_D, z=2.6, bevel=3.0, dome=0.6, tilt=(0, 0.1), inset=2.4, shadow_k=0.8,
            lines=[s.rrect(CX - 0.35, 484, CX + 0.35, 524, 0.2)])
for g in (-1, 1): s.grille(s.rrect(min(X(g, 8), X(g, 34)), 488, max(X(g, 8), X(g, 34)), 498, 0.4), period=2.0)
sysl('stern gondola: 2 main drives + 2 diagonal manoeuvring drives', CX, 530)

# ================================================================ side FLIPPERS (from SS v1) with a thruster on each flipper deck
FIN = {}
def rrot(c, u, a0, a1, hw, ch=2.5):
    """chamfered rectangle along axis u (unit), from a0 to a1 along it, half-width hw, centred on point c"""
    v = np.array([-u[1], u[0]]); P = lambda a, b: tuple(c + u*a + v*b)
    return s.poly([P(a0, -hw + ch), P(a0 + ch, -hw), P(a1 - ch, -hw), P(a1, -hw + ch), P(a1, hw - ch), P(a1 - ch, hw), P(a0 + ch, hw), P(a0, hw - ch)])
for g in (-1, 1):
    # thick flipper; its outer-aft corner is cut square to the thrust line and the drive fires OUT of that face
    n = np.array([g*0.7071, 0.7071]); port = np.array([X(g, 125), 501.0])          # centre of the chamfer face
    diag_jet(g, *(port + n*4.0), 13)                                               # drive buried inside the flipper
    fin = s.poly([(X(g, 92), 424), (X(g, 132), 474), (X(g, 132), 494), (X(g, 118), 508), (X(g, 72), 500)])
    FIN[g] = fin
    s.plate(fin, PL_D*1.05, z=2.6, bevel=3.4, dome=1.0, tilt=(g*0.2, 0.05), inset=2.6, shadow_k=0.85,
            paint=[(fin & (np.abs(xx_ - X(g, 130)) < 2.2), SKY)])
    le = s.poly([(X(g, 92), 424), (X(g, 132), 474), (X(g, 128), 479), (X(g, 89), 432)]) & fin                   # armoured leading edge
    s.plate(le, PL_L, z=3.0, bevel=1.8, inset=0.8, shadow_k=0.8)
    v = np.array([-n[1], n[0]])
    lip = s.poly([tuple(port + v*9 - n*1.5), tuple(port + v*9 - n*5), tuple(port - v*9 - n*5), tuple(port - v*9 - n*1.5)])
    s.plate(lip, PL_D*0.8, z=2.9, bevel=1.2, inset=0.6, shadow_k=0.7)             # exhaust port frame on the cut face
    s.rgb[s.disk(*(port - n*9 + v*6), 0.9)] = np.array(PINK); s.rgb[s.disk(*(port - n*9 - v*6), 0.9)] = np.array(PINK)
    ex_ = port + n*13; SMALL.append((float(ex_[0]), float(ex_[1]), 135 if g < 0 else -135))
sysl('side flippers, each with a diagonal manoeuvring thruster on its deck', X(1, 120), 490)

# ================================================================ inner deck (only shows in the seams between gores)
deck = erode(hull, 6)
s.plate(deck, PL_D*0.85, z=1.0, bevel=1.6, inset=1.2, shadow_k=0.4)

# ================================================================ GORE ARMOUR: the envelope as longitudinal strips (EL meridians made real)
GORES = [(0.00, 0.30, 3.8, PL_L), (0.31, 0.58, 3.4, PL), (0.59, 0.84, 3.0, PL), (0.85, 1.01, 2.6, PL_D*1.08)]
CUTS = [20, 96, 176, 262, 350, 432, 520]
gm = {}
for gi, (u0, u1, zz, col) in enumerate(GORES):
    band = hull & (U >= u0 + 0.008) & (U <= u1 - 0.008)
    if gi == 0: band = hull & (U <= u1 - 0.008)
    gm[gi] = band
    for k in range(len(CUTS) - 1):
        seg = band & (yy_ > CUTS[k] + 1.2) & (yy_ < CUTS[k + 1] - 1.2)
        if not seg.any(): continue
        for g in ((-1, 1) if gi else (0,)):                           # each strip is its own plate (left / right)
            part = seg if g == 0 else seg & ((xx_ - CX)*g > 0)
            m = s.plate(part, col, z=zz + 0.25*((k + gi) % 2), bevel=3.0, dome=0.6, inset=2.4, shadow_k=0.8)
            if gi in (1, 2): s.bolt_row(m, 1.6, 5)
s.auto_z = False                                                   # surface hardware stays on its gore's layer
s.plate_details((gm[1] | gm[2]) & (yy_ > 60) & (yy_ < 470) & ~s.rrect(CX - 48, 40, CX + 48, 520) & ~(np.abs(yy_ - 336) < 50), n=46, seed=7, erode=3.0)
s.auto_z = True
sysl('envelope: longitudinal armour gores (shingled segments)', X(-1, 100), 300)

# ================================================================ ARMAGEDDON: 3 launch SILOS built pointing FORWARD - tunnel entrances
# each silo is an armoured vault: an arched (quonset-like) orange roof running aft, open at the FRONT where the dark
# launch tunnel shows, with the torpedo's red eye deep inside. A thick arch frame rings the mouth.
SW = 29                                                                              # vault half-width
for i, my in enumerate(MUZ):
    ZO = 1.4*i
    top = my - 12 if i == 0 else my - 20                                             # higher step laps OVER the back of the silo ahead
    st = s.rrect(CX - SW - 14, top, CX + SW + 14, (MUZ[i + 1] - 12) if i < 2 else my + TL + 8, 8)
    s.plate(st, PL_D*0.72, z=1.4 + ZO, bevel=2.4, inset=1.8, shadow_k=0.9)
    if i:
        s.rgb[st & (yy_ < top + 1.8)] = (176, 180, 190)                                # lit riser on the step's front face
        s.rgb[s.rrect(CX - SW - 13, top - 3.5, CX + SW + 13, top, 0.5) & s.a & ~st] *= 0.5   # contact shade on the lower silo                                                                       # front silo lowest, back silo highest
    y0, y1 = my, my + TL                                                             # mouth row .. vault back wall
    for g in (-1, 1):                                                                # buttress cheeks either side of the vault
        ch = s.poly([(X(g, SW - 1), y0 + 4), (X(g, SW + 9), y0 + 12), (X(g, SW + 9), y1 - 6), (X(g, SW - 1), y1)])
        s.plate(ch, PL, z=2.8 + ZO, bevel=1.8, tilt=(g*0.3, 0), inset=1.2, shadow_k=0.8)
        s.grille(s.rrect(min(X(g, SW + 2), X(g, SW + 7)), y0 + 18, max(X(g, SW + 2), X(g, SW + 7)), y1 - 12, 0.4), period=1.8)   # launch-blast vents
    roof = s.rrect(CX - SW, y0 + 9, CX + SW, y1, 5)
    u = np.clip((xx_ - CX)/SW, -1, 1)
    m = s.plate(roof, ORG, z=3.4 + ZO, bevel=1.6, dome=2.2, inset=1.2, shadow_k=0.85,
                lines=[s.rrect(CX - SW, yr, CX + SW, yr + 0.6, 0.2) for yr in np.arange(y0 + 20, y1 - 4, 10)])   # arch ribs
    cyl = np.sqrt(np.clip(1 - u**2, 0, 1))                                          # arched roof: shade across the vault
    k_ = (0.55 + 0.55*cyl + 0.35*np.exp(-(u/0.18)**2))[..., None]
    s.rgb[roof] = np.clip(s.rgb[roof]*k_[roof], 0, 255)
    tun = s.rrect(CX - SW + 5, y0, CX + SW - 5, y0 + 12, 4)                           # the open tunnel mouth, seen from above
    d_ = np.clip((yy_ - y0)/12, 0, 1)
    s.rgb[tun] = (np.array([52, 50, 56])*(1 - 0.7*d_[..., None]))[tun]; s.a |= tun; s.z[tun] = 1.9 + ZO
    arch = (s.rrect(CX - SW, y0 - 3, CX + SW, y0 + 11, 6) & ~s.rrect(CX - SW + 5, y0 + 1, CX + SW - 5, y0 + 13, 4))
    s.plate(arch, PL_L, z=3.8 + ZO, bevel=1.6, dome=0.6, inset=0.8, shadow_k=0.85)       # thick arch frame round the mouth
    nose = s.ell(CX, y0 + 11, 11, 5) & (yy_ < y0 + 11)                                # torpedo nose waiting in the tunnel
    tn = np.clip(1 - np.abs(xx_ - CX)/11, 0, 1)
    s.rgb[nose] = (np.array([120, 124, 132])*(0.4 + 0.7*tn[..., None]))[nose]
    s.rgb[s.ell(CX, y0 + 6.8, 3.0, 1.6)] = (230, 60, 70); s.rgb[s.ell(CX - 0.6, y0 + 6.4, 1.0, 0.5)] = (255, 170, 170)   # EL red eye = warhead tip
    for g in (-1, 1): s.rgb[s.disk(X(g, SW - 2.5), y0 + 1.5, 0.9)] = (255, 90, 80)  # mouth marker lights
sysl('ARMAGEDDON: 3 forward-facing launch silos (tunnel mouths), fire front -> middle -> back', CX, MUZ[1] + 30)

# ---- defensive flare launchers (Neow's right-click defence): 2 per side on the mid gores
for g in (-1, 1):
    for y in (300, 372):
        hw = HW[int(y*s.SS)]; xl = X(g, hw*0.5)
        fl = s.rrect(xl - 7, y - 10, xl + 7, y + 10, 2)
        s.plate(fl, PL_D, z=3.9, bevel=1.8, inset=1.2, shadow_k=0.8)
        for i in range(2):
            for j in range(3):
                px_, py_ = xl - 3.2 + i*6.4, y - 6 + j*6
                s.rgb[s.disk(px_, py_, 2.0)] = (190, 110, 50); s.rgb[s.disk(px_, py_, 1.4)] = (22, 22, 26)
sysl("defensive flare launchers (right-click defence, cooldown)", X(1, 60), 300)

# ================================================================ PROW: heavy cap over the nose (the tankiest ship leads with armour)
prow = SP([(CX - 4, 18), (CX - 44, 24), (CX - 80, 44), (CX - 96, 66), (CX - 60, 60), (CX - 30, 56), (CX, 58)])
prow &= hull
m = s.plate(prow, PL_L, z=4.6, bevel=3.2, ridge=('x', CX, 3.0, 60), tilt=(0, -0.25), dome=0.8, inset=2.4,
            paint=[(prow & (ax_ < 5), SKY)], lines=[s.rrect(X(g, dx) - 0.35, 20, X(g, dx) + 0.35, 60, 0.2) for g in (-1, 1) for dx in (24, 52)])
s.bolt_row(m & ~(ax_ < 7), 1.6, 5)
def glacis(g):                                                     # shingled glacis slabs down the bow shoulders
    for i, (y0, y1, zz) in enumerate(((104, 150, 3.9), (78, 118, 4.1), (56, 92, 4.3))):
        hw0, hw1 = HW[int(y0*s.SS)], HW[int(y1*s.SS)]
        sl = s.poly([(X(g, hw0 - 1), y0), (X(g, hw1 - 1), y1), (X(g, hw1 - 16), y1 - 4), (X(g, hw0 - 14), y0 + 2)]) & hull
        m_ = s.plate(sl, PL_L if i == 2 else PL, z=zz, bevel=2.0, tilt=(g*0.25, -0.25), inset=1.6)
for g in (-1, 1): glacis(g)
sysl('prow cap + shingled bow glacis: heaviest armour on the ship', X(-1, 50), 36)

# ================================================================ drive core: buried deep, armoured cover
zmark(0.4, s.drive_core, CX, 352, 26, glow=PINK)
VP.core_armour(s, CX, 352, 23, glow=PINK, z=3.6)
sysl('drive core (buried, armoured petal cover, heat slits)', CX, 352)

# ================================================================ command tower: 3 stepped tiers aft of the core
cmd1 = SP([(CX - 20, 388), (CX - 34, 404), (CX - 36, 468), (CX - 26, 484)])
m1 = s.plate(cmd1, PL, z=4.0, bevel=3.6, dome=1.2, inset=2.8, shadow_k=0.85, paint=[(cmd1 & (np.abs(yy_ - 472) < 2.4), SKY)])
s.bolt_row(m1, 1.8, 5)
cmd2 = SP([(CX - 10, 396), (CX - 24, 410), (CX - 24, 452), (CX - 16, 462)])
m2 = s.plate(cmd2, PL_L, z=5.2, bevel=3.0, dome=1.4, ridge=('x', CX, 2.0, 24), inset=2.4, shadow_k=0.85)
glass = SP([(CX - 10, 399), (CX - 21, 410), (CX - 21, 415), (CX - 10, 406)]) & m2
gy = np.clip((yy_ - 398)/18, 0, 1); s.rgb[glass] = (SKY*(1.25 - 0.5*gy[..., None]))[glass]
cmd3 = SP([(CX - 7, 422), (CX - 13, 430), (CX - 13, 448), (CX - 8, 454)])
s.plate(cmd3, PL_L*1.03, z=6.2, bevel=2.4, dome=1.4, ridge=('x', CX, 1.6, 13), inset=1.8, shadow_k=0.85)
s.mount(CX, 440, 4.6, PL, well_col=(70, 96, 140))
sysl('command tower (3 tiers), bridge glass forward', CX, 404)

# ================================================================ purposeful flank hardware on the gores
for g in (-1, 1):
    for y in (150, 236, 322, 408):                                                # heat radiators on the outer gores
        hw = HW[int(y*s.SS)]
        r_ = s.rrect(min(X(g, hw*0.66), X(g, hw*0.80)), y - 18, max(X(g, hw*0.66), X(g, hw*0.80)), y + 18, 2) & hull
        s.grille(r_, period=2.0)
    for y in (196, 286):                                                          # crew hatches on the mid gores
        hw = HW[int(y*s.SS)]; xh = X(g, hw*0.45)
        s.hatch(xh - 5, y - 4, xh + 5, y + 4, haz=False)
sysl('radiator panels on the outer gores', X(1, 100), 236); sysl('crew hatches', X(-1, 55), 196)

# ================================================================ livery: EL sky-blue on the outer gores + white pinstripe at the gore line
armour = s.a.copy()
s.livery(armour, gm[3] | gm[2] & (U > 0.72), tuple(SKY), keep=0.35)
pin = hull & (np.abs(U - 0.585) < 0.006) & (yy_ > 60) & (yy_ < 500)
s.rgb[pin] = (228, 232, 238)
s.emblem(CX, 316, 5.0)

# ================================================================ exact symmetry, then one-sided items
_h = CX*s.SS
s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
s.lights([(X(-1, 126), 250), (X(1, 126), 250), (X(-1, 44), 500), (X(1, 44), 500), (CX, 21)],
         [(255, 70, 60), (90, 255, 120), (255, 70, 60), (90, 255, 120), (255, 255, 240)])

sprite = s.render()
sprite.save(_ROOT + '/ss_style/neow_ss_v6.png')
json.dump(dict(W=W, H=H, slots=SL['slots'], ENG=ENG, small=SMALL, lat=[]), open(_ROOT + '/ss_style/neow_ss_v6_slots.json', 'w'))
json.dump(SYSTEMS, open(_ROOT + '/ss_style/neow_v6_systems.json', 'w'))
print('ok')
