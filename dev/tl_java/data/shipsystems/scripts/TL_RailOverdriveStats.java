package data.shipsystems.scripts;

import java.util.List;

import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.combat.WeaponAPI;
import com.fs.starfarer.api.impl.combat.BaseShipSystemScript;

/** Asura-II - Rail Overdrive: ballistic rate of fire doubled, half flux, faster slugs, cruiser-speed surge. */
public class TL_RailOverdriveStats extends BaseShipSystemScript {

	public void apply(MutableShipStatsAPI stats, String id, State state, float effectLevel) {
		float e = effectLevel;
		stats.getBallisticRoFMult().modifyMult(id, 1f + 1f * e);
		stats.getBallisticWeaponFluxCostMod().modifyMult(id, 1f - 0.5f * e);
		stats.getBallisticProjectileSpeedMult().modifyMult(id, 1f + 0.5f * e);
		stats.getMaxSpeed().modifyFlat(id, 30f * e);
		stats.getAcceleration().modifyPercent(id, 100f * e);
	}

	public void unapply(MutableShipStatsAPI stats, String id) {
		stats.getBallisticRoFMult().unmodify(id);
		stats.getBallisticWeaponFluxCostMod().unmodify(id);
		stats.getBallisticProjectileSpeedMult().unmodify(id);
		stats.getMaxSpeed().unmodify(id);
		stats.getAcceleration().unmodify(id);
	}

	public StatusData getStatusData(int index, State state, float effectLevel) {
		if (index == 0) return new StatusData("ballistic rate of fire +100%", false);
		if (index == 1) return new StatusData("ballistic flux cost -50%", false);
		if (index == 2) return new StatusData("top speed +30", false);
		return null;
	}
}
