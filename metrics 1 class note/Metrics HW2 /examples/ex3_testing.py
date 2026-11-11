"""Example 3 — testing a restriction in a nonlinear model.

Made-up model (NOT the homework model):
    y_t = c * exp(d * z_t) + g * w_t + u_t      theta = (c, d, g)
Test  H0: d = 0.5

(i)  Unrestricted: estimate all of theta by NLS, then t-test / Wald test on d.
(ii) Restricted only: impose d = 0.5 (model becomes LINEAR in c, g -> plain OLS),
     then run ONE GNR at the restricted estimates and test the coefficient on the
     d-column (LM-type test; equivalently n * R^2 from that GNR).

Run:  .venv/bin/python examples/ex3_testing.py
"""
import numpy as np
import statsmodels.api as sm
from scipy import stats

rng = np.random.default_rng(7)

n = 100
z = rng.uniform(0, 1, size=n)
w = rng.uniform(0, 1, size=n)
y = 2.0 * np.exp(0.5 * z) + 1.0 * w + rng.normal(size=n)   # H0 is true here


def x_fun(theta):
    c, d, g = theta
    return c * np.exp(d * z) + g * w


def jacobian(theta):
    c, d, g = theta
    return np.column_stack([np.exp(d * z),          # d/dc
                            c * z * np.exp(d * z),  # d/dd
                            w])                     # d/dg


def gnr_nls(theta0, tol=1e-8, max_iter=200):
    theta = np.asarray(theta0, dtype=float)
    for _ in range(max_iter):
        b, *_ = np.linalg.lstsq(jacobian(theta), y - x_fun(theta), rcond=None)
        theta += b
        if np.max(np.abs(b)) < tol:
            break
    return theta


# ===================== (i) unrestricted: t-test =====================
theta_u = gnr_nls([1.0, 1.0, 1.0])
resid_u = y - x_fun(theta_u)
J = jacobian(theta_u)
s2 = resid_u @ resid_u / (n - 3)
se = np.sqrt(np.diag(s2 * np.linalg.inv(J.T @ J)))

d0 = 0.5
t_stat = (theta_u[1] - d0) / se[1]
p_t = 2 * (1 - stats.t.cdf(abs(t_stat), df=n - 3))       # two-sided p-value
print("Unrestricted estimates:", theta_u.round(4), " SE:", se.round(4))
print(f"(i)  t = {t_stat:.4f},  p = {p_t:.4f}")
# Wald version: W = t^2 ~ chi2(1)
print(f"     Wald = {t_stat**2:.4f},  p = {1 - stats.chi2.cdf(t_stat**2, df=1):.4f}")

# ===================== (ii) restricted only: GNR / LM test =====================
# With d fixed at 0.5, y = c*exp(0.5 z) + g*w + u  is linear -> OLS gives c~, g~
Xr = np.column_stack([np.exp(d0 * z), w])
c_r, g_r = np.linalg.lstsq(Xr, y, rcond=None)[0]
theta_r = np.array([c_r, d0, g_r])
resid_r = y - x_fun(theta_r)

# GNR: regress restricted residuals on the FULL Jacobian evaluated at theta_r
gnr = sm.OLS(resid_r, jacobian(theta_r)).fit()
print("\nRestricted estimates:", theta_r.round(4))
print(gnr.summary(xname=["c", "d", "g"]).tables[1])

t_lm = gnr.tvalues[1]                                     # t-stat on the d column
print(f"(ii) GNR t on d = {t_lm:.4f},  p = {gnr.pvalues[1]:.4f}")

# n * R^2 version (uncentered R^2, since the regressand has no constant)
r2_unc = 1 - gnr.ssr / (resid_r @ resid_r)
lm = n * r2_unc
print(f"     LM = n*R^2 = {lm:.4f},  p = {1 - stats.chi2.cdf(lm, df=1):.4f}")
