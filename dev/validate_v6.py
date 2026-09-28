import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
import json, csv, os, re, glob, sys
import os as _os
_ROOT = _os.path.dirname(_os.path.abspath(__file__))
M = _ROOT + '/build/TerraLight'
REF = json.load(open(_ROOT + '/vanilla_ref.json'))
err = []; warn = []

def lj(p):
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'(?m)^\s*#.*$', '', t)          # SS allows # comments
    t = re.sub(r',(\s*[}\]])', r'\1', t)         # and trailing commas
    t = re.sub(r'\[([A-Z_][A-Z_, ]*)\]', lambda m: '[' + ','.join('"%s"' % x.strip() for x in m.group(1).split(',') if x.strip()) + ']', t)
    t = re.sub(r':\s*([A-Z_]+)\s*([,}])', r':"\1"\2', t)
    try: return json.loads(t)
    except Exception as e: err.append(f'JSON {p}: {e}'); return None

def rcsv(p):
    rows = list(csv.reader(open(p, encoding='utf-8')))
    hdr = rows[0]
    for i, r in enumerate(rows[1:], 2):
        if r and any(r) and len(r) != len(hdr): err.append(f'CSV {p} row {i}: {len(r)} cols vs {len(hdr)}')
    return [dict(zip(hdr, r)) for r in rows[1:] if r and any(r) and not r[0].startswith('#') and r[hdr.index('id')] if 'id' in hdr]

# all json-ish files parse
for p in glob.glob(M + '/**/*', recursive=True):
    if p.endswith(('.json', '.ship', '.variant', '.wpn', '.proj', '.system', '.faction')): lj(p)

# id sets
def ids(p, col='id'):
    return {r[col] for r in rcsv(p)}
vw = set(REF['weapon_op']); mw = ids(M + '/data/weapons/weapon_data.csv')
vs = set(REF['system_ids']); ms = ids(M + '/data/shipsystems/ship_systems.csv')
vh = set(REF['hullmod_cost']); mh = ids(M + '/data/hullmods/hull_mods.csv')
vwing = set(REF['wing_op'])
vproj = set(REF['proj_ids'])
mproj = {lj(p)['id'] for p in glob.glob(M + '/data/weapons/proj/*.proj')}
vstyles = set(REF['engine_styles'])
mstyles = set(lj(M + '/data/config/engine_styles.json') or {})
allw = vw | mw; alls = vs | ms; allh = vh | mh

# ship_data
sd = rcsv(M + '/data/hulls/ship_data.csv')
hulls = {}
for p in glob.glob(M + '/data/hulls/*.ship'):
    h = lj(p); hulls[h['hullId']] = h
    if not os.path.exists(M + '/' + h['spriteName']): err.append(f'sprite missing {h["spriteName"]}')
    for s in h.get('weaponSlots', []):
        if s['type'] != 'STATION_MODULE' and s['mount'] not in ('TURRET', 'HARDPOINT', 'HIDDEN'): err.append(f'{p} bad mount {s}')
    for bw in h.get('builtInWeapons', {}).values():
        if bw not in allw: err.append(f'{h["hullId"]} builtin weapon {bw} unknown')
    for bm in h.get('builtInMods', []):
        if bm not in allh: err.append(f'{h["hullId"]} builtin mod {bm} unknown')
    for bw in h.get('builtInWings', []):
        if bw not in vwing: err.append(f'{h["hullId"]} builtin wing {bw} unknown')
    for e in h.get('engineSlots', []):
        if e.get('style') == 'CUSTOM' and e.get('styleId') not in mstyles | vstyles: err.append(f'{h["hullId"]} engine style {e.get("styleId")}')
    sl = {s['id'] for s in h.get('weaponSlots', [])}
    for k in h.get('builtInWeapons', {}):
        if k not in sl: err.append(f'{h["hullId"]} builtin on missing slot {k}')
for r in sd:
    if r['id'] not in hulls: err.append(f'ship_data id {r["id"]} has no .ship')
    for col in ('system id', 'defense id'):
        sysid = r.get(col, '')
        if sysid and sysid not in alls: err.append(f'{r["id"]} {col} {sysid} unknown')
for hid in hulls:
    if hid not in {r['id'] for r in sd}: err.append(f'.ship {hid} not in ship_data')

