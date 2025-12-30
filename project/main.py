# main.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from project.course import fetch_course_data  # your function

def get_all_course_links():
    """Fetch all course links from the modular courses home page."""
    
    driver = webdriver.Chrome()
    driver.get("https://www.sunbeaminfo.in/modular-courses-home")

    # Find the container
    container = driver.find_element(By.CLASS_NAME, "modular_courses_home_wrap")

    # Get all anchor tags inside it
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
    # Get
    name = url.rstrip("/").split("/")[-1]
    # Replace non-alphanumeric characters with underscores
    name = re.sub(r'\W+', '_', name)
    return f"{name}.txt"

if __name__ == "__main__":
    # Get all course links
    course_links = get_all_course_links()
    print(f"Total courses found: {len(course_links)}")

    # Fetch data for each course and save in separate TXT files
    for url in course_links:
        filename = make_filename_from_url(url)
        print(f"\nFetching data for {url} -> Saving as {filename}")
        fetch_course_data(url, filename)
        print(f"Saved: {filename}")
