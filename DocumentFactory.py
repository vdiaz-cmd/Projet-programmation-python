from Document import Document, HackerNewsDocument, ArxivDocument, DocumentType

class DocumentFactory:
    @staticmethod
    def create(doc_type, **fields):
        if doc_type == DocumentType.HACKER_NEWS:
            return HackerNewsDocument(**fields)
        if doc_type == DocumentType.ARXIV:
            return ArxivDocument(**fields)
        if doc_type == DocumentType.DOCUMENT:
            return Document(**fields)
        raise ValueError(f"DocumentType inconnu : {doc_type}")
