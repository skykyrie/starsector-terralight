# Terra Light v0.9 - playtest 3 (refit sprite fix, carriers' launch points, Hastur owns its hangar, TL detailing Tiamat/Asura...)
# (v0.8:) Terra Light v0.8 - playtest 2 fixes (weapon hiding, Abaddon blast, loadouts with S-mods...) on top of v0.7.
# (v0.7:) Terra Light v0.7 - Abaddon/Duilius/Garm/Hannibal/Hastur/Regulus revisions on top of v0.6.
# (v0.6 notes:) Terra Light v0.6 - playtest revision of the v0.5 build (user feedback 2026-09-28).
# Changes vs v0.5: bigger flames sized to each nozzle, roomier shields, refittable under-hull slots (script-rendered below the hull),
# Hellhound command-tower module + swivel drive, Fenrir/Garm vectoring pods, Hastur module under the hull, Iris rear PD,
# Siren transform (starts in carrier mode, deck animation), Neow (damper system + 360 flares on right-click), Tiamat projectile
# triple cannon, Abaddon Apocalypse launch sequence, custom ship systems + balance pass.
import json, os, shutil, csv, io, math, re
import numpy as np, cv2
from PIL import Image, ImageDraw
import sys as _sys, os as _os
_ROOT = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _ROOT)
from tl_desc import TL_DESC

SS = _ROOT + '/ss_style/'; WP = _ROOT + '/weapons/'; JAVA = _ROOT + '/tl_java/'
REF = json.load(open(_ROOT + '/vanilla_ref.json'))   # ids/costs from the base game (no game files needed)
MOD = _ROOT + '/build/TerraLight'
VERSION = '0.9.2'; GAMEVER = '0.98a-RC8'
if os.path.exists(MOD): shutil.rmtree(MOD)
os.makedirs(MOD, exist_ok=True)
def mk(p): os.makedirs(os.path.join(MOD, p), exist_ok=True); return os.path.join(MOD, p)
def wjson(p, d): open(os.path.join(MOD, p), 'w').write(json.dumps(d, indent=2))
def wcsv(p, cols, rows):
    buf = io.StringIO(); w = csv.DictWriter(buf, cols); w.writeheader()
    for r in rows: w.writerow({c: r.get(c, '') for c in cols})
    open(os.path.join(MOD, p), 'w').write(buf.getvalue())
for p in ('graphics/ships/terralight', 'graphics/weapons/terralight', 'graphics/missiles/terralight',
          'data/hulls', 'data/variants', 'data/weapons/proj', 'data/strings', 'data/config', 'data/shipsystems/scripts/ai',
          'data/hullmods', 'data/world/factions'):
    mk(p)
def rgba(p): return Image.open(p).convert('RGBA')

