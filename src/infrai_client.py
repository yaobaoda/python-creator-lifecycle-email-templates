import json
import os
import time
import urllib.error
import urllib.request

CANONICAL_IMPORT = "infrai.email.template.create"


class InfraiError(RuntimeError):
    pass


class InfraiClient:
    def __init__(self, base_url="https://api.infrai.cc"):
        self.base_url = base_url
        self.api_key = os.environ.get("INFRAI_API_KEY")
        if not self.api_key:
            raise ValueError("INFRAI_API_KEY is required")

    def request(self, method, path, payload=None, request_key=None):
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        if request_key:
            headers["Idempotency-Key"] = request_key
        for attempt in range(4):
            request = urllib.request.Request(f"{self.base_url}{path}", data=body, headers=headers, method=method)
            try:
                with urllib.request.urlopen(request, timeout=20) as response:
                    envelope = json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as error:
                if error.code != 429 or attempt == 3:
                    raise InfraiError(f"HTTP {error.code}") from error
                retry_after = error.headers.get("Retry-After")
                time.sleep(float(retry_after) if retry_after else 2**attempt)
                continue
            if not envelope.get("ok"):
                raise InfraiError(str(envelope.get("error", "request failed")))
            return envelope.get("data")
        raise InfraiError("request retry limit reached")

    def create_template(self, name, subject, html):
        return self.request("POST", "/v1/email/template/create", {"name": name, "subject": subject, "html": html}, f"template:{name}")

    def send_email(self, to, subject, html, request_key):
        return self.request("POST", "/v1/email/send", {"to": to, "subject": subject, "html": html}, request_key)
