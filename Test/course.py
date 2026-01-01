


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_course_data(url, output_file="course_data.txt"):
    """Fetch course info and accordion content from a course page and save to a TXT file."""
    
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    
    try:
        driver.get(url)
        
        with open(output_file, "w", encoding="utf-8") as file:

            # ---------- BASIC COURSE INFO ----------
            info = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "course_info"))
            )
            file.write("===== BASIC INFO =====\n")
            file.write(info.text.strip() + "\n\n")
            print("===== BASIC INFO =====")
            print(info.text.strip())

            # ---------- ACCORDION DATA ----------
            accordion_buttons = wait.until(
                EC.presence_of_all_elements_located((
                    By.XPATH, "//div[@id='accordion']//a[@data-toggle='collapse']"
                ))
            )

            for btn in accordion_buttons:
                title = btn.text.strip()
                file.write(f"\n===== {title.upper()} =====\n")
                print(f"\n===== {title.upper()} =====")

                # Safe click
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                driver.execute_script("arguments[0].click();", btn)

                # Get corresponding content
                collapse_id = btn.get_attribute("href").split("#")[-1]

                panel = wait.until(
                    EC.presence_of_element_located((
                        By.XPATH, f"//div[@id='{collapse_id}']//div[@class='panel-body']"
                    ))
                )

                # Allow animation/render
                time.sleep(0.4)

                text = panel.text.strip()
                file.write(text if text else "No data found")
                file.write("\n\n")
                print(text if text else "No data found")
    
    finally:
        driver.quit()


# Example usage:
fetch_course_data("https://www.sunbeaminfo.in/modular-courses/core-java-classes", "core_java.txt")
fetch_course_data("https://www.sunbeaminfo.in/modular-courses/python-classes-in-pune", "python.txt")
