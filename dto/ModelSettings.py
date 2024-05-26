import decimal


class ModelSettings:
    def __init__(self, model=None, temperature=None, max_tokens=None, top_p: decimal = None):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p if isinstance(top_p, float) else float(top_p)
