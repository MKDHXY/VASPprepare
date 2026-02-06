import os
import math

# ===== 常数 =====
kB = 8.617333262e-5  # eV/K
T = 293.15           # K

results = []

for root, dirs, files in os.walk("."):
    if "OUTCAR" not in files:
        continue

    ts = 0.0
    count = 0

    with open(os.path.join(root, "OUTCAR"), "r", errors="ignore") as f:
        for line in f:
            # 只要实频
            if " f  =" in line and "f/i" not in line:
                try:
                    # 倒数第二个是 meV
                    energy_meV = float(line.split()[-2])
                except:
                    continue

                # meV → eV
                hv = energy_meV / 1000.0
                x = hv / (kB * T)

                # T*S_i
                ts_i = kB * T * (
                    x / (math.exp(x) - 1.0)
                    - math.log(1.0 - math.exp(-x))
                )

                ts += ts_i
                count += 1

    folder = os.path.basename(os.path.normpath(root))
    results.append((folder, count, ts))

# ===== 输出报告 =====
print("folder\tmodes\tTS_vib(eV)")
for f, n, ts in results:
    print(f"{f}\t{n}\t{ts:.8f}")

# ===== Excel 专用列 =====
print("\n=== EXCEL_TS_COLUMN ===")
for _, _, ts in results:
    print(f"{ts:.8f}")
