from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(directory):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents


def load_pdf(path):
    loader = PyPDFLoader(path)
    documents = loader.load()
    return documents


def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks
