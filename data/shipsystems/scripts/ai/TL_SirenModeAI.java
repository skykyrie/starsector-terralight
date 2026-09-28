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

/** Siren AI: stay a carrier at range; raise the guns when an enemy warship closes in, fold them again once it is clear. */
public class TL_SirenModeAI implements ShipSystemAIScript {
	private ShipAPI ship;
	private ShipSystemAPI system;
	private CombatEngineAPI engine;
	private IntervalUtil tracker = new IntervalUtil(0.8f, 1.2f);
	private float held = 0f;

	public void init(ShipAPI ship, ShipSystemAPI system, ShipwideAIFlags flags, CombatEngineAPI engine) {
		this.ship = ship;
		this.system = system;
		this.engine = engine;
	}

	public void advance(float amount, Vector2f missileDangerDir, Vector2f collisionDangerDir, ShipAPI target) {
		held += amount;
		tracker.advance(amount);
		if (!tracker.intervalElapsed()) return;
		if (system.getCooldownRemaining() > 0 || system.isChargeup() || system.isChargedown()) return;
		if (held < 8f) return;                       // no flip-flopping: keep a mode for at least 8 s

		float nearest = 999999f;
		List ships = engine.getShips();
		for (int i = 0; i < ships.size(); i++) {
			ShipAPI o = (ShipAPI) ships.get(i);
			if (o == null || !o.isAlive() || o.isHulk() || o.isFighter() || o.getOwner() == ship.getOwner() || o.getOwner() > 1) continue;
			float d = Misc.getDistance(ship.getLocation(), o.getLocation()) - o.getCollisionRadius() - ship.getCollisionRadius();
			if (d < nearest) nearest = d;
		}
		boolean on = system.isOn();
		if (!on && nearest < 900f) { ship.useSystem(); held = 0f; }
		else if (on && nearest > 1700f) { ship.useSystem(); held = 0f; }
	}
}
