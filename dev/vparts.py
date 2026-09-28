"""vparts - detailed stern / engine part library (studied from the vanilla Onslaught stern):
long FLUTED engine housings with ring bands, bulbous nozzle lips with a hot specular spot, dark exhaust mouths,
lengthwise pipe bundles, ribbed struts, duct manifolds. All parts draw into a vstyle.Ship."""
import numpy as np
from scipy import ndimage as ndi
from vstyle import Ship

def _cyl_shade(s, x, w):
    u = np.clip((s.xx/s.SS - x)/(w/2), -1, 1); cyl = np.sqrt(np.clip(1 - u**2, 0, 1))
    return u, cyl

def engine_housing(s, x, y0, y1, w, metal=(150, 146, 144), accent=None, flutes=None, bands=2, lip=True, taper=0.62):
    """engine can seen from above, vanilla-like: TAPERED body (narrow root -> full width at the bulb), dark fluting
    with thin bright ribs, occluded root, ring bands, bulbous exit lip with a hot specular spot, dark mouth"""
    S = s.SS; yy = s.yy/S; xx = s.xx/S
    f = np.clip((yy - y0)/max(1, y1 - y0), 0, 1)
    hw = w/2*(taper + (1 - taper)*np.sqrt(f))                                        # half-width along the can
    body = (np.abs(xx - x) <= hw) & (yy >= y0) & (yy <= y1)
    lipm = s.ell(x, y1, w/2 + 1.4, max(2.2, w*0.15)) if lip else np.zeros_like(body)
    m = body | lipm
    s.shadow(m, 1.4, 1.8, 0.7, 1.0)
    import vstyle as _vs
    u = np.clip((xx - x)/np.maximum(hw, 0.5), -1, 1)*_vs._sx(x); cyl = np.sqrt(np.clip(1 - u**2, 0, 1))
    lum = 0.12 + 0.62*cyl*(1 - 0.4*u) + 0.55*np.exp(-((u + 0.42)/0.11)**2)
    nf = flutes or max(3, int(w/2.4))
    ph = ((u + 1)/2*nf) % 1.0
    rib = np.where(ph < 0.28, 1.25, np.where(ph < 0.4, 0.45, 0.8))                   # bright rib, dark groove, mid face
    lum = np.where(body, lum*rib, lum)
    lum = lum*(0.45 + 0.55*np.clip(f/0.35, 0, 1))                                    # root sinks into the hull (occlusion)
    for k in range(bands):
        yb = y0 + (y1 - y0)*(0.3 + 0.6*(k + 1)/(bands + 1))
        lum = np.where(body & (np.abs(yy - yb) < 0.9), lum*0.35, lum)
        lum = np.where(body & (np.abs(yy - yb + 1.3) < 0.45), np.minimum(lum*1.6, 1.5), lum)
    warm = np.array(metal, np.float32)
    col = warm[None, None, :]*lum[..., None]
    col = col*(1 + 0.12*np.array([0.25, 0.0, -0.2])[None, None, :]*f[..., None])     # slight warm heat tint near the exit
    if accent is not None:
        acc = body & (np.abs(yy - (y0 + (y1 - y0)*0.18)) < 1.2); col[acc] = np.array(accent, np.float32)*(0.4 + 0.7*cyl[acc])[:, None]
    if lip:
        L_ = np.clip(1 - np.hypot((xx - x)/(w/2 + 1.4), (yy - y1)/max(2.2, w*0.15)), 0, 1)
        lc = warm*(0.45 + 1.0*L_[..., None])
        col = np.where(lipm[..., None], lc, col)
        col[s.ell(x, y1 + 0.5, w/2 - 1.4, max(0.9, w*0.06))] = (18, 16, 20)
        spot = s.ell(x - w*0.2*_vs._sx(x), y1 - max(1.0, w*0.07), w*0.11, max(0.7, w*0.045))
        col[spot & lipm] = (255, 244, 228)
    e = m & ~ndi.binary_erosion(m, iterations=max(1, int(0.7*S))); col[e] *= 0.25
    s.rgb[m] = np.clip(col[m], 0, 255); s.a |= m
    return m

