"""Local preview of public/ that answers like Cloudflare (wrangler.jsonc):
/page serves page.html, /page.html redirects to /page, and any address
that doesn't exist gets 404.html with status 404.

    python tools/serve.py [port]
"""
import http.server
import os
import sys
from functools import partial

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public')
# read by Cloudflare as settings, never served
CONFIG_FILES = {'_headers', '_redirects'}
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5500


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, '.webp': 'image/webp'}

    def do_GET(self):
        if self.route():
            super().do_GET()

    def do_HEAD(self):
        if self.route():
            super().do_HEAD()

    def route(self):
        path, sep, query = self.path.partition('?')
        if path.endswith('.html'):
            clean = path[:-len('.html')]
            if clean.endswith('/index'):
                clean = clean[:-len('index')]
            self.send_response(308)
            self.send_header('Location', clean + sep + query)
            self.end_headers()
            return False
        # dotfiles (.git and the like) are never deployed
        if any(part.startswith('.') for part in path.split('/')) or path.strip('/') in CONFIG_FILES:
            return self.not_found()
        fs = self.translate_path(path)
        if os.path.isfile(fs):
            return True
        if os.path.isdir(fs):
            return os.path.isfile(os.path.join(fs, 'index.html')) or self.not_found()
        if os.path.isfile(fs + '.html'):
            self.path = path + '.html' + sep + query
            return True
        return self.not_found()

    def not_found(self):
        with open(os.path.join(ROOT, '404.html'), 'rb') as f:
            body = f.read()
        self.send_response(404)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)
        return False


if __name__ == '__main__':
    handler = partial(Handler, directory=ROOT)
    with http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler) as httpd:
        print(f'Serving {ROOT} at http://localhost:{PORT}', flush=True)
        httpd.serve_forever()
