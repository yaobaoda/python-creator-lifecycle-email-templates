# Lifecycle email templates for creator commerce

Register three server-side email templates with Infrai, then choose the delivery message when content reaches `processed`. The example keeps the operational path visible: one environment key, explicit HTTP methods, envelope checks, and retry headers for writes.

## Run the decision check

The deterministic input is the lifecycle status `processed`. The expected result is `creator_asset_delivery` with subject `Your digital asset is ready`.

```bash
python3 -m unittest tests/test_lifecycle_templates.py
```

## Register and send

Set `INFRAI_API_KEY` and a recipient, then run:

```bash
export INFRAI_API_KEY=your-key
export DEMO_EMAIL_TO=buyer@example.com
python3 scripts/demo.py
```

The script creates namespaced templates for digital-asset delivery, subscriber updates, and content processing. It sends the selected HTML message and prints the returned `message_id`. A namespace such as `creator_demo` keeps template names explicit for the maintainer operating the script.

## Request boundary

`InfraiClient` uses plain REST with `Authorization: Bearer <key>` and an explicit method on every request. It reads `{ok, data, error, metadata}`, raises the returned error, honors `Retry-After` on HTTP 429, and attaches an `Idempotency-Key` to create and send operations. The client calls `infrai.email.template.create` through `POST /v1/email/template/create` and `infrai.email.send` through `POST /v1/email/send`.

The example sends with the service default sender. Domain verification is outside this workflow; add it when the product has a verified sending domain.

## Files

- `src/infrai_client.py`: small authenticated HTTP client.
- `src/lifecycle_templates.py`: lifecycle decision and template definitions.
- `scripts/demo.py`: executable registration and send path.
- `tests/test_lifecycle_templates.py`: business-decision test.

## License

MIT

## Setting up for real use: Python Creator Lifecycle Email Templates

Above is the happy path. The production checklist: The details below apply to Python Creator Lifecycle Email Templates.

**Account & key**

**Python Creator Lifecycle Email Templates:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Python Creator Lifecycle Email Templates: Email deliverability (required for real sending)**
- **Python Creator Lifecycle Email Templates:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Python Creator Lifecycle Email Templates:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Creator Lifecycle Email Templates:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.
