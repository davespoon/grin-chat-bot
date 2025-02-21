import os
from typing import Any

from langchain.chains.openai_functions import create_extraction_chain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import BasePromptTemplate

import constants

from langchain_community.document_loaders import PyPDFLoader, OnlinePDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import prompts.prompt_templates
from prompts import schemas

SUPPORTED_EXTENSIONS = ['.pdf', '.txt', '.csv']


def load_documents(directory: str) -> tuple[list[Document], list[float]]:
    all_documents: list[Document] = []
    modification_times: list[float] = []

    for fn in os.listdir(directory):
        file_path = os.path.join(directory, fn)
        if os.path.isfile(file_path):
            loader = get_loader(file_path)
            raw_documents = loader.load()
            modification_time = os.path.getmtime(file_path)
            all_documents.extend(raw_documents)
            modification_times.append(modification_time)

    return all_documents, modification_times


def extract_resume_info(text, prompt_template):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    extraction_chain = create_extraction_chain(
        schemas.resume_schema,
        llm,
        prompt_template)

    structured_data = extraction_chain.run(text)
    return structured_data


def get_loader(file_path: str):
    _, ext = os.path.splitext(file_path)
    if ext.lower() in SUPPORTED_EXTENSIONS:
        if ext.lower() == '.pdf':
            return PyPDFLoader(file_path)
        elif ext.lower() == '.txt':
            return TextLoader(file_path)
        elif ext.lower() == '.csv':
            return CSVLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def load_online_pdf(uri):
    loader = OnlinePDFLoader(uri)
    return loader.load()


def load_pdf(path):
    loader = PyPDFLoader(path)
    documents = loader.load()
    return documents


def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=constants.CHUNK_SIZE,
                                                   chunk_overlap=constants.CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(documents)
    return chunks


def save_file(file) -> str:
    if file:
        try:
            filename = file.filename
            file.save(os.path.join(constants.DATA_PATH, filename))
            return filename
        except Exception as e:
            raise IOError(f"Failed to save file: {e}")
    return None
