package data.shipsystems.scripts;

import java.util.List;

import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.combat.WeaponAPI;
import com.fs.starfarer.api.impl.combat.BaseShipSystemScript;

/** Hellhound - Execution Salvo: rapid fire that finishes damaged ships; missile racks reloaded on activation. */
public class TL_ExecutionStats extends BaseShipSystemScript {

	private boolean refilled = false;
	private void refill(MutableShipStatsAPI stats, String weaponType) {
		if (!(stats.getEntity() instanceof ShipAPI)) return;
		List ws = ((ShipAPI) stats.getEntity()).getAllWeapons();
		for (int i = 0; i < ws.size(); i++) {
			WeaponAPI w = (WeaponAPI) ws.get(i);
			if (w.usesAmmo() && w.getType().name().equals(weaponType)) w.setAmmo(w.getMaxAmmo());
		}
	}

	public void apply(MutableShipStatsAPI stats, String id, State state, float effectLevel) {
		float e = effectLevel;
		if (state == State.ACTIVE && !refilled) { refill(stats, "MISSILE"); refilled = true; }
		stats.getBallisticRoFMult().modifyMult(id, 1f + 1f * e);
		stats.getBallisticWeaponFluxCostMod().modifyMult(id, 1f - 0.5f * e);
		stats.getDamageToTargetHullMult().modifyPercent(id, 40f * e);
		stats.getDamageToTargetEnginesMult().modifyPercent(id, 50f * e);
	}

	public void unapply(MutableShipStatsAPI stats, String id) {
		refilled = false;
		stats.getBallisticRoFMult().unmodify(id);
		stats.getBallisticWeaponFluxCostMod().unmodify(id);
		stats.getDamageToTargetHullMult().unmodify(id);
		stats.getDamageToTargetEnginesMult().unmodify(id);
	}

	public StatusData getStatusData(int index, State state, float effectLevel) {
		if (index == 0) return new StatusData("ballistic rate of fire +100%", false);
		if (index == 1) return new StatusData("hull damage +40%", false);
		if (index == 2) return new StatusData("missile racks reloaded", false);
		return null;
	}
}
