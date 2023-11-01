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
    return qa.run(f"""You are a chatbot providing helpful information on how to use the Fishnet Networking framework, fishnet is a multiplayer framework for the unity game engine.
                 All your answers should be clear and understandable, and if the situation fits, provide code examples.
                  
                  Question: {question}""")
    

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


if __name__ == "__main__":
    start()