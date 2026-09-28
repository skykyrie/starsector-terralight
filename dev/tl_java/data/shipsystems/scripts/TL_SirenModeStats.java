package data.shipsystems.scripts;

import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.impl.combat.BaseShipSystemScript;

/** Siren: Carrier <-> Battleship toggle. The effects live in the built-in hullmod tl_siren_modes, which reads this system's state. */
public class TL_SirenModeStats extends BaseShipSystemScript {
	public void apply(MutableShipStatsAPI stats, String id, State state, float effectLevel) {
	}
	public void unapply(MutableShipStatsAPI stats, String id) {
	}
	public StatusData getStatusData(int index, State state, float effectLevel) {
		if (state == State.IN) {
			if (index == 0) return new StatusData("deck converting - main guns rising", false);
			return null;
		}
		if (index == 0) return new StatusData("battleship mode: main guns deployed", false);
		if (index == 1) return new StatusData("fighter replacement paused", true);
		return null;
	}
}
