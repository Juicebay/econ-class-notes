"""How sensitive are the capital rows to the choice of K(1976Q1)?"""
import numpy as np
import openpyxl

wb = openpyxl.load_workbook("Assignment1_data.xlsx", read_only=True, data_only=True)
rows = list(wb["Combined"].iter_rows(values_only=True))
data = rows[1:]
q = np.array([r[0] for r in data])
d = np.array([[float(v) for v in r[1:]] for r in data])
T = len(q)
output, pop = d[:, 60], d[:, 63]
investment = d[:, 43]
delta = 0.025


def sim(K0, I):
    K = np.empty(T)
    K[0] = K0
    for t in range(T - 1):
        K[t + 1] = I[t] + (1 - delta) * K[t]
    return K


def stats(series):
    lam = 1600
    X = np.diag((1 + 6 * lam) * np.ones(T))
    X += np.diag(-4 * lam * np.ones(T - 1), 1) + np.diag(-4 * lam * np.ones(T - 1), -1)
    X += np.diag(lam * np.ones(T - 2), 2) + np.diag(lam * np.ones(T - 2), -2)
    X[0, 0], X[0, 1], X[1, 0], X[1, 1] = 1 + lam, -2 * lam, -2 * lam, 1 + 5 * lam
    X[T-1, T-1], X[T-2, T-1], X[T-1, T-2], X[T-2, T-2] = 1 + lam, -2 * lam, -2 * lam, 1 + 5 * lam
    m = np.linalg.inv(X)
    raw = np.log(np.column_stack(series))
    c = raw - m @ raw
    v = (c.T @ c) / T
    sd = np.sqrt(np.diag(v)) * 100
    corr = v / np.sqrt(np.outer(np.diag(v).copy(), np.diag(v).copy()))
    return sd, corr[:, 0]


def k0_for(kind):
    lo, hi = 1e8, 1e16

    def gap(K0):
        K = sim(K0, investment)
        if kind == "logdiff":
            return np.mean(np.diff(np.log(K))) - np.mean(np.diff(np.log(investment)))
        g1 = K[1:] / K[:-1] - 1
        g2 = investment[1:] / investment[:-1] - 1
        return g1.mean() - g2.mean()
    for _ in range(300):
        mid = np.sqrt(lo * hi)
        if gap(mid) > 0:
            lo = mid
        else:
            hi = mid
    return np.sqrt(lo * hi)


print("K(1976Q1) under each reading of the calibration rule:")
cands = {}
for kind in ("logdiff", "simplediff"):
    K0 = k0_for(kind)
    cands[kind] = K0
    print("   %-11s K0 = %.6g   K/Y(1976Q1) = %.2f" % (kind, K0, K0 / output[0]))
for nm, K0 in [("I0/delta", investment[0] / delta),
               ("30*I0", 30 * investment[0]), ("35*I0", 35 * investment[0]),
               ("40*I0", 40 * investment[0])]:
    cands[nm] = K0
    print("   %-11s K0 = %.6g   K/Y(1976Q1) = %.2f" % (nm, K0, K0 / output[0]))

print("\n   K0 choice        sd(capital) corr(capital,y)  sd(cap prod) corr(cap prod,y)")
for nm, K0 in cands.items():
    K = sim(K0, investment)
    sd, cr = stats([output / pop, K / pop, output / K])
    print("   %-15s %8.2f %10.2f %14.2f %12.2f" % (nm, sd[1], cr[1], sd[2], cr[2]))

# also: capital built from the broader business investment series
K = sim(cands["logdiff"] * (d[:, 41][0] / investment[0]), d[:, 41])
sd, cr = stats([output / pop, K / pop, output / K])
print("   (K from business gross fixed capital formation: sd k %.2f corr %.2f, sd y/k %.2f corr %.2f)"
      % (sd[1], cr[1], sd[2], cr[2]))

# and with investment turned into a quarterly flow (I/4, K0/4)
K = sim(cands["logdiff"] / 4, investment / 4)
sd, cr = stats([output / pop, K / pop, output / K])
print("   (I as a quarterly flow, I/4:  sd k %.2f corr %.2f, sd y/k %.2f corr %.2f)"
      % (sd[1], cr[1], sd[2], cr[2]))
