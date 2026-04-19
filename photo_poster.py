import anthropic
import os
import requests
import io
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

PAGE_TOKEN = os.getenv("FACEBOOK_PAGE_TOKEN")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")

SCOPES = ["https://www.googleapis.com/auth/drive"]

READY_FOLDER_ID = "1PjBjQmdPMSxa4oF5oMCzoO2hpVx62gJ2"
ARCHIVE_FOLDER_ID = "1Q8bBrEbkp6jC0q8yQy4_VBKkT2YT2r5r"

def get_google_drive_service():
    print("Connecting to Google Drive...")
    creds = None
    if os.path.exists("google_token.json"):
        creds = Credentials.from_authorized_user_file("google_token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "google_credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("google_token.json", "w") as token:
            token.write(creds.to_json())
    service = build("drive", "v3", credentials=creds)
    print("Connected to Google Drive!")
    return service

def get_photos_from_folder(service, folder_id):
    print("Checking for new photos...")
    results = service.files().list(
        q="'" + folder_id + "' in parents and mimeType contains 'image/' and trashed=false",
        fields="files(id, name, mimeType)"
    ).execute()
    return results.get("files", [])

def download_photo(service, file_id, file_name):
    print("Downloading: " + file_name)
    request = service.files().get_media(fileId=file_id)
    file_buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(file_buffer, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    file_buffer.seek(0)
    return file_buffer

def write_caption(file_name):
    print("Claude is writing caption for: " + file_name)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are a social media manager for Alliance Group Builders LLC. "
                    "A licensed construction company in Eastern Massachusetts. "
                    "Write an engaging Facebook caption for a job site photo. "
                    "The photo file name is: " + file_name + ". "
                    "Use the file name as a hint about what the photo might show. "
                    "Company credentials: "
                    "Licensed and Insured in Massachusetts. "
                    "Unrestricted CSL License CS-119447. "
                    "HIC License 211374. "
                    "OSHA 30 Certified. "
                    "MBE Certified State of MA and City of Boston. "
                    "24 plus years field experience. "
                    "Phone: 877-502-2225. "
                    "Caption should: "
                    "Start with something attention grabbing about the work. "
                    "Show pride in craftsmanship and quality. "
                    "Be warm and professional. "
                    "End with call to action to call 877-502-2225 for free estimate. "
                    "Between 50 and 100 words. "
                    "No emoji or special characters. "
                    "Plain text only. "
                    "Output ONLY the caption text nothing else."
                )
            }
        ]
    )
    return message.content[0].text.strip()

def post_photo_to_facebook(photo_buffer, caption, file_name):
    print("Posting photo to Facebook...")
    url = "https://graph.facebook.com/v18.0/" + PAGE_ID + "/photos"
    files = {
        "source": (file_name, photo_buffer, "image/jpeg")
    }
    data = {
        "caption": caption,
        "access_token": PAGE_TOKEN,
        "published": "true"
    }
    response = requests.post(url, files=files, data=data)
    result = response.json()
    print("Facebook response: " + str(result))
    if "id" in result:
        print("Photo posted successfully!")
        print("Post ID: " + result["id"])
        with open("post_log.txt", "a", encoding="utf-8") as log:
            log.write("\n" + str(datetime.now()) + "\n")
            log.write("PHOTO POST\n")
            log.write("File: " + file_name + "\n")
            log.write("Post ID: " + result["id"] + "\n")
            log.write("Caption: " + caption + "\n")
            log.write("-" * 50 + "\n")
        return True
    else:
        print("Error posting photo: " + str(result))
        return False

def move_to_archive(service, file_id, file_name):
    print("Moving " + file_name + " to archive...")
    file = service.files().get(
        fileId=file_id,
        fields="parents"
    ).execute()
    previous_parents = ",".join(file.get("parents"))
    service.files().update(
        fileId=file_id,
        addParents=ARCHIVE_FOLDER_ID,
        removeParents=previous_parents,
        fields="id, parents"
    ).execute()
    print("Moved to archive!")

def run_photo_poster():
    print("=" * 50)
    print("AGB PHOTO POSTER")
    print("=" * 50)
    print("Checking Google Drive for new photos...")
    print()
    service = get_google_drive_service()
    photos = get_photos_from_folder(service, READY_FOLDER_ID)
    if not photos:
        print("No photos found in Photos - Ready to Post folder!")
        print("Upload photos to Google Drive to get started!")
        return
    print("Found " + str(len(photos)) + " photos to post!")
    print()
    photo = photos[0]
    file_name = photo["name"]
    file_id = photo["id"]
    photo_buffer = download_photo(service, file_id, file_name)
    caption = write_caption(file_name)
    print("Caption: " + caption)
    print()
    success = post_photo_to_facebook(photo_buffer, caption, file_name)
    if success:
        move_to_archive(service, file_id, file_name)
        print("\nPhoto posted and archived successfully!")
    print("=" * 50)

if __name__ == "__main__":
    run_photo_poster()