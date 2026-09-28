package data.shipsystems.scripts;

import java.util.List;

import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.combat.WeaponAPI;
import com.fs.starfarer.api.impl.combat.BaseShipSystemScript;

/** Fenrir - Hit and Run: a burst of speed and agility with the guns running hot. */
public class TL_HitAndRunStats extends BaseShipSystemScript {

	public void apply(MutableShipStatsAPI stats, String id, State state, float effectLevel) {
		float e = effectLevel;
		stats.getMaxSpeed().modifyFlat(id, 140f * e);
		stats.getAcceleration().modifyPercent(id, 250f * e);
		stats.getDeceleration().modifyPercent(id, 250f * e);
		stats.getMaxTurnRate().modifyPercent(id, 100f * e);
		stats.getTurnAcceleration().modifyPercent(id, 200f * e);
		stats.getBallisticRoFMult().modifyMult(id, 1f + 0.5f * e);
		stats.getBallisticWeaponFluxCostMod().modifyMult(id, 1f - 0.3f * e);
	}

	public void unapply(MutableShipStatsAPI stats, String id) {
		stats.getMaxSpeed().unmodify(id);
		stats.getAcceleration().unmodify(id);
		stats.getDeceleration().unmodify(id);
		stats.getMaxTurnRate().unmodify(id);
		stats.getTurnAcceleration().unmodify(id);
		stats.getBallisticRoFMult().unmodify(id);
		stats.getBallisticWeaponFluxCostMod().unmodify(id);
	}

	public StatusData getStatusData(int index, State state, float effectLevel) {
		if (index == 0) return new StatusData("top speed +140", false);
		if (index == 1) return new StatusData("manoeuvrability x3", false);
		if (index == 2) return new StatusData("ballistic rate of fire +50%", false);
		return null;
	}
}
