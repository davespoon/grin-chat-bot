import vertexai

from vertexai.language_models import TextGenerationModel


def get_completion(prompt, project, location):
    vertexai.init(project=project, location=location)
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_k": 40,
        "top_p": 0.95,
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(prompt, **parameters)
    return response
