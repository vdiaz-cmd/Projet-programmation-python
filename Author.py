# 4.2.1
class Author:
    def __init__(self, name, ndoc = 0, production = {}):
        self.name = name
        self.ndoc = ndoc
        self.production = production

# 4.2.2
    def add(self, doc_id, doc):
        self.production[doc_id] = doc
        self.ndoc = len(self.production)

    def __str__(self):
        return f"{self.name}, {self.ndoc} documents"

    