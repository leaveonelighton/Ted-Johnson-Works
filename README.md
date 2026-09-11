# Ted Johnson Works website

This repository is the authoritative, deployment-ready website for `tedjohnsonworks.com`.

The files in the repository root are the finished static site. Deploy `main` directly to the website document root; no build command is required.

## Host-only files

The post-payment intake form submits to `/submit-checkup.php`. The handler and PHPMailer runtime are versioned here. Its private SMTP password configuration must remain on Hostinger outside `public_html` and must never be committed.

## Deployment boundary

- Deploy the repository root to `public_html`.
- Preserve `~/domains/tedjohnsonworks.com/.tjw-private/mail-config.php` on Hostinger. It sits one level above `public_html`, outside the Git deployment target.
- Do not commit passwords, API keys, SMTP credentials, payment secrets, backups, or exported customer data.
