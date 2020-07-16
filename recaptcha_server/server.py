#Python 3
import json
import urllib.request
import urllib.parse
from os import curdir, sep
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

SITE_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
SITE_SECRET = b'6LfeHx4UAAAAAFWXGh_xcL0B8vVcXnhn9q_SnQ1b'
RECAPTCHA_RESPONSE_PARAM = b'g-recaptcha-response'

class Handler(BaseHTTPRequestHandler):
  def set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def get_html_text(self):
    return open(curdir + sep + 'feedback.html').read().encode()

  def do_GET(self):
    self.set_headers();
    htmltext = self.get_html_text();
    self.wfile.write(htmltext % b'')

  def do_POST(self):
    self.set_headers();
    post_body = parse_qs(self.rfile.read(int(self.headers['Content-Length'])))

    success = False
    if RECAPTCHA_RESPONSE_PARAM in post_body:
      token = post_body[RECAPTCHA_RESPONSE_PARAM][0]
      resp = urllib.request.urlopen(
          SITE_VERIFY_URL, urllib.parse.urlencode(
              {'secret': SITE_SECRET, 'response': token}, True).encode()).read()
      if json.loads(resp).get("success"):
        success = True

    if success:
      message = 'Thanks for the feedback!'
    else:
      message = 'There was an error.'

    htmltext = self.get_html_text();
    self.wfile.write(htmltext % message.encode())

if __name__ == '__main__':
  httpd = HTTPServer(('', 8080), Handler)
  httpd.serve_forever()
  print("Server is running at http://localhost:8080")
