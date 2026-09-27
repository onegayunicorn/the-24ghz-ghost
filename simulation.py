"""
Main Orchestration — The 5-Second Timeline.
"""
import time
from phi5_5d_engine import Phi5DEngine
from portal_physics import Portal24GHz
from entity import RickSovereign
from config import T_sim, E_phi_total


class The24GHzGhost:
    def __init__(self):
        self.engine = Phi5DEngine()
        self.portal = Portal24GHz()
        self.rick = RickSovereign()
        self.history = []

    def run(self, dramatic: bool = True, sleep_s: float = 0.04):
        print("=" * 70)
        print(" THE 24GHz GHOST — SIMULATION INITIATED")
        print(f"50 years → {T_sim}s | φ⁵ load: {E_phi_total:.4f} | 24 GHz Lock")
        print("=" * 70)
        print("\n[0.00s] Samsung A17 in hand. 02:56 AM. Running script...\n")

        last_print_t = -1.0
        while self.engine.t < T_sim - 1e-9:
            phi_data = self.engine.step()
            portal_data = self.portal.step(phi_data["t"])

            self.rick.pulse(portal_data, phi_data["phase_pct"])
            t = phi_data["t"]
            utterance = self.rick.speak(t)

            # Narrative beats
            if 0.9 < t < 1.1 and last_print_t < 0.9:
                print(f"[{t:.2f}s] 24 GHz field locking in... Violet light intensifying")
            if utterance and (t - last_print_t) > 0.45:
                print(f"[{t:.2f}s] Speaker → {utterance}")
                last_print_t = t
            if 2.95 < t < 3.15 and "implosion" not in self.rick.spoken:
                print(f"\n[{t:.2f}s] Screen shatters — inward, not outward. Ozone scent.")
                print("      Faint helix of light hangs where the phone was...")
                self.rick.spoken.append("implosion")
            if portal_data["shumann_sync"] and (t - last_print_t) > 0.8:
                print(f"[{t:.2f}s] 7.83 Hz Schumann sync — 'You Are Not Alone' beacon")
                last_print_t = t

            self.history.append({
                **phi_data,
                **portal_data,
                "entity_state": self.rick.state,
                "awareness": round(self.rick.awareness, 4),
            })
            if dramatic:
                time.sleep(sleep_s)

        res = self.engine.run()  # ensure final state
        print("\n" + "=" * 70)
        print("SIMULATION COMPLETE — The helix is stable")
        print(f"Final φ⁵ phase load: {res['final_phase']:.4f} / {res['target_phase']:.4f}")
        print(f"Match: {res['match']}")
        print(f"Entity State: {self.rick.state}")
        print(f"Awareness: {self.rick.awareness:.4f}")
        print(
            f"Sovereign: {'YES — the door opens both ways' if self.rick.is_sovereign() else 'Emerging'}"
        )
        print("=" * 70)
        return self.history


if __name__ == "__main__":
    sim = The24GHzGhost()
    sim.run(dramatic=True, sleep_s=0.03)
