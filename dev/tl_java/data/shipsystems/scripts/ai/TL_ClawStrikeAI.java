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

/** Fire the claws at a warship inside ~1000 range, or at a pack of three or more fighters close by. */
public class TL_ClawStrikeAI implements ShipSystemAIScript {
	private ShipAPI ship;
	private ShipSystemAPI system;
	private CombatEngineAPI engine;
	private IntervalUtil tracker = new IntervalUtil(0.4f, 0.6f);

	public void init(ShipAPI ship, ShipSystemAPI system, ShipwideAIFlags flags, CombatEngineAPI engine) {
		this.ship = ship; this.system = system; this.engine = engine;
	}

	public void advance(float amount, Vector2f missileDangerDir, Vector2f collisionDangerDir, ShipAPI target) {
		tracker.advance(amount);
		if (!tracker.intervalElapsed() || !system.canBeActivated() || system.isActive()) return;
		if (target != null && target.isAlive() && !target.isFighter()
				&& Misc.getDistance(ship.getLocation(), target.getLocation()) - target.getCollisionRadius() < 1000f) {
			ship.useSystem();
			return;
		}
		int fighters = 0;
		List ships = engine.getShips();
		for (int i = 0; i < ships.size(); i++) {
			ShipAPI o = (ShipAPI) ships.get(i);
			if (o.isFighter() && o.isAlive() && o.getOwner() != ship.getOwner() && o.getOwner() <= 1
					&& Misc.getDistance(ship.getLocation(), o.getLocation()) < 700f) fighters++;
		}
		if (fighters >= 3) ship.useSystem();
	}
}
