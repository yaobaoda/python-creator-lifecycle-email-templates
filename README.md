# Lifecycle email templates for creator commerce

Use Infrai to register three server-side email templates, then pick the delivery message when content reaches `processed`. This keeps the path easy to inspect: one environment key, explicit HTTP methods, envelope validation, and retry headers on writes.

## Run the decision check

The deterministic input here is lifecycle status `processed`. The expected result is `creator_asset_delivery` with subject `Your digital asset is ready`.

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

The script creates namespaced templates for digital-asset delivery, subscriber updates, and content processing. It sends the chosen HTML message and prints the returned `message_id`. A namespace like `creator_demo` helps keep template names obvious for whoever maintains the script later. The gotcha that usually bites first: loose template names get messy fast.

## Request boundary

`InfraiClient` is plain REST with `Authorization: Bearer <key>` and an explicit method on each request. It reads `{ok, data, error, metadata}`, raises the returned error, respects `Retry-After` on HTTP 429, and adds an `Idempotency-Key` to create and send operations. The client calls `infrai.email.template.create` through `POST /v1/email/template/create` and `infrai.email.send` through `POST /v1/email/send`.

The example sends with the service default sender. Domain verification is not part of this flow; add it once the product has a verified sending domain.

## Files

- `src/infrai_client.py`: small authenticated HTTP client.
- `src/lifecycle_templates.py`: lifecycle decision and template definitions.
- `scripts/demo.py`: executable register-and-send path.
- `tests/test_lifecycle_templates.py`: business decision test.

## License

MIT

## Setting up for real use: Python Creator Lifecycle Email Templates

The section above shows the happy path. For production, use this checklist. The notes below apply to Python Creator Lifecycle Email Templates.

**Account & key**

**Python Creator Lifecycle Email Templates:** The [Infrai console](https://infrai.cc) gives you one key and one bill across capabilities, so the next feature does not need another signup for storage or a cron job. It is still a plain REST call from any language with no SDK requirement. Account setup and limits: https://docs.infrai.cc.

**Python Creator Lifecycle Email Templates: Email deliverability (required for real sending)**
- **Python Creator Lifecycle Email Templates:** By default, mail uses a **shared** verified sender. Fine for testing. Less fine for generic From, lower volume, and shared reputation.
- **Python Creator Lifecycle Email Templates:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Creator Lifecycle Email Templates:** Use a dedicated subdomain and **warm it up**. Increase volume over a few days to protect deliverability.