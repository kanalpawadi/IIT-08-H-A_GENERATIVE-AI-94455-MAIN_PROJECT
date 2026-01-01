import os
import chromadb
from langchain.embeddings import init_embeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)

db = chromadb.PersistentClient(path="./Text_data")
collection = db.get_or_create_collection(name="CourseData")

#divide the data in chunks 
def load_and_split_txt(txt_path):
    loader = TextLoader(txt_path, encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)
    return chunks

base_folder = r"E:\SUNBEAM_INTERN\SUNBEAM_PROJECT\Project_IIT-08-H-A_GENERATIVE-AI-94455\Data_Scrapping\Course"

for file in os.listdir(base_folder):
    if file.endswith(".txt"):
        file_path = os.path.join(base_folder, file)
        print("Processing:", file_path)

        chunks = load_and_split_txt(file_path)

        for i, chunk in enumerate(chunks):
            embedding = embed_model.embed_documents([chunk.page_content])

            collection.add(
                ids=[f"{file}_{i}"],
                embeddings=embedding,
                metadatas=[{"source": file_path}],
                documents=[chunk.page_content]
            )

print("Embedding completed successfully!")
