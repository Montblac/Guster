import html
import mimetypes
import os
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse, quote


class WebApp:
    def __init__(self, images=None, host='0.0.0.0', port=5000):
        self.images = images or []
        self.host = host
        self.port = port
        self.image_dir = Path(os.getcwd()) / 'images'
        self.image_names = [Path(path).name for path in self.images]

    def get_image_name(self, previous_image=None):
        if not self.image_names:
            return None

        choices = [name for name in self.image_names if name != previous_image]
        if not choices:
            choices = self.image_names
        return random.choice(choices)

    def resolve_image_path(self, image_name):
        if not image_name:
            return None

        candidate = (self.image_dir / image_name).resolve()
        try:
            candidate.relative_to(self.image_dir.resolve())
        except ValueError:
            return None

        if not candidate.is_file():
            return None
        return candidate

    def make_handler(self):
        app = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urlparse(self.path)
                if parsed.path == '/':
                    previous_image = parse_qs(parsed.query).get('previous_image', [None])[0]
                    image_name = app.get_image_name(previous_image)
                    self._send_html(app.render_index(image_name))
                    return

                if parsed.path.startswith('/images/'):
                    image_name = parsed.path.replace('/images/', '', 1)
                    self._send_image(image_name)
                    return

                self.send_error(404, 'Not found')

            def do_POST(self):
                if self.path != '/':
                    self.send_error(404, 'Not found')
                    return

                length = int(self.headers.get('Content-Length', 0))
                params = parse_qs(self.rfile.read(length).decode('utf-8'))
                previous_image = params.get('previous_image', [None])[0]
                image_name = app.get_image_name(previous_image)
                self._send_html(app.render_index(image_name))

            def do_HEAD(self):
                if self.path == '/':
                    html_doc = app.render_index(app.get_image_name())
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

            def _send_image(self, image_name):
                image_path = app.resolve_image_path(image_name)
                if not image_path:
                    self.send_error(404, 'Image not found')
                    return

                content_type = mimetypes.guess_type(str(image_path))[0] or 'application/octet-stream'
                data = image_path.read_bytes()
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, format, *args):
                return

        return Handler

    def render_index(self, image_name):
        if image_name:
            image_src = quote(image_name)
            image_html = (
                f'<img src="/images/{image_src}" alt="Random Guster image" />'
                '<form method="post">'
                f'<input type="hidden" name="previous_image" value="{html.escape(image_name)}" />'
                '<button type="submit">Generate another image</button>'
                '</form>'
            )
        else:
            image_html = '<p>No images found in the <code>images/</code> directory.</p>'

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
    {image_html}
  </main>
</body>
</html>'''

    def run(self):
        server = ThreadingHTTPServer((self.host, self.port), self.make_handler())
        print(f'Serving on http://{self.host}:{self.port}')
        server.serve_forever()
