import time
from behave import given, when, then
from playwright.sync_api import expect  # 同步导入
from src.pages.base_action import BasePage
from src.utils.excel import ExcelUtil
from src.utils.screenshot import Screenshot
from src.utils.yaml import testCasePath


@given("open the login page")
def step(context):
    BasePage.open_page(context,  ExcelUtil.get_cell(testCasePath, "Project","url", "value"))
    Screenshot.attach_to_report(context, name=f"{context.feature.name}_{context.scenario.name}_1")

@given(u'maximize browser window')
def step_impl(context):
    context.page.set_viewport_size({"width": 1920, "height": 1080})


@when('input user "{userAccount}"')
def step(context, userAccount):

    data = ExcelUtil.get_row(testCasePath, "Login", userAccount)
    user = ExcelUtil.get_cell(data, "username")
    pwd = ExcelUtil.get_cell(data, "password")

    BasePage.input(context,"#user-name", user)
    BasePage.input(context,"#password", pwd)


@when("click login button")
def step(context):
    Screenshot.attach_to_report(context, name=f"{context.feature.name}_{context.scenario.name}_1")
    BasePage.click(context,"#login-button")


@then("login with {status} account")
def step(context, status):

    time.sleep(2)
    if "success" in status:  # ✅ 修正拼写
        assert "inventory" in context.page.url
    else:
        # ✅ 同步断言方法名：to_be_visible()
        expect(context.page.locator(f'//h3[contains(text(), {status})]')).to_be_visible()

    Screenshot.attach_to_report(context, name=f"{context.feature.name}_{context.scenario.name}_1")