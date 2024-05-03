from sentence_transformers import SentenceTransformer


class Transformer:
    model = SentenceTransformer('sentence-t5-base')

    def __init__(self, sentence):
        self.embedding = self.encode(sentence)

    def encode(self, sentence):
        return self.model.encode(sentence)

    def print_info(self):
        print(len(self.embedding[0]))
        print(self.embedding[0])

    def decode(self, embedding):
        return self.model.decode(embedding)
