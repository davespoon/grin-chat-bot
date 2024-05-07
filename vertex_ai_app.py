import os

from dotenv import load_dotenv
from google.cloud import aiplatform

from language_models.gcloud.vertex_ai_api_helper import (
    generate_and_save_embeddings,
    get_model_from_platform, load_sentence, generate_text_embeddings, generate_context)

load_dotenv()

project = os.getenv("GCP_PROJECT")
location = "europe-north1"
pdf_path = "ApplePie.pdf"
bucket_name = "grin-chat-bot-bucket"
embed_file_path = "grin-chat-bot-embed.json"
sentence_file_path = "grin-chat-bot-sentence.json"
index_name = "grin_chat_bot_index"
index_id = "2245185151732547584"

if __name__ == "__main__":
    generate_and_save_embeddings(pdf_path, sentence_file_path, embed_file_path, project, location)
    # upload_file(bucket_name, embed_file_path, location)
    # create_vector_index(bucket_name, index_name)

    model = get_model_from_platform(project, location, "gemini-pro")
    index_ep = aiplatform.MatchingEngineIndexEndpoint(index_id)

    data = load_sentence(sentence_file_path)

    query = "what is second step to cook apple pie?"
    qry_emb = generate_text_embeddings(query, project, location)

    response = index_ep.find_neighbors(deployed_index_id=index_id, queries=[qry_emb[0]], num_neighbors=10)
    matching_ids = [neighbor.id for sublist in response for neighbor in sublist]

    context = generate_context(matching_ids, data)
    prompt = f"Based on the context delimited in backticks, answer the query. ```{context}``` {query}"

    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)
    print(response.text)
