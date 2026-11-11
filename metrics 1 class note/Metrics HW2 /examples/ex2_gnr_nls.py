"""Example 2 — NLS by successive Gauss-Newton Regressions (GNR).

Made-up model (NOT the homework model):
    y_t = c * exp(d * z_t) + u_t        theta = (c, d)

GNR at a guess theta_j:
    regress  (y - x(theta_j))  on  X(theta_j) = Jacobian  ->  coefficients b
    update   theta_{j+1} = theta_j + b
    stop when b is ~0  (then residuals are orthogonal to the Jacobian = NLS first-order conditions)

Run:  .venv/bin/python examples/ex2_gnr_nls.py
"""
import numpy as np
import pandas as pd
from scipy import optimize

rng = np.random.default_rng(42)

# ---------------- data ----------------
n = 200
z = rng.uniform(0, 1, size=n)
y = 2.0 * np.exp(0.5 * z) + rng.normal(size=n)


# ---------------- model pieces ----------------
def x_fun(theta, z):
    """Regression function x_t(theta)."""
    c, d = theta
    return c * np.exp(d * z)


def jacobian(theta, z):
    """n x k matrix of derivatives of x_t(theta) w.r.t. each parameter."""
    c, d = theta
    dx_dc = np.exp(d * z)               # d/dc [c e^{dz}] = e^{dz}
    dx_dd = c * z * np.exp(d * z)       # d/dd [c e^{dz}] = c z e^{dz}
    return np.column_stack([dx_dc, dx_dd])


# ---------------- successive GNRs ----------------
def gnr_nls(theta0, y, z, tol=1e-8, max_iter=100, verbose=True):
    theta = np.asarray(theta0, dtype=float)
    for it in range(1, max_iter + 1):
        resid = y - x_fun(theta, z)
        J = jacobian(theta, z)
        b, *_ = np.linalg.lstsq(J, resid, rcond=None)   # OLS of resid on J
        theta = theta + b
        ssr = np.sum((y - x_fun(theta, z)) ** 2)
        if verbose:
            print(f"iter {it:2d}  theta = {theta}  SSR = {ssr:.6f}  |step| = {np.max(np.abs(b)):.2e}")
        if np.max(np.abs(b)) < tol:
            break
    return theta, it


theta_hat, iters = gnr_nls(theta0=[1.0, 1.0], y=y, z=z)
print(f"\nConverged in {iters} iterations")

# ---------------- standard errors ----------------
# Var(theta_hat) = s^2 (J'J)^{-1},  J evaluated at theta_hat,  s^2 = SSR / (n - k)
J = jacobian(theta_hat, z)
resid = y - x_fun(theta_hat, z)
k = len(theta_hat)
s2 = resid @ resid / (n - k)            # @ = matrix multiply
cov = s2 * np.linalg.inv(J.T @ J)       # .T = transpose
se = np.sqrt(np.diag(cov))

table = pd.DataFrame({"estimate": theta_hat, "std.err": se, "t-stat": theta_hat / se},
                     index=["c", "d"])
print(table.round(4))

# ---------------- check against scipy's built-in NLS ----------------
popt, pcov = optimize.curve_fit(lambda z, c, d: c * np.exp(d * z), z, y, p0=[1.0, 1.0])
print("\nscipy curve_fit:", popt.round(4), " SE:", np.sqrt(np.diag(pcov)).round(4))

# ---------------- final GNR as a check ----------------
# At the NLS estimate, the GNR coefficients should be ~0 and its OLS std errors equal the NLS SEs.
import statsmodels.api as sm
final = sm.OLS(resid, J).fit()
print("\nFinal GNR coefficients (should be ~0):", final.params.round(8))
print("Final GNR std errors   (match above):", final.bse.round(4))
