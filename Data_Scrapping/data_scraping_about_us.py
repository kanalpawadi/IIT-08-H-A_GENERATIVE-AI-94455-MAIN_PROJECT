from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AboutUsScraper:
    def __init__(self, url = "https://www.sunbeaminfo.in/about-us"):
        self.url = url
        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, 10)

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        return driver

    def open_page(self):
        self.driver.get(self.url)
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

    def fetch_main_about_text(self):

        data = []

        division = self.driver.find_element(By.ID, "about_us_page")
        area = division.find_element(By.CSS_SELECTOR, ".main_info")

        paragraphs = area.find_elements(By.TAG_NAME, "p")
        for p in paragraphs:
            text = p.text.strip()
            if text:
                # print(text)
                data.append(text)
        
        return data

    def fetch_title_bar_text(self):
        title_bar = self.driver.find_element(
            By.CSS_SELECTOR, ".about_other_data.accordion_outer_box"
        )
        panel_title = title_bar.find_element(By.CSS_SELECTOR, ".panel-title")
        title_text = panel_title.find_element(By.TAG_NAME, "a")


        title = title_text.text.strip()
        # print("\n")
        # print(title)
        return title
        

    def fetch_plus_button_content(self):
        data = []

        plus_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapse4']"))
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", plus_button
        )
        plus_button.click()

        div = self.wait.until(
            EC.presence_of_element_located((By.ID, "collapse4"))
        )

        text_area = div.find_element(
            By.CSS_SELECTOR,
            ".col-xs-12.col-sm-12.col-md-12 .list_style"
        )

        paragraphs = text_area.find_elements(By.TAG_NAME, "p")
        for p in paragraphs:
            text = p.text.strip()
            if text:
                # print(text)
                data.append(text)
        
        return data

    def close(self):
        self.driver.quit()


    def run(self):
        self.open_page()

        # result = {
        #     "main_about": self.fetch_main_about_text(),
        #     "title": self.fetch_title_bar_text(),
        #     "details": self.fetch_plus_button_content(),
        # }

        result = []
        result.extend(self.fetch_main_about_text())
        result.append(self.fetch_title_bar_text())
        result.extend(self.fetch_plus_button_content())

        self.close()
        return result

