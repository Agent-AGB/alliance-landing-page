import anthropic
import os
import requests
import json
import base64
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

SERVICE_TOWN_COMBOS = [
    {"service": "Roofing", "town": "Brockton", "state": "MA", "slug": "roofing-brockton-ma"},
    {"service": "Roofing", "town": "Plymouth", "state": "MA", "slug": "roofing-plymouth-ma"},
    {"service": "Roofing", "town": "Falmouth", "state": "MA", "slug": "roofing-falmouth-ma"},
    {"service": "Roofing", "town": "Quincy", "state": "MA", "slug": "roofing-quincy-ma"},
    {"service": "Roofing", "town": "Cape Cod", "state": "MA", "slug": "roofing-cape-cod-ma"},
    {"service": "Roofing", "town": "Norwood", "state": "MA", "slug": "roofing-norwood-ma"},
    {"service": "Roofing", "town": "Marshfield", "state": "MA", "slug": "roofing-marshfield-ma"},
    {"service": "Roofing", "town": "Hingham", "state": "MA", "slug": "roofing-hingham-ma"},
    {"service": "Roofing", "town": "Barnstable", "state": "MA", "slug": "roofing-barnstable-ma"},
    {"service": "Roofing", "town": "Worcester", "state": "MA", "slug": "roofing-worcester-ma"},
    {"service": "Roofing", "town": "Boston", "state": "MA", "slug": "roofing-boston-ma"},
    {"service": "Roofing", "town": "Weymouth", "state": "MA", "slug": "roofing-weymouth-ma"},
    {"service": "Roofing", "town": "Randolph", "state": "MA", "slug": "roofing-randolph-ma"},
    {"service": "Roofing", "town": "Stoughton", "state": "MA", "slug": "roofing-stoughton-ma"},
    {"service": "Roofing", "town": "Easton", "state": "MA", "slug": "roofing-easton-ma"},
    {"service": "Roofing", "town": "Abington", "state": "MA", "slug": "roofing-abington-ma"},
    {"service": "Roofing", "town": "Rockland", "state": "MA", "slug": "roofing-rockland-ma"},
    {"service": "Roofing", "town": "Hanover", "state": "MA", "slug": "roofing-hanover-ma"},
    {"service": "Roofing", "town": "Pembroke", "state": "MA", "slug": "roofing-pembroke-ma"},
    {"service": "Roofing", "town": "Duxbury", "state": "MA", "slug": "roofing-duxbury-ma"},
    {"service": "Roofing", "town": "Kingston", "state": "MA", "slug": "roofing-kingston-ma"},
    {"service": "Roofing", "town": "Wareham", "state": "MA", "slug": "roofing-wareham-ma"},
    {"service": "Roofing", "town": "Sandwich", "state": "MA", "slug": "roofing-sandwich-ma"},
    {"service": "Roofing", "town": "Yarmouth", "state": "MA", "slug": "roofing-yarmouth-ma"},
    {"service": "Roofing", "town": "Dennis", "state": "MA", "slug": "roofing-dennis-ma"},
    {"service": "Roofing", "town": "Harwich", "state": "MA", "slug": "roofing-harwich-ma"},
    {"service": "Roofing", "town": "Chatham", "state": "MA", "slug": "roofing-chatham-ma"},
    {"service": "Roofing", "town": "Orleans", "state": "MA", "slug": "roofing-orleans-ma"},
    {"service": "Roofing", "town": "Brewster", "state": "MA", "slug": "roofing-brewster-ma"},
    {"service": "Roofing", "town": "Eastham", "state": "MA", "slug": "roofing-eastham-ma"},
    {"service": "Home Additions", "town": "Brockton", "state": "MA", "slug": "home-additions-brockton-ma"},
    {"service": "Home Additions", "town": "Plymouth", "state": "MA", "slug": "home-additions-plymouth-ma"},
    {"service": "Home Additions", "town": "Cape Cod", "state": "MA", "slug": "home-additions-cape-cod-ma"},
    {"service": "Home Additions", "town": "Quincy", "state": "MA", "slug": "home-additions-quincy-ma"},
    {"service": "Home Additions", "town": "Norwood", "state": "MA", "slug": "home-additions-norwood-ma"},
    {"service": "Home Additions", "town": "Hingham", "state": "MA", "slug": "home-additions-hingham-ma"},
    {"service": "Home Additions", "town": "Marshfield", "state": "MA", "slug": "home-additions-marshfield-ma"},
    {"service": "Home Additions", "town": "Boston", "state": "MA", "slug": "home-additions-boston-ma"},
    {"service": "Home Additions", "town": "Worcester", "state": "MA", "slug": "home-additions-worcester-ma"},
    {"service": "Home Additions", "town": "Weymouth", "state": "MA", "slug": "home-additions-weymouth-ma"},
    {"service": "Home Additions", "town": "Easton", "state": "MA", "slug": "home-additions-easton-ma"},
    {"service": "Home Additions", "town": "Duxbury", "state": "MA", "slug": "home-additions-duxbury-ma"},
    {"service": "Home Additions", "town": "Yarmouth", "state": "MA", "slug": "home-additions-yarmouth-ma"},
    {"service": "Home Additions", "town": "Barnstable", "state": "MA", "slug": "home-additions-barnstable-ma"},
    {"service": "Home Additions", "town": "Sandwich", "state": "MA", "slug": "home-additions-sandwich-ma"},
    {"service": "Home Additions", "town": "Wareham", "state": "MA", "slug": "home-additions-wareham-ma"},
    {"service": "Siding Installation", "town": "Brockton", "state": "MA", "slug": "siding-brockton-ma"},
    {"service": "Siding Installation", "town": "Plymouth", "state": "MA", "slug": "siding-plymouth-ma"},
    {"service": "Siding Installation", "town": "Cape Cod", "state": "MA", "slug": "siding-cape-cod-ma"},
    {"service": "Siding Installation", "town": "Quincy", "state": "MA", "slug": "siding-quincy-ma"},
    {"service": "Siding Installation", "town": "Norwood", "state": "MA", "slug": "siding-norwood-ma"},
    {"service": "Siding Installation", "town": "Boston", "state": "MA", "slug": "siding-boston-ma"},
    {"service": "Siding Installation", "town": "Worcester", "state": "MA", "slug": "siding-worcester-ma"},
    {"service": "Siding Installation", "town": "Hingham", "state": "MA", "slug": "siding-hingham-ma"},
    {"service": "Siding Installation", "town": "Weymouth", "state": "MA", "slug": "siding-weymouth-ma"},
    {"service": "Siding Installation", "town": "Barnstable", "state": "MA", "slug": "siding-barnstable-ma"},
    {"service": "Siding Installation", "town": "Yarmouth", "state": "MA", "slug": "siding-yarmouth-ma"},
    {"service": "Siding Installation", "town": "Sandwich", "state": "MA", "slug": "siding-sandwich-ma"},
    {"service": "Siding Installation", "town": "Marshfield", "state": "MA", "slug": "siding-marshfield-ma"},
    {"service": "Siding Installation", "town": "Duxbury", "state": "MA", "slug": "siding-duxbury-ma"},
    {"service": "Window Replacement", "town": "Brockton", "state": "MA", "slug": "window-replacement-brockton-ma"},
    {"service": "Window Replacement", "town": "Plymouth", "state": "MA", "slug": "window-replacement-plymouth-ma"},
    {"service": "Window Replacement", "town": "Cape Cod", "state": "MA", "slug": "window-replacement-cape-cod-ma"},
    {"service": "Window Replacement", "town": "Quincy", "state": "MA", "slug": "window-replacement-quincy-ma"},
    {"service": "Window Replacement", "town": "Boston", "state": "MA", "slug": "window-replacement-boston-ma"},
    {"service": "Window Replacement", "town": "Worcester", "state": "MA", "slug": "window-replacement-worcester-ma"},
    {"service": "Window Replacement", "town": "Norwood", "state": "MA", "slug": "window-replacement-norwood-ma"},
    {"service": "Window Replacement", "town": "Hingham", "state": "MA", "slug": "window-replacement-hingham-ma"},
    {"service": "Window Replacement", "town": "Weymouth", "state": "MA", "slug": "window-replacement-weymouth-ma"},
    {"service": "Window Replacement", "town": "Barnstable", "state": "MA", "slug": "window-replacement-barnstable-ma"},
    {"service": "Window Replacement", "town": "Yarmouth", "state": "MA", "slug": "window-replacement-yarmouth-ma"},
    {"service": "Window Replacement", "town": "Sandwich", "state": "MA", "slug": "window-replacement-sandwich-ma"},
    {"service": "Window Replacement", "town": "Easton", "state": "MA", "slug": "window-replacement-easton-ma"},
    {"service": "Window Replacement", "town": "Marshfield", "state": "MA", "slug": "window-replacement-marshfield-ma"},
    {"service": "Deck Builder", "town": "Brockton", "state": "MA", "slug": "deck-builder-brockton-ma"},
    {"service": "Deck Builder", "town": "Plymouth", "state": "MA", "slug": "deck-builder-plymouth-ma"},
    {"service": "Deck Builder", "town": "Cape Cod", "state": "MA", "slug": "deck-builder-cape-cod-ma"},
    {"service": "Deck Builder", "town": "Quincy", "state": "MA", "slug": "deck-builder-quincy-ma"},
    {"service": "Deck Builder", "town": "Norwood", "state": "MA", "slug": "deck-builder-norwood-ma"},
    {"service": "Deck Builder", "town": "Hingham", "state": "MA", "slug": "deck-builder-hingham-ma"},
    {"service": "Deck Builder", "town": "Marshfield", "state": "MA", "slug": "deck-builder-marshfield-ma"},
    {"service": "Deck Builder", "town": "Boston", "state": "MA", "slug": "deck-builder-boston-ma"},
    {"service": "Deck Builder", "town": "Duxbury", "state": "MA", "slug": "deck-builder-duxbury-ma"},
    {"service": "Deck Builder", "town": "Yarmouth", "state": "MA", "slug": "deck-builder-yarmouth-ma"},
    {"service": "Deck Builder", "town": "Barnstable", "state": "MA", "slug": "deck-builder-barnstable-ma"},
    {"service": "Deck Builder", "town": "Sandwich", "state": "MA", "slug": "deck-builder-sandwich-ma"},
    {"service": "Deck Builder", "town": "Weymouth", "state": "MA", "slug": "deck-builder-weymouth-ma"},
    {"service": "Deck Builder", "town": "Easton", "state": "MA", "slug": "deck-builder-easton-ma"},
    {"service": "Kitchen Remodel", "town": "Brockton", "state": "MA", "slug": "kitchen-remodel-brockton-ma"},
    {"service": "Kitchen Remodel", "town": "Cape Cod", "state": "MA", "slug": "kitchen-remodel-cape-cod-ma"},
    {"service": "Kitchen Remodel", "town": "Plymouth", "state": "MA", "slug": "kitchen-remodel-plymouth-ma"},
    {"service": "Kitchen Remodel", "town": "Quincy", "state": "MA", "slug": "kitchen-remodel-quincy-ma"},
    {"service": "Kitchen Remodel", "town": "Boston", "state": "MA", "slug": "kitchen-remodel-boston-ma"},
    {"service": "Kitchen Remodel", "town": "Worcester", "state": "MA", "slug": "kitchen-remodel-worcester-ma"},
    {"service": "Kitchen Remodel", "town": "Norwood", "state": "MA", "slug": "kitchen-remodel-norwood-ma"},
    {"service": "Kitchen Remodel", "town": "Hingham", "state": "MA", "slug": "kitchen-remodel-hingham-ma"},
    {"service": "Kitchen Remodel", "town": "Weymouth", "state": "MA", "slug": "kitchen-remodel-weymouth-ma"},
    {"service": "Kitchen Remodel", "town": "Barnstable", "state": "MA", "slug": "kitchen-remodel-barnstable-ma"},
    {"service": "Kitchen Remodel", "town": "Yarmouth", "state": "MA", "slug": "kitchen-remodel-yarmouth-ma"},
    {"service": "Kitchen Remodel", "town": "Sandwich", "state": "MA", "slug": "kitchen-remodel-sandwich-ma"},
    {"service": "Kitchen Remodel", "town": "Duxbury", "state": "MA", "slug": "kitchen-remodel-duxbury-ma"},
    {"service": "Kitchen Remodel", "town": "Marshfield", "state": "MA", "slug": "kitchen-remodel-marshfield-ma"},
    {"service": "Bathroom Remodel", "town": "Brockton", "state": "MA", "slug": "bathroom-remodel-brockton-ma"},
    {"service": "Bathroom Remodel", "town": "Plymouth", "state": "MA", "slug": "bathroom-remodel-plymouth-ma"},
    {"service": "Bathroom Remodel", "town": "Cape Cod", "state": "MA", "slug": "bathroom-remodel-cape-cod-ma"},
    {"service": "Bathroom Remodel", "town": "Quincy", "state": "MA", "slug": "bathroom-remodel-quincy-ma"},
    {"service": "Bathroom Remodel", "town": "Boston", "state": "MA", "slug": "bathroom-remodel-boston-ma"},
    {"service": "Bathroom Remodel", "town": "Worcester", "state": "MA", "slug": "bathroom-remodel-worcester-ma"},
    {"service": "Bathroom Remodel", "town": "Norwood", "state": "MA", "slug": "bathroom-remodel-norwood-ma"},
    {"service": "Bathroom Remodel", "town": "Hingham", "state": "MA", "slug": "bathroom-remodel-hingham-ma"},
    {"service": "Bathroom Remodel", "town": "Weymouth", "state": "MA", "slug": "bathroom-remodel-weymouth-ma"},
    {"service": "Bathroom Remodel", "town": "Barnstable", "state": "MA", "slug": "bathroom-remodel-barnstable-ma"},
    {"service": "Bathroom Remodel", "town": "Yarmouth", "state": "MA", "slug": "bathroom-remodel-yarmouth-ma"},
    {"service": "Bathroom Remodel", "town": "Sandwich", "state": "MA", "slug": "bathroom-remodel-sandwich-ma"},
    {"service": "Bathroom Remodel", "town": "Duxbury", "state": "MA", "slug": "bathroom-remodel-duxbury-ma"},
    {"service": "Bathroom Remodel", "town": "Marshfield", "state": "MA", "slug": "bathroom-remodel-marshfield-ma"},
    {"service": "Structural Repairs", "town": "Brockton", "state": "MA", "slug": "structural-repairs-brockton-ma"},
    {"service": "Structural Repairs", "town": "Cape Cod", "state": "MA", "slug": "structural-repairs-cape-cod-ma"},
    {"service": "Structural Repairs", "town": "Plymouth", "state": "MA", "slug": "structural-repairs-plymouth-ma"},
    {"service": "Structural Repairs", "town": "Quincy", "state": "MA", "slug": "structural-repairs-quincy-ma"},
    {"service": "Structural Repairs", "town": "Boston", "state": "MA", "slug": "structural-repairs-boston-ma"},
    {"service": "Structural Repairs", "town": "Worcester", "state": "MA", "slug": "structural-repairs-worcester-ma"},
    {"service": "Structural Repairs", "town": "Norwood", "state": "MA", "slug": "structural-repairs-norwood-ma"},
    {"service": "Structural Repairs", "town": "Weymouth", "state": "MA", "slug": "structural-repairs-weymouth-ma"},
    {"service": "Structural Repairs", "town": "Barnstable", "state": "MA", "slug": "structural-repairs-barnstable-ma"},
    {"service": "Structural Repairs", "town": "Yarmouth", "state": "MA", "slug": "structural-repairs-yarmouth-ma"},
    {"service": "New Construction", "town": "Brockton", "state": "MA", "slug": "new-construction-brockton-ma"},
    {"service": "New Construction", "town": "Plymouth", "state": "MA", "slug": "new-construction-plymouth-ma"},
    {"service": "New Construction", "town": "Cape Cod", "state": "MA", "slug": "new-construction-cape-cod-ma"},
    {"service": "New Construction", "town": "Quincy", "state": "MA", "slug": "new-construction-quincy-ma"},
    {"service": "New Construction", "town": "Boston", "state": "MA", "slug": "new-construction-boston-ma"},
    {"service": "New Construction", "town": "Worcester", "state": "MA", "slug": "new-construction-worcester-ma"},
    {"service": "New Construction", "town": "Norwood", "state": "MA", "slug": "new-construction-norwood-ma"},
    {"service": "New Construction", "town": "Easton", "state": "MA", "slug": "new-construction-easton-ma"},
    {"service": "New Construction", "town": "Duxbury", "state": "MA", "slug": "new-construction-duxbury-ma"},
    {"service": "New Construction", "town": "Marshfield", "state": "MA", "slug": "new-construction-marshfield-ma"},
    {"service": "Cleanouts and Demolition", "town": "Brockton", "state": "MA", "slug": "cleanouts-demolition-brockton-ma"},
    {"service": "Cleanouts and Demolition", "town": "Plymouth", "state": "MA", "slug": "cleanouts-demolition-plymouth-ma"},
    {"service": "Cleanouts and Demolition", "town": "Boston", "state": "MA", "slug": "cleanouts-demolition-boston-ma"},
    {"service": "Cleanouts and Demolition", "town": "Worcester", "state": "MA", "slug": "cleanouts-demolition-worcester-ma"},
    {"service": "Cleanouts and Demolition", "town": "Cape Cod", "state": "MA", "slug": "cleanouts-demolition-cape-cod-ma"},
    {"service": "Cleanouts and Demolition", "town": "Quincy", "state": "MA", "slug": "cleanouts-demolition-quincy-ma"},
    {"service": "Cleanouts and Demolition", "town": "Norwood", "state": "MA", "slug": "cleanouts-demolition-norwood-ma"},
    {"service": "Cleanouts and Demolition", "town": "Weymouth", "state": "MA", "slug": "cleanouts-demolition-weymouth-ma"},
    {"service": "Cleanouts and Demolition", "town": "Randolph", "state": "MA", "slug": "cleanouts-demolition-randolph-ma"},
    {"service": "Cleanouts and Demolition", "town": "Stoughton", "state": "MA", "slug": "cleanouts-demolition-stoughton-ma"},
    {"service": "Flooring Installation", "town": "Brockton", "state": "MA", "slug": "flooring-brockton-ma"},
    {"service": "Flooring Installation", "town": "Plymouth", "state": "MA", "slug": "flooring-plymouth-ma"},
    {"service": "Flooring Installation", "town": "Cape Cod", "state": "MA", "slug": "flooring-cape-cod-ma"},
    {"service": "Flooring Installation", "town": "Quincy", "state": "MA", "slug": "flooring-quincy-ma"},
    {"service": "Flooring Installation", "town": "Boston", "state": "MA", "slug": "flooring-boston-ma"},
    {"service": "Flooring Installation", "town": "Worcester", "state": "MA", "slug": "flooring-worcester-ma"},
    {"service": "Flooring Installation", "town": "Norwood", "state": "MA", "slug": "flooring-norwood-ma"},
    {"service": "Flooring Installation", "town": "Hingham", "state": "MA", "slug": "flooring-hingham-ma"},
    {"service": "Flooring Installation", "town": "Weymouth", "state": "MA", "slug": "flooring-weymouth-ma"},
    {"service": "Flooring Installation", "town": "Barnstable", "state": "MA", "slug": "flooring-barnstable-ma"},
    {"service": "Painting", "town": "Brockton", "state": "MA", "slug": "painting-brockton-ma"},
    {"service": "Painting", "town": "Plymouth", "state": "MA", "slug": "painting-plymouth-ma"},
    {"service": "Painting", "town": "Cape Cod", "state": "MA", "slug": "painting-cape-cod-ma"},
    {"service": "Painting", "town": "Quincy", "state": "MA", "slug": "painting-quincy-ma"},
    {"service": "Painting", "town": "Boston", "state": "MA", "slug": "painting-boston-ma"},
    {"service": "Painting", "town": "Worcester", "state": "MA", "slug": "painting-worcester-ma"},
    {"service": "Painting", "town": "Norwood", "state": "MA", "slug": "painting-norwood-ma"},
    {"service": "Painting", "town": "Hingham", "state": "MA", "slug": "painting-hingham-ma"},
    {"service": "Painting", "town": "Weymouth", "state": "MA", "slug": "painting-weymouth-ma"},
    {"service": "Painting", "town": "Barnstable", "state": "MA", "slug": "painting-barnstable-ma"},
    {"service": "Insulation", "town": "Brockton", "state": "MA", "slug": "insulation-brockton-ma"},
    {"service": "Insulation", "town": "Plymouth", "state": "MA", "slug": "insulation-plymouth-ma"},
    {"service": "Insulation", "town": "Cape Cod", "state": "MA", "slug": "insulation-cape-cod-ma"},
    {"service": "Insulation", "town": "Quincy", "state": "MA", "slug": "insulation-quincy-ma"},
    {"service": "Insulation", "town": "Boston", "state": "MA", "slug": "insulation-boston-ma"},
    {"service": "Insulation", "town": "Worcester", "state": "MA", "slug": "insulation-worcester-ma"},
    {"service": "Insulation", "town": "Norwood", "state": "MA", "slug": "insulation-norwood-ma"},
    {"service": "Insulation", "town": "Barnstable", "state": "MA", "slug": "insulation-barnstable-ma"},
    {"service": "Insulation", "town": "Yarmouth", "state": "MA", "slug": "insulation-yarmouth-ma"},
    {"service": "Insulation", "town": "Sandwich", "state": "MA", "slug": "insulation-sandwich-ma"},
    {"service": "Full Home Renovation", "town": "Brockton", "state": "MA", "slug": "full-home-renovation-brockton-ma"},
    {"service": "Full Home Renovation", "town": "Plymouth", "state": "MA", "slug": "full-home-renovation-plymouth-ma"},
    {"service": "Full Home Renovation", "town": "Cape Cod", "state": "MA", "slug": "full-home-renovation-cape-cod-ma"},
    {"service": "Full Home Renovation", "town": "Quincy", "state": "MA", "slug": "full-home-renovation-quincy-ma"},
    {"service": "Full Home Renovation", "town": "Boston", "state": "MA", "slug": "full-home-renovation-boston-ma"},
    {"service": "Full Home Renovation", "town": "Worcester", "state": "MA", "slug": "full-home-renovation-worcester-ma"},
    {"service": "Full Home Renovation", "town": "Norwood", "state": "MA", "slug": "full-home-renovation-norwood-ma"},
    {"service": "Full Home Renovation", "town": "Hingham", "state": "MA", "slug": "full-home-renovation-hingham-ma"},
    {"service": "Full Home Renovation", "town": "Barnstable", "state": "MA", "slug": "full-home-renovation-barnstable-ma"},
    {"service": "Full Home Renovation", "town": "Duxbury", "state": "MA", "slug": "full-home-renovation-duxbury-ma"},
    {"service": "Framing Contractor", "town": "Brockton", "state": "MA", "slug": "framing-contractor-brockton-ma"},
    {"service": "Framing Contractor", "town": "Plymouth", "state": "MA", "slug": "framing-contractor-plymouth-ma"},
    {"service": "Framing Contractor", "town": "Cape Cod", "state": "MA", "slug": "framing-contractor-cape-cod-ma"},
    {"service": "Framing Contractor", "town": "Quincy", "state": "MA", "slug": "framing-contractor-quincy-ma"},
    {"service": "Framing Contractor", "town": "Boston", "state": "MA", "slug": "framing-contractor-boston-ma"},
    {"service": "Framing Contractor", "town": "Worcester", "state": "MA", "slug": "framing-contractor-worcester-ma"},
    {"service": "Framing Contractor", "town": "Norwood", "state": "MA", "slug": "framing-contractor-norwood-ma"},
    {"service": "Framing Contractor", "town": "Barnstable", "state": "MA", "slug": "framing-contractor-barnstable-ma"},
    {"service": "General Contractor", "town": "Brockton", "state": "MA", "slug": "general-contractor-brockton-ma"},
    {"service": "General Contractor", "town": "Plymouth", "state": "MA", "slug": "general-contractor-plymouth-ma"},
    {"service": "General Contractor", "town": "Cape Cod", "state": "MA", "slug": "general-contractor-cape-cod-ma"},
    {"service": "General Contractor", "town": "Quincy", "state": "MA", "slug": "general-contractor-quincy-ma"},
    {"service": "General Contractor", "town": "Boston", "state": "MA", "slug": "general-contractor-boston-ma"},
    {"service": "General Contractor", "town": "Worcester", "state": "MA", "slug": "general-contractor-worcester-ma"},
    {"service": "General Contractor", "town": "Norwood", "state": "MA", "slug": "general-contractor-norwood-ma"},
    {"service": "General Contractor", "town": "Hingham", "state": "MA", "slug": "general-contractor-hingham-ma"},
    {"service": "General Contractor", "town": "Weymouth", "state": "MA", "slug": "general-contractor-weymouth-ma"},
    {"service": "General Contractor", "town": "Barnstable", "state": "MA", "slug": "general-contractor-barnstable-ma"},
    {"service": "General Contractor", "town": "Yarmouth", "state": "MA", "slug": "general-contractor-yarmouth-ma"},
    {"service": "General Contractor", "town": "Sandwich", "state": "MA", "slug": "general-contractor-sandwich-ma"},
    {"service": "General Contractor", "town": "Marshfield", "state": "MA", "slug": "general-contractor-marshfield-ma"},
    {"service": "General Contractor", "town": "Duxbury", "state": "MA", "slug": "general-contractor-duxbury-ma"},
    {"service": "General Contractor", "town": "Easton", "state": "MA", "slug": "general-contractor-easton-ma"},
    {"service": "General Contractor", "town": "Stoughton", "state": "MA", "slug": "general-contractor-stoughton-ma"},
    {"service": "General Contractor", "town": "Randolph", "state": "MA", "slug": "general-contractor-randolph-ma"},
    {"service": "General Contractor", "town": "Abington", "state": "MA", "slug": "general-contractor-abington-ma"},
    {"service": "General Contractor", "town": "Rockland", "state": "MA", "slug": "general-contractor-rockland-ma"},
    {"service": "General Contractor", "town": "Hanover", "state": "MA", "slug": "general-contractor-hanover-ma"},
    {"service": "General Contractor", "town": "Pembroke", "state": "MA", "slug": "general-contractor-pembroke-ma"},
    {"service": "General Contractor", "town": "Kingston", "state": "MA", "slug": "general-contractor-kingston-ma"},
    {"service": "General Contractor", "town": "Wareham", "state": "MA", "slug": "general-contractor-wareham-ma"},
    {"service": "General Contractor", "town": "Bourne", "state": "MA", "slug": "general-contractor-bourne-ma"},
    {"service": "General Contractor", "town": "Mashpee", "state": "MA", "slug": "general-contractor-mashpee-ma"},
    {"service": "General Contractor", "town": "Dennis", "state": "MA", "slug": "general-contractor-dennis-ma"},
    {"service": "General Contractor", "town": "Harwich", "state": "MA", "slug": "general-contractor-harwich-ma"},
    {"service": "General Contractor", "town": "Chatham", "state": "MA", "slug": "general-contractor-chatham-ma"},
    {"service": "General Contractor", "town": "Orleans", "state": "MA", "slug": "general-contractor-orleans-ma"},
    {"service": "General Contractor", "town": "Brewster", "state": "MA", "slug": "general-contractor-brewster-ma"},
    {"service": "General Contractor", "town": "Eastham", "state": "MA", "slug": "general-contractor-eastham-ma"},
    {"service": "General Contractor", "town": "Wellfleet", "state": "MA", "slug": "general-contractor-wellfleet-ma"},
    {"service": "General Contractor", "town": "Truro", "state": "MA", "slug": "general-contractor-truro-ma"},
    {"service": "General Contractor", "town": "Provincetown", "state": "MA", "slug": "general-contractor-provincetown-ma"},
]

