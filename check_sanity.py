import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("SANITY_TOKEN")
project_id = os.getenv("SANITY_PROJECT_ID")

url = "https://" + project_id + ".api.sanity.io/v2021-10-21/data/query/production"
headers = {"Authorization": "Bearer " + token}
params = {"query": '*[_type=="post"]{title, slug, publishedAt}'}

r = requests.get(url, headers=headers, params=params)
data = r.json()

posts = data.get("result", [])
print("Posts in Sanity: " + str(len(posts)))
print()
for post in posts:
    print("Title: " + post.get("title", ""))
    print("Slug: " + str(post.get("slug", {}).get("current", "")))
    print("Published: " + str(post.get("publishedAt", "")))
    print("-" * 30)
    