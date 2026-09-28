"""Split-render helpers: render a ship's moving/removable parts as separate sprites on the same canvas.

Usage inside a ship script (see vs_hellhound4.py):
    ctx = SplitCtx(s, active)            # active = set of part names drawn in this run
    with ctx('tower'): ...drawing...     # a section owned by part 'tower'
Excluded sections still RUN (so s.rng is consumed exactly as in the full ship and every other plate keeps its jitter),
but their rgb/alpha/z writes are rolled back afterwards.

Lighting: each part is lit by the renderer's depth pass computed on an 'effective' height map = the part's own z where
the part is, and the full ship's z around it (so it gets the same shadows/AO it has in the full ship).  The hull is lit
alone (no other part's shadow baked in); shadows a part casts onto the parts below it go into that part's sprite as a
soft black semi-transparent fringe."""
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as ndi


class SplitCtx:
    def __init__(self, s, active):
        self.s, self.active = s, set(active)
    def __call__(self, name):
        return _Sec(self, name)
    def on(self, name):
        return name in self.active


class _Sec:
    def __init__(self, ctx, name): self.ctx, self.name = ctx, name
    def __enter__(self):
        s = self.ctx.s
        self.snap = None if self.ctx.on(self.name) else (s.rgb.copy(), s.a.copy(), s.z.copy())
        return self
    def __exit__(self, *exc):
        if self.snap is not None:
            s = self.ctx.s; s.rgb[:], s.a[:], s.z[:] = self.snap
        return False


def depth_k(S, z, a, zmax=None, unit=2.2, sdir=(0.42, 0.91), s_str=0.62, tint=0.30, ao=0.38, ao_r=3.5, s_soft=0.7):
    """same maths as vstyle.Ship.depth_pass, but returns the per-pixel multiplier instead of applying it"""
    h, w = z.shape
    z = z*a; zmax = max(1e-3, float(z.max()) if zmax is None else zmax)      # zmax: the FULL ship's (sets the height-lift scale)
    dirs = [sdir] if np.ndim(sdir[0]) == 0 else list(sdir)
    sha = np.zeros_like(z); step = 1.0
    n = int(zmax*unit*S*1.6/step) + 1
    for dd in dirs:
        d = np.array(dd, np.float32); d /= np.linalg.norm(d)
        hs = z.copy()
        for k in range(1, n + 1):
            M = np.float32([[1, 0, d[0]*k*step], [0, 1, d[1]*k*step]])
            sh = cv2.warpAffine(z, M, (w, h), borderValue=0) - k*step/(unit*S)
            np.maximum(hs, sh, out=hs)
        np.maximum(sha, np.clip((hs - z)/0.55, 0, 1), out=sha)
    sha = cv2.GaussianBlur(sha, (0, 0), s_soft*S)
    zb = cv2.GaussianBlur(z, (0, 0), ao_r*S)
    occ = np.clip((zb - z)/1.4, 0, 1)
    lift = (1 - tint) + tint*np.clip(z/zmax, 0, 1)**0.8/0.85
    return lift*(1 - s_str*sha)*(1 - ao*occ)


def finish(s, rgb, a, sharpen=0.55):
    """vstyle.Ship.render() without the depth pass, on given buffers"""
    af = a.astype(np.float32)
    out = np.dstack([rgb*af[..., None], af*255])
    out = cv2.resize(out, (s.W, s.H), interpolation=cv2.INTER_AREA)
    al = out[..., 3:4]/255
    c = np.where(al > 0, out[..., :3]/np.maximum(al, 1e-6), 0)
    if sharpen:
        bl = cv2.GaussianBlur(c, (0, 0), 0.8)
        c = c + sharpen*(c - bl)
    return Image.fromarray(np.dstack([np.clip(c, 0, 255), out[..., 3:4]]).astype(np.uint8), 'RGBA')


def lit_part(s, part, ctx, zmax):
    """part/ctx = (rgb, a, z) snapshots taken before the depth pass.  ctx = the ship the part is lit within (its own
    pixels use the part's z, everything else casts shadows/AO from ctx).  zmax = full ship's max z (keeps the lift scale)."""
    rgb, a, z = part; crgb, ca, cz = ctx
    ze, ae = np.where(a, z, cz), a | ca
    k = depth_k(s.SS, ze, ae, zmax=zmax, **s.depth)
    out = rgb.copy(); out[a] *= k[a][:, None]
    return finish(s, out, a)


def over(*ims):
    """alpha-composite PIL RGBA images in order (first = bottom)"""
    base = Image.new('RGBA', ims[0].size, (0, 0, 0, 0))
    for im in ims: base = Image.alpha_composite(base, im)
    return base


def add_shadow_fringe(part_im, full_im, others_im, reach=8, max_a=0.85, floor=0.035):
    """shadow the part casts onto what lies under it (in the full ship) -> black semi-transparent pixels round the part"""
    P = np.asarray(part_im).astype(np.float32); F = np.asarray(full_im).astype(np.float32); O = np.asarray(others_im).astype(np.float32)
    solid = P[..., 3] > 0
    near = ndi.binary_dilation(solid, iterations=reach) & ~solid & (O[..., 3] > 200)
    lumF = F[..., :3].mean(2); lumO = np.maximum(O[..., :3].mean(2), 1.0)
    sh = np.clip(1 - lumF/lumO, 0, max_a); sh[sh < floor] = 0; sh[~near] = 0
    out = P.copy(); m = sh > 0
    out[m, :3] = 0; out[m, 3] = sh[m]*255
    return Image.fromarray(out.astype(np.uint8), 'RGBA')


def diff_stats(a_im, b_im):
    A = np.asarray(a_im).astype(np.int16); B = np.asarray(b_im).astype(np.int16)
    Ap = A[..., :3]*(A[..., 3:4]/255.0); Bp = B[..., :3]*(B[..., 3:4]/255.0)     # premultiplied (ignores rgb under alpha 0)
    d = np.abs(np.concatenate([Ap - Bp, (A[..., 3:4] - B[..., 3:4]).astype(np.float64)], 2))
    vis = (A[..., 3] > 0) | (B[..., 3] > 0)
    return dict(max=float(d.max()), mean=float(d[vis].mean()), p99=float(np.percentile(d[vis].max(1), 99)),
                n_gt16=int((d.max(2) > 16).sum()), n_vis=int(vis.sum()))


def bbox(im, thr=128):
    al = np.asarray(im)[..., 3]; ys, xs = np.nonzero(al >= thr)
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def split_lr(im, cx):
    """split a mirrored pair part (drawn + lit together) into its left (x < cx) and right (x >= cx) halves"""
    A = np.asarray(im).copy(); B = A.copy()
    A[:, int(cx):] = 0; B[:, :int(cx)] = 0
    return Image.fromarray(A, 'RGBA'), Image.fromarray(B, 'RGBA')