# ======================================================================================= ships
SHIPS = [
 ('tiamat',   'Tiamat',   'Battleship',            'CAPITAL_SHIP', 'tiamat_ss_v32.png',        'tiamat_ss_v32'),
 ('asura',    'Asura-II', 'Advanced Battleship',   'CAPITAL_SHIP', 'asura_ss_v11.png',         'asura_ss_v11'),
 ('neow',     'Neow',     'Fortified Battleship',  'CAPITAL_SHIP', 'neow_ss_v6.png',           'neow_ss_v6'),
 ('artemis',  'Artemis',  'Catapult Carrier',      'CAPITAL_SHIP', 'artemis_ss_v12.png',       'artemis_ss_v12'),
 ('siren',    'Siren',    'Convertible Carrier',   'CAPITAL_SHIP', 'siren_ss_v12_closed.png',  'siren_ss_v12'),
 ('hastur',   'Hastur',   'Battlecruiser',         'CRUISER',      'hastur_ss_v4_hull.png',    'hastur_ss_v4'),
 ('hannibal', 'Hannibal', 'Heavy Cruiser',         'CRUISER',      'hannibal_ss_v3.png',       'hannibal_ss_v3'),
 ('regulus',  'Regulus',  'Escort Cruiser',        'CRUISER',      'regulus_ss_v1.png',        'regulus_ss_v1'),
 ('duilius',  'Duilius',  'Claw Cruiser',          'CRUISER',      'duilius_ss_v1.png',        'duilius_ss_v1'),
 ('abaddon',  'Abaddon',  'Missile Cruiser',       'CRUISER',      'abaddon_ss_v8_hull_noshadow.png', 'abaddon_ss_v8'),
 ('iris',     'Iris',     'Carrier',               'CRUISER',      'iris_ss_v9.png',           'iris_ss_v9'),
 ('selene',   'Selene',   'Fast Carrier',          'CRUISER',      'selene_ss_v4.png',         'selene_ss_v4'),
 ('fenrir',   'Fenrir',   'Interdiction Destroyer','DESTROYER',    'fenrir_ss_v4_hull.png',    'fenrir_ss_v4'),
 ('hellhound','Hellhound','Light Destroyer',       'DESTROYER',    'hellhound_ss_v4_hull.png', 'hellhound_ss_v4'),
 ('garm',     'Garm',     'Assault Destroyer',     'DESTROYER',    'garm_ss_v4_hull.png',      'garm_ss_v4'),
]
# fp, hull, armour, flux, diss, OP, bays, speed, acc, dec, turn, tacc, mass, shield, arc, upkeep, eff, system, crew min/max, cargo, fuel, fuel/ly, burn, value, deployCR, peakCR, sup, engine style
STATS = {
 'tiamat':   (42, 24000, 1900, 28000,1600, 330, 0, 40, 18, 12, 7, 11, 5200, 'FRONT', 300, .5, .8, 'tl_triple_overcharge', 450, 800, 400, 500, 8, 7, 450000, 25, 600, 36, 'TL_VIOLET'),
 'asura':    (42, 19000, 1700, 24000,1500, 330, 0, 50, 24, 16, 9, 13, 4400, 'FRONT', 270, .5, .8, 'tl_rail_overdrive',    400, 700, 350, 450, 7, 8, 440000, 25, 600, 36, 'TL_ORANGE'),
 'neow':     (42, 26000,20000,18000, 900, 280, 0, 25, 10,  8, 5,  8, 6500, 'PHASE',   0,  0,  0, 'damper',               500, 900, 500, 600, 9, 7, 450000, 28, 600, 38, 'TL_ORANGE'),
 'artemis':  (40, 14000, 1200, 18000, 900, 280, 8, 35, 15, 10, 6, 10, 4800, 'FRONT', 300, .5, .8, 'reservewing',          500, 900, 600, 600, 8, 7, 450000, 25, 600, 36, 'TL_PINK'),
 'siren':    (40, 16000, 1400, 21000,1100, 290, 4, 40, 18, 12, 7, 11, 4600, 'FRONT', 300, .5, .8, 'tl_siren_mode',        480, 850, 500, 550, 8, 7, 440000, 25, 600, 36, 'TL_ORANGE'),
 'hastur':   (27, 12500, 1300, 16000,1050, 220, 2, 65, 38, 30,14, 22, 2600, 'FRONT', 240, .4, .75,'tl_replica_wing',      250, 400, 200, 250, 3, 8, 240000, 15, 480, 20, 'TL_CYAN'),
 'hannibal': (24, 12000, 1450, 15000,1000, 230, 0, 65, 36, 30,14, 22, 2400, 'FRONT', 240, .4, .75,'tl_ap_focus',          220, 350, 150, 200, 3, 8, 220000, 15, 480, 18, 'TL_VIOLET'),
 'regulus':  (20,  9500, 1100, 12000, 800, 190, 0, 55, 30, 24,12, 18, 2300, 'FRONT', 270, .4, .8, 'tl_pd_overdrive',      200, 330, 150, 200, 3, 8, 200000, 15, 480, 17, 'TL_TEAL'),
 'duilius':  (23, 11000, 1400, 12500, 800, 200, 0, 70, 40, 32,14, 22, 2800, 'FRONT', 240, .4, .8, 'tl_claw_strike',       220, 350, 150, 200, 3, 8, 220000, 15, 480, 18, 'TL_YELLOW'),
 'abaddon':  (24, 13000, 1600, 11000, 700, 160, 0, 45, 25, 20,10, 15, 3200, 'PHASE',   0,  0,  0, 'tl_apocalypse',        200, 330, 150, 200, 3, 8, 260000, 15, 480, 20, 'TL_GREEN'),
 'iris':     (22,  8000,  950, 10500, 650, 180, 4, 50, 28, 22,11, 16, 2200, 'FRONT', 240, .4, .85,'reservewing',          220, 380, 200, 250, 3, 8, 220000, 15, 480, 16, 'TL_PINK'),
 'selene':   (18,  6500,  800,  8500, 550, 140, 2, 90, 50, 40,18, 26, 1500, 'FRONT', 270, .4, .85,'tl_wing_rally',        140, 240, 120, 180, 2, 9, 180000, 12, 420, 13, 'TL_VIOLET'),
 'fenrir':   (13,  4000,  600,  6500, 420, 110, 0,115, 75, 60,26, 44,  750, 'FRONT', 200, .4, .8, 'tl_hit_and_run',        60, 110,  60, 100, 1, 10,100000, 10, 360,  9, 'TL_ORANGE'),
 'hellhound':(11,  4200,  650,  6500, 450, 105, 0,100, 70, 55,26, 42,  650, 'FRONT', 200, .4, .8, 'tl_execution',          50,  90,  50,  80, 1, 9,  80000,  8, 360,  7, 'TL_BLUE'),
 'garm':     (12,  4500,  750,  6000, 400, 100, 0, 85, 58, 44,23, 36,  850, 'FRONT', 200, .4, .8, 'displacer',             60, 110,  60,  90, 1, 9,  95000, 10, 360,  8, 'TL_ORANGE'),
}
DEFENSE = {'neow': 'tl_flare_screen', 'abaddon': 'tl_flare_screen'}
EXTRA_TAGS = {k: 'special_allows_system_use, system_allows_special_use' for k in DEFENSE}
NO_BREAK = ('abaddon', 'hellhound', 'fenrir', 'garm', 'siren')
ENGINE_STYLES = {'TL_VIOLET': (225, 120, 255), 'TL_ORANGE': (255, 150, 60), 'TL_PINK': (255, 110, 190), 'TL_CYAN': (90, 220, 240),
                 'TL_TEAL': (60, 225, 190), 'TL_YELLOW': (255, 210, 90), 'TL_GREEN': (120, 255, 150), 'TL_BLUE': (100, 170, 255)}
