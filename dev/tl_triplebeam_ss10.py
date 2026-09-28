import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Triple Beam Cannon v9 - big barrels. 128x128 canvas, pivot dead centre (64,64); barrels point up.
Fires beam-bolt projectiles: burst of 2 from each of the 3 stacked barrels (6 bolts per shot).
Barrel tips (distance ahead of the pivot): bottom 54, middle 46, top 38 (v10: shorter, bulkier) -> .wpn turretOffsets."""
import numpy as np
from vstyle import Ship
from PIL import Image

N = 128; C = N/2
STEEL = np.array([118, 122, 130]); STEEL_D = np.array([76, 79, 86]); STEEL_L = np.array([160, 164, 172])
BLUE = np.array([70, 120, 220]); EMIT = np.array([236, 110, 190]); HOSE = (62, 64, 70); COPPER = (160, 116, 80)
TIPS = (54, 46, 38)

def build():
    s = Ship(N, N, seed=9)
    s.cable([(C - 6, C + 12), (C - 9, C + 19), (C, C + 22), (C + 9, C + 19), (C + 6, C + 12)], 3.6, HOSE, clamps=0)      # power pigtail
    blk = s.poly([(C - 15, C + 15), (C - 18, C + 9), (C - 18, C - 8), (C - 13, C - 15), (C + 13, C - 15), (C + 18, C - 8), (C + 18, C + 9), (C + 15, C + 15)])
    s.plate(blk, STEEL, bevel=3.2, ridge=('x', C, 3.0, 18), inset=2.4, shadow_k=0.75)
    for g in (-1, 1):
        fin = s.rrect(min(C + g*18, C + g*22), C - 7, max(C + g*18, C + g*22), C + 9, 0.8)
        s.plate(fin, STEEL_D, bevel=1.0, outline=0.6, shadow_k=0.55, notch=0); s.grille(fin, period=1.8, axis='h', depth=0.35)
        for yy in (C - 11, C + 11): s.rgb[s.disk(C + g*12.5, yy, 1.0)] = (40, 42, 46)
        s.cable([(C + g*9, C + 10), (C + g*11, C + 1), (C + g*8, C - 14)], 2.2, COPPER, clamps=0, cast=False)
    for yy in (C - 3, C + 2):
        s.rgb[s.rrect(C - 17, yy, C + 17, yy + 1.8, 0.4) & blk] = BLUE
        s.rgb[s.rrect(C - 11, yy, C - 3, yy + 0.6, 0.2) & blk] = (170, 210, 255)
    hub = s.disk(C, C, 6.5); s.plate(hub, STEEL_L, bevel=2.6, dome=0.7, outline=0.7, shadow_k=0.55, notch=0)
    s.rgb[s.disk(C, C, 2.3)] = (36, 38, 42)
    col = s.poly([(C - 14, C - 14), (C - 14, C - 19), (C - 11, C - 22), (C + 11, C - 22), (C + 14, C - 19), (C + 14, C - 14)])
    s.plate(col, STEEL_L, bevel=2.0, ridge=('x', C, 1.6, 14), inset=1.6, shadow_k=0.65, notch=0)
    for bx in (C - 10.5, C + 10.5): s.rgb[s.disk(bx, C - 18, 0.9)] = (40, 42, 46)
    for (w, tip, c_) in ((21.0, TIPS[0], (96, 98, 106)), (16.0, TIPS[1], (126, 128, 136)), (11.0, TIPS[2], (164, 166, 174))):
        top = C - tip
        s.cylinder(C - w/2, top, C + w/2, C - 20, c_, axis='v', outline=0.8)
        s.rgb[s.rrect(C - w/2 + 0.8, top + 0.6, C + w/2 - 0.8, top + 3.6, 0.9)] = EMIT
        s.rgb[s.rrect(C - 1.4, top + 1.0, C + 1.4, top + 2.6, 0.5)] = (255, 222, 245)
    for yy in (C - 29,):
        cl = s.rrect(C - 11.5, yy, C + 11.5, yy + 3.2, 0.8); s.rgb[cl] = STEEL_D; s.rgb[s.rrect(C - 11.5, yy, C + 11.5, yy + 0.8, 0.3)] = STEEL_L
    return s.render(sharpen=0.45)

if __name__ == '__main__':
    im = build(); im.save(_ROOT + '/weapons/tl_triplebeam_turret_ss_v10.png')
    old = Image.open(_ROOT + '/weapons/tl_triplebeam_turret_ss_v9.png')
    G = Image.new('RGBA', (244, 128), (16, 17, 22, 255)); G.alpha_composite(old, (0, 0)); G.alpha_composite(im, (116, 0))
    Image.fromarray(np.kron(np.array(G), np.ones((4, 4, 1), np.uint8))).save('/mnt/user-data/outputs/TripleBeam_v9_vs_v10_4x.png'); print('ok')
