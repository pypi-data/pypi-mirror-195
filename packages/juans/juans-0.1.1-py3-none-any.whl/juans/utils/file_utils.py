import os


def get_folder_size(dir_path="."):
    """获取dir_path文件夹下所有文件的大小, 单位为MB"""
    size = 0
    for path, dirs, files in os.walk(dir_path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    return round(size / 1024 / 1024, 2)


def list_files(dir_path, suffix=["jfif", "jpg", "png", "jpeg"]):
    """获取dir_pathwen文件夹及子文件夹下所有满足suffix尾缀的文件名"""
    file_names = []
    # root是subfolder
    # files 是subfolder下所有的file names
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.split(".")[-1] in suffix:
                file_names.append(os.path.join(root, file))
    return file_names
