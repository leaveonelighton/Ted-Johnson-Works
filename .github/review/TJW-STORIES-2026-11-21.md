# Ted’s Stories and RSS — owner review

**Status: DRAFT ONLY. No merge, deployment, social posting, email, or Metricool connection change.**

## Existing site and baseline

Inspected November 21, 2026 (America/Chicago). Baseline main: `3dcae4506186675c081c020884782de13ed41626`, including merged Metricool tracker PR #39. The `hostinger` production branch records deployment of that main commit. Live homepage, Stories, series page, ten local articles, sitemap, robots, navigation and tracker files matched main byte for byte in HTTP GET checks. All ten article URLs returned 200 with their existing apex canonical URLs. Production `/feed.xml` returned 404, as expected before this draft release.

The repository is the finished static HTML site; no WordPress, database, CMS, framework migration, site registration, or hosting change was added. Existing open draft PRs #11, #31 and #32 were inspected and left untouched. None overlap the changed runtime files here.

The hub already linked five `/articles/` articles, the series, the retirement story, an Amazon jobs resource, and Ted’s external LinkedIn story. Four published Learn’n as We Go episodes were reachable through the series but absent from the hub’s article list. The retirement story was absent from the sitemap. The jobs resource and retirement story used similar “Cheese Moved” wording but are different pages, not duplicate articles.

## Proposed improvements

- Keep **Ted’s Stories** as the public name and retain the established navy, gold and Lexend design.
- List every local article once, with its existing description, original URL and content-checked topic. Eight Tech Works articles, one Food Works article and one personal/career article.
- Preserve the series, LinkedIn story card, photo/archive and book blocks, and the existing clearly separate Leave One Light On link. No content is imported from or written to Leave One Light On.
- Add topic jump links, visible RSS links, readable cards, and links to existing practical help. Photo Works and Body Works point to existing content; no new articles or empty article categories are invented.
- Add static `/feed.xml`, ten unique canonical GUIDs, RSS 2.0 channel fields and Atom self-discovery. Add HTML feed discovery to homepage, hub, series and ten articles.
- Add only the missing retirement-story sitemap entry, retaining every old sitemap URL. No URLs, redirects, canonicals, historical SEO metadata or existing structured data changed.

## Feed inventory and publication evidence

All descriptions are copied from existing article meta descriptions, after reading the article contents. Feed titles use existing page titles without the site suffix; the retirement item uses its existing visible H1. No author/email field is fabricated. The external LinkedIn article, series landing page, Amazon referral resource, albums, products and nonprofit content are not feed items.

