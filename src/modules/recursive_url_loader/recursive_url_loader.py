from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_core.documents.base import Document
from bs4 import BeautifulSoup as Soup
from logging import getLogger

logger = getLogger(__name__)


def load_docs(url: str, max_depth: int, root_selector: str) -> list[Document]:
    loader = RecursiveUrlLoader(
        url=url,
        max_depth=max_depth,
        extractor=lambda x: (lambda y: y.get_text() if y else "None")(
            Soup(x, "html.parser").select_one(root_selector)
        ),
    )
    docs = loader.load()
    return docs


def transform_docs_to_csv_body(docs: list[Document]) -> list[dict]:
    csv_body = [
        {
            "source": doc.metadata["source"],
            "title": doc.metadata.get("title", "").replace("\n", "\\n"),
            "description": doc.metadata.get("description", "").replace("\n", "\\n"),
            "content": doc.page_content.replace("\n", "\\n"),
            "language": doc.metadata.get("language", ""),
            "docs_sync_at": doc.metadata.get("docs_updated_at", ""),
        }
        for doc in docs
    ]
    return csv_body


def read_data_and_load_csv(url_root, max_depth, selector="body") -> list[dict]:
    # URL配下のドキュメントを再起的に取得しCSVファイルに保存する
    docs = load_docs(url=url_root, max_depth=max_depth, root_selector=selector)
    logger.info(f"ページ数:{len(docs)}")
    csv_body = transform_docs_to_csv_body(docs)
    return csv_body
