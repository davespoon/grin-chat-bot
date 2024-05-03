import vertexai

from vertexai.language_models import TextGenerationModel


def run(prompt):
    vertexai.init(project='pure-toolbox-39006', location='us-central1')
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_k": 40,
        "top_p": 0.95,
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(prompt, **parameters)
    return response
