"""Vanilla-Starsector-like sprite renderer.

What the vanilla sprites do (studied from Paragon / Onslaught / Eagle) and how this module copies it:
  * two materials: smooth painted ARMOUR PLATES on top of dark, dense exposed MACHINERY ("guts")
    -> Ship.guts() fills a region with procedurally kit-bashed machinery; Ship.plate() lays armour over it
  * every plate has its own volume: rounded bevel, crisp dark outline, bright rim on the lit edge,
    soft gradient + weathering mottle, and it casts a shadow onto whatever is under it
  * turret wells are recessed concentric rings; engines are metallic cans with a specular stripe, poking out aft
  * symmetric, crisp at 1x (supersampled, then sharpened)
"""
import numpy as np, cv2
from scipy import ndimage as ndi
from PIL import Image

LIGHT = np.array([-0.55, -0.65, 0.52]); LIGHT = LIGHT/np.linalg.norm(LIGHT)
SYM_CX = None          # set to the ship centre-line (sprite px) for mirror-symmetric lighting
def _sx(xc):
    """mirror factor for sideways highlights: objects right of the centre-line get their highlight mirrored"""
    return -1.0 if (SYM_CX is not None and xc > SYM_CX + 0.5) else 1.0

class Ship:
    def __init__(self, W, H, SS=3, seed=0):
        self.W, self.H, self.SS = W, H, SS
        self.w, self.h = W*SS, H*SS
        self.yy, self.xx = np.mgrid[0:self.h, 0:self.w].astype(np.float32)
        self.rgb = np.zeros((self.h, self.w, 3), np.float32)
        self.a = np.zeros((self.h, self.w), bool)
        self.z = np.zeros((self.h, self.w), np.float32)      # height map (layer units) for the depth pass
        self.auto_z = False; self.zstep = 1.0; self.depth = None
        self.rng = np.random.default_rng(seed)
        self.mottle = self._noise(14, 0.9) + 0.5*self._noise(5, 0.8) + 0.25*self._noise(2, 0.6)
        self.fine = self.rng.normal(0, 1, (self.h, self.w)).astype(np.float32)
        self.fine = cv2.GaussianBlur(self.fine, (0, 0), 0.6*SS)
        self.fine /= self.fine.std() + 1e-6

    def _noise(self, cell, blur):
        g = self.rng.normal(0, 1, (self.H//cell + 2, self.W//cell + 2)).astype(np.float32)
        n = cv2.resize(g, (self.w, self.h), interpolation=cv2.INTER_CUBIC)
        n = cv2.GaussianBlur(n, (0, 0), blur*self.SS)
        return n/(n.std() + 1e-6)

    # ------------------------------------------------------------ masks (sprite-pixel coordinates)
    def rrect(self, x0, y0, x1, y1, r=0.5):
        s = self.SS; x0, y0, x1, y1, r = x0*s, y0*s, x1*s, y1*s, max(r, 0.01)*s
        cx = np.clip(self.xx, x0 + r, x1 - r); cy = np.clip(self.yy, y0 + r, y1 - r)
        return np.hypot(self.xx - cx, self.yy - cy) <= r
    def disk(self, cx, cy, r):
        s = self.SS; return np.hypot(self.xx - cx*s, self.yy - cy*s) <= r*s
    def ell(self, cx, cy, a, b):
        s = self.SS; return ((self.xx - cx*s)/(a*s))**2 + ((self.yy - cy*s)/(b*s))**2 <= 1
    def poly(self, pts):
        m = np.zeros((self.h, self.w), np.uint8)
        cv2.fillPoly(m, [np.array([[x*self.SS, y*self.SS] for x, y in pts], np.int32)], 1, lineType=cv2.LINE_8)
        return m > 0
    @staticmethod
    def mirror_pts(pts, cx):
        return pts + [(2*cx - x, y) for x, y in pts[::-1]]
    def sym(self, m):          # mirror a mask about the sprite centre line
        return m | m[:, ::-1]

    # ------------------------------------------------------------ lighting
    def _shade(self, h, gain=1.5, spec=0.35, sp_pow=18):
        gy, gx = np.gradient(h)
        gx *= self.SS; gy *= self.SS                          # h is in sprite px, gradient per sprite px
        n = np.dstack([-gx, -gy, np.ones_like(gx)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
        nl = (n*LIGHT).sum(2)
        shade = 1 + gain*(nl - LIGHT[2])
        hv = n + np.array([0, 0, 1.0]) + LIGHT; hv /= np.linalg.norm(hv, axis=2, keepdims=True)   # rough Blinn
        sp = np.clip((n*(LIGHT + np.array([0, 0, 1.0]))/np.linalg.norm(LIGHT + [0, 0, 1])).sum(2), 0, 1)**sp_pow*spec
        return np.clip(shade, 0.25, 1.9), sp, nl

    def shadow(self, mask, dx=1.6, dy=2.2, strength=0.6, blur=1.1):
        s = self.SS
        if SYM_CX is not None: dx = 0.0
        m = mask.astype(np.float32)
        M = np.float32([[1, 0, dx*s], [0, 1, dy*s]])
        sh = cv2.warpAffine(m, M, (self.w, self.h))
        sh = cv2.GaussianBlur(sh, (0, 0), blur*s)
        k = (1 - strength*sh)[..., None]
        tgt = ~mask
        self.rgb[tgt] *= k[tgt]

    # ------------------------------------------------------------ armour plate
    def plate(self, mask, color, *a, dz=None, z=None, **k):
        m = self._plate(mask, color, *a, **k)
        if self.auto_z: self.raise_z(mask if m is None else m, dz, z)
        return m

    def _plate(self, mask, color, bevel=3.0, gain=1.8, outline=0.9, tex=0.035, grime=0.03, cast=True,
              paint=(), dome=0.0, spec=0.3, grad=0.24, lines=(), shadow_k=0.6, inset=0.0, jitter=0.04, tilt=(0, 0), ridge=None, notch=0, notch_corners='tl,tr,bl,br'):
        """mask: plate footprint.  color: base RGB.  paint: [(mask, rgb), ...] painted before lighting.
        dome: extra large-scale curvature (sprite px of lift at the plate's middle)."""
        if not mask.any(): return
        s = self.SS
        if notch:                                   # Terra Light signature: stepped double notch on the plate corners
            ys_, xs_ = np.where(mask); X0, X1, Y0, Y1 = xs_.min()/s, (xs_.max() + 1)/s, ys_.min()/s, (ys_.max() + 1)/s
            cut = np.zeros_like(mask)
            for c_ in notch_corners.split(','):
                for k in (1, 2):
                    a_ = notch*k/2; b_ = notch*(3 - k)/2
                    xa = X0 if 'l' in c_ else X1 - a_; ya = Y0 if 't' in c_ else Y1 - b_
                    cut |= self.rrect(xa - 0.01, ya - 0.01, xa + a_ + 0.01, ya + b_ + 0.01, 0.01)
            mask = mask & ~cut
        if cast: self.shadow(mask, strength=shadow_k)
        d = ndi.distance_transform_edt(mask)/s
        t = np.clip(d/bevel, 0, 1); h = bevel*0.55*(1 - (1 - t)**2)
        if dome:
            dd = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 6*s)
            h = h + dome*dd
        col = np.empty((self.h, self.w, 3), np.float32); col[:] = color
        col *= 1 + self.rng.normal(0, jitter)
        for pm, pc in paint:
            col[pm & mask] = pc
        # engraved panel lines: a dark groove with a light lip under it
        for lm in lines:
            lm = lm & mask
            h = h - 0.35*lm
        if tilt != (0, 0) or ridge:                 # faceted surfaces: planar tilt and/or a ridge line
            yy0, xx0 = np.where(mask); mx, my = xx0.mean()/s, yy0.mean()/s
            h = h + np.where(mask, tilt[0]*(self.xx/s - mx) + tilt[1]*(self.yy/s - my), 0)
            if ridge:                               # ('x', centre, lift, halfwidth) or ('y', ...)
                ax, c0, lift, hw = ridge
                q = (self.xx/s if ax == 'x' else self.yy/s) - c0
                h = h + np.where(mask, lift*np.clip(1 - np.abs(q)/hw, 0, 1), 0)
        if inset:                                   # engraved contour line running parallel to the plate edge
            h = h - 0.4*(mask & (np.abs(d - inset) < 0.33))
        shade, sp, nl = self._shade(h, gain, spec)
        # soft gradient: lighter towards the upper-left of each plate
        ys, xs = np.where(mask)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        gy = (self.yy - y0)/max(y1 - y0, 1); gx = (self.xx - x0)/max(x1 - x0, 1)
        g = 1 + grad*(0.5 - 0.75*gy - 0.25*gx)
        mot = 1 + tex*self.mottle + 0.018*self.fine
        c = col*(shade*g*mot)[..., None] + 255*sp[..., None]
        # grime: darker blotches where the low-frequency noise is high
        c *= (1 - grime*np.clip(self.mottle - 0.8, 0, 2))[..., None]
        c *= (0.8 + 0.2*np.clip(d/4.0, 0, 1))[..., None]          # plates darken towards their edges (vanilla-like falloff)
        # rim light on lit edges, dark outline on all edges
        rim = mask & (d > outline) & (d < outline + 0.9) & (nl > LIGHT[2] + 0.05)
        c[rim] = np.minimum(c[rim]*1.28 + 12, 255)
        if inset:                                   # double contour: light line just inside the engraved one
            li = mask & (np.abs(d - inset - 0.75) < 0.3); c[li] = np.minimum(c[li]*1.2 + 10, 255)
        edge = mask & (d <= outline)
        c[edge] = c[edge]*0.28
        self.rgb[mask] = c[mask]; self.a |= mask
        return mask

    def engrave(self, mask, depth=0.5, light_lip=True):
        """cut a thin line into whatever is already painted"""
        s = self.SS
        self.rgb[mask] *= depth
        if light_lip:
            M = np.float32([[1, 0, 0], [0, 1, 0.8*s]])
            lip = cv2.warpAffine(mask.astype(np.uint8), M, (self.w, self.h)) > 0
            lip &= ~mask & self.a
            self.rgb[lip] = np.minimum(self.rgb[lip]*1.18 + 6, 255)

    # ------------------------------------------------------------ machinery
    def guts(self, mask, seed=1, tone=(74, 76, 80), minc=3, maxc=11, mirror=True, cast=False):
        """dense dark kit-bash machinery: boxes, grilles, pipe runs, ports, recesses, in a BSP of small cells"""
        if not mask.any(): return
        s = self.SS; rng = np.random.default_rng(seed)
        ys, xs = np.where(mask)
        X0, X1, Y0, Y1 = xs.min()//s, xs.max()//s + 1, ys.min()//s, ys.max()//s + 1
        if mirror: X1 = min(X1, self.W//2 + 1)
        hm = np.zeros((self.h, self.w), np.float32); tm = np.full((self.h, self.w), 0.8, np.float32)
        cells = []
        def split(x0, y0, x1, y1, d):
            w, h = x1 - x0, y1 - y0
            if (w <= maxc and h <= maxc and rng.random() < 0.55) or (w < 2*minc and h < 2*minc) or d > 12:
                cells.append((x0, y0, x1, y1)); return
            if (h >= w and h >= 2*minc) or w < 2*minc:
                k = int(rng.integers(y0 + minc, y1 - minc + 1)); split(x0, y0, x1, k, d + 1); split(x0, k, x1, y1, d + 1)
            else:
                k = int(rng.integers(x0 + minc, x1 - minc + 1)); split(x0, y0, k, y1, d + 1); split(k, y0, x1, y1, d + 1)
        split(int(X0), int(Y0), int(X1), int(Y1), 0)
        for (x0, y0, x1, y1) in cells:
            a0, a1, b0, b1 = x0*s, x1*s, y0*s, y1*s
            ly, lx = np.mgrid[b0:b1, a0:a1].astype(np.float32)
            u = (lx - a0 + 0.5)/(a1 - a0); v = (ly - b0 + 0.5)/(b1 - b0)
            w, h = x1 - x0, y1 - y0
            r = rng.random()
            if r < 0.34:                                   # raised box, maybe with a lid line / bolts
                e = np.minimum(np.minimum(u, 1 - u)*w, np.minimum(v, 1 - v)*h)
                lift = rng.uniform(0.6, 1.8)
                hh = lift*np.clip(e/0.9, 0, 1); tt = rng.uniform(0.75, 1.35)
                if rng.random() < 0.4 and min(w, h) >= 5:
                    hh = hh - 0.4*((np.abs(v - 0.5)*h < 0.35) if h > w else (np.abs(u - 0.5)*w < 0.35))
            elif r < 0.52:                                 # grille / vent slats
                per = rng.choice([1.5, 2.0])
                if h >= w: hh = 0.5*(((ly/s) % per) < per/2)
                else:      hh = 0.5*(((lx/s) % per) < per/2)
                hh = hh.astype(np.float32); tt = rng.uniform(0.55, 0.85)
            elif r < 0.70:                                 # pipe bundle along the long axis
                pw = rng.choice([1.6, 2.2, 3.0])
                q = ((ly/s) if w > h else (lx/s)) % pw
                hh = 0.9*np.sqrt(np.clip(1 - ((q - pw/2)/(pw/2))**2, 0, 1)); tt = rng.uniform(1.0, 1.45)
            elif r < 0.82 and min(w, h) >= 4:              # round port / small mount
                cx, cy = (a0 + a1)/2, (b0 + b1)/2; rr = min(w, h)*s/2 - 0.4*s
                dd = np.hypot(lx - cx, ly - cy)/max(rr, 1)
                hh = np.where(dd < 1, 0.9 - 0.6*(np.abs(dd - 0.6) < 0.18) - 0.5*(dd < 0.3), 0.2).astype(np.float32)
                tt = rng.uniform(0.9, 1.3)
            else:                                          # dark recess
                hh = np.full(lx.shape, -0.6, np.float32); tt = rng.uniform(0.35, 0.55)
            # cell borders read as seams
            border = (np.minimum(np.minimum(u, 1 - u)*w, np.minimum(v, 1 - v)*h) < 0.35)
            hm[b0:b1, a0:a1] = np.where(border, -0.3, hh)
            tm[b0:b1, a0:a1] = np.where(border, 0.45, tt)
        if mirror:
            half = self.w//2
            hm[:, half:] = hm[:, :half][:, ::-1][:, :self.w - half]; tm[:, half:] = tm[:, :half][:, ::-1][:, :self.w - half]
        hb = cv2.GaussianBlur(hm, (0, 0), 0.35*s)
        shade, sp, nl = self._shade(hb, gain=1.25, spec=0.35, sp_pow=12)
        c = np.array(tone, np.float32)[None, None, :]*(tm*shade)[..., None] + 255*sp[..., None]
        c *= (1 + 0.04*self.fine)[..., None]
        if cast: self.shadow(mask)
        self.rgb[mask] = np.clip(c[mask], 0, 255); self.a |= mask

    # ------------------------------------------------------------ parts
    def mount(self, x, y, r, rim_col, well_col=(58, 60, 64), cast=True):
        """recessed turret well: bevelled outer collar, dark groove, detailed inner ring, centre cap"""
        s = self.SS
        m = self.disk(x, y, r)
        if cast: self.shadow(m, 0.8, 1.1, 0.4)
        dd = np.hypot(self.xx - x*s, self.yy - y*s)/(r*s)
        hh = np.select([dd > 0.82, dd > 0.72, dd > 0.46, dd > 0.40, dd > 0.14],
                       [0.9*np.sin(np.clip((1 - dd)/0.18, 0, 1)*np.pi/2) + 0.2, -0.4, 0.1 - 0.25*(np.abs(dd - 0.6) < 0.04), -0.3, 0.35],
                       0.55).astype(np.float32)
        hh = cv2.GaussianBlur(hh, (0, 0), 0.3*s)
        shade, sp, nl = self._shade(hh, 1.4, 0.4)
        col = np.where((dd > 0.82)[..., None], np.array(rim_col, np.float32), np.array(well_col, np.float32))
        col = np.where(((dd > 0.72) & (dd <= 0.82))[..., None], np.array([30, 30, 34], np.float32), col)
        c = col*shade[..., None] + 255*sp[..., None]
        # notch marks on the inner ring
        ang = np.arctan2(self.yy - y*s, self.xx - x*s)
        notch = (dd > 0.47) & (dd < 0.7) & ((np.degrees(ang) % 30) < 4)
        c[notch] *= 0.55
        edge = m & (dd > 0.94); c[edge] *= 0.35
        self.rgb[m] = c[m]; self.a |= m

    def nozzle(self, x, y0, y1, w, color=(150, 146, 150), cast=True):
        """engine can seen from above: metallic cylinder with a specular stripe, ring bands, flared lip at the end"""
        s = self.SS
        m = self.rrect(x - w/2, y0, x + w/2, y1, min(w/2, 3)) | self.rrect(x - w/2 - 0.8, y1 - 3, x + w/2 + 0.8, y1, 1.2)
        if cast: self.shadow(m, 1.2, 1.2, 0.5)
        u = np.clip((self.xx/s - x)/(w/2 + 0.8), -1, 1)*_sx(x)
        cyl = np.sqrt(np.clip(1 - u**2, 0, 1))
        lum = 0.25 + 0.7*cyl*(1 - 0.4*u) + 0.7*np.exp(-((u + 0.4)/0.12)**2)     # specular stripe left of centre
        band = ((np.abs(self.yy/s - (y1 - 6)) < 0.6) | (np.abs(self.yy/s - (y1 - 9)) < 0.6) | (np.abs(self.yy/s - (y0 + 3)) < 0.6))
        lum = lum*np.where(band, 0.62, 1.0)
        lum = np.where(self.yy/s > y1 - 3, lum*0.8, lum)
        c = np.array(color, np.float32)[None, None, :]*lum[..., None]
        edge = m & ~ndi.binary_erosion(m, iterations=max(1, int(0.8*s)))
        c[edge] *= 0.3
        self.rgb[m] = np.clip(c[m], 0, 255); self.a |= m

    def lights(self, pts, cols):
        for (x, y), col in zip(pts, cols):
            g = self.disk(x, y, 1.6); self.rgb[g] = self.rgb[g]*0.4 + np.array(col)*0.6
            self.rgb[self.disk(x, y, 0.8)] = np.minimum(np.array(col)*1.2 + 40, 255)

    def windows(self, x0, x1, y, mask, step=2.4, lit=(255, 222, 160), frac=0.8, seed=3):
        rng = np.random.default_rng(seed)
        for x in np.arange(x0, x1, step):
            m = self.rrect(x, y, x + 1.2, y + 1.2, 0.2) & mask
            self.rgb[m] = lit if rng.random() < frac else self.rgb[m]*0.25

    def stencil(self, x, y, text_bits, h=5, col=(40, 40, 44), mask=None, seed=0):
        """blocky stencil glyphs (hull numbers)"""
        rng = np.random.default_rng(seed)
        cx = x
        for _ in range(text_bits):
            g = rng.integers(0, 4)
            if g == 0:   m = self.rrect(cx, y, cx + 3, y + h, 0.3) & ~self.rrect(cx + 1, y + 1, cx + 2, y + h - 1, 0.1)
            elif g == 1: m = self.rrect(cx, y, cx + 3, y + 1.1, 0.2) | self.rrect(cx + 1, y, cx + 2.1, y + h, 0.2)
            elif g == 2: m = self.rrect(cx, y, cx + 1.1, y + h, 0.2) | self.rrect(cx + 1.9, y, cx + 3, y + h, 0.2) | self.rrect(cx, y + h/2 - 0.5, cx + 3, y + h/2 + 0.5, 0.2)
            else:        m = self.rrect(cx, y, cx + 3, y + 1.1, 0.2) | self.rrect(cx, y + h - 1.1, cx + 3, y + h, 0.2) | self.rrect(cx, y, cx + 1.1, y + h, 0.2)
            if mask is not None: m &= mask
            self.rgb[m] = self.rgb[m]*0.3 + np.array(col)*0.7
            cx += 4.3

    def hazard(self, x0, y0, x1, y1, mask=None, period=4):
        m = self.rrect(x0, y0, x1, y1, 0.2)
        if mask is not None: m &= mask
        band = (((self.xx + self.yy)/self.SS) % period) < period/2
        lum = self.rgb.mean(2, keepdims=True)/140
        self.rgb[m & band] = (np.array([214, 176, 60])*lum)[m & band]
        self.rgb[m & ~band] = (np.array([46, 44, 42])*lum)[m & ~band]

    # ------------------------------------------------------------ output
    def raise_z(self, mask, dz=None, z=None):
        """put a part on its own layer: z = (what it sits on) + dz, or an absolute z"""
        if mask is None or not mask.any(): return
        if z is None:
            under = self.z[mask]; z = float(np.percentile(under, 70)) + (self.zstep if dz is None else dz)
        self.z[mask] = z

    def depth_pass(self, unit=2.2, sdir=(0.42, 0.91), s_str=0.62, tint=0.30, ao=0.38, ao_r=3.5, s_soft=0.7):
        """vanilla-like layering: parts on higher layers cast soft shadows (light from upper-left) onto lower ones,
        higher layers read lighter, crevices between layers get ambient occlusion."""
        S = self.SS; z = self.z*self.a; zmax = max(1e-3, float(z.max()))
        dirs = [sdir] if np.ndim(sdir[0]) == 0 else list(sdir)      # one direction, or several (e.g. a symmetric pair)
        sha = np.zeros_like(z); step = 1.0                          # supersampled px per march step
        n = int(zmax*unit*S*1.6/step) + 1
        for dd in dirs:
            d = np.array(dd, np.float32); d /= np.linalg.norm(d)
            hs = z.copy()
            for k in range(1, n + 1):
                M = np.float32([[1, 0, d[0]*k*step], [0, 1, d[1]*k*step]])
                sh = cv2.warpAffine(z, M, (self.w, self.h), borderValue=0) - k*step/(unit*S)
                np.maximum(hs, sh, out=hs)
            np.maximum(sha, np.clip((hs - z)/0.55, 0, 1), out=sha)
        sha = cv2.GaussianBlur(sha, (0, 0), s_soft*S)
        zb = cv2.GaussianBlur(z, (0, 0), ao_r*S)
        occ = np.clip((zb - z)/1.4, 0, 1)
        lift = (1 - tint) + tint*np.clip(z/zmax, 0, 1)**0.8/0.85
        k = lift*(1 - s_str*sha)*(1 - ao*occ)
        self.rgb[self.a] *= k[self.a][:, None]

    def render(self, sharpen=0.55):
        if self.depth is not None: self.depth_pass(**self.depth)
        a = self.a.astype(np.float32)
        out = np.dstack([self.rgb*a[..., None], a*255])
        out = cv2.resize(out, (self.W, self.H), interpolation=cv2.INTER_AREA)
        al = out[..., 3:4]/255
        rgb = np.where(al > 0, out[..., :3]/np.maximum(al, 1e-6), 0)
        if sharpen:
            bl = cv2.GaussianBlur(rgb, (0, 0), 0.8)
            rgb = rgb + sharpen*(rgb - bl)
        return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), out[..., 3:4]]).astype(np.uint8), 'RGBA')

def _occupy_ok(occ, s, x0, y0, x1, y1):
    a, b, c, d = int(x0*s), int(np.ceil(x1*s)), int(y0*s), int(np.ceil(y1*s))
    if a < 0 or c < 0 or b > occ.shape[1] or d > occ.shape[0]: return False
    return occ[c:d, a:b].all()

def plate_details(self, mask, n=30, seed=0, mirror=True, erode=3.0, kinds=(0.34, 0.26, 0.2, 0.12, 0.08), occ=None):
    """small surface hardware on top of plates, like vanilla sprites: engraved sub-panels, ports, vent slots,
    raised mini-boxes, bolt pairs.  Placed on the left half and mirrored."""
    s = self.SS; rng = np.random.default_rng(seed)
    occ = ndi.binary_erosion(mask, iterations=max(1, int(erode*s))) if occ is None else occ.copy()
    ys, xs = np.where(occ)
    if mirror:
        k = xs < self.w//2 - 2*s; ys, xs = ys[k], xs[k]
    if len(xs) == 0: return
    def place(fn, x0, y0, x1, y1):
        spots = [(x0, y0, x1, y1)]
        if mirror: spots.append((self.W - x1, y0, self.W - x0, y1))
        if not all(_occupy_ok(occ, s, *sp) for sp in spots): return False
        for sp in spots:
            fn(*sp); occ[int(sp[1]*s) - s:int(sp[3]*s) + s, int(sp[0]*s) - s:int(sp[2]*s) + s] = False
        return True
    def panel(x0, y0, x1, y1):
        m = self.rrect(x0, y0, x1, y1, 0.8); inner = self.rrect(x0 + 0.7, y0 + 0.7, x1 - 0.7, y1 - 0.7, 0.5)
        self.engrave(m & ~inner, 0.5); self.rgb[inner] *= rng.choice([0.9, 0.95, 1.06])
    def port(x0, y0, x1, y1):
        cx, cy, r = (x0 + x1)/2, (y0 + y1)/2, (x1 - x0)/2
        self.rgb[self.disk(cx, cy, r)] *= 0.45
        self.rgb[self.disk(cx - 0.3, cy - 0.3, r*0.62)] = np.minimum(self.rgb[self.disk(cx - 0.3, cy - 0.3, r*0.62)]*1.9 + 10, 255)
        self.rgb[self.disk(cx, cy, r*0.3)] *= 0.5
    def slots(x0, y0, x1, y1):
        for yy in np.arange(y0, y1 - 0.8, 1.8):
            self.engrave(self.rrect(x0, yy, x1, yy + 0.9, 0.3), 0.35)
    def box(x0, y0, x1, y1):
        m = self.rrect(x0, y0, x1, y1, 0.6)
        self.shadow(m, 0.8, 1.0, 0.45, 0.6)
        base = self.rgb[m].mean(0)
        self.rgb[m] = base*0.95
        tl = m & ~self.rrect(x0 + 0.8, y0 + 0.8, x1 + 2, y1 + 2, 0.3); br_ = m & ~self.rrect(x0 - 2, y0 - 2, x1 - 0.8, y1 - 0.8, 0.3)
        self.rgb[tl] = np.minimum(self.rgb[tl]*1.3 + 8, 255); self.rgb[br_] *= 0.5
    def bolts(x0, y0, x1, y1):
        for bx in (x0 + 0.8, x1 - 0.8):
            m = self.disk(bx, (y0 + y1)/2, 0.7); self.rgb[m] = self.rgb[m]*0.45
    fns = (panel, port, slots, box, bolts)
    placed = tries = 0
    while placed < n and tries < n*40:
        tries += 1
        i = rng.integers(0, len(xs)); x, y = xs[i]/s, ys[i]/s
        kind = rng.choice(5, p=kinds)
        if kind == 0:   w, h = rng.uniform(6, 16), rng.uniform(5, 14)
        elif kind == 1: w = h = rng.uniform(3, 6)
        elif kind == 2: w, h = rng.uniform(4, 9), rng.uniform(4, 8)
        elif kind == 3: w, h = rng.uniform(3, 7), rng.uniform(3, 8)
        else:           w, h = rng.uniform(4, 7), 1.6
        if place(fns[kind], x - w/2, y - h/2, x + w/2, y + h/2): placed += 1
