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

/** Launch the Apocalypse at a cruiser or capital 900-2800 away that is roughly ahead (it only has one). */
public class TL_ApocalypseAI implements ShipSystemAIScript {
	private ShipAPI ship;
	private ShipSystemAPI system;
	private CombatEngineAPI engine;
	private IntervalUtil tracker = new IntervalUtil(0.5f, 0.8f);

	public void init(ShipAPI ship, ShipSystemAPI system, ShipwideAIFlags flags, CombatEngineAPI engine) {
		this.ship = ship; this.system = system; this.engine = engine;
	}

	public void advance(float amount, Vector2f missileDangerDir, Vector2f collisionDangerDir, ShipAPI target) {
		tracker.advance(amount);
		if (!tracker.intervalElapsed() || !system.canBeActivated() || system.isActive()) return;
		ShipAPI t = target;
		if (t == null || !t.isAlive() || t.getOwner() == ship.getOwner() || !(t.isCapital() || t.isCruiser())) {
			t = null;
			List ships = engine.getShips();
			for (int i = 0; i < ships.size(); i++) {
				ShipAPI o = (ShipAPI) ships.get(i);
				if (!o.isAlive() || o.isHulk() || o.getOwner() == ship.getOwner() || o.getOwner() > 1) continue;
				if (!(o.isCapital() || o.isCruiser())) continue;
				if (t == null || o.isCapital() && !t.isCapital()) t = o;
			}
		}
		if (t == null) return;
		float d = Misc.getDistance(ship.getLocation(), t.getLocation());
		float off = Misc.getAngleDiff(ship.getFacing(), Misc.getAngleInDegrees(ship.getLocation(), t.getLocation()));
		boolean dying = ship.getHullLevel() < 0.35f;
		if ((d > 700f && d < 3000f && off < 45f) || (dying && d < 3000f)) {
			ship.setShipTarget(t);
			ship.useSystem();
		}
	}
}
