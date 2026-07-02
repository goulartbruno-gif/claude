import logging
import sys

from fastmcp import FastMCP

import bling_client

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

mcp = FastMCP("Bling")


@mcp.tool()
def bling_request(method: str, path: str, params: dict | None = None, json_body: dict | None = None) -> dict:
    """Make an authenticated request to the Bling API v3 (e.g. method="GET", path="/Api/v3/produtos").
    Prefer GET for exploration — POST/PUT/DELETE mutate real fiscal and inventory data.
    Consult https://developer.bling.com.br/referencia for the resource paths and payload shapes;
    only /Api/v3/produtos has been verified when this tool was built."""
    return bling_client.api_request(method, path, params, json_body)


@mcp.tool()
def bling_list_products(page: int = 1) -> dict:
    """List products from Bling (GET /Api/v3/produtos), paginated."""
    return bling_client.api_request("GET", "/Api/v3/produtos", params={"pagina": page})


if __name__ == "__main__":
    logger.info("Starting Bling MCP server...")
    mcp.run()
