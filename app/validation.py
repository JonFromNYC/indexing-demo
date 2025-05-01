from typing import Dict

def is_valid_document(doc: Dict) -> bool:
    """
    Validates that a document contains required Glean fields.

    Args:
        doc (dict): The document to validate.

    Returns
        bool: True if valid, False otherwise.
    """
    try:
        d = doc["document"]

        if not isinstance(d.get("body"), dict):
            return False

        required_fields = [
            d.get("datasource"),
            d.get("objectType"),
            d.get("id"),
            d.get("title"),
            d["body"].get("mimeType"),
            d["body"].get("textContent"),
        ]

        return all(bool(field) for field in required_fields)
    except (KeyError, TypeError):
        return False
