import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Abaddon - Starsector style v8 = v7 drawing split into separately rendered PARTS on the same 300x560 canvas
(DESIGN 'Abaddon 3D v3/v4': the side boosters retract 24 px outward on slide rails at torpedo launch).
  hull              : everything fixed - front frame (hex pads, fighter cockpit, core cover, frame-corner PD), the 3 I-beam
                      slide rails per side (fixed under the frame, end stops outboard) + nav lights; lit alone; the shadow the
                      frame/rails cast onto the boosters (at rest) is a soft black semi-transparent fringe in this sprite
  boosterL/boosterR : each side booster alone - body, belt, grilles, box thruster, diagonal jet, docking clamps, retro housing
                      + 3 nozzles, and the rail CARRIAGES (new: hidden under the frame at rest, peek out when retracted); lit alone
Stack (bottom -> top): boosterL, boosterR, hull  (the frame + rails are ABOVE the boosters).
Outputs ss_style/abaddon_ss_v8_{hull,boosterL,boosterR,full,open,hull_noshadow,shadow_rest,shadow_open}.png + abaddon_ss_v8_slots.json (v7 json + parts/retro/retract_px).
The Apocalypse torpedo stays apocalypse_ss_v2.png (not re-rendered here)."""
import json, numpy as np
from scipy import ndimage as ndi
from PIL import Image
import vstyle, vparts as VP
from vstyle import Ship, spline
import splitlib as SL

W, H, CX = 300, 560, 150
MEN = [(98, 256), (202, 256)]
PD = [(CX + g*110, py) for g in (-1, 1) for py in (230, 318)]
RAILS = (201, 266, 330)
CLAMPS = (176, 384)
ENG = [(67, 432), (233, 432)]
RETRACT = 24
FX = 70                                       # retro housing centre x (left)
RETRO = [[FX - 11, 126.0], [FX, 126.5], [FX + 11, 126.0]]          # nozzle exits (upper L, lower, upper R), left booster at rest

ARM = np.array([127, 134, 118]); ARM_L = np.array([169, 176, 156]); ARM_D = np.array([85, 91, 78]); DARK = np.array([28, 31, 26])
GRN = np.array([79, 224, 122]); GRN_D = np.array([42, 138, 74]); BRZ = np.array([201, 143, 58])
HAZ = np.array([255, 208, 64]); GLS = np.array([125, 255, 154]); GLOW = np.array([234, 255, 234])
SEAM = (44, 48, 40)
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))
SMALL = []
PARTS = ('hull', 'boost')
X = lambda g, dx: CX + g*dx

# ---------------------------------------------------------------- local helpers (as v7)
def rpoly(s, pts, r):
    m = s.poly(pts)
    inner = ndi.distance_transform_edt(m)/s.SS > r
    return ndi.distance_transform_edt(~inner)/s.SS <= r

def solid(s, mask, color, h, z=None, outline=0.9, spec=0.3, gain=1.5, paint=(), shadow_k=0.8, cast=True, tex=0.015):
    if not mask.any(): return mask
    if cast: s.shadow(mask, strength=shadow_k)
    shade, sp, nl = s._shade(np.where(mask, h, 0).astype(np.float32), gain, spec)
    col = np.empty((s.h, s.w, 3), np.float32); col[:] = color
    for pm, pc in paint: col[pm & mask] = pc
    c = col*(shade*(1 + tex*s.mottle + 0.015*s.fine))[..., None] + 255*sp[..., None]
    d = ndi.distance_transform_edt(mask)/s.SS
    rim = mask & (d > outline) & (d < outline + 0.9) & (nl > vstyle.LIGHT[2] + 0.05)
    c[rim] = np.minimum(c[rim]*1.25 + 10, 255)
    e = mask & (d <= outline); c[e] *= 0.3
    s.rgb[mask] = np.clip(c[mask], 0, 255); s.a |= mask
    if z is not None: s.z[mask] = z
    return mask

def tube_v(s, cx, y0, y1, hw0, hw1, color, z, k=0.5, **kw):
    yy_ = s.yy/s.SS; xx_ = s.xx/s.SS
    hw = hw0 + (hw1 - hw0)*np.clip((yy_ - y0)/max(1e-6, y1 - y0), 0, 1)
    m = (np.abs(xx_ - cx) <= hw) & (yy_ >= y0) & (yy_ <= y1)
    h = k*np.sqrt(np.clip(hw**2 - (xx_ - cx)**2, 0, None))
    return solid(s, m, color, h, z=z, **kw)

def slats(s, x0, x1, y0, y1, first, step, th, z):
    yy_ = s.yy/s.SS
    well = s.rrect(x0, y0, x1, y1, 1.2)
    s.plate(well, DARK*1.3, z=z - 0.25, bevel=0.8, inset=0.0, shadow_k=0.9, outline=0.6)
    for py in np.arange(first, y1 - 2.0, step):
        sl = s.rrect(x0 + 2, py - th/2, x1 - 2, py + th/2, 0.5)
        s.plate(sl, GRN*0.95, z=z - 0.1, bevel=0.7, dome=0.2, shadow_k=0.7, outline=0.45, tex=0.0, gain=1.2)
        s.rgb[sl & (np.abs(yy_ - (py - th/2 + 0.55)) < 0.3)] = np.minimum(GRN*1.25 + 30, 255)

def mirror(s):
    _h = CX*s.SS
    s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]


def build(active, shift=0):
    """draw the ship with only the `active` parts kept; returns the Ship before its depth pass.
    shift > 0: the (left, pre-mirror) booster is moved `shift` px outward before the hull is drawn (one-pass OPEN reference)."""
    SYSTEMS.clear(); SMALL.clear()
    _L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = CX
    s = Ship(W, H, seed=171)
    P = SL.SplitCtx(s, active)
    s.auto_z = True; s.depth = dict(unit=6.0, s_str=0.85, tint=0.36, ao=0.55, ao_r=5, sdir=((0.6, 0.8), (-0.6, 0.8)), s_soft=0.9)
    _plate0, _bolt0 = s.plate, s.bolt_row
    def _plate(mask, color, *a, **k):
        k.setdefault('tex', 0.018); k.setdefault('grime', 0.0); k.setdefault('notch', 0); return _plate0(mask, color, *a, **k)
    def _bolt(m, inset=1.8, spacing=4.0, seed=0):
        if m is not None and m.sum()/s.SS**2 > 700: _bolt0(m, inset, spacing*2.4)
    s.plate, s.bolt_row = _plate, _bolt
    yy_ = s.yy/s.SS; xx_ = s.xx/s.SS; ax_ = np.abs(xx_ - CX)
    A, B = 40, 94
    BOOST = [(B, 140), (A + 13, 140), (A, 170), (A, 400), (A + 8, 430), (B, 430)]
    FR = [(62, 195), (238, 195), (260, 214), (260, 318), (244, 335), (56, 335), (40, 318), (40, 214)]
    bm = rpoly(s, BOOST, 3.0)
    frm = rpoly(s, FR, 3.0)

    # ---------------------------------------------------------------- machinery base (fully covered by plates; split by footprint)
    s.guts(bm | frm, seed=173, tone=(50, 54, 46), minc=3, maxc=10); s.z[:] = 0
    keep = np.zeros_like(s.a)
    if P.on('boost'): keep |= bm
    if P.on('hull'): keep |= frm & ~bm
    s.a &= keep

    with P('boost'):
        # ------------------------------------------------------------ rear: box thruster + diagonal jet
        ex = 67
        s.plate(s.rrect(ex - 22, 426, ex + 22, 439, 2.0), ARM_D, z=1.9, bevel=1.6, dome=0.3, inset=1.0, shadow_k=0.9)
        for k in (-1, 0, 1):
            s.plate(s.rrect(ex + k*12 - 1.6, 431, ex + k*12 + 1.6, 438, 0.6), ARM, z=2.0, bevel=0.6, shadow_k=0.8, outline=0.5)
        s.plate(s.rrect(ex - 17.5, 435.5, ex + 17.5, 441.6, 1.0), DARK*1.6, z=1.6, bevel=0.8, shadow_k=0.8)
        s.rgb[s.rrect(ex - 15, 440.3, ex + 15, 441.8, 0.4)] = GLOW
        s.rgb[s.rrect(ex - 15, 439.6, ex + 15, 440.3, 0.2)] = GRN*0.9
        e = np.array([A + 2.0, 421.0]); n_ = np.array([-0.7071, 0.7071])
        VP.diag_jet(s, -1, *(e + n_*2.0), 11, T=34, metal=tuple(ARM_L*0.95), z=0.8)
        for gg in (-1, 1):
            ex_ = np.array([X(gg, CX - A - 2.0), 421.0]) + np.array([gg*0.7071, 0.7071])*14
            SMALL.append((float(ex_[0]), float(ex_[1]), 135 if gg < 0 else -135))
        sysl('box thrusters at the booster rears (2 main engines) + small diagonal jets on the rear outer corners', ex, 436)

        # ------------------------------------------------------------ front: retro housing + 3 small nozzles
        fx = FX
        tube_v(s, fx, 126.5, 134.5, 5.2, 4.3, ARM*0.8, 0.8, k=0.55, shadow_k=0.6)
        s.plate(s.rrect(fx - 21, 133.2, fx + 21, 140.8, 1.6), ARM_L, z=1.7, bevel=1.2, dome=0.3, inset=0.8, shadow_k=0.9)
        for k in range(5): s.rgb[s.rrect(fx - 17 + k*2.2, 136.2, fx - 16 + k*2.2, 138.4, 0.2)] = SEAM if k % 2 else HAZ*0.8
        for dx in (-11, 11):
            tube_v(s, fx + dx, 126.0, 134.5, 5.4, 4.4, ARM, 1.4, k=0.55, shadow_k=0.7)
            s.rgb[s.rrect(fx + dx - 5.3, 126.0, fx + dx + 5.3, 127.3, 0.5)] = BRZ
            s.rgb[s.rrect(fx + dx - 5.0, 132.6, fx + dx + 5.0, 133.4, 0.3)] = ARM_L*1.1
        sysl('retro housing on each booster front: 3 small nozzles fire forward to halt the ship at launch', fx, 130)

        # ------------------------------------------------------------ booster body
        belt = s.rrect(A - 3.2, 165, A + 2, 405, 1.2)
        s.plate(belt, ARM_L*0.92, z=1.1, bevel=1.0, dome=0.2, shadow_k=0.9)
        for py in range(180, 400, 30): s.rgb[belt & (np.abs(yy_ - py) < 0.6)] = SEAM
        s.plate(bm, ARM_D, z=2.4, bevel=2.6, dome=0.4, inset=1.6, shadow_k=0.95)
        inner = ndi.distance_transform_edt(bm)/s.SS > 3.0
        for (y0, y1, col) in [(143, 196, ARM), (198, 333, ARM_L*0.96), (336, 398, ARM), (400, 428, ARM*1.04)]:
            pm = inner & (yy_ > y0) & (yy_ < y1)
            s.plate(pm, col, z=2.6, bevel=1.6, dome=0.3, inset=1.2, shadow_k=0.9)
            s.bolt_row(pm, 1.6, 5)
        slats(s, A + 7, B - 7, 149, 191, 153.5, 6, 3.0, 2.6)
        slats(s, A + 7, B - 7, 339, 397, 343.5, 6, 3.0, 2.6)
        s.rgb[bm & (np.abs(xx_ - (B - 1.2)) < 0.5) & (yy_ > 143) & (yy_ < 428)] = BRZ*0.85
        sysl('side boosters: EL-green radiator grilles fore + aft, outer armour belt (retract 24 px on their rails at launch)', 67, 170)

        # ------------------------------------------------------------ docking clamps
        for py in CLAMPS:
            s.plate(s.rrect(B - 3, py - 8, B + 3, py + 8, 1.0), ARM_D, z=2.0, bevel=0.8, shadow_k=0.9)
            jaw = s.poly(spline([(B - 1, py - 5), (B + 8, py - 4.2), (B + 11, py - 1.5), (B + 11, py + 1.5), (B + 8, py + 4.2), (B - 1, py + 5)], 6, True))
            s.plate(jaw, BRZ, z=2.3, bevel=1.0, dome=0.3, tilt=(0.25, 0), shadow_k=0.9, outline=0.6)
            s.rgb[s.rrect(B + 8.6, py - 2.2, B + 10.4, py + 2.2, 0.4)] = DARK*1.8
        sysl('docking clamps (bronze jaws) on the booster inner walls', B + 6, 176)

        # ------------------------------------------------------------ NEW: rail carriages (3D: 14 x 8 at CX-83; hidden under the frame at rest)
        st = s.rng.bit_generator.state                     # keep the rng stream = v7 (hull plates keep their jitter)
        for py in RAILS:
            cm = s.rrect(60, py - 4, 74, py + 4, 1.0)
            s.plate(cm, ARM_D*0.95, z=2.95, bevel=0.9, dome=0.2, shadow_k=0.9, outline=0.5)
            s.rgb[cm & (np.abs(yy_ - (py + 3.0)) < 0.35)] = BRZ*0.8                      # bronze skid edge
            for bx in (62.2, 71.8): s.rgb[s.disk(bx, py - 2.6, 0.55) | s.disk(bx, py + 2.2, 0.55)] = SEAM
        s.rng.bit_generator.state = st

    if shift:                                               # move what is drawn so far (left booster) outward
        d = int(round(shift*s.SS))
        for arr in (s.rgb, s.a, s.z):
            arr[:, :-d] = arr[:, d:].copy(); arr[:, -d:] = 0
    with P('hull'):
        # ------------------------------------------------------------ slide rails (fixed under the frame, stick out past it)
        for py in RAILS:
            r_ = s.rrect(24, py - 2.5, 102, py + 2.5, 0.8)
            s.plate(r_, ARM_L, z=3.2, bevel=0.9, shadow_k=0.95, outline=0.5)
            s.rgb[s.rrect(25, py - 0.9, 101, py + 0.9, 0.3)] = BRZ
            s.rgb[r_ & (np.abs(yy_ - (py - 1.6)) < 0.3)] = SEAM
            s.plate(s.rrect(22.6, py - 3.3, 25.6, py + 3.3, 0.6), ARM_D, z=3.4, bevel=0.7, shadow_k=0.9, outline=0.5)
        sysl('3 I-beam slide rails per side (booster retraction), end stops outboard', 30, 266)

        # ------------------------------------------------------------ FRONT FRAME
        s.plate(frm, ARM, z=4.9, bevel=3.2, dome=0.6, inset=2.2, shadow_k=0.95)
        brow = rpoly(s, [(70, 199), (230, 199), (250, 216), (250, 226), (50, 226), (50, 216)], 1.5)
        s.plate(brow, ARM_L, z=5.15, bevel=1.6, dome=0.3, tilt=(0, -0.04), inset=1.0, shadow_k=0.95)
        rear = rpoly(s, [(52, 312), (248, 312), (240, 329), (60, 329)], 1.5)
        s.plate(rear, ARM_L, z=5.15, bevel=1.6, dome=0.3, inset=1.0, shadow_k=0.95)
        for (m_, y0) in ((brow, 212), (rear, 320)):
            for xs in (74, 118): s.rgb[m_ & (np.abs(xx_ - xs) < 0.5) & (yy_ > y0 - 11)] = SEAM
        s.rgb[s.rrect(45.3, 210, 46.7, 322, 0.5)] = BRZ
        for py in (286, 292, 298):
            s.plate(s.rrect(65, py - 0.9, 75, py + 0.9, 0.5), DARK*1.2, z=4.8, bevel=0.4, shadow_k=0.5, outline=0.3)
        for py in (242, 270):
            s.rgb[frm & (np.abs(yy_ - py) < 0.45) & (xx_ > 48) & (xx_ < 78)] = SEAM
        s.bolt_row(s.rrect(49, 230, 78, 308, 2), 1.4, 5)
        sysl('front frame: armoured bridge over the torpedo gap, brow + rear plates, bronze trim, vents', 60, 256)

        for (mx, my) in MEN[:1]:
            hexm = s.poly([(mx + 20*np.cos(np.radians(90 + 60*k)), my + 20*np.sin(np.radians(90 + 60*k))) for k in range(6)])
            s.plate(hexm, ARM_L, z=5.1, bevel=1.8, dome=0.3, inset=1.2, shadow_k=0.95)
            rr = np.hypot(xx_ - mx, yy_ - my)
            s.plate(s.disk(mx, my, 15.2) & (rr > 11.8), BRZ, z=5.35, bevel=1.1, dome=0.5, shadow_k=0.9, outline=0.6)
            s.mount(mx, my, 12, ARM_D, well_col=(46, 50, 44)); s.z[rr < 12] = 5.0
        sysl('2 medium energy on hex pads (bronze rings), 270 deg', 98, 256)

        for (px, py) in PD[:2]:
            VP.sunk_mount(s, px, py, 5.4, (-1, 0), metal=ARM_D, lip_metal=ARM_L, z=4.8, lip_z=5.5, accent=BRZ)
        sysl('4 small ballistic PD sunk in the frame corners, 180 deg to their side', 40, 230)

        # ------------------------------------------------------------ FIGHTER COCKPIT
        FUY, FUA, FUB = 252, 26, 88
        u_ = (xx_ - CX)/FUA; v_ = (yy_ - FUY)/FUB; q_ = 1 - u_**2 - v_**2
        fus = q_ >= 0
        stripe = fus & (np.abs(ax_ - 22.5) < 0.55) & (yy_ > 197) & (yy_ < 327) & (q_ > 0.03)
        solid(s, fus, ARM_L, 9.0*np.sqrt(np.clip(q_, 0, None)), z=5.9, gain=1.6, paint=[(stripe, GRN)], shadow_k=0.95)
        for py in (190, 290, 318): s.rgb[fus & (np.abs(yy_ - py) < 0.45) & (ax_ < 26*np.sqrt(np.clip(1 - ((py - FUY)/FUB)**2, 0, 1)) - 2.5) & (ax_ > 9.5)] = ARM*0.75
        s.plate(s.rrect(CX - 0.7, 127, CX + 0.7, 145, 0.5), ARM_D, z=6.0, bevel=0.5, shadow_k=0.7, outline=0.3)
        cr = 12*np.clip((yy_ - 142)/36, 0, 1)
        cone = (ax_ <= cr) & (yy_ >= 142) & (yy_ <= 178.5)
        solid(s, cone, ARM, 0.75*np.sqrt(np.clip(cr**2 - (xx_ - CX)**2, 0, None)), z=6.1, gain=1.6, shadow_k=0.95)
        s.rgb[cone & (yy_ > 177.3)] = ARM_D*0.8
        for gg in (-1, 1):
            ix = X(gg, 25.5)
            s.plate(s.rrect(ix - 4, 238, ix + 4, 270, 1.6), ARM*0.78, z=6.0, bevel=1.2, dome=0.3, tilt=(-gg*0.15, 0), shadow_k=0.95)
            s.rgb[s.rrect(ix - 3, 239.4, ix + 3, 241.6, 0.5)] = DARK
            s.plate(s.rrect(ix - 4.5, 236.8, ix + 4.5, 239.3, 0.8), ARM_L, z=6.15, bevel=0.6, shadow_k=0.8, outline=0.5)
        cu = (xx_ - CX)/15; cv = (yy_ - 220)/36; cq = 1 - cu**2 - cv**2
        can = cq >= 0
        hoops = can & ((np.abs(yy_ - 208.5) < 0.6) | (np.abs(yy_ - 226.9) < 0.6))
        gl = np.clip(0.55 + 0.65*np.sqrt(np.clip(cq, 0, 1)) - 0.25*np.clip(cv, 0, 1), 0, 1.3)
        solid(s, can, GLS*0.72, 8.0*np.sqrt(np.clip(cq, 0, None)), z=6.8, gain=1.9, spec=0.6, shadow_k=0.95, paint=[(hoops, ARM_D)])
        s.rgb[can & ~hoops] = np.clip(s.rgb[can & ~hoops]*gl[can & ~hoops][:, None], 0, 255)
        glint = can & (((xx_ - CX)/3.2)**2 + ((yy_ - 199)/7.5)**2 < 1)
        s.rgb[glint] = np.minimum(s.rgb[glint]*0.55 + 110, 255)
        for gg in (-1, 1):
            s.plate(s.rrect(X(gg, 15.4) - 0.8, 186, X(gg, 15.4) + 0.8, 258, 0.6), ARM_D, z=6.85, bevel=0.5, shadow_k=0.8, outline=0.3)
            s.plate(s.rrect(X(gg, 12) - 2, 278, X(gg, 12) + 2, 318, 0.8), ARM, z=6.25, bevel=0.8, shadow_k=0.9, outline=0.5)
        spine = s.rrect(CX - 9, 259, CX + 9, 337, 3)
        s.plate(spine, ARM, z=6.3, bevel=1.6, dome=0.4, ridge=('x', CX, 0.8, 9), inset=1.0, shadow_k=0.95)
        for py in (266, 272): s.rgb[spine & (np.abs(yy_ - py) < 0.45)] = SEAM
        VP.core_armour(s, CX, 302, 10.5, glow=tuple(GRN), metal=ARM_L*0.84, z=6.5)
        sysl('jet-style fighter cockpit: nose cone + pitot, green bubble canopy, intakes, livery stripes, dorsal spine', CX, 220)
        sysl('drive core under an armoured petal hatch on the cockpit spine', CX, 302)

    mirror(s)
    with P('hull'):
        s.lights([(X(-1, 91), 204), (X(1, 91), 204), (CX, 127)], [(255, 70, 60), (90, 255, 120), (255, 255, 240)])
    return s


def shift_im(im, dx):
    A = np.asarray(im); B = np.zeros_like(A)
    if dx < 0: B[:, :dx] = A[:, -dx:]
    else: B[:, dx:] = A[:, :A.shape[1] - dx]
    return Image.fromarray(B, 'RGBA')


if __name__ == '__main__':
    D = _ROOT + '/ss_style/'; OUT = D + 'abaddon_ss_v8_'
    snap = lambda s: (s.rgb.copy(), s.a.copy(), s.z.copy())
    sF = build(PARTS); zmax = float((sF.z*sF.a).max()); full_ref = sF.render()          # one pass, boosters at rest (== v7)
    sO = build(PARTS, shift=RETRACT); open_ref = sO.render()                           # one pass, boosters retracted (reference)
    sH = build({'hull'}); hs = snap(sH); hull0 = SL.lit_part(sH, hs, hs, zmax)          # hull lit alone
    sB = build({'boost'}); bs = snap(sB); pair = SL.lit_part(sB, bs, bs, zmax)          # boosters lit alone (lowest layer)
    L, R = SL.split_lr(pair, CX)
    hull_im = SL.add_shadow_fringe(hull0, full_ref, pair, reach=18)                     # frame/rail shadow on the boosters at rest
    comp = SL.over(L, R, hull_im)
    Lo, Ro = shift_im(L, -RETRACT), shift_im(R, RETRACT)
    hull_open = SL.add_shadow_fringe(hull0, open_ref, SL.over(Lo, Ro), reach=18)      # frame/rail/PD shadow on the RETRACTED boosters
    fringe = lambda im: Image.fromarray(np.where((np.asarray(hull0)[..., 3:] > 0), 0, np.asarray(im)).astype(np.uint8), 'RGBA')
    opn = SL.over(Lo, Ro, hull_open)
    naive = SL.over(Lo, Ro, hull_im)                                                  # hull.png as-is over shifted boosters
    hull_im.save(OUT + 'hull.png'); L.save(OUT + 'boosterL.png'); R.save(OUT + 'boosterR.png')
    hull0.save(OUT + 'hull_noshadow.png'); fringe(hull_im).save(OUT + 'shadow_rest.png'); fringe(hull_open).save(OUT + 'shadow_open.png')
    comp.save(OUT + 'full.png'); opn.save(OUT + 'open.png')
    naive.save(_ROOT + '/_scratch/abaddon_open_naive.png')

    v7 = json.load(open(D + 'abaddon_ss_v7_slots.json'))
    retro = [[float(X(g, CX - x)), y] for g in (-1, 1) for (x, y) in RETRO]
    v7.update(parts=dict(order=['boosterL', 'boosterR', 'hull'],
                         note='bottom -> top; the hull (front frame + slide rails) is ABOVE both boosters',
                         shadow=dict(base='abaddon_ss_v8_hull_noshadow.png', rest='abaddon_ss_v8_shadow_rest.png', open='abaddon_ss_v8_shadow_open.png',
                                     note='hull.png = hull_noshadow + shadow_rest; for exact shadows while retracting, draw hull_noshadow and crossfade shadow_rest -> shadow_open with the retraction'),
                         moving=dict(boosterL=dict(dx=-RETRACT, carries=dict(ENG=[0], small=[0], retro=[0, 1, 2])),
                                     boosterR=dict(dx=RETRACT, carries=dict(ENG=[1], small=[1], retro=[3, 4, 5])))),
              retro=retro, retract_px=RETRACT)
    json.dump(v7, open(OUT + 'slots.json', 'w'))
    json.dump(SYSTEMS, open(D + 'abaddon_v8_systems.json', 'w'))

    v7im = Image.open(D + 'abaddon_ss_v7.png')
    print('one-pass full vs v7 :', SL.diff_stats(full_ref, v7im))
    print('composite vs v7     :', SL.diff_stats(comp, v7im))
    print('open comp vs open 1-pass ref:', SL.diff_stats(opn, open_ref))
    print('naive open (hull.png) vs ref:', SL.diff_stats(naive, open_ref))
    print('hull_noshadow+shadow_rest == hull.png:', SL.diff_stats(SL.over(hull0, fringe(hull_im)), hull_im)['max'])
    open_ref.save(_ROOT + '/_scratch/abaddon_open_ref.png')
    print('retro', retro)
    print('bbox L', SL.bbox(L), 'R', SL.bbox(R), 'hull', SL.bbox(hull_im))
