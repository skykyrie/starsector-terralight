import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Hastur built-in medium energy twin-beam (Tiamat mechanism: arm + collar fixed on the sponson, only this barrel head turns 135 deg).
80x80 canvas, pivot at the centre (40,40), barrels point up. Two barrels stacked OVER-UNDER (as in hastur3d.html): the upper one
narrower and brighter, the lower one showing as a darker shoulder either side. Barrel tips 36 px ahead of the pivot -> .wpn turretOffsets."""
import numpy as np
from vstyle import Ship
from PIL import Image
N = 80; C = N/2
STEEL = np.array([112, 118, 128]); STEEL_D = np.array([70, 74, 82]); STEEL_L = np.array([158, 164, 174])
PINK = np.array([236, 104, 170]); GLOW = (255, 214, 240)
def build():
    s = Ship(N, N, seed=21)
    # hub: rounded block the barrels come out of (collar bearing underneath, hidden by the hull sponson)
    hub = s.poly([(C - 8, C + 9), (C - 10, C + 5), (C - 10, C - 6), (C - 7, C - 9), (C + 7, C - 9), (C + 10, C - 6), (C + 10, C + 5), (C + 8, C + 9)])
    s.plate(hub, STEEL, bevel=2.6, ridge=('x', C, 2.0, 10), inset=1.8, shadow_k=0.7)
    for yy in (C - 1.5, C + 3): s.rgb[s.rrect(C - 9, yy, C + 9, yy + 1.2, 0.3) & hub] = PINK*0.85
    for g in (-1, 1):
        s.plate(s.rrect(min(C + g*10, C + g*13), C - 4, max(C + g*10, C + g*13), C + 6, 0.8), STEEL_D, bevel=0.8, outline=0.6, shadow_k=0.5, notch=0)
        s.grille(s.rrect(min(C + g*10, C + g*13), C - 3, max(C + g*10, C + g*13), C + 5, 0.5), period=1.6, axis='h', depth=0.35)
    # lower barrel (wider shoulder), then upper barrel on top
    s.cylinder(C - 5.6, C - 36, C + 5.6, C - 8, (84, 88, 96), axis='v', outline=0.8)
    s.cylinder(C - 3.4, C - 34, C + 3.4, C - 8, (150, 154, 164), axis='v', outline=0.8)
    for yy in (C - 16, C - 25):                                                     # cooling / focusing rings
        s.rgb[s.rrect(C - 5.8, yy, C + 5.8, yy + 1.6, 0.5)] = STEEL_D
        s.rgb[s.rrect(C - 3.6, yy, C + 3.6, yy + 1.6, 0.5)] = PINK*0.9
    s.rgb[s.rrect(C - 5.2, C - 36, C + 5.2, C - 33.6, 0.9)] = PINK*0.75             # lower emitter lip
    s.rgb[s.rrect(C - 3.0, C - 34.4, C + 3.0, C - 31.8, 0.8)] = PINK                # upper emitter lip
    s.rgb[s.rrect(C - 1.0, C - 34.0, C + 1.0, C - 32.4, 0.4)] = GLOW
    cap = s.disk(C, C + 2, 3.2); s.plate(cap, STEEL_L, bevel=1.4, dome=0.6, outline=0.6, shadow_k=0.5, notch=0)
    return s.render(sharpen=0.45)
if __name__ == '__main__':
    import os; os.makedirs(_ROOT + '/weapons', exist_ok=True)
    im = build(); im.save(_ROOT + '/weapons/tl_hastur_beam_turret_ss_v1.png'); print(im.size)
