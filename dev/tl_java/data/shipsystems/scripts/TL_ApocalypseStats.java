package data.shipsystems.scripts;

import java.awt.Color;
import java.util.ArrayList;
import java.util.EnumSet;
import java.util.List;

import org.lwjgl.opengl.GL11;
import org.lwjgl.util.vector.Vector2f;

import com.fs.starfarer.api.Global;
import com.fs.starfarer.api.combat.CollisionClass;
import com.fs.starfarer.api.combat.CombatEngineAPI;
import com.fs.starfarer.api.combat.CombatEngineLayers;
import com.fs.starfarer.api.combat.CombatEntityAPI;
import com.fs.starfarer.api.combat.CombatLayeredRenderingPlugin;
import com.fs.starfarer.api.combat.ViewportAPI;
import com.fs.starfarer.api.graphics.SpriteAPI;
import com.fs.starfarer.api.combat.DamageType;
import com.fs.starfarer.api.combat.MissileAIPlugin;
import com.fs.starfarer.api.combat.MissileAPI;
import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.combat.ShipCommand;
import com.fs.starfarer.api.combat.ShipSystemAPI;
import com.fs.starfarer.api.combat.ShipEngineControllerAPI;
import com.fs.starfarer.api.impl.combat.BaseShipSystemScript;
import com.fs.starfarer.api.util.Misc;

/**
 * Abaddon - Apocalypse (once per battle).
 * Charge-up: clamps release, the Abaddon brakes hard (retro jets). Active: the docked torpedo slides out forward UNPOWERED,
 * drifts clear under the front frame, then ignites and bursts toward the point the ship was aiming at. It is heavily armoured
 * (takes half damage) with a huge hull and CAN be shot down; ships in its path are shoved aside and take ramming damage.
 * It only detonates at the aim point (or when its fuel runs out).
 */
public class TL_ApocalypseStats extends BaseShipSystemScript {
	public static final String LAUNCHED = "tl_apoc_launched";

	public void apply(MutableShipStatsAPI stats, String id, State state, float effectLevel) {
		float e = effectLevel;
		stats.getMaxSpeed().modifyMult(id, 1f - 0.85f * e);
		stats.getDeceleration().modifyPercent(id, 400f * e);
		stats.getMaxTurnRate().modifyMult(id, 1f - 0.5f * e);
		if (state != State.ACTIVE || !(stats.getEntity() instanceof ShipAPI)) return;
		ShipAPI ship = (ShipAPI) stats.getEntity();
		if (ship.getCustomData().get(LAUNCHED) != null) return;
		ship.setCustomData(LAUNCHED, Boolean.TRUE);
		launch(ship);
	}

	public void unapply(MutableShipStatsAPI stats, String id) {
		stats.getMaxSpeed().unmodify(id);
		stats.getDeceleration().unmodify(id);
		stats.getMaxTurnRate().unmodify(id);
	}

	/** it needs a locked target (R): the warhead homes on that ship and detonates when its tip reaches it */
	public boolean isUsable(ShipSystemAPI system, ShipAPI ship) {
		ShipAPI t = ship.getShipTarget();
		return t != null && t.isAlive() && !t.isHulk() && t.getOwner() != ship.getOwner();
	}

	public String getInfoText(ShipSystemAPI system, ShipAPI ship) {
		if (ship.getCustomData().get(LAUNCHED) != null) return null;
		if (!isUsable(system, ship)) return "NO TARGET";
		return "READY";
	}

	public StatusData getStatusData(int index, State state, float effectLevel) {
		if (index == 0) return new StatusData(state == State.IN ? "clamps releasing - braking" : "Apocalypse away", false);
		return null;
	}

	public static Vector2f aimPoint(ShipAPI ship) {
		CombatEngineAPI engine = Global.getCombatEngine();
		if (engine.getPlayerShip() == ship && ship.getShipAI() == null && ship.getMouseTarget() != null) return new Vector2f(ship.getMouseTarget());
		ShipAPI t = ship.getShipTarget();
		if (t == null || !t.isAlive() || t.getOwner() == ship.getOwner()) t = best(ship);
		if (t != null) return new Vector2f(t.getLocation());
		Vector2f p = Misc.getUnitVectorAtDegreeAngle(ship.getFacing());
		p.scale(2500f);
		return Vector2f.add(p, ship.getLocation(), p);
	}

