from src.utils import config
from src.utils.excel import ExcelUtil

BASE_DIR = config.ConfigUtil.get_value("report_dir")
SCREENSHOT_DIR = f"{BASE_DIR}/screenshot"
REPORT_PATHS = {
    "xls": f"{BASE_DIR}/xls",
    "summary": f"{BASE_DIR}/Summary",
    "doc": f"{BASE_DIR}/doc"
}

testCasepath = config.ConfigUtil.get_value("testCasePath")
LOG_DIR = config.ConfigUtil.get_value("log_dir")

data = ExcelUtil.get_row(testCasepath, "Project", "project_Name")
PROJECT_NAME = ExcelUtil.get_cell(data,"value")