def pipe_bundle(s, x0, x1, y0, y1, n=4, metal=(128, 126, 126), clamps=(), gap=0.6):
    """n parallel lengthwise pipes between x0..x1 (cylinder shaded), optional clamp bands at y in clamps"""
    w = (x1 - x0)/n
    for k in range(n):
        cx = x0 + w*(k + 0.5)
        s.cylinder(cx - w/2 + gap/2, y0, cx + w/2 - gap/2, y1, metal, axis='v', cast=(k == 0), outline=0.4)
    for yc in clamps:
        cl = s.rrect(x0 - 0.6, yc, x1 + 0.6, yc + 2.2, 0.6)
        s.plate(cl, np.array(metal)*0.75, bevel=0.8, outline=0.4, shadow_k=0.45)

def rib_strut(s, p0, p1, w=2.4, metal=(118, 114, 112)):
    """angled structural strut with a highlight edge"""
    return s.cable([p0, p1], w, metal, clamps=0, smooth=False)

def duct_manifold(s, x, y, w, h, metal=(112, 110, 112), n_ports=3):
    """box manifold feeding the engines: bevelled block + port rings along its lower edge"""
    m = s.rrect(x - w/2, y - h/2, x + w/2, y + h/2, 1.4)
    s.plate(m, np.array(metal), bevel=1.6, dome=0.5, inset=1.2, outline=0.6, shadow_k=0.6)
    for k in range(n_ports):
        px = x - w/2 + w*(k + 0.5)/n_ports
        s.rgb[s.disk(px, y + h/2 - 2, 1.3)] = (30, 30, 34); s.rgb[s.disk(px - 0.4, y + h/2 - 2.4, 0.5)] = (190, 190, 194)
    return m

def nozzle_cluster(s, cx, y_exit, main_w, length, metal=(150, 146, 144), n_side=2, side_w=None, accent=None):
    """one main fluted drive + satellite cans either side (stepped back), fed by pipe bundles, with struts"""
    side_w = side_w or max(4, main_w*0.32)
    parts = []
    span = main_w/2 + (side_w + 0.8)*n_side + 8
    bay = s.poly([(cx - span, y_exit - length - 6), (cx + span, y_exit - length - 6), (cx + span - 3, y_exit - 8), (cx - span + 3, y_exit - 8)])
    s.rgb[bay] = (26, 25, 29); s.a |= bay
    for yy_ in np.arange(y_exit - length - 4, y_exit - 10, 3.0):                   # recess back-wall ribbing
        s.rgb[bay & s.rrect(cx - span, yy_, cx + span, yy_ + 0.8, 0.1)] = (40, 38, 42)
    for g in (-1, 1):
        for k in range(n_side):
            sx = cx + g*(main_w/2 + side_w/2 + 0.8 + k*(side_w + 0.8))
            ye = y_exit - 4 - k*3
            parts.append(engine_housing(s, sx, ye - length*0.55, ye, side_w, metal=metal, bands=1, flutes=3))
        px0 = cx + g*(main_w/2 + (side_w + 0.8)*n_side + 1)
        pipe_bundle(s, min(px0, px0 + g*6), max(px0, px0 + g*6), y_exit - length, y_exit - 6, n=3, clamps=(y_exit - length*0.6,))
    for g in (-1, 1):                                                                # armoured struts manifold -> satellites
        sheath(s, [(cx + g*(main_w/2 - 2), y_exit - length - 1), (cx + g*(main_w/2 + side_w*n_side + 2), y_exit - length*0.45)], 2.2, accent or (90, 150, 240))
    parts.append(engine_housing(s, cx, y_exit - length, y_exit, main_w, metal=metal, bands=3, accent=accent))
    duct_manifold(s, cx, y_exit - length - 4, main_w + 2*side_w*n_side, 8, n_ports=2*n_side + 1)
    return parts

# ------------------------------------------------------------------ connections: hoses, power, data, actuators
HOSE = (70, 72, 78); COPPER = (168, 120, 78); DATA = (200, 165, 70)

def actuator(s, p0, p1, w=2.2):
    """hydraulic gimbal actuator: dark cylinder half + bright polished rod half + joint pins"""
    mx, my = (p0[0] + p1[0])/2, (p0[1] + p1[1])/2
    s.cable([p0, (mx, my)], w, (86, 88, 94), clamps=0, smooth=False)
    s.cable([(mx, my), p1], w*0.55, (200, 202, 208), clamps=0, smooth=False)
    for (x, y) in (p0, p1):
        s.rgb[s.disk(x, y, w*0.75)] = (40, 42, 46); s.rgb[s.disk(x - 0.3, y - 0.3, w*0.3)] = (190, 192, 198)