	public static ShipAPI best(ShipAPI ship) {
		ShipAPI best = null;
		float score = 0f;
		List ships = Global.getCombatEngine().getShips();
		for (int i = 0; i < ships.size(); i++) {
			ShipAPI o = (ShipAPI) ships.get(i);
			if (!o.isAlive() || o.isHulk() || o.isFighter() || o.getOwner() == ship.getOwner() || o.getOwner() > 1) continue;
			float d = Misc.getDistance(ship.getLocation(), o.getLocation());
			if (d > 3000f) continue;
			float sc = (o.isCapital() ? 4f : o.isCruiser() ? 3f : o.isDestroyer() ? 1.5f : 1f) * (1f - d / 4000f);
			if (sc > score) { score = sc; best = o; }
		}
		return best;
	}

	private void launch(ShipAPI ship) {
		CombatEngineAPI engine = Global.getCombatEngine();
		float f = (float) Math.toRadians(ship.getFacing());
		float c = (float) Math.cos(f), s = (float) Math.sin(f);
		Vector2f loc = new Vector2f(ship.getLocation().x + %%AP_X%%f * c - %%AP_Y%%f * s, ship.getLocation().y + %%AP_X%%f * s + %%AP_Y%%f * c);
		Object o = engine.spawnProjectile(ship, null, "tl_apocalypse", loc, ship.getFacing(), ship.getVelocity());
		if (!(o instanceof MissileAPI)) return;
		MissileAPI m = (MissileAPI) o;
		m.setCollisionClass(CollisionClass.NONE);
		ship.setCustomData("tl_apoc_missile", m);
		ship.setCustomData("tl_apoc_under", Boolean.TRUE);
		Vector2f v = Misc.getUnitVectorAtDegreeAngle(ship.getFacing());
		v.scale(70f);
		m.getVelocity().set(ship.getVelocity().x + v.x, ship.getVelocity().y + v.y);
		m.setMissileAI(new ApocAI(m, ship, aimPoint(ship), ship.getShipTarget()));
		Global.getSoundPlayer().playSound("system_orion_device_explosion", 0.5f, 0.3f, loc, ship.getVelocity());
	}

	/** a brief white-green flash over the whole screen when the warhead goes off */
	public static class Flash implements CombatLayeredRenderingPlugin {
		private float t = 0f;
		public void init(CombatEntityAPI entity) {}
		public void cleanup() {}
		public boolean isExpired() { return t > %%FLASH_TIME%%f; }
		public void advance(float amount) {
			if (!Global.getCombatEngine().isPaused()) t += amount;
		}
		public EnumSet getActiveLayers() { return EnumSet.of(CombatEngineLayers.ABOVE_SHIPS_AND_MISSILES_LAYER); }
		public float getRenderRadius() { return 10000000f; }
		public void render(CombatEngineLayers layer, ViewportAPI v) {
			float a = t < 0.08f ? t / 0.08f : Math.max(0f, 1f - (t - 0.08f) / (%%FLASH_TIME%%f - 0.08f));
			a = a * a * 0.95f;
			if (a <= 0f) return;
			GL11.glPushAttrib(GL11.GL_ALL_ATTRIB_BITS);
			GL11.glDisable(GL11.GL_TEXTURE_2D);
			GL11.glEnable(GL11.GL_BLEND);
			GL11.glBlendFunc(GL11.GL_SRC_ALPHA, GL11.GL_ONE_MINUS_SRC_ALPHA);
			GL11.glColor4f(0.93f, 1f, 0.95f, a);
			float x = v.getLLX(), y = v.getLLY(), w = v.getVisibleWidth(), h = v.getVisibleHeight();
			GL11.glBegin(GL11.GL_QUADS);
			GL11.glVertex2f(x - 10f, y - 10f);
			GL11.glVertex2f(x + w + 10f, y - 10f);
			GL11.glVertex2f(x + w + 10f, y + h + 10f);
			GL11.glVertex2f(x - 10f, y + h + 10f);
			GL11.glEnd();
			GL11.glPopAttrib();
		}
	}

	/** drift -> ignite -> burn to the aim point, shove ships in the way, detonate */
	public static class ApocAI implements MissileAIPlugin {
		private MissileAPI m;
		private ShipAPI source;
		private Vector2f aim;
		private float t = 0f;
		private List hit = new ArrayList();
		private boolean done = false;
		private float lastHp = -1f;
		private float spriteW = -1f, spriteH = -1f;
		private boolean under = true;

		private ShipAPI target;

		public ApocAI(MissileAPI m, ShipAPI source, Vector2f aim, ShipAPI target) {
			this.m = m; this.source = source; this.aim = aim; this.target = target;
		}

