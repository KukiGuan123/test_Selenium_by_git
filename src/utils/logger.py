# ==============================
# 日志工具类（追加模式，不删除历史）
# ==============================
import logging
import os
from datetime import datetime
from src.utils.yaml import LOG_DIR

class Logger:
    def __init__(self):
        self.logger = logging.getLogger("test_framework")
        self.logger.setLevel(logging.INFO)

        # 防止重复添加 handler（关键！）
        if self.logger.handlers:
            return

        # ======================
        # 格式定义
        # ======================
        fmt = "%(asctime)s - %(levelname)s - %(message)s"
        date_fmt = "%Y-%m-%d %H:%M:%S"

        # ======================
        # 1. 文件输出（追加模式 a = append）
        # 🔥 关键：mode="a" 不会删除旧日志
        # ======================
        log_file = os.path.join(LOG_DIR, f"behave_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="a")
        file_handler.setFormatter(logging.Formatter(fmt, date_fmt))

        # ======================
        # 2. 控制台彩色输出
        # ======================
        class ColorFormatter(logging.Formatter):
            def format(self, record):
                msg = super().format(record)
                if record.levelno == logging.INFO:
                    return f"\033[94m{msg}\033[0m"
                elif record.levelno == logging.ERROR:
                    return f"\033[91m{msg}\033[0m"
                return msg

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter(fmt, date_fmt))

        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)


    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)