import os

# 白名单文件
keep_files = {
    "POTCAR",
    "INCAR",
    "POSCAR",
    "submit.sh",
    "KPOINTS",
}

# 当前目录
base_dir = os.getcwd()

for entry in os.listdir(base_dir):
    subdir_path = os.path.join(base_dir, entry)

    # 只处理子文件夹
    if os.path.isdir(subdir_path):
        for filename in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, filename)

            # 只删除文件（不动子文件夹）
            if os.path.isfile(file_path) and filename not in keep_files:
                try:
                    os.remove(file_path)
                    print(f"已删除: {file_path}")
                except Exception as e:
                    print(f"删除失败: {file_path}，原因: {e}")
