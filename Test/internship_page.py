from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# start selenium browser session
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options = chrome_options)

wait = WebDriverWait(driver, 20)

# load desired page in the browser
driver.get("https://www.sunbeaminfo.in/internship")

def main_info():

    main_info = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='minHeightDiv']//div[@id='internship']//div[@class='container']//div[@class='col-xs-12 col-sm-7 col-md-8']//div[@class='main_info wow fadeInUp']")
            )
        )

    print(main_info.text.strip())
    data = main_info.text.strip()



def dropOne():

    def clean(text):
        return " ".join(text.split())

    plus_button1 = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseOneA']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button1)
    plus_button1.click()

    dropOneTitle = list_style= wait.until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='#collapseOneA']"))
    )

    print(dropOneTitle.text.strip())

    list_style= wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='collapseOneA']//div[@class='col-xs-12']//div[@class='list_style']"))
    )

    paragraph_uls = list_style.find_elements(By.XPATH, ".//ul[not(descendant::table)]")

    for ul in paragraph_uls:
            print(ul.text.strip())

    table_title = list_style.find_element( By.XPATH, ".//table/tbody/tr[1]").text.strip()

    print(table_title)

    table_rows = list_style.find_elements(By.XPATH, ".//ul/table/tbody/tr")

    for row in table_rows[2:]: 
        cols = row.find_elements(By.XPATH, './/td')

        info_new = {
            "Sr.no": clean(cols[0].text),
            "Duration": clean(cols[1].text),
            "Structure": clean(cols[2].text),
            "Mode": clean(cols[3].text)
        }
        print(info_new)
    
    




def dropTwo():
    plus_button2 = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseTwo']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button2)
    plus_button2.click()

    dropTwoTitle = list_style= wait.until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='#collapseTwo']"))
    )

    print(dropTwoTitle.text.strip())


    list_style = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='collapseTwo']//div[@class='col-xs-12']//div[@class='list_style']"))
    )

    lis = list_style.find_elements(By.XPATH, ".//ul/li")

    for li in lis:
        print(li.text.strip())



def dropFour():
    plus_button2 = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseFour']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button2)
    plus_button2.click()

    dropFourTitle = list_style= wait.until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='#collapseFour']"))
    )

    print(dropFourTitle.text.strip())

    list_style = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='collapseFour']//div[@class='col-xs-12']//div[@class='list_style']"))
    )

    lists = list_style.find_elements(By.XPATH, ".//ul/li")

    paras = list_style.find_elements(By.XPATH, ".//ul/p")

    for li in lists:
        print(li.text.strip())

    for para in paras:
        print(para.text.strip())


def dropSix():
    plus_button2 = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button2)
    plus_button2.click()

    dropSixTitle = list_style= wait.until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='#collapseSix']"))
    )

    print(dropSixTitle.text.strip())

    list_style = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='collapseSix']//div[@class='col-xs-12']//div[@class='list_style']"))
    )

    head = list_style.find_element(By.XPATH, ".//ul/li")

    print(head.text.strip())

    table_rows = list_style.find_elements(By.XPATH, ".//ul/table/tbody/tr")
        
    for row in table_rows[1:]: 
        cols = row.find_elements(By.XPATH, './/td')

        info_new = {
            "Technology": cols[0].text.strip(),
                "Aim": cols[1].text.strip(),
                "Prerequisite": cols[2].text.strip(),
                "Learning": cols[3].text.strip(),
                "Location": cols[4].text.strip()
        }
        print(info_new)


def batch_schedule():
    heading = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='minHeightDiv']//div[@id='internship']//div[@class='container']//div[@class='col-xs-12 col-sm-7 col-md-8']//h4[@style='font-weight:500;']")
        )
    )
    print(heading.text.strip())

    try:

        table_div = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='minHeightDiv']//div[@id='internship']//div[@class='container']//div[@class='col-xs-12 col-sm-7 col-md-8']//div[@class='table-responsive']")
            )
        )

        table_rows = table_div.find_elements(By.XPATH, "//table[@class='table table-bordered table-striped']//tbody/tr")

        for row in table_rows: 
            cols = row.find_elements(By.XPATH, './/td')

            info_new = {
                "Sr.no": cols[0].text.strip(),
                    "Batch": cols[1].text.strip(),
                    "Batch Duration": cols[2].text.strip(),
                    "Start Date": cols[3].text.strip(),
                    "End Date": cols[4].text.strip(),
                    "Time": cols[5].text.strip(),
                    "Fees (Rs.)": cols[6].text.strip()
            }
            print(info_new)
    except:
        print("No Data found")




main_info()
dropOne()
dropTwo()
dropFour()
dropSix()
batch_schedule()