from flask import Flask
from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
import PyPDF2

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
app = Flask(__name__)
#hell0 world
@app.route('/')

 ✅ RetrievalQA replaced with modern LCEL chain
def create_retrieval_chain(vectorstore, llm, prompt):
    retriever = vectorstore.as_retriever()
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

text_splitter = CharacterTextSplitter(
    separator='\n',
    chunk_size=2000,
    chunk_overlap=200,
    length_function=len,
)
embeddings = HuggingFaceEmbeddings()
def perform_qa(query):
        
        db= FAISS.load_local("vector_index", embeddings, allow_dangerous_deserialization=True)
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        rqa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
        result = rqa.invoke(query)
        return result['result']
def home():
    return "Flask is working!"

if __name__ == '__main__':
    app.run(debug=True)
