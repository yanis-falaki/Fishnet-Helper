from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import faiss
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from datetime import datetime
import sqlite3
from flask_cors import CORS

from llm import getResponse

app = Flask(__name__)
CORS(app)

load_dotenv("./.env")
embeddings = OpenAIEmbeddings()
new_vectorstore = faiss.FAISS.load_local("./faiss_vectorstore", embeddings)
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=new_vectorstore.as_retriever())

db_connection = sqlite3.connect("visitor_data.db")
db_global_cursor = db_connection.cursor()
db_global_cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitor_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME,
        request TEXT,
        response TEXT,
        ip TEXT
    )
''')
db_connection.commit()
db_connection.close()

@app.route('/api/query', methods=['POST'])
def handle_query():
    text = request.data.decode('utf-8')
    ip = request.remote_addr  # Get the IP address of the sender
    timestamp = datetime.now()  # Use the actual datetime format

    response = getResponse(qa, text)

    db_connection = sqlite3.connect("visitor_data.db")
    db_cursor = db_connection.cursor()
    db_cursor.execute("INSERT INTO visitor_logs (timestamp, request, response, ip) VALUES (?, ?, ?, ?)",
                        (timestamp, text, response, ip))
    db_connection.commit()

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7770, debug=True)
