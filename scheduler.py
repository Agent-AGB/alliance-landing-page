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

def create_and_post():
    print("\n" + str(datetime.now()) + " - Starting auto post...")
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
        url = "https://graph.facebook.com/v18.0/" + PAGE_ID + "/feed"
        payload = {
            "message": post_text,
            "access_token": PAGE_TOKEN
        }
        response = requests.post(url, data=payload)
        result = response.json()
        if "id" in result:
            print("SUCCESS! Post published!")
            print("Post ID: " + result["id"])
            with open("post_log.txt", "a", encoding="utf-8") as log:
                log.write("\n" + str(datetime.now()) + "\n")
                log.write("Topic: " + topic + "\n")
                log.write("Post ID: " + result["id"] + "\n")
                log.write("Content: " + post_text + "\n")
                log.write("-" * 50 + "\n")
        else:
            print("Error: " + str(result))
    except Exception as e:
        print("Error: " + str(e))

print("AGB Auto Scheduler is running!")
print("Claude will post to Facebook automatically!")
print("Press Ctrl+C to stop")
print("------------------------------------------------------")
print("Scheduled posts:")
print("Every day at 9:00 AM")
print("Every day at 5:00 PM")
print("------------------------------------------------------")

schedule.every().day.at("09:00").do(create_and_post)
schedule.every().day.at("17:00").do(create_and_post)

create_and_post()

while True:
    schedule.run_pending()
    time.sleep(60)