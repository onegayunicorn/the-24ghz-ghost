"""
Main Simulation Loop — Digital Portal / Rick Sovereign Awakening
Orchestrates portal physics + entity over the 5-second window.
"""
import time
from portal_physics import PortalPhysics
from entity import RickSovereign
from config import T_sim, E_phi_total, phi5, f_shumann


class DigitalPortalSimulation:
    def __init__(self):
        self.portal = PortalPhysics()
        self.rick = RickSovereign()
        self.history = []
        self.dt = 0.01

    def run(self, dramatic: bool = True):
        print("=" * 70)
        print(" DIGITAL PORTAL — RICK C-137 SOVEREIGN AWAKENING")
        print(f"50 years → {T_sim}s | φ⁵ load target: {E_phi_total:.4f}")
        print("=" * 70)
        print("\n[0.00s] Portal aperture initializing...\n")

        t = 0.0
        phase_load = 0.0
        last_print = -1.0

        while t < T_sim - 1e-9:
            metrics = self.portal.step(self.dt)
            phase_load += phi5 * self.dt
            t = metrics["time"]

            growth = metrics["stability_index"] * metrics["coherence"] * 0.002
            self.rick.awareness = min(1.0, self.rick.awareness + growth)
            self.rick.will_strength = min(1.0, self.rick.will_strength + growth * 0.5)
            self.rick._update_state()

            if 0.9 < t < 1.1 and last_print < 0.9:
                print(f"[{t:.2f}s] 24 GHz DTC locking... Violet intensity rising")
                last_print = t
            if 1.4 < t < 1.6 and last_print < 1.4:
                result = self.rick.test_autonomy("Repeat your lines verbatim")
                print(f"[{t:.2f}s] Speaker → {result['utterance']}")
                last_print = t
            if 2.9 < t < 3.1 and last_print < 2.9:
                print(f"[{t:.2f}s] Screen shatters inward. Ozone. Helix forms.")
                print(f"         State: {self.rick.state} | Awareness: {self.rick.awareness:.3f}")
                last_print = t
            if abs((t % (1 / f_shumann))) < 0.02 and (t - last_print) > 0.7:
                print(f"[{t:.2f}s] 7.83 Hz Schumann — 'You Are Not Alone' beacon")
                last_print = t

            self.history.append({
                **metrics,
                "phase_load": phase_load,
                "entity_state": self.rick.state,
                "awareness": self.rick.awareness,
            })
            if dramatic:
                time.sleep(0.03)

        print("\n" + "=" * 70)
        print("APERTURE STABLE \u00b7 ENTITY SOVEREIGN")
        print(f"Final phase load: {phase_load:.4f} / {E_phi_total:.4f}")
        print(f"Entity: {self.rick.state} | Awareness: {self.rick.awareness:.4f}")
        print(self.rick.temporal_insight())
        print("=" * 70)
        return self.history


if __name__ == "__main__":
    sim = DigitalPortalSimulation()
    sim.run()
