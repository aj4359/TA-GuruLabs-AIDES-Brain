"""Read-only discovery triage. Trends are leads, NOT validated demand."""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

FEEDS = {
    "Google Trends UK": "https://trends.google.com/trending/rss?geo=GB",
    "Product Hunt": "https://www.producthunt.com/feed",
}
SENSITIVE = re.compile(r"\b(medicine|medication|diagnos|investment|loan|debt relief|crypto profit|weight loss|prescription|passport|visa|legal advice)\b", re.I)
CATEGORIES = {
    "career": ("cv", "resume", "job", "interview", "career", "recruitment"),
    "productivity": ("document", "template", "planner", "spreadsheet", "organis", "workflow"),
    "creative": ("comic", "music", "game", "art", "animation", "video"),
    "consumer_help": ("budget", "household", "clean", "storage", "phone", "photo"),
}
def classify(title):
    title = title.lower()
    return [k for k, words in CATEGORIES.items() if any(w in title for w in words)]
def triage(title, source, link):
    title = " ".join(title.split())[:160]
    cats = classify(title)
    flagged = bool(SENSITIVE.search(title))
    return {
        "title": title, "source": source, "source_url": link,
        "category_hypotheses": cats, "sensitive_review": flagged,
        "status": "investigate" if cats and not flagged else "manual-review" if flagged else "watch",
        "evidence_level": "trend-mention-only",
        "buyer_demand_verified": False, "product_viability_verified": False,
        "next_check": "Find independent buyer pain, purchase intent, existing competing offers, delivery and platform permissions; do not claim sales potential yet."
    }
def retrieve(url):
    req = urllib.request.Request(url, headers={"User-Agent":"TA-GuruLabs-Retail-Opportunity-Desk/0.1 (public-feed-research)"})
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read(350_000)
def parse_items(xml_bytes):
    root = ET.fromstring(xml_bytes)
    out = []
    for item in root.findall(".//item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        if title and link.startswith("https://"): out.append((title,link))
    ns={"a":"http://www.w3.org/2005/Atom"}
    for entry in root.findall(".//a:entry",ns):
        title=entry.findtext("a:title","",ns).strip()
        links=entry.findall("a:link",ns)
        link=next((x.attrib.get("href","") for x in links if x.attrib.get("rel","alternate")=="alternate"), "")
        if not link and links: link=links[0].attrib.get("href","")
        if title and link.startswith("https://"): out.append((title,link))
    return out
def run(fetch=retrieve):
    results=[]; errors={}
    for source,url in FEEDS.items():
        try:
            seen=set()
            for title,link in parse_items(fetch(url)):
                if link in seen: continue
                seen.add(link)
                results.append(triage(title,source,link))
                if len(seen)>=25: break
        except Exception as ex:
            errors[source]=str(ex)[:300]
    return {"generated_utc":datetime.now(timezone.utc).isoformat(),"mode":"read-only research, no buying/posting","sources":FEEDS,
            "items":results,"source_errors":errors,
            "warning":"Trend mentions are not proof of sales or customer demand. No products, transactions, posts or customers verified."}
if __name__=="__main__":
    report=run()
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path("retail_desk/output/latest.json")
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Saved {len(report['items'])} unverified leads; source errors: {len(report['source_errors'])} -> {path}")
