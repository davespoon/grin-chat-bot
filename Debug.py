from language_models.sentence_transformer.Transformer import Transformer

if __name__ == "__main__":
    sentence = ['DoiT is a great company to work for']
    transformer = Transformer(sentence)
    transformer.print_info()
