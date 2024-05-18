import os

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(directory):
    loaders = [UnstructuredPDFLoader(os.path.join(directory, fn)) for fn in os.listdir(directory)]
    all_documents = []

    for loader in loaders:
        raw_documents = loader.load()
        all_documents.extend(raw_documents)
        return all_documents


def load_pdf(path):
    loader = PyPDFLoader(path)
    documents = loader.load()
    return documents


def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks
