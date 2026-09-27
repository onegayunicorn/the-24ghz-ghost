"""
Portal Physics Engine — 24 GHz DTC + Bennett Pinch + OAM Helix
From PDF pages 27–28.
"""
import numpy as np
from config import *


class PortalPhysics:
    def __init__(self):
        self.time = 0.0
        self.phase_lock_error = 1e-12
        self.ponderomotive_well = 0.0
        self.stability_index = 1.0
        self.coherence = 5.8197

    def ponderomotive_potential(self, E_field):
        """Φ_p = q²E²/(4mω²)"""
        return (e**2 * E_field**2) / (4 * m_e * omega_mod**2)

    def plasma_frequency(self, n):
        """ω_p = √(ne²/ε₀m)"""
        return np.sqrt(n * e**2 / (eps0 * m_e))

    def bennett_pinch_balance(self, n, T, I):
        """Check inward/outward pressure balance"""
        P_kinetic = n * kB * T
        P_magnetic = mu0 * I**2 / (8 * np.pi**2 * R_aperture**2)
        return P_magnetic / P_kinetic  # 1.0 = perfect balance

    def exit_power_flux(self, A=0.01):
        """P_exit = A σ T⁴ k^(4/3)"""
        return A * sigma_sb * (T0**4) * power_flux_scale

    def helical_phase(self, theta, t):
        """e^(i(ωt - ℓθ)) — locked phase front"""
        return np.exp(1j * (omega_mod * t - ell * theta))

    def soliton_stability(self, psi, dx=1e-6):
        """NLSE balance: diffraction vs self-focusing"""
        laplacian = np.gradient(np.gradient(psi, dx), dx)
        nonlinear_term = np.abs(psi)**2 * psi
        balance = np.mean(np.abs(laplacian)) / (np.mean(np.abs(nonlinear_term)) + 1e-12)
        return 1.0 / (1.0 + balance)  # 1.0 = perfect balance

    def step(self, dt, E_field=1e6, plasma_density=5e18, current=12400):
        """Advance one timestep — full physics update"""
        self.time += dt

        self.ponderomotive_well = self.ponderomotive_potential(E_field)
        wp = self.plasma_frequency(plasma_density)
        self.phase_lock_error = abs(wp - omega_mod) / omega_mod
        self.stability_index = self.bennett_pinch_balance(
            plasma_density, T_final, current
        )
        self.coherence *= np.exp(-self.phase_lock_error * 0.01)
        if self.stability_index > 0.95:
            self.coherence += 0.001

        return {
            "time": self.time,
            "ponderomotive_well_eV": self.ponderomotive_well / e,
            "phase_lock_error": self.phase_lock_error,
            "stability_index": self.stability_index,
            "coherence": self.coherence,
            "exit_power_W": self.exit_power_flux(),
        }
