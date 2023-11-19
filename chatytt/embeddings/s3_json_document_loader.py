from typing import List, Iterator, Optional

from langchain.document_loaders.base import BaseLoader
from langchain.schema import Document
from langchain.text_splitter import TextSplitter

from chatytt.utils.s3 import load_json_from_s3_as_dict


class S3JsonFileLoader(BaseLoader):
    def __init__(self, bucket, key, text_splitter: Optional[TextSplitter] = None):
        super().__init__()
        self.bucket = bucket
        self.key = key
        self.text_splitter = text_splitter

    def load(self, split_doc: bool = False) -> List[Document]:
        dict_obj = load_json_from_s3_as_dict(bucket=self.bucket, key=self.key)
        doc = [self._convert_to_document(dict_obj)]

        if split_doc:
            return self.apply_text_splitter(doc)

        return doc

    def _convert_to_document(self, dict_obj) -> Document:
        return Document(
            page_content=dict_obj["transcript"], metadata=self._get_metadata()
        )

    def apply_text_splitter(self, doc):
        if self.text_splitter is None:
            raise ValueError(
                "To split document, you must define a text_splitter "
                "when creating instance of S3JsonDocumentLoader"
            )

        return self.text_splitter.split_documents(doc)

    def _get_metadata(self) -> dict:
        return {"source": f"s3://{self.bucket}/{self.key}"}

    # Taken from langchain/document_loaders/base.py to avoid implementation when
    # this method is upgraded to abstractmethod in BaseLoader
    def lazy_load(
        self,
    ) -> Iterator[Document]:
        """A lazy loader for Documents."""
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement lazy_load()"
        )
