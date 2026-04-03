class BasePage:
    def __init__(self, page):
        self.page = page

    def open_page(self,url):
        """打开页面并等待完全加载"""
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle")
        print(f"✅ [页面打开成功] {url}")

    def click(self, xpathString):
        self.page.click(xpathString)

    def input(self,xpathString,value):
        self.page.fill(xpathString, value)

    def select_by_value(self, xpathString, value):
        self.page.select_option(xpathString, value)