HINTS = {'artemis': 'CARRIER', 'iris': 'CARRIER', 'selene': 'CARRIER', 'siren': 'CARRIER, COMBAT', 'hastur': 'SHIP_WITH_MODULES, CARRIER, COMBAT',
         'hellhound': 'SHIP_WITH_MODULES'}
BUILTIN_MODS = {'siren': ['tl_siren_modes']}
ENG_CAP = {'hellhound': 70}
ENG_OVR = {'hannibal': 46, 'regulus': 44, 'neow': 50}
ENG_MIN = {'CAPITAL_SHIP': 32.0, 'CRUISER': 24.0, 'DESTROYER': 16.0}           # the lamp lens: flame narrower than the whole rim
SWING = {'hellhound': 6.0, 'fenrir': 14.0, 'garm': 15.0}
SHIELD_MULT, SHIELD_ADD = 1.22, 28

def alpha_bounds(a, W, H, CX, CY):
    cnt, _ = cv2.findContours(a.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = max(cnt, key=cv2.contourArea)
    poly = cv2.approxPolyDP(cnt, 2.5, True)[:, 0, :]
    b = []
    for (px, py) in poly[::-1]: b += [round((H - py) - CY, 1), round(CX - px, 1)]
    return b

def nozzle(a, px, py):
    """walk down from the engine point to the nozzle exit; measure the nozzle width a few px inside the exit"""
    px, y = int(round(px)), int(round(py))
    H, W = a.shape
    while y + 1 < H and a[y + 1, px] and y < py + 40: y += 1
    row = min(y - 2, H - 1)
    l = px
    while l - 1 >= 0 and a[row, l - 1] and px - l < 70: l -= 1
    r = px
    while r + 1 < W and a[row, r + 1] and r - px < 70: r += 1
    return y, (r - l + 1)

SHIP_COLS = 'name,id,designation,tech/manufacturer,system id,fleet pts,hitpoints,armor rating,max flux,8/6/5/4%,flux dissipation,ordnance points,fighter bays,max speed,acceleration,deceleration,max turn rate,turn acceleration,mass,shield type,defense id,shield arc,shield upkeep,shield efficiency,phase cost,phase upkeep,min crew,max crew,cargo,fuel,fuel/ly,range,max burn,base value,cr %/day,CR to deploy,peak CR sec,CR loss/sec,supplies/rec,supplies/mo,c/s,c/f,f/s,f/f,crew/s,crew/f,hints,tags,logistics n/a reason,codex variant id,rarity,breakProb,minPieces,maxPieces,travel drive,number'.split(',')
ship_rows, desc_rows, variants_out, report = [], [], [], []
BUILTIN_WEAPONS = set()
JAVA_CONST = {}
SPRITES = {}                          # settings.json graphics entries used by the scripts

STOCK = {('SMALL', 'BALLISTIC'): 'vulcan', ('SMALL', 'ENERGY'): 'pdlaser', ('SMALL', 'MISSILE'): 'harpoon_single',
         ('MEDIUM', 'BALLISTIC'): 'heavymauler', ('MEDIUM', 'ENERGY'): 'pulselaser', ('MEDIUM', 'MISSILE'): 'harpoonpod',
         ('MEDIUM', 'COMPOSITE'): 'heavymauler', ('LARGE', 'BALLISTIC'): 'mark9', ('LARGE', 'ENERGY'): 'hil',
         ('LARGE', 'MISSILE'): 'pilum'}
WINGS = {'artemis': ['broadsword_wing', 'broadsword_wing', 'talon_wing', 'talon_wing', 'wasp_wing', 'wasp_wing', 'dagger_wing', 'dagger_wing'],
         'siren': ['broadsword_wing', 'broadsword_wing', 'wasp_wing', 'wasp_wing'], 'iris': ['talon_wing', 'talon_wing', 'dagger_wing', 'dagger_wing'],
         'selene': ['broadsword_wing', 'talon_wing'], 'hastur': ['talon_wing', 'talon_wing']}

def ship_slots(key, S):
    """normalise a ship's slot list: ids, under-hull slots, built-ins, special conversions"""
    out, n, uh, main = [], 0, 0, 0
    for s in S['slots']:
        s = dict(s)
        weapon_type = s['type'] in ('BALLISTIC', 'ENERGY', 'MISSILE', 'COMPOSITE')
        under = s.get('hide') or (s['mount'] == 'HIDDEN' and weapon_type and key in ('hastur', 'asura'))
        if key == 'abaddon' and s['type'] == 'STATION_MODULE': continue          # torpedo is script-driven now
        if key == 'duilius' and s['type'] == 'SYSTEM':                          # claw galleries: spawn points for Claw Strike
            s.update(size='SMALL', mount='HIDDEN', arc=30)
        if key == 'regulus' and s['type'] == 'MISSILE': s['builtin'] = 'tl_bubble'
        if key == 'hastur' and s['type'] == 'ENERGY' and s['size'] == 'MEDIUM':
            side = 1 if s['px'] < S['W'] / 2 else -1
            s['angle'], s['arc'] = (70 * side, 160) if s['py'] < 150 else (110 * side, 160)
        if key == 'duilius' and s.get('hide'): s['py'] = 60
        if key == 'garm' and s.get('hide'): s['py'] = 52
        if key == 'tiamat' and s.get('builtin') == 'tl_triplebeam':      # front pair converge dead ahead; each side's pair overlaps 30-150
            side = 1 if s['px'] < S['W'] / 2 else -1
            front = s['py'] < S['H'] / 2
            s['angle'], s['arc'] = (70 * side, 160) if front else (110 * side, 160)
        if s['type'] == 'LAUNCH_BAY':
            s['size'] = 'LARGE'
            if key == 'selene':                                              # fighters use the hangar decks on the side pods
                s['launch'] = [(s['px'], y) for y in (140, 170, 200)]
            else:                                                            # launch points on the bay itself (a lone point = ship centre)
                s['launch'] = [(s['px'], s['py'] + d) for d in (0, -10, 10)]
        if key == 'asura' and s['size'] == 'LARGE':
            s['builtin'] = 'tl_quadrail' if not under else 'tl_quadrail_twin'
        if under:
            uh += 1; s['id'] = f'UH {uh:03d}'; s['mount'] = 'TURRET'
        elif key == 'siren' and s['type'] == 'ENERGY' and s['size'] == 'LARGE':
            main += 1; s['id'] = f'MAIN {main}'
        out.append(s)
    return out

def extra_slots(key, S, a, W, H):
    """decorative / system slots added by the build (px, py in sprite pixels)"""
    ex = []
    if key in ('neow', 'abaddon'):                        # 8 flare tubes all round the envelope, pointing out
        CX, CY = W / 2, H / 2
        for k in range(8):
            ang = k * 45.0                                # 0 = forward (up), CCW
            dx, dy = -math.sin(math.radians(ang)), -math.cos(math.radians(ang))
            t = 0
            while True:
                x, y = int(CX + dx * (t + 1)), int(CY + dy * (t + 1))
                if not (0 <= x < W and 0 <= y < H) or not a[y, x]: break
                t += 1
            ex.append(dict(id=f'FL {k+1}', px=CX + dx * (t - 18), py=CY + dy * (t - 18), size='SMALL', type='SYSTEM', mount='HIDDEN',
                           angle=ang if ang <= 180 else ang - 360, arc=40))
    if key == 'siren':
        for did in ('DECK', 'DECK2'):
            ex.append(dict(id=did, px=S['deck_px'], py=S['deck_py'], size='LARGE', type='DECORATIVE', mount='TURRET', angle=0, arc=0,
                           builtin='tl_deco_siren_deck'))
    if key in ('fenrir', 'garm'):
        for side in ('L', 'R'):
            p = S[f'pivot_{side}']
            ex.append(dict(id=f'SW_{side}', px=p[0], py=p[1], size='MEDIUM', type='DECORATIVE', mount='TURRET', angle=0, arc=60,
                           builtin=f'tl_deco_{key}_{side}'))
    return ex

def build_ship(key, name, desig, size, sprite, slotfile, prefix='tl_', module_of=None, S=None, spr_img=None, shield_img=None, bounds_img=None):
    hid = prefix + key
    if S is None: S = json.load(open(SS + slotfile + '_slots.json'))
    W, H = S['W'], S['H']
    im = spr_img if spr_img is not None else rgba(SS + sprite)
    (HULL_SPRITE_OVERRIDE.get(key) if module_of is None and key in HULL_SPRITE_OVERRIDE else im).save(f'{MOD}/graphics/ships/terralight/{hid}.png')
    arr = np.array(im)[..., 3] > 20
    CX, CY = W / 2, H / 2
    loc = lambda px, py: [round((H - py) - CY, 1), round(CX - px, 1)]
    if bounds_img is None and module_of is None and key in HULL_SPRITE_OVERRIDE: bounds_img = HULL_SPRITE_OVERRIDE[key]
    bounds = alpha_bounds(np.array(bounds_img)[..., 3] > 20 if bounds_img is not None else arr, W, H, CX, CY)
    rad = max(math.hypot(bounds[i], bounds[i + 1]) for i in range(0, len(bounds), 2))
    slots, builtins, n = [], {}, 0
    slist = (ship_slots(key, S) if module_of is None else [dict(s) for s in S['slots']]) + extra_slots(key, S, arr, W, H)
    for s in slist:
        n += 1
        sid = s.get('id') or f'WS {n:03d}'
        locs = loc(s['px'], s['py'])
        if s.get('launch'): locs = [c for (x, y) in s['launch'] for c in loc(x, y)]
        ent = dict(id=sid, angle=round(float(s.get('angle', 0)), 1), arc=round(float(s.get('arc', 0)), 1),
                   locations=locs, mount=s['mount'], size=s['size'], type=s['type'])
        slots.append(ent); s['sid'] = sid
        if s.get('builtin'): builtins[sid] = s['builtin']; BUILTIN_WEAPONS.add(s['builtin'])
    st = STATS.get(key)
    style = st[-1] if st else 'TL_CYAN'
    engines = []
    full_a = np.array(shield_img if shield_img is not None else im)[..., 3] > 20
    for (px, py) in (S.get('ENG') or S.get('eng') or []):
        ey, nw = nozzle(full_a, px, py)
        w = min(max(1.15 * nw, ENG_MIN[size]), ENG_CAP.get(key, 72.0))
        w = max(w, ENG_OVR.get(key, 0))
        engines.append(dict(angle=180.0, contrailSize=round(w * 2.2, 1), length=round(min(max(w * 4.2, 70), 260), 1),
                            location=loc(px, ey - 2), style='CUSTOM', styleId=style, width=round(w, 1)))
    for (px, py, ang) in (S.get('small') or [d[:3] for d in S.get('diag', [])]):
        engines.append(dict(angle=float(ang), contrailSize=22.0, length=50.0, location=loc(px, py), style='CUSTOM', styleId=style, width=13.0))
    # shield: a clear margin round the whole ship (incl. module / moving parts when a composite is given)
    sa = np.array(shield_img)[..., 3] > 20 if shield_img is not None else arr
    ys, xs = np.nonzero(sa)
    scx, scy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    srad = float(np.max(np.hypot(xs - scx, ys - scy)))
    shield_r = round(srad * SHIELD_MULT + SHIELD_ADD)
    ship = dict(bounds=bounds, center=[CX, CY], collisionRadius=round(max(rad + 4, shield_r + 2)), coversColor='', engineSlots=engines,
                height=H, width=W, hullId=hid, hullName=name, hullSize=size, shieldCenter=loc(scx, scy), shieldRadius=shield_r,
                spriteName=f'graphics/ships/terralight/{hid}.png', style='HIGH_TECH', viewOffset=0,
                weaponSlots=slots, builtInMods=['tl_hull'] + BUILTIN_MODS.get(key, []), builtInWeapons=builtins, builtInWings=[])
    return hid, ship, slist, loc, rad

# ---------------------------------------------------------------------------------------------- standard loadouts
VW = {k: {'OPs': v} for k, v in REF['weapon_op'].items()}
VWING = {k: {'op cost': v} for k, v in REF['wing_op'].items()}
VHM = REF['hullmod_cost']
HM_COL = {'DESTROYER': 'cost_dest', 'CRUISER': 'cost_cruiser', 'CAPITAL_SHIP': 'cost_capital', 'FRIGATE': 'cost_frigate'}
MAX_VENTS = {'DESTROYER': 20, 'CRUISER': 30, 'CAPITAL_SHIP': 50, 'FRIGATE': 10}
def w_op(w): return float(VW[w]['OPs'] or 0) if w in VW else 0.0
def stock_for(key, s):
    t, z = s['type'], s['size']
    if key == 'asura' and t == 'MISSILE' and z == 'SMALL': return 'harpoon' if 90 < s['px'] < 200 else 'annihilator'
    if key == 'fenrir' and t == 'BALLISTIC' and z == 'MEDIUM': return 'heavyneedler' if s['py'] < 100 else 'heavymauler'
    if key == 'garm' and t == 'BALLISTIC' and z == 'LARGE': return 'gauss'
    if key == 'garm' and t == 'BALLISTIC' and z == 'SMALL' and s['py'] < 130: return 'railgun'
    if key == 'hannibal' and t == 'ENERGY': return 'heavyblaster' if z == 'MEDIUM' else 'hil'
    if key in ('hellhound', 'hellhound_tower') and t == 'BALLISTIC' and z == 'SMALL' and s['py'] < 120: return 'railgun'
    if key == 'hellhound' and t == 'MISSILE': return 'harpoon'
    if key == 'duilius' and t == 'BALLISTIC' and z == 'LARGE': return 'gauss'
    return STOCK.get((z, t))
SHIELDLESS = ('neow', 'abaddon')
CARRIERS = ('artemis', 'siren', 'iris', 'selene')
MISSILE_SHIPS = ('asura', 'iris', 'hellhound')
def loadout(key, hullsize, op, weapons_op, wings_op, has_shield, is_module):
    """S-mods (free) + regular hullmods by priority, keeping half the max vents in reserve, then vents to max, then capacitors"""
    if is_module:
        smods, prio = [], []
    else:
        smods = ['hardenedshieldemitter', 'heavyarmor'] if has_shield else ['heavyarmor', 'reinforcedhull']
        prio = (['expanded_deck_crew'] if key in CARRIERS else []) + ['armoredweapons', 'blast_doors', 'targetingunit'] + \
               (['missleracks'] if key in MISSILE_SHIPS else []) + ['fluxdistributor', 'fluxcoil', 'autorepair', 'reinforcedhull',
               'pointdefenseai', 'stabilizedshieldemitter' if has_shield else 'hardened_subsystems']
    left = op - weapons_op - wings_op
    mv = MAX_VENTS[hullsize]; reserve = mv // 2
    mods = []
    for m in prio:
        if m in smods or m in mods: continue
        c = float(VHM[m][HM_COL[hullsize]])
        if left - c >= reserve: mods.append(m); left -= c
    vents = int(min(mv, max(0, left))); left -= vents
    caps = int(min(mv, max(0, left))); left -= caps
    for m in ['eccm', 'turretgyros', 'magazines', 'advancedshieldemitter' if has_shield else 'insulatedengine', 'solar_shielding']:
        if is_module or m in mods or m in smods: continue
        c = float(VHM[m][HM_COL[hullsize]])
        if c <= left: mods.append(m); left -= c
    return smods, mods, vents, caps, left

LOADOUT_REPORT = []
def variants_for(hid, key, slist, ship, modules=None):
    def groups(filled):
        g = {}
        for s in slist:
            if s['type'] in ('LAUNCH_BAY', 'STATION_MODULE', 'SYSTEM', 'DECORATIVE'): continue
            w = s.get('builtin') or (filled and stock_for(key, s))
            if not w: continue
            pd = s['size'] == 'SMALL' and not s.get('builtin') and w not in ('railgun', 'harpoon', 'annihilator')
            gk = 'tl_quadrail' if w == 'tl_quadrail_twin' else w
            g.setdefault((gk, pd), {})[s['sid']] = w
        return [dict(autofire=pd, mode='LINKED', weapons=ws) for (w, pd), ws in g.items()]
    is_module = hid in MODULE_OP
    op = MODULE_OP.get(hid) or STATS[key][5]
    for vid, vname, filled, goal in ((f'{hid}_Hull', 'Hull', False, False), (f'{hid}_standard', 'Standard', True, True)):
        gr = groups(filled)
        wings = WINGS.get(key, []) if filled else []
        smods, mods, vents, caps = [], [], 0, 0
        if filled:
            wop = sum(w_op(w) for g in gr for sid, w in g['weapons'].items() if not any(s['sid'] == sid and s.get('builtin') for s in slist))
            gop = sum(float(VWING[w]['op cost'] or 0) for w in wings)
            has_shield = not is_module and STATS[key][13] not in ('NONE', 'PHASE')
            smods, mods, vents, caps, left = loadout(key, ship['hullSize'], op, wop, gop, has_shield, is_module)
            LOADOUT_REPORT.append((vid, op, wop, gop, smods, mods, vents, caps, left))
        v = dict(displayName=vname, fluxCapacitors=caps, fluxVents=vents, goalVariant=goal,
                 hullId=hid, hullMods=smods + mods, permaMods=list(smods), sMods=list(smods), quality=0, variantId=vid,
                 weaponGroups=gr, wings=wings)
        if modules: v['modules'] = [{sid: f'{mv}_{"standard" if filled else "Hull"}'} for sid, mv in modules]
        wjson(f'data/variants/{vid}.variant', v)
        variants_out.append(vid)

def ship_row(key, hid, name, desig, size, rad):
    st = STATS[key]
    (fp, hp, arm, flux, diss, op, bays, spd, acc, dec, turn, tacc, mass, sh, arc, upk, eff, sysid,
     cmin, cmax, cargo, fuel, fly, burn, value, dep, peak, sup, _) = st
    return {'name': name, 'id': hid, 'designation': desig, 'tech/manufacturer': 'Terra Light', 'system id': sysid,
            'fleet pts': fp, 'hitpoints': hp, 'armor rating': arm, 'max flux': flux, 'flux dissipation': diss, 'ordnance points': op,
            'fighter bays': bays or '', 'max speed': spd, 'acceleration': acc, 'deceleration': dec, 'max turn rate': turn,
            'turn acceleration': tacc, 'mass': mass, 'shield type': sh, 'defense id': DEFENSE.get(key, ''), 'shield arc': arc or '',
            'shield upkeep': upk or '', 'shield efficiency': eff or '', 'min crew': cmin, 'max crew': cmax, 'cargo': cargo, 'fuel': fuel,
            'fuel/ly': fly, 'max burn': burn, 'base value': value, 'cr %/day': 3, 'CR to deploy': dep, 'peak CR sec': peak,
            'CR loss/sec': 0.25, 'supplies/rec': sup, 'supplies/mo': sup, 'hints': HINTS.get(key, ''),
            'tags': ', '.join(t for t in ('tl_bp', EXTRA_TAGS.get(key, '')) if t), 'codex variant id': f'{hid}_standard',
            'breakProb': 0 if key in NO_BREAK else 0.5, 'minPieces': 2, 'maxPieces': 3, 'number': len(ship_rows) + 1}

def module_row(mid, desig, hp, arm, bays, hints, op=30):
    return {'name': '', 'id': mid, 'designation': desig, 'tech/manufacturer': 'Terra Light', 'fleet pts': 1,
            'hitpoints': hp, 'armor rating': arm, 'max flux': 2000, 'flux dissipation': 150, 'ordnance points': op,
            'fighter bays': bays or '', 'max speed': 0, 'acceleration': 0, 'deceleration': 0, 'max turn rate': 10, 'turn acceleration': 10,
            'mass': 400, 'shield type': 'NONE', 'min crew': 0, 'max crew': 0, 'fuel/ly': 1, 'base value': 1, 'CR to deploy': 1,
            'supplies/rec': 0, 'supplies/mo': 0, 'hints': hints, 'tags': 'module_hull_bar_only', 'breakProb': 1, 'minPieces': 2,
            'maxPieces': 3, 'number': len(ship_rows) + 1}

def centred_crop(im, px, py, pad=2):
    """crop a part so that (px, py) is the exact centre of the result (sprites turn about their centre)"""
    x0, y0, x1, y1 = im.getbbox()
    hx = max(px - x0, x1 - px) + pad; hy = max(py - y0, y1 - py) + pad
    hx, hy = int(math.ceil(hx)), int(math.ceil(hy))
    out = Image.new('RGBA', (2 * hx, 2 * hy), (0, 0, 0, 0))
    out.alpha_composite(im.crop((int(px - hx), int(py - hy), int(px + hx), int(py + hy))))
    return out

OLD = {'neow': 'nodens', 'duilius': 'corvus', 'hellhound': 'cerberus', 'garm': 'gulon'}
RENAME = {'Nodens': 'Neow', 'Corvus': 'Duilius', 'Cerberus': 'Hellhound', 'Gulon': 'Garm'}
def rn(t):
    for a, b in RENAME.items(): t = t.replace(a, b)
    return t

HULL_SPRITE_OVERRIDE, MODULE_OP = {}, {}
DECO = {}                            # decorative weapon id -> (sprite path, size, frames)
for (key, name, desig, size, sprite, slotfile) in SHIPS:
    S = json.load(open(SS + slotfile + '_slots.json'))
    modules, extra_rows, shield_img = None, [], None

    if key == 'siren':                                   # animated deck: crop the region that changes between the 5 frames
        frames = [rgba(SS + f'siren_ss_v12_{m}.png') for m in ('closed', 'open', 'siloopen', 'deck', 'battleship')]
        base = np.array(frames[0]).astype(int); diff = np.zeros(base.shape[:2], bool)
        for f in frames[1:]: diff |= np.abs(np.array(f).astype(int) - base).max(axis=2) > 6
        ys, xs = np.nonzero(diff)
        cx = S['W'] / 2; hx = int(math.ceil(max(cx - xs.min(), xs.max() + 1 - cx))) + 1
        y0, y1 = int(ys.min()) - 1, int(ys.max()) + 2
        if (y1 - y0) % 2: y1 += 1
        S['deck_px'], S['deck_py'] = cx, (y0 + y1) / 2
        for i, f in enumerate(frames):
            p = f'graphics/weapons/terralight/tl_siren_deck_{i:02d}.png'
            f.crop((int(cx - hx), y0, int(cx + hx), y1)).save(f'{MOD}/{p}')
        DECO['tl_deco_siren_deck'] = ('graphics/weapons/terralight/tl_siren_deck_00.png', 'LARGE', 5)

    if key in ('fenrir', 'garm'):                        # vectoring side pods = decorative turrets pivoting on their hubs
        part = {'fenrir': 'booster', 'garm': 'pod'}[key]
        for side in ('L', 'R'):
            p = S[f'pivot_{side}']
            c = centred_crop(rgba(SS + f'{key}_ss_v4_{part}{side}.png'), p[0], p[1])
            path = f'graphics/weapons/terralight/tl_{key}_{part}_{side}.png'; c.save(f'{MOD}/{path}')
            DECO[f'tl_deco_{key}_{side}'] = (path, 'MEDIUM', 1)
        shield_img = rgba(SS + f'{key}_ss_v4_full.png')

    if key == 'hellhound':
        # swivelling lamp-head drive, drawn below the hull by TL_Hull (pivot = ball joint)
        pv = S['pivot_drive']
        c = centred_crop(rgba(SS + 'hellhound_ss_v4_drive.png'), pv[0], pv[1])
        c.save(f'{MOD}/graphics/ships/terralight/tl_hellhound_drive.png')
        SPRITES['hellhound_drive'] = 'graphics/ships/terralight/tl_hellhound_drive.png'
        W, H = S['W'], S['H']
        JAVA_CONST.update(HH_PIVOT_X=round((H - pv[1]) - H / 2, 1), HH_PIVOT_Y=round(W / 2 - pv[0], 1))
        # command tower = module carrying the 3 under-band guns (click the tower in the refit screen to fit them)
        x0, y0, x1, y1 = S['tower_bbox']; tcx, tcy = (x0 + x1) / 2, (y0 + y1) / 2
        tim = centred_crop(rgba(SS + 'hellhound_ss_v4_tower.png'), tcx, tcy, pad=1)
        TW, TH = tim.size; ox, oy = tcx - TW / 2, tcy - TH / 2
        mslots = []
        for i, s in enumerate(S['module_slots']):
            gx = {63: 65, 85: 85, 107: 105}.get(int(s['px']), s['px'])      # pulled 22 px aft, inside the tower (refit click area)
            mslots.append(dict(s, id=f'UH {i+1:03d}', mount='TURRET', px=gx - ox, py=108 - oy))
        MS = dict(W=TW, H=TH, ENG=[], small=[], slots=mslots)
        mhid, mship, mslist, mloc, mrad = build_ship('hellhound_tower', 'Hellhound Command Tower', 'Module', 'DESTROYER', None, None,
                                                     S=MS, spr_img=tim, module_of='hellhound')
        mship['moduleAnchor'] = [0.0, 0.0]
        mship['builtInMods'] = ['tl_hull', 'reduced_explosion']
        mship['shieldRadius'] = 0
        wjson(f'data/hulls/{mhid}.ship', mship)
        extra_rows.append(module_row(mhid, 'Hellhound Command Tower', 1500, 450, 0, 'UNBOARDABLE, HIDE_IN_CODEX, MODULE', op=40))
        MODULE_OP[mhid] = 40
        variants_for(mhid, 'hellhound_tower', mslist, mship)
        S['slots'] = S['slots'] + [dict(id='MODULE_TOWER', px=tcx, py=tcy, size='SMALL', type='STATION_MODULE', mount='HIDDEN', angle=0, arc=0)]
        modules = [('MODULE_TOWER', mhid)]
        shield_img = rgba(SS + 'hellhound_ss_v4_full.png')
        comp = rgba(SS + 'hellhound_ss_v4_drive.png'); comp.alpha_composite(rgba(SS + 'hellhound_ss_v4_hull.png'))
        HULL_SPRITE_OVERRIDE['hellhound'] = comp
        shutil.copy(SS + 'hellhound_ss_v4_hull.png', f'{MOD}/graphics/ships/terralight/tl_hellhound_combat.png')
        SPRITES['hellhound_hull'] = 'graphics/ships/terralight/tl_hellhound_combat.png'

    if key == 'hastur':                                  # command ball = module rendered UNDER the front hull
        mim = rgba(SS + 'hastur_ss_v4_module.png'); x0, y0, x1, y1 = mim.getbbox()
        x0 -= 2; y0 -= 2; x1 += 2; y1 += 2; crop = mim.crop((x0, y0, x1, y1))
        mc = S['module_center']
        MS = dict(W=x1 - x0, H=y1 - y0, ENG=[], small=[], slots=[dict(s, px=s['px'] - x0, py=s['py'] - y0) for s in S['module_slots'] if s['type'] != 'LAUNCH_BAY'])
        S['slots'] = S['slots'] + [dict(s, px=s['px'] + dx) for s in S['module_slots'] if s['type'] == 'LAUNCH_BAY' for dx in (-12, 12)]   # 2 bays in the hangar mouth; controlled from the Hastur itself
        mhid, mship, mslist, mloc, mrad = build_ship('hastur_bridge', 'Hastur Command Module', 'Module', 'CRUISER', None, None,
                                                     S=MS, spr_img=crop, module_of='hastur')
        mship['moduleAnchor'] = mloc(mc[0] - x0, mc[1] - y0)
        mship['builtInMods'] = ['tl_hull', 'reduced_explosion']
        mship['shieldRadius'] = 0
        wjson(f'data/hulls/{mhid}.ship', mship)
        extra_rows.append(module_row(mhid, 'Hastur Command Module', 5500, 1100, 0, 'UNBOARDABLE, HIDE_IN_CODEX, MODULE, UNDER_PARENT', op=40))
        MODULE_OP[mhid] = 40
        variants_for(mhid, 'hastur_bridge', mslist, mship)
        modules = [('MODULE_COMMAND', mhid)]
        shield_img = rgba(SS + 'hastur_ss_v4_full.png')

    bounds_img = None
    if key == 'abaddon':                                 # side boosters drawn below the frame by TL_Hull (they retract on launch)
        shield_img = bounds_img = rgba(SS + 'abaddon_ss_v8_full.png')
        HULL_SPRITE_OVERRIDE['abaddon'] = rgba(SS + 'abaddon_ss_v8_full.png')
        shutil.copy(SS + 'abaddon_ss_v8_hull_noshadow.png', f'{MOD}/graphics/ships/terralight/tl_abaddon_frame.png')
        SPRITES['abaddon_frame'] = 'graphics/ships/terralight/tl_abaddon_frame.png'
        for nm in ('boosterL', 'boosterR', 'shadow_rest', 'shadow_open'):
            path = f'graphics/ships/terralight/tl_abaddon_{nm}.png'
            shutil.copy(SS + f'abaddon_ss_v8_{nm}.png', f'{MOD}/{path}'); SPRITES[f'abaddon_{nm}'] = path
    hid, ship, slist, loc, rad = build_ship(key, name, desig, size, sprite, slotfile, S=S, shield_img=shield_img, bounds_img=bounds_img)

    if key == 'abaddon':                                 # docked Apocalypse (drawn below the hull until launched)
        ap = rgba(SS + 'apocalypse_ss_v2.png'); bx0, by0, bx1, by1 = ap.getbbox()
        acx, acy = (bx0 + bx1) / 2, (by0 + by1) / 2
        JAVA_CONST.update(AP_X=loc(acx, acy)[0], AP_Y=loc(acx, acy)[1], AB_RETRACT=S['retract_px'],
                          RETRO_X=', '.join(f'{loc(x, y)[0]}f' for x, y in S['retro']), RETRO_Y=', '.join(f'{loc(x, y)[1]}f' for x, y in S['retro']))
    wjson(f'data/hulls/{hid}.ship', ship)
    ship_rows.append(ship_row(key, hid, name, desig, size, rad))
    for r in extra_rows: r['number'] = len(ship_rows) + 1; ship_rows.append(r)
    variants_for(hid, key, slist, ship, modules)
    desc, tac = TL_DESC[key]
    desc_rows.append({'id': hid, 'type': 'SHIP', 'text1': rn(desc), 'text2': rn(tac or ''), 'text3': '', 'text4': ''})
    report.append((hid, size, len(ship['weaponSlots']), len(ship['builtInWeapons']), round(rad), ship['shieldRadius'],
                   [e['width'] for e in ship['engineSlots']]))
wcsv('data/hulls/ship_data.csv', SHIP_COLS, ship_rows)

wjson('data/config/engine_styles.json', {k: {"engineColor": [*c, 255], "engineCampaignColor": [*c, 200], "contrailParticleSizeMult": 5,
      "contrailParticleDuration": 1.4, "contrailParticleFinalSizeMult": 2.5, "contrailMaxSpeedMult": 0.5, "contrailAngularVelocityMult": 0,
      "contrailColor": [*c, 45], "contrailCampaignColor": [*c, 90], "type": "GLOW"} for k, c in ENGINE_STYLES.items()})
exec(open(_ROOT + '/build_v11_part2.py').read())