def get_next_combo():
    log_file = "service_page_log.json"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            published = json.load(f)
    else:
        published = []
    for combo in SERVICE_TOWN_COMBOS:
        if combo["slug"] not in published:
            return combo
    print("All " + str(len(SERVICE_TOWN_COMBOS)) + " service pages published!")
    print("Add more combos to SERVICE_TOWN_COMBOS to keep going!")
    return None

def mark_published(slug):
    log_file = "service_page_log.json"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            published = json.load(f)
    else:
        published = []
    published.append(slug)
    with open(log_file, "w") as f:
        json.dump(published, f)

def write_service_page(combo):
    service = combo["service"]
    town = combo["town"]
    state = combo["state"]
    print("Writing service page: " + service + " in " + town + " " + state)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are an expert SEO content writer for Alliance Group Builders LLC. "
                    "Write a complete SEO optimized service page for: "
                    + service + " in " + town + " " + state + ". "
                    "Target keyword: " + service + " " + town + " " + state + ". "
                    "Company: Alliance Group Builders LLC. "
                    "Licensed and Insured in Massachusetts. "
                    "Unrestricted CSL License CS-119447. "
                    "HIC License 211374. "
                    "OSHA 30 Certified. "
                    "MBE Certified through State of Massachusetts and City of Boston. "
                    "24 plus years of field experience. "
                    "Phone: 877-502-2225. "
                    "Free consultation and fixed price estimates. "
                    "The page must include: "
                    "1. Strong H1 with service and town name naturally. "
                    "2. Why Alliance Group Builders is the best choice in " + town + ". "
                    "3. Specific details about " + service + " in " + town + " Massachusetts. "
                    "4. Local knowledge about " + town + " building codes or weather. "
                    "5. What the process looks like from start to finish. "
                    "6. Cost information and payment options. "
                    "7. FAQ section with 3 questions specific to " + town + ". "
                    "8. Strong call to action. "
                    "9. Between 800 and 1200 words. "
                    "10. Mention specific neighborhoods or landmarks in " + town + " if possible. "
                    "Write in HTML format using h1 h2 h3 p ul li strong tags only. "
                    "No html head body or doctype tags. "
                    "Plain text only no special characters."
                )
            }
        ]
    )
    return message.content[0].text.strip()

