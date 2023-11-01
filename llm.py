from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import faiss
from dotenv import load_dotenv
import os
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import GitbookLoader

def start():
    load_dotenv("./.env")
    embeddings = OpenAIEmbeddings()
    #storeEmbeddings(embeddings=embeddings)
    new_vectorstore = faiss.FAISS.load_local("./faiss_vectorstore", embeddings)
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever = new_vectorstore.as_retriever())
    res = qa.run("""You are a chatbot providing helpful information on how to use the Fishnet Networking framework, fishnet is a multiplayer framework for the unity game engine.
                 All your answers should be clear and understandable, and if the situation fits, provide code examples.
                 Question: What is prediction v2? is it better than v1?""")
    print(res)


def getResponse(qa, question):
    return qa.run(f"""You are a chatbot providing helpful information on how to use the Fishnet Networking framework, fishnet is a multiplayer framework for the unity game engine.
                 All your answers should be clear and understandable, and if the situation fits, provide code examples.
                  
                  Question: {question}""")
    

def storeEmbeddings(embeddings):
    docs = loadDocuments()
    vectorstore = faiss.FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_vectorstore")

def loadDocuments():
    path = './Fishnet/Assets/'
    #loader = DirectoryLoader(path, glob="**/*.cs", loader_cls=TextLoader)
    loader = GitbookLoader("https://fish-networking.gitbook.io/", load_all_paths=True)
    documents = loader.load()
    textSplitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50, separator="\n")
    docs = textSplitter.split_documents(documents=documents)
    return docs




if __name__ == "__main__":
    start()