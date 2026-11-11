"""Example 4 — numerical MLE and Monte Carlo checks.

Use this to CHECK pen-and-paper answers, e.g. "is my closed-form MLE right?"
or "is my formula for E(estimator) right?".

Made-up example (NOT a homework distribution): Poisson(lam),
    log L(lam) = sum( x*log(lam) - lam - log(x!) )  ->  closed-form MLE = mean(x)

Run:  .venv/bin/python examples/ex4_mle_and_simulation.py
"""
import numpy as np
from scipy import optimize, stats

rng = np.random.default_rng(1)

# ---------------- 1. Numerical MLE ----------------
x = rng.poisson(lam=3.0, size=500)


def neg_loglik(params):
    lam = params[0]
    if lam <= 0:
        return np.inf                              # keep the search in the valid region
    return -np.sum(stats.poisson.logpmf(x, lam))   # minimise the NEGATIVE log-likelihood


res = optimize.minimize(neg_loglik, x0=[1.0], method="Nelder-Mead")
print("numerical MLE :", res.x[0].round(4))
print("closed form   :", x.mean().round(4))       # should match

# One-parameter alternative: minimize_scalar with bounds
res1 = optimize.minimize_scalar(lambda lam: -np.sum(stats.poisson.logpmf(x, lam)),
                                bounds=(1e-6, 20), method="bounded")
print("minimize_scalar:", round(res1.x, 4))

# Writing a log-density by hand instead of using scipy.stats:
#   logf = np.log(theta) + (theta - 1) * np.log(x)     # e.g. for some density f(x, theta)
#   return -np.sum(logf)

# ---------------- 2. Monte Carlo: mean and variance of an estimator ----------------
# Example: s_ML^2 = sum((x - xbar)^2) / n  for x ~ N(0, sigma^2)
#   theory: E = sigma^2 (n-1)/n ,  Var = 2 sigma^4 (n-1)/n^2
n, sigma2, reps = 20, 4.0, 20_000
est = np.empty(reps)                               # pre-allocate storage
for r in range(reps):
    draw = rng.normal(0, np.sqrt(sigma2), size=n)
    est[r] = np.sum((draw - draw.mean()) ** 2) / n

print(f"\nsimulated mean = {est.mean():.4f}   theory = {sigma2 * (n - 1) / n:.4f}")
print(f"simulated var  = {est.var():.4f}   theory = {2 * sigma2**2 * (n - 1) / n**2:.4f}")

# ---------------- 3. Regression residuals with matrices ----------------
#   e = y - X b,  b = (X'X)^{-1} X'y
X = np.column_stack([np.ones(n), rng.uniform(size=n)])
y = X @ np.array([1.0, 2.0]) + rng.normal(size=n)
b = np.linalg.solve(X.T @ X, X.T @ y)              # solve() is safer than inv()
e = y - X @ b
print("\nb =", b.round(4), "  e'e/n =", round(e @ e / n, 4))
