# Terra Light - locked ship designs
## Tiamat (capital) - LOCKED
- boombox oval cylinder; white bow cap; green ring + 2... (see tiamat2.py) 3 thrusters aft behind centred pink command bubble
- 4x built-in Triple Beam Cannon (Large Energy) HIDDEN wall mounts, 160 arcs (front 0-160, rear 20-180)
- 8x Small Energy PD: 4 wall (car-tyre), 4 deck rails
## Asura-II (capital) - LOCKED
- orange boat hull, 2x built-in Quad Railgun (Large Ballistic, same stats): top TURRET + HIDDEN exactly below, both 300 arc
- 8x Small Missile (torpedo / anti-fighter = its PD): 3 per gunwale + 2 flanking centred green bridge on stern deck
- 2 big stern thrusters. Faster than typical capital (cruiser speed)
## Nodens (capital) - LOCKED
- blue zeppelin; 3 orange nose domes = Armageddon torpedo outlets (built-in Large Missile HIDDEN, 30 arc, angles 15/0/-15)
- built-in Armageddon: limited ammo that RELOADS over time (long cooldown), sit-back artillery playstyle
- twin command gondolas under hull: fully hidden (not drawn)
- ship system: flarelauncher (flares from nose outlets / SYSTEM slots); tankiest ship (very high armor/hull)
- 2 tail thrusters
## General
- PD counts: capitals ~6-8, cruisers 3-4, destroyers 2-3, frigates 1-2
- Crab = transport fighter, not a ship (excluded)
- wall/under-hull weapons -> HIDDEN built-ins; "car tyre" peeking for wall mounts
## Roster / classes (user-confirmed)
- CAPITAL: Tiamat, Asura-II, Neow (renamed from Nodens), Artemis (carrier), Siren (battleship/carrier convertible)
- CRUISER: Hastur (battle-cruiser/carrier, sprite ~80% scale), Hannibal, Regulus, Corvus (NEEDS NEW NAME - clashes w/ vanilla Corvus system), Abaddon (missile ship, 1-use built-in Apocalypse missile), Iris (carrier), Selene (fast carrier)
- DESTROYER: Fenrir, Hellhound (DDG-MN6; English patch said Cerberus), Garm (renamed from Grant/Gulon)
## Hastur (cruiser) - LOCKED (v7)
- ball + fat baguette (same width as ball, ~2x ball diameter long) on its forehead
- 4 Medium Energy turrets (2 each side of baguette), 3 built-in Medium Ballistic PD railguns HIDDEN under baguette
- 1 fighter bay (hangar, ball front under baguette), 2 Small Ballistic turrets on ball sides at the ball/baguette joint (visible, swappable)
- blue command screen band on ball behind baguette; 2 thrusters on ball only
## Artemis (capital carrier) - LOCKED (v4)
- twin green flight decks (catamaran), catapult rail + pink shuttle in the gap, 8 Small Energy PD on outer rails
- 8 fighter bays (4 per deck); command centre = pink stick in stern joint, screen at the forward tip
- ship system: custom, greatly reduces fighter replacement time (needs stats script); 4 engines
## Corvus -> renamed DUILIUS (cruiser, 8 hidden claw hatches, 4 per side)
## Siren (capital, convertible) - LOCKED (v2)
- wide 4:3 orange deck hull, command pod behind stern on visible connector, 2 engines
- 8 Small Ballistic PD, 3 Large Energy main guns (2 fore, 1 aft) only active in Battleship mode
- ship system toggle Carrier<->Battleship: carrier = 4 built-in Athena (CHU-03 robot) wings out, guns folded/disabled;
  battleship = fighters recalled & held, guns up. add 2-3s transition, 10-15s cooldown, AI switch logic, reduced OP
- Athena wing lives in Terra Light; NO dependency on Arma Armatura (just avoid ID clashes)
## Hannibal (cruiser) - LOCKED-ish (v2)
- violet bulb body + LONG forward snout; 3 identical BUILT-IN Medium Energy AP beams, all HIDDEN, angle 0 arc 30: 2 side by side at snout front + 1 at snout tip
- 6 Small Ballistic PD on body walls (3 per side); command head (pink, cyan visor) near thrusters; 2 pink ring engines
- orange peg under body = landing leg (not drawn)
- Hannibal, Regulus, Duilius: same sprite length (~412 px pre-scale)
- Hannibal/Regulus/Duilius: ONE big central thruster each
## Regulus (cruiser) - v2
- pink Hannibal-like body; 4 BUILT-IN green bubble-missile pods (Medium Missile, HIDDEN, short range; anti close-in cruiser/destroyer):
  2 at snout tip (fwd, arc 120) + 2 at rear body (sides, arc 180); 18 Small Energy PD: 12 on snout walls (6/side) + 6 on body walls (3/side)
  bubble missile: missile weapon, ENERGY damage type, small but strong blast (small AoE radius), short range
## Duilius (cruiser, ex-Corvus) - v2
- yellow cylinder, blue side panels with 4 claw hatches per side (8), ribbed rear + 1 big thruster, pink command dome at rear
- SHIP SYSTEM: launches all 8 claws at the nearest ship at once; claws = ballistic weapon, FRAGMENTATION damage (SYSTEM/hidden slots at hatches)
- ONE swappable Large Ballistic HARDPOINT at the bow edge (weapon sprite = barrels sticking out, changes with weapon), arc 10
- 6 Small Ballistic PD on top (3/side)
## Abaddon (cruiser, missile ship) - LOCKED (v6)
- Abaddon hull = ONLY yellow parts: angular armoured front frame (2 Medium Energy on hex pads + swept-canopy cockpit),
  each hand ends in a yellow box thruster w/ green vents (its 2 engines). No green body.
- APOCALYPSE WARHEAD TORPEDO: built-in MODULE (STATION_MODULE slot), cruiser-sized red torpedo (~112 px wide, ~530 long incl. bell), fins, gigantic GREEN thruster bell
- v6 layout: long side bodies (y150-420), front frame deepened and centred on them -> H-shape after launch
- ability: once per battle, launches it. Torpedo flies to the point the ship aims at and only explodes there;
  ships it touches on the way are shoved aside and take ramming damage
- 4 Small Ballistic PD on the box thrusters (proposed, unconfirmed)
## Iris (cruiser carrier) - v7
- green flat flight deck, chamfered bow, stern block tapering to command-room width, green command tower at rear, 2 small engines
- 4 swappable Medium Missile on plain round mount pads sized for vanilla 40px racks (pink trim ring):
  2 stacked on the centreline in front of the command room + 1 on each green extension block (angle +-20, arc 180)
- 8 Small Ballistic PD (4 per side along deck edges); 4 fighter bays
## Revisions (2026-09-25)
- NEW MECHANIC "under-hull slots": normal swappable TURRET slots (refittable in the refit screen) whose weapon sprites are hidden in combat
  by a built-in hullmod script (every frame: weapon sprite/barrel/under/glow alpha = 0 for listed slot IDs). Marked hide=True in slot json.
- Hannibal: 3 Medium Energy now SWAPPABLE, all TURRET arc 30 fwd; 2 side-by-side visible on orange rings, middle one under the snout tip = hidden-sprite
- Hastur: 3 Medium Ballistic under the baguette = swappable hidden-sprite slots (arc 300)
- Duilius: bow gun -> TWO Large Ballistic swappable hidden-sprite slots under the bow tip (arc 30); generic twin muzzles painted peeking past the bow
- Regulus: front bubble-missile pods = 4 warheads each (one column on the exposed outer half), pods tucked so their inner half sits under the snout tip;
  body PD reduced to 2 per side -> 12 snout + 4 body = 16 Small Energy PD
- Asura: painted pink missile boxes replaced by plain round mounts sized for vanilla small racks
- Iris: plain round medium missile mounts (see Iris v7)
- General rule: swappable slots get plain mount rings, not painted launchers (weapon sprite draws on top)
## Revisions 2 (2026-09-25)
- Regulus PD: snout 2 per side (4) + body 3 per side (6) = 10 Small Energy
- Hannibal: middle slot sits directly between/under the two side slots (y=78) under the snout, nothing drawn at the tip
- Built-ins drawn: Tiamat triple-barrel emitters poke out of the wall rings; Asura top Quad Railgun turret sprite (pink dome + 4 barrels);
  Neow outlets show Armageddon warhead noses; Regulus pods & Abaddon Apocalypse already drawn; others are hidden/under-hull
