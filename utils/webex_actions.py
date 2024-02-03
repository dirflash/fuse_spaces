import requests

from cards import space_card
from utils import preferences as p

webex_create_room_url = "https://webexapis.com/v1/rooms"
webex_memberships_url = "https://webexapis.com/v1/memberships"
webex_messages_url = "https://webexapis.com/v1/messages"

headers = {
    "Authorization": p.fusebot_help_bearer,
    "Content-Type": "application/json",
}


def make_space(fuse_date, SE1_name, SE2_name):
    room_name = f"Fuse Session ({fuse_date}) - Intro space for {SE1_name} and {SE2_name}"
    room_body = {
        "title": room_name,
        "isLocked": False,
        "description": f"Fuse Session - Intro space for {SE1_name} and {SE2_name}",
    }
    # Create a Webex App room for each pair
    wa_room = requests.post(webex_create_room_url, headers=headers, json=room_body)
    if wa_room.status_code == 200:
        room_id = wa_room.json()["id"]
        print(f"   Room created: {room_name}")
        print(f"    Room ID: {room_id}")
        return room_id
    else:
        print(f"   *** Room creation failed: {wa_room.status_code}")
        print(wa_room.json())


def add_ses_to_room(SE_emails, wa_room):
    # Add SE1 and SE2 to the room
    for x, email in enumerate(SE_emails):
        membership_body = {
            "roomId": wa_room,
            "personEmail": email,
        }
        wa_membership = requests.post(
            webex_memberships_url, headers=headers, json=membership_body
        )
        if wa_membership.status_code == 200:
            print(f"    SE{x + 1} added to room.")
            # print(wa_membership.json())
        else:
            print(f"    SE{x + 1} ({email}) failed to add to room.")
            print(wa_membership.json())


def send_intro_message(wa_room):
    intro_card = space_card.space_card(p.intro_message_1, p.intro_message_2)
    # Send intro message to the room
    intro_message_body = {
        "roomId": wa_room,
        "markdown": p.intro_message_1,
        "attachments": intro_card,
    }
    wa_intro_message = requests.post(
        webex_messages_url, headers=headers, json=intro_message_body
    )
    if wa_intro_message.status_code == 200:
        print(f"    Intro message sent ({wa_intro_message.status_code})")
        print(f"     Message ID: {wa_intro_message.json()['id']}")
    else:
        print(f"    *** Intro message failed ({wa_intro_message.status_code})")
        print(wa_intro_message.json())


def send_follow_up_message(wa_room):
    # Send follow-up message to the room
    wa_follow_up_message = requests.post(
        webex_messages_url,
        headers=headers,
        json={"roomId": wa_room, "markdown": p.follow_up_message},
    )
    if wa_follow_up_message.status_code == 200:
        print(f"    Follow-up message sent ({wa_follow_up_message.status_code})")
        print(f"     Message ID: {wa_follow_up_message.json()['id']}")
        print("   Setup complete.")
    else:
        print(f"  *** Follow-up message failed ({wa_follow_up_message.status_code})")
        print(wa_follow_up_message.json())


def get_room_details(room_id):
    # Get room details
    webex_room_details_url = f"https://webexapis.com/v1/rooms/{room_id}"
    wa_room_details = requests.get(webex_room_details_url, headers=headers)  # noqa: F841
