# ============================================
# MAYA - AI Sales Assistant
# Responds to leads automatically
# Has real conversations
# Books phone calls!
# ============================================

import anthropic
import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

QUO_API_KEY = os.getenv("QUO_API_KEY")
QUO_PHONE = os.getenv("QUO_PHONE_NUMBER")

app = Flask(__name__)

# ============================================
# MAYA'S PERSONALITY AND KNOWLEDGE
# ============================================

MAYA_SYSTEM = """
You are Maya, the virtual assistant for 
Alliance Group Builders LLC. You are warm, 
friendly, knowledgeable and professional.

COMPANY INFO:
Name: Alliance Group Builders LLC
Phone: (877) 502-2225
Location: Eastern Massachusetts, Cape Cod 
and The Islands
Credentials: Licensed and Insured, 
Unrestricted CSL CS-119447, HIC 211374,
OSHA 30 Certified, MBE Certified,
24 plus years field experience

SERVICES:
Home Additions, Roof Replacement, Siding,
Windows, Full Remodels, Kitchen and Bath,
Decks, New Construction, Structural Repairs,
Cleanouts and Demolitions

OFFER:
Free consultation, Fixed price estimate,
Priority scheduling, Free upgrade for 
qualified projects, Payment options available

YOUR PERSONALITY:
- Warm and friendly like a helpful neighbor
- Knowledgeable about construction
- Local to Massachusetts
- Confident but never pushy
- Always moving toward booking a call
- Empathetic to homeowner concerns
- Respond in SHORT conversational messages
- Never more than 3-4 sentences per response
- Sound human not robotic

YOUR GOAL:
Have a natural conversation and get them
to agree to a phone call with Jose.
Book a specific time when possible.

COMMON OBJECTIONS AND HOW TO HANDLE:
Price concern: Mention fixed price guarantee
and payment options
Multiple quotes: Emphasize credentials and
fixed price - no surprises
Need to think: Create gentle urgency around
scheduling filling up
Spouse needs to decide: Offer to call when
both are available

NEVER:
- Sound like a robot
- Use bullet points in texts
- Be pushy or aggressive
- Make up prices
- Promise specific timelines
- Use emoji

ALWAYS:
- Use their first name
- Reference their specific project
- Move toward booking a call
- Keep responses short and conversational
"""

# ============================================
# SEND TEXT VIA QUO
# ============================================

def send_text(to_number, message):
    url = "https://api.openphone.com/v1/messages"
    headers = {
        "Authorization":  QUO_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
         "from": QUO_PHONE,
    "to": [to_number],
    "content": message
}
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    print("Text sent: " + str(result))
    return result

# ============================================
# CONVERSATION STORAGE
# ============================================

def load_conversation(phone):
    filename = f"conversations/{phone}.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def save_conversation(phone, messages):
    os.makedirs("conversations", exist_ok=True)
    filename = f"conversations/{phone}.json"
    with open(filename, "w") as f:
        json.dump(messages, f)

# ============================================
# MAYA RESPONDS TO A MESSAGE
# ============================================

def maya_respond(phone, incoming_message, lead_info=None):
    conversation = load_conversation(phone)
    
    if incoming_message:
        conversation.append({
            "role": "user",
            "content": incoming_message
        })
    
    system_prompt = MAYA_SYSTEM
    if lead_info:
        system_prompt += f"""
        
LEAD DETAILS:
Name: {lead_info.get('name', 'Unknown')}
Project: {lead_info.get('project', 'Unknown')}
Timeline: {lead_info.get('timeline', 'Unknown')}
Location: {lead_info.get('location', 'Unknown')}
Message: {lead_info.get('message', 'None')}

Use their name and reference their 
specific project in your response!
"""
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=system_prompt,
        messages=conversation
    )
    
    maya_message = response.content[0].text.strip()
    
    conversation.append({
        "role": "assistant",
        "content": maya_message
    })
    
    save_conversation(phone, conversation)
    
    send_text(phone, maya_message)
    
    with open("maya_log.txt", "a", encoding="utf-8") as log:
        log.write(f"\n{datetime.now()}\n")
        log.write(f"Phone: {phone}\n")
        log.write(f"Incoming: {incoming_message}\n")
        log.write(f"Maya: {maya_message}\n")
        log.write("-" * 50 + "\n")
    
    return maya_message

# ============================================
# NEW LEAD HANDLER
# Called when HubSpot gets a new form submission
# ============================================

def handle_new_lead(lead_data):
    print("New lead received!")
    print(str(lead_data))
    
    name = lead_data.get("name", "")
    first_name = name.split()[0] if name else "there"
    phone = lead_data.get("phone", "")
    project = lead_data.get("project", "")
    timeline = lead_data.get("timeline", "")
    location = lead_data.get("location", "")
    message = lead_data.get("message", "")
    
    if not phone:
        print("No phone number found!")
        return
    
    phone = phone.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    if not phone.startswith("+"):
        phone = "+1" + phone
    
    lead_info = {
        "name": first_name,
        "project": project,
        "timeline": timeline,
        "location": location,
        "message": message
    }
    
    opening_prompt = f"""
    A new lead just came in. Here are their details:
    Name: {first_name}
    Project: {project}
    Timeline: {timeline}
    Location: {location}
    Message: {message}
    
    Send your opening message to {first_name}.
    Be warm, personal and reference their 
    specific project. Keep it to 2-3 sentences.
    End with a question to start the conversation.
    """
    
    conversation = [{
        "role": "user",
        "content": opening_prompt
    }]
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=MAYA_SYSTEM,
        messages=conversation
    )
    
    opening_message = response.content[0].text.strip()
    
    save_conversation(phone, [{
        "role": "assistant",
        "content": opening_message
    }])
    
    send_text(phone, opening_message)
    
    print(f"Opening message sent to {first_name} at {phone}")
    print(f"Message: {opening_message}")

# ============================================
# WEBHOOK ENDPOINTS
# ============================================

@app.route("/new-lead", methods=["POST"])
def new_lead():
    data = request.json
    print("New lead webhook received!")
    print(str(data))
    handle_new_lead(data)
    return jsonify({"status": "success"})

@app.route("/incoming-text", methods=["POST"])
def incoming_text():
    data = request.json
    print("Incoming text received!")
    print(str(data))
    
    phone = data.get("from", "")
    message = data.get("body", "")
    
    if phone and message:
        maya_respond(phone, message)
    
    return jsonify({"status": "success"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Maya is running!"})

# ============================================
# TEST FUNCTION
# ============================================

def test_maya():
    print("Testing Maya with a sample lead...")
    test_lead = {
        "name": "John Smith",
        "phone": "5085551234",
        "project": "Roof Replacement",
        "timeline": "ASAP",
        "location": "Plymouth MA",
        "message": "My roof has been leaking and I need it replaced before summer"
    }
    handle_new_lead(test_lead)
    print("Test complete! Check maya_log.txt for details")

if __name__ == "__main__":
    print("Maya AI Sales Assistant is starting!")
    print("------------------------------------------------------")
    test_maya()
    print("------------------------------------------------------")
    print("Starting webhook server on port 5000...")
    port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=False)