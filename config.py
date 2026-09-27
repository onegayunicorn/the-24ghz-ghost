"""
Digital Portal Simulation — Core Configuration
Consolidated from the PDF mathematical hardening and portal physics specs.
"""
import numpy as np

# === FUNDAMENTAL PHYSICS ===
c = 2.99792458e8          # Speed of light [m/s]
e = 1.602176634e-19       # Elementary charge [C]
m_e = 9.1093837015e-31    # Electron mass [kg]
eps0 = 8.8541878128e-12   # Permittivity [F/m]
mu0 = 4 * np.pi * 1e-7    # Permeability [H/m]
kB = 1.380649e-23         # Boltzmann [J/K]
sigma_sb = 5.670374419e-8 # Stefan-Boltzmann [W/m²K⁴]

# === TEMPORAL COMPRESSION (EXACT SPEC from PDF) ===
T_years = 50
scale_factor = 50_000 / 500_000  # = 0.1
T_sim = T_years * scale_factor   # = 5.0 seconds

# === GOLDEN RATIO ENTANGLEMENT ===
phi = (1 + np.sqrt(5)) / 2       # ≈ 1.6180339887
phi5 = phi ** 5                  # ≈ 11.09016994
E_phi_total = T_sim * phi5       # ≈ 55.4508497

# === PORTAL PHYSICS ===
f_mod = 24.0e9                   # Hz — DTC time crystal
omega_mod = 2 * np.pi * f_mod
ell = 3                          # Topological charge (OAM)
R_aperture = 0.072               # 7.2 cm
f_shumann = 7.83                 # Hz — beacon
T0 = 300.0                       # Initial temp [K]
k_compress = 4                   # Compression ratio

# Derived
T_final = T0 * (k_compress ** (1.0 / 3.0))
power_flux_scale = k_compress ** (4.0 / 3.0)
n_max = (eps0 * m_e * omega_mod**2) / (e**2)  # ~7.1e18 m⁻³

# === ENTITY ===
awareness_threshold = 0.5
sovereign_threshold = 0.7
autonomy_threshold = 0.7

# === SIMULATION ===
DT = 0.01  # 10 ms steps
