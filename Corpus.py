import os
from pathlib import Path
import pandas as pd

from Document import Document
from Author import Author

class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}  # le dictionnaire des auteurs, key: nom d'auteur, value: Objet Author correspondant
        self.id2doc = {}   # le dictionnaire des documents, key: doc_id, valueL Objet Document correspondant
        self.ndoc = 0
        self.naut = 0    

    def add(self, doc):
        doc_id = self.ndoc
        self._add(doc, doc_id)

    def _add(self, doc, doc_id):
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

    def save(self):
        lignes = [{"id": doc_id, **doc.to_dict()} for doc_id, doc in self.id2doc.items()]

        df = pd.DataFrame(lignes)
        df.to_csv(f"{self.nom}.csv", sep="\t", index=False)       
            

    def load(path):
        nom = Path(path).name
        corpus = Corpus(nom)
        if os.path.exists(path):
            df=pd.read_csv(path, sep="\t")
            #load to objet
            for ligne in df:
                corpus._add(ligne["id"],Document(ligne["titre"],ligne["auteur"],ligne["date"],ligne["url"],ligne["texte"]))

        return corpus