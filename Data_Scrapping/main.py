# main.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import init_embeddings
from course import fetch_course_data
import chromadb
import re


embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)

# Initiating chromadb
db = chromadb.PersistentClient(path = "./knowledge_base")
collection = db.get_or_create_collection("Sunbeam_Data")

#  Recursive Text Splitter
splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n"],   # split by dropdown blocks
    chunk_size=600,      
    chunk_overlap=100
)

def get_all_course_links():
    """Fetch all course links from the modular courses home page."""
    
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

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

def safe_id(text):
    return re.sub(r"\W+", "_", text.lower())

def make_filename_from_url(url):
    """Convert course URL into a safe filename."""
    
    name = url.rstrip("/").split("/")[-1]
    # Replace non-alphanumeric characters with underscores
    name = re.sub(r'\W+', '_', name)
    return f"{name}.txt"

def store_course_data():
    course_links = get_all_course_links()
    print(f"Total courses found: {len(course_links)}")

    for url in course_links:
        filename = make_filename_from_url(url)
        print(f"\nFetching data for {url} -> Saving as {filename}")

        data = fetch_course_data(url, filename)

        print(data["course_name"])

        course_name = data["course_name"]
        course_content = data["content"]

        print(f"Saved + Embedded: {filename}")

        metadata = {
            "course":course_name,
            "url" : url
        }
        embed = embed_model.embed_documents([course_content])

        collection.add(
            ids=[course_name],
            embeddings=embed,
            documents=[course_content],
            metadatas=[metadata]
)
        
store_course_data()



        
        



        


