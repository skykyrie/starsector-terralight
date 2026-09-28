package data.shipsystems.scripts;

import java.util.List;

import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.combat.WeaponAPI;
import com.fs.starfarer.api.impl.combat.BaseShipSystemScript;

/** Tiamat - Triple Overcharge: energy weapons fire twice as fast for less flux and hit harder. */
public class TL_TripleOverchargeStats extends BaseShipSystemScript {

	public void apply(MutableShipStatsAPI stats, String id, State state, float effectLevel) {
		float e = effectLevel;
		stats.getEnergyRoFMult().modifyMult(id, 1f + 1f * e);
		stats.getEnergyWeaponFluxCostMod().modifyMult(id, 1f - 0.5f * e);
		stats.getEnergyWeaponDamageMult().modifyPercent(id, 25f * e);
	}

	public void unapply(MutableShipStatsAPI stats, String id) {
		stats.getEnergyRoFMult().unmodify(id);
		stats.getEnergyWeaponFluxCostMod().unmodify(id);
		stats.getEnergyWeaponDamageMult().unmodify(id);
	}

	public StatusData getStatusData(int index, State state, float effectLevel) {
		if (index == 0) return new StatusData("energy rate of fire +100%", false);
		if (index == 1) return new StatusData("energy flux cost -50%", false);
		if (index == 2) return new StatusData("energy damage +25%", false);
		return null;
	}
}
