#projet
import json
import xmltodict
import urllib.parse
import urllib.request
from html import unescape
from Document import HackerNewsDocument, ArxivDocument
from Document import Document
from Author import Author
from Corpus import Corpus
from DocumentFactory import DocumentFactory
from Document import DocumentType

theme = "climate"

id2doc = {}
id2aut = {}
id_doc = 0

#1.1 Hacker News
param = urllib.parse.urlencode({"query": theme, "tags": "story", "hitsPerPage": 50})
url = "https://hn.algolia.com/api/v1/search?" + param
print(url)

with urllib.request.urlopen(url) as reponse:
    donnees = json.loads(reponse.read().decode("utf-8"))

for hit in donnees["hits"]:
    texte = hit.get("story_text")
    if not texte:
        texte = hit["title"]
    texte = texte.replace("<p>", " ")
    texte = unescape(texte)

    titre = hit["title"]
    auteur = hit["author"]
    date = hit["created_at"]
    lien = hit.get("url") or "https://news.ycombinator.com/item?id=" + str(hit["objectID"])

    doc = DocumentFactory.create(DocumentType.HACKER_NEWS, titre=titre, auteur=auteur,
                                 date=date, url=lien, texte=texte,
                                 nb_comments=hit.get("num_comments") or 0)
    id2doc[id_doc] = doc

    if auteur not in id2aut:
        id2aut[auteur] = Author(auteur)
    id2aut[auteur].add(id_doc, doc)

    id_doc += 1          # après l'ajout de l'auteur, pour garder le même id

print("Documents Hacker News :", len(id2doc))

#1.2 arXiv
params = urllib.parse.urlencode({"search_query": "all:" + theme, "start": 0, "max_results": 50})
urlx = "http://export.arxiv.org/api/query?" + params
print(urlx)

with urllib.request.urlopen(urlx) as reponse:
    d_arxiv = xmltodict.parse(reponse.read().decode("utf-8"))

entrees = d_arxiv["feed"].get("entry", [])
if isinstance(entrees, dict):
    entrees = [entrees]

for entree in entrees:
    texte = entree["summary"].replace("\n", " ").strip()

    titre = entree["title"].replace("\n", " ").strip()
    date = entree["published"]
    lien = entree["id"]
    auteurs = entree["author"]
    if isinstance(auteurs, dict):
        auteurs = [auteurs]
    auteur = auteurs[0]["name"]
    autres_auteurs = [a["name"] for a in auteurs[1:]]

    doc = DocumentFactory.create(DocumentType.ARXIV, titre = titre, auteur = auteur,date = date, url = lien, texte = texte, autres_auteurs = autres_auteurs)
    id2doc[id_doc] = doc

    if auteur not in id2aut:
        id2aut[auteur] = Author(auteur)
    id2aut[auteur].add(id_doc, doc)

    id_doc += 1

print("Taille du corpus :", len(id2doc))

print("Nombre de documents: ", len(id2doc))

for i, doc in id2doc.items():
    nb_mots = len(doc.texte.split(" "))
    nb_phrases = len(doc.texte.split("."))
    print("Document", i, ":", nb_mots, "mots,", nb_phrases, "phrases")


corpus = Corpus.get_instance("corpus_" + theme)

for doc in id2doc.values():
    corpus.add(doc)
print(repr(corpus))

corpus.afficher_par_date(5)
corpus.afficher_par_titre(5)

corpus.save()
corpus2 = Corpus.load(corpus.nom + ".csv")
print(repr(corpus2))

# --- filtrage et statistiques ---
id2doc = {i: doc for i, doc in id2doc.items() if len(doc.texte) >= 20}
print("Après filtrage :", len(id2doc))

chaine = " ".join(doc.texte for doc in id2doc.values())
print("longueur de la chaine: ", len(chaine))

nom = input("Entrez le nom de l'auteur : ")

if nom in id2aut:
    author = id2aut[nom]

    nombre = len(author.production)
    total = 0

    for doc in author.production.values():
        total += len(doc.texte)

    if nombre > 0:
        moyenne = total / nombre
    else:
        moyenne = 0

    print(f"Nombre de documents : {nombre}")
    print(f"Taille moyenne : {moyenne:.2f} caractères")
else:
    print("Auteur inconnu")

#test td5 partie 3 3.1
    
doc1 = HackerNewsDocument("Titre 1", "Alice", "2024-01-01", "http://...", "Texte...", nb_comments=5)
doc2 = ArxivDocument("Titre 2", "Bob", "2024-02-01", "http://...", "Texte...",
                     autres_auteurs=["Carlos", "Diana"])

assert doc1.type == DocumentType.HACKER_NEWS
assert doc2.type == DocumentType.ARXIV

n_avant = corpus.ndoc
corpus.add(doc1)
corpus.add(doc2)

assert corpus.ndoc == n_avant + 2
assert "Alice" in corpus.authors
assert "Bob" in corpus.authors
print("Partie 3.1 OK")

#test td5 partie 4.1 patron Singleton

c1 = Corpus.get_instance("corpus_" + theme)
c2 = Corpus.get_instance("otro_nombre")
assert c1 is c2          # es el mismo objeto
print("Singleton OK")