def create_service_html(combo, content):
    service = combo["service"]
    town = combo["town"]
    state = combo["state"]
    title = service + " Contractor " + town + " " + state + " | Alliance Group Builders"
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>""" + title + """</title>
<meta name="description" content="Licensed """ + service + """ contractor serving """ + town + """ MA. Alliance Group Builders LLC - Free estimates, fixed pricing, OSHA 30 certified, MBE certified. Call 877-502-2225.">
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
.hero-phone { color:#C9A84C; font-size:1.2rem; font-weight:800; margin-top:16px; }
.article { max-width:800px; margin:0 auto; padding:60px 40px; }
.article h2 { font-size:1.5rem; font-weight:800; color:#0D0D0D; margin:40px 0 16px; }
.article h3 { font-size:1.1rem; font-weight:700; color:#0D0D0D; margin:24px 0 12px; }
.article p { font-size:1rem; line-height:1.8; color:#333; margin-bottom:16px; }
.article ul { margin:16px 0 16px 24px; }
.article li { font-size:1rem; line-height:1.8; color:#333; margin-bottom:8px; }
.article strong { color:#0D0D0D; font-weight:700; }
.trust-bar { background:#f8f8f6; padding:24px 40px; border-top:2px solid #C9A84C; }
.trust-inner { max-width:800px; margin:0 auto; display:flex; gap:24px; flex-wrap:wrap; }
.trust-item { font-size:0.78rem; font-weight:700; color:#0D0D0D; letter-spacing:0.5px; text-transform:uppercase; }
.cta-box { background:#0D0D0D; padding:48px; margin:48px 0; text-align:center; }
.cta-box h3 { color:#C9A84C; font-size:1.4rem; font-weight:800; margin-bottom:12px; }
.cta-box p { color:rgba(255,255,255,0.7); margin-bottom:24px; font-size:0.95rem; }
.cta-box a { background:#C9A84C; color:#0D0D0D; padding:14px 32px; font-weight:700; text-decoration:none; font-size:0.9rem; letter-spacing:1px; text-transform:uppercase; display:inline-block; }
footer { background:#0a0a0a; padding:32px 40px; text-align:center; color:rgba(255,255,255,0.3); font-size:0.78rem; }
@media(max-width:768px) {
  nav { padding:0 16px; }
  .hero { padding:40px 16px; }
  .hero h1 { font-size:1.6rem; }
  .article { padding:40px 16px; }
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
    <div class="hero-tag">""" + town + """ Massachusetts</div>
    <h1>""" + service + """ Contractor in """ + town + """ """ + state + """</h1>
    <div class="hero-phone">Call Now: (877) 502-2225</div>
  </div>
</div>
<div class="trust-bar">
  <div class="trust-inner">
    <span class="trust-item">Licensed and Insured</span>
    <span class="trust-item">CSL CS-119447</span>
    <span class="trust-item">HIC 211374</span>
    <span class="trust-item">OSHA 30 Certified</span>
    <span class="trust-item">MBE Certified</span>
    <span class="trust-item">Free Estimates</span>
  </div>
</div>
<div class="article">
""" + content + """
<div class="cta-box">
  <h3>Get Your Free """ + service + """ Estimate in """ + town + """</h3>
  <p>Alliance Group Builders LLC serves """ + town + """ and all of Eastern Massachusetts. Licensed, insured and ready to help.</p>
  <a href="../index.html#estimate-form">Get Free Estimate Now</a>
</div>
</div>
<footer>
  Alliance Group Builders LLC - """ + service + """ Contractor """ + town + """ MA - Licensed and Insured - CSL CS-119447 - HIC 211374 - OSHA 30 - MBE Certified - (877) 502-2225
</footer>
</body>
</html>"""
    return html

