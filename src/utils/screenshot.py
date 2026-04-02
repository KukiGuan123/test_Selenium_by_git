from datetime import datetime
from src.utils.yaml import SCREENSHOT_DIR

class Screenshot:
    @staticmethod
    def attach_to_report(context, name="screenshot"):
        try:
            img_bytes = context.page.screenshot(full_page=True)
            dt = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            path = f"{SCREENSHOT_DIR}/{name}_{dt}.png"

            with open(path, "wb") as f:
                f.write(img_bytes)

            # 🔥 关键：支持一个步骤无限截图
            if not hasattr(context, "screenshot_multi"):
                context.screenshot_multi = []

            context.screenshot_multi.append(path)
            context.current_screenshot_path = path

            print(f"✅ 截图成功：{path}")
            return path

        except Exception as e:
            print(f"❌ 截图失败: {e}")
            context.current_screenshot_path = None
            return None