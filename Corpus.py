import os
from pathlib import Path
import pandas as pd

from Document import Document
from Author import Author


class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}  # clé : nom de l'auteur, valeur : objet Author
        self.id2doc = {}   # clé : doc_id, valeur : objet Document
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

    def afficher_par_date(self, n=5):
        docs = sorted(self.id2doc.values(), key=lambda d: d.date)
        for doc in docs[:n]:
            print(f"{doc.date} - {doc}")

    def afficher_par_titre(self, n=5):
        docs = sorted(self.id2doc.values(), key=lambda d: d.titre.lower())
        for doc in docs[:n]:
            print(f"{doc.titre} ({doc.date})")

    def __repr__(self):
        return f"Corpus '{self.nom}' : {self.ndoc} document(s), {self.naut} auteur(s)"

    def save(self):
        lignes = [{"id": doc_id, **doc.to_dict()} for doc_id, doc in self.id2doc.items()]
        df = pd.DataFrame(lignes)
        df.to_csv(f"{self.nom}.csv", sep="\t", index=False)

    def load(path):
        nom = Path(path).stem
        corpus = Corpus(nom)
        if os.path.exists(path):
            df = pd.read_csv(path, sep="\t", keep_default_na=False)
            for ligne in df.to_dict("records"):
                ligne.pop("id")
                corpus.add(Document(**ligne))
        return corpus
