package data.shipsystems.scripts;

import java.util.List;

import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.combat.WeaponAPI;
import com.fs.starfarer.api.impl.combat.BaseShipSystemScript;

/** Hannibal - AP Focus: capital-killer focus for the forward energy battery. */
public class TL_APFocusStats extends BaseShipSystemScript {

	public void apply(MutableShipStatsAPI stats, String id, State state, float effectLevel) {
		float e = effectLevel;
		stats.getEnergyWeaponDamageMult().modifyPercent(id, 60f * e);
		stats.getEnergyWeaponRangeBonus().modifyPercent(id, 30f * e);
		stats.getEnergyWeaponFluxCostMod().modifyMult(id, 1f - 0.4f * e);
		stats.getDamageToCapital().modifyPercent(id, 50f * e);
	}

	public void unapply(MutableShipStatsAPI stats, String id) {
		stats.getEnergyWeaponDamageMult().unmodify(id);
		stats.getEnergyWeaponRangeBonus().unmodify(id);
		stats.getEnergyWeaponFluxCostMod().unmodify(id);
		stats.getDamageToCapital().unmodify(id);
	}

	public StatusData getStatusData(int index, State state, float effectLevel) {
		if (index == 0) return new StatusData("energy damage +60%", false);
		if (index == 1) return new StatusData("energy range +30%", false);
		if (index == 2) return new StatusData("damage vs capital ships +50%", false);
		return null;
	}
}
