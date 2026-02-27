import html
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


class GusterWebApp:
    def __init__(
        self,
        image_urls: list[str] | None = None,
        nicknames: list[str] | None = None,
        host: str = "localhost",
        port: int = 5000,
    ):
        self.image_urls = image_urls or []
        self.nicknames = nicknames or []
        self.host = host
        self.port = port

    @staticmethod
    def _choose_different(options: list[str], previous_value: str | None = None) -> str | None:
        if not options:
            return None

        candidates = [value for value in options if value != previous_value]
        if not candidates:
            candidates = options
        return random.choice(candidates)

    def get_image_url(self, previous_image: str | None = None) -> str | None:
        return self._choose_different(self.image_urls, previous_image)

    def get_nickname(self, previous_nickname: str | None = None) -> str | None:
        return self._choose_different(self.nicknames, previous_nickname)

    def make_handler(self):
        app = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urlparse(self.path)
                if parsed.path != "/":
                    self.send_error(404, "Not found")
                    return

                params = parse_qs(parsed.query)
                previous_image = params.get("previous_image", [None])[0]
                previous_nickname = params.get("previous_nickname", [None])[0]
                image_url = app.get_image_url(previous_image)
                nickname = app.get_nickname(previous_nickname)
                self._send_html(app.render_index(image_url, nickname))

            def do_POST(self):
                if self.path != "/":
                    self.send_error(404, "Not found")
                    return

                length = int(self.headers.get("Content-Length", 0))
                params = parse_qs(self.rfile.read(length).decode("utf-8"))
                previous_image = params.get("previous_image", [None])[0]
                previous_nickname = params.get("previous_nickname", [None])[0]
                image_url = app.get_image_url(previous_image)
                nickname = app.get_nickname(previous_nickname)
                self._send_html(app.render_index(image_url, nickname))

            def do_HEAD(self):
                if self.path != "/":
                    self.send_error(404, "Not found")
                    return

                html_doc = app.render_index(app.get_image_url(), app.get_nickname())
                encoded = html_doc.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()

            def _send_html(self, html_doc: str):
                encoded = html_doc.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

            def log_message(self, format, *args):
                return

        return Handler

    def render_index(self, image_url: str | None, nickname: str | None) -> str:
        nickname_html = (
            f'<p class="nickname">{html.escape(nickname)}</p>'
            if nickname
            else '<p class="nickname empty">No nicknames found in <code>data/nicknames.txt</code>.</p>'
        )

        if image_url:
            image_html = (
                f'<img src="{html.escape(image_url, quote=True)}" alt="Random Guster image" />'
                '<form method="post">'
                f'<input type="hidden" name="previous_image" value="{html.escape(image_url)}" />'
                f'<input type="hidden" name="previous_nickname" value="{html.escape(nickname or "")}" />'
                '<button type="submit">Generate another</button>'
                "</form>"
            )
        else:
            image_html = (
                "<p>No image URLs found in <code>data/image_urls.txt</code>. Add one URL per line.</p>"
                '<form method="post">'
                f'<input type="hidden" name="previous_nickname" value="{html.escape(nickname or "")}" />'
                '<button type="submit">Generate another nickname</button>'
                "</form>"
            )

        return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Guster Generator</title>
  <style>
    body {{ margin: 2rem auto; max-width: 42rem; padding: 0 1rem; font-family: Arial, sans-serif; }}
    .container {{
      text-align: center;
      border: 1px solid #ddd;
      border-radius: 10px;
      padding: 1rem;
    }}
    .nickname {{ font-size: 1.1rem; font-weight: 700; }}
    img {{ width: 100%; max-height: 420px; object-fit: cover; border-radius: 8px; }}
    button {{ margin-top: 1rem; padding: 0.6rem 1rem; }}
  </style>
</head>
<body>
  <main class=\"container\">
    <h1>Burton Guster Generator</h1>
    {nickname_html}
    {image_html}
  </main>
</body>
</html>"""

    def run(self):
        server = ThreadingHTTPServer((self.host, self.port), self.make_handler())
        print(f"Serving on http://{self.host}:{self.port}")
        server.serve_forever()
