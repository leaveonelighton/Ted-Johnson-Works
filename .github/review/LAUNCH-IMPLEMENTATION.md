# Approved launch pricing — implementation status

September 30, 2026. The redesign and pricing structure are approved. Publication is **not** authorized. PR #8 remains a draft and must not be merged.

| Offer | Approved website launch rate | Regular offer | Checkout status |
|---|---|---|---|
| Technology Clarity Call | $19.99, 15–30 minutes | Preserve $39 / 30-minute Payhip offer separately where practical | Created unlisted product `FrA7a`; direct launch checkout verified USD $19.99 base and total for US/Texas |
| Small Business Technology Checkup | $99, up to 60 minutes, concise written priorities | Regular $149 | Not created or verified; Stripe installation confirmed, but payment tools were not exposed in this session |
| Contract IT | Project/contract quote | No fixed rate | Remains quote-based |

## Safe implementation prepared

- `.github/tools/offers.json`: approved launch label, regular-price wording, duration, and exact amounts in cents (1999 / 9900).
- `.github/tools/activate-offers.py`: requires a recorded, live, matching checkout observation for **both** offers before any HTML is written. A command-line flag alone cannot activate prices. Observations must match amount, currency, URL, live mode, and be no more than 24 hours old.
- `.github/review/checkout-verification.json`: explicitly unverified; contains no invented checkout URLs or successful observations.
- `assets/site.css`: prepared readable launch-label and regular-price styling.
- `.github/tools/qa-static.py`: checks launch labels, regular-price companions, approved durations, verified checkout amounts, and every marked checkout destination when launch pricing is activated.

No public-facing HTML price or payment button has been changed. Existing $39 / $149 amounts and their original checkout links remain on the unmerged review branch. Payhip changes: added a $19.99 launch plan to the original product, then duplicated the coaching product as unlisted `FrA7a` to avoid its inherited $39 thumbnail and 30-minute checkout title. Renamed the duplicate to the 15–30-minute website launch offer and removed only the duplicate’s inherited thumbnail. The website will use `FrA7a` plan `PjWlK0XkGv`. The original `W6nhP` $39 plan remains unchanged. The duplicate retains its copied $39 plan as well; no plans were deleted. No Stripe product, price, or payment link has been changed. No bank, payout, tax, legal, email, private configuration, secret, or deployment setting has been changed.

## Preparation checks

1. An activation attempt using the old payment links and unverified evidence was rejected before writing any HTML; all HTML checksums stayed unchanged.
2. Static references/disclosures/secrets checks passed on the unchanged review pages.
3. An isolated test copy exercises future activation, all launch/regular labels, duration preservation, idempotence, and price/link mismatch rejection. Test evidence is synthetic and is not copied into the review branch or represented as actual checkout verification.

## Remaining steps

1. Payhip launch amount verified in the seller session: https://payhip.com/order?link=FrA7a&pricing_plan=PjWlK0XkGv showed USD $19.99 base and $19.99 total for United States/Texas (public test ZIP 76033). Check guest checkout separately before publication. UK checkout showed $4.00 tax / $23.99 total; location-dependent taxes remain untouched. No payment was submitted. Reverify the amount if activation occurs more than 24 hours after the recorded observation.
2. Obtain working Stripe payment-tool access or explicit approval for cloud-browser fallback. Inspect the existing Business Checkup product/link and its post-payment return behavior. Prefer a separate $99 one-time launch price/link while preserving the $149 regular destination; maintain the return to `business.html#start-checkup`.
3. Record only actual checkout observations in `checkout-verification.json`, then activate with matching URLs.
4. Re-run static, browser, mobile, form, external-link, and deployment QA and click through the actual website buttons to both correct checkout amounts. Preserve the PHP handler and private mail config.
5. Update the completion report and PR #8. Prepare the final Nextdoor post after readiness; do not publish it.
6. Obtain Ted’s explicit site-publication authorization before merging or deploying.

**PR #8 is not ready to merge:** the $99 Stripe launch checkout is not verified yet. Full activated-site QA and the final Nextdoor post remain pending those dependencies.
