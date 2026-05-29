Morning Cup AI — Project Handoff

I'm building a static HTML website called Morning Cup AI at morningcupai.com, hosted on GitHub Pages from the repo https://github.com/morningcupai/morningcupai. The local project lives at ~/morning-cup-ai/.

Tech stack: Plain HTML, one shared style.css, one shared nav.js (vanilla JS). Google Fonts: Lora (headings) + Inter (body). No frameworks, no build tools.

Brand:
- Navy: #2A3F55 — headings, nav background, buttons, pills
- Cream: #FDF6EC — hero and card backgrounds
- Slate: #6B7B8A — subtext
- Base font size: 18px (audience is adults 55+)

Current file structure at repo root:
  index.html              ← redirects to /home
  home/index.html         ← real home page (URL: morningcupai.com/home)
  archive.html            ← post listing (was blog.html)
  subscribe.html
  voice-cloning-scam.html ← first published post
  style.css
  nav.js                  ← sticky nav with scroll shadow at 50px
  CNAME                   ← morningcupai.com
  Images/
    voice-cloning-scam.jpg

Pages:
- Home (/home) — hero with 80px cup icon, Beehiiv embed signup form, wave divider, horizontally scrolling featured posts section
- Archive (/archive.html) — post grid with thumbnail cards (thumbnail, date, pillar pill, title, excerpt, read more)
- Subscribe (/subscribe.html) — Beehiiv embed form (form ID: 33f11184-4187-438a-ae10-380ac4d7e57f)
- Post pages — full-width hero image (400px), back to archive link, pillar pill, body text, navy AI prompt callout, amber scam watch callout, cream closing block

Nav links (all pages): Home → /home · Archive → /archive.html · Subscribe → /subscribe.html

Post card structure: `<img class="blog-card-thumb">` + `<div class="blog-card-body">` containing date, pillar pill, h2, excerpt, read-more link. Cards use .blog-card + .featured-card on home page.

Published posts:
1. Your grandson called. He needed money. But it wasn't him. — voice-cloning-scam.html — January 7, 2026 — Scam Protection

Key CSS classes to know: .blog-card, .blog-card-thumb, .blog-card-body, .blog-card-pillar, .blog-card-date, .post-hero-img, .callout-prompt (navy), .callout-scam (amber #FEF3C7), .post-closing (cream), .featured-card, .featured-scroll

Post template pattern: When adding a new post, update three places: (1) create the post HTML page, (2) add a card to archive.html, (3) add a card to home/index.html featured scroll section.

Image convention: Post images go in Images/ (capital I) at repo root. Reference as src="/Images/filename.jpg" using absolute paths from all pages — do not use relative paths like ../Images/.
