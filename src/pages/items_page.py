class ItemPage:
    def __init__(self, page):
        self.page = page

    def sortByValue(self, optionValue):
        self.page.select_option('//*[@id="header_container"]//select[@class="product_sort_container"]',optionValue)

    def click(self, xpathString):
        self.page.click(xpathString)



    def add_in_cart(self):
        self.page.click('//*[@id="add-to-cart"]')


    def remove_goods(self,goods):
        self.page.click(f'//div[text()="{goods}"]/ancestor::div[@class="cart_item"]')





