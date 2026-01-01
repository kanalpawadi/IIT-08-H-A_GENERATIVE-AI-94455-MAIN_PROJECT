from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.sunbeaminfo.in/modular-courses-home")

# Find the container
container = driver.find_element(By.CLASS_NAME, "modular_courses_home_wrap")

# Get all anchor tags inside it
links = container.find_elements(By.TAG_NAME, "a")

# Store / Print them
course_links = []
for link in links:
    href = link.get_attribute("href")
    if href:            # avoid empty links
        course_links.append(href)
        print(href)

print("Total links:", len(course_links))