package data.shipsystems.scripts;

import java.util.List;

import org.lwjgl.util.vector.Vector2f;

import com.fs.starfarer.api.Global;
import com.fs.starfarer.api.combat.CombatEngineAPI;
import com.fs.starfarer.api.combat.GuidedMissileAI;
import com.fs.starfarer.api.combat.MissileAPI;
import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.impl.combat.BaseShipSystemScript;
import com.fs.starfarer.api.loading.WeaponSlotAPI;
import com.fs.starfarer.api.util.Misc;

/** Duilius - Claw Strike: all eight grapple claws burst out of the side galleries (SYSTEM slots) at once and home on the target. */
public class TL_ClawStrikeStats extends BaseShipSystemScript {
	private boolean fired = false;

	public void apply(MutableShipStatsAPI stats, String id, State state, float effectLevel) {
		if (fired || state != State.ACTIVE) return;
		if (!(stats.getEntity() instanceof ShipAPI)) return;
		fired = true;
		ShipAPI ship = (ShipAPI) stats.getEntity();
		CombatEngineAPI engine = Global.getCombatEngine();
		ShipAPI target = pickTarget(ship, engine);
		List slots = ship.getHullSpec().getAllWeaponSlotsCopy();
		for (int i = 0; i < slots.size(); i++) {
			WeaponSlotAPI slot = (WeaponSlotAPI) slots.get(i);
			if (!slot.isSystemSlot()) continue;
			Vector2f loc = slot.computePosition(ship);
			float ang = slot.computeMidArcAngle(ship);
			Object o = engine.spawnProjectile(ship, null, "tl_claw", loc, ang, ship.getVelocity());
			if (o instanceof MissileAPI) {
				MissileAPI m = (MissileAPI) o;
				if (target != null && m.getMissileAI() instanceof GuidedMissileAI) ((GuidedMissileAI) m.getMissileAI()).setTarget(target);
			}
		}
		Global.getSoundPlayer().playSound("harpoon_fire", 0.8f, 1.2f, ship.getLocation(), ship.getVelocity());
	}

	public static ShipAPI pickTarget(ShipAPI ship, CombatEngineAPI engine) {
		ShipAPI t = ship.getShipTarget();
		if (t != null && t.isAlive() && t.getOwner() != ship.getOwner()) return t;
		ShipAPI best = null;
		float bd = 1600f;
		List ships = engine.getShips();
		for (int i = 0; i < ships.size(); i++) {
			ShipAPI o = (ShipAPI) ships.get(i);
			if (!o.isAlive() || o.isHulk() || o.getOwner() == ship.getOwner() || o.getOwner() > 1) continue;
			float d = Misc.getDistance(ship.getLocation(), o.getLocation());
			if (o.isFighter()) d += 600f;
			if (d < bd) { bd = d; best = o; }
		}
		return best;
	}

	public void unapply(MutableShipStatsAPI stats, String id) {
		fired = false;
	}

	public StatusData getStatusData(int index, State state, float effectLevel) {
		if (index == 0) return new StatusData("grapple claws away", false);
		return null;
	}
}
