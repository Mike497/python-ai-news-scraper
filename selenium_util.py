from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait

from config_util import ConfigUtil


class SeleniumUtil:

    def __init__(self):
        config = ConfigUtil().get_config()

        # Set Chrome options and init WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        # chrome_options.add_argument("--window-size=1024,768")  # Set the window size if not in headless mode (e.g. for debug)
        chrome_service = Service(config['chromedriver']['path'])

        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.find_by_class_query = "return document.getElementsByClassName(\"{}\")[{}];"

    def find_text_in_url_by_class(self, url: str, title_class_name: str, content_class_name: str, index: int,
                                  timeout=10):
        self.driver.get(url)
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.driver.execute_script("return document.readyState") == "complete"
        )
        return self.driver.execute_script(
            self.find_by_class_query.format(title_class_name, index)).text, self.driver.execute_script(
            self.find_by_class_query.format(content_class_name, index)).text

    def __del__(self):
        if self.driver:
            self.driver.quit()
