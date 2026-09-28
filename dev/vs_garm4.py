import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Garm - Starsector style v4 = v3 drawing, split into separately rendered PARTS on the same 200x250 canvas:
  hull        : everything fixed, incl. the two fixed pylons
  podL / podR : each side thruster pod that swivels (nacelle + orange hoops, aft can + orange lip, swivel hub disk),
                lit within the full ship, plus the soft shadow it casts on its pylon (black semi-transparent fringe)
Outputs ss_style/garm_ss_v4_{hull,podL,podR,full}.png + garm_ss_v4_slots.json (v3 slots + pivot_L/pivot_R).
Composite order (bottom -> top): hull, podL, podR."""
import json, numpy as np
import vstyle, vparts as VP
from vstyle import Ship, spline

W, H, CX = 200, 250, 100
DCY, DRX, DRZ = 98, 70, 68                        # dome centre + top-view radii (3D DX, DZ)
BX0, BY0, BY1, BR = 38, 132, 220, 20              # rear box (3D hw 58 + 6 bevel, squeezed 2 px so the pods fit the canvas)
TOPS = [(CX, 50, 4.4), (CX, 80, 5.4), (CX, 110, 5.6)]          # dome small ballistic: px, py, collar z (terraced)
PD = [(CX - 40, 203), (CX + 40, 203)]
PODX, PODY = 18, 192                              # side thruster pods (3D has them at 7/193 - pulled in to fit 200 px)
HUBX = 33
ENG = [(CX, 232)]

AR = np.array([158, 124, 76]); AR_L = np.array([196, 166, 118]); AR_D = np.array([94, 74, 48])
ORG = np.array([224, 120, 42]); JADE = np.array([63, 154, 120]); GLS = np.array([127, 240, 200])
GREY = np.array([138, 142, 148]); GREY_D = np.array([74, 78, 84]); SEAM = (52, 42, 30)
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))
import splitlib as SL
PARTS = ('hull', 'pod')
PIVL = (HUBX, PODY)                       # left pod swivel hub centre (right = mirrored)


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

    def tier(hw, y0, y1, r):
        return s.poly(spline([(X(-1, hw - r), y0), (X(1, hw - r), y0), (X(1, hw), y0 + r), (X(1, hw), y1 - r), (X(1, hw - r), y1),
                              (X(-1, hw - r), y1), (X(-1, hw), y1 - r), (X(-1, hw), y0 + r)], 8, True))
    # ================================================================ silhouette + machinery base
    u_ = (xx_ - CX)/DRX; v_ = (yy_ - DCY)/DRZ; rb = np.hypot(u_, v_); ab = np.degrees(np.arctan2(v_, u_))   # -90 = forward
    dome = rb <= 1.0
    box = s.rrect(BX0, BY0, W - BX0, BY1, BR)
    inner = rb < 0.717                                 # part of the dome that stands above the box top (3D: h > 46)
    prof = [(0, -24), (6, -22), (10, -16), (12, -8), (12, 8), (11, 12)]
    def pod_mask(px):
        k = 11/12
        pts = [(px - r*k, PODY + z) for r, z in prof] + [(px + r*k, PODY + z) for r, z in prof[::-1]]
        return s.poly(spline(pts, 10, True))
    pods = pod_mask(PODX) | pod_mask(W - PODX)
    pyl = s.rrect(HUBX - 2, 184, BX0 + 3, 200, 1.5); pyl |= s.sym(pyl)
    drive = s.rrect(CX - 23, 212, CX + 23, 230, 3) | s.rrect(CX - 27, 244, CX + 27, 248.4, 1.6)
    s.guts(dome | box | pods | pyl | drive, seed=143, tone=(56, 50, 42), minc=3, maxc=10); s.z[:] = 0
    keep = np.zeros_like(s.a)
    if P.on('hull'): keep |= (dome | box | pyl | drive) & ~pods
    if P.on('pod'): keep |= pods
    s.a &= keep                                          # one BSP guts layout, trimmed per part
    with P('hull'):
        # ================================================================ main drive: grey ribbed collar + cooled bell, orange lip
        s.plate(s.rrect(CX - 20, 212, CX + 20, 229, 3), GREY_D, z=3.0, bevel=1.6, dome=0.8, inset=0.6, shadow_k=0.8)       # neck
        bell = s.poly([(CX - 11, 228), (CX + 11, 228), (CX + 17, 234), (CX + 23, 240), (CX + 26, 246), (CX - 26, 246), (CX - 23, 240), (CX - 17, 234)])
        s.plate(bell, GREY, z=2.8, bevel=2.0, dome=0.9, inset=0.0, shadow_k=0.8)
        for k in range(-4, 5):                                                              # cooling ribs down the bell
            x0, x1 = CX + k*2.2, CX + k*5.4
            for t in np.linspace(0, 1, 50):
                s.rgb[s.disk(x0 + (x1 - x0)*t, 229.5 + 15.5*t, 0.32) & bell] = GREY_D*0.8
        s.plate(s.rrect(CX - 27, 245, CX + 27, 248.6, 1.6), ORG, z=3.0, bevel=1.0, dome=0.3, shadow_k=0.8)                # orange lip
        for i, y in enumerate((218, 222, 226)):                                             # ribbed collar
            rib = s.rrect(CX - 23, y - 1.8, CX + 23, y + 1.8, 1.6)
            s.plate(rib, GREY*(1.08 if i % 2 == 0 else 0.92), z=3.3, bevel=1.0, dome=0.4, shadow_k=0.8)
            for k in range(-5, 6): s.rgb[rib & (np.abs(xx_ - (CX + 22*np.sin(k*np.pi/12))) < 0.5)] = GREY_D*0.7
        sysl('main drive: grey ribbed collar + cooled bell nozzle, orange lip', CX, 236)
    # ================================================================ side thruster pods on swivel hubs + pylons (at rest)
    for g in (-1, 1):
        px = X(g, CX - PODX); hx = X(g, CX - HUBX)
        with P('hull'):
            s.plate(s.rrect(min(hx, X(g, CX - BX0 - 3)), 184, max(hx, X(g, CX - BX0 - 3)), 200, 1.5), AR, z=2.0, bevel=1.2, inset=0.5, shadow_k=0.8)   # pylon
        with P('pod'):
            hub = s.disk(hx, PODY, 4.6)
            s.plate(hub, GREY*1.25, z=2.4, bevel=1.4, dome=0.5, shadow_k=0.8, paint=[(hub & (np.hypot(xx_ - hx, yy_ - PODY) > 3.5), ORG)])
            s.rgb[s.disk(hx, PODY, 1.2)] = GREY_D
            can = s.poly([(px - 8.6, 202), (px + 8.6, 202), (px + 7.6, 211), (px - 7.6, 211)])
            s.plate(can, GREY, z=2.4, bevel=1.4, dome=0.6, shadow_k=0.8)
            s.plate(s.rrect(px - 8.6, 210, px + 8.6, 212.4, 1.0), ORG, z=2.5, bevel=0.8, shadow_k=0.8)
            pm = pod_mask(px)
            s.plate(pm, AR*1.04, z=2.8, bevel=6.0, dome=2.4, inset=1.0, shadow_k=0.9, paint=[(pm & (yy_ < 175) & (np.abs(xx_ - px) < 3.2), AR_L)])
            for yb in (180, 190):                                                           # orange hoops round the nacelle
                band = s.rrect(px - 11.6, yb - 1.6, px + 11.6, yb + 1.6, 1.0) & s.rrect(px - 11.6, 170, px + 11.6, 205, 9)
                s.plate(band, ORG*1.1, z=2.9, bevel=0.8, dome=0.3, outline=0.4, shadow_k=0.8)
            s.rgb[pm & (np.abs(xx_ - px) < 0.45) & (yy_ > 182) & (yy_ < 188)] = SEAM
    sysl('2 side thruster pods on swivel hubs + pylons: forward thrust, vector for strafe, differential turns', PODX, 192)
    with P('hull'):
        # ================================================================ dome: shell, stepped latitude rows, orange livery ring, meridian seams
        s.plate(dome, AR_D, z=1.2, bevel=3.0, dome=1.6, inset=2.0, shadow_k=0.9)
        rows = ((0.94, 1.01, AR*0.9, 1.6), (0.814, 0.94, AR*0.98, 2.6), (0.667, 0.814, AR*1.05, 3.8), (-1, 0.667, AR*1.13, 4.9))
        for (r0, r1, col, z) in rows:
            band = dome & (rb > r0) & (rb < r1)
            s.plate(band, col, z=z, bevel=2.0 if r0 > 0 else 5.0, dome=0.8 if r0 > 0 else 3.0, outline=0.6, inset=0.8, shadow_k=0.9)
        liv = dome & (np.abs(rb - 0.826) < 0.022)
        s.plate(liv, ORG, z=3.9, bevel=0.8, dome=0.3, outline=0.4, shadow_k=0.8)                          # orange livery ring
        for a_ in (-120, -150, 180, 150, 120):                                              # meridian seams (none on the centreline)
            seam = dome & (np.abs(((ab - a_ + 180) % 360) - 180) < 0.55/np.maximum(rb, 0.3)) & (rb > 0.41) & (rb < 0.985) & ~liv
            s.rgb[seam] = SEAM
        cz = np.sqrt(np.clip(1 - rb**2, 0, 1)); lam = (-0.78*v_ + 0.62*cz)/np.sqrt(u_**2 + v_**2 + cz**2 + 1e-6)   # sphere shading across the rows
        s.rgb[dome] *= np.clip(0.7 + 0.5*lam, 0.6, 1.2)[dome][:, None]
        sysl('dome: stepped latitude rows, meridian seams, orange livery ring', X(-1, 44), 72)

        # ================================================================ rear box (drawn over the dome's aft skirt; the crown stands above it)
        bx = box & ~inner
        s.plate(bx, AR, z=4.0, bevel=4.0, dome=0.8, inset=2.0, shadow_k=0.95)
        trim = s.rrect(48, 147, W - 48, 209, 3) & ~inner
        s.plate(trim, ORG, z=4.3, bevel=0.8, shadow_k=0.8)
        top = s.rrect(50, 149, W - 50, 207, 2.5) & ~inner
        s.plate(top, AR_L, z=4.5, bevel=1.4, dome=0.2, inset=0.9, shadow_k=0.9)
        s.bolt_row(top, 1.6, 5)
        for g in (-1, 1):                                                                   # jade side panels on the flanks (EL green)
            jp = s.rrect(min(X(g, CX - BX0 - 0.6), X(g, CX - BX0 - 5.4)), 151, max(X(g, CX - BX0 - 0.6), X(g, CX - BX0 - 5.4)), 205, 1.2)
            s.plate(jp, JADE, z=4.1, bevel=1.0, tilt=(g*0.35, 0), inset=0.0, shadow_k=0.85)
            for k in range(5): s.rgb[jp & (np.abs(yy_ - (156 + k*11)) < 0.5)] = (24, 60, 46)
            for k in range(4): s.rgb[s.rrect(X(g, 52) - 0.8, 162 + k*11, X(g, 52) + 0.8, 165 + k*11, 0.3)] = (255, 214, 150)   # crew lights
        sysl('rear box: top plate + orange trim, jade side panels (EL green)', X(1, 56), 178)

        # ================================================================ dome small ballistic x3, terraced down the centreline (sunk, orange lips)
        for (px, py, z) in TOPS:
            VP.sunk_mount(s, px, py, 5.6, (0, -1), metal=AR_D, lip_metal=AR_L, z=z, lip_z=z + 0.7, accent=ORG)
        sysl('3 small ballistic terraced down the dome, superfiring, 120 deg forward', CX, 80)

        # ================================================================ 2 small ballistic PD near the box's rear corners, facing aft (lip on the aft side)
        for (px, py) in PD:
            VP.sunk_mount(s, px, py, 4.8, (0, 1), metal=AR_D, lip_metal=AR_L, z=4.4, lip_z=5.0, accent=ORG)
        sysl('2 small ballistic PD on the rear box, facing aft, 180 deg', PD[0][0], PD[0][1])

        # ================================================================ COMMAND TOWER (long, 3 tiers): jade band, jade visor glass, vents, fire-control dome
        c0 = tier(20.6, 149.4, 210.6, 9)
        s.plate(c0, JADE, z=5.0, bevel=1.2, shadow_k=0.95)
        c1 = tier(19.0, 151, 209, 8)
        s.plate(c1, AR, z=5.4, bevel=2.6, dome=0.9, inset=1.8, shadow_k=0.95)
        s.bolt_row(c1, 1.6, 5)
        c2 = tier(14.6, 155.6, 206, 6)
        s.plate(c2, AR_L, z=6.4, bevel=2.2, dome=1.0, ridge=('x', CX, 1.2, 14), inset=1.4, shadow_k=0.95)
        glass = tier(12.2, 156.2, 161.4, 2.4) & c2
        gy = np.clip((yy_ - 156.2)/5.2, 0, 1); s.rgb[glass] = np.clip(GLS*(1.12 - 0.5*gy[..., None]), 0, 255)[glass]
        for k_ in (-8, -4, 0, 4, 8): s.rgb[glass & (np.abs(xx_ - (CX + k_)) < 0.35)] = (20, 70, 52)
        c3 = tier(9.4, 166.6, 201.4, 5)
        s.plate(c3, AR_L*1.04, z=7.3, bevel=1.8, dome=1.0, inset=1.1, shadow_k=0.95)
        for g in (-1, 1):
            for k in range(4): s.rgb[s.rrect(min(X(g, 3.4), X(g, 8.0)), 189.6 + k*3, max(X(g, 3.4), X(g, 8.0)), 190.6 + k*3, 0.3)] = SEAM   # vents
        s.plate(s.disk(CX, 176, 4.4), AR_L, z=7.8, bevel=1.3, dome=1.0, inset=0.5, shadow_k=0.95)               # fire-control dome
        s.rgb[s.disk(CX, 175.4, 1.5)] = (40, 120, 92)
        sysl('command tower (3 tiers, long): jade visor glass, vents, fire-control dome', CX, 158)
    # ================================================================ symmetry + lights
    _h = CX*s.SS
    s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
    with P('hull'):
        s.lights([(X(-1, DRX - 1.5), DCY), (X(1, DRX - 1.5), DCY), (CX, 216)], [(255, 70, 60), (90, 255, 120), (255, 255, 240)])
    return s


if __name__ == '__main__':
    OUT = _ROOT + '/ss_style/garm_ss_v4_'
    snap = lambda s: (s.rgb.copy(), s.a.copy(), s.z.copy())
    sF = build(PARTS); full_snap = snap(sF); zmax = float((sF.z*sF.a).max()); full_ref = sF.render()   # whole ship in one pass (== v3)
    sH = build({'hull'}); hs = snap(sH)
    hull_im = SL.lit_part(sH, hs, hs, zmax)                                      # hull lit on its own (pods swing, no baked pod shadow)
    sM = build({'pod'}); pair = SL.lit_part(sM, snap(sM), full_snap, zmax)     # both pods, lit within the full ship
    pair = SL.add_shadow_fringe(pair, full_ref, hull_im)                          # shadow each pod casts on the pylons/hull
    L, R = SL.split_lr(pair, CX)
    comp = SL.over(hull_im, L, R)
    hull_im.save(OUT + 'hull.png'); L.save(OUT + 'podL.png'); R.save(OUT + 'podR.png'); comp.save(OUT + 'full.png')
    v3 = json.load(open(_ROOT + '/ss_style/garm_ss_v3_slots.json'))
    v3.update(pivot_L=[float(PIVL[0]), float(PIVL[1])], pivot_R=[float(2*CX - PIVL[0]), float(PIVL[1])],
              parts=dict(order=['hull', 'podL', 'podR']))
    json.dump(v3, open(OUT + 'slots.json', 'w'))
    json.dump(SYSTEMS, open(_ROOT + '/ss_style/garm_v4_systems.json', 'w'))
    from PIL import Image
    v3im = Image.open(_ROOT + '/ss_style/garm_ss_v3.png')
    print('one-pass full vs v3 :', SL.diff_stats(full_ref, v3im))
    print('composite vs v3     :', SL.diff_stats(comp, v3im))
    print('pivots', v3['pivot_L'], v3['pivot_R'], 'ENG', v3['ENG'])