def engine_plumbing(s, x, y0, y1, w, accent=(90, 150, 240), manifold_y=None, rng=None):
    """connections ON an engine can: 2 fuel hoses down the flanks into flanged sockets, an accent power cable into
    the top ring, thin data wires, 2 gimbal actuators, strap clamps"""
    my = manifold_y if manifold_y is not None else y0 - 3
    L = y1 - y0
    for g in (-1, 1):
        xs = x + g*(w*0.36)
        hose = [(xs + g*1.5, my), (xs + g*2.2, y0 + L*0.12), (xs, y0 + L*0.45), (xs - g*w*0.08, y0 + L*0.62)]
        s.cable(hose, max(1.4, w*0.09), HOSE, clamps=L*0.18, clamp_col=(150, 152, 158))
        s.connector(hose[-1][0], hose[-1][1], max(1.2, w*0.08), body=(120, 122, 128), ring=(200, 150, 60))
        # thin copper coolant line hugging the hose
        s.cable([(p[0] + g*1.6, p[1]) for p in hose[:-1]], max(0.7, w*0.035), COPPER, clamps=0, cast=False)
        # gimbal actuator from the manifold edge to the can at ~55 % length
        actuator(s, (x + g*(w*0.62), my + 1), (x + g*(w*0.42), y0 + L*0.55), max(1.4, w*0.08))
    # power cable (ship accent colour) down the spine of the can into the top ring band
    pc = [(x + w*0.05, my), (x + w*0.05, y0 + L*0.1), (x - w*0.02, y0 + L*0.3)]
    s.cable(pc, max(1.2, w*0.08), tuple(int(v*0.8) for v in accent), clamps=L*0.12, clamp_col=(40, 42, 48))
    s.connector(pc[-1][0], pc[-1][1], max(1.1, w*0.075), body=(100, 102, 110), ring=tuple(accent))
    # data wires (thin amber) to a sensor pod near the exit
    sx, sy = x + w*0.22, y0 + L*0.8
    s.cable([(x - w*0.12, y0 + L*0.32), (x - w*0.16, y0 + L*0.55), (sx, sy)], 0.7, DATA, clamps=0, cast=False)
    s.rgb[s.disk(sx, sy, max(0.9, w*0.05))] = (60, 62, 66); s.rgb[s.disk(sx, sy, max(0.45, w*0.022))] = (255, 90, 70)
    # strap clamps around the can
    for f in (0.22, 0.7):
        yb = y0 + L*f
        st = s.rrect(x - w/2 + 0.2, yb, x + w/2 - 0.2, yb + max(1.2, w*0.06), 0.4)
        s.rgb[st] = s.rgb[st]*0.45 + np.array([120, 122, 128])*0.55
        for g in (-1, 1): s.rgb[s.disk(x + g*(w/2 - 1.2), yb + 0.6, 0.55)] = (210, 212, 216)

def satellite_plumbing(s, x, y0, y1, w, my):
    s.cable([(x, my), (x + 0.5, y0 + (y1 - y0)*0.2)], max(1.0, w*0.16), HOSE, clamps=0)
    s.connector(x + 0.5, y0 + (y1 - y0)*0.2, max(0.9, w*0.12), body=(120, 122, 128), ring=(200, 150, 60))
    s.cable([(x - w*0.3, y0 + (y1 - y0)*0.25), (x - w*0.3, y0 + (y1 - y0)*0.6)], 0.6, COPPER, clamps=0, cast=False)

_nc0 = nozzle_cluster
def nozzle_cluster(s, cx, y_exit, main_w, length, metal=(150, 146, 144), n_side=2, side_w=None, accent=None, plumbing=True):
    side_w = side_w or max(4, main_w*0.32)
    parts = _nc0(s, cx, y_exit, main_w, length, metal=metal, n_side=n_side, side_w=side_w, accent=accent)
    if plumbing:
        my = y_exit - length - 1
        for g in (-1, 1):
            for k in range(n_side):
                sx = cx + g*(main_w/2 + side_w/2 + 0.8 + k*(side_w + 0.8)); ye = y_exit - 4 - k*3
                satellite_plumbing(s, sx, ye - length*0.55, ye, side_w, my)
        engine_plumbing(s, cx, y_exit - length, y_exit, main_w, accent=accent or (90, 150, 240), manifold_y=my)
    return parts

