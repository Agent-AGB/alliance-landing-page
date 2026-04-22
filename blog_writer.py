import anthropic
import os
import requests
import json
import re
import base64
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
SANITY_TOKEN = os.getenv("SANITY_TOKEN")
SANITY_PROJECT_ID = os.getenv("SANITY_PROJECT_ID")
SANITY_DATASET = os.getenv("SANITY_DATASET")
SANITY_AUTHOR_ID = os.getenv("SANITY_AUTHOR_ID")

SEO_TOPICS = [
    {
        "title": "How Much Does a Roof Replacement Cost in Massachusetts in 2026",
        "keyword": "roof replacement cost Massachusetts",
        "service": "roofing",
        "slug": "roof-replacement-cost-massachusetts-2026"
    },
    {
        "title": "Do I Need a Permit for a Deck in Massachusetts",
        "keyword": "deck permit Massachusetts",
        "service": "decks",
        "slug": "deck-permit-massachusetts-guide"
    },
    {
        "title": "Home Addition Cost Guide for Massachusetts Homeowners",
        "keyword": "home addition cost Massachusetts",
        "service": "additions",
        "slug": "home-addition-cost-massachusetts"
    },
    {
        "title": "Vinyl vs Fiber Cement Siding in New England Weather",
        "keyword": "best siding New England",
        "service": "siding",
        "slug": "vinyl-vs-fiber-cement-siding-new-england"
    },
    {
        "title": "How Long Does a Kitchen Remodel Take in Massachusetts",
        "keyword": "kitchen remodel timeline Massachusetts",
        "service": "remodeling",
        "slug": "kitchen-remodel-timeline-massachusetts"
    },
    {
        "title": "What Is an Unrestricted CSL License in Massachusetts",
        "keyword": "unrestricted CSL license Massachusetts contractor",
        "service": "licensing",
        "slug": "unrestricted-csl-license-massachusetts"
    },
    {
        "title": "MassSave Rebates for Home Renovations in 2026",
        "keyword": "MassSave rebates home renovation 2026",
        "service": "energy",
        "slug": "masssave-rebates-home-renovation-2026"
    },
    {
        "title": "How to Choose a Licensed Contractor in Massachusetts",
        "keyword": "licensed contractor Massachusetts how to choose",
        "service": "licensing",
        "slug": "how-to-choose-licensed-contractor-massachusetts"
    },
    {
        "title": "Roof Replacement in Brockton MA - What Homeowners Need to Know",
        "keyword": "roof replacement Brockton MA",
        "service": "roofing",
        "slug": "roof-replacement-brockton-ma"
    },
    {
        "title": "Home Addition Contractor Cape Cod - Complete Guide",
        "keyword": "home addition contractor Cape Cod",
        "service": "additions",
        "slug": "home-addition-contractor-cape-cod"
    },
    {
        "title": "Window Replacement Cost Guide Massachusetts 2026",
        "keyword": "window replacement cost Massachusetts",
        "service": "windows",
        "slug": "window-replacement-cost-massachusetts-2026"
    },
    {
        "title": "Bathroom Remodel Cost Massachusetts - Full Breakdown",
        "keyword": "bathroom remodel cost Massachusetts",
        "service": "remodeling",
        "slug": "bathroom-remodel-cost-massachusetts"
    },
    {
        "title": "Structural Repairs Massachusetts - Signs Your Home Needs Help",
        "keyword": "structural repairs Massachusetts",
        "service": "structural",
        "slug": "structural-repairs-massachusetts-warning-signs"
    },
    {
        "title": "Deck Builder Massachusetts - What to Expect",
        "keyword": "deck builder Massachusetts",
        "service": "decks",
        "slug": "deck-builder-massachusetts-guide"
    },
    {
        "title": "MBE Certified Contractor Massachusetts - What It Means for You",
        "keyword": "MBE certified contractor Massachusetts",
        "service": "licensing",
        "slug": "mbe-certified-contractor-massachusetts"
    },
]

def get_next_topic():
    log_file = "blog_log.json"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            published = json.load(f)
    else:
        published = []
    for topic in SEO_TOPICS:
        if topic["slug"] not in published:
            return topic
    print("All topics published! Add more topics to SEO_TOPICS list!")
    return None

def mark_published(slug):
    log_file = "blog_log.json"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            published = json.load(f)
    else:
        published = []
    if slug not in published:
        published.append(slug)
    with open(log_file, "w") as f:
        json.dump(published, f)

