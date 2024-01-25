from flask import Flask, render_template, request
import os
import pandas as pd
import matplotlib.pyplot as plt
from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import PyPDF2
# Set up Flask
app = Flask(__name__)

# Set up LangChain
os.environ["OPENAI_API_KEY"] = "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"

# Loading PDFs and chunking with LangChain
loader = PyPDFLoader(r"F:\COMPANY SPECIFIC DOCS\gen ai test\48lawsofpower.pdf")
pages = loader.load_and_split()
chunks = pages

with open(r"F:\COMPANY SPECIFIC DOCS\gen ai test\48lawsofpower.pdf", 'rb') as f:
    pdf = PyPDF2.PdfFileReader(f)
    text = " ".join(page.extract_text() for page in pdf.pages)

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=24,
    length_function=count_tokens,
)

chunks = text_splitter.create_documents([text])
 
# Create vector database
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(chunks, embeddings)

# Load question-answering chain
chain = load_qa_chain(OpenAI(model="gpt-3.5-turbo-instruct"), chain_type="stuff")

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    if request.method == 'POST':
        question = request.form['question']

        # Use LangChain to get the answer
        docs = db.similarity_search(question)
        answer = chain.run(input_documents=docs, question=question)

        return render_template('index.html', question=question, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