# ------------------------------------------------------------------ FAR-FUTURE connections (replace hoses/pistons/clamps)
def lightline(s, pts, col, width=0.8, glow=True):
    """flush light-guide line inlaid in the surface: dark groove + bright core + soft glow"""
    g = s.cable(pts, width + 1.2, (26, 28, 34), clamps=0, cast=False, smooth=False)
    s.rgb[g] = (26, 28, 34)
    c = s.cable(pts, width, col, clamps=0, cast=False, smooth=False)
    s.rgb[c] = np.minimum(np.array(col, np.float32)*1.1 + 30, 255)
    return g

def sheath(s, pts, w, accent, metal=(96, 100, 110)):
    """armoured conduit sheath: faceted smooth tube (ridge-lit), segmented by thin glowing seams - no clamps"""
    m = s.cable(pts, w, metal, clamps=0, smooth=False)
    # faceted look: darken one half along the path, light edge on the other
    L = 0.0; segs = []
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        seg = np.hypot(x1 - x0, y1 - y0); t = 5.0
        while t < seg - 2:
            cx, cy = x0 + (x1 - x0)*t/seg, y0 + (y1 - y0)*t/seg; nx, ny = -(y1 - y0)/seg, (x1 - x0)/seg
            sm = s.poly([(cx + nx*w/2 - (x1 - x0)/seg*0.35, cy + ny*w/2 - (y1 - y0)/seg*0.35), (cx + nx*w/2 + (x1 - x0)/seg*0.35, cy + ny*w/2 + (y1 - y0)/seg*0.35),
                         (cx - nx*w/2 + (x1 - x0)/seg*0.35, cy - ny*w/2 + (y1 - y0)/seg*0.35), (cx - nx*w/2 - (x1 - x0)/seg*0.35, cy - ny*w/2 - (y1 - y0)/seg*0.35)]) & m
            s.rgb[sm] = np.minimum(np.array(accent, np.float32)*1.1 + 25, 255)
            t += 7.0
    return m

def coupling_node(s, x, y, r, accent):
    """magnetic coupling node: flush dark disc, glowing ring, bright centre - no bolts, no flange"""
    rr = np.hypot(s.xx/s.SS - x, s.yy/s.SS - y); m = rr < r
    s.rgb[m] = (30, 32, 38); s.a |= m
    ring = (rr < r*0.8) & (rr > r*0.55); s.rgb[ring] = np.minimum(np.array(accent, np.float32)*1.15 + 20, 255)
    s.rgb[rr < r*0.25] = (235, 245, 255)
    s.rgb[m & (rr > r*0.9)] = (150, 154, 162)

def field_gimbal(s, x, y, w, accent):
    """field-coil gimbal collar at the engine root: segmented armour ring with emitter slits glowing in the accent"""
    col = s.rrect(x - w/2 - 1.6, y - 2.4, x + w/2 + 1.6, y + 2.4, 1.6)
    s.plate(col, np.array([110, 114, 122]), bevel=1.2, dome=0.4, outline=0.5, shadow_k=0.55)
    for k in range(-2, 3):
        sx = x + k*w*0.2
        s.rgb[s.rrect(sx - w*0.06, y - 0.7, sx + w*0.06, y + 0.7, 0.3)] = np.minimum(np.array(accent, np.float32)*1.2 + 30, 255)
    for g in (-1, 1): coupling_node(s, x + g*(w/2 + 0.6), y, 1.8, accent)

