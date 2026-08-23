from dataclasses import dataclass

from .infrai_client import InfraiClient


@dataclass(frozen=True)
class LifecycleTemplate:
    name: str
    subject: str
    html: str


TEMPLATES = (
    LifecycleTemplate("creator_asset_delivery", "Your digital asset is ready", "<p>Your download is ready.</p>"),
    LifecycleTemplate("creator_subscriber_update", "A creator update is available", "<p>A new update is available.</p>"),
    LifecycleTemplate("creator_content_processing", "Your content is processing", "<p>We are processing your content.</p>"),
)


def template_for(status):
    if status == "processed":
        return TEMPLATES[0]
    if status == "subscriber_updated":
        return TEMPLATES[1]
    return TEMPLATES[2]


def register_templates(client, namespace):
    return [client.create_template(f"{namespace}_{item.name}", item.subject, item.html) for item in TEMPLATES]
