import time

from behave import given, when, then
from playwright.sync_api import expect  # 同步导入

from src.pages.items_page import ItemPage
from src.utils.screenshot import Screenshot


@given("sort all item")
def sort(context):
    ItemPage.sortByValue(context, "Name (Z to A)")
    Screenshot.attach_to_report(
        context,
        name=f"{context.feature.name}_{context.scenario.name}_1"
    )

@when('click "{goods}" and check details')
def clickGoods(context,goods):
    ItemPage.click(context,f'//div[text()="{goods}"]')
    expect(context.page.locator('//*[@id="back-to-products"]')).to_be_visible()
    Screenshot.attach_to_report(
        context,
        name=f"{context.feature.name}_{context.scenario.name}_1"
    )

@when('add in cart')
def addInCart(context):
    ItemPage.add_in_cart(context)
    time.sleep(1)
    Screenshot.attach_to_report(
        context,
        name=f"{context.feature.name}_{context.scenario.name}_1"
    )
    expect(context.page.locator('//*[@id="remove"]')).to_be_visible()

@then('check if "{goods}" is in cart')
def checkInCart(context,goods):
    ItemPage.click(context,'//*[@id="shopping_cart_container"]/a')
    Screenshot.attach_to_report(
        context,
        name=f"{context.feature.name}_{context.scenario.name}_1"
    )
    expect(context.page.locator(f'//div[text()="{goods}"]')).to_be_visible()

@then('back to all items page')
def addInCart(context):
    Screenshot.attach_to_report(
        context,
        name=f"{context.feature.name}_{context.scenario.name}_1"
    )
    ItemPage.click(context,'//*[@id="continue-shopping"]')

@given("enter the cart")
def sort(context):
    ItemPage.click(context, '//*[@id="shopping_cart_container"]/a')
    Screenshot.attach_to_report(
        context,
        name=f"{context.feature.name}_{context.scenario.name}_1"
    )

@when('remove "{goods}"')
def clickGoods(context,goods):
    ItemPage.click(context,f'//div[text()="{goods}"]/ancestor::div[@class="cart_item"]//button')

    Screenshot.attach_to_report(
        context,
        name=f"{context.feature.name}_{context.scenario.name}_1"
    )


@then('check if "{goods}" is removed')
def checkInCart(context,goods):

    expect(context.page.locator(f'//div[text()="{goods}"]')).not_to_be_visible()
    Screenshot.attach_to_report(
        context,
        name=f"{context.feature.name}_{context.scenario.name}_2"
    )
