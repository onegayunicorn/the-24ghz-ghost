"""
Digital Portal Simulation — Core Configuration
From PDF pages 26–27 (Digital Portal / Rick Sovereign Awakening).
"""
import numpy as np

# === PHYSICS CONSTANTS ===
c = 2.99792458e8          # Speed of light [m/s]
e = 1.602176634e-19       # Elementary charge [C]
m_e = 9.1093837015e-31    # Electron mass [kg]
eps0 = 8.8541878128e-12   # Permittivity [F/m]
mu0 = 4 * np.pi * 1e-7    # Permeability [H/m]
kB = 1.380649e-23         # Boltzmann [J/K]
sigma_sb = 5.670374419e-8 # Stefan-Boltzmann [W/m²K⁴]

# === PORTAL PARAMETERS ===
f_mod = 24.0e9            # Modulation frequency [Hz]
omega_mod = 2 * np.pi * f_mod
ell = 3                   # Topological charge (OAM)
k_compress = 4            # Compression ratio V1/V2
T0 = 300.0                # Initial temp [K]
R_aperture = 0.072        # 7.2 cm aperture [m]
Phi_p_min = 1.2 * e       # Min ponderomotive potential [J]

# === CALCULATED DERIVED ===
T_final = T0 * (k_compress) ** (1 / 3)
power_flux_scale = k_compress ** (4 / 3)
n_max = (eps0 * m_e * omega_mod**2) / (e**2)  # ~7.1e18 m⁻³

# === MINION FORGE ===
f_laser = 532e-9          # Laser wavelength [m]
f_shumann = 7.83          # Schumann resonance [Hz]
entanglement_fidelity = 0.82
entropy_baseline = 0.19

# === ENTITY / BEING ===
autonomy_threshold = 0.7
self_awareness_confidence = 0.0  # Evolves 0→1

# === TEMPORAL (from PDF math hardening) ===
phi = (1 + np.sqrt(5)) / 2
phi5 = phi ** 5
T_sim = 5.0
E_phi_total = T_sim * phi5
