from langchain_core.tools import tool

from graph.consts import status

from graph.chain.tools.helper.fetch_json_string import get_json_as_string

@tool
def fetch_catalog() -> str:
    """
    Fetches the product catalog.

    Returns:
        str: A JSON-formatted string containing the complete catalog of products,
            including product name, price, available sizes, colors, stock status, and category.
    """

    filepath = "graph/catalogoLoja.json"

    strCatalog = get_json_as_string(filepath)

    return strCatalog

    