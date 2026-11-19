from Document import HackerNewsDocument
from Document import Source
from Document import ArxivDocument

class DocumentFactory:
    @staticmethod
    def create(source, **fields):
        if source == Source.HACKER_NEWS:
            return HackerNewsDocument(**fields)
            pass

        if source == Source.ARXIV:
            return ArxivDocument(**fields)

        raise ValueError("Source inconnu : " + source)
