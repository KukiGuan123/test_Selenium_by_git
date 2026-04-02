import os
import subprocess
import sys

# 强制切换终端编码
os.system("chcp 65001")
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

if __name__ == '__main__':
    result = subprocess.run([
        sys.executable, "-m", "behave"
    ])

    if result.returncode == 0:
        print("\n✅ 测试执行完成！")
        print("📊 Excel / Word 报告已在 outputs 文件夹生成")
    else:
        print("\n❌ 测试执行失败！")