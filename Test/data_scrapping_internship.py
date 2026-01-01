from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# start selenium browser session
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options = chrome_options)


# load desired page in the browser
driver.get("https://www.sunbeaminfo.in/internship")


page = driver.find_element(By.ID, "minHeightDiv")

main_div = page.find_element(By.CSS_SELECTOR, ".main_info.wow.fadeInUp")

paragraphs = main_div.find_elements(By.TAG_NAME, "p")

for p in paragraphs:
            text = p.text.strip()
            if text:
                print(text)


wait = WebDriverWait(driver, 10)



plus_button1 = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseOneA']"))
)
driver.execute_script(
    "arguments[0].scrollIntoView(true);", plus_button1
)
plus_button1.click()

div =   wait.until(
    EC.presence_of_element_located((By.ID, "collapseOneA"))
)

text_area = div.find_element(
    By.CSS_SELECTOR,
    ".list_style"
)

# print(text_area.text.strip())

paragraphs = text_area.find_elements(By.TAG_NAME, "ul")
for p in paragraphs:
            text = p.text.strip()
            if text:
                print(text)


plus_button2 = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseTwo']"))
)
driver.execute_script(
    "arguments[0].scrollIntoView(true);", plus_button2
)
plus_button2.click()

text1 =   wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[@href='#collapseTwo']"))
)
print(text1.text.strip())

text_area =  wait.until(
    EC.presence_of_element_located((By.ID, 'collapseTwo'))
)

print(text_area.text.strip())




plus_button3 = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseThree']"))
)
driver.execute_script(
    "arguments[0].scrollIntoView(true);", plus_button3
)
plus_button3.click()

text2 =   wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[@href='#collapseThree']"))
)
print(text2.text.strip())

text_area =  wait.until(
    EC.presence_of_element_located((By.ID, 'collapseThree'))
)

print(text_area.text.strip())



plus_button4 = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseFour']"))
)
driver.execute_script(
    "arguments[0].scrollIntoView(true);", plus_button4
)
plus_button4.click()

text3 =   wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[@href='#collapseFour']"))
)
print(text3.text.strip())

text_area2 =  wait.until(
    EC.presence_of_element_located((By.ID, 'collapseFour'))
)

print(text_area2.text.strip())





