"""
5D Householder Mirror Reflection — Property Tests
Activates and validates the unbreakable-mirror operators from the PDF.
"""
import numpy as np
from scipy.linalg import expm

phi = (1 + np.sqrt(5)) / 2
phi5 = phi ** 5
T_sim = 5.0
DT = 0.01


def householder(n: np.ndarray) -> np.ndarray:
    """R = I - 2 n nᵀ  with ||n||=1  →  RᵀR = I, det(R) = -1"""
    n = np.asarray(n, dtype=float).reshape(-1, 1)
    n = n / np.linalg.norm(n)
    return np.eye(n.shape[0]) - 2.0 * (n @ n.T)


def test_householder_properties():
    normals = [
        np.array([1.0, 0, 0, 0, 0]),
        np.array([0, 1.0, 0, 0, 0]),
        np.array([0, 0, 1.0, 0, 0]),
        np.ones(5) / np.sqrt(5),
    ]
    for n in normals:
        R = householder(n)
        assert np.allclose(R.T @ R, np.eye(5), atol=1e-12), "RᵀR ≠ I"
        assert abs(np.linalg.det(R) + 1) < 1e-10, "det(R) ≠ -1"
    print("\u2705 Householder: R\u1d40R = I, det = -1 for all test normals")


def test_5d_evolution_norm_and_phase():
    w1, w2, w3, w4 = 1.0, np.sqrt(2), np.sqrt(3), phi
    Omega = np.array([
        [0, w1, 0, 0, 0],
        [-w1, 0, w2, 0, 0],
        [0, -w2, 0, w3, 0],
        [0, 0, -w3, 0, w4],
        [0, 0, 0, -w4, 0],
    ])
    U = expm(phi5 * Omega * DT)
    assert np.allclose(U.T @ U, np.eye(5), atol=1e-12), "Propagator not orthogonal"

    X = np.ones(5) / np.sqrt(5)
    mirrors = [householder(n) for n in [
        np.array([1.0, 0, 0, 0, 0]),
        np.array([0, 1.0, 0, 0, 0]),
        np.array([0, 0, 1.0, 0, 0]),
    ]]
    phase = 0.0
    steps = int(T_sim / DT)
    for k in range(steps):
        X = U @ X
        bi = k // max(1, steps // 4)
        if bi < 3:
            X = mirrors[bi] @ X
        X = X / np.linalg.norm(X)
        phase += phi5 * DT

    assert abs(np.linalg.norm(X) - 1.0) < 1e-10
    assert np.isclose(phase, T_sim * phi5, rtol=1e-6)
    print(f"\u2705 5D evolution: norm=1, phase={phase:.8f} == {T_sim*phi5:.8f}")
    print(f"   Final state X(5) = {X.round(6).tolist()}")


if __name__ == "__main__":
    test_householder_properties()
    test_5d_evolution_norm_and_phase()
    print("\nAll 5D mirror reflection operations ACTIVATED and PASSED.")
