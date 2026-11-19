from Document import HackerNewsDocument
from Document import DocumentType
from Document import ArxivDocument

class DocumentFactory:
    @staticmethod
    def create(doc_type, **fields):
        if doc_type == DocumentType.HACKER_NEWS:
            return HackerNewsDocument(**fields)
            pass

        if doc_type == DocumentType.ARXIV:
            return ArxivDocument(**fields)

        raise ValueError("Source inconnu : " + doc_type)
