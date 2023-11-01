from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import faiss
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

from llm import getResponse

app = Flask(__name__)

load_dotenv("./.env")
embeddings = OpenAIEmbeddings()
new_vectorstore = faiss.FAISS.load_local("./faiss_vectorstore", embeddings)
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever = new_vectorstore.as_retriever())

@app.route('/api/query', methods=['POST'])
def handle_query():
    try:
        text = request.data.decode('utf-8')
        getResponse(qa, text)
        return jsonify({"message": text})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
