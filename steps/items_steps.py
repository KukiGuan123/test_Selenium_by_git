import time
from behave import given, when, then
from playwright.sync_api import expect  # 同步导入
from src.pages.base_action import BasePage
from src.utils.excel import ExcelUtil
from src.utils.screenshot import Screenshot
from src.utils.yaml import testCasePath


@given("sort all item")
def sort(context):
    BasePage.select_by_value(context, '//*[@id="header_container"]//select[@class="product_sort_container"]',"Name (Z to A)")
    Screenshot.attach_to_report(context, name=f"{context.feature.name}_{context.scenario.name}_1")

@when('click "{goods}" and check details')
def clickGoods(context,goods):
    BasePage.click(context,f'//div[text()="{goods}"]')
    expect(context.page.locator('//*[@id="back-to-products"]')).to_be_visible()
    Screenshot.attach_to_report(context, name=f"{context.feature.name}_{context.scenario.name}_1")

@when('add in cart')
def addInCart(context):
    BasePage.click(context,'//*[@id="add-to-cart"]')
    time.sleep(1)
    Screenshot.attach_to_report(context, name=f"{context.feature.name}_{context.scenario.name}_1")
    expect(context.page.locator('//*[@id="remove"]')).to_be_visible()

@then('check if "{goods}" is in cart')
def checkInCart(context,goods):
    BasePage.click(context,'//*[@id="shopping_cart_container"]/a')
    Screenshot.attach_to_report(context, name=f"{context.feature.name}_{context.scenario.name}_1")
    expect(context.page.locator(f'//div[text()="{goods}"]')).to_be_visible()

@then('back to all items page')
def addInCart(context):
    Screenshot.attach_to_report(context,name=f"{context.feature.name}_{context.scenario.name}_1")
    BasePage.click(context,'//*[@id="continue-shopping"]')

@given("enter the cart")
def sort(context):
    BasePage.click(context,'//*[@id="shopping_cart_container"]/a')
    Screenshot.attach_to_report(context,name=f"{context.feature.name}_{context.scenario.name}_1")

@when('remove "{goods}"')
def removeGoods(context,goods):
    BasePage.click(context,f'//div[text()="{goods}"]/ancestor::div[@class="cart_item"]//button')
    Screenshot.attach_to_report(context,name=f"{context.feature.name}_{context.scenario.name}_1")


@then('check if "{goods}" is removed')
def checkInCart(context,goods):
    expect(context.page.locator(f'//div[text()="{goods}"]')).not_to_be_visible()
    Screenshot.attach_to_report(context,name=f"{context.feature.name}_{context.scenario.name}_1")

@when('enter checkout page')
def enterCheckout(context):
    BasePage.click(context,f'//*[@id="checkout"]')
    Screenshot.attach_to_report(context,name=f"{context.feature.name}_{context.scenario.name}_1")

@then('inpput "{user}" and finish')
def checkInCart(context,user):
    missCol = ExcelUtil.get_cell(testCasePath, "Checkout",user, "missCol")
    fisrtName = ExcelUtil.get_cell(testCasePath, "Checkout", user, "First Name")
    lastName = ExcelUtil.get_cell(testCasePath, "Checkout", user, "Last Name")
    zipCode = ExcelUtil.get_cell(testCasePath, "Checkout", user, "Postal Code")

    if fisrtName is not None:
        BasePage.input(context,'//*[@id="first-name"]',fisrtName)

    if lastName is not None:
        BasePage.input(context,'//*[@id="last-name"]',lastName)

    if zipCode is not None:
        BasePage.input(context, '//*[@id="postal-code"]', zipCode)

    Screenshot.attach_to_report(context, name=f"{context.feature.name}_{context.scenario.name}_1")
    BasePage.click(context,'//*[@id="continue"]')

    if missCol is not None:
        expect(context.page.locator(f'//h3[contains(text(),"{missCol}")]')).to_be_visible()
    else:
        expect(context.page.locator('// span[text() = "Checkout: Overview"]')).to_be_visible()

    Screenshot.attach_to_report(context,name=f"{context.feature.name}_{context.scenario.name}_2")