| Original article URL and title | Topic | Verified publication date |
| --- | --- | --- |
| [Who Moved My Cheese? What Every Generation Should Know About Retirement](https://tedjohnsonworks.com/cheese-moved-so-did-ted.html) | Ted's Stories | 2026-11-21 |
| [Moving at the FREEZE of Business](https://tedjohnsonworks.com/articles/moving-at-the-freeze-of-business.html) | Tech Works | Not verified; omitted |
| [Is Your Face the New Password?](https://tedjohnsonworks.com/articles/is-your-face-the-new-password.html) | Tech Works | Not verified; omitted |
| [How Many Passwords Does One Human Need?](https://tedjohnsonworks.com/articles/how-many-passwords-does-one-human-need.html) | Tech Works | Not verified; omitted |
| [Life Savings Gone. Here's Your Identity Monitoring Subscription.](https://tedjohnsonworks.com/articles/life-savings-gone-identity-monitoring-subscription.html) | Tech Works | Not verified; omitted |
| [AI for People Who Don’t Want to Become AI Experts](https://tedjohnsonworks.com/articles/ai-for-people-who-dont-want-to-become-ai-experts.html) | Tech Works | Not verified; omitted |
| [How I Built TedJohnsonWorks.com Without Hiring an Agency](https://tedjohnsonworks.com/articles/how-i-built-ted-johnson-works.html) | Tech Works | Not verified; omitted |
| [How I Keep TedJohnsonWorks.com Running Without Babysitting It](https://tedjohnsonworks.com/articles/how-i-keep-tedjohnsonworks-running.html) | Tech Works | Not verified; omitted |
| [How I Use Payhip to Sell Practical Guides](https://tedjohnsonworks.com/articles/how-i-use-payhip-to-sell-practical-guides.html) | Tech Works | Not verified; omitted |
| [Working Under Chef Al Hynes at the Belleview-Biltmore](https://tedjohnsonworks.com/articles/working-under-chef-al-hynes-at-the-belleview-biltmore.html) | Food Works | Not verified; omitted |

The retirement byline explicitly says November 21, 2026, consistent with publication PR #37. The hub displays that date. No exact first-live time is verified. RSS `pubDate` is optional but requires a time and timezone, so this version omits it for all items rather than inventing times. The inventory records the verified day and its source. Dates in article research citations, footer copyright, Git author history, or recollected events are not treated as publication dates. Metricool’s handling of undated entries remains a live acceptance test; do not claim integration works yet.

## Changed files

| File(s) | Change |
| --- | --- |
| `stories.html` | Improve hub listings and topic navigation; preserve existing header/footer and retained content blocks; add RSS discovery. |
| `assets/stories.css` | Hub-only layout and readable link/card styles; no shared CSS edits. |
| `feed.xml` | New static ten-item RSS 2.0 feed. |
| `sitemap.xml` | One additive retirement-story URL. |
| `index.html`, `learnn-as-we-go.html`, `cheese-moved-so-did-ted.html` | One head-only RSS discovery link each. Bodies are byte-identical. |
| `articles/ai-for-people-who-dont-want-to-become-ai-experts.html` | Head-only RSS discovery. |
| `articles/how-i-built-ted-johnson-works.html` | Head-only RSS discovery. |
| `articles/how-i-keep-tedjohnsonworks-running.html` | Head-only RSS discovery. |
| `articles/how-i-use-payhip-to-sell-practical-guides.html` | Head-only RSS discovery. |
| `articles/how-many-passwords-does-one-human-need.html` | Head-only RSS discovery. |
| `articles/is-your-face-the-new-password.html` | Head-only RSS discovery. |
| `articles/life-savings-gone-identity-monitoring-subscription.html` | Head-only RSS discovery. |
| `articles/moving-at-the-freeze-of-business.html` | Head-only RSS discovery. |
| `articles/working-under-chef-al-hynes-at-the-belleview-biltmore.html` | Head-only RSS discovery. |
| `.github/tools/stories.json` | Reviewed article inventory, category and date evidence. |
| `.github/tools/stories-feed.py` | Standard-library feed generator/checker; no website build/runtime dependency. |
| `.github/tools/qa-stories.py` | Preservation, RSS, SEO and link verification. |
| `.github/review/TJW-STORIES-2026-11-21.md` | This owner report, maintenance and rollback instructions. |
| `.github/review/tjw-stories-verification-20261121.json` | Recorded source, browser and read-only production evidence. |

The `.github/` tools and reports are already excluded from the existing deployment workflow. Preview configuration and responsive test harness exist only in scratch, outside the checkout; they are excluded from this PR. No deployment workflow changes.

## Verification performed

| Check | Result and scope |
| --- | --- |
| Scoped automated source suite | **PASS:** 683 assertions; 352 local references; 64 other tracked files preserved; 17 existing structured-data blocks parsed; ten article bodies byte-identical. |
| RSS XML and RSS 2.0 fields | **PASS:** ElementTree parsing, required channel fields, nonempty item fields, unique links/GUIDs, absolute canonical URLs and inventory parity. |
| Independent RSS reader | **PASS:** `feedparser` reports `rss20`, ten entries, `bozo=False`. |
| Internal article links | **PASS:** all local references/fragments in changed HTML resolve; no new broken internal references. All ten existing public article URLs return 200. |
| SEO source audit | **PASS:** all 30 HTML pages have one canonical each, no duplicate canonical destinations or noindex meta rules, existing JSON-LD parses. All feed articles covered by sitemap after the additive correction. Production inspected article/header responses contain no X-Robots-Tag restrictions. |
| Genuine browser desktop review | **PASS:** Cloud Chrome static preview; usable width and scroll width both 1348px. Homepage→Stories, series→hub, desktop More Works keyboard Enter/Escape, RSS link→browser XML tree. |
| Genuine browser 340/375/768 review | **PASS for hub:** three test-only same-origin iframes at explicit CSS widths. Usable document widths/scroll widths 325/325, 360/360, 753/753 (15px scrollbars). All ten listings present; menu open/close and More Works keyboard Enter/Escape worked at each width. Screenshots inspected for narrow hero/listings and tablet layout. |
| Topic and article navigation | **PASS:** 340px Tech Works anchor scroll observed in screenshot; Food Works article opened and returned to hub. |
| Images and alt text | **PASS within changed pages:** hub/series/articles contain no images to alter; all four preserved homepage book covers loaded with natural width 130px and nonempty meaningful alt text after expanding the existing shelf. |
| Business functions | **SOURCE PRESERVATION PASS:** header/footer/form markup, offers, checkout URLs, affiliate links, customer handlers, photographs and product files preserved. No live payment, purchase, email or customer form submitted. |
| Visitor tracking | **PRESERVATION PASS:** no additional script or tracking added; PR #39 tracker and shared navigation JS byte-identical. Existing subdirectory issue below remains. |
| Original `.github/tools/qa-static.py` | **FAIL, pre-existing:** identical 26 errors before/after, caused by old promotional-price/checkout fixtures. No new missing-link/reference errors. Prices and payment code intentionally untouched. |
| Whitespace/diff review | `git diff --check` passed; runtime diff restricted to listed files, additive feed metadata and approved hub work. |

These browser checks use real rendered iframe viewports, not source-only responsive claims. They are not physical-device testing, full screen-reader certification, or live production verification of the proposed release. The user’s connected Chrome could not reach the isolated local preview; browser QA continued in Cloud Chrome through the supported local preview.

## Existing findings and remaining limits

1. **Tracker subdirectory path:** existing `assets/nav.js` injects relative `assets/metricool-tracker.js`. On `/articles/...` that resolves to `/articles/assets/metricool-tracker.js`, which returned HTTP 404. Root-page tracker file exists and is unchanged. Reported only; fixing it requires separate scoped owner approval because this assignment explicitly preserves tracker configuration.
2. **Sitemap outside article scope:** `12-things-youll-actually-use.html`, `amazon-opportunities.html` and `privacy.html` still lack sitemap entries. No entries were removed. These can be reviewed in a separate sitemap task.
3. No `og:image` is configured on the ten feed articles, and those article bodies have no images. Existing metadata is protected. RSS reading can work without images, but future social preview imagery requires a separately approved decision and must not be assumed.
4. Existing technical articles mention a historical Astro/source build workflow, while today’s authoritative checkout consists of finished static files. Historical story text was preserved.
5. External LinkedIn availability, all historical source links, external affiliate destinations, live forms, checkout transactions and Search Console were not comprehensively retested. Source preservation does not claim those external services passed live functional tests.
6. The draft feed is not published. Its production HTTP status, XML content type, crawler access, W3C online validation and Metricool acceptance remain unverified. Local parser checks do not prove Metricool compatibility, especially for undated entries.

## Adding future approved articles without rebuilding

1. Add the approved static article at its chosen original URL, with matching canonical and accurate title/description. Verify the public-release date only from reliable publication evidence; leave unknown dates empty.
2. Add one card to the appropriate topic in `stories.html` and one record to `.github/tools/stories.json`. Do not create duplicate entries or classify solely from the title.
3. Add RSS discovery to the new article’s head and its canonical URL to `sitemap.xml`.
4. Run `python .github/tools/stories-feed.py` and `python .github/tools/stories-feed.py --check`. This writes static XML only; it does not build, publish or deploy the site. Python’s standard library is sufficient for generation.
5. Run scoped verification with BeautifulSoup and feedparser available: `python .github/tools/qa-stories.py`. That suite intentionally enforces preservation against this assignment’s baseline; a future owner-authorized article-body change needs a freshly reviewed baseline/allowlist. Review the diff, preview, and obtain release approval normally.
6. Commit the reviewed HTML and `feed.xml` together. Do not change an existing item GUID when editing its description. Exact publication timestamps, if later verified, can be introduced in a separately reviewed generator update; do not derive them from file mtimes.

## Approval and rollback

**No release is authorized now.** Owner must separately and explicitly approve merging this draft PR to `main` and the resulting production deployment. The existing workflow deploys automatically from main, so merge approval must acknowledge both effects. After release, recheck live articles, canonical/discovery tags, sitemap and `/feed.xml` status/content type, then test standard RSS-reader access.

**Separate Metricool gate:** after the approved feed is live, obtain explicit permission to test/connect `https://tedjohnsonworks.com/feed.xml` to the existing **Ted Johnson Works** brand only if connection changes are needed. Preserve the tracker. Check actual accepted items and dates in Metricool; report failure if not accepted. Do not create an Autolist, change schedules, publish posts or enable automatic sharing. Every future social post still requires owner approval.

**Rollback:** before merge, close the draft PR; production is unchanged. After a separately authorized release, revert the single merge/squash commit on `main` through an approved rollback PR and let the existing Hostinger workflow redeploy. That restores the prior hub and discovery/sitemap state and removes the new feed/styles. Do not change products, tracking, forms or hosting settings. Already-consumed RSS items may remain cached by readers.

Provider references consulted: [RSS 2.0 specification](https://www.rssboard.org/rss-specification), [Metricool RSS guide](https://help.metricool.com/what-is-an-rss-feed-and-how-does-it-work-in-metricool-1tupq), and [Metricool website/blog connection guide](https://help.metricool.com/how-to-connect-your-website-or-blog-to-metricool-ejuy1). Metricool read-only brand settings confirmed Ted Johnson Works brand 8254715 with website connected; no blog-feed acceptance was asserted.
