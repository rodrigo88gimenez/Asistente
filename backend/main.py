from fastapi import FastAPI, UploadFile, File, Form
from typing import List
import shutil
import os

from fastapi.middleware.cors import CORSMiddleware

from backend.services.processor import process_file
from backend.services.ai import generate_response
from backend.services.doc_generator import generate_doc

app = FastAPI()

# 🔓 CORS (necesario para GitHub Pages)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(default=[]),
    text: str = Form(default="")
):
    texts = []

    # 🔹 texto manual
    if text:
        texts.append(text)

    # 🔹 archivos
    for file in files:
        file_path = f"{UPLOAD_DIR}/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = process_file(file_path, file.content_type)
        texts.append(extracted_text)

    combined_text = "\n".join(texts)

    response = generate_response(combined_text)

    return {
        "response": response,
        "raw_text": combined_text
    }


@app.post("/generate-doc")
async def create_doc(text: str):
    file_path = generate_doc(text)
    return {"file": file_path}