def engine_plumbing(s, x, y0, y1, w, accent=(90, 150, 240), manifold_y=None, rng=None):
    """far-future engine connections: 2 armoured conduit sheaths with glowing seams into coupling nodes, a field-coil
    gimbal collar, flush light-guide data lines, segmented armour collars with emitter slits"""
    my = manifold_y if manifold_y is not None else y0 - 3
    L = y1 - y0
    field_gimbal(s, x, y0 + L*0.1, w*0.72, accent)
    for g in (-1, 1):
        xs = x + g*(w*0.34)
        path = [(xs + g*1.2, my), (xs + g*1.2, y0 + L*0.3), (xs, y0 + L*0.5)]
        sheath(s, path, max(1.6, w*0.11), accent)
        coupling_node(s, path[-1][0], path[-1][1], max(1.4, w*0.09), accent)
        lightline(s, [(x + g*w*0.14, y0 + L*0.16), (x + g*w*0.14, y0 + L*0.46), (x + g*w*0.24, y0 + L*0.58), (x + g*w*0.24, y0 + L*0.82)], accent, 0.6)
    for f in (0.66,):                                                               # segmented armour collar near the exit
        yb = y0 + L*f
        cl = s.rrect(x - w/2, yb, x + w/2, yb + max(1.6, w*0.07), 0.5)
        s.rgb[cl] = s.rgb[cl]*0.4 + np.array([130, 134, 142])*0.6
        s.rgb[cl & (np.abs(s.xx/s.SS - x) < w*0.12)] = np.minimum(np.array(accent, np.float32)*1.2 + 30, 255)

def satellite_plumbing(s, x, y0, y1, w, my, accent=(90, 150, 240)):
    sheath(s, [(x, my), (x, y0 + (y1 - y0)*0.22)], max(1.1, w*0.18), accent)
    coupling_node(s, x, y0 + (y1 - y0)*0.22, max(1.0, w*0.15), accent)

def nozzle_cluster(s, cx, y_exit, main_w, length, metal=(150, 146, 144), n_side=2, side_w=None, accent=None, plumbing=True):
    side_w = side_w or max(4, main_w*0.32); acc = accent or (90, 150, 240)
    parts = _nc0(s, cx, y_exit, main_w, length, metal=metal, n_side=n_side, side_w=side_w, accent=accent)
    if plumbing:
        my = y_exit - length - 1
        for g in (-1, 1):
            for k in range(n_side):
                sx = cx + g*(main_w/2 + side_w/2 + 0.8 + k*(side_w + 0.8)); ye = y_exit - 4 - k*3
                satellite_plumbing(s, sx, ye - length*0.55, ye, side_w, my, acc)
        engine_plumbing(s, cx, y_exit - length, y_exit, main_w, accent=acc, manifold_y=my)
    return parts

# ---------------------------------------------------------------- step 1d (CHOSEN): structural pylons
def pylon(s, x, y0, y1, w_top, w_bot=None, accent=(255, 150, 60), metal=(130, 134, 142), lean=0.0, vent=True):
    """armoured structural pylon the engine hangs from (lines implied inside): wedge plate, vent grille in the
    upper part, a thin lit accent seam down the lower part. lean shifts the bottom sideways (px)."""
    w_bot = w_bot if w_bot is not None else w_top*0.55
    xb = x + lean
    m = s.poly([(x - w_top/2, y0), (x + w_top/2, y0), (xb + w_bot/2, y1 - w_bot*0.6), (xb, y1), (xb - w_bot/2, y1 - w_bot*0.6)])
    s.plate(m, np.array(metal), bevel=min(2.4, w_top*0.3), tilt=(0.12 if lean >= 0 else -0.12, 0.1), inset=min(1.8, w_top*0.22), shadow_k=0.8, notch=0)
    L = y1 - y0
    if vent and w_top >= 4:
        gw = w_top*0.28
        s.grille(m & s.rrect(x - gw, y0 + L*0.1, x + gw, y0 + L*0.45, 0.4), period=2.0)
    yy = s.yy/s.SS; xx = s.xx/s.SS
    t = np.clip((yy - y0)/L, 0, 1); xc = x + lean*t
    seam = m & (np.abs(xx - xc) < 0.45) & (yy > y0 + L*0.52) & (yy < y1 - 1.2)
    s.rgb[seam] = np.array(accent)
    return m

