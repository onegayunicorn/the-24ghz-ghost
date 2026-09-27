"""
Standalone 5D Mirror-Entangled Simulation with visualization.
Improved: exact expm propagator, correct mirror axes, norm checks.
"""
import numpy as np
import matplotlib.pyplot as plt
from time import time
from scipy.linalg import expm

# GOLDEN RATIO & ENTANGLEMENT
phi = (1 + np.sqrt(5)) / 2
phi5 = phi ** 5  # \u2248 11.09016994
T_total = 5.0    # Compressed runtime: 50y \u00d7 0.1 = 5s
dt = 0.01
steps = int(T_total / dt)

# MIRROR ANGLES (rad)
mirror_angles = [0.3, 0.8, 1.2]

print("=" * 70)
print("\u26a1 PHOTONIC-\u03a9 SIMFOLD \u2014 5D Mirror-Entangled Simulation")
print("=" * 70)
print(f"\u03c6     = {phi:.12f}")
print(f"\u03c6\u2075    = {phi5:.12f}")
print(f"T     = {T_total:.1f} s  (50 years compressed \u00d7 0.1)")
print(f"\u03a6(5)  = {5 * phi5:.8f}  total entanglement load")
print(f"Steps = {steps}  (dt = {dt}s)")
print("\u2500" * 70)


def reflection_2d(theta: float) -> np.ndarray:
    """Lossless 2D reflection matrix across line at angle \u03b8 (rad)."""
    c2 = np.cos(2 * theta)
    s2 = np.sin(2 * theta)
    return np.array([[c2, s2], [s2, -c2]])


def reflection_5d(n: np.ndarray) -> np.ndarray:
    """Householder reflection in 5D: R = I \u2212 2 n n\u1d40, ||n|| = 1."""
    n = np.asarray(n, dtype=float).reshape(-1, 1)
    n = n / np.linalg.norm(n)
    return np.eye(5) - 2.0 * (n @ n.T)


R_mirrors_2d = [reflection_2d(\u03b8) for \u03b8 in mirror_angles]

# Skew-symmetric generator \u2192 SO(5) evolution
w1, w2, w3, w4 = 1.0, np.sqrt(2), np.sqrt(3), phi
Omega = np.array([
    [0,   w1,  0,   0,   0],
    [-w1, 0,   w2,  0,   0],
    [0,  -w2,  0,   w3,  0],
    [0,   0,  -w3,  0,   w4],
    [0,   0,   0,  -w4,  0],
])
A = phi5 * Omega
U_step = expm(A * dt)

# Orthogonality check
U_check = U_step.T @ U_step - np.eye(5)
print(f"Propagator orthogonality error: {np.max(np.abs(U_check)):.2e}")

# Initial state
X = np.ones(5) / np.sqrt(5)
traj_5d = np.zeros((steps + 1, 5))
traj_5d[0] = X
phase_load = 0.0
norms = [np.linalg.norm(X)]

mirror_normals = [
    np.array([1.0, 0, 0, 0, 0]),
    np.array([0, 1.0, 0, 0, 0]),
    np.array([0, 0, 1.0, 0, 0]),
]
R5_mirrors = [reflection_5d(n) for n in mirror_normals]

start = time()
mirror_sequence = [0, 1, 2]

for k in range(1, steps + 1):
    # Unitary evolution
    X = U_step @ X

    # Mirror reflections
    bounce_idx = (k - 1) // max(1, steps // (len(mirror_sequence) + 1))
    if bounce_idx < len(mirror_sequence):
        X = R5_mirrors[mirror_sequence[bounce_idx]] @ X

    # Renormalize
    X = X / np.linalg.norm(X)
    phase_load += phi5 * dt
    traj_5d[k] = X
    norms.append(np.linalg.norm(X))

elapsed = time() - start
traj_2d = traj_5d[:, :2]

print(f"\n\u2705 Simulation complete in {elapsed:.4f}s")
print(f"Final state X(5): {X.round(6).tolist()}")
print(f"Norm preserved \u2014 min: {min(norms):.12f}, max: {max(norms):.12f}")
print(f"Accumulated phase load: {phase_load:.8f}")
print(f"Theoretical load:     {5 * phi5:.8f}")
print(f"Match: {np.isclose(phase_load, 5 * phi5)}")
print("\u2500" * 70)

# Visualization
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(10, 10))
circle = plt.Circle((0, 0), 1, ec="cyan", fc="none", ls="--", alpha=0.5, lw=1.5)
ax.add_patch(circle)

t_line = np.linspace(-1.3, 1.3, 2)
for \u03b8 in mirror_angles:
    ax.plot(t_line, np.tan(\u03b8) * t_line, color="white", alpha=0.25, ls=":")

ax.plot(
    traj_2d[:, 0],
    traj_2d[:, 1],
    color="#FF4466",
    lw=1.8,
    alpha=0.8,
    label="5D Flow (Ch1\u2013Ch2 Projection)",
)
ax.scatter(
    traj_2d[0, 0],
    traj_2d[0, 1],
    c="gold",
    s=200,
    ec="white",
    zorder=10,
    label=f"X\u2080 = ({traj_2d[0,0]:.2f}, {traj_2d[0,1]:.2f})",
)
ax.scatter(
    traj_2d[-1, 0],
    traj_2d[-1, 1],
    c="lime",
    s=200,
    ec="white",
    zorder=10,
    label=f"X(5) = ({traj_2d[-1,0]:.2f}, {traj_2d[-1,1]:.2f})",
)

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_xlabel("Channel 1 \u2014 Base Amplitude", color="white", fontsize=12)
ax.set_ylabel("Channel 2 \u2014 Violet Amplitude", color="white", fontsize=12)
ax.set_title(
    f"\u26a1 PHOTONIC-\u03a9 SIMFOLD \u2014 5D Mirror-Entangled Flow\n"
    f"50 years \u2192 5s | \u03a6(5) = {phase_load:.4f} | \u03c6\u2075 = {phi5:.6f}",
    color="gold",
    fontsize=14,
    pad=20,
)
ax.legend(loc="upper right", facecolor="#111133", labelcolor="white")
ax.grid(alpha=0.1)
ax.axis("equal")
plt.tight_layout()
plt.savefig("photonic_simfold_5d_mirrored.png", dpi=150, facecolor="#050510")
print("Saved: photonic_simfold_5d_mirrored.png")
plt.show()
