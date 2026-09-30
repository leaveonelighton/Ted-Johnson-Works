# Ted Johnson Works redesign — September 30, 2026

**Review version only. Not published. Payment services remain unchanged.**

Source: `leaveonelighton/Ted-Johnson-Works`, starting at main commit `e1cb8f75542e67e41f4dbc0b07aacf5b248d6d27`.

Review branch: `redesign/technology-paid-work-2026-09-30`.

## What changed

The homepage now answers “What can Ted help you with right now?” and leads with contract IT and paid technology services. Its order is contract/project work, Clarity Call, Business Checkup, practical AI, technology books/resources, brief credibility, and More Works.

Dark navy, gold, cream, Lexend, the original CSS assets, and the established card/button styling remain. New shared navigation includes Technology, Contract IT, Small Business, Practical AI, More Works, and About / Contact. More Works contains Body Works, Food Works, Photography, Stories, Books, and Ted Recommends. Mobile has an accessible Menu button; More Works works with keyboard controls. Navigation also works without JavaScript.

Contract IT is based on `Theodore_Johnson_Desktop_Refresh_Migration_Resume.docx`, read from Ted’s September 30 résumé. It covers desktop refresh, Windows migration, PC imaging/deployment, SCCM/endpoint rollout support, desk-side support, asset/lifecycle refresh, and short-term projects. The original Word résumé is available to download. Project contact asks for location, dates, device/user count, scope, and onsite/remote needs; no contract rate or availability was invented.

The Business Checkup retains its ten-question checklist, strongest service copy, service standard, scheduling expectations, written priorities, and post-payment intake. Leave One Light On is kept out of the homepage, service navigation, and technology offers; it remains a clearly separate outbound destination on Stories.

## Pages and files

| Page | Action |
|---|---|
| `index.html` | Technology-led homepage rebuilt; useful old anchors route to corresponding sections |
| `contract-it.html` | Added: project services, résumé-based experience, download, contact |
| `business.html` | Reorganized: current offers, checklist, original intake and standards |
| `quick-tech-help.html` | Added: Clarity Call, scope, preparation, triage link |
| `practical-ai.html` | Added: practical tasks, learning, original AI/book/article links |
| `body-works.html` | Added: existing fitness books and Vo Lam content moved here |
| `food-works.html` | Added: existing cookbook-in-development position and kitchen resource routes |
| `photography.html` | Existing album retained; renamed Ted Johnson Photography / Life in Pictures |
| `stories.html` | Added: existing four articles, picture-story route, book, separate movement link |
| `picks.html` | Retained recommendations, categories, affiliate links/disclosures; renamed Ted Johnson Recommends |
| `books.html` | Added: existing technology, AI, fitness, story, and in-development book cards |
| `about.html` | Added: short background, email contact, résumé, purchased-checkup intake route |
| `start.html` | Rebuilt as a simple service/resource chooser |
| `triage.html` | Retained tool; stale payment prices replaced with service-page destinations |
| `martial-arts.html`, `articles/*.html` | Content retained; shared navigation/footer; service CTA routed to current details |
| `assets/site.css`, `assets/nav.js` | Added: responsive layout, More Works menu, mobile navigation, focus/reduced-motion support |
| `downloads/Theodore_Johnson_Desktop_Refresh_Migration_Resume.docx` | Added: original résumé, without rewriting the source document |
| `sitemap.xml` | Updated to all 19 actual static HTML pages |
| `.github/tools/offers.json`, `activate-offers.py`, `qa-static.py`, `qa-browser.cjs` | Added: staged pricing and pre-release checks, excluded from production deployment |
| `.github/review/*` | Review report, screenshots, and QA evidence; excluded from production deployment |
| `.github/workflows/deploy-hostinger.yml` | Same deployment path; fitness assertions now check Body Works; explicit private-file exclusions/check added |

No URLs were deleted. Existing photography and resource pages retain their paths. Original book cards moved to Books and Body Works with their links/disclosures. No new products, affiliate links, catering offers, or photography rates were invented. The photography page still contains its existing archive placeholders; this task does not substitute invented photographs.

## Pricing awaiting authorization

| Offer | Review version / current checkout | Prepared offer |
|---|---|---|
| Technology Clarity Call | $39, 30 minutes, existing Payhip URL | **$19.99, 15–30 minutes** |
| Small Business Technology Checkup | $149, about 60–90 minutes, existing Stripe URL | **$99, up to 60 minutes**, plus concise written priorities |

**The public-facing review copy intentionally retains current prices.** New pricing is staged in `.github/tools/offers.json`. A dry run activated it in a disposable copy and verified that all website $39/$149 prices and 60–90-minute durations were replaced. No payment setting was changed.

### Every original price/duration location

| Original location | Existing copy | Preparation in redesign |
|---|---|---|
| `business.html`, Clarity comparison heading | “30-Minute Small Business Technology Clarity Call — $39” | Separated name, marked price and duration fields |
| `business.html`, Clarity comparison path | “One issue → $39 Clarity Call” | Consolidated into the same offer card; no duplicate price |
| `business.html`, Clarity comparison button | “Book the $39 Clarity Call” | Price-free button; marked checkout URL |
| `business.html`, Checkup comparison heading | “Small Business Technology Checkup — $149” | Separated name, marked price and duration fields |
| `business.html`, Checkup comparison path | “Broader technology review → $149 Technology Checkup” | Consolidated into the same offer card; no duplicate price |
| `business.html`, Checkup comparison button | “Start the $149 Technology Checkup” | Price-free button; marked checkout URL |
| `business.html#checkup`, launch card heading | “$149 Small Business Technology Checkup” | Marked price field |
| `business.html#checkup`, launch card paragraph | “About 60–90 minutes” | Marked duration field |
| `business.html#service-standard`, scheduling card | “approximately 60–90 minutes” | Marked duration field |
| `triage.html`, business result JavaScript | “Start the $149 Business Checkup” | Links to Business Checkup details without duplicating pricing |
| `triage.html`, personal result JavaScript | “Get a $35 Clarity Call” (already stale) | Links to Quick Tech Help; obsolete $35 removed |
| Original `index.html` and `start.html` Clarity cards | “Thirty focused minutes” | Replaced with central service route or marked duration |
| `articles/how-i-keep-tedjohnsonworks-running.html`, CTA | “focused 30-minute Technology Clarity Call” | Price/duration-free service CTA linked to Quick Tech Help |