Ship.plate_details = plate_details

# ---------------------------------------------------------------- functional parts (every detail has a job)
def cylinder(self, x0, y0, x1, y1, color, axis='v', bands=(), cast=True, outline=0.8, caps=None):
    """a tank / capacitor / pipe lying on the deck: cylinder shading across its short axis, ring bands, optional end caps"""
    s = self.SS
    r = min(x1 - x0, y1 - y0)/2
    m = self.rrect(x0, y0, x1, y1, r*0.9)
    if cast: self.shadow(m, 1.0, 1.4, 0.5, 0.9)
    if axis == 'v': u = np.clip((self.xx/s - (x0 + x1)/2)/((x1 - x0)/2), -1, 1)*_sx((x0 + x1)/2); along = self.yy/s
    else:           u = np.clip((self.yy/s - (y0 + y1)/2)/((y1 - y0)/2), -1, 1); along = self.xx/s
    cyl = np.sqrt(np.clip(1 - u**2, 0, 1))
    lum = 0.3 + 0.72*cyl*(1 - 0.35*u) + 0.55*np.exp(-((u + 0.42)/0.16)**2)
    for b in bands: lum = np.where(np.abs(along - b) < 0.6, lum*0.55, lum)
    c = np.array(color, np.float32)[None, None, :]*lum[..., None]
    if caps is not None:
        cm = m & ((along < (y0 if axis == 'v' else x0) + 2.2) | (along > (y1 if axis == 'v' else x1) - 2.2))
        c[cm] = np.array(caps, np.float32)*(0.6 + 0.6*cyl[cm])[:, None]
    e = m & ~ndi.binary_erosion(m, iterations=max(1, int(outline*s))); c[e] *= 0.3
    self.rgb[m] = np.clip(c[m], 0, 255); self.a |= m
    return m

