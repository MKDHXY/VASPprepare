import os
import re

def parse_poscar_counts(lines):
    """
    返回：
    elements: [元素名列表]
    counts:   [对应个数列表]
    coord_start: 坐标起始行号
    """
    elements = lines[5].split()
    counts = list(map(int, lines[6].split()))

    idx = 7
    if lines[idx].strip().lower().startswith("selective"):
        idx += 1
    if lines[idx].strip().lower().startswith(("direct", "cart")):
        idx += 1

    return elements, counts, idx


base_dir = os.getcwd()

for d in os.listdir(base_dir):
    subdir = os.path.join(base_dir, d)
    if not os.path.isdir(subdir):
        continue

    poscar_path = os.path.join(subdir, "POSCAR")
    contcar_path = os.path.join(subdir, "CONTCAR")

    if not (os.path.isfile(poscar_path) and os.path.isfile(contcar_path)):
        continue

    with open(poscar_path, "r") as f:
        pos_lines = f.readlines()

    with open(contcar_path, "r") as f:
        cont_lines = f.readlines()

    # 1️⃣ 用 CONTCAR 前 N 行替换 POSCAR
    n = len(pos_lines)
    new_lines = cont_lines[:n]

    # 2️⃣ 解析元素和坐标起始行
    elements, counts, coord_start = parse_poscar_counts(new_lines)

    total_atoms = sum(counts)
    coord_lines = new_lines[coord_start:coord_start + total_atoms]

    # 3️⃣ 全部先设为 F F F
    coord_lines = [
        re.sub(r"(T\s+T\s+T)", "F   F   F", line)
        if len(line.split()) >= 6 else line
        for line in coord_lines
    ]

    # 4️⃣ 计算需要放开的原子数（非 Ga / Li）
    free_atoms = 0
    for elem, cnt in zip(elements, counts):
        if elem not in ("Ga", "Li"):
            free_atoms += cnt

    # 5️⃣ 从后往前把 F F F → T T T
    changed = 0
    for i in range(len(coord_lines) - 1, -1, -1):
        if changed >= free_atoms:
            break
        if "F   F   F" in coord_lines[i]:
            coord_lines[i] = coord_lines[i].replace(
                "F   F   F", "T   T   T", 1
            )
            changed += 1

    # 写回
    new_lines[coord_start:coord_start + total_atoms] = coord_lines

    with open(poscar_path, "w") as f:
        f.writelines(new_lines)

    print(f"[OK] 已处理: {subdir}")
