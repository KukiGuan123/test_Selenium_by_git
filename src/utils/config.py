import yaml
from pathlib import Path
from typing import Any


class ConfigUtil:
    """全局配置工具类：读取 config.yml 任意数据"""

    # 内部缓存，只加载一次
    __config = None

    @staticmethod
    def __load_config() -> dict:
        """加载配置文件（内部用）"""
        if ConfigUtil.__config is not None:
            return ConfigUtil.__config

        try:
            base_path = Path(__file__).resolve().parent.parent  # src/
            config_path = base_path / "config" / "config.yml"

            with open(config_path, "r", encoding="utf-8") as f:
                ConfigUtil.__config = yaml.safe_load(f) or {}
            return ConfigUtil.__config

        except Exception as e:
            raise RuntimeError(f"配置文件加载失败：{str(e)}")

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        获取 一级 配置
        示例：ConfigUtil.get("report")
        """
        config = ConfigUtil.__load_config()
        return config.get(key, default)

    @staticmethod
    def get_value(*keys: str, default: Any = None) -> Any:
        """
        ✅ 获取 任意层级 配置（万能方法）
        示例：
          ConfigUtil.get_value("report", "file_prefix")
          ConfigUtil.get_value("database", "host")
          ConfigUtil.get_value("api", "timeout")
        """
        config = ConfigUtil.__load_config()
        temp = config

        for k in keys:
            if isinstance(temp, dict) and k in temp:
                temp = temp[k]
            else:
                return default

        return temp