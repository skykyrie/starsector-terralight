package data.shipsystems.scripts;

import java.util.ArrayList;
import java.util.List;

import com.fs.starfarer.api.Global;
import com.fs.starfarer.api.combat.FighterLaunchBayAPI;
import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.impl.combat.BaseShipSystemScript;
import com.fs.starfarer.api.loading.FighterWingSpecAPI;

/**
 * Hastur - Replica Wing: every wing (the hangar is in the command module) instantly launches a full set of replica craft that
 * fight alongside the originals for the duration - a 2-fighter wing becomes 2 x 2.
 */
public class TL_ReplicaWingStats extends BaseShipSystemScript {
	public static final float DURATION = 20.0f;
	private boolean done = false;

	public void apply(MutableShipStatsAPI stats, String id, State state, float effectLevel) {
		if (done || effectLevel < 1f || !(stats.getEntity() instanceof ShipAPI)) return;
		done = true;
		ShipAPI ship = (ShipAPI) stats.getEntity();
		List bays = new ArrayList(ship.getLaunchBaysCopy());
		List mods = ship.getChildModulesCopy();
		for (int i = 0; i < mods.size(); i++) {
			ShipAPI m = (ShipAPI) mods.get(i);
			if (m.isAlive()) bays.addAll(m.getLaunchBaysCopy());
		}
		float minRate = Global.getSettings().getFloat("minFighterReplacementRate");
		for (int i = 0; i < bays.size(); i++) {
			FighterLaunchBayAPI bay = (FighterLaunchBayAPI) bays.get(i);
			if (bay.getWing() == null) continue;
			bay.setCurrRate(Math.max(minRate, bay.getCurrRate()));
			bay.makeCurrentIntervalFast();
			FighterWingSpecAPI spec = bay.getWing().getSpec();
			int add = spec.getNumFighters();
			int maxTotal = spec.getNumFighters() + add;
			int actual = maxTotal - bay.getWing().getWingMembers().size();
			if (actual > 0) {
				bay.setFastReplacements(bay.getFastReplacements() + add);
				bay.setExtraDeployments(actual);
				bay.setExtraDeploymentLimit(maxTotal);
				bay.setExtraDuration(DURATION);
			}
		}
	}

	public void unapply(MutableShipStatsAPI stats, String id) {
		done = false;
	}

	public StatusData getStatusData(int index, State state, float effectLevel) {
		if (index == 0) return new StatusData("replica wing launching", false);
		return null;
	}
}
