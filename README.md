# Ted Johnson Works website

This repository is the authoritative, deployment-ready website for `tedjohnsonworks.com`.

The files in the repository root are the finished static site. Deploy `main` directly to the website document root; no build command is required.

## Host-only files

The post-payment intake form submits to `/submit-checkup.php`. That handler and its private SMTP/environment configuration must remain on Hostinger and must never be committed to this public repository.

## Deployment boundary

- Deploy the repository root to `public_html`.
- Preserve the Hostinger-managed `submit-checkup.php` handler and its private configuration.
- Do not commit passwords, API keys, SMTP credentials, payment secrets, backups, or exported customer data.

