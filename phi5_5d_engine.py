"""
5D Mirrored Photonic Evolution with φ⁵ entanglement weighting.
Implements Householder reflections (unbreakable mirrors) and skew-symmetric flow.
"""
import numpy as np
from scipy.linalg import expm
from config import phi, phi5, T_sim, E_phi_total, DT


class Phi5DEngine:
    """5D mirrored photonic evolution with φ^5 entanglement weighting"""

    def __init__(self):
        self.t = 0.0
        self.dt = DT
        self.steps = int(T_sim / self.dt)
        # Initial state: uniform unit vector in 5D
        self.X = np.ones(5) / np.sqrt(5)

        # Householder mirror normals (first three coordinate planes)
        self.mirror_normals = [
            np.array([1.0, 0, 0, 0, 0]),
            np.array([0, 1.0, 0, 0, 0]),
            np.array([0, 0, 1.0, 0, 0]),
        ]
        self.mirrors = [self._householder(n) for n in self.mirror_normals]

        # Skew-symmetric generator: preserves norm under φ^5 amplification
        w1, w2, w3, w4 = 1.0, np.sqrt(2), np.sqrt(3), phi
        self.Omega = np.array([
            [0,   w1,  0,   0,   0],
            [-w1, 0,   w2,  0,   0],
            [0,  -w2,  0,   w3,  0],
            [0,   0,  -w3,  0,   w4],
            [0,   0,   0,  -w4,  0],
        ])
        self.A = phi5 * self.Omega  # φ^5 weighted Lie algebra element

        # Exact propagator for SO(5) evolution (improved over Euler)
        self.U_step = expm(self.A * self.dt)

        # Tracking
        self.trajectory = np.zeros((self.steps + 1, 5))
        self.trajectory[0] = self.X.copy()
        self.phase_load = 0.0
        self.norms = [np.linalg.norm(self.X)]
        self.bounce_idx = 0
        self._step_count = 0

    def _householder(self, n: np.ndarray) -> np.ndarray:
        """Unbreakable mirror: R = I - 2nnᵀ, det=-1, RᵀR=I"""
        n = np.asarray(n, dtype=float).reshape(-1, 1)
        n = n / np.linalg.norm(n)
        return np.eye(5) - 2.0 * (n @ n.T)

    def step(self) -> dict:
        self._step_count += 1
        k = self._step_count

        # 1. Unitary evolution — φ^5 amplified exact flow
        self.X = self.U_step @ self.X

        # 2. Apply mirror reflections in sequence
        bounce_period = max(1, self.steps // (len(self.mirrors) + 1))
        self.bounce_idx = (k - 1) // bounce_period
        if self.bounce_idx < len(self.mirrors):
            self.X = self.mirrors[self.bounce_idx] @ self.X

        # 3. Renormalize (numerical cleanup; structure already preserves norm)
        norm = np.linalg.norm(self.X)
        if norm > 0:
            self.X = self.X / norm

        # 4. Accumulate entanglement phase
        self.phase_load += phi5 * self.dt

        # Record
        if k <= self.steps:
            self.trajectory[k] = self.X
        self.norms.append(norm)
        self.t += self.dt

        return {
            "t": round(self.t, 4),
            "X": self.X.round(6).tolist(),
            "norm": round(float(norm), 10),
            "phase_load": round(self.phase_load, 6),
            "phase_pct": round(100.0 * self.phase_load / E_phi_total, 2),
            "bounce_mirror": self.bounce_idx if self.bounce_idx < len(self.mirrors) else None,
        }

    def run(self) -> dict:
        """Run remaining steps to completion."""
        while self._step_count < self.steps:
            self.step()
        return {
            "final_X": self.X.round(6).tolist(),
            "final_phase": round(self.phase_load, 6),
            "target_phase": round(E_phi_total, 6),
            "norm_min": round(float(min(self.norms)), 10),
            "norm_max": round(float(max(self.norms)), 10),
            "traj_2d": self.trajectory[:, :2],
            "match": bool(np.isclose(self.phase_load, E_phi_total, rtol=1e-6)),
        }
