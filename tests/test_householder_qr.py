"""Unit tests for Householder QR and applications."""
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from householder_qr import (
    householder_matrix,
    householder_qr,
    least_squares_qr,
    orthogonalize_basis,
    project_onto_column_space,
    qr_project_5d_state,
    sequential_mirror_qr,
    verify_qr,
)


def test_explicit_mirror_properties():
    for n in [np.array([1.0, 0, 0, 0, 0]), np.ones(5) / np.sqrt(5)]:
        R = householder_matrix(n)
        assert np.allclose(R.T @ R, np.eye(5), atol=1e-12)
        assert abs(np.linalg.det(R) + 1) < 1e-10


def test_qr_random():
    rng = np.random.default_rng(0)
    for shape in [(5, 5), (8, 3), (4, 6)]:
        A = rng.standard_normal(shape)
        rep = verify_qr(A)
        assert rep["pass"], rep


def test_least_squares():
    rng = np.random.default_rng(1)
    A = rng.standard_normal((10, 3))
    x_true = np.array([1.0, -2.0, 0.5])
    b = A @ x_true
    x = least_squares_qr(A, b)
    assert np.allclose(x, x_true, atol=1e-10)


def test_orthogonalize():
    rng = np.random.default_rng(2)
    V = rng.standard_normal((6, 3))
    Q = orthogonalize_basis(V)
    assert np.allclose(Q.T @ Q, np.eye(3), atol=1e-12)


def test_projection():
    A = np.eye(5)[:, :3]
    x = np.array([1.0, 2, 3, 4, 5])
    p = project_onto_column_space(A, x)
    assert np.allclose(p, [1, 2, 3, 0, 0])


def test_5d_bridge():
    X = np.ones(5) / np.sqrt(5)
    Xp = qr_project_5d_state(X)
    assert abs(np.linalg.norm(Xp) - 1) < 1e-12
    Xf, Qeq = sequential_mirror_qr(X, [np.eye(5)[0], np.eye(5)[1]])
    assert abs(np.linalg.norm(Xf) - 1) < 1e-12
    assert np.allclose(Qeq.T @ Qeq, np.eye(5), atol=1e-10)


if __name__ == "__main__":
    test_explicit_mirror_properties()
    test_qr_random()
    test_least_squares()
    test_orthogonalize()
    test_projection()
    test_5d_bridge()
    print("\u2705 All Householder-QR application tests PASSED")
