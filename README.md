# Ted Johnson Works

Official website and digital hub for Ted Johnson Works.

## Purpose

TedJohnsonWorks.com is the personal and commercial hub for Theodore “Ted” Johnson. It is intentionally separate from Leave One Light On and from the dedicated *The Light in the Window* book site.

The site is designed to grow across Ted's body of work: books, technology and AI, strength and bodybuilding, martial arts, cooking, stories, practical guides, and carefully disclosed recommendations.

## Stack

- Astro static site generation
- Lexend-first readable typography
- Responsive navy / ivory / gold design system
- Structured content in `src/data/site.ts`
- SEO canonical metadata, Person + WebSite structured data, robots.txt and sitemap.xml
- GitHub Actions build verification on every push and pull request

## Local development

```bash
npm install
npm run dev
```

Production build:

```bash
npm run build
```

Astro writes the static site to `dist/`.

## Content workflow

Most homepage offerings and future shelves are defined in `src/data/site.ts`. Updating that structured data updates the generated site without hand-editing repeated cards.

## Deployment target

Primary domain: `https://tedjohnsonworks.com`

Source of truth: the `main` branch of this GitHub repository.

GitHub Actions automatically builds `main` and force-publishes only the compiled static output to the `hostinger` branch. Hostinger should deploy that branch directly to the website root.

Recommended Hostinger Git settings:

- Repository: `leaveonelighton/Ted-Johnson-Works`
- Branch: `hostinger`
- Root directory: `public_html`
- Auto-deployment: enabled

Do not connect Hostinger directly to `main` for this static deployment path; `main` contains Astro source code while `hostinger` contains the production-ready HTML/CSS/assets.

Do not place Hostinger credentials or deployment secrets in repository files.
