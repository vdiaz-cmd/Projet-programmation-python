from datetime import datetime

class Document:
    def __init__(self,titre,auteur,date,url,texte):
        self.titre = titre
        self.auteur = auteur
        self.date = datetime.fromisoformat(date.replace("Z", ""))
        self.url = url
        self.texte = texte

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
            "texte": self.texte
        }