# variants
for p in glob.glob(M + '/data/variants/*.variant'):
    v = lj(p); h = hulls.get(v['hullId'])
    if not h: err.append(f'{p} hull {v["hullId"]} unknown'); continue
    slots = {s['id']: s for s in h.get('weaponSlots', [])}
    for g in v.get('weaponGroups', []):
        for sid, wid in g['weapons'].items():
            if sid not in slots: err.append(f'{v["variantId"]} slot {sid} not on hull')
            if wid not in allw: err.append(f'{v["variantId"]} weapon {wid} unknown')
    for w in v.get('wings', []):
        if w not in vwing: err.append(f'{v["variantId"]} wing {w} unknown')
    for hm in v.get('hullMods', []) + v.get('permaMods', []):
        if hm not in allh: err.append(f'{v["variantId"]} hullmod {hm} unknown')
    for m in v.get('modules', []):
        for sid, mv in m.items():
            if sid not in slots: err.append(f'{v["variantId"]} module slot {sid} missing')
            if not os.path.exists(f'{M}/data/variants/{mv}.variant'): err.append(f'module variant {mv} missing')

# weapons
for p in glob.glob(M + '/data/weapons/*.wpn'):
    w = lj(p)
    if w['id'] not in mw: err.append(f'wpn {w["id"]} not in weapon_data.csv')
    for k in ('turretSprite', 'hardpointSprite', 'turretUnderSprite', 'hardpointUnderSprite'):
        if k in w and w[k] and not os.path.exists(M + '/' + w[k]): err.append(f'{w["id"]} {k} missing {w[k]}')
    if 'projectileSpecId' in w and w['projectileSpecId'] not in vproj | mproj: err.append(f'{w["id"]} proj {w["projectileSpecId"]} unknown')
for p in glob.glob(M + '/data/weapons/proj/*.proj'):
    j = lj(p)
    if j.get('sprite') and not os.path.exists(M + '/' + j['sprite']): err.append(f'proj sprite missing {j["sprite"]}')
for r in rcsv(M + '/data/weapons/weapon_data.csv'):
    if not os.path.exists(f'{M}/data/weapons/{r["id"]}.wpn'): err.append(f'weapon_data {r["id"]} has no .wpn')

# systems
for p in glob.glob(M + '/data/shipsystems/*.system'):
    j = lj(p)
    for k in ('statsScript', 'aiScript'):
        if j.get(k):
            f = M + '/' + j[k].replace('.', '/') + '.java'
            if not os.path.exists(f): err.append(f'{k} {j[k]} -> no {f}')
for r in rcsv(M + '/data/hullmods/hull_mods.csv'):
    f = M + '/' + r['script'].replace('.', '/') + '.java'
    if not os.path.exists(f): err.append(f'hullmod script missing {f}')

# sounds
snd = ' '.join('"%s"' % x for x in REF['sound_ids'])
for p in glob.glob(M + '/data/**/*.*', recursive=True):
    if p.endswith(('.wpn', '.system')):
        for k, v in re.findall(r'"(\w*[sS]ound\w*)"\s*:\s*"([^"]+)"', open(p).read()):
            if f'"{v}"' not in snd: err.append(f'{os.path.basename(p)} sound {v} not in vanilla sounds.json')
for p in glob.glob(M + '/data/**/*.java', recursive=True):
    for v in re.findall(r'playSound\("([^"]+)"', open(p).read()):
        if f'"{v}"' not in snd: err.append(f'{os.path.basename(p)} sound {v} missing')
    for v in re.findall(r'spawnProjectile\([^,]+,[^,]+,\s*"([^"]+)"', open(p).read()):
        if v not in allw: err.append(f'{os.path.basename(p)} spawns unknown weapon {v}')
# system files exist for our csv rows + weapon for WEAPON systems
for r in rcsv(M + '/data/shipsystems/ship_systems.csv'):
    if not os.path.exists(f'{M}/data/shipsystems/{r["id"]}.system'): err.append(f'system {r["id"]} has no .system')
for p in glob.glob(M + '/data/shipsystems/*.system'):
    j = lj(p)
    if j.get('weaponDataId') and j['weaponDataId'] not in allw: err.append(f'{p} weapon {j["weaponDataId"]} unknown')
# settings graphics
st = lj(M + '/data/config/settings.json')
for cat, d in st.get('graphics', {}).items():
    for k, v in d.items():
        if not os.path.exists(M + '/' + v): err.append(f'settings sprite {k} missing {v}')
# decorative frames
for p in glob.glob(M + '/data/weapons/*.wpn'):
    w = lj(p)
    for i in range(1, w.get('numFrames', 1)):
        f = M + '/' + w['turretSprite'].replace('_00.png', f'_{i:02d}.png')
        if not os.path.exists(f): err.append(f'frame missing {f}')
# faction / descriptions
fac = lj(M + '/data/world/factions/independent.faction')
for hid in fac.get('knownShips', {}).get('hulls', []):
    if hid not in hulls: err.append(f'faction hull {hid} unknown')
rcsv(M + '/data/strings/descriptions.csv')
mi = lj(M + '/mod_info.json'); print('mod_info', mi)
print('ERRORS', len(err)); print('\n'.join(err))
print('WARN', len(warn)); print('\n'.join(warn))
