from flask import Flask, request, jsonify, render_template_string
from urllib.parse import unquote
import json

app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<html>
<head><title>Cookie to Token Converter</title></head>
<body>
  <h2>Cookie to Token Converter</h2>
  <form method="POST">
    <textarea name="cookie" rows="10" cols="60" placeholder="Yahan apni cookie string daalein..."></textarea><br><br>
    <button type="submit">Convert</button>
  </form>
  {% if token %}
    <h3>Converted Token (JSON):</h3>
    <pre>{{ token }}</pre>
  {% endif %}
</body>
</html>
'''

def cookie_to_token(cookie_str):
    cookies = cookie_str.split('; ')
    token_dict = {}
    for cookie in cookies:
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            token_dict[key] = unquote(value)
    return json.dumps(token_dict, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    if request.method == 'POST':
        cookie_str = request.form.get('cookie')
        if cookie_str:
            token = cookie_to_token(cookie_str)
    return render_template_string(HTML_FORM, token=token)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
