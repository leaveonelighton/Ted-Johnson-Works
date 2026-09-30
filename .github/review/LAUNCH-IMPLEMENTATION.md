# Approved launch pricing — completion report

September 30, 2026. The approved redesign and launch pricing are implemented on PR #8's review branch. **Nothing has been merged, deployed, or posted to Nextdoor.** Publication still requires Ted's explicit authorization. This report supersedes the earlier redesign report's pricing/status sections.

## Verified checkout amounts

| Offer | Website copy | Verified live destination |
|---|---|---|
| Technology Clarity Call | Website Launch Rate — $19.99; Regular $39; 15–30 minutes | https://payhip.com/order?link=FrA7a&pricing_plan=PjWlK0XkGv — USD $19.99 base and total for US/Texas |
| Small Business Technology Checkup | Website Launch Rate — $99; Regular $149; up to 60 minutes plus concise written priorities | https://buy.stripe.com/4gM5kE5TI6cC4Y67x18Zq01 — USD $99.00; duration and deliverable displayed |
| Contract IT | Project/contract quote | No fixed rate or checkout introduced |

Both amounts were verified before HTML activation; observations are recorded in checkout-verification.json. No purchase was made or card details entered. Payhip verification used the seller session and public Cleburne test ZIP 76033. UK checkout calculated $4.00 tax / $23.99 total; location-dependent tax behavior is unchanged. Stripe preserves the original automatic-tax setting (off).

## Payment changes made

**Payhip:** Added a $19.99 website-launch plan to original coaching product W6nhP, then duplicated the product as unlisted FrA7a to avoid the inherited $39 graphic and 30-minute checkout title. Renamed the copy to Technology Clarity Call — Website Launch (15–30 minutes) and removed only its inherited thumbnail. Website launch checkout uses plan PjWlK0XkGv. Original W6nhP plan QyBbwR5LGD remains $39 / 30 minutes. The copy retains its copied $39 plan; the original retains the additional $19.99 plan bxGaM23aGD. No plans were deleted. Those extra plans are not website CTA destinations.

**Stripe:** Duplicated the existing $149 product/link into product prod_VMD9ASffqIZCfM and link plink_1ULUlrLjkDWvpCdxt02ukQ4q. Set its one-time USD price to $99, updated its title/description to the website launch offer, up to 60 minutes, concise written priorities, and Regular $149. Removed only the copy's inherited $149 graphic. The new link returns to https://tedjohnsonworks.com/business.html#start-checkup; the destination was opened and its intake section verified. The original $149 product/link remains unchanged, including its original return URL. Customer-name/phone collection, quantity 1 with adjustment disabled, payment methods, and other duplicated settings are preserved.

No bank, payout, tax configuration, legal entity, unrelated product, email setting, private configuration, secret, or deployment setting was changed.

## Exact files changed during launch implementation

Website:
- index.html
- business.html
- quick-tech-help.html
- assets/site.css

Maintenance:
- .github/tools/offers.json
- .github/tools/activate-offers.py
- .github/tools/qa-static.py
- .github/tools/qa-browser.cjs
- README.md

Review:
- .github/review/checkout-verification.json
- .github/review/LAUNCH-IMPLEMENTATION.md
- .github/review/static-launch-qa.json
- .github/review/external-launch-qa.json
- .github/review/browser-qa.json
- .github/review/home-mobile.png
- .github/review/mobile-menu.png
- .github/review/index-desktop.png
- .github/review/business-desktop.png
- .github/review/NEXTDOOR-LAUNCH-DRAFT.md

Activation updated all 21 staged fields in the three HTML pages and added six launch labels and six regular-price companions. Every price/duration location is listed in static-launch-qa.json. Existing $39/$149 amounts appear as regular comparisons in these service sections. All eight checkout buttons use the matching launch destinations. The checklist and strongest service copy remain intact. Contract IT and the other approved redesign pages remain in place.

## QA results

- Static: 19 pages, 503 internal references, 25 external destinations; no errors. Launch/regular labels, durations, checkout evidence/URLs, disclosures, and private-file/credential checks passed.
- Browser/mobile: 95 layouts at 320, 390, 768, 1024, and 1440 pixels; 317 assertions passed, no JavaScript errors. Visual review confirmed readable offer cards and retained visual identity.
- All eight checkout CTAs were clicked locally with outbound navigation intercepted; all opened the exact verified launch URLs. Actual checkout amounts were separately inspected in the cloud browser.
- Forms: missing/invalid-email validation, success/error states, all eight intake fields plus two anti-spam fields, POST method, handler destination, and timing field passed. Submission was intercepted; no live mail sent.
- All 30 triage paths, mobile Menu/More Works, Escape behavior, navigation without JavaScript, and photography album passed.
- Intake form/checklist comparison passed. PHP handler, PHPMailer, and deployment workflow unchanged during this pricing phase. No secrets or .tjw-private files added.
- Ran the existing workflow's production-preparation/validation block successfully; did not run its publish step. Main and hostinger branches unchanged.
- External links: 16/25 returned HTTP 200, including new payment destinations. Nine existing Amazon destinations returned 500/503 and require manual confirmation; see external-launch-qa.json. No affiliate links replaced or invented.
- Activation safeguards rejected missing/unverified evidence and wrong checkout amounts before writing HTML. Isolated activation/idempotence tests passed; synthetic evidence was not used as actual verification.

## Readiness and manual checks

Implementation is ready for final review. PR #8 remains draft and is **not cleared for merging/publication** until explicit publication authorization and remaining manual checks are addressed:

1. Guest/incognito Payhip checkout, scheduling, and client access. Amount verification used the seller session.
2. Optional authorized end-to-end purchase-to-intake and SMTP-delivery check. No real purchase or email delivery test performed.
3. Inspect nine Amazon destinations. Existing short link https://amzn.to/4h7p6JZ redirects to an Amazon orders page rather than a product; supply the correct affiliate destination if retained. Confirm book paperback/Kindle targets.
4. No launch expiration date was specified or invented. Optional cleanup of extra Payhip plans can be handled separately without affecting the verified website destination.
5. After authorized publication, verify the live homepage, both checkouts, intake return, and delivery before posting the [Nextdoor draft](NEXTDOOR-LAUNCH-DRAFT.md).

The Nextdoor post is prepared with launch prices, regular comparisons, durations, and written priorities. It has not been posted or scheduled. Leave One Light On remains separate.
