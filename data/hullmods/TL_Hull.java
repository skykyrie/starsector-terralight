package data.hullmods;

import java.util.ArrayList;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.List;

import java.awt.Color;

import org.lwjgl.util.vector.Vector2f;

import com.fs.starfarer.api.GameState;
import com.fs.starfarer.api.Global;
import com.fs.starfarer.api.combat.BaseHullMod;
import com.fs.starfarer.api.combat.CombatEngineAPI;
import com.fs.starfarer.api.combat.CombatEngineLayers;
import com.fs.starfarer.api.combat.CombatEntityAPI;
import com.fs.starfarer.api.combat.CombatLayeredRenderingPlugin;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.combat.DamageAPI;
import com.fs.starfarer.api.combat.DamageType;
import com.fs.starfarer.api.combat.DamagingProjectileAPI;
import com.fs.starfarer.api.combat.MissileAPI;
import com.fs.starfarer.api.combat.listeners.DamageDealtModifier;
import com.fs.starfarer.api.combat.ShipEngineControllerAPI;
import com.fs.starfarer.api.combat.ShipSystemAPI;
import com.fs.starfarer.api.combat.ViewportAPI;
import com.fs.starfarer.api.combat.WeaponAPI;
import com.fs.starfarer.api.graphics.SpriteAPI;

/**
 * Terra Light hull features (built into every Terra Light hull and module).
 *  1. UNDER-HULL WEAPONS: any weapon in a slot whose id starts with "UH" is a normal, refittable slot, but in combat its
 *     sprites are hidden and redrawn on the layer below the ships, so the hull covers it and only the barrels peek out.
 *  2. VECTORING DRIVES: Hellhound's lamp-head drive block (drawn below the hull), Fenrir's boosters and Garm's side pods
 *     (decorative slots "SW_L"/"SW_R") swing when the ship strafes or turns, and their engine flames swing with them.
 *  3. ABADDON: the docked Apocalypse torpedo and the two side boosters are drawn below the front frame. When the Apocalypse
 *     system fires, the boosters slide 24 px outward on their rails (main flames cut, retro jets on the booster fronts brake the
 *     ship), the torpedo drifts out under the frame, and the boosters close again once it is clear.
 */
public class TL_Hull extends BaseHullMod {

	public static final String RKEY = "tl_hull_renderer";
	public static final String SWING = "tl_swing";
	public static final String APOC_LAUNCHED = "tl_apoc_launched";
	public static final String APOC_T0 = "tl_apoc_t0";
	public static final String APOC_MISSILE = "tl_apoc_missile";
	public static final String APOC_UNDER = "tl_apoc_under";
	public static final String BOOSTER = "tl_booster";
	public static final float RETRACT = 24.0f;
	public static final float[] RETRO_X = {154.0f, 153.5f, 154.0f, 154.0f, 153.5f, 154.0f};
	public static final float[] RETRO_Y = {91.0f, 80.0f, 69.0f, -91.0f, -80.0f, -69.0f};

	public void advanceInCombat(ShipAPI ship, float amount) {
		CombatEngineAPI engine = Global.getCombatEngine();
		if (engine == null || ship == null) return;

		Renderer r = (Renderer) engine.getCustomData().get(RKEY);
		if (r == null) {
			r = new Renderer();
			engine.getCustomData().put(RKEY, r);
			engine.addLayeredRenderingPlugin(r);
		}
		r.register(ship);

		List weapons = ship.getAllWeapons();
		for (int i = 0; i < weapons.size(); i++) {
			WeaponAPI w = (WeaponAPI) weapons.get(i);
			if (isUnder(w)) hide(w);
		}

		String hid = ship.getHullSpec().getHullId();
		if (ship.getCustomData().get("tl_init") == null) {
			ship.setCustomData("tl_init", Boolean.TRUE);
			// refit/codex show the whole ship; in combat the moving parts are drawn separately, so swap to the bare hull
			// (only in real combat - the refit screen also runs this hullmod, and must keep the full sprite)
			if (Global.getCurrentState() == GameState.COMBAT) {
				if (hid.equals("tl_abaddon")) swapSprite(ship, "abaddon_frame");
				if (hid.equals("tl_hellhound")) swapSprite(ship, "hellhound_hull");
			}
			if (hid.startsWith("tl_regulus")) ship.addListener(new BubbleVsSize());
			if (hid.startsWith("tl_duilius")) ship.addListener(new ClawBypass());
		}
		float max = 0f;
		if (hid.startsWith("tl_hellhound")) max = 6.0f;
		else if (hid.startsWith("tl_fenrir")) max = 14.0f;
		else if (hid.startsWith("tl_garm")) max = 15.0f;
		if (max > 0f && !engine.isPaused()) swing(ship, amount, max, hid.startsWith("tl_hellhound"));
		if (hid.startsWith("tl_abaddon")) abaddon(ship, engine);
	}

