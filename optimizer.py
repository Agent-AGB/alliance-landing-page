import anthropic
import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

PAGE_TOKEN = os.getenv("FACEBOOK_PAGE_TOKEN")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
AD_ACCOUNT_ID = os.getenv("FACEBOOK_AD_ACCOUNT_ID")

def get_ad_performance():
    print("Reading Facebook ad performance...")
    url = "https://graph.facebook.com/v18.0/act_" + AD_ACCOUNT_ID + "/ads"
    params = {
        "fields": "name,status,insights{impressions,clicks,ctr,spend,actions}",
        "date_preset": "last_7d",
        "access_token": PAGE_TOKEN
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "error" in data:
        print("Error: " + str(data["error"]))
        return []
    ads = []
    for ad in data.get("data", []):
        ad_info = {
            "id": ad.get("id"),
            "name": ad.get("name"),
            "status": ad.get("status"),
            "impressions": 0,
            "clicks": 0,
            "ctr": 0,
            "spend": 0,
            "leads": 0
        }
        insights = ad.get("insights", {}).get("data", [])
        if insights:
            insight = insights[0]
            ad_info["impressions"] = int(insight.get("impressions", 0))
            ad_info["clicks"] = int(insight.get("clicks", 0))
            ad_info["ctr"] = float(insight.get("ctr", 0))
            ad_info["spend"] = float(insight.get("spend", 0))
            for action in insight.get("actions", []):
                if action["action_type"] in ["lead", "complete_registration"]:
                    ad_info["leads"] = int(action.get("value", 0))
        ads.append(ad_info)
        print("Ad: " + ad_info["name"])
        print("  Impressions: " + str(ad_info["impressions"]))
        print("  Clicks: " + str(ad_info["clicks"]))
        print("  CTR: " + str(ad_info["ctr"]) + "%")
        print("  Spend: $" + str(ad_info["spend"]))
        print("  Leads: " + str(ad_info["leads"]))
    return ads

def analyze_performance(ads):
    print("\nClaude is analyzing your ad performance...")
    if not ads:
        print("No ads found!")
        return None
    ads_summary = json.dumps(ads, indent=2)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are an expert Facebook ads analyst for Alliance Group Builders LLC. "
                    "A licensed construction company in Eastern Massachusetts. "
                    "Analyze this Facebook ad performance data from the last 7 days: "
                    + ads_summary +
                    " Provide analysis including: "
                    "1. BEST PERFORMING AD: Which ad has best CTR and leads. "
                    "2. WORST PERFORMING AD: Which ad needs improvement. "
                    "3. KEY INSIGHTS: What patterns do you see. "
                    "4. RECOMMENDATIONS: Specific changes to make. "
                    "5. NEW AD COPY: Write improved version of worst performing ad. "
                    "Include headline max 40 chars and primary text max 150 chars. "
                    "6. BUDGET RECOMMENDATION: Increase decrease or maintain budget. "
                    "Be specific and actionable. Plain text only no special characters."
                )
            }
        ]
    )
    analysis = message.content[0].text.strip()
    print("Analysis complete!")
    return analysis

def save_report(ads, analysis):
    report_date = datetime.now().strftime("%Y-%m-%d")
    filename = "reports/weekly_report_" + report_date + ".txt"
    os.makedirs("reports", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("ALLIANCE GROUP BUILDERS - WEEKLY AD REPORT\n")
        f.write("=" * 50 + "\n")
        f.write("Week ending: " + report_date + "\n\n")
        f.write("RAW AD PERFORMANCE DATA:\n")
        f.write("-" * 30 + "\n")
        for ad in ads:
            f.write("Ad: " + ad["name"] + "\n")
            f.write("Impressions: " + str(ad["impressions"]) + "\n")
            f.write("Clicks: " + str(ad["clicks"]) + "\n")
            f.write("CTR: " + str(ad["ctr"]) + "%\n")
            f.write("Spend: $" + str(ad["spend"]) + "\n")
            f.write("Leads: " + str(ad["leads"]) + "\n\n")
        f.write("\nCLAUDE'S ANALYSIS AND RECOMMENDATIONS:\n")
        f.write("-" * 30 + "\n")
        f.write(analysis)
    print("Report saved to " + filename)
    return filename

def send_email_report(analysis, report_date):
    print("\nGenerating weekly email summary...")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "Write a short friendly email summary of this Facebook ad analysis "
                    "for Jose at Alliance Group Builders. "
                    "Keep it under 200 words. "
                    "Start with a greeting. "
                    "Give the key highlights. "
                    "Tell him what the agent changed automatically. "
                    "Tell him what to expect next week. "
                    "Sign it as: Your AGB Marketing Agent. "
                    "Analysis: " + analysis +
                    " Plain text only. No special characters."
                )
            }
        ]
    )
    email_content = message.content[0].text.strip()
    with open("weekly_email.txt", "w", encoding="utf-8") as f:
        f.write("Subject: AGB Weekly Ad Report - " + report_date + "\n\n")
        f.write(email_content)
    print("Email saved to weekly_email.txt")
    print("\nEmail preview:")
    print("-" * 30)
    print(email_content)

def run_optimizer():
    print("=" * 50)
    print("AGB SELF OPTIMIZING AD AGENT")
    print("=" * 50)
    print("Running analysis for week ending " + datetime.now().strftime("%Y-%m-%d"))
    print()
    ads = get_ad_performance()
    if not ads:
        print("No ad data available yet!")
        print("Run this again after ads have been running for a few days!")
        return
    analysis = analyze_performance(ads)
    if analysis:
        report_date = datetime.now().strftime("%Y-%m-%d")
        save_report(ads, analysis)
        send_email_report(analysis, report_date)
        print("\n" + "=" * 50)
        print("OPTIMIZATION COMPLETE!")
        print("=" * 50)
        print("Check reports folder for full weekly report!")
        print("Check weekly_email.txt for email summary!")

if __name__ == "__main__":
    run_optimizer()