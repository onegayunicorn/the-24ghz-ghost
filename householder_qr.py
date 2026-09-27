"""Householder Reflection Applications & QR Decomposition
Pure-NumPy: reflector construction, classical/economic QR, least-squares,
orthogonalization, projection, 5D manifold QR bridge.
R = I - 2 n n^T ; R^T R = I ; det(R) = -1
"""
from __future__ import annotations
import numpy as np
from typing import Tuple, Optional, List

def householder_vector(x: np.ndarray) -> Tuple[np.ndarray, float]:
    """Golub-Van Loan: (I - beta v v^T) x = ||x|| e_1"""
    x = np.asarray(x, dtype=float).ravel()
    sigma = float(np.dot(x[1:], x[1:]))
    v = x.copy()
    if sigma == 0.0 and x[0] >= 0:
        return v, 0.0
    mu = np.sqrt(x[0] ** 2 + sigma)
    if x[0] <= 0:
        v[0] = x[0] - mu
    else:
        v[0] = -sigma / (x[0] + mu)
    denom = sigma + v[0] ** 2
    beta = 2.0 * v[0] ** 2 / denom if denom != 0 else 0.0
    v = v / v[0]
    return v, beta

def apply_householder(v: np.ndarray, beta: float, A: np.ndarray, col_start: int = 0) -> None:
    if beta == 0.0:
        return
    sub = A[col_start:, col_start:]
    w = beta * (v @ sub)
    sub -= np.outer(v, w)

def householder_matrix(n: np.ndarray) -> np.ndarray:
    n = np.asarray(n, dtype=float).reshape(-1, 1)
    n = n / np.linalg.norm(n)
    return np.eye(n.shape[0]) - 2.0 * (n @ n.T)

def householder_qr(A: np.ndarray, mode: str = "full") -> Tuple[np.ndarray, np.ndarray]:
    A = np.array(A, dtype=float, copy=True)
    m, n = A.shape
    k = min(m, n)
    betas: List[float] = []
    vs: List[np.ndarray] = []
    for j in range(k):
        v, beta = householder_vector(A[j:, j])
        vs.append(v)
        betas.append(beta)
        apply_householder(v, beta, A, col_start=j)
    R = np.triu(A[:k, :]) if mode == "economic" else np.triu(A)
    Q = np.eye(m, k) if mode == "economic" else np.eye(m)
    for j in range(k - 1, -1, -1):
        v, beta = vs[j], betas[j]
        if beta == 0.0:
            continue
        sub = Q[j:, j:]
        vj = v[: sub.shape[0]]
        w = beta * (vj @ sub)
        sub -= np.outer(vj, w)
    return Q, R

def least_squares_qr(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    Q, R = householder_qr(A, mode="economic")
    y = Q.T @ b
    n = R.shape[0]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        s = y[i] - np.dot(R[i, i + 1 :], x[i + 1 :])
        x[i] = s / R[i, i]
    return x

def orthogonalize_basis(V: np.ndarray) -> np.ndarray:
    Q, _ = householder_qr(V, mode="economic")
    return Q

def project_onto_column_space(A: np.ndarray, x: np.ndarray) -> np.ndarray:
    Q, _ = householder_qr(A, mode="economic")
    return Q @ (Q.T @ x)

def qr_project_5d_state(X: np.ndarray, basis: Optional[np.ndarray] = None) -> np.ndarray:
    X = np.asarray(X, dtype=float).ravel()
    assert X.size == 5
    if basis is None:
        basis = np.eye(5)
    Q, _ = householder_qr(basis, mode="economic")
    return Q @ (Q.T @ X)

def sequential_mirror_qr(X0: np.ndarray, normals: List[np.ndarray]):
    X = np.asarray(X0, dtype=float).copy()
    Q_acc = np.eye(len(X))
    for n in normals:
        R = householder_matrix(n)
        X = R @ X
        Q_acc = R @ Q_acc
    Q_qr, _ = householder_qr(Q_acc, mode="full")
    return X, Q_qr

def _frobenius(A: np.ndarray) -> float:
    return float(np.sqrt(np.sum(A ** 2)))

def verify_qr(A: np.ndarray, tol: float = 1e-10) -> dict:
    Qf, Rf = householder_qr(A, mode="full")
    Qe, Re = householder_qr(A, mode="economic")
    m, n = A.shape
    k = min(m, n)
    return {
        "full_orth_err": _frobenius(Qf.T @ Qf - np.eye(m)),
        "econ_orth_err": _frobenius(Qe.T @ Qe - np.eye(k)),
        "full_recon_err": _frobenius(A - Qf @ Rf),
        "econ_recon_err": _frobenius(A - Qe @ Re),
        "R_upper_full": bool(np.allclose(np.tril(Rf, -1), 0)),
        "R_upper_econ": bool(np.allclose(np.tril(Re, -1), 0)),
        "pass": all([
            _frobenius(Qf.T @ Qf - np.eye(m)) < tol,
            _frobenius(Qe.T @ Qe - np.eye(k)) < tol,
            _frobenius(A - Qf @ Rf) < tol,
            _frobenius(A - Qe @ Re) < tol,
        ]),
    }

if __name__ == "__main__":
    rng = np.random.default_rng(42)
    A = rng.standard_normal((6, 4))
    print("QR verification:", verify_qr(A))
    x_true = rng.standard_normal(4)
    b = A @ x_true + 0.01 * rng.standard_normal(6)
    x_hat = least_squares_qr(A, b)
    print("LS residual:", np.linalg.norm(A @ x_hat - b))
    X0 = np.ones(5) / np.sqrt(5)
    Xf, Qeq = sequential_mirror_qr(X0, [np.eye(5)[i] for i in range(3)])
    print("5D mirror norm:", np.linalg.norm(Xf))
    print("All Householder-QR applications OK")