	private void abaddon(ShipAPI ship, CombatEngineAPI engine) {
		ShipSystemAPI sys = ship.getSystem();
		boolean launched = ship.getCustomData().get(APOC_LAUNCHED) != null;
		float now = engine.getTotalElapsedTime(false);
		float p = 0f, dt = 0f;
		if (!launched) {
			if (sys != null && sys.getEffectLevel() > 0f) p = sys.getEffectLevel();
		} else {
			Object t0 = ship.getCustomData().get(APOC_T0);
			if (t0 == null) { t0 = new Float(now); ship.setCustomData(APOC_T0, t0); }
			dt = now - ((Float) t0).floatValue();
			p = dt < 3.4f ? 1f : Math.max(0f, 1f - (dt - 3.4f) / 0.8f);
		}
		ship.setCustomData(BOOSTER, new Float(p));
		if (p <= 0.01f || engine.isPaused() || !ship.isAlive()) return;

		// boosters are open: main drives and diagonal jets (all on the boosters) are cut
		List engines = ship.getEngineController().getShipEngines();
		for (int i = 0; i < engines.size(); i++) {
			ShipEngineControllerAPI.ShipEngineAPI e = (ShipEngineControllerAPI.ShipEngineAPI) engines.get(i);
			ship.getEngineController().setFlameLevel(e.getEngineSlot(), 0f);
		}
		// retro jets on the booster fronts fire while the ship brakes
		if (!launched || dt < 2.5f) {
			Vector2f fwd = new Vector2f((float) Math.cos(Math.toRadians(ship.getFacing())), (float) Math.sin(Math.toRadians(ship.getFacing())));
			Color c = new Color(150, 255, 170, 255);
			for (int i = 0; i < RETRO_X.length; i++) {
				float side = RETRO_Y[i] > 0 ? 1f : -1f;
				Vector2f loc = Renderer.local(ship, RETRO_X[i], RETRO_Y[i] + side * RETRACT * p);
				Vector2f vel = new Vector2f(ship.getVelocity().x + fwd.x * 160f, ship.getVelocity().y + fwd.y * 160f);
				engine.addHitParticle(loc, vel, 12f + (float) Math.random() * 6f, 0.9f, 0.12f, c);
			}
		}
	}

	public static boolean isUnder(WeaponAPI w) {
		return w.getSlot() != null && w.getSlot().getId() != null && w.getSlot().getId().startsWith("UH");
	}

	/** The engine resets weapon sprite alpha every frame, so under-hull weapons are hidden by shrinking their sprites to 0 x 0
	 *  (the real size is remembered and restored only while TL_Hull draws them on the layer below the ships). */
	public static void hide(WeaponAPI w) {
		shrink(w.getSprite());
		shrink(w.getUnderSpriteAPI());
		shrink(w.getBarrelSpriteAPI());
		shrink(w.getGlowSpriteAPI());
	}

	public static Map sizes() {
		CombatEngineAPI engine = Global.getCombatEngine();
		Map m = (Map) engine.getCustomData().get("tl_sprite_sizes");
		if (m == null) { m = new HashMap(); engine.getCustomData().put("tl_sprite_sizes", m); }
		return m;
	}

	public static void shrink(SpriteAPI s) {
		if (s == null) return;
		Map m = sizes();
		if (!m.containsKey(s)) m.put(s, new float[] {s.getWidth(), s.getHeight()});
		s.setSize(0f, 0f);
	}

	public static void restore(SpriteAPI s) {
		if (s == null) return;
		float[] wh = (float[]) sizes().get(s);
		if (wh != null) s.setSize(wh[0], wh[1]);
	}

