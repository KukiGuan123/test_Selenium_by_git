class BasePage:
    def __init__(self, page):
        self.page = page

    def open_page(self,url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def click(self, xpathString):
        self.page.click(xpathString)

    def input(self,xpathString,value):
        self.page.fill(xpathString, value)

    def selectByValue(self, xpathString, value):
        self.page.select_option(xpathString, value)