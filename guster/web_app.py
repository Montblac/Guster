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
        display_name = nickname or "No nickname available"
        nickname_html = (
            f'<h1 class="nickname">{html.escape(display_name)}</h1>'
            if nickname
            else '<h1 class="nickname empty">No nicknames found in <code>data/nicknames.txt</code>.</h1>'
        )

        if image_url:
            image_html = (
                '<figure class="image-frame">'
                f'<img src="{html.escape(image_url, quote=True)}" alt="Random Guster image" loading="eager" decoding="async" />'
                "</figure>"
                '<form method="post">'
                f'<input type="hidden" name="previous_image" value="{html.escape(image_url)}" />'
                f'<input type="hidden" name="previous_nickname" value="{html.escape(nickname or "")}" />'
                '<button type="submit">C&#39;mon, son. Another one.</button>'
                "</form>"
            )
        else:
            image_html = (
                '<p class="empty">No image URLs found in <code>data/image_urls.txt</code>. Add one URL per line.</p>'
                '<form method="post">'
                f'<input type="hidden" name="previous_nickname" value="{html.escape(nickname or "")}" />'
                '<button type="submit">C&#39;mon, son. Another one.</button>'
                "</form>"
            )

        return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <meta name="color-scheme" content="dark" />
  <title>Guster Generator</title>
  <style>
    :root {{
      --nord0: #2e3440;
      --nord1: #3b4252;
      --nord2: #434c5e;
      --nord3: #4c566a;
      --nord4: #d8dee9;
      --nord5: #e5e9f0;
      --nord6: #eceff4;
      --nord8: #88c0d0;
      --nord9: #81a1c1;
      --nord10: #5e81ac;
      --radius: clamp(0.6rem, 1.2vw, 1rem);
      --space: clamp(0.9rem, 2vw, 1.35rem);
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ height: 100%; }}
    body {{
      margin: 0;
      font-family: "Segoe UI Variable", "Segoe UI", "Inter", system-ui, sans-serif;
      background:
        radial-gradient(1000px 680px at 8% 8%, rgba(94, 129, 172, 0.34), transparent 60%),
        radial-gradient(780px 560px at 92% 92%, rgba(136, 192, 208, 0.2), transparent 62%),
        var(--nord0);
      color: var(--nord6);
      display: grid;
      place-items: center;
      padding: clamp(0.75rem, 1.9vw, 1.4rem);
    }}
    .container {{
      width: min(100%, 70rem);
      display: grid;
      gap: var(--space);
      text-align: center;
      background: linear-gradient(180deg, rgba(59, 66, 82, 0.93), rgba(46, 52, 64, 0.98));
      border: 1px solid rgba(216, 222, 233, 0.16);
      border-radius: var(--radius);
      box-shadow: 0 1rem 2rem rgba(0, 0, 0, 0.35);
      padding: clamp(1rem, 2.2vw, 1.8rem);
      backdrop-filter: blur(6px);
    }}
    .app-label {{
      margin: 0;
      font-size: 0.72rem;
      font-weight: 650;
      text-transform: uppercase;
      letter-spacing: 0.16em;
      color: var(--nord4);
      opacity: 0.82;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(1.25rem, 3.1vw, 2.45rem);
      letter-spacing: 0.02em;
      color: var(--nord5);
    }}
    .nickname {{
      margin: 0;
      font-size: clamp(1.1rem, 2.9vw, 2rem);
      font-weight: 700;
      color: var(--nord8);
      overflow-wrap: anywhere;
      line-height: 1.2;
    }}
    .image-frame {{
      margin: 0;
      width: 100%;
      min-height: clamp(14rem, 44vh, 36rem);
      display: grid;
      place-items: center;
      border-radius: calc(var(--radius) - 0.1rem);
      border: 1px solid rgba(216, 222, 233, 0.18);
      overflow: hidden;
      background: var(--nord1);
    }}
    img {{
      display: block;
      width: 100%;
      height: auto;
      max-height: min(72vh, 56rem);
      object-fit: contain;
    }}
    form {{ margin: 0; }}
    button {{
      width: min(100%, 18rem);
      border: 1px solid rgba(216, 222, 233, 0.26);
      border-radius: 999px;
      padding: 0.8rem 1.2rem;
      font: inherit;
      font-weight: 700;
      letter-spacing: 0.01em;
      color: var(--nord6);
      background:
        linear-gradient(165deg, rgba(136, 192, 208, 0.2), rgba(46, 52, 64, 0)) padding-box,
        linear-gradient(135deg, var(--nord10), var(--nord9)) border-box;
      box-shadow: 0 0.45rem 1.2rem rgba(94, 129, 172, 0.35);
      cursor: pointer;
      transition: filter 140ms ease, transform 140ms ease, box-shadow 140ms ease;
    }}
    button:hover {{
      filter: brightness(1.08);
      box-shadow: 0 0.65rem 1.35rem rgba(129, 161, 193, 0.42);
    }}
    button:active {{ transform: translateY(1px); }}
    button:focus-visible {{
      outline: 2px solid var(--nord8);
      outline-offset: 2px;
    }}
    code {{
      background: rgba(229, 233, 240, 0.12);
      border-radius: 0.35rem;
      padding: 0.08rem 0.34rem;
      color: var(--nord4);
    }}
    .empty {{ color: var(--nord4); }}
  </style>
</head>
<body>
  <main class=\"container\">
    <p class="app-label">Guster Nickname Generator</p>
    {nickname_html}
    {image_html}
  </main>
</body>
</html>"""

    def run(self):
        server = ThreadingHTTPServer((self.host, self.port), self.make_handler())
        print(f"Serving on http://{self.host}:{self.port}")
        server.serve_forever()
