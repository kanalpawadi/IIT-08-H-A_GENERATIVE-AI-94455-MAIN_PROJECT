from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# start selenium browser session
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 20)

driver.get("https://www.sunbeaminfo.in/internship")

# create text file
file = open("Sunbeam_internship_data.txt", "w", encoding="utf-8")


def write(text="", indent=0):
    line = ("    " * indent) + text
    file.write(line + "\n")
    print(line)


def main_info():
    main_info = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='minHeightDiv']//div[@id='internship']//div[@class='container']//div[@class='col-xs-12 col-sm-7 col-md-8']//div[@class='main_info wow fadeInUp']")
        )
    )
    write(main_info.text.strip())
    write()


def dropOne():

    def clean(text):
        return " ".join(text.split())

    plus_button1 = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseOneA']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button1)
    plus_button1.click()

    title = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='#collapseOneA']"))
    )
    write("\n" + title.text.strip())

    list_style = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='collapseOneA']//div[@class='col-xs-12']//div[@class='list_style']")
        )
    )

    paragraph_uls = list_style.find_elements(By.XPATH, ".//ul[not(descendant::table)]")
    for ul in paragraph_uls:
        write(ul.text.strip(), indent=1)

    table_title = list_style.find_element(By.XPATH, ".//table/tbody/tr[1]").text.strip()
    write("\n" + table_title, indent=1)

    table_rows = list_style.find_elements(By.XPATH, ".//ul/table/tbody/tr")
    for row in table_rows[2:]:
        cols = row.find_elements(By.XPATH, ".//td")
        info_new = {
            "Sr.no": clean(cols[0].text),
            "Duration": clean(cols[1].text),
            "Structure": clean(cols[2].text),
            "Mode": clean(cols[3].text)
        }
        for k, v in info_new.items():
            write(f"{k}: {v}", indent=2)
        write()


def dropTwo():
    plus_button2 = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseTwo']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button2)
    plus_button2.click()

    title = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='#collapseTwo']"))
    )
    write("\n" + title.text.strip())

    list_style = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='collapseTwo']//div[@class='col-xs-12']//div[@class='list_style']")
        )
    )

    lis = list_style.find_elements(By.XPATH, ".//ul/li")
    for li in lis:
        write(li.text.strip(), indent=1)


def dropFour():
    plus_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseFour']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
    plus_button.click()

    title = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='#collapseFour']"))
    )
    write("\n" + title.text.strip())

    list_style = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='collapseFour']//div[@class='col-xs-12']//div[@class='list_style']")
        )
    )

    for li in list_style.find_elements(By.XPATH, ".//ul/li"):
        write(li.text.strip(), indent=1)

    for para in list_style.find_elements(By.XPATH, ".//ul/p"):
        write(para.text.strip(), indent=1)


def dropSix():
    plus_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
    plus_button.click()

    title = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='#collapseSix']"))
    )
    write("\n" + title.text.strip())

    list_style = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='collapseSix']//div[@class='col-xs-12']//div[@class='list_style']")
        )
    )

    head = list_style.find_element(By.XPATH, ".//ul/li")
    write(head.text.strip(), indent=1)

    table_rows = list_style.find_elements(By.XPATH, ".//ul/table/tbody/tr")
    for row in table_rows[1:]:
        cols = row.find_elements(By.XPATH, ".//td")
        info_new = {
            "Technology": cols[0].text.strip(),
            "Aim": cols[1].text.strip(),
            "Prerequisite": cols[2].text.strip(),
            "Learning": cols[3].text.strip(),
            "Location": cols[4].text.strip()
        }
        for k, v in info_new.items():
            write(f"{k}: {v}", indent=2)
        write()


def batch_schedule():
    heading = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='minHeightDiv']//div[@id='internship']//div[@class='container']//div[@class='col-xs-12 col-sm-7 col-md-8']//h4[@style='font-weight:500;']")
        )
    )
    write("\n" + heading.text.strip())

    try:
        table_div = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='table-responsive']")
            )
        )

        rows = table_div.find_elements(By.XPATH, ".//tbody/tr")
        for row in rows:
            cols = row.find_elements(By.XPATH, ".//td")
            info_new = {
                "Sr.no": cols[0].text.strip(),
                "Batch": cols[1].text.strip(),
                "Batch Duration": cols[2].text.strip(),
                "Start Date": cols[3].text.strip(),
                "End Date": cols[4].text.strip(),
                "Time": cols[5].text.strip(),
                "Fees (Rs.)": cols[6].text.strip()
            }
            for k, v in info_new.items():
                write(f"{k}: {v}", indent=2)
            write()
    except:
        write("No Data found")

main_info()
dropOne()
dropTwo()
dropFour()
dropSix()
batch_schedule()

file.close()
driver.quit()
