import chromadb

db = chromadb.PersistentClient(path = "./knowledge_base")
collection = db.get_or_create_collection("Sunbeam_Data")

all_data = collection.get()["ids"]
for id in all_data:
    print(id)
# print(all_data)