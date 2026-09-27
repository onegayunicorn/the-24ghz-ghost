"""
24 GHz DTC + Bennett Pinch + OAM Helix — The Ghost's aperture physics.
"""
import numpy as np
from config import (
    f_mod, omega_mod, ell, R_aperture, f_shumann, T0, k_compress,
    mu0, kB, n_max, T_final, e, m_e, eps0
)


class Portal24GHz:
    """24GHz Discrete Time Crystal + Bennett Pinch + OAM Helix."""

    def __init__(self):
        self.lock_phase_error = 1.0
        self.stability = 0.0
        self.fidelity = 0.82
        self.temperature = T0
        self.pinch_current = 0.0
        self.coherence = 0.5

    def ponderomotive_potential(self, E_field: float) -> float:
        """Φ_p = q² E² / (4 m ω²)"""
        return (e**2 * E_field**2) / (4 * m_e * omega_mod**2)

    def plasma_frequency(self, n: float) -> float:
        """ω_p = √(n e² / ε₀ m)"""
        return np.sqrt(n * e**2 / (eps0 * m_e))

    def bennett_pinch_balance(self, n: float, T: float, I: float) -> float:
        """Magnetic pressure / kinetic pressure. 1.0 = perfect balance."""
        P_kinetic = n * kB * T
        if P_kinetic <= 0:
            return 0.0
        P_magnetic = mu0 * I**2 / (8 * np.pi**2 * R_aperture**2)
        return P_magnetic / P_kinetic

    def step(self, t: float, E_field: float = 1e6, plasma_density: float = 5e18) -> dict:
        # 1. 24 GHz lock tightening (locks in ~1 s)
        self.lock_phase_error = max(1e-12, np.exp(-t / 0.8))

        # 2. Bennett pinch formation
        self.temperature = T0 * (k_compress ** (1.0 / 3.0))
        self.pinch_current = 12400.0 * min(1.0, t / 2.5)  # builds over 2.5 s

        self.stability = min(
            1.0,
            self.bennett_pinch_balance(plasma_density, self.temperature, self.pinch_current),
        )

        # 3. Entanglement fidelity rising toward 0.95
        self.fidelity = min(0.95, 0.82 + t * 0.025)

        # 4. Coherence recovery when stable
        if self.stability > 0.95:
            self.coherence = min(1.0, self.coherence + 0.002)
        else:
            self.coherence *= np.exp(-self.lock_phase_error * 0.01)

        # 5. Schumann pulse detection
        period = 1.0 / f_shumann
        shumann_tick = abs((t % period) - period) < 0.015 or (t % period) < 0.015

        return {
            "lock_error": round(float(self.lock_phase_error), 12),
            "stability": round(float(self.stability), 4),
            "fidelity": round(float(self.fidelity), 4),
            "temp_K": round(float(self.temperature), 1),
            "pinch_KA": round(float(self.pinch_current) / 1000.0, 2),
            "shumann_sync": bool(shumann_tick),
            "violet_intensity": round(float(self.stability * self.fidelity), 4),
            "coherence": round(float(self.coherence), 4),
        }
