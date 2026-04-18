import subprocess
import anthropic
import os
import requests
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
import random

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

PAGE_TOKEN = os.getenv("FACEBOOK_PAGE_TOKEN")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")

TOPICS = [
    "roofing replacement and why homeowners should not wait",
    "home additions and how they add value to Massachusetts properties",
    "the importance of hiring a licensed and insured contractor",
    "window replacement and energy savings for Cape Cod homeowners",
    "deck building and outdoor living for New England weather",
    "kitchen and bathroom remodeling tips for homeowners",
    "what MBE certification means and why it matters",
    "OSHA 30 certification and job site safety",
    "siding installation and protecting your home",
    "new construction stick frame builds in Eastern Massachusetts",
    "structural repairs and why catching problems early saves money",
    "cleanouts and demolitions for property investors",
    "financing options and how homeowners can start projects now",
    "the Alliance Preferred Project Package and free estimate offer",
    "why fixed price estimates protect homeowners from surprise costs",
]

ARTICLE_TOPICS = [
    "termite damage prevention Massachusetts homes 2026",
    "pest control tips New England homeowners 2026",
    "roof damage warning signs homeowners 2026",
    "energy efficiency upgrades Massachusetts homes 2026",
    "mold prevention tips New England homes 2026",
    "ice dam prevention Massachusetts winter 2026",
    "foundation problems warning signs homeowners 2026",
    "home value increase renovations Massachusetts 2026",
    "Cape Cod housing market trends 2026",
    "Massachusetts homeowner rebate programs 2026",
    "winter weatherproofing New England homes 2026",
    "first time home buyer tips Massachusetts 2026",
    "home inspection red flags buyers 2026",
    "contractor hiring tips Massachusetts homeowners 2026",
    "structural damage warning signs homes 2026",
    "MassSave energy efficiency program homeowners 2026",
    "Massachusetts Clean Energy Center rebates 2026",
    "Mass Housing first time buyer programs 2026",
    "Massachusetts down payment assistance programs 2026",
    "MassWorks infrastructure program 2026",
    "Massachusetts weatherization assistance program 2026",
    "Mass Save heat pump rebates Massachusetts 2026",
    "Massachusetts solar panel incentives homeowners 2026",
    "Massachusetts lead paint removal assistance program 2026",
    "Massachusetts septic system repair loan program 2026",
    "Massachusetts historic preservation grants homeowners 2026",
    "Massachusetts first time homebuyer tax credit 2026",
    "Massachusetts affordable housing programs 2026",
    "Massachusetts CDBG community development grants 2026",
    "Massachusetts home repair assistance low income 2026",
    "Boston neighborhood housing services programs 2026",
    "Massachusetts DPA down payment assistance 2026",
    "Mass Housing partnership programs contractors 2026",
    "Massachusetts energy audit programs free homeowners 2026",
    "Cape Cod housing assistance programs 2026",
]

def post_to_facebook(text):
    url = "https://graph.facebook.com/v18.0/" + PAGE_ID + "/feed"
    payload = {
        "message": text,
        "access_token": PAGE_TOKEN
    }
    response = requests.post(url, data=payload)
    result = response.json()
    if "id" in result:
        print("SUCCESS! Post published!")
        print("Post ID: " + result["id"])
        with open("post_log.txt", "a", encoding="utf-8") as log:
            log.write("\n" + str(datetime.now()) + "\n")
            log.write("Post ID: " + result["id"] + "\n")
            log.write("Content: " + text + "\n")
            log.write("-" * 50 + "\n")
        return True
    else:
        print("Error: " + str(result))
        return False

def create_and_post():
    print("\n" + str(datetime.now()) + " - Creating regular post...")
    topic = random.choice(TOPICS)
    print("Topic: " + topic)
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "You are a social media manager for Alliance Group Builders LLC. "
                        "A licensed construction company in Eastern Massachusetts, "
                        "Cape Cod and The Islands. "
                        "Write ONE engaging Facebook post about this topic: " + topic + ". "
                        "Company credentials: "
                        "Licensed and Insured in Massachusetts. "
                        "Unrestricted CSL License CS-119447. "
                        "HIC License 211374. "
                        "OSHA 30 Certified. "
                        "MBE Certified through State of Massachusetts and City of Boston. "
                        "24 plus years of field experience. "
                        "Phone: 877-502-2225. "
                        "Tone: Premium, trustworthy, professional but approachable. "
                        "End with call to action to call 877-502-2225 "
                        "or visit website for free estimate. "
                        "Between 100 and 200 words. "
                        "No emoji or special characters. "
                        "Plain text only. "
                        "Output ONLY the post text nothing else."
                    )
                }
            ]
        )
        post_text = message.content[0].text.strip()
        post_to_facebook(post_text)
    except Exception as e:
        print("Error: " + str(e))