		public void advance(float amount) {
			CombatEngineAPI engine = Global.getCombatEngine();
			if (done || engine.isPaused()) return;
			t += amount;
			// capital-grade armour: damage taken each frame is cut like a hit on %%AP_ARMOR%% armour (min 15% gets through)
			if (lastHp < 0f) lastHp = m.getHitpoints();
			if (m.getHitpoints() < lastHp) {
				float d = lastHp - m.getHitpoints();
				float taken = d * Math.max(0.15f, d / (d + %%AP_ARMOR%%f));
				lastHp = lastHp - taken;
				m.setHitpoints(lastHp);
			}
			lastHp = m.getHitpoints();
			// while it slides out under the Abaddon's frame, TL_Hull draws it below the hull; engine dark
			// stays drawn below the Abaddon until its tail has cleared the hull (not just until the drift ends)
			if (under && (Misc.getDistance(m.getLocation(), source.getLocation()) > %%AP_CLEAR%%f || !engine.isEntityInPlay(source))) {
				under = false;
				source.removeCustomData("tl_apoc_under");
			}
			// the engine resets missile alpha every frame, so while it is under the hull its own sprite is shrunk to nothing
			SpriteAPI sp = m.getSpriteAPI();
			if (sp != null) {
				if (spriteW < 0f) { spriteW = sp.getWidth(); spriteH = sp.getHeight(); }
				if (under) sp.setSize(0f, 0f); else sp.setSize(spriteW, spriteH);
			}
			if (under) {
				List fl = m.getEngineController().getShipEngines();
				for (int i = 0; i < fl.size(); i++)
					m.getEngineController().setFlameLevel(((ShipEngineControllerAPI.ShipEngineAPI) fl.get(i)).getEngineSlot(), 0f);
			}
			// shootable in open space; no hard collision near ships (it shoves them instead of detonating on contact)
			boolean nearShip = false;
			List all = engine.getShips();
			for (int i = 0; i < all.size(); i++) {
				ShipAPI o = (ShipAPI) all.get(i);
				if (o.isFighter() || !engine.isEntityInPlay(o)) continue;
				if (Misc.getDistance(o.getLocation(), m.getLocation()) < o.getCollisionRadius() + m.getCollisionRadius() + 60f) { nearShip = true; break; }
			}
			m.setCollisionClass(nearShip || under ? CollisionClass.NONE : CollisionClass.MISSILE_NO_FF);
			if (t < %%AP_DRIFT%%f) {                       // unpowered drift, clear of the Abaddon
				List es = m.getEngineController().getShipEngines();
				for (int i = 0; i < es.size(); i++)
					m.getEngineController().setFlameLevel(((ShipEngineControllerAPI.ShipEngineAPI) es.get(i)).getEngineSlot(), 0f);
				if (m.getVelocity().length() < 40f) {
					Vector2f v = Misc.getUnitVectorAtDegreeAngle(m.getFacing());
					v.scale(40f);
					m.getVelocity().set(v);
				}
				return;
			}
			if (target != null && target.isAlive() && engine.isEntityInPlay(target)) aim.set(target.getLocation());
			float want = Misc.getAngleInDegrees(m.getLocation(), aim);
			float diff = Misc.normalizeAngle(want - m.getFacing());
			if (diff > 180f) diff -= 360f;
			if (diff > 2f) m.giveCommand(ShipCommand.TURN_LEFT);
			else if (diff < -2f) m.giveCommand(ShipCommand.TURN_RIGHT);
			if (Math.abs(diff) < 60f) m.giveCommand(ShipCommand.ACCELERATE);

			// ram anything in the way (not the Abaddon itself)
			List ships = engine.getShips();
			for (int i = 0; i < ships.size(); i++) {
				ShipAPI o = (ShipAPI) ships.get(i);
				if (o == source || o == target || o.isHulk() || !o.isAlive() || hit.contains(o) || o.getParentStation() == source) continue;
				float d = Misc.getDistance(o.getLocation(), m.getLocation());
				if (d > o.getCollisionRadius() * 0.8f + 45f) continue;
				hit.add(o);
				Vector2f away = Vector2f.sub(o.getLocation(), m.getLocation(), new Vector2f());
				if (away.lengthSquared() < 1f) away.set(1f, 0f);
				away.normalise();
				float push = o.isFighter() ? 400f : Math.max(60f, 250f * 1500f / Math.max(300f, o.getMass()));
				away.scale(push);
				Vector2f.add(o.getVelocity(), away, o.getVelocity());
				engine.applyDamage(o, m.getLocation(), %%AP_RAM%%f, DamageType.KINETIC, 0f, false, false, source);
			}

			// detonate when the warhead's tip reaches the target (or its aim point if the target is gone / out of fuel)
			Vector2f tip = Misc.getUnitVectorAtDegreeAngle(m.getFacing());
			tip.scale(%%AP_HALF%%f);
			Vector2f.add(tip, m.getLocation(), tip);
			boolean hitTarget = target != null && target.isAlive() && engine.isEntityInPlay(target)
					&& Misc.getDistance(tip, target.getLocation()) < target.getCollisionRadius() * 0.85f;
			float dist = Misc.getDistance(tip, aim);
			if (hitTarget || dist < 60f || t > %%AP_FUEL%%f) detonate(engine);
		}

