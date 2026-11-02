"""Independent re-implementation of HW.m in Python, to check the submitted numbers.

Reads the same Assignment1_data.xlsx, builds the same 12 series, runs the same HP
filter, and prints the statistics the assignment asks for -- plus the capital-stock
block the submitted answer left out, and the correlations quoted in question 3 that
the submitted MATLAB script never computes.
"""
import numpy as np
import openpyxl

XL = "Assignment1_data.xlsx"
wb = openpyxl.load_workbook(XL, read_only=True, data_only=True)
ws = wb["Combined"]
rows = list(ws.iter_rows(values_only=True))
hdr, data = rows[0], rows[1:]
q = np.array([r[0] for r in data])
d = np.array([[float(v) for v in r[1:]] for r in data])
T = d.shape[0]
assert T == 202, T


def col(i):
    return d[:, i]


C = dict(  # header positions minus 1 (column 0 = quarter, dropped above)
    output=60,
    semidur=35, nondur=36, services=37,
    investment=43,
    govcons=39, govinv=48,
    exports=53, imports=56,
    nominal=29,
    hours=62, pop=63, exrate=64,
)

output = col(C["output"])
consumption = col(C["semidur"]) + col(C["nondur"]) + col(C["services"])
investment = col(C["investment"])
govcons = col(C["govcons"])
govinv = col(C["govinv"])
exports = col(C["exports"])
imports = col(C["imports"])
hours = col(C["hours"])
pop = col(C["pop"])
exrate = 100 * col(C["exrate"])
nominal = col(C["nominal"])

print("imports positive throughout:", bool((imports > 0).all()),
      " min value:", imports.min())
print("exports-investment etc. sanity: output[0]=%.0f  output[-1]=%.0f" % (output[0], output[-1]))

netexports = 1 + (exports - imports) / output
productivity = output / hours
price = 100 * nominal / output

# ---------------------------------------------------------------- capital stock
# K(t+1) = I(t) + (1-delta) K(t), delta = 0.025, K(1976Q1) chosen so that the
# average growth rates of K and of I over the sample are identical.
delta = 0.025


def capital_k0(K0, I=None, scale=1.0):
    I = investment if I is None else I
    K = np.empty(T)
    K[0] = K0
    for t in range(T - 1):
        K[t + 1] = scale * I[t] + (1 - delta) * K[t]
    return K


def growth_gap(K0):
    K = capital_k0(K0)
    return np.mean(np.diff(np.log(K))) - np.mean(np.diff(np.log(investment)))


lo, hi = 1e9, 1e15
assert growth_gap(lo) > 0 > growth_gap(hi), (growth_gap(lo), growth_gap(hi))
for _ in range(200):
    mid = np.sqrt(lo * hi)
    if growth_gap(mid) > 0:
        lo = mid
    else:
        hi = mid
K0 = np.sqrt(lo * hi)
K = capital_k0(K0)
capmpk = output / K
print("K0 = %.6g   avg growth K = %.6f   avg growth I = %.6f"
      % (K0, np.mean(np.diff(np.log(K))), np.mean(np.diff(np.log(investment)))))
print("avg growth I (SAAR turned into quarterly flow) unchanged: %.6f"
      % np.mean(np.diff(np.log(investment / 4))))
print("K per capita 1976Q1 = %.0f   2000Q1 = %.0f   2026Q2 = %.0f"
      % (K[0] / pop[0], K[96] / pop[96], K[-1] / pop[-1]))
print("K/Y in 1976Q1 = %.2f   2026Q2 = %.2f   (annual-rate ratios)"
      % (K[0] / output[0], K[-1] / output[-1]))

y = output / pop
c = consumption / pop
i = investment / pop
gc = govcons / pop
gi = govinv / pop
ex = exports / pop
im = imports / pop
n = hours / pop
k = K / pop
mpk = output / K
w = productivity
nx = netexports
pgdp = price

cols = [y, c, i, gc, gi, ex, im, nx, n, w, k, mpk, exrate, pgdp]
names = ["Output", "Consumption", "Investment", "Gov cons", "Gov inv", "Exports",
         "Imports", "Net exports", "Hours", "Lab prod", "Capital", "Cap prod",
         "Ex rate", "Price"]

a = np.column_stack(cols)
lam = 1600
nvar = a.shape[1]
X = np.diag((1 + 6 * lam) * np.ones(T))
X += np.diag(-4 * lam * np.ones(T - 1), 1) + np.diag(-4 * lam * np.ones(T - 1), -1)
X += np.diag(lam * np.ones(T - 2), 2) + np.diag(lam * np.ones(T - 2), -2)
X[0, 0] = 1 + lam
X[0, 1] = -2 * lam
X[1, 0] = -2 * lam
X[1, 1] = 1 + 5 * lam
X[T - 1, T - 1] = 1 + lam
X[T - 2, T - 1] = -2 * lam
X[T - 1, T - 2] = -2 * lam
X[T - 2, T - 2] = 1 + 5 * lam
hpmat = np.linalg.inv(X)
raw = np.log(a)
trend = hpmat @ raw
cyc = raw - trend
vcv = (cyc.T @ cyc) / T
var = np.diag(vcv).copy()
sd = np.sqrt(var) * 100
corr = vcv / np.sqrt(np.outer(var, var))

print("\n%-12s %8s %8s" % ("variable", "sd%", "corr(y)"))
for j, nm in enumerate(names):
    print("%-12s %8.2f %8.2f" % (nm, sd[j], corr[j, 0]))
