import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("SANITY_TOKEN")
project_id = os.getenv("SANITY_PROJECT_ID")

url = "https://" + project_id + ".api.sanity.io/v2021-10-21/data/query/production"
headers = {"Authorization": "Bearer " + token}
params = {"query": '*[_type=="author"]'}

r = requests.get(url, headers=headers, params=params)
print(r.json())