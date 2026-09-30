# Ted Johnson Works website

This repository is the authoritative, deployment-ready website for `tedjohnsonworks.com`.

The files in the repository root are the finished static site; no build command is required. Approved changes merged to `main` run `.github/workflows/deploy-hostinger.yml`, which prepares the `hostinger` branch for the existing hosting connection. Do not manually deploy a review branch or dispatch the production workflow without publishing authorization.

## September 30 redesign review

The technology-led redesign is prepared on `redesign/technology-paid-work-2026-09-30`. See [the review report](.github/review/REDESIGN-REVIEW.md) for pages, pricing inventory, QA, and publishing decisions. Review screenshots and machine-readable QA are in `.github/review/`; that directory is excluded from production deployment.

Current $39 / $149 checkout copy remains aligned with unchanged payment destinations. The proposed $19.99 / $99 offers and revised durations are staged in `.github/tools/offers.json`. After authorized payment updates, `.github/tools/activate-offers.py` renders verified offer details into static pages. This is a maintenance step, not a hosting build dependency. `.github/tools/qa-static.py` checks references, disclosures, offer fields, and deployment boundaries.

## Host-only files

The post-payment intake form submits to `/submit-checkup.php`. The handler and PHPMailer runtime are versioned here. Its private SMTP password configuration must remain on Hostinger outside `public_html` and must never be committed.

## Deployment boundary

- Deploy the repository root to `public_html`.
- Preserve `~/domains/tedjohnsonworks.com/.tjw-private/mail-config.php` on Hostinger. It sits one level above `public_html`, outside the Git deployment target.
- Do not commit passwords, API keys, SMTP credentials, payment secrets, backups, or exported customer data.
