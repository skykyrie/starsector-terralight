package data.shipsystems.scripts;

import java.util.List;

import com.fs.starfarer.api.combat.FighterWingAPI;
import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.impl.combat.BaseShipSystemScript;

/** Selene - Wing Rally: its fighters are patched up and surge (speed, damage, toughness); the Selene itself sprints. */
public class TL_WingRallyStats extends BaseShipSystemScript {
	private boolean healed = false;

	public void apply(MutableShipStatsAPI stats, String id, State state, float effectLevel) {
		float e = effectLevel;
		stats.getMaxSpeed().modifyFlat(id, 50f * e);
		stats.getAcceleration().modifyPercent(id, 100f * e);
		if (!(stats.getEntity() instanceof ShipAPI)) return;
		ShipAPI ship = (ShipAPI) stats.getEntity();
		List wings = ship.getAllWings();
		for (int i = 0; i < wings.size(); i++) {
			FighterWingAPI wing = (FighterWingAPI) wings.get(i);
			List members = wing.getWingMembers();
			for (int j = 0; j < members.size(); j++) {
				ShipAPI f = (ShipAPI) members.get(j);
				MutableShipStatsAPI fs = f.getMutableStats();
				fs.getMaxSpeed().modifyPercent(id, 50f * e);
				fs.getAcceleration().modifyPercent(id, 100f * e);
				fs.getBallisticWeaponDamageMult().modifyPercent(id, 50f * e);
				fs.getEnergyWeaponDamageMult().modifyPercent(id, 50f * e);
				fs.getMissileWeaponDamageMult().modifyPercent(id, 50f * e);
				fs.getHullDamageTakenMult().modifyMult(id, 1f - 0.4f * e);
				fs.getArmorDamageTakenMult().modifyMult(id, 1f - 0.4f * e);
				if (state == State.ACTIVE && !healed) {
					f.setHitpoints(Math.min(f.getMaxHitpoints(), f.getHitpoints() + 0.5f * f.getMaxHitpoints()));
				}
			}
		}
		if (state == State.ACTIVE) healed = true;
	}

	public void unapply(MutableShipStatsAPI stats, String id) {
		healed = false;
		stats.getMaxSpeed().unmodify(id);
		stats.getAcceleration().unmodify(id);
		if (!(stats.getEntity() instanceof ShipAPI)) return;
		ShipAPI ship = (ShipAPI) stats.getEntity();
		List wings = ship.getAllWings();
		for (int i = 0; i < wings.size(); i++) {
			List members = ((FighterWingAPI) wings.get(i)).getWingMembers();
			for (int j = 0; j < members.size(); j++) {
				MutableShipStatsAPI fs = ((ShipAPI) members.get(j)).getMutableStats();
				fs.getMaxSpeed().unmodify(id);
				fs.getAcceleration().unmodify(id);
				fs.getBallisticWeaponDamageMult().unmodify(id);
				fs.getEnergyWeaponDamageMult().unmodify(id);
				fs.getMissileWeaponDamageMult().unmodify(id);
				fs.getHullDamageTakenMult().unmodify(id);
				fs.getArmorDamageTakenMult().unmodify(id);
			}
		}
	}

	public StatusData getStatusData(int index, State state, float effectLevel) {
		if (index == 0) return new StatusData("fighters: speed +50%, damage +50%, damage taken -40%", false);
		if (index == 1) return new StatusData("fighters repaired", false);
		return null;
	}
}
