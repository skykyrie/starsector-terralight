import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Fenrir - Starsector style v4 = v3 drawing, split into separately rendered PARTS on the same 190x236 canvas:
  hull     : everything fixed, incl. the two fixed booster pylons (their hub end plate stays)
  boosterL / boosterR : each side booster that swivels (lathe nacelle + flush orange rings, aft nozzle + lip, swivel hub disk),
             lit within the full ship, plus the soft shadow it casts on its pylon (black semi-transparent fringe)
Outputs ss_style/fenrir_ss_v4_{hull,boosterL,boosterR,full}.png + fenrir_ss_v4_slots.json (v3 slots + pivot_L/pivot_R).
Composite order (bottom -> top): hull, boosterL, boosterR."""
import json, numpy as np
from scipy import ndimage as ndi
import vstyle, vparts as VP
from vstyle import Ship, spline

W, H, CX = 190, 236, 95
BX, BY, BZ, BCZ, FF, ZC = 56.0, 62.0, 70.0, 120.0, 0.8, 0.94          # bulb (same numbers as the 3D)
HP = (CX, 28)                                                          # nose hardpoint (gimbal ball centre)
GUN_Y = 84
def zz(py): return np.minimum(ZC, (np.asarray(py, np.float64) - BCZ)/BZ)
def ffz(z): return FF + (1 - FF)*np.minimum(1, (z + 1)*0.9)
def hwB(py):
    z = zz(py); return BX*np.sqrt(np.clip(1 - z*z, 0, 1))*ffz(z)
def hB(py):
    z = zz(py); return BY*np.sqrt(np.clip(1 - z*z, 0, 1))
HX = float(hwB(GUN_Y))                                                 # hull half-width at the side guns (42.6)
SG = [(CX - (HX + 21), GUN_Y), (CX + (HX + 21), GUN_Y)]                # side-gun pivots (31.4 / 158.6, 84)
TOP = (CX, 118)
PD = [(CX - 30, 162), (CX + 30, 162)]
ENG = [(CX, 214)]
NAC_X = 19; NAC_Y0 = 156; PIV = (CX - 57, 184)                        # left booster nacelle axis, swivel hub
NAC = [(0, 0), (5, 8), (12, 12.5), (22, 14), (44, 14), (52, 12.5), (56, 11)]

AR = np.array([112, 118, 130]); AR_D = np.array([80, 85, 96]); AR_L = np.array([142, 148, 160])   # gunmetal 0x5a5f69, lifted for the sprite
ORG = np.array([255, 122, 42]); ORG_D = np.array([196, 84, 26]); CYN = np.array([90, 208, 255]); SEAM = (36, 38, 44)
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))
import splitlib as SL
PARTS = ('hull', 'booster')
PIVL = (CX - 57, 184)                       # left booster swivel hub centre (right = mirrored)


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

    def form(mask, hmap, k=0.55, spec=0.10):
        """round-form shading from an analytic height map (the 3D surface), laid over the plates so the bulb, cowl, casings
        and nacelles read as real volumes (light from the front, like the other TL sprites)"""
        shade, sp, nl = s._shade(hmap.astype(np.float32), gain=k, spec=spec, sp_pow=10)
        f = np.clip(shade, 0.55, 1.35)
        s.rgb[mask] = np.clip(s.rgb[mask]*f[mask][:, None] + 255*sp[mask][:, None], 0, 255)
    # ================================================================ silhouette + machinery base
    HWm = hwB(yy_); HBm = hB(yy_)
    hull = (yy_ >= 50) & (yy_ <= 186) & (ax_ <= HWm)
    belt = (yy_ >= 54) & (yy_ <= 184) & (ax_ <= HWm + 3.4) & (ax_ >= HWm - 2.5)
    pyl_pts = [(CX - hwB(184) + 2, 175), (CX - hwB(184) + 2, 197), (47, 191.5), (43.5, 188), (43.5, 181), (47, 178)]
    pylon = s.poly(spline(pyl_pts, 6, True))
    s.guts(hull | pylon, seed=143, tone=(46, 48, 54), minc=3, maxc=10); s.z[:] = 0
    if not P.on('hull'): s.a[:] = False                    # guts only under the hull + pylons
    with P('hull'):
        # ================================================================ side boosters: fixed pylon -> swivel hub -> lathe nacelle, aft nozzle
        s.plate(pylon, AR_L, z=2.6, bevel=1.8, dome=0.5, tilt=(0, 0.06), inset=1.2, shadow_k=0.85)
        form(pylon, 6*np.sqrt(np.clip(1 - ((yy_ - 185.5)/11)**2, 0, 1)), k=0.5)
        s.plate(pylon & (np.abs(yy_ - 184) < 2.0) & (xx_ > 47) & (xx_ < 70), ORG, z=2.7, bevel=0.8, shadow_k=0.7)         # orange top strip
        for xv in (52, 60, 68): s.rgb[s.disk(xv, 179.3, 0.55)] = SEAM; s.rgb[s.disk(xv, 188.7, 0.55)] = SEAM
    with P('booster'):
        nr = np.interp(yy_ - NAC_Y0, [a for a, b in NAC], [b for a, b in NAC], left=-1, right=-1)
        nac = (np.abs(xx_ - NAC_X) <= nr) & (yy_ >= NAC_Y0) & (yy_ <= NAC_Y0 + 56)
        noz = s.poly([(NAC_X - 8.5, 211), (NAC_X + 8.5, 211), (NAC_X + 10.4, 220), (NAC_X - 10.4, 220)])
        s.plate(noz, AR_D*0.8, z=1.4, bevel=1.2, dome=0.3, inset=0.6, shadow_k=0.85)
        form(noz, np.sqrt(np.clip(np.interp(yy_, [211, 220], [8.5, 10.4])**2 - (xx_ - NAC_X)**2, 0, None)), k=0.7)
        lipn = s.rrect(NAC_X - 11.4, 219, NAC_X + 11.4, 222, 1.4)
        s.plate(lipn, ORG, z=1.5, bevel=0.9, dome=0.3, shadow_k=0.8)
        s.plate(nac, AR, z=2.2, bevel=2.2, dome=0.6, inset=1.4, shadow_k=0.9,
                paint=[(nac & (np.abs(yy_ - (NAC_Y0 + zr)) < 1.0), ORG) for zr in (18, 30, 42)])
        for zr in (18, 30, 42):                                                              # flush rings: thin dark edge lines
            s.rgb[nac & (np.abs(np.abs(yy_ - (NAC_Y0 + zr)) - 1.0) < 0.3)] = ORG_D*0.6
        s.rgb[nac & (np.abs(yy_ - 164) < 0.4) & (np.abs(xx_ - NAC_X) < nr - 1.0)] = SEAM     # nose-cone seam
        s.rgb[nac & (np.abs(yy_ - 206) < 0.4) & (np.abs(xx_ - NAC_X) < nr - 1.0)] = SEAM
        form(nac, np.sqrt(np.clip(nr**2 - (xx_ - NAC_X)**2, 0, None)), k=0.85, spec=0.25)
        hub = s.disk(*PIV, 4.6)
        s.plate(hub, AR_L, z=2.8, bevel=1.4, dome=0.6, inset=0.0, shadow_k=0.9)
        rh = np.hypot(xx_ - PIV[0], yy_ - PIV[1])
        s.rgb[hub & (rh > 3.3) & (rh < 4.2)] = ORG; s.rgb[hub & (rh < 1.4)] = (40, 42, 48)
        sysl('side boosters: lathe nacelles with flush orange rings on fixed pylons + swivel hubs (vector +-14 when strafing)', NAC_X, 184)
    with P('hull'):
        # ================================================================ main drive on the rear bulkhead: neck + 3 orange ribs + big bell + lip
        bell = s.poly([(CX - 25, 201), (CX + 25, 201), (CX + 19.5, 221), (CX - 19.5, 221)])
        s.plate(bell, AR*1.08, z=1.7, bevel=2.0, dome=0.5, inset=1.2, shadow_k=0.9)
        form(bell, np.sqrt(np.clip(np.interp(yy_, [201, 221], [25, 19.5])**2 - ax_**2, 0, None)), k=0.7, spec=0.15)
        for yv in (207, 214): s.rgb[bell & (np.abs(yy_ - yv) < 0.45) & (ax_ < np.interp(yy_, [201, 221], [25, 19.5]) - 1.5)] = SEAM
        lip = s.rrect(CX - 26.4, 219.6, CX + 26.4, 223.4, 1.8)
        s.plate(lip, AR_L, z=1.8, bevel=1.0, dome=0.3, shadow_k=0.85)
        s.plate(s.rrect(CX - 19, 185, CX + 19, 202, 3), AR_D*0.85, z=2.0, bevel=1.6, dome=0.5, shadow_k=0.9)           # drive neck
        for i, y in enumerate((189, 194, 199)):
            rb_ = s.rrect(CX - 21.7 + 0.4*i, y - 2.2, CX + 21.7 - 0.4*i, y + 2.2, 2.0)
            s.plate(rb_, ORG, z=2.3, bevel=1.1, dome=0.4, shadow_k=0.9)
            form(rb_, np.sqrt(np.clip((21.7 - 0.4*i)**2 - ax_**2, 0, None)), k=0.6)
            for k in range(-5, 6):
                nx = CX + (21 - 0.4*i)*np.sin(k*np.pi/12); s.rgb[rb_ & (np.abs(xx_ - nx) < 0.5)] = ORG_D*0.7
        sysl('ribbed orange drive collar + one big bell on the flat rear bulkhead', CX, 205)

        # ================================================================ hull: equator belt, panelled bulb (centre band between the stripes higher)
        s.plate(belt, AR_D, z=2.6, bevel=1.6, dome=0.3, shadow_k=0.95)
        LAT = [50, 74, 98, 146, 170, 186.5]
        SK = 0.523                                                                          # stripe position: sin(0.55) of the half-width
        for k in range(len(LAT) - 1):
            band = hull & (yy_ >= LAT[k] + 0.6) & (yy_ <= LAT[k + 1] - 0.6)
            side = band & (ax_ > HWm*SK + 1.4)
            mid = band & (ax_ <= HWm*SK + 1.4)
            if k in (0, 4): side, mid = band & np.zeros_like(band), band
            zb = 1.5 + 2.8*float(hB((LAT[k] + LAT[k + 1])/2))/BY
            s.plate(side, AR*(1.0 + 0.03*(k % 2)), z=zb - 0.5, bevel=2.0, dome=0.6, tilt=(-0.35, 0), inset=1.3, shadow_k=0.9)
            s.plate(mid, AR_L*0.94 if k % 2 else AR*1.06, z=zb, bevel=2.2, dome=0.8, inset=1.5, shadow_k=0.9)
        seams = hull & np.zeros_like(hull)
        for py in LAT[1:-1]: seams |= hull & (np.abs(yy_ - py) < 0.6)
        s.rgb[seams] = SEAM
        for g in (-1,):                                                                        # radiator slots on the rear flanks (the core runs hot)
            for k in range(5):
                py = 150 + k*3.6; x0 = X(g, float(hwB(py)) - 4.5); x1 = X(g, float(hwB(py))*SK + 5.5)
                s.engrave(s.rrect(x0, py, x1, py + 1.3, 0.5) & hull, 0.4)
            hat = s.rrect(CX - 7, 174, CX + 7, 182, 1.5)                                      # rear service hatch
            s.engrave(hat & ~s.rrect(CX - 6.2, 174.8, CX + 6.2, 181.2, 1.0), 0.45)
            for xv in (CX - 3, CX, CX + 3): s.rgb[s.rrect(xv - 0.5, 176.5, xv + 0.5, 179.5, 0.3)] = SEAM
        bulk = hull & (yy_ > 185)
        s.rgb[bulk] = AR_D*0.7                                                                    # flat rear bulkhead edge
        # racing stripes: raised orange tubes at a = +-0.55 rad, py 82..186
        spts = [(X(-1, float(hwB(py))*SK), py) for py in np.arange(82, 187, 4)]
        z0 = s.z.copy()
        stripe = s.cable(spts, 2.6, ORG, clamps=0, cast=True, smooth=True)
        s.z[stripe] = z0[stripe] + 0.2
        sysl('tall gunmetal bulb: equator belt, latitude seams, orange racing stripes, flat rear bulkhead', X(-1, 40), 140)

        # ================================================================ visors: cyan glass bands in orange frames (front + each side)
        def band_poly(ph, ln, th0, th1, sx, n=40):
            fw = [(CX - sx*np.cos(ph - ln/2 + ln*i/n)*np.sin(th0), BCZ + BZ*np.sin(ph - ln/2 + ln*i/n)*np.sin(th0)) for i in range(n + 1)]
            bk = [(CX - sx*np.cos(ph - ln/2 + ln*i/n)*np.sin(th1), BCZ + BZ*np.sin(ph - ln/2 + ln*i/n)*np.sin(th1)) for i in range(n, -1, -1)]
            return s.poly(fw + bk)
        def visor(ph, ln, th, tl, sx, nm):
            fr = band_poly(ph, ln + 0.06, th - tl/2 - 0.05, th + tl/2 + 0.05, sx)
            z0 = s.z.copy()
            s.plate(fr, ORG, bevel=0.8, dome=0.2, outline=0.6, shadow_k=0.85); s.z[fr] = z0[fr] + 0.1
            gl = band_poly(ph, ln, th - tl/2, th + tl/2, sx)
            t = ndi.distance_transform_edt(gl)/s.SS
            s.rgb[gl] = np.clip(CYN*(0.75 + 0.5*np.clip(t/2.0, 0, 1))[..., None], 0, 255)[gl]
            s.rgb[gl & (t < 0.5)] = CYN*0.45
            for k in range(1, nm):                                                              # mullions
                a = ph - ln/2 + ln*k/nm
                p0 = (CX - sx*np.cos(a)*np.sin(th - tl/2), BCZ + BZ*np.sin(a)*np.sin(th - tl/2)); p1 = (CX - sx*np.cos(a)*np.sin(th + tl/2), BCZ + BZ*np.sin(a)*np.sin(th + tl/2))
                for tt in np.linspace(0, 1, 12): s.rgb[s.disk(p0[0] + (p1[0] - p0[0])*tt, p0[1] + (p1[1] - p0[1])*tt, 0.45) & gl] = (24, 60, 84)
            return fr
        vf = visor(np.pi*1.5, 0.9, 1.0, 0.13, BX*0.84, 6)
        vs = visor(0.0, 0.7, 1.1, 0.12, BX*0.98, 4)
        # round-form shading over the whole bulb (true ellipsoid surface of the 3D), before the crown hardware
        hm = HBm*np.sqrt(np.clip(1 - (ax_/np.maximum(HWm, 0.5))**2, 0, 1))
        form(hull, hm*0.55, k=0.6, spec=0.08)
        sysl('cyan visor bands in orange frames: front + both sides (no tower)', CX, 62)

        # ================================================================ side-gun mounts (hull part): bolted root plate, collar, armoured pod casing
        for g in (-1,):
            gx, gy = SG[0]
            root = s.rrect(X(g, HX + 3.2), GUN_Y - 12.5, X(g, HX - 1.5), GUN_Y + 12.5, 2.2)
            s.plate(root, AR_D, z=2.6, bevel=1.4, dome=0.3, inset=0.0, shadow_k=0.9)
            for k in range(5): s.rgb[s.disk(X(g, HX + 1.6), GUN_Y - 9.6 + k*4.8, 0.6)] = SEAM
            col = s.rrect(X(g, HX + 8.5), GUN_Y - 6.8, X(g, HX + 1), GUN_Y + 6.8, 2.0)
            s.plate(col, AR_L, z=2.4, bevel=1.4, dome=0.4, shadow_k=0.9)
            form(col, np.sqrt(np.clip(6.8**2 - (yy_ - GUN_Y)**2, 0, None)), k=0.6)
            ring = s.rrect(X(g, HX + 3.2), GUN_Y - 7.6, X(g, HX + 1.4), GUN_Y + 7.6, 0.8)
            s.plate(ring, ORG, z=2.5, bevel=0.6, shadow_k=0.8)
            # casing: ellipsoid 13 x 15 centred 2 px behind the hub, open at the front (+-72 deg) round the hub
            ccx, ccy = gx, gy + 2
            u = (xx_ - ccx)/13.0; v = (yy_ - ccy)/15.0; re = np.hypot(u, v)
            ang = np.degrees(np.arctan2(u, -v))                                                # 0 = forward, +-180 = aft
            shell = (re <= 1.0) & (np.abs(ang) > 72) & (np.hypot(xx_ - gx, yy_ - gy) > 8.2)
            s.plate(shell, AR_L*0.96, z=2.9, bevel=2.2, dome=0.5, inset=1.2, shadow_k=0.95)
            form(shell, 13*np.sqrt(np.clip(1 - re**2, 0, None)), k=0.55, spec=0.12)
            for sg in (-1, 1):                                                                 # orange edge lips along the opening
                a = np.radians(sg*72); dx, dy = np.sin(a), -np.cos(a)
                t = np.linspace(0, 1, 50)
                for tt in t:
                    rx, ry = 13*dx*tt, 15*dy*tt
                    if np.hypot(rx + ccx - gx, ry + ccy - gy) < 8.0 or tt > 0.97: continue
                    s.rgb[s.disk(ccx + rx, ccy + ry, 1.0) & shell] = ORG
            rs = np.hypot(xx_ - gx, yy_ - gy)
            s.rgb[shell & (rs < 9.4)] *= 0.62                                                   # inner edge of the shell round the hub
            s.mount(gx, gy, 7.2, AR_D)                                                          # plain turret ring (the gun sprite sits here)
            s.z[s.disk(gx, gy, 7.2)] = 2.5
        sysl('2 side guns: built-in mounts (root plate + collar) with armoured pod casings open at the front, 60 deg fwd', SG[0][0], GUN_Y)

        # ================================================================ nose cowl + hardpoint muzzle seat
        cr = lambda py: np.interp(py, [26, 54], [15.0, 21.9])
        cowl = (yy_ >= 26) & (yy_ <= 55 + 7*(ax_/22.0)**2) & (ax_ <= cr(yy_)) & ~((yy_ > 54) & (ax_ > 21.9 - (yy_ - 54)*0.2))
        s.plate(cowl, AR_L, z=3.2, bevel=2.4, dome=0.5, inset=1.4, shadow_k=0.95,
                paint=[(cowl & (np.abs(yy_ - 48) < 1.1), ORG)])
        for py in (32, 37, 42): s.rgb[cowl & (np.abs(yy_ - py) < 0.45) & (ax_ < cr(yy_) - 1.2)] = SEAM
        form(cowl, np.sqrt(np.clip(cr(yy_)**2 - ax_**2, 0, None))*0.9, k=0.6, spec=0.14)
        seat = s.disk(HP[0], HP[1], 9.5) & (yy_ < 27.2)
        s.plate(seat, AR_D, z=3.0, bevel=1.2, shadow_k=0.9)
        s.mount(HP[0], HP[1], 8.2, AR_D)                                                        # gimbal seat ring (hardpoint sprite on top)
        s.z[s.disk(HP[0], HP[1], 8.2)] = 2.9
        mlip = s.rrect(CX - 17, 24.6, CX + 17, 28.2, 1.6)
        mlip &= ~s.disk(HP[0], HP[1], 8.4)
        s.plate(mlip, AR_D*1.1, z=3.4, bevel=0.9, dome=0.3, shadow_k=0.9)                     # muzzle-port lip
        sysl('nose cowl with the medium ballistic hardpoint (gimbal ball in the muzzle port, 45 deg)', CX, 40)

        # ================================================================ crown: the core's armoured barbette + turret seat (360), heat slits
        tx, ty = TOP
        rt = np.hypot(xx_ - tx, yy_ - ty); at = np.degrees(np.arctan2(yy_ - ty, xx_ - tx))
        barb = rt < 25.5
        s.plate(barb, AR_D*1.05, z=4.8, bevel=2.6, dome=0.6, inset=0.0, shadow_k=0.95,
                paint=[(barb & (np.abs(rt - 23.6) < 0.9), ORG)])
        for k in range(8):
            a = 22.5 + 45*k
            sl = (np.abs(((at - a + 180) % 360) - 180) < 7.0) & (rt > 25.2) & (rt < 27.4)
            s.plate(sl, ORG, z=4.6, bevel=0.5, outline=0.5, shadow_k=0.8)
            s.rgb[sl & (np.abs(rt - 26.3) < 0.35)] = (120, 40, 10)
        brim = (rt < 21.8) & (rt > 16.6)
        s.plate(brim, AR_L, z=5.3, bevel=1.4, dome=0.4, inset=0.0, shadow_k=0.95)
        for a in range(0, 360, 30): s.rgb[s.disk(tx + 19.2*np.cos(np.radians(a)), ty + 19.2*np.sin(np.radians(a)), 0.55)] = SEAM
        s.rgb[(rt <= 16.6) & (rt > 15.6)] = (26, 28, 32)
        s.mount(tx, ty, 15.6, AR_D)                                                              # turret seat ring (turret sprite on top)
        s.z[rt < 16.6] = 5.0
        sysl('core turret: armoured barbette on the crown, heat slits round it, 360 deg', tx, ty)

        # ================================================================ 2 small ballistic PD sunk into the rear crown, orange outboard-aft lips
        VP.sunk_mount(s, PD[0][0], PD[0][1], 4.6, (-0.8, 0.6), metal=AR_D, lip_metal=AR_L, z=4.2, lip_z=4.9, accent=ORG)
        sysl('2 small ballistic PD in the rear crown, facing aft, 180 deg', PD[0][0], PD[0][1])
    # ================================================================ symmetry + lights
    _h = CX*s.SS
    s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
    with P('hull'):
        s.lights([(X(-1, 57.5), 126), (X(1, 57.5), 126)], [(255, 70, 60), (90, 255, 120)])
    return s


if __name__ == '__main__':
    OUT = _ROOT + '/ss_style/fenrir_ss_v4_'
    snap = lambda s: (s.rgb.copy(), s.a.copy(), s.z.copy())
    sF = build(PARTS); full_snap = snap(sF); zmax = float((sF.z*sF.a).max()); full_ref = sF.render()   # whole ship in one pass (== v3)
    sH = build({'hull'}); hs = snap(sH)
    hull_im = SL.lit_part(sH, hs, hs, zmax)                                      # hull lit on its own (boosters swing, no baked booster shadow)
    sM = build({'booster'}); pair = SL.lit_part(sM, snap(sM), full_snap, zmax)     # both boosters, lit within the full ship
    pair = SL.add_shadow_fringe(pair, full_ref, hull_im)                          # shadow each booster casts on the pylons/hull
    L, R = SL.split_lr(pair, CX)
    comp = SL.over(hull_im, L, R)
    hull_im.save(OUT + 'hull.png'); L.save(OUT + 'boosterL.png'); R.save(OUT + 'boosterR.png'); comp.save(OUT + 'full.png')
    v3 = json.load(open(_ROOT + '/ss_style/fenrir_ss_v3_slots.json'))
    v3.update(pivot_L=[float(PIVL[0]), float(PIVL[1])], pivot_R=[float(2*CX - PIVL[0]), float(PIVL[1])],
              parts=dict(order=['hull', 'boosterL', 'boosterR']))
    json.dump(v3, open(OUT + 'slots.json', 'w'))
    json.dump(SYSTEMS, open(_ROOT + '/ss_style/fenrir_v4_systems.json', 'w'))
    from PIL import Image
    v3im = Image.open(_ROOT + '/ss_style/fenrir_ss_v3.png')
    print('one-pass full vs v3 :', SL.diff_stats(full_ref, v3im))
    print('composite vs v3     :', SL.diff_stats(comp, v3im))
    print('pivots', v3['pivot_L'], v3['pivot_R'], 'ENG', v3['ENG'])
