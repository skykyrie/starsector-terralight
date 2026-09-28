# build_v6 part 2 - weapons, ship systems, hullmods, scripts, settings (exec'd from build_v6.py)

# ======================================================================================= weapons
blank = 'graphics/weapons/terralight/tl_blank.png'
Image.new('RGBA', (4, 4), (0, 0, 0, 0)).save(f'{MOD}/{blank}')
def cp(src, dst): shutil.copy(src, f'{MOD}/{dst}'); return dst
tri = cp(WP + 'tl_triplebeam_turret_ss_v10.png', 'graphics/weapons/terralight/tl_triplebeam_turret.png')
qr = cp(WP + 'tl_quadrail_turret_ss_v3.png', 'graphics/weapons/terralight/tl_quadrail_turret.png')
hb = cp(WP + 'tl_hastur_beam_turret_ss_v1.png', 'graphics/weapons/terralight/tl_hastur_beam_turret.png')
arm = cp(WP + 'tl_armageddon_torpedo.png', 'graphics/missiles/terralight/tl_armageddon_torpedo.png')
ap = Image.open(SS + 'apocalypse_ss_v2.png'); apc = ap.crop(ap.getbbox()); apc.save(f'{MOD}/graphics/missiles/terralight/tl_apocalypse.png')
SPRITES['apocalypse_docked'] = 'graphics/missiles/terralight/tl_apocalypse.png'
APW, APH = apc.size
def bubble():
    im = Image.new('RGBA', (12, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((2, 5, 9, 15), 2, fill=(240, 196, 60, 255), outline=(90, 70, 20, 255))
    d.ellipse((1, 0, 10, 9), fill=(236, 60, 80, 255), outline=(100, 20, 30, 255)); d.ellipse((3, 2, 6, 5), fill=(255, 190, 200, 255))
    return im
def claw():
    # big three-finger grapple claw (twice the old size): gunmetal hub, yellow hooked talons, cable socket
    S = 4; W, H = 32 * S, 40 * S
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = W // 2
    d.rectangle((cx - 3 * S, 30 * S, cx + 3 * S, 39 * S), fill=(46, 50, 56, 255))
    d.ellipse((cx - 8 * S, 18 * S, cx + 8 * S, 32 * S), fill=(96, 102, 110, 255), outline=(28, 30, 34, 255), width=S)
    d.ellipse((cx - 4 * S, 21 * S, cx + 4 * S, 28 * S), fill=(140, 146, 154, 255))
    for side in (-1, 1):
        pts = [(cx + side * 6 * S, 22 * S), (cx + side * 13 * S, 12 * S), (cx + side * 12 * S, 3 * S), (cx + side * 8 * S, 1 * S)]
        d.line(pts, fill=(40, 34, 12, 255), width=5 * S, joint='curve'); d.line(pts, fill=(255, 198, 46, 255), width=3 * S, joint='curve')
    pts = [(cx, 20 * S), (cx, 8 * S), (cx - 2 * S, 1 * S)]
    d.line(pts, fill=(40, 34, 12, 255), width=5 * S, joint='curve'); d.line(pts, fill=(255, 198, 46, 255), width=3 * S, joint='curve')
    d.ellipse((cx - 2 * S, 24 * S, cx + 2 * S, 27 * S), fill=(255, 90, 60, 255))
    return im.resize((32, 40), Image.LANCZOS)
bubble().save(f'{MOD}/graphics/missiles/terralight/tl_bubble.png'); claw().save(f'{MOD}/graphics/missiles/terralight/tl_claw.png')

def missile_proj(pid, sprite, size, center, crad, color, acc, turn, hp_expl, expl_r, eng_loc, eng_w, eng_len, arming=0.3, mtype='MISSILE', maxspeed=None):
    d = {"id": pid, "specClass": "missile", "missileType": mtype, "sprite": sprite, "size": size, "center": center,
         "collisionRadius": crad, "collisionClass": "MISSILE_NO_FF", "explosionColor": [*color, 255], "explosionRadius": expl_r,
         "flameoutTime": 1, "armingTime": arming, "noEngineGlowTime": 0.1, "fadeTime": 0.5,
         "engineSpec": {"turnAcc": turn * 3, "turnRate": turn, "acc": acc, "dec": acc / 2},
         "engineSlots": [{"id": "ES1", "loc": eng_loc, "style": "CUSTOM",
             "styleSpec": {"mode": "QUAD_STRIP", "engineColor": [*color, 255], "contrailDuration": 1, "contrailWidthMult": 1,
                           "contrailWidthAddedFractionAtEnd": 2, "contrailMinSeg": 5, "contrailMaxSpeedMult": 0.5,
                           "contrailAngularVelocityMult": 0.5, "contrailColor": [*color, 60], "type": "GLOW"},
             "width": eng_w, "length": eng_len, "angle": 180.0}]}
    if maxspeed: d["engineSpec"]["maxSpeed"] = maxspeed
    if hp_expl: d["explosionSpec"] = {"duration": 0.1, "radius": hp_expl[0], "coreRadius": hp_expl[1], "collisionClass": "HITS_SHIPS_AND_ASTEROIDS",
        "collisionClassByFighter": "HITS_SHIPS_AND_ASTEROIDS", "particleSizeMin": 5.0, "particleSizeRange": 3.0, "particleDuration": 1,
        "particleCount": 150, "particleColor": [*color, 255], "explosionColor": [*color, 255],
        "detailedExplosionFlashColorFringe": [*color, 255], "detailedExplosionFlashRadius": hp_expl[0] * 2.5, "useDetailedExplosion": True}
    wjson(f'data/weapons/proj/{pid}.proj', d)

missile_proj('tl_armageddon_torp', arm, [64, 132], [32, 66], 40, (255, 140, 60), 220, 12, (320, 140), 900, [-60, 0], 30, 120, arming=1.0, mtype='ROCKET')
# Apocalypse: steered by TL_ApocalypseStats' own AI (drift -> burn); big green bell flame
missile_proj('tl_apocalypse_torp', 'graphics/missiles/terralight/tl_apocalypse.png', [APW, APH], [APW / 2, APH / 2], 60, (120, 255, 150), 220, 40,
             (260, 130), 600, [-(APH / 2 - 10), 0], 90, 320, arming=0.1, mtype='MISSILE', maxspeed=520)
missile_proj('tl_bubble_warhead', 'graphics/missiles/terralight/tl_bubble.png', [12, 16], [6, 8], 8, (255, 90, 110), 900, 90, None, 130, [-8, 0], 5, 16)
missile_proj('tl_claw_proj', 'graphics/missiles/terralight/tl_claw.png', [32, 40], [16, 20], 18, (255, 200, 60), 900, 160, None, 90, [-20, 0], 8, 26)
# Tiamat: the triple cannon fires beam-like energy bolts (projectiles), not a continuous laser
wjson('data/weapons/proj/tl_triplebeam_shot.proj', {"id": "tl_triplebeam_shot", "specClass": "projectile", "spawnType": "BALLISTIC_AS_BEAM",
      "collisionClass": "RAY", "collisionClassByFighter": "RAY_FIGHTER", "length": 150.0, "width": 20.0, "fadeTime": 0.3,
      "fringeColor": [255, 70, 170, 255], "coreColor": [255, 240, 250, 255], "textureType": "SMOOTH", "textureScrollSpeed": -256.0,
      "pixelsPerTexel": 1.0})

def wpn(wid, spec): wjson(f'data/weapons/{wid}.wpn', dict({"id": wid}, **spec))
BEAM = lambda size, spr, offs, fringe, core, width: {"specClass": "beam", "type": "ENERGY", "size": size, "displayArcRadius": 600,
    "turretSprite": spr, "hardpointSprite": spr, "turretOffsets": offs, "turretAngleOffsets": [0] * (len(offs) // 2),
    "hardpointOffsets": offs, "hardpointAngleOffsets": [0] * (len(offs) // 2), "barrelMode": "LINKED",
    "fringeColor": [*fringe, 255], "coreColor": [*core, 255], "glowColor": [*fringe, 255], "darkCore": False, "width": width,
    "textureType": "ROUGH", "textureScrollSpeed": 64.0, "pixelsPerTexel": 5.0, "collisionClass": "RAY", "collisionClassByFighter": "RAY_FIGHTER",
    "fireSoundTwo": "high_intensity_laser_loop"}
wpn('tl_triplebeam', {"specClass": "projectile", "type": "ENERGY", "size": "LARGE", "displayArcRadius": 900,
    "turretSprite": tri, "hardpointSprite": tri, "turretOffsets": [54, 0, 46, 0, 38, 0], "turretAngleOffsets": [0, 0, 0],
    "hardpointOffsets": [54, 0, 46, 0, 38, 0], "hardpointAngleOffsets": [0, 0, 0], "barrelMode": "LINKED",
    "animationType": "MUZZLE_FLASH", "glowColor": [255, 90, 190, 255],
    "muzzleFlashSpec": {"length": 45.0, "spread": 10.0, "particleSizeMin": 14.0, "particleSizeRange": 16.0, "particleDuration": 0.15,
                        "particleCount": 12, "particleColor": [255, 120, 200, 255]},
    "projectileSpecId": "tl_triplebeam_shot", "fireSoundTwo": "pulse_laser_fire"})
wjson('data/weapons/proj/tl_hastur_shot.proj', {"id": "tl_hastur_shot", "specClass": "projectile", "spawnType": "BALLISTIC_AS_BEAM",
      "collisionClass": "RAY", "collisionClassByFighter": "RAY_FIGHTER", "length": 110.0, "width": 14.0, "fadeTime": 0.25,
      "fringeColor": [255, 90, 190, 255], "coreColor": [255, 235, 250, 255], "textureType": "SMOOTH", "textureScrollSpeed": -256.0,
      "pixelsPerTexel": 1.0})
wpn('tl_hastur_beam', {"specClass": "projectile", "type": "ENERGY", "size": "MEDIUM", "displayArcRadius": 700,
    "turretSprite": hb, "hardpointSprite": hb, "turretOffsets": [36, -4, 36, 4], "turretAngleOffsets": [0, 0],
    "hardpointOffsets": [36, -4, 36, 4], "hardpointAngleOffsets": [0, 0], "barrelMode": "LINKED", "animationType": "MUZZLE_FLASH",
    "glowColor": [255, 90, 190, 255],
    "muzzleFlashSpec": {"length": 30.0, "spread": 8.0, "particleSizeMin": 10.0, "particleSizeRange": 10.0, "particleDuration": 0.12,
                        "particleCount": 8, "particleColor": [255, 130, 210, 255]},
    "projectileSpecId": "tl_hastur_shot", "fireSoundTwo": "pulse_laser_fire"})
QRS = {"specClass": "projectile", "type": "BALLISTIC", "size": "LARGE", "displayArcRadius": 1200, "turretSprite": qr, "hardpointSprite": qr,
       "turretOffsets": [78, -7, 78, 7, 78, -16, 78, 16], "turretAngleOffsets": [0, 0, 0, 0], "hardpointOffsets": [78, -7, 78, 7, 78, -16, 78, 16],
       "hardpointAngleOffsets": [0, 0, 0, 0], "barrelMode": "ALTERNATING", "animationType": "MUZZLE_FLASH",
       "muzzleFlashSpec": {"length": 50.0, "spread": 6.0, "particleSizeMin": 12.0, "particleSizeRange": 12.0, "particleDuration": 0.18,
                           "particleCount": 14, "particleColor": [255, 180, 120, 255]},
       "projectileSpecId": "railgun_shot", "fireSoundTwo": "railgun_fire"}
wpn('tl_quadrail', QRS); wpn('tl_quadrail_twin', dict(QRS, turretSprite=blank, hardpointSprite=blank, projectileSpecId="heavymauler_shot",
                                                     fireSoundTwo="heavy_mauler_fire"))
MSL = lambda size, spr, offs, proj, sound="swarmer_fire": {"specClass": "projectile", "type": "MISSILE", "size": size,
    "turretSprite": spr, "hardpointSprite": spr, "turretOffsets": offs, "turretAngleOffsets": [0] * (len(offs) // 2),
    "hardpointOffsets": offs, "hardpointAngleOffsets": [0] * (len(offs) // 2), "barrelMode": "ALTERNATING", "animationType": "SMOKE",
    "renderHints": [], "displayArcRadius": 800,
    "smokeSpec": {"particleSizeMin": 12.0, "particleSizeRange": 12.0, "cloudParticleCount": 6, "cloudDuration": 1.0, "cloudRadius": 8.0,
                  "blowbackParticleCount": 3, "blowbackDuration": 1.5, "blowbackLength": 18.0, "blowbackSpread": 12.0, "particleColor": [180, 170, 160, 100]},
    "projectileSpecId": proj, "fireSoundTwo": sound}
NEOW = json.load(open(SS + 'neow_ss_v6_slots.json'))['slots'][0]['offsets']
wpn('tl_armageddon', MSL('LARGE', blank, [c for o in NEOW for c in o], 'tl_armageddon_torp', sound="reaper_fire"))
wpn('tl_apocalypse', MSL('LARGE', blank, [0, 0], 'tl_apocalypse_torp', sound="reaper_fire"))
wpn('tl_bubble', MSL('MEDIUM', blank, [4, -8, 4, -3, 4, 3, 4, 8], 'tl_bubble_warhead'))
wpn('tl_claw', MSL('SMALL', blank, [2, 0], 'tl_claw_proj', sound="harpoon_fire"))
# Neow flare tubes (fired from the 8 SYSTEM slots all round the hull by the right-click defence system)
wpn('tl_neow_flare', {"specClass": "projectile", "type": "SYSTEM", "size": "SMALL", "turretSprite": "", "hardpointSprite": "",
    "hardpointOffsets": [0, 0], "turretOffsets": [0, 0], "hardpointAngleOffsets": [0], "turretAngleOffsets": [0], "barrelMode": "ALTERNATING",
    "animationType": "SMOKE", "interruptibleBurst": False,
    "smokeSpec": {"particleSizeMin": 10.0, "particleSizeRange": 10.0, "cloudParticleCount": 3, "cloudDuration": 1.0, "cloudRadius": 10.0,
                  "blowbackParticleCount": 0, "blowbackDuration": 2.0, "blowbackLength": 30.0, "blowbackSpread": 10.0, "particleColor": [100, 100, 100, 150]},
    "projectileSpecId": "flare_standard", "fireSoundTwo": "launch_flare_1"})
# decorative moving parts (Siren deck frames, Fenrir boosters, Garm pods)
for did, (path, dsize, nframes) in DECO.items():
    spec = {"specClass": "beam", "type": "DECORATIVE", "size": dsize, "showDamageWhenDecorative": False, "renderBelowAllWeapons": True,
            "turretSprite": path, "hardpointSprite": path, "turretOffsets": [0, 0], "turretAngleOffsets": [0],
            "hardpointOffsets": [0, 0], "hardpointAngleOffsets": [0], "fringeColor": [255, 255, 255, 255], "coreColor": [255, 255, 255, 255],
            "glowColor": [255, 255, 255, 255], "width": 1.0, "textureType": "ROUGH", "textureScrollSpeed": 1.0, "pixelsPerTexel": 1.0}
    if nframes > 1: spec.update(numFrames=nframes, frameRate=0, alwaysAnimate=False)
    wpn(did, spec)

WPN_COLS = 'name,id,tier,rarity,base value,range,damage/second,damage/shot,emp,impact,turn rate,OPs,ammo,ammo/sec,reload size,type,energy/shot,energy/second,chargeup,chargedown,burst size,burst delay,min spread,max spread,spread/shot,spread decay/sec,beam speed,proj speed,launch speed,flight time,proj hitpoints,autofireAccBonus,extraArcForAI,hints,tags,groupTag,tech/manufacturer,for weapon tooltip>>,primaryRoleStr,speedStr,trackingStr,turnRateStr,accuracyStr,customPrimary,customPrimaryHL,customAncillary,customAncillaryHL,noDPSInTooltip,number'.split(',')
common = {'tier': 3, 'rarity': 0, 'base value': 0, 'OPs': 0, 'tags': 'no_drop, no_dealer, no_sell', 'tech/manufacturer': 'Terra Light'}
W_ROWS = [
 dict(common, name='Triple Beam Cannon', id='tl_triplebeam', range=1100, **{'damage/shot': 220, 'impact': 12, 'turn rate': 16, 'type': 'ENERGY',
      'energy/shot': 180, 'chargeup': 0.1, 'chargedown': 0.6, 'proj speed': 1500, 'primaryRoleStr': 'Built-in Beam Cannon', 'number': 1}),
 dict(common, name='Twin Beam Cannon', id='tl_hastur_beam', range=900, **{'damage/shot': 130, 'impact': 8, 'turn rate': 24, 'type': 'ENERGY',
      'energy/shot': 110, 'chargeup': 0.05, 'chargedown': 0.45, 'proj speed': 1400, 'primaryRoleStr': 'Built-in Beam Cannon', 'number': 2}),
 dict(common, name='Quad Railgun', id='tl_quadrail', range=1200, **{'damage/shot': 250, 'impact': 40, 'turn rate': 18, 'type': 'KINETIC',
      'energy/shot': 300, 'chargedown': 0.8, 'burst size': 4, 'burst delay': 0.08, 'proj speed': 1400, 'primaryRoleStr': 'Built-in Kinetic', 'number': 3}),
 dict(common, name='Quad Railgun (Lower)', id='tl_quadrail_twin', range=1200, **{'damage/shot': 250, 'impact': 40, 'turn rate': 18,
      'type': 'HIGH_EXPLOSIVE', 'energy/shot': 280, 'chargedown': 0.8, 'burst size': 4, 'burst delay': 0.08, 'proj speed': 1200,
      'primaryRoleStr': 'Built-in Explosive', 'number': 4}),
 dict(common, name='Armageddon Torpedo', id='tl_armageddon', range=2500, **{'damage/shot': 5000, 'impact': 100, 'turn rate': 20, 'ammo': 9,
      'ammo/sec': 0.2, 'reload size': 3, 'type': 'HIGH_EXPLOSIVE', 'chargedown': 1, 'burst size': 3, 'burst delay': 0.4, 'proj speed': 400,
      'launch speed': 60, 'flight time': 8, 'proj hitpoints': 1500, 'hints': 'STRIKE', 'primaryRoleStr': 'Built-in Torpedo', 'number': 5}),
 dict(common, name='Apocalypse Warhead', id='tl_apocalypse', range=3000, **{'damage/shot': 3000, 'impact': 300, 'turn rate': 40, 'ammo': 1,
      'type': 'HIGH_EXPLOSIVE', 'chargedown': 1, 'burst size': 1, 'proj speed': 520, 'launch speed': 70, 'flight time': 16, 'proj hitpoints': 30000,
      'hints': 'SYSTEM', 'primaryRoleStr': 'One-shot Warhead', 'number': 6}),
 dict(common, name='Bubble Missile Pod', id='tl_bubble', range=750, **{'damage/shot': 250, 'impact': 5, 'turn rate': 60, 'ammo': 24,
      'ammo/sec': 0.8, 'reload size': 4, 'type': 'ENERGY', 'chargedown': 2, 'burst size': 4, 'burst delay': 0.1, 'proj speed': 500,
      'launch speed': 100, 'flight time': 2.2, 'proj hitpoints': 60, 'primaryRoleStr': 'Built-in Missile', 'number': 7}),
 dict(common, name='Grapple Claw', id='tl_claw', range=1200, **{'damage/shot': 700, 'emp': 300, 'impact': 60, 'turn rate': 160, 'ammo': 1,
      'type': 'FRAGMENTATION', 'chargedown': 1, 'burst size': 1, 'proj speed': 700, 'launch speed': 250, 'flight time': 3,
      'proj hitpoints': 200, 'hints': 'SYSTEM', 'primaryRoleStr': 'Claw Strike', 'number': 8}),
 dict(common, name='Neow Flare Tube', id='tl_neow_flare', range=400, **{'damage/shot': 10, 'emp': 100, 'ammo/sec': 0, 'type': 'ENERGY',
      'energy/shot': 0, 'energy/second': 0, 'chargeup': 0, 'chargedown': 0.1, 'burst size': 4, 'burst delay': 0.1, 'min spread': 40,
      'max spread': 40, 'proj speed': 150, 'launch speed': 300, 'flight time': 3, 'proj hitpoints': 1, 'hints': 'SYSTEM', 'number': 9}),
]
for i, did in enumerate(DECO): W_ROWS.append({'name': did, 'id': did, 'hints': 'SYSTEM', 'tags': 'hide_in_codex', 'number': 10 + i})
for r in W_ROWS:
    if r['id'] in ('tl_apocalypse', 'tl_claw', 'tl_neow_flare'): r['tags'] = r['tags'] + ', hide_in_codex'
wcsv('data/weapons/weapon_data.csv', WPN_COLS, W_ROWS)
WDESC = {'tl_triplebeam': "One of the Tiamat's four triple-barrel beam cannons. Each shot is a linked volley of three high-energy bolts.",
         'tl_hastur_beam': "Over-under twin beam cannon on the Hastur's side sponsons, firing linked pairs of high-energy bolts.",
         'tl_quadrail': "The Asura-II's four-barrel railgun turret. A twin loaded with explosive slugs is mounted under the hull.",
         'tl_quadrail_twin': "The lower twin of the Asura-II's Quad Railgun, firing explosive slugs from under the hull.",
         'tl_armageddon': "The Neow's three launch tubes fire Armageddon torpedoes one after another. The magazine reloads all three together.",
         'tl_apocalypse': "The Abaddon carries a single cruiser-sized warhead between its boosters. Launched by the ship system, once per battle.",
         'tl_bubble': "Short-range energy warheads fired in salvos from the Regulus' green pods to break up close-in attackers.",
         'tl_claw': "Remote grapple claws launched from the Duilius' side galleries by its ship system."}
for wid, t in WDESC.items(): desc_rows.append({'id': wid, 'type': 'WEAPON', 'text1': t, 'text2': '', 'text3': 'Built-in weapon.', 'text4': ''})

# ======================================================================================= ship systems
def vanilla_system(name):
    return REF['system_templates'][name]
def sys_from(template, sid, stats_cls=None, ai=None, ai_script=None, extra=None, weapon_types=None):
    t = vanilla_system(template)
    if weapon_types: t = re.sub(r'"weaponTypes"\s*:\s*\[[^\]]*\]', f'"weaponTypes":[{weapon_types}]', t)
    t = re.sub(r'"id"\s*:\s*"[^"]*"', f'"id":"{sid}"', t, count=1)
    if stats_cls: t = re.sub(r'"statsScript"\s*:\s*"[^"]*"', f'"statsScript":"data.shipsystems.scripts.{stats_cls}"', t, count=1)
    if ai: t = re.sub(r'"aiType"\s*:\s*"[^"]*"', f'"aiType":"{ai}"', t, count=1)
    if ai_script: t = t.replace(f'"aiType":"{ai}"', f'"aiType":"{ai}",\n\t"aiScript":"data.shipsystems.scripts.ai.{ai_script}"', 1)
    if extra: t = t.replace('"type"', extra + '\n\t"type"', 1)
    t = re.sub(r'(?m)^\s*#.*\n', '', t)                 # drop the vanilla developer comments
    t = re.sub(r'\s#[^\n"]*$', '', t, flags=re.M)
    t = re.sub(r'\n\s*\n+', '\n', t)
    open(f'{MOD}/data/shipsystems/{sid}.system', 'w').write(t)

sys_from('highenergyfocus', 'tl_triple_overcharge', 'TL_TripleOverchargeStats')
sys_from('ammofeed', 'tl_rail_overdrive', 'TL_RailOverdriveStats')
sys_from('highenergyfocus', 'tl_ap_focus', 'TL_APFocusStats')
sys_from('ammofeed', 'tl_pd_overdrive', 'TL_PDOverdriveStats', weapon_types='ENERGY, MISSILE')
sys_from('targetingfeed', 'tl_wing_rally', 'TL_WingRallyStats')
sys_from('maneuveringjets', 'tl_hit_and_run', 'TL_HitAndRunStats', ai='BURN_DRIVE')
sys_from('ammofeed', 'tl_execution', 'TL_ExecutionStats')
sys_from('reservewing', 'tl_replica_wing', 'TL_ReplicaWingStats', ai='CUSTOM', ai_script='TL_ReplicaWingAI')
sys_from('ammofeed', 'tl_claw_strike', 'TL_ClawStrikeStats', ai='CUSTOM', ai_script='TL_ClawStrikeAI', weapon_types='MISSILE')
for sid, cls, ai, snd in (('tl_apocalypse', 'TL_ApocalypseStats', 'TL_ApocalypseAI', 'system_forgevats'),
                          ('tl_siren_mode', 'TL_SirenModeStats', 'TL_SirenModeAI', 'system_forgevats')):
    wjson(f'data/shipsystems/{sid}.system', {"id": sid, "type": "STAT_MOD", "aiType": "CUSTOM",
          "aiScript": f"data.shipsystems.scripts.ai.{ai}", "statsScript": f"data.shipsystems.scripts.{cls}",
          "useSound": snd, "outOfUsesSound": "gun_out_of_ammo"})
open(f'{MOD}/data/shipsystems/tl_flare_screen.system', 'w').write(json.dumps({"id": "tl_flare_screen", "type": "WEAPON", "aiType": "FLARE",
     "weaponDataId": "tl_neow_flare", "outOfUsesSound": "gun_out_of_ammo"}, indent=1))
SYS_COLS = 'name,id,flux/second,f/s (base rate),f/s (base cap),flux/use,f/u (base rate),f/u (base cap),cr/u,max uses,regen,charge up,active,down,cooldown,toggle,noDissipation,noHardDissipation,hardFlux,noFiring,noTurning,noStrafing,noAccel,noShield,noVent,isPhaseCloak,tags,icon'.split(',')
IC = 'graphics/icons/hullsys/'
SYS_ROWS = [
 dict(name='Triple Overcharge', id='tl_triple_overcharge', **{'charge up': 0.5, 'active': 8, 'down': 1, 'cooldown': 18, 'tags': 'offensive', 'icon': IC + 'high_energy_focus.png'}),
 dict(name='Rail Overdrive', id='tl_rail_overdrive', **{'charge up': 0.5, 'active': 8, 'down': 1, 'cooldown': 18, 'tags': 'offensive', 'icon': IC + 'ammo_feeder.png'}),
 dict(name='AP Focus', id='tl_ap_focus', **{'charge up': 0.5, 'active': 7, 'down': 1, 'cooldown': 15, 'tags': 'offensive', 'icon': IC + 'high_energy_focus.png'}),
 dict(name='Screen Overdrive', id='tl_pd_overdrive', **{'charge up': 0.3, 'active': 8, 'down': 1, 'cooldown': 16, 'tags': 'defensive', 'icon': IC + 'missile_racks.png'}),
 dict(name='Wing Rally', id='tl_wing_rally', **{'charge up': 0.5, 'active': 8, 'down': 1, 'cooldown': 20, 'tags': 'offensive', 'icon': IC + 'targeting_feed.png'}),
 dict(name='Hit and Run', id='tl_hit_and_run', **{'charge up': 0.2, 'active': 4, 'down': 0.6, 'cooldown': 10, 'tags': 'movement', 'icon': IC + 'maneuvering_jets.png'}),
 dict(name='Execution Salvo', id='tl_execution', **{'charge up': 0.3, 'active': 5, 'down': 0.5, 'cooldown': 14, 'tags': 'offensive', 'icon': IC + 'ammo_feeder.png'}),
 dict(name='Claw Strike', id='tl_claw_strike', **{'max uses': 2, 'regen': 0.05, 'charge up': 0.3, 'active': 0.3, 'down': 0.5, 'cooldown': 3, 'tags': 'offensive', 'icon': IC + 'missile_racks.png'}),
 dict(name='Apocalypse', id='tl_apocalypse', **{'max uses': 1, 'charge up': 1.0, 'active': 0.4, 'down': 2.5, 'cooldown': 1, 'tags': 'offensive', 'icon': IC + 'nova_burst.png'}),
 dict(name='Battleship Mode', id='tl_siren_mode', **{'charge up': 3.5, 'down': 3.5, 'cooldown': 10, 'toggle': 'TRUE', 'tags': 'special', 'icon': IC + 'fortress_shield.png'}),
 dict(name='Replica Wing', id='tl_replica_wing', **{'charge up': 0.5, 'active': 0.2, 'down': 0.5, 'cooldown': 45, 'tags': 'offensive', 'icon': IC + 'reserve_deployment.png'}),
 dict(name='Flare Screen', id='tl_flare_screen', **{'max uses': 3, 'regen': 0.05, 'cooldown': 4, 'tags': 'defensive', 'icon': IC + 'flare_launcher.png'}),
]
wcsv('data/shipsystems/ship_systems.csv', SYS_COLS, SYS_ROWS)
SYSDESC = {
 'tl_triple_overcharge': 'Energy weapons fire twice as fast for half the flux and deal 25% more damage.',
 'tl_rail_overdrive': 'Ballistic weapons fire twice as fast for half the flux, slugs fly 50% faster, and the Asura-II surges forward.',
 'tl_ap_focus': 'Energy weapons deal 60% more damage and reach 30% further; +50% damage against capital ships.',
 'tl_pd_overdrive': 'Double damage to fighters and missiles, +50% damage to destroyers (+25% to frigates), +150 PD range; the bubble pods are reloaded.',
 'tl_wing_rally': 'The Selene\'s fighters are patched up (half their hull restored) and surge: faster, harder-hitting and tougher.',
 'tl_hit_and_run': 'A short burst of speed and agility with the guns running hot. Get in, strike, get out.',
 'tl_execution': 'Rapid fire that tears into damaged hulls; the missile racks are reloaded.',
 'tl_claw_strike': 'All eight grapple claws burst out of the side galleries at once and home on the target. Claws ignore shields and tear into the hull (fragmentation). Holds 2 volleys; the galleries rebuild one volley every 20 seconds.',
 'tl_apocalypse': 'Once per battle. The side boosters slide open on their rails and the Abaddon brakes on its retro jets; the Apocalypse warhead drifts out, ignites and flies to the point the ship aimed at. Capital-grade armour and hull, but it can be shot down. Ships in its path are shoved aside. Needs a locked target: the warhead homes on it and detonates when its tip reaches the ship, with a 2200-unit blast whose damage and flux overload build from the rim to the centre. The blast hits friend and foe (not the Abaddon itself).',
 'tl_siren_mode': 'Carrier mode (off): main guns folded under the deck. Battleship mode (on): the deck converts, the three main guns rise and fire; fighters stay out but replacement pauses until the ship returns to carrier mode.',
 'tl_flare_screen': 'Right-click (these hulls carry no shield). Fires decoy flares from eight tubes all round the hull.',
 'tl_replica_wing': 'Every wing launches a full set of replica fighters that fight alongside the originals for 20 seconds (a 2-fighter wing becomes 2 x 2).'
}
for sid, t in SYSDESC.items(): desc_rows.append({'id': sid, 'type': 'SHIP_SYSTEM', 'text1': t, 'text2': '', 'text3': '', 'text4': ''})
wcsv('data/strings/descriptions.csv', ['id', 'type', 'text1', 'text2', 'text3', 'text4'], desc_rows)

# ======================================================================================= scripts (templated constants) + hullmods
JAVA_CONST.update(HH_SWING=SWING['hellhound'], FN_SWING=SWING['fenrir'], GM_SWING=SWING['garm'], SIDE_ENGINE_MIN=30,
                  AP_ARMOR=1750, AP_OVERLOAD_FRAC=0.7, AP_OVERLOAD_MAX=15, AP_HALF=APH / 2 - 10, AP_CLEAR=APH / 2 + 190, FLASH_TIME=0.9, REPLICA_DURATION=20, AP_DRIFT=2.6, AP_FUEL=14.0, AP_RAM=1500, AP_RADIUS=2200, AP_CORE=220, AP_DMG=30000, AP_MINDMG=0)
for root, _, files in os.walk(JAVA):
    for f in files:
        src = open(os.path.join(root, f)).read()
        for k, v in JAVA_CONST.items(): src = src.replace(f'%%{k}%%', v if isinstance(v, str) else str(float(v)))
        assert '%%' not in src, f
        dst = os.path.join(MOD, os.path.relpath(os.path.join(root, f), JAVA))
        os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'w').write(src)
HM_COLS = 'name,id,tier,rarity,tech/manufacturer,tags,uiTags,base value,unlocked,hidden,hiddenEverywhere,cost_frigate,cost_dest,cost_cruiser,cost_capital,script,desc,short,sModDesc,sprite'.split(',')
wcsv('data/hullmods/hull_mods.csv', HM_COLS, [
 {'name': 'Terra Light Frame', 'id': 'tl_hull', 'tier': 3, 'hidden': 'TRUE', 'tech/manufacturer': 'Terra Light', 'tags': 'special',
  'cost_frigate': 0, 'cost_dest': 0, 'cost_cruiser': 0, 'cost_capital': 0, 'script': 'data.hullmods.TL_Hull',
  'desc': 'Terra Light hull fittings: weapons in under-hull mounts sit beneath the armour with only their barrels exposed; vectoring drives swing with the ship\'s manoeuvres.',
  'short': 'Under-hull mounts and vectoring drives.', 'sprite': 'graphics/hullmods/integrated_targeting_unit.png'},
 {'name': 'Convertible Decks', 'id': 'tl_siren_modes', 'tier': 3, 'hidden': 'TRUE', 'tech/manufacturer': 'Terra Light', 'tags': 'special',
  'cost_frigate': 0, 'cost_dest': 0, 'cost_cruiser': 0, 'cost_capital': 0, 'script': 'data.hullmods.TL_SirenModes',
  'desc': 'Starts in carrier mode: the three main guns are folded below the flight deck and cannot fire. Battleship mode (ship system): the deck converts and the guns rise; fighters keep fighting but replacement is paused until the ship returns to carrier mode.',
  'short': 'Switches between carrier and battleship modes.', 'sprite': 'graphics/hullmods/expanded_deck_crew.png'}])

# ======================================================================================= faction hook, settings, mod info
HULLS = [r['id'] for r in ship_rows if 'MODULE' not in r.get('hints', '')]
wjson('data/world/factions/independent.faction', {"knownShips": {"hulls": HULLS}, "priorityShips": {"hulls": []}})
wjson('data/config/settings.json', {"designTypeColors": {"Terra Light": [235, 110, 210, 255]}, "graphics": {"terralight": SPRITES}})
wjson('mod_info.json', {"id": "terralight", "name": "Terra Light", "author": "Skykyrie", "version": VERSION,
      "description": "Union warships of the Terra Light war, redrawn top-down in the Starsector style from the SNES game Earth Light (Hudson Soft, 1992). 15 ships: 5 capitals, 7 cruisers, 3 destroyers.",
      "gameVersion": GAMEVER})
open(f'{MOD}/README.txt', 'w').write(open(_ROOT + '/readme_mod.txt').read().replace('{VERSION}', VERSION).replace('{GAMEVER}', GAMEVER))

for r in report: print(r)
print('variants', len(variants_out), 'builtin weapons', sorted(BUILTIN_WEAPONS), 'java consts', JAVA_CONST)
for r in LOADOUT_REPORT: print('LO', r[0], 'op', r[1], 'weap', r[2], 'wings', r[3], 'left', r[8])
