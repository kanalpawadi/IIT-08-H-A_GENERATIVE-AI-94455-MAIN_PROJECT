from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.embeddings import init_embeddings
from data_scraping_about_us import AboutUsScraper

from main import store_course_data

import chromadb

# initiating embedding model
embed_model = init_embeddings(
    model= "text-embedding-nomic-embed-text-v1",
    provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "not-needed",
    check_embedding_ctx_length = False
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


# Method to get fist line of data
def get_first_line(chunk):
    for line in chunk.splitlines():
        line = line.strip()
        if line:
            return line
    return "Unknown"


def get_chunks_of_internship_data():

    #Read file 
    with open("Sunbeam_internship_data.txt", "r", encoding="utf-8") as f:
        text = f.read()

    # chunking
    chunks = splitter.split_text(text)

    # # Print chunks
    # for i, chunk in enumerate(chunks, 1):
    #     print(f"\n== CHUNK{i} ==")
    #     print(chunk)
    
    return chunks


def store_internship_data():

    chunks = get_chunks_of_internship_data()
    
    all_ids = collection.get()["ids"]

    for i, chunk in enumerate(chunks):

        first_line = get_first_line(chunk)

        id = f"Internship_data_{first_line}"

        if id in all_ids:
            collection.delete(ids = [id])
        
        chunk_embedding = embed_model.embed_documents([chunk])

        document = chunk

        metadata = {
            "source": "Sunbeam Internship Data",
            "title" : first_line,
        }

        collection.add(
            ids=[id],
            embeddings=chunk_embedding,
            documents= [document],
            metadatas= [metadata]
        )



def store_about_page():

    about_scraper = AboutUsScraper()
    data = about_scraper.run()

    full_text = "\n\n".join(data)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )

    chunks = splitter.split_text(full_text)

    all_ids = collection.get()["ids"]

    for i, chunk in enumerate(chunks):
        doc_id = f"sunbeam_about_us_{i}"

        if id in all_ids:
            collection.delete(ids = [id])

        embedding_about_us = embed_model.embed_documents([chunk])

        metadata_about_us = {
                "source": "Sunbeam About Us",
                "title": "About Sunbeam"
            }

        collection.add(
            ids=[doc_id],
            embeddings=embedding_about_us,
            documents=[chunk],
            metadatas=[metadata_about_us]
        )




store_internship_data()
store_about_page()
store_course_data()

all_data = collection.get()["metadatas"]

# print("all data",all_data)
for data in all_data:
    print(data)
