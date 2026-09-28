import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
# GitHub README art for Terra Light: banner.png + roster.png (sprites from the built mod / ss_style composites)
import json, math, random, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
M = _ROOT + '/build/TerraLight/'; SS = _ROOT + '/ss_style/'
F = _ROOT + '/tools/fonts/'
OUT = _ROOT + '/../docs/'
os.makedirs(OUT, exist_ok=True)

def orb(size, w='Bold'):
    f = ImageFont.truetype(F + 'Orbitron.ttf', size)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f
def raj(size, semi=True): return ImageFont.truetype(F + ('Rajdhani-SemiBold.ttf' if semi else 'Rajdhani-Medium.ttf'), size)

SPR = {  # full-looking sprite per ship (moving parts composited in)
 'tiamat': M + 'graphics/ships/terralight/tl_tiamat.png', 'asura': M + 'graphics/ships/terralight/tl_asura.png',
 'neow': M + 'graphics/ships/terralight/tl_neow.png', 'artemis': M + 'graphics/ships/terralight/tl_artemis.png',
 'siren': SS + 'siren_ss_v12_battleship.png', 'hastur': SS + 'hastur_ss_v4_full.png',
 'hannibal': M + 'graphics/ships/terralight/tl_hannibal.png', 'regulus': M + 'graphics/ships/terralight/tl_regulus.png',
 'duilius': M + 'graphics/ships/terralight/tl_duilius.png', 'abaddon': M + 'graphics/ships/terralight/tl_abaddon.png',
 'iris': M + 'graphics/ships/terralight/tl_iris.png', 'selene': M + 'graphics/ships/terralight/tl_selene.png',
 'fenrir': SS + 'fenrir_ss_v4_full.png', 'hellhound': SS + 'hellhound_ss_v4_full.png', 'garm': SS + 'garm_ss_v4_full.png'}
ENGC = {'tiamat': (225, 120, 255), 'asura': (255, 150, 60), 'neow': (255, 150, 60), 'artemis': (255, 110, 190), 'siren': (255, 150, 60),
        'hastur': (90, 220, 240), 'hannibal': (225, 120, 255), 'regulus': (60, 225, 190), 'duilius': (255, 210, 90), 'abaddon': (120, 255, 150),
        'iris': (255, 110, 190), 'selene': (225, 120, 255), 'fenrir': (255, 150, 60), 'hellhound': (100, 170, 255), 'garm': (255, 150, 60)}

def ship_img(k):
    im = Image.open(SPR[k]).convert('RGBA')
    if k == 'abaddon':      # docked warhead under the frame
        t = Image.open(M + 'graphics/missiles/terralight/tl_apocalypse.png').convert('RGBA')
        base = Image.new('RGBA', im.size, (0, 0, 0, 0))
        base.alpha_composite(t, (im.width // 2 - t.width // 2, int(im.height / 2 - 9.5) - t.height // 2)); base.alpha_composite(im); im = base
    return im

def engines(k):
    h = json.load(open(M + f'data/hulls/tl_{k}.ship')); CX, CY = h['center']; H = h['height']
    return [(CX - e['location'][1], H - (e['location'][0] + CY), e['width'], e['length'], e['angle']) for e in h['engineSlots']]

def with_flames(k, scale):
    """sprite + soft additive-looking exhaust plumes below it, scaled"""
    im = ship_img(k); pad = 140
    c = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    glow = Image.new('RGBA', c.size, (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    col = ENGC[k]
    for (x, y, w, L, ang) in engines(k):
        x += pad; y += pad; a = math.radians(ang)
        ux, uy = -math.sin(a), -math.cos(a)
        L = L * 0.75
        for i in range(14):
            f = i / 13; r = w * (0.55 - 0.4 * f)
            cx, cy = x + ux * L * f, y + uy * L * f
            al = int(200 * (1 - f) ** 1.3)
            g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*col, al))
        g.ellipse([x - w * 0.3, y - w * 0.3, x + w * 0.3, y + w * 0.3], fill=(255, 250, 240, 230))
    glow = glow.filter(ImageFilter.GaussianBlur(5))
    c.alpha_composite(glow); c.alpha_composite(im, (pad, pad))
    return c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS), pad * scale

def space(W, H, seed=3, density=1.0):
    random.seed(seed)
    bg = Image.new('RGBA', (W, H), (6, 8, 18, 255))
    neb = Image.new('RGBA', (W, H), (0, 0, 0, 0)); n = ImageDraw.Draw(neb)
    for (cx, cy, r, col) in [(W * 0.78, H * 0.35, 260, (120, 40, 170, 120)), (W * 0.55, H * 0.9, 220, (40, 60, 160, 110)),
                             (W * 0.95, H * 0.85, 200, (200, 60, 140, 80)), (W * 0.2, H * 0.1, 180, (30, 80, 150, 70))]:
        n.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], fill=col)
    bg.alpha_composite(neb.filter(ImageFilter.GaussianBlur(90)))
    s = ImageDraw.Draw(bg)
    for _ in range(int(W * H / 1400 * density)):
        x, y = random.random() * W, random.random() * H; b = random.randint(90, 255); r = random.choice([0.5, 0.6, 0.8, 1.1, 1.5])
        s.ellipse([x - r, y - r, x + r, y + r], fill=(b, b, min(255, b + 20), 255))
    return bg

