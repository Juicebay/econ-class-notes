"""Example 1 — generating random data from a model.

Run:  .venv/bin/python examples/ex1_generate_data.py
"""
import numpy as np
import pandas as pd

# ---- 1. A random number generator with a seed (same numbers every run) ----
rng = np.random.default_rng(123)

# ---- 2. Draw random variables -----------------------------------------------
n = 5
a = rng.uniform(low=3, high=5, size=n)        # Uniform(3, 5)
e = rng.normal(loc=0, scale=1, size=n)        # N(0, 1)
e2 = rng.normal(loc=0, scale=2, size=n)       # N(0, 4)  -> scale is the SD, not variance
print("uniform draws:", a)
print("normal draws :", e)

# ---- 3. Element-wise math on arrays (no loops needed) -----------------------
print("a squared    :", a ** 2)               # power:   **
print("a^0.3        :", a ** 0.3)
print("log(a)       :", np.log(a))            # natural log
print("exp(a)       :", np.exp(a))

# ---- 4. Build y from a made-up nonlinear model ------------------------------
#      y = c * exp(d * z) + e ,   c = 2, d = 0.5
n = 100
z = rng.uniform(0, 1, size=n)
e = rng.normal(0, 1, size=n)
c, d = 2.0, 0.5
y = c * np.exp(d * z) + e

# ---- 5. Put it in a table to look at it ------------------------------------
df = pd.DataFrame({"y": y, "z": z, "e": e})
print(df.head())
print(df.describe())

# ---- 6. Stack columns into a matrix -----------------------------------------
X = np.column_stack([np.ones(n), z])          # n x 2 matrix: constant and z
print("X shape:", X.shape)                    # (100, 2)

# ---- 7. Repeat for several sample sizes with a loop -------------------------
for n in [50, 100, 200]:
    z = rng.uniform(0, 1, size=n)
    y = c * np.exp(d * z) + rng.normal(size=n)
    print(f"n = {n:3d}   mean of y = {y.mean():.3f}")
