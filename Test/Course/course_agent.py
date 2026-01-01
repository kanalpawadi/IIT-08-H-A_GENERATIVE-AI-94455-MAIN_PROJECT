import chromadb
from langchain_openai import ChatOpenAI
from langchain.embeddings import init_embeddings
from dotenv import load_dotenv
load_dotenv()

print("Initializing Chroma...")
client = chromadb.PersistentClient(
    path="./Text_data"
)
collection = client.get_collection("CourseData")

print("Documents in DB:", collection.count())
print("Loading SAME Embedding Model Used During Storage...")
embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)

print("Initializing LLM...")
llm = ChatOpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",
    model="google/gemma-3-4b",
    timeout=120
)


def search_courses(query, top_k=3):
    """Semantic search using SAME embeddings used during storage"""

    query_embedding = embed_model.embed_query(query)

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    if not result["documents"] or len(result["documents"][0]) == 0:
        return "No relevant course data found."

    docs = result["documents"][0]
    metas = result["metadatas"][0]


    # print(docs)

    context = ""
    for i, doc in enumerate(docs):
        context += (
            f"\n\n[RESULT {i+1}]\n"
            f"Source: {metas[i]['source']}\n"
            f"{doc}\n"
        )

    return context


print("\nConsole Agent")
print("Type 'exit' to quit\n")

while True:
    question = input("Ask Something About Courses ➜ ")
    if question.lower() in ["exit", "quit"]:
        break
    context = search_courses(question)
    # print(context)
    prompt = f"""
    You are a Sunbeam Course Assistant.
    Answer the user using ONLY the below course data.
    If the answer is not found, strictly say:
    "Not available in stored course data."

    COURSE DATA:
    {context}

    QUESTION:
    {question}

    FINAL ANSWER (clear bullet points, course specific):
    # """

    try:
        response = llm.invoke(prompt)
        print("\nAI Response:\n")
        print(response.content)
    except Exception as e:
        print("\nModel Error:", e)

