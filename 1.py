import os
import shutil

# 当前目录
base_dir = os.getcwd()

# 源 INCAR（和脚本同目录）
source_incar = os.path.join(base_dir, "INCAR")

if not os.path.isfile(source_incar):
    raise FileNotFoundError("当前目录下未找到 INCAR 文件")

for entry in os.listdir(base_dir):
    subdir_path = os.path.join(base_dir, entry)

    # 只处理子文件夹
    if os.path.isdir(subdir_path):
        target_incar = os.path.join(subdir_path, "INCAR")

        try:
            shutil.copy2(source_incar, target_incar)
            print(f"已复制并覆盖: {target_incar}")
        except Exception as e:
            print(f"处理失败: {target_incar}，原因: {e}")