print("corr(hours, labour productivity) = %.4f" % corr[8, 9])
print("corr(hours, capital productivity) = %.4f" % corr[8, 11])
print("corr(capital, output) = %.4f" % corr[10, 0])

# ------------------------------------------------------------------- dates
ty = np.array([float(s[:4]) + (float(s[-1]) - 1) / 4 for s in q])
cyc_pct = 100 * cyc[:, 0]
pc_pct = 100 * cyc[:, 13]

print("\n-- output cycle, %, by quarter --")
for s, v in zip(q, cyc_pct):
    if 1979 <= float(s[:4]) <= 1993:
        print("  %s %+6.2f" % (s, v))

print("\n-- episode windows --")
for label, lo_, hi_ in [("early 1980s", 1980, 1984), ("early 1990s", 1987, 1993),
                        ("early 1990s*", 1988, 1993), ("Great Recession", 2007, 2011)]:
    win = np.where((ty >= lo_) & (ty <= hi_))[0]
    p = win[np.argmax(cyc_pct[win])]
    t_ = win[np.argmin(cyc_pct[win])]
    back = next((j for j in range(t_, T) if cyc_pct[j] >= 0), None)
    below = (back - (p + 1)) if back else None
    print("  %-16s peak %s (%+.2f)  trough %s (%+.2f)  %d qtrs peak->trough"
          % (label, q[p], cyc_pct[p], q[t_], cyc_pct[t_], t_ - p))
    print("                   below trend from %s to %s = %s quarters"
          % (q[p + 1], q[back] if back else "end", below))
    if back is None or ty[back] > hi_ + 12:
        print("                   cycle 1993Q4-2000:", " ".join(
            "%s%+.1f" % (q[j][2:], cyc_pct[j]) for j in range(
                max(t_, int(np.where(q == "1993Q3")[0][0])), min(T, int(np.where(q == "1999Q4")[0][0]) + 1))))

# horizon used in the answers' text (peak 2008Q3 -> back at trend)
t_ = int(np.where(q == "2009Q2")[0][0])
back = next(j for j in range(t_, T) if cyc_pct[j] >= 0)
print("  Great Recession back at/above trend: %s" % q[back])

print("\n-- question 3 correlations (output cycle vs price cycle) --")
for lo_, hi_ in [(2007, 2011), (2008, 2010.75), (1979, 1982), (1978, 1983),
                 (1979, 1983), (1980, 1983), (1979, 1981), (1975.0, 2026.0)]:
    win = np.where((ty >= lo_) & (ty <= hi_))[0]
    print("  %7.4g-%7.4g: corr = %+.3f  (n=%d, output min %+.2f, price min %+.2f)"
          % (lo_, hi_, np.corrcoef(cyc_pct[win], pc_pct[win])[0, 1], len(win),
             cyc_pct[win].min(), pc_pct[win].min()))
win = np.where((ty >= 1979) & (ty <= 1982.75))[0]
print("  price cycle 1979-1982:", " ".join("%s%+.1f" % (q[j][2:], pc_pct[j]) for j in win))
print("  output cycle 1979-1982:", " ".join("%s%+.1f" % (q[j][2:], cyc_pct[j]) for j in win))
print("  corr of first differences 1979-1982: %+.3f"
      % np.corrcoef(np.diff(cyc_pct[win]), np.diff(pc_pct[win]))[0, 1])
print("  corr of log levels 1979-1982: %+.3f"
      % np.corrcoef(raw[win, 0], raw[win, 13])[0, 1])
# where does -0.58 come from? scan every 4-year window in the sample
best = []
for a0 in range(T - 16):
    w = slice(a0, a0 + 17)
    best.append((np.corrcoef(cyc_pct[w], pc_pct[w])[0, 1], q[a0], q[a0 + 16]))
best.sort()
print("  most negative 17-quarter windows:", ["%s-%s %+.2f" % (a, b, c) for c, a, b in best[:4]])
print("  windows closest to -0.58:", sorted(
    ["%s-%s %+.3f" % (a, b, c) for c, a, b in best], key=lambda s: abs(float(s.split()[-1]) + 0.58))[:4])
win = np.where((ty >= 2009) & (ty <= 2009.75))[0]
print("  price cycle within 2009: %s" % ", ".join("%s %+.2f" % (q[j], pc_pct[j]) for j in win))

print("\n-- question 4 --")
k19 = int(np.where(q == "2019Q4")[0][0])
k20 = int(np.where(q == "2020Q2")[0][0])
for j, nm in [(0, "output"), (13, "price"), (8, "hours")]:
    win20 = np.where((ty >= 2020) & (ty <= 2020.75))[0]
    m1 = win20[np.argmin(cyc[:, j][win20])]
    back = next(t for t in range(k20, T) if raw[t, j] >= raw[k19, j])
    print("  %-7s fall 2019Q4->2020Q2 %+.1f%%   cycle low %+.1f%% (%s)   back at 2019Q4 %s"
          % (nm, 100 * (raw[k20, j] - raw[k19, j]), 100 * cyc[m1, j], q[m1], q[back]))

print("\n-- covid magnitudes vs Great Recession --")
print("  output trough depth ratio: %.2f" % (abs(cyc_pct[k20]) / 3.42))
print("  hours/output fall ratio: %.2f" % (24.7 / 14.1))
