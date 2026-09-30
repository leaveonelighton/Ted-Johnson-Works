const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '../..');
const review = path.join(root, '.github/review');
fs.mkdirSync(review, { recursive: true });
const server = http.createServer((req, res) => {
  let pathname = decodeURIComponent(req.url.split('?')[0]);
  if (pathname === '/') pathname = '/index.html';
  const file = path.join(root, pathname);
  try {
    const types = { '.css': 'text/css', '.js': 'application/javascript', '.html': 'text/html', '.xml': 'application/xml' };
    res.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
    res.end(fs.readFileSync(file));
  } catch { res.writeHead(404); res.end('Not found'); }
});
const report = { layouts: [], errors: [], checks: [], liveFormSubmitted: false };
const assert = (value, description) => { if (!value) throw Error(description); report.checks.push(description); };
server.listen(8767, '127.0.0.1', async () => {
  let browser;
  try {
    browser = await chromium.launch({ executablePath: process.env.BROWSER_EXECUTABLE_PATH || undefined, headless: true,
      args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
      ...(process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY, bypass: 'localhost,127.0.0.1' } } : {}) });
    const context = await browser.newContext({ ignoreHTTPSErrors: true });
    // QA must never send customer intake or mail to the live service.
    let captured;
    await context.route('**/submit-checkup.php', async route => {
      captured = { url: route.request().url(), method: route.request().method(), body: route.request().postData() };
      await route.fulfill({ status: 200, contentType: 'text/html', body: '<p>QA intercepted submission. Nothing sent.</p>' });
    });
    const page = await context.newPage();
    page.on('pageerror', error => report.errors.push(error.message));
    const files = fs.readdirSync(root).filter(x => x.endsWith('.html')).concat(fs.readdirSync(path.join(root,'articles')).map(x=>'articles/'+x));
    for (const width of [320, 390, 768, 1024, 1440]) {
      await page.setViewportSize({ width, height: 960 });
      for (const file of files) {
        await page.goto('http://127.0.0.1:8767/' + file, { waitUntil: 'domcontentloaded' });
        await page.waitForFunction(() => document.documentElement.classList.contains('nav-ready'));
        const layout = await page.evaluate(() => ({
          viewport: innerWidth, document: document.documentElement.scrollWidth,
          h1Count: document.querySelectorAll('h1').length,
          overflowing: Array.from(document.querySelectorAll('main h1,main h2,main h3,main p,main a,main input,main select,main textarea')).filter(el => {
            if (!el.getClientRects().length || el.closest('[aria-hidden="true"]')) return false;
            const r = el.getBoundingClientRect();
            if (el.closest('.album-track') && (r.left >= innerWidth || r.right <= 0)) return false;
            return r.width > innerWidth + 1 || r.right > innerWidth + 1 || r.left < -1;
          }).slice(0,6).map(el => el.tagName + ':' + el.textContent.slice(0,60))
        }));
        report.layouts.push({ file, width, ...layout });
        assert(layout.document <= width + 1 && layout.overflowing.length === 0, `No overflow: ${file} at ${width}px`);
        assert(layout.h1Count === 1, `One main heading: ${file} at ${width}px`);
      }
    }
    // Click every local checkout CTA, intercepting navigation before any live request.
    const offers = JSON.parse(fs.readFileSync(path.join(root,'.github/tools/offers.json'))).planned;
    const evidence = JSON.parse(fs.readFileSync(path.join(review,'checkout-verification.json')));
    if (fs.readFileSync(path.join(root,'index.html'),'utf8').includes('data-field="label"')) {
      for (const file of ['index.html','business.html','quick-tech-help.html']) {
        await page.goto('http://127.0.0.1:8767/'+file, {waitUntil:'domcontentloaded'});
        const amounts = page.locator('[data-field="price"]');
        for (let i=0; i<await amounts.count(); i++) {
          const amount = amounts.nth(i);
          const name = await amount.getAttribute('data-offer');
          assert(await amount.isVisible() && await amount.innerText() === offers[name].price, `Visible launch amount ${file}/${name}`);
          assert(await page.locator(`[data-offer="${name}"][data-field="regular_price"]`).first().isVisible(), `Visible regular price ${file}/${name}`);
        }
        const count = await page.locator('[data-field="checkout"]').count();
        for (let i=0; i<count; i++) {
          await page.goto('http://127.0.0.1:8767/'+file, {waitUntil:'domcontentloaded'});
          const button = page.locator('[data-field="checkout"]').nth(i);
          const name = await button.getAttribute('data-offer');
          const expected = evidence[name].url;
          let clickedUrl;
          await page.route(expected, async route => {
            clickedUrl = route.request().url();
            await route.fulfill({status:200,contentType:'text/html',body:'<p>Checkout navigation intercepted for QA.</p>'});
          });
          await button.click();
          await page.waitForURL(expected);
          assert(clickedUrl === expected, `Checkout CTA ${file}/${i} opens verified ${name} URL`);
          await page.unroute(expected);
        }
      }
    }
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('http://127.0.0.1:8767/index.html', { waitUntil: 'domcontentloaded' });
    await page.screenshot({ path: path.join(review,'home-mobile.png'), fullPage: true });
    await page.getByRole('button', { name: 'Menu', exact: true }).click();
    assert(await page.locator('.nav-toggle').getAttribute('aria-expanded') === 'true', 'Mobile Menu opens');
    await page.locator('.more-works summary').click();
    assert(await page.getByRole('link',{name:'Food Works',exact:true}).isVisible(), 'More Works reveals all section links');
    await page.screenshot({ path: path.join(review, 'mobile-menu.png') });
    await page.keyboard.press('Escape');
    assert(!(await page.locator('.more-works').evaluate(el => el.open)), 'Escape closes More Works');
    await page.keyboard.press('Escape');
    assert(await page.locator('.nav-toggle').getAttribute('aria-expanded') === 'false', 'Escape closes mobile menu');
    await page.setViewportSize({ width: 1440, height: 1000 });
    for (const file of ['index.html','contract-it.html','business.html','body-works.html']) {
      await page.goto('http://127.0.0.1:8767/'+file, { waitUntil: 'domcontentloaded' });
      await page.screenshot({ path: path.join(review, file.replace('.html','')+'-desktop.png'), fullPage: true });
    }
    // Existing intake: required email, timing field, field names, confirmation states.
    await page.goto('http://127.0.0.1:8767/business.html?submitted=success#start-checkup', { waitUntil: 'domcontentloaded' });
    assert(await page.locator('#checkup-success').isVisible(), 'Success confirmation visible');
    assert(!(await page.locator('.checkup-form').isVisible()), 'Success hides intake form');
    await page.goto('http://127.0.0.1:8767/business.html?submitted=error#start-checkup', { waitUntil: 'domcontentloaded' });
    assert(await page.locator('#checkup-error').isVisible(), 'Error confirmation visible');
    assert(await page.locator('.checkup-form').isVisible(), 'Error keeps retry form available');
    await page.goto('http://127.0.0.1:8767/business.html#start-checkup', { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => document.querySelector('#form-started-at').value !== '');
    assert(await page.locator('#email').evaluate(el => !el.checkValidity()), 'Missing email blocks form submission');
    await page.locator('#email').fill('bad-email');
    assert(await page.locator('#email').evaluate(el => !el.checkValidity()), 'Invalid email blocks form submission');
    await page.locator('#email').fill('qa@example.com');
    await page.locator('#business-name').fill('QA — intercepted locally');
    await page.locator('#harder-than-it-should-be').fill('Checking the preserved form without sending email.');
    await page.getByRole('button',{name:'Send My Checkup Information'}).click();
    await page.waitForURL('**/submit-checkup.php');
    assert(captured.method === 'POST', 'Form preserves POST method');
    assert(captured.url === 'https://tedjohnsonworks.com/submit-checkup.php', 'Form preserves live handler destination (request intercepted)');
    const fields = new URLSearchParams(captured.body);
    assert(['business_name','your_name','challenge','email','phone','best_contact','website','city_state','company_fax','form_started_at'].every(k=>fields.has(k)), 'All 8 intake fields and 2 anti-spam fields retained');
    assert(Number(fields.get('form_started_at')) > 0, 'Timing anti-spam field populated');
    // Every triage decision path remains operational.
    await page.goto('http://127.0.0.1:8767/triage.html', { waitUntil: 'domcontentloaded' });
    for (const category of ['internet','account','customer','software','unsure']) {
      for (const contextValue of ['personal','business']) {
        for (const urgency of ['blocked','recurring','planning']) {
          await page.locator(`[name=category][value=${category}]`).check();
          await page.locator(`[name=context][value=${contextValue}]`).check();
          await page.locator(`[name=urgency][value=${urgency}]`).check();
          await page.getByRole('button',{name:'Show My Next Step'}).click();
          const href = await page.locator('#primary-action').getAttribute('href');
          const expected = contextValue === 'business' && urgency !== 'planning' ? 'business.html#checkup' : 'quick-tech-help.html#clarity-call';
          assert(href === expected, `Triage route ${category}/${contextValue}/${urgency}`);
          assert(await page.locator('#triage-result').isVisible(), `Triage result ${category}/${contextValue}/${urgency}`);
          await page.getByRole('button',{name:'Start over',exact:true}).click();
          assert(!(await page.locator('#triage-result').isVisible()), 'Triage reset hides result');
        }
      }
    }
    await page.goto('http://127.0.0.1:8767/photography.html', { waitUntil: 'domcontentloaded' });
    const next = page.getByRole('button',{name:/Next/});
    if (await next.count()) {
      await next.click();
      await page.waitForFunction(() => document.querySelector('[data-album-current]').textContent === '2');
      assert((await page.locator('body').innerText()).includes('2 / 5'), 'Photography archive next slide works');
    }
    const noJs = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 844 },ignoreHTTPSErrors:true });
    const noJsPage = await noJs.newPage();
    await noJsPage.goto('http://127.0.0.1:8767/index.html', {waitUntil:'domcontentloaded'});
    assert(await noJsPage.getByRole('link',{name:'Contract IT',exact:true}).first().isVisible(), 'Navigation remains available without JavaScript');
    assert(report.errors.length === 0, 'No browser JavaScript errors');
  } catch (error) { report.failure = error.stack; process.exitCode = 1; }
  finally {
    fs.writeFileSync(path.join(review,'browser-qa.json'), JSON.stringify(report, null, 2));
    console.log(JSON.stringify({layoutChecks:report.layouts.length, passed:report.checks.length, errors:report.errors, failure:report.failure}));
    await browser?.close(); server.close();
  }
});
