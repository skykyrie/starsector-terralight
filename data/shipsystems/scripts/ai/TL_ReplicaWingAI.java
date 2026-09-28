package data.shipsystems.scripts.ai;

import java.util.List;

import org.lwjgl.util.vector.Vector2f;

import com.fs.starfarer.api.combat.CombatEngineAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.combat.ShipSystemAIScript;
import com.fs.starfarer.api.combat.ShipSystemAPI;
import com.fs.starfarer.api.combat.ShipwideAIFlags;
import com.fs.starfarer.api.util.IntervalUtil;
import com.fs.starfarer.api.util.Misc;

/** Launch the replica wing when the Hastur's fighters are out and enemies are within ~2500. */
public class TL_ReplicaWingAI implements ShipSystemAIScript {
	private ShipAPI ship;
	private ShipSystemAPI system;
	private CombatEngineAPI engine;
	private IntervalUtil tracker = new IntervalUtil(0.8f, 1.2f);

	public void init(ShipAPI ship, ShipSystemAPI system, ShipwideAIFlags flags, CombatEngineAPI engine) {
		this.ship = ship; this.system = system; this.engine = engine;
	}

	public void advance(float amount, Vector2f missileDangerDir, Vector2f collisionDangerDir, ShipAPI target) {
		tracker.advance(amount);
		if (!tracker.intervalElapsed() || !system.canBeActivated() || system.isActive()) return;
		boolean hasBay = !ship.getLaunchBaysCopy().isEmpty();
		List mods = ship.getChildModulesCopy();
		for (int i = 0; i < mods.size(); i++) {
			ShipAPI m = (ShipAPI) mods.get(i);
			if (m.isAlive() && !m.getLaunchBaysCopy().isEmpty()) hasBay = true;
		}
		if (!hasBay) return;
		List ships = engine.getShips();
		for (int i = 0; i < ships.size(); i++) {
			ShipAPI o = (ShipAPI) ships.get(i);
			if (!o.isAlive() || o.isHulk() || o.isFighter() || o.getOwner() == ship.getOwner() || o.getOwner() > 1) continue;
			if (Misc.getDistance(ship.getLocation(), o.getLocation()) < 2500f) { ship.useSystem(); return; }
		}
	}
}
