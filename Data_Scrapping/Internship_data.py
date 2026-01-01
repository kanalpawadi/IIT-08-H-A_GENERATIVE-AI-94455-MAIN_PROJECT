from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initiating selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

driver.get("https://www.sunbeaminfo.in/internship")

# creating file
file = open("Sunbeam_internship_data.txt", "w", encoding="utf-8")

def write(text="", indent=0):
    line = ("    " * indent) + text
    file.write(line + "\n")
    print(line)

#  Main page info 
def main_info():
    main_info = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='minHeightDiv']//div[@id='internship']//div[@class='container']//div[@class='col-xs-12 col-sm-7 col-md-8']//div[@class='main_info wow fadeInUp']")
            )
        )
    write(main_info.text.strip())
    write()

#  Parsing dropdown
def parse_dropdown(collapse_id):

    plus_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//a[@href='#{collapse_id}']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_btn)
    plus_btn.click()

    title = plus_btn.text.strip()
    write(f"\n{title}")

    collapse_div = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//div[@id='{collapse_id}']//div[@class='list_style']"))
    )

    # detect if table exists
    tables = collapse_div.find_elements(By.XPATH, ".//table")

    block_lines = []
    seen = set()

    # paragraphs data
    for p in collapse_div.find_elements(By.XPATH, ".//p"):
        text = p.text.strip()
        if text and text not in seen:
            block_lines.append(text)
            seen.add(text)

    for ul in collapse_div.find_elements(By.XPATH, ".//ul"):
            for li in ul.find_elements(By.XPATH, ".//li"):
                text = li.text.strip()
                if text and text not in seen:
                    block_lines.append(f"- {text}")
                    seen.add(text)

    # table data
    if tables:
        for table in tables:
            rows = table.find_elements(By.XPATH, ".//tr")
            for row in rows:
                cols = [
                    c.text.strip()
                    for c in row.find_elements(By.XPATH, ".//th/td")
                    if c.text.strip()
                ]
                if cols:
                    line = " | ".join(cols)
                    if line not in seen:
                        block_lines.append(line)
                        seen.add(line)

        

    # writing data as one paragraph
    write("\n".join(block_lines), indent=1)

    return title, "\n".join(block_lines)




# Batch Schedule Data
def batch_schedule():
    heading = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//h4[@style='font-weight:500;']"
        ))
    )
    write("\n" + heading.text.strip())

    try:
        table = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='table-responsive']//table"))
        )

        rows = table.find_elements(By.XPATH, ".//tr")
        for row in rows:
            cols = [c.text.strip() for c in row.find_elements(By.XPATH, ".//th|.//td")]
            if cols:
                write(" | ".join(cols), indent=2)
    except:
        write("No Data found")

# calling functions
main_info()
parse_dropdown("collapseOneA")
parse_dropdown("collapseTwo")
parse_dropdown("collapseFour")
parse_dropdown("collapseSix")
batch_schedule()

# closing
file.close()
driver.quit()
