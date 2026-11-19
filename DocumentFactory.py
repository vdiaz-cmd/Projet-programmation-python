from Document import HackerNewsDocument, ArxivDocument, DocumentType

class DocumentFactory:
    @staticmethod
    def create(doc_type, **fields):
        if doc_type == DocumentType.HACKER_NEWS:
            return HackerNewsDocument(**fields)
        if doc_type == DocumentType.ARXIV:
            return ArxivDocument(**fields)
        raise ValueError(f"Source inconnu : {doc_type}")
