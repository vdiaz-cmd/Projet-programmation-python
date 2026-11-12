#projet
import json
import xmltodict
import urllib.parse
import urllib.request
from html import unescape
from Document import Document
from Author import Author

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

    doc = Document(titre, auteur, date, lien, texte)
    id2doc[id_doc] = doc
    id_doc += 1
    #4.2.3
    if auteur not in id2aut:
        id2aut[auteur] = Author(auteur)
    id2aut[auteur].add(id_doc, doc)
    id2doc[id_doc] = Document(titre, auteur, date, lien, texte)
    id_doc += 1

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

    doc = Document(titre, auteur, date, lien, texte)
    id2doc[id_doc] = doc
    id_doc += 1
    #4.2.3
    if auteur not in id2aut:
        id2aut[auteur] = Author(auteur)
    id2aut[auteur].add(id_doc, doc)
    id2doc[id_doc] = Document(titre, auteur, date, lien, texte)
    id_doc += 1

print("Taille du corpus :", len(id2doc))

#3.1
print("Nombre de documents: ", len(id2doc))

#3.2
for i, doc in id2doc.items():
    nb_mots = len(doc.texte.split(" "))
    nb_phrases = len(doc.texte.split("."))
    print("Document", i, ":", nb_mots, "mots,", nb_phrases, "phrases")

#3.3
id2doc = {i: doc for i, doc in id2doc.items() if len(doc.texte) >= 20}
print("Après filtrage :", len(id2doc))

#3.4
chaine = " ".join(doc.texte for doc in id2doc.values())
print("longueur de la chaine: ", len(chaine))

#4.2.4
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