def save_to_github(filename, content, combo):
    if not GITHUB_TOKEN or not GITHUB_REPO:
        os.makedirs("services", exist_ok=True)
        with open("services/" + filename, "w", encoding="utf-8") as f:
            f.write(content)
        print("Saved locally to services/" + filename)
        return True
    url = "https://api.github.com/repos/" + GITHUB_REPO + "/contents/services/" + filename
    headers = {
        "Authorization": "token " + GITHUB_TOKEN,
        "Content-Type": "application/json"
    }
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    payload = {
        "message": "Add service page: " + combo["service"] + " " + combo["town"],
        "content": encoded
    }
    response = requests.put(url, headers=headers, json=payload)
    result = response.json()
    if "content" in result:
        print("Published to GitHub!")
        print("URL: " + result["content"]["html_url"])
        return True
    else:
        print("GitHub error: " + str(result))
        os.makedirs("services", exist_ok=True)
        with open("services/" + filename, "w", encoding="utf-8") as f:
            f.write(content)
        return False

def run_service_page_writer():
    print("=" * 50)
    print("AGB SERVICE PAGE WRITER")
    print("=" * 50)
    combo = get_next_combo()
    if not combo:
        return
    print("Service: " + combo["service"])
    print("Town: " + combo["town"] + " " + combo["state"])
    print()
    content = write_service_page(combo)
    html = create_service_html(combo, content)
    filename = combo["slug"] + ".html"
    success = save_to_github(filename, html, combo)
    if success:
        mark_published(combo["slug"])
        print("\nService page complete!")
        print("Live at: https://alliance-landing-page.vercel.app/services/" + filename)
    print("=" * 50)

if __name__ == "__main__":
    run_service_page_writer()