def create_article_post():
    print("\n" + str(datetime.now()) + " - Creating article post...")
    topic = random.choice(ARTICLE_TOPICS)
    print("Searching for articles about: " + topic)
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search"
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Search the web for a recent and relevant article about: " + topic + ". "
                        "Find a high quality article from a reputable source. "
                        "Then write a Facebook post for Alliance Group Builders LLC "
                        "that shares this article with homeowners. "
                        "The post should: "
                        "Start with an attention grabbing insight from the article. "
                        "Explain why this matters for Massachusetts homeowners. "
                        "Connect it naturally to Alliance Group Builders services. "
                        "Include the article link. "
                        "End with a soft call to action. "
                        "Keep it between 100 and 200 words. "
                        "No emoji or special characters. "
                        "Plain text only. "
                        "Format: "
                        "POST TEXT: the full post ready to copy "
                        "ARTICLE LINK: the url "
                    )
                }
            ]
        )

        response_text = ""
        article_link = ""

        for block in message.content:
            if hasattr(block, "text"):
                response_text = block.text

        if "POST TEXT:" in response_text:
            post_part = response_text.split("POST TEXT:")[1]
            if "ARTICLE LINK:" in post_part:
                post_text = post_part.split("ARTICLE LINK:")[0].strip()
                article_link = post_part.split("ARTICLE LINK:")[1].strip()
            else:
                post_text = post_part.strip()
        else:
            post_text = response_text.strip()

        if article_link:
            full_post = post_text + "\n\nRead more: " + article_link
        else:
            full_post = post_text

        print("Article post created!")
        post_to_facebook(full_post)

    except Exception as e:
        print("Error: " + str(e))

def run_optimizer():
    print("\nRunning weekly ad optimizer...")
    subprocess.run(["python", "optimizer.py"])

def run_weekly_report():
    print("\nRunning weekly email report...")
    subprocess.run(["python", "weekly_report.py"])

print("AGB Auto Scheduler is running!")
print("Claude will post to Facebook automatically!")
print("Including article posts every Tuesday and Thursday!")
print("------------------------------------------------------")
print("Schedule:")
print("Monday 7am EST - Weekly email report")
print("Monday 8am EST - Ad optimizer runs")
print("Monday 9am and 5pm EST - Regular posts")
print("Tuesday 9am and 5pm EST - Regular posts")
print("Tuesday 10am EST - Article post")
print("Wednesday 9am and 5pm EST - Regular posts")
print("Thursday 9am and 5pm EST - Regular posts")
print("Thursday 10am EST - Article post")
print("Friday 9am and 5pm EST - Regular posts")
print("Saturday 9am EST - Regular post")
print("Sunday 6pm EST - Regular post")
print("------------------------------------------------------")

schedule.every().monday.at("11:00").do(run_weekly_report)
schedule.every().monday.at("12:00").do(run_optimizer)
schedule.every().monday.at("13:00").do(create_and_post)
schedule.every().monday.at("21:00").do(create_and_post)
schedule.every().tuesday.at("13:00").do(create_and_post)
schedule.every().tuesday.at("14:00").do(create_article_post)
schedule.every().tuesday.at("21:00").do(create_and_post)
schedule.every().wednesday.at("13:00").do(create_and_post)
schedule.every().wednesday.at("21:00").do(create_and_post)
schedule.every().thursday.at("13:00").do(create_and_post)
schedule.every().thursday.at("14:00").do(create_article_post)
schedule.every().thursday.at("21:00").do(create_and_post)
schedule.every().friday.at("13:00").do(create_and_post)
schedule.every().friday.at("21:00").do(create_and_post)
schedule.every().saturday.at("13:00").do(create_and_post)
schedule.every().sunday.at("22:00").do(create_and_post)

create_and_post()

while True:
    schedule.run_pending()
    time.sleep(60)