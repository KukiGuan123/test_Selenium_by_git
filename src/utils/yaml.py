from src.utils import config
from src.utils.excel import ExcelUtil
from src.utils.logger import Logger

# 测试用例路径
testCasePath = config.ConfigUtil.get_value("testCasePath")

# 项目名字
PROJECT_NAME = ExcelUtil.get_cell(testCasePath, "Project", "project_Name","value")

# 邮箱配置
smtp_server = ExcelUtil.get_cell(testCasePath, "Project","smtp_server","value")
smtp_port = ExcelUtil.get_cell(testCasePath, "Project","smtp_port","value")
from_email = ExcelUtil.get_cell(testCasePath, "Project","from_email","value")
password = ExcelUtil.get_cell(testCasePath, "Project","password","value")
to_email = ExcelUtil.get_cell(testCasePath, "Project","to_email","value")

# 报告路径
BASE_DIR = config.ConfigUtil.get_value("report_dir")
SCREENSHOT_DIR = f"{BASE_DIR}/screenshot"   # 截图路径
REPORT_PATHS = {
                "xls": f"{BASE_DIR}/xls",
                "summary": f"{BASE_DIR}/Summary",
                "doc": f"{BASE_DIR}/doc"
                }  # 测试报告路径
LOG_DIR = config.ConfigUtil.get_value("log_dir")  # 日志路径


detailExcelReport = "详细Excel报告"
detailWordReport =  "详细Word报告"
summaryExcelReport =  "总结报告"

logger = Logger()