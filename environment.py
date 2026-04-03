import os
import time
from playwright.sync_api import sync_playwright

from src.utils.send_email import send_email_with_batch_files
from src.utils.yaml import logger, summaryExcelReport
from src.utils import screenshot
from src.utils.reportGenerator import ReportGenerator
from src.utils.yaml import REPORT_PATHS, LOG_DIR, SCREENSHOT_DIR, PROJECT_NAME

report = ReportGenerator()
# 自动创建目录
for path in [LOG_DIR, SCREENSHOT_DIR, *REPORT_PATHS.values()]:
    os.makedirs(path, exist_ok=True)


playwright = None
browser = None
current_feature = ""
current_scenario = ""


def before_all(context):
    global playwright, browser
    logger.info("=" * 60)
    logger.info("🚀 开始执行自动化测试")
    logger.info("=" * 60)
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)

def before_feature(context, feature):
    global current_feature
    current_feature = feature.name
    logger.info(f"\n📦 Feature: {current_feature}")
    context.page = browser.new_page()
    context.screenshot_multi = []

def before_scenario(context, scenario):
    global current_scenario
    current_scenario = scenario.name
    logger.info("\n"+"=" * 140 )
    logger.info( f"Scenario :{current_scenario}" )

    # ✅ Scenario 开始计时
    context._scenario_start_time = time.time()


def before_step(context,steps):
    context._step_start_time = time.time()  # 记录开始时间


# ✅ 步骤结束 → 你的日志先输出
def after_step(context, step):
    cost_time = time.time() - context._step_start_time
    cost_str = f"{cost_time:.3f}s"

    result = "Pass" if step.status == "passed" else "Fail"
    error = str(step.exception)[:200] if step.exception else ""
    step_name = f"{step.keyword} {step.name}"

    pic_list = getattr(context, "screenshot_multi", [])
    if pic_list:
        combined_pic = ";".join(pic_list)
        report.add_step(current_feature, current_scenario, step_name, result, error, combined_pic)
        context.screenshot_multi.clear()
    else:
        pic = getattr(context, "current_screenshot_path", None)
        report.add_step(current_feature, current_scenario, step_name, result, error, pic)

    if result == "Pass":
        logger.info(f"✅ {step.name} | PASS | 耗时 {cost_str}")
    else:
        logger.error(f"❌ {step.name} | FAIL | {error} | 耗时 {cost_str}")


def after_scenario(context, scenario):
    if scenario.status == "failed":
        pic = screenshot.Screenshot.attach_to_report(context,  f"{current_feature}_{current_scenario}_fail")
        context.current_screenshot_path = pic
        logger.error(f"📸 失败已截图：{current_scenario}")

def after_feature(context, feature):
    context.page.close()
    logger.info(f"✅ Feature 完成：{feature.name}，浏览器已关闭")


def after_all(context):
    xls = report._save_excel()
    doc = report._save_word()
    sum_xls = f"{REPORT_PATHS['summary']}/{PROJECT_NAME}_{summaryExcelReport}_{report.time_str}.xlsx"

    logger.info( "=" * 80)
    logger.info("✅ 测试完成，报告已生成：")
    logger.info(f"📊 详细Excel: {xls}")
    logger.info(f"📊 总结Excel: {sum_xls}")
    logger.info(f"📄 Word报告: {doc}")
    logger.info( "=" * 80)

    # 发送邮箱
    files = [xls, sum_xls, doc]
    send_email_with_batch_files(files)

    browser.close()
    playwright.stop()