import os
import time
from playwright.sync_api import sync_playwright
from behave.model import Status

from src.utils.send_email import send_email_with_batch_files
from src.utils.yaml import logger, summaryExcelReport
from src.utils import screenshot
from src.utils.reportGenerator import ReportGenerator
from src.utils.yaml import REPORT_PATHS, LOG_DIR, SCREENSHOT_DIR, PROJECT_NAME

report = ReportGenerator()
for path in [LOG_DIR, SCREENSHOT_DIR, *REPORT_PATHS.values()]:
    os.makedirs(path, exist_ok=True)

playwright = None
browser = None
current_feature = ""
current_scenario = ""

test_results = []
pass_count = 0
fail_count = 0
skip_count = 0


def before_all(context):
    global playwright, browser
    global pass_count, fail_count, skip_count, test_results
    pass_count = 0
    fail_count = 0
    skip_count = 0
    test_results = []

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
    logger.info("\n" + "=" * 120)
    logger.info(f"Scenario :{current_scenario}")
    context._scenario_start_time = time.time()
    context._scenario_failed = False


def before_step(context, steps):
    context._step_start_time = time.time()


def after_step(context, step):
    cost_time = time.time() - context._step_start_time
    cost_str = f"{cost_time:.3f}s"

    if context._scenario_failed:
        result = "Skip"
        error = "skipped because previous step failed"
    else:
        if step.status == Status.passed:
            result = "Pass"
            error = ""
        else:
            result = "Fail"
            error = str(step.exception)[:200] if step.exception else ""
            context._scenario_failed = True

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
    elif result == "Skip":
        logger.info(f"⏭️ {step.name} | SKIP")
    else:
        logger.error(f"❌ {step.name} | FAIL | {error}")


def after_scenario(context, scenario):
    global pass_count, fail_count, skip_count, test_results

    if scenario.status == "failed":
        pic = screenshot.Screenshot.attach_to_report(context, f"{current_feature}_{current_scenario}_fail")
        context.current_screenshot_path = pic
        logger.error(f"📸 失败已截图：{current_scenario}")

    # ====================== 🔥 强制补写所有未执行步骤为 SKIP（核心代码）======================
    for step in scenario.steps:
        step_name = f"{step.keyword} {step.name}"
        found = False
        for s in report.all_steps:
            if s["scenario"] == current_scenario and s["step"] == step_name:
                found = True
                break
        if not found:
            report.add_step(
                feature=current_feature,
                scenario=current_scenario,
                step=step_name,
                result="Skip",
                error="前置步骤失败，跳过执行",
                pic_path=None
            )

    # 统计
    if scenario.status == Status.passed:
        pass_count += 1
    elif scenario.status == Status.failed:
        fail_count += 1
        failed_step_obj = next((s for s in scenario.steps if s.status == Status.failed), None)
        failed_step = f"{failed_step_obj.keyword} {failed_step_obj.name}" if failed_step_obj else ""
        error_msg = str(failed_step_obj.exception)[:200] if failed_step_obj and failed_step_obj.exception else ""
        test_results.append({
            "feature": current_feature,
            "scenario": current_scenario,
            "result": "Fail",
            "failed_step": failed_step,
            "error": error_msg
        })
    elif scenario.status == Status.skipped:
        skip_count += 1


def after_feature(context, feature):
    context.page.close()
    logger.info(f"✅ Feature 完成：{feature.name}，浏览器已关闭")


def after_all(context):
    xls = report._save_excel()
    doc = report._save_word()
    sum_xls = f"{REPORT_PATHS['summary']}/{PROJECT_NAME}_{summaryExcelReport}_{report.time_str}.xlsx"

    logger.info("=" * 80)
    logger.info("✅ 测试完成，报告已生成：")
    logger.info(f"📊 详细Excel: {xls}")
    logger.info(f"📊 总结Excel: {sum_xls}")
    logger.info(f"📄 Word报告: {doc}")
    logger.info("=" * 80)

    total_count = pass_count + fail_count + skip_count
    logger.info(f"📊 最终统计：Scenario总数={total_count} | 成功={pass_count} | 失败={fail_count} | 跳过={skip_count}")

    files = [xls, sum_xls, doc]
    send_email_with_batch_files(
        file_list=files,
        test_results=test_results,
        pass_count=pass_count,
        fail_count=fail_count,
        skip_count=skip_count
    )

    browser.close()
    playwright.stop()