# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader
import tempfile

from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize embedding model with Sentence Transformers
# embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/multi-qa-distilbert-cos-v1')
embedding_model = HuggingFaceEmbeddings(model_name='BAAI/bge-large-en-v1.5')

import fitz  # PyMuPDF
from read_file import *
import secrets
import string

def generate_secure_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# Example usage
def collection_name_to_file(random_string, uploded_file_name):
    file_path = 'all_collections.txt'
    with open(file_path, 'a') as file:
        file.write(random_string+"  "+ uploded_file_name+'\n')


def load_collection_get_retriever(secret):
    vectorstore = Chroma(
        # client=client,
        collection_name=secret,
        embedding_function=embedding_model,
        persist_directory="./chroma_db",

    )
    retriever=vectorstore.as_retriever(search_kwargs={"k": 6})
    return retriever

def docx_content_save_to_vectorstore(content):
    text_splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\n\n", "\n", " ", ".", ",", "\u200b", "\uff0c", "\u3001",
        "\uff0e", "\u3002", ""
    ],
    chunk_size=1200,
    chunk_overlap=200,
    length_function=len   
    )

    secret=generate_secure_random_string()
    docs=text_splitter.create_documents(texts=[content])
    for doc in docs:
        print(doc,"\n\n")
    vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory="./chroma_db",
    collection_name=secret

    )
 

    vectorstore_retreiver = vectorstore.as_retriever(search_kwargs={"k": 6})
    return secret

def pdf_content_save_to_vectorstore(content):
    # Replace 'your_pdf_file.pdf' with the actual path to your PDF file.
    
    text_splitter = RecursiveCharacterTextSplitter(
       separators=[
            "\n\n", "\n", " ", ".", ",", "\u200b", "\uff0c", "\u3001",
            "\uff0e", "\u3002", ""
        ],
        chunk_size=1200,
        chunk_overlap=200,
        length_function=len,
    )

    secret=generate_secure_random_string()
    print(secret)
    docs=text_splitter.create_documents(texts=[content])    

    vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory="./chroma_db",
    collection_name=secret

    )
    return secret



