from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_course_data(url, output_file="course_data.txt"):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    combined_text = ""   

    try:
        driver.get(url)

        with open(output_file, "w", encoding="utf-8") as file:

            info = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "course_info"))
            )

            basic = info.text.strip()
            combined_text += "BASIC INFO:\n" + basic + "\n\n"
            file.write("Basic Information ..\n" + basic + "\n\n")

            accordion_buttons = wait.until(
                EC.presence_of_all_elements_located((
                    By.XPATH, "//div[@id='accordion']//a[@data-toggle='collapse']"
                ))
            )

            for btn in accordion_buttons:
                title = btn.text.strip()
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                driver.execute_script("arguments[0].click();", btn)

                collapse_id = btn.get_attribute("href").split("#")[-1]

                panel = wait.until(
                    EC.presence_of_element_located((
                        By.XPATH, f"//div[@id='{collapse_id}']//div[@class='panel-body']"
                    ))
                )

                time.sleep(0.4)
                text = panel.text.strip() or "No data found"

                combined_text += f"{title}:\n{text}\n\n"
                file.write(f"{title.upper()}\n{text}\n\n")

    finally:
        driver.quit()

    return combined_text        
 
