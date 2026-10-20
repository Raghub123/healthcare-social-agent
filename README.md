# Healthcare social content starter (zero-cost draft MVP)

This MVP generates a curated **template-based** social post and a 1080×1080 PNG. It does **not** call AI APIs, fetch live news, request approval automatically, or publish to any platform. Nothing is published without a later, separate publishing integration.

## Setup on iPad
1. Create a **private** GitHub repository. GitHub Free private repos have an included Actions quota; stay within the quota and avoid enabling paid overages.
2. Upload `generate.py` and `.github/workflows/drafts.yml` using GitHub's web editor (create each path), or upload these files from a desktop. GitHub's web upload UI may not preserve hidden folders; use **Add file → Create new file** for `.github/workflows/drafts.yml`.
3. Open repository **Settings → Actions → General → Workflow permissions**. Enable read/write workflow permissions, if your account allows it, so the workflow can commit draft files. Keep repository access limited to trusted users.
4. Open **Actions → Create healthcare content draft → Run workflow**.
5. After completion, open `drafts/YYYY-MM-DD.json` and matching PNG. Review manually. The workflow also runs Monday, Wednesday and Friday at 03:17 UTC (08:47 IST); scheduled runs can be delayed.

## Next stage
Introduce a protected approval gate (separate review and publishing workflows), a free-tier LLM with strict quota and fallback, and one official publishing integration. Never treat an editable JSON `approved` field alone as proof of authorization. Require a verified GitHub environment approval or trusted reviewer action before publishing; record platform post IDs to prevent duplicates. Keep tokens in GitHub Actions secrets. Use a service-specific account and minimum permissions. Do not post patient data, unverifiable clinical claims, or fabricated testimonials.
