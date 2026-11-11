# %% Setup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy import optimize
import statsmodels.api as sm

np.set_printoptions(suppress=True, precision=4)
pd.set_option("display.float_format", "{:.4f}".format)
pd.set_option("display.width", 200)


# ======================================================================
# QUESTION 1
# ======================================================================

# %% Q1 - data
rng = np.random.default_rng(6140)
n = 200
x1, x2 = rng.uniform(1, 2, size=(2, n))      # X1, X2 ~ U(1, 2)
u = rng.normal(size=n)                       # u ~ N(0, 1)


# %% Q1 - GNR function
def gnr(beta_true, alpha_true=1):
    # generate y from the true model
    y = alpha_true * (x1**beta_true + x2**(1 - beta_true)) + u

    theta = np.array([0.5, 0.3])             # starting guess (alpha, beta)
    for j in range(1, 101):
        a, b = theta
        fit = a * (x1**b + x2**(1 - b))                            # x(theta)
        X = np.column_stack([x1**b + x2**(1 - b),                  # d x / d alpha
                             a * (x1**b * np.log(x1) - x2**(1 - b) * np.log(x2))])  # d x / d beta
        resid = y - fit
        step = np.linalg.solve(X.T @ X, X.T @ resid)               # GNR: regress resid on X
        theta = theta + step
        if abs(step).max() < 1e-8:
            break

    # SSR and standard errors at the final theta
    a, b = theta
    resid = y - a * (x1**b + x2**(1 - b))
    ssr = resid @ resid
    se = np.sqrt(np.diag(ssr / (n - 2) * np.linalg.inv(X.T @ X)))
    return theta, se, ssr, j


# %% Q1(i), Q1(ii) - three values of beta
for beta_true in [0.5, 0.1, 0.001]:
    theta, se, ssr, j = gnr(beta_true)
    print(f"true beta = {beta_true}")
    print(f"  alpha_hat = {theta[0]:.4f} (se {se[0]:.4f})   beta_hat = {theta[1]:.4f} (se {se[1]:.4f})")
    print(f"  SSR = {ssr:.4f}   iterations = {j}\n")

# Comment: estimates of alpha are close to the true value, while beta is mostly
# estimated imprecisely. SSR is nearly identical across all 3 regressions.


# ======================================================================
# QUESTION 2
# ======================================================================

# %% Q2(a) - generate samples (true: beta1 = beta2 = beta3 = 1, gamma = 2)
beta1, beta2, beta3, gamma = 1, 1, 1, 2
sample_sizes = [50, 100, 200]

data = {}                                            # data[m] = (y, z1, z2, z3)
for m in sample_sizes:
    z1, z2, z3 = rng.uniform(1, 2, size=(3, m))      # X1, X2, X3 ~ U(1, 2)
    v = rng.normal(size=m)                           # u ~ N(0, 1)
    y = beta1 * z1 + beta2 * z2 + beta3 * z3**gamma + v
    data[m] = (y, z1, z2, z3)


# %% Q2(a) - GNR function for (b1, b2, b3, gamma)
def gnr_q2(y, z1, z2, z3, theta0=(0.5, 0.5, 0.5, 1.5)):
    m = len(y)
    theta = np.array(theta0, dtype=float)
    for j in range(1, 101):
        b1, b2, b3, g = theta
        resid = y - (b1 * z1 + b2 * z2 + b3 * z3**g)
        X = np.column_stack([z1, z2, z3**g, b3 * z3**g * np.log(z3)])   # derivatives
        step = np.linalg.solve(X.T @ X, X.T @ resid)
        theta = theta + step
        if abs(step).max() < 1e-8:
            break
    b1, b2, b3, g = theta
    resid = y - (b1 * z1 + b2 * z2 + b3 * z3**g)
    ssr = resid @ resid
    se = np.sqrt(np.diag(ssr / (m - 4) * np.linalg.inv(X.T @ X)))
    return theta, se, ssr, j


# %% Q2(a) - estimates for each sample size
rows = []
for m in sample_sizes:
    theta, se, ssr, j = gnr_q2(*data[m])
    for name, est, s_e in zip(["beta1", "beta2", "beta3", "gamma"], theta, se):
        rows.append({"n": m, "param": name, "estimate": est, "std.err": s_e})
    print(f"n = {m}: SSR = {ssr:.4f}, iterations = {j}")

table = pd.DataFrame(rows).pivot(index="param", columns="n", values=["estimate", "std.err"])
print("\n", table.loc[["beta1", "beta2", "beta3", "gamma"]])


# %% Q2(b)(i) - unrestricted (Wald) test of H0: gamma = 1
gamma_hat = table.loc["gamma", "estimate"]      # Series indexed by n: 50, 100, 200
gamma_se = table.loc["gamma", "std.err"]

t = (gamma_hat - 1) / gamma_se                  # subtract first, then divide
p = 2 * (1 - stats.norm.cdf(abs(t)))            # two-sided p-value, t ~ N(0,1) asymptotically

gamma_results = pd.DataFrame({"gamma_hat": gamma_hat, "se": gamma_se, "t": t, "p-value": p,
                              "reject at 5%": abs(t) > 1.96})
print(gamma_results)


# %% Q2(b)(ii) - restricted (LM / GNR) test of H0: gamma = 1
rows = []
for m in sample_sizes:
    y, z1, z2, z3 = data[m]

    # Step 1: impose gamma = 1 -> model is linear -> plain OLS, keep the residuals
    Z = np.column_stack([z1, z2, z3])
    b_r = np.linalg.solve(Z.T @ Z, Z.T @ y)          # restricted (b1, b2, b3)
    u_r = y - Z @ b_r                                # restricted residuals

    # Step 2: regress the residuals on all 4 derivative columns, evaluated at gamma = 1
    X = np.column_stack([z1, z2, z3, b_r[2] * z3 * np.log(z3)])
    coef = np.linalg.solve(X.T @ X, X.T @ u_r)
    ssr_gnr = np.sum((u_r - X @ coef) ** 2)
    se = np.sqrt(np.diag(ssr_gnr / (m - 4) * np.linalg.inv(X.T @ X)))

    # Step 3: t-stat on the gamma column
    t_lm = coef[3] / se[3]
    p_lm = 2 * (1 - stats.norm.cdf(abs(t_lm)))
    rows.append({"n": m, "t_LM": t_lm, "p-value": p_lm, "reject at 5%": abs(t_lm) > 1.96})

print(pd.DataFrame(rows).set_index("n"))
