# ============================================
# AGB WEEKLY EMAIL REPORT
# Sends a full summary every Monday morning
# ============================================

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
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
REPORT_EMAIL = os.getenv("REPORT_EMAIL")

# ============================================
# GET FACEBOOK PAGE STATS
# ============================================

def get_page_stats():
    print("Getting Facebook page stats...")
    url = "https://graph.facebook.com/v18.0/" + PAGE_ID + "/insights"
    params = {
        "metric": "page_impressions,page_reach,page_engaged_users,page_fans",
        "period": "week",
        "access_token": PAGE_TOKEN
    }
    response = requests.get(url, params=params)
    data = response.json()
    stats = {}
    if "data" in data:
        for item in data["data"]:
            stats[item["name"]] = item["values"][-1]["value"] if item["values"] else 0
    return stats

# ============================================
# GET AD PERFORMANCE
# ============================================

def get_ad_stats():
    print("Getting ad performance...")
    url = "https://graph.facebook.com/v18.0/act_" + AD_ACCOUNT_ID + "/insights"
    params = {
        "fields": "impressions,clicks,ctr,spend,actions",
        "date_preset": "last_7d",
        "access_token": PAGE_TOKEN
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "data" in data and data["data"]:
        insight = data["data"][0]
        leads = 0
        for action in insight.get("actions", []):
            if action["action_type"] in ["lead", "complete_registration"]:
                leads = int(action.get("value", 0))
        return {
            "impressions": insight.get("impressions", 0),
            "clicks": insight.get("clicks", 0),
            "ctr": insight.get("ctr", 0),
            "spend": insight.get("spend", 0),
            "leads": leads
        }
    return {
        "impressions": 0,
        "clicks": 0,
        "ctr": 0,
        "spend": 0,
        "leads": 0
    }

# ============================================
# GET POSTS FROM LOG
# ============================================

def get_posts_this_week():
    print("Reading post log...")
    posts = []
    if os.path.exists("post_log.txt"):
        with open("post_log.txt", "r", encoding="utf-8") as f:
            content = f.read()
        week_ago = datetime.now() - timedelta(days=7)
        lines = content.split("\n")
        for line in lines:
            try:
                if "2026" in line or "2025" in line:
                    posts.append(line.strip())
            except:
                pass
    return len(posts)

# ============================================
# GENERATE REPORT WITH CLAUDE
# ============================================

def generate_report(page_stats, ad_stats, posts_count):
    print("Claude is generating your weekly report...")
    
    report_data = (
        "Facebook Page Stats This Week: " + str(page_stats) + ". "
        "Facebook Ad Performance: " + str(ad_stats) + ". "
        "Number of posts published this week: " + str(posts_count) + ". "
    )
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are the AI marketing agent for Alliance Group Builders LLC. "
                    "Write a friendly professional weekly report email for Jose. "
                    "Use this data from the past week: " + report_data +
                    "The email should include: "
                    "1. FRIENDLY GREETING and week summary "
                    "2. FACEBOOK PAGE PERFORMANCE "
                    "   - Page reach and impressions "
                    "   - Engagement numbers "
                    "   - Follower growth "
                    "3. FACEBOOK AD PERFORMANCE "
                    "   - Impressions and clicks "
                    "   - Click through rate "
                    "   - Money spent "
                    "   - Leads generated "
                    "   - Cost per lead "
                    "4. CONTENT PUBLISHED "
                    "   - How many posts went out "
                    "   - Types of content "
                    "5. WINS THIS WEEK "
                    "   - What performed best "
                    "   - Any milestones reached "
                    "6. ACTION ITEMS FOR NEXT WEEK "
                    "   - Specific recommendations "
                    "   - What to watch for "
                    "7. MOTIVATIONAL CLOSING "
                    "Keep it friendly, clear and actionable. "
                    "Sign it as: Your AGB AI Marketing Agent. "
                    "Plain text only. No special characters."
                )
            }
        ]
    )
    
    return message.content[0].text.strip()

# ============================================
# SEND EMAIL VIA RESEND
# ============================================

def send_email(report_content):
    print("Sending weekly report email...")
    
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": "Bearer " + RESEND_API_KEY,
        "Content-Type": "application/json"
    }
    
    week_ending = datetime.now().strftime("%B %d %Y")
    
    payload = {
        "from": "AGB Marketing Agent <onboarding@resend.dev>",
        "to": [REPORT_EMAIL],
        "subject": "AGB Weekly Marketing Report - Week Ending " + week_ending,
        "text": report_content
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if "id" in result:
        print("Email sent successfully!")
        print("Email ID: " + result["id"])
    else:
        print("Email error: " + str(result))
        print("Report saved locally instead!")
        with open("weekly_report.txt", "w", encoding="utf-8") as f:
            f.write("WEEKLY REPORT - " + week_ending + "\n\n")
            f.write(report_content)
        print("Check weekly_report.txt!")

# ============================================
# MAIN FUNCTION
# ============================================

def run_weekly_report():
    print("=" * 50)
    print("AGB WEEKLY REPORT GENERATOR")
    print("=" * 50)
    print("Generating report for week ending " + datetime.now().strftime("%B %d %Y"))
    print()
    
    page_stats = get_page_stats()
    ad_stats = get_ad_stats()
    posts_count = get_posts_this_week()
    
    report = generate_report(page_stats, ad_stats, posts_count)
    
    with open("weekly_report.txt", "w", encoding="utf-8") as f:
        f.write("WEEKLY REPORT - " + datetime.now().strftime("%B %d %Y") + "\n\n")
        f.write(report)
    
    print("\nReport preview:")
    print("-" * 30)
    print(report[:500] + "...")
    
    if RESEND_API_KEY:
        send_email(report)
    else:
        print("\nNo email API key found!")
        print("Report saved to weekly_report.txt")
        print("Add RESEND_API_KEY to .env to get email delivery!")

if __name__ == "__main__":
    run_weekly_report()