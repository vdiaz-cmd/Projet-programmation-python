from datetime import datetime
from enum import Enum

class DocumentType(Enum):
    HACKER_NEWS = "HackerNews"
    ARXIV = "Arxiv"
    DOCUMENT = "Document"

class Document:
    def __init__(self,titre,auteur,date,url,texte):
        self.titre = titre
        self.auteur = auteur
        self.date = datetime.fromisoformat(date.replace("Z", ""))
        self.url = url
        self.texte = texte
        self.type = DocumentType.DOCUMENT

    def afficher(self):
        print("Titre :", self.titre)
        print("Auteur :", self.auteur)
        print("Date :",self.date)
        print("URL :", self.url)
        print("Texte :",self.texte)

    def __str__(self):
        return self.titre

    def to_dict(self):
        return {
            "titre": self.titre,
            "auteur": self.auteur,
            "date": self.date,
            "url": self.url,
            "texte": self.texte,
            "type": self.type
        }

class HackerNewsDocument(Document):
    def __init__(self, titre,auteur,date,url,texte,nb_comments=0):
     # super() = la classe mère : on lui laisse remplir les attributs communs
        super().__init__(titre,auteur,date,url,texte)
        self.nb_comments = nb_comments
        self.type = DocumentType.HACKER_NEWS

    #accesseur
    def get_nb_comments(self):
        return self.nb_comments

    #mutateur
    def set_nb_comments(self, nb_comments):
        if not isinstance(nb_comments,int) or nb_comments < 0:
            print("Nombre de commentaires invalides")
        else:
            self.nb_comments=nb_comments

    def __str__(self):
        return f"[Hacker News] {self.titre} ({self.nb_comments} commentaires)"


class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, autres_auteurs):
        super().__init__(titre, auteur, date, url, texte)
        self.autres_auteurs = autres_auteurs
        self.type = DocumentType.ARXIV        
    def __str__(self):
        return "[Arxiv]" + self.titre + "auteur" + self.auteur + "autres auteurs: ".join(self.autres_auteurs)
    def get_type(self):
        return self.type
    
