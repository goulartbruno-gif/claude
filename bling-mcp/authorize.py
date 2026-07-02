import secrets
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

import bling_client

_result: dict = {}


class CallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        _result["code"] = query.get("code", [None])[0]
        _result["state"] = query.get("state", [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("<h1>Autorizado. Pode fechar esta aba.</h1>".encode("utf-8"))


def main():
    if not bling_client.CLIENT_ID or not bling_client.CLIENT_SECRET:
        print("Defina BLING_CLIENT_ID e BLING_CLIENT_SECRET antes de rodar este script.")
        sys.exit(1)

    redirect = urlparse(bling_client.REDIRECT_URI)
    port = redirect.port or 8765

    state = secrets.token_urlsafe(16)
    url = bling_client.build_authorize_url(state)
    print(f"Abrindo o navegador para autorizar o app no Bling:\n{url}\n")
    webbrowser.open(url)

    server = HTTPServer(("localhost", port), CallbackHandler)
    print(f"Aguardando o redirect em {bling_client.REDIRECT_URI} ...")
    server.handle_request()

    if _result.get("state") != state:
        print("State não bate — aborta por segurança (possível CSRF).")
        sys.exit(1)
    if not _result.get("code"):
        print("Não recebeu o parâmetro 'code' no callback.")
        sys.exit(1)

    tokens = bling_client.exchange_code(_result["code"])
    print(f"Tokens salvos em {bling_client.TOKENS_FILE}. Acesso expira em {tokens.get('expires_in')}s.")


if __name__ == "__main__":
    main()
