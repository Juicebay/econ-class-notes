"""ECON*6020 Assignment 2, parts (f) and (g).

Written in a plain loop style so it translates line by line to MATLAB.
Law of motion (from part d), discretized with annual steps:
    k(t+1) = k(t) + s*y(t) - delta*k(t)
    y(t)   = a^(1-alpha) * (L/N)^(b(1-alpha)) * k(t)^(b(1-alpha)+alpha)
"""
import numpy as np
import matplotlib.pyplot as plt

# ---------------- Parameters ----------------
alpha = 1/3
a = 1.0
delta = 0.10
LN = 1.0          # L/N
s = 0.25
T = 100           # years


def output(k, b):
    return a**(1 - alpha) * LN**(b * (1 - alpha)) * k**(b * (1 - alpha) + alpha)


def steady_state(b):
    # s*y = delta*k  ->  k* = [s a^(1-alpha) (L/N)^(b(1-alpha)) / delta]^(1/((1-alpha)(1-b)))
    return (s * a**(1 - alpha) * LN**(b * (1 - alpha)) / delta) ** (1 / ((1 - alpha) * (1 - b)))


def simulate(b, k0):
    k = np.zeros(T + 1)
    y = np.zeros(T + 1)
    k[0] = k0
    for t in range(T):
        y[t] = output(k[t], b)
        k[t + 1] = k[t] + s * y[t] - delta * k[t]
    y[T] = output(k[T], b)
    g = y[1:] / y[:-1] - 1          # growth rate of income per capita, years 1..T
    return k, y, g


# ---------------- Part (f) ----------------
kss0 = steady_state(0)
k0 = kss0 / 4
print(f"(f) b=0:   k* = {kss0:.4f},  k0 = k*/4 = {k0:.4f}")
print(f"    b=1/2: k* = {steady_state(0.5):.4f}  (same k0)")

k_b0, y_b0, g_b0 = simulate(0.0, k0)
k_b5, y_b5, g_b5 = simulate(0.5, k0)

years = np.arange(1, T + 1)
for name, g in [("b=0", g_b0), ("b=1/2", g_b5)]:
    print(f"    {name:6s} growth: year 1 = {100*g[0]:.2f}%, year 10 = {100*g[9]:.2f}%, "
          f"year 50 = {100*g[49]:.2f}%, year 100 = {100*g[99]:.2f}%")

plt.figure(figsize=(7, 4))
plt.plot(years, 100 * g_b0, label="b = 0")
plt.plot(years, 100 * g_b5, label="b = 1/2")
plt.xlabel("Year")
plt.ylabel("Growth rate of income per capita (%)")
plt.title("Part (f): growth paths from k0 = k*(b=0)/4")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("hw2_f_growth.png", dpi=150)

# ---------------- Part (g) ----------------
# b=0: c = y - delta*k, max over k:  alpha*k^(alpha-1) = delta
k_gold = (alpha * a**(1 - alpha) / delta) ** (1 / (1 - alpha))
s_gold = delta * k_gold / output(k_gold, 0)    # equals alpha
print(f"(g) k_gold = {k_gold:.4f},  s_gold = {s_gold:.4f},  k*(s=0.25) = {kss0:.4f}")
print("    s < s_gold, so k* < k_gold: dynamically efficient." if s < s_gold
      else "    s > s_gold: dynamically inefficient.")
