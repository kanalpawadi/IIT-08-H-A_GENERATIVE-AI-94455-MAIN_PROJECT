# main.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from course import fetch_course_data
from vector_store import add_course_to_chroma

import uuid
import time
import re
 

def get_all_course_links():
    """Fetch all course links from the modular courses home page."""
    
    driver = webdriver.Chrome()
    driver.get("https://www.sunbeaminfo.in/modular-courses-home")

     
    container = driver.find_element(By.CLASS_NAME, "modular_courses_home_wrap")

    #find the anchor tag
    links = container.find_elements(By.TAG_NAME, "a")

    course_links = []
    for link in links:
        href = link.get_attribute("href")
        if href:
            course_links.append(href)
    driver.quit()
    return course_links

def make_filename_from_url(url):
    """Convert course URL into a safe filename."""
    
    name = url.rstrip("/").split("/")[-1]
    # Replace non-alphanumeric characters with underscores
    name = re.sub(r'\W+', '_', name)
    return f"{name}.txt"

if __name__ == "__main__":
    course_links = get_all_course_links()
    print(f"Total courses found: {len(course_links)}")

    for url in course_links:
        filename = make_filename_from_url(url)
        print(f"\nFetching data for {url} -> Saving as {filename}")

        text = fetch_course_data(url, filename)

        course_id = str(uuid.uuid4())

        add_course_to_chroma(url, text)


        print(f"Saved + Embedded: {filename}")