	/** swing angle follows strafe/turn input; +angle = counter-clockwise (exhaust swings to starboard = push to port) */
	private void swing(ShipAPI ship, float amount, float max, boolean allEngines) {
		ShipEngineControllerAPI ec = ship.getEngineController();
		float target = 0f;
		if (ec.isStrafingLeft()) target += max;
		if (ec.isStrafingRight()) target -= max;
		if (ec.isTurningLeft()) target -= max * 0.8f;
		if (ec.isTurningRight()) target += max * 0.8f;
		if (target > max) target = max;
		if (target < -max) target = -max;

		Object o = ship.getCustomData().get(SWING);
		float cur = o == null ? 0f : ((Float) o).floatValue();
		float step = max * 3f * amount;
		if (cur < target) cur = Math.min(target, cur + step);
		else if (cur > target) cur = Math.max(target, cur - step);
		ship.setCustomData(SWING, new Float(cur));

		// decorative booster/pod slots
		List weapons = ship.getAllWeapons();
		for (int i = 0; i < weapons.size(); i++) {
			WeaponAPI w = (WeaponAPI) weapons.get(i);
			if (w.getSlot() == null) continue;
			String sid = w.getSlot().getId();
			if ("SW_L".equals(sid) || "SW_R".equals(sid)) w.setCurrAngle(ship.getFacing() + cur);
		}
		// engine flames: all engines (Hellhound) or only the side engines (Fenrir / Garm pods)
		List engines = ec.getShipEngines();
		float f = (float) Math.toRadians(ship.getFacing());
		for (int i = 0; i < engines.size(); i++) {
			ShipEngineControllerAPI.ShipEngineAPI e = (ShipEngineControllerAPI.ShipEngineAPI) engines.get(i);
			if (!allEngines) {
				Vector2f d = Vector2f.sub(e.getLocation(), ship.getLocation(), new Vector2f());
				float localY = -d.x * (float) Math.sin(f) + d.y * (float) Math.cos(f);
				if (Math.abs(localY) < 30.0f) continue;
			}
			e.getEngineSlot().setAngle(180f + cur);
		}
	}

	public String getDescriptionParam(int index, ShipAPI.HullSize hullSize) {
		return null;
	}

	/** same canvas, same pivot: keep the old sprite's centre so the ship does not jump */
	private static void swapSprite(ShipAPI ship, String key) {
		SpriteAPI old = ship.getSpriteAPI();
		float cx = old.getCenterX(), cy = old.getCenterY();
		ship.setSprite("terralight", key);
		ship.getSpriteAPI().setCenter(cx, cy);
	}

	/** Duilius grapple claws ignore shields: a claw that hits a shield is re-applied to the hull behind it as fragmentation damage */
	public static class ClawBypass implements DamageDealtModifier {
		public String modifyDamageDealt(Object param, CombatEntityAPI target, DamageAPI damage, Vector2f point, boolean shieldHit) {
			if (!(param instanceof DamagingProjectileAPI)) return null;
			DamagingProjectileAPI p = (DamagingProjectileAPI) param;
			if (p.getProjectileSpecId() == null || !p.getProjectileSpecId().equals("tl_claw_proj")) return null;
			if (!shieldHit || !(target instanceof ShipAPI)) return null;
			ShipAPI t = (ShipAPI) target;
			Vector2f dir = Vector2f.sub(t.getLocation(), point, new Vector2f());
			if (dir.lengthSquared() > 1f) { dir.normalise(); dir.scale(Math.min(60f, t.getCollisionRadius() * 0.4f)); }
			Vector2f hullPoint = Vector2f.add(point, dir, new Vector2f());
			Global.getCombatEngine().applyDamage(t, hullPoint, damage.getDamage(), DamageType.FRAGMENTATION, 300f,
					true, false, p.getSource());
			damage.getModifier().modifyMult("tl_claw_bypass", 0f);
			return "tl_claw_bypass";
		}
	}

	/** Regulus bubble missiles: half damage to cruisers, normal to capitals, double to destroyers, frigates, fighters and missiles */
	public static class BubbleVsSize implements DamageDealtModifier {
		public String modifyDamageDealt(Object param, CombatEntityAPI target, DamageAPI damage, Vector2f point, boolean shieldHit) {
			if (!(param instanceof DamagingProjectileAPI)) return null;
			String pid = ((DamagingProjectileAPI) param).getProjectileSpecId();
			if (pid == null || !pid.equals("tl_bubble_warhead")) return null;
			float m = 1f;
			if (target instanceof ShipAPI) {
				ShipAPI t = (ShipAPI) target;
				if (t.isFighter() || t.isFrigate() || t.isDestroyer()) m = 2f;
				else if (t.isCruiser()) m = 0.5f;
			} else if (target instanceof MissileAPI) m = 2f;
			if (m == 1f) return null;
			damage.getModifier().modifyMult("tl_bubble_vs_size", m);
			return "tl_bubble_vs_size";
		}
	}

	/** one per combat: draws under-hull weapons, the Hellhound drive block and the docked Apocalypse below all ships */
	public static class Renderer implements CombatLayeredRenderingPlugin {
		private List ships = new ArrayList();
		private SpriteAPI hhDrive;
		private SpriteAPI apoc, boosterL, boosterR, shadowRest, shadowOpen;

		public void register(ShipAPI ship) {
			if (!ships.contains(ship)) ships.add(ship);
		}

