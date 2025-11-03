from flask import Flask, request, jsonify, render_template_string
from urllib.parse import unquote
import json

app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<html>
<head><title>Facebook Cookie to Token Converter</title></head>
<body>
  <h2>Facebook Cookie to Token Converter</h2>
  <form method="POST">
    <textarea name="cookie" rows="10" cols="60" placeholder="Yahan apni Facebook cookies daalein..."></textarea><br><br>
    <button type="submit">Convert</button>
  </form>
  {% if token %}
    <h3>Converted Token (JSON):</h3>
    <pre>{{ token }}</pre>
    <h3>Raw Cookie String (Use for API/Bot):</h3>
    <pre>{{ raw_cookie }}</pre>
  {% endif %}
</body>
</html>
'''

def cookie_to_token(cookie_str):
    # Cookies को JSON dictionary में convert करें
    cookies = cookie_str.split('; ')
    token_dict = {}
    for cookie in cookies:
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            token_dict[key] = unquote(value)
    return token_dict

def create_raw_cookie(cookie_dict):
    # Cookies की json dict को फिर से एक cookie string में बदलें
    parts = [f"{key}={value}" for key, value in cookie_dict.items()]
    return "; ".join(parts)

@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    raw_cookie = None
    if request.method == 'POST':
        cookie_str = request.form.get('cookie')
        if cookie_str:
            token_dict = cookie_to_token(cookie_str)
            token = json.dumps(token_dict, indent=4)
            raw_cookie = create_raw_cookie(token_dict)
    return render_template_string(HTML_FORM, token=token, raw_cookie=raw_cookie)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