		/** planet-killer blast: damage and overload fall off from the centre to the edge of a huge radius */
		private void detonate(CombatEngineAPI engine) {
			done = true;
			source.removeCustomData("tl_apoc_under");
			Vector2f loc = new Vector2f(m.getLocation());
			float R = %%AP_RADIUS%%f;
			List all = new ArrayList(engine.getShips());
			for (int i = 0; i < all.size(); i++) {
				ShipAPI o = (ShipAPI) all.get(i);
				if (o == source || !engine.isEntityInPlay(o)) continue;
				float d = Math.max(0f, Misc.getDistance(o.getLocation(), loc) - o.getCollisionRadius() * 0.5f);
				if (d >= R) continue;
				float f = 1f - d / R;
				float dmg = %%AP_DMG%%f * f * (float) Math.sqrt(f);
				if (o.isFighter()) dmg = Math.max(dmg, 5000f);
				Vector2f dir = Vector2f.sub(loc, o.getLocation(), new Vector2f());
				if (dir.lengthSquared() > 1f) { dir.normalise(); dir.scale(o.getCollisionRadius() * 0.4f); }
				Vector2f hitAt = Vector2f.add(o.getLocation(), dir, new Vector2f());
				engine.applyDamage(o, hitAt, dmg, DamageType.HIGH_EXPLOSIVE, dmg * 0.25f, true, false, source);
				if (!o.isFighter() && o.getFluxTracker() != null && d < R * %%AP_OVERLOAD_FRAC%%f)
					o.getFluxTracker().forceOverload(%%AP_OVERLOAD_MAX%%f * (1f - d / (R * %%AP_OVERLOAD_FRAC%%f)));
				Vector2f push = Vector2f.sub(o.getLocation(), loc, new Vector2f());
				if (push.lengthSquared() > 1f) {
					push.normalise();
					push.scale(f * 300f * Math.min(1f, 1500f / Math.max(300f, o.getMass())));
					Vector2f.add(o.getVelocity(), push, o.getVelocity());
				}
			}
			// missiles caught in the fireball are destroyed
			List ms = new ArrayList(engine.getMissiles());
			for (int i = 0; i < ms.size(); i++) {
				MissileAPI x = (MissileAPI) ms.get(i);
				if (x != m && Misc.getDistance(x.getLocation(), loc) < R * 0.8f) engine.applyDamage(x, x.getLocation(), 100000f, DamageType.HIGH_EXPLOSIVE, 0f, true, false, source);
			}
			Color core = new Color(220, 255, 225, 255), mid = new Color(120, 255, 160, 255), rim = new Color(40, 200, 110, 255);
			engine.addHitParticle(loc, new Vector2f(), R * 2.2f, 1f, 0.4f, 2.5f, core);
			engine.spawnExplosion(loc, new Vector2f(), core, R * 0.5f, 2.5f);
			engine.spawnExplosion(loc, new Vector2f(), mid, R * 1.1f, 3.5f);
			engine.spawnExplosion(loc, new Vector2f(), rim, R * 1.8f, 4.5f);
			for (int k = 0; k < 90; k++) {
				float a = (float) (Math.random() * 360.0);
				float r = (float) (Math.random() * R * 0.9f);
				Vector2f p = Misc.getUnitVectorAtDegreeAngle(a);
				Vector2f v = new Vector2f(p);
				p.scale(r);
				Vector2f.add(p, loc, p);
				v.scale(80f + (float) Math.random() * 250f);
				engine.addHitParticle(p, v, 40f + (float) Math.random() * 90f, 1f, 1.5f + (float) Math.random() * 2f, k % 2 == 0 ? mid : rim);
			}
			Global.getSoundPlayer().playSound("system_orion_device_explosion", 0.6f, 2f, loc, new Vector2f());
			engine.addLayeredRenderingPlugin(new Flash());
			engine.removeEntity(m);
		}
	}
}