		public void init(CombatEntityAPI entity) {}
		public void cleanup() {}
		public boolean isExpired() { return false; }
		public void advance(float amount) {}
		public float getRenderRadius() { return 1000000f; }

		public EnumSet getActiveLayers() {
			return EnumSet.of(CombatEngineLayers.UNDER_SHIPS_LAYER);
		}

		public static Vector2f local(ShipAPI ship, float x, float y) {
			float f = (float) Math.toRadians(ship.getFacing());
			float c = (float) Math.cos(f), s = (float) Math.sin(f);
			return new Vector2f(ship.getLocation().x + x * c - y * s, ship.getLocation().y + x * s + y * c);
		}

		public void render(CombatEngineLayers layer, ViewportAPI viewport) {
			CombatEngineAPI engine = Global.getCombatEngine();
			if (engine == null) return;
			for (int i = ships.size() - 1; i >= 0; i--) {
				ShipAPI ship = (ShipAPI) ships.get(i);
				if (!engine.isEntityInPlay(ship)) { ships.remove(i); continue; }
				float alpha = ship.getCombinedAlphaMult();
				if (alpha <= 0f) continue;
				if (!viewport.isNearViewport(ship.getLocation(), ship.getCollisionRadius() + 200f)) continue;
				String hid = ship.getHullSpec().getHullId();

				if (hid.startsWith("tl_hellhound") && ship.getParentStation() == null) {
					if (hhDrive == null) hhDrive = Global.getSettings().getSprite("terralight", "hellhound_drive");
					Object o = ship.getCustomData().get(SWING);
					float cur = o == null ? 0f : ((Float) o).floatValue();
					Vector2f p = local(ship, -42.0f, 0.0f);
					hhDrive.setAngle(ship.getFacing() - 90f + cur);
					hhDrive.setAlphaMult(alpha);
					hhDrive.renderAtCenter(p.x, p.y);
				}
				if (hid.startsWith("tl_abaddon")) {
					if (apoc == null) {
						apoc = Global.getSettings().getSprite("terralight", "apocalypse_docked");
						boosterL = Global.getSettings().getSprite("terralight", "abaddon_boosterL");
						boosterR = Global.getSettings().getSprite("terralight", "abaddon_boosterR");
						shadowRest = Global.getSettings().getSprite("terralight", "abaddon_shadow_rest");
						shadowOpen = Global.getSettings().getSprite("terralight", "abaddon_shadow_open");
					}
					float ang = ship.getFacing() - 90f;
					Object o = ship.getCustomData().get(BOOSTER);
					float p = o == null ? 0f : ((Float) o).floatValue();
					if (ship.getCustomData().get(APOC_LAUNCHED) == null && !ship.isHulk()) {
						Vector2f d = local(ship, 9.5f, 0.0f);
						draw1(apoc, d, ang, alpha);
					} else if (ship.getCustomData().get(APOC_UNDER) != null) {
						MissileAPI m = (MissileAPI) ship.getCustomData().get(APOC_MISSILE);
						if (m != null && engine.isEntityInPlay(m)) draw1(apoc, m.getLocation(), m.getFacing() - 90f, alpha);
					}
					draw1(boosterL, local(ship, 0f, RETRACT * p), ang, alpha);
					draw1(boosterR, local(ship, 0f, -RETRACT * p), ang, alpha);
					draw1(shadowRest, ship.getLocation(), ang, alpha * (1f - p));
					if (p > 0f) draw1(shadowOpen, ship.getLocation(), ang, alpha * p);
				}

				List weapons = ship.getAllWeapons();
				for (int j = 0; j < weapons.size(); j++) {
					WeaponAPI w = (WeaponAPI) weapons.get(j);
					if (!isUnder(w)) continue;
					Vector2f loc = w.getLocation();
					float ang = w.getCurrAngle() - 90f;
					draw(w.getUnderSpriteAPI(), loc, ang, alpha);
					draw(w.getSprite(), loc, ang, alpha);
					SpriteAPI b = w.getBarrelSpriteAPI();
					if (b != null) {
						restore(b);
						b.setAngle(ang);
						w.renderBarrel(b, loc, alpha);
						b.setSize(0f, 0f);
					}
				}
			}
		}

		private static void draw1(SpriteAPI s, Vector2f loc, float ang, float alpha) {
			if (s == null) return;
			s.setAngle(ang);
			s.setAlphaMult(alpha);
			s.renderAtCenter(loc.x, loc.y);
		}

		private static void draw(SpriteAPI s, Vector2f loc, float ang, float alpha) {
			if (s == null) return;
			restore(s);
			s.setAngle(ang);
			s.setAlphaMult(alpha);
			s.renderAtCenter(loc.x, loc.y);
			s.setSize(0f, 0f);
		}
	}
}
