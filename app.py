from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from typing import Annotated

from typing import List
from io import BytesIO
from embedding import *
from inference import *
from fastapi.middleware.cors import CORSMiddleware
from read_file import *
app = FastAPI()

origins = ["*"]

app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Check if the uploaded file is either a PDF or DOCX
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX are allowed.")

    # Read the content of the file based on its type
    # content = ""
    # if file.content_type == "application/pdf":
    #     file_type="pdf"
    #     # Read PDF content
    #     pdf_reader = PyPDF2.PdfReader(file.file)
    #     for page in pdf_reader.pages:
    #         content += page.extract_text()
 
    if file.content_type == "application/pdf":
        file_type = "pdf"
    # Read PDF content using PyMuPDF
        pdf_document = fitz.open(stream=file.file.read(), filetype="pdf")
        content=""
        for page in pdf_document:
            content += page.get_text()
        pdf_document.close()

        secrets=pdf_content_save_to_vectorstore(content)             
        

    if file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        file_type="docx"
        try:
            file_bytes=await file.read()
            content=read_docx(file_bytes)
            secrets=docx_content_save_to_vectorstore(content)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading DOCX file: {e}")    
        
    collection_name_to_file(secrets, file.filename)
    
    return {"secret":secrets,"filename": file.filename, "content": content, }


@app.post("/query/")
async def query_file(secret:str=Form(...),query: str = Form(...)):
    retriever=load_collection_get_retriever(secret)
    res=query_to_chain_with_chunks(retriever,query)

    return {"response":res["answer"], "context": res["context"], "secret":secret}

