from flask import Flask, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import DEFAULT_BRANCH
from .security import webhook
from .tasks import sync_and_apply

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.post("/webhook/apply")
@webhook
def apply():
    if request.json.get("ref") != f"refs/heads/{DEFAULT_BRANCH}":
        return jsonify(message="not main branch, skipping")

    sync_and_apply.send()

    return jsonify(message="ok")