def grille(self, mask, period=2.0, axis='h', depth=0.4):
    """radiator / vent fins: alternating lit fin tops and dark gaps across the mask"""
    s = self.SS
    q = ((self.yy if axis == 'h' else self.xx)/s) % period
    fin = mask & (q < period*0.55); gap = mask & ~fin
    self.rgb[gap] *= depth
    top = fin & (q < 0.5); self.rgb[top] = np.minimum(self.rgb[top]*1.3 + 10, 255)

def reactor(self, x, y, r, shell, glow=(110, 170, 255)):
    """reactor housing: domed armoured ring, radial cooling fins, glowing core window"""
    s = self.SS
    m = self.disk(x, y, r)
    self.plate(m, shell, bevel=3, dome=2.0, inset=2.5, shadow_k=0.7)
    rr = np.hypot(self.xx/s - x, self.yy/s - y); ang = np.degrees(np.arctan2(self.yy/s - y, self.xx/s - x))
    fins = m & (rr > r*0.55) & (rr < r*0.9) & ((ang % 20) < 7)
    self.rgb[fins] *= 0.55
    ring = m & (rr < r*0.55) & (rr > r*0.42); self.rgb[ring] = (30, 32, 36)
    core = m & (rr <= r*0.42)
    t = np.clip(1 - rr/(r*0.42), 0, 1)[..., None]
    self.rgb[core] = (np.array(glow)*(0.55 + 0.45*t) + 255*0.35*t**2)[core]

