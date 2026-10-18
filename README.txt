Solstead Energy — concept website

public/index.html  main page (everything inline: styles, script, illustrations)
public/404.html    "page not found" page
public/_headers    security headers and noindex for Cloudflare
wrangler.jsonc     Cloudflare Workers settings

Local preview
  python tools/serve.py 5502 and open http://localhost:5502
  (answers like Cloudflare: addresses without .html and the 404 page).
  Fonts load from Google Fonts, so the page needs internet for the right typeface.

Deploy to Cloudflare
  No build step: Cloudflare serves the public folder as is; README, tools and wrangler.jsonc stay private.
  1. Push this folder to an empty GitHub repository.
  2. dash.cloudflare.com → Workers & Pages → Create → Import a repository → that repository.
  3. Project name: solsted-site (must match "name" in wrangler.jsonc).
     Build command: empty. Deploy command: npx wrangler deploy
  4. Deploy. The site appears at solsted-site.<your-account>.workers.dev.
  Own domain: in wrangler.jsonc set "workers_dev": false and add
  "routes": [{ "pattern": "your-domain", "custom_domain": true }].

Brand, products, prices and figures are fictional (design concept).
That's why the site is kept out of search engines (X-Robots-Tag: noindex in public/_headers).
