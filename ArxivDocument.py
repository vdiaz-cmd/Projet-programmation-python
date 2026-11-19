from Document import Document
from Document import Source
class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, autres_auteurs):
        super().__init__(titre, auteur, date, url, texte)
        self.autres_auteurs = autres_auteurs
        self.genre = Source.ARXIV        
    def __str__(self):
        return super().__str__() + "autres auteurs: ".join(self.autres_auteurs)

    def get_genre(self):
        return self.genre