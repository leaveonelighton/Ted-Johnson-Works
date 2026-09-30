# Ted Johnson Works website

This repository is the authoritative, deployment-ready website for `tedjohnsonworks.com`.

The files in the repository root are the finished static site; no build command is required. Approved changes merged to `main` run `.github/workflows/deploy-hostinger.yml`, which prepares the `hostinger` branch for the existing hosting connection. Do not manually deploy a review branch or dispatch the production workflow without publishing authorization.

## September 30 redesign review

The technology-led redesign is prepared on `redesign/technology-paid-work-2026-09-30`. See [the review report](.github/review/REDESIGN-REVIEW.md) for pages, pricing inventory, QA, and publishing decisions. Review screenshots and machine-readable QA are in `.github/review/`; that directory is excluded from production deployment.

The approved website launch offers are active on the review branch: Technology Clarity Call $19.99 / 15–30 minutes (Regular $39), and Small Business Technology Checkup $99 / up to 60 minutes with concise written priorities (Regular $149). Both live checkout amounts were verified before activation. Contract IT remains quote-based. See [the launch completion report](.github/review/LAUNCH-IMPLEMENTATION.md) for exact checkout links, product changes, QA, and remaining manual checks. Publication is not authorized.

`.github/tools/activate-offers.py` requires fresh matching checkout evidence before changing price copy. `.github/tools/qa-static.py` checks references, disclosures, offer fields, and deployment boundaries; `.github/tools/qa-browser.cjs` checks responsive layouts, navigation, forms, triage, and checkout-button navigation.

## Host-only files

The post-payment intake form submits to `/submit-checkup.php`. The handler and PHPMailer runtime are versioned here. Its private SMTP password configuration must remain on Hostinger outside `public_html` and must never be committed.

## Deployment boundary

- Deploy the repository root to `public_html`.
- Preserve `~/domains/tedjohnsonworks.com/.tjw-private/mail-config.php` on Hostinger. It sits one level above `public_html`, outside the Git deployment target.
- Do not commit passwords, API keys, SMTP credentials, payment secrets, backups, or exported customer data.
