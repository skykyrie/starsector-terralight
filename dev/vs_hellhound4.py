import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Hellhound - Starsector style v4 = v3 drawing, split into separately rendered PARTS on the same 170x286 canvas:
  hull  : nose, handle (complete shell + seams under where the tower sat), gun band + its 3 top mounts, missile ledges,
          socket collar + gangway bellows over the ball joint, actuator brackets + stub actuator cylinders
  tower : the long 3-tier command tower module (saddle base, tiers, visor, fire-control dome, mast + its light),
          plus the soft shadow it casts on the handle (black semi-transparent fringe)
  drive : the swivelling lamp-head drive block on the ball joint (faceted flare, ribs, blue ring, actuator lugs, grey notched
          rim, rim nav lights) + the actuator piston rods/rod-end eyes that move with it
Outputs ss_style/hellhound_ss_v4_{hull,tower,drive,full}.png + hellhound_ss_v4_slots.json.
Composite order (bottom -> top): drive, hull, tower."""
import json, numpy as np
from scipy.interpolate import PchipInterpolator
import vstyle, vparts as VP
from vstyle import Ship, spline
import splitlib as SL

W, H, CX = 170, 286, 85
HR = 34
GUNS = [(63, 86), (85, 86), (107, 86)]
MIS = [(43, 38), (127, 38)]
ENG = [(CX, 250)]
PIVOT = (CX, 185)                                    # ball joint centre (3D: ball r20 at py 185)
ZK = 1/12.0                                          # 3D height (px) -> render z

AR = np.array([125, 138, 122]); AR_D = np.array([82, 92, 80]); AR_L = np.array([166, 178, 162])
BLU = np.array([58, 143, 216]); BLU_L = np.array([122, 184, 240]); GLS = np.array([143, 208, 255])
RIMC = np.array([116, 121, 130]); SEAM = (38, 44, 38); DARK = (25, 28, 26)
PARTS = ('hull', 'tower', 'drive')
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))

_hp = PchipInterpolator([18, 19, 20, 23, 26, 30, 34, 42, 50, 56, 59, 62, 172, 175, 177, 181], [0, 11, 16, 22.5, 26, 28.6, 30, 30.7, 31, 31, 32.8, 34, 34, 33, 31, 30])
def r_hull(py): return np.where((py >= 18) & (py <= 181), _hp(np.clip(py, 18, 181)), -1.0)
_fp = PchipInterpolator([195, 197, 201, 208, 218, 228, 233, 236], [27, 33, 37, 50, 63, 71, 74, 74])
def r_flare(py): return np.where((py >= 195) & (py <= 236), _fp(np.clip(py, 195, 236)), -1.0)
def r_rim(py): return np.where((py >= 234) & (py <= 250), np.interp(py, [234, 236, 238, 240, 246, 248, 250], [74, 80, 81.5, 82, 82, 80.5, 78]), -1.0)
def r_band(py): return np.where((py >= 72) & (py <= 100), np.interp(py, [72, 73.5, 75, 78, 94, 97, 98.5, 100], [34, 38, 40, 41, 41, 40, 38, 34]), -1.0)


def build(active):
    """draw the ship with only the `active` parts kept; returns the Ship before its depth pass"""
    SYSTEMS.clear()
    _L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = CX
    s = Ship(W, H, seed=141)
    P = SL.SplitCtx(s, active)
    s.auto_z = True; s.depth = dict(unit=7.0, s_str=0.9, tint=0.38, ao=0.6, ao_r=5, sdir=((0.6, 0.8), (-0.6, 0.8)), s_soft=0.9)
    _plate0, _bolt0 = s.plate, s.bolt_row
    def _plate(mask, color, *a, **k):
        k.setdefault('tex', 0.018); k.setdefault('grime', 0.0); k.setdefault('notch', 0); return _plate0(mask, color, *a, **k)
    def _bolt(m, inset=1.8, spacing=4.0, seed=0):
        if m is not None and m.sum()/s.SS**2 > 700: _bolt0(m, inset, spacing*2.4)
    s.plate, s.bolt_row = _plate, _bolt
    X = lambda g, dx: CX + g*dx
    yy_ = s.yy/s.SS; xx_ = s.xx/s.SS; ax_ = np.abs(xx_ - CX)
    def cylz(mask, R, base=0.0):
        Rm = R[mask] if np.ndim(R) else R
        s.z[mask] = base + np.sqrt(np.clip(Rm**2 - ax_[mask]**2, 0, None))*ZK

    RH, RF, RR, RB = r_hull(yy_), r_flare(yy_), r_rim(yy_), r_band(yy_)
    hull = ax_ <= RH
    flare = ax_ <= RF
    rim = ax_ <= RR
    band = ax_ <= RB
    bell = (ax_ <= 36) & (yy_ >= 184) & (yy_ <= 196.5)
    ledges = s.rrect(X(-1, 49), 27, X(-1, 28), 49, 4) | s.rrect(X(1, 28), 27, X(1, 49), 49, 4)

    # ============================================================ silhouette + machinery base (one BSP layout, trimmed per part)
    s.guts(hull | flare | rim | bell | ledges, seed=143, tone=(44, 50, 46), minc=3, maxc=9); s.z[:] = 0
    g_drive = flare | rim
    g_hull = (hull | bell | ledges) & ~g_drive
    keep = np.zeros_like(s.a)
    if P.on('hull'): keep |= g_hull
    if P.on('drive'): keep |= g_drive
    s.a &= keep

    with P('hull'):
        # ======================================================== missile ledges at the nose tip, plain mount pads
        for g in (-1, 1):
            led = s.rrect(min(X(g, 28), X(g, 49)), 27, max(X(g, 28), X(g, 49)), 49, 4)
            s.plate(led, AR_D, z=0.3, bevel=1.8, dome=0.4, inset=1.0, shadow_k=0.9)
            top = s.rrect(min(X(g, 30), X(g, 47.5)), 29, max(X(g, 30), X(g, 47.5)), 47, 3)
            s.plate(top & ~s.disk(X(g, 42), 38, 7.4), BLU*0.95, z=0.45, bevel=1.0, dome=0.2, inset=0.0, shadow_k=0.8)
            s.plate(s.disk(X(g, 42), 38, 7.2), AR, z=0.55, bevel=1.4, dome=0.3, inset=0.6, shadow_k=0.9)
            before = s.rgb.copy(); s.mount(X(g, 42), 38, 5.4, AR_L); s.z[np.abs(s.rgb - before).sum(2) > 0.5] = 0.5
            for k in range(3): s.rgb[s.rrect(min(X(g, 46.5), X(g, 48)), 31 + k*2, max(X(g, 46.5), X(g, 48)), 31.8 + k*2, 0.2)] = SEAM
        sysl('2 small missile pads on armoured side ledges at the nose tip, 120 deg, 20 deg out', X(-1, 42), 38)

        # ======================================================== actuator brackets on the handle flanks (py 164)
        for g in (-1, 1):
            br = s.rrect(min(X(g, 31), X(g, 41)), 159, max(X(g, 31), X(g, 41)), 169, 1.6)
            s.plate(br, AR_D, z=0.35, bevel=1.4, inset=0.6, shadow_k=0.9)

        # ======================================================== sensor dome at the nose tip
        s.plate(s.ell(CX, 19, 7, 4.9), GLS*0.95, z=0.6, bevel=1.6, dome=1.0, inset=0.0, shadow_k=0.9)
        s.rgb[s.ell(CX - 2.2, 16.2, 2.0, 1.1)] = (225, 245, 255)

        # ======================================================== handle + nose block (one lathe): shell, seams, hoops
        s.plate(hull, AR, z=2.8, bevel=9.0, dome=2.0, inset=2.0, shadow_k=0.95); cylz(hull, RH)
        for g in (-1, 1): s.rgb[hull & (np.abs(xx_ - X(g, 31.4)) < 0.5) & (yy_ > 100) & (yy_ < 176)] = SEAM
        for py in (146, 160): s.rgb[hull & (np.abs(yy_ - py) < 0.55) & (ax_ < RH - 1.2)] = SEAM
        nose = hull & (yy_ < 60.5)
        s.plate(nose, AR*1.06, z=2.8, bevel=6.0, dome=1.8, inset=1.6, shadow_k=0.95); cylz(nose, RH)
        s.rgb[nose & (np.abs(yy_ - 56.5) < 0.55) & (ax_ < RH - 1.2)] = SEAM
        for py in (26, 50):
            s.rgb[nose & (np.abs(yy_ - py) < 0.75) & (ax_ < RH - 0.8)] = AR_L*1.08
            s.rgb[nose & (np.abs(yy_ - py - 1.0) < 0.35) & (ax_ < RH - 0.8)] = SEAM
        for f in (0.4, 0.75):
            s.rgb[nose & (np.abs(yy_ - (20 + 4*f)) < 0.35) & (ax_ < r_hull(20 + 4*f) - 1)] = AR*0.9
        s.rgb[s.ell(CX, 19.9, 7.4, 0.8) & (yy_ > 19.3)] = BLU
        hoop = (np.abs(yy_ - 62) < 1.3) & (ax_ <= 35.4)
        s.plate(hoop, AR_L, z=3.0, bevel=0.9, dome=0.2, shadow_k=0.8); cylz(hoop, 35.4)
        for g in (-1, 1):
            for py in (36, 42): s.rgb[s.rrect(X(g, 25.5) - 0.7, py - 1.4, X(g, 25.5) + 0.7, py + 1.4, 0.3)] = (200, 236, 255)
        sysl('armoured cylinder hull: rounded nose block, hoops, seams, glass sensor dome at the tip', X(1, 20), 40)

        # ======================================================== signal-blue gun band + 3 small ballistic sunk
        s.plate(band, BLU, z=3.4, bevel=3.0, dome=1.4, inset=1.2, shadow_k=0.95); cylz(band, RB)
        for py in (81, 91): s.rgb[band & (np.abs(yy_ - py) < 0.6) & (ax_ < RB - 1.0)] = BLU_L
        for (px, py) in GUNS:
            od = (0, -1) if px == CX else ((1 if px > CX else -1), 0)
            VP.sunk_mount(s, px, py, 5.0, od, metal=AR*0.9, lip_metal=BLU_L, z=3.5, lip_z=3.9, accent=BLU*0.8)
        sysl('signal-blue gun band: 3 small ballistic sunk on top (+3 under-hull beneath, now on the tower module), 150 deg fwd', CX, 86)

    with P('tower'):
        # ======================================================== COMMAND TOWER: saddle base + 3 tiers, blue visor, fire-control dome, mast
        sad = (ax_ <= 25.2) & (yy_ >= 102) & (yy_ <= 170)
        s.plate(sad, AR_L*0.95, z=3.1, bevel=1.6, dome=0.6, inset=0.8, shadow_k=0.95); cylz(sad, 37.0)
        for py in (101, 171):
            e = (ax_ <= 26.4) & (np.abs(yy_ - py) < 1.1)
            s.plate(e, BLU, z=3.15, bevel=0.8, shadow_k=0.8); cylz(e, 37.6)
        def tier(hw, y0, y1, r):
            return s.poly(spline([(X(-1, hw - r), y0), (X(1, hw - r), y0), (X(1, hw), y0 + r), (X(1, hw), y1 - r), (X(1, hw - r), y1),
                                  (X(-1, hw - r), y1), (X(-1, hw), y1 - r), (X(-1, hw), y0 + r)], 8, True))
        c1 = tier(16.4, 102.6, 169.4, 7)
        s.plate(c1, AR, z=44.6*ZK, bevel=2.6, dome=0.9, inset=1.8, shadow_k=0.95, paint=[(c1 & (np.abs(yy_ - 163) < 1.0), BLU)])
        s.bolt_row(c1, 1.6, 5)
        c2 = tier(12.4, 108.6, 165.4, 6)
        s.plate(c2, AR_L, z=52.6*ZK, bevel=2.2, dome=1.0, ridge=('x', CX, 1.0, 12), inset=1.4, shadow_k=0.95)
        glass = tier(10.5, 109.2, 113.6, 2.5) & c2
        gy = np.clip((yy_ - 109.2)/4.4, 0, 1); s.rgb[glass] = np.clip(GLS*(1.12 - 0.5*gy[..., None]), 0, 255)[glass]
        for k_ in (-6, 0, 6): s.rgb[glass & (np.abs(xx_ - (CX + k_)) < 0.4)] = (30, 60, 90)
        for g in (-1, 1):
            for k in range(3): s.rgb[s.rrect(min(X(g, 8.6), X(g, 11.4)), 151 + k*3, max(X(g, 8.6), X(g, 11.4)), 152 + k*3, 0.3)] = SEAM
        c3 = tier(7.9, 122.6, 159.4, 4.5)
        s.plate(c3, AR_L*1.04, z=58.6*ZK, bevel=1.8, dome=0.9, inset=1.1, shadow_k=0.95)
        for k in range(3): s.rgb[c3 & (np.abs(yy_ - (142 + k*4)) < 0.4) & (ax_ < 5)] = SEAM
        s.plate(s.disk(CX, 130, 4.2), AR_L, z=62.5*ZK, bevel=1.4, dome=1.0, inset=0.5, shadow_k=0.95)
        s.rgb[s.disk(CX, 130, 1.6)] = (40, 90, 140)
        s.plate(s.disk(CX, 161.2, 1.6), AR_L, z=67*ZK, bevel=0.8, shadow_k=0.9)
        sysl('long command tower module (3 tiers on a saddle base), blue visor glass forward, fire-control dome, mast', CX, 112)

    with P('drive'):
        # ======================================================== LAMP-HEAD DRIVE BLOCK: faceted flare (12 ribs), blue ring, lugs, grey notched rim
        dFp = _fp.derivative()
        th = np.degrees(np.arcsin(np.clip(ax_/np.maximum(RF, 1), 0, 1)))
        for (a0, a1) in ((0, 15), (15, 45), (45, 75), (75, 91)):
            ac = np.radians(min((a0 + a1)/2, 70))
            for g in ((-1,) if a0 == 0 else (-1, 1)):
                fm = flare & (th >= a0) & (th < a1) & (((xx_ - CX)*g >= 0) if a0 else True)
                tx = -g*np.tan(ac)*0.30 if a0 else 0.0
                s.plate(fm, AR*0.92, z=3.0, bevel=1.2, dome=1.4, tilt=(tx, 0.22/np.cos(ac)), inset=0.0, shadow_k=0.5, outline=0.5)
        fl = np.clip((yy_ - 195)/41, 0, 1)
        s.rgb[flare] *= (1.08 - 0.22*np.clip((fl[flare] - 0.35)/0.65, 0, 1))[:, None]
        cylz(flare, RF)
        for k in range(12):
            a = np.radians(k*30 + 15)
            if np.cos(a) <= 0.05: continue
            pts = [(CX + np.sin(a)*(float(r_flare(py)) + 0.6), py) for py in np.linspace(202, 229.5, 12)]
            m = s.cable(pts, 1.9, AR_L, clamps=0)
            s.z[m] = (np.sqrt(np.clip(r_flare(yy_[m])**2 - ax_[m]**2, 0, None)) + 1.2)*ZK
        fr = (np.abs(yy_ - 201.5) < 1.5) & (ax_ <= 38.6)
        s.plate(fr, BLU, z=3.2, bevel=0.9, dome=0.2, shadow_k=0.8); cylz(fr, 38.8)
        for g in (-1, 1):
            lug = s.rrect(min(X(g, 57), X(g, 66)), 209.5, max(X(g, 57), X(g, 66)), 218.5, 1.4) & ~flare
            s.plate(lug, AR_D, z=0.5, bevel=1.2, inset=0.5, shadow_k=0.9)
        s.plate(rim, RIMC, z=6.8, bevel=4.0, dome=1.4, inset=1.6, shadow_k=0.95, paint=[(rim & (yy_ > 247), RIMC*0.8)]); cylz(rim, RR)
        for k in range(-5, 6):
            nx = CX + 82.4*np.sin(np.radians(k*15))
            s.rgb[rim & (np.abs(xx_ - nx) < 0.9) & (yy_ > 239) & (yy_ < 247)] = DARK
        s.rgb[rim & (np.abs(yy_ - 236.2) < 0.4) & (ax_ < RR - 1.5)] = (90, 94, 100)
        sysl('lamp-head drive block on the ball joint: faceted flare with 12 ribs + blue ring, grey notched armoured rim', X(-1, 40), 222)

    with P('hull'):
        # ======================================================== socket collar + gangway bellows over the ball joint
        sock = (yy_ >= 176) & (yy_ <= 184) & (ax_ <= 31 + (yy_ - 176)/4)
        s.plate(sock, AR_L*0.95, z=3.0, bevel=1.4, dome=0.4, inset=0.7, shadow_k=0.95); cylz(sock, 31 + (yy_ - 176)/4)
        for k in range(-3, 4):
            bx = CX + 33.6*np.sin(np.radians(k*22.5)); s.rgb[s.disk(bx, 178.5, 0.8)] = (50, 56, 50)
            s.rgb[s.disk(bx - 0.25, 178.2, 0.35)] = AR_L*1.1
        for i in range(9):
            py = 185.9 + i*1.1; ridge = i % 2 == 1
            rr_ = 35.2 if ridge else 32.8
            f = (np.abs(yy_ - py) < 0.62) & (ax_ <= rr_)
            s.plate(f, np.array((58, 63, 60)) if ridge else AR_D, z=2.9, bevel=0.45, outline=0.3, shadow_k=0.4); cylz(f, rr_)
        for py in (185, 195):
            f = (np.abs(yy_ - py) < 1.25) & (ax_ <= 35.9)
            s.plate(f, BLU, z=3.0, bevel=0.8, dome=0.2, shadow_k=0.85); cylz(f, 35.9)
        sysl('armoured socket collar (bolted, blue seal) + gangway bellows over the ball joint', X(1, 30), 190)

    # ============================================================ hydraulic actuators: cylinder on the hull bracket, piston rod on the drive lug
    for g in (-1, 1):
        A = np.array([X(g, 40), 164.0]); B = np.array([X(g, 63), 214.0]); u = (B - A)/np.linalg.norm(B - A)
        C = A + u*22
        with P('hull'):
            m = s.cable([tuple(A), tuple(C)], 4.6, AR_L*0.95, clamps=0, smooth=False); s.z[m] = 0.7
        with P('drive'):
            m = s.cable([tuple(C), tuple(B)], 2.6, (206, 210, 216), clamps=0, smooth=False); s.z[m] = 0.6
        with P('hull'):
            cf = s.poly([tuple(C + np.array([-u[1], u[0]])*3.1 - u*0.9), tuple(C + np.array([-u[1], u[0]])*3.1 + u*0.9),
                         tuple(C - np.array([-u[1], u[0]])*3.1 + u*0.9), tuple(C - np.array([-u[1], u[0]])*3.1 - u*0.9)])
            s.plate(cf, BLU, z=0.75, bevel=0.6, shadow_k=0.6)
        for P_, part in ((A, 'hull'), (B, 'drive')):
            with P(part):
                s.plate(s.disk(*P_, 2.1), AR_D, z=0.8, bevel=0.8, shadow_k=0.7)
                s.rgb[s.disk(P_[0] - 0.4, P_[1] - 0.4, 0.7)] = (196, 200, 206)
    sysl('2 hydraulic actuators swing the whole drive block +-6 deg when strafing (cylinders on the hull, rods on the drive)', X(-1, 52), 190)

    # ============================================================ symmetry + lights
    _h = CX*s.SS
    s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
    with P('drive'): s.lights([(X(-1, 82.6), 238), (X(1, 82.6), 238)], [(255, 70, 60), (90, 255, 120)])
    with P('tower'): s.lights([(CX, 161.2)], [(255, 255, 240)])
    return s


if __name__ == '__main__':
    OUT = _ROOT + '/ss_style/hellhound_ss_v4_'
    snap = lambda s: (s.rgb.copy(), s.a.copy(), s.z.copy())
    sF = build(PARTS); full_snap = snap(sF); zmax = float((sF.z*sF.a).max()); full_ref = sF.render()   # whole ship in one pass (== v3)
    sC = build({'hull', 'drive'}); hull_ctx = snap(sC)                        # the hull is lit without the tower (no tower shadow baked in)
    ims = {}
    for p in PARTS:
        sp = build({p}); ims[p] = SL.lit_part(sp, snap(sp), hull_ctx if p == 'hull' else full_snap, zmax)
    ims['hull'] = SL.add_shadow_fringe(ims['hull'], full_ref, ims['drive'])       # bellows/socket shadow falling on the drive block
    ims['tower'] = SL.add_shadow_fringe(ims['tower'], full_ref, SL.over(ims['drive'], ims['hull']))
    comp = SL.over(ims['drive'], ims['hull'], ims['tower'])
    for p in PARTS: ims[p].save(OUT + p + '.png')
    comp.save(OUT + 'full.png')
    tb = SL.bbox(ims['tower'], 250)
    v3 = json.load(open(_ROOT + '/ss_style/hellhound_ss_v3_slots.json'))
    slots = [sl for sl in v3['slots'] if not sl.get('hide')]
    module_slots = [dict(sl, mount='TURRET', hide=True) for sl in v3['slots'] if sl.get('hide')]
    json.dump(dict(W=W, H=H, slots=slots, ENG=ENG, small=[], lat=[], pivot_drive=list(PIVOT), tower_bbox=tb,
                   module_slots=module_slots, parts=dict(order=['drive', 'hull', 'tower'])),
              open(OUT + 'slots.json', 'w'))
    json.dump(SYSTEMS, open(_ROOT + '/ss_style/hellhound_v4_systems.json', 'w'))
    from PIL import Image
    v3im = Image.open(_ROOT + '/ss_style/hellhound_ss_v3.png')
    print('one-pass full vs v3 :', SL.diff_stats(full_ref, v3im))
    print('composite vs v3     :', SL.diff_stats(comp, v3im))
    print('tower_bbox', tb, 'pivot', PIVOT, 'ENG', ENG)