# ------------------------------------------------------------------ banner
W, H = 1280, 480
b = space(W, H)
fleet = [('siren', 0.40, 760, 170), ('tiamat', 0.40, 900, 160), ('neow', 0.40, 1040, 175), ('asura', 0.40, 1180, 160),
         ('hastur', 0.40, 720, 350), ('abaddon', 0.36, 860, 345), ('garm', 0.42, 990, 380), ('fenrir', 0.42, 1100, 375),
         ('hellhound', 0.42, 1215, 372)]
for k, sc, x, y in sorted(fleet, key=lambda f: f[3]):
    im, pad = with_flames(k, sc)
    b.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
shade = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(shade)
for x in range(0, 640):
    sd.line([(x, 0), (x, H)], fill=(4, 6, 14, int(235 * max(0, 1 - x / 640) ** 1.2)))
b.alpha_composite(shade)
d = ImageDraw.Draw(b)
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
gd.text((60, 120), 'TERRA LIGHT', font=orb(78, 'Black'), fill=(255, 110, 210, 255))
b.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
d.text((60, 120), 'TERRA LIGHT', font=orb(78, 'Black'), fill=(255, 238, 250, 255))
d.text((64, 222), 'EARTH LIGHT WARSHIPS FOR STARSECTOR', font=orb(22, 'Medium'), fill=(150, 220, 255, 255))
d.line([(64, 262), (520, 262)], fill=(255, 110, 210, 200), width=2)
d.text((64, 276), '15 ships  ·  custom ship systems  ·  moving parts', font=raj(28), fill=(220, 225, 240, 255))
d.text((64, 314), 'Unofficial fan mod  ·  Starsector 0.98a', font=raj(24, False), fill=(150, 160, 185, 255))
b.convert('RGB').save(OUT + 'banner.png', optimize=True)

# ------------------------------------------------------------------ roster
ROWS = [('CAPITAL SHIPS', [('tiamat', 'Tiamat', 'Battleship', 'Triple Overcharge'), ('asura', 'Asura-II', 'Advanced Battleship', 'Rail Overdrive'),
                          ('neow', 'Neow', 'Fortified Battleship', 'Damper Field + Flares'), ('artemis', 'Artemis', 'Catapult Carrier', 'Reserve Deployment'),
                          ('siren', 'Siren', 'Convertible Carrier', 'Battleship Mode')]),
        ('CRUISERS', [('hastur', 'Hastur', 'Battlecruiser', 'Replica Wing'), ('hannibal', 'Hannibal', 'Heavy Cruiser', 'AP Focus'),
                      ('regulus', 'Regulus', 'Escort Cruiser', 'Screen Overdrive'), ('duilius', 'Duilius', 'Claw Cruiser', 'Claw Strike'),
                      ('abaddon', 'Abaddon', 'Missile Cruiser', 'Apocalypse'), ('iris', 'Iris', 'Carrier', 'Reserve Deployment'),
                      ('selene', 'Selene', 'Fast Carrier', 'Wing Rally')]),
        ('DESTROYERS', [('fenrir', 'Fenrir', 'Interdiction Destroyer', 'Hit and Run'), ('hellhound', 'Hellhound', 'Light Destroyer', 'Execution Salvo'),
                        ('garm', 'Garm', 'Assault Destroyer', 'Phase Skimmer')])]
SC = {'CAPITAL SHIPS': 0.62, 'CRUISERS': 0.62, 'DESTROYERS': 0.62}      # one scale for all = true relative size
W = 1280
cells = []
for title, ships in ROWS:
    ims = [(s, ship_img(s[0])) for s in ships]
    ims = [(s, im.crop(im.getbbox()).resize((int(im.crop(im.getbbox()).width * SC[title]), int(im.crop(im.getbbox()).height * SC[title])), Image.LANCZOS)) for s, im in ims]
    cells.append((title, ims))
rowh = [max(im.height for _, im in ims) + 110 for _, ims in cells]
H = 150 + sum(rowh) + 60 * len(cells) + 40
r = space(W, H, seed=9, density=0.35)
d = ImageDraw.Draw(r)
d.text((W // 2, 60), 'THE FLEET', font=orb(46, 'Black'), fill=(255, 238, 250, 255), anchor='mm')
d.text((W // 2, 104), 'all ships shown at the same scale', font=raj(24, False), fill=(150, 160, 185, 255), anchor='mm')
y = 150
for (title, ims), rh in zip(cells, rowh):
    d.text((60, y), title, font=orb(22, 'Bold'), fill=(150, 220, 255, 255)); d.line([(60, y + 34), (W - 60, y + 34)], fill=(90, 110, 160, 160), width=1)
    y += 56
    n = len(ims); slot = (W - 120) / n
    for i, ((k, name, desig, sysname), im) in enumerate(ims):
        cx = 60 + slot * (i + 0.5)
        top = y + (rh - 110 - im.height)
        r.alpha_composite(im, (int(cx - im.width / 2), int(top)))
        ty = y + rh - 100
        d.text((cx, ty), name.upper(), font=orb(19, 'Bold'), fill=(255, 238, 250, 255), anchor='mt')
        d.text((cx, ty + 28), desig, font=raj(20), fill=(200, 205, 225, 255), anchor='mt')
        d.text((cx, ty + 52), sysname, font=raj(19, False), fill=(*ENGC[k], 255), anchor='mt')
    y += rh + 4
r.convert('RGB').save(OUT + 'roster.png', optimize=True)
print('ok', os.listdir(OUT))
