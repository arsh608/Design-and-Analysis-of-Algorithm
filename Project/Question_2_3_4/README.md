# Divide & Conquer — Python Solutions

This project contains **complete implementations** and a **nice UI** for:

1. **Closest Pair of Points** — O(*n* log *n*) divide & conquer.
2. **Integer Multiplication (Karatsuba)** — Divide & conquer multiplication for big integers.

It also includes:

- **20 datasets** (10 per problem) with input size **> 100**.
- A batch runner that **applies the algorithms** on all datasets and saves results + plots.
- A **Streamlit app** where you can select any dataset file and **see the algorithms working** (trace + visuals).

---

## Quick Start

```bash
# 1) Create a virtualenv (optional)
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run the UI
streamlit run app_streamlit.py
```

Open the local URL Streamlit prints (usually http://localhost:8501).

> If you prefer desktop UI: `python app_tk.py` (basic Tkinter version).

---

## Datasets (20 files)

- `datasets/closest_pair/points_###.txt`Format:

  ```
  n
  x1 y1
  x2 y2
  ...
  xn yn
  ```
- `datasets/integer_multiplication/ints_###.txt`
  Format: two lines, big integers A then B (each at least 100 digits).

All datasets here were generated with varying sizes (points: 120..500; integers: 128..416 digits).

---

## Batch Runner

```bash
python run_all.py
```

- Produces `outputs/results.csv` with per-dataset timings and sizes.
- Saves plots for each closest-pair dataset to `outputs/plots/*.png`.

---

## What the UI Shows

**Closest Pair:**

Select a `points_*.txt` file.

See the scatter of points and the closest pair highlighted.

Toggle “Show working / trace” to view the divide & conquer steps (merge layers, strip size, etc.).

**Karatsuba Multiplication:**

- Select an `ints_*.txt` file.
- See input sizes (digits) and the product (first/last 120 digits shown).
- Toggle “Show working / trace” to see the recursion structure (depths and split sizes).

---

## Algorithms Overview

- **Closest Pair (Divide & Conquer)**:Split points by median *x*. Recurse on left/right halves to get distances `dL`, `dR`.Merge step scans a vertical **strip** of points within distance `d=min(dL,dR)` from the middle line, checking only nearby neighbors sorted by *y*. Total time: **O(n log n)**.
- **Karatsuba (Divide & Conquer)**:
  Split each integer into high/low halves at base 10^m:
  `a = aH * 10^m + aL`, `b = bH * 10^m + bL`
  Compute `z2=aH*bH`, `z0=aL*bL`, `z1=(aH+aL)*(bH+bL) - z2 - z0`.
  Combine: `z2*10^(2m) + z1*10^m + z0`.
  Time: **O(n^log2(3)) ~ O(n^1.585)**, better than classical O(n^2).

---

## File Tree (important parts)

```
algorithms/
  closest_pair.py
  karatsuba.py

datasets/
  closest_pair/
    points_001.txt ... points_010.txt
  integer_multiplication/
    ints_001.txt   ... ints_010.txt

outputs/
  plots/  # saved PNGs from batch runner

app_streamlit.py   # Main UI
run_all.py         # Applies both algorithms to all datasets
requirements.txt
README.md
```
