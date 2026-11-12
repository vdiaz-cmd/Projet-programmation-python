#4.3.4 test the function save and load of Corpus
#save
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Document import Document
from Corpus import Corpus

corpus = Corpus("Corpus de test")

doc1 = Document(
    titre="Rain",
    auteur="Alice",
    date="2026-03-15",
    url="https://example.com/rain",
    texte="Rain falls."
)

doc2 = Document(
    titre="Clouds",
    auteur="Bob",
    date="2026-01-10",
    url="https://example.com/clouds",
    texte='Clouds bring rain, wind and "cool" weather.\nThe sky changes.'
)

doc3 = Document(
    titre="Sun",
    auteur="Alice",
    date="2026-02-20",
    url="https://example.com/sun",
    texte="The sun shines."
)

corpus.add(doc1)
corpus.add(doc2)
corpus.add(doc3)

print(corpus)

corpus.save()

#load
corpus = Corpus.load("Corpus de test.csv")
print(corpus)