import os
import constants

from langchain_community.document_loaders import PyPDFLoader, OnlinePDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(directory):
    all_documents = []
    modification_times = []

    for fn in os.listdir(directory):
        file_path = os.path.join(directory, fn)
        if os.path.isfile(file_path):
            loader = get_loader(file_path)
            raw_documents = loader.load()
            modification_time = os.path.getmtime(file_path)
            all_documents.extend(raw_documents)
            modification_times.append(modification_time)

    return all_documents, modification_times


def get_loader(file_path):
    _, ext = os.path.splitext(file_path)
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
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks


def save_file(file):
    if file:
        filename = file.filename
        file.save(os.path.join(constants.DATA_PATH, filename))
        return filename
    return None