def write_blog_post(topic):
    print("Claude is writing blog post about: " + topic["title"])
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are an expert SEO content writer for Alliance Group Builders LLC. "
                    "A licensed construction company in Eastern Massachusetts. "
                    "Write a complete SEO optimized blog post about: " + topic["title"] + ". "
                    "Target keyword: " + topic["keyword"] + ". "
                    "Company details to naturally include: "
                    "Alliance Group Builders LLC. "
                    "Licensed and Insured in Massachusetts. "
                    "Unrestricted CSL License CS-119447. "
                    "HIC License 211374. "
                    "OSHA 30 Certified. "
                    "MBE Certified through State of Massachusetts and City of Boston. "
                    "24 plus years of field experience. "
                    "Phone: 877-502-2225. "
                    "Serving Eastern Massachusetts, Cape Cod and The Islands. "
                    "Free consultation and fixed price estimates. "
                    "The blog post must include: "
                    "1. SEO optimized H1 title using the target keyword naturally. "
                    "2. Introduction paragraph that hooks the reader immediately. "
                    "3. At least 5 H2 sections covering the topic thoroughly. "
                    "4. Real specific information about Massachusetts costs "
                    "permits codes and local market knowledge. "
                    "5. At least one mention of specific Massachusetts towns. "
                    "6. FAQ section at the end with 3 to 5 common questions. "
                    "7. Strong call to action at the end mentioning Alliance Group Builders. "
                    "8. Word count between 1000 and 1500 words. "
                    "9. Natural keyword usage throughout not stuffed. "
                    "10. People first content that genuinely helps homeowners. "
                    "Write in HTML format with proper tags. "
                    "Use h1 h2 h3 p ul li strong tags. "
                    "Do NOT include html head body or doctype tags. "
                    "Just the article content HTML. "
                    "Plain text only in the content no special characters."
                )
            }
        ]
    )
    return message.content[0].text.strip()

