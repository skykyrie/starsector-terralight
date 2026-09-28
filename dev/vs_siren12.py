import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Siren - Starsector style v1 (Terra Light language: layer shadows v2, symmetric light + mirror, buried armoured core,
drives from under the hull + diagonal corner jets, 3-tier command concept).  Same canvas + slots as the locked EL Siren.
Wide half-cylinder hull with a flat flight deck; 3 main-gun IRIS wells (guns fold under the deck in carrier mode and rise
in battleship mode), 4 Artemis-style hangar ramps, 8 PD on the side belts, command pod on a neck behind the stern."""
import json, numpy as np
from scipy import ndimage as ndi
import vstyle, vparts as VP
from vstyle import Ship, spline

J = json.load(open(_ROOT + '/siren_slots.json'))
W, H = J['W'], J['H']; CX = W//2
SLOTS = J['slots']
PD = [(s_['px'], s_['py']) for s_ in SLOTS if s_['size'] == 'SMALL' and s_['type'] == 'BALLISTIC']
GUNS = [(s_['px'], s_['py']) for s_ in SLOTS if s_['size'] == 'LARGE']
BAYS = [(s_['px'], s_['py']) for s_ in SLOTS if s_['type'] == 'LAUNCH_BAY']
ENG = [tuple(e) for e in J['ENG']]
POD = (CX, 330, 32)

PL = np.array([130, 132, 138]); PL_D = np.array([96, 98, 106]); PL_L = np.array([158, 160, 166])
ORG = np.array([232, 146, 96]); ORG_D = np.array([176, 96, 66]); DECKC = np.array([92, 128, 60])
PINK = np.array([230, 90, 140]); CYAN = np.array([120, 230, 250])
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))

_L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = CX
# v2: bays moved onto the FIXED deck (side strips + aft strip) so they keep working when the central hatch opens
BAYS = [(CX - 14, 124), (CX + 14, 124), (CX - 14, 146), (CX + 14, 146)]      # v6: launch points clustered in the ONE silo hangar (no visible bays)
for s_ in SLOTS:
    if s_['type'] == 'LAUNCH_BAY': s_['px'], s_['py'] = BAYS[[(70, 150), (270, 150), (120, 225), (220, 225)].index((s_['px'], s_['py']))]
HX0, HX1, HY0, HY1 = CX - 88, CX + 88, 58, 208
# v11: gun silos are part of the hangar floor - guns nudged so each silo fits the floor (slots shared with EL)
GMAP = {(108, 100): (112, 104), (232, 100): (228, 104), (170, 185): (170, 174)}      # v12: no two guns share a deck column
for s_ in SLOTS:
    if s_['size'] == 'LARGE': s_['px'], s_['py'] = GMAP[(s_['px'], s_['py'])]
GUNS = [(s_['px'], s_['py']) for s_ in SLOTS if s_['size'] == 'LARGE']
GR = 27                                                                   # gun silo / platform radius
# v3 CONTOURS: PD regrouped as pairs sunk in 2 notches per side, sheltered by armour lobes fore and aft
PDP = {70: (104, 64), 118: (104, 111), 166: (104, 158), 214: (104, 206)}      # v6: all PD on the green deck strips, evenly spaced (none between the lobes)
for s_ in SLOTS:
    if s_['size'] == 'SMALL' and s_['type'] == 'BALLISTIC':
        g_ = -1 if s_['px'] < CX else 1; dx_, s_['py'] = PDP[s_['py']]; s_['px'] = CX + g_*dx_
PD = [(s_['px'], s_['py']) for s_ in SLOTS if s_['size'] == 'SMALL' and s_['type'] == 'BALLISTIC']                      # the big armoured deck hatch over the gun bay
import sys
MODE = sys.argv[1] if len(sys.argv) > 1 else 'closed'      # closed | open (carrier launch/recover frame) | battleship
s = Ship(W, H, seed=81)
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

# ================================================================ silhouette
R_ = [(0, 22), (40, 23), (78, 26), (110, 32), (132, 44), (140, 64), (140, 130), (140, 200), (136, 236), (122, 256), (90, 265), (40, 266)]
core = s.poly(spline([(CX + a, y) for a, y in R_] + [(CX - a, y) for a, y in R_[::-1][:-1]], 12, True))
LOBES = {}
for g in (-1, 1):
    LB = [[(122, 36), (138, 40), (150, 56), (152, 74), (146, 82), (128, 82), (124, 60)],     # bow shoulder: forward face slopes back (glacis)
          [(128, 112), (148, 116), (153, 132), (153, 154), (147, 164), (128, 164)],       # mid lobe between the two PD notches
          [(128, 200), (148, 204), (153, 220), (150, 236), (140, 248), (126, 250)]]       # aft lobe, carries the corner jets
    LOBES[g] = [s.poly(spline([(X(g, a), y) for a, y in pts], 8, True)) for pts in LB]
hull = core | LOBES[-1][0] | LOBES[-1][1] | LOBES[-1][2] | LOBES[1][0] | LOBES[1][1] | LOBES[1][2]
neck = s.rrect(CX - 20, 250, CX + 20, 262, 4)
pod = s.disk(POD[0], POD[1], POD[2])
pod = s.poly(spline([(X(-1, 34), 217), (X(1, 34), 217), (X(1, 42), 226), (X(1, 42), 290), (X(1, 32), 304), (X(-1, 32), 304), (X(-1, 42), 290), (X(-1, 42), 222)], 10, True))
s.guts(hull | neck | pod, seed=83, tone=(50, 52, 58), minc=3, maxc=10); s.z[:] = 0

# ================================================================ stern: 2 mains from under the hull + a diagonal jet on each rear corner
def eng_z(z, *a, **k):
    m = VP.engine_housing(s, *a, **k); s.z[m] = z; return m
for (ex, ey) in ENG: eng_z(1.3, ex, 250, 292, 34, metal=MET, bands=2)
SMALL = []
for g in (-1, 1):
    n = np.array([g*0.7071, 0.7071])
    for e in (np.array([X(g, 150), 234.0]), np.array([X(g, 139), 247.0])):     # 2 diagonal jets on the aft lobe's rear face
        VP.diag_jet(s, g, *(e + n*5.0), 15, T=44, metal=(176, 174, 180), z=3.6);   # raised z: not buried in the lobes' shadow
        ex_ = e + n*17; SMALL.append((float(ex_[0]), float(ex_[1]), 135 if g < 0 else -135))
sysl('2 main drives + 2 diagonal corner jets per side', ENG[1][0], 288)

# ================================================================ hull armour: side belts (the half-cylinder's flanks) + fore/aft rims
s.plate(hull, PL, z=3.0, bevel=3.2, dome=0.6, inset=2.4, shadow_k=0.9)
for g in (-1, 1):
    belt = core & ((xx_ - CX)*g > 120) & (yy_ > 40) & (yy_ < 246)
    s.plate(belt, PL, z=3.3, bevel=2.2, tilt=(g*0.35, 0), inset=1.6, shadow_k=0.9)
    for k, lb in enumerate(LOBES[g]):                                                # armour lobes: highest layer on the flank
        s.plate(lb, PL_L, z=4.2 + 0.1*k, bevel=2.8, dome=0.8, tilt=(g*0.35, -0.1), inset=2.0, shadow_k=0.95,
                paint=[(lb & (np.abs(xx_ - X(g, 150)) < 1.8), ORG)])
        s.bolt_row(lb, 1.6, 4.5)
bow = hull & (yy_ < 44); aft = hull & (yy_ > 244)
s.plate(bow, PL_D*1.05, z=3.3, bevel=2.6, dome=0.5, inset=2.0, shadow_k=0.9, paint=[(bow & (np.abs(yy_ - 34) < 2.2), ORG)])
s.plate(aft, PL_D*1.05, z=3.3, bevel=2.6, dome=0.5, inset=2.0, shadow_k=0.9)
sysl('contoured flank: 3 armour lobes per side, PD pairs sunk in the notches between them', X(-1, 150), 140)

# ================================================================ fixed deck (side strips + aft strip): EL green, carries the fighter silos
deck = s.rrect(CX - 118, 46, CX + 118, 242, 12)
# v10 DECK IN DEPTH (vanilla-style): the fixed deck is no longer one green sheet. Under it: machinery (guts, z 1.2).
# On it: separate armour plates with gaps that show the machinery below, a lit POWER TRENCH down each strip carrying the core's
# power out to the PD and the flank lobes, cross-feeds, vents and access hatches. EL green survives as the plates' livery band.
s.guts(deck, seed=91, tone=(66, 70, 76), minc=2, maxc=7); s.z[deck] = 1.7
for g in (-1, 1):
    for (y0_, y1_) in [(48, 55), (73, 102), (120, 149), (167, 197), (215, 240)]:     # side-strip plates between the PD collars
        pl_ = s.rrect(min(X(g, 90), X(g, 111)), y0_, max(X(g, 90), X(g, 111)), y1_, 2.5) & deck
        s.plate(pl_, PL*0.98, z=2.5, bevel=1.8, dome=0.4, tilt=(g*0.2, 0.1), inset=1.2, shadow_k=0.9,
                paint=[(pl_ & (np.abs(xx_ - X(g, 94)) < 1.6), DECKC*1.2)])
        if y1_ - y0_ > 20:
            s.grille(s.rrect(min(X(g, 99), X(g, 107)), y0_ + 5, max(X(g, 99), X(g, 107)), y0_ + 12, 0.5), period=1.6)
            s.hatch(min(X(g, 97), X(g, 108)) , y1_ - 11, max(X(g, 97), X(g, 108)), y1_ - 5, haz=False)
    s.channel([(X(g, 115), 50), (X(g, 115), 238)], 4.4, light=tuple(PINK), step=9, nodes=False)   # power trench (outer edge)
    for yf in (87, 135, 183):                                                       # cross-feeds: hangar wall -> trench -> lobes
        s.channel([(X(g, 96), yf), (X(g, 118), yf)], 3.0, light=tuple(PINK), step=6, nodes=False)
fore = deck & (yy_ < 57) & (np.abs(xx_ - CX) < 86)
for k, (x0_, x1_) in enumerate([(-86, -46), (-44, -2), (2, 44), (46, 86)]):          # fore strip: 4 plates, vents between
    p_ = s.rrect(CX + x0_, 47, CX + x1_, 56, 2) & deck
    s.plate(p_, PL*0.98, z=2.5, bevel=1.6, inset=1.0, shadow_k=0.9, paint=[(p_ & (np.abs(yy_ - 49.5) < 1.2), DECKC*1.2)])
for xv in (-24, 24): s.grille(s.rrect(CX + xv - 10, 49.5, CX + xv + 10, 54, 0.5), period=1.6)
for g in (-1, 1):                                                                   # aft strip either side of the tower
    for (x0_, x1_) in [(46, 86), (88, 118)]:
        p_ = s.rrect(min(X(g, x0_), X(g, x1_)), 211, max(X(g, x0_), X(g, x1_)), 240, 3) & deck
        s.plate(p_, PL*0.98, z=2.5, bevel=1.8, dome=0.4, inset=1.2, shadow_k=0.9, paint=[(p_ & (np.abs(yy_ - 214) < 1.2), DECKC*1.2)])
    s.grille(s.rrect(min(X(g, 52), X(g, 80)), 222, max(X(g, 52), X(g, 80)), 230, 0.5), period=1.6)
    s.channel([(X(g, 44), 226), (X(g, 115), 226)], 3.0, light=tuple(PINK), step=6, nodes=False)   # tower <- trench feed
sysl('deck in depth: armour plates over machinery, lit power trenches + cross-feeds, vents, access hatches', X(-1, 100), 130)
def silo(x, y, r=12.5):
    """fighter launch silo: octagonal armoured collar + split blast doors (EL green) + launch light"""
    c8 = s.poly(Ship.mirror_pts([(x - 7, y - r - 5), (x - r - 5, y - 7), (x - r - 5, y + 7), (x - 7, y + r + 5)], x))
    s.plate(c8, PL, z=2.9, bevel=2.0, inset=1.4, shadow_k=0.9)
    rr = np.hypot(xx_ - x, yy_ - y)
    s.rgb[rr < r + 1.5] = (24, 26, 28); s.z[rr < r + 1.5] = 2.1
    for sd in (-1, 1):
        leaf = (rr < r) & ((xx_ - x)*sd > 0.7)
        s.plate(leaf, DECKC*1.25, z=3.1, bevel=1.6, dome=0.7, inset=1.0, shadow_k=0.75, lines=[leaf & (np.abs(rr - r*0.6) < 0.3)])
    s.rgb[s.disk(x, y - r - 2.5, 0.9)] = (170, 255, 150)

hatch = s.rrect(HX0, HY0, HX1, HY1, 10)
if MODE == 'closed':
    # ============ CARRIER MODE: the gun bay is sealed by a heavy armoured hatch - two leaves meeting on the centre line,
    # each built from shingled armour slabs (fore slab on top), EL green paint on the leaves, heavy hinge rails
    for g in (-1, 1):
        leaf = hatch & ((xx_ - CX)*g > 0.9)
        cuts = [HY0, 88, 118, 148, 178, HY1]
        for k in range(len(cuts) - 1):
            sl = leaf & (yy_ >= cuts[k] - (1.5 if k else 0)) & (yy_ <= cuts[k + 1] + 0.5)
            s.plate(sl, PL_D*1.05, z=3.2 + 0.3*(len(cuts) - k), bevel=2.6, dome=0.4, tilt=(g*0.1, 0.18), inset=2.0, shadow_k=0.9,
                    paint=[(sl & (np.abs(xx_ - X(g, 72)) < 2.2), DECKC*1.2), (sl & (np.abs(xx_ - X(g, 6)) < 1.4), ORG)])
        rail = s.rrect(min(X(g, 86), X(g, 94)), HY0 + 4, max(X(g, 86), X(g, 94)), HY1 - 4, 2)
        s.plate(rail, PL_D, z=3.9, bevel=1.4, inset=0.8, shadow_k=0.85)
    s.rgb[hatch & (np.abs(xx_ - CX) < 0.9)] = (22, 24, 26)                        # centre seam
    for y in (70, 133, 196): s.rgb[s.disk(CX, y, 1.1)] = (255, 170, 90)           # seam lock lights
    sysl('CARRIER mode (idle): silo hangar sealed; it animates open whenever fighters launch or land', CX, 130)
elif MODE in ('open', 'siloopen'):
    # ============ CARRIER MODE: the central SILO HANGAR stands open - fighters come and go through it. The hatch leaves are
    # stowed under the rails; we look down a deep shaft: lit inner walls (aft wall catches the light, fore wall in shadow),
    # a dark hangar floor far below with 4 lit launch cradles (the 4 fighter bays), guide-light grid, rim landing lights.
    D = 6                                                                           # apparent wall depth
    ix0, ix1, iy0, iy1 = HX0 + D, HX1 - D, HY0 + D*0.7, HY1 - D
    s.rgb[hatch] = (20, 22, 24); s.a |= hatch; s.z[hatch] = 0.8
    fl = s.rrect(ix0, iy0, ix1, iy1, 4)
    for g in (-1, 1):                                                               # side walls (trapezoids)
        xo, xi = (HX0, ix0) if g < 0 else (HX1, ix1)
        wall = s.poly([(xo, HY0), (xi, iy0), (xi, iy1), (xo, HY1)]) & hatch
        dd = np.clip(np.abs(xx_ - xo)/D, 0, 1)
        s.rgb[wall] = (np.array([96, 102, 108])*(0.95 - 0.55*dd[..., None]))[wall]
        for yv in np.arange(HY0 + 14, HY1 - 10, 12):                               # wall ribs
            s.rgb[wall & (np.abs(yy_ - yv) < 0.4)] *= 0.6
    aw = s.poly([(HX0, HY1), (ix0, iy1), (ix1, iy1), (HX1, HY1)]) & hatch             # aft wall: faces the light
    da = np.clip((HY1 - yy_)/D, 0, 1); s.rgb[aw] = (np.array([150, 156, 160])*(1.0 - 0.5*da[..., None]))[aw]
    fw = s.poly([(HX0, HY0), (ix0, iy0), (ix1, iy0), (HX1, HY0)]) & hatch             # fore wall: in shadow
    s.rgb[fw] = (40, 44, 48)
    s.rgb[fl] = (44, 48, 52)                                                        # hangar floor far below
    for xg in np.arange(ix0 + 8, ix1, 16): s.rgb[fl & (np.abs(xx_ - xg) < 0.35)] = (58, 64, 68)
    for yg in np.arange(iy0 + 8, iy1, 16): s.rgb[fl & (np.abs(yy_ - yg) < 0.35)] = (58, 64, 68)
    # ---------------- HANGAR INTERIOR v11: 3 GUN SILOS in the floor (the main guns live below them), the DRIVE CORE between
    # them, power conduits core -> each gun lift and -> the repair bays, 2 fighter repair bays in the aft corners, crew rooms +
    # pressure room on the fore wall, side-wall pressure rooms, catwalks.
    CORE = (CX, 112)
    def conduit(p0, p1, w=2.6):
        v = np.array(p1, float) - np.array(p0, float); L_ = np.linalg.norm(v); u = v/L_; n = np.array([-u[1], u[0]])
        q = lambda a, b: tuple(np.array(p0) + u*a + n*b)
        m = s.poly([q(0, -w), q(L_, -w), q(L_, w), q(0, w)]) & fl
        s.rgb[m] = (30, 30, 36)
        s.rgb[s.poly([q(0, -0.6), q(L_, -0.6), q(L_, 0.6), q(0, 0.6)]) & fl] = np.array(PINK)*0.9
    for (gx, gy) in GUNS:                                                           # core -> gun lifts
        v = np.array([gx - CORE[0], gy - CORE[1]], float); v /= np.linalg.norm(v)
        conduit(tuple(np.array(CORE) + v*18), tuple(np.array([gx, gy]) - v*(GR + 3)))
    RB = [(CX - 58, 178), (CX + 58, 178)]
    for (bx, by) in RB:                                                             # core -> repair bays (secondary)
        conduit((CX + np.sign(bx - CX)*14, 124), (bx - np.sign(bx - CX)*12, by - 12), 1.8)
    conduit((CX, 94), (CX, 88), 2.6)                                                 # core -> fore wall / crew block
    ring = s.disk(*CORE, 19)
    s.plate(ring, PL_D, z=1.3, bevel=1.8, inset=1.2, shadow_k=0.8, notch=0)          # core containment collar
    zmark(1.4, s.drive_core, CORE[0], CORE[1], 15, glow=tuple(PINK))
    for a_ in range(0, 360, 30): s.rgb[s.disk(CORE[0] + 17.5*np.cos(np.radians(a_)), CORE[1] + 17.5*np.sin(np.radians(a_)), 0.7)] = (40, 42, 46)
    for (bx, by) in RB:                                                             # FIGHTER REPAIR BAYS (aft corners)
        pad = s.rrect(bx - 15, by - 13, bx + 15, by + 13, 2)
        s.rgb[pad & fl] = (70, 76, 80); s.rgb[pad & fl & ~erode(pad, 0.9)] = (200, 170, 60)
        for sx in (-1, 1): s.rgb[s.rrect(bx + sx*5 - 0.6, by - 9, bx + sx*5 + 0.6, by + 9, 0.3) & fl] = (200, 170, 60)
        g_ = np.sign(bx - CX); gx_ = bx + g_*12
        s.plate(s.rrect(min(gx_, gx_ + g_*4), by - 12, max(gx_, gx_ + g_*4), by + 12, 1), PL, z=1.5, bevel=0.8, inset=0.4, shadow_k=0.8, notch=0)
        s.plate(s.rrect(min(bx, gx_), by - 2, max(bx, gx_), by + 2, 1), PL_L, z=1.7, bevel=0.6, inset=0.3, shadow_k=0.8, notch=0)
        s.rgb[s.disk(bx, by, 2.0)] = (60, 66, 70); s.rgb[s.disk(bx, by, 0.9)] = (255, 200, 90)
    for (x0_, x1_) in ((CX - 24, CX - 8), (CX + 8, CX + 24)):                     # CREW ROOMS on the fore wall
        cr = s.rrect(x0_, iy0 + 1, x1_, iy0 + 20, 2)
        s.plate(cr, PL, z=1.6, bevel=1.2, inset=0.8, shadow_k=0.85, notch=0)
        for k in range(3): s.rgb[s.rrect(x0_ + 3, iy0 + 5 + k*4.6, x1_ - 3, iy0 + 6.6 + k*4.6, 0.3)] = (255, 222, 150)
    al = s.rrect(CX - 7, iy0 + 1, CX + 7, iy0 + 22, 1.5)                             # PRESSURE ROOM between them, opens onto the floor
    s.plate(al, PL_L, z=1.7, bevel=1.2, inset=0.8, shadow_k=0.85, notch=0)
    s.rgb[s.rrect(CX - 5, iy0 + 4, CX + 5, iy0 + 19, 0.8)] = (36, 40, 46)
    s.rgb[s.rrect(CX - 5.5, iy0 + 20.5, CX + 5.5, iy0 + 22, 0.3)] = (150, 156, 164)
    s.rgb[s.disk(CX - 3, iy0 + 3, 0.8)] = (90, 255, 120); s.rgb[s.disk(CX + 3, iy0 + 3, 0.8)] = (255, 70, 60)
    for g in (-1, 1):                                                               # side-wall pressure rooms (crew decks beyond)
        xw = ix0 if g < 0 else ix1
        al = s.rrect(min(xw, xw - g*11), 137, max(xw, xw - g*11), 157, 1.5)
        s.plate(al, PL_L, z=1.7, bevel=1.2, inset=0.8, shadow_k=0.85, notch=0)
        s.rgb[s.rrect(min(xw - g*2, xw - g*9), 140, max(xw - g*2, xw - g*9), 154, 0.8)] = (36, 40, 46)
        s.rgb[s.rrect(min(xw - g*10.5, xw - g*12), 142, max(xw - g*10.5, xw - g*12), 152, 0.3)] = (150, 156, 164)
        s.rgb[s.disk(xw - g*5.5, 139, 0.7)] = (90, 255, 120); s.rgb[s.disk(xw - g*5.5, 155, 0.7)] = (255, 70, 60)
    for (gx, gy) in GUNS:                                                           # the 3 GUN SILOS
        rr = np.hypot(xx_ - gx, yy_ - gy); an = np.degrees(np.arctan2(yy_ - gy, xx_ - gx))
        c8 = s.poly(Ship.mirror_pts([(gx - 12, gy - GR - 4), (gx - GR - 4, gy - 12), (gx - GR - 4, gy + 12), (gx - 12, gy + GR + 4)], gx))
        s.plate(c8 & fl, PL_D, z=1.6, bevel=1.6, inset=1.0, shadow_k=0.9, notch=0)   # armoured silo collar
        for a_ in (45, 135, 225, 315):
            s.rgb[s.disk(gx + (GR + 1)*np.cos(np.radians(a_)), gy + (GR + 1)*np.sin(np.radians(a_)), 1.0)] = (255, 170, 90)   # lift status lights
        if MODE == 'open':                                                           # closed: two orange blast doors, seam, hazard lip
            for sd in (-1, 1):
                leaf = (rr < GR) & ((xx_ - gx)*sd > 0.6)
                s.plate(leaf, ORG*0.85, z=1.8, bevel=1.4, dome=0.5, inset=0.8, shadow_k=0.8, notch=0,
                        lines=[leaf & (np.abs(rr - GR*0.62) < 0.3)])
            s.rgb[(rr < GR) & (np.abs(xx_ - gx) < 0.6)] = (24, 24, 28)
            s.rgb[(np.abs(rr - GR - 0.8) < 0.8) & ((an // 20) % 2 == 0)] = (220, 180, 50)
        else:                                                                        # open: dark shaft with lift rails
            sh = rr < GR
            s.rgb[sh] = (np.array([48, 52, 58])*np.clip(1.1 - rr/GR, 0.12, 1)[..., None])[sh]; s.z[sh] = 0.3
            for a_ in (0, 90, 180, 270):
                s.rgb[sh & (np.abs(((an - a_ + 180) % 360) - 180) < 3) & (rr > GR*0.55)] = (96, 100, 108)
    for g in (-1, 1):                                                               # stowed hatch leaves under the rails
        s.plate(s.rrect(min(X(g, 84), X(g, 90)), HY0 + 2, max(X(g, 84), X(g, 90)), HY1 - 2, 1.5), PL, z=2.4, bevel=1.0, inset=0.5, shadow_k=0.8)
        s.plate(s.rrect(min(X(g, 86), X(g, 94)), HY0 + 4, max(X(g, 86), X(g, 94)), HY1 - 4, 2), PL_D, z=3.9, bevel=1.4, inset=0.8, shadow_k=0.85)
    rim = hatch & ~erode(hatch, 1.4)
    for k_, yv in enumerate(np.arange(HY0 + 4, HY1, 10)):                           # rim landing lights
        for xs_ in (HX0 + 0.8, HX1 - 0.8): s.rgb[s.disk(xs_, yv, 0.8)] = (190, 255, 170)
    for xv in np.arange(HX0 + 10, HX1 - 6, 12): s.rgb[s.disk(xv, HY1 - 0.8, 0.8)] = (190, 255, 170)
    sysl('CARRIER (hangar open): 3 gun silos in the floor, drive core between them, repair bays, crew + pressure rooms', CX, 130)
else:
    # ============ BATTLESHIP MODE: the hatch leaves have slid under the side rails, the bay is open. Its floor is lighter
    # crew-deck armour (crew still work below); the 3 main-gun platforms are LIFTED high out of it on their lift columns.
    floor = hatch
    s.plate(floor, PL_L*1.02, z=1.6, bevel=1.8, inset=1.4, shadow_k=0.9,
            lines=[s.rrect(HX0, y, HX1, y + 0.6, 0.1) for y in (96, 140, 176)] + [s.rrect(CX + dx - 0.3, HY0, CX + dx + 0.3, HY1, 0.1) for dx in (-44, 44)])
    for (hx, hy) in [(CX - 66, 150), (CX + 66, 150), (CX - 30, 72), (CX + 30, 72)]:     # crew hatches + walkway lights
        s.hatch(hx - 6, hy - 4, hx + 6, hy + 4, haz=False)
    for yl in np.arange(HY0 + 8, HY1 - 4, 9):
        for sd in (-1, 1): s.rgb[s.disk(X(sd, 80), yl, 0.7)] = (255, 220, 150)
    for g in (-1, 1):                                                               # retracted leaf edges under the rails
        s.plate(s.rrect(min(X(g, 84), X(g, 90)), HY0 + 2, max(X(g, 84), X(g, 90)), HY1 - 2, 1.5), PL, z=2.4, bevel=1.0, inset=0.5, shadow_k=0.8)
        s.plate(s.rrect(min(X(g, 86), X(g, 94)), HY0 + 4, max(X(g, 86), X(g, 94)), HY1 - 4, 2), PL_D, z=3.9, bevel=1.4, inset=0.8, shadow_k=0.85)
    for (gx, gy) in GUNS:                                                           # 2nd-layer deck: cut-outs round each gun silo
        rr = np.hypot(xx_ - gx, yy_ - gy)
        oc_ = s.poly(Ship.mirror_pts([(gx - 12, gy - GR - 1.5), (gx - GR - 1.5, gy - 12), (gx - GR - 1.5, gy + 12), (gx - 12, gy + GR + 1.5)], gx))
        s.rgb[oc_ & hatch] *= 0.4                                                   # octagonal cut-out = platform footprint + 1.5 px
        s.rgb[oc_ & ~erode(oc_, 0.8) & hatch] = (170, 176, 184)                       # lit cut edge of the deck
        if MODE == 'deck': continue
        for a_ in (45, 135, 225, 315):                                              # lift columns (seen past the platform edge)
            cxp, cyp = gx + 27*np.cos(np.radians(a_)), gy + 27*np.sin(np.radians(a_))
            s.plate(s.disk(cxp, cyp, 3.2), PL_D, z=2.6, bevel=1.0, dome=0.6, inset=0.4, shadow_k=0.8)
        plat = s.poly(Ship.mirror_pts([(gx - 11, gy - 27), (gx - 27, gy - 11), (gx - 27, gy + 11), (gx - 11, gy + 27)], gx))
        s.plate(plat, PL, z=5.0, bevel=2.8, dome=0.6, inset=2.0, shadow_k=0.95, paint=[(plat & (np.abs(rr - 24) < 1.2), ORG)])
        s.bolt_row(plat, 1.6, 5)
        zmark(5.3, s.mount, gx, gy, 16, PL_D)                                        # large energy turret ring
    sysl('BATTLESHIP mode: silo hangar converted to an armoured deck, 3 gun platforms lifted up from inside the ship', CX, 130)

# ================================================================ buried core (armoured cover) aft on the deck
sysl('drive core: at the heart of the silo hangar (visible when the hangar is open)', CX, 131)

# ================================================================ PD on armoured blisters along the belts
for g in (-1, 1):                                                                   # notch floor: a sunk armoured socket pad per pair
    for y_ in (64, 111, 158, 206):                                                            # deck-strip mounts: octagonal armour collar set into the deck
        c8 = s.poly(Ship.mirror_pts([(X(g, 104) - 5, y_ - 12), (X(g, 104) - 12, y_ - 5), (X(g, 104) - 12, y_ + 5), (X(g, 104) - 5, y_ + 12)], X(g, 104)))
        s.plate(c8, PL_D, z=2.8, bevel=1.8, inset=1.2, shadow_k=0.9)
for (px, py) in PD:                                                                 # mounts SUNK into the pad (dark socket, flush ring)
    rr = np.hypot(xx_ - px, yy_ - py)
    s.rgb[rr < 7.6] = (30, 32, 36); s.z[rr < 7.6] = 2.6
    zmark(2.9, s.mount, px, py, 6.0, PL_D)
sysl('8 small ballistic PD: 4 per side sunk in octagonal collars on the green deck strips', X(-1, 104), 111)

# ================================================================ command: elongated 3-tier tower (Tiamat/Asura/Artemis concept) over neck + pod
s.plate(neck | pod, PL_D, z=2.6, bevel=2.4, dome=0.6, inset=1.6, shadow_k=0.9)
# v6: WIDER + SHORTER tower (about the length of the main drives)
cmd1 = s.poly(spline([(X(-1, 30), 218), (X(1, 30), 218), (X(1, 40), 228), (X(1, 40), 288), (X(1, 30), 302), (X(-1, 30), 302), (X(-1, 40), 288), (X(-1, 40), 228)], 10, True))
m1 = s.plate(cmd1, PL, z=4.0, bevel=3.2, dome=1.0, inset=2.4, shadow_k=0.9, paint=[(cmd1 & (np.abs(yy_ - 294) < 2.0), ORG)])
s.bolt_row(m1, 1.6, 5)
cmd2 = s.poly(spline([(X(-1, 19), 222), (X(1, 19), 222), (X(1, 30), 230), (X(1, 30), 284), (X(1, 21), 294), (X(-1, 21), 294), (X(-1, 30), 284), (X(-1, 30), 230)], 10, True))
m2 = s.plate(cmd2, PL_L, z=5.2, bevel=2.8, dome=1.3, ridge=('x', CX, 1.8, 30), inset=2.0, shadow_k=0.9)
glass = s.poly(spline([(X(-1, 19), 224.5), (X(1, 19), 224.5), (X(1, 28), 231), (X(1, 28), 236), (X(1, 18), 230), (X(-1, 18), 230), (X(-1, 28), 236), (X(-1, 28), 231)], 8, True)) & m2
gy = np.clip((yy_ - 224)/12, 0, 1); s.rgb[glass] = (CYAN*(1.15 - 0.55*gy[..., None]))[glass]
for k_ in range(-26, 27, 4): s.rgb[glass & (np.abs(xx_ - (CX + k_)) < 0.35)] = (40, 70, 80)
cmd3 = s.poly(spline([(X(-1, 11), 244), (X(1, 11), 244), (X(1, 17), 252), (X(1, 17), 282), (X(1, 12), 290), (X(-1, 12), 290), (X(-1, 17), 282), (X(-1, 17), 252)], 8, True))
s.plate(cmd3, PL_L*1.03, z=6.3, bevel=2.2, dome=1.3, ridge=('x', CX, 1.4, 17), inset=1.6, shadow_k=0.9, paint=[(cmd3 & (np.abs(yy_ - 247) < 1.4), ORG)])
for yv in (256, 264): s.grille(s.rrect(CX - 9, yv, CX + 9, yv + 5, 1), period=1.6)
s.mount(CX, 274, 4.6, PL, well_col=(120, 70, 90))
sysl('command tower (3 tiers) from just aft of the silo hangar to 10 px past the drives; cyan bridge glass forward', CX, 222)

# ================================================================ symmetry + lights
_h = CX*s.SS
s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
s.lights([(X(-1, 150), 64), (X(1, 150), 64), (X(-1, 124), 256), (X(1, 124), 256), (CX, 24)],
         [(255, 70, 60), (90, 255, 120), (255, 70, 60), (90, 255, 120), (255, 255, 240)])

sprite = s.render()
sprite.save(_ROOT + f'/ss_style/siren_ss_v12_{MODE}.png')
json.dump(dict(W=W, H=H, slots=SLOTS, ENG=ENG, small=SMALL, lat=[]), open(_ROOT + '/ss_style/siren_ss_v12_slots.json', 'w'))
json.dump(SYSTEMS, open(_ROOT + '/ss_style/siren_v12_systems.json', 'w'))
print('ok')
