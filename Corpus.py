import pandas as pd

from Document import Document
from Author import Author

class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}  # nom des authors
        self.id2doc = {}   # id du document
        self.ndoc = 0
        self.naut = 0    

    def add(self, doc):
        doc_id = self.ndoc
        self.id2doc[doc_id] = doc
        self.ndoc += 1

        if doc.auteur not in self.authors:
            self.authors[doc.auteur] = Author(doc.auteur)
            self.naut += 1
        self.authors[doc.auteur].add(doc_id, doc)

    def _cle_date(self, doc):
        return str(doc.date)

    def afficher_par_date(self):
        docs = sorted(self.id2doc.values(), key=self._cle_date)
        for doc in docs:
            print(f"{doc.date} - {doc}")

    def afficher_par_titre(self):
        docs = sorted(self.id2doc.values(), key=lambda d: d.titre.lower())
        for doc in docs:
            print(f"${doc.title} ({doc.date})")

    def __repr__(self):
        return f"Corpus '{self.nom}' : {self.ndoc} document(s), {self.naut} auteur(s)"

