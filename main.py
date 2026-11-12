#projet
import json
import xmltodict
import urllib.parse
from html import unescape
import pandas as pd
import os


theme= "climate"

#2.3
if os.path.exists("corpus.csv"):
    df=pd.read_csv("corpus.csv", sep="\t")
    df["texte"] = df["texte"].fillna("")
else:
    docs=[]
    origines = []

    #1.1
    param = urllib.parse.urlencode({"query": theme, "tags": "story", "hitsPerPage": 50}) 
    url = "https://hn.algolia.com/api/v1/search?" + param
    print(url)

    with urllib.request.urlopen(url) as reponse:
        donnees = json.loads(reponse.read().decode("utf-8"))

    print(donnees.keys())               # champ réponse complete
    print(donnees["hits"][0].keys())    # champ 1 résultat

    # Le champ contenant le contenu textuel est story_text. Il est absent des
    # documents qui ne pointent que vers un lien extérieur : dans ce cas on se
    # rabat sur le titre (champ title), toujours présent.
    for hit in donnees["hits"]:
        texte = hit.get("story_text")    # champ qui contient texte (none si le champ n'existe pas)
        if not texte:
            texte = hit["title"]
            # le texte contient du HTML : <p> pour les paragraphes et des caractères
            # échappés comme &#x27; pour l'apostrophe
        texte = texte.replace("<p>", " ")
        texte = unescape(texte)
        docs.append(texte)
        origines.append("hackernews")

    print("Documents Hacker News :", len(docs))

    #1.2
    params= urllib.parse.urlencode({"search_query": "all:" + theme, "start":0, "max_results": 50})
    urlx= "http://export.arxiv.org/api/query?" + params
    print(urlx)

    with urllib.request.urlopen(urlx) as reponse:
        d_arxiv= xmltodict.parse(reponse.read().decode("utf-8"))

    print(d_arxiv.keys())                # feed : la racine du document XML
    print(d_arxiv["feed"].keys())        # title, id, updated, entry...


    # Attention : s'il n'y a qu'un seul résultat, xmltodict renvoie un simple
    # dictionnaire et non une liste ; s'il n'y en a aucun, la clef entry est absente.
    #on veut que ce soit toujours une liste
    entrees = d_arxiv["feed"].get("entry", []) #on veut entry mais s'il n'existe pas, on a une liste vide
    #ainsi le cas de 0 articles ne provoque pas d'erreur

    if isinstance(entrees, dict): #demande, est-ce que est un dict? si oui (seulment un article), on l'enferme dans un liste
        entrees = [entrees]
        print(len(entrees))
        print(entrees[0].keys())             # les champs disponibles pour un article

    # Le champ contenant le contenu textuel est summary (le résumé de l'article).
    for entree in entrees:
        texte = entree["summary"].replace("\n", " ").strip()
        docs.append(texte)
        origines.append("arxiv")

    print("Taille du corpus :", len(docs))

    #2.1 et 2.2
    df = pd.DataFrame({"id": range(len(docs)), "texte": docs, "origine": origines})
    df.to_csv("corpus.csv", sep="\t", index=False)
    print(df.head())   


print(df.head())

#3.1

print("Nombre de documents: ", len(df))

#3.2
for i in range(len(df)):
    texte = df["texte"][i]
    nb_mots = len(texte.split(" ")) #séparer a chaque espace
    nb_phrases = len(texte.split(".")) #séparer a chaque point 
    print("Document", i, ":", nb_mots, "mots,", nb_phrases, "phrases")

#3.3

df= df[df["texte"].str.len()>=20] #str.len longueur de chaque element dans texte (str applique à chaque element de texte)
                                #len(df["texte"]) nº d'elements dans texte
print("Après filtrage :", len(df))

#3.4

chaine = " ".join(df["texte"])
print("longueur de la chaine: ", len(chaine))
