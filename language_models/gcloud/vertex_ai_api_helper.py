import json
import re
import uuid

import PyPDF2
import vertexai
from google.cloud import aiplatform, storage
from langchain_text_splitters import TextSplitter, RecursiveCharacterTextSplitter, CharacterTextSplitter
from vertexai.language_models import TextEmbeddingModel
from vertexai.preview.generative_models import GenerativeModel
from langchain_community.document_loaders import PyPDFLoader


def get_model_from_platform(project: str, location: str, model_name: str = "gemini-pro") -> GenerativeModel:
    initialize_vertex_ai(location, project)
    return GenerativeModel(model_name)


def initialize_aiplatform(location, project):
    aiplatform.init(project=project, location=location)


def initialize_vertex_ai(location, project):
    initialize_aiplatform(location, project)
    vertexai.init()


def extract_sentences_from_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    text_splitter = RecursiveCharacterTextSplitter([".", "?", "!"], keep_separator=False, chunk_size=50,
                                                   chunk_overlap=0)
    chunks = loader.load_and_split(text_splitter)
    sentences = [chunk.page_content for chunk in chunks]
    return sentences


def generate_text_embeddings(sentences, project, location) -> list:
    aiplatform.init(project=project, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings(sentences)
    vectors = [embedding.values for embedding in embeddings]
    return vectors


def generate_and_save_embeddings(pdf_path, sentence_file_path, embed_file_path, project, location):
    sentences = extract_sentences_from_pdf(pdf_path)
    if sentences:
        embeddings = generate_text_embeddings(sentences, project, location)

        with open(embed_file_path, 'w') as embed_file, open(sentence_file_path, 'w') as sentence_file:
            for sentence, embedding in zip(sentences, embeddings):
                id = str(uuid.uuid4())

                embed_item = {"id": id, "embedding": embedding}
                sentence_item = {"id": id, "sentence": sentence}

                json.dump(sentence_item, sentence_file)
                sentence_file.write('\n')
                json.dump(embed_item, embed_file)
                embed_file.write('\n')


def upload_file(bucket_name, file_path, location):
    storage_client = storage.Client()
    if not storage_client.get_bucket(bucket_name):
        bucket = storage_client.create_bucket(bucket_name, location=location)
    else:
        bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.blob(file_path)
    blob.upload_from_filename(file_path)


def load_sentence(sentence_file_path):
    data = []
    with open(sentence_file_path, 'r') as file:
        for line in file:
            entry = json.loads(line)
            data.append(entry)
    return data


def generate_context(ids, data):
    concatenated_names = ''
    for id in ids:
        for entry in data:
            if entry['id'] == id:
                concatenated_names += entry['sentence'] + "\n"
    return concatenated_names.strip()


def create_vector_index(bucket_name, index_name):
    index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name=index_name,
        contents_delta_uri="gs://" + bucket_name,
        dimensions=768,
        approximate_neighbors_count=10)

    index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
        display_name=index_name,
        public_endpoint_enabled=True)

    index_endpoint.deploy_index(
        index=index, deployed_index_id=index_name)
