import chromadb

db = chromadb.PersistentClient(path="./Text_data")
collection = db.get_or_create_collection(name="CourseData")

all_data = collection.get()["ids"]
for id in all_data:
    print(id)
# print(all_data)