def engine_cowl(s, x, y0, y1, w_top, w_bot, accent=(255, 150, 60), metal=(134, 138, 148)):
    """armoured pylon-cowl sitting directly ABOVE a drive: covers the drive root, the bell emerges from under its lip.
    vent grille up top, two lit accent seams down the flanks, dark occlusion line under the lip."""
    r = min(4.0, w_bot*0.24)
    from vstyle import spline
    pts = [(x - w_top/2, y0), (x + w_top/2, y0), (x + w_top/2 - (w_top - w_bot)*0.2, y0 + (y1 - y0)*0.45), (x + w_bot/2, y1 - r),
           (x + w_bot/2 - r*0.7, y1), (x - w_bot/2 + r*0.7, y1), (x - w_bot/2, y1 - r), (x - w_top/2 + (w_top - w_bot)*0.2, y0 + (y1 - y0)*0.45)]
    m = s.poly(spline(pts, 10, True)) | s.poly([(x - w_top/2, y0), (x + w_top/2, y0), (x + w_top/2 - 1, y0 + 3), (x - w_top/2 + 1, y0 + 3)])
    s.shadow(m & (s.yy/s.SS > y1 - 3), 0.0, 1.6, 0.8, 0.9)                         # lip throws shade onto the drive
    s.plate(m, np.array(metal), bevel=min(2.4, w_bot*0.18), dome=0.5, tilt=(0, 0.12), inset=min(1.8, w_bot*0.12), shadow_k=0.8, notch=0)
    L = y1 - y0; yy = s.yy/s.SS; xx = s.xx/s.SS
    gw = w_top*0.26
    s.grille(m & s.rrect(x - gw, y0 + L*0.14, x + gw, y0 + L*0.5, 0.4), period=2.0)
    t = np.clip((yy - y0)/L, 0, 1); hw = (w_top/2 + (w_bot/2 - w_top/2)*t) - max(1.6, w_bot*0.14)
    for g in (-1, 1):
        seam = m & (np.abs(xx - (x + g*hw)) < 0.45) & (yy > y0 + L*0.3) & (yy < y1 - r - 0.6)
        s.rgb[seam] = np.array(accent)
    lip = m & (yy > y1 - 1.3); s.rgb[lip] *= 0.55
    return m

def core_armour(s, x, y, r, glow=(255, 170, 90), metal=(118, 122, 130), z=3.2):
    """the drive core sits DEEP in the hull; on deck only its armoured cover shows: a thick bolted ring + 8 overlapping
    petal plates, with 4 narrow heat slits that let the core's glow leak out (it's a vent, not a window)"""
    yy = s.yy/s.SS; xx = s.xx/s.SS
    rr = np.hypot(xx - x, yy - y); an = (np.degrees(np.arctan2(yy - y, xx - x)) + 360) % 360
    ring = s.disk(x, y, r + 4)
    s.plate(ring, np.array(metal)*0.85, z=z, bevel=2.6, dome=0.6, inset=1.6, shadow_k=0.85, notch=0)
    cov = s.disk(x, y, r)
    for k in range(8):                                                     # petals, drawn so each overlaps the next
        a0 = k*45.0
        pet = cov & (((an - a0) % 360) < 50)
        s.plate(pet, np.array(metal)*(1.0 + 0.04*(k % 2)), z=z + 0.4 + 0.08*k, bevel=1.6, dome=0.5, inset=0.8, shadow_k=0.6, notch=0)
    s.plate(s.disk(x, y, r*0.34), np.array(metal)*1.1, z=z + 1.2, bevel=1.6, dome=0.8, inset=1.0, shadow_k=0.7, notch=0)   # centre boss
    for k in range(4):                                                     # heat slits
        a = np.radians(45 + 90*k)
        m = (np.abs(((an - (45 + 90*k) + 180) % 360) - 180) < 3.2) & (rr > r*0.45) & (rr < r*0.9)
        t = np.clip(1 - np.abs(rr - r*0.68)/(r*0.25), 0, 1)
        s.rgb[m] = (np.array(glow)*(0.55 + 0.45*t[m][:, None]))
    for k in range(12):
        a = np.radians(k*30 + 15); s.rgb[s.disk(x + (r + 2)*np.cos(a), y + (r + 2)*np.sin(a), 0.6)] = (40, 42, 46)