## Revisions 3 (2026-09-25) - slot sizes + under-hull rendering
- Hannibal: 3 Medium Energy (2 visible side-by-side + 1 under the snout tip edge, y=40)
- Duilius: 2 Medium Ballistic under the bow edge (x=+-26, y=58), arc 30; painted muzzles removed
- Hastur: 3 Medium Ballistic moved to the baguette's front edge (CX-44,42),(CX,28),(CX+44,42)
- UNDER-HULL SLOTS are rendered BELOW the ship (script: hide weapon sprites, redraw them on a below-ships render layer
  at the weapon's position/facing) so only the barrels peek past the hull edge. Still normal refittable TURRET slots.
## Selene (cruiser, fast carrier) - LOCKED (v3)
- purple dome body, decorative flat pink HALF-OVAL cap on the front of the dome (no command room), 2 short green launch decks from purple side pods
- 2 fighter bays (one per deck); 2 MEDIUM COMPOSITE slots on orange sponsons (pods' outer sides); big 3-nozzle engine crest
- speed: second fastest in the mod (after Fenrir). PD: 2 Small Ballistic on the engine crest (confirmed). Weakest ship of the original game - keep it fragile
## Fenrir (destroyer, fastest ship) - v2
- pink core, 4 spherical pods: 3 in a forward-pointing triangle (tip + pair) + 1 in the middle; each = MEDIUM BALLISTIC turret (swappable), all forward, arc 60
- 8-barrel rotary look = portrait flavour; thrusters: 1 big main + 1 side thruster pod each side (3 total), orange ribbed collar
## Revisions 4 - heavier cruiser guns (so cruisers out-gun the 4-medium Fenrir)
- Hannibal: 2 Medium Energy (visible, top) + 1 LARGE Energy under the snout tip (y=52, drawn below hull), all fwd 30 deg
- Duilius: 2 LARGE Ballistic under the bow edge (x=+-30, y=66, drawn below hull), fwd 20 deg; balance via narrow arc + OP budget
- Fenrir: keep 4 Medium Ballistic, OP ~85-90, low armour/weak shield, fastest ship
## Hellhound (destroyer, light) - LOCKED (v2)
- FLASHLIGHT shape: long cylindrical handle forward, flared "lamp head" at the stern = grey rim + one big thruster lens
- blue band across the middle of the neck: 3 Small Ballistic in a horizontal row (arc 150 fwd)
  + 3 more Small Ballistic exactly beneath them (under-hull hidden-sprite slots, refittable)
- short stick at the front tip with 1 Small Missile pod each side (arc 120)
## Garm (assault destroyer, ex-Grant/Gulon) - v2
- big yellow front dome + orange rear box (green side panels), green command bump, grey ribbed main thruster
  + 1 side thruster pod each side (like Fenrir) = 3 thrusters
- 1 LARGE Ballistic under the nose (swappable, drawn below hull, fixed fwd arc 10) = the quad railgun
- 3 Small Ballistic turrets lined up front-to-back on the centreline of the dome (arc 120 fwd)
## Art styles (2026-09-25)
- KEEP the Earth Light (EL) sprites. Add a Starsector-style (SS) redesign per ship with IDENTICAL canvas size + slot positions,
  so both share one .ship file. Player option to pick EL or SS look (setting read at game load that swaps sprite paths).
- SS language: faceted chamfered armour hulls, flat spine strip + angled side plates, BSP plating/seams/vents/rivets,
  gunmetal (~118,116,108) with the ship's EL colour as muted accent stripes/trim, octagonal turret wells, angular sponsons,
  low specular. Helpers: shiplib.plate_detail / armour_edge; scripts ss_<ship>.py -> ss_style/<ship>_ss.png
- SS test done: Hannibal (long armoured prow + faceted rear section + superstructure/bridge), Hastur (arched long forward hull + squat core)
- SS v2 rule: DIRECT shapes, few corners - straight sides + one angled nose/tail cut, hexagon bodies, rect sponsons, circular turret wells
- SS paint job (approved): accent-painted panels, pinstripe inset from edge, hazard stripes at deck edges/engine blocks/mount lips, stencilled hull codes, grime streaks running aft. Tiamat SS v1 done.
- Tiamat UPDATE: Triple Beam Cannon = built-in TURRET (not hidden) with its own sprite (weapons/tl_triplebeam_turret_*.png):
  pink domed emitter hub + 3 bundled barrels w/ blue focusing rings, from the portrait; sits in a big blue ring mount on an
  armoured wall sponson; angle +-90, ARC 180. (EL version to be updated the same way)
- Tiamat v4 (wall-mount look): ring seen EDGE-ON as a blue lip on a thickened wall section; the Triple Beam Cannon pivots just
  outside the lip (x = wall +-6) and is rendered BELOW the hull (same under-hull render helper), so the wall hides the
  inboard half of the hub and only the outer half-dome + barrels show. Swings fore/aft through 180.
- Tiamat beam arcs = option B (confirmed): front pair -5..168 (173 deg), rear pair 12..180 (168 deg), mirrored; wall PD 150; deck PD 360
- Asura SS v1: pointed wedge prow (orange cap), straight sides, raised keel strip, stern deck w/ centred bridge (green window), orange barbette ring for the Quad Railgun (built-in turret sprite weapons/tl_quadrail_turret_*.png, twin hidden below), round missile wells

## Asura-II widened (locked)
- Compared with vanilla capitals (Paragon 0.89, Onslaught 0.83, Conquest 0.47, Odyssey 0.40 width/length): old Asura 0.32 was the thinnest.
- Widened to a Conquest-like shape: canvas 290x440, CX 145, hull ~200 wide (ratio ~0.5). Applies to BOTH styles (shared slots).
- Slot re-spacing: |dx|<40 unchanged, otherwise pushed out by 34 px. Gunwale missile wells at x 62/228, deck pods at 108/182, quad railgun (turret + hidden twin) at (145,100), engines at CX+-40.
- Narrow v4 kept: asura_narrow_v4.py, asura_union_narrow.png, asura_slots_narrow.json; SS v1 kept in ss_asura_v1.py.
- SS style now adds a dense small-detail layer (shiplib.greebles: machinery boxes, capped ports, vent banks, pipe runs with clamps), kept clear of mounts, paint bands and hull edges, applied before the paint job.
- Asura SS v2 paint: orange gunwale armour belts, orange prow cap, prow flank chevrons, keel chevrons, stern-deck corner panels, accent panels, pinstripe, hazard bands (keel, stern deck, engine block), hull codes, grime.

## Capital size target (user rule)
- Earth Light capitals should be Onslaught-Conquest sized: hull area ~54k-63k px (Onslaught 274x329, Conquest 188x397).
- Current: Tiamat 62k (in range), Asura 66k EL / 69k SS (slightly big), Neow 54k (in range, thin 0.36), Artemis 91k (144%), Siren 76k (121%). Waiting on the user's revision list.

## SS detail density v2 (applies to all Starsector-style hulls)
- armour_blocks (big raised sections split by dark trenches), greebles + fine_greebles, cross frames on keels and rails,
  window_row crew windows, nav_lights (red port / green starboard / white centre), rcs thruster blocks, antenna masts,
  render(ao=2.2) ambient occlusion. Paint job still applied on top.
- Done: Asura SS v3, Tiamat SS v5 (v4 kept in ss_tiamat_v4.py). Hastur/Hannibal still on the old density.

## Size decisions (2026-09-25)
- Artemis (91k) and Siren (76k) keep their size: justified by their many fighter bays.
- Neow must be the biggest/tankiest: ~1.2x Paragon (taken as 1.2x width and length = ~106k area, above Artemis).
  Options rendered by neow_big.py: A = same zeppelin scaled evenly (220x605), B = same length, fatter (300x444).
  Locked v3 kept in nodens.py / nodens_v3.py until the user picks.
- Neow option C (proposed): envelope 1.2x longer (494), half-width 128, fittings x1.25 -> hull 256x520, ratio 0.49, area ~105k (143% Paragon).
  Files: nodens_C_union.png, nodens_C_slots.json (`python3 neow_big.py C 128`).
- Neow option C v2: the 3 Armageddon outlets are lined up in a column on the centreline, each ~0.4x hull width
  (radius 51 -> 102 px across) at y 85/195/305; slots LARGE MISSILE HIDDEN, all angle 0, arc 30. `python3 neow_big.py C 128 51`
- Neow option C v3: outlets are now 3 forward-pointing orange launch tubes (64 px wide = 0.25x hull width, 67 long),
  stacked in steps right behind the nose tip (front tube pokes past the tip; each rear tube sits higher so it can fire over).
  Slots at each muzzle (CX, 33/84/135), LARGE MISSILE HIDDEN, angle 0, arc 30. `python3 neow_big.py C 128 32 pipes`
- Neow option C v4: tubes cleaned up - 12 px gap between tubes, clear hull space ahead of the front tube, each tube in a
  recessed blue cradle, only a slight height step. Muzzle slots at (148, 70/149/228).
## Neow - LOCKED size + tubes (option C v4)
- Hull 256x520 (~105k area, 1.44x Paragon), 3 orange launch tubes in a spaced column behind the nose.
- tl_armageddon = ONE built-in LARGE MISSILE weapon on a HIDDEN slot at the middle muzzle (148,149), angle 0, arc 30.
  .wpn: turretOffsets/hardpointOffsets [79.2,0, 0,0, -79.2,0] (front, middle, back), barrelMode ALTERNATING,
  burstSize 3, burstDelay ~0.4 -> fires front tube, then middle, then back.
  weapon_data.csv: max ammo 3, ammo/sec 0.05, reload size 3 -> all 3 torpedoes come back together every 60 s.
- Torpedo projectile sprite weapons/tl_armageddon_torpedo.png 64x132 (46 px body = fills the tube mouth). Needs a big
  collision radius and high missile HP so PD can't swat it instantly (balance later).
- Name check: no vanilla Starsector weapon called Armageddon; the ids stay prefixed tl_ to avoid clashes with other mods.
- EL Neow promoted: nodens_union.png / nodens_slots.json are now option C v4 (old v3 kept as *_v3).
## Neow - Starsector style v1 (ss_neow.py)
- Long octagon envelope (flat nose, straight flanks, tapered tail) + 2 straight-edged tail fins; hull ~111k area.
- Recessed tube bay with the 3 round orange launch tubes (steel bands, loaded warhead in each mouth), hazard strip ahead.
- Gore bands (EL seams) as raised strips with frames + crew windows, 2 ring frames, spine, observation block with windows.
- Paint: blue accent panels, pinstripe, nose cap, gore stripes, flank chevrons, fin tips, hazard bands, hull codes, grime.

## Vanilla-like detailing (friends' feedback: "blocky, stickers on the hull") - vstyle.py
- Studied Paragon/Onslaught/Eagle: painted armour PLATES over dark exposed MACHINERY; each plate bevelled, faceted
  (tilt/ridge), outlined, rim-lit, darker toward edges, casting a shadow; recessed ring turret wells; metal engine cans;
  small hardware on plates follows symmetry (ports, vent slots, sub-panels, bolts); crisp 1x output (sharpened).
- vstyle.Ship: guts(), plate(tilt, ridge, inset, dome, paint, lines), mount(), nozzle(), plate_details(), engrave(),
  stencil(), hazard(), lights(), windows(), render().
- Tiamat SS v6 (vs_tiamat.py -> ss_style/tiamat_ss_v6.png): same box silhouette + slots; old v5 kept (ss_tiamat.py).
## Tiamat v7 - casemate beam mounts (user's wall-mount drawing guide)
- Stationary part in the HULL: casemate sponson (15 px proud of the wall, ~88 px tall) with an open, recessed well:
  dark #1e2124 fill, 1 px hydraulic lines, pure-black AO line at the hull join, metal tracking-groove ring
  (bright top / dark bottom) + Tiamat's blue ring, pivot socket; hazard jaw tips; glowing blue energy conduit to the core.
- Rotating part = weapon sprite weapons/tl_triplebeam_turret_ss_v2.png: 96x96, pivot dead centre (48,48), ball casing
  r16 with #e2e8f0 top rim / #1a1a1a bottom rim, blue emitter ring, shroud, 3 barrels with pink emitter tips, rear coupling.
  Normal turret rendering now (no under-hull trick needed - the back of the ball swings into the dark well).
- Pivots unchanged (CX+-96, y 120/262). Arcs still option B (~168-173 deg); the guide mentions 135 deg - pending user choice.
- Files: vs_tiamat.py -> ss_style/tiamat_ss_v7.png (v6 kept: vs_tiamat_v6.py, tiamat_ss_v6a.png), tl_triplebeam_ss.py.
## Tiamat v8 - SIDE-WALL beam mounts + purposeful detailing (vs_tiamat8.py, tiamat8_sheet.py)
- User: guns must sit ON THE SIDE WALL, not on top of the hull. Gun sprite (tl_triplebeam_turret_ss_v2, 96x96 centred pivot)
  is drawn BELOW the hull (render plugin: hide weapon sprite, redraw on BELOW_SHIPS layer); hull shows the wall frame
  edge-on: dark recess + black AO line, blue ring lip ends above/below the ball, and a top YOKE ARM with pivot pin
  (hull layer, so it covers the gun root = gun visibly hangs on the wall). PD wall mounts use the same (small yoke).
- User: every detail must have a purpose. v8 parts: frontal armour, sensor dome, comms/ECM prongs, RCS quads,
  supply hatches, beam capacitor banks (4 capacitors, blue terminals) + beam heat radiators next to each mount,
  crew habitat (cabin windows), airlocks, lifeboats, PD capacitor boxes, spine = main power trunk (glow seam +
  inspection hatches), PD gun rails with PD radiators, reactor (feeds the beams), power/coolant trunk lines,
  propellant tanks, engineering/life-support decks, bridge + fire-control sensor + comm mast, engine radiators,
  3 main + 4 manoeuvring engines, nav lights. Systems map: Tiamat_v8_systems_map.png.
## Tiamat v9 - "race car" layout (vs_tiamat9.py, tiamat9_sheet.py) - user: v8 too blocky
- Top view like a NASCAR car: smooth spline body, flared fenders, pinched waist; the 4 Triple Beams sit in the 4
  "wheel wells" like big tyres (pivots unchanged CX+-96, y 120/262). Well socket (liked from v7): dark floor, hydraulic
  lines, black AO arch edge, tracking groove + blue ring; bolted fender flare arch with blue edge.
- Gun v3 (tl_triplebeam_ss3.py -> weapons/tl_triplebeam_turret_ss_v3.png, 96x96 centred pivot): tyre-like drum with
  treaded cooling rim, 3 barrels STACKED VERTICALLY shown as a stepped telescope (bottom widest/longest, top
  narrowest/shortest) -> 3 pink emitter tips visible; stack clamps. Renders normally (above hull) in its well.
- Detailing = connections + armour: reactor -> 4 blue power cables (clamped) -> beam capacitor -> socket into each well;
  coolant pipes into the wells; yellow PD feed cables + sockets; data line bridge -> sensor dome; flanged fuel lines
  tanks -> engines; armour = 3-section bolted hood + nose cap, bolted quarter panels, overlapping bolted waist strakes,
  bolted fender arches.
## Tiamat v10 - v7 body + user's sketch (vs_tiamat10.py, tiamat10_sheet.py)
- User sketch: main box hull, narrower centre block running past it at bow and stern, 4 rectangular "tyre" pods
  bolted to the side walls (front pair / rear pair with a gap). Shape back to v7 (v9 race-car outline rejected).
- Canvas widened to 284x400 (CX 142) so the pods fit; old slot x + 12. Pods: 40x112, rounded, pivot at CX+-109, y 120/262
  (NEW pivot x - pod centre). Pod = strut-bolted to wall, tread (cooling fins) on the outer face, bolted end caps with
  hazard strips, v7 well socket (dark floor, hydraulic lines, AO, tracking groove + blue ring), power + coolant cable
  sockets on the inner face. Gun v3 sits in the socket. Wall PD bulges in the gap between pods (x CX+-93, y 178/206).
- Deck: v7 layout (chevron spine power bus, PD rails, capacitor banks + radiators facing each pod, habitat + airlock,
  reactor, aft deck with tanks, bridge) + v9 connections (power cables, PD feeds, data line, flanged fuel lines) + bolts.
- Slots: ss_style/tiamat_ss_v10_slots.json. Forum mod threads (topics 35818, 34917, 30580) blocked (HTTP 402);
  14935 = Tahlan Shipworks (text only, no sprites visible).
## Tiamat v11 (vs_tiamat11.py) - user: keep v7 SIZE, just add the tyre spaces, not chunky
- Back to v7 canvas 260x400 and v7 outline; bbox 221x383 (v7 was 217x377). No centre-block extensions.
- Tyre spaces: 23x104 notches cut into each side wall (front y 68-172, rear 210-314); slim tyre pods 36x96 sit in them,
  18 px proud of the wall. Pod: tread fins outer face, bolted end caps + hazard, v7 well socket r16.5 (tracking ring
  14-16, blue ring 13-13.8). Pivot CX+-92, y 120/262. Wall PD bulges in the gap (y 178/206).
- Gun v4 (tl_triplebeam_ss4.py -> weapons/tl_triplebeam_turret_ss_v4.png): drum r14 (was 17), same stacked barrels.
- Slots: ss_style/tiamat_ss_v11_slots.json.
## Detailing study - Tahlan Shipworks, Diable Avionics, xxarra (user-uploaded ship folders; Detailing_study_3_mods.png)
- Tahlan: chamfered/stepped plate notches, inner contour line on every plate, glowing recessed bays (light strips),
  bold livery stripes over grey + white core block, many detailed round wells, engine-can clusters at the stern.
- DA: big calm flat painted panels, dark conduit channels between panels like circuit traces with small cyan lights
  (visible cable routing), livery stripes that cross seams, teal glass panels with light rows.
- xxarra: radiator slat banks sticking out of the silhouette, painted armour over dense machinery, thick 2-tone bevels,
  layered overlapping plates with step shadows, ragged engine-cluster sterns.
- To apply: notched plates + inner contour; recessed lit conduit channels carrying cables; one livery across the hull;
  calm panels vs dense zones; function shapes the outline; glowing bays / window rows.
## Terra Light detailing language (TL signature, v12 - vs_tiamat12.py) - apply to every SS ship
- Notched plates: every armour plate gets a stepped double notch on its corners (vstyle plate(notch=3)).
- Double contour: dark engraved line + light line just inside every plate edge (inset).
- Lit conduit channels: recessed dark trenches carrying the cables, running lights along both walls (ship accent colour
  for power, amber for data/PD), grey NODE RINGS with a light at every bend (TL-only - DA uses plain traces).
- One livery across the hull (stripes cross seams): Tiamat = blue "horizon band" with white pinstripes across the waist,
  blue + white slashes on each tyre pod, blue centre stripe on the bow.
- TL emblem ("Earth Light"): planet disc with a rising sun on its horizon, on the bow (both sides).
- Kept: tyre pods / well sockets, stacked-barrel gun v4, v7 size.  Out: Tiamat_v12_TL_detailing.png, Tiamat_v12_systems_map.png
## Tiamat v13 - side-wall gun bays from the user's reference render (vs_tiamat13.py, tiamat13_sheet.py)
- Tyre pods -> armoured GUN BAYS in the side walls (same footprint): notched frame bolted into the wall, deep dark recess
  (hydraulic lines, AO edge, top-left frame shadow), feed pipes down the inner wall, slide rails top/bottom, brackets,
  pivot socket, CAUTION/HOT EXHAUST hazard + stencil plates on the frame ends, power + coolant sockets.
- Gun v5 (tl_triplebeam_ss5.py -> weapons/tl_triplebeam_turret_ss_v5.png, 96x96 centred pivot = middle of the drum):
  long breech drum along the barrel axis, dark feed hoses + copper coolant lines wrapped over it, manifold blocks on the
  flanks, rear actuator cap, front collar, 3 stacked stepped barrels with pink tips. Guns forward = breech lies in the bay.
- Limit: Starsector draws everything from straight above and only rotates sprites flat, so the reference's side view
  is translated into its top-down equivalent (a perspective-drawn gun would look wrong once it rotates).
## Tiamat v14 - SIDE TURRETS (vs_tiamat14.py, tl_triplebeam_ss6.py, tiamat14_sheet.py)
- User: gun goes on the SIDE of the drum, not inside the bay; the drum is where the gunner sits.
- Gun v6: drum = gunner cabin (teal canopy/viewport on the front-outboard quarter with frame bars + console light,
  roof hatch, grab rails, blue feed ring, nav lights); triple barrel pack (breech block + 3 stacked stepped barrels,
  clamps) hangs on the drum's OUTBOARD side on a trunnion arm, hoses from cabin to breech. Pivot = drum centre.
  Two sprites: weapons/tl_triplebeam_turret_ss_v6_L.png (port, pack on the left) and _R (starboard).
  -> needs 2 built-in weapon ids (tl_triplebeam_l / tl_triplebeam_r); fire offset ~20 px to the pack side.
- Hull: bay shortened to the cabin (recess y+-24) with life-support vents above/below; barrel pack sits just outside
  the bay frame when forward.
## Tiamat v15 - LOCK CANDIDATE (vs_tiamat15.py, tl_triplebeam_ss7.py)
- v7 model: casemate sponsons ("tyres", 32x88, 18 px proud of the wall) with the v7 well, on v12 TL detailing.
- Built-in Triple Beam = gun sprite only (barrel pack, no cockpit): weapons/tl_triplebeam_turret_ss_v7.png 96x96 centred
  pivot. Pivot on the OUTER FACE of each sponson (CX+-108, y 120/262).
- STATIC base in the hull: trunnion arm from the well's back wall to the sponson face + mount collar (tracking ring,
  blue ring, bearing). MOVING part = barrels only.
- Arcs 135 deg: front 0..135 (angle +-67.5), rear 45..180 (angle +-112.5); + = left side.
- Small energy PD: 4 per side on the centre-hull gun rails (CX+-34, y 104/140/176/212), 360 deg; wall PD between the
  beams REMOVED. Slots in ss_style/tiamat_ss_v15_slots.json.
## Tiamat v16 (vs_tiamat16.py) - gun wells filled with working machinery
- Each casemate well now holds: back-wall cable bundle (power/coolant/data, clamped) into the trunnion arm; traverse
  servo (motor can + gearbox) with a brass pinion meshing the collar ring = what turns the barrels; 2 beam capacitor
  cells with blue terminals; coolant pump (impeller) piped to the collar; ready/charging/fault status lights.
## Tiamat v17 (vs_tiamat17.py) - capital-size command superstructure (old bridge 58x66 -> 88x72, 3 tiers)
- Tier 1 crew/operations block (dx<=44, y 266-338): crew-deck window rows down both flanks, side access airlocks,
  blue aft band, TL emblem. Tier 2 bridge: forward-pointing prow with a wraparound window band (mullions, glint,
  amber/blue consoles behind the glass). Tier 3 CIC / flag bridge with a window slit, crowned by the main fire-control
  dome; 2 comm masts behind, station-keeping thrusters on the flanks. Data line now starts at the bridge front.
## Tiamat v18 (vs_tiamat18.py) + combat mock-up (sim_tiamat.py)
- Command superstructure made taller toward the ship's centre: tier 1 y 204-338, bridge glazing now at y ~212,
  CIC/flag bridge y 236-322 with flag-deck windows, fire-control dome at (CX,306).
- Engine-like DRIVE CORE (vstyle.drive_core) at the ship's centre (CX,170, r22): bolted rim, swept turbine blades,
  stator ring, 4 struts, glowing hub. Spine shortened to one chevron (84-142); side rails became core coolant radiator
  spines (y 84-198). Power cables now run core -> capacitors -> casemates.
- Small energy PD: 4 per side near the side edges, inboard of the casemates (CX+-66, y 88/152/230/292), on armoured
  bulges, angle +-90, arc 210 (placeholder). Tanks moved to y 302-332; habitat shortened to y 162-220.
- Sim (visual approximation, not the game engine): engine flames w/ throttle flicker, RCS jets while turning, placeholder
  FRONT 270 deg shield with impact ripples, arc overlay, Triple Beams tracking/firing within arcs, PD sweeps.
  Out: Tiamat_v18_combat_sim.mp4 / .gif, Tiamat_v18_layout.png.
## Tiamat v19 (vs_tiamat19.py, tl_triplebeam_ss8.py, sim_tiamat19.py)
- LATERAL THRUSTERS for strafing: 3 per side on the wall (y 68 / 191 / 322), each a bolted housing with 2 outward nozzle
  bells + fuel feed. Engine slots (for the .ship): (CX-+96, y) angle +-90 (outward). Old bow RCS removed.
- Built-in Triple Beam v8 (weapons/tl_triplebeam_turret_ss_v8.png): heavier - breech block 24 wide with heat-sink fins,
  charge coils, copper lines, hub r5, barrel collar; stacked barrels 11 / 8.2 / 5.6 wide (was 7.2 / 5.4 / 3.8).
- Sim v19: full burn -> turning (lateral pairs bow/stern opposite) -> strafe right (left thrusters) -> strafe left ->
  shield -> arcs -> firing. Out: Tiamat_v19_combat_sim.mp4 / .gif.
- Vanilla engines (wiki): engineSlots have location, length, width, angle, contrailSize, style (engine_styles.json);
  flames are drawn by the game (not in the hull sprite); plume length/width also affect engine HP; contrailSize 128
  marks an engine as a Maneuvering Jets engine.
## Tiamat v20 (vs_tiamat20.py, tl_triplebeam_ss9.py, sim_tiamat20.py)
- Triple Beam v9: 128x128 canvas, pivot (64,64); stacked barrels 16 / 12 / 8 wide, tips 62 / 52 / 42 px ahead of the pivot
  (-> .wpn turretOffsets 62,0 52,0 42,0), breech 32 wide with fins, charge coils, hub r6.5.
- Firing: BEAM-BOLT projectiles (energy PROJECTILE with a long thin beam-like sprite): each shot = burst of 2 from each
  of the 3 barrels = 6 bolts (barrelMode LINKED, burstSize 2). Sim: shot every 0.9 s, bolt speed 900, 34 px bolt.
- Side thrusters v2 (studied Eagle / Conquest outboard engines): bolted pylon, pod body with ring bands, 2 flared bells
  pointing out (ring seams, dark lip, ember glow), cooling vanes, flanged fuel line + socket, hazard exhaust mark on the
  wall. Positions y 62 / 191 / 322; engine slots at (CX-+109.5, y) angle +-90.
## Tiamat v21 (vs_tiamat21.py, tl_triplebeam_ss10.py, sim_tiamat21.py)
- Triple Beam v10: shorter + bulkier barrels 21 / 16 / 11 wide, tips 54 / 46 / 38 px ahead of pivot (.wpn offsets);
  breech 36 wide, one wide clamp.
- Hull clean-up: plate texture halved + no grime, darker/coarser machinery (reads as shadow), bolts only on big plates
  and ~2.4x wider spaced + softer, tiny hazard chips removed, fewer clamps (none on thin cables), window rows halved,
  flag-deck dot grid -> 2 clean window bands, data channel lights sparser + no node rings.
## Asura-II Starsector style v3 (vs_asura3.py, tl_quadrail_ss2.py) - Tiamat-v21 method
- Same canvas/slots as widened EL (290x440). Wedge prow = 2 cheek plates + ridge plate + orange cap, bow sensor dome, ECM
  prongs, TL emblem. Quad Railgun barbette r32 (traverse ring, orange ring, dark well) + magazines w/ ammo feed chutes +
  5-cell capacitor banks per side; orange-glow drive core (CX,212) with a power spine to the barbette.
- 6 gunwale missile sponsons with inboard reload racks (4 rounds each, red warhead tips), orange stripe on the wall belts,
  crew decks + airlocks + life-support vents, aft engineering blocks w/ propellant tanks + radiators, aft wall armour.
- Command block tall toward the centre; bridge glazing = GREEN command room (EL identity), CIC w/ green bands + dome, masts;
  deck missile pods flank it; aft access hatch. 2 main drives (40 wide) + 2 manoeuvring; 3 lateral thrusters per side
  (y 195/255/330). Livery: orange waist band + white pinstripes.
- Quad Railgun v2: 128x128 centred pivot, armoured house w/ glacis, flank capacitor packs, cupola, 4 rails in 2 pairs with
  coil bands + pink muzzle rings (EL), orange coil jackets, ammo chute + power pigtail. Muzzles 58 px ahead of the pivot.
## Asura-II Starsector style v4 (vs_asura4.py, tl_quadrail_ss3.py)
- User: less blocky / more spaceship contour; hated the pod-style side thrusters; longer + bigger railgun barrels;
  wider main-drive gap.
- Spline hull: ogive prow, flared shoulders, slight waist, rounded stern; contour armour skin band (15 px) following the
  hull line with orange edge stripe; lower deck armour under everything (machinery only in trenches); rounded modules,
  teardrop missile blisters, rounded command block; engine nacelle cowls.
- Side thrusters v3 = FLUSH fairings in the hull wall with 3 recessed nozzle slots (ember at the mouth), no pods.
- Main drives moved to CX+-56 (ENG in asura_slots.json, EL asura.py updated too - shared .ship engine slots).
- Quad Railgun v3: 168x168 canvas, centred pivot, rails 9.2 wide (was 6.6), muzzles 78 px ahead (was 58), 2 pair clamps.
- Asura sim (sim_asura.py -> AsuraII_v4_combat_sim.mp4/.gif): full burn, turn right, strafe L/R with flush thrusters
  (3 slot flames each), placeholder front shield, arcs (railgun 300 pink, missiles 180 green), Quad Railgun 4-rail slug
  salvo every 1.2 s + hidden twin 0.15 s later, missile salvos from all 8 launchers (vanilla Swarmer sprite as stand-in).
## Vanilla Onslaught mock sim (sim_onslaught.py) - reference
- Wiki stats: FRONT shield 180, Burn Drive, speed 25, 2x built-in Thermal Pulse Cannon, 3 LB, 9 MB, 6 SB, 4 MM.
  Slot positions/arcs/engines read off the sprite by eye (no onslaught.ship) -> approximate.
- Finding: visible size of vanilla large weapons ~34x37 (Hellbore) / 34x47 (TPC) px vs our Triple Beam v10 45x78 and
  Quad Railgun v3 59x115 -> ours are ~2-3x vanilla large weapons (Onslaught_vs_TerraLight_scale.png).
## Real fx study (user uploaded graphics/fx + data) - simlib.py, run_sims.py
- Flames are drawn by the game from white alpha textures tinted by engine_styles.json engineColor:
  engineflame32 (x axis = plume, nozzle at left, tapers to a forked tip), engineglow32 (band glow), smoke32 contrails.
  LOW_TECH: engine (255,125,25), SMOKE contrails (50,50,50,50) size x2, 3 s, grow x2.5. MIDLINE (255,145,75) GLOW
  contrails. HIGH_TECH (100,165,255). Shields: shields256 fill + shields256ring, hull_styles colours
  (LOW_TECH inner (255,125,125,75), ring white).
- .ship coords: location [fwd, left] from `center` (center measured from sprite bottom-left) -> sprite px =
  (cx - loc[1], H - (cy + loc[0])). Onslaught engines: 4x (len 64, w 20) + 2x centre (len 100, w 30), LOW_TECH.
- simlib renders: 3-layer flame (fading glow band + coloured flame + white-hot core + nozzle bloom), world-space
  contrails, engines fire by thrust direction / torque, Burn Drive = ~1.9x length, real shield textures.
- Terra Light engine styles for the sims: TL_TIAMAT pink-violet (225,120,255) GLOW, TL_ASURA orange (255,140,55) SMOKE.
- Finding: with identical flame rendering, the remaining gap is the STERN HARDWARE in the hull sprites - vanilla packs
  many detailed nozzles + machinery around them; ours have a few clean cylinders -> next: redo sterns.
## Asura strong drives (run_sims.py asura -> AsuraII_v4_strong_drives_sim.mp4/.gif)
- Fastest capital: main engine slots length 190 / width 56 (vs Onslaught 100/30), glow x1.7, 4 shock diamonds, power x1.15;
  small drives 90/16 with 2 diamonds. Style TL_ASURA: engineColor (255,150,60), GLOW contrails (255,150,70,22), 1.6 s.
- Placeholder boost system: flames x2.4, speed x3.6. simlib gained diamonds / glow_mult / power / boost_level / yoff.
## Stern redo - Step 1: part library (vparts.py, parts_sheet.py -> Stern_parts_step1.png)
- Studied the Onslaught stern: tapered fluted engine cans (narrow root sinking into the hull, full width at a bulbous
  exit lip with a hot specular spot), dark grooves / thin bright ribs, lengthwise pipe bundles, angled struts, dark bay.
- Parts: engine_housing (taper, flutes, occluded root, ring bands, lip + mouth + spec, accent ring), pipe_bundle,
  rib_strut, duct_manifold, nozzle_cluster (main drive + stepped satellite cans + pipes + struts + manifold in a dark
  ribbed recess). Rendered at SS=4. Next: step 2 Tiamat stern, step 3 Asura stern.
- Step 1b: engine connections (vparts.engine_plumbing / satellite_plumbing / actuator): 2 fuel hoses per main can down
  the flanks with clamps into flanged sockets (+ copper coolant lines), accent-colour power cable into the top ring with
  a socket, thin amber data wires to a red-lit sensor pod near the exit, 2 hydraulic gimbal actuators (dark cylinder +
  polished rod + pins), 2 strap clamps with bolts; satellites get a feed hose + socket + coolant line.
- Step 1c (user: hoses/pistons/clamps look archaic - far future setting): connections replaced with
  armoured conduit SHEATHS (smooth faceted tubes segmented by glowing accent seams, no clamps), magnetic COUPLING NODES
  (flush dark disc + glowing ring + bright core, no bolts/flanges), FIELD-COIL GIMBAL collar at the engine root
  (segmented ring with glowing emitter slits + nodes, no pistons), flush LIGHT-GUIDE lines for data, segmented armour
  collar with emitter slit near the exit. Struts are sheaths too. Rule for all ships: no archaic hardware
  (bolted flanges, hose clamps, pistons) unless a design explicitly asks for an archaic look.

## Stern step 1d - connection style CHOSEN: D (structural pylons)
- Engine hangs from 2 armoured pylons (vented grille + accent seam), lines implied inside. No cables/hoses anywhere.
- Next: step 2 = apply to Tiamat stern, step 3 = Asura stern.
- Step 2 done (vs_tiamat22.py -> ss_style/tiamat_ss_v22.png): 3 fluted mains + 2 manoeuvring drives (moved outboard to X+-54),
  4 pylons (vparts.pylon) at CX+-15 and X+-43, pink/violet accent ACC_T (225,120,255). Tank->engine hoses removed, replaced by flush feed ports.
- v23 (vs_tiamat23.py): user wants engines emerging from BENEATH the pylons (v21 layout) with v22 detailing.
  Mains 23w from y354, man drives back at X+-44 (behind mains), 4 wide pylons (15/14w) laid over the engine roots.
  + diagonal rear corner jets on the v7 chamfers (X+-76, 356), drawn upright in a sub-tile and rotated 45deg (diag_jet). slots json: diag.
- VANILLA CHECK (199 .ship files): side-facing engines (90/270) only on drones/stations (gargoyle, merlon, ravelin, station_small).
  Crewed ships use rear-corner jets angled 160-200 (15-20 deg off axis, contrailSize 128): conquest, onslaught, eagle, falcon, aurora...
- v24 (vs_tiamat24.py): side thrusters REMOVED. 1 wide centre main (32w) + 2 side drives (16w, CX+-33) + 2 corner jets (same 16w drive, 45 deg).
  Every drive has an engine_cowl (vparts) directly above it covering its root; bell emerges under the lip. Stern block grilles removed.
- v25 (vs_tiamat25.py): cowls removed - drives emerge straight from under the stern block (block = pylon). Centre main 44w,
  side drives 16w pushed out to CX+-43. Corner jets (16w, 45deg) come out of hull-integrated fairings along the v7 chamfer,
  merged into one plate with the stern block.
- v26 (vs_tiamat26.py): drives shorter (pushed into hull). Centre main 40w + 4 satellites (7w @CX+-24.5, 6w @CX+-31, stepped back);
  side drives 14w @CX+-45 + 1 outboard satellite each (6w @CX+-57); corner jets 14w + 1 satellite each.
  Corner jets now exit a solid corner WEDGE merged into the stern block (outer edge = hull chamfer, small bulge at the exit, 2 engraved seams).
- v27 (vs_tiamat27.py): LAYER/DEPTH system in vstyle (backup vstyle_pre_depth.py): Ship.z height map, plate(z=/dz=), auto_z,
  raise_z, depth_pass (height-marched cast shadows toward lower-right, height tint = higher is lighter, AO in crevices), s.depth=dict(...)
  Tiamat heights: guts 0, engines 0.5-1.3, deck 1-2.5, stern 2.2, aft 2.3, belt 3.0 base + slabs 3.7/3.95 (belt split into overlapping slabs),
  ram 3.2, cap 4.2, sponsons 3.9, gun arm 4.4, collar 4.9, cmd tiers 3.3/4.7/6.0. zmark() for cylinders/mounts/core.
  Engines: centre 40w + 4 satellites tucked under its flanks in 2 ranks (8w@21.5, 7w@27.5); side drives + corner jets get 1 satellite EACH side (6w @ +-8.5).
- v28 (vs_tiamat28.py): satellites dumped -> 1 wide centre main + 1 drive each side (clear gaps) + 1 corner jet per side.
  RAM ARMOUR bow: 3 shingled glacis slabs per bow chamfer (fore slab on top) + heavy crescent prow plate (z 4.8) over cap/ram; front antennas removed.
  SYMMETRY: vstyle.SYM_CX + _sx() mirror sideways highlights; light from the bow (LIGHT x=0); depth sdir (0,1);
  and the finished left half is mirrored onto the right before the one-sided items (data line, nav lights, stencil).

## Asura v5 (vs_asura5.py -> ss_style/asura_ss_v5.png, slots asura_ss_v5_slots.json)
- Tiamat v28 language applied: side thrusters removed; symmetric light + left->right mirror; depth layers
  (deck 1.0, engines 1.1-1.3, stern/nacelle cowls 2.2-2.4, decks/eng 2.3-2.4, skin 3.0, prow 3.2, barbette 3.4, blisters 3.7 (+mount 4.0),
  keel 3.9, tip 4.4, cmd 3.4/4.8/6.0).
- Stern: 2 big fluted mains (40w) emerge from under the nacelle cowls, 2 small centre drives (12w) under a centre stern block,
  corner jets (14w, 45deg) out of the rounded rear corners of the contour skin.
- Asura v6 (vs_asura6.py): 3 big mains (CX 34w, CX+-44 30w) + 2 small per side (CX+-67 10w, CX+-78 9w), all under one stern
  armour block (hull & y>384, z 2.4) with engraved seams + 2 grilles. Nacelle ellipses + corner jets removed (no room; small outboard drives replace them).
- CORE RULE (all ships): the drive core sits DEEP (z 0.4); on deck only vparts.core_armour shows: bolted ring + 8 overlapping petals + boss,
  4 heat slits leaking the core glow. Applied to Asura v6 (orange) and Tiamat v29 (blue).
- Asura v7 (vs_asura7.py): middle main pushed in (exit 431, sides 434); the 4 small drives (10w @CX+-66, 9w @CX+-80) now fire
  DIAGONALLY back-outward (45deg, rotated tiles) from under the stern block edge. slots json 'small' = (x, y, angle).

## Neow SS v2 (vs_neow2.py -> ss_style/neow_ss_v2.png) - first pass in the current language
- Zeppelin envelope from longitudinal armour GORES (4 per side, z 3.8 spine -> 2.6 rim, shingled by 6 cross cuts), EL sky-blue on outer gores,
  white pinstripe; plate_details hardware on mid gores; 3 Armageddon tubes (orange pipes, muzzle collars, red eye) in a recessed bay;
  prow cap + shoulder glacis; buried pink core; 3-tier command tower aft; gondola stern block: 2 mains + 2 diagonal small drives.
- Asura v8 (vs_asura8.py): middle main exit 424 (deep), small diagonal drives moved outboard to CX+-75 / CX+-87.
- Neow v3 (vs_neow3.py): side FLIPPERS back (SS v1 shape) with a diagonal thruster ON each flipper deck (pad + collar, drawn over the fin);
  gondola small drives removed. Armageddon = 3 MISSILE SILOS (octagonal armoured collars, corner exhaust vents, orange split blast doors,
  hinge blocks, red launch-ready eye). Heavier gore plates (bevel 3, inset 2.4). 4 defensive flare launchers (2x3 cells) on the mid gores.
- NEOW GAMEPLAY (for the mod build): no shield -> ship_data.csv "shield type" = PHASE with "defense id" = tl_neow_flares
  (vanilla precedent: Invictus = PHASE + canister_flak, Vanguard = PHASE + damper). tl_neow_flares = flarelauncher-style system with cooldown.
  Armour: must exceed the vanilla max (Invictus 10000) - exact value TBD with the user.
- Neow v4 (vs_neow4.py): flipper detailing - armoured leading edge, vented trailing-edge heat shield, 2 spar lines, thruster HOUSING pod
  (chamfered, 2 seams, intake vent, 2 bracing lugs, pink status light) fed by a flush lit power channel from the hull.
  Silos now FORWARD-FACING launch vaults (tunnel entrances): arched orange roof with ribs + cylinder shading, open dark tunnel mouth at the
  front with a thick arch frame + marker lights, torpedo nose with the EL red-eye warhead visible inside, vented buttress cheeks.
- NEOW ARMOUR = 20000 (user decision; vanilla max is Invictus 10000).
- Neow v5 (vs_neow5.py): flipper made THICK and clean (bevel 3.4, dome); its outer-aft corner is cut square to the thrust line and the
  drive is buried inside the flipper, firing diagonally out of that face (port frame + 2 pink lights). Pod/lugs/channel removed.
  diag_jet now clips to the canvas.
- Silos TERRACED: front silo lowest (z+0), middle +1.4, back +2.8. Each higher deck step laps over the back of the silo ahead,
  with a lit riser + contact shade, so the stepped launch line reads clearly (rear silos fire over the ones in front).

## Artemis SS v1 (vs_artemis1.py -> ss_style/artemis_ss_v1.png) - first pass in the current language
- Locked EL layout kept (catamaran, same slots). Layers: guts 0, catapult trench 1.2, flight decks 2.2 (recessed EL green), hatches 2.5,
  hull 3.0, inner rail 3.4, outer rail 3.6, PD blisters 4.0, shuttle 3.3, command stick 3.8 / bridge tip 5.0.
- 8 lift/launch hatches (hazard frames) = the 8 fighter bays; runway dashes, bow chevrons, deck edge lights.
- Buried armoured core in each hull stern; 4 mains under the hull sterns + 2 diagonal corner jets. Pink lit magnetic catapult rail.
- Artemis v2 (vs_artemis2.py): launch hatches removed. RUNWAY language studied from vanilla Astral/Heron (Eos not in vanilla data):
  dark lengthwise-strip deck, 2 rows of tiny guide lights, glowing green edge line sweeping round the aft end, lit launch threshold bar,
  glowing pink recovery slot aft; each bow opens into an ARCHED LAUNCH MOUTH (open to space, Astral-style) under a gantry arch with marker lights.
  Corner jets: 2 per side, stepped down the outer stern wall.
- Artemis v3 (vs_artemis3.py): user found v2 (Astral runways/open bow) ugly -> back to v1 base (closed bows, green deck, chevrons, edge lights).
  Fighter bays = 8 HANGARS in the style of the user's reference: raised armoured frame, recessed dark interior, 6 glowing green slats
  (brightest mid-length), shade under the forward lip, frame marker lights. 2 corner jets per side kept.
- Artemis v4 (vs_artemis4.py): hangars = LAUNCH RUNWAYS INTO THE SHIP (user's reference): per deck 2 long recessed slots open at the bow end,
  2 rows of glowing green guide-light dashes, floor darkening aft, running under an armoured hangar overhang (vent, mouth shade, lights).
  Each slot serves 2 of the 8 fighter bays.
- Artemis v5 (vs_artemis5.py): 4 runway hatches per deck side by side (one per fighter bay), all starting at the hangar overhang and running forward.
- Artemis v6 (vs_artemis6.py): user asked to go BACK to the v1 fighter hatches (lift/launch hatches with hazard frames, runway dashes,
  chevrons, edge lights). v2-v5 hatch/runway experiments rejected. Kept: 2 diagonal corner jets per side.
- Artemis v7 (vs_artemis7.py): the 4 v1 hatches per deck now packed from the BACK of the deck (bay rows y 360/314/268/222, slots json updated)
  and turned into RUNWAY HATCHES: hazard-framed ramp that slopes down aft (floor darkens), 2 rows of green guide lights, roll-in chevrons
  pointing aft, dark tunnel mouth under an armoured hood -> fighters drive from the deck into the ship. Runway dashes only on the front half.
- Artemis v8 (vs_artemis8.py): hangar entrances (futuristic, per reference): chamfered armour frame, ramp sinking aft, 2 rows of bright
  green guide lights with glow halo, arched brow + dark arched mouth where the fighter drives in. No hazard stripes/chevrons.
  Spaced with LANDING GAPS, still starting from the back (bay rows 356/290/224/158).
- COMMAND ROOM RULE (all ships from now on): Tiamat/Asura concept = 3 stepped tiers tallest toward the centre, wide bridge glass on the
  front of tier 2, fire-control dome on tier 3, faction/EL colour as a livery band. Artemis: tower over the stern joint, EL pink bands +
  short pink comms spine aft (remnant of the EL stick).
- Artemis v9 (vs_artemis9.py): hatches FUSED with the deck (no frame): ramp cut straight into the flight deck, sinking aft, guide lights,
  the deck itself arches over the dark mouth. Command tower LONGER: tiers now 290-436 / 300-410 / 330-400, bridge glass moved forward,
  2 vents + dome on tier 3, pink bands fore and aft.
- LAYER SHADOWS v2 (vstyle.depth_pass): sdir may be a LIST of directions; shadows from each are max-combined. Standard now:
  depth = dict(unit=7.0, s_str=0.9, tint=0.38, ao=0.6, ao_r=5, sdir=((0.6, 0.8), (-0.6, 0.8)), s_soft=0.9) -> every raised layer throws a
  soft, clearly visible shadow down-left AND down-right (symmetric), plus stronger AO in crevices.
- Artemis v10 (vs_artemis10.py): hangar ramps drawn WITH DEPTH: cut walls widen aft (taller), floor narrows + darkens, grip ribs crowd
  together, guide lights shrink/dim toward the aft, the deck itself overhangs a black tunnel mouth with a lit arched lip and throws a
  shadow onto the ramp. Uses LAYER SHADOWS v2.
- Artemis v11 (vs_artemis11.py): hangar ramps widened to the full deck width (half-width 33.5 inside the rails), wall growth 6 px, guide
  lights inset and converging.
- Artemis v11 accepted as "passable for now". Next in queue: Siren (capital, convertible). Open: re-render Tiamat/Asura/Neow with LAYER SHADOWS v2.
- LAYER SHADOWS v2 applied to all finished capitals: Tiamat v30 (vs_tiamat30.py), Asura v9 (vs_asura9.py), Neow v6 (vs_neow6.py), Artemis v11.

## Siren ship-system rule UPDATE (user, replaces the old "fighters recalled & held" line)
- Battleship mode: fighters STAY deployed and keep fighting, guns up; but fighter REPLACEMENT is PAUSED (the refit timer does not count down).
- Carrier mode: replacement timer resumes ticking from where it paused; guns folded/disabled as before.
- Implementation plan (ShipSystemStatsScript / EveryFrame): battleship mode -> for each FighterLaunchBayAPI, freeze refit progress
  (store the bay's current replacement progress each frame and write it back, or apply a huge FighterRefitTimeMult); carrier mode -> remove.
  Do NOT touch the fighter replacement RATE, only the timer. Transition 2-3 s, cooldown 10-15 s, AI switch logic, as before.

## Siren SS v1 (vs_siren1.py -> ss_style/siren_ss_v1.png) - first pass in the current language
- Parts promoted to vparts: diag_jet(s, g, x, y, w), hangar_ramp(s, bx, by, hw, L) (Artemis-approved ramp), iris_hatch(s, x, y, r) (turret well).
- Wide half-cylinder hull: grey armour z 3.0, side belts z 3.5 (orange stripe = Siren EL orange), bow/aft rims 3.3; recessed EL-green flight
  deck z 2.2 (panel grid, edge lights, chevrons); 4 hangar ramps at the EL bay spots with white landing marks; 3 main-gun IRIS wells
  (guns fold under in carrier mode); buried pink core aft; 8 PD on belt blisters; 2 mains under the stern + 1 diagonal jet per corner;
  command = 3 ROUND tiers on the neck (EL pod reshaped), wide cyan bridge visor.
- Siren v2 (vs_siren2.py <mode>; outputs siren_ss_v2_carrier.png / siren_ss_v2_battleship.png):
  * CARRIER: central gun bay (CX+-88, y58-208) sealed by a 2-leaf armoured hatch of shingled slabs (fore slab highest), EL-green + orange
    stripes, heavy hinge rails, centre seam with lock lights.
  * BATTLESHIP: leaves slid under the rails; bay floor = LIGHTER crew-deck armour (crew hatches, walkway lights); 3 octagonal main-gun
    PLATFORMS lifted high (z 5.0) on 4 lift columns each, shaft shadow round them, large energy turret rings.
  * Fighter bays moved to the FIXED deck so they work in both modes: (63,140), (277,140), (120,226), (220,226) - octagonal launch SILOS
    with split EL-green doors.
  * Command = elongated 3-tier tower along neck+pod (same concept as Tiamat/Asura/Artemis), cyan bridge glass forward, orange bands.
  * 2 diagonal jets per rear corner (bigger, visible).
  * Mod build plan: hull sprite = battleship-open interior; the hatch leaves = DECORATIVE animated slot (frames closed -> open) drawn over it;
    gun platforms = part of the large-weapon slot art (or decorative lift anim); switch driven by the Carrier<->Battleship system script.
- WEAPON PROTECTION STUDY (vanilla): small mounts sit ~11-31 px inside the hull edge on capitals, SUNK in thick armour rings, with armour
  mass / lobes / wedges outboard; PD grouped. Ours sat 8-9 px from the edge on raised blisters (Artemis, Siren). User: big guns stay exposed
  (accepted); fix small weapons via CONTOURED silhouettes (not brick-shaped). Vanilla silhouette: fills-box 0.64-0.74, solidity 0.80-0.90.
- Siren v3 (vs_siren3.py <mode>): CONTOUR pass - core hull at +-140 + 3 armour LOBES per side to +-153 (bow shoulder with a back-sloping
  glacis face, mid lobe, aft lobe carrying the 2 corner jets); PD regrouped as PAIRS sunk into socket pads in the 2 notches per side
  (slots: x CX+-128, y 88/104/176/192 - shared with EL). Solidity 0.87 -> 0.85, fills-box 0.70 -> 0.67.
- Siren v4 (vs_siren4.py <mode>): PD SPREAD OUT per side - 1 sunk in each flank notch (CX+-128, y 96/184) + 1 fore and 1 aft on the green
  deck strip in octagonal collars (CX+-104, y 64/206), clear of the silos. Green octagons = the 4 fighter launch SILOS (split EL-green doors).
- Siren v5 (vs_siren5.py <mode>): small deck silos REMOVED. The central bay is the SILO HANGAR:
  * CARRIER: hangar OPEN - deep shaft (inner walls: aft wall lit, fore wall in shadow, ribbed side walls), dark hangar floor with guide grid and
    4 lit LAUNCH CRADLES = the 4 fighter bays (slots CX+-44, y 98/168), rim landing lights, hatch leaves stowed under the rails.
  * BATTLESHIP: the hangar converts into an armoured deck; 3 gun platforms lifted up from inside the ship (unchanged from v2-v4).
- Siren v6 (vs_siren6.py closed|open|battleship): NO visible fighter bays - the ONE silo hangar is the fighter gate.
  * closed = carrier idle (sealed 2-leaf hatch); open = carrier launch/recover frame (shaft + lit lift pad); battleship = armoured deck, 3 guns up.
  * Mod: animated decorative hatch plays closed->open when any wing launches/recovers (FighterLaunchBayAPI activity), CARRIER mode only;
    launch-bay slots clustered at the hangar centre (hidden).
  * PD: no mounts between the armour lobes; all 8 on the green deck strips (CX+-104, y 64/111/158/206) in octagonal collars.
  * Command tower WIDER + SHORTER (~52 px, just longer than the 42 px main drives): tiers +-31 / +-23 / +-13, y 250-302.
- Siren v7 (vs_siren7.py closed|open|battleship): command tower wider (+-40 / +-30 / +-17) and 4 px longer (to y 306); corner jets
  brightened (metal 176,174,180) and raised to z 3.6 so the lobes' shadows no longer bury them.
- Siren v8 (vs_siren8.py closed|open|battleship): deck core cover REMOVED (core buried under the tower, nothing on deck). Command tower now
  runs from just aft of the silo hangar (y 213) to 10 px past the drive exits (y 302), width kept (+-40); glass forward, 2 vents + dome.
- Siren v9 (vs_siren9.py closed|open|battleship): tower starts 5 px lower (y 218). DRIVE CORE now sits at the centre of the SILO HANGAR
  floor (containment collar, pink glow), visible only in the open-hangar frame. Hangar interior: 4 lit power conduits core -> walls
  (+ secondary feeds), 4 FIGHTER REPAIR BAYS (yellow markings, skid guides, gantry arm + weld head, parts racks), 2 CREW ROOMS per side wall
  (lit windows) with a PRESSURE ROOM/airlock between them (inner green / outer red cycle lights, doors), catwalks along fore/aft walls.
- Siren v10 (vs_siren10.py closed|open|battleship): DECK IN DEPTH - green sheet replaced by machinery (guts) under separate armour plates
  with gaps, EL-green livery bands on the plates, lit pink POWER TRENCH down each side strip + 3 cross-feeds per side (hangar wall ->
  trench -> lobes), aft feeds into the tower, vents and access hatches; fore/aft strips plated with vents.
- Siren SIM (sim_siren.py -> Siren_v10_modes_sim.mp4/.gif, 36 s; `python sim_siren.py tf` -> Siren_transform_5s.mp4/.gif):
  carrier launch through the silo hangar (fighters rise out of the shaft), 5 s transform (0-25% doors slide open, 25-55% armoured deck
  slides in, 55-100% gun platforms rise), battleship fire with wings still out, a fighter lost -> replacement timer FROZEN (6.0 s),
  5 s transform back, timer resumes, replacement launches, recall into the hangar. Vanilla Broadswords + autopulse/vulcan as placeholders.
  simlib additions: c['hull'] per-frame sprite swap, c['slot_scale'] (per-slot sprite scale, no fire unless 1.0), Sim.hook, c['hud'] bottom bar.
- Siren v11 (vs_siren11.py closed|open|siloopen|deck|battleship; tf_siren.py -> Siren_v11_transform_5s.mp4/.gif + _steps.png):
  3 GUN SILOS built into the hangar floor (octagonal collars, orange split blast doors, hazard lip, lift lights); guns moved to fit the
  floor: (116,104), (224,104), (170,174), silo/platform r 27. Interior re-laid: core (CX,112) between the silos with conduits to each gun
  lift, 2 repair bays in the aft corners, crew rooms + pressure room on the fore wall, side-wall pressure rooms. Wall depth D 13 -> 6.
  TRANSFORM (5 s): 0-20% hangar doors slide open, 20-40% gun-silo doors open, 40-70% platforms rise out of the silos (scale + light +
  shadow), 70-100% 2nd-layer armoured deck slides in with CUT-OUTS matching the 3 guns (lit cut edge), closing round them.
- Siren v12 (vs_siren12.py; deck_sheet_siren.py -> Siren_v12_deck_vertical.png): 2nd-layer deck now slides VERTICALLY in 2 interlocking
  leaves: fore leaf slides aft, aft leaf slides fore; per deck column each leaf stops at the gun footprint (octagon + 1.5 px cut-out), else
  they meet at y 140 -> no leaf ever passes through a turret. Outer guns nudged to x 112 / 228 so no two guns share a deck column
  (verified: 0 stacked columns). SIREN DONE for now -> next ship.
- WEAPON PROTECTION applied: vparts.sunk_mount (octagonal collar, dark socket, turret ring below the collar, raised crescent LIP on the
  outboard side + faction accent). Tiamat v31 (vs_tiamat31.py): 8 deck PD sunk. Asura v10 (vs_asura10.py): 6 wall missiles sunk into
  their blisters + 2 deck missiles sunk. Positions unchanged (slots unchanged).

## Hastur SS v1 (vs_hastur1.py -> ss_style/hastur_ss_v1.png) - first pass in the current language (EL slots unchanged)
- Baguette: waisted contour (70 -> 62 at the waist between the sponsons, tapering aft), longitudinal armour bands (spine highest) cut
  into 5 segments, cyan livery lines, lit power trenches beside the spine + cross-feeds to the sponsons, waist radiators, hatches.
- 4 medium energy in armoured SPONSON lobes (contour) with sunk mounts + pink lips; 2 small ballistic in ball-flank blisters (sunk).
- 3 hidden medium railguns = embrasures in the prow armour (barrel tips visible inside) under a prow cap.
- Buried core (cyan) under an armoured cover mid-baguette; hangar mouth under the baguette's aft overhang (fighter bay).
- Ball: stepped armour shell ring with EL cyan band; 3-tier command tower on the ball with the EL blue screen as bridge glass.
- 2 drives from under the ball + 1 diagonal jet per rear quarter. Layer shadows v2, symmetric light + mirror.
- Hastur v2 (vs_hastur2.py): STACKED hulls - ball z 1.8-2.3, baguette z 5-6.8 over the front third of the ball, casts its shadow +
  overhang darkening onto the ball; tower lowered (3.0-4.6) below the baguette. 4 medium energy = BUILT-IN side turrets with the Tiamat
  mechanism (trunnion arm + collar + tracking ring + EL pink ring, pivot at the sponson face CX+-84, arcs 0-135 front / 45-180 rear,
  builtin 'tl_hastur_beam', barrels = weapon sprite - needs its own art; preview uses a 0.62x Triple Beam). 3 hidden = medium BALLISTIC
  (mount HIDDEN, swappable) behind the prow embrasures. 4 small ballistic PD: (CX+-62, 320) at the hull joint, (CX+-60, 370) near the
  diagonal jets, sunk with cyan lips. Diagonal jets bigger/brighter (15 w, z 3.6). Nav lights moved off the jets.
- Hastur v3 (vs_hastur3.py hull|module -> hastur_ss_v3_hull.png, hastur_ss_v3_module.png, composite hastur_ss_v3_full.png):
  TWO-PART SHIP. Main hull = front hull (baguette), now ending at the ball centre (covers the front HALF of the ball); clean armour only
  (longitudinal bands, cyan lines, bolts; trenches/hatches/radiators/core cover/hangar mouth removed). Its drop shadow is BAKED into the
  sprite as semi-transparent alpha so it falls on the module below. Slots: 4 built-in medium energy (Tiamat mechanism), 3 hidden medium
  ballistic, launch bay (hidden), STATION_MODULE slot 'MODULE_COMMAND' at (CX, 342).
  COMMAND MODULE = the ball (the whole back hull is the command room): radial armour panels, stepped shell ring + cyan band, docking
  collar (under the front hull), curved blue COMMAND VISOR across its front, 2 small ballistic (CX+-52, 362) sunk either side of the visor,
  2 drives + 1 diagonal jet per rear quarter. module_slots in the json.
  Mod note: parent/module draw order must put the front hull OVER the module (verify in-game; fall back to baking if needed).
- Hastur 3D block-out (artifact 'Hastur 3D Block-out', source scratchpad/hastur3d.html, three.js r128) v2 per user:
  ball rounder (vertical radius 60 of 75); VISOR on the ball's FRONT face under the front hull; DOCKING HANGAR (fighter bay) below the
  visor; 2 small ballistic either side of visor/hangar; 3 medium ballistic in a COLUMN along the front hull's belly, 90 deg forward arc;
  front hull FATTER (34 + bevels; drive core inside, cyan side vents); hull detail (top plates, side belts + seams, sponson seams);
  built-in side turrets = 2 barrels (Tiamat mechanism). Parts 1,2,3,5,9,10 otherwise unchanged. 2D sprites to follow once the 3D is approved.
- Hastur 3D v3 (user: "really satisfied"): front small ballistic IN LINE with the hangar (either side, equator); 2 more small ballistic
  near the diagonal jets (#11, rear quarters); HULL CONNECTION (#12): front hull raised onto a docking cradle - saddle wrapping the ball's
  crown (16 ribs), central docking neck + clamp ring with bolts + cyan ring, 2 load pylons, forward A-frame struts from the hull belly to
  the ball's front shoulders (foot pads), cyan-ringed transfer conduits (power + crew) from the hull core down into the module.
  Small ballistic total = 4 (2 front, 2 rear). Source kept at ss/hastur3d.html.
- NEW WORKFLOW RULE (user): make a 3D block-out (three.js artifact, numbered parts, show/separate/camera/arc-sweep) for every ship
  BEFORE/alongside its 2D sprite, so layout mistakes show up early. Next: redraw Hastur 2D from the approved 3D, then 3D for the others.
- Hastur 3D v4: A-frame struts + transfer conduits REMOVED (user: sticks in front of the visor looked weird); saddle cradle + pylons removed.
  Connection = ELEVATOR TOWER on the ball's crown (py 326): bolted clamp collar on the ball, armoured column, 2 glass lift tubes with lit
  cars, top collar + cyan ring in the hull belly; front hull raised (HB 90) so the tower reads. Rear small ballistic (#11) moved out to the
  ball's sides (phi 0.5 +- 0.40 pi), clear of the drives and diagonal jets.
- Hastur v4 2D (vs_hastur4.py hull|module; hastur_ss_v4_hull/module/full.png) redrawn from the APPROVED 3D (user: fine, view is top-down):
  front hull = nose plate, 3 plate bands (spine highest), side armour belts on the straight walls, cyan core vents at the waist, built-in
  side turrets (arm + collar, 2-barrel weapon sprite TBD); 3 medium ballistic HIDDEN in a belly column (CX, 70/120/170) arc 90.
  Module = meridian ribs, crown seam, cyan rim band, VISOR + DOCKING HANGAR on the front face (launch bay slot at (CX, 270) in
  module_slots), 4 small ballistic (CX+-53, 289) front / (CX+-68, 364) sides, ELEVATOR TOWER on the crown (CX, 326) with 2 lift tubes.

## Hannibal 3D block-out v1 (artifact 'Hannibal 3D Block-out', source ss/hannibal3d.html) - from the locked EL layout
- 1 bulb body (ellipsoid 96x104 top, 58 tall, violet band, ribs, core inside - violet vents), 2 snout (cylinder r40 x-scaled to 50,
  py 34-250, rides over the bulb front; spine plate, rings, side belts), 3 medium energy x2 on orange rings at the snout front (30 deg),
  4 large energy under the snout tip (hidden sprite), 5 small ballistic PD x6 on the bulb walls, 6 pink command head with cyan visor
  (EL, py 332), 7 one central drive (pink ring stack), 8 diagonal jets x2, 9 orange window rows, 10 landing leg (3D only).
- Hannibal 3D v2: part 4 is MEDIUM energy (not large) - same turret as part 3; ALL 3 medium energy arcs = 90 deg forward.
  Detail pass: snout armour panels + side grille strips + side lights, keel with ribs under the snout, nose cap armour hoops + sensor dome,
  bulb shingled dome tiles (3 rows), radiator fins on the rear quarters, side hatches with orange strips, red/green nav lights, sensor mast
  + dish + beacon behind the head, head brow armour + ear pods, drive housing collar + 8 cooling fins.
- Hannibal 3D v3 (approved to draw): part 3 moved IN LINE with part 4 at py 52 (all 3 medium energy on one line); command head raised
  on a 26-unit neck (2 collar rings) so the bridge sees over the snout; mast/dish/beacon lifted too.
- Hannibal SS v1 (vs_hannibal1.py -> ss_style/hannibal_ss_v1.png) drawn from the 3D: bulb = shingled dome tiles (3 rows) + crown plate
  with violet ring, meridian ribs, violet rim band, orange window rows, radiator fins, violet core vents; snout (z highest after the head)
  = spine plate, armour panels, hoop seams, side belts + orange lights, violet lines, nose hoops + cyan sensor; 3 medium energy in line
  at py 52 (2 on orange rings, middle hidden under the tip), arcs 90 fwd; 6 PD sunk (violet lips); raised pink head + cyan visor + brow +
  ear pods; pink ring-stack drive + 2 diagonal jets.
- Hannibal command room TRIAL: 3D v4 has a toggle Tower (Terra Light) / Head (Earth Light). Tower = 3 stepped tiers at the head spot,
  same height, pink top tier + cyan visor glass on tier 2's front, violet band, fire-control dome, vents. 2D: vs_hannibal2.py ->
  hannibal_ss_v2.png (tower) vs v1 (head); comparison Hannibal_head_vs_tower.png. Awaiting the user's pick.
- Hannibal v3 (vs_hannibal3.py -> hannibal_ss_v3.png; 3D v5): user picked the TOWER; made LONGER (tiers 282-374 / 286-362 / 302-348)
  and the PINK TOP REMOVED (top tier = light armour). Cyan visor glass forward on tier 2, violet band, vents, fire-control dome.
- Hannibal v3 ACCEPTED ('good enough'). Next: Regulus.

## Regulus 3D block-out v1 (artifact 'Regulus 3D Block-out', source ss/regulus3d.html; built on the Hannibal template)
- Bulb 92x100 (EL pink livery) + snout +-48 py 30-250; 4 built-in bubble-missile pods (green): fore pair tucked under the snout tip
  (4 warheads each, facing fwd, arc 120), aft pair on the rear flanks (10 warheads each on the outer face, arc 180); 10 small energy PD
  (2/side snout walls, 3/side body, sunk, pink lips); command = Hannibal-approved 3-tier TOWER (no EL head); 1 central drive + 2 diagonal
  jets; window rows; green landing leg (3D only).

## Regulus 3D v2
- Aft bubble-missile pods now point forward: 8 warheads each (2 rows x 4) on the front face, yaw ±0.15 outward. Slot change: aft pods angle ~±8 fwd, arc 120 (was 90°/180° to the sides).
- Palette split from Hannibal: sand armour (0xa9a290), teal livery (0x33c9b4), lime pods (0xb4dc3c), amber visor glass, pale-cyan window lights, teal drive glow/core. Hannibal keeps grey/violet/orange/cyan.

## Regulus 3D v3
- Aft pods rebuilt as crescents wrapped round the bulb's rear flank (angle 90°→135° from the bow, radial offset +3..+39, 22 tall + lid), flat front face at the widest point (py 272) carrying 8 warheads (2x4). Future slot: ~(52,272)/(278,272), angle ~0, arc 120.
- Diagonal jets shrunk (~70%) and moved beside the main drive (bulb angle 2.66, ~x±41, py ~361), 45° outward. Regulus top speed to be set below Hannibal's.
- Body PD: 3 per side in one line on the bulb equator at angles 0.78/1.04/1.30 (between snout and pod fronts). Window rows moved below the PD line and under the pods; radiator fins removed; hatch/nav lights moved clear.

## Duilius 3D v1 (duilius3d.html)
- Canvas 190x436, CX=95. Elliptic capsule hull (half-width 52, half-height 40), nose py 48, cylinder py 100-310, stern cap to py 344.
- Palette (distinct from Hannibal/Regulus): gunmetal armour 0x8f979f, yellow livery 0xffc62e, cobalt claw bays 0x2f7ef0, pink tower glass (EL pink-dome cue).
- Claw bays: side galleries x +-46..62, py 112-322; 4 hatches each at py 136/191/246/301 (sliding doors, grapple claw + cable inside). Ship system fires all 8.
- 2 Large Ballistic under the bow at (65,66)/(125,66), under-hull, arc 20; barrels poke ~40 px past the nose.
- 6 Small Ballistic PD sunk into the upper hull at x+-30, py 96/176/256, yellow outboard lip, arc 240 to their side.
- Drive core under an armoured petal cover on the spine (py 216). 3-tier command tower at the stern (py ~266-334).
- Drive: ribbed collar py 348-398 (EL ribs) + one big bell (ENG 95,416); 2 small diagonal jets at (51/139, 334), 45 deg outward.

## Regulus SS v1 (vs_regulus1.py -> ss_style/regulus_ss_v1.png, 330x412) - from 3D v3
- slots: fore pods (109,66)/(221,66) HIDDEN MEDIUM MISSILE angle +-20 arc 120; aft pods (52,270)/(278,270) angle +-10 arc 120;
  10 SMALL ENERGY PD: snout (115.5/214.5, 130/185) + bulb equator at bulb angles 0.78/1.04/1.30; ENG (165,392); 2 small jets.
- core vents from the 3D omitted in 2D (they would sit on top of the bulb PD in top view).
## Duilius SS v1 (vs_duilius1.py -> ss_style/duilius_ss_v1.png, 190x436) - from 3D v1
- slots: 6 SMALL BALLISTIC PD (65/125, 96/176/256) arc 240; 2 LARGE BALLISTIC under-hull (65/125, 66) arc 20 hide; 8 SYSTEM claw slots (33/157, 136/191/246/301); ENG (95,416).

## Abaddon 3D v1 (abaddon3d.html) - canvas 300x560, CX=150
- Palette: olive-gunmetal armour 0x7f8676, green livery/radiators 0x4fe07a (EL green), bronze trim, crimson torpedo, green visor glass.
- Side bodies x 40-94 / 206-260, py 140-430, height +-34; green radiator grilles py 150-190 + 340-396; box thrusters on the rear faces (ENG 67/233, 432).
- Front frame py 195-335 (chamfered), bridging both bodies ABOVE the torpedo (y 46-64); 2 Medium Energy on hex pads (98/202, 256) arc 270;
  3-tier command tower (py ~205-285) replaces the swept canopy; drive-core petal cover at (150,302); 4 Small Ballistic PD sunk in the outer walls at (40/260, 230/318).
- 2 small diagonal jets at the rear outer corners (42/258, 420).
- Apocalypse torpedo (module): ellipse 56x44, nose py 18, body to 440, bell ring py 458. Docked: 4 X-fins RETRACTED into the tail, bell petals CLOSED
  (bud, fits the 112 px gap) so it can slide out forward; 4 bronze docking clamps (inner walls, py 176/384) swing open to launch. Fins + bell deploy after launch.

## Abaddon 3D v2
- Command room = FIGHTER COCKPIT (user, exception to the 3-tier tower rule): jet-style nose fuselage on the centreline (py ~150-332, half-width 15),
  pointed nose cone + pitot past the frame front, green bubble canopy (py ~192-252) with frame hoops + rails, side air intakes, dorsal spine with the core cover (150,302).
- FRONT FRAME RETRACTS on launch (user): split on the centreline; both halves (with the 2 Medium Energy + the 4 PD in their corners) slide out 92 px sideways,
  torpedo fires, halves close again. Cockpit rides on the PORT half. Timeline: frame 0-0.8 s, clamps 0.4-0.9 s, torpedo from 1.0 s, frame closes ~4.4-5.3 s.
- Torpedo fins now stay OUT while docked (EL look) - the open frame gives them a clear path; bell still bud-closed until clear of the hull.
- Starsector note: needs an open-frame hull sprite (or animated deco halves) + the module launch script.

## Abaddon 3D v3 (v2 frame-retract + always-out fins CANCELLED by user)
- Back to v1 frame (fixed, one piece). Jet-style fighter cockpit kept on the frame centreline (user request), core cover on its dorsal spine.
- LAUNCH: the 2 side boosters (side bodies, with their grilles, engines, jets and docking clamps) retract 24 px outward so the torpedo can detach,
  clamps let go, torpedo slides out forward, boosters close again. Frame + mediums + frame-corner PD stay put. Fins retracted / bell bud while docked (as v1).

## Abaddon 3D v4
- Booster retraction on SLIDE RAILS: 3 I-beam rails per side fixed under the frame (py 201/266/330, x offset 48-126, bronze wear strip, end stops),
  carriages on the boosters ride them. Retro jets on the booster fronts brake the ship during the launch.
- Cockpit widened: fuselage half-width 26 (was 15), canopy 15 wide x 36 long, intakes at +-25.5, spine 18 wide.
- Launch sequence: clamps release + boosters retract 24 px (0-0.9 s); the Abaddon HALTS (retros) while the torpedo drifts out UNPOWERED (from 1.0 s);
  once clear, the fins slide out of its base (3.8 s), the bell opens (4.2 s), then it ignites and bursts toward the target (4.8 s); boosters close (4.2-5.0 s).
- v4b: booster-front retro thrusters = armoured housing + 3 small nozzles each (bronze tip rings, glow + flame while halting). ABADDON 3D APPROVED (good enough).

## Iris 3D v1 (iris3d.html) - canvas 220x436, CX=110
- Palette (distinct): white ceramic armour 0xcfd3d0, emerald deck 0x2fae62 (EL green deck), magenta trim 0xe0409a, blue tower glass.
- Flight deck py 30-272 (chamfered bow), top y 20; 2 runway lanes (x 74/146); 4 HANGAR RAMPS at the bays (74/146, 120/220), 38x58 openings,
  ramp slopes DOWN toward the stern into a lit hangar mouth (the lane runs into the ship); magenta approach lip at each ramp's bow edge.
- Deck edge sponsons (armoured rails) with tapered bulges holding 8 Small Ballistic PD (x 30/190, py 80/140/200/260), sunk, magenta lip.
- Raised stern block (top y 30) py 272-410 tapering; 2 centreline Medium Missile pads (110, 298/342) arc 240; 2 extension pods on arms (26/194, 340) with pads, +-20 arc 180.
- 3-tier command tower (py ~364-408), blue glass; core deep below it with heat vents either side. 2 round main drives on the stern face (95/125, 410); 2 diagonal jets on the stern taper (54/166, 372).
- Iris confirmed CRUISER (user): 4 bays = one more than vanilla cruiser carriers Heron/Mora (3). User: bigger than 'Eos' (not in our vanilla data copy). Canvas stays 220x436.
## Iris 3D v2 - contours (user: "too brick-like")
- Hull built from half-width profiles: ogive bow (hw 0->82 over py 22-80), slight waist bulge, deck 82-84 hw; stern hw 84 to py 318 then convex cosine taper to 40 at py 410.
- Stacked bevelled tiers stepping inward: deck rim (y 11-19), hangar tier (-6..11, inset 9), keel tier (-22..-6, inset 24); stern: main tier, stepped top plate, keel tier.
- Tube sponson fairings along both deck edges with flattened PD blisters; sloped glacis deck->stern; raised oval missile deck on the stern; dorsal ridge into the tower;
  extension pods = domed round pods on swept bevelled fairings grown out of the stern flanks.
- Iris 3D v3: deck detailing - two-tone deck (lighter lanes), plate seam grid, catapult tracks + shuttles from each ramp's bow edge forward, lane lights, stern recovery zones (magenta hatch) + 3 arrestor wires per lane, service hatches, tie-downs, edge heat grates, bow threshold bars.
- Iris 3D v4: deck recoloured from emerald to slate grey (user: green too flashy): deck 0x4a535c, lanes 0x5c6670, seams 0x353c43, ramps 0x3a424a.

## Selene 3D v1 (selene3d.html) - canvas 320x390, CX=160
- Palette: plum armour 0x7a6a86, rose-gold trim 0xe0a07c, muted rose sensor cap, graphite decks 0x3e4148 (not green - user found green flashy on Iris), mint glass.
- Dome (160,262) 80x86, 58 tall: ribs, rose-gold equator band, shingled crown plates, crew windows under the equator.
- EL pink half-oval cap -> armoured sensor cap with a mint glass slit on the dome front. Core under a petal cover on the crown (the EL light plate).
- Low 3-tier command tower on the dome's rear slope (TL tower rule).
- Side pods (60/260, py 215-315) + short launch decks forward (py 112-222), one hangar ramp per deck (py 156-200) sloping down into the pod, catapult + lane lines.
- 2 Medium Composite on rose-gold ringed sponsons (24/296, 262) arc 200 +-20; engine crest py 305-356 with 2 PD sunk (90/230, 330) arc 240; 3 big drives (120/160/200); 2 diagonal jets at the crest corners.
## Selene 3D v2
- Diagonal jets moved to the side pods' rear outer corners (38/282, 306), 45 deg outward.
- Hangar ramps in the decks removed: each deck runs straight into a HANGAR PORTAL at the pod front (py ~201-219): armoured hood (posts + roof), dark bay, lit edges, rose-gold lintel, retracted blast-door slats, threshold stripes.
- No command tower (user): command room inside the dome behind 4 mint VISOR bands at lat 0.45 (front = bridge, back, left, right) with rose-gold frames + mullions; sensor cap removed.
- Selene v2b: diagonal jets back on the engine drive block (crest) outer corners (83/237, 350). SELENE 3D APPROVED.

## Fenrir 3D v1 (fenrir3d.html) - canvas 190x236, CX=95
- Palette: gunmetal 0x5a5f69, signal-orange livery 0xff7a2a (EL orange ribs), cyan visor.
- Low teardrop core body (py 20-204) with orange racing stripes; 4 armoured spherical gun pods (r 27) at (95,40),(59,90),(131,90),(95,146), each a swappable Medium Ballistic turret, fwd arc 60.
- Core petal cover in the gap between the pods (95,95); low 3-tier tower behind the middle pod (95,180); orange ribbed collar + big main bell (ENG 95,214).
- Side engine pods (37/153, 162-206) on swept pylons, rear-firing (not lateral); diagonal jets on their outer rear corners.
- PROPOSAL: 2 Small Ballistic PD sunk in the side engine pods (37/153, 176) - not in the old slot list, awaiting user.
## Fenrir 3D v2
- Bulkier body: half-width 68, 28 tall, broad front (taper 0.84), armoured side skirts, dorsal plate.
- Gun pods: FRONT LINE of 3 - tip (95,40) raised + (46,58),(144,58) either side, overlapping/stacked; middle pod (95,150) raised out of the body. SLOTS CHANGE: pair moved from (59/131,90) to (46/144,58).
- Side engine pods bulkier (32/158, 156-208); diagonal jets now the SAME nozzle as the aft thrusters (r 9: can, collar, orange rib + lip, glow) in an angled armoured cowling on each pod's outer rear corner.
## Fenrir 3D v3 (user: bulk = HEIGHT)
- Body back to half-width 56 but 40 tall; rear clipped to a flat bulkhead at py 186 so the drive (collar py 186-201, bell to ~222) mounts behind it with no overlap.
- Gun pods: tip pod FORMS the nose (95,34); flank pods on the hull sides beside the tip (45/145, 64) at mid-height; 4th pod ON THE CORE on the crown (95,112), its armoured seat with heat slits = the core cover.
- Long 3-tier command tower on the rear crown (py ~137-183).
- Side boosters rebuilt clean: lathe nacelles (px 35/155, py 150-206) with flush orange rings, swept airfoil pylons, aft nozzle; diagonal jet = same nozzle from a blended blister on the rear outer flank; PD proposal on the nacelle crowns.
- SLOTS: MB (95,34), (45,64), (145,64), (95,112).
## Fenrir 3D v4 (checked vs EL art: the body is a tall bulb)
- Hull: 62 up / 44 down, half-width 56, py 50-186, flat rear bulkhead; latitude + meridian seams, orange stripes, equator belt.
- Pods on BOLTED NECKS (hull flange + bolts, orange pod collar) - no interpenetration: tip (95,22) fwd arc 60; left flank (26,84) turned 90 CCW = faces LEFT arc 90; right flank (164,84) turned 90 CW = faces RIGHT arc 90; core pod on top of the core (95,118) arc 300 (its wide neck = core cover).
- SLOTS: MB (95,22) a0 arc60; (26,84) a90 arc90; (164,84) a-90 arc90; (95,118) a0 arc300.
- Long 3-tier tower rising out of the rear crown (py ~144-184); boosters (px 32/158) nacelles unchanged in style.
## Fenrir 3D v5
- HAND pods: whole side pods rolled 90 deg outward (left CCW, right CW seen from astern) - turret seat on the pod's outer face, barrels forward;
  the hand swivels on its neck (wrist) to aim, 60 deg forward arc. Tip pod forward 60. SLOTS: hands (26/164, 84) angle 0 arc 60.
- 4th gun: pod removed - turret sits directly on the core's armoured barbette on the crown (95,118), 300 arc; heat slits round the barbette.
- Tower removed: cyan VISOR bands (orange frames, mullions) - front (between the 3 front guns and the top gun) + each hull side.
- Diagonal jets removed: side boosters hang on SWIVEL HUBS and vector left/right when strafing (engine/sim note: rotate the booster deco + flame with lateral thrust).
## Fenrir 3D v6 - pods removed from the 3 front guns
- Tip gun = Medium Ballistic HARDPOINT in an armoured nose cowl (95, ~26), fixed forward.
- Side guns = turrets on flat armoured sponsons at the ends of short bolted arms from the flanks (~(33/157, 84)), arc 135 angled 20 deg outward (left +20, right -20) so they can still aim to the centreline.
- Core turret on the crown barbette unchanged (300 arc).
## Fenrir 3D v7
- Boosters: nacelles moved out/back (px 23/167, py 156-212); fixed pylon from hull to a swivel hub on each nacelle's inner flank (57 px out, py 184); vector +-14 deg; checked clear of hull + main drive at both extremes.
- Side guns = Tiamat/Hastur built-in mechanism mounted sideways: flank sponson lobe, fixed arm + outward collar, barrel cluster turns at the collar tip (pivot ~(14/176, 84)); arc 135 angled 20 out; inward extreme checked clear of the lobe.
- Hardpoint: gimbal ball in a widened muzzle port, 45 deg arc, pivot at the ball (no cowl clipping).
- Core turret: 360.
- SLOTS: HP MB (95,~28) a0 arc45; MB (14,84) a20 arc135; MB (176,84) a-20 arc135; MB (95,118) arc360.
## Fenrir 3D v8
- Side-gun sponson lobes REMOVED (user). Bolted root plate on the flank -> fixed arm -> outward collar (orange ring + end cap); gun head = round vertical hub + rotary barrels on a bracket at the collar FRONT (pivot ~(95+-(hx+32), 66) = (21/169, 66)).
- Arc check (top view, barrel cluster r 4.6): outward limit (87.5 deg) min clearance 3.7 px, inward limit (47.5 deg past centre) 7.5 px; hardpoint at +-22.5 deg stays 5.8 px inside the muzzle port; core turret 360 clears the crown.
- SLOTS: side MB (21,66) a+20 arc135 / (169,66) a-20 arc135.
## Fenrir 3D v9
- Side guns SHORT (user: no long stick): bolted socket plate + short collar on the flank, round gun hub on the collar end at (95+-(hx+9.5), 84) = (43/147, 84).
  Arc 60 straight ahead (+-30) - covers the hardpoint's +-22.5 so both can hit the same target. Clearance: inward limit 4.9 px from the hull, outward 10.9 px.
- PD moved OFF the boosters: 2 Small Ballistic sunk into the rear crown behind the top gun at (74/116, 162), ~200 deg arc covering the rear quarters (forward limit ~9 deg, clear of the barbette). Still a proposal.
- SLOTS: HP MB (95,~28) arc45; MB (43,84) a0 arc60; MB (147,84) a0 arc60; MB (95,118) arc360; PD SB (74,162) a108 arc200, (116,162) a-108 arc200.
- Fenrir v10: side guns get a rounded armoured POD CASING round the gun base (ellipsoid 11.5x10.5x13.5 fixed to the collar), open at the front +-62 deg with orange edge lips; barrels at the +-30 limits need <=58 deg -> clear.
## Fenrir 3D v11 - motion collision pass (automated: collision_check_3d.py samples every moving part across its arc and ray-tests vertices against static meshes)
- Side guns: collar slimmer (r 6-7, to hx+8), orange ring moved to the root; gun hub (r 6.5, h 12) at hx+21 -> pivot (31/159, 84); casing 13x13x15 with a +-72 deg front opening; casing seam band removed (it crossed the mouth). Result: 0 hits vs hull/collar/casing/lips across +-30.
- PD moved to x +-30 (off the orange stripe) on a short pedestal, arc 180 (+-90 around +-108): 0 hits.
- Boosters: hub r 4.5 fully outside the nacelle (nacelle px 19/171), pylon ends at the hub, rings shrunk: 0 hits at 0/+-14 deg (only the hinge pin in its bearing).
- Remaining contacts are by design only: hardpoint barrels in their gimbal ball, top turret in its ring seat, booster pin in its hub.
- SLOTS: side MB (31,84)/(159,84) arc60; PD (65,162)/(125,162) arc180.
FENRIR 3D APPROVED pending this pass.

## Hellhound 3D v1 (hellhound3d.html) - canvas 170x286, CX=85
- Palette: muted sage armour 0x7d8a7a (not flashy green), signal-blue band/trim 0x3a8fd8, red gun noses, blue glass.
- One lathe hull: nose block py 18-62, handle r34 py 62-178, flared faceted lamp head py 178-236 (ribs), grey armoured rim py 234-250, recessed lens drive (ENG 85,~252) with ring baffles.
- Sensor stick py -20..26; 2 Small Missile racks on stub wings AHEAD of the nose block (66/104, 6) arc 120 +-20 (slot moved from py 32 - old spot was inside the nose block).
- Blue gun band py 104-132: 3 Small Ballistic on top (63/85/107,118) + 3 exactly beneath (under-hull), 150 fwd; collision check: only turrets-in-pedestal contacts.
- No tower: visors on the handle (top/bridge + sides) at py 86. Core petal cover on the handle back (85,156). 2 diagonal jets on the flare flanks (22/148, 214).
## Hellhound 3D v2
- Gun band moved forward to py 72-100 (old visor spot); 6 Small Ballistic at (63/85/107, 86) top + beneath. Visors removed.
- Command tower (3 tiers, saddle base hugging the handle, blue visor) at the old band spot py ~100-136.
- Stick removed; sensor dome at the nose tip. 2 Small Missile racks on armoured side ledges at the tip: (43/127, 38) arc 120 +-20.
- Diagonal jets removed; main drive = lens + baffles + vanes on a GIMBAL (vertical pins in a gimbal ring inside the recessed well), sways +-6 deg when strafing.
  Check: nozzle max radius ~60.5 vs well inner 68 at +-6 deg -> clear; guns/missiles only touch their own pedestals.
- Hellhound v3: drive core cover removed (user); command tower lengthened to py ~102-170 (3 tiers, visor at the front, fire-control dome + mast).
- Hellhound v4: WHOLE lamp head (flare+rim+lens) is one drive block on a BALL JOINT (ball r26 at py 185) in an armoured socket collar on the handle end (py 176-185, blue seal ring, bolts); 2 hydraulic actuators (handle-flank brackets py 164 -> flare lugs at x+-57 py 201) re-aim live; swivels +-5.7 deg when strafing; min clearance flare-front vs socket ring ~2 px. Inner nozzle sway removed.
- Hellhound v5: lamp interior = real thruster: dark aft plate (r53-71), big bell nozzle (exit r52, throat r15 at 44 deep) with 36 cooling-tube ribs + white-hot throat, 8 vernier nozzles (r6.4) in the annulus. Flare now starts py 195; GANGWAY BELLOWS (train-connector accordion, 10 folds, blue end frames) cover the ball joint py 185-195 and bend with the swivel. Actuator lugs moved to py 214 (x+-63). Ball joint r20.
## 3D RULE (user, after Hellhound): every 3D block-out gets a THRUSTER FLIGHT PREVIEW - toggle/buttons for idle / forward / strafe L / strafe R / turn
   that light each thruster's flame by what it would do in that manoeuvre (and move any vectoring parts), so the engine flames can be checked in motion.

## Garm 3D v1 (garm3d.html) - canvas 200x250, CX=100
- Palette: muted ochre armour 0x9e7c4c, orange livery 0xe0782a, jade panels/glass 0x3f9a78, gunmetal rails, red gun eyes.
- Tall dome (100,98) 70 wide, 66 up; rear box py 138-214 hw 58 with jade side panels (EL); 3-tier tower on top where the EL green bump is; core petal cover on the box (100,202).
- 3 Small Ballistic terraced down the dome centreline (100, 50/80/110), superfiring, arc 120 (front one on a taller pedestal to clear the slope).
- Quad railgun (Large Ballistic, under-hull) in an armoured belly bay under the nose (100,~52), 4 rails + clamps, arc 10.
- Main drive (100,214+): grey ribbed collar + cooled bell nozzle. Side thruster pods (26/174, ~192) on swivel hubs: forward thrust, vector +-15 for strafe, differential for turns. No diagonal jets.
- FLIGHT PREVIEW buttons (Idle/Forward/Strafe L/R/Turn L/R) drive flames + pod vectoring (new 3D rule).
- Garm v2: core cover removed; tower lengthened (py ~151-209, fire-control dome, vents); quad railgun bay pulled back 18 px (bay centre py 76, barrel tips ~py 0; slot (100,70)).
- Garm v3: 2 Small Ballistic PD on the rear engine box near its rear corners (60/140, 203), facing back, arc 180. Railgun bay lowered 8 px (rails were clipping the dome belly after the pull-back). GARM 3D DONE.

## 2D pass after the 3D round (2026-09-28)
- New SS sprites drawn from the approved 3D: vs_abaddon7 (+apocalypse_ss_v2 module), vs_iris8, vs_selene4, vs_fenrir3, vs_hellhound3, vs_garm3 (slots json next to each).
  Garm pods pulled in to x 18/182 to fit the 200 px canvas (ENG [18,212],[182,212]).
- Artemis v12: rail PD now VP.sunk_mount (green outboard lip) instead of raised blisters.
- Hastur built-in twin-beam weapon sprite: weapons/tl_hastur_beam_turret_ss_v1.png (80x80, pivot centre, over-under barrels, tips 36 px ahead).
- Sheets: /mnt/user-data/outputs/TerraLight_2D/<Ship>.png (EL art | EL sprite | TL sprite) + _All_ships_overview.png.

## Mod v0.6.0 (build_v6.py + build_v6_part2.py, scripts in tl_java/) - user playtest fixes (2026-09-28)
- Flames sized to each nozzle (auto-measured), brighter styles; shields = 1.12x ship extent + 16 (incl. modules/moving parts).
- Under-hull slots: id "UH nnn", normal TURRET (refittable); hullmod tl_hull hides the sprites and redraws them on UNDER_SHIPS_LAYER.
- Hellhound: tower = module tl_hellhound_tower carrying the 3 under-band guns (click tower in refit); drive block drawn under the hull,
  swings +-6 deg with strafe/turn (engine flame angle follows). Fenrir boosters (+-14) / Garm pods (+-15) = decorative slots SW_L/SW_R.
- Hastur ball module: UNDER_PARENT. Iris v9: 2 rear-corner small ballistic PD.
- Siren: starts carrier (MAIN guns hidden + force no-fire), deco slot DECK plays closed/open/siloopen/deck/battleship frames with the system,
  battleship mode pauses fighter refit. AI: battleship when enemy < 900, carrier when > 1700, holds a mode >= 8 s.
- Neow: shield PHASE + defense tl_neow_flares (right-click, 8 SYSTEM tubes all round), system = damper; Armageddon reload 30 s.
- Tiamat triple cannon = BALLISTIC_AS_BEAM projectile volley. Abaddon Apocalypse = system script (brake, drift 2.6 s, burn to aim point,
  unstoppable, shoves + 1500 ram dmg, 15000 HE r420 at aim point). Duilius Claw Strike fires 8 claws from SYSTEM slots.
- Custom systems: Tiamat Triple Overcharge, Asura Rail Overdrive, Hastur Beam Lance, Hannibal AP Focus, Regulus Screen Overdrive,
  Selene Wing Rally, Fenrir Hit and Run, Hellhound Execution Salvo, Garm Assault Charge. Balance buffs in STATS.
- Scripts compile-checked against the 0.98a API source mirror (github jaghaimo/starsector-api) + stubs (scratchpad/jcheck.sh).

## Mod v0.7.0 (build_v7.py + build_v7_part2.py) - user revisions (2026-09-28)
- Abaddon: no shield (PHASE + defense tl_flare_screen = right-click flares, 8 tubes), hull 13000 / armour 1600. Apocalypse only as the
  F system (weapon hidden from codex). Sprites split (vs_abaddon8.py): hull_noshadow = frame + rails; boosters L/R + frame shadows drawn
  below the frame by TL_Hull; on launch boosters slide 24 px out (main flames cut, 6 retro jets brake), torpedo drifts out drawn under
  the frame, boosters close 3.4-4.2 s after launch. Torpedo: 12000 HP, takes half damage, shootable except when overlapping ships
  (then it shoves them); shot down = 3000 HE blast; script detonation at aim point 15000 HE r420.
- Duilius Claw Strike: 2 stored volleys, 1 rebuilt every 20 s; claw weapon hidden from codex.
- Garm system = vanilla Phase Skimmer (displacer). Hannibal AP Focus: +50% vs capitals (replaces armour pen).
- Hastur system = Replica Wing (TL_ReplicaWingStats: extra full wing per bay incl. module bays, 20 s).
- Regulus Screen Overdrive: + 50% vs destroyers, +25% vs frigates.

## Mod v0.8.0 (build_v8.py + build_v8_part2.py) - playtest 2 (2026-09-28)
- Weapon hiding: engine resets sprite alpha each frame -> under-hull/folded weapons now hidden by shrinking sprites to 0x0 (size restored
  only while TL_Hull draws them below the ships). Siren carrier mode also setForceDisabled on MAIN guns.
- Abaddon/Hellhound: refit sprite = full composite; combat swaps (ship.setSprite) to the bare hull (parts drawn by TL_Hull).
- Apocalypse: 30000 HP, armour-like reduction (1750); blast r1400, dmg 17000*(1-d/R)^2 HE bypassing shields, overload up to 10 s
  inside 0.6R, pushes ships, kills missiles/fighters in the fireball; friendly fire except the Abaddon.
- Regulus bubbles: DamageDealtModifier - x0.5 cruisers, x1 capitals, x2 destroyers/frigates/fighters/missiles.
- Selene bays: LARGE, 3 launch points each along the pod decks (py 140/170/200). Hellhound tower guns at (65/85/105, 108).
- Tiamat cannon arcs: front -10..150, rear 30..190. Shields 1.22x extent + 28. Armageddon reload 20 s.
- Hastur twin cannon = BALLISTIC_AS_BEAM projectile. Buffs: Tiamat, Asura, Hastur, Hannibal, Hellhound, Duilius speed 70.
- Standard variants: 2 S-mods (hardened shields + heavy armour; shieldless: heavy armour + reinforced bulkheads), hullmods by
  priority keeping half max vents in reserve, vents/caps to max, leftovers on extra mods. Custom stock weapons per ship (stock_for).

## TL unique detailing on the capitals (user: no visible drive core / internal connections)
- Tiamat v32 (vs_tiamat32.py) + Asura v11 (vs_asura11.py): same canvas/silhouette/livery/slots (slots json identical to v31/v10).
  Closed armour deck over the machinery base (engraved seams, no trenches); drive core + petal cover, power/data conduits, cables,
  capacitor cylinders, tanks, reload racks and casemate-well machinery removed -> notched armour blocks with sunk hatches, flush vents,
  hazard edges, livery stripes, stencils. Casemate wells/arms/collars and the Quad Railgun barbette unchanged.

## Mod v0.9.0 (build_v9.py + build_v9_part2.py) - playtest 3 (2026-09-28)
- setSprite swap (Abaddon/Hellhound) only in GameState.COMBAT and keeps the old sprite centre (refit ran the hullmod -> wrong sprite + offset).
- Every launch bay gets 3 launch points on the bay (a lone point launched from the ship centre). Hastur's hangar moved to the parent hull
  (1 bay, CARRIER hint, wing in parent variant) so the player controls the wing and Replica Wing uses it.
- Apocalypse: usable only with a locked target (isUsable), homes on it, detonates when the tip touches it; blast r2200, 30000*f^1.5,
  overload up to 15 s inside 0.7R.
- Duilius claws 2x size, 700 FRAG + 300 EMP, shield hits re-applied to hull (ClawBypass listener); bow guns at py 60, stock Gauss.
- Garm railgun slot py 52 (barrels show), dome smalls = Railgun attack group, rear = Vulcan PD. Asura quad railguns share a group.
- Hastur side cannons: front -10..150, rear 30..190 (like Tiamat). Flames 1.15x nozzle, x4.2 length, minimums; Hannibal 46 / Regulus 44 / Neow 50.
- Siren transform 3.5 s each way, eased gun scale, DECK/DECK2 cross-fade between deck frames.
- Tiamat v32 / Asura v11 sprites: closed TL armour, no exposed core/conduits.

## Mod v0.9.1 (build_v10.py + build_v10_part2.py) - playtest 4, user QA pass (2026-09-28)
- Released Apocalypse: own sprite shrunk to 0 (alpha is reset by the engine) and drawn below the Abaddon until its centre is
  APH/2+190 from the ship; flames dark while under. Screen-wide flash (GL quad, ABOVE_SHIPS_AND_MISSILES_LAYER, 0.9 s) on detonation.
  Blast stays friendly-fire except the Abaddon (user confirmed).
- Asura quad railguns 250/slug (both). Hastur: 2 bays (2 x Talon), twin cannon barrels offset +-4 (2 bolts side by side).
- Armageddon: 9 ammo, reloads 3 per 15 s.
- Dependencies: none (vanilla API only; no LazyLib/MagicLib/LunaLib/GraphicsLib/AshLib). Merged vanilla files: settings.json,
  engine_styles.json, independent.faction. User QA: "overall this passes".