def hatch(self, x0, y0, x1, y1, haz=True):
    """airlock / cargo hatch: recessed door with a hazard frame and a handle"""
    m = self.rrect(x0, y0, x1, y1, 0.8)
    if haz: self.hazard(x0, y0, x1, y1, m, period=2.4)
    inner = self.rrect(x0 + 1.4, y0 + 1.4, x1 - 1.4, y1 - 1.4, 0.5)
    self.rgb[inner] = self.rgb[inner]*0 + (82, 86, 94)
    self.engrave(inner & ~self.rrect(x0 + 2.1, y0 + 2.1, x1 - 2.1, y1 - 2.1, 0.4), 0.4)
    cx = (x0 + x1)/2; self.rgb[self.rrect(cx - 1.5, (y0 + y1)/2 - 0.5, cx + 1.5, (y0 + y1)/2 + 0.5, 0.2)] = (150, 154, 160)

def rcs(self, x, y, dirs, base):
    """manoeuvring thruster quad: small housing with nozzle bells pointing in dirs ('u','d','l','r')"""
    m = self.rrect(x - 3, y - 3, x + 3, y + 3, 1)
    self.plate(m, base, bevel=1.2, outline=0.5, shadow_k=0.5)
    for d in dirs:
        if d in 'ud':
            ny = y - 4.2 if d == 'u' else y + 4.2
            n = self.rrect(x - 1.3, ny - 1.3, x + 1.3, ny + 1.3, 0.4)
        else:
            nx = x - 4.2 if d == 'l' else x + 4.2
            n = self.rrect(nx - 1.3, y - 1.3, nx + 1.3, y + 1.3, 0.4)
        self.rgb[n] = (40, 40, 44); self.a |= n

