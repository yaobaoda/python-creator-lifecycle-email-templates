import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.infrai_client import InfraiClient
from src.lifecycle_templates import register_templates, template_for


recipient = os.environ.get("DEMO_EMAIL_TO")
if not recipient:
    raise SystemExit("DEMO_EMAIL_TO is required")

client = InfraiClient()
namespace = os.environ.get("TEMPLATE_NAMESPACE", "creator_demo")
register_templates(client, namespace)
chosen = template_for("processed")
sent = client.send_email(recipient, chosen.subject, chosen.html, f"lifecycle:{namespace}:processed:{recipient}")
print({"selected": chosen.name, "message_id": sent.get("message_id")})