def create_html_page(topic, content):
    date = datetime.now().strftime("%B %d %Y")
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>""" + topic["title"] + """ | Alliance Group Builders LLC</title>
<meta name="description" content="Expert guide for Massachusetts homeowners. Alliance Group Builders LLC - Licensed, Insured, OSHA 30 Certified, MBE Certified contractor serving Eastern MA.">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: Inter, sans-serif; background:#ffffff; color:#0D0D0D; }
nav { background:#0D0D0D; padding:0 40px; display:flex; justify-content:space-between; align-items:center; height:72px; position:sticky; top:0; z-index:999; }
.logo { color:white; font-size:1.1rem; font-weight:800; text-decoration:none; }
.logo span { color:#C9A84C; }
.nav-cta { background:#C9A84C; color:#0D0D0D; padding:10px 22px; font-size:0.85rem; font-weight:700; text-decoration:none; }
.hero { background:#0D0D0D; padding:60px 40px; }
.hero-inner { max-width:800px; margin:0 auto; }
.hero-tag { color:#C9A84C; font-size:0.75rem; font-weight:700; letter-spacing:3px; text-transform:uppercase; margin-bottom:16px; }
.hero h1 { font-size:2.2rem; font-weight:800; color:#ffffff; letter-spacing:-0.5px; line-height:1.2; margin-bottom:16px; }
.hero-meta { color:rgba(255,255,255,0.4); font-size:0.82rem; }
.article { max-width:800px; margin:0 auto; padding:60px 40px; }
.article h2 { font-size:1.5rem; font-weight:800; color:#0D0D0D; margin:40px 0 16px; }
.article h3 { font-size:1.1rem; font-weight:700; color:#0D0D0D; margin:24px 0 12px; }
.article p { font-size:1rem; line-height:1.8; color:#333; margin-bottom:16px; }
.article ul { margin:16px 0 16px 24px; }
.article li { font-size:1rem; line-height:1.8; color:#333; margin-bottom:8px; }
.article strong { color:#0D0D0D; font-weight:700; }
.cta-box { background:#0D0D0D; padding:48px; margin:48px 0; text-align:center; }
.cta-box h3 { color:#C9A84C; font-size:1.4rem; font-weight:800; margin-bottom:12px; }
.cta-box p { color:rgba(255,255,255,0.7); margin-bottom:24px; font-size:0.95rem; }
.cta-box a { background:#C9A84C; color:#0D0D0D; padding:14px 32px; font-weight:700; text-decoration:none; font-size:0.9rem; letter-spacing:1px; text-transform:uppercase; display:inline-block; }
.trust-bar { background:#f8f8f6; padding:24px 40px; border-top:2px solid #C9A84C; }
.trust-inner { max-width:800px; margin:0 auto; display:flex; gap:24px; flex-wrap:wrap; }
.trust-item { font-size:0.78rem; font-weight:700; color:#0D0D0D; letter-spacing:0.5px; text-transform:uppercase; }
footer { background:#0a0a0a; padding:32px 40px; text-align:center; color:rgba(255,255,255,0.3); font-size:0.78rem; }
@media(max-width:768px) {
  nav { padding:0 16px; }
  .hero { padding:40px 16px; }
  .hero h1 { font-size:1.6rem; }
  .article { padding:40px 16px; }
  .trust-bar { padding:16px; }
}
</style>
</head>
<body>
<nav>
  <a href="../index.html" class="logo">Alliance <span>Group Builders</span></a>
  <a href="../index.html#estimate-form" class="nav-cta">Free Estimate</a>
</nav>
<div class="hero">
  <div class="hero-inner">
    <div class="hero-tag">Massachusetts Construction Guide</div>
    <h1>""" + topic["title"] + """</h1>
    <div class="hero-meta">Published """ + date + """ by Alliance Group Builders LLC</div>
  </div>
</div>
<div class="trust-bar">
  <div class="trust-inner">
    <span class="trust-item">Licensed and Insured</span>
    <span class="trust-item">CSL CS-119447</span>
    <span class="trust-item">HIC 211374</span>
    <span class="trust-item">OSHA 30 Certified</span>
    <span class="trust-item">MBE Certified</span>
    <span class="trust-item">24+ Years Experience</span>
  </div>
</div>
<div class="article">
""" + content + """
<div class="cta-box">
  <h3>Ready to Get Started?</h3>
  <p>Alliance Group Builders LLC serves Eastern Massachusetts, Cape Cod and The Islands. Licensed, insured and ready to help with your project.</p>
  <a href="../index.html#estimate-form">Get Your Free Estimate</a>
</div>
</div>
<footer>
  Alliance Group Builders LLC - Licensed and Insured in Massachusetts - CSL CS-119447 - HIC 211374 - OSHA 30 Certified - MBE Certified - (877) 502-2225
</footer>
</body>
</html>"""
    return html

def get_file_sha(filename):
    url = "https://api.github.com/repos/" + GITHUB_REPO + "/contents/blog/" + filename
    headers = {
        "Authorization": "token " + GITHUB_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    if "sha" in result:
        return result["sha"]
    return None

def save_to_github(filename, content, topic):
    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("No GitHub token found - saving locally only!")
        os.makedirs("blog", exist_ok=True)
        with open("blog/" + filename, "w", encoding="utf-8") as f:
            f.write(content)
        print("Saved locally to blog/" + filename)
        return True
    url = "https://api.github.com/repos/" + GITHUB_REPO + "/contents/blog/" + filename
    headers = {
        "Authorization": "token " + GITHUB_TOKEN,
        "Content-Type": "application/json"
    }
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    payload = {
        "message": "Add blog post: " + topic["title"],
        "content": encoded
    }
    sha = get_file_sha(filename)
    if sha:
        print("File exists - updating...")
        payload["sha"] = sha
    response = requests.put(url, headers=headers, json=payload)
    result = response.json()
    if "content" in result:
        print("Published to GitHub successfully!")
        print("URL: " + result["content"]["html_url"])
        os.makedirs("blog", exist_ok=True)
        with open("blog/" + filename, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    else:
        print("GitHub error: " + str(result))
        os.makedirs("blog", exist_ok=True)
        with open("blog/" + filename, "w", encoding="utf-8") as f:
            f.write(content)
        return False

def save_to_sanity(topic, content):
    print("Publishing to Sanity CMS for alliance-grp.net...")
    if not SANITY_TOKEN or not SANITY_PROJECT_ID:
        print("No Sanity credentials - skipping!")
        return False
    url = "https://" + SANITY_PROJECT_ID + ".api.sanity.io/v2021-10-21/data/mutate/" + SANITY_DATASET
    headers = {
        "Authorization": "Bearer " + SANITY_TOKEN,
        "Content-Type": "application/json"
    }
    blocks = []
    paragraphs = content.replace("<h2>", "\n<h2>").replace("<p>", "\n<p>").split("\n")
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        clean = re.sub("<[^>]+>", "", para).strip()
        if not clean:
            continue
        if "<h2>" in para or "<h3>" in para:
            style = "h2"
        else:
            style = "normal"
        blocks.append({
            "_type": "block",
            "_key": os.urandom(8).hex(),
            "style": style,
            "children": [{
                "_type": "span",
                "_key": os.urandom(8).hex(),
                "text": clean
            }]
        })
    payload = {
        "mutations": [{
            "createOrReplace": {
                "_type": "post",
                "_id": "blog-" + topic["slug"],
                "title": topic["title"],
                "slug": {
                    "_type": "slug",
                    "current": topic["slug"]
                },
                "author": {
                    "_type": "reference",
                    "_ref": SANITY_AUTHOR_ID
                },
                "publishedAt": datetime.now().isoformat(),
                "body": blocks
            }
        }]
    }
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    if "transactionId" in result:
        print("Published to Sanity successfully!")
        print("Post will appear on alliance-grp.net!")
        return True
    else:
        print("Sanity error: " + str(result))
        return False

def run_blog_writer():
    print("=" * 50)
    print("AGB SEO BLOG WRITER")
    print("=" * 50)
    topic = get_next_topic()
    if not topic:
        return
    print("Writing post: " + topic["title"])
    print("Target keyword: " + topic["keyword"])
    print()
    content = write_blog_post(topic)
    html = create_html_page(topic, content)
    filename = topic["slug"] + ".html"
    github_success = save_to_github(filename, html, topic)
    sanity_success = save_to_sanity(topic, content)
    if github_success or sanity_success:
        mark_published(topic["slug"])
        print("\nBlog post complete!")
        print("File: blog/" + filename)
        print("Title: " + topic["title"])
        print("Keyword: " + topic["keyword"])
        if github_success:
            print("Live at: https://alliance-landing-page.vercel.app/blog/" + filename)
        if sanity_success:
            print("Also live at: alliance-grp.net!")
    print("=" * 50)

if __name__ == "__main__":
    run_blog_writer()