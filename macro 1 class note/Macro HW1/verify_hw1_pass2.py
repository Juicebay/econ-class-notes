"""Second pass: the specific claims in the written answer that don't match the code."""
import numpy as np
import openpyxl

wb = openpyxl.load_workbook("Assignment1_data.xlsx", read_only=True, data_only=True)
rows = list(wb["Combined"].iter_rows(values_only=True))
data = rows[1:]
q = np.array([r[0] for r in data])
d = np.array([[float(v) for v in r[1:]] for r in data])
T = len(q)
ty = np.array([float(s[:4]) + (float(s[-1]) - 1) / 4 for s in q])

output, nominal = d[:, 60], d[:, 29]
hours, pop, exrate = d[:, 62], d[:, 63], d[:, 64]

lam = 1600
X = np.diag((1 + 6 * lam) * np.ones(T))
X += np.diag(-4 * lam * np.ones(T - 1), 1) + np.diag(-4 * lam * np.ones(T - 1), -1)
X += np.diag(lam * np.ones(T - 2), 2) + np.diag(lam * np.ones(T - 2), -2)
X[0, 0], X[0, 1], X[1, 0], X[1, 1] = 1 + lam, -2 * lam, -2 * lam, 1 + 5 * lam
X[T-1, T-1], X[T-2, T-1], X[T-1, T-2], X[T-2, T-2] = 1 + lam, -2 * lam, -2 * lam, 1 + 5 * lam
hpmat = np.linalg.inv(X)
y = output / pop
price = 100 * nominal / output
raw = np.log(np.column_stack([y, price, hours / pop]))
cyc = raw - hpmat @ raw
cyc_pct = 100 * cyc[:, 0]
pc_pct = 100 * cyc[:, 1]

print("=== (a) Great Recession: is the fall monotone 2008Q3 -> 2009Q2? ===")
i0 = int(np.where(q == "2008Q3")[0][0])
for j in range(i0, i0 + 6):
    print("   %s  log level %.6f  qoq %+.3f%%  cycle %+.2f%%"
          % (q[j], raw[j, 0], 100 * (raw[j, 0] - raw[j - 1, 0]), cyc_pct[j]))

print("\n=== (b) early 1990s: cycle 1988-1998 ===")
for j in range(int(np.where(q == "1988Q1")[0][0]), int(np.where(q == "1998Q4")[0][0]) + 1):
    print("   %s %+6.2f%%" % (q[j], cyc_pct[j]))

print("\n=== (c) quarters below trend, peak -> first quarter at/above trend ===")
for label, pk, tr in [("early 1980s", "1981Q2", "1982Q4"), ("early 1990s", "1989Q1", "1992Q2"),
                      ("early 1990s (peak 1988Q2)", "1988Q2", "1992Q2"),
                      ("early 1990s (peak 1990Q1)", "1990Q1", "1992Q2"),
                      ("Great Recession", "2008Q3", "2009Q2")]:
    p = int(np.where(q == pk)[0][0])
    t_ = int(np.where(q == tr)[0][0])
    back = next((j for j in range(t_, T) if cyc_pct[j] >= 0), None)
    below = int(np.sum(cyc_pct[p+1:back] < 0)) if back else None
    print("   %-27s peak %s trough %s (%d qtrs)  back at trend %s  quarters below trend %s"
          % (label, pk, tr, t_ - p, q[back], below))

print("\n=== (d) question 4: percent changes, log vs exact ===")
k19 = int(np.where(q == "2019Q4")[0][0])
k20 = int(np.where(q == "2020Q2")[0][0])
for j, nm in [(0, "output"), (1, "price"), (2, "hours")]:
    logchg = 100 * (raw[k20, j] - raw[k19, j])
    exact = 100 * (np.exp(raw[k20, j] - raw[k19, j]) - 1)
    print("   %-7s log %+.2f%%   exact %+.2f%%   ratio hours/output(exact) later" % (nm, logchg, exact))
print("   hours exact / output exact = %.2f" % ((np.exp(raw[k20, 2] - raw[k19, 2]) - 1) /
                                                (np.exp(raw[k20, 0] - raw[k19, 0]) - 1)))

print("\n=== (e) last-quarter aggregates vs the raw monthly CSVs ===")
import csv


def read_csv(path):
    out = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('"COL'):
            continue
        a, b = line.split(",")
        out.append((a, float(b)))
    return out


hrs = read_csv("hours_worked_V4391505_monthly.csv")
pp = read_csv("population_v1_quarterly.csv")
fx1 = read_csv("exchangerate_V37426_1976-2016_monthly.csv")
fx2 = read_csv("exchangerate_V111666275_2017-2026_monthly.csv")
fx = dict(fx1 + fx2)
for yr, qs, months in (("2019", "1", ["01", "02", "03"]), ("2020", "2", ["04", "05", "06"]),
                       ("2026", "2", ["04", "05", "06"])):
    s = sum(v for (m, v) in hrs if m.startswith(yr + "-") and m[5:] in months)
    f = np.mean([fx["%s-%s" % (yr, m)] for m in months])
    row = int(np.where(q == "%sQ%s" % (yr, qs))[0][0])
    print("   %sQ%s  hours csv sum %.0f  xlsx %.0f  |  fx csv avg %.6f  xlsx %.6f"
          % (yr, qs, s, hours[row], f, exrate[row]))
print("   population csv 2026-04 = %.0f, xlsx 2026Q2 = %.0f"
      % ([v for m, v in pp if m == "2026-04"][0], pop[int(np.where(q == "2026Q2")[0][0])]))
