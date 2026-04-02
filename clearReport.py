import os
import shutil
from src.utils.yaml import BASE_DIR

def clean_folder(folder_path):
    """清空文件夹下所有文件和子文件夹，保留文件夹本身"""
    if not os.path.exists(folder_path):
        print(f"文件夹不存在: {folder_path}")
        return

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
                print(f"删除文件: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"删除文件夹: {item_path}")
        except Exception as e:
            print(f"删除失败 {item_path}: {e}")


if __name__ == "__main__":
    print("开始清空 report 文件夹...")
    # 清空所有子目录
    for sub_dir in ["doc", "screenshot", "Summary", "xls","log"]:
        sub_path_report = os.path.join(BASE_DIR, sub_dir)
        clean_folder(sub_path_report)
        sub_path_log = os.path.join(BASE_DIR, sub_dir)
        clean_folder(sub_path_log)
    print("✅ report 文件夹已清空！")