### Every current offer field to activate

- `index.html`: Clarity price, duration, checkout; Checkup price, duration, checkout — **6 fields**.
- `quick-tech-help.html#clarity-call`: price, duration, checkout — **3 fields**.
- `business.html`: hero Checkup checkout; comparison Clarity price/duration/checkout; comparison Checkup price/duration/checkout; launch-card price/duration/checkout; service-standard duration; final Checkup checkout — **12 fields**.

That is **21 fields**. Other routes link to these service pages rather than repeating a price. The exact inventory is in `static-qa.json`.

After authorized payment updates and verification of the checkout amounts, run:

```bash
python -m pip install beautifulsoup4
python .github/tools/activate-offers.py --payments-verified \
  --clarity-url 'VERIFIED_HTTPS_CLARITY_CHECKOUT_URL' \
  --checkup-url 'VERIFIED_HTTPS_CHECKUP_CHECKOUT_URL'
python .github/tools/qa-static.py
```

This edits website files only. It does not change Stripe or Payhip. Review the resulting diff and obtain publishing authorization before merging to main.

If website-only pricing is chosen, the Clarity Call needs a checkout that charges $19.99 while the existing Payhip offer remains $39. Simply showing $19.99 next to the existing $39 payment page would be misleading. The actual new links or price changes must be verified before activation. $99 follows the latest instruction; earlier discussion of $99.99 has not been carried into this plan.

## QA evidence

- **Internal references:** 503 checked across 19 HTML pages; zero missing files, broken anchors, or duplicate IDs. Includes CSS, JavaScript, résumé, navigation, and content links.
- **Responsive layout:** all 19 pages checked at 320, 390, 768, 1024, and 1440 pixels; 95 page/viewport combinations. Browser QA completed 297 assertions with no JavaScript errors. Intentional off-screen carousel slides and the anti-spam honeypot are excluded from page-overflow assertions.
- **Navigation:** mobile Menu and More Works tested, Escape controls tested, navigation checked without JavaScript.
- **Forms:** required/invalid email validation, timing-field initialization, success/error states, POST method, all eight intake fields, and two anti-spam fields checked. Browser submission was intercepted locally; nothing was submitted to the live handler or emailed.
- **Triage:** all 30 category/context/urgency combinations checked, including reset and correct service destination.
- **Preservation:** checklist text and form DOM identical to baseline; original photography album DOM retained; original recommendation destinations retained; `submit-checkup.php` and PHPMailer unchanged.
- **External destinations:** 25 actual outbound link destinations checked. 16 returned HTTP 200, including existing Stripe, all three Payhip URLs, the separate book/movement sites, and ten Amazon short links. Nine Amazon links returned HTTP 500/503 and need manual confirmation; they were preserved. Preconnect roots and future canonical page URLs are not counted as broken external links.
- **Pricing activation:** disposable-copy dry run passed for all 21 fields; no old $39/$149 or 60–90-minute copy remained in that activated copy. The review branch retains current pricing.
- **Deployment preparation:** rsync exclusions and required production assets/assertions simulated successfully. Main-to-hostinger deployment path retained. No production push or workflow dispatch performed.
- **Secrets:** tracked/pending files checked for private config paths and common credential signatures. No `.tjw-private`, `.env`, credentials, or customer data introduced. Git whitespace check passed.

**Limits:** SMTP delivery and a real payment-to-intake transaction were not exercised because live service changes/testing were not authorized. PHP is not installed in this execution environment; the unchanged handler was checked by preservation, not a new PHP execution test. Successful HTTP responses confirm reachability, not that a transaction completes or that a checkout amount has changed.

The nine Amazon destinations requiring confirmation are:

- `https://amzn.to/4cFb1C8` — paperback button, Body Works and Books
- `https://amzn.to/4cHQVqW` — Kindle button, Body Works and Books
- `https://amzn.to/4d5znF7` — existing martial-arts link
- `https://amzn.to/4h7p6JZ` — Amazon Prime
- `https://amzn.to/4rdu38Q` — Audible
- `https://amzn.to/4xLbAmg` — fitness book resource card
- Existing Amazon search links for The Computer Skills Nobody Taught You, The No-Nonsense Home Technology Checklist, and The Owner’s Manual for the Human Body — Stewardship.

## Ted’s decisions before publishing

1. Approve the redesign after reviewing the screenshots/pages.
2. Choose website-only special pricing or the same prices everywhere. Payhip remains unchanged until explicitly authorized.
3. Authorize the necessary payment updates/new checkout links and verify $19.99 / $99 against the actual destinations; then activate website copy.
4. Confirm the nine Amazon destinations manually or provide replacement links if they also fail in a normal browser.
5. Authorize merging/publishing. Merging to main automatically starts the existing production deployment.

Contract rates, travel radius, food services, and photography sales can be decided later. Their current pages do not promise unapproved offers. After the site and prices are ready, prepare the final TJW Nextdoor post. No Nextdoor post was published or queued.