Ship.cylinder = cylinder; Ship.grille = grille; Ship.reactor = reactor; Ship.hatch = hatch; Ship.rcs = rcs

# ---------------------------------------------------------------- smooth outlines, cables, connectors, armour bolts
def spline(pts, n=24, closed=True):
    """Catmull-Rom through pts -> dense point list (for smooth, non-blocky outlines)"""
    P = np.array(pts, np.float32)
    if closed: P = np.vstack([P[-1], P, P[0], P[1]])
    else:      P = np.vstack([P[0], P, P[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t*t, t*t*t
            out.append(0.5*((2*p1) + (-p0 + p2)*t + (2*p0 - 5*p1 + 4*p2 - p3)*t2 + (-p0 + 3*p1 - 3*p2 + p3)*t3))
    if not closed: out.append(P[-2])
    return [tuple(p) for p in out]

def spoly(self, pts, n=24):
    return self.poly(spline(pts, n, True))

def cable(self, pts, width, color, clamps=10.0, clamp_col=None, cast=True, smooth=True):
    """a cable / pipe bundle laid over the hull: rounded tube shading, cast shadow, clamps every `clamps` px"""
    s = self.SS
    path = spline(pts, 16, closed=False) if smooth and len(pts) > 2 else pts
    m8 = np.zeros((self.h, self.w), np.uint8)
    cv2.polylines(m8, [np.array([[x*s, y*s] for x, y in path], np.int32)], False, 1, thickness=max(1, int(width*s)), lineType=cv2.LINE_8)
    m = m8 > 0
    self.plate(m, np.array(color), bevel=width/2, outline=0.5, cast=cast, shadow_k=0.55, tex=0.0, grime=0.0, grad=0.0, jitter=0.0, spec=0.45)
    if clamps:
        L = 0.0; acc = clamps/2
        for (x0, y0), (x1, y1) in zip(path[:-1], path[1:]):
            seg = np.hypot(x1 - x0, y1 - y0); t = acc
            while t < seg:
                cx, cy = x0 + (x1 - x0)*t/seg, y0 + (y1 - y0)*t/seg
                nx, ny = -(y1 - y0)/seg, (x1 - x0)/seg
                a = (width/2 + 0.9)
                q = [(cx + nx*a - (x1 - x0)/seg*0.8, cy + ny*a - (y1 - y0)/seg*0.8), (cx + nx*a + (x1 - x0)/seg*0.8, cy + ny*a + (y1 - y0)/seg*0.8),
                     (cx - nx*a + (x1 - x0)/seg*0.8, cy - ny*a + (y1 - y0)/seg*0.8), (cx - nx*a - (x1 - x0)/seg*0.8, cy - ny*a - (y1 - y0)/seg*0.8)]
                cm = self.poly(q)
                self.rgb[cm] = clamp_col if clamp_col is not None else np.array(color)*0.55
                self.rgb[cm & ~ndi.binary_erosion(cm, iterations=1)] *= 0.5
                t += clamps
            acc = t - seg
    return m

def connector(self, x, y, r, body=(110, 114, 122), ring=(200, 150, 60)):
    """round socket where a cable plugs into a module: collar, coloured locking ring, bolts"""
    m = self.disk(x, y, r)
    self.plate(m, np.array(body), bevel=r*0.6, dome=0.4, outline=0.5, shadow_k=0.5)
    rr = np.hypot(self.xx/self.SS - x, self.yy/self.SS - y)
    self.rgb[m & (rr > r*0.45) & (rr < r*0.65)] = ring
    self.rgb[m & (rr <= r*0.3)] = (34, 36, 40)

def bolt_row(self, mask, inset=1.8, spacing=4.0, seed=0):
    """armour bolts along the inside of a plate's edge (the plate is bolted to the frame)"""
    s = self.SS
    d = ndi.distance_transform_edt(mask)/s
    band = mask & (np.abs(d - inset) < 0.25)
    ys, xs = np.where(band)
    if len(xs) == 0: return
    order = np.lexsort((xs, ys)); pts = np.stack([xs[order], ys[order]], 1)/s
    taken = np.zeros((0, 2), np.float32)
    for (x, y) in pts:
        if len(taken) == 0 or (((taken[:, 0] - x)**2 + (taken[:, 1] - y)**2) > spacing**2).all():
            taken = np.vstack([taken, [x, y]])
    for (x, y) in taken:
        self.rgb[self.disk(x, y, 0.75)] *= 0.62
        tl = self.disk(x - 0.35, y - 0.35, 0.35); self.rgb[tl] = np.minimum(self.rgb[tl]*1.15 + 4, 255)

Ship.spoly = spoly; Ship.cable = cable; Ship.connector = connector; Ship.bolt_row = bolt_row


# ---------------------------------------------------------------- Terra Light identity parts
def channel(self, pts, width, light=(120, 180, 255), step=5.0, nodes=True, smooth=False):
    """recessed conduit channel (DA-style routing, TL look): dark trench with a bevelled lip, running lights along
    both walls, and TL 'node rings' at every bend. Cables can then be laid inside it."""
    s = self.SS
    path = spline(pts, 12, closed=False) if smooth and len(pts) > 2 else pts
    m8 = np.zeros((self.h, self.w), np.uint8)
    cv2.polylines(m8, [np.array([[x*s, y*s] for x, y in path], np.int32)], False, 1, thickness=max(1, int(width*s)), lineType=cv2.LINE_8)
    for (x, y) in path: cv2.circle(m8, (int(x*s), int(y*s)), int(width*s/2), 1, -1)
    m = m8 > 0
    d = ndi.distance_transform_edt(m)/s
    self.rgb[m] = (26, 28, 32)
    lip = m & (d < 0.8); self.rgb[lip] = (12, 12, 14)
    M_ = np.float32([[1, 0, 0], [0, 1, 0.9*s]])
    sh = (cv2.warpAffine(m.astype(np.uint8), M_, (self.w, self.h)) > 0) & ~m & self.a
    self.rgb[sh] = np.minimum(self.rgb[sh]*1.15 + 8, 255)                     # lit lower lip of the trench
    self.a |= m
    acc = 0.0
    for (x0, y0), (x1, y1) in zip(path[:-1], path[1:]):
        seg = np.hypot(x1 - x0, y1 - y0); t = step/2 - acc
        while t < seg:
            cx, cy = x0 + (x1 - x0)*t/seg, y0 + (y1 - y0)*t/seg
            nx, ny = -(y1 - y0)/seg, (x1 - x0)/seg
            for sg in (-1, 1):
                lx, ly = cx + sg*nx*(width/2 - 1.1), cy + sg*ny*(width/2 - 1.1)
                self.rgb[self.disk(lx, ly, 0.55)] = light
            t += step
        acc = (seg - (t - step)) % step
    if nodes:
        for (x, y) in pts[1:-1]:
            rr = np.hypot(self.xx/s - x, self.yy/s - y)
            ring = (rr < width/2 + 1.6) & (rr > width/2 + 0.2)
            self.rgb[ring] = (150, 156, 166); self.rgb[(rr <= width/2 + 1.6) & (rr > width/2 + 1.1)] = (60, 62, 68)
            self.rgb[self.disk(x, y, 0.9)] = light
    return m

def livery(self, mask, region, color, keep=0.35):
    """one paint job across the whole hull: tint every armour pixel inside `region` (keeps the shading)"""
    m = mask & region
    lum = self.rgb[m].mean(1, keepdims=True)/150.0
    self.rgb[m] = self.rgb[m]*keep + np.array(color, np.float32)*lum*(1 - keep)

def emblem(self, x, y, r, col=(230, 232, 236), dark=(40, 60, 110)):
    """Terra Light emblem: a planet disc with the light of a rising sun on its horizon ('Earth Light')."""
    s = self.SS
    rr = np.hypot(self.xx/s - x, self.yy/s - y)
    self.rgb[rr < r] = dark
    self.rgb[(rr < r) & (rr > r - 0.9)] = col
    sun = (np.hypot(self.xx/s - x, self.yy/s - (y + r*0.35)) < r*0.42) & (self.yy/s < y + r*0.25)
    self.rgb[sun & (rr < r - 0.9)] = (255, 214, 120)
    hz = (np.abs(self.yy/s - (y + r*0.25)) < 0.45) & (rr < r - 0.9)
    self.rgb[hz] = col

Ship.channel = channel; Ship.livery = livery; Ship.emblem = emblem

def drive_core(self, x, y, r, shell=(100, 104, 114), glow=(120, 185, 255), spin=0.0):
    """engine-like drive core seen from above: armoured bolted rim, turbine blade ring, stator ring,
    glowing hub with spinner, 4 support struts. `spin` (deg) rotates the blades (for animation)."""
    s = self.SS
    m = self.disk(x, y, r)
    self.plate(m, np.array(shell), bevel=3, dome=1.2, inset=2.4, shadow_k=0.8)
    rr = np.hypot(self.xx/s - x, self.yy/s - y); an = (np.degrees(np.arctan2(self.yy/s - y, self.xx/s - x)) - spin) % 360
    for a_ in range(0, 360, 20):
        bx, by = x + (r - 1.4)*np.cos(np.radians(a_)), y + (r - 1.4)*np.sin(np.radians(a_))
        self.rgb[self.disk(bx, by, 0.6)] = (38, 40, 44)
    well = rr < r*0.82; self.rgb[well] = (24, 26, 30)
    blades = well & (rr > r*0.42) & (((an + (rr/r)*55) % 15) < 7.5)                       # swept turbine blades
    tb = np.clip((rr - r*0.42)/(r*0.4), 0, 1)
    self.rgb[blades] = (np.array([150, 156, 168])*(0.65 + 0.5*tb[..., None]))[blades]
    self.rgb[well & (np.abs(rr - r*0.42) < 0.5)] = (180, 186, 196)                           # stator ring
    for a_ in (45, 135, 225, 315):                                                            # support struts
        st = well & (np.abs(((np.degrees(np.arctan2(self.yy/s - y, self.xx/s - x)) - a_ + 180) % 360) - 180) < 3.5) & (rr > r*0.3)
        self.rgb[st] = (120, 124, 132)
    hub = rr < r*0.34
    t = np.clip(1 - rr/(r*0.34), 0, 1)[..., None]
    self.rgb[hub] = (np.array(glow)*(0.6 + 0.4*t) + 255*0.45*t**2)[hub]
    self.rgb[rr < r*0.12] = (230, 240, 255)
    ring = (rr > r*0.82) & (rr < r*0.86); self.rgb[ring] = (glow[0]*0.6, glow[1]*0.6, glow[2]*0.8)
    self.a |= m
Ship.drive_core = drive_core
