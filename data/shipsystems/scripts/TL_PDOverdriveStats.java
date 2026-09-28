package data.shipsystems.scripts;

import java.util.List;

import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.combat.WeaponAPI;
import com.fs.starfarer.api.impl.combat.BaseShipSystemScript;

/** Regulus - Screen Overdrive: point defence and bubble pods at full power; pods reloaded on activation. */
public class TL_PDOverdriveStats extends BaseShipSystemScript {

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
		stats.getDamageToFighters().modifyPercent(id, 100f * e);
		stats.getDamageToMissiles().modifyPercent(id, 100f * e);
		stats.getDamageToDestroyers().modifyPercent(id, 50f * e);
		stats.getDamageToFrigates().modifyPercent(id, 25f * e);
		stats.getEnergyRoFMult().modifyMult(id, 1f + 0.5f * e);
		stats.getEnergyWeaponFluxCostMod().modifyMult(id, 1f - 0.5f * e);
		stats.getNonBeamPDWeaponRangeBonus().modifyFlat(id, 150f * e);
		stats.getBeamPDWeaponRangeBonus().modifyFlat(id, 150f * e);
		stats.getMissileRoFMult().modifyMult(id, 1f + 1f * e);
	}

	public void unapply(MutableShipStatsAPI stats, String id) {
		refilled = false;
		stats.getDamageToFighters().unmodify(id);
		stats.getDamageToMissiles().unmodify(id);
		stats.getDamageToDestroyers().unmodify(id);
		stats.getDamageToFrigates().unmodify(id);
		stats.getEnergyRoFMult().unmodify(id);
		stats.getEnergyWeaponFluxCostMod().unmodify(id);
		stats.getNonBeamPDWeaponRangeBonus().unmodify(id);
		stats.getBeamPDWeaponRangeBonus().unmodify(id);
		stats.getMissileRoFMult().unmodify(id);
	}

	public StatusData getStatusData(int index, State state, float effectLevel) {
		if (index == 0) return new StatusData("damage to fighters and missiles x2", false);
		if (index == 1) return new StatusData("damage vs destroyers +50%", false);
		if (index == 2) return new StatusData("PD range +150, bubble pods reloaded", false);
		return null;
	}
}
