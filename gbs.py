import os
import math

# ===== 常数 =====
KB = 8.617333262e-5  # eV/K
T = 298.15
kBT = KB * T

results = []

for root, dirs, files in os.walk("."):
    if "OUTCAR" not in files:
        continue

    outcar = os.path.join(root, "OUTCAR")

    toten = None
    freqs_mev = []

    with open(outcar, "r", errors="ignore") as f:
        for line in f:
            # ---- TOTEN ----
            if "free  energy   TOTEN" in line:
                try:
                    toten = float(line.split()[-2])
                except:
                    pass

            # ---- 振动频率（忽略虚频）----
            if " f  =" in line and "f/i" not in line:
                try:
                    mev = float(line.split()[-2])
                    freqs_mev.append(mev)
                except:
                    pass

    if toten is None or len(freqs_mev) == 0:
        continue

    # ===== 计算 =====
    sum_mev = sum(freqs_mev)
    zpe = 0.5 * sum_mev / 1000.0  # eV

    thermal = 0.0
    for mev in freqs_mev:
        e = mev / 1000.0
        thermal += kBT * math.log(1.0 - math.exp(-e / kBT))

    G = toten + zpe + thermal

    folder = os.path.basename(os.path.normpath(root))
    results.append((folder, toten, zpe, G, len(freqs_mev)))

# ===== 排序（按文件夹名）=====
results.sort(key=lambda x: x[0])

# ===== REPORT =====
print("REPORT (DFT + harmonic vib, ignore f/i)")
print("folder\tmodes\tTOTEN(eV)\tZPE(eV)\tG(eV)")
for r in results:
    print(f"{r[0]}\t{r[4]}\t{r[1]:.6f}\t{r[2]:.6f}\t{r[3]:.6f}")

# ===== Excel 可粘贴区 =====
print("\n==== EXCEL_COLUMNS ====")
print("TOTEN(eV)")
for r in results:
    print(f"{r[1]:.8f}")

print("\nZPE(eV)")
for r in results:
    print(f"{r[2]:.8f}")

print("\nG(eV)")
for r in results:
    print(f"{r[3]:.8f}")
