class LoginPage:
    def __init__(self, page):
        self.page = page

    def open_page(self,url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def input_value(self,xpathSring, password):
        self.page.fill(xpathSring, password)

    def click_login(self,xpathSring):
        self.page.click(xpathSring)