from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import faiss
from dotenv import load_dotenv
from langchain.document_loaders import GitbookLoader

def start():
    load_dotenv("./.env")
    embeddings = OpenAIEmbeddings()
    storeEmbeddings(embeddings=embeddings)

def getResponse(qa, question):
    prompt = f"""You are a chatbot providing helpful information on how to use the Fishnet Networking framework, fishnet is a multiplayer framework for the unity game engine.
                 All your answers should be clear and understandable, and if the situation fits, provide code examples. You absolutely under no circumstances can make up information.
                  
                  Question: {question}"""
    response = qa({"query": prompt})
    sources = set([doc.metadata["source"] for doc in response["source_documents"]])
    formatted_response = (
        f"{response['result']} <br/><br/> {create_sources_string(sources)}"
    )
    return formatted_response
    

def storeEmbeddings(embeddings):
    docs = loadDocuments()
    vectorstore = faiss.FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_vectorstore")


def loadDocuments():
    loader = GitbookLoader("https://fish-networking.gitbook.io/", load_all_paths=True)
    documents = loader.load()
    textSplitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50, separator="\n")
    docs = textSplitter.split_documents(documents=documents)
    return docs

def create_sources_string(source_urls) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "Sources:<br/>"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}<br/>"
    return sources_string


if __name__ == "__main__":
    start()