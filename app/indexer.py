import logging
from typing import Union
from app.validation import is_valid_document
import glean_indexing_api_client as indexing_api

def deliver(document: dict) -> dict | None:
    """
    Sends a single document to the Glean Indexing API.

    Args:
        document (dict): A dictionary representing a document.

    Returns
        dict | None: API response if successful, None if an error occurred.
    """
    # Check if the document is valid. Stop processing if not.
    if not is_valid_document(document):
        logging.error("Invalid document, skipping indexing.")
        return None
    
    connection = indexing_api.DocumentsAPI(get_api_client())

    try:
        response = connection.index_document(document=document)
        logging.info(f"indexed document id: {document['document']['id']}")
        return response
    except indexing_api.ApiException as e:
        logging.error(f"Exception when calling deliver() -> indexing_api: {e}")
        return None

def index_documents(documents: Union[dict, list[dict]]) -> None:
    """
    Indexes one or more documents with Glean.

    Args:
        documents (dict or list[dict]): A single document or list of documents.

    Returns
        None
    """
    if isinstance(documents, dict):
        documents = [documents]

    for doc in documents:
        deliver(doc)