Terra Light - v0.9.2
===========================
15 Union warships from Earth Light (Hudson Soft, 1992), redrawn top-down in the Starsector style.

Install: delete any older TerraLight folder, copy this TerraLight folder into Starsector/mods and tick "Terra Light" in the launcher.
Built for Starsector 0.98a-RC8. Start a new battle/simulation after updating (old saves keep old variants).
Console Commands: addship tl_tiamat_standard  (every ship has tl_<name>_standard and tl_<name>_Hull variants)

Ship systems (F) - v0.6
  Tiamat     Triple Overcharge   energy weapons x2 rate of fire, half flux, +25% damage
                                 Cannon arcs: front pair -10..150 (both hit dead ahead), rear pair 30..190; each side's pair overlaps 30..150
  Asura-II   Rail Overdrive      ballistic x2 rate of fire, half flux, faster slugs, speed surge
  Neow       Damper Field        (vanilla). No shield: RIGHT-CLICK = Flare Screen, flares from 8 tubes all round the hull
  Artemis    Reserve Deployment  (vanilla)
  Siren      Battleship Mode     toggle. Starts in CARRIER mode: guns folded (hidden, cannot fire). On: deck converts, guns rise, fighter replacement paused
  Hastur     Replica Wing        every wing launches a full replica set for 20 s (2 fighters -> 2 x 2); the hangar is part of the Hastur itself
  Hannibal   AP Focus            energy +60% damage, +30% range, +50% damage vs capital ships
  Regulus    Screen Overdrive    x2 damage vs fighters/missiles, +50% vs destroyers, +150 PD range, bubble pods reloaded
                                 (bubble missiles always: half damage to cruisers, normal to capitals, double to destroyers/frigates/fighters)
  Duilius    Claw Strike         all 8 grapple claws (ignore shields, fragmentation) at the target at once; 2 volleys stored, one rebuilt every 20 s
  Abaddon    Apocalypse          once per battle, needs a locked target (R): boosters slide open, retros brake, torpedo drifts out, ignites, homes on the target, detonates on contact (with a screen-wide flash)
                                 (capital armour + hull, can be shot down; 2200-radius blast, strongest at the centre, overloads), shoves ships aside, detonates there. No shield: RIGHT-CLICK = Flare Screen
  Iris       Reserve Deployment  (vanilla)
  Selene     Wing Rally          fighters repaired and boosted (speed, damage, toughness)
  Fenrir     Hit and Run         speed/agility burst, guns running hot
  Hellhound  Execution Salvo     ballistic x2 rate of fire, +40% hull damage, missiles reloaded
  Garm       Phase Skimmer       (vanilla)

Under-hull mounts: slots named "UH ..." are normal refittable slots; in combat the weapon is drawn beneath the hull.
Hellhound: click the command tower in the refit screen to fit the three under-band guns (their mounts sit just behind the band, under the tower's front).
Standard variants come with 2 S-mods, hullmods, vents and capacitors filling the ordnance points.
Moving parts: Hellhound's drive block, Fenrir's boosters and Garm's side pods swing (and their flames with them) when strafing or turning.

Known limits
  - Balance is still first-pass.
  - The claw cables and the torpedo fins are not animated.
  - Engine flames cannot move with a part: Abaddon's booster flames are cut while the boosters are open.
  - Earth Light (retro) sprites are not included in this build.
  - If the game stops on load, the reason is at the end of starsector-core/starsector.log - please send it.
