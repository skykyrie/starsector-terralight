import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Quad Railgun v2 (Asura-II built-in, LARGE BALLISTIC) in the vanilla-like / Terra Light style.
128x128 canvas, pivot dead centre (64,64); barrels point up. Armoured turret house with 4 rail barrels in pairs,
magnetic coil bands, capacitor packs on the flanks, ammo feed at the back. Muzzles 58 px ahead of the pivot. v3: 168x168 canvas, rails 9.2 wide, muzzles 78 px ahead."""
import numpy as np
from vstyle import Ship
from PIL import Image

N = 168; C = N/2
STEEL = np.array([122, 124, 130]); STEEL_D = np.array([80, 82, 88]); STEEL_L = np.array([164, 166, 172])
ORNG = np.array([200, 120, 56]); ORNG_D = np.array([140, 80, 36]); PINK = np.array([214, 90, 160])
HOSE = (62, 64, 70); COPPER = (160, 116, 80)

def build():
    s = Ship(N, N, seed=21)
    # ammo feed chute from the magazine (enters the turret from behind)
    s.cable([(C - 5, C + 34), (C - 5, C + 20)], 5.0, (96, 98, 104), clamps=0)
    for yy in (C + 23, C + 28, C + 33): s.rgb[s.rrect(C - 8, yy, C - 2, yy + 1.2, 0.3)] = (60, 62, 66)
    s.cable([(C + 7, C + 32), (C + 9, C + 24), (C + 7, C + 18)], 2.6, HOSE, clamps=0)                     # power pigtail
    # turret house: wide armoured block, sloped front glacis
    house = s.poly([(C - 22, C + 20), (C - 26, C + 12), (C - 26, C - 8), (C - 18, C - 20), (C + 18, C - 20), (C + 26, C - 8), (C + 26, C + 12), (C + 22, C + 20)])
    s.plate(house, STEEL, bevel=3.4, ridge=('x', C, 2.6, 26), inset=2.6, shadow_k=0.8, notch=3.0,
            paint=[(s.rrect(C - 26, C + 4, C + 26, C + 8), ORNG)])
    glacis = s.poly([(C - 18, C - 20), (C - 24, C - 10), (C + 24, C - 10), (C + 18, C - 20)])
    s.plate(glacis, STEEL_L, bevel=1.8, tilt=(0, 0.35), inset=1.4, shadow_k=0.6, notch=0)
    # capacitor packs on both flanks (charge the rails), orange terminals
    for g in (-1, 1):
        for k in range(3):
            y0 = C - 6 + k*7
            s.cylinder(min(C + g*20, C + g*29), y0, max(C + g*20, C + g*29), y0 + 5.6, (150, 152, 158), axis='h', caps=tuple(ORNG))
        s.cable([(C + g*18, C + 16), (C + g*14, C + 10), (C + g*12, C - 8)], 1.8, COPPER, clamps=0, cast=False)
    # gunner / sensor cupola, offset to one side like a real turret
    s.mount(C + 11, C + 6, 5.0, STEEL_L, well_col=(80, 110, 140))
    s.rgb[s.disk(C - 12, C + 11, 1.2)] = (40, 42, 46); s.rgb[s.disk(C + 1, C + 14, 1.2)] = (40, 42, 46)
    # four rail barrels in two pairs, each rail = two conductor bars with coil bands
    for bx in (C - 16.5, C - 6.5, C + 6.5, C + 16.5):                                            # v3: longer + bigger rails
        s.cylinder(bx - 4.6, C - 78, bx + 4.6, C - 16, (132, 134, 140), axis='v', outline=0.8,
                   bands=(C - 64, C - 52, C - 40, C - 28))
        s.rgb[s.rrect(bx - 0.8, C - 77, bx + 0.8, C - 18, 0.3)] = (40, 38, 44)                 # rail gap
        s.rgb[s.rrect(bx - 4.2, C - 78, bx + 4.2, C - 74.5, 0.8)] = PINK                        # muzzle glow ring (EL pink)
        s.rgb[s.rrect(bx - 2.0, C - 77.5, bx + 2.0, C - 76.2, 0.4)] = (255, 210, 235)
    for yy in (C - 58, C - 34):                                                                  # pair clamps
        for cx in (C - 11.5, C + 11.5):
            cl = s.rrect(cx - 10.5, yy, cx + 10.5, yy + 4, 1.0); s.plate(cl, STEEL_D, bevel=1.0, outline=0.6, shadow_k=0.5, notch=0)
            s.rgb[s.rrect(cx - 10.5, yy, cx + 10.5, yy + 1.0, 0.3)] = STEEL_L
    # orange coil jackets at the barrel roots
    for cx in (C - 11.5, C + 11.5):
        j = s.rrect(cx - 11, C - 22, cx + 11, C - 15, 1)
        s.plate(j, ORNG, bevel=1.2, outline=0.6, shadow_k=0.5, notch=0)
        for xx in np.arange(cx - 9.5, cx + 10, 2.2): s.rgb[s.rrect(xx, C - 21.5, xx + 0.7, C - 15.5, 0.2)] = ORNG_D
    return s.render(sharpen=0.45)

if __name__ == '__main__':
    im = build(); im.save(_ROOT + '/weapons/tl_quadrail_turret_ss_v3.png')
    Image.fromarray(np.kron(np.array(im), np.ones((3, 3, 1), np.uint8))).save('/mnt/user-data/outputs/QuadRailgun_v3_3x.png'); print('ok')