# ---------------------------------------------------------------- shared parts promoted from the capitals
def diag_jet(s, g, cx_, cy_, w_, metal=(146, 144, 150), T=40, z=1.1):
    """small drive drawn upright in its own supersampled tile, rotated 45 deg so it fires back-outward (g = -1 left, +1 right),
    stamped onto the hull arrays (clipped to the canvas)"""
    from vstyle import Ship
    j = Ship(T, T, SS=s.SS, seed=5)
    mm = engine_housing(j, T/2, 3, T - 11, w_, metal=metal, bands=2); j.z[mm] = z
    ang = -45 if g < 0 else 45
    rgb = np.stack([ndi.rotate(j.rgb[..., c], ang, reshape=False, order=1) for c in range(3)], -1)
    al = ndi.rotate(j.a.astype(np.float32), ang, reshape=False, order=1) > 0.5
    zr = ndi.rotate(j.z, ang, reshape=False, order=0)
    ox, oy = int(round((cx_ - T/2)*s.SS)), int(round((cy_ - T/2)*s.SS))
    x0, y0 = max(0, ox), max(0, oy); x1, y1 = min(s.w, ox + j.w), min(s.h, oy + j.h)
    sub = (slice(y0, y1), slice(x0, x1)); tl = (slice(y0 - oy, y1 - oy), slice(x0 - ox, x1 - ox))
    al, rgb, zr = al[tl], rgb[tl], zr[tl]
    s.rgb[sub][al] = rgb[al]; s.a[sub] |= al; s.z[sub][al] = zr[al]

def hangar_ramp(s, bx, by, hw, L=42, light=(130, 255, 180), deck_z=2.2, wall_grow=None):
    """Artemis-approved hangar ramp cut into a flight deck, drawn WITH DEPTH: walls widen aft, floor narrows/darkens,
    grip ribs crowd together, guide lights shrink + dim, and the deck overhangs a black tunnel mouth (lit arched lip +
    overhang shadow). (bx, by) = ramp centre, hw = half-width, L = length; fighters drive in toward +y (aft)."""
    from vstyle import spline
    yy_ = s.yy/s.SS; xx_ = s.xx/s.SS
    wg = wall_grow if wall_grow is not None else max(3.0, hw*0.18)
    yA = by - L/2; yM = by + L/2 - 9; yB = by + L/2 - 1
    f = lambda y: np.clip((y - yA)/(yM - yA), 0, 1)
    pit = s.poly([(bx - hw, yA), (bx + hw, yA), (bx + hw, yB), (bx - hw, yB)])
    deck0 = s.rgb.copy()
    s.rgb[pit] = (60, 66, 68); s.a |= pit
    ff = f(yy_)
    for sd in (-1, 1):
        wall = pit & ((xx_ - bx)*sd > hw - wg*ff) & (yy_ < yM + 0.5)
        s.rgb[wall] = (np.array([150, 158, 154])*(1.0 - 0.5*ff[..., None]))[wall]
        s.rgb[wall & ((xx_ - bx)*sd > hw - 0.7)] = (150, 160, 158)
    floor = pit & (np.abs(xx_ - bx) <= hw - wg*ff) & (yy_ < yM)
    s.rgb[floor] = (np.array([96, 106, 104])*(1.0 - 0.72*ff[..., None]))[floor]
    for k in range(9):
        yr = yA + 2 + (yM - yA - 3)*(1 - (1 - k/9)**1.7)
        s.rgb[floor & (np.abs(yy_ - yr) < 0.35)] *= 0.55
    for sd in (-1, 1):
        for k in range(9):
            u = k/9; yl = yA + 3 + (yM - yA - 6)*(1 - (1 - u)**1.5)
            xl = bx + sd*(hw - 3.2 - wg*f(yl)); r_ = 1.25 - 0.55*u
            s.rgb[s.ell(xl, yl, 0.9*r_, 0.8*r_)] = np.array(light)*(1.0 - 0.5*u)
    mouth = pit & (yy_ >= yM - 3.5)
    md = np.clip((yy_ - (yM - 3.5))/4.5, 0, 1)
    s.rgb[mouth] = (np.array([40, 46, 48])*(1 - md[..., None]))[mouth]
    over = s.poly(spline([(bx - hw - 1, yB + 1), (bx - hw - 1, yM + 3), (bx - hw*0.6, yM - 0.5), (bx, yM - 2.5), (bx + hw*0.6, yM - 0.5), (bx + hw + 1, yM + 3), (bx + hw + 1, yB + 1)], 12, False))
    over &= pit
    s.rgb[over] = deck0[over]
    front = over & ~np.roll(over, int(1.3*s.SS), axis=0)
    s.rgb[front] = np.clip(deck0[front]*1.5 + 20, 0, 255)
    mid = over & ~front & ~np.roll(over, int(2.4*s.SS), axis=0); s.rgb[mid] = deck0[mid]*0.8
    sh = pit & ~over & np.roll(over, -int(3.0*s.SS), axis=0); s.rgb[sh] *= 0.5
    s.z[pit] = deck_z - 0.45*ff[pit]; s.z[over] = deck_z + 0.1
    return pit

