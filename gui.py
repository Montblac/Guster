import html
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs


class WebApp:
    def __init__(self, images=None, nicknames=None, host='0.0.0.0', port=5000):
        self.images = images or []
        self.nicknames = nicknames or []
        self.host = host
        self.port = port

    def get_image_name(self, previous_image=None):
        if not self.images:
            return None

        choices = [name for name in self.images if name != previous_image]
        if not choices:
            choices = self.images
        return random.choice(choices)

    def get_nickname(self, previous_nickname=None):
        if not self.nicknames:
            return None

        choices = [name for name in self.nicknames if name != previous_nickname]
        if not choices:
            choices = self.nicknames
        return random.choice(choices)

    def make_handler(self):
        app = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                path = self.path.split('?', 1)[0]
                if path == '/':
                    query = self.path.split('?', 1)[1] if '?' in self.path else ''
                    params = parse_qs(query)
                    previous_image = params.get('previous_image', [None])[0]
                    previous_nickname = params.get('previous_nickname', [None])[0]
                    image_name = app.get_image_name(previous_image)
                    nickname = app.get_nickname(previous_nickname)
                    self._send_html(app.render_index(image_name, nickname))
                    return

                self.send_error(404, 'Not found')

            def do_POST(self):
                if self.path != '/':
                    self.send_error(404, 'Not found')
                    return

                length = int(self.headers.get('Content-Length', 0))
                params = parse_qs(self.rfile.read(length).decode('utf-8'))
                previous_image = params.get('previous_image', [None])[0]
                previous_nickname = params.get('previous_nickname', [None])[0]
                image_name = app.get_image_name(previous_image)
                nickname = app.get_nickname(previous_nickname)
                self._send_html(app.render_index(image_name, nickname))

            def do_HEAD(self):
                if self.path == '/':
                    html_doc = app.render_index(app.get_image_name(), app.get_nickname())
                    encoded = html_doc.encode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', str(len(encoded)))
                    self.end_headers()
                    return
                self.send_error(404, 'Not found')

            def _send_html(self, html_doc):
                encoded = html_doc.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

            def log_message(self, format, *args):
                return

        return Handler

    def render_index(self, image_name, nickname):
        nickname_html = (
            f'<p class="nickname">{html.escape(nickname)}</p>'
            if nickname else
            '<p class="nickname empty">No nicknames found in <code>nicknames.txt</code>.</p>'
        )

        if image_name:
            image_html = (
                f'<img src="{html.escape(image_name, quote=True)}" alt="Random Guster image" />'
                '<form method="post">'
                f'<input type="hidden" name="previous_image" value="{html.escape(image_name)}" />'
                f'<input type="hidden" name="previous_nickname" value="{html.escape(nickname or "")}" />'
                '<button type="submit">Generate another image</button>'
                '</form>'
            )
        else:
            image_html = (
                '<p>No image URLs found in <code>img</code>. Add one URL per line to the file.</p>'
                '<form method="post">'
                f'<input type="hidden" name="previous_nickname" value="{html.escape(nickname or "")}" />'
                '<button type="submit">Generate another nickname</button>'
                '</form>'
            )

        return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Guster Image Generator</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #708090;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
    }}
    .container {{
      width: min(90vw, 520px);
      text-align: center;
      background: rgba(0, 0, 0, 0.2);
      border-radius: 12px;
      padding: 20px;
    }}
    img {{
      width: 100%;
      max-height: 420px;
      object-fit: cover;
      border-radius: 10px;
      border: 2px solid rgba(255, 255, 255, 0.35);
    }}
    button {{
      margin-top: 16px;
      border: none;
      border-radius: 8px;
      background: #191970;
      color: white;
      font-size: 1rem;
      padding: 10px 18px;
      cursor: pointer;
    }}
    button:hover {{
      background: #0f0f4c;
    }}
  </style>
</head>
<body>
  <main class="container">
    <h1>Burton Guster Image Generator</h1>
    {nickname_html}
    {image_html}
  </main>
</body>
</html>'''

    def run(self):
        server = ThreadingHTTPServer((self.host, self.port), self.make_handler())
        print(f'Serving on http://{self.host}:{self.port}')
        server.serve_forever()
