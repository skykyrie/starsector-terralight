package data.hullmods;

import java.util.List;

import com.fs.starfarer.api.combat.BaseHullMod;
import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.combat.ShipSystemAPI;
import com.fs.starfarer.api.combat.WeaponAPI;
import com.fs.starfarer.api.graphics.SpriteAPI;

/**
 * Siren convertible deck. The ship starts in CARRIER mode (system off):
 *   the three main guns (slots MAIN 1-3) are folded below the deck - hidden and unable to fire; fighters launch and refit normally.
 * Turning the system on plays the 5-step deck transform (decorative slot DECK: closed, open, silos open, deck, battleship)
 * and raises the guns. In BATTLESHIP mode the guns fire, fighters stay out and keep fighting, but their replacement timer is paused.
 */
public class TL_SirenModes extends BaseHullMod {
	public static final String KEY = "tl_siren_modes";

	public void advanceInCombat(ShipAPI ship, float amount) {
		if (ship == null) return;
		MutableShipStatsAPI stats = ship.getMutableStats();
		ShipSystemAPI sys = ship.getSystem();
		float e = 0f;
		boolean on = false;
		if (sys != null) {
			on = sys.isOn();
			e = sys.getEffectLevel();
			if (!on && !sys.isChargedown()) e = 0f;
		}
		boolean battle = on && e >= 1f;

		// guns rise during the second half of the transform
		float vis = (e - 0.4f) / 0.45f;
		if (vis < 0f) vis = 0f;
		if (vis > 1f) vis = 1f;
		vis = vis * vis * (3f - 2f * vis);                 // ease in/out: the guns glide up and down on their platforms
		float fp = e * 4f;                                 // deck frames 0..4, cross-faded between neighbours
		int frame = (int) Math.floor(fp);
		if (frame > 3) frame = 3;
		float frac = fp - frame;

		List weapons = ship.getAllWeapons();
		for (int i = 0; i < weapons.size(); i++) {
			WeaponAPI w = (WeaponAPI) weapons.get(i);
			if (w.getSlot() == null) continue;
			String sid = w.getSlot().getId();
			if (sid == null) continue;
			if (sid.startsWith("MAIN")) {
				// carrier mode: the gun is folded under the deck - disabled and not drawn; it grows back in as its platform rises
				w.setForceDisabled(!battle);
				if (!battle) {
					w.setForceNoFireOneFrame(true);
					if (w.isFiring()) w.stopFiring();
				}
				scale(ship, w.getSprite(), vis);
				scale(ship, w.getUnderSpriteAPI(), vis);
				scale(ship, w.getBarrelSpriteAPI(), vis);
				scale(ship, w.getGlowSpriteAPI(), battle ? 1f : 0f);
			} else if (sid.equals("DECK") && w.getAnimation() != null) {
				w.getAnimation().setFrame(frame);
				w.getAnimation().setAlphaMult(1f - frac);
			} else if (sid.equals("DECK2") && w.getAnimation() != null) {
				w.getAnimation().setFrame(Math.min(frame + 1, w.getAnimation().getNumFrames() - 1));
				w.getAnimation().setAlphaMult(frac);
			}
		}

		if (on) stats.getFighterRefitTimeMult().modifyMult(KEY, 100000f);
		else stats.getFighterRefitTimeMult().unmodify(KEY);
	}

	/** the engine resets weapon alpha every frame, so the folded guns are hidden by scaling their sprites (real size remembered) */
	private static void scale(ShipAPI ship, SpriteAPI s, float f) {
		if (s == null) return;
		String key = "tl_sz_" + System.identityHashCode(s);
		float[] wh = (float[]) ship.getCustomData().get(key);
		if (wh == null) { wh = new float[] {s.getWidth(), s.getHeight()}; ship.setCustomData(key, wh); }
		s.setSize(wh[0] * f, wh[1] * f);
	}

	public String getDescriptionParam(int index, ShipAPI.HullSize hullSize) {
		return null;
	}
}