def iris_hatch(s, x, y, r, metal=(118, 122, 130), accent=(236, 150, 100), z=2.6, petals=6):
    """retractable turret well: a flush armoured ring with a segmented iris door (overlapping petals, centre seam boss) -
    the main gun folds down under it (carrier mode) and rises through it (battleship mode)"""
    yy = s.yy/s.SS; xx = s.xx/s.SS
    rr = np.hypot(xx - x, yy - y); an = (np.degrees(np.arctan2(yy - y, xx - x)) + 360) % 360
    ring = s.disk(x, y, r + 4)
    s.plate(ring, np.array(metal)*0.8, z=z, bevel=2.2, inset=1.4, shadow_k=0.85, notch=0)
    s.rgb[ring & (rr > r + 1.2) & (rr < r + 2.2)] = np.array(accent)*0.9                 # accent ring = gun well marker
    cov = s.disk(x, y, r)
    step = 360.0/petals
    for k in range(petals):
        pet = cov & (((an - k*step + 12*(rr/r)) % 360) < step + 4)                      # swept iris blades
        s.plate(pet, np.array(metal)*(1.0 + 0.05*(k % 2)), z=z + 0.2 + 0.05*k, bevel=1.4, dome=0.4, inset=0.6, shadow_k=0.6, notch=0)
    s.plate(s.disk(x, y, r*0.22), np.array(metal)*1.1, z=z + 0.6, bevel=1.2, dome=0.6, inset=0.6, shadow_k=0.7, notch=0)
    for k in range(12):
        a = np.radians(k*30 + 15); s.rgb[s.disk(x + (r + 2)*np.cos(a), y + (r + 2)*np.sin(a), 0.6)] = (40, 42, 46)

def sunk_mount(s, x, y, r, out_dir, metal=(100, 104, 112), lip_metal=(156, 160, 168), z=2.6, lip_z=3.9, accent=None):
    """weapon mount SUNK into the armour (vanilla protection): octagonal armoured collar, dark socket, turret ring set below
    the collar, and a raised crescent LIP on the exposed side (out_dir = unit vector pointing away from the hull centre)
    that stands higher than the turret base and shadows it."""
    from vstyle import Ship
    yy = s.yy/s.SS; xx = s.xx/s.SS
    R = r + 5
    c8 = s.poly(Ship.mirror_pts([(x - R*0.42, y - R), (x - R, y - R*0.42), (x - R, y + R*0.42), (x - R*0.42, y + R)], x))
    s.plate(c8, np.array(metal), z=z, bevel=1.8, inset=1.2, shadow_k=0.9, notch=0)
    rr = np.hypot(xx - x, yy - y)
    sock = rr < r + 1.4; s.rgb[sock] = (26, 28, 32); s.z[sock] = z - 0.5
    before = s.rgb.copy(); a0 = s.a.copy()
    s.mount(x, y, r, np.array(metal))
    ch = (np.abs(s.rgb - before).sum(2) > 0.5) | (s.a & ~a0); s.z[ch] = z - 0.3
    ox, oy = out_dir; d = ((xx - x)*ox + (yy - y)*oy)/max(1e-6, np.hypot(ox, oy))
    lip = (rr > r + 1.6) & (rr < R + 2.5) & (d > (r + 1.6)*0.35)
    s.plate(lip, np.array(lip_metal), z=lip_z, bevel=1.6, dome=0.5, inset=0.6, shadow_k=0.9, notch=0,
            paint=[(lip & (np.abs(rr - R - 1.2) < 0.9), accent)] if accent